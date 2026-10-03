---
name: rendu-documents
allowed-tools:
  - Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/html_vers_pdf.py *)
  - Bash(python ${CLAUDE_SKILL_DIR}/scripts/html_vers_pdf.py *)
  - Bash(py ${CLAUDE_SKILL_DIR}/scripts/html_vers_pdf.py *)
description: Fabriquer les fichiers à imprimer ou projeter pour la classe — PDF A4 noir et blanc par défaut (HTML + feuille de style fournie, converti par script), diaporama ou document modifiable sur demande — avec nommage dans sorties/ et vérification visuelle avant livraison. À charger dès qu'un fichier doit être créé.
---

# Rendu des documents

**Où** : dans le dossier de sortie que tes consignes indiquent ; à défaut, dans `sorties/` du dossier de travail. Sources HTML et aperçus dans `sorties/src/`. **Jamais dans le dossier de ce skill.** Si le prof ne voit pas ton dossier de travail (conversation sur claude.ai, par exemple), envoie les PDF là où il peut les télécharger avec l'option `--sortie` du script (claude.ai : `--sortie /mnt/user-data/outputs`).

**Ne fabrique un fichier que s'il sert** : un contenu court (dictée, problème du jour, calcul mental, quelques phrases) va dans la réponse, sans PDF, sauf si le prof demande une fiche à imprimer (`programme-cycle2` §1).

## 1. Choisir le format

| Situation | Format |
|---|---|
| Par défaut (fiche élève, corrigé, prep, évaluation, dictée, leçon) | **PDF A4 portrait, noir et blanc** |
| Le prof a une préférence de format | Ce format-là |
| Le prof veut modifier le document lui-même | `.docx` (en plus du PDF, ou à la place s'il le demande) |
| Projection au tableau, séance de découverte collective | `.pptx` ou PDF **paysage** (une idée par page), seulement si demandé ou clairement utile |
| Affichage de classe | PDF A4 ou A3 paysage, gros caractères |

## 2. Nommage

`AAAA-MM-JJ_<niveau>_<matiere>-<domaine>_<type>[_variante].<ext>`

| Élément | Codes |
|---|---|
| Date | date d'utilisation en classe si elle est connue (journée du 8 octobre → `2026-10-08`), sinon date de production |
| Niveau | `CE1`, `CE2`, `CE1-CE2` |
| Matière | `fr`, `maths`, `qlm`, `emc`, `evar`, `lve`, `arts`, `eps`, `multi` (journée, semaine : `AAAA-MM-JJ_CE1-CE2_multi_journee.pdf`) |
| Domaine | mot court sans accent : `lecture`, `ecriture`, `dictee`, `oral`, `vocabulaire`, `grammaire`, `conjugaison`, `orthographe`, `culture`, `poesie`, `numeration`, `calcul`, `problemes`, `fractions`, `grandeurs`, `geometrie`, `donnees`… |
| Type | `cours`, `lecon`, `exercice`, `dictee`, `lecture`, `problemes`, `atelier`, `plan-travail`, `seance-N` (N = numéro dans la séquence) ou `seance`, `sequence`, `programmation`, `journee`, `semaine`, `evaluation`, `affichage`, `etiquettes`, `diaporama` |
| Variante | `_prep`, `_fiche` (feuille élève), `_corrige`, `_lecon`, `_allegee` (moins de contenu), `_adapte` (même contenu, forme adaptée : police agrandie…), `_projection` |

Exemples : `2026-10-01_CE1_fr-grammaire_exercice.pdf`, `2026-10-01_CE1_fr-grammaire_exercice_corrige.pdf`, `2026-10-01_CE1-CE2_fr-grammaire_seance-1_prep.pdf`. Les documents d'une séance de séquence portent tous le type `seance-N` et la variante dit ce que c'est (`…_seance-2_prep.pdf`, `…_CE1_fr-grammaire_seance-2_fiche.pdf`) : deux séances le même jour ne s'écrasent jamais.

Garde les **sources HTML** dans `sorties/src/` (même nom, `.html`), pour pouvoir corriger et régénérer. Les aperçus PNG y vont aussi, jamais à côté des PDF.

## 3. PDF : la chaîne HTML → PDF

Chaque étape se fait **en un seul tour** pour tous les documents de la production (fiche, corrigé, prep…) : c'est ce qui rend la fabrication rapide.

1. Lis le modèle `${CLAUDE_SKILL_DIR}/assets/modele-fiche-eleve.html` (une fois par session), puis écris **tous** les documents dans le même tour (appels d'écriture en parallèle), dans `sorties/src/<nom>.html`, avec `<link rel="stylesheet" href="fiche.css">`. **Ne copie ni la feuille de style ni les définitions des pictogrammes** : le script de l'étape 3 les ajoute. `fiche.css` contient l'en-tête, les pictogrammes de consignes et les composants courants (exercice, consigne numérotée avec pictogramme, exemple, étiquettes, lignage Seyès, lignes, défi ★) ; les autres composants (cadres de problème « Mon schéma / Mon calcul / Ma phrase réponse », opérations posées, texte de lecture numéroté, leçon, demi-A4, tableaux) sont donnés en commentaire à la fin du modèle. N'ouvre pas `fiche.css` : le modèle suffit. **Une seule notion par fiche** : supprime ce qui ne sert pas.
2. Classe du `<body>` : `ce1` (14 pt, défaut), `ce2` (13 pt), `adapte` (16 pt, espacements augmentés), `prof` (prep, corrigé : 11 pt, dense).
3. Convertis **tous les fichiers en une seule commande** (chaque PDF prend le nom de son HTML et va dans `sorties/`) :
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/html_vers_pdf.py sorties/src/A.html sorties/src/B.html --apercu
   ```
   Lance-la depuis le dossier de travail, ou donne des chemins complets. Remplace `${CLAUDE_SKILL_DIR}` par le vrai chemin si ton outil ne l'a pas fait. Sous Windows, `python3` n'existe souvent pas : utilise `python` ou `py`.
   Le script essaie Playwright/Chromium, puis un Chrome/Chromium/Edge installé, puis WeasyPrint, et donne le nombre de pages de chaque PDF. Si rien ne marche, il le dit : livre alors le HTML en expliquant « ouvre-le dans ton navigateur, Imprimer > Enregistrer en PDF, A4, graphiques d'arrière-plan cochés ». **N'improvise pas un autre moteur** (reportlab, script maison) : la mise en page de `fiche.css` serait perdue. Ne laisse dans `sorties/` que les documents et leurs sources (pas de script, pas de profil de navigateur).
4. **Lis le compte rendu du script** : pour chaque PDF, il donne le nombre de pages et le remplissage de la dernière page. Une feuille élève qui déborde de peu est déjà resserrée par le script (espacements seulement, jamais la police) : il le signale, n'y touche plus.
5. **Vérifie visuellement, une seule fois** : l'option `--apercu` crée un PNG des pages (jusqu'à 3) dans `sorties/src/`. Regarde, dans un même tour, la page 1 de chaque **feuille élève** (une par niveau). Pour le corrigé, la prep et les versions allégée ou adaptée, le compte rendu du script suffit. Contrôle : rien de coupé, place suffisante pour écrire, pictogrammes et lignes visibles.
6. **Ne corrige que les vrais défauts** : contenu coupé ou illisible, place insuffisante pour écrire, feuille élève de plus de 2 pages, ou dernière page remplie à 30 % au plus. Retire alors des items (jamais la taille de police, jamais < 14 pt pour les CE1), reconvertis **seulement** les fichiers corrigés, et ne regarde de nouveau que si c'était un défaut visuel. Une fiche d'une page et demie est acceptable : ne la fais pas tenir de force sur une page.

Composants et règles de mise en page :
- **Noir et blanc** : pas d'information portée par la couleur ; gris seulement pour les éléments secondaires.
- **Police** : Andika (conçue pour l'apprentissage de la lecture, a et g « scolaires ») si installée, sinon Luciole, sinon Arial/Liberation Sans. Pas d'écriture cursive imprimée sauf si une police cursive scolaire est installée et que le prof la demande.
- **Lignage** : `.seyes` (style="--n:3" = 3 lignes, carreau de 8 mm) pour l'écriture en cursive ; `.seyes.grand` (carreau de 12 mm, interlignes de 3 mm) pour les élèves qui ont besoin d'un lignage agrandi ; `.lignes` pour des réponses courtes.
- **Figures géométriques et schémas** : SVG en ligne, dimensions en mm si l'élève doit mesurer ; dans « À vérifier », rappelle d'imprimer **à 100 %** (sans « ajuster à la page »).
- **Images** : pas d'images trouvées sur internet (droits) ; dessins simples en SVG, ou cadre « Dessine… » laissé à l'élève.

## 4. Diaporama (.pptx)

- Si un skill `pptx` est disponible dans l'environnement, suis-le. Sinon, `python-pptx` : format 16:9, fond blanc, police sans empattement ≥ 32 pt, une idée par diapositive, peu de texte. **Aucun texte projeté sous 24 pt**, petites aides comprises : ce qui ne se lit pas du fond de la classe va dans les notes de la diapositive.
- Séance de découverte : corpus et questions, la règle n'apparaît qu'en fin (diapositive « Ce qu'on a découvert »).
- Vérifie le rendu (conversion en PDF via LibreOffice si disponible : `soffice --headless --convert-to pdf`, puis aperçu PNG).

## 5. Document modifiable (.docx)

- Si un skill `docx` est disponible, suis-le. Sinon : `pandoc source.html -o sortie.docx` (mise en page simplifiée) ou `python-docx`.
- Préviens en une ligne que la mise en page Word peut différer du PDF.

## 6. Après la création

- Dans la réponse : liste des fichiers créés (chemins), une ligne sur ce qu'ils contiennent, l'encadré « À vérifier ». Ne recopie pas le contenu du PDF dans la réponse, sauf si c'est court (une dictée, un problème du jour).
