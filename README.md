# Galerie photo

Site statique généré avec [Sigal](https://sigal.readthedocs.io/) à partir des
dossiers de photos voisins de ce dossier `src`.

```
gallery\
├── Traversée de Vallons-de-l'Erdre 2026\   ← une bibliothèque (album)
│   ├── 01_P1020001_web.jpg …
│   └── selection_galerie.md                ← titres, légendes et ordre
├── Week-end en Bretagne\
│   └── …
└── src\                                    ← ce dossier
    ├── sigal.conf.py                       ← configuration
    ├── plugins\selection_captions.py       ← lit selection_galerie.md
    └── theme\                              ← thème PhotoSwipe adapté
```

Le site généré est écrit dans `..\..\gallery_site` (à côté de `gallery`),
car Sigal refuse d'écrire à l'intérieur du dossier des photos.

## Installation (une fois)

Avec Python 3.10 ou plus récent, depuis `gallery\src` :

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

Pas besoin d'activer le venv (PowerShell bloque `Activate.ps1` par défaut) :
on appelle directement les exécutables de `.venv\Scripts`.

## Générer et voir la galerie

```powershell
.\.venv\Scripts\sigal build      # génère ..\..\gallery_site
.\.venv\Scripts\sigal serve -b   # l'ouvre sur http://127.0.0.1:8000
```

`sigal build` ne retraite que les photos nouvelles ou modifiées.
Pour tout régénérer : `.\.venv\Scripts\sigal build -f`.

## Ajouter une bibliothèque

1. Créer un dossier dans `gallery` : son nom sert de titre par défaut.
2. Y mettre les photos (exportées en JPEG, 2560 px max suffit).
3. Facultatif : un `selection_galerie.md` sur le même modèle que les existants.
4. Relancer `sigal build`.

## Titres et légendes

Le plugin `selection_captions` lit `selection_galerie.md` dans chaque album :

| Élément du .md | Devient |
|---|---|
| `# Nom — sélection pour la galerie` | Titre de l'album (partie avant « — ») |
| Première phrase du paragraphe d'intro | Description de l'album |
| Colonne après `Fichier` | Titre de la photo |
| Colonne suivante, sinon le titre `## …` du tableau | Description de la photo |
| Ordre des lignes | Ordre des photos |

La photo est reconnue par son code `P1020xxx` dans le nom du fichier.
Les notes `*(…)*` et les mentions « — ouverture » / « — fin » sont retirées.

La légende s'affiche au survol de la miniature (toujours visible sur
téléphone) et à côté ou sous la photo agrandie.

Pour écrire une légende à la main, le format Sigal standard reste prioritaire :
un `index.md` dans l'album, ou un `<nom_de_la_photo>.md` à côté d'une photo :

```markdown
Title: Citroën 2CV jaune
Une touche de couleur joyeuse.
```

## Mise en ligne (plus tard)

Prévu : Cloudflare Pages, gratuit, sur un sous-domaine OVH.

```powershell
npx wrangler pages deploy ..\..\gallery_site --project-name galerie
```

Puis, côté OVH, un enregistrement CNAME `photos` → `galerie.pages.dev`.
