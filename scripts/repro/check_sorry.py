#!/usr/bin/env python3
"""Detect uncommented Lean sorry/admit tokens. Proof-hygiene only."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TOKEN = re.compile(r"(?<![-/])\b(sorry|admit)\b")


def scan_file(path: Path) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        stripped = line.split("--", 1)[0]
        if TOKEN.search(stripped):
            hits.append({"path": str(path), "line": number, "text": line.strip()})
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan Lean files for uncommented sorry/admit")
    parser.add_argument("--root", type=Path, default=Path("05_lean_formalization"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    files = sorted(args.root.rglob("*.lean"))
    hits: list[dict[str, object]] = []
    for path in files:
        hits.extend(scan_file(path))
    payload = {"files_scanned": len(files), "hits": hits, "status": "FAIL" if hits else "PASS"}
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"scanned={len(files)} sorry_or_admit={len(hits)} status={payload['status']}")
        for hit in hits:
            print(f"{hit['path']}:{hit['line']}: {hit['text']}")
    return 30 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
