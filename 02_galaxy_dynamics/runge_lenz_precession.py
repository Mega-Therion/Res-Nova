#!/usr/bin/env python3
"""Runge-Lenz (apsidal) precession under the live mu_std, and from the external-field quadrupole.

2026-10-06, exploratory. The numbers are computed here [D]; reading the two channels below as
one symmetry story is [O].

Two terms break the Kepler (Runge-Lenz) symmetry of a bound orbit around a mass M:

1. Radial channel: g = nu(y) g_N with y = g_N/a0. The field is spherical, so angular momentum
   is conserved, but the Runge-Lenz vector rotates. For near-circular orbits the apsidal angle is
   Psi = pi / sqrt(1 - 2 n(y)), with n(y) = d ln nu / d ln y. The pericentre advances by
   2 Psi - 2 pi per radial period, at rate (Omega - kappa) = Omega (1 - sqrt(1 - 2 n)).
   This is checked below against direct orbit integration.

2. External-field (EFE) quadrupole: delta Phi = -(Q2/2) x^i x^j (e_i e_j - delta_ij/3). The term
   is anisotropic, so it also torques the orbit. Averaging the disturbing function over a Kepler
   ellipse gives, for an orbit near the reference plane and a field at latitude beta and in-plane
   angle phi from perihelion,
       d(varpi)/dt = Q2 sqrt(1 - e^2) / (2 n_orb) * [cos^2(beta) (5 cos^2(phi) - 1) - 1],
   which for beta = 0 reads Q2 sqrt(1 - e^2) / (4 n_orb) * (1 + 5 cos 2 phi). The formula is
   checked below against direct integration. Q2 is canon's efe_quadrupole_q2.Q2: Milgrom 2009
   QUMOND, in the form of Hees et al. 2016 eq. 12.

Run: python3 runge_lenz_precession.py   ->  RUNGE_LENZ_PRECESSION.json
"""

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import efe_quadrupole_q2 as efe  # noqa: E402  (canon: NU dict, Q2(nu, a0, ge), A0_DERIVED, GM)

GM_SUN = efe.GM  # same constant as the canon Q2 calculation
AU = 1.495978707e11
YEAR = 365.25 * 86400.0  # Julian year, s
MAS_PER_RAD = 180.0 / math.pi * 3600.0e3
A0_DERIVED = efe.A0_DERIVED  # cH0/2pi, the declared anchor [O]
A0_SPARC = 1.1607e-10  # live mu_std SPARC fit [E] (CURRENT_STATE)
NU2 = efe.NU["mu_std (nu_2)"]
NU1 = efe.NU["mu_dual/simple (nu_1)"]
Q2_BOUND_2026 = (
    1.6e-27,
    1.8e-27,
)  # arXiv:2602.17884, as used in CASSINI_EFE_QUADRUPOLE_2026-09-27
Q2_PASS_2SIGMA = 5.2e-27  # canon's 2-sigma PASS threshold

# JPL approximate Keplerian elements, J2000 (Standish): a [AU], e, longitude of perihelion [deg]
PLANETS = {
    "Mercury": (0.38709927, 0.20563593, 77.45779628),
    "Earth": (1.00000261, 0.01671123, 102.93768193),
    "Saturn": (9.53667594, 0.05386179, 92.59887831),
}
SGR_A_RA_DEC = (266.41683, -29.00781)  # ICRS, degrees
OBLIQUITY_J2000 = 23.4392911  # degrees


# ---------------------------------------------------------------- part 1: radial channel
def n_nu2(y):
    """d ln nu_2 / d ln y in closed form (nu_2 = inverse of mu_std)."""
    s = math.sqrt(1.0 + 4.0 / y**2)
    return -2.0 / (y**2 * s * (1.0 + s))


def n_nu1(y):
    """d ln nu_1 / d ln y in closed form (nu_1 = inverse of mu_simple = mu_dual)."""
    t = math.sqrt(1.0 + 4.0 / y)
    return -2.0 / (t * y * (1.0 + t))


def n_numeric(nu, y, h=1e-4):
    return float(
        (math.log(nu(y * math.exp(h))) - math.log(nu(y * math.exp(-h)))) / (2 * h)
    )


def apsidal(n):
    """Return (pericentre advance per radial period [rad], apsidal rate / orbital frequency).

    Both are written with log1p/expm1 so that n ~ 1e-12 keeps full relative precision.
    """
    advance = (
        2 * math.pi * math.expm1(-0.5 * math.log1p(-2 * n))
    )  # 2 pi (Omega/kappa - 1)
    rate = -math.expm1(0.5 * math.log1p(-2 * n))  # 1 - kappa/Omega
    return advance, rate


def measured_advance(nu, r_apo, kick, n_peri=6):
    """Integrate a planar orbit in g = nu(1/r^2)/r^2 (units GM = a0 = 1, so y = 1/r^2).

    Start at apocentre r_apo with speed (1 - kick) v_circ. Return the mean pericentre advance
    per radial period, its spread, and y at the guiding-centre radius.
    """

    def acc(r):
        return float(nu(1.0 / r**2)) / r**2

    vc = math.sqrt(r_apo * acc(r_apo))
    v0 = (1 - kick) * vc

    def rhs(t, s):
        x, y, vx, vy = s
        r = math.hypot(x, y)
        a = acc(r) / r
        return [vx, vy, -a * x, -a * y]

    def peri(t, s):
        return s[0] * s[2] + s[1] * s[3]

    peri.direction = 1

    period = 2 * math.pi * r_apo / vc
    sol = solve_ivp(
        rhs,
        (0, (n_peri + 2) * 2 * period),
        [r_apo, 0.0, 0.0, v0],
        method="DOP853",
        rtol=1e-12,
        atol=1e-15,
        events=peri,
    )
    pts = sol.y_events[0][:n_peri]
    ang = np.unwrap(np.arctan2(pts[:, 1], pts[:, 0]))
    adv = np.diff(ang)
    L = r_apo * v0
    r_g = brentq(lambda r: r * math.sqrt(r * acc(r)) - L, 1e-6 * r_apo, r_apo)
    return float(adv.mean()), float(adv.std()), 1.0 / r_g**2


# ---------------------------------------------------------------- part 2: EFE quadrupole
def efe_rate_formula(ecc, phi, beta, q2_over_n):
    """Secular d(varpi)/dt in units where n_orb = 1; q2_over_n = Q2/n_orb (rad/s if Q2 in s^-2)."""
    return (
        q2_over_n
        * math.sqrt(1 - ecc**2)
        / 2
        * (math.cos(beta) ** 2 * (5 * math.cos(phi) ** 2 - 1) - 1)
    )


def efe_rate_numeric(ecc, phi, beta, eps=1e-5, n_orbits=300):
    """Direct check: units GM = a = n_orb = 1, orbit starts at pericentre on +x in the xy-plane.

    Field direction e = (cos b cos phi, cos b sin phi, sin b), strength eps = Q2/n_orb^2. The
    secular rate is a linear fit to the in-plane angle of the Runge-Lenz vector, sampled once
    per Kepler period.
    """
    eh = np.array(
        [math.cos(beta) * math.cos(phi), math.cos(beta) * math.sin(phi), math.sin(beta)]
    )

    def rhs(t, s):
        x = s[:3]
        r = math.sqrt(x @ x)
        a = -x / r**3 + eps * (eh * (eh @ x) - x / 3.0)
        return np.concatenate([s[3:], a])

    rp = 1 - ecc
    vp = math.sqrt((1 + ecc) / (1 - ecc))
    t_eval = 2 * math.pi * np.arange(n_orbits + 1)
    sol = solve_ivp(
        rhs,
        (0, t_eval[-1]),
        [rp, 0, 0, 0, vp, 0],
        method="DOP853",
        rtol=1e-12,
        atol=1e-14,
        t_eval=t_eval,
    )
    X, V = sol.y[:3].T, sol.y[3:].T
    A = np.cross(V, np.cross(X, V)) - X / np.linalg.norm(X, axis=1)[:, None]
    ang = np.unwrap(np.arctan2(A[:, 1], A[:, 0]))
    return float(np.polyfit(t_eval, ang, 1)[0])


def galactic_centre_ecliptic():
    ra, dec = (math.radians(v) for v in SGR_A_RA_DEC)
    eps = math.radians(OBLIQUITY_J2000)
    sin_b = math.sin(dec) * math.cos(eps) - math.cos(dec) * math.sin(eps) * math.sin(ra)
    lam = math.atan2(
        math.sin(ra) * math.cos(eps) + math.tan(dec) * math.sin(eps), math.cos(ra)
    )
    return math.degrees(lam) % 360.0, math.degrees(math.asin(sin_b))


def main():
    out = {
        "constants": {"a0_derived": A0_DERIVED, "a0_sparc": A0_SPARC, "GM_sun": GM_SUN}
    }

    # Part 1a: closed form vs numerical derivative
    checks = []
    for y in (1e-2, 1e-1, 1.0, 10.0, 1e2, 1e3):
        checks.append({"y": y, "n_closed": n_nu2(y), "n_numeric": n_numeric(NU2, y)})
    out["n_closed_form_check"] = checks

    # Part 1b: table over y for nu_2 and nu_1
    table = []
    for y in (1e-3, 1e-2, 1e-1, 0.5, 1.0, 2.0, 10.0, 1e2, 1e3, 1e4, 1e5, 6.26e5, 1e7):
        row = {"y": y}
        for name, nfun in (("mu_std", n_nu2), ("mu_simple", n_nu1)):
            n = nfun(y)
            adv, rate = apsidal(n)
            row[name] = {
                "n": n,
                "advance_per_radial_period_rad": adv,
                "rate_over_Omega": rate,
            }
        table.append(row)
    out["radial_channel_table"] = table
    out["deep_mond_limit"] = {
        "advance_rad": 2 * math.pi * (1 / math.sqrt(2) - 1),
        "rate_over_Omega": 1 - math.sqrt(2),
    }

    # Part 1c: direct orbit integration (nu_2)
    integ = []
    for y_target, kick in (
        (1e-2, 0.01),
        (1e-1, 0.01),
        (1.0, 0.01),
        (10.0, 0.01),
        (1e2, 0.01),
        (1e3, 0.01),
        (1.0, 0.3),
    ):
        adv_m, spread, y_g = measured_advance(NU2, 1.0 / math.sqrt(y_target), kick)
        adv_p, _ = apsidal(n_nu2(y_g))
        integ.append(
            {
                "y_guiding": y_g,
                "kick": kick,
                "measured_rad": adv_m,
                "spread_rad": spread,
                "predicted_rad": adv_p,
                "rel_diff": (adv_m - adv_p) / abs(adv_p),
            }
        )
    out["radial_channel_integration_check"] = integ

    # Part 2a: EFE secular formula vs direct integration
    efe_checks = []
    eps = 1e-5
    for ecc, phi_deg, beta_deg in (
        (0.2, 0, 0),
        (0.2, 90, 0),
        (0.2, 30, 0),
        (0.05, 0, 0),
        (0.2, 0, 40),
    ):
        num = efe_rate_numeric(ecc, math.radians(phi_deg), math.radians(beta_deg), eps)
        frm = efe_rate_formula(ecc, math.radians(phi_deg), math.radians(beta_deg), eps)
        efe_checks.append(
            {
                "e": ecc,
                "phi_deg": phi_deg,
                "beta_deg": beta_deg,
                "numeric": num,
                "formula": frm,
                "rel_diff": (num - frm) / abs(frm),
            }
        )
    out["efe_formula_integration_check"] = efe_checks
    # At phi = 30 deg the field-to-perihelion angle drifts during the run (d/dphi of the rate is
    # nonzero there), so the offset should grow linearly with run length. It does if the formula
    # is the right instantaneous rate.
    frm30 = efe_rate_formula(0.2, math.radians(30), 0.0, eps)
    out["efe_phi30_convergence"] = {
        str(n): (efe_rate_numeric(0.2, math.radians(30), 0.0, eps, n_orbits=n) - frm30)
        / abs(frm30)
        for n in (30, 100, 300)
    }

    # Part 2b: Q2 for mu_std from canon, at both a0 values and both g_e
    q2 = {}
    for a0_name, a0 in (("derived", A0_DERIVED), ("sparc", A0_SPARC)):
        for ge in (1.9e-10, 2.4e-10):
            Q, _ = efe.Q2(NU2, a0, ge)
            q2[f"a0={a0_name},ge={ge:.1e}"] = float(Q)
    out["Q2_mu_std"] = q2

    # Part 2c: planets: EFE channel vs radial channel
    lam_gc, beta_gc = galactic_centre_ecliptic()
    out["galactic_centre_ecliptic_deg"] = {"lambda": lam_gc, "beta": beta_gc}
    planets = {}
    for name, (a_au, ecc, varpi_deg) in PLANETS.items():
        a = a_au * AU
        n_orb = math.sqrt(GM_SUN / a**3)
        phi = math.radians(varpi_deg - lam_gc)
        beta = math.radians(beta_gc)
        geom = (
            math.sqrt(1 - ecc**2)
            / 2
            * (math.cos(beta) ** 2 * (5 * math.cos(phi) ** 2 - 1) - 1)
        )
        row = {
            "n_orb_per_s": n_orb,
            "phi_deg": (varpi_deg - lam_gc) % 360.0,
            "geometry_factor": geom,
        }
        for key, Q in q2.items():
            rate = Q / n_orb * geom
            row[f"efe_{key}_mas_per_cy"] = rate * YEAR * 100 * MAS_PER_RAD
        bound_rate = Q2_PASS_2SIGMA / n_orb * geom
        row["efe_at_2sigma_bound_mas_per_cy"] = bound_rate * YEAR * 100 * MAS_PER_RAD
        for a0_name, a0 in (("derived", A0_DERIVED), ("sparc", A0_SPARC)):
            y = GM_SUN / a**2 / a0
            _, rate_frac = apsidal(n_nu2(y))
            row[f"radial_a0={a0_name}_y"] = y
            row[f"radial_a0={a0_name}_mas_per_cy"] = (
                rate_frac * n_orb * YEAR * 100 * MAS_PER_RAD
            )
        planets[name] = row
    out["planets"] = planets

    (HERE / "RUNGE_LENZ_PRECESSION.json").write_text(json.dumps(out, indent=2))

    # ---- printout
    print("Part 1a  n(y) closed form vs numerical derivative (nu_2):")
    for c in checks:
        print(
            f"  y={c['y']:<8g} closed={c['n_closed']:.10e}  numeric={c['n_numeric']:.10e}"
        )
    print(
        "\nPart 1b  radial channel: advance per radial period [rad] and apsidal rate / Omega"
    )
    for row in table:
        s, m = row["mu_std"], row["mu_simple"]
        print(
            f"  y={row['y']:<9g} mu_std: {s['advance_per_radial_period_rad']:+.4e} rad, rate {s['rate_over_Omega']:+.4e}"
            f" | mu_simple: {m['advance_per_radial_period_rad']:+.4e} rad"
        )
    print(
        f"  deep-MOND limit: {out['deep_mond_limit']['advance_rad']:+.6f} rad per radial period, "
        f"rate {out['deep_mond_limit']['rate_over_Omega']:+.6f} Omega"
    )
    print("\nPart 1c  direct integration (nu_2):")
    for c in integ:
        print(
            f"  y_g={c['y_guiding']:<10.4g} kick={c['kick']:<5} measured={c['measured_rad']:+.6e} "
            f"predicted={c['predicted_rad']:+.6e} rel diff={c['rel_diff']:+.2e} (spread {c['spread_rad']:.1e})"
        )
    print("\nPart 2a  EFE secular formula vs direct integration (eps = Q2/n^2 = 1e-5):")
    for c in efe_checks:
        print(
            f"  e={c['e']} phi={c['phi_deg']} beta={c['beta_deg']}: numeric={c['numeric']:+.6e} "
            f"formula={c['formula']:+.6e} rel diff={c['rel_diff']:+.2e}"
        )
    print("\nPart 2b  Q2(mu_std) from canon efe_quadrupole_q2 [1e-27 s^-2]:")
    for k, v in q2.items():
        print(f"  {k}: {v * 1e27:.2f}")
    print(
        f"\nGalactic centre: ecliptic lambda={lam_gc:.3f} deg, beta={beta_gc:.3f} deg"
    )
    print(
        "Part 2c  perihelion precession [mas/century]: EFE channel vs radial channel (mu_std)"
    )
    for name, row in planets.items():
        efe_vals = ", ".join(
            f"{k.split('_', 1)[1].replace('_mas_per_cy', '')}={v:+.4f}"
            for k, v in row.items()
            if k.startswith("efe_a0")
        )
        print(
            f"  {name}: phi={row['phi_deg']:.1f} deg, geometry={row['geometry_factor']:+.4f}"
        )
        print(f"     EFE: {efe_vals}")
        print(
            f"     EFE at the 2-sigma Q2 bound (5.2e-27): {row['efe_at_2sigma_bound_mas_per_cy']:+.4f}"
        )
        print(
            f"     radial: derived a0 {row['radial_a0=derived_mas_per_cy']:+.3e} (y={row['radial_a0=derived_y']:.3e}),"
            f" SPARC a0 {row['radial_a0=sparc_mas_per_cy']:+.3e}"
        )


if __name__ == "__main__":
    main()
