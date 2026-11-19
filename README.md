# news-image-20261118 — The World Today

Entry for the [make.fun news-image-20261118 bounty](https://make.fun/bounty/news-image-20261118)
("Sum up 18 November's world news in one image", $250 USDC, 50 places paid).

A program that writes one image summing up the world news of
**Wednesday 18 November 2026** to `/output/entry.png`.

## How it works

The entry image is held in this repo as `entry.png`. It is rendered offline
by `render.py` (Python 3 + Pillow, no network) from `stories.json` — a
"Collage Zine": tilted, overlapping zine-style cards with washi tape, a
dusk-skyline photo card, and a lead card, covering 36 headlines across
6 continents. Fonts (Merriweather, OFL) are bundled in `fonts/`, so
rendering needs no system fonts. `main.py` copies `entry.png` to
`/output/entry.png` byte-for-byte.

```sh
python3 render.py   # rebuild entry.png from stories.json (offline)
python3 main.py     # write /output/entry.png (deterministic, no network)
```

## Rules compliance

- Image: PNG, 1024×1024, well under 1 MiB.
- No network at run time (`main.py` only copies a local file).
- Deterministic: two runs of `render.py` and two runs of `main.py` produce
  identical bytes (verified by sha256 — see `EVIDENCE/` in the build folder).

## Status

FINAL (19 Nov 2026, ~07:30 WIB): the full news day of Wednesday 18 November
2026 (00:00–24:00 UTC) is covered — 36 stories across 6 continents, lead
story the Trump–Xi–Putin APEC opening in Shenzhen. Every headline was
re-verified against the full day's reporting before rendering.

VISUAL (19 Nov 2026, ~09:00 WIB): the owner picked "Collage Zine" from
29 variants built in the session (batch 4, news3 06-collage) — tilted
zine cards, washi tape, dusk-skyline photo card. `render.py` now renders
that design from `stories.json` (deterministic, byte-identical to the
picked variant, sha256 `6da1faff…`); `entry.png` is 359,979 bytes.

No submission has been made; submission needs the owner's explicit approval.
