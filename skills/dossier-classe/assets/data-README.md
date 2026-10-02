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
