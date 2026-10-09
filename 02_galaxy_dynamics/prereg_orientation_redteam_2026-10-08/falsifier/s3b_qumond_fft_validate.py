#!/usr/bin/env python3
"""Validation of s3: same spectral QUMOND solver, run also on the LINEARISED source
F_lin = nu_e[g_Nint + K0 (z.g_Nint) z] in the same periodic box. The linear solve must
return axis = nu_e, perp = nu_e(1+K0/2) (B&Z eq. 15) if solver + box are sound; the
difference full - linear isolates the non-linear (transition-regime) correction.
Control: g_Ne = 0 must give axis/perp = 1 exactly (cubic symmetry)."""
import numpy as np
import scipy.fft as sfft

def nu(y):
    y = np.maximum(y, 1e-300)
    return np.sqrt((1 + np.sqrt(1 + 4 / y**2)) / 2)
Kq = lambda y: -2 / (y**2 + y * np.sqrt(y**2 + 4) + 4)
YE = 1.9e-10 / 1.042e-10
NE, K0 = nu(YE), Kq(YE)


def sample(g, gN, ns):
    res = []
    for n in ns:
        pts = [((0, 0, n), (0, 0, 1)), ((0, 0, -n), (0, 0, -1)),
               ((n, 0, 0), (1, 0, 0)), ((-n, 0, 0), (-1, 0, 0)),
               ((0, n, 0), (0, 1, 0)), ((0, -n, 0), (0, -1, 0))]
        Fr = [-sum(g[c][p] * e[c] for c in range(3)) for p, e in pts]
        FN = np.mean([-sum(gN[c][p] * e[c] for c in range(3)) for p, e in pts])
        res.append((np.mean(Fr[:2]) / FN, np.mean(Fr[2:]) / FN, FN))
    return res


def solve(N, Lbox, sig, gNe, ns, linear=False):
    h = Lbox / N
    k1 = 2 * np.pi * sfft.fftfreq(N, d=h); k1r = 2 * np.pi * sfft.rfftfreq(N, d=h)
    kx, ky, kz = k1[:, None, None], k1[None, :, None], k1r[None, None, :]
    k2 = kx**2 + ky**2 + kz**2; k2[0, 0, 0] = 1.0
    phik = -4 * np.pi * np.exp(-0.5 * k2 * sig**2) / h**3 / k2; phik[0, 0, 0] = 0
    s = (N, N, N)
    gN = [sfft.irfftn(-1j * kk * phik, s=s, workers=8) for kk in (kx, ky, kz)]
    del phik
    if linear:
        F = [NE * gN[0], NE * gN[1], NE * (1 + K0) * gN[2]]
    else:
        tz = gN[2] + gNe
        gm = np.sqrt(gN[0]**2 + gN[1]**2 + tz**2)
        nv = nu(gm)
        F = [nv * gN[0], nv * gN[1], nv * tz]
        del tz, gm, nv
    Fk = [sfft.rfftn(f, workers=8) for f in F]; del F
    kdotF = (kx * Fk[0] + ky * Fk[1] + kz * Fk[2]) / k2; del Fk
    g = [sfft.irfftn(kk * kdotF, s=s, workers=8) for kk in (kx, ky, kz)]
    return [(n * h,) + t for n, t in zip(ns, sample(g, gN, ns))]


print(f"y_e={YE:.4f} nu_e={NE:.4f} K0={K0:.4f}; analytic linear: axis {NE:.4f} perp {NE*(1+K0/2):.4f} ratio {1/(1+K0/2):.4f}")
print("control (gNe=0, full):", [(round(r, 2), round(a / p, 8)) for r, a, p, fn in solve(128, 16.0, 0.25, 0.0, [8, 16])])
configs = [(256, 32.0, 0.20, [6, 7, 8, 9, 10, 12, 14, 16, 24, 32]),
           (256, 40.0, 0.30, [8, 10, 13, 19, 26, 38, 51])]
for N, Lb, sg, ns in configs:
    full = solve(N, Lb, sg, YE, ns)
    lin = solve(N, Lb, sg, YE, ns, linear=True)
    print(f"\nN={N} L={Lb} soft={sg}")
    print("   r    q=gNi/gNe | linear-box axis perp | full axis perp  ax/pp | corrected(full-linbox+analytic) axis perp ax/pp")
    for (r, a, p, fn), (_, la, lp, _) in zip(full, lin):
        ca, cp = a - la + NE, p - lp + NE * (1 + K0 / 2)
        print(f" {r:6.3f}  {fn/YE:7.4f}   | {la:7.4f} {lp:7.4f}     | {a:7.4f} {p:7.4f} {a/p:7.4f} | {ca:7.4f} {cp:7.4f} {ca/cp:7.4f}")
