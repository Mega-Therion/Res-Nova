#!/usr/bin/env python3
"""Member-galaxy phantom inside R_500. QUMOND flux of |g_N| only.

The smooth test in cluster_mond_test.py is the spherical identity
    g = ν(|g_N|) g_N,   M_dyn(R_500) = ν M_bar.
Substructure can change the answer only by breaking that symmetry. The flux
identity still holds for any shape:

    ∫_∂V g · dA = ∫_∂V ν(|g_N|) g_N · dA,
    M_dyn = R^2 / G * <ν g_N · n>.

This script evaluates that surface integral at R_500. Gas stays the smooth
β-model used by aest_mu2_correction.py (core rc = 0.1 R_500). Stars are
f_star = 0.015 of M_500, the same fraction as cluster_mond_test.py, split
into equal galaxies of 10^11 M_sun (last one takes the remainder) and placed
on the same cumulative mass profile, cut at 0.85 R_500 so none sit on the
sphere. The μ^2 Φ integral is not used. Cassini files are not read.

A second, labelled stress case puts ALL baryons into 30 equal clumps on that
same profile. X-ray gas is not observed to be 30 clumps. The row is an upper
bracket on what clumping can do, not a model of these clusters.
"""

import math
import numpy as np
import cluster_mond_test as cm

F_STAR = cm.F_STAR
M_GAL = 1.0e11 * cm.MSUN  # equal-galaxy split; assumption, not a measured LF
R_CUT = 0.85  # galaxy centres stay inside this fraction of R_500
N_SURF = 2048
RC_FRAC = 0.1
N_STRESS = 30
RNG = np.random.default_rng(20261106)


def nu_of_s(s):
    """ν(y) for μ_std, y = |g_N|/a0. ν = 1 at large y."""
    s = np.maximum(s, 1e-30)
    x = np.sqrt((s * s + s * np.sqrt(s * s + 4.0)) / 2.0)
    return x / s


def fibonacci_sphere(n):
    i = np.arange(n, dtype=float)
    z = 1.0 - (2.0 * i + 1.0) / n
    r = np.sqrt(np.maximum(0.0, 1.0 - z * z))
    phi = i * math.pi * (3.0 - math.sqrt(5.0))
    return np.stack((r * np.cos(phi), r * np.sin(phi), z), axis=1)


def beta_menc(r, rc, norm):
    u = r / rc
    return norm * (u - np.arctan(u))


def sample_radii(n, rc, r_max, rng):
    """Inverse CDF of dM/dr for M(r) ∝ r/rc - arctan(r/rc)."""
    grid = np.linspace(1e-4 * rc, r_max, 20000)
    cdf = beta_menc(grid, rc, 1.0)
    cdf = cdf / cdf[-1]
    u = rng.random(n)
    return np.interp(u, cdf, grid)


def flux_mdyn(g_vec, n_hat, R):
    """M such that 4π G M = ∫ (vector) · dA, vector already = ν g_N or g_N."""
    radial = np.einsum("ij,ij->i", g_vec, n_hat)
    return R * R / cm.G_SI * float(np.mean(radial))


def g_gas_vec(points, rc, norm):
    rad = np.linalg.norm(points, axis=1)
    menc = beta_menc(rad, rc, norm)
    g = cm.G_SI * menc / np.maximum(rad, 1e-20) ** 2
    return (g / np.maximum(rad, 1e-20))[:, None] * points


def g_points_vec(points, pos, mass):
    if len(mass) == 0:
        return np.zeros_like(points)
    d = points[:, None, :] - pos[None, :, :]
    dist2 = np.einsum("ijk,ijk->ij", d, d)
    dist = np.sqrt(dist2)
    dist3 = np.maximum(dist, 1e-12) ** 3
    return cm.G_SI * np.einsum("ij,ijk->ik", mass[None, :] / dist3, d)


def place_galaxies(n, mass_each, rc, r_max, rng):
    rad = sample_radii(n, rc, r_max, rng)
    n_hat = fibonacci_sphere(n)
    # shuffle directions; the fibonacci set is regular
    rng.shuffle(n_hat)
    return n_hat * rad[:, None], np.full(n, mass_each)


def analyse_one(c, n_hat, rng):
    M500 = c["M500"] * 1e14 * cm.MSUN
    Mgas = c["fgas"] * M500
    Mstar = F_STAR * M500
    R = cm.r_delta(M500, c["z"])
    rc = RC_FRAC * R
    r_max = R_CUT * R
    norm = Mgas / ((R / rc) - math.atan(R / rc))
    shell = n_hat * R

    # --- smooth: gas + stars both in the β-model, stars scaled into norm ---
    norm_all = (Mgas + Mstar) / ((R / rc) - math.atan(R / rc))
    g_s = g_gas_vec(shell, rc, norm_all)
    s_s = np.linalg.norm(g_s, axis=1) / cm.A0
    M_smooth = flux_mdyn(nu_of_s(s_s)[:, None] * g_s, n_hat, R)
    M_newt = flux_mdyn(g_s, n_hat, R)

    # --- members: gas smooth, stars as equal 1e11 M_sun galaxies ---
    n_gal = max(1, int(math.floor(Mstar / M_GAL)))
    masses = np.full(n_gal, M_GAL)
    masses[-1] = Mstar - M_GAL * (n_gal - 1)
    pos, _ = place_galaxies(n_gal, 1.0, rc, r_max, rng)
    # place_galaxies used unit mass; overwrite with the real masses via positions only
    g_c = g_gas_vec(shell, rc, norm) + g_points_vec(shell, pos, masses)
    s_c = np.linalg.norm(g_c, axis=1) / cm.A0
    M_clump = flux_mdyn(nu_of_s(s_c)[:, None] * g_c, n_hat, R)
    M_newt_c = flux_mdyn(g_c, n_hat, R)

    # tide at each galaxy: cluster g vs galaxy g at R_e
    rad = np.linalg.norm(pos, axis=1)
    g_ext = cm.G_SI * beta_menc(rad, rc, norm) / np.maximum(rad, 1e-20) ** 2
    # half-light scale. R_e = 3 kpc (M/1e11 Msun)^0.3. g uses M/2 inside R_e.
    m_in_sun = masses / cm.MSUN
    Re = 3.0e3 * cm.MPC_M / 1.0e6 * (m_in_sun / 1.0e11) ** 0.3
    g_gal = cm.G_SI * (0.5 * masses) / Re**2
    # radial tides: cluster ~ 2 g_ext / r for a point mass; galaxy ~ g_gal / R_e
    tide_gal = g_gal / Re
    tide_cl = 2.0 * g_ext / np.maximum(rad, 1e-20)

    # --- stress: every baryon in N_STRESS equal clumps, same profile ---
    Mtot = Mgas + Mstar
    pos_e, _ = place_galaxies(N_STRESS, 1.0, rc, r_max, rng)
    mass_e = np.full(N_STRESS, Mtot / N_STRESS)
    g_e = g_points_vec(shell, pos_e, mass_e)
    s_e = np.linalg.norm(g_e, axis=1) / cm.A0
    M_stress = flux_mdyn(nu_of_s(s_e)[:, None] * g_e, n_hat, R)

    def ratio(M):
        return M500 / M

    return dict(
        name=c["name"],
        M500=c["M500"],
        n_gal=n_gal,
        R_smooth=ratio(M_smooth),
        R_members=ratio(M_clump),
        R_stress=ratio(M_stress),
        newt_err=M_newt / (Mgas + Mstar) - 1.0,
        newt_err_c=M_newt_c / (Mgas + Mstar) - 1.0,
        g_ratio_med=float(np.median(g_gal / np.maximum(g_ext, 1e-40))),
        tide_ratio_med=float(np.median(tide_gal / np.maximum(tide_cl, 1e-40))),
        frac_gal_dominates=float(np.mean(g_gal > g_ext)),
    )


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def main():
    n_hat = fibonacci_sphere(N_SURF)
    rows = []
    print(
        f"a0 = {cm.A0:.4e} m/s^2   f_star = {F_STAR}   "
        f"M_gal = 1e11 Msun   surface samples = {N_SURF}"
    )
    print(
        f"{'cluster':<18}{'Ngal':>5}{'R_smooth':>10}{'R_members':>11}"
        f"{'R_stress':>10}{'g_gal/g_ext':>12}{'T_gal/T_cl':>11}{'newt':>9}"
    )
    for c in cm.load().values():
        row = analyse_one(c, n_hat, RNG)
        rows.append(row)
        print(
            f"{row['name']:<18}{row['n_gal']:>5}{row['R_smooth']:>10.3f}"
            f"{row['R_members']:>11.3f}{row['R_stress']:>10.3f}"
            f"{row['g_ratio_med']:>12.2f}{row['tide_ratio_med']:>11.2f}"
            f"{row['newt_err_c']:>9.1e}"
        )
    print("-" * 86)
    print(
        f"{'MEDIAN':<18}{'':>5}{median([r['R_smooth'] for r in rows]):>10.3f}"
        f"{median([r['R_members'] for r in rows]):>11.3f}"
        f"{median([r['R_stress'] for r in rows]):>10.3f}"
        f"{median([r['g_ratio_med'] for r in rows]):>12.2f}"
        f"{median([r['tide_ratio_med'] for r in rows]):>11.2f}"
    )
    print()
    print("R = M_500(lensing) / M_dyn(QUMOND flux). R = 1 would close.")
    print("R_smooth: gas + stars both in the β-model (the spherical |g_N| identity).")
    print("R_members: stars as 1e11 Msun galaxies inside 0.85 R_500, gas smooth.")
    print(f"R_stress: all baryons in {N_STRESS} clumps. Not an X-ray model.")
    print("g_gal/g_ext: median over galaxies of g(M/2 at R_e) / g_cluster(r).")
    print("T_gal/T_cl: median of (g_gal/R_e) / (2 g_ext/r).")
    print("newt: Newtonian flux / (M_gas+M_star) - 1. Must stay ~0 (Gauss check).")
    print(
        f"max |Newtonian error|, smooth = "
        f"{max(abs(r['newt_err']) for r in rows):.2e}"
    )
    print(
        f"max |Newtonian error|, members = "
        f"{max(abs(r['newt_err_c']) for r in rows):.2e}"
    )
    closed = [r for r in rows if r["R_members"] < 1.2]
    print(f"clusters with R_members < 1.2: {len(closed)} / {len(rows)}")
    closed_s = [r for r in rows if r["R_stress"] < 1.2]
    print(f"clusters with R_stress < 1.2: {len(closed_s)} / {len(rows)}")


if __name__ == "__main__":
    main()
