#!/usr/bin/env python3
"""Render the front-page image (1024x1024 PNG) from stories.json.

Offline, deterministic: same stories.json -> same PNG bytes.
Run:  python3 render.py   (writes entry.png next to this file)

Layout (newspaper front page, the pattern the leaderboard Top 10 use):
  masthead + date line
  lead story (top 1-2 stories, larger type)
  headlines grouped by continent (6 sections)
  small world index panel (story locations as dots on a graticule)
  footer (story count, sources note)

Fonts: DejaVu (present on the build machine). If a font file is missing,
falls back to PIL's built-in bitmap font so rendering never crashes.
"""

import json
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
BG = (250, 248, 242)      # newsprint off-white
INK = (18, 18, 18)
RULE = (18, 18, 18)
MUTED = (90, 88, 82)
ACCENT = (158, 27, 27)    # deep red masthead rule
PANEL = (232, 230, 222)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=4):
    lines = wrap(draw, text, fnt, width)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)

    date_line = data["date_line"]
    lead = data["lead"]
    sections = data["sections"]          # [{continent, headlines: [str]}]
    draft = data.get("draft", False)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x0, x1 = 36, W - 36

    # ---- masthead ----
    f_mast = font(SERIF, 58)
    d.text((x0, 22), "THE WORLD TODAY", font=f_mast, fill=INK)
    f_date = font(SANS_BOLD, 17)
    d.text((x0, 96), date_line, font=f_date, fill=ACCENT)
    if draft:
        tag = "DRAFT LAYOUT"
        d.text((x1 - d.textlength(tag, font=f_date), 96), tag,
               font=f_date, fill=ACCENT)
    d.line([(x0, 128), (x1, 128)], fill=RULE, width=3)
    d.line([(x0, 134), (x1, 134)], fill=RULE, width=1)

    # ---- lead story ----
    y = 152
    f_lead = font(SERIF, 30)
    y = draw_wrapped(d, x0, y, lead["headline"], f_lead, x1 - x0, leading=6)
    f_stand = font(SERIF_REG, 17)
    y = draw_wrapped(d, x0, y, lead["standfirst"], f_stand, x1 - x0, leading=3)
    y += 6
    d.line([(x0, y), (x1, y)], fill=RULE, width=1)
    y += 12

    # ---- continent sections: 2 columns x 3 rows ----
    col_w = (x1 - x0 - 24) // 2
    row_h = 196
    f_sec = font(SANS_BOLD, 15)
    f_head = font(SERIF, 14)
    for i, sec in enumerate(sections[:6]):
        cx = x0 + (i % 2) * (col_w + 24)
        cy = y + (i // 2) * row_h
        d.rectangle([cx, cy, cx + col_w, cy + 20], fill=INK)
        d.text((cx + 8, cy + 2), sec["continent"].upper(), font=f_sec,
               fill=BG)
        hy = cy + 28
        for hl in sec["headlines"][:6]:
            hy = draw_wrapped(d, cx, hy, "\u2022  " + hl, f_head, col_w - 4,
                              leading=1)
            hy += 3
            if hy > cy + row_h - 18:
                break

    y = y + 3 * row_h + 8

    # ---- world index panel: graticule + story dots ----
    panel_top = y
    panel_h = 88
    d.rectangle([x0, panel_top, x1, panel_top + panel_h], fill=PANEL)
    f_pan = font(SANS_BOLD, 13)
    d.text((x0 + 10, panel_top + 8), "WHERE THE NEWS HAPPENED",
           font=f_pan, fill=MUTED)
    # graticule
    for gx in range(x0 + 180, x1 - 10, 72):
        d.line([(gx, panel_top + 30), (gx, panel_top + panel_h - 8)],
               fill=(200, 198, 190), width=1)
    d.line([(x0 + 170, panel_top + 58), (x1 - 10, panel_top + 58)],
           fill=(200, 198, 190), width=1)
    # dots: (lon, lat, label) -> equirectangular placement
    for lon, lat, label in data.get("map_points", []):
        px = int((x0 + 180) + (lon + 180) / 360 * (x1 - 10 - (x0 + 180)))
        py = int(panel_top + 30 + (90 - lat) / 180 * (panel_h - 38))
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=ACCENT)
        f_lab = font(SANS, 12)
        tw = d.textlength(label, font=f_lab)
        lx = px + 8 if px + 8 + tw <= x1 - 10 else px - 8 - tw
        d.text((lx, py - 7), label, font=f_lab, fill=INK)

    # ---- footer ----
    total = sum(len(s["headlines"]) for s in sections)
    f_foot = font(SANS, 13)
    foot = (f"{total} stories  \u00b7  6 continents  \u00b7  Sources: wire and "
            f"major outlets, 18 Nov 2026"
            + ("  \u00b7  DRAFT \u2014 final image rendered 19 Nov 2026"
               if draft else ""))
    d.text((x0, panel_top + panel_h + 12), foot, font=f_foot, fill=MUTED)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
