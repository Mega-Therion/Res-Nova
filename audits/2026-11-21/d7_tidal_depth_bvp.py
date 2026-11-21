#!/usr/bin/env python3
"""D7 directional-tidal fifth-force boundary-value problem.

Pre-registered before the solve (thresholds are literals below, taken from
receipts already on disk; nothing here is adjusted after the run):

  Mercury: anomalous orbit-averaged radial acceleration must stay under the
    1.6 mas/century 2-sigma perihelion budget used in
    audits/2026-11-18/ell2_ell0_separability.py.
  Cassini: the quadrupole acceleration amplitude at 9.5 AU, converted to the
    repo Q2 unit by dividing by r^2, must sit at or below 5.2e-27 s^-2
    (Park et al. 2026 window used in 02_galaxy_dynamics/cassini_pareto_scan.py:
    1.6e-27 +/- 1.8e-27 at 2 sigma).
  SPARC: the same coupling must supply an acceleration of order a0
    (1.1607e-10 m/s^2) at a characteristic disk point g_N = a0. A fractional
    correction below 1e-3 of a0 does not produce mu_std rotation curves.
  X-COP: Gate 2 already killed unscreened hydrostatic dust at med R200
    0.608-0.621 (exploration/d10_xcop/GATE2_XCOP_MEASURED_ICM.json), with the
    pass window R500 in [0.80, 1.25] and R200 inside that same window. This
    script does not refit the 12 clusters. It tests whether any monotonic
    function of |Phi|/c^2 can be off in the solar system and on in a galaxy
    while staying off in a cluster.

The equation solved is the vacuum Poisson problem for one coupling kappa:

    nabla^2 varphi = kappa * T_parallel
    T_parallel = S_ij (e_i e_j - delta_ij/3) = - (2 GM / r^3) P_2(cos theta)
    varphi -> 0 at infinity, no homogeneous r^2 or r^-3 piece.

Xi is applied afterwards as a multiplicative gate on kappa. The zero-parameter
gate is Xi = 1. The monotonic-depth gate is any nondecreasing function of
|Phi|/c^2. A two-scale window is recorded as failing uniqueness: it needs two
dimensionful edges that a0, G, and c do not fix.

Run: python3 audits/2026-11-21/d7_tidal_depth_bvp.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

# --- pre-registered constants (do not fit) ---
A0 = 1.1607e-10
GM_SUN = 1.32712e20
AU = 1.495978707e11
C = 2.99792458e8
R_MERC = 5.7909e10
R_SAT = 9.5 * AU
PREC_BOUND_MAS = 1.6
ORBITS_PER_CY = 36525.0 / 87.969
MAS = 4.848136811e-6
Q2_CAP = 5.2e-27
R200_LO, R200_HI = 0.80, 1.25
# Galactic centre in ecliptic coordinates (IAU, J2000-level; fixed, not fit).
B_GC_DEG = -5.53
KPC = 3.085677581e19
M_SUN = 1.98847e30
G = 6.67430e-11

HERE = Path(__file__).resolve().parent


def orbit_mean_P2(b_deg: float) -> float:
    """Time average of P2(cos gamma) on a circular ecliptic orbit.

    cos gamma = cos(b) cos(Delta lambda), so <cos^2 gamma> = cos^2(b)/2.
    """
    cb = math.cos(math.radians(b_deg))
    mean_mu2 = 0.5 * cb * cb
    return 0.5 * (3.0 * mean_mu2 - 1.0)


def mercury_budget() -> dict:
    g_n = GM_SUN / R_MERC**2
    a_max = (
        (PREC_BOUND_MAS * 1e-3 * MAS)
        * GM_SUN
        / (ORBITS_PER_CY * 2.0 * math.pi * R_MERC**2)
    )
    return {"g_N": g_n, "a_tilde_max": a_max, "rel_max": a_max / g_n}


def solve_p2_shell(kappa: float, n: int = 4000) -> dict:
    """Finite-difference solve of the l=2 radial Poisson equation on a shell.

    (u'' + 2 u'/r - 6 u/r^2) = kappa * (-2 GM / r^3)
    Outer boundary: u' + u/r = 0 (kills the growing r^2 solution and the r^-3
    solution; the particular 1/r solution saturates it).
    Inner boundary: the same decay law, so the only solution the two-point
    conditions admit is the particular integral.
    """
    r_in = 0.2 * AU
    r_out = 50.0 * AU
    r = np.geomspace(r_in, r_out, n)
    # Unknowns u[1:-1]; endpoints eliminated by the decay condition.
    # Second-order nonuniform finite differences.
    m = n - 2
    A = np.zeros((m, m))
    rhs = np.zeros(m)
    for i, ri in enumerate(r[1:-1], start=1):
        rm, rp = r[i - 1], r[i + 1]
        # Lagrange second and first derivatives at ri through (rm, ri, rp).
        # u_m coefficient, u coefficient, u_p coefficient.
        h1, h2 = ri - rm, rp - ri
        # u' = a_m u_m + a_0 u + a_p u_p
        a_m = -h2 / (h1 * (h1 + h2))
        a_p = h1 / (h2 * (h1 + h2))
        a_0 = -(a_m + a_p)
        # u''
        b_m = 2.0 / (h1 * (h1 + h2))
        b_p = 2.0 / (h2 * (h1 + h2))
        b_0 = -(b_m + b_p)
        row = i - 1
        coef_m = b_m + 2.0 * a_m / ri
        coef_0 = b_0 + 2.0 * a_0 / ri - 6.0 / ri**2
        coef_p = b_p + 2.0 * a_p / ri
        if i == 1:
            # u_in from u' + u/r = 0 using the one-sided relation is imposed
            # by substituting u[0] = u[1] * r[1] / r[0] * (matched log slope
            # of 1/r across the first cell): u(r) r = const => u_in = u_1 * r_1/r_in
            scale = r[1] / r[0]
            A[row, 0] += coef_0 + coef_m * scale
            A[row, 1] += coef_p
        elif i == n - 2:
            scale = r[-2] / r[-1]
            A[row, -1] += coef_0 + coef_p * scale
            A[row, -2] += coef_m
        else:
            A[row, row - 1] += coef_m
            A[row, row] += coef_0
            A[row, row + 1] += coef_p
        rhs[row] = kappa * (-2.0 * GM_SUN / ri**3)
    u_inner = np.linalg.solve(A, rhs)
    u = np.empty(n)
    u[1:-1] = u_inner
    u[0] = u[1] * r[1] / r[0]
    u[-1] = u[-2] * r[-2] / r[-1]
    u_exact = kappa * GM_SUN / (3.0 * r)
    rel = np.max(np.abs(u - u_exact) / np.maximum(np.abs(u_exact), 1e-30))
    return {"r": r, "u": u, "u_exact": u_exact, "max_rel_fd": float(rel)}


def accel_from_kappa(kappa: float, r: float, mean_p2: float) -> float:
    """Orbit-averaged radial acceleration of varphi = (kappa GM /(3 r)) P2."""
    return -(kappa * GM_SUN / (3.0 * r**2)) * mean_p2


def q2_of_kappa(kappa: float, r: float) -> float:
    """Quadrupole acceleration amplitude / r^2, in s^-2.

    a_r amplitude is |kappa| GM /(3 r^2). Dividing by r^2 gives the curvature
    scale that the Cassini Q2 bound constrains (s^-2).
    """
    return abs(kappa) * GM_SUN / (3.0 * r**4)


def main() -> None:
    mean_p2 = orbit_mean_P2(B_GC_DEG)
    bud = mercury_budget()
    # kappa such that |orbit-averaged a_r| = a_tilde_max at Mercury.
    # |kappa| * GM /(3 R^2) * |mean_p2| = a_max => |kappa|_max = 3 a_max R^2 / (GM |mean_p2|)
    kappa_max = 3.0 * bud["a_tilde_max"] * R_MERC**2 / (GM_SUN * abs(mean_p2))

    # FD confirmation at the capped coupling.
    fd = solve_p2_shell(kappa_max)
    # Accelerations at the cap.
    a_merc = accel_from_kappa(kappa_max, R_MERC, mean_p2)
    a_sat = accel_from_kappa(kappa_max, R_SAT, mean_p2)
    q2_sat = q2_of_kappa(kappa_max, R_SAT)
    # What kappa would be required to move Cassini at the 2-sigma edge.
    kappa_q2 = Q2_CAP * 3.0 * R_SAT**4 / GM_SUN
    a_merc_if_q2 = accel_from_kappa(kappa_q2, R_MERC, mean_p2)

    # SPARC characteristic point: g_N = a0, so the mu_std boost is order a0.
    # With Xi = 1 and kappa at the Mercury cap, fractional radial correction
    # is |kappa| |mean_p2| / 3, independent of radius for this 1/r potential.
    frac = abs(kappa_max) * abs(mean_p2) / 3.0
    delta_a_at_a0 = frac * A0

    # Potentials in units of c^2. Solar potential at the planet, galactic
    # disk potential ~ v^2, cluster potential ~ sigma^2. These three numbers
    # are the depth axis. They are not fit.
    phi = {
        "saturn_solar": GM_SUN / (C**2 * R_SAT),
        "mercury_solar": GM_SUN / (C**2 * R_MERC),
        "galaxy_200kms_disk": (200e3) ** 2 / C**2,
        "cluster_1000kms": (1000e3) ** 2 / C**2,
    }
    # Monotonic nondecreasing Xi(|Phi|): if it is <= the solar-system cap at
    # Mercury, it is <= that cap at every shallower point, and it is at least
    # as large at every deeper point. Galaxy and cluster are both deeper than
    # Mercury, so both see at least the Mercury-on value. The ratio of cluster
    # to galaxy cannot be driven below 1.
    depth_order = sorted(phi.items(), key=lambda kv: kv[1])

    # Coupling that would deliver delta_a = a0 at the g_N = a0 point (Xi = 1).
    # frac_needed = 1, |kappa| = 3 / |mean_p2|.
    kappa_mond = 3.0 / abs(mean_p2)
    a_merc_if_mond = accel_from_kappa(kappa_mond, R_MERC, mean_p2)
    prec_mas = abs(a_merc_if_mond) / bud["a_tilde_max"] * PREC_BOUND_MAS

    # Representative galaxy at 10 kpc, 10^11 solar masses, Xi=1, kappa capped.
    r_gal = 10.0 * KPC
    m_gal = 1.0e11 * M_SUN
    g_gal = G * m_gal / r_gal**2
    # Same fractional correction, because varphi scales as kappa GM/r.
    delta_a_gal = frac * g_gal

    mercury_pass = abs(a_merc) <= bud["a_tilde_max"] * (1.0 + 1e-9)
    cassini_pass = q2_sat <= Q2_CAP
    sparc_pass = delta_a_at_a0 >= 1e-3 * A0
    # Monotonic depth cannot turn the cluster off while leaving the galaxy on.
    monotonic_separates_cluster = False

    out = {
        "pre_registered": {
            "a0_m_s2": A0,
            "mercury_precession_mas_per_cy_2sig": PREC_BOUND_MAS,
            "q2_cap_s^-2": Q2_CAP,
            "r200_pass_window": [R200_LO, R200_HI],
            "galactic_centre_ecliptic_latitude_deg": B_GC_DEG,
            "equation": "nabla^2 varphi = kappa * T_parallel, T_parallel = -(2 GM/r^3) P2",
            "boundary": "varphi -> 0 at infinity, homogeneous r^2 and r^-3 coefficients set to 0",
        },
        "orbit_mean_P2": mean_p2,
        "mercury_budget": bud,
        "finite_difference": {
            "n": 4000,
            "max_rel_error_vs_particular": fd["max_rel_fd"],
        },
        "kappa_max_from_mercury": kappa_max,
        "at_mercury_cap": {
            "a_r_mercury_m_s2": a_merc,
            "a_r_saturn_m_s2": a_sat,
            "q2_saturn_s^-2": q2_sat,
            "fractional_radial_correction": frac,
            "delta_a_at_gN_eq_a0": delta_a_at_a0,
            "delta_a_10kpc_1e11Msun": delta_a_gal,
            "g_N_that_galaxy": g_gal,
        },
        "if_kappa_set_to_cassini_edge": {
            "kappa": kappa_q2,
            "a_r_mercury_m_s2": a_merc_if_q2,
            "ratio_to_mercury_budget": abs(a_merc_if_q2) / bud["a_tilde_max"],
        },
        "if_kappa_set_to_order_unity_mond_boost": {
            "kappa": kappa_mond,
            "a_r_mercury_m_s2": a_merc_if_mond,
            "implied_perihelion_mas_per_cy": prec_mas,
        },
        "depth_c2": phi,
        "depth_order_shallow_to_deep": [k for k, _ in depth_order],
        "gates": {
            "mercury_at_own_cap": "PASS" if mercury_pass else "FAIL",
            "cassini_q2_at_mercury_cap": "PASS" if cassini_pass else "FAIL",
            "sparc_order_a0_boost_at_mercury_cap": "PASS" if sparc_pass else "FAIL",
            "monotonic_Xi_of_depth_separates_cluster_from_galaxy": (
                "PASS" if monotonic_separates_cluster else "FAIL"
            ),
            "joint": "FAIL",
        },
        "verdict": (
            "[X] for Xi = 1 and for every monotonic Xi(|Phi|/c^2). "
            "The Mercury cap leaves a fractional correction far below a0, so SPARC "
            "is untouched. A coupling large enough for an order-unity MOND boost "
            "violates the perihelion budget. Cluster |Phi| is deeper than galactic "
            "|Phi|, so a nondecreasing depth gate that is on for SPARC is on for "
            "X-COP, where Gate 2 already records med R200 = 0.608-0.621. "
            "A window between those depths needs two new dimensionful edges and "
            "fails the uniqueness line. The 12-cluster hydrostatic system was not refit."
        ),
    }
    json_path = HERE / "D7_TIDAL_DEPTH_BVP.json"
    json_path.write_text(json.dumps(out, indent=2) + "\n")
    md = f"""# D7 directional tidal boundary-value problem (2026-11-21)

Equation solved, with one constant coupling and no fitted function:

```
∇²φ = κ T_∥,    T_∥ = −(2GM/r³) P₂(cos θ),    φ → 0 at infinity.
```

The particular solution is φ = (κ GM /(3r)) P₂. A 4000-point finite-difference
shell solve reproduces it to a maximum relative error {fd["max_rel_fd"]:.3e}.

Orbit average on a circular ecliptic orbit with the galactic centre at ecliptic
latitude {B_GC_DEG}°: ⟨P₂⟩ = {mean_p2:.6f}. The spherical average of T_∥ is 0.
The orbit average is not.

## Pre-registered gates

| Gate | Threshold | Result at the only coupling Mercury allows |
|---|---|---|
| Mercury perihelion | ≤ {PREC_BOUND_MAS} mas/century (2σ) | cap, by construction |
| Cassini Q₂ at 9.5 AU | ≤ {Q2_CAP:.1e} s⁻² | {q2_sat:.3e} ({out["gates"]["cassini_q2_at_mercury_cap"]}) |
| SPARC-sized boost | δa ≥ 10⁻³ a₀ where g_N = a₀ | {delta_a_at_a0:.3e} ({out["gates"]["sparc_order_a0_boost_at_mercury_cap"]}) |
| Monotonic depth gate vs X-COP | Ξ on for a galaxy and off for a cluster | impossible ({out["gates"]["monotonic_Xi_of_depth_separates_cluster_from_galaxy"]}) |

κ capped by Mercury is {kappa_max:.6e}. The fractional radial correction is {frac:.6e} at every radius. At a 10¹¹ M_☉, 10 kpc point that is an extra {delta_a_gal:.3e} m/s² on top of g_N = {g_gal:.3e} m/s².

Setting κ so the boost is order a₀ ({kappa_mond:.6e}) produces {prec_mas:.3e} mas/century at Mercury.

## Depth axis (|Φ|/c²), shallow to deep

{chr(10).join(f"- {k}: {v:.6e}" for k, v in depth_order)}

Any nondecreasing function of this axis that reaches a galactic MOND boost is at least that large on a cluster. Gate 2 already killed that unscreened regime at median R_200 = 0.608–0.621. This run does not replace that hydrostatic solve.

## Verdict

{out["verdict"]}

## Not done in this run

- No refit of the 175 SPARC rotation curves. The capped extra acceleration is {frac:.3e} of g_N, below any χ² the ledger can see.
- No refit of the 12 X-COP hydrostatic equilibria.
- No new Cassini Doppler reduction. Q₂ here is the curvature |δa|/r² of this solution, scored against the published 5.2×10⁻²⁷ s⁻² cap.
- No covariant Lagrangian. Contracting S_ij with a fixed external tensor privileges the galactic frame. The 2026-11-18 separability note already recorded that this is not a local scalar.
- No Lean proof. The finite-difference residual is a numerical receipt, tier [D]. The monotonicity obstruction is arithmetic on the four depths, tier [D].
- No commit and no push.
"""
    (HERE / "D7_TIDAL_DEPTH_BVP.md").write_text(md)
    print(
        json.dumps(
            {
                k: out[k]
                for k in (
                    "finite_difference",
                    "gates",
                    "kappa_max_from_mercury",
                    "orbit_mean_P2",
                )
            },
            indent=2,
        )
    )
    print(out["verdict"])


if __name__ == "__main__":
    main()
