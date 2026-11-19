#!/usr/bin/env python3
"""Render the front-page image (1024x1024 PNG) from stories.json.

Design: "Collage Zine" — tilted, overlapping zine-style cards with washi
tape, a dusk-skyline photo card, and a lead card. Chosen by the user on
2026-11-19 from 29 variants built in the competition session (batch 4,
news3_variants.py, 06-collage).

Offline, deterministic: same stories.json -> same PNG bytes. Fonts are
bundled in fonts/ (Merriweather, SIL Open Font License 1.1) so rendering
needs no network and no system fonts.
Run:  python3 render.py   (writes entry.png next to this file)

Layout:
  masthead line + two tape strips
  lead card (tilted -1.5 deg) + photo card (tilted +2 deg)
  six continent cards (tilted -2..+2 deg, overlapping like a zine)
  footer line (story count)
"""

import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
W, H = 1024, 1024

MERRIWEATHER = {
    "r": "merriweather-v33-latin-regular.ttf",
    "b": "merriweather-v33-latin-700.ttf",
    "x": "merriweather-v33-latin-900.ttf",
}


def F(weight, size):
    try:
        return ImageFont.truetype(
            os.path.join(FONTS, MERRIWEATHER[weight]), size)
    except OSError:
        return ImageFont.load_default()


def wrap(d, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if d.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, fnt, width, fill, leading=2):
    for ln in wrap(d, text, fnt, width):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def draw_bridge(d, x, y, w, h, color, deck=True):
    """Schematic suspension/arch bridge: two towers, arc, deck line."""
    d.line([(x, y + h - 6), (x + w, y + h - 6)], fill=color, width=3)
    d.arc([x + w * 0.15, y, x + w * 0.85, y + h * 1.7], 180, 360, fill=color,
          width=3)
    for fx in (0.22, 0.5, 0.78):
        tx = x + w * fx
        d.line([(tx, y + 4), (tx, y + h - 6)], fill=color, width=3)
    if deck:
        for fx in (0.3, 0.4, 0.6, 0.7):
            d.line([(x + w * fx, y + h * 0.45), (x + w * fx, y + h - 6)],
                   fill=color, width=1)


def make_card(w, h, bg):
    img = Image.new("RGBA", (w, h), bg + (255,))
    return img, ImageDraw.Draw(img)


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)

    base = Image.new("RGB", (W, H), (238, 234, 226))
    d = ImageDraw.Draw(base)
    d.text((30, 18), "THE WORLD TODAY  ·  WEDNESDAY 18 NOVEMBER 2026",
           font=F("b", 16), fill=(40, 40, 40))
    # tape strips stuck over the two top cards
    d.rectangle([110, 66, 200, 80], fill=(255, 214, 90))
    d.rectangle([700, 60, 790, 74], fill=(255, 214, 90))

    def place(card_img, x, y, angle):
        rot = card_img.rotate(angle, expand=True, resample=Image.BICUBIC)
        base.paste(rot, (x, y), rot)

    # lead card
    card, cd = make_card(500, 290, (255, 255, 255))
    cd.rectangle([0, 0, 500, 10], fill=(165, 30, 25))
    draw_wrapped(cd, 18, 26, data["lead"]["headline"],
                 F("x", 26), 464, (25, 22, 18), leading=4)
    draw_wrapped(cd, 18, 150, data["lead"]["standfirst"],
                 F("r", 14), 464, (90, 85, 75), leading=3)
    cd.text((18, 252), "— the top story", font=F("b", 13),
            fill=(165, 30, 25))
    place(card, 28, 72, -1.5)
    # photo card: skyline + bridge
    pcard, pd = make_card(420, 260, (24, 44, 96))
    for yy in range(0, 260):
        t = yy / 260
        c = tuple(int(a + (b - a) * t) for a, b in
                  zip((24, 44, 96), (232, 120, 60))) + (255,)
        pd.line([(0, yy), (420, yy)], fill=c)
    pd.ellipse([300, 20, 380, 100], fill=(255, 214, 90, 255))
    for bx, bw, bh in [(0, 60, 140), (70, 50, 180), (130, 70, 120),
                       (210, 55, 160), (290, 70, 200), (360, 60, 130)]:
        pd.rectangle([bx, 260 - bh, bx + bw, 260], fill=(16, 20, 40, 255))
    draw_bridge(pd, 110, 170, 200, 70, (255, 255, 255, 255))
    place(pcard, 560, 66, 2)
    # continent cards
    spots = [(28, 392, 300, 260, 1.0, 0), (348, 382, 300, 272, -2.0, 1),
             (668, 352, 322, 262, 1.5, 2), (28, 682, 310, 272, -1.0, 3),
             (358, 682, 300, 272, 2.0, 4), (678, 642, 312, 282, -1.5, 5)]
    colors = [(165, 30, 25), (0, 90, 160), (0, 120, 60),
              (150, 60, 0), (110, 40, 130), (0, 120, 120)]
    for x, y, w, h, ang, i in spots:
        sec = data["sections"][i]
        card, cd = make_card(w, h, (255, 255, 255))
        cd.rectangle([0, 0, w, 8], fill=colors[i])
        cd.text((14, 18), sec["continent"].upper(),
                font=F("b", 14), fill=colors[i])
        hy = 46
        for hl in sec["headlines"][:6]:
            hy = draw_wrapped(cd, 14, hy, hl, F("r", 12),
                              w - 28, (30, 30, 30), leading=1)
            hy += 2
        place(card, x, y, ang)
    d.text((30, 992), "36 stories  ·  6 continents  ·  18 Nov 2026",
           font=F("r", 12), fill=(120, 115, 105))

    out = os.path.join(HERE, "entry.png")
    base.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
