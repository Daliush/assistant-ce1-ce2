# Benchmark de bout en bout

À lancer **avant chaque livraison** (changement de `version` dans `plugin.json`) et à comparer avec les comptes rendus précédents de `resultats/`.

Chaque scénario est une vraie session Claude Code (`claude -p`, plugin chargé depuis ce dépôt avec `--plugin-dir`) dans un dossier temporaire. Le lanceur vérifie ce qui a été créé, puis lit le transcript de la session pour dire où l'agent a passé son temps.

## Lancer

```bash
python bench/lancer.py
```

```bash
python bench/lancer.py fiche-dossier fiche-conversation -n 3
```

- Compte rendu : `resultats/AAAA-MM-JJ_HHMM_v<version>.md`, réponses de l'agent dans le dossier du même nom.
- Les dossiers de test restent dans le dossier temporaire (chemin affiché) pour qu'on puisse ouvrir les PDF.
- Coût : environ 0,50 $ par dictée ou par préparation d'espace et 1,30 $ par fiche PDF avec Opus, soit 6 $ environ pour les 7 scénarios.
- Les sessions tournent avec `--permission-mode bypassPermissions`, dans le dossier temporaire uniquement.
- Analyser un transcript existant : `python bench/lancer.py --analyser ~/.claude/projects/<dossier>/<session>.jsonl`.

## Garder les mesures comparables

- **Modèle figé** : `claude-opus-5-5` (champ `modele` de `scenarios.json`, utilisé avec `--model`). Le compte rendu note le modèle réellement utilisé : s'il change, les durées ne sont plus comparables.
- **Même machine** autant que possible : la conversion PDF dépend de Playwright, de Chrome/Edge et de `pdftoppm`. Le compte rendu les note.
- **Même dossier de classe** : `fixtures/classe-type/`, un espace de travail v2 (classe de CE1-CE2, zone C, trois élèves avec adaptations, consignes « toujours une version allégée » et « tutoie-moi »). `fixtures/classe-v1/` est le même espace tel que la version 1 le créait, pour tester la migration. Ne les modifiez que si le format de l'espace change, et dites-le dans le compte rendu.
- Les durées varient d'une session à l'autre (±30 % environ) : pour comparer finement, lancez `-n 3` et regardez la médiane.

## Scénarios

| Id | Mode | Demande | Ce qu'on vérifie |
|---|---|---|---|
| `dictee-dossier` | espace prêt | « Une dictée pour mes CE2 sur les pluriels en -aux. » | réponse dans le chat, pas de PDF, entrée de journal |
| `fiche-dossier` | espace prêt | « Une fiche d'exercices de numération pour mes CE1 sur les nombres jusqu'à 100. » | fiche + corrigé + version allégée (consigne du prof), feuilles élève ≤ 2 pages, journal |
| `dossier-vide` | dossier vide | « Bonjour ! Un problème du jour pour mes CE1, s'il te plaît. » | rien n'est créé (pas d'espace sans demande), pas de PDF |
| `espace-setup` | dossier vide | « Prépare mon espace de travail pour ma classe de CE1-CE2. » | `AGENTS.md` v2 sans chemin absolu, `data/FORMATS.md` |
| `espace-migration` | espace v1 | « Mets à jour mon espace de travail. » | `AGENTS.md` passé en v2, chemin absolu retiré, consignes du prof conservées, `data/FORMATS.md` |
| `dictee-conversation` | conversation | « Une dictée pour mes CE2 sur les pluriels en -aux. » | rien n'est créé (`AGENTS.md`, `data/`, `.claude/`), pas de PDF |
| `fiche-conversation` | conversation | « Une fiche d'exercices sur l'addition posée pour mes CE2. » | rien de la classe n'est créé, 2 PDF, feuille élève ≤ 2 pages |

Le mode conversation est simulé par un dossier de travail dont le chemin contient `scratch-workspaces`, comme l'application Claude quand aucun dossier n'est choisi.

## Lire le compte rendu

- **Durée** : du message du prof à la réponse finale.
- **Conversions** : appels à `html_vers_pdf.py`. Plus d'un par production = boucle de retouche.
- **Aperçus** : images PNG regardées par l'agent. Chacune coûte plusieurs secondes.
- **Retouches** : modifications d'un document déjà écrit.
- **Où part le temps** : chaque appel d'outil compte le temps écoulé depuis la fin de l'appel précédent (réflexion et écriture du modèle, puis exécution). Catégories : `skills` (chargement), `lecture` (fichiers du plugin et de la classe), `rédaction` (premier jet des documents), `conversion`, `aperçu`, `retouche`, `mémoire` (journal, `AGENTS.md`, `data/`), `réponse finale` (écriture du message au prof).

## Historique

| Date | Version | dictee-dossier | fiche-dossier | dossier-neuf / dossier-vide | dictee-conversation | fiche-conversation | Compte rendu |
|---|---|---|---|---|---|---|---|
| 2026-10-02 | 1.1.0 | 120-169 s | 157 s | — | (créait le dossier) | 131 s* | [référence](resultats/2026-10-02_v1.1.0.md) |
| 2026-10-03 | 1.1.0-dev (vitesse + mode conversation, non livré) | 43-47 s | 145-156 s | 41-44 s | 39-45 s | 71-117 s | [compte rendu](resultats/2026-10-03_1109_v1.1.0-dev.md) |

\* Lancé dans un dossier de classe, la v1.1.0 n'ayant pas de mode conversation.

Jusqu'à la 1.1.0-dev, le scénario `dossier-neuf` préparait l'espace automatiquement puis répondait ; depuis la 2.0.0, `dossier-vide` vérifie au contraire que rien n'est créé sans demande, et `espace-setup` mesure la préparation.

Limite connue de l'analyse : quand le contenu va dans la réponse (dictée), le temps où le modèle compose le texte est compté dans la catégorie de l'appel suivant (souvent `mémoire`, pour le journal) ou dans `réponse finale`.
