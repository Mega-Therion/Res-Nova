#!/usr/bin/env python3
"""Flag tier tags that the canonical legend does not define.

Four incompatible tier vocabularies were in simultaneous use before
docs/EPISTEMIC_TIER_LEGEND.md existed -- `[C]` meaning both "cited" and
"conjectured", `[P]` meaning both "proved" and "proposed". This keeps new
vocabulary from appearing without a definition.

    python3 scripts/tier_legend_check.py            # report
    python3 scripts/tier_legend_check.py --check    # exit 1 on undefined tags
    python3 scripts/tier_legend_check.py --self-test
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEGEND = ROOT / "docs" / "EPISTEMIC_TIER_LEGEND.md"

# A tier tag is either a single capital with an optional star or slash-pair --
# [P], [D*], [P/O] -- or one of a small set of word tags. Anything else in
# brackets is maths ([L_k]), a citation key ([Smith2020]) or prose.
TAG = re.compile(r"(?<![\w`])\[([A-Z]\*?|[A-Z]/[A-Z]|conj|arith|emp|thm|cond|cited)\](?!\()")

# Tags that are not epistemic claims: citation keys, markdown checkboxes,
# array indices, and the hand-rolled tags of unrelated conventions.
NOT_A_TIER = {"x", "X ", "ref", "i", "n", "m", "s", "a", "b", "c", "e", "g",
              "t", "url", "TODO", "WIP", "sic", "0", "1", "2"}


def legend_tags() -> set[str]:
    if not LEGEND.exists():
        return set()
    body = LEGEND.read_text(encoding="utf-8")
    return set(re.findall(r"^\| `\[([^\]]+)\]`", body, re.M))


def scan(files: list[Path], allowed: set[str]) -> list[str]:
    hits = []
    for path in files:
        rel = str(path.relative_to(ROOT))
        if rel.startswith("docs/EPISTEMIC_TIER_LEGEND"):
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for n, line in enumerate(lines, 1):
            for m in TAG.finditer(line):
                tag = m.group(1)
                if tag in allowed or tag in NOT_A_TIER or tag.lower() in NOT_A_TIER:
                    continue
                # inside a maths span it is notation, not a tier:
                # \mathcal{D}[L] is the Lindblad dissipator, not tag [L].
                if line.count("$", 0, m.start()) % 2 == 1:
                    continue
                hits.append(f"{rel}:{n}: tier tag [{tag}] is not in the legend")
    return hits


def tracked_md() -> list[Path]:
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "*.md"],
                         capture_output=True, text=True).stdout.splitlines()
    skip = ("raw/", "80_Archive/", "docs/recovered/", "archive")
    return [ROOT / f for f in out if not any(s in f for s in skip)]


def self_test() -> int:
    allowed = {"P", "D", "D*", "C", "conj", "E", "O", "X", "A", "arith"}
    cases = [("this is [P] proved", False), ("status [Q] unknown", True),
             ("see [conj] above", False), ("cite [Smith2020]", False)]
    fails = 0
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        for text, should_hit in cases:
            p = Path(d) / "t.md"
            p.write_text(text, encoding="utf-8")
            lines = text.splitlines()
            hit = False
            for line in lines:
                for m in TAG.finditer(line):
                    tag = m.group(1)
                    if tag in allowed or tag in NOT_A_TIER:
                        continue
                    hit = True
            if hit != should_hit:
                print(f"SELF-TEST FAIL: {text!r} -> {hit}, expected {should_hit}",
                      file=sys.stderr)
                fails += 1
    if fails:
        return 1
    print(f"tier_legend_check self-test: PASS ({len(cases)} cases, "
          f"{len(legend_tags())} tags defined in the legend)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    allowed = legend_tags()
    files = tracked_md()
    hits = scan(files, allowed)
    print("TIER LEGEND CHECK")
    print("-" * 17)
    print(f"{'tags defined in legend':<30}{len(allowed)}")
    print(f"{'markdown surfaces scanned':<30}{len(files)}")
    print(f"{'undefined tier tags':<30}{len(hits)}")
    if hits:
        print()
        for h in hits[:15]:
            print("  " + h)
        if len(hits) > 15:
            print(f"  ... and {len(hits) - 15} more")
    return 1 if (hits and args.check) else 0


if __name__ == "__main__":
    raise SystemExit(main())
