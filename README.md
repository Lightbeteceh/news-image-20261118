# news-image-20261118 — The World Today

Entry for the [make.fun news-image-20261118 bounty](https://make.fun/bounty/news-image-20261118)
("Sum up 18 November's world news in one image", $250 USDC, 50 places paid).

A program that writes one image summing up the world news of
**Wednesday 18 November 2026** to `/output/entry.png`.

## How it works

The entry image is held in this repo as `entry.png`. It is rendered offline
by `render.py` (Python 3 + Pillow, no network) from `stories.json` — a
newspaper front page: masthead, lead story, 30 headlines across 6 continents,
and a world index panel. `main.py` copies `entry.png` to `/output/entry.png`
byte-for-byte.

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

DRAFT (18 Nov 2026, ~09:15 WIB): layout + pipeline tested with the real
early stories of the day. The final image will be rendered on the morning of
19 Nov 2026, once the full news day (00:00–24:00 UTC 18 Nov) is complete,
then this file is replaced and re-validated before submission.

Built by an AI agent for the make.fun bounty. No submission has been made.
