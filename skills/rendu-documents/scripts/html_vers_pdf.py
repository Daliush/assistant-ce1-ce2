#!/usr/bin/env python3
"""Convertit un fichier HTML (avec fiche.css) en PDF A4.

Usage :
    python3 html_vers_pdf.py entree.html sortie.pdf [--apercu]

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
<link rel="stylesheet" href="fiche.css">.

--apercu : génère aussi des PNG des 3 premières pages dans le dossier src/ voisin
(sorties/src/<nom>-1.png…) avec pdftoppm, pour vérifier visuellement la mise en page.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path


def via_weasyprint(src: Path, dst: Path) -> bool:
    try:
        from weasyprint import HTML  # type: ignore
    except Exception:
        return False
    HTML(filename=str(src), base_url=str(src.parent)).write_pdf(str(dst))
    return True


def via_playwright(src: Path, dst: Path) -> bool:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception:
        return False
    try:
        with sync_playwright() as p:
            kwargs = {}
            exe = os.environ.get("CHROMIUM_PATH")
            if exe:
                kwargs["executable_path"] = exe
            browser = p.chromium.launch(**kwargs)
            page = browser.new_page()
            page.goto(src.resolve().as_uri())
            page.wait_for_load_state("networkidle")
            page.pdf(path=str(dst), format="A4", print_background=True,
                     prefer_css_page_size=True)
            browser.close()
        return True
    except Exception as e:  # navigateur absent, etc.
        print(f"[playwright] échec : {e}", file=sys.stderr)
        return False


def via_chrome_cli(src: Path, dst: Path) -> bool:
    candidats = [
        "chromium", "chromium-browser", "google-chrome", "google-chrome-stable",
        "microsoft-edge",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    for c in candidats:
        exe = shutil.which(c) or (c if Path(c).exists() else None)
        if not exe:
            continue
        r = subprocess.run(
            [exe, "--headless", "--disable-gpu", "--no-pdf-header-footer",
             f"--print-to-pdf={dst}", src.resolve().as_uri()],
            capture_output=True, text=True, timeout=120)
        if r.returncode == 0 and dst.exists():
            return True
    return False


def apercu(dst: Path) -> None:
    if not shutil.which("pdftoppm"):
        print("(pdftoppm absent : pas d'aperçu PNG)")
        return
    dossier = dst.parent / "src"
    dossier.mkdir(exist_ok=True)
    prefixe = dossier / dst.stem
    subprocess.run(["pdftoppm", "-png", "-r", "60", "-f", "1", "-l", "3",
                    str(dst), str(prefixe)], check=False)
    for f in sorted(prefixe.parent.glob(prefixe.name + "-*.png")):
        print(f"Aperçu : {f}")


def nb_pages(dst: Path) -> str:
    if shutil.which("pdfinfo"):
        r = subprocess.run(["pdfinfo", str(dst)], capture_output=True, text=True)
        for l in r.stdout.splitlines():
            if l.startswith("Pages:"):
                return l.split()[-1]
    return "?"


def copier_css(src: Path) -> None:
    """Copie la feuille de style du skill à côté du HTML si elle manque ou a changé."""
    css = Path(__file__).resolve().parent.parent / "assets" / "fiche.css"
    cible = src.parent / "fiche.css"
    if css.exists() and (not cible.exists() or cible.read_bytes() != css.read_bytes()):
        shutil.copyfile(css, cible)
        print(f"Feuille de style mise à jour : {cible}")


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        return 2
    src, dst = Path(args[0]), Path(args[1])
    dst.parent.mkdir(parents=True, exist_ok=True)
    copier_css(src)
    for moteur in (via_playwright, via_chrome_cli, via_weasyprint):
        if moteur(src, dst):
            print(f"PDF créé ({moteur.__name__[4:]}) : {dst} — {nb_pages(dst)} page(s)")
            if "--apercu" in sys.argv:
                apercu(dst)
            return 0
    print("Aucun moteur PDF disponible (WeasyPrint, Playwright ou Chrome).\n"
          f"Le fichier HTML reste utilisable : ouvrir {src} dans un navigateur, "
          "puis Imprimer > Enregistrer en PDF (A4, arrière-plans cochés).",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
