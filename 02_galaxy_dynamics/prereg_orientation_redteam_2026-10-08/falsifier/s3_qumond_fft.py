#!/usr/bin/env python3
"""Independent numerical check of the EFE anisotropy sign and size.

Full (non-linearised) QUMOND for a softened point mass in a uniform Newtonian external
field, solved spectrally in a periodic box:  g = longitudinal part of nu(|g_N|/a0) g_N.
Units G = M = a0 = 1.  External Newtonian field g_Ne = GE/A0 of the mock generator.
Compares, at the same points, with
  (i) linear QUMOND (Banik & Zhao 2018 eq. 15): boost = nu_e (1 + K0/2 sin^2 th)
 (ii) the mock generator's E boost (wide_binary_fish.boost('E'), 1D-QUMOND vector form),
      called through an unmodified copy of the module with a fixed external direction.
Uniform-field offsets (k=0 mode) cancel in the +-axis averages used below."""
import sys
import numpy as np
import scipy.fft as sfft

sys.dont_write_bytecode = True
import wbf_copy as WB  # byte-identical copy of 02_galaxy_dynamics/wide_binary_fish.py

nu = lambda y: np.sqrt((1 + np.sqrt(1 + 4 / y**2)) / 2)
Kq = lambda y: -2 / (y**2 + y * np.sqrt(y**2 + 4) + 4)
YE = WB.GE / WB.A0


def solve(N, Lbox, sig, gNe, ns):
    h = Lbox / N
    k1 = 2 * np.pi * sfft.fftfreq(N, d=h)
    k1r = 2 * np.pi * sfft.rfftfreq(N, d=h)
    kx, ky, kz = k1[:, None, None], k1[None, :, None], k1r[None, None, :]
    k2 = kx**2 + ky**2 + kz**2
    k2[0, 0, 0] = 1.0
    rho_k = np.exp(-0.5 * k2 * sig**2) / h**3          # unit-mass Gaussian, grid-normalised
    phik = -4 * np.pi * rho_k / k2
    phik[0, 0, 0] = 0
    s = (N, N, N)
    gN = [sfft.irfftn(-1j * kk * phik, s=s, workers=8) for kk in (kx, ky, kz)]
    del phik, rho_k
    gN[2] += gNe                                       # external Newtonian field along +z
    gmag = np.sqrt(gN[0]**2 + gN[1]**2 + gN[2]**2)
    nv = nu(gmag)
    Fk = [sfft.rfftn(nv * g, workers=8) for g in gN]
    # Newtonian internal magnitude at the sample points (before overwrite)
    gN[2] -= gNe
    kdotF = (kx * Fk[0] + ky * Fk[1] + kz * Fk[2]) / k2
    out = []
    g = [sfft.irfftn(kk * kdotF, s=s, workers=8) for kk in (kx, ky, kz)]  # longitudinal part
    for n in ns:
        pts = {"+z": ((0, 0, n), (0, 0, 1)), "-z": ((0, 0, -n), (0, 0, -1)),
               "+x": ((n, 0, 0), (1, 0, 0)), "-x": ((-n, 0, 0), (-1, 0, 0)),
               "+y": ((0, n, 0), (0, 1, 0)), "-y": ((0, -n, 0), (0, -1, 0))}
        Fr, FN = {}, {}
        for key, (ijk, rh) in pts.items():
            Fr[key] = -sum(g[c][ijk] * rh[c] for c in range(3))      # inward radial, QUMOND
            FN[key] = -sum(gN[c][ijk] * rh[c] for c in range(3))     # inward radial, Newton
        ax = 0.5 * (Fr["+z"] + Fr["-z"]); pp = 0.25 * (Fr["+x"] + Fr["-x"] + Fr["+y"] + Fr["-y"])
        fn = np.mean(list(FN.values()))
        out.append((n * h, fn, ax / fn, pp / fn))
    return out


def code_E_boost(yint, cos_t):
    """bE from the mock generator's boost('E'), external direction fixed at angle t."""
    class FixedRNG:
        def __init__(self, u): self.u = u
        def normal(self, size): return self.u
    u = np.array([[cos_t, np.sqrt(max(0.0, 1 - cos_t**2)), 0.0]])
    WB.RNG = FixedRNG(u)
    q1 = np.array([0.5]); Q = WB.q_two_body(q1)[0]
    b = WB.boost("E", np.array([yint * WB.A0]), q1)[0]
    return 1 + (b - 1) / Q


ns = [6, 8, 12, 16, 24, 32]
ne = nu(YE); K0 = Kq(YE)
print(f"y_e = GE/A0 = {YE:.4f}; nu_e = {ne:.4f}; K0 = {K0:.4f}")
print(f"linear QUMOND (B&Z eq.15): boost axis = {ne:.4f}, perp = {ne*(1+K0/2):.4f}, ratio = {1/(1+K0/2):.4f}")
print(f"mock E linear limit: axis = nu_e(1+K0) = {ne*(1+K0):.4f}, perp = nu_e = {ne:.4f}, ratio = {1+K0:.4f}")
for (N, Lb, sg) in ((256, 32.0, 0.20), (256, 24.0, 0.15)):
    print(f"\nFFT QUMOND  N={N} L={Lb} soft={sg}")
    print("   r   gNint/gNe | PDE axis  PDE perp  PDE ax/pp | mockE axis mockE perp mockE ax/pp")
    for r, fn, a, p in solve(N, Lb, sg, YE, ns):
        ea = 0.5 * (code_E_boost(fn, 1.0) + code_E_boost(fn, -1.0))
        ep = code_E_boost(fn, 0.0)
        print(f" {r:5.3f}  {fn/YE:7.3f}   | {a:7.4f}  {p:7.4f}   {a/p:7.4f}  | {ea:7.4f}   {ep:7.4f}    {ea/ep:7.4f}")
# control: no external field -> axis/perp must be 1 (cubic symmetry)
print("\ncontrol gNe=0:", [(round(r, 3), round(a / p, 6)) for r, fn, a, p in solve(128, 16.0, 0.25, 0.0, [8, 16])])
