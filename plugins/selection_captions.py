"""Légendes, titres et ordre des photos lus dans selection_galerie.md.

Chaque dossier d'album peut contenir un fichier ``selection_galerie.md`` avec :

- un titre ``# Nom de l'album — ...`` (la partie avant le tiret long devient
  le titre de l'album) ;
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


def _clean(text):
    text = EDITOR_NOTE_RE.sub("", text).strip()
    return POSITION_NOTE_RE.sub("", text).strip()


def parse_selection(path):
    title = intro = section = header = None
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
                if line and title and intro is None and section is None:
                    intro = line

    album_title = re.split(r"\s+—\s+", title)[0] if title else None
    album_description = intro.split(". ")[0].rstrip(".") + "." if intro else None
    return album_title, album_description, photos


def _media_code(media):
    match = CODE_RE.search(media.src_filename)
    return match.group() if match else None


def album_initialized(album):
    path = os.path.join(album.src_path, SELECTION_FILE)
    if not os.path.isfile(path):
        return
    album_title, album_description, photos = parse_selection(path)

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
