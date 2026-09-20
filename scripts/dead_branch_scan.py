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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus_surfaces  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / "docs" / "dead_branch_baseline.txt"

# (label, pattern, what to use instead)
RETIRED = [
    ("mu_dual interpolating function",
     re.compile(r"\\mu_\{?\\?(?:text|mathrm)?\{?dual\}?|mu_dual|"
                r"\\mu\s*\(\s*x\s*\)\s*=\s*x\s*/\s*\(\s*1\s*\+\s*x\s*\)"),
     "mu_std(x) = x/sqrt(1+x^2); mu_dual falsified 2026-09-12"),
    ("F_dual kinetic function",
     # \mathcal{F}_{\text{dual}} is the form the LaTeX actually uses and the
     # old pattern missed it entirely: there is no contiguous "F_" in
     # "\mathcal{F}_{\text{dual}}", so the dead entity's commonest written
     # form slipped the gate completely. Allow a "}" between F and "_".
     re.compile(r"F\}?_\{?\\?(?:text|mathrm|rm)?\s*\{?dual\}?|F_dual"),
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
# zenodo*.json is here because it is a PUBLISHED DESCRIPTION -- it becomes the
# public deposit record -- and C-04 sat open in it for weeks precisely because
# this gate only ever looked at prose. Measurement artifacts (A0_REEXTRACTION_*,
# PARAMETER_LEDGER, claims.json) are deliberately NOT globbed: a data file that
# records a0 under mu_dual as the falsified control must name it, and scanning
# those would punish correct provenance.
LIVE_GLOBS = ("*.tex", "*.md", "zenodo*.json")
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
    r"BRANCH NOTICE|BRANCH NOTE|SUBSTRATE NOTICE|SUPERSEDED|RETRACTED|"
    r"retired (branch|substrate)|falsified .{0,30}(branch|function)", re.I)
# 200, not 40: a LaTeX preamble routinely runs past 100 lines, so a banner
# placed correctly right after \maketitle sat OUTSIDE a 40-line window and the
# gate could not see it. This is safe only because the exemption is
# entity-scoped -- head_notice_covers() still requires the notice to name the
# very entity being flagged, so a V_240 banner never licenses an F_dual claim
# no matter how wide this window is.
FILE_NOTICE_HEAD_LINES = 200


NOTICE_BLOCK_LINES = 14


def head_notice_covers(head: str, label: str) -> bool:
    """True only if a notice BLOCK in the head names this very entity.

    The entity must appear inside the notice itself, not merely somewhere in
    the head. Requiring only "somewhere in the head" was wrong: once the head
    window grew past a LaTeX preamble, ordinary body prose mentioning F_dual
    satisfied it, and a V_240 banner silently licensed an F_dual claim -- the
    exact over-permissiveness this function exists to prevent."""
    lines = head.splitlines()
    pats = [pat for lbl, pat, _ in RETIRED if lbl == label]
    if not pats:
        return False
    for i, line in enumerate(lines):
        if not FILE_NOTICE.search(line):
            continue
        # Bound the block by the notice's OWN structure, not a fixed window.
        # A fixed window absorbed ordinary prose that followed a short banner,
        # which is how a V_240 notice could still cover an F_dual mention.
        # Terminate on: a blank line; the line closing a \fbox/\parbox group
        # ("}}"); or leaving a markdown blockquote run.
        quoted = line.lstrip().startswith(">")
        span = []
        for ln in lines[i:i + NOTICE_BLOCK_LINES]:
            if span:
                if not ln.strip():
                    break
                if quoted and not ln.lstrip().startswith(">"):
                    break
            span.append(ln)
            if "}}" in ln:
                break
        block = "\n".join(span)
        if any(p.search(block) for p in pats):
            return True
    return False

RETIRED_CONTEXT = re.compile(
    r"retire|retract|falsif|dead|do not use|superseded|obsolete|"
    r"no[- ]go|historical|deprecat|\[X\]|void|predates|"
    r"ruled out|excluded by", re.I)


# Surface enumeration lives in scripts/corpus_surfaces.py -- the single place
# that binds this submodule to 00_CANONICAL. Three gates were each written with
# their own `git -C <submodule> ls-files` and all three were blind to the
# canonical directory; sharing the helper stops the next one repeating it.
def tracked() -> list[tuple[Path, str]]:
    """(absolute path, display path) for every live surface this gate owns."""
    return corpus_surfaces.surfaces(LIVE_GLOBS, EXEMPT)


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


def scan_lines(lines: list[str], rel: str, base: set[str]) -> list[str]:
    """Decide every line of ONE surface.

    Split out of scan() so the permissiveness regression (--regression) can
    drive the REAL decision path over synthetic fixtures. If the test had its
    own copy of this logic it could pass while scan() rotted, which is the
    failure mode the regression exists to catch."""
    hits = []
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


def scan(skip_baseline: bool = False) -> list[str]:
    base = load_baseline() if skip_baseline else set()
    hits = []
    for path, rel in tracked():
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        hits.extend(scan_lines(lines, rel, base))
    return hits


# --------------------------------------------------------------------------
# Permissiveness regression.
#
# This rule has failed OPEN twice, both times silently, and both times it was
# an ad-hoc manual injection test that caught it -- never the self-test:
#
#   1. The first file-notice rule exempted the WHOLE file once any notice
#      appeared in its head. A V_240 banner in PAPER_02 then silenced an
#      injected F_dual claim, and 28 of 130 files were wholly blind.
#   2. Fixing that, the head window was later widened 40 -> 200 so banners
#      after a LaTeX \maketitle could be seen. head_notice_covers() asked only
#      whether the entity appeared ANYWHERE IN THE HEAD, so with a wide window
#      ordinary body prose naming F_dual satisfied it -- a V_240 banner again
#      licensed an F_dual claim.
#
# Both are the same failure: a notice about entity A excusing a live claim
# about entity B. These fixtures pin that shut. They run the real scan_lines()
# path and touch no tracked file, so the gate can never leave the repo dirty.
# --------------------------------------------------------------------------

_PREAMBLE = ["\\documentclass{article}"] + [f"% preamble filler {i}" for i in range(120)]
_V240_NOTICE = [
    "\\fbox{\\parbox{0.9\\textwidth}{\\textbf{SUBSTRATE NOTICE (2026-09-20).}",
    "This document states its substrate on the big-dimension frame",
    "$V_{240}(\\mathbb{R}^{57{,}600})$, which was \\textbf{retired 2026-08-25}.",
    "The live substrate is $V_2(\\mathbb{R}^3)$ via Cartan triality.}}",
]
_FDUAL_NOTICE = [
    "\\textbf{BRANCH NOTICE.} The results below are proved about",
    "$\\mathcal{F}_{\\text{dual}}$, a \\textbf{retired} branch falsified 2026-09-12.",
]
_FILLER = [f"Ordinary body text line {i}." for i in range(40)]
_CLAIM_FDUAL = ["We adopt $F_{dual}$ as the live kinetic function."]
_CLAIM_V240 = ["The substrate is $V_{240}(\\mathbb{R}^{57{,}600})$."]


def _regression_cases() -> list[tuple[str, list[str], str, bool]]:
    """(name, lines, entity-label-substring, must_fire)"""
    return [
        # The two historical escapes, in fixture form.
        ("V_240 notice must NOT license an F_dual claim",
         _PREAMBLE + _V240_NOTICE + _FILLER + _CLAIM_FDUAL, "F_dual", True),
        ("body prose naming F_dual in the head must NOT license it either",
         _PREAMBLE + _V240_NOTICE
         + ["Historically F_dual was studied here."] + _FILLER
         + _CLAIM_FDUAL, "F_dual", True),
        # The exemption must still work for the entity it names.
        ("V_240 notice DOES cover V_240 mentions",
         _PREAMBLE + _V240_NOTICE + _FILLER + _CLAIM_V240, "V_240", False),
        ("F_dual notice DOES cover F_dual mentions",
         _PREAMBLE + _FDUAL_NOTICE + _FILLER + _CLAIM_FDUAL, "F_dual", False),
        # A banner placed after a long preamble must be visible at all.
        ("notice past line 40 is still seen (head window)",
         _PREAMBLE + _FILLER + _V240_NOTICE + _FILLER + _CLAIM_V240, "V_240", False),
        # No notice anywhere: the claim must fire.
        ("unremediated F_dual claim fires",
         _PREAMBLE + _FILLER + _CLAIM_FDUAL, "F_dual", True),
        # Local remediation on the line itself still works.
        ("inline 'ruled out' remediates",
         _PREAMBLE + ["$F_{dual}$ is ruled out by solar-system screening."],
         "F_dual", False),
    ]


def regression() -> int:
    bad = 0
    for name, lines, entity, must_fire in _regression_cases():
        hits = scan_lines(lines, "fixture.tex", set())
        fired = any(entity in h for h in hits)
        if fired != must_fire:
            want = "FIRE" if must_fire else "stay silent"
            print(f"  REGRESSION FAIL: {name}\n"
                  f"    expected the gate to {want}; it did not.")
            bad += 1
    verdict = "PASS" if not bad else "FAIL"
    print(f"dead_branch permissiveness regression: {verdict} "
          f"({len(_regression_cases())} fixtures, 0 tracked files touched)")
    return 1 if bad else 0


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
    ap.add_argument("--regression", action="store_true",
                    help="permissiveness fixtures; touches no tracked file")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.regression:
        return regression()

    hits = scan(skip_baseline=args.check)
    base = load_baseline()
    print("DEAD-BRANCH SCAN")
    print("-" * 16)
    print(f"{'retired entities tracked':<34}{len(RETIRED)}")
    print(f"{'live surfaces scanned':<34}{len(tracked())}")
    print(f"{'violations':<34}{len(hits)}")
    if args.check and base:
        print(f"{'baselined (triaged, accepted)':<34}{len(base)}")
    if hits:
        print()
        for h in hits[:20]:
            print("  " + h)
        if len(hits) > 20:
            print(f"  ... and {len(hits) - 20} more")
    return 1 if (hits and args.check) else 0


if __name__ == "__main__":
    raise SystemExit(main())
