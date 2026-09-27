#!/usr/bin/env python3
"""How much Shapiro delay does the Milky Way's MOND 'phantom dark matter' add on the GW170817 line of sight?
Why it matters: light and gravitational waves from GW170817 arrived 1.74 s apart after sharing this path.
If only photons felt the phantom potential (photon-only / disformal lensing: a 'dark matter emulator',
Boran et al. 2018, PRD 97, 041501), the two would have arrived ~this delay apart. Estimate only:
point-mass Milky Way, mu_std (QUMOND nu_std), external field in the 1D collinear approximation."""
import numpy as np
from scipy.integrate import quad
import astropy.units as u
from astropy.coordinates import SkyCoord, Galactocentric
from efe_quadrupole_q2 import A0_DERIVED as A0
G, C, MSUN, KPC = 6.674e-11, 2.998e8, 1.989e30, 3.0857e19
nu = lambda y: np.sqrt(0.5 + np.sqrt(0.25 + 1.0 / y**2))              # QUMOND nu for mu_std
def g_tot(r, M, ge):                                                   # 1D EFE (collinear) estimate
    gN = G * M / r**2
    return nu((gN + ge) / A0) * (gN + ge) - nu(ge / A0) * ge
def phi_dark(r, M, ge, rmax=1e3 * 1e3 * KPC):                          # potential of (g - gN), zero at infinity
    f = lambda lr: (g_tot(np.exp(lr), M, ge) - G * M / np.exp(lr)**2) * np.exp(lr)
    inner = quad(f, np.log(r), np.log(rmax), limit=400)[0]
    ye = ge / A0; h = 1e-6
    L = (np.log(nu(ye * (1 + h))) - np.log(nu(ye * (1 - h)))) / (np.log(1 + h) - np.log(1 - h))
    tail = (nu(ye) * (1 + L) - 1) * G * M / rmax                       # linear-EFE 1/r tail beyond rmax
    return -(inner + tail)
src = SkyCoord(ra=197.4487 * u.deg, dec=-23.3839 * u.deg, distance=40 * u.Mpc).transform_to(Galactocentric())
sun = -np.array([Galactocentric().galcen_distance.to_value(u.m), 0, -Galactocentric().z_sun.to_value(u.m)])
tgt = np.array([src.x.to_value(u.m), src.y.to_value(u.m), src.z.to_value(u.m)])
n = (tgt - sun) / np.linalg.norm(tgt - sun); D = np.linalg.norm(tgt - sun)
print(f"a0 = {A0:.3e} m/s^2; NGC 4993 at Galactocentric angle {np.degrees(np.arccos(np.dot(n, -sun/np.linalg.norm(sun)))):.0f} deg from the Sun-to-Galactic-Centre direction")
for M in (5e10 * MSUN, 6e10 * MSUN, 7e10 * MSUN):
    vf = (G * M * A0) ** 0.25
    for eta in (0.01, 0.02, 0.03):
        ge = eta * A0
        s = np.logspace(np.log10(0.1 * KPC), np.log10(D), 160)
        ph = np.array([abs(phi_dark(np.linalg.norm(sun + si * n), M, ge)) for si in s])
        dt = 2 / C**3 * np.trapezoid(ph, s)
        print(f"M_b={M/MSUN:.0e} Msun (v_f={vf/1e3:.0f} km/s), g_e={eta:.2f} a0: phantom Shapiro delay = {dt/86400:6.0f} days "
              f"-> 1.74 s is {1.74/dt:.1e} of it")
