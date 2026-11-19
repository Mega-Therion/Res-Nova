#!/usr/bin/env python3
"""
The three-exclusion feasibility scan for the AeST completion of mu_std.

Question: is there any point in AeST's parameter space that satisfies ALL THREE
exclusions at once?

  (1) Cassini Q2       bare mu_std excluded; needs screening
  (2) k-essence        C^AB -> 0 at mu=0 drives c_s^2 -> 2 (superluminal)
  (3) BBN vs stability 5% bound on G_cosmo/G_N forces lam_s >= 19,
                       non-folding caps lam_s < (27+12*sqrt6)/5 = 11.2788

Formulas taken verbatim from the corpus, not invented:
  G_cosmo/G_N = lam*(2-K_B)/(2*(1+lam))        Wave3BBNAndSpinCCP2Bounds.lean:12
  non-folding  lam < (27+12*sqrt6)/5            Wave3BBNAndSpinCCP2Bounds.lean:128
  c_s^2        (2-K_B)(1+K_B*lam/2)/(K2*K_B)   TARGET_D6_RELATIVISTIC_STABILITY.md:38
  stability    0 < K_B < 2                     Minkowski stability ceiling

Run: python3 audits/2026-11-18/aest_three_exclusion_scan.py   (exit 0)
"""
import math
from itertools import product

LAM_CEIL = (27 + 12*math.sqrt(6))/5          # 11.2788... non-folding ceiling
RATIO_CEIL = LAM_CEIL/(1+LAM_CEIL)           # sqrt(27/32) = 0.91856

def g_ratio(KB, lam):
    """G_cosmo/G_N = lam(2-K_B)/(2(1+lam))."""
    return lam*(2-KB)/(2*(1+lam))

def cs2(KB, lam, K2):
    """Minkowski scalar speed squared; K2 is the corpus's calligraphic K2."""
    return (2-KB)*(1+0.5*KB*lam)/(K2*KB)

print("="*78)
print("AeST THREE-EXCLUSION SCAN")
print("="*78)

print(f"\nnon-folding ceiling      lam_s < {LAM_CEIL:.6f}")
print(f"implied ratio ceiling    lam/(1+lam) < {RATIO_CEIL:.6f}  = sqrt(27/32) = {math.sqrt(27/32):.6f}")

# --- what is the best G_cosmo/G_N achievable inside the stability window? ---
# sup is analytic: G ratio increases as K_B -> 0 and is increasing in lam, so
# sup = lim_{K_B->0, lam->LAM_CEIL} = LAM_CEIL/(1+LAM_CEIL)
sup_ratio = RATIO_CEIL
grid = max(g_ratio(KB, lam) for KB in [i/10000 for i in range(1,20000)]
                                 for lam in [LAM_CEIL*(1-e) for e in (1e-2,1e-3,1e-4,1e-6)])
print(f"\nsup G_cosmo/G_N inside {{0<K_B<2, 0<lam<{LAM_CEIL:.4f}}} = {sup_ratio:.6f}  (analytic: K_B->0, lam->ceiling)")
print(f"  grid corroboration (K_B>=1e-4, lam within 1e-6 of ceiling): {grid:.6f}")
print(f"  grid <= sup: {grid <= sup_ratio + 1e-12}")

# --- threshold BBN bound at which feasibility opens ---
delta_min = 1 - RATIO_CEIL
print(f"\nBBN bound delta (require G_cosmo/G_N >= 1-delta):")
print(f"  feasibility opens only for delta > {delta_min:.6f}  ({100*delta_min:.3f}%)")
for pct in (5, 8, 8.2, 9, 10, 15):
    ok = pct/100 > delta_min
    print(f"  {pct:>5}% bound (need >= {1-pct/100:.2f}):  {'FEASIBLE' if ok else 'IMPOSSIBLE'}")

# --- if feasible at 10%, where is the region? ---
print("\n" + "="*78)
print("10% BBN bound: the feasible region")
print("="*78)
print(f"{'lam_s':>9}{'K_B max':>12}{'c_s^2 (K2=75)':>16}{'c_s^2 (K2=150)':>16}{'causal?':>10}")
for lam in (9.0, 10.0, 11.0, LAM_CEIL-1e-6):
    # K_B such that g_ratio == 0.90 exactly
    KB = 2*(1 - 0.90*(1+lam)/lam)
    if KB <= 0: continue
    c75, c150 = cs2(KB, lam, 75), cs2(KB, lam, 150)
    print(f"{lam:>9.4f}{KB:>12.5f}{c75:>16.4f}{c150:>16.4f}{'yes' if c150<=1 else 'NO':>10}")

# --- what K2 does causality demand at the tightest viable point? ---
lam = LAM_CEIL - 1e-9
KB = 2*(1 - 0.90*(1+lam)/lam)
need = (2-KB)*(1+0.5*KB*lam)/KB        # K2 required for c_s^2 = 1
print(f"\nat lam_s -> {lam:.4f}, K_B -> {KB:.5f}:")
print(f"  c_s^2 <= 1 requires K2 >= {need:.3f}")
print(f"  corpus D6-04 uses K2 = 75 and 7.5e5 -> c_s^2 = {cs2(KB,lam,75):.4f} and {cs2(KB,lam,7.5e5):.6f}")

# --- Cassini: is screening available at any point in the region? ---
print("\n" + "="*78)
print("Cassini: the one that parameter choice cannot fix")
print("="*78)
print("""  Screening in AeST requires J built only from Y^p, p >= 3/2, with no linear piece.
  The live embedding is J_std(Y) = F_std(sqrt Y), so J'(Y) = mu_std(sqrt Y) -> 1 as Y -> inf,
  i.e. J ~ Y: a LINEAR piece. In SZ's classification that is the TRACKING branch.
  On tracking, G_N = (1+1/lam_s) G_hat and the scalar leaves a residual, not a screened zero.

  Residual for mu_std:  1 - mu_std(x) ~ 1/(2x^2)  ->  force deficit a0*x*[1-mu] -> a0/2
  A constant offset does not decay with r, and no choice of lam_s or K_B removes it
  because (1+lam_s) > 1 for every lam_s > 0.

  => Cassini is NOT a tuning problem in AeST. It is an embedding-class problem.
     Passing it requires either (a) a J with no linear term (p >= 3/2), which changes
     the galaxy law and must be re-fitted to SPARC, or (b) a second scale that switches
     the fifth force off below some acceleration, which AeST alone does not supply.""")

print("\n" + "="*78)
print("VERDICT")
print("="*78)
print(f"""  c_T = c                PASS  structural (Einstein-Hilbert tensor sector, no Weyl coupling)
  c_s^2 <= 1             PASS  requires K2 >~ {need:.0f}; K2 = 75 gives {cs2(KB,LAM_CEIL-1e-9,75):.2f}
  BBN at 5%              FAIL  exact no-go: ceiling {RATIO_CEIL:.4f} < 0.95, gap {0.95-RATIO_CEIL:.4f}
  BBN at > {100*delta_min:.2f}%        PASS  lam_s -> {LAM_CEIL:.4f}, K_B <~ {KB:.4f}
  Cassini Q2             FAIL  tracking branch, constant residual a0/2; not tunable

  Two of three are survivable by parameter choice. The third is not, and it is the
  binding one. The live bottleneck is the embedding class, not the numbers.""")
