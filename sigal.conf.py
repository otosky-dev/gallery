# Configuration Sigal de la galerie.
# Les commandes (sigal build / sigal serve) se lancent depuis ce dossier "src".

# Titre affiché en haut de chaque page.
title = "Galerie photo"
author = ""
html_language = "fr"

# Les albums sont les dossiers voisins de "src" (un dossier = une bibliothèque).
source = ".."
# Sigal refuse d'écrire dans le dossier source : le site généré va donc dans
# un dossier voisin de "gallery" (ex. C:\Users\thiba\source\repos\gallery_site).
destination = "../../gallery_site"

# On n'explore pas le code ni les dossiers techniques.
# (".?*" et non ".*", qui exclurait aussi la racine ".")
ignore_directories = ["src", "src/*", ".?*", ".?*/*"]

theme = "theme"

# Les photos sont publiées telles quelles (déjà exportées pour le web) :
# pas de redimensionnement ni de recompression, seules les miniatures sont générées.
# Les fichiers sont copiés avec leurs EXIF.
use_orig = True

# Miniatures recadrées pour une grille régulière.
make_thumbs = True
thumb_dir = "thumbnails"
thumb_size = (480, 320)
thumb_fit = True
jpg_options = {"quality": 85, "optimize": True, "progressive": True}

# Ordre des albums (« Ordre : n » dans selection_galerie.md) et des photos
# (ordre des tableaux), fixés par le plugin.
albums_sort_attr = "album_order"
medias_sort_attr = "filename"

# Plugin maison : légendes, titres et ordre lus dans selection_galerie.md.
plugin_paths = ["plugins"]
plugins = ["selection_captions"]

# Ni carte ni archive zip.
show_map = False
zip_gallery = False
