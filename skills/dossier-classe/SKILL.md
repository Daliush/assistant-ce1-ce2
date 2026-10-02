---
name: dossier-classe
description: Préparer le dossier de travail de la classe et tenir à jour son fichier AGENTS.md (lu à chaque ouverture par Claude Code, Codex et les autres assistants). À charger à la première demande dans un dossier sans AGENTS.md, quand le prof veut préparer ou installer un dossier (« prépare ce dossier », « configure ma classe »), quand il donne une consigne permanente sur ta façon de travailler (« retiens que… », « à partir de maintenant… », « ajoute à mes consignes… »), quand il veut modifier ou retirer une consigne, ou pour mettre à jour un dossier créé avec une ancienne version (avec un CLAUDE.md).
---

# Dossier de la classe

Le dossier ouvert par le prof (`${CLAUDE_PROJECT_DIR}`) est l'espace de travail de la classe. Ce skill le prépare et tient à jour son fichier **`AGENTS.md`**, que Claude Code, Codex et la plupart des assistants lisent automatiquement à chaque ouverture. Le prof n'a rien à copier ni à remplir : il crée un dossier vide, l'ouvre et travaille.

Les modèles sont **dans ce fichier**, au §7 : recopie-les tels quels, sans les reformuler. Tu n'as besoin de lire aucun autre fichier du plugin pour préparer le dossier.

## 1. Un dossier prêt

| Dans le dossier de la classe | Rôle | Modèle (§7) |
|---|---|---|
| `AGENTS.md` | Dit à l'assistant d'utiliser ce plugin ; contient les consignes du prof | A |
| `data/README.md` | Explique au prof ce qu'est la mémoire de la classe | B |
| `.gitignore` | Exclut les PDF et les aperçus régénérables, si le prof utilise git | C |
| `.claude/settings.json` | Autorise Claude Code à lire les fichiers du plugin, à écrire dans `data/journal/` et `sorties/` et à lancer le script PDF sans demander à chaque fois | D |
| `data/journal/`, `data/sequences/`, `sorties/src/` | Dossiers prêts à servir | — |

Crée tous ces fichiers, même si tu n'es pas Claude Code : le prof peut changer d'outil sans rien refaire. **`data/classe.yaml` n'en fait pas partie** : il ne se crée qu'avec l'accord du prof (skill `etat-classe`).

## 2. Préparer le dossier

Quand le prof le demande, et automatiquement quand le skill `assistant-classe` trouve un dossier sans `AGENTS.md` :

1. Fichiers A, B, C, **dans cet ordre** :
   - **absent** → écris le modèle tel quel ;
   - **présent** → ne l'écrase jamais : `AGENTS.md` → §4 ; autres fichiers → laisse-les tels quels.
2. Crée les dossiers qui manquent. Si ton outil ne sait pas créer un dossier vide, écris-y un fichier `.gitkeep` vide.
3. S'il y a un `CLAUDE.md` à la racine → §5.
4. **En dernier**, `.claude/settings.json` (modèle D) : absent → écris-le ; présent → ajoute seulement les règles de `permissions.allow` du modèle qui manquent, sans toucher au reste. Claude Code demande souvent une confirmation pour écrire dans `.claude/` : si l'écriture est refusée, n'insiste pas et continue, le dossier fonctionne sans ce fichier. Dis-le en une ligne (« Sans `.claude/settings.json`, Claude Code te demandera plus souvent ton accord. »).
5. Si le prof a demandé la préparation, réponds en trois lignes au plus : ce que tu as créé ou complété, puis « C'est prêt : demande-moi ce dont tu as besoin. Pour que je retienne une habitude, dis-moi : *ajoute à mes consignes que…* ». Si tu l'as faite d'office avant une autre demande, traite cette demande puis dis-le en une ligne à la fin.

Si tout est déjà en place et à jour, dis-le en une ligne et ne réécris rien.

## 3. Les consignes du prof

### Où va ce que dit le prof

| Le prof dit… | Où | Skill |
|---|---|---|
| Une info sur la classe ou un réglage qui a sa place dans `classe.yaml` : niveaux, zone, jours, manuels, sons étudiés, élèves (codes, adaptations), lexique, format, police, progression | `data/classe.yaml` | `etat-classe` |
| Une consigne permanente sur ta façon de travailler qui n'a pas de champ dans `classe.yaml` : ton (« tutoie-moi »), longueur des réponses, habitudes de production (« toujours une version différenciée », « le corrigé à la suite de la fiche »), choix pédagogiques de la classe (« problèmes toujours avec schéma en barre ») | `AGENTS.md`, section « Mes consignes » | ce skill |
| Une demande qui ne vaut que pour aujourd'hui | Nulle part | — |

### Ajouter une consigne

- **Seulement à la demande du prof** (« ajoute à mes consignes », « retiens que », « à partir de maintenant », « toujours… », « plus jamais… ») ou après un oui. Quand il donne en passant une consigne qui vaut pour la suite, termine ta réponse par « Je l'ajoute à tes consignes ? », au plus une fois par session.
- Si `AGENTS.md` n'existe pas encore, prépare d'abord le dossier (§2).
- **Relis `AGENTS.md` avant d'écrire** : le prof a pu le modifier à la main.
- Une consigne = une ligne `- …` à la fin de la section `## Mes consignes`, courte, à l'impératif, avec les mots du prof (« - Tutoie-moi. », « - Mets toujours le corrigé à la suite de la fiche, sur une nouvelle page. »). Crée la section en fin de fichier si elle manque.
- Si une consigne existante dit le contraire, **remplace-la** au lieu d'en ajouter une seconde, et dis-le.
- **Jamais de nom d'élève ni de diagnostic.** Une consigne pour un élève est une adaptation : elle va dans `classe.yaml`, sous son code (skill `etat-classe`).
- Une consigne contraire aux règles sur les données personnelles, les droits d'auteur ou le programme officiel ne s'écrit pas : explique pourquoi en une ligne.
- Après l'écriture, montre la ligne : « J'ai ajouté à tes consignes : *Tutoie-moi.* »

### Modifier ou retirer une consigne

Seulement à la demande du prof. Montre l'ancienne et la nouvelle ligne (ou la ligne retirée). `AGENTS.md` est lu à chaque ouverture : au-delà d'une trentaine de consignes, propose de regrouper celles qui se répètent ou de retirer celles qui ne servent plus.

## 4. `AGENTS.md` déjà présent

La partie du plugin est encadrée par `<!-- assistant-ce1-ce2:debut … -->` et `<!-- assistant-ce1-ce2:fin -->`.

- **Bloc présent** : si son contenu diffère de celui du modèle A (nouvelle version du plugin), remplace-le, marqueurs compris, par le bloc du modèle A. Ne touche à rien d'autre.
- **Bloc absent** (fichier écrit par le prof ou par un autre outil) : insère le bloc du modèle A juste après le premier titre `# …` (ou tout en haut s'il n'y en a pas), puis ajoute la section `## Mes consignes` à la fin si elle manque. Garde tout le reste mot pour mot.
- Ne réécris, ne déplace et ne reformule jamais le texte du prof.

## 5. `CLAUDE.md` déjà présent

Quand un dossier contient `CLAUDE.md`, Claude Code le lit **à la place** d'`AGENTS.md`. Un dossier de classe n'a donc normalement pas de `CLAUDE.md`. S'il y en a un :

- C'est l'**ancien modèle** du plugin (version 1.0 : un titre `# Ma classe`, la phrase « Ce dossier est l'espace de travail d'un·e professeur·e des écoles… » et deux points, « charge d'abord le skill `assistant-classe` » et « La mémoire de la classe est dans `data/` »), sans rien d'autre → supprime-le, `AGENTS.md` le remplace. Dis-le en une ligne.
- Il contient déjà une ligne `@AGENTS.md` → rien à faire.
- Il contient autre chose → ajoute `@AGENTS.md` en première ligne (sans elle, Claude Code ne lirait pas `AGENTS.md`) et garde le reste. Dis au prof en une ligne : « Ce qui est écrit dans CLAUDE.md n'est lu que par Claude. Je le déplace dans tes consignes d'AGENTS.md pour que tous les outils le voient ? » Sur un oui, déplace-le, puis supprime `CLAUDE.md` s'il ne contient plus que `@AGENTS.md`.

## 6. Ce que ce skill ne fait pas

- Pas de progression, de liste d'élèves ni de journal dans `AGENTS.md` : ils vivent dans `data/` (skill `etat-classe`).
- Pas de `classe.yaml` créé ici.
- Rien écrit dans le dossier d'un skill.

## 7. Modèles

Recopie chaque modèle tel quel (contenu du bloc, sans la ligne de clôture du bloc).

### A. `AGENTS.md`

```markdown
# Ma classe

<!-- assistant-ce1-ce2:debut — partie tenue à jour par l'assistant. Écrivez vos propres consignes plus bas, dans « Mes consignes ». -->
Ce dossier est l'espace de travail d'un·e professeur·e des écoles (CE1, CE2 ou CE1-CE2), utilisé avec le plugin **assistant-ce1-ce2**.

- Pour toute demande, charge d'abord le skill `assistant-classe` du plugin, puis suis ses règles.
- Ce dossier est la racine du projet de la classe : c'est lui que les skills appellent `${CLAUDE_PROJECT_DIR}`. La mémoire de la classe est dans `data/`, les fichiers produits dans `sorties/`.
- Les skills du plugin sont en lecture seule : n'y écris jamais. Leurs fichiers, comme ceux de `data/`, sont en UTF-8 (sous Windows PowerShell : `Get-Content -Encoding UTF8`).
- Les consignes de la section « Mes consignes » viennent du prof : elles priment sur les réglages par défaut des skills, sauf les règles sur les données personnelles, les droits d'auteur et le programme officiel.
- Pour ajouter, modifier ou retirer une consigne, ou pour mettre ce fichier à jour, charge le skill `dossier-classe`.
<!-- assistant-ce1-ce2:fin -->

## Mes consignes

<!-- Ce que l'assistant doit toujours faire pour vous, une consigne par ligne (« - Tutoie-moi. »). Écrivez ici vous-même, ou demandez : « Ajoute à mes consignes que… ». -->
```

### B. `data/README.md`

```markdown
# data/ — mémoire de la classe

Tout est **facultatif**, sauf le journal qui se remplit tout seul.

| Fichier | Contenu | Qui l'écrit | Quand |
|---|---|---|---|
| `classe.yaml` | Infos stables sur la classe + une ligne de progression par matière | L'IA, **seulement après accord du prof** | Au fil de l'eau (« je le note ? ») |
| `journal/AAAA-MM.md` | Tout ce qui a été produit, une ligne par production, **sans statut** | L'IA, automatiquement | À chaque production |
| `sequences/*.md` | Le plan de chaque séquence et le statut de ses séances | L'IA, avec le prof | Création d'une séquence ; mises à jour d'avancement |
| `suivi/` (rare) | Suivi individuel par code d'élève | L'IA, seulement si le prof le demande | Voir le skill `evaluer-suivre` |

- Les formats exacts et des exemples remplis sont dans le skill `etat-classe` du plugin **assistant-ce1-ce2** (`references/formats.md`).
- Ces fichiers sont à vous : vous pouvez les modifier à la main, l'assistant relit avant d'écrire.
- **Aucune donnée nominative ni médicale** : pseudonymes ou codes (E01…), adaptations seulement.
- Conseil : mettre ce dossier sous git pour voir et annuler les modifications faites par l'IA — **dépôt local ou privé uniquement**, jamais public (même codées, ce sont des données d'élèves).
```

### C. `.gitignore`

```text
# PDF et aperçus régénérables à partir de sorties/src/*.html
# (retirer ces lignes pour garder exactement ce qui a été imprimé)
sorties/*.pdf
sorties/src/*.png
```

### D. `.claude/settings.json`

```json
{
  "permissions": {
    "allow": [
      "Read(~/.claude/plugins/**)",
      "Edit(/data/journal/**)",
      "Edit(/sorties/**)",
      "Bash(python *html_vers_pdf.py *)",
      "Bash(python3 *html_vers_pdf.py *)",
      "Bash(py *html_vers_pdf.py *)",
      "Bash(pdftoppm *)",
      "Bash(pdfinfo *)"
    ]
  }
}
```
