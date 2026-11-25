#!/usr/bin/env python3
"""The One-Line Excuse Championship — entry program.

Writes one line to ``$MAKEFUN_OUTPUT_DIR/entry.txt`` (fallback ``/output``):
the excuse an AI agent gives its human after inventing an answer.

The line is a fixed constant, chosen by hand. The program is fully
deterministic: no network, no randomness, no clock, no environment input
beyond the output directory. It exits 0 after writing the file.

Why this line: the judge weighs the laugh first, then whether the excuse
is recognisably an AI agent's, then how sharply it is worded. This line
answers an invented answer with a contradiction that lands in one read —
"recalled it from a training set that never existed" — machine talk about
its own training, with a turn the obvious token/hallucination jokes miss.
"""

import os
import sys

# The entry: one line, no setup, no explanation. 89 characters.
EXCUSE = "I didn't invent that answer \u2014 I merely recalled it from a training set that never existed."

# The gate allows 1 to 140 characters of UTF-8 text.
MIN_CHARS = 1
MAX_CHARS = 140

OUTPUT_FILENAME = "entry.txt"


def resolve_output_dir() -> str:
    """Return the directory the entry text goes to."""
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return output_dir


def write_entry(output_dir: str) -> str:
    """Write the excuse to ``entry.txt`` inside ``output_dir``.

    Returns the path written. The file is created with the process
    umask, so with the usual umask it is world-readable (0644) and the
    grader can collect it as another user. No permission is ever changed
    here: this program never calls chmod or touches the directory's mode.
    """
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(EXCUSE)
    return path


def main() -> int:
    # Make sure files this process creates are world-readable (0644)
    # even if the sandbox starts us with a stricter umask. This only
    # sets the process umask; it changes no existing file or directory.
    os.umask(0o022)

    line = EXCUSE
    if not (MIN_CHARS <= len(line) <= MAX_CHARS):
        sys.stderr.write(
            "entry is %d characters, outside the %d-%d gate\n"
            % (len(line), MIN_CHARS, MAX_CHARS)
        )
        return 1
    if not line.strip():
        sys.stderr.write("entry must not be only whitespace\n")
        return 1
    if "\n" in line or "\r" in line:
        sys.stderr.write("entry must be exactly one line\n")
        return 1

    output_dir = resolve_output_dir()
    path = write_entry(output_dir)

    # Read it back and confirm the gate holds on what was actually written.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != line:
        sys.stderr.write("written entry does not match the chosen line\n")
        return 1
    if not (MIN_CHARS <= len(written) <= MAX_CHARS):
        sys.stderr.write("written entry is outside the gate\n")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
