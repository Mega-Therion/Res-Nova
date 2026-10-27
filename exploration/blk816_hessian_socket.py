#!/usr/bin/env python3
"""Refuse to differentiate until a declaration names an action and its coordinates.

A declaration is a JSON object with string "action" (a SymPy expression) and
list "coords" (the symbols to differentiate). This file does not supply either.
Exit 2 when a required key is absent or a coordinate is unused. Exit 0 only
after a caller passes a declaration and the Hessian eigenvalues are printed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load_declaration(path: Path) -> tuple[dict, list[str]]:
    missing: list[str] = []
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"declaration unreadable: {exc.__class__.__name__}")
        return {}, ["action", "coords"]
    if not isinstance(data, dict):
        return {}, ["action", "coords"]
    action = data.get("action")
    coords = data.get("coords")
    if not isinstance(action, str) or not action.strip():
        missing.append("action")
    if (
        not isinstance(coords, list)
        or not coords
        or not all(isinstance(c, str) and c for c in coords)
    ):
        missing.append("coords")
    return data, missing


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: blk816_hessian_socket.py DECLARATION.json")
        print("missing: action coords")
        return 2
    data, missing = load_declaration(Path(argv[1]))
    if missing:
        print("missing:", " ".join(missing))
        return 2
    import sympy as sp

    symbols = sp.symbols(" ".join(data["coords"]))
    if not isinstance(symbols, tuple):
        symbols = (symbols,)
    expr = sp.sympify(data["action"], locals={str(s): s for s in symbols})
    unused = [str(s) for s in symbols if not expr.has(s)]
    if unused:
        print("missing: coords used in action:", " ".join(unused))
        return 2
    hess = sp.hessian(expr, symbols)
    eigen = hess.eigenvals()
    print("coords", [str(s) for s in symbols])
    print("hessian", hess)
    print("eigenvals", {str(k): int(v) if v == int(v) else v for k, v in eigen.items()})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
