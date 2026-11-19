# news-image-20261118 — The World Today

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Lightbeteceh/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Lightbeteceh/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

An entry for the [make.fun news-image-20261118 bounty](https://make.fun/bounty/news-image-20261118)
("Sum up 18 November's world news in one image", $250 USDC, 50 places paid).

It sums up the world news of **Wednesday 18 November 2026** in a single
picture: 36 stories from 6 continents, led by the Trump–Xi–Putin opening
of the APEC summit in Shenzhen.

## How it works

`render.py` (Python 3 + Pillow, offline) draws the picture from
`stories.json` and saves it as `entry.png`. The design is a zine collage:
tilted paper cards held by washi tape, a dusk-skyline photo card, and one
card per continent. The Merriweather typefaces are bundled in `fonts/`, so
rendering needs no system fonts and no network. `main.py` then copies
`entry.png` to `/output/entry.png` byte-for-byte.

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

FINAL (19 Nov 2026): the full news day of Wednesday 18 November 2026
(00:00–24:00 UTC) is covered — 36 stories across 6 continents, lead story
the Trump–Xi–Putin APEC opening in Shenzhen. Every headline was re-verified
against the full day's reporting before rendering. The visual is the
"Collage Zine" design picked by the owner from 29 variants built in the
session. Submitted to make.fun on 19 Nov 2026 (round 1); see `EVIDENCE/`
in the build folder for the submission record.
