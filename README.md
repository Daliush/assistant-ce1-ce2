# Assistant CE1-CE2

Un plugin [Claude Code](https://code.claude.com), qui fonctionne aussi avec [Codex](#utiliser-avec-codex-chatgpt), pour préparer la classe en **CE1, CE2 ou CE1-CE2** : séances, séquences, fiches d'exercices, leçons, dictées, textes de lecture, problèmes, journées, évaluations. Les documents sortent en **PDF A4 imprimables en noir et blanc**, avec leur corrigé et une fiche de préparation.

Il s'appuie sur les **programmes officiels en vigueur en 2026-2027**, relus sur les textes du Bulletin officiel : repères de période, listes fermées (temps, verbes, champ numérique), horaires.

## Ce qu'on peut lui demander

Tout se fait en français, en langage courant :

- « Prépare-moi la première séance de grammaire sur la phrase pour mes CE1 et mes CE2. »
- « Une séance de maths complète pour lundi, pour mes CE1 et mes CE2. »
- « Prépare-moi la séance suivante sur la phrase. »
- « Une dictée pour mes CE2 sur les pluriels en -aux. »
- « 10 problèmes de partage pour mes CE1 cette semaine. »
- « Organise ma journée de jeudi. »
- « J'ai besoin d'un exercice de culture littéraire pour mes CE1. » (il propose plusieurs formats)

### Ce qu'il sait faire

- **Respecter le programme du niveau** : il cite l'objectif officiel visé et respecte les repères de la période en cours. Par exemple, pas de fractions avant la période 2 en CE1, et pas de nombres au-delà de 1 000.
- **Gérer le double niveau** : chaque séance est organisée minute par minute, en indiquant qui est avec le prof et qui travaille en autonomie, avec une activité « j'ai fini » prévue.
- **Écrire des textes adaptés** : textes déchiffrables pour les CE1 selon les sons déjà étudiés, longueurs conformes aux repères, textes originaux ou du domaine public uniquement.
- **Suivre l'avancement** : il retient les séquences en cours, demande où on en est avant de préparer la séance suivante, et tient un journal de tout ce qui a été préparé.
- **Fabriquer les documents** : fiche élève par niveau, corrigé séparé, fiche de préparation, version adaptée si besoin (police agrandie, consignes lues).

## Installation

### 1. Prérequis

- [Claude Code](https://code.claude.com) **2.1.277 ou plus récent** (pour qu'il lise `AGENTS.md`), connecté à un compte Claude : dans un terminal, ou dans l'onglet Code de l'application Claude. Vérifier avec `claude --version`, mettre à jour avec `claude update`. Ou bien Codex : voir [Utiliser avec Codex](#utiliser-avec-codex-chatgpt).
- **Python 3**, pour fabriquer les PDF. Il est déjà là sous macOS et Linux. Sous Windows, installez-le depuis [python.org](https://www.python.org/downloads/) (cochez « Add python.exe to PATH ») ou depuis le Microsoft Store.
- **Google Chrome ou Microsoft Edge** : le script s'en sert pour convertir les fiches en PDF. Sous Windows, Edge est toujours présent : rien à installer. Pour un rendu plus rapide, vous pouvez ajouter Playwright : `pip install playwright` puis `playwright install chromium`.

  Sans Python ni navigateur, l'assistant livre des fichiers HTML à imprimer depuis le navigateur.
- Facultatif :
  - `pip install python-pptx`, pour les diaporamas PowerPoint ;
  - `pdftoppm` (paquet `poppler-utils` ou `poppler`), pour que l'assistant vérifie visuellement ses PDF ;
  - la police gratuite [Andika](https://software.sil.org/andika/), conçue pour l'apprentissage de la lecture.

### 2. Installer le plugin (une fois)

Dans Claude Code :

```
/plugin marketplace add Daliush/assistant-ce1-ce2
/plugin install assistant-ce1-ce2@assistant-ce1-ce2-marketplace
```

Ou depuis un terminal :

```bash
claude plugin marketplace add Daliush/assistant-ce1-ce2
claude plugin install assistant-ce1-ce2@assistant-ce1-ce2-marketplace
```

### 3. Créer le dossier de la classe

Créez un dossier vide où vous voulez, par exemple `classe-2026-2027` (un dossier par classe ou par année), ouvrez-le dans Claude Code et demandez ce dont vous avez besoin. Rien n'est à copier ni à remplir.

```bash
mkdir classe-2026-2027
cd classe-2026-2027
claude
```

Dans l'application Claude, ouvrez simplement ce dossier depuis l'onglet Code.

Dès votre première demande, l'assistant prépare le dossier tout seul : il crée le fichier `AGENTS.md` et les dossiers `data/` et `sorties/`, puis vous répond. Vous pouvez aussi commencer par « Prépare ce dossier pour ma classe ».

Les premières fois, Claude Code peut vous poser trois questions. Acceptez-les :

- la confiance dans le dossier, à la première ouverture ;
- la lecture de fichiers hors du dossier : ce sont les fichiers du plugin (programmes, modèles). Choisissez de continuer à l'autoriser ;
- l'écriture de `.claude/settings.json`, qui évite ensuite de redemander à chaque fiche.

Ensuite, deux façons de lui apprendre votre classe :

- **vos habitudes** : « Ajoute à mes consignes que je veux toujours une version différenciée. » Elles sont écrites dans `AGENTS.md`, que vous pouvez aussi modifier à la main ;
- **vos informations** (méthode de lecture, sons étudiés, zone de vacances, élèves qui ont besoin d'adaptations…) : quand vous en donnez une, l'assistant propose de la noter dans `data/classe.yaml`.

### Recevoir les mises à jour

Les mises à jour ne s'installent pas toutes seules. Deux possibilités :

- activer la mise à jour automatique : dans `/plugin`, onglet **Marketplaces**, choisir `assistant-ce1-ce2-marketplace` puis **Enable auto-update** ;
- ou mettre à jour à la main : `claude plugin update assistant-ce1-ce2@assistant-ce1-ce2-marketplace`.

Dossier créé avec la version 1.0 (copie de `modele-classe/`) : demandez « Mets à jour mon dossier de classe ». L'assistant ajoute `AGENTS.md` et retire l'ancien `CLAUDE.md`, sans toucher à vos données.

## Utiliser avec Codex (ChatGPT)

Le même dépôt s'installe aussi comme plugin [Codex](https://developers.openai.com/codex) : mêmes skills, même dossier de classe (`AGENTS.md`, `data/`, `sorties/`). On peut passer d'un outil à l'autre sur le même dossier.

Dans un terminal, avec Codex CLI installé (`npm install -g @openai/codex`) :

```bash
codex plugin marketplace add Daliush/assistant-ce1-ce2
codex plugin add assistant-ce1-ce2@assistant-ce1-ce2-marketplace
```

Redémarrez l'application Codex si elle était ouverte. Ensuite, comme avec Claude Code : créez un dossier vide, ouvrez-le dans Codex et demandez ce dont vous avez besoin.

Pour mettre à jour : `codex plugin marketplace upgrade`, puis relancez la commande `codex plugin add` ci-dessus.

Bon à savoir :

- `.claude/settings.json` ne sert qu'à Claude Code. Avec ses réglages par défaut, Codex écrit dans le dossier ouvert sans demander.
- Sous Windows, Codex passe par PowerShell : les skills lui disent de lire les fichiers en UTF-8, sinon les accents sont abîmés.

## Où sont vos fichiers

Le plugin ne contient que les instructions. **Tout ce qui concerne votre classe reste dans le dossier de la classe** : mettre à jour le plugin n'y touche jamais.

```
classe-2026-2027/
├── AGENTS.md               # dit à l'assistant d'utiliser le plugin, et garde vos consignes
├── .claude/settings.json   # autorise l'écriture sans demander dans data/journal/ et sorties/
├── data/                   # la mémoire de la classe
│   ├── classe.yaml         # facultatif : créé seulement quand vous dites « oui, note-le »
│   ├── journal/            # tout ce qui a été préparé, mois par mois (automatique)
│   └── sequences/          # vos séquences et où vous en êtes
└── sorties/                # les PDF à imprimer
    └── src/                # leurs sources HTML (modifiables) et les aperçus
```

Les fichiers sont nommés `date_niveau_matière-domaine_type`, par exemple `2026-10-05_CE1_maths-numeration_exercice.pdf`.

## Données personnelles

- **Jamais de nom réel d'élève** : codes ou pseudonymes (E01, E02…).
- **Jamais de diagnostic** : seulement les adaptations utiles (« consignes lues », « police agrandie »).
- `classe.yaml` n'est modifié qu'avec votre accord.
- Si vous versionnez le dossier de la classe avec git, gardez le dépôt **local ou privé** : même codées, ce sont des données d'élèves.

## Programmes utilisés (2026-2027)

| Matière | Texte de référence |
|---|---|
| Français, mathématiques | Programmes du cycle 2, BO n° 41 du 31 octobre 2024 (annuels, avec repères de période) |
| Enseignement moral et civique | BO n° 24 du 13 juin 2024 |
| Éducation à la vie affective et relationnelle | BO n° 6 du 6 février 2025 |
| Questionner le monde, langues vivantes, arts, EPS | Programme du cycle 2, BO n° 31 du 30 juillet 2020 |
| Horaires | Arrêté du 9 novembre 2015 |

**Rentrée 2027** : de nouveaux programmes entrent en vigueur en CE1-CE2 pour les sciences, l'histoire-géographie, l'EPS et les langues vivantes, avec une nouvelle grille horaire. Le skill `programme-cycle2` devra être mis à jour (voir la section « Validité » de son `SKILL.md`).

## Pas encore couvert

PPRE, mots aux familles et réunion de rentrée, cahier de remplacement, projets d'école. L'assistant peut aider sur ces sujets en conversation, mais sans règles dédiées.

---

## Pour les développeurs

### Organisation du dépôt

Ce dépôt est à la fois le plugin et une marketplace qui le contient (`.claude-plugin/marketplace.json`, source `./`). Codex lit cette même marketplace (format reconnu tel quel) et son propre manifeste, `.codex-plugin/plugin.json`.

```
assistant-ce1-ce2/
├── .claude-plugin/
│   ├── plugin.json           # manifeste Claude Code
│   └── marketplace.json      # marketplace, lue par Claude Code et par Codex
├── .codex-plugin/
│   └── plugin.json           # manifeste Codex (même nom, même version)
├── skills/
│   ├── assistant-classe/     # point d'entrée : règles générales, emplacement des données, choix des skills
│   ├── programme-cycle2/     # programme officiel CE1 et CE2 (données de référence)
│   ├── planifier/            # programmation, séquence, séance, journée, double niveau, choix d'activité
│   ├── didactique-francais/  # comment enseigner et écrire des contenus de français
│   ├── didactique-maths/     # comment enseigner et écrire des contenus de maths
│   ├── supports-eleve/       # forme des fiches, leçons, plans de travail, évaluations
│   ├── rendu-documents/      # HTML + CSS + script → PDF (assets/, scripts/)
│   ├── evaluer-suivre/       # évaluations, groupes de besoin, livret, analyse d'erreurs
│   ├── etat-classe/          # format de data/ et règles de lecture et d'écriture
│   └── dossier-classe/       # prépare le dossier de classe et tient AGENTS.md à jour (modèles inclus dans SKILL.md)
```

### Principes

- **Un seul agent** charge les skills dont il a besoin. Il n'y a pas de sous-agent par matière ou par niveau.
- **Données de référence dans les skills, état de la classe dans le projet de l'utilisateur.** Les skills désignent leurs propres fichiers par `${CLAUDE_SKILL_DIR}` et ceux de la classe par `${CLAUDE_PROJECT_DIR}`. Ils fonctionnent donc installés en plugin, dans `~/.claude/skills/` ou dans `.claude/skills/` d'un projet.
- **Le plugin n'écrit jamais dans son propre dossier.**
- **`assistant-classe` remplace un `CLAUDE.md`**, qu'un plugin ne peut pas fournir. Le dossier de classe n'a qu'un `AGENTS.md`, créé à la demande par `dossier-classe` : il renvoie vers `assistant-classe` et porte les consignes du prof, entre un bloc géré par le plugin (marqueurs `assistant-ce1-ce2:debut` / `fin`, remplacé quand le modèle change) et la section « Mes consignes », qui n'appartient qu'au prof.
- **`AGENTS.md` plutôt que `CLAUDE.md`**, pour être lu par tous les outils. Claude Code le lit seul depuis la version 2.1.277, à condition que le dossier n'ait pas de `CLAUDE.md` (sinon il lit `CLAUDE.md` à la place) : `dossier-classe` supprime donc l'ancien `CLAUDE.md` de la version 1.0, ou y ajoute `@AGENTS.md` si le prof y a écrit autre chose.

### Tester en local

```bash
claude plugin validate .                         # manifestes
cd /chemin/vers/un-dossier-vide
claude --plugin-dir /chemin/vers/assistant-ce1-ce2
```

Avec Codex, la marketplace locale est copiée à l'installation : après chaque modification, retirez puis réinstallez le plugin.

```bash
codex plugin marketplace add /chemin/vers/assistant-ce1-ce2
codex plugin remove assistant-ce1-ce2@assistant-ce1-ce2-marketplace
codex plugin add assistant-ce1-ce2@assistant-ce1-ce2-marketplace
codex exec --ephemeral --skip-git-repo-check -C /chemin/vers/un-dossier-vide "Une dictée pour mes CE2 sur les pluriels en -aux"
```

### Versions et livraisons

Les utilisateurs ne reçoivent une nouvelle version que lorsque le champ `version` de `.claude-plugin/plugin.json` change. **Un push sans changement de version n'est pas livré** : on peut donc pousser librement sur `master` entre deux livraisons, mais un commit « v1.2.0 » sans changement du champ `version` ne sera jamais reçu par ceux qui ont déjà le plugin.

Pour livrer :

1. incrémenter `version` dans `.claude-plugin/plugin.json` **et** `.codex-plugin/plugin.json`, avec le même numéro (`1.0.0` → `1.0.1` pour une correction, `1.1.0` pour un ajout, `2.0.0` pour un changement qui casse le format de `data/`) ;
2. `claude plugin validate --strict .` ;
3. committer, puis taguer et pousser : `claude plugin tag --push` (crée le tag `assistant-ce1-ce2--v1.0.1`).

Ne mettez pas de `version` dans `marketplace.json` : celle de `plugin.json` fait foi.

### Contribuer

Les corrections de programme doivent citer le texte officiel (BO et page). Toute règle pédagogique qui ne vient pas d'un texte officiel est signalée comme « repère d'usage » dans les skills.
