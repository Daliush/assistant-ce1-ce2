---
name: supports-eleve
description: Concevoir les documents que les élèves de CE1-CE2 ont entre les mains ou sous les yeux — fiche d'exercices, trace écrite (leçon), plan de travail, atelier autonome, fiche de dictée, questionnaire de lecture, évaluation, affichage — avec consignes adaptées, progressivité, différenciation et corrigé. À charger dès qu'un support élève est produit en fichier (le contenu vient des skills de didactique, la mise en fichier de rendu-documents) ; pas pour un contenu court donné dans la réponse.
---

# Supports élève

Ce skill décide **la forme pédagogique** d'un document élève. Le contenu vient de `didactique-francais` / `didactique-maths` (et `programme-cycle2`), la fabrication du fichier de `rendu-documents`.

Gabarits détaillés par type : `references/types-de-supports.md`.

## Règles pour tout support élève

### En-tête
- « Prénom : ________ Date : ________ » ; le titre de la notion ; le niveau (CE1 / CE2) discret en haut à droite.
- En double niveau, **un fichier par niveau** (ne jamais mettre les exercices CE1 et CE2 sur la même feuille, sauf atelier commun).

### Consignes
- **Un seul verbe d'action** par consigne, à l'impératif, en tête : *Lis, Entoure, Souligne, Relie, Complète, Écris, Colorie, Recopie, Range, Calcule, Trace*.
- **Courtes** (une ligne si possible), **numérotées**, en **gras**, avec **un exemple fait** quand la tâche est nouvelle.
- CE1 en début d'année : consignes **déchiffrables** et accompagnées d'un **pictogramme** constant (même picto = même verbe toute l'année) ; elles sont **lues collectivement** avant l'autonomie.
- Lexique de la classe (`classe.yaml` → `lexique`) respecté dans les consignes.

### Contenu
- **Une notion par fiche.** Pas d'exercice qui mobilise une notion non étudiée.
- **Progressivité** : repérer → compléter → transformer → produire. 3 à 5 exercices ; 4 à 8 items chacun.
- **Différenciation sur la même fiche** plutôt que trois fiches : exercices de base pour tous + un exercice **★ défi** (prolongement) en fin de fiche. Pour l'étayage, une **version allégée** `…_allegee.pdf` : **moins de contenu** (moins d'items, mots-étiquettes, phrases à compléter, dictée à trous), même mise en forme que la fiche. Produite si le prof la demande ; sinon proposée en une ligne. Règle valable pour tous les supports, dictées comprises.
- **Place pour répondre** suffisante (lignes d'écriture pour l'écrit, cases pour les calculs, cadre « Mon schéma » pour les problèmes).
- **Autocorrection possible** pour les fiches d'autonomie (fiche réponse séparée, ou réponse vérifiable : puzzle, code couleur).
- **Une page A4** quand c'est possible ; deux maximum. Dimensionne la fiche dès le premier jet (repère d'usage) : en CE1, une page A4 tient environ 5 exercices simples de 4 items ; compte double un exercice avec images, lignage Seyès, cadres de problème ou opérations posées. Une version allégée tient sur une page.
- **Demi-A4** quand la fiche tient sur une demi-page (dictée, petite fiche de réinvestissement, ticket de sortie) : deux exemplaires identiques sur la même feuille, chacun avec son en-tête, séparés par le pointillé de découpe (`.demi-a4`). Le prof photocopie deux fois moins.

### Corrigé et document prof
- **Le corrigé est un fichier séparé** (`…_corrige.pdf`), calculé/vérifié, avec les réponses acceptables.
- L'encadré **« À vérifier »** n'est **jamais** sur la feuille élève : il va dans la réponse au prof et sur la fiche de préparation.

### Accessibilité et adaptations
- Police sans empattement, taille 14 pt minimum pour les CE1, 13 pt pour les CE2 (16 pt pour une adaptation « police agrandie »), interligne 1,5, texte aligné à gauche (jamais justifié), pas d'italique ni de majuscules pour du texte long, espace entre les exercices.
- Adaptations de `classe.yaml` → `eleves[].adaptations` : produire la **version adaptée** en plus, nommée `…_adapte.pdf`, **sans nom d'élève** sur le fichier. C'est **le même contenu** que la fiche, seule la forme change (police 16 pt avec `<body class="adapte">`, lignage agrandi, espacements). Un élève qui a besoin d'une police agrandie fait les mêmes exercices que les autres : ne lui donne pas la version allégée à la place. Si un élève relève des deux, adapte la version allégée (`…_allegee_adapte.pdf`).
- « Consignes lues » ne change pas le document : rappelle-le dans la fiche de préparation (qui lit, à quel moment).
- Noir et blanc : jamais d'information portée uniquement par la couleur (« colorie en rouge » → « colorie », « entoure », « souligne »).

## Ce que tu livres pour un support

Ce skill sert quand le support part en fichier. Un contenu court que le prof dicte ou écrit au tableau (dictée, problème du jour…) va dans la réponse, sans fichier (`assistant-classe` §1).

1. La feuille élève (par niveau).
2. Le corrigé (sauf pour une dictée : son texte, donné dans la réponse, sert de corrigé).
3. Si demandé ou si c'est une séance : la fiche de préparation (`planifier`). Pas de fiche de préparation pour une fiche d'exercices ou une dictée isolées.
4. Version allégée ou adaptée : selon les règles ci-dessus ; sinon, proposée en une ligne.
5. Dans la réponse : en 2-3 lignes ce que contient le support, l'hypothèse faite (période, sons connus…), puis « À vérifier ».
