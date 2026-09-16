#!/usr/bin/env python3
"""Machine verification for REPRESENTATION_AUDIT_A0_SPARC_2026-09-16.md (RN-CO-05).

Representation audit of the empirical acceleration scale a0:
- C-class: equivalent dresses of the SAME claimed number (horizon, crossing-time,
  frequency units) — verified identical, selection-free.
- P-class: genuinely DIFFERENT candidate numbers (H0-choice family, Lambda forms,
  Milgrom's a_dS, extraction-mu dependence) — measured against the live mu_std
  bootstrap window, with what-kills-what stated.

All inputs are from the corpus's own JSON artifacts (A0_MEASUREMENT.json,
A0_ESTIMATE.json, A0_REEXTRACTION_MU_STD.json) and standard constants.
Run:  python3 scripts/a0_representation_audit.py
"""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
gal = root / "02_galaxy_dynamics"

meas = json.loads((gal / "A0_MEASUREMENT.json").read_text())
reex = json.loads((gal / "A0_REEXTRACTION_MU_STD.json").read_text())

c = 2.99792458e8                 # m/s
Mpc = 3.0856775814913673e22      # m
a0_claim = meas["a0_claimed_cH0_over_2pi"]     # 1.0421e-10, corpus canonical
a0_mond = meas["a0_mond_empirical"]            # 1.2e-10, literature fitted value

# live closure (mu_std) window from the 2026-09-12 re-extraction
w_lo, w_hi = reex["mu_std"]["bootstrap_68"]
w_mid = reex["mu_std"]["a0_best"]
w_sig = (w_hi - w_lo) / 2                        # bootstrap half-width as sigma proxy

print("== C-class: equivalent dresses of the canonical claim ==")
# C1: implied H0 of the corpus canonical a0 = cH0/2pi
H0_ms = a0_claim * 2 * 3.141592653589793 / c        # 1/s
H0_kmsMpc = H0_ms * Mpc / 1e3
print(f"C1  a0 = cH0/2pi = {a0_claim:.4e} implies H0 = {H0_kmsMpc:.1f} km/s/Mpc (Planck-adjacent)")
# C2: crossing-time identity  c/a0 = 2pi/H0  (t_MOND = one Hubble period)
t_mond = c / a0_claim
t_hubble_period = 2 * 3.141592653589793 / H0_ms
print(f"C2  c/a0 = {t_mond:.4e} s ; 2pi/H0 = {t_hubble_period:.4e} s ; identical: {abs(t_mond - t_hubble_period) < 1}")
# C3: frequency units a0/c = H0/2pi
print(f"C3  a0/c = {a0_claim/c:.4e} Hz ; H0/2pi = {H0_ms/6.283185307179586:.4e} Hz (identical by C1)")
print("   -> all three dresses are the SAME number; no selection content (Theorem-D discipline)")

print()
print("== P-class 1: H0-choice family (a0 = cH0/2pi at different H0) ==")
for label, H0k in [("Planck 67.4", 67.4), ("canonical 70", 70.0), ("SH0ES 73.0", 73.0)]:
    a0 = c * (H0k * 1e3 / Mpc) / 6.283185307179586
    inside = "INSIDE" if w_lo <= a0 <= w_hi else "OUTSIDE"
    tension = (a0 - w_mid) / w_sig
    print(f"  H0={label:14s} -> a0 = {a0:.4e}  {inside:7s} mu_std window  tension {tension:+.2f} sigma_boot")

print()
print("== P-class 2: Lambda / de Sitter forms (NOT equivalent to the Hubble form) ==")
OmL = 0.69
a0_lambda = a0_claim * (3 * OmL) ** 0.5      # c^2 sqrt(Lambda)/2pi
a0_ds = a0_claim * OmL ** 0.5                # c H_ds / 2pi, H_ds = H0 sqrt(OmL)
print(f"  c^2 sqrt(Lambda)/2pi = {a0_lambda:.4e}  (factor {((3*OmL)**0.5):.3f} HIGH vs canonical)")
print(f"  c H_ds/2pi           = {a0_ds:.4e}  (factor {OmL**0.5:.3f} LOW vs canonical)")
print("  -> the three forms differ by MEASURED factors sqrt(3 OmL), sqrt(OmL):")
print("     the canonical claim is specifically the HUBBLE-radius form, not the")
print("     de Sitter horizon form. The choice is cosmology-dependent [O].")

print()
print("== P-class 3: Milgrom's a_dS = cH0 (no 2pi) ==")
a_dS = c * H0_ms
print(f"  a_dS = cH0 = {a_dS:.4e}  -> ratio to mu_std window centre: {a_dS/w_mid:.2f} (factor ~2pi off)")
print("  -> the 2pi is REQUIRED for numerical agreement; its first-principles origin stays [O]")
print("     (D2 supplement 6.2 flagged the same offset on the Unruh route)")

print()
print("== P-class 4: extraction-mu dependence (F6) ==")
d_lo, d_hi = reex["mu_dual"]["bootstrap_68"]
d_mid = reex["mu_dual"]["a0_best"]
print(f"  mu_dual extraction: a0 = {d_mid:.4e}  68% [{d_lo:.4e}, {d_hi:.4e}]")
print(f"  mu_std  extraction: a0 = {w_mid:.4e}  68% [{w_lo:.4e}, {w_hi:.4e}]")
shift = (w_mid - d_mid) / d_mid * 100
overlap = not (d_hi < w_lo or w_hi < d_lo)
print(f"  shift: {shift:+.1f}%  windows overlap: {overlap}")
print(f"  direction provable: mu_std(x) > mu_dual(x) for all x>0  (x/sqrt(1+x^2) > x/(1+x)")
print(f"  iff sqrt(1+x^2) < 1+x iff 0 < 2x) -- same data sits deeper in MOND at fixed a0,")
print(f"  so the fit compensates with a larger a0. Verified in A0_REEXTRACTION headline.")
print(f"  consequence: the fitted-a0 row of any table MUST state its extraction mu;")
print(f"  a0 alone is not mu-invariant -- the pair (mu, a0) is what SPARC measures.")
# old-window tension (A0_MEASUREMENT harness, mu_dual-era)
t_old = meas["tension_claim_sigma"]
print(f"  legacy harness (mu_dual era): tension of canonical claim = {t_old:.2f} sigma (stat+syst)")

print()
print("== P-class 5: precision/evolution constraints (F7) ==")
v3 = reex["v3_a0z_test"]
print(f"  v3 a0(z) test under live closure: chi2 const {v3['chi2_H_const']:.3f} vs horizon")
print(f"  {v3['chi2_H_horizon']:.3f} -> delta chi2 = {v3['delta_chi2']:.3f}, significance")
print(f"  {v3['significance_sigma']:.2f} sigma, verdict {v3['verdict']}")
print(f"  ever_conclusive across bootstrap 68%: {v3['across_bootstrap_68']['ever_conclusive']}")
print("  -> the 5.9 sigma constant-a0 verdict (extracted under falsified mu_dual) is")
print("     unrecoverable; a0(z) remains open, not ruled out")

print()
print("== SUMMARY ==")
print(f"  live a0 (mu_std, harness-qualified): {w_mid:.4e} m/s^2, 68% [{w_lo:.4e}, {w_hi:.4e}]")
print(f"  canonical claim cH0/2pi (H0=67.4):    {a0_claim:.4e} m/s^2")
print(f"  tension vs live window: {(a0_claim - w_mid)/w_sig:+.2f} sigma_boot")
print(f"  at SH0ES H0=73: tension {(c*73e3/Mpc/6.283185307179586 - w_mid)/w_sig:+.2f} sigma_boot")
print(f"  validation gap: reextract harness gives {d_mid:.3e} for mu_dual vs A0_ESTIMATE's")
print(f"  1.107e-10 -- exact-pipeline reproduction remains [O] (corpus's own record)")
