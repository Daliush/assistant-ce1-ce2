#!/usr/bin/env python3
"""Prépare ou met à jour l'espace de travail d'une classe (plugin assistant-ce1-ce2).

Usage :
    python3 preparer_espace.py [DOSSIER]      (défaut : dossier courant)

Sans jamais écraser le texte du prof :
  - AGENTS.md : créé s'il manque ; sinon seul le bloc du plugin (entre les
    marqueurs assistant-ce1-ce2:debut et :fin) est remplacé, ou inséré après
    le premier titre s'il n'existe pas, et la section « Mes consignes » est
    ajoutée si elle manque ;
  - data/FORMATS.md : tenu par le plugin, remplacé s'il a changé ;
  - data/README.md, .gitignore : créés s'ils manquent, laissés sinon ;
  - .claude/settings.json : créé s'il manque, sinon complété des règles
    d'autorisation qui manquent ;
  - data/journal/, data/sequences/, sorties/src/ : créés s'ils manquent ;
  - CLAUDE.md (Claude Code le lit à la place d'AGENTS.md) : supprimé s'il est
    l'ancien modèle de la version 1.0 ; sinon « @AGENTS.md » est ajouté en
    première ligne et le script le signale.
Affiche ce qui a été créé, mis à jour ou laissé tel quel.
"""
import json
import re
import sys
from pathlib import Path

MODELES = Path(__file__).resolve().parent.parent / "assets" / "modeles"
DEBUT = "<!-- assistant-ce1-ce2:debut"
FIN = "<!-- assistant-ce1-ce2:fin -->"
BLOC = re.compile(re.escape(DEBUT) + r".*?" + re.escape(FIN), re.S)
CLAUDE_V1 = (
    "# Ma classe Ce dossier est l'espace de travail d'un·e professeur·e des écoles (CE1, CE2 ou CE1-CE2), "
    "utilisé avec le plugin **assistant-ce1-ce2**. - Pour toute demande, charge d'abord le skill "
    "`assistant-classe` du plugin, puis suis ses règles. - La mémoire de la classe est dans `data/` "
    "(ce dossier), les fichiers produits dans `sorties/`. Les skills du plugin sont en lecture seule : "
    "n'y écris jamais."
)


def lire(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def ecrire(p: Path, texte: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texte, encoding="utf-8", newline="\n")


def agents(dossier: Path, rapport: list) -> None:
    modele = lire(MODELES / "AGENTS.modele.md")
    bloc = BLOC.search(modele).group(0)
    f = dossier / "AGENTS.md"
    if not f.exists():
        ecrire(f, modele)
        rapport.append("créé : AGENTS.md")
        return
    texte = lire(f)
    if BLOC.search(texte):
        nouveau = BLOC.sub(lambda m: bloc, texte, count=1)
    else:
        m = re.search(r"^# .*$", texte, re.M)
        if m:
            nouveau = texte[:m.end()] + "\n\n" + bloc + "\n" + texte[m.end():]
        else:
            nouveau = bloc + "\n\n" + texte
    if not re.search(r"^## Mes consignes\s*$", nouveau, re.M):
        nouveau = nouveau.rstrip() + "\n\n" + modele[modele.index("## Mes consignes"):]
    if nouveau != texte:
        ecrire(f, nouveau)
        rapport.append("mis à jour : AGENTS.md (partie du plugin ; « Mes consignes » inchangé)")
    else:
        rapport.append("déjà à jour : AGENTS.md")


def copie_si_absent(modele: str, cible: Path, nom: str, rapport: list) -> None:
    if cible.exists():
        rapport.append(f"laissé tel quel : {nom}")
    else:
        ecrire(cible, lire(MODELES / modele))
        rapport.append(f"créé : {nom}")


def formats(dossier: Path, rapport: list) -> None:
    f = dossier / "data" / "FORMATS.md"
    modele = lire(MODELES / "FORMATS.modele.md")
    if f.exists() and lire(f) == modele:
        rapport.append("déjà à jour : data/FORMATS.md")
        return
    rapport.append(("mis à jour : " if f.exists() else "créé : ") + "data/FORMATS.md")
    ecrire(f, modele)


def reglages(dossier: Path, rapport: list) -> None:
    f = dossier / ".claude" / "settings.json"
    modele = json.loads(lire(MODELES / "settings.modele.json"))
    if not f.exists():
        ecrire(f, json.dumps(modele, ensure_ascii=False, indent=2) + "\n")
        rapport.append("créé : .claude/settings.json")
        return
    try:
        actuel = json.loads(lire(f))
    except (json.JSONDecodeError, UnicodeDecodeError):
        rapport.append("à signaler : .claude/settings.json illisible (JSON invalide), laissé tel quel")
        return
    regles = actuel.setdefault("permissions", {}).setdefault("allow", [])
    manquantes = [r for r in modele["permissions"]["allow"] if r not in regles]
    if manquantes:
        regles.extend(manquantes)
        ecrire(f, json.dumps(actuel, ensure_ascii=False, indent=2) + "\n")
        rapport.append(f"mis à jour : .claude/settings.json ({len(manquantes)} autorisation(s) ajoutée(s))")
    else:
        rapport.append("déjà à jour : .claude/settings.json")


def claude_md(dossier: Path, rapport: list) -> None:
    f = dossier / "CLAUDE.md"
    if not f.exists():
        return
    texte = lire(f)
    if " ".join(texte.split()) == CLAUDE_V1:
        f.unlink()
        rapport.append("supprimé : CLAUDE.md (ancien modèle de la version 1.0, remplacé par AGENTS.md)")
    elif re.search(r"^@AGENTS\.md\s*$", texte, re.M):
        rapport.append("laissé tel quel : CLAUDE.md (il importe déjà AGENTS.md)")
    else:
        ecrire(f, "@AGENTS.md\n\n" + texte)
        rapport.append("à signaler : CLAUDE.md contient d'autres consignes ; « @AGENTS.md » ajouté en "
                       "première ligne pour que Claude Code lise aussi AGENTS.md")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    dossier = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not dossier.is_dir():
        print(f"Dossier introuvable : {dossier}")
        return 2
    rapport = []
    agents(dossier, rapport)
    formats(dossier, rapport)
    copie_si_absent("data-README.modele.md", dossier / "data" / "README.md", "data/README.md", rapport)
    copie_si_absent("gitignore.modele", dossier / ".gitignore", ".gitignore", rapport)
    for sous in ("data/journal", "data/sequences", "sorties/src"):
        d = dossier / sous
        if not d.exists():
            d.mkdir(parents=True)
            rapport.append(f"créé : {sous}/")
    claude_md(dossier, rapport)
    try:
        reglages(dossier, rapport)
    except OSError as e:
        rapport.append(f"à signaler : .claude/settings.json non écrit ({e})")
    print(f"Espace de travail : {dossier}")
    print("\n".join("  " + l for l in rapport))
    return 0


if __name__ == "__main__":
    sys.exit(main())
