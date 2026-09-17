#!/usr/bin/env python3
"""Machine verifier for A0_HIGHZ_COROLLARY_COMPARISON_2026-09-17.md. Exit 0 = all checks pass."""
import math, sys

OK, FAIL = 0, 0
def check(name, cond, detail=""):
    global OK, FAIL
    if cond: OK += 1; print(f"  [OK]   {name} {detail}")
    else: FAIL += 1; print(f"  [FAIL] {name} {detail}")

Om, Ol = 0.315, 0.685  # Planck 2018 per PR #68
def corollary(z): return math.sqrt(Om * (1 + z)**3 + Ol)

# C1: corollary at z=1 = 1.790, ln-separation from constancy = 0.582
r1 = corollary(1.0)
check("C1 corollary(1)=1.790", abs(r1 - 1.790) < 5e-3, f"got {r1:.4f}")
check("C1 ln-separation 0.582", abs(math.log(r1) - 0.582) < 5e-3, f"got {math.log(r1):.4f}")

# C2: corollary at the 2-bin z_eff values matches the PR #68 'Hubble pred' column
c_lo, c_hi = corollary(0.867), corollary(1.960)
check("C2 corollary(0.867)=1.654", abs(c_lo - 1.654) < 5e-3, f"got {c_lo:.4f}")
check("C2 corollary(1.960)=2.976", abs(c_hi - 2.976) < 5e-3, f"got {c_hi:.4f}")

# C3: the corollary's ln-deviations from the measured points are < 0.5 (calibration nuisance size)
dev_lo = abs(math.log(2.597) - math.log(c_lo))
dev_hi = abs(math.log(2.286) - math.log(c_hi))
check("C3 ln-dev both bins < 0.5", dev_lo < 0.5 and dev_hi < 0.5,
      f"lo {dev_lo:.3f} hi {dev_hi:.3f}")

# C4: the corollary is OUTSIDE both 95% intervals, in opposite directions
check("C4 below low-bin 95% CI", c_lo < 1.954, f"{c_lo:.4f} < 1.954")
check("C4 above high-bin 95% CI", c_hi > 2.685, f"{c_hi:.4f} > 2.685")

# C5: S8 link — the injected 1.791x equals the corollary at z=1; bias far below the separation
check("C5 S8 injection = corollary(1)", abs(1.791 - r1) < 1e-2, "1.791 vs %.4f" % r1)
check("C5 S8 bias 0.0416 << 0.582", 0.0416 < 0.1 * 0.582)

# C6: Ciocan+2026 external row: 2.38e-10 / 1.16306e-10 = 2.05, within 0.14 ln of corollary(1)
cioc = 2.38e-10 / 1.16306e-10
check("C6 Ciocan ratio 2.05", abs(cioc - 2.05) < 1e-2, f"got {cioc:.3f}")
check("C6 Ciocan within 0.14 ln of corollary", abs(math.log(cioc) - math.log(r1)) < 0.14,
      f"{abs(math.log(cioc)-math.log(r1)):.3f}")

print(f"\n{OK} passed, {FAIL} failed (of {OK+FAIL})")
sys.exit(0 if FAIL == 0 else 1)
