#!/usr/bin/env python3
"""
Horizon-selection audit (open residue of obligation 3).

Question: a0 = c*H/(2*pi) reads the 2*pi as a horizon's thermal circle. WHICH
horizon? This script computes the a0 each candidate horizon implies with Planck
2018 base-LCDM parameters (arXiv:1807.06209, TT,TE,EE+lowE+lensing) and tests it
against the distance-robust, non-flow-only extraction T3 (95%) in
02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json, both at the SPARC
ladder zero point and with the whole distance scale moved to Planck (a0 ∝ 1/D).

Checks (exit 0 iff all pass):
  K1  Kodama/Hayward surface gravity of the flat-FLRW apparent horizon is
      DERIVED here from the metric (kappa = 1/2 box_h R at R = 1/H, sympy) and
      must equal the formula quoted in Cai-Cao-Hu arXiv:0809.1554 p.7,
      kappa = -(1 - Rdot_A/(2 H R_A))/R_A, and NOT the sign-flipped variant.
      The sign matters: the flipped variant would land INSIDE the window.
  K2  Rdot_A computed by numerical differentiation of R_A(t) along the
      integrated LCDM solution equals c(1+q) analytically.
  K3  Event-horizon integral reduces to c/H exactly for pure de Sitter, and for
      LCDM lies strictly between c/H0 and c/H_Lambda.
  K4  Particle horizon (comoving, today) lands in the textbook ~14 Gpc range.
  K5  Numerical consistency table vs T3 95%: Hubble/apparent (quasi-static)
      form inside at both zero points; dS/Kodama/particle/cH0/c sqrtL outside at
      both; the true LCDM event horizon is excluded ONLY at the ladder zero point.
  K6  Milgrom's own identification (astro-ph/9805346 eq. 8-9: a0 = 2 (Lambda/3)^1/2,
      c=1) is outside.
  K7  Discriminating power of a0(z): at z=1 the Hubble form and the Lambda form
      differ by more than the full relative width of the T3 95% interval.
"""

import json
import math
import pathlib
import sys

import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp

ROOT = pathlib.Path(__file__).resolve().parent.parent
J = json.loads(
    (ROOT / "02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json").read_text()
)
T3 = J["treatments"]["T3_nonflow_only"]["bootstrap_95"]

c = 299792458.0
Mpc = 3.0856775814913673e22
H0_kms = 67.36
H0 = H0_kms * 1e3 / Mpc
Om = 0.3153
h = H0_kms / 100
Or = 2.469e-5 / h**2 * (1 + 0.2271 * 3.046)
OL = 1.0 - Om - Or
LADDER_SHIFT = (
    67.36 / 73.0
)  # move the SPARC ladder zero point to Planck: a0 -> a0 * shift

results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")


def E(a):
    return math.sqrt(Or / a**4 + Om / a**3 + OL)


def q_of(a):
    # q = -1 - Hdot/H^2 = sum_i (1+3w_i)/2 Omega_i(a): radiation 1, matter 1/2, Lambda -1
    num = Or / a**4 + 0.5 * Om / a**3 - OL
    return num / E(a) ** 2


# ---------------- K1: Kodama surface gravity from the metric ----------------
t, r = sp.symbols("t r", positive=True)
A = sp.Function("a")(t)
R = A * r
# 2-metric h = diag(-1, a^2) on (t, r); box_h R = (1/sqrt|h|) d_i (sqrt|h| h^ij d_j R)
sqrth = A
boxR = (
    sp.diff(sqrth * (-1) * sp.diff(R, t), t)
    + sp.diff(sqrth * (1 / A**2) * sp.diff(R, r), r)
) / sqrth
kappa_expr = sp.simplify(boxR / 2)
Hs = sp.diff(A, t) / A
# at the apparent horizon R = 1/H (c=1)  -> r = 1/(a H)
kappa_AH = sp.simplify(kappa_expr.subs(r, 1 / (A * Hs)))
RA = 1 / Hs
quoted = -(1 - sp.diff(RA, t) / (2 * Hs * RA)) / RA
flipped = -(1 + sp.diff(RA, t) / (2 * Hs * RA)) / RA
d_quoted = sp.simplify(kappa_AH - quoted)
d_flipped = sp.simplify(kappa_AH - flipped)
# magnitude check (overall sign of box is signature-convention dependent)
ok_k1 = (d_quoted == 0 or sp.simplify(kappa_AH + quoted) == 0) and not (
    d_flipped == 0 or sp.simplify(kappa_AH + flipped) == 0
)
check(
    "K1 Kodama kappa from metric == Cai-Cao-Hu quoted sign (not flipped)",
    ok_k1,
    f"kappa_AH={sp.simplify(kappa_AH)}",
)

q0 = q_of(1.0)
kodama_factor = (1 - q0) / 2
flipped_factor = (3 + q0) / 2

# ---------------- K2: Rdot_A numerically along LCDM ----------------
sol = solve_ivp(
    lambda tt, y: [y[0] * H0 * E(y[0])],
    [0, 2e17],
    [1.0],
    dense_output=True,
    rtol=1e-11,
    atol=1e-13,
)
dt = 1e14
sol_b = solve_ivp(
    lambda tt, y: [y[0] * H0 * E(y[0])],
    [0, -2e17],
    [1.0],
    dense_output=True,
    rtol=1e-11,
    atol=1e-13,
)
a_p = sol.sol(dt)[0]
a_m = sol_b.sol(-dt)[0]
RA_p = c / (H0 * E(a_p))
RA_m = c / (H0 * E(a_m))
RAdot_num = (RA_p - RA_m) / (2 * dt)
RAdot_an = c * (1 + q0)
check(
    "K2 dR_A/dt numeric == c(1+q0)",
    abs(RAdot_num / RAdot_an - 1) < 1e-4,
    f"num={RAdot_num/c:.6f}c an={RAdot_an/c:.6f}c q0={q0:.4f}",
)


# ---------------- K3: event horizon ----------------
def event_horizon(Om_, OL_, Or_):
    f = lambda a: 1.0 / (a * a * math.sqrt(Or_ / a**4 + Om_ / a**3 + OL_))
    return c / H0 * quad(f, 1, np.inf, limit=400)[0]


RE_dS = event_horizon(0.0, 1.0, 0.0)
RE = event_horizon(Om, OL, Or)
check("K3a event horizon, pure dS == c/H", abs(RE_dS / (c / H0) - 1) < 1e-8)
check(
    "K3b LCDM: c/H0 < R_E < c/H_Lambda",
    c / H0 < RE < c / (H0 * math.sqrt(OL)),
    f"R_E={RE/Mpc/1e3:.3f} Gpc, c/H0={c/H0/Mpc/1e3:.3f}, c/H_L={c/(H0*math.sqrt(OL))/Mpc/1e3:.3f}",
)

# ---------------- K4: particle horizon ----------------
RP = (
    c
    / H0
    * quad(lambda a: 1.0 / (a * a * E(a)), 0, 1, limit=400, points=[1e-4, 1e-2])[0]
)
check(
    "K4 particle horizon in [13.5, 15] Gpc",
    13.5 < RP / Mpc / 1e3 < 15.0,
    f"R_P={RP/Mpc/1e3:.2f} Gpc",
)

# ---------------- K5: candidate table ----------------
HL = H0 * math.sqrt(OL)
cands = {
    "Hubble/apparent horizon, quasi-static T=1/(2pi R_A) [Cai-Kim, Cai-Cao-Hu]": c
    * H0
    / (2 * math.pi),
    "de Sitter static patch / asymptotic event horizon H_L=H0 sqrt(OL)": c
    * HL
    / (2 * math.pi),
    "LCDM cosmological event horizon today, c^2/(2pi R_E)": c * c / (2 * math.pi * RE),
    "apparent horizon, Kodama-Hayward |kappa|/2pi = cH0(1-q0)/(4pi)": c
    * H0
    * kodama_factor
    / (2 * math.pi),
    "particle horizon today, c^2/(2pi R_P)": c * c / (2 * math.pi * RP),
    "Milgrom a_dS = cH0 (no 2pi)": c * H0,
    "c sqrt(Lambda)/2pi = cH0 sqrt(3 OL)/2pi": c
    * H0
    * math.sqrt(3 * OL)
    / (2 * math.pi),
    "[sabotage] Kodama with sign flipped, cH0(3+q0)/(4pi)": c
    * H0
    * flipped_factor
    / (2 * math.pi),
}
lo, hi = T3
lo2, hi2 = lo * LADDER_SHIFT, hi * LADDER_SHIFT
print(
    f"\nT3 95% (ladder zero point): [{lo:.4e}, {hi:.4e}]; moved to Planck scale: [{lo2:.4e}, {hi2:.4e}]"
)
print(
    f"q0={q0:.4f}  Kodama factor (1-q0)/2={kodama_factor:.4f}  R_E={RE/Mpc/1e3:.3f} Gpc  R_P={RP/Mpc/1e3:.2f} Gpc"
)
inside = {}
for k, v in cands.items():
    i1, i2 = lo <= v <= hi, lo2 <= v <= hi2
    inside[k] = (i1, i2)
    print(f"  a0={v:.4e}  in(ladder)={i1!s:5} in(Planck-scale)={i2!s:5}  {k}")
keys = list(cands)
check("K5a Hubble quasi-static form inside at both zero points", all(inside[keys[0]]))
check(
    "K5b dS/H_L, Kodama, particle, cH0, c sqrtL outside at BOTH zero points",
    all(not any(inside[keys[i]]) for i in (1, 3, 4, 5, 6)),
)
check(
    "K5d LCDM event horizon: outside at ladder zero point, INSIDE at Planck-scale zero point (ladder-covariant, not excluded)",
    (not inside[keys[2]][0]) and inside[keys[2]][1],
)
check(
    "K5c sign-flipped Kodama WOULD be inside at ladder zero point (sign is load-bearing)",
    inside[keys[7]][0],
)

# ---------------- K6: Milgrom 1999 identification ----------------
a0_milgrom = 2 * c * HL  # a0_hat = 2 (Lambda/3)^{1/2}, c=1 -> 2 c H_L
check(
    "K6 Milgrom astro-ph/9805346 a0_hat=2cH_L outside",
    not (lo2 <= a0_milgrom <= hi),
    f"{a0_milgrom:.3e}",
)

# ---------------- K7: a0(z) discriminant ----------------
a1 = 0.5
ratio_hubble = E(a1)
ratio_kodama = E(a1) * (1 - q_of(a1)) / (1 - q0)
rel_width = (hi - lo) / cands[keys[0]]
print(
    f"\na0(z=1)/a0(0): Hubble form {ratio_hubble:.3f}; Kodama form {ratio_kodama:.3f}; Lambda form 1.000; "
    f"T3 95% relative width {rel_width:.3f}"
)
check(
    "K7 Hubble vs Lambda form separation at z=1 exceeds T3 95% relative width",
    (ratio_hubble - 1) > rel_width,
)

print(f"\n{sum(results)}/{len(results)} checks passed")
sys.exit(0 if all(results) else 1)
