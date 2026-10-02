---
name: rendu-documents
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/html_vers_pdf.py *)
description: Fabriquer les fichiers à imprimer ou projeter pour la classe — PDF A4 noir et blanc par défaut (HTML + feuille de style fournie, converti par script), diaporama ou document modifiable sur demande — avec nommage dans sorties/ et vérification visuelle avant livraison. À charger dès qu'un fichier doit être créé.
---

# Rendu des documents

Tous les fichiers produits vont dans `${CLAUDE_PROJECT_DIR}/sorties/` (sources et aperçus dans `sorties/src/`), **jamais dans le dossier de ce skill**.

## 1. Choisir le format

| Situation | Format |
|---|---|
| Par défaut (fiche élève, corrigé, prep, évaluation, dictée, leçon) | **PDF A4 portrait, noir et blanc** |
| `classe.yaml` → `preferences.format` | Ce format-là |
| Le prof veut modifier le document lui-même | `.docx` (en plus du PDF, ou à la place s'il le demande) |
| Projection au tableau, séance de découverte collective | `.pptx` ou PDF **paysage** (une idée par page), seulement si demandé ou clairement utile |
| Affichage de classe | PDF A4 ou A3 paysage, gros caractères |

## 2. Nommage

`sorties/AAAA-MM-JJ_<niveau>_<matiere>-<domaine>_<type>[_variante].<ext>` — **codes, date et variantes : tableau unique dans `${CLAUDE_SKILL_DIR}/../etat-classe/references/formats.md` §0**.

Exemples : `2026-10-01_CE1_fr-grammaire_exercice.pdf`, `2026-10-01_CE1_fr-grammaire_exercice_corrige.pdf`, `2026-10-01_CE1-CE2_fr-grammaire_seance-1_prep.pdf`, `2026-10-08_CE1-CE2_multi_journee.pdf`.

Garde les **sources HTML** dans `sorties/src/` (même nom, `.html`), pour pouvoir corriger et régénérer. Les aperçus PNG y vont aussi.

## 3. PDF : la chaîne HTML → PDF

1. Lis le modèle `${CLAUDE_SKILL_DIR}/assets/modele-fiche-eleve.html` (outil de lecture) et écris ton document dans `${CLAUDE_PROJECT_DIR}/sorties/src/<nom>.html`, avec `<link rel="stylesheet" href="fiche.css">`. **Ne copie pas la feuille de style toi-même** : le script de l'étape 3 la place à côté du HTML et la met à jour : il contient l'en-tête, les pictogrammes de consignes et les composants courants (exercice, consigne numérotée avec pictogramme, exemple, étiquettes, lignage Seyès, lignes, défi ★) ; les autres composants (cadres de problème « Mon schéma / Mon calcul / Ma phrase réponse », texte de lecture numéroté, leçon, demi-A4) sont donnés en commentaire à la fin du modèle. **Une seule notion par fiche** : supprime ce qui ne sert pas.
2. Classe du `<body>` : `ce1` (14 pt, défaut), `ce2` (13 pt), `adapte` (16 pt, espacements augmentés), `prof` (prep, corrigé : 11 pt, dense).
3. Convertis :
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/html_vers_pdf.py ${CLAUDE_PROJECT_DIR}/sorties/src/X.html ${CLAUDE_PROJECT_DIR}/sorties/X.pdf --apercu
   ```
   Le script essaie Playwright/Chromium, puis un Chrome/Chromium/Edge installé, puis WeasyPrint. Si rien ne marche, il le dit : livre alors le HTML en expliquant « ouvre-le dans ton navigateur, Imprimer > Enregistrer en PDF, A4, graphiques d'arrière-plan cochés ».
4. **Vérifie toujours visuellement** : l'option `--apercu` crée un PNG de chaque page (jusqu'à 3) dans `sorties/src/` ; regarde au moins la page 1 (outil de lecture d'image). Contrôle : rien de coupé, pas de page presque vide, place suffisante pour écrire, pictogrammes et lignes visibles, tient sur 1 page si prévu.
5. Si le PDF fait une page de trop, réduis les marges internes ou le nombre d'items plutôt que la taille de police (jamais < 14 pt pour les CE1).

Composants et règles de mise en page :
- **Noir et blanc** : pas d'information portée par la couleur ; gris seulement pour les éléments secondaires.
- **Police** : Andika (conçue pour l'apprentissage de la lecture, a et g « scolaires ») si installée, sinon Luciole, sinon Arial/Liberation Sans. Pas d'écriture cursive imprimée sauf si une police cursive scolaire est installée et que le prof la demande.
- **Lignage** : `.seyes` (style="--n:3" = 3 lignes, carreau de 8 mm) pour l'écriture en cursive ; `.seyes.grand` (carreau de 12 mm, interlignes de 3 mm) pour les élèves qui ont besoin d'un lignage agrandi ; `.lignes` pour des réponses courtes.
- **Figures géométriques et schémas** : SVG en ligne, dimensions en mm si l'élève doit mesurer ; dans « À vérifier », rappelle d'imprimer **à 100 %** (sans « ajuster à la page »).
- **Images** : pas d'images trouvées sur internet (droits) ; dessins simples en SVG, ou cadre « Dessine… » laissé à l'élève.

## 4. Diaporama (.pptx)

- Si un skill `pptx` est disponible dans l'environnement, suis-le. Sinon, `python-pptx` : format 16:9, fond blanc, police sans empattement ≥ 32 pt, une idée par diapositive, peu de texte.
- Séance de découverte : corpus et questions, la règle n'apparaît qu'en fin (diapositive « Ce qu'on a découvert »).
- Vérifie le rendu (conversion en PDF via LibreOffice si disponible : `soffice --headless --convert-to pdf`, puis aperçu PNG).

## 5. Document modifiable (.docx)

- Si un skill `docx` est disponible, suis-le. Sinon : `pandoc source.html -o sortie.docx` (mise en page simplifiée) ou `python-docx`.
- Préviens en une ligne que la mise en page Word peut différer du PDF.

## 6. Après la création

- Ajoute la ligne de journal (skill `etat-classe`).
- Dans la réponse : liste des fichiers créés (chemins), une ligne sur ce qu'ils contiennent, l'encadré « À vérifier ». Ne recopie pas le contenu du PDF dans la réponse, sauf si c'est court (une dictée, un problème du jour).
