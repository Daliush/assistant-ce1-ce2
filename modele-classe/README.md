# Ma classe — espace de travail

Dossier de travail d'une classe, à utiliser avec le plugin **assistant-ce1-ce2**.
Un dossier par classe (ou par année) : copiez ce modèle et renommez-le, par exemple `classe-2026-2027`.

## Démarrer

1. Installez le plugin une fois pour toutes : https://github.com/Daliush/assistant-ce1-ce2#installation
2. Ouvrez ce dossier dans Claude Code (`cd classe-2026-2027 && claude`), acceptez la demande de confiance la première fois, puis demandez, en français :
   « Fais-moi une dictée pour mes CE2 sur les pluriels en -aux. »

Rien n'est à remplir pour commencer.

## Ce qu'il y a ici

```
classe-2026-2027/
├── CLAUDE.md               # dit à l'assistant d'utiliser le plugin
├── .claude/settings.json   # autorise l'écriture sans demander dans data/journal/ et sorties/
├── data/                   # la mémoire de votre classe (voir data/README.md)
│   ├── classe.yaml         # facultatif, créé quand vous dites « oui, note-le »
│   ├── journal/            # tout ce qui a été produit, mois par mois (automatique)
│   └── sequences/          # vos séquences et où vous en êtes
└── sorties/                # les PDF à imprimer
    └── src/                # leurs sources HTML (modifiables) et les aperçus
```

## Confidentialité

Pas de nom réel d'élève ni de diagnostic : codes (E01…) et adaptations seulement.
Si vous versionnez ce dossier avec git, gardez le dépôt **local ou privé**.
