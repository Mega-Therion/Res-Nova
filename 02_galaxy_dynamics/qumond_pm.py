#!/usr/bin/env python3
"""QUMOND field solver on a 3D grid with isolated boundaries and an optional uniform external field. It is groundwork
shared by D7 (a deep-MOND dwarf in a host's field, then in an aether wind) and D5 (non-linear structure).

QUMOND (Milgrom 2010): del^2 Phi_N = 4 pi G rho;  g_M = nu(|g_N,tot|/a0) g_N,tot;  del^2 Phi_M = -div g_M,
where g_N,tot = -grad Phi_N + g_eN (uniform host field). The internal MOND potential is the isolated solution of the
second equation; the uniform external MOND field nu_e g_eN has zero divergence and is carried separately.
nu is the mu_std pair: nu(y) = sqrt((1 + sqrt(1 + 4/y^2)) / 2).
Poisson solves use the Hockney-Eastwood zero-padded FFT convolution with the free-space Green's function; the cell
self-term uses the cube average of 1/r (2.3800772/dx).

Gates (units G = a0 = M = 1, so the MOND radius sqrt(GM/a0) = 1; Plummer dwarf, scale b):
  1a isolated: QUMOND is exact in spherical symmetry, g(r) = nu(g_N(r)) g_N(r) with g_N = G M(<r) / r^2;
     the grid must reproduce it in the deep-MOND range.
  1b external field g_eN along -z: the far-field monopole of the internal MOND potential must approach
     nu_e (1 + L_e/3) Phi_N, with L_e = d ln nu / d ln y at y_e = g_eN / a0 (linearizing nu(|g_e + g_N|)).
  1c the same diagnostics at two resolutions must agree.
Usage: qumond_pm.py   Output: QUMOND_PM_GATES.json"""

import json, math
import numpy as np

SELF_TERM = (
    2.3800772  # (1/dx^3) * integral over a cube of side dx centred at 0 of dx/|x|
)


def nu_std(y):
    y = np.maximum(y, 1e-300)
    return np.sqrt(0.5 * (1 + np.sqrt(1 + 4 / y**2)))


def green_fft(n, dx):
    m = 2 * n
    d = np.minimum(np.arange(m), m - np.arange(m)) * dx
    r = np.sqrt(d[:, None, None] ** 2 + d[None, :, None] ** 2 + d[None, None, :] ** 2)
    G = np.empty_like(r)
    nz = r > 0
    G[nz] = -1.0 / (4 * math.pi * r[nz])
    G[~nz] = -SELF_TERM / (4 * math.pi * dx)
    return np.fft.rfftn(G)


def poisson_isolated(src, dx, Gk):
    """Solve del^2 Phi = src with isolated (free-space) boundaries."""
    n = src.shape[0]
    pad = np.zeros((2 * n,) * 3)
    pad[:n, :n, :n] = src
    return (
        np.fft.irfftn(np.fft.rfftn(pad) * Gk, s=pad.shape, axes=(0, 1, 2))[:n, :n, :n]
        * dx**3
    )


def grad(phi, dx):
    return np.stack(np.gradient(phi, dx, edge_order=2))


def div(vec, dx):
    return sum(np.gradient(vec[i], dx, axis=i, edge_order=2) for i in range(3))


def solve(rho, dx, g_eN=0.0, G=1.0, a0=1.0, Gk=None):
    """Returns (Phi_N, Phi_M_internal, g_N internal, g_M internal). The external field g_eN points along -z."""
    n = rho.shape[0]
    Gk = green_fft(n, dx) if Gk is None else Gk
    phiN = poisson_isolated(4 * math.pi * G * rho, dx, Gk)
    gN = -grad(phiN, dx)
    ext = np.zeros(3)[:, None, None, None]
    ext[2] = -g_eN
    gtot = gN + ext
    gm_tot = nu_std(np.sqrt((gtot**2).sum(0)) / a0) * gtot
    phiM = poisson_isolated(-div(gm_tot, dx), dx, Gk)
    return phiN, phiM, gN, -grad(phiM, dx)


def plummer(n, L, b, M=1.0):
    x = (np.arange(n) - (n - 1) / 2) * (L / n)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    r = np.sqrt(X**2 + Y**2 + Z**2)
    return (
        3 * M / (4 * math.pi * b**3) * (1 + (r / b) ** 2) ** -2.5,
        (X, Y, Z, r),
        L / n,
    )


def shell_average(field, r, radii, width):
    return np.array([field[(r > R - width) & (r < R + width)].mean() for R in radii])


def gates(n, L=80.0, b=1.0, g_eN=0.1):
    rho, (X, Y, Z, r), dx = plummer(n, L, b)
    Gk = green_fft(n, dx)
    out = {"n": n, "L": L, "dx": dx, "b": b}
    # 1a isolated
    phiN, phiM, gN, gM = solve(rho, dx, 0.0, Gk=Gk)
    radii = np.array([3.0, 5.0, 8.0, 12.0, 16.0])
    gmag = np.sqrt((gM**2).sum(0))
    gN_exact = radii / (radii**2 + b**2) ** 1.5  # G M(<r)/r^2 for Plummer
    g_exact = nu_std(gN_exact) * gN_exact
    g_grid = shell_average(gmag, r, radii, 0.75 * dx)
    out["isolated"] = {
        "radii": radii.tolist(),
        "g_grid_over_exact": (g_grid / g_exact).tolist(),
        "deep_mond_check_g_r": (g_grid * radii).tolist(),
    }
    # 1b external field
    phiN, phiM, gN, gM = solve(rho, dx, g_eN, Gk=Gk)
    ye = g_eN
    nue = float(nu_std(ye))
    h = 1e-6
    Le = float(
        (math.log(nu_std(ye * (1 + h))) - math.log(nu_std(ye * (1 - h))))
        / (math.log(1 + h) - math.log(1 - h))
    )
    far = np.array([12.0, 16.0, 20.0, 24.0])
    ratio = shell_average(phiM, r, far, 0.75 * dx) / shell_average(
        phiN, r, far, 0.75 * dx
    )
    out["external"] = {
        "g_eN": g_eN,
        "nu_e": nue,
        "L_e": Le,
        "predicted_monopole_ratio": nue * (1 + Le / 3),
        "radii": far.tolist(),
        "phiM_over_phiN_shell": ratio.tolist(),
        "r_e = sqrt(GM/g_eN)": math.sqrt(1 / g_eN),
    }
    return out


def main():
    res = {"coarse": gates(96), "fine": gates(128)}
    for k, v in res.items():
        print(k, json.dumps(v, indent=None)[:900], flush=True)
    json.dump(res, open("QUMOND_PM_GATES.json", "w"), indent=2)


if __name__ == "__main__":
    main()
