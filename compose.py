#!/usr/bin/env python3
"""Build the front page for Saturday 21 November 2026 (build-time only).

Composes assets/hero.png into a 1024x1024 newspaper front page and
writes entry.png next to this script. Run: python3 compose.py
Requires Pillow (build machine only -- main.py is stdlib-only).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)      # newsprint off-white
INK = (16, 16, 16)           # near-black
RED = (178, 34, 34)          # kicker red
GREY = (90, 86, 78)          # captions
RULE = (16, 16, 16)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, leading, fill=INK):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tile_height(draw, w, head, deck, head_size=22, deck_size=17):
    """Height a tile needs: rule + headline lines + deck lines."""
    hf = font(SANS_B, head_size)
    df = font(SANS, deck_size)
    h_lines = wrap(draw, head, hf, w)
    d_lines = wrap(draw, deck, df, w)
    height = 12 + len(h_lines) * (head_size + 5) + 2 + len(d_lines) * (deck_size + 5)
    return height, h_lines, d_lines


def tile(draw, x, y, w, head, deck, head_size=22, deck_size=17):
    """One story tile: bold headline + short deck, with a top rule."""
    _, h_lines, d_lines = tile_height(draw, w, head, deck, head_size, deck_size)
    draw.line([(x, y), (x + w, y)], fill=RULE, width=2)
    y += 10
    hf = font(SANS_B, head_size)
    y = draw_lines(draw, h_lines, hf, x, y, head_size + 5)
    y += 2
    df = font(SANS, deck_size)
    draw_lines(draw, d_lines, df, x, y, deck_size + 5)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)
    mx = 32                      # side margin
    cw = W - 2 * mx              # content width

    # ---- Nameplate -------------------------------------------------
    name_f = font(SERIF, 64)
    name = "THE WORLD TODAY"
    nw = draw.textlength(name, font=name_f)
    draw.text(((W - nw) / 2, 22), name, font=name_f, fill=INK)

    # ---- Date line -------------------------------------------------
    y = 104
    draw.line([(mx, y), (W - mx, y)], fill=RULE, width=2)
    date_f = font(SANS_B, 30)
    date = "SATURDAY 21 NOVEMBER 2026"
    dw = draw.textlength(date, font=date_f)
    draw.text(((W - dw) / 2, y + 10), date, font=date_f, fill=INK)
    y = y + 52
    draw.line([(mx, y), (W - mx, y)], fill=RULE, width=2)

    # ---- Lead story ------------------------------------------------
    y += 16
    kick_f = font(SANS_B, 23)
    draw.text((mx, y), "GULF WAR \u2014 BAHRAIN", font=kick_f, fill=RED)
    y += 34
    head_f = font(SERIF, 44)
    headline = "IRAN STRIKES BAHRAIN; U.S. BASES SAID HIT"
    y = draw_lines(draw, wrap(draw, headline, head_f, cw),
                   head_f, mx, y, 51)
    y += 6
    deck_f = font(SANS, 22)
    deck = ("Tehran's Guards say they hit two U.S. positions; Bahrain "
            "says a civilian industrial site burned, no one hurt, and "
            "its air defences stopped other attacks.")
    y = draw_lines(draw, wrap(draw, deck, deck_f, cw), deck_f, mx, y, 29)

    # ---- Hero photo ------------------------------------------------
    y += 12
    hero = Image.open("assets/hero.png").convert("RGB")
    hw, hh = 960, 176
    hero = hero.resize((hw, int(hw * hero.height / hero.width)),
                       Image.LANCZOS)
    top = max(0, (hero.height - hh) // 2 - 40)
    hero = hero.crop((0, top, hw, top + hh))
    page.paste(hero, ((W - hw) // 2, y))
    y += hh + 8
    cap_f = font(SERIF_REG, 18)
    draw.text((mx, y),
              "Fire at an industrial site in Bahrain after Saturday's Iranian strike.",
              font=cap_f, fill=GREY)
    y += 24

    # ---- Story tiles, two columns x three rows --------------------
    draw.line([(mx, y), (W - mx, y)], fill=RULE, width=2)
    y += 6
    col_w = (cw - 24) // 2
    tiles = [
        ("COP31: DEAL IN SIGHT",
         "Climate talks in Antalya run past their deadline; the summit "
         "president says a final deal is close, but the draft leaves "
         "out fossil fuels."),
        ("MEXICO CAPTURES \u2018EL CHAPO ISIDRO\u2019",
         "FBI most-wanted cartel boss Fausto Isidro Meza Flores seized "
         "in Sinaloa; 11 dead in the violence that followed."),
        ("MISSILES HIT KRYVYI RIH \u2014 AND POLAND",
         "Russian missile kills two in Zelensky's hometown and wounds "
         "dozens; missiles and a drone cross into NATO member Poland."),
        ("RUSSIAN SHIP BURNS IN THE GULF OF FINLAND",
         "Cargo ship Sparta II ablaze after a drone strike; crew "
         "evacuates. Finland says Ukraine is likely behind it."),
        ("AI SELL-OFF PUSHES STOCKS INTO CORRECTION",
         "Nasdaq's worst week since March 2020 erases its 2026 gains; "
         "Nvidia halts H200 chip exports to China."),
        ("IN BRIEF",
         "Dengue cut 69% in Brazil mosquito study. EU\u2013Indonesia "
         "trade deal after 10 years. Peru quake. Nigeria boat "
         "capsizes, 24 dead. Paolo Bulgari dies at 89."),
    ]
    for row in range(3):
        pair = tiles[row * 2:row * 2 + 2]
        row_h = max(tile_height(draw, col_w, h, d)[0] for h, d in pair)
        for col, (head, deck) in enumerate(pair):
            tx = mx + col * (col_w + 24)
            tile(draw, tx, y, col_w, head, deck)
        y += row_h + 8
    assert y <= H, "tiles overflow by %dpx" % (y - H)

    page.save("entry.png", optimize=True)
    print("wrote entry.png", page.size)


if __name__ == "__main__":
    main()
