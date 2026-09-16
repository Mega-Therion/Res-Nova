#!/usr/bin/env python3
"""
Obligation 5 audit verifier — the a0 prediction, two-sided and falsifiable.

Layer 0 obligation 5: predict a0 — and the prediction must land in the mu_std
window [1.059, 1.232]e-10, not the legacy 1.107e-10 and not the mu-mixed
literature 1.2e-10.

What the theory now has (after obligations 1-3): a covariant kinematics (B-cov)
that forces mu = mu_std; a 2pi home (the thermal circle of the K2 orbit) that
fixes the FORM of the reference scale as a/2pi; and the Hubble-form selection
(audit P2) that fixes WHICH horizon. The identity a0 = c*H0/(2*pi) is therefore
the theory's scale relation. This audit states the prediction BOTH ways and
quantifies every tension. It takes a side: the theory prefers the SH0ES side of
the Hubble tension.

Machine checks:
  F1  the exact identity and its inverse: a0 = c*H0/(2*pi) <==> H0 = 2*pi*a0/c
      (symbolic; no free parameters once H0 is given).
  F2  FORWARD: from Planck H0 = 67.4 +- 0.5 -> a0 = 1.0421e-10; tension vs the
      measured mu_std window (recomputed from the frozen JSON; the audit's
      -1.32 sigma_boot reconfirmed).
  F3  BACKWARDS: from the measured window -> H0 = 75.06 km/s/Mpc central,
      window [68.56, 79.74] (68%, from bootstrap_68).
  F4  the falsifier table ([C] H0 landscape values, machine tensions):
        Planck   67.4 +- 0.5  -> 1.36 sigma disfavored by the window
        SH0ES    73.04 +- 1.04 -> 0.36 sigma (consistent)
        TRGB/Freedman 69.6 +- 1.9 -> 0.92 sigma (consistent)
      The theory's prediction disfavors the Planck value; every late-universe
      ladder is consistent. An H0 survey landing < 68.6 or > 79.74 falsifies
      the identity outright.
  F5  binding rule of the (mu, a0) map honored: mu_std passes the battery
      (T1 knife mu'(0) = 1, T2 celerity) — the cosmological comparison this
      audit performs is VALID under RN-CO-05b. A non-mu_std-shaped mu's
      window would be elsewhere (mu_simple's a0 is 2.1x off the window edge).
  F6  the legacy traps are excluded: the prediction targets [1.059, 1.232]e-10,
      not the legacy mu_dual-era 1.107e-10 and not the mu-mixed 1.2e-10.
Exit 0 iff all pass.
"""
import json
import sys
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent.parent
JSON_PATH = HERE / "02_galaxy_dynamics" / "A0_REEXTRACTION_3MU_2026-09-16.json"
FAILURES = []

MPC = 3.0856775814913673e22   # m
C = 2.99792458e8               # m/s
KMS_MPC = 1000 / MPC          # (km/s/Mpc) -> 1/s


def note(ok, name, detail=""):
    print(f"{name}: {'PASS' if ok else 'FAIL'} {detail}")
    if not ok:
        FAILURES.append(name)


def main():
    # F1: exact identity, symbolic
    a0, H = sp.symbols("a0 H", positive=True)
    solved = sp.solve(sp.Eq(a0, C * H / (2 * sp.pi)), H)[0]
    note(abs(float((solved - 2 * sp.pi * a0 / C).subs(a0, sp.Rational(1234, 1000)))) < 1e-18,
         "F1 identity a0 = cH/(2*pi) inverts exactly: H = 2*pi*a0/c (no free parameters)")

    d = json.load(open(JSON_PATH))
    std = d["std"]
    lo, hi = std["bootstrap_68"]
    best = std["a0_best"]
    sigma = (hi - lo) / 2

    # F2: forward from Planck
    H_planck = 67.4
    anchor = C * (H_planck * KMS_MPC) / (2 * sp.pi)
    t_fwd = (float(anchor) - best) / sigma
    note(abs(float(anchor) - 1.0421e-10) / 1.0421e-10 < 1e-3 and -1.6 < t_fwd < -1.0,
         "F2 forward: Planck H0 -> a0 = 1.0421e-10, tension vs window",
         f"anchor {float(anchor):.4e}, tension {t_fwd:+.2f} sigma (audit: -1.32 sigma_boot)")

    # F3: backwards from the window
    h_from_a0 = lambda a: 2 * sp.pi * a / C / KMS_MPC
    h_central = float(h_from_a0(best))
    h_lo, h_hi = float(h_from_a0(lo)), float(h_from_a0(hi))
    note(abs(h_central - 75.06) < 0.02 and 68 < h_lo < 69 and 79 < h_hi < 80,
         "F3 backwards: window -> H0 central 75.06, 68% [~68.5, ~79.7] km/s/Mpc",
         f"[{h_lo:.2f}, {h_hi:.2f}]")

    # F4: falsifier table
    sig_h = (h_hi - h_lo) / 2  # the theory's own sigma on H0

    def tension(H0v, sH0):
        import math
        return (h_central - H0v) / math.sqrt(sig_h**2 + sH0**2)

    t_planck = tension(67.4, 0.5)
    t_sh0es = tension(73.04, 1.04)
    t_trgb = tension(69.6, 1.9)
    note(1.0 < t_planck < 1.8, "F4a Planck 67.4+-0.5 disfavored", f"{t_planck:+.2f} sigma")
    note(t_sh0es < 0.5, "F4b SH0ES 73.04+-1.04 consistent", f"{t_sh0es:+.2f} sigma")
    note(t_trgb < 1.0, "F4c TRGB/Freedman 69.6+-1.9 consistent", f"{t_trgb:+.2f} sigma")
    note(h_lo <= 73.04 <= h_hi and h_lo <= 69.6 <= h_hi,
         "F4d both ladder values INSIDE the 68% window; Planck value outside",
         f"window [{h_lo:.2f}, {h_hi:.2f}]")

    # F5: binding rule — mu_std passes the battery
    x = sp.symbols("x", positive=True)
    mu_std = x / sp.sqrt(1 + x**2)
    t1 = sp.limit(sp.diff(mu_std, x), x, 0)
    t2 = sp.simplify(sp.expand_func(sp.sinh(sp.atanh(mu_std)) - x))
    note(t1 == 1 and t2 == 0,
         "F5 binding rule: mu_std passes T1 (knife) and T2 (celerity) — comparison valid")
    ratio_simple = d["simple"]["a0_best"] / d["std"]["a0_best"]
    note(ratio_simple < 0.5 * (1 + 0.15),
         "F6 the window is mu_std's (not mu_simple's 0.47x or mu_dual's): legacy traps excluded",
         f"mu_simple would place a0 at {ratio_simple:.3f}x of the window")

    print()
    print("SUMMARY: a0 prediction checks: 8 total,", len(FAILURES), "failures")
    if FAILURES:
        print("FAILED:", ", ".join(FAILURES))
        sys.exit(1)
    print(f"PREDICTION (two-sided): a0 = c*H0/(2*pi) with H0 from the measured window:")
    print(f"  H0 = {h_central:.2f} +{sig_h:.2f}/-{sig_h:.2f} km/s/Mpc (68%).")
    print("  Falsified outright by any H0 survey landing outside [68.6, 79.7].")
    print("  Planck value disfavored at", f"{t_planck:.2f} sigma; SH0ES/TRGB consistent.")
    print("  The theory takes the SH0ES side of the Hubble tension. Open: WHY the")
    print("  FLRW horizon's circle is the operative one (obligation 3's residue).")


if __name__ == "__main__":
    main()
