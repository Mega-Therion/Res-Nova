#!/usr/bin/env python3
"""Which side does light have a harder time coming from? Shapiro delay through the Milky Way's
(baryonic + mu_std phantom) potential, by direction, for a source 40 Mpc away. Estimate: softened spherical
Milky Way (Plummer a = 3 kpc), QUMOND nu_std, 1D collinear external field. Also: aether-frame one-way light
speed from ahead/behind for the Sun's CMB-frame motion (round trip stays exactly c)."""
import numpy as np
from scipy.integrate import quad
import astropy.units as u
from astropy.coordinates import SkyCoord, Galactocentric, get_constellation
from efe_quadrupole_q2 import A0_DERIVED as A0
G, C, MSUN, KPC = 6.674e-11, 2.998e8, 1.989e30, 3.0857e19
M, A, GE = 6e10 * MSUN, 3 * KPC, 0.02 * A0
nu = lambda y: np.sqrt(0.5 + np.sqrt(0.25 + 1.0 / y**2))
gN = lambda r: G * M * r / (r * r + A * A) ** 1.5
gT = lambda r: nu((gN(r) + GE) / A0) * (gN(r) + GE) - nu(GE / A0) * GE
RMAX = 1e6 * KPC
def phi(r, g):                                          # potential of field g, zero at infinity (1/r tail beyond RMAX)
    inner = quad(lambda lr: g(np.exp(lr)) * np.exp(lr), np.log(max(r, 1e-3 * KPC)), np.log(RMAX), limit=400)[0]
    return -(inner + g(RMAX) * RMAX)
rg = np.logspace(np.log10(0.01 * KPC), np.log10(0.99 * RMAX), 400)
PN = np.array([phi(r, gN) for r in rg]); PT = np.array([phi(r, gT) for r in rg])
iN = lambda r: np.interp(np.log(r), np.log(rg), PN); iT = lambda r: np.interp(np.log(r), np.log(rg), PT)
gc = Galactocentric(); sun = np.array([-gc.galcen_distance.to_value(u.m), 0, gc.z_sun.to_value(u.m)])
def delay(l, b, D=40 * 1e3 * KPC):
    tgt = SkyCoord(l=l * u.deg, b=b * u.deg, distance=D * u.m, frame="galactic").transform_to(gc)
    n = np.array([tgt.x.to_value(u.m), tgt.y.to_value(u.m), tgt.z.to_value(u.m)]) - sun; n /= np.linalg.norm(n)
    s = np.concatenate([np.linspace(0, 30 * KPC, 3000)[1:], np.logspace(np.log10(30 * KPC), np.log10(D), 400)[1:]])
    rr = np.linalg.norm(sun[None, :] + s[:, None] * n[None, :], axis=1)
    return 2 / C**3 * np.trapezoid(np.abs(iN(rr)), s) / 86400, 2 / C**3 * np.trapezoid(np.abs(iT(rr) - iN(rr)), s) / 86400
dirs = {"toward Galactic Centre": (0, 0), "Galactic anti-centre": (180, 0), "north Galactic pole": (0, 90),
        "ahead of our motion (CMB apex)": (264.021, 48.253), "behind us (CMB anti-apex)": (84.021, -48.253),
        "Great Attractor": (307, 9), "GW170817 / NGC 4993": (308.37, 39.30)}
print(f"source at 40 Mpc; M_b = 6e10 Msun (Plummer 3 kpc), g_e = 0.02 a0, a0 = {A0:.3e}")
print(f"{'direction':32s} {'constellation':14s} {'baryons (d)':>11s} {'phantom (d)':>11s} {'total (d)':>9s}")
for k, (l, b) in dirs.items():
    dn, dd = delay(l, b)
    con = get_constellation(SkyCoord(l=l * u.deg, b=b * u.deg, frame="galactic"))
    print(f"{k:32s} {con:14s} {dn:11.0f} {dd:11.0f} {dn + dd:9.0f}")
beta = 369.82e3 / C
print(f"\nAether-frame one-way light speed (Sun at {369.82} km/s vs CMB frame; round trip = c exactly):")
print(f"  light arriving from behind (catching up): c/(1+v/c) = {1/(1+beta):.6f} c")
print(f"  light arriving from ahead  (head-on):     c/(1-v/c) = {1/(1-beta):.6f} c")
