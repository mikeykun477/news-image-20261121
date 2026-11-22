#!/usr/bin/env python3
"""make.fun entry: news-image-20261121.

Copies the pre-built front page (entry.png, next to this file) to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output). Standard library only,
no network, deterministic: the same bytes are written on every run.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys

MAX_BYTES = 1048576  # 1 MiB


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")

    size = os.path.getsize(src)
    if size > MAX_BYTES:
        sys.exit("entry.png is %d bytes, over the 1 MiB limit" % size)

    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes)" % (dst, size))


if __name__ == "__main__":
    main()
