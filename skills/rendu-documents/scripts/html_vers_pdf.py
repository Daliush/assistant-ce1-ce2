#!/usr/bin/env python3
"""Convertit un ou plusieurs fichiers HTML (avec fiche.css) en PDF A4.

Usage :
    python3 html_vers_pdf.py sorties/src/a.html [sorties/src/b.html ...] [--apercu] [--sortie DOSSIER]
    python3 html_vers_pdf.py entree.html sortie.pdf [--apercu]     (ancienne forme, un seul fichier)

Convertis tous les fichiers d'une production en une seule commande : le
navigateur n'est lancé qu'une fois (ou les conversions tournent en parallèle).
Chaque PDF porte le nom de son HTML et va dans DOSSIER (--sortie), sinon dans le
dossier parent de src/ (sorties/src/a.html -> sorties/a.pdf).

Essaie, dans l'ordre :
  1. Playwright + Chromium (pip install playwright ; playwright install chromium)
  2. Un Chromium / Chrome / Edge installé (mode headless --print-to-pdf ;
     le format A4 vient de la règle @page de fiche.css)
  3. WeasyPrint (pip install weasyprint ; sous macOS/Windows il faut aussi Pango)
Si aucun n'est disponible, le script le dit : le prof peut ouvrir le HTML dans
son navigateur et faire « Imprimer > Enregistrer en PDF » (A4, marges par défaut,
graphiques d'arrière-plan cochés).

La feuille de style assets/fiche.css du skill est copiée automatiquement à côté
du HTML (si elle manque ou a changé) : le HTML doit simplement contenir
<link rel="stylesheet" href="fiche.css">. Les pictogrammes de consignes
(<svg class="picto"><use href="#p-entoure"/></svg>) sont ajoutés au HTML s'il
les utilise sans les définir.

Feuille élève qui déborde de peu (dernière page remplie au plus au tiers,
<body> sans classe prof ni adapte) : le script essaie de la faire tenir sur une
page de moins en resserrant les espacements (classes serre-1 à serre-3 de
fiche.css, jamais la taille du texte). Il garde le premier niveau qui marche,
l'écrit dans le HTML et le signale.

--apercu : génère aussi des PNG des 3 premières pages à côté du HTML
(sorties/src/<nom>-1.png…) avec pdftoppm, pour vérifier visuellement la mise en
page, et indique le remplissage de la dernière page.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def via_weasyprint(travaux):
    try:
        from weasyprint import HTML  # type: ignore
    except Exception:
        return set()
    faits = set()
    for src, dst in travaux:
        try:
            HTML(filename=str(src), base_url=str(src.parent)).write_pdf(str(dst))
            faits.add(src)
        except Exception as e:
            print(f"[weasyprint] échec pour {src.name} : {e}", file=sys.stderr)
    return faits


def via_playwright(travaux):
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception:
        return set()
    faits = set()
    try:
        with sync_playwright() as p:
            kwargs = {}
            exe = os.environ.get("CHROMIUM_PATH")
            if exe:
                kwargs["executable_path"] = exe
            browser = p.chromium.launch(**kwargs)
            for src, dst in travaux:
                page = browser.new_page()
                try:
                    page.goto(src.resolve().as_uri())
                    page.wait_for_load_state("networkidle")
                    page.pdf(path=str(dst), format="A4", print_background=True,
                             prefer_css_page_size=True)
                    faits.add(src)
                except Exception as e:
                    print(f"[playwright] échec pour {src.name} : {e}", file=sys.stderr)
                finally:
                    page.close()
            browser.close()
    except Exception as e:  # navigateur absent, etc.
        print(f"[playwright] échec : {e}", file=sys.stderr)
    return faits


def attendre_pdf(dst: Path, delai: float = 20) -> bool:
    """Attend que le PDF existe et ne grossisse plus : Edge rend la main avant de l'écrire."""
    fin = time.monotonic() + delai
    taille = -1
    while time.monotonic() < fin:
        if dst.exists():
            t = dst.stat().st_size
            if t > 0 and t == taille:
                return True
            taille = t
        time.sleep(0.3)
    return False


def trouver_chrome():
    candidats = [
        "chromium", "chromium-browser", "google-chrome", "google-chrome-stable",
        "microsoft-edge", "msedge",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for c in candidats:
        exe = shutil.which(c) or (c if Path(c).exists() else None)
        if exe:
            return exe
    return None


def via_chrome_cli(travaux):
    exe = trouver_chrome()
    if not exe:
        return set()
    faits = set()
    restants = list(travaux)
    # Second essai sans le bac à sable du navigateur : nécessaire quand
    # l'assistant tourne lui-même dans un bac à sable (Codex sous Windows).
    for options in ([], ["--no-sandbox"]):
        lances = []
        for src, dst in restants:
            dst.unlink(missing_ok=True)
            # Profil temporaire : ne touche pas au navigateur ouvert du prof.
            profil = tempfile.mkdtemp(prefix="html_vers_pdf-")
            proc = subprocess.Popen(
                [exe, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                 "--no-first-run", f"--user-data-dir={profil}", *options,
                 f"--print-to-pdf={dst.resolve()}", src.resolve().as_uri()],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            lances.append((src, dst, profil, proc))
        echecs = []
        for src, dst, profil, proc in lances:
            try:
                ok = proc.wait(timeout=120) == 0 and attendre_pdf(dst)
            except subprocess.TimeoutExpired:
                proc.kill()
                ok = False
            shutil.rmtree(profil, ignore_errors=True)
            if ok:
                faits.add(src)
            else:
                echecs.append((src, dst))
        restants = echecs
        if not restants:
            break
    return faits


def nb_pages(dst: Path) -> str:
    if shutil.which("pdfinfo"):
        r = subprocess.run(["pdfinfo", str(dst)], capture_output=True, text=True)
        for l in r.stdout.splitlines():
            if l.startswith("Pages:"):
                return l.split()[-1]
    try:  # sans pdfinfo : compte les objets /Type /Page (PDF de Chrome et WeasyPrint)
        n = len(re.findall(rb"/Type\s*/Page(?![s\w])", dst.read_bytes()))
        return str(n) if n else "?"
    except OSError:
        return "?"


def remplissage(dst: Path, page: int):
    """Part de la hauteur de la page occupée (0 à 1), d'après un rendu en niveaux de gris."""
    if not shutil.which("pdftoppm"):
        return None
    with tempfile.TemporaryDirectory() as tmp:
        prefixe = Path(tmp) / "p"
        subprocess.run(["pdftoppm", "-gray", "-r", "20", "-f", str(page), "-l", str(page),
                        "-singlefile", str(dst), str(prefixe)], capture_output=True)
        f = prefixe.with_suffix(".pgm")
        if not f.exists():
            return None
        data = f.read_bytes()
    champs, pos = [], 0
    while len(champs) < 4:  # en-tête PGM binaire : P5 largeur hauteur max
        m = re.compile(rb"\s*(#[^\n]*\n\s*)*(\S+)").match(data, pos)
        if not m:
            return None
        champs.append(m.group(2))
        pos = m.end()
    if champs[0] != b"P5":
        return None
    largeur, hauteur = int(champs[1]), int(champs[2])
    pixels = data[pos + 1:]
    for y in range(hauteur - 1, -1, -1):
        ligne = pixels[y * largeur:(y + 1) * largeur]
        if ligne and min(ligne) < 160:
            return (y + 1) / hauteur
    return 0.0


def classes_body(src: Path):
    m = re.search(r"<body[^>]*\bclass=\"([^\"]*)\"", src.read_text(encoding="utf-8"))
    return m.group(1).split() if m else []


def avec_serrage(html: str, niveau: int) -> str:
    """Remplace ou ajoute la classe serre-N du <body>."""
    def remplacer(m):
        balise = m.group(0)
        if re.search(r"\bclass=\"", balise):
            balise = re.sub(r"\s*\bserre-\d\b", "", balise)
            return re.sub(r"\bclass=\"", f'class="serre-{niveau} ', balise, count=1)
        return balise[:-1] + f' class="serre-{niveau}">'
    return re.sub(r"<body[^>]*>", remplacer, html, count=1)


def resserrer(travaux, convertir):
    """Essaie de retirer une page aux feuilles élève qui débordent. Renvoie {src: niveau}."""
    gardes = {}
    candidats = []
    for src, dst in travaux:
        classes = classes_body(src)
        pages = nb_pages(dst)
        if "prof" in classes or "adapte" in classes or not pages.isdigit() or int(pages) < 2:
            continue
        r = remplissage(dst, int(pages))
        if r is not None and r > 0.35:  # vraie page de plus : les espacements n'y suffiront pas
            continue
        deja = max([int(c[6:]) for c in classes if re.fullmatch(r"serre-\d", c)] or [0])
        candidats.append((src, dst, int(pages), deja))
    def essayer(liste):
        """liste de (src, dst, pages, niveau) -> {(src, niveau): (essai_src, essai_dst)} réussis."""
        travaux_essai, reussis = [], {}
        for src, dst, _, niveau in liste:
            essai_src = src.with_name(f"{src.stem}.essai{niveau}.html")
            essai_src.write_text(avec_serrage(src.read_text(encoding="utf-8"), niveau), encoding="utf-8")
            travaux_essai.append((essai_src, dst.with_name(f"{dst.stem}.essai{niveau}.pdf")))
        faits = convertir(travaux_essai)
        for (src, _, pages, niveau), (essai_src, essai_dst) in zip(liste, travaux_essai):
            n = nb_pages(essai_dst) if essai_src in faits else "?"
            if n.isdigit() and int(n) < pages:
                reussis[(src, niveau)] = (essai_src, essai_dst)
        return reussis, travaux_essai

    # Un seul essai au niveau maximal : s'il ne gagne pas de page, les autres non plus.
    a_essayer = [(s, d, p, 3) for s, d, p, deja in candidats if deja < 3]
    reussis, fichiers = essayer(a_essayer)
    # Puis un niveau plus doux, s'il suffit.
    plus_doux = [(s, d, p, n) for s, d, p, deja in candidats if (s, 3) in reussis
                 for n in (1, 2) if n > deja]
    r2, f2 = essayer(plus_doux)
    reussis.update(r2)
    fichiers += f2
    for src, dst, _, _ in a_essayer:
        niveaux = sorted(n for (s, n) in reussis if s == src)
        if niveaux:
            essai_src, essai_dst = reussis[(src, niveaux[0])]
            src.write_text(essai_src.read_text(encoding="utf-8"), encoding="utf-8")
            os.replace(essai_dst, dst)
            gardes[src] = niveaux[0]
    for essai_src, essai_dst in fichiers:
        essai_src.unlink(missing_ok=True)
        essai_dst.unlink(missing_ok=True)
    return gardes


def apercu(src: Path, dst: Path) -> None:
    if not shutil.which("pdftoppm"):
        print("  (pdftoppm absent : pas d'aperçu PNG)")
        return
    prefixe = src.parent / dst.stem
    for vieux in prefixe.parent.glob(prefixe.name + "-*.png"):  # aperçus d'un rendu précédent
        vieux.unlink(missing_ok=True)
    subprocess.run(["pdftoppm", "-png", "-r", "60", "-f", "1", "-l", "3",
                    str(dst), str(prefixe)], check=False)
    for f in sorted(prefixe.parent.glob(prefixe.name + "-*.png")):
        print(f"  Aperçu : {f}")


def copier_css(dossier: Path) -> None:
    """Copie la feuille de style du skill à côté du HTML si elle manque ou a changé."""
    css = ASSETS / "fiche.css"
    cible = dossier / "fiche.css"
    if css.exists() and (not cible.exists() or cible.read_bytes() != css.read_bytes()):
        shutil.copyfile(css, cible)
        print(f"Feuille de style mise à jour : {cible}")


def ajouter_pictogrammes(src: Path) -> None:
    """Insère les définitions des pictogrammes si le HTML s'en sert sans les définir."""
    html = src.read_text(encoding="utf-8")
    if 'href="#p-' not in html or 'id="p-' in html:
        return
    defs = (ASSETS / "pictogrammes.svg").read_text(encoding="utf-8")
    html, n = re.subn(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + defs, html, count=1)
    if n:
        src.write_text(html, encoding="utf-8")


def main() -> int:
    try:
        sys.stdout.reconfigure(errors="replace")
        sys.stderr.reconfigure(errors="replace")
    except Exception:
        pass
    argv = sys.argv[1:]
    sortie = None
    if "--sortie" in argv:
        i = argv.index("--sortie")
        if i + 1 >= len(argv):
            print(__doc__)
            return 2
        sortie = Path(argv[i + 1])
        del argv[i:i + 2]
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2

    if len(args) == 2 and args[1].lower().endswith(".pdf"):
        travaux = [(Path(args[0]), Path(args[1]))]
    else:
        travaux = []
        for a in args:
            src = Path(a)
            dossier = sortie or (src.parent.parent if src.parent.name == "src" else src.parent)
            travaux.append((src, dossier / (src.stem + ".pdf")))

    manquants = [str(s) for s, _ in travaux if not s.exists()]
    if manquants:
        print("Fichier introuvable : " + ", ".join(manquants), file=sys.stderr)
        return 2

    for dossier in {s.parent.resolve() for s, _ in travaux}:
        copier_css(dossier)
    for src, dst in travaux:
        ajouter_pictogrammes(src)
        dst.parent.mkdir(parents=True, exist_ok=True)

    def convertir(lot):
        """Convertit un lot avec le premier moteur qui marche. Renvoie {src: moteur}."""
        moteurs, restants = {}, list(lot)
        for moteur in (via_playwright, via_chrome_cli, via_weasyprint):
            if not restants:
                break
            for src in moteur(restants):
                moteurs[src] = moteur.__name__[4:]
            restants = [(s, d) for s, d in restants if s not in moteurs]
        return moteurs

    moteurs = convertir(travaux)
    reussis = [(s, d) for s, d in travaux if s in moteurs]
    serrages = resserrer(reussis, convertir)
    for src, dst in reussis:
        pages = nb_pages(dst)
        ligne = f"PDF créé ({moteurs[src]}) : {dst} — {pages} page(s)"
        if src in serrages:
            ligne += f" ; espacements resserrés (serre-{serrages[src]}) pour gagner une page"
        if "--apercu" in sys.argv and pages.isdigit():
            r = remplissage(dst, int(pages))
            if r is not None:
                ligne += f" ; dernière page remplie à {round(r * 10) * 10} %"
        print(ligne)
        if "--apercu" in sys.argv:
            apercu(src, dst)
    restants = [(s, d) for s, d in travaux if s not in moteurs]

    if restants:
        print("Aucun moteur PDF n'a pu convertir : "
              + ", ".join(s.name for s, _ in restants) + "\n"
              "(WeasyPrint, Playwright ou Chrome/Edge nécessaires). Le HTML reste "
              "utilisable : l'ouvrir dans un navigateur, puis Imprimer > Enregistrer "
              "en PDF (A4, arrière-plans cochés).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
