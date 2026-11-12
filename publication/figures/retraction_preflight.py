#!/usr/bin/env python3
"""Fail a figure source that carries the retracted holonomy 141.99.

scan_tex is pure. The CLI scans publication/figures/*.tex and, with --compile,
runs pdflatex on each file.
"""

import re
import subprocess
import sys
from pathlib import Path

HOLONOMY = re.compile(r"141\.99")
# 141.99(1 + z)^κ and the same form with a named exponent.
PAIRED = re.compile(
    r"141\.99\s*\(\s*1\s*\+\s*z\s*\)\s*\^|"
    r"\(\s*1\s*\+\s*z\s*\)\s*\^\s*(\{)?\s*(\\kappa|\\kappa_|κ)",
    re.IGNORECASE,
)


def scan_tex(text: str) -> list[tuple[int, str]]:
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        if HOLONOMY.search(line) or PAIRED.search(line):
            hits.append((i, line.strip()))
    return hits


def main() -> int:
    compile_pdf = "--compile" in sys.argv
    root = Path(__file__).resolve().parent
    texes = sorted(root.glob("*.tex"))
    if not texes:
        print("no tex files")
        return 1
    failed = 0
    for path in texes:
        hits = scan_tex(path.read_text())
        print(f"{path.name}: hits={len(hits)}")
        for n, line in hits:
            print(f"  L{n}: {line}")
            failed += 1
        if compile_pdf and not hits:
            r = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", path.name],
                cwd=root,
                capture_output=True,
                text=True,
            )
            pdf = path.with_suffix(".pdf")
            ok = r.returncode == 0 and pdf.exists() and pdf.stat().st_size > 0
            print(
                f"  pdflatex={r.returncode} pdf_bytes={pdf.stat().st_size if pdf.exists() else 0}"
            )
            if not ok:
                failed += 1
                sys.stderr.write(r.stdout[-1500:])
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
