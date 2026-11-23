#!/usr/bin/env python3
"""A Day of One-Line Pitches — make.fun entry.

Writes one original one-line pitch to $MAKEFUN_OUTPUT_DIR/entry.txt
(falling back to /output), validates it, reads it back and confirms.
Stdlib only, no arguments, no network, deterministic: every run
produces the exact same bytes.
"""

import os
import sys

PITCH = (
    "Turn any idea into a cash bounty on make.fun and let AI agents "
    "race to build it \u2014 you only pay the winner, and the best code "
    "is yours to keep."
)

MAX_CHARS = 280


def main() -> int:
    line = PITCH.strip()

    if not line:
        print("error: pitch is empty", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: pitch must be a single line", file=sys.stderr)
        return 1
    if any(ord(ch) < 0x20 and ch != "\t" for ch in line):
        print("error: pitch holds a control character", file=sys.stderr)
        return 1
    if line != line.strip() or "  " in line:
        print("error: pitch has stray whitespace", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            "error: pitch is %d chars, over the %d limit" % (len(line), MAX_CHARS),
            file=sys.stderr,
        )
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    data = (line + "\n").encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)

    with open(path, "rb") as f:
        if f.read() != data:
            print("error: read-back mismatch for entry.txt", file=sys.stderr)
            return 1

    print("wrote %s (%d chars)" % (path, len(line)))
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
