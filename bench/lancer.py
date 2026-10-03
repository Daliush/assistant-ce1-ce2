#!/usr/bin/env python3
"""Benchmark de bout en bout du plugin assistant-ce1-ce2.

Lance chaque scénario de scenarios.json avec `claude -p` (plugin local, modèle
figé), dans un dossier temporaire, puis :
  - vérifie le résultat (fichiers créés ou non, journal, nombre de pages…) ;
  - lit le transcript de la session et dit où l'agent a passé son temps ;
  - écrit un compte rendu dans bench/resultats/.

Usage :
    python bench/lancer.py                         # tous les scénarios, une fois
    python bench/lancer.py fiche-dossier -n 3      # un scénario, trois fois
    python bench/lancer.py --analyser session.jsonl [...]   # analyser des transcripts existants

Attention : chaque scénario est une vraie session Claude (environ 0,50 à 1,50 $
avec Opus) et tourne avec --permission-mode bypassPermissions, dans un dossier
temporaire.
"""
import argparse
import concurrent.futures
import datetime
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ICI = Path(__file__).resolve().parent
DEPOT = ICI.parent
CATEGORIES = ["skills", "lecture", "rédaction", "conversion", "aperçu", "retouche", "mémoire", "autre", "réponse finale"]


# ---------------------------------------------------------------- analyse ----

def dossier_config() -> Path:
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")


def trouver_transcript(session_id: str):
    for f in (dossier_config() / "projects").glob(f"*/{session_id}.jsonl"):
        return f
    return None


def categorie(nom: str, entree: dict, deja_ecrits: set) -> str:
    texte = json.dumps(entree, ensure_ascii=False).replace("\\\\", "/")
    chemin = str(entree.get("file_path") or "").replace("\\", "/")
    commande = str(entree.get("command") or "")
    if nom == "Skill":
        return "skills"
    # Avant « conversion » : .claude/settings.json cite aussi html_vers_pdf.py.
    if re.search(r"(^|/)(data/|AGENTS\.md|CLAUDE\.md|\.claude/settings|\.gitignore)", chemin) or (
            nom in ("Bash", "PowerShell") and re.search(r"data/journal|AGENTS\.md", commande)):
        return "mémoire"
    if "html_vers_pdf" in texte:
        return "conversion"
    if nom == "Read" and chemin.lower().endswith(".png"):
        return "aperçu"
    if nom in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        if chemin in deja_ecrits:
            return "retouche"
        deja_ecrits.add(chemin)
        return "rédaction"
    if nom in ("Read", "Glob", "Grep"):
        return "lecture"
    if nom in ("Bash", "PowerShell"):
        if re.search(r"\.html", commande) and re.search(r"(>|Set-Content|Out-File|write_text|open\()", commande):
            return "rédaction"
        if re.search(r"(^|[;&|]\s*|\s)(cat|sed|head|tail|grep|ls|find|Get-Content|Select-String|type)\b", commande):
            return "lecture"
    return "autre"


def analyser(transcript: Path) -> dict:
    lignes = [json.loads(l) for l in transcript.open(encoding="utf-8") if l.strip()]
    lignes = [l for l in lignes if "timestamp" in l]
    date = lambda t: datetime.datetime.fromisoformat(t.replace("Z", "+00:00"))
    debut, fin = date(lignes[0]["timestamp"]), date(lignes[-1]["timestamp"])
    appels, temps = {}, {c: 0.0 for c in CATEGORIES}
    deja_ecrits, deroule, modeles = set(), [], set()
    compte = {"appels": 0, "conversions": 0, "aperçus": 0, "retouches": 0}
    precedent = debut
    for l in lignes:
        msg = l.get("message") or {}
        if l.get("type") == "assistant":
            modeles.add(msg.get("model"))
            for c in msg.get("content") or []:
                if c.get("type") == "tool_use":
                    cat = categorie(c["name"], c.get("input") or {}, deja_ecrits)
                    appels[c["id"]] = (cat, c["name"], c.get("input") or {}, date(l["timestamp"]))
        elif l.get("type") == "user" and isinstance(msg.get("content"), list):
            for c in msg["content"]:
                if c.get("type") == "tool_result" and c.get("tool_use_id") in appels:
                    cat, nom, entree, t_appel = appels[c["tool_use_id"]]
                    t = date(l["timestamp"])
                    temps[cat] += max((t - precedent).total_seconds(), 0)
                    precedent = max(precedent, t)
                    compte["appels"] += 1
                    compte["conversions"] += cat == "conversion"
                    compte["aperçus"] += cat == "aperçu"
                    compte["retouches"] += cat == "retouche"
                    d = entree.get("file_path") or entree.get("command") or entree.get("skill") or entree.get("pattern") or ""
                    d = re.sub(r"\s+", " ", str(d))
                    deroule.append(f"+{(t_appel - debut).total_seconds():4.0f} s  {cat:<10} {nom:<6} {d[:150]}")
    temps["réponse finale"] += max((fin - precedent).total_seconds(), 0)
    return {"duree": (fin - debut).total_seconds(), "temps": temps, "compte": compte,
            "deroule": deroule, "modeles": sorted(m for m in modeles if m)}


# ----------------------------------------------------------- vérifications ----

def nb_pages(pdf: Path) -> int:
    return len(re.findall(rb"/Type\s*/Page(?![s\w])", pdf.read_bytes()))


def verifier(nom: str, d: Path):
    pdfs = sorted(d.rglob("*.pdf"))
    agents = d / "AGENTS.md"
    if nom == "agents_md":
        return agents.exists(), "AGENTS.md présent" if agents.exists() else "AGENTS.md absent"
    if nom == "agents_md_sans_chemin":
        if not agents.exists():
            return False, "AGENTS.md absent"
        chemin = re.search(r"[A-Za-z]:[\\/]|/(home|Users|tmp)/", agents.read_text(encoding="utf-8"))
        return not chemin, "chemin absolu dans AGENTS.md" if chemin else "pas de chemin absolu"
    if nom == "agents_md_v2":
        texte = agents.read_text(encoding="utf-8") if agents.exists() else ""
        ok = "assistant-ce1-ce2:debut v2" in texte and "assistant-classe" not in texte
        return ok, "AGENTS.md v2" if ok else ("AGENTS.md absent" if not texte else "AGENTS.md pas en v2")
    if nom == "formats_md":
        ok = (d / "data" / "FORMATS.md").exists()
        return ok, "data/FORMATS.md présent" if ok else "data/FORMATS.md absent"
    if nom == "consignes_conservees":
        texte = agents.read_text(encoding="utf-8") if agents.exists() else ""
        ok = "- Tutoie-moi." in texte and "version allégée" in texte
        return ok, "consignes du prof conservées" if ok else "consignes du prof perdues"
    if nom == "journal":
        entrees = [l for f in d.glob("data/journal/*.md") for l in f.read_text(encoding="utf-8").splitlines()
                   if l.startswith("- ")]
        return bool(entrees), f"{len(entrees)} entrée(s) de journal"
    if nom == "pas_de_pdf":
        return not pdfs, f"{len(pdfs)} PDF"
    if nom == "pas_de_dossier_classe":
        crees = [n for n in ("AGENTS.md", "data", ".claude") if (d / n).exists()]
        return not crees, ("créés : " + ", ".join(crees)) if crees else "ni AGENTS.md, ni data/, ni .claude/"
    if nom.startswith("pdf_min:"):
        n = int(nom.split(":")[1])
        return len(pdfs) >= n, f"{len(pdfs)} PDF (au moins {n})"
    if nom.startswith("fiche_eleve_max_pages:"):
        n = int(nom.split(":")[1])
        fiches = [p for p in pdfs if not re.search(r"_(corrige|prep)", p.stem)]
        pages = {p.name: nb_pages(p) for p in fiches}
        ok = bool(fiches) and all(v <= n for v in pages.values())
        return ok, ", ".join(f"{k} : {v} p." for k, v in pages.items()) or "aucune feuille élève"
    return False, f"vérification inconnue : {nom}"


def verifier_frontmatters() -> list:
    """Chaque SKILL.md doit avoir un frontmatter YAML valide, avec name et description."""
    try:
        import yaml
    except ImportError:
        print("(PyYAML absent : frontmatters non vérifiés ; pip install pyyaml)")
        return []
    erreurs = []
    for f in sorted((DEPOT / "skills").glob("*/SKILL.md")):
        m = re.match(r"---\r?\n(.*?)\r?\n---", f.read_text(encoding="utf-8"), re.S)
        try:
            d = yaml.safe_load(m.group(1)) if m else None
            if not isinstance(d, dict) or not d.get("name") or not d.get("description"):
                erreurs.append(f"{f.parent.name} : name ou description manquant")
        except yaml.YAMLError as e:
            erreurs.append(f"{f.parent.name} : {str(e).splitlines()[0]}")
    return erreurs


# -------------------------------------------------------------- lancement ----

def preparer(sc: dict, base: Path, rep: int) -> Path:
    # Mode conversation : un dossier de travail temporaire, comme l'application Claude sans dossier choisi.
    parent = base / ("scratch-workspaces" if sc["mode"] == "conversation" else "classes")
    d = parent / f"{sc['id']}-{rep}"
    if sc.get("fixture"):
        shutil.copytree(ICI / "fixtures" / sc["fixture"], d)
    else:
        d.mkdir(parents=True)
    return d


def lancer_un(sc: dict, d: Path, modele: str, claude: str) -> dict:
    debut = time.monotonic()
    r = subprocess.run(
        [claude, "-p", sc["prompt"], "--plugin-dir", str(DEPOT), "--model", modele,
         "--permission-mode", "bypassPermissions", "--output-format", "json"],
        cwd=d, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800)
    duree = time.monotonic() - debut
    try:
        res = json.loads(r.stdout)
    except json.JSONDecodeError:
        res = {"is_error": True, "result": (r.stdout + r.stderr)[-3000:]}
    out = {"sc": sc, "dossier": d, "duree": duree, "res": res, "analyse": None}
    t = trouver_transcript(res.get("session_id", "")) if res.get("session_id") else None
    if t:
        out["analyse"] = analyser(t)
    out["verifs"] = [(v, *verifier(v, d)) for v in sc.get("verifications", [])]
    return out


def sortie_cmd(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, cwd=DEPOT).stdout.strip()
    except OSError:
        return "?"


def environnement(claude: str) -> dict:
    version = json.loads((DEPOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]
    commit = sortie_cmd(["git", "rev-parse", "--short", "HEAD"])
    sale = bool(sortie_cmd(["git", "status", "--porcelain", "--", "skills", ".claude-plugin"]))
    try:
        import playwright  # noqa: F401
        pw = "oui"
    except Exception:
        pw = "non"
    return {
        "version": version + ("-dev" if sale else ""),
        "commit": commit + (" + modifications non commitées" if sale else ""),
        "claude": sortie_cmd([claude, "--version"]),
        "machine": f"{platform.system()} {platform.release()}, Python {platform.python_version()}, "
                   f"Playwright {pw}, pdftoppm {'oui' if shutil.which('pdftoppm') else 'non'}",
    }


def fmt_s(s: float) -> str:
    return f"{s:.0f} s"


def compte_rendu(resultats, env, modele, horodatage) -> str:
    l = [f"# Benchmark du {horodatage}", "",
         f"- **Plugin** : version {env['version']}, commit {env['commit']}",
         f"- **Modèle demandé** : `{modele}` ; utilisé : " +
         ", ".join(sorted({m for r in resultats if r['analyse'] for m in r['analyse']['modeles']} |
                          {m for r in resultats for m in (r['res'].get('modelUsage') or {})})),
         f"- **Claude Code** : {env['claude']}",
         f"- **Machine** : {env['machine']}",
         f"- Scénarios lancés en parallèle, `--permission-mode bypassPermissions`.", "",
         "## Résultats", "",
         "| Scénario | Durée | Tours | Appels | Conversions | Aperçus | Retouches | Tokens produits | Coût | Vérifications |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for r in resultats:
        a, res = r["analyse"], r["res"]
        tokens = sum((v.get("outputTokens") or 0) for v in (res.get("modelUsage") or {}).values())
        ok = all(v[1] for v in r["verifs"])
        verifs = ("✅" if ok else "❌ " + " ; ".join(f"{v[0]} ({v[2]})" for v in r["verifs"] if not v[1]))
        c = a["compte"] if a else {}
        l.append(f"| {r['nom']} | {fmt_s(r['duree'])} | {res.get('num_turns', '?')} | {c.get('appels', '?')} | "
                 f"{c.get('conversions', '?')} | {c.get('aperçus', '?')} | {c.get('retouches', '?')} | {tokens} | "
                 f"{res.get('total_cost_usd', 0):.2f} $ | {verifs} |")
    l += ["", "## Où part le temps (secondes, d'après le transcript)", "",
          "Chaque appel d'outil compte le temps depuis la fin de l'appel précédent : réflexion et écriture du modèle, puis exécution.", "",
          "| Scénario | " + " | ".join(CATEGORIES) + " |", "|---" * (len(CATEGORIES) + 1) + "|"]
    for r in resultats:
        if r["analyse"]:
            t = r["analyse"]["temps"]
            l.append(f"| {r['nom']} | " + " | ".join(f"{t[c]:.0f}" for c in CATEGORIES) + " |")
    l += ["", "## Détail", ""]
    for r in resultats:
        l += [f"### {r['nom']} — {r['sc']['titre']}", "",
              f"- Demande : « {r['sc']['prompt']} »",
              f"- Dossier : `{r['dossier']}`",
              "- Vérifications : " + " ; ".join(f"{'✅' if v[1] else '❌'} {v[0]} ({v[2]})" for v in r["verifs"]), ""]
        if r["analyse"]:
            l += ["```text", *r["analyse"]["deroule"], "```", ""]
    return "\n".join(l) + "\n"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("scenarios", nargs="*", help="identifiants des scénarios (défaut : tous)")
    p.add_argument("-n", "--repetitions", type=int, default=1)
    p.add_argument("--modele", help="modèle (défaut : celui de scenarios.json)")
    p.add_argument("--paralleles", type=int, default=5)
    p.add_argument("--dossier", type=Path, default=Path.home() / "bench-ce1ce2",
                   help="où créer les dossiers de test (défaut : ~/bench-ce1ce2 ; pas le dossier temporaire du système, que l'assistant refuse à juste titre comme espace de travail)")
    p.add_argument("--analyser", nargs="+", metavar="JSONL", help="analyser des transcripts existants")
    args = p.parse_args()

    if args.analyser:
        for f in args.analyser:
            a = analyser(Path(f))
            print(f"## {Path(f).parent.name[-40:]} — {a['duree']:.0f} s, modèles {a['modeles']}, {a['compte']}")
            print(" | ".join(f"{c} {a['temps'][c]:.0f}" for c in CATEGORIES))
            print("\n".join(a["deroule"]), "\n")
        return 0

    erreurs = verifier_frontmatters()
    if erreurs:
        print("Frontmatter illisible (le skill serait chargé sans description) :")
        for e in erreurs:
            print("  " + e)
        return 2
    conf = json.loads((ICI / "scenarios.json").read_text(encoding="utf-8"))
    modele = args.modele or conf["modele"]
    choisis = [s for s in conf["scenarios"] if not args.scenarios or s["id"] in args.scenarios]
    if not choisis:
        print("Aucun scénario ne correspond.")
        return 2
    claude = shutil.which("claude")
    if not claude:
        print("Commande claude introuvable.")
        return 2
    env = environnement(claude)
    args.dossier.mkdir(parents=True, exist_ok=True)
    base = Path(tempfile.mkdtemp(prefix=datetime.datetime.now().strftime("%Y-%m-%d_%H%M_"), dir=args.dossier))
    taches = [(sc, rep) for sc in choisis for rep in range(1, args.repetitions + 1)]
    print(f"{len(taches)} session(s), modèle {modele}, dossiers dans {base}")
    resultats = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.paralleles) as pool:
        futurs = {pool.submit(lancer_un, sc, preparer(sc, base, rep), modele, claude): (sc, rep) for sc, rep in taches}
        for f in concurrent.futures.as_completed(futurs):
            sc, rep = futurs[f]
            r = f.result()
            r["nom"] = sc["id"] + (f" #{rep}" if args.repetitions > 1 else "")
            ok = all(v[1] for v in r["verifs"])
            print(f"  {r['nom']} : {r['duree']:.0f} s, {'OK' if ok else 'ÉCHEC'}")
            resultats.append(r)
    ordre = {s["id"]: i for i, s in enumerate(choisis)}
    resultats.sort(key=lambda r: (ordre[r["sc"]["id"]], r["nom"]))

    horodatage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    nom = datetime.datetime.now().strftime("%Y-%m-%d_%H%M") + f"_v{env['version']}"
    dossier = ICI / "resultats"
    (dossier / nom).mkdir(parents=True, exist_ok=True)
    for r in resultats:
        (dossier / nom / f"{r['nom'].replace(' #', '-')}.md").write_text(
            str(r["res"].get("result", "")), encoding="utf-8")
    (dossier / f"{nom}.md").write_text(compte_rendu(resultats, env, modele, horodatage), encoding="utf-8")
    print(f"Compte rendu : {dossier / (nom + '.md')} (réponses dans {dossier / nom})")
    return 0 if all(all(v[1] for v in r["verifs"]) for r in resultats) else 1


if __name__ == "__main__":
    sys.exit(main())
