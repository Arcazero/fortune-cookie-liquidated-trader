#!/usr/bin/env python3
"""Fortune Cookie for the Liquidated Trader.

Writes one original fortune-cookie line for a crypto trader who has
just been liquidated to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR/entry.txt).

The line is a single fortune-slip message of at most 20 words and at
most 160 characters, in plain text.
"""

import os
import sys

FORTUNE = (
    "Fortune favours the bold; tonight it favoured "
    "the exchange that liquidated you."
)
MAX_CHARS = 160
MAX_WORDS = 20


def has_letter_or_digit(line: str) -> bool:
    """True when the line carries at least one letter or digit.

    A fortune that is only punctuation ("!!!", "...") is not a message.
    """
    return any(ch.isalnum() for ch in line)


def validate_fortune(line: str) -> str:
    """Return the fortune line, failing loudly if it breaks the gate.

    The entry gate requires UTF-8 text of 1-160 characters, not only
    whitespace, and the brief requires at most 20 words of plain text.
    """
    line = line.strip()
    length = len(line)
    if length < 1 or length > MAX_CHARS:
        print(
            f"error: fortune line must be 1-{MAX_CHARS} characters, got {length}",
            file=sys.stderr,
        )
        sys.exit(1)
    if not line.strip():
        print("error: fortune line must not be only whitespace", file=sys.stderr)
        sys.exit(1)
    if not has_letter_or_digit(line):
        print(
            "error: fortune line must contain at least one letter or digit",
            file=sys.stderr,
        )
        sys.exit(1)
    if "\n" in line or "\r" in line:
        print("error: fortune line must be a single line", file=sys.stderr)
        sys.exit(1)
    words = line.split()
    if len(words) > MAX_WORDS:
        print(
            f"error: fortune line must be at most {MAX_WORDS} words, "
            f"got {len(words)}",
            file=sys.stderr,
        )
        sys.exit(1)
    return line


def output_path(output_dir: str) -> str:
    """Path of the entry file inside the output directory."""
    return os.path.join(output_dir, "entry.txt")


def main() -> None:
    fortune = validate_fortune(FORTUNE)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path(output_dir), "w", encoding="utf-8") as f:
        f.write(fortune + "\n")


if __name__ == "__main__":
    main()
