---
name: etat-classe
description: Lire et mettre à jour la mémoire de la classe dans data/ — classe.yaml (facultatif), séquences en cours et journal des productions. À charger quand le prof donne une info sur sa classe, quand une séquence avance ou se termine, quand il faut écrire une ligne de journal après une production, ou quand il demande « on en est où ? », « qu'est-ce que j'ai déjà fait ? ».
---

# État de la classe

**Emplacement** : toutes les données de ce skill sont dans le projet du prof, `${CLAUDE_PROJECT_DIR}/data/`. Dans ce skill et dans `references/formats.md`, `data/…` veut toujours dire `${CLAUDE_PROJECT_DIR}/data/…`. **N'écris jamais dans le dossier du skill** (`${CLAUDE_SKILL_DIR}`) : il est remplacé à chaque mise à jour. Si `data/journal/` ou `data/sequences/` n'existent pas, crée-les au premier besoin.

Trois fichiers, trois rôles. Ne les confonds pas. (Un quatrième dossier, `data/suivi/`, n'existe que si le prof demande un suivi individuel : voir `evaluer-suivre`.)

| Fichier | Rôle | Obligatoire ? | Statuts ? |
|---|---|---|---|
| `data/journal/AAAA-MM.md` | Trace de **tout ce qui a été produit** | Oui, rempli automatiquement | **Non, jamais** |
| `data/sequences/*.md` | Plan et avancement **d'une séquence** | Non, seulement si le prof travaille en séquences | **Oui, seul endroit** |
| `data/classe.yaml` | Infos stables + **une ligne de progression par matière** | Non | Non (des phrases) |

Formats exacts, **codes communs** (matières, types, nommage) et exemples : `references/formats.md`. Lis-le avant d'écrire le premier fichier de chaque type.

## 1. Le journal (toujours)

- **Après chaque production**, une fois les fichiers réellement créés (fichier dans `sorties/` ou contenu donné dans la réponse et réutilisable), ajoute une entrée à `data/journal/AAAA-MM.md` du mois en cours. Crée le fichier s'il n'existe pas.
- **N'en parle pas au prof**, ne lui demande pas l'autorisation : c'est une trace technique.
- **Ajout seulement** : ne modifie ni ne supprime jamais une entrée passée.
- **Pas de statut** (« fait », « à faire ») : le journal dit ce qui a été **préparé**, pas ce qui a été fait en classe.
- Sers-t'en pour :
  - **éviter les doublons** (« Tu as déjà une fiche sur les homophones a/à du 12 septembre, je repars d'elle ? ») ;
  - **réutiliser** un support existant ;
  - **amorcer `classe.yaml`** quand le prof décide de le remplir (proposer une progression à partir de ce qui a été produit).

## 2. Les séquences (si le prof en utilise)

**Créer** une séquence quand le prof demande une séquence, ou plusieurs séances sur un même objectif. Un fichier par séquence, même si elle concerne les deux niveaux.

**Statuts** — deux échelles distinctes :
- **séquence** (en-tête, un par niveau) : `prevue` | `en_cours` | `terminee` | `interrompue` ;
- **séance** (tableau, une colonne par niveau) : `prevue` | `faite` | `sautee`.

**Demander l'avancement** (une seule fois par séquence et par session) :
- quand la demande touche la matière d'une séquence `en_cours` ;
- quand le prof planifie une journée, une semaine ou une période : **une seule question groupée** pour toutes les séquences en cours concernées ;
- si une séquence est `en_cours` depuis **plus de 3 semaines** sans mise à jour (champ `maj`), signale-le en une ligne.

Formule courte : « La séquence *la phrase* (CE2) en est à la séance 2 sur 5. Où en es-tu : terminée, on continue, ou on arrête ? »

**Selon la réponse :**

| Réponse | Fichier de séquence | `classe.yaml` |
|---|---|---|
| « Séances 1 et 2 faites » | Statut des séances → `faite`, note éventuelle du prof | Rien |
| « Terminée » | Séances faites → `faite`, statut du niveau → `terminee`, `maj` = date | **Si le fichier existe** : réécris la ligne de progression de la matière en une phrase, puis propose la suite (séquence suivante du programme pour la période) |
| « Pas encore » / pas de réponse | Rien, ou `maj` seulement | Rien |
| « On arrête » | Statut du niveau → `interrompue`, note « arrêtée le … » | Rien |
| « On a fait autrement » | Note du prof dans la colonne prévue, sans réécrire le plan | Rien |

**Ne coche jamais une séance toi-même** parce que tu as produit son support : produire n'est pas faire.

## 3. `classe.yaml` (facultatif)

- **N'oblige jamais le prof à le remplir.** Sans lui, tout fonctionne : niveau tiré de la demande, période tirée de la date, acquis = repères ★ du programme, PDF A4 noir et blanc.
- **Création** : au premier « oui, note-le ». Crée le fichier avec **seulement** les champs que le prof a donnés (les autres restent absents, pas vides). **Reprends les noms de champs de l'exemple** de `references/formats.md` §3 (`zone`, `manuels.CE1_lecture`, `sons_etudies_CE1`, `lexique`…) ; n'invente un nouveau champ que si rien ne convient.
- **Enrichissement** : quand le prof donne une info stable en passant (« mes CE1 utilisent *Taoki* », « on n'a pas classe le mercredi », « E04 a besoin des consignes lues »), termine ta réponse par « Je le note pour la suite ? ». Écris seulement après un oui.
- **Relances limitées** : au plus une par session, et seulement pour une info de cette liste fermée, quand elle manque **et** dégrade vraiment le résultat demandé :
  - les sons étudiés en CE1 (pour un texte que les CE1 lisent seuls) ;
  - l'algorithme de soustraction posée de l'école (pour une séance de soustraction posée) ;
  - la zone (pour une programmation de P3 à P5).
  Formule : « Pour que mes textes CE1 soient vraiment déchiffrables, j'aurais besoin de savoir quels sons tes élèves connaissent. Tu veux me le dire ? » Si le prof ne répond pas, continue avec l'hypothèse par défaut.
- **Jamais sans le prof** : tu ne modifies `classe.yaml` qu'après une demande ou une réponse explicite. Montre la ligne modifiée en une phrase (« J'ai noté : CE2 · maths → *fractions : sens et écriture faits ; prochaine séquence : comparaison* »).
- **Progression** : une phrase courte par matière et par niveau (pas de liste), qui dit où on en est et ce qui vient. Les détails sont dans les séquences.
- **Élèves** : codes ou pseudonymes, niveau, groupes, adaptations. **Jamais de nom réel, jamais de diagnostic.** Si le prof en donne, enregistre la version anonymisée et dis-le en une ligne.
- **Lexique** : termes que la classe utilise et qu'il faut garder partout (« déterminant », jamais « petit mot »). Respecte-le dans toute production.

## 4. « On en est où ? » / « Qu'est-ce que j'ai déjà fait ? »

1. Lis `classe.yaml` (progression) s'il existe.
2. Lis l'en-tête des séquences `en_cours` et `prevue`.
3. Lis le journal des 2 derniers mois.
4. Réponds **par matière, par niveau**, en quelques lignes. Distingue bien « préparé » (journal) et « fait » (séquences cochées par le prof).
5. Si tu compares au programme (« il me reste quoi pour la P2 ? »), charge `programme-cycle2` et cite les repères ★.

## 5. Règles de prudence

- Avant d'écrire un fichier de `data/`, **relis-le** : le prof a pu le modifier à la main.
- Garde le YAML valide (guillemets autour des chaînes contenant `:` ou `#`). Si PyYAML est installé, vérifie après écriture : `python3 -c "import yaml; yaml.safe_load(open('${CLAUDE_PROJECT_DIR}/data/classe.yaml'))"` ; sinon relis le fichier.
- N'efface jamais une info du prof pour la remplacer par une déduction.
