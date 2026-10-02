# Formats des fichiers de data/ et de sorties/

## 0. Codes communs (référence unique, utilisée partout)

| Élément | Codes |
|---|---|
| Niveau | `CE1`, `CE2`, `CE1-CE2` |
| Matière (noms de fichiers) | `fr`, `maths`, `qlm`, `emc`, `evar`, `lve`, `arts`, `eps`, `multi` (journée, semaine) |
| Matière (texte du journal) | Français, Maths, QLM, EMC, EVAR, LVE, Arts, EPS, Toutes matières |
| Domaine | mot court sans accent : `lecture`, `ecriture`, `dictee`, `oral`, `vocabulaire`, `grammaire`, `conjugaison`, `orthographe`, `culture`, `poesie`, `numeration`, `calcul`, `problemes`, `fractions`, `grandeurs`, `geometrie`, `donnees`… |
| Type (fichier et journal) | `cours`, `lecon`, `exercice`, `dictee`, `lecture`, `problemes`, `atelier`, `plan-travail`, `seance-N` (N = numéro dans la séquence) ou `seance`, `sequence`, `programmation`, `journee`, `semaine`, `evaluation`, `affichage`, `etiquettes`, `diaporama` |
| Variante (fichier seulement) | `_prep`, `_fiche` (feuille élève), `_corrige`, `_lecon`, `_allegee` (moins de contenu), `_adapte` (même contenu, forme adaptée : police agrandie…), `_projection` |

- **Nom de fichier** : `sorties/AAAA-MM-JJ_<niveau>_<matiere>-<domaine>_<type>[_variante].<ext>` ; pour une journée ou une semaine : `AAAA-MM-JJ_CE1-CE2_multi_journee.pdf`.
- **Séance d'une séquence** : tous ses documents portent le type `seance-N` et la variante dit ce que c'est : `…_fr-grammaire_seance-2_prep.pdf`, `…_CE1_fr-grammaire_seance-2_fiche.pdf`, `…_seance-2_fiche_corrige.pdf`. Ainsi deux séances le même jour ne s'écrasent jamais.
- **Date du nom de fichier** = date d'utilisation en classe si elle est connue (journée du 8 octobre → `2026-10-08`), sinon date de production. Le journal, lui, est toujours classé par **date de production**.
- **Séquence** : `data/sequences/<P>_<matiere>_<domaine>_<titre-court>.md`, avec les mêmes codes (ex. `P1_fr_grammaire_la-phrase.md`).
- Aperçus PNG et sources HTML : dans `sorties/src/`, jamais à côté des PDF.

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

Format d'une entrée :
`- <niveau> · <Matière> · <Domaine> · <type> · « <titre court> »` puis, en retrait, les fichiers produits et, s'il y en a une, la séquence liée.

- **niveau**, **Matière**, **type** : codes du §0. Le corrigé, la prep et la version adaptée sont listés sous l'entrée de leur document, pas comme entrées séparées.
- Écrite **après** la création des fichiers, avec leurs chemins réels. Une entrée par production du tour (si tu as produit une dictée puis des problèmes, deux entrées).
- Pas de statut, pas de commentaire sur la qualité.

## 2. Séquence — `data/sequences/<P>_<matiere>_<domaine>_<slug>.md`

Nom : période prévue, code matière (§0), domaine, titre court en minuscules avec tirets. Exemple : `P1_fr_grammaire_la-phrase.md`.

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
- **CE1** : « Reconnaître et utiliser les trois types de phrases, en lien avec la ponctuation : déclarative, interrogative et impérative. » (`programme-cycle2/references/francais/ce1.md`)
- **CE2** : « Utiliser la ponctuation de fin de phrase (. ! ?) et reconnaître les marques du discours rapporté. » (`francais/ce2.md`)

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
- Séquence pour un seul niveau : `niveaux: [CE2]`, `statut: {CE2: prevue}`, colonnes de l'autre niveau supprimées (une seule colonne « Statut »).
- `maj` : date de la dernière mise à jour d'un statut ; sert à repérer une séquence oubliée (> 3 semaines).

## 3. Classe — `data/classe.yaml`

**Tous les champs sont facultatifs.** Ne crée que ceux que le prof a donnés. Exemple complet (une vraie classe en aura beaucoup moins au début) :

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
- `progression` : **une phrase par matière** (et par niveau en français, maths, EMC). Réécrite (pas complétée) quand une séquence se termine ou quand le prof la corrige.
- `eleves` : **aucun nom réel, aucun diagnostic**. Seulement `id` (ou pseudonyme), `niveau`, `groupes`, `adaptations`.
- `sons_etudies_CE1` : précieux pour les textes de lecture CE1 ; c'est la seule info qui justifie une relance.
- `soustraction_posee` : algorithme de l'école (`cassage` ou `compensation`), utile en maths.
- Ajoute un champ nouveau si le prof donne une info stable qui ne rentre nulle part (ex. `rituels: "calcul mental tous les matins 15 min"`), en restant court.
