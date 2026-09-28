"""Gate B1 failed its pre-set criterion (c) at the innermost shell (r = 0.1 kpc): both channel ratios move from ~1.000
(32x64) to ~1.009 (48x96). Diagnosis, not a revised gate: is it the solution or the sharp-shell diagnostic?
Hypothesis: bilinear-element derivatives at the 2x2 Gauss points carry an O(h) error of opposite sign at each +/- pair;
a sharp |r - r0| < 0.12 r0 selection splits pairs, so the shell average carries O(h/r) noise that need not shrink
monotonically. Tests, on the B1 solutions (g_e = 0.03 a0, box asinh(100)) at 32x64, 48x96 and a new 64x128:
  (a) the sharp-shell ratios (reproduce the gate);
  (b) the same with a smooth radial weight exp(-((r - r0)/(0.15 r0))^2) (pairs get equal weight);
  (c) the flux through the sphere r = r0 itself, by point evaluation of the FE solution (Gauss-Legendre in cos theta),
      the exact statement of both flux laws."""

import math, os
import numpy as np
import solve_fe as FE

vf = 10 / 299792.458
b = 3e-4
M = 12 * math.pi * vf**4 / FE.A0T
g_e = 0.03 * FE.A0T
SHELLS = (0.1e-3, 0.2e-3, 0.3e-3, 0.6e-3, 1.2e-3)


def flux(r):
    return M * r**3 / (r**2 + b**2) ** 1.5 / (12 * math.pi * r**2)


def eval_at(g, nodes, R, z):
    """(value, d_R, d_z) of every field at points (R, z), from the bilinear FE interpolant. nodes: (NF, nnode)."""
    xi, eta = np.arcsinh(R / g.a), np.arcsinh(z / g.a)
    i = np.clip((xi / g.dxi).astype(int), 0, g.nR - 1)
    j = np.clip(((eta - g.eta[0]) / g.deta).astype(int), 0, g.nz - 1)
    s, t = xi / g.dxi - i, (eta - g.eta[0]) / g.deta - j
    hR, hz = g.a * np.cosh(xi), g.a * np.cosh(eta)
    out = np.zeros((len(R), FE.NF, 3))
    for di, dj, N, dNs, dNt in (
        (0, 0, (1 - s) * (1 - t), -(1 - t), -(1 - s)),
        (1, 0, s * (1 - t), (1 - t), -s),
        (0, 1, (1 - s) * t, -t, (1 - s)),
        (1, 1, s * t, t, s),
    ):
        val = nodes[:, (i + di) * (g.nz + 1) + (j + dj)].T
        out[:, :, 0] += val * N[:, None]
        out[:, :, 1] += val * (dNs / (g.dxi * hR))[:, None]
        out[:, :, 2] += val * (dNt / (g.deta * hz))[:, None]
    return out


def analyse(nR, nz):
    g = FE.GridFE(nR, nz, 1e-4, math.asinh(100.0), math.asinh(100.0))
    P = FE.ProblemFE(g, 0.0, FE.plummer_fn(M, b), g_e)
    path = f"cache_static_fe_{nR}x{nz}.npz"
    if os.path.exists(path):
        x = np.load(path)["x"]
    else:
        x, ok, gn = P.newton(
            FE.initial_guess_fe(g, P.dm, M, b), tol=1e-9, maxit=20, verbose=False
        )
        np.savez(path, x=x, residual=gn)
    q = (P.D @ x).reshape(g.ng, FE.NQ)
    qt = q + P.qbg
    c = lambda qq, n, k: qq[:, 3 * FE.FIX[n] + k]
    r = np.hypot(g.Rg, g.zg)
    drq = lambda qq, n: (g.Rg * c(qq, n, 1) + g.zg * c(qq, n, 2)) / r
    ph = -0.5 * drq(q, "S") - drq(q, "F")
    mo = FE.mu_std(np.hypot(c(qt, "F", 1), c(qt, "F", 2)) / FE.A0T) * drq(qt, "F")
    ref = flux(r)
    nodes = P.dm.to_nodes(x)
    ct, wt = np.polynomial.legendre.leggauss(400)
    print(f"--- {nR}x{nz}")
    for r0 in SHELLS:
        sel = np.abs(r - r0) < 0.12 * r0
        sharp = [
            np.sum(f[sel] * g.w[sel]) / np.sum(ref[sel] * g.w[sel]) for f in (ph, mo)
        ]
        wb = g.w * np.exp(-(((r - r0) / (0.15 * r0)) ** 2))
        smooth = [np.sum(f * wb) / np.sum(ref * wb) for f in (ph, mo)]
        Rs, zs = r0 * np.sqrt(1 - ct**2), r0 * ct
        J = eval_at(g, nodes, Rs, zs)
        rad = lambda k: (Rs * J[:, FE.FIX[k], 1] + zs * J[:, FE.FIX[k], 2]) / r0
        ph_s = -0.5 * rad("S") - rad("F")
        Fz_tot = J[:, FE.FIX["F"], 2] + g_e
        gtot = np.hypot(J[:, FE.FIX["F"], 1], Fz_tot)
        mo_s = FE.mu_std(gtot / FE.A0T) * (rad("F") + g_e * ct)
        sphere = [0.5 * np.sum(wt * f) / flux(r0) for f in (ph_s, mo_s)]
        print(
            f"  r = {r0 * 1e3:.1f} kpc: sharp {sharp[0]:.4f} {sharp[1]:.4f} | smooth {smooth[0]:.4f} {smooth[1]:.4f} "
            f"| sphere {sphere[0]:.4f} {sphere[1]:.4f}   (Newton, MOND)",
            flush=True,
        )


for n in ((32, 64), (48, 96), (64, 128)):
    analyse(*n)
