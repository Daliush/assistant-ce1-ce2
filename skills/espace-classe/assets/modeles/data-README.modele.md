# data/ — mémoire de la classe

Tout est **facultatif**, sauf le journal qui se remplit tout seul.

| Fichier | Contenu | Qui l'écrit | Quand |
|---|---|---|---|
| `classe.yaml` | Infos stables sur la classe + une ligne de progression par matière | L'assistant, **seulement après votre accord** | Au fil de l'eau (« je le note ? ») |
| `journal/AAAA-MM.md` | Tout ce qui a été préparé, une ligne par production, **sans statut** | L'assistant, automatiquement | À chaque production |
| `sequences/*.md` | Le plan de chaque séquence et le statut de ses séances | L'assistant, avec vous | Création d'une séquence ; « où en est-on ? » |
| `suivi/` (rare) | Suivi individuel par code d'élève | L'assistant, seulement si vous le demandez | — |
| `FORMATS.md` | Formats que l'assistant suit pour écrire ces fichiers | Le plugin, à chaque mise à jour de l'espace | — |

- Ces fichiers sont à vous : vous pouvez les modifier à la main, l'assistant relit avant d'écrire.
- **Aucune donnée nominative ni médicale** : pseudonymes ou codes (E01…), adaptations seulement.
- Conseil : mettre ce dossier sous git pour voir et annuler les modifications faites par l'assistant — **dépôt local ou privé uniquement**, jamais public (même codées, ce sont des données d'élèves).
