#!/usr/bin/env python3
"""Item 2: x_e = g_ext/a0 at the Sun from V0^2/R0, for several a0. Literature inputs are [C]
(values as recalled; B&Z 2018 setup verified from arXiv:1805.12273 text: 232.8 km/s, 8.2 kpc)."""
import numpy as np
from scipy import constants as C

kpc = 1e3 * C.parsec
Mpc = 1e6 * C.parsec
c = C.c

def a0_cH(H0):  # bare cH0/2pi
    return c * (H0 * 1e3 / Mpc) / (2 * np.pi)

A0 = {
    "1.2e-10 (lit.)": 1.2e-10,
    "cH0/2pi H0=67.4": a0_cH(67.4),
    "cH0/2pi H0=73.0": a0_cH(73.0),
    "canon 5.461e-11*sqrt5": 5.461e-11 * np.sqrt(5),
}
for k, v in A0.items():
    print(f"a0[{k}] = {v:.5e} m/s^2")
print("code A0 = 1.042e-10 vs cH0/2pi(67.4) =", f"{a0_cH(67.4):.5e}",
      f"rel.err {(1.042e-10 / a0_cH(67.4) - 1) * 100:+.3f}%")

# [C] inputs (recalled): V0 = 229.0+-0.2(stat) (Eilers+2019), 232.8+-3 (McMillan 2017),
# 236+-7 (Reid+2019), 240+-8 (Reid+2014); R0 = 8.122 (GRAVITY 2018), 8.178 (GRAVITY 2019),
# 8.2 (McMillan 2017), 8.275 (GRAVITY 2021), 8.15+-0.15 (Reid+2019)
V0s = np.array([229.0, 232.8, 236.0, 240.0])
R0s = np.array([8.122, 8.178, 8.2, 8.275])
g = (V0s[:, None] * 1e3) ** 2 / (R0s[None, :] * kpc)
print("\ng_ext = V0^2/R0 grid (1e-10 m/s^2); rows V0", V0s, "cols R0", R0s)
print(np.array2string(g / 1e-10, precision=4))
gmin, gmax = g.min(), g.max()
gref = (232.8e3) ** 2 / (8.2 * kpc)
print(f"g_ext range {gmin:.4e} .. {gmax:.4e} ; reference (232.8, 8.2) {gref:.4e}")

mu = lambda x: x / np.sqrt(1 + x * x)
nu = lambda y: np.sqrt((1 + np.sqrt(1 + 4 / y**2)) / 2)
Kq = lambda y: -2 / (y**2 + y * np.sqrt(y**2 + 4) + 4)

print("\n a0 label               | x_e (min..ref..max) | K_e=1/(1+x^2) (max..ref..min) | y_e=x mu(x) | K0(QUMOND)")
for k, a0 in A0.items():
    xs = np.array([gmin, gref, gmax]) / a0
    Ks = 1 / (1 + xs**2)
    ys = xs * mu(xs)
    print(f" {k:22s} | {xs[0]:.3f} {xs[1]:.3f} {xs[2]:.3f} | {Ks[0]:.4f} {Ks[1]:.4f} {Ks[2]:.4f}"
          f" | {ys[0]:.3f}..{ys[2]:.3f} | {Kq(ys[0]):.4f}..{Kq(ys[2]):.4f}")

# The mock generator's E uses GE = 1.9e-10 as a NEWTONIAN field inside nu_std(GE/A0):
GE, A0c = 1.9e-10, 1.042e-10
ye = GE / A0c
gtrue = nu(ye) * GE
xe_true = gtrue / A0c
print(f"\ncode: y_e=GE/A0={ye:.4f}; implied true field nu*GE={gtrue:.4e} (cf. V0^2/R0 {gmin:.3e}..{gmax:.3e})")
print(f"code: implied AQUAL x_e={xe_true:.4f}, K_e=L={1/(1+xe_true**2):.4f}, QUMOND K0(y_e)={Kq(ye):.4f}")
print(f"claimed x_e=1.8 vs code y_e={ye:.3f}: the claimed value matches the Newtonian ratio, not g/a0")
# anisotropy (EFE-dominated limit) for the claimed and for the code-consistent K
for lab, Lv in (("claimed K_e=0.236", 1 / (1 + 1.8**2)), ("code-consistent L=%.4f" % (1 / (1 + xe_true**2)), 1 / (1 + xe_true**2))):
    print(f"  {lab}: v_c^2(0)/v_c^2(90) AQUAL = {np.sqrt(1+Lv):.4f};  QUMOND 1/(1+K0/2) = {1/(1 - Lv/(1+Lv)/2):.4f}")
