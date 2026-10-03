# Formats des fichiers de data/

<!-- Fichier tenu à jour par l'assistant (plugin assistant-ce1-ce2) et remplacé à chaque mise à jour de l'espace : ne le modifiez pas. -->

Formats que l'assistant suit pour écrire dans `data/`. Les fichiers eux-mêmes (`classe.yaml`, journal, séquences) sont au prof : il peut les modifier à la main, l'assistant les relit avant d'écrire.

## 0. Codes

| Élément | Codes |
|---|---|
| Niveau | `CE1`, `CE2`, `CE1-CE2` |
| Matière (noms de fichiers) | `fr`, `maths`, `qlm`, `emc`, `evar`, `lve`, `arts`, `eps`, `multi` (journée, semaine) |
| Matière (texte du journal) | Français, Maths, QLM, EMC, EVAR, LVE, Arts, EPS, Toutes matières |
| Domaine | mot court sans accent : `lecture`, `ecriture`, `dictee`, `oral`, `vocabulaire`, `grammaire`, `conjugaison`, `orthographe`, `culture`, `poesie`, `numeration`, `calcul`, `problemes`, `fractions`, `grandeurs`, `geometrie`, `donnees`… (dans le texte du journal : avec accents, « Numération ») |
| Type | `cours`, `lecon`, `exercice`, `dictee`, `lecture`, `problemes`, `atelier`, `plan-travail`, `seance-N` (N = numéro dans la séquence) ou `seance`, `sequence`, `programmation`, `journee`, `semaine`, `evaluation`, `affichage`, `etiquettes`, `diaporama` |

## 1. Journal — `data/journal/AAAA-MM.md`

Un fichier par mois. Une section par jour (date de production), une entrée par production. Ajout en fin de fichier uniquement.

```markdown
# Journal — octobre 2026

## 2026-10-01
- CE1-CE2 · Français · Grammaire · seance-1 · « La phrase : observer et trier » (séance 1/5)
  sorties/2026-10-01_CE1-CE2_fr-grammaire_seance-1_prep.pdf
  sorties/2026-10-01_CE1_fr-grammaire_exercice.pdf
  sorties/2026-10-01_CE2_fr-grammaire_exercice.pdf
  séquence : P1_fr_grammaire_la-phrase.md
- CE2 · Maths · Fractions · cours · « Fractions d'une bande-unité »
  sorties/2026-10-01_CE2_maths-fractions_cours.pdf

## 2026-10-03
- CE1 · Français · Dictée · dictee · « Dictée de mots, sons [ou] et [on] » (contenu dans la réponse, pas de fichier)
```

Format d'une entrée : `- <niveau> · <Matière> · <Domaine> · <type> · « <titre court> »`, puis, en retrait, les fichiers produits et, s'il y en a une, la séquence liée.

- Le corrigé, la prep et les versions allégée ou adaptée sont listés sous l'entrée de leur document, pas comme entrées séparées.
- Écrite **après** la création des fichiers, avec leurs chemins réels. Une entrée par production du tour (une dictée puis des problèmes : deux entrées).
- Pas de statut, pas de commentaire sur la qualité : le journal dit ce qui a été **préparé**, pas ce qui a été fait en classe.

## 2. Séquence — `data/sequences/<P>_<matiere>_<domaine>_<titre-court>.md`

Nom : période prévue, code matière, domaine, titre court en minuscules avec tirets. Exemple : `P1_fr_grammaire_la-phrase.md`. Un fichier par séquence, même si elle concerne les deux niveaux.

```markdown
---
titre: La phrase
matiere: fr
domaine: grammaire
niveaux: [CE1, CE2]
periode: P1
statut: {CE1: en_cours, CE2: en_cours}
creee: 2026-10-01
maj: 2026-10-01
---

# La phrase — CE1-CE2

## Objectifs du programme
- **CE1** : « Reconnaître et utiliser les trois types de phrases, en lien avec la ponctuation : déclarative, interrogative et impérative. »
- **CE2** : « Utiliser la ponctuation de fin de phrase (. ! ?) et reconnaître les marques du discours rapporté. »

## Prérequis
- CE1 : majuscule et point découverts au CP.
- CE2 : notion de phrase vue au CE1.

## Séances

| # | Objectif CE1 | Objectif CE2 | Statut CE1 | Statut CE2 | Note du prof |
|---|---|---|---|---|---|
| 1 | Observer et trier : phrase / pas phrase (majuscule, point, sens) | Idem, puis trier selon la ponctuation finale | faite | faite | Les CE1 ont eu besoin de plus de temps |
| 2 | Remettre des mots dans l'ordre ; majuscule et point | Phrases déclaratives / interrogatives | prevue | faite | |
| 3 | Phrases déclaratives / interrogatives à l'oral puis à l'écrit | Phrases impératives ; discours rapporté (« … ») | prevue | prevue | |
| 4 | Réinvestissement en dictée et en production | Transformations de type ; réinvestissement | prevue | prevue | |
| 5 | Évaluation | Évaluation | prevue | prevue | |

## Supports produits
- Séance 1 : sorties/2026-10-01_CE1-CE2_fr-grammaire_seance-1_prep.pdf

## Évaluation prévue
- Séance 5 : critères de réussite par niveau.
```

- **Statut d'une séance** : `prevue` | `faite` | `sautee`, **une colonne par niveau** (en décalage, les deux niveaux n'avancent pas au même rythme). C'est le prof qui le donne.
- **Statut de la séquence** : un par niveau, dans l'en-tête : `prevue` | `en_cours` | `terminee` | `interrompue`. Une séquence passe `en_cours` quand le prof dit avoir fait la première séance (ou demande la séance 2).
- Séquence pour un seul niveau : `niveaux: [CE2]`, `statut: {CE2: prevue}`, une seule colonne « Statut ».
- `maj` : date de la dernière mise à jour d'un statut. Une séquence `en_cours` sans mise à jour depuis plus de 3 semaines se signale en une ligne.

Selon la réponse du prof à « où en est-on ? » :

| Réponse | Fichier de séquence | `classe.yaml` |
|---|---|---|
| « Séances 1 et 2 faites » | Statut des séances → `faite`, note éventuelle du prof | Rien |
| « Terminée » | Séances faites → `faite`, statut du niveau → `terminee`, `maj` = date | S'il existe : réécris la ligne de progression de la matière, puis propose la séquence suivante |
| « Pas encore » / pas de réponse | Rien, ou `maj` seulement | Rien |
| « On arrête » | Statut du niveau → `interrompue`, note « arrêtée le … » | Rien |
| « On a fait autrement » | Note du prof dans la colonne prévue, sans réécrire le plan | Rien |

## 3. Classe — `data/classe.yaml`

**Tous les champs sont facultatifs.** Ne crée que ceux que le prof a donnés (les autres restent absents, pas vides) et reprends ces noms de champs. Exemple complet (une vraie classe en aura beaucoup moins au début) :

```yaml
annee: "2026-2027"
zone: B                      # A, B ou C (vacances d'hiver et de printemps)
jours: [lundi, mardi, jeudi, vendredi]

niveaux:
  CE1: 11
  CE2: 13

emploi_du_temps:
  creneaux_imposes:
    - "lundi 13h30-14h15 : piscine (période 2)"
    - "jeudi 9h00-10h00 : intervenant musique"
  remarques: "Récréation 10h15-10h30 et 15h15-15h30"

manuels:
  CE1_lecture: "méthode syllabique de la classe (préciser le titre)"
  CE2_maths: "fichier de l'école"

sons_etudies_CE1: "tous les sons simples + ou, on, an, oi (au 01/10)"
soustraction_posee: cassage    # cassage ou compensation : algorithme de l'école

lexique:
  - "déterminant (jamais « petit mot »)"
  - "verbe conjugué / infinitif"
  - "nom propre / nom commun"

preferences:
  format: pdf                # pdf | docx | pptx
  impression: a4_noir_et_blanc
  police: "Arial 14 pour les CE1"
  diaporama: false

acquis_supposes:
  CE1: "Le CP a vu le passé composé à l'oral seulement."

eleves:
  - id: E01
    niveau: CE1
    groupes: {lecture: fragile}
    adaptations: [consignes lues, police 16]
  - id: E02
    niveau: CE2
    groupes: {maths: avance}

progression:
  francais:
    CE1: "Sons simples et ou/on/an faits ; séquence la phrase en cours (séance 2/5)."
    CE2: "Phrase et ponctuation terminées ; prochaine séquence : le verbe."
  maths:
    CE1: "Nombres jusqu'à 100 consolidés ; centaines en cours."
    CE2: "Nombres jusqu'à 1 000 révisés ; fractions : sens et écriture en cours."
  qlm: "Commun : le vivant, cycle de vie (en cours)."
  emc: "CE1 : respecter les autres, les règles de classe ; CE2 : conseil d'élèves lancé."
  lve: "Anglais commun : salutations, couleurs, nombres 1-20."
  arts: "Musique : 2 chants appris."
  eps: "Jeux collectifs P1 ; natation en P2."
```

Règles :
- `progression` : **une phrase par matière** (et par niveau en français, maths, EMC), qui dit où on en est et ce qui vient. Réécrite (pas complétée) quand une séquence se termine ou quand le prof la corrige.
- `eleves` : **aucun nom réel, aucun diagnostic**. Seulement `id` (code ou pseudonyme), `niveau`, `groupes`, `adaptations`. Si le prof donne un nom ou un diagnostic, enregistre la version anonymisée et dis-le.
- `lexique` : termes de la classe à garder partout, dans toutes les productions.
- Un champ nouveau seulement si une info stable ne rentre nulle part (ex. `rituels: "calcul mental tous les matins 15 min"`), en restant court.
- Garde le YAML valide (guillemets autour des chaînes qui contiennent `:` ou `#`). Si PyYAML est installé, vérifie après écriture : `python -c "import yaml; yaml.safe_load(open('data/classe.yaml', encoding='utf-8'))"`.

## 4. Suivi individuel — `data/suivi/<code>.md` (seulement à la demande du prof)

Un fichier par code d'élève (ex. `data/suivi/E03.md`), une ligne par observation :

```markdown
# E03 — CE2

- 2026-10-02 · Lecture · fluence · 58 mots/min sur un texte de CE2 · entraînement quotidien en binôme
```

Format d'une ligne : date · domaine · compétence · observation · mesure prise. Des observations et des besoins, jamais de diagnostic ni de conclusion sur la personne. Même codées, ce sont des données personnelles : dossier local, jamais publié.
