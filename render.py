#!/usr/bin/env python3
"""Build the entry image for the news-image-20261118 bounty (1024x1024 PNG).

The design is a zine collage: the lead story and a dusk-skyline photo sit
on tilted paper cards held by washi tape, with six continent cards
overlapping underneath like cuttings pinned to a board. Everything on the
page comes from ``stories.json`` in this same folder — the 36 headlines of
Wednesday 18 November 2026, grouped by continent, plus the lead story.

Run it with ``python3 render.py``; it writes ``entry.png`` next to itself.
It needs nothing from the network: the Merriweather typefaces it sets the
page in are bundled under ``fonts/`` (SIL Open Font License 1.1), and the
only third-party import is Pillow. Given the same ``stories.json`` it
always writes the same bytes.
"""

import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
TYPE_DIR = os.path.join(HERE, "fonts")
PAGE_W, PAGE_H = 1024, 1024

# Merriweather cuts bundled with the entry (regular / bold / black).
CUTS = {
    "regular": "merriweather-v33-latin-regular.ttf",
    "bold": "merriweather-v33-latin-700.ttf",
    "black": "merriweather-v33-latin-900.ttf",
}

PAPER = (238, 234, 226)     # the board the cards are pinned to
CARD = (255, 255, 255)
TAPE = (255, 214, 90)
RULE_RED = (165, 30, 25)
BODY = (25, 22, 18)
SOFT = (90, 85, 75)
FAINT = (120, 115, 105)


def typeface(cut, size):
    """A Merriweather face at the given size, from the bundled fonts."""
    try:
        return ImageFont.truetype(os.path.join(TYPE_DIR, CUTS[cut]), size)
    except OSError:
        return ImageFont.load_default()


def wrap_lines(draw, text, face, width):
    """Greedy word wrap: split text into lines that fit a pixel width."""
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=face) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, x, y, text, face, width, colour, spacing=2):
    """Draw wrapped text and return the y coordinate just below it."""
    for line in wrap_lines(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=colour)
        y += face.size + spacing
    return y


def suspension_bridge(draw, x, y, w, h, colour, hangers=True):
    """A schematic bridge: deck line, arch, three towers, hanger lines."""
    draw.line([(x, y + h - 6), (x + w, y + h - 6)], fill=colour, width=3)
    draw.arc([x + w * 0.15, y, x + w * 0.85, y + h * 1.7], 180, 360,
             fill=colour, width=3)
    for frac in (0.22, 0.5, 0.78):
        tower_x = x + w * frac
        draw.line([(tower_x, y + 4), (tower_x, y + h - 6)], fill=colour,
                  width=3)
    if hangers:
        for frac in (0.3, 0.4, 0.6, 0.7):
            draw.line([(x + w * frac, y + h * 0.45),
                       (x + w * frac, y + h - 6)], fill=colour, width=1)


def blank_card(w, h, colour):
    """An empty RGBA card of the given size, with a draw context."""
    card = Image.new("RGBA", (w, h), colour + (255,))
    return card, ImageDraw.Draw(card)


def stick(board, card, x, y, tilt):
    """Paste a card onto the board, rotated a few degrees like a cutting."""
    turned = card.rotate(tilt, expand=True, resample=Image.BICUBIC)
    board.paste(turned, (x, y), turned)


def dusk_card(w, h):
    """The photo card: a city skyline at dusk, sun low, bridge in front."""
    card, pen = blank_card(w, h, (24, 44, 96))
    for row in range(h):
        blend = row / h
        sky = tuple(int(a + (b - a) * blend) for a, b in
                    zip((24, 44, 96), (232, 120, 60))) + (255,)
        pen.line([(0, row), (w, row)], fill=sky)
    pen.ellipse([300, 20, 380, 100], fill=(255, 214, 90, 255))
    skyline = [(0, 60, 140), (70, 50, 180), (130, 70, 120),
               (210, 55, 160), (290, 70, 200), (360, 60, 130)]
    for bx, bw, bh in skyline:
        pen.rectangle([bx, h - bh, bx + bw, h], fill=(16, 20, 40, 255))
    suspension_bridge(pen, 110, 170, 200, 70, (255, 255, 255, 255))
    return card


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)

    board = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    pen = ImageDraw.Draw(board)

    # Masthead line, then two tape strips the top cards tuck under.
    pen.text((30, 18), "THE WORLD TODAY  ·  WEDNESDAY 18 NOVEMBER 2026",
             font=typeface("bold", 16), fill=(40, 40, 40))
    pen.rectangle([110, 66, 200, 80], fill=TAPE)
    pen.rectangle([700, 60, 790, 74], fill=TAPE)

    # The lead story, on the biggest card, tilted a touch left.
    lead, lpen = blank_card(500, 290, CARD)
    lpen.rectangle([0, 0, 500, 10], fill=RULE_RED)
    draw_lines(lpen, 18, 26, data["lead"]["headline"],
               typeface("black", 26), 464, BODY, spacing=4)
    draw_lines(lpen, 18, 150, data["lead"]["standfirst"],
               typeface("regular", 14), 464, SOFT, spacing=3)
    lpen.text((18, 252), "— the top story", font=typeface("bold", 13),
              fill=RULE_RED)
    stick(board, lead, 28, 72, -1.5)

    # The dusk skyline photo, tilted a touch right.
    stick(board, dusk_card(420, 260), 560, 66, 2)

    # Six continent cards, each a different colour tab, overlapping.
    # (x, y, width, height, tilt, section index)
    layout = [
        (28, 392, 300, 260, 1.0, 0),
        (348, 382, 300, 272, -2.0, 1),
        (668, 352, 322, 262, 1.5, 2),
        (28, 682, 310, 272, -1.0, 3),
        (358, 682, 300, 272, 2.0, 4),
        (678, 642, 312, 282, -1.5, 5),
    ]
    tabs = [(165, 30, 25), (0, 90, 160), (0, 120, 60),
            (150, 60, 0), (110, 40, 130), (0, 120, 120)]
    for x, y, w, h, tilt, i in layout:
        section = data["sections"][i]
        card, cpen = blank_card(w, h, CARD)
        cpen.rectangle([0, 0, w, 8], fill=tabs[i])
        cpen.text((14, 18), section["continent"].upper(),
                  font=typeface("bold", 14), fill=tabs[i])
        line_y = 46
        for headline in section["headlines"][:6]:
            line_y = draw_lines(cpen, 14, line_y, headline,
                                typeface("regular", 12), w - 28,
                                (30, 30, 30), spacing=1)
            line_y += 2
        stick(board, card, x, y, tilt)

    pen.text((30, 992), "36 stories  ·  6 continents  ·  18 Nov 2026",
             font=typeface("regular", 12), fill=FAINT)

    out = os.path.join(HERE, "entry.png")
    board.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes, {PAGE_W}x{PAGE_H})")


if __name__ == "__main__":
    main()
