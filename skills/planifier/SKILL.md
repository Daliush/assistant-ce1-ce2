---
name: planifier
description: Organiser l'enseignement en CE1, CE2 ou CE1-CE2 — programmation de période, séquence, séance, journée, semaine, cahier journal, gestion du double niveau (qui est avec le prof, qui est en autonomie), et choix du format d'activité quand la demande est ouverte (« j'ai besoin d'un exercice de culture littéraire pour mes CE1 »). À charger dès qu'il faut décider quoi faire, dans quel ordre, combien de temps et avec quelle organisation.
---

# Planifier

Ce skill décide **quoi, dans quel ordre, combien de temps et avec quelle organisation**. Le contenu didactique vient de `didactique-francais` ou `didactique-maths`, les attendus de `programme-cycle2`, les fiches de `supports-eleve`.

## 1. Repérer le niveau de planification demandé

| Demande | Ce que tu produis | Référence |
|---|---|---|
| « Que faire en P2 en maths ? », « programmation » | Programmation de période : séquences par semaine, par niveau | `references/sequence-et-seance.md` §1 |
| « Une séquence sur… », « commencer à traiter… » | Plan de séquence (4 à 8 séances) + fichier dans `data/sequences/` | `references/sequence-et-seance.md` §2 |
| « Une séance », « un cours », « la première séance » | Fiche de préparation de séance | `references/sequence-et-seance.md` §3 |
| « Organise ma journée de jeudi », « ma semaine », « cahier journal » | Emploi du temps détaillé + cahier journal | `references/journee-et-semaine.md` |
| « J'ai besoin de quelque chose pour… » (format non précisé) | 2 à 4 formats d'activité au choix, puis production de celui choisi | `references/formats-activites.md` |
| Toute séance en CE1-CE2 | Organisation minute par minute des deux groupes | `references/double-niveau.md` |

**Séquence avant séance** : si le prof demande une séance sur une notion nouvelle, propose d'abord en 5 lignes le plan de la séquence (objectif final, nombre de séances), puis détaille la séance demandée. Ne bloque pas : la séance est produite dans la même réponse.

## 2. Demande ouverte : proposer, puis produire

Quand le prof ne précise pas le format (« un exercice de culture littéraire pour mes CE1 »), propose **2 à 4 formats adaptés** en une ligne chacun (durée, organisation, matériel), avec ta recommandation en premier. Exemple :

> Pour tes CE1 en culture littéraire, je te propose :
> 1. **(Recommandé)** Lecture offerte d'un conte de Grimm + questionnaire de compréhension en images (30 min, collectif puis individuel)
> 2. Carte d'identité d'un personnage (20 min, autonomie, après une lecture déjà faite)
> 3. Mise en réseau : trier 6 couvertures inventées par type de récit (conte, fable, documentaire) (20 min, binômes)
>
> Je pars sur lequel ?

Si le prof est pressé ou dit « fais au mieux », produis directement le format recommandé et dis-le en une ligne. Catalogue complet : `references/formats-activites.md`.

## 3. Règles de planification

- **Partir du programme** : objectifs cités, repères ★ de la période en cours, listes fermées.
- **Partir de ce qui existe** : `classe.yaml` (progression, contraintes d'emploi du temps), séquences en cours, journal (supports déjà produits, à réutiliser).
- **Prérequis** : vérifie ce que l'élève est censé savoir (niveau précédent dans `programme-cycle2`, ou année précédente : CP pour les CE1, CE1 pour les CE2). Si un prérequis est fragile, prévois une activité de rappel courte, pas une séquence de révision.
- **Nouvelle notion de langue** : la première séance est une séance d'**observation et de manipulation** (corpus, tri, transformation), pas un cours magistral suivi d'une trace écrite. La trace écrite vient quand les élèves ont formulé la règle (souvent séance 2 ou 3).
- **Maths** : manipuler, représenter, abstraire (concret → imagé → symbolique) ; calcul mental chaque jour ; problèmes chaque jour (≥ 10 par semaine).
- **Français** : dictée chaque jour, vocabulaire chaque jour en séance distincte de la grammaire, lecture chaque jour.
- **Durées réalistes** : CE1 en début d'année ≈ 15-20 min d'attention sur une même tâche ; une séance de 45 min contient au moins deux phases différentes.
- **Horaires officiels** : respecte la grille (voir `${CLAUDE_SKILL_DIR}/../programme-cycle2/references/horaires-et-calendrier.md`) quand tu construis une semaine ; signale un écart important plutôt que de le corriger d'autorité.
- **Différenciation** : prévois pour chaque séance un **étayage** (pour ceux qui bloquent) et un **prolongement** (pour ceux qui ont fini), pas trois fiches différentes.

## 4. Classe à double niveau

Lis `references/double-niveau.md` pour toute séance CE1-CE2. L'essentiel :

- Écris toujours la séance en **deux colonnes CE1 / CE2** avec les mêmes tranches horaires, et indique pour chaque tranche **où est le prof** (●).
- **Le prof démarre avec le groupe qui découvre** une notion nouvelle ; l'autre groupe fait une tâche **connue**.
- En début d'année, **les CE1 commencent avec le prof** ; leur autonomie porte sur une tâche qu'ils viennent de faire avec lui.
- Prévois les **transitions** (consigne de l'autonomie donnée avant de partir, signal de fin, que faire si je bloque) et une activité **« j'ai fini »**.

## 5. Après la planification

- Mode dossier : une séquence créée → fichier `data/sequences/…` (skill `etat-classe`), statut `prevue` ; une production → ligne de journal (`assistant-classe` §5).
- Mode conversation : le plan de séquence est dans la réponse, rien n'est enregistré.
- Termine par l'encadré **« À vérifier »** (durées, prérequis supposés, matériel, créneaux imposés).
