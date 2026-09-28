"""Command-line allowlists for the D7 wind scripts. Arguments are mapped to constants, so no file path or executed
code is ever built from raw user input."""

import sys


def pick_dir(argv=None, i=1, default="par"):
    argv = sys.argv if argv is None else argv
    a = argv[i] if len(argv) > i else default
    if a == "par":
        return "par"
    if a == "perp":
        return "perp"
    raise SystemExit(f"direction must be 'par' or 'perp', got {a!r}")


def pick_k2(argv=None, i=2, default="75"):
    argv = sys.argv if argv is None else argv
    a = argv[i] if len(argv) > i else default
    if a == "75":
        return 75
    if a == "750000":
        return 750000
    raise SystemExit(f"K2 must be 75 or 750000, got {a!r}")
