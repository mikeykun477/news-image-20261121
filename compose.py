#!/usr/bin/env python3
"""Rebuild the front page for Saturday 21 November 2026 (build time only).

This script is the recipe behind ``entry.png``: it lays out the hero
illustration from ``assets/hero.png`` as a one-page newspaper front —
masthead, date line, lead story, captioned photo, then six short story
tiles — and saves the result as ``entry.png`` next to this file.

It runs on the build machine only and needs Pillow.  The entrypoint
(``main.py``) is standard-library only and simply ships the finished
picture, so nothing here ever runs at judging time.

Run from the repository root::

    python3 compose.py
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- page setup
PAGE_W, PAGE_H = 1024, 1024
MARGIN = 32
CONTENT_W = PAGE_W - 2 * MARGIN
GUTTER = 24

PALETTE = {
    "paper": (247, 243, 234),   # newsprint off-white
    "ink": (16, 16, 16),        # near-black
    "kicker": (178, 34, 34),    # kicker red
    "caption": (90, 86, 78),    # grey captions
}

FONT_FILES = {
    "serif_bold": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "sans_bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
}

BASE = os.path.dirname(os.path.abspath(__file__))
HERO_PATH = os.path.join(BASE, "assets", "hero.png")
OUTPUT_PATH = os.path.join(BASE, "entry.png")

# ------------------------------------------------------------------- content
MASTHEAD = "THE WORLD TODAY"
DATE_LINE = "SATURDAY 21 NOVEMBER 2026"

LEAD = {
    "kicker": "GULF WAR \u2014 BAHRAIN",
    "headline": "IRAN STRIKES BAHRAIN; U.S. BASES SAID HIT",
    "deck": (
        "Tehran's Guards say they hit two U.S. positions; Bahrain "
        "says a civilian industrial site burned, no one hurt, and "
        "its air defences stopped other attacks."
    ),
    "caption": (
        "Fire at an industrial site in Bahrain after Saturday's "
        "Iranian strike."
    ),
}

# Six tiles, read left to right, top row first.
TILES = [
    (
        "COP31: DEAL IN SIGHT",
        "Climate talks in Antalya run past their deadline; the summit "
        "president says a final deal is close, but the draft leaves "
        "out fossil fuels.",
    ),
    (
        "MEXICO CAPTURES \u2018EL CHAPO ISIDRO\u2019",
        "FBI most-wanted cartel boss Fausto Isidro Meza Flores seized "
        "in Sinaloa; 11 dead in the violence that followed.",
    ),
    (
        "MISSILES HIT KRYVYI RIH \u2014 AND POLAND",
        "Russian missile kills two in Zelensky's hometown and wounds "
        "dozens; missiles and a drone cross into NATO member Poland.",
    ),
    (
        "RUSSIAN SHIP BURNS IN THE GULF OF FINLAND",
        "Cargo ship Sparta II ablaze after a drone strike; crew "
        "evacuates. Finland says Ukraine is likely behind it.",
    ),
    (
        "AI SELL-OFF PUSHES STOCKS INTO CORRECTION",
        "Nasdaq's worst week since March 2020 erases its 2026 gains; "
        "Nvidia halts H200 chip exports to China.",
    ),
    (
        "IN BRIEF",
        "Dengue cut 69% in Brazil mosquito study. EU\u2013Indonesia "
        "trade deal after 10 years. Peru quake. Nigeria boat "
        "capsizes, 24 dead. Paolo Bulgari dies at 89.",
    ),
]

HERO_W, HERO_H = 960, 176

# ------------------------------------------------------------- type handling
_typeface_cache = {}


def typeface(kind, size):
    """A TrueType face, cached so each (kind, size) loads only once."""
    key = (kind, size)
    face = _typeface_cache.get(key)
    if face is None:
        face = ImageFont.truetype(FONT_FILES[kind], size)
        _typeface_cache[key] = face
    return face


def fit_words(canvas, text, face, max_width):
    """Split ``text`` into lines that fit ``max_width`` (greedy wrap)."""
    lines = []
    current = ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if canvas.textlength(candidate, font=face) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paint_lines(canvas, lines, face, x, top, leading, colour=None):
    """Draw stacked lines starting at ``top``; return the next free y."""
    y = top
    fill = PALETTE["ink"] if colour is None else colour
    for line in lines:
        canvas.text((x, y), line, font=face, fill=fill)
        y += leading
    return y


def rule(canvas, y, weight=2):
    """A full-width horizontal rule at height ``y``."""
    canvas.line([(MARGIN, y), (PAGE_W - MARGIN, y)],
                fill=PALETTE["ink"], width=weight)


def centred_text(canvas, text, face, y, colour=None):
    """Draw ``text`` centred on the page at height ``y``."""
    width = canvas.textlength(text, font=face)
    fill = PALETTE["ink"] if colour is None else colour
    canvas.text(((PAGE_W - width) / 2, y), text, font=face, fill=fill)


# ---------------------------------------------------------------- story tiles
def tile_layout(canvas, width, headline, deck, head_size=22, deck_size=17):
    """Measure a tile: its pixel height plus its wrapped headline/deck."""
    head_face = typeface("sans_bold", head_size)
    deck_face = typeface("sans", deck_size)
    head_lines = fit_words(canvas, headline, head_face, width)
    deck_lines = fit_words(canvas, deck, deck_face, width)
    height = (
        12
        + len(head_lines) * (head_size + 5)
        + 2
        + len(deck_lines) * (deck_size + 5)
    )
    return height, head_lines, deck_lines


def paint_tile(canvas, x, top, width, headline, deck):
    """One tile: top rule, bold headline, short deck underneath."""
    _, head_lines, deck_lines = tile_layout(canvas, width, headline, deck)
    canvas.line([(x, top), (x + width, top)],
                fill=PALETTE["ink"], width=2)
    y = top + 10
    y = paint_lines(canvas, head_lines, typeface("sans_bold", 22),
                    x, y, 22 + 5)
    y += 2
    paint_lines(canvas, deck_lines, typeface("sans", 17), x, y, 17 + 5)


# ------------------------------------------------------------------- sections
def paint_nameplate(canvas):
    """Masthead, centred at the top of the page."""
    centred_text(canvas, MASTHEAD, typeface("serif_bold", 64), 22)


def paint_dateline(canvas):
    """Date line between two rules; returns the y just below the lower rule."""
    y = 104
    rule(canvas, y)
    centred_text(canvas, DATE_LINE, typeface("sans_bold", 30), y + 10)
    y += 52
    rule(canvas, y)
    return y


def paint_lead(canvas, y):
    """Kicker, big headline and deck; returns the y below the deck."""
    y += 16
    canvas.text((MARGIN, y), LEAD["kicker"],
                font=typeface("sans_bold", 23), fill=PALETTE["kicker"])
    y += 34
    head_face = typeface("serif_bold", 44)
    y = paint_lines(canvas, fit_words(canvas, LEAD["headline"], head_face,
                                      CONTENT_W),
                    head_face, MARGIN, y, 51)
    y += 6
    deck_face = typeface("sans", 22)
    y = paint_lines(canvas, fit_words(canvas, LEAD["deck"], deck_face,
                                      CONTENT_W),
                    deck_face, MARGIN, y, 29)
    return y


def paint_hero(canvas, page, y):
    """Hero photo, cropped to a wide band, with its caption below."""
    y += 12
    photo = Image.open(HERO_PATH).convert("RGB")
    scaled = photo.resize((HERO_W, int(HERO_W * photo.height / photo.width)),
                          Image.LANCZOS)
    crop_top = max(0, (scaled.height - HERO_H) // 2 - 40)
    band = scaled.crop((0, crop_top, HERO_W, crop_top + HERO_H))
    page.paste(band, ((PAGE_W - HERO_W) // 2, y))
    y += HERO_H + 8
    canvas.text((MARGIN, y), LEAD["caption"],
                font=typeface("serif", 18), fill=PALETTE["caption"])
    return y + 24


def paint_story_grid(canvas, y):
    """Two-column, three-row grid of story tiles; returns the final y."""
    rule(canvas, y)
    y += 6
    col_width = (CONTENT_W - GUTTER) // 2
    for row in range(3):
        pair = TILES[row * 2:row * 2 + 2]
        row_height = max(
            tile_layout(canvas, col_width, head, deck)[0]
            for head, deck in pair
        )
        for col, (headline, deck) in enumerate(pair):
            paint_tile(canvas, MARGIN + col * (col_width + GUTTER),
                       y, col_width, headline, deck)
        y += row_height + 8
    return y


def build_page():
    """Compose the whole front page and return the finished image."""
    page = Image.new("RGB", (PAGE_W, PAGE_H), PALETTE["paper"])
    canvas = ImageDraw.Draw(page)
    paint_nameplate(canvas)
    y = paint_dateline(canvas)
    y = paint_lead(canvas, y)
    y = paint_hero(canvas, page, y)
    y = paint_story_grid(canvas, y)
    if y > PAGE_H:
        raise ValueError("tiles overflow by %dpx" % (y - PAGE_H))
    return page


def verify_output(path):
    """Re-open the saved picture and confirm it is a 1024x1024 RGB PNG."""
    with Image.open(path) as check:
        check.load()
        if check.size != (PAGE_W, PAGE_H) or check.mode != "RGB":
            raise ValueError(
                "%s came back as %s %s, expected %dx%d RGB"
                % (path, check.size, check.mode, PAGE_W, PAGE_H)
            )
    if os.path.getsize(path) > 1024 * 1024:
        raise ValueError("%s is over the 1 MiB limit" % path)


def main():
    page = build_page()
    page.save(OUTPUT_PATH, optimize=True)
    verify_output(OUTPUT_PATH)
    print("wrote entry.png", page.size)


if __name__ == "__main__":
    main()
