#!/usr/bin/env python3
"""
RN-CO-05b STANDING FALSIFIER BATTERY — the (mu, a0) map as a permanent test.

Formalizes ledger open-item 8 (and layer 0 obligation 6): "any theory whose mu is
not mu_std-shaped is displaced ~2x in a0" — measured 2026-09-16 in
A0_REEXTRACTION_3MU_2026-09-16.json (a0(simple)/a0(std) = 0.469 ~ 1/2, windows
pairwise disjoint).

PART A — standing map checks (exit 1 if any fail):
  A1  the three extraction windows are pairwise disjoint
  A2  deep-MOND ratio a0(simple)/a0(std) in [0.45, 0.55] (pure prediction 1/2,
      measured 0.469, mid-regime residual -3.1%)
  A3  ordering a0(simple) < a0(dual) < a0(std)

PART B — the battery proper, run on the reference mus (exit 1 if any misbehave):
  B1  mu_std   : T1 knife PASS (mu'(0)=1), T2 celerity PASS  ->  a0 comparable
      with cosmology (the live measured object)
  B2  mu_dual  : T1 PASS, T2 FAIL (odds-coupling = presence coordinate; killed
      by chiral input + solar system)
  B3  mu_simple: T1 FAIL (mu'(0)=1/2, the normalization knife) ->  predicted
      ~2x a0 displacement, confirmed by the measured 0.469 shadow

The battery on a NEW candidate mu (use: battery(mu_callable)):
  T1  normalization knife   mu'(0) = 1            (else a0 displaced ~2x)
  T2  celerity identification sinh(artanh mu(x)) = x  (else not mu_std-shaped;
      equivalent to mu = x/sqrt(1+x^2) for monotone mu)
A candidate failing T1 or T2 is falsified by the SPARC extraction: its a0 will
not land in the mu_std window [1.059, 1.232]e-10, and cosmological comparisons
(binding rule, layer 0 section 2) are invalid for it.
"""
import json
import sys
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent.parent
JSON_PATH = HERE / "02_galaxy_dynamics" / "A0_REEXTRACTION_3MU_2026-09-16.json"
FAILURES = []


def note(ok, name, detail="", record=True):
    print(f"  {name}: {'PASS' if ok else 'FAIL'} {detail}")
    if not ok and record:
        FAILURES.append(name)
    return ok


def load_map():
    d = json.load(open(JSON_PATH))
    # tolerate either the flat or per-mu layout
    if "rows" in d:
        return d["rows"]
    return d


def win(row):
    return row["bootstrap_68"]


def disjoint(a, b):
    return win(a)[1] < win(b)[0] or win(b)[1] < win(a)[0]


def part_a(rows):
    print("PART A — standing (mu, a0) map checks")
    r = rows
    simple, dual, std = r["simple"], r["dual"], r["std"]
    note(disjoint(simple, dual) and disjoint(simple, std) and disjoint(dual, std),
         "A1 windows pairwise disjoint",
         f"[{win(simple)[0]:.3e},{win(simple)[1]:.3e}] "
         f"[{win(dual)[0]:.3e},{win(dual)[1]:.3e}] "
         f"[{win(std)[0]:.3e},{win(std)[1]:.3e}]")
    ratio = simple["a0_best"] / std["a0_best"]
    note(0.45 <= ratio <= 0.55, "A2 deep-MOND ratio ~1/2", f"measured {ratio:.4f}")
    note(simple["a0_best"] < dual["a0_best"] < std["a0_best"], "A3 ordering simple<dual<std",
         f"{simple['a0_best']:.3e} < {dual['a0_best']:.3e} < {std['a0_best']:.3e}")
    return win(std)


def battery(mu, name, x_sym=None, record=False):
    """Run the T1/T2 battery on a candidate mu. Returns dict of results.
    Battery FAILs are the verdict on the candidate, not harness failures;
    pass record=True to treat them as harness failures (live candidates)."""
    x = x_sym or sp.symbols("x", positive=True)
    expr = sp.sympify(mu(x)) if not isinstance(mu(x), sp.Basic) else mu(x)
    t1 = sp.limit(sp.diff(expr, x), x, 0)
    t2_diff = sp.simplify(sp.expand_func(sp.sinh(sp.atanh(expr)) - x))
    print(f"  candidate {name}:")
    note(t1 == 1, "T1 knife mu'(0)=1", f"mu'(0) = {t1}", record=record)
    note(t2_diff == 0, "T2 celerity x = sinh(artanh mu)", "mu_std-shaped" if t2_diff == 0 else "NOT mu_std-shaped -> a0 displaced ~2x", record=record)
    return {"T1": t1 == 1, "T2": t2_diff == 0}


def part_b():
    print("PART B — battery on reference mus")
    x = sp.symbols("x", positive=True)
    print(" B1:")
    r_std = battery(lambda t: t / sp.sqrt(1 + t**2), "mu_std", x)
    print(" B2:")
    r_dual = battery(lambda t: t / (1 + t), "mu_dual", x)
    print(" B3:")
    r_simple = battery(lambda t: t / (1 + sp.sqrt(1 + t**2)), "mu_simple", x)
    ok = r_std == {"T1": True, "T2": True} and r_dual == {"T1": True, "T2": False} \
        and r_simple == {"T1": False, "T2": False}
    note(ok, "B4 references behave as recorded (std passes; dual fails T2; simple fails T1)")


def main():
    rows = load_map()
    std_window = part_a(rows)
    part_b()
    print()
    print("SUMMARY: RN-CO-05b falsifier battery:", "0 failures" if not FAILURES else f"{len(FAILURES)} FAILURES",
          f"({', '.join(FAILURES) if FAILURES else 'map intact; references verified'})")
    print("Binding rule: cosmological comparison of a0 only for mu_std-shaped mu;")
    print(f"live window {std_window} (mu_std row).")
    sys.exit(1 if FAILURES else 0)


if __name__ == "__main__":
    main()
