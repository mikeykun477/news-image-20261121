#!/usr/bin/env python3
"""Deliver the finished front page for the make.fun news-image entry.

The picture itself — ``entry.png``, a one-page newspaper front for
Saturday 21 November 2026 — is built ahead of time and shipped next to
this file.  All this entrypoint does is place an exact copy of it where
the harness looks for it, so the result is the same on every run:

* destination: ``$MAKEFUN_OUTPUT_DIR/entry.png`` (``/output`` if the
  variable is unset or empty),
* the copy is refused when the picture is bigger than 1 MiB,
* only the Python standard library is used, and nothing is fetched
  from the network.

Usage::

    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import sys

# Largest picture the harness accepts, in bytes.
SIZE_LIMIT = 1024 * 1024

# Fallback destination when MAKEFUN_OUTPUT_DIR is not set.
DEFAULT_DIR = "/output"

# Name of the shipped picture, here and in the output directory.
ENTRY_NAME = "entry.png"

# Copy in 64 KiB chunks; small enough to be polite, big enough to be fast.
CHUNK = 64 * 1024


def die(message):
    """Print an error and stop with a non-zero exit status."""
    print("main.py: " + message, file=sys.stderr)
    raise SystemExit(1)


def script_dir():
    """Directory holding this file, resolved to an absolute path."""
    return os.path.dirname(os.path.abspath(__file__))


def output_dir():
    """Destination directory, honouring MAKEFUN_OUTPUT_DIR."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_DIR
    return os.path.expanduser(chosen)


def source_path():
    """Absolute path of the shipped front page."""
    return os.path.join(script_dir(), ENTRY_NAME)


def destination_path(directory):
    """Full path of the picture once it has been delivered."""
    return os.path.join(directory, ENTRY_NAME)


def checked_byte_count(path):
    """Size of ``path`` in bytes, refusing anything over the limit."""
    try:
        found = os.path.getsize(path)
    except OSError as exc:
        die("cannot stat %s: %s" % (path, exc))
    if found > SIZE_LIMIT:
        die(
            "%s is %d bytes, over the %d-byte limit"
            % (ENTRY_NAME, found, SIZE_LIMIT)
        )
    return found


def stream_copy(src, dst, expected):
    """Copy ``src`` to ``dst`` a chunk at a time, counting every byte.

    Returns the number of bytes written.  The count is checked against
    ``expected`` afterwards so a short or truncated copy can never
    pass silently.
    """
    written = 0
    with open(src, "rb") as reader, open(dst, "wb") as writer:
        while True:
            block = reader.read(CHUNK)
            if not block:
                break
            writer.write(block)
            written += len(block)
    if written != expected:
        die(
            "copied %d bytes of %s, expected %d"
            % (written, ENTRY_NAME, expected)
        )
    return written


def verify_delivery(dst, expected):
    """Re-stat the delivered file; a size mismatch means a bad copy."""
    try:
        actual = os.path.getsize(dst)
    except OSError as exc:
        die("cannot stat delivered file %s: %s" % (dst, exc))
    if actual != expected:
        die(
            "delivered %s is %d bytes, expected %d"
            % (dst, actual, expected)
        )
    return actual


def deliver():
    """Copy the front page into the output directory and report it."""
    src = source_path()
    total = checked_byte_count(src)
    directory = output_dir()
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as exc:
        die("cannot create %s: %s" % (directory, exc))
    dst = destination_path(directory)
    stream_copy(src, dst, total)
    verify_delivery(dst, total)
    print("wrote %s (%d bytes)" % (dst, total))
    return dst


def main():
    deliver()


if __name__ == "__main__":
    main()
