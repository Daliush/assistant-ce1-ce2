---
name: espace-classe
description: Préparer ou mettre à jour l'espace de travail d'une classe de CE1, CE2 ou CE1-CE2 (AGENTS.md, data/, sorties/), pour que l'assistant range les documents et garde la mémoire de la classe d'une session à l'autre. Seulement quand le prof le demande explicitement (« prépare mon espace de travail », « installe ce dossier pour ma classe », « mets à jour mon espace »), jamais de ta propre initiative. Exception : si l'AGENTS.md du dossier demande de charger le skill assistant-classe (espace créé avec la version 1 du plugin), propose la mise à jour en une ligne.
---

# Espace de travail de la classe

Un espace de travail est un dossier que le prof ouvre dans Claude Code ou Codex. Son `AGENTS.md`, lu à chaque ouverture, dit où ranger ce que les skills produisent et ce qu'il faut retenir ; `data/` garde la mémoire de la classe ; `sorties/` reçoit les documents. Sans espace, les autres skills marchent tout aussi bien : ils ne rangent rien et ne retiennent rien.

## 1. Quand

- **Seulement à la demande du prof.** Ne crée jamais d'espace de toi-même et ne le propose pas à chaque demande. Seule exception : un espace de la version 1 (son `AGENTS.md` parle du skill `assistant-classe`) : propose une fois « Ton dossier a été préparé avec l'ancienne version de l'assistant : je le mets à jour ? ».
- **Pas de dossier à lui** (conversation sur claude.ai ou dans l'application Claude sans dossier choisi, dossier de travail temporaire) : n'écris rien. Explique en deux lignes qu'il faut ouvrir un dossier à lui dans Claude Code ou Codex pour que l'assistant garde la mémoire de la classe. En attendant, ses habitudes peuvent aller dans les instructions de son projet ou dans ses préférences.
- **Dossier qui contient déjà autre chose** (projet de code, documents personnels) : demande d'abord si c'est bien le dossier de la classe.

## 2. Préparer ou mettre à jour : une commande

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/preparer_espace.py "<dossier de la classe>"
```

Remplace `${CLAUDE_SKILL_DIR}` par le vrai chemin si ton outil ne l'a pas fait ; sous Windows, utilise `python` ou `py`. Le même script prépare un dossier vide et met à jour un espace existant, sans jamais écraser le texte du prof :

| Fichier | Absent | Présent |
|---|---|---|
| `AGENTS.md` | créé | seule la partie du plugin (entre les marqueurs `assistant-ce1-ce2:debut` et `:fin`) est remplacée ; insérée après le premier titre si elle manque ; « Mes consignes » ajouté s'il manque |
| `data/FORMATS.md` | créé | remplacé s'il a changé (fichier du plugin) |
| `data/README.md`, `.gitignore` | créés | laissés tels quels |
| `.claude/settings.json` | créé | complété des autorisations qui manquent |
| `data/journal/`, `data/sequences/`, `sorties/src/` | créés | — |
| `CLAUDE.md` | — | ancien modèle de la version 1.0 → supprimé ; autre contenu → `@AGENTS.md` ajouté en première ligne (sinon Claude Code ne lirait pas `AGENTS.md`) |

Puis réponds en trois lignes au plus : ce qui a été créé ou mis à jour (d'après le compte rendu du script), puis « C'est prêt : demande-moi ce dont tu as besoin. Pour que je retienne une habitude, dis-moi : *ajoute à mes consignes que…* ».

- Le script signale un `CLAUDE.md` avec d'autres consignes : demande « Ce qui est écrit dans CLAUDE.md n'est lu que par Claude. Je le déplace dans tes consignes d'AGENTS.md pour que tous les outils le voient ? ». Sur un oui, déplace-le à la fin de « Mes consignes », puis supprime `CLAUDE.md` s'il ne contient plus que `@AGENTS.md`.
- Claude Code peut demander l'accord du prof pour écrire dans `.claude/` : si c'est refusé, n'insiste pas et dis en une ligne « Sans `.claude/settings.json`, Claude Code te demandera plus souvent ton accord. ».
- `data/classe.yaml` ne fait pas partie de l'espace de départ : il ne se crée qu'avec l'accord du prof (règles dans `AGENTS.md`).

## 3. Sans Python

Fais la même chose à la main avec les modèles de `${CLAUDE_SKILL_DIR}/assets/modeles/` (`AGENTS.modele.md`, `FORMATS.modele.md`, `data-README.modele.md`, `gitignore.modele`, `settings.modele.json`), en suivant le tableau ci-dessus. Recopie-les tels quels, sans les reformuler, et n'y écris jamais de chemin absolu : le prof peut déplacer ou renommer son dossier. Le modèle v1.0 de `CLAUDE.md` à supprimer tient en six lignes : un titre `# Ma classe`, la phrase « Ce dossier est l'espace de travail d'un·e professeur·e des écoles… », puis « charge d'abord le skill `assistant-classe` » et « La mémoire de la classe est dans `data/` ».

## 4. Ce que ce skill ne fait pas

- Il n'écrit pas les consignes du prof : `AGENTS.md` dit lui-même comment les ajouter.
- Il ne crée pas `classe.yaml`, ni journal, ni séquence : ce sont les règles d'`AGENTS.md` qui s'en chargent au fil du travail.
- Il n'écrit rien dans le dossier d'un skill.
