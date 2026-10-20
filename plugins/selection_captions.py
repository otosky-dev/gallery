"""Légendes, titres et ordre des photos lus dans selection_galerie.md.

Chaque dossier d'album peut contenir un fichier ``selection_galerie.md`` avec :

- un titre ``# Nom de l'album — ...`` (la partie avant le tiret long devient
  le titre de l'album) ;
- facultatif, juste sous le titre : ``Ordre : 1`` (position de l'album sur
  l'accueil) et ``Légende : 30 août 2026`` (petite ligne affichée sous le
  titre de l'album, par exemple les dates de prise de vue) ;
- un paragraphe d'introduction (sa première phrase devient la description) ;
- un ou plusieurs tableaux ``| # | Fichier | ... |``. La colonne qui suit
  ``Fichier`` donne le titre de la photo ; la suivante, s'il y en a une, sa
  description. Sinon, la description est le sous-titre ``## ...`` du tableau.

L'ordre des lignes des tableaux fixe l'ordre des photos dans l'album.
Un ``index.md`` (album) ou ``<photo>.md`` (photo), au format Sigal habituel,
reste prioritaire sur ce fichier.
"""

import os
import re

from sigal import signals

SELECTION_FILE = "selection_galerie.md"
CODE_RE = re.compile(r"P\d{7}")
EDITOR_NOTE_RE = re.compile(r"\s*\*\([^)]*\)\*")
POSITION_NOTE_RE = re.compile(r"\s+—\s+(ouverture|fin)$", re.IGNORECASE)
ALBUM_META_RE = re.compile(r"^(Ordre|Légende)\s*:\s*(.+)$", re.IGNORECASE)


def _clean(text):
    text = EDITOR_NOTE_RE.sub("", text).strip()
    return POSITION_NOTE_RE.sub("", text).strip()


def parse_selection(path):
    title = intro = section = header = None
    album_meta = {}
    photos = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# ") and title is None:
                title = line[2:].strip()
            elif line.startswith("## "):
                section = line[3:].strip()
                header = None
            elif line.startswith("|"):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if header is None:
                    header = cells
                elif not set("".join(cells)) <= set("-: "):
                    row = dict(zip(header, cells))
                    code = CODE_RE.search(row.get("Fichier", ""))
                    others = [c for c in header if c not in ("#", "Fichier")]
                    if code and others:
                        photos.append({
                            "code": code.group(),
                            "title": _clean(row.get(others[0], "")),
                            "description": _clean(row.get(others[1], ""))
                            if len(others) > 1 else (section or ""),
                        })
            else:
                header = None
                meta = ALBUM_META_RE.match(line)
                if meta and section is None and intro is None:
                    album_meta[meta.group(1).lower()] = meta.group(2).strip()
                elif line and title and intro is None and section is None:
                    intro = line

    album_title = re.split(r"\s+—\s+", title)[0] if title else None
    album_description = intro.split(". ")[0].rstrip(".") + "." if intro else None
    return album_title, album_description, album_meta, photos


def _media_code(media):
    match = CODE_RE.search(media.src_filename)
    return match.group() if match else None


def album_initialized(album):
    # Lu par albums_sort_attr = "album_order" (sigal.conf.py) : les albums
    # sans « Ordre » passent après les autres, par nom.
    album.album_order = "9999 " + album.name
    album.legend = ""

    path = os.path.join(album.src_path, SELECTION_FILE)
    if not os.path.isfile(path):
        return
    album_title, album_description, album_meta, photos = parse_selection(path)

    order = album_meta.get("ordre", "")
    if order.isdigit():
        album.album_order = f"{int(order):04d}"
    album.legend = album_meta.get("légende", "")

    if not os.path.isfile(album.markdown_metadata_filepath):
        if album_title:
            album.title = album_title
        if album_description:
            album.description = album_description

    by_code = {p["code"]: (i, p) for i, p in enumerate(photos)}
    album.selection_order = {code: i for code, (i, _) in by_code.items()}
    for media in album.medias:
        entry = by_code.get(_media_code(media))
        if entry is None or os.path.isfile(media.markdown_metadata_filepath):
            continue
        _, photo = entry
        media.title = photo["title"]
        media.description = photo["description"]


def medias_sorted(album):
    order = getattr(album, "selection_order", None)
    if order:
        album.medias.sort(key=lambda m: order.get(_media_code(m), len(order)))


def register(settings):
    signals.album_initialized.connect(album_initialized)
    signals.medias_sorted.connect(medias_sorted)
