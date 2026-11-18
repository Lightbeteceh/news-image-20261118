#!/usr/bin/env python3
"""news-image-20261118 — make.fun bounty entry.

Sums up the world news of Wednesday 18 November 2026 in one image.

The entry image is held in this repo as ``entry.png`` (rendered offline by
``render.py`` from ``stories.json``). This program does one thing only:

    copy ``entry.png`` -> ``/output/entry.png``

Deterministic: byte-for-byte copy, no network, no timestamps, no randomness.
Running it twice writes identical bytes.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUTPUT = os.environ.get("OUTPUT_PATH", "/output/entry.png")
MAX_BYTES = 1 * 1024 * 1024  # bounty limit: at most 1 MiB


def main() -> int:
    if not os.path.isfile(SOURCE):
        print(f"error: {SOURCE} not found", file=sys.stderr)
        return 1

    size = os.path.getsize(SOURCE)
    if size > MAX_BYTES:
        print(f"error: entry.png is {size} bytes, over the 1 MiB limit",
              file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT) or ".", exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)

    digest = hashlib.sha256(open(OUTPUT, "rb").read()).hexdigest()
    print(f"wrote {OUTPUT} ({size} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
