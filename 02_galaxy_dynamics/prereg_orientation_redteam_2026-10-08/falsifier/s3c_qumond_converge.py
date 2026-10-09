#!/usr/bin/env python3
"""Convergence study for s3/s3b: null-point regularisation |g_N| -> sqrt(|g_N|^2+eps^2),
optional Gaussian filter on F, three resolutions/boxes. Reports the 'corrected' ratio
(full - linear-in-same-box + analytic linear) at common radii."""
import numpy as np, scipy.fft as sfft
def nu(y):
    y = np.maximum(y, 1e-300); return np.sqrt((1 + np.sqrt(1 + 4 / y**2)) / 2)
Kq = lambda y: -2 / (y**2 + y * np.sqrt(y**2 + 4) + 4)
YE = 1.9e-10 / 1.042e-10; NE, K0 = nu(YE), Kq(YE)
AX, PP = NE, NE * (1 + K0 / 2)

def run(N, Lb, sig, eps, filt, rs):
    h = Lb / N; ns = [int(round(r / h)) for r in rs]
    k1 = 2*np.pi*sfft.fftfreq(N, d=h); k1r = 2*np.pi*sfft.rfftfreq(N, d=h)
    kx, ky, kz = k1[:, None, None], k1[None, :, None], k1r[None, None, :]
    k2 = kx**2 + ky**2 + kz**2; k2[0, 0, 0] = 1.0
    W = np.exp(-0.5 * k2 * (filt * h)**2) if filt else 1.0
    phik = -4*np.pi*np.exp(-0.5*k2*sig**2)/h**3/k2; phik[0, 0, 0] = 0
    s = (N, N, N)
    gN = [sfft.irfftn(-1j*kk*phik, s=s, workers=8) for kk in (kx, ky, kz)]; del phik
    out = {}
    for mode in ("full", "lin"):
        if mode == "lin":
            F = [NE*gN[0], NE*gN[1], NE*(1+K0)*gN[2]]
        else:
            tz = gN[2] + YE; gm = np.sqrt(gN[0]**2 + gN[1]**2 + tz**2 + eps**2); nv = nu(gm)
            F = [nv*gN[0], nv*gN[1], nv*tz]; del tz, gm, nv
        Fk = [sfft.rfftn(f, workers=8)*W for f in F]; del F
        kdF = (kx*Fk[0] + ky*Fk[1] + kz*Fk[2]) / k2; del Fk
        g = [sfft.irfftn(kk*kdF, s=s, workers=8) for kk in (kx, ky, kz)]; del kdF
        res = []
        for n in ns:
            pts = [((0,0,n),(0,0,1)),((0,0,-n),(0,0,-1)),((n,0,0),(1,0,0)),((-n,0,0),(-1,0,0)),((0,n,0),(0,1,0)),((0,-n,0),(0,-1,0))]
            Fr = [-sum(g[c][p]*e[c] for c in range(3)) for p, e in pts]
            FN = np.mean([-sum(gN[c][p]*e[c] for c in range(3)) for p, e in pts])
            res.append((np.mean(Fr[:2])/FN, np.mean(Fr[2:])/FN, FN))
        out[mode] = res; del g
    return [(n*h, f[2]/YE, f[0], f[1], f[0]-l[0]+AX, f[1]-l[1]+PP) for n, f, l in zip(ns, out["full"], out["lin"])]

rs = [0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]
print(f"analytic linear (B&Z eq.15): axis {AX:.4f} perp {PP:.4f} ratio {AX/PP:.4f}")
for cfg in [(256, 16.0, 0.10, 0.0, 0), (256, 16.0, 0.10, 0.02, 1.5), (256, 24.0, 0.15, 0.02, 1.5), (256, 32.0, 0.20, 0.02, 1.5)]:
    N, Lb, sg, eps, fl = cfg
    rows = run(N, Lb, sg, eps, fl, [r for r in rs if r < Lb/5])
    print(f"\nN={N} L={Lb} soft={sg} eps={eps} filt={fl}h :  r  q | raw ax/pp | corrected axis perp ax/pp")
    for r, q, a, p, ca, cp in rows:
        print(f"   {r:5.3f} {q:6.3f} | {a/p:7.4f} | {ca:7.4f} {cp:7.4f} {ca/cp:7.4f}")
