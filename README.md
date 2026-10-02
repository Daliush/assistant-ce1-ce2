# Assistant CE1-CE2

Un plugin [Claude Code](https://code.claude.com) pour préparer la classe en **CE1, CE2 ou CE1-CE2** : séances, séquences, fiches d'exercices, leçons, dictées, textes de lecture, problèmes, journées, évaluations. Les documents sortent en **PDF A4 imprimables en noir et blanc**, avec leur corrigé et une fiche de préparation.

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

- [Claude Code](https://code.claude.com) installé et connecté à un compte Claude.
- Pour fabriquer les PDF, **une seule** de ces options :
  - `pip install playwright && playwright install chromium` (recommandé) ;
  - ou Google Chrome, Chromium ou Microsoft Edge installé ;
  - ou `pip install weasyprint` (sous macOS et Windows, il faut aussi la bibliothèque Pango).

  Sans aucun de ces outils, l'assistant livre des fichiers HTML à imprimer depuis le navigateur.
- Facultatif : `pdftoppm` (paquet `poppler-utils` ou `poppler`), pour que l'assistant vérifie visuellement ses PDF ; la police gratuite [Andika](https://software.sil.org/andika/), conçue pour l'apprentissage de la lecture.

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

Copiez le dossier [`modele-classe/`](modele-classe/) de ce dépôt (bouton **Code → Download ZIP** sur GitHub) et renommez-le, par exemple `classe-2026-2027`. Prévoyez un dossier par classe ou par année.

```bash
cd classe-2026-2027
claude
```

La première fois, acceptez la demande de confiance du dossier : c'est elle qui active les autorisations du fichier `.claude/settings.json`. Puis demandez ce dont vous avez besoin.

Rien n'est à remplir pour commencer. Quand vous donnez une information utile sur votre classe (méthode de lecture, sons étudiés, zone de vacances, élèves qui ont besoin d'adaptations…), l'assistant propose de la noter pour la suite.

### Recevoir les mises à jour

Les mises à jour ne s'installent pas toutes seules. Deux possibilités :

- activer la mise à jour automatique : dans `/plugin`, onglet **Marketplaces**, choisir `assistant-ce1-ce2-marketplace` puis **Enable auto-update** ;
- ou mettre à jour à la main : `claude plugin update assistant-ce1-ce2@assistant-ce1-ce2-marketplace`.

## Où sont vos fichiers

Le plugin ne contient que les instructions. **Tout ce qui concerne votre classe reste dans le dossier de la classe** : mettre à jour le plugin n'y touche jamais.

```
classe-2026-2027/
├── CLAUDE.md               # dit à l'assistant d'utiliser le plugin
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

Ce dépôt est à la fois le plugin et une marketplace qui le contient (`.claude-plugin/marketplace.json`, source `./`).

```
assistant-ce1-ce2/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skills/
│   ├── assistant-classe/     # point d'entrée : règles générales, emplacement des données, choix des skills
│   ├── programme-cycle2/     # programme officiel CE1 et CE2 (données de référence)
│   ├── planifier/            # programmation, séquence, séance, journée, double niveau, choix d'activité
│   ├── didactique-francais/  # comment enseigner et écrire des contenus de français
│   ├── didactique-maths/     # comment enseigner et écrire des contenus de maths
│   ├── supports-eleve/       # forme des fiches, leçons, plans de travail, évaluations
│   ├── rendu-documents/      # HTML + CSS + script → PDF (assets/, scripts/)
│   ├── evaluer-suivre/       # évaluations, groupes de besoin, livret, analyse d'erreurs
│   └── etat-classe/          # format de data/ et règles de lecture et d'écriture
└── modele-classe/            # dossier de classe vide, à copier par les utilisateurs
```

### Principes

- **Un seul agent** charge les skills dont il a besoin. Il n'y a pas de sous-agent par matière ou par niveau.
- **Données de référence dans les skills, état de la classe dans le projet de l'utilisateur.** Les skills désignent leurs propres fichiers par `${CLAUDE_SKILL_DIR}` et ceux de la classe par `${CLAUDE_PROJECT_DIR}`. Ils fonctionnent donc installés en plugin, dans `~/.claude/skills/` ou dans `.claude/skills/` d'un projet.
- **Le plugin n'écrit jamais dans son propre dossier.**
- **`assistant-classe` remplace un `CLAUDE.md`**, qu'un plugin ne peut pas fournir. Le `CLAUDE.md` du dossier de classe se contente de renvoyer vers lui.

### Tester en local

```bash
claude plugin validate .                         # manifestes
cd /chemin/vers/une-copie-de-modele-classe
claude --plugin-dir /chemin/vers/assistant-ce1-ce2
```

### Versions et livraisons

Les utilisateurs ne reçoivent une nouvelle version que lorsque le champ `version` de `.claude-plugin/plugin.json` change. **Un push sans changement de version n'est pas livré** : on peut donc pousser librement sur `main` entre deux livraisons.

Pour livrer :

1. incrémenter `version` dans `plugin.json` (`1.0.0` → `1.0.1` pour une correction, `1.1.0` pour un ajout, `2.0.0` pour un changement qui casse le format de `data/`) ;
2. `claude plugin validate --strict .` ;
3. committer, puis taguer et pousser : `claude plugin tag --push` (crée le tag `assistant-ce1-ce2--v1.0.1`).

Ne mettez pas de `version` dans `marketplace.json` : celle de `plugin.json` fait foi.

### Contribuer

Les corrections de programme doivent citer le texte officiel (BO et page). Toute règle pédagogique qui ne vient pas d'un texte officiel est signalée comme « repère d'usage » dans les skills.
