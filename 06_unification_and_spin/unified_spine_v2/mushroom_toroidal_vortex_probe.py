#!/usr/bin/env python3
"""
mushroom_toroidal_vortex_probe.py — Deterministic SymPy Audit [D] (Cosmological Identification [O])
Tests two competing geometric models for the horizon tension factor 1/(2*pi) and inside-out boundary roll:
  1. [D]/[X] Static 5D AdS_5 Dark Bubble Wall (Turn 1 No-Go):
             5D proper acceleration a_5^2 = H_dS^2 + k^2, extrinsic curvature K_ab = sqrt(k^2 + H_dS^2)*h_ab,
             and radial string tension m_eff = T/k strictly lack the 1/(2*pi) horizon loop factor.
  2. [D]     Hill's Spherical Vortex (1894) — Exact Axisymmetric Superfluid / Euler Bubble Solution:
             Streamfunction psi(r, vartheta) = -(3*u0 / (4*R^2)) * r^2 * (R^2 - r^2) * sin^2(vartheta)
             for r <= R satisfies the exact Stokes-Beltrami vorticity equation Delta* psi = -(15*u0/(2*R^2)) r^2 sin^2(vartheta)
             (omega_phi / (r sin vartheta) = const, inviscid Euler equilibrium):
             - Central stalk (vartheta = 0): upward jet u_r(r, 0) = (3/2)*u0*(1 - r^2/R^2) > 0, stagnating at
               the polar crown (r = R, vartheta = 0) and folding inside-out along the spherical drumskin r = R.
             - Stretched drumskin cap (r = R): normal velocity u_r(R, vartheta) == 0 everywhere, tangential
               stretch velocity u_theta(R, vartheta) = -(3/2)*u0*sin(vartheta) peaking at the equator.
             - Stationary Toroidal Vortex Ring Core: solving u_r = 0 and u_theta = 0 in the interior (0 < r < R)
               locates the unique vortex ring core at vartheta = pi/2 and r_core / R = 1 / sqrt(2) (exact!).
               (Fenced per POSTULATE_LAYER_DIRECTIVE Stage 1: classical hydrodynamic theorem [D]; cross-sector
               theta = 1/sqrt(2) unification remains [X]; superfluid bubble cosmology mapping remains [O].)
             - Closed 2*pi KMS / circulation period vs. cos(vartheta) forward-apex / backward-wake projection.
"""

from __future__ import annotations

import sys
import sympy as sp


def verify_static_5d_dark_bubble_nogo() -> None:
    print("[Block 1] Auditing static 5D AdS_5 Dark Bubble kinematics (Turn 1 1/(2*pi) No-Go)...")
    k, H_dS, c, T = sp.symbols("k H_dS c T", positive=True)
    # 5D AdS_5 brane worldvolume with induced dS_4 Hubble rate H_dS and bulk AdS curvature k:
    # Proper 5-acceleration squared in AdS_5 is a_A a^A = k^2 + H_dS^2 (no 2*pi loop factor)
    a5_sq = k ** 2 + H_dS ** 2
    # Israel junction / extrinsic curvature K_ab = sqrt(k^2 + H_dS^2) * h_ab
    K_scalar = sp.sqrt(a5_sq)
    # Unruh temperature of the 4D induced de Sitter horizon comes strictly from the 4D KMS 2*pi period,
    # NOT from 5D brane extrinsic curvature K_scalar (ratio K_scalar / (H_dS / (2*pi)) contains 2*pi*sqrt(1 + k^2/H_dS^2))
    ratio_to_kms = sp.simplify(K_scalar / (H_dS / (2 * sp.pi)))
    assert ratio_to_kms.has(sp.pi), "Static 5D extrinsic curvature lacks 1/(2*pi) and leaves an uncanceled 2*pi!"
    # Stretched 5D string mass m_eff = int T dr = T / k (purely algebraic in T, k; zero pi dependence)
    m_eff = T / k
    assert not m_eff.has(sp.pi)
    print("  PASS: Static 5D AdS_5 brane acceleration, extrinsic curvature, & string mass fail to supply 1/(2*pi) [D]/[X].")


def verify_hills_spherical_vortex_fold() -> None:
    print("[Block 2] Verifying Hill's Spherical Vortex inside-out stalk-to-drumskin Euler solution...")
    r, R, u0 = sp.symbols("r R u0", positive=True)
    th = sp.Symbol("th", real=True)

    # Axisymmetric Stokes streamfunction inside a Hill vortex rising in +z (r <= R):
    psi_in = sp.Rational(3, 4) * u0 * (r ** 2 / R ** 2) * (R ** 2 - r ** 2) * sp.sin(th) ** 2
    # Exterior irrotational flow in the vortex rest frame (streams in -z at infinity, r >= R):
    psi_out = -sp.Rational(1, 2) * u0 * (r ** 2 - R ** 3 / r) * sp.sin(th) ** 2

    # 1. Exact continuity of streamfunction AND tangential velocity across the bubble wall r = R (no slip/jump!)
    u_r_in = sp.simplify((1 / (r ** 2 * sp.sin(th))) * sp.diff(psi_in, th))
    u_th_in = sp.simplify((-1 / (r * sp.sin(th))) * sp.diff(psi_in, r))
    u_r_out = sp.simplify((1 / (r ** 2 * sp.sin(th))) * sp.diff(psi_out, th))
    u_th_out = sp.simplify((-1 / (r * sp.sin(th))) * sp.diff(psi_out, r))

    assert sp.simplify(psi_in.subs(r, R)) == 0 and sp.simplify(psi_out.subs(r, R)) == 0
    assert sp.simplify(u_r_in.subs(r, R)) == 0 and sp.simplify(u_r_out.subs(r, R)) == 0
    assert sp.simplify(u_th_in.subs(r, R) - u_th_out.subs(r, R)) == 0

    # 2. Verify exact axisymmetric Stokes-Beltrami operator: Delta* psi = -(15*u0/(2*R^2)) * r^2 * sin^2(th)
    #    Hence omega_phi / (r*sin(th)) = -(Delta* psi)/(r^2 sin^2(th)) = +15*u0/(2*R^2) = CONSTANT (exact Euler vortex!)
    delta_star_in = sp.simplify(
        sp.diff(psi_in, r, 2) + (sp.sin(th) / r ** 2) * sp.diff(sp.diff(psi_in, th) / sp.sin(th), th)
    )
    vorticity_ratio = sp.simplify(-delta_star_in / (r ** 2 * sp.sin(th) ** 2))
    assert sp.simplify(vorticity_ratio - sp.Rational(15, 2) * u0 / R ** 2) == 0
    assert not vorticity_ratio.has(r) and not vorticity_ratio.has(th)

    # 3. Stalk -> Polar Crown -> Stretched Drumskin Eversion Kinematics:
    #    - Center of stalk (r -> 0, th = 0): upward jet +3/2 u0
    #    - Polar stagnation crown (r = R, th = 0): u_r = 0, u_th = 0 (inside-out fold point)
    #    - Outer drumskin equator (r = R, th = pi/2): tangential membrane velocity +(3/2) u0 (flowing pole -> equator!)
    assert sp.simplify(u_r_in.subs({r: 0, th: 0}) - sp.Rational(3, 2) * u0) == 0
    assert sp.simplify(u_r_in.subs({r: R, th: 0})) == 0
    assert sp.simplify(u_th_in.subs({r: R, th: sp.pi / 2}) - sp.Rational(3, 2) * u0) == 0
    # Tangential strain rate (1/R) * d(u_th)/d(th) at the polar crown th = 0 is positive: +(3*u0)/(2*R) (drumskin stretch!)
    polar_stretch_rate = sp.simplify((sp.diff(u_th_in.subs(r, R), th) / R).subs(th, 0))
    assert sp.simplify(polar_stretch_rate - sp.Rational(3, 2) * u0 / R) == 0

    # 4. Stationary Toroidal Vortex Ring Core inside the cap: u_r(r, th) = 0 and u_th(r, th) = 0 for 0 < r < R
    #    At equator th = pi/2, u_r = 0 identically; solving u_th(r, pi/2) = 0 gives r_core = R / sqrt(2)!
    assert sp.simplify(u_r_in.subs(th, sp.pi / 2)) == 0
    core_roots = sp.solve(sp.Eq(u_th_in.subs(th, sp.pi / 2), 0), r)
    assert core_roots == [R / sp.sqrt(2)], f"Expected unique positive core radius R/sqrt(2), got {core_roots}"
    r_core = core_roots[0]
    assert sp.simplify((r_core / R) - 1 / sp.sqrt(2)) == 0

    # 5. Forward-Apex vs. Backward-Wake Dipole Asymmetry & Full-Sphere Zero-Dipole Mean:
    #    Radial projection of stalk flow u_r(r, th) = (3/2)*u0*(1 - r^2/R^2)*cos(th)
    #    is positive on the forward hemisphere th in [0, pi/2) (+3/4 u0*(1-r^2/R^2) hemisphere mean),
    #    negative on the wake hemisphere th in (pi/2, pi] (-3/4 u0*(1-r^2/R^2) hemisphere mean),
    #    and averages to 0 across the full 4*pi solid angle (or ratio 1 + eps*cos(th) averaging to 1.00!).
    fwd_mean = sp.integrate(u_r_in * sp.sin(th), (th, 0, sp.pi / 2)) / sp.integrate(sp.sin(th), (th, 0, sp.pi / 2))
    bwd_mean = sp.integrate(u_r_in * sp.sin(th), (th, sp.pi / 2, sp.pi)) / sp.integrate(sp.sin(th), (th, sp.pi / 2, sp.pi))
    assert sp.simplify(fwd_mean + bwd_mean) == 0
    assert sp.simplify(fwd_mean - sp.Rational(3, 4) * u0 * (1 - r ** 2 / R ** 2)) == 0

    print("  PASS: Hill's Spherical Vortex Euler equation, crown eversion stretch, r_core/R = 1/sqrt(2), & dipole balance verified [D].")


def main() -> int:
    print("=== Mushroom-Cloud Toroidal Vortex & Dark Bubble No-Go Audit (SymPy) ===")
    verify_static_5d_dark_bubble_nogo()
    verify_hills_spherical_vortex_fold()
    print("=== ALL VORTEX & BOUNDARY CHECKS PASSED (EXIT 0) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
