# Ma classe

<!-- assistant-ce1-ce2:debut v2 — partie tenue à jour par l'assistant : ne la modifiez pas, demandez « mets à jour mon espace de travail ». Écrivez vos consignes plus bas, dans « Mes consignes ». -->
Ce dossier est l'espace de travail d'un·e professeur·e des écoles de CE1, CE2 ou CE1-CE2. Les skills du plugin **assistant-ce1-ce2** disent comment préparer la classe ; ce fichier dit où ranger ce qui est produit et ce qu'il faut retenir. Les chemins partent de ce dossier. Fichiers en UTF-8 (sous Windows PowerShell : `Get-Content -Encoding UTF8`).

## Avant de produire

- Lis `data/classe.yaml` s'il existe, une fois par session : niveaux, zone, jours et créneaux imposés, sons étudiés en CE1, lexique de la classe, méthode de soustraction posée, préférences, élèves (codes) et leurs adaptations, progression. Ces infos remplacent les hypothèses par défaut des skills.
- Si la demande touche une matière qui a une séquence `en_cours` dans `data/sequences/`, lis-la et demande une seule fois par session où elle en est (« La séquence *la phrase* (CE2) en est à la séance 2 sur 5. Terminée, on continue, ou on arrête ? »). Pour une journée ou une semaine, une seule question groupée. Ne coche jamais une séance toi-même : produire n'est pas faire.
- Regarde le journal du mois (`data/journal/`) pour éviter les doublons (« Tu as déjà une fiche sur a/à du 12 septembre, je repars d'elle ? »).

## Où ranger

- Les documents (PDF…) dans `sorties/`, leurs sources HTML et leurs aperçus dans `sorties/src/`.
- Une séquence planifiée : `data/sequences/<P>_<matière>_<domaine>_<titre-court>.md`, statut `prevue`.
- Formats de `data/` (journal, séquence, `classe.yaml`, suivi) : `data/FORMATS.md`, à lire avant d'écrire pour la première fois un fichier d'un type.
- Rien dans les dossiers du plugin.

## Après chaque production : le journal

Ajoute une entrée à `data/journal/AAAA-MM.md` (mois en cours) une fois les fichiers créés, et aussi quand le contenu est seulement dans la réponse. Sans demander ni en parler, en ajout seulement, sans statut :

```markdown
## 2026-10-03
- CE2 · Français · Dictée · dictee · « Pluriels en -al/-aux » (contenu dans la réponse, pas de fichier)
- CE1 · Maths · Numération · exercice · « Les nombres jusqu'à 100 »
  sorties/2026-10-03_CE1_maths-numeration_exercice.pdf
  sorties/2026-10-03_CE1_maths-numeration_exercice_corrige.pdf
```

## Mémoire de la classe

- `data/classe.yaml` ne se crée et ne se modifie qu'avec l'accord du prof. Quand il donne une info stable en passant (« mes CE1 utilisent Taoki »), termine par « Je le note pour la suite ? », au plus une fois par session, et montre la ligne écrite.
- Si une de ces infos manque et compte vraiment, demande-la une fois par session : sons étudiés en CE1 (texte que les CE1 lisent seuls), méthode de soustraction posée (séance de soustraction posée), zone (programmation de P3 à P5).
- Séquence terminée : statuts mis à jour dans son fichier, ligne de `progression` de `classe.yaml` réécrite (s'il existe), puis propose la suite.
- « On en est où ? » : `classe.yaml` (progression), en-têtes des séquences `en_cours` et `prevue`, journal des deux derniers mois. Distingue « préparé » (journal) et « fait » (séquences).
- Suivi individuel (`data/suivi/<code>.md`) : seulement si le prof le demande.
- Jamais de nom réel d'élève ni de diagnostic dans ces fichiers : codes (E01…) et adaptations seulement. Relis un fichier de `data/` avant de l'écrire : le prof a pu le modifier.

## Consignes du prof

Les consignes de « Mes consignes » priment sur les réglages par défaut des skills, sauf les règles sur les données personnelles, les droits d'auteur et le programme officiel. Pour en ajouter une (« retiens que… », « à partir de maintenant… ») : relis ce fichier, ajoute une ligne `- …` courte à la fin de « Mes consignes », avec les mots du prof, remplace une consigne contraire au lieu d'en ajouter une, puis montre la ligne. Une info sur la classe va dans `classe.yaml`, pas ici. Ne modifie jamais le reste de ce fichier : pour le mettre à jour, utilise le skill `espace-classe`.
<!-- assistant-ce1-ce2:fin -->

## Mes consignes

<!-- Ce que l'assistant doit toujours faire pour vous, une consigne par ligne (« - Tutoie-moi. »). Écrivez ici vous-même, ou demandez : « Ajoute à mes consignes que… ». -->
