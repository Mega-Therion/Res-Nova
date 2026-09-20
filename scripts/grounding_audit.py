#!/usr/bin/env python3
"""Grounding audit: does a formal module touch physics, or only arithmetic?

A Lean module that elaborates with zero `sorry` has proved whatever it states.
It has not thereby said anything about the world. `stiefelEigenvalue k n :=
k * (n - (k+1)/2)` is a function from two reals to a real; proving it positive
is arithmetic, and the word "Stiefel" in the name is not carrying any
mathematical content. 34 of this repository's 55 modules were in that shape
when this audit was written.

This classifies every module and records, per module, whether anyone has
written down what its symbols are supposed to denote physically.

    tier ARITH   quantifies only over ℝ (or nothing). Real theorems, but about
                 numbers. May not be cited in a manuscript as physical evidence.
    tier STRUCT  quantifies over an actual mathematical structure -- a matrix,
                 a Lie algebra, a manifold, a measure, a derivative.

The denotation column cannot be computed. It is a judgement, written once per
module in docs/grounding_ledger.yaml, and then held to.

    python3 scripts/grounding_audit.py            # report
    python3 scripts/grounding_audit.py --check    # exit 1 on a violation
    python3 scripts/grounding_audit.py --write    # refresh the ledger skeleton
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEAN_DIR = ROOT / "05_lean_formalization"
LEDGER = ROOT / "docs" / "grounding_ledger.yaml"
BACKLOG = ROOT / "docs" / "grounding_backlog.txt"

# Evidence that a module reasons about a structure rather than about numbers.
STRUCTURE = re.compile(
    r"\b(Manifold|ChartedSpace|SmoothManifold|MeasureTheory|Measure|"
    r"InnerProductSpace|NormedSpace|NormedAddCommGroup|Matrix|LieAlgebra|"
    r"LieGroup|TensorProduct|Module|Submodule|ContinuousLinearMap|HasDerivAt|"
    r"deriv|integral|Topology|Metric|Filter|EuclideanSpace|Finset|Subgroup|"
    r"MonoidHom|RingHom|LinearMap|Basis|Matrix\.det|Matrix\.trace)\b")

# A definition whose entire type is ℝ → … → ℝ: a named number, not a structure.
PLAIN_REAL_DEF = re.compile(
    r"^\s*(?:noncomputable\s+)?def\s+(\w+)[^:\n]*:\s*(?:ℝ\s*→\s*)*ℝ\s*:?=", re.M)

THEOREM = re.compile(r"^\s*(theorem|lemma)\s+(\w+)", re.M)

# Physical constants appearing as free parameters are a grounding signal only
# when the module says what they are; on their own they are just names.
CONSTANTS = re.compile(r"\b(hbar|ħ|c_scale|speed_of_light|G_newton|a_?0|"
                       r"H_?0|M_Pl|k_B|Lambda|alpha_?em)\b")


def strip_comments(text: str) -> str:
    text = re.sub(r"/-.*?-/", " ", text, flags=re.S)
    return "\n".join(l for l in text.splitlines() if not l.strip().startswith("--"))


def classify(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    body = strip_comments(raw)
    structures = len(STRUCTURE.findall(body))
    plain = PLAIN_REAL_DEF.findall(body)
    theorems = [m[1] for m in THEOREM.findall(body)]
    return {
        "module": path.stem,
        "tier": "STRUCT" if structures else "ARITH",
        "structures": structures,
        "plain_real_defs": len(plain),
        "plain_names": plain[:6],
        "theorems": len(theorems),
        "constants": sorted(set(CONSTANTS.findall(body)))[:6],
    }


def load_ledger() -> dict:
    """Minimal reader: module -> {denotes, observable, falsifier}."""
    if not LEDGER.exists():
        return {}
    out, cur = {}, None
    for raw in LEDGER.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        m = re.match(r"^\s*-\s*module:\s*(\S+)", raw)
        if m:
            cur = {"module": m.group(1)}
            out[m.group(1)] = cur
            continue
        m = re.match(r"^\s+([a-z_]+):\s*(.*)$", raw)
        if m and cur is not None:
            v = m.group(2).strip().strip('"')
            cur[m.group(1)] = None if v in ("", "null", "~", "TODO") else v
    return out


def write_skeleton(rows: list[dict]) -> None:
    led = load_ledger()
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    out = ["# Grounding ledger.",
           "#",
           "# One entry per formal module. The three judgement fields cannot be",
           "# computed and must be written by a person:",
           "#",
           "#   denotes    -- what the module's symbols are claimed to denote",
           "#                 physically. \"none\" is a legitimate answer: it means",
           "#                 the module is mathematics, not a physical claim.",
           "#   observable -- the measurable quantity or dataset it touches,",
           "#                 or \"none\".",
           "#   falsifier  -- the measurement that would kill the claim,",
           "#                 or \"none\".",
           "#",
           "# tier is computed, not written: STRUCT means the module quantifies",
           "# over a mathematical structure; ARITH means it quantifies over ℝ.",
           "# An ARITH module may not be cited in a manuscript as physical",
           "# evidence, however green the kernel is.",
           "",
           "modules:"]
    for r in sorted(rows, key=lambda x: (x["tier"], x["module"])):
        prev = led.get(r["module"], {})
        out += [f"  - module: {r['module']}",
                f"    tier: {r['tier']}",
                f"    theorems: {r['theorems']}",
                f"    structures: {r['structures']}",
                f"    plain_real_defs: {r['plain_real_defs']}",
                f"    denotes: {prev.get('denotes') or 'TODO'}",
                f"    observable: {prev.get('observable') or 'TODO'}",
                f"    falsifier: {prev.get('falsifier') or 'TODO'}",
                ""]
    LEDGER.write_text("\n".join(out), encoding="utf-8")


MANUSCRIPT_GLOBS = ("01_foundational_action/*.tex", "02_galaxy_dynamics/*.tex",
                    "03_observer_jwst/*.tex", "*.tex")


def manuscript_citations() -> dict:
    """Which modules do the manuscripts name? A .tex that points at a module is
    offering it as evidence to a reader."""
    cited = {}
    seen = set()
    for g in MANUSCRIPT_GLOBS:
        for tex in ROOT.glob(g):
            if tex in seen or "publication/" in str(tex):
                continue
            seen.add(tex)
            body = tex.read_text(encoding="utf-8", errors="replace")
            for m in re.finditer(r"([A-Z][A-Za-z0-9_]{3,})\\?\.lean", body):
                cited.setdefault(m.group(1).replace("\\", ""), set()).add(
                    str(tex.relative_to(ROOT)))
    return cited


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    rows = [classify(p) for p in sorted(LEAN_DIR.glob("*.lean"))
            if p.name != "lakefile.lean"]
    if args.write:
        write_skeleton(rows)
        print(f"ledger skeleton written to {LEDGER.relative_to(ROOT)}")
        return 0

    led = load_ledger()
    arith = [r for r in rows if r["tier"] == "ARITH"]
    struct = [r for r in rows if r["tier"] == "STRUCT"]
    th_a = sum(r["theorems"] for r in arith)
    th_s = sum(r["theorems"] for r in struct)

    print("GROUNDING AUDIT")
    print("-" * 15)
    print(f"{'modules':<34}{len(rows)}")
    print(f"{'  STRUCT (touches a structure)':<34}{len(struct):>4}   "
          f"{th_s:>4} theorems")
    print(f"{'  ARITH  (plain real arithmetic)':<34}{len(arith):>4}   "
          f"{th_a:>4} theorems")
    pct = th_a / max(th_a + th_s, 1) * 100
    print(f"{'theorems that are arithmetic':<34}{pct:.0f}%")

    undeclared = [r["module"] for r in rows
                  if not (led.get(r["module"], {}).get("denotes"))]
    print(f"{'modules with no denotation entry':<34}{len(undeclared)}")

    cited = manuscript_citations()
    by_name = {r["module"]: r for r in rows}
    print(f"{'modules cited by a manuscript':<34}{len(cited)}")

    backlog = set()
    if BACKLOG.exists():
        backlog = {l.strip() for l in BACKLOG.read_text(encoding="utf-8").splitlines()
                   if l.strip() and not l.startswith("#")}

    if args.check:
        problems = []
        if not LEDGER.exists():
            problems.append("no grounding ledger; run --write")
        # The binding rule: a module a manuscript offers as evidence must say
        # what it denotes. An unanswered denotation on an uncited module is a
        # backlog item, not a build failure.
        for mod, texs in sorted(cited.items()):
            r = by_name.get(mod)
            if r is None:
                continue
            e = led.get(mod) or {}
            where = ", ".join(sorted(texs))
            if not e.get("denotes"):
                if mod in backlog:
                    continue        # known, dated, being worked down
                problems.append(f"{mod}: cited by {where} but the ledger does "
                                f"not say what it denotes physically")
            elif r["tier"] == "ARITH" and e.get("denotes") != "none" \
                    and not e.get("observable"):
                problems.append(f"{mod}: cited by {where} as physics, but it "
                                f"quantifies only over ℝ and names no observable")
        print()
        if problems:
            print(f"GROUNDING CHECK: FAIL ({len(problems)})")
            for p in problems[:25]:
                print("  " + p)
            if len(problems) > 25:
                print(f"  ... and {len(problems) - 25} more")
            return 1
        print(f"GROUNDING CHECK: PASS "
              f"({len(backlog)} cited module(s) still awaiting a denotation, "
              f"tracked in {BACKLOG.name})")
    else:
        print("\nARITH modules (named numbers, not structures):")
        for r in sorted(arith, key=lambda x: -x["theorems"])[:14]:
            names = ", ".join(r["plain_names"][:3])
            print(f"  {r['module'][:38]:<40}{r['theorems']:>3} thms   {names[:46]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
