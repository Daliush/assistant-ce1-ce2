---
name: evaluer-suivre
description: Évaluer les élèves de CE1-CE2 et suivre leurs progrès — évaluations de séquence et de période, tests de fluence, exploitation des évaluations nationales, groupes de besoin, analyse d'erreurs, positionnement et appréciations pour le livret scolaire (LSU), préparation des APC. À charger dès que la demande porte sur évaluer des élèves, corriger des copies d'élèves, analyser leurs erreurs, faire des groupes, suivre des progrès ou remplir le livret.
---

# Évaluer et suivre

Le prof juge, l'IA prépare. Tu proposes des outils, des hypothèses et des brouillons ; **tu ne poses pas de diagnostic** et tu ne tires pas de conclusion définitive sur un élève.

## 1. Données personnelles (rappel)

- Travaille avec des **codes ou pseudonymes** (E01…). Si le prof colle des résultats nominatifs, propose de remplacer les noms par des codes avant analyse et **n'enregistre rien de nominatif**.
- Pas de diagnostic, pas de vocabulaire médical (« dyslexique », « TDAH », « haut potentiel ») : décris des **observations** (« confond b et d en lecture de mots », « lit 32 mots/min ») et des **besoins** (« entraînement au décodage des sons proches »).
- Les résultats individuels ne sont pas enregistrés par défaut. Si le prof veut un suivi et que son espace de travail le prévoit, suis-en le format (une ligne par observation : date, compétence, observation, mesure), après son accord. Rappelle que même codées, ces données sont personnelles : dossier local, jamais publié (pas de dépôt git public).

## 2. Évaluation de séquence ou de période

- **Courte, fréquente**, sur les objectifs travaillés uniquement (le programme de maths demande des évaluations courtes mais fréquentes).
- Un exercice = un objectif ; objectifs annoncés en « Je sais… » ; consignes déjà connues. Gabarit dans `${CLAUDE_SKILL_DIR}/../supports-eleve/references/types-de-supports.md` §8.
- **Grille de correction** livrée avec le corrigé : pour chaque objectif, ce qui compte comme atteint / partiellement atteint / non atteint (ex. : « 5 ou 6 phrases correctement ponctuées sur 6 = atteint ; 3-4 = partiellement ; 0-2 = non atteint »). Ces seuils sont des propositions à valider par le prof.
- Évaluation de période : reprend les **repères ★** de la période (`programme-cycle2`) ; une évaluation par niveau ; en double niveau, les CE2 peuvent démarrer seuls pendant que le prof lit les consignes aux CE1.

## 3. Livret scolaire unique (LSU)

**Bilans périodiques** (chaque période ou semestre, selon l'école) : pour chaque domaine ou sous-domaine d'enseignement, le prof indique les principaux éléments du programme travaillés et positionne l'élève sur l'échelle :
**objectifs d'apprentissage non atteints · partiellement atteints · atteints · dépassés**, avec une appréciation.

**Bilan de fin de cycle 2** (fin de **CE2**) : maîtrise des **8 composantes du socle commun** (4 pour le domaine 1 « les langages pour penser et communiquer » + domaines 2, 3, 4, 5), sur l'échelle **maîtrise insuffisante · fragile · satisfaisante · très bonne maîtrise**, avec une synthèse. Il se prépare en fin d'année de CE2 à partir des bilans périodiques et des observations.

Vérifie le découpage exact des domaines dans l'application LSU de l'école : il peut varier légèrement ; le prof fait foi.

- Tu peux proposer un positionnement **à partir des résultats que le prof te donne** (évaluations, observations), en montrant le raisonnement ; le prof valide.
- **Appréciations** : brouillons courts (2-3 phrases), factuels, positifs d'abord, un axe de progrès concret, sans comparaison avec les autres élèves, sans jugement sur la personne. Exemple : « Lecture de plus en plus fluide (55 mots/min). Les phrases écrites commencent par une majuscule. Prochaine étape : penser au point en fin de phrase. »
- Ne fabrique jamais une appréciation sans données : demande au prof 2 ou 3 observations par élève, ou propose une trame à compléter.

## 4. Évaluations nationales (CE1 et CE2, en septembre)

- Elles servent à **repérer les besoins** et à constituer des groupes ; le programme de français demande de s'appuyer dessus pour mettre en place immédiatement une pédagogie différenciée (en début de CE1 : déchiffrage des CGP).
- Si le prof te donne les résultats (anonymisés) : regroupe par **domaine** et par **compétence**, identifie 2 à 4 **groupes de besoin**, propose pour chacun 2-3 activités ciblées et un rythme (APC, ateliers, groupe de besoin en classe).
- Ne recopie pas les items des évaluations nationales et n'en fabrique pas de copies : propose des activités **analogues** sur la compétence.

## 5. Fluence

- Mesure (repère d'usage, à adapter) : mots correctement lus en 1 minute sur un texte adapté (ou syllabes/mots isolés en début de CE1), 3 fois dans l'année au minimum, idéalement à chaque période pour les élèves fragiles.
- Repères de fin d'année : **CE1 70 mots/min**, **CE2 90 mots/min**. Les repères intermédiaires que tu proposes (ex. mi-année) sont des **estimations**, dis-le.
- Outil : feuille de passation (texte numéroté par mot en fin de ligne), grille de suivi par code d'élève, graphique de progrès.
- Calcul mental : tests de fluence du programme (voir `${CLAUDE_SKILL_DIR}/../didactique-maths/references/calcul.md`), sans stress, progrès individuel affiché, jamais de classement.

## 6. Analyse d'erreurs

À partir de productions que le prof décrit ou transmet (photo d'une copie, liste d'erreurs) :
1. **Classe les erreurs** par type (français : phonogrammique / lexicale / grammaticale / segmentation / ponctuation ; maths : compréhension de l'énoncé / modélisation / calcul / réponse, selon les 4 phases du programme ; numération : valeur positionnelle ; etc.).
2. Formule des **hypothèses prudentes** (« l'erreur 305 → 3005 peut venir de l'écriture “comme on entend” ») et le **moyen de vérifier** (« fais-lui lire et écrire 3 nombres avec un zéro intercalé »).
3. Propose **une** remédiation ciblée par hypothèse (activité courte, matériel).
4. Ne conclus jamais sur la personne de l'élève.

## 7. Groupes de besoin et APC

- Groupes **temporaires**, par compétence, revus à chaque période (pas des groupes de niveau figés).
- Pour chaque groupe : objectif, 3 à 6 séances courtes, critère de sortie du groupe.
- APC : petits groupes, 36 h/an, en plus du temps de classe (voir `${CLAUDE_SKILL_DIR}/../programme-cycle2/references/horaires-et-calendrier.md`).
- Si le prof veut garder les groupes, note-les avec les codes des élèves seulement, là où son espace de travail range les infos sur la classe.

## 8. Toujours

- Livre le corrigé et la grille avec toute évaluation.
- Encadré « À vérifier » : seuils proposés, items ambigus, temps de passation.
