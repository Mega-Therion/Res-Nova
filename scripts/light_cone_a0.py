#!/usr/bin/env python3
"""
Light-cone a0 audit: separate LOCAL physics at emission, TRANSPORT along our past
light cone, and OUR INFERENCE today, for the a0 = c H / 2pi family of readings.

Inputs (all repo or cited):
  - Planck 2018 base LCDM (arXiv:1807.06209): H0 = 67.36, Om = 0.3153, flat, radiation
    as in scripts/horizon_selection_audit.py (same numbers, same q(a), same Kodama form).
  - D5 AeST K(Q) background: |H/H_LCDM - 1| <= 3.6e-3 for a in [1e-4, 1], exactly 0
    today (TARGET_D5_COSMOLOGICAL_SECTOR.md sec 2.4, lines 221-226) -> background-level
    LCDM-equivalent; the bound is carried as a systematic.
  - T3 non-flow 95% a0 interval: 02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json.

Checks (exit 0 iff all pass):
  L1  Etherington: D_L is built from flux bookkeeping (energy redshift, arrival-rate
      dilation, comoving area) and D_A from proper size at emission, as separate
      constructions; eta = D_L/((1+z)^2 D_A) == 1 to 1e-12 at all z.
  L2  Distance exponents, measured by finite-difference log-slopes of the inference
      model (not assumed): BTFR a0_inf ∝ D^-2 (via D_L), rotation-curve a0_inf ∝ D^-1
      (via D_A). Slopes must be -2 and -1 to 1e-5.
  L3  Distance-free combination a0_R^2 / a0_BTFR is invariant (1e-10) under assumed-
      cosmology errors of BOTH scale (H0 73 vs 67.36) and shape (Om 0.25/0.40), per
      redshift bin, and it is NOT invariant when the true photon sector violates
      reciprocity (eta_true = (1+z)^0.1): the combination isolates transport.
  L4  Local readings reproduce the merged horizon audit K7 numbers at z=1:
      Hubble 1.791, Kodama 0.962 (consistency with HORIZON_SELECTION_AUDIT).
  L5  D5 background deviation bound (3.6e-3) is < 2% of the Hubble-vs-Lambda
      separation at z = 0.5 (so using Planck LCDM cannot change the discriminant).
  L6  D_A(z) in LCDM has its maximum in 1.4 < z < 1.8 (textbook ~1.6).
  L7  Discriminant feasibility: with the combination route (scale systematic 0), a
      3-sigma Hubble-vs-Lambda separation at z=1 leaves a positive statistical budget;
      with the BTFR route the H0 zero-point systematic alone consumes > 25% of the
      z=0.5 separation (the route choice is load-bearing).
"""

import json
import math
import pathlib
import sys

from scipy.integrate import quad

ROOT = pathlib.Path(__file__).resolve().parent.parent
J = json.loads(
    (ROOT / "02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json").read_text()
)
T3 = J["treatments"]["T3_nonflow_only"]

c = 299792458.0
Mpc = 3.0856775814913673e22
G = 6.67430e-11
Msun = 1.98892e30
kpc = Mpc / 1e3

results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")


class Cosmo:
    def __init__(self, H0_kms=67.36, Om=0.3153, eta_eps=0.0, Or=None):
        self.H0_kms = H0_kms
        self.H0 = H0_kms * 1e3 / Mpc
        self.Om = Om
        h = H0_kms / 100
        self.Or = 2.469e-5 / h**2 * (1 + 0.2271 * 3.046) if Or is None else Or
        self.OL = 1.0 - Om - self.Or
        self.eta_eps = eta_eps  # reciprocity violation of the TRUE photon sector only

    def E(self, z):
        a = 1 / (1 + z)
        return math.sqrt(self.Or / a**4 + self.Om / a**3 + self.OL)

    def q(self, z):
        a = 1 / (1 + z)
        return (self.Or / a**4 + 0.5 * self.Om / a**3 - self.OL) / self.E(z) ** 2

    def chi(self, z):  # comoving distance (flat => transverse comoving distance)
        return c / self.H0 * quad(lambda zz: 1 / self.E(zz), 0, z, limit=200)[0]

    def D_A(self, z):
        # proper transverse size at emission: l = a_e * chi * dtheta  ->  D_A = chi/(1+z)
        a_e = 1 / (1 + z)
        return a_e * self.chi(z)

    def D_L(self, z):
        # flux bookkeeping: emitted power L spread over comoving sphere area 4 pi chi^2,
        # each photon's energy redshifted by 1/(1+z), arrival rate dilated by 1/(1+z)
        energy_factor = 1 / (1 + z)
        rate_factor = 1 / (1 + z)
        area = 4 * math.pi * self.chi(z) ** 2
        flux_per_L = energy_factor * rate_factor / area
        DL = math.sqrt(1 / (4 * math.pi * flux_per_L))
        return DL * (1 + z) ** self.eta_eps


PL = Cosmo()


# ---------------- LOCAL ----------------
def local_ratios(z, C=PL):
    hub = C.E(z)
    lam = 1.0
    kod = C.E(z) * (1 - C.q(z)) / (1 - C.q(0))
    return hub, lam, kod


a0_T3 = T3["a0_best"]
lo, hi = T3["bootstrap_95"]
a0_hub0 = c * PL.H0 / (2 * math.pi)

# ---------------- L1 Etherington ----------------
worst = max(
    abs(PL.D_L(z) / ((1 + z) ** 2 * PL.D_A(z)) - 1) for z in (0.1, 0.5, 1, 2, 5)
)
check(
    "L1 Etherington eta == 1 (separate D_L / D_A constructions)",
    worst < 1e-12,
    f"max|eta-1|={worst:.1e}",
)


# ---------------- INFERENCE model ----------------
# A synthetic deep-MOND galaxy at redshift z with TRUE a0, TRUE baryonic mass, TRUE
# transition radius R_t (where G M / R_t^2 = a0).  Observables: V_flat (line width,
# redshift-corrected: distance-independent), bolometric flux F (∝ M / D_L,true^2), angular
# transition radius theta_t = R_t / D_A,true.  Observer inverts with assumed cosmology.
def observe(z, a0_true, M_true, C_true):
    V = (G * M_true * a0_true) ** 0.25
    F = M_true / (4 * math.pi * C_true.D_L(z) ** 2)  # mass-to-light folded to 1
    Rt = math.sqrt(G * M_true / a0_true)
    theta = Rt / C_true.D_A(z)
    return V, F, theta


def infer(z, obs, C_ass):
    V, F, theta = obs
    M = F * 4 * math.pi * C_ass.D_L(z) ** 2
    a0_btfr = V**4 / (G * M)
    R = theta * C_ass.D_A(z)
    a0_R = V**2 / R
    return a0_btfr, a0_R, a0_R**2 / a0_btfr


# ---------------- L2 exponents by log-slope ----------------
z = 1.0
M0 = 1e11 * Msun
obs = observe(z, a0_hub0, M0, PL)
eps = 1e-6
Ca = Cosmo(H0_kms=67.36)
Cb = Cosmo(H0_kms=67.36 * (1 + eps), Or=Ca.Or)  # same Omegas -> distances scale as 1/H0 exactly
b_a, r_a, _ = infer(z, obs, Ca)
b_b, r_b, _ = infer(z, obs, Cb)
dlnD = -math.log(1 + eps)
slope_B = math.log(b_b / b_a) / dlnD
slope_R = math.log(r_b / r_a) / dlnD
check(
    "L2 BTFR a0 ∝ D^-2, rotation-curve a0 ∝ D^-1 (measured log-slopes)",
    abs(slope_B + 2) < 1e-5 and abs(slope_R + 1) < 1e-5,
    f"slope_BTFR={slope_B:.6f} slope_R={slope_R:.6f}",
)

# ---------------- L3 combination ----------------
assumed = {
    "H0=73 (scale)": Cosmo(H0_kms=73.0),
    "Om=0.25 (shape)": Cosmo(Om=0.25),
    "Om=0.40 (shape)": Cosmo(Om=0.40),
    "H0=73,Om=0.25": Cosmo(H0_kms=73.0, Om=0.25),
}
table_inf = []
max_comb_dev = 0.0
for zz in (0.5, 1.0, 2.0):
    a0_true = a0_hub0 * PL.E(zz)
    o = observe(zz, a0_true, M0, PL)
    for name, Cass in assumed.items():
        bt, rr, cb = infer(zz, o, Cass)
        table_inf.append((zz, name, bt / a0_true, rr / a0_true, cb / a0_true))
        max_comb_dev = max(max_comb_dev, abs(cb / a0_true - 1))
C_viol = Cosmo(eta_eps=0.1)
o_v = observe(1.0, a0_hub0 * PL.E(1.0), M0, C_viol)
_, _, cb_v = infer(1.0, o_v, PL)
viol_dev = cb_v / (a0_hub0 * PL.E(1.0)) - 1
check(
    "L3 a0_R^2/a0_BTFR invariant under scale+shape errors; broken by eta_true != 1",
    max_comb_dev < 1e-10 and abs(viol_dev) > 1e-2,
    f"max dev (eta=1)={max_comb_dev:.1e}; eta=(1+z)^0.1 at z=1 -> {viol_dev:+.4f}",
)

# ---------------- L4 local consistency with horizon audit ----------------
h1, _, k1 = local_ratios(1.0)
check(
    "L4 Hubble/Kodama a0(z=1)/a0(0) match HORIZON_SELECTION K7 (1.791 / 0.962)",
    abs(h1 - 1.791) < 5e-4 and abs(k1 - 0.962) < 5e-4,
    f"hub={h1:.4f} kod={k1:.4f}",
)

# ---------------- L5 D5 bound ----------------
D5_BOUND = 3.6e-3
sep05 = PL.E(0.5) - 1
check(
    "L5 D5 |dH/H| bound < 2% of Hubble-vs-Lambda separation at z=0.5",
    D5_BOUND < 0.02 * sep05,
    f"sep(0.5)={sep05:.4f}, bound/sep={D5_BOUND/sep05:.4f}",
)

# ---------------- L6 D_A max ----------------
zs = [0.01 * i for i in range(50, 300)]
zmax = max(zs, key=PL.D_A)
check(
    "L6 D_A maximum in 1.4<z<1.8",
    1.4 < zmax < 1.8,
    f"z_max={zmax:.2f}, D_A,max={PL.D_A(zmax)/Mpc:.0f} Mpc",
)

# ---------------- DISCRIMINANT ----------------
# Systematic budget on the RATIO a0(z)/a0(0), fractional, 1-sigma:
#   anchor: T3 95% half-width / 1.96 relative to best (local a0 statistical)
#   zp: distance zero-point mismatch between the z=0 ladder anchor (SPARC, H0=73-like) and
#       high-z cosmological distances (Planck 67.36): full log-difference taken as 1 sigma;
#       enters as |exponent| * ln(73/67.36): BTFR 2, R 1, combination 0
#   Om: Planck sigma(Om)=0.0073 propagated through D(z) with the route's exponent
#   D5: 3.6e-3 (background)
sig_anchor = (hi - lo) / (2 * 1.96) / a0_T3
zp = math.log(73.0 / 67.36)


def sig_Om(zz, expo):
    d1 = Cosmo(Om=0.3153 + 0.0073).D_A(zz)
    d0 = PL.D_A(zz)
    return abs(expo) * abs(math.log(d1 / d0))


disc = []
for zz in (0.5, 1.0, 2.0):
    hub, lam, kod = local_ratios(zz)
    sep = hub - 1.0
    row = {"z": zz, "hubble": hub, "lambda": lam, "kodama": kod, "sep_hub_lam": sep}
    for route, expo in (("BTFR", 2), ("R", 1), ("comb", 0)):
        sys_tot = math.sqrt(
            sig_anchor**2 + (expo * zp) ** 2 + sig_Om(zz, expo) ** 2 + D5_BOUND**2
        )
        # required total 1-sigma fractional precision for a 3-sigma separation, in units of
        # the constant-a0 prediction (fraction of a0(0))
        need = sep / 3
        stat = math.sqrt(need**2 - sys_tot**2) if need > sys_tot else float("nan")
        row[route] = (sys_tot, need, stat)
    disc.append(row)

d1 = [r for r in disc if r["z"] == 1.0][0]
d05 = [r for r in disc if r["z"] == 0.5][0]
check(
    "L7 z=1 combination route leaves positive stat budget; BTFR zp systematic > 25% of z=0.5 separation",
    not math.isnan(d1["comb"][2]) and (2 * zp) > 0.25 * d05["sep_hub_lam"],
    f"comb stat budget z=1: {d1['comb'][2]:.3f}; 2*zp={2*zp:.3f} vs sep(0.5)={d05['sep_hub_lam']:.3f}",
)

# ---------------- print tables ----------------
print(
    "\nLOCAL a0(z)/a0(0) [D] (Planck 2018 LCDM background; D5 AeST equal to <=3.6e-3)"
)
for zz in (0.5, 0.9, 1.0, 1.5, 2.0, 2.4):
    hub, lam, kod = local_ratios(zz)
    print(
        f"  z={zz:<4} Hubble {hub:.3f}  Lambda {lam:.3f}  Kodama {kod:.3f}  | "
        f"a0_Hubble={a0_hub0*hub:.3e}"
    )
print(
    "\nTRANSPORT [D] (eta=1 by construction of a metric, number-conserving photon sector)"
)
for zz in (0.5, 1.0, 2.0):
    print(
        f"  z={zz:<4} D_A={PL.D_A(zz)/Mpc:8.1f} Mpc  D_L={PL.D_L(zz)/Mpc:8.1f} Mpc  (1+z)^2={(1+zz)**2:.2f}  "
        f"eta={PL.D_L(zz)/((1+zz)**2*PL.D_A(zz)):.12f}"
    )
print("\nINFERENCE a0_inf/a0_true (truth: Planck LCDM, Hubble-form a0) [D]")
for zz, name, bt, rr, cb in table_inf:
    print(
        f"  z={zz:<4} assumed {name:<16} BTFR {bt:.4f}  R {rr:.4f}  R^2/BTFR {cb:.6f}"
    )
print(
    f"  eta_true=(1+z)^0.1 at z=1, observer assumes eta=1: R^2/BTFR ratio {1+viol_dev:.4f}"
)
print("\nDISCRIMINANT Hubble vs Lambda (3 sigma), fractional of a0(0) [D]")
print(f"  sigma_anchor={sig_anchor:.3f} zp=ln(73/67.36)={zp:.4f}")
for r in disc:
    s = f"  z={r['z']:<4} sep={r['sep_hub_lam']:.3f} need sigma_tot<={r['BTFR'][1]:.3f} |"
    for route in ("BTFR", "R", "comb"):
        sy, _, st = r[route]
        s += f" {route}: sys={sy:.3f} stat_req={'IMPOSSIBLE' if math.isnan(st) else f'{st:.3f}'} |"
    print(s)
print(
    "\nGenzel+2017 redshift range: Hubble form E(0.9)=%.2f, E(2.4)=%.2f; Milgrom 1703.06110 "
    "'all but exclude ~4 a0 at z~2'" % (PL.E(0.9), PL.E(2.4))
)

print(f"\n{sum(results)}/{len(results)} checks passed")
sys.exit(0 if all(results) else 1)
