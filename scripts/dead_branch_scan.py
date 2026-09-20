#!/usr/bin/env python3
"""Fail the build when a retired construction appears on a live surface.

CURRENT_STATE_READ_THIS_FIRST.md exists because an external agent built a brief
from cached material and wrote four papers on a function that had been falsified
two hours earlier. The countermeasure was a document agents are told to read.

A document is not a countermeasure. On 2026-09-20 a fresh Claude session
re-derived the internal-gauge soldering no-go -- retracted seven weeks earlier,
with an audit already on disk -- and published three canonical notes on top of
it. The instruction to read the file was in place. It did not help, partly
because the dispatch rule pointed at a path that did not exist.

This makes the same rule mechanical: retired entities fail the gate.

    python3 scripts/dead_branch_scan.py            # report
    python3 scripts/dead_branch_scan.py --check    # exit 1 on a live hit
    python3 scripts/dead_branch_scan.py --self-test
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / "docs" / "dead_branch_baseline.txt"

# (label, pattern, what to use instead)
RETIRED = [
    ("mu_dual interpolating function",
     re.compile(r"\\mu_\{?\\?(?:text|mathrm)?\{?dual\}?|mu_dual|"
                r"\\mu\s*\(\s*x\s*\)\s*=\s*x\s*/\s*\(\s*1\s*\+\s*x\s*\)"),
     "mu_std(x) = x/sqrt(1+x^2); mu_dual falsified 2026-09-12"),
    ("F_dual kinetic function",
     re.compile(r"F_\{?\\?(?:text|mathrm)?\{?dual\}?|F_dual"),
     "the mu_std branch; F_dual falsified with mu_dual"),
    ("V_240 big-dimension substrate",
     re.compile(r"V_\{?240\}?|57,?600\s*[-\s]*dimensional|"
                r"V_m\(\\mathbb\{R\}\^N\).{0,40}240"),
     "V_2(R^3) via Cartan triality; V_240 retired 2026-08-25"),
    ("generalized Einstein-aether completion",
     re.compile(r"generali[sz]ed Einstein[- ]aether|disformal coupling.{0,30}"
                r"vector field"),
     "AeST (Skordis-Zlosnik, arXiv:2007.00082); retired 2026-09-12"),
    ("internal-gauge soldering",
     re.compile(r"internal[- ]gauge soldering|baryon[- ]to[- ]internal[- ]curvature"),
     "AeST covariant completion; retracted 2026-08-02"),
    ("fabricated a0(z) figure",
     re.compile(r"a0_z_analysis\.png"),
     "do not cite -- 3 of 5 points fabricated"),
]

# Surfaces where a retired entity is a defect. Everything else -- archives,
# logs, retracted papers, audit scripts, this file -- may name them freely.
LIVE_GLOBS = ("*.tex", "*.md")
EXEMPT = (
    "raw/Logs/", "80_Archive/", "obsidian_vault_legacy/", "archive/",
    "docs/recovered/", "archive_previous_iterations/", "Tier_2_Physics_Attempt/",
    "CURRENT_STATE_READ_THIS_FIRST.md", "scripts/", "SOLDERING_",
    "PEER_REVIEW_READINESS.md", "TARGET_D7_COVARIANT_COMPLETION.md",
    "TARGET_D1_SUPPLEMENT", "TARGET_D2_SUPPLEMENT", "_AUDIT_", "AUDIT_LEDGER",
    "CHANGELOG", "OPEN_PROBLEMS", "VERIFICATION_RUN",
    # Audit artifacts whose SUBJECT is the retired entities. Naming a dead
    # branch in order to flag it is the intended use, not a violation.
    "RES_NOVA_INVENTORY_", "RES_NOVA_CONTRADICTION_LOG_",
)
# A line that marks the entity as dead is a correct mention, not a violation.
# A document-level notice remediates the mentions it actually covers. Local
# +/-3-line context cannot see a banner 200 lines above, so the head of the
# file is checked separately -- but PER ENTITY. A V_240 substrate banner does
# NOT license an unqualified F_dual claim later in the same file; an earlier
# version of this rule exempted whole files and silenced 28 of them.
FILE_NOTICE = re.compile(
    r"BRANCH NOTICE|SUBSTRATE NOTICE|SUPERSEDED|RETRACTED|"
    r"retired (branch|substrate)|falsified .{0,30}(branch|function)", re.I)
FILE_NOTICE_HEAD_LINES = 40


def head_notice_covers(head: str, label: str) -> bool:
    """True only if the head notice names the entity this mention is about."""
    if not FILE_NOTICE.search(head):
        return False
    for other_label, pat, _ in RETIRED:
        if other_label == label and pat.search(head):
            return True
    return False

RETIRED_CONTEXT = re.compile(
    r"retire|retract|falsif|dead|do not use|superseded|obsolete|"
    r"no[- ]go|historical|deprecat|\[X\]|void|predates|"
    r"ruled out|excluded by", re.I)


# Surfaces OUTSIDE this submodule that must still be scanned. C-00 of the
# 2026-09-20 contradiction log: GUT_TOE_CANONICAL_SCOPE.md calls itself "the
# single canonical reference for the scope, status and roadmap" of the whole
# program, and carried a [P] tag on the falsified mu_dual -- but it lives in
# the PARENT repo, so `git ls-files` here never listed it and this gate had
# never once looked at the document every agent is pointed to. Paths are
# relative to the parent of the submodule root.
EXTRA_SCAN_ROOTS = ["00_CANONICAL"]


def _ls_files(repo: Path, prefix: str = "") -> list[str]:
    r = subprocess.run(["git", "-C", str(repo), "ls-files", prefix or "."],
                       capture_output=True, text=True)
    return r.stdout.splitlines() if r.returncode == 0 else []


def _keep(rel: str) -> bool:
    return (any(Path(rel).match(g) for g in LIVE_GLOBS)
            and not any(e in rel for e in EXEMPT))


def tracked() -> list[tuple[Path, str]]:
    """(absolute path, display path) for every live surface this gate owns."""
    out = [(ROOT / f, f) for f in _ls_files(ROOT) if _keep(f)]
    parent = ROOT.parent
    for extra in EXTRA_SCAN_ROOTS:
        if not (parent / extra).is_dir():
            continue
        for f in _ls_files(parent, extra):
            if _keep(f):
                out.append((parent / f, f"../{f}"))
    return out


def baseline_key(rel: str, label: str, line: str) -> str:
    """Key a baselined mention by its CONTENT, not its line number.

    Keying on file:line meant that inserting text anywhere above a baselined
    mention shifted it and the gate reported a phantom new violation -- which
    is exactly what happened when D3 gained its citation block. The hash of
    the normalised line survives edits elsewhere in the file and still changes
    if the mention itself is edited."""
    digest = hashlib.sha1(" ".join(line.split()).encode("utf-8")).hexdigest()[:12]
    return f"{rel}::{label}::{digest}"


def load_baseline() -> set[str]:
    if not BASELINE.exists():
        return set()
    return {l.strip() for l in BASELINE.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")}


def scan(skip_baseline: bool = False) -> list[str]:
    base = load_baseline() if skip_baseline else set()
    hits = []
    for path, rel in tracked():
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        head = "\n".join(lines[:FILE_NOTICE_HEAD_LINES])
        for n, line in enumerate(lines, 1):
            window = "\n".join(lines[max(0, n - 3):n + 2])
            if RETIRED_CONTEXT.search(window):
                continue
            for label, pat, instead in RETIRED:
                m = pat.search(line)
                if m:
                    if head_notice_covers(head, label):
                        break
                    if baseline_key(rel, label, line) in base:
                        break
                    hits.append(f"{rel}:{n}: {label} -- {m.group(0)[:40]!r}\n"
                                f"      use instead: {instead}")
                    break
    return hits


def self_test() -> int:
    cases = [
        ("mu_dual(x) = x/(1+x) is the interpolating function", True),
        ("the V_240 substrate underlies the frame", True),
        ("see a0_z_analysis.png for the fit", True),
        ("mu_std(x) = x/sqrt(1+x^2) is the live branch", False),
        ("mu_dual was falsified on 2026-09-12 and is retired", False),
    ]
    fails = 0
    for text, should_hit in cases:
        hit = any(p.search(text) for _, p, _ in RETIRED)
        ctx = bool(RETIRED_CONTEXT.search(text))
        flagged = hit and not ctx
        if flagged != should_hit:
            print(f"SELF-TEST FAIL: {text!r} -> flagged={flagged}, "
                  f"expected {should_hit}", file=sys.stderr)
            fails += 1
    if fails:
        return 1
    print(f"dead_branch_scan self-test: PASS ({len(cases)} cases, "
          f"{len(RETIRED)} retired entities tracked)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    hits = scan(skip_baseline=args.check)
    base = load_baseline()
    print("DEAD-BRANCH SCAN")
    print("-" * 16)
    print(f"{'retired entities tracked':<34}{len(RETIRED)}")
    print(f"{'live surfaces scanned':<34}{len(tracked())}")
    print(f"{'violations':<34}{len(hits)}")
    if args.check and base:
        print(f"{'baselined, awaiting triage':<34}{len(base)}")
    if hits:
        print()
        for h in hits[:20]:
            print("  " + h)
        if len(hits) > 20:
            print(f"  ... and {len(hits) - 20} more")
    return 1 if (hits and args.check) else 0


if __name__ == "__main__":
    raise SystemExit(main())
