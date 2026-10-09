#!/usr/bin/env python3
"""Item 3: size of the orientation signal in R units, projection dilution, and a power
upper bound.  R = alpha(s)/alpha(control) is a VELOCITY-scale ratio (wide_binary_fish.py
docstring), so R ~ sqrt(v^2 factor).  EFE-dominated (q -> 0) angular factors only: this is
the maximum anisotropy (s3c shows it is smaller, and reversed for q >~ 0.3, at finite q).
Ignored: relative-velocity direction, s/r projection-factor correlations, orbit sampling
of theta, contaminants.  Sky positions and separation vectors isotropic."""
import numpy as np

rng = np.random.default_rng(20261008)
nu = lambda y: np.sqrt((1 + np.sqrt(1 + 4 / y**2)) / 2)
Kq = lambda y: -2 / (y**2 + y * np.sqrt(y**2 + 4) + 4)
q1 = 0.5; Q = (2 / 3) * (1 - q1**1.5 - (1 - q1)**1.5) / (q1 * (1 - q1))
YE = 1.9e-10 / 1.042e-10; NE = nu(YE); K0 = Kq(YE)
xc = 1.8; muc = xc / np.sqrt(1 + xc**2); Kc = 1 / (1 + xc**2)

models = {  # boost b(theta) on g (= v^2 at fixed r), EFE-dominated limit
    "prereg AQUAL x=1.8 K=0.236": lambda s2: 1 / (muc * np.sqrt(1 + Kc * s2)),
    "QUMOND B&Z eq15, code y_e":  lambda s2: NE * (1 + 0.5 * K0 * s2),
    "existing mock E (algebraic)": lambda s2: NE * (1 + K0 * (1 - s2)),
}

N = 4_000_000
def unit(n):
    v = rng.normal(size=(n, 3)); return v / np.linalg.norm(v, axis=1)[:, None]
los = unit(N); nvec = unit(N); g = np.array([1.0, 0.0, 0.0])   # g_ext direction = to GC
cos_t = nvec @ g; s2 = 1 - cos_t**2
ns = nvec - np.sum(nvec * los, 1)[:, None] * los
gs = g[None, :] - (los @ g)[:, None] * los
cpsi = np.abs(np.sum(ns * gs, 1)) / (np.linalg.norm(ns, axis=1) * np.linalg.norm(gs, axis=1))
med = np.median(cpsi)
print(f"MC N={N}: median |cos psi| = {med:.5f} (uniform psi -> cos45 = {np.cos(np.pi/4):.5f}); Q(q1=0.5)={Q:.4f}")
A_sky = cpsi > med
A_3d = np.abs(cos_t) > np.median(np.abs(cos_t))
print(f"<sin^2 th> aligned/perp: 3D split {s2[A_3d].mean():.4f}/{s2[~A_3d].mean():.4f};"
      f" sky split {s2[A_sky].mean():.4f}/{s2[~A_sky].mean():.4f}  (extreme 0/1)")

rows = {}
for name, b in models.items():
    for useQ in (True, False):
        v2 = (lambda bb: 1 + Q * (bb - 1)) if useQ else (lambda bb: bb)
        R0, R90 = np.sqrt(v2(b(0.0))), np.sqrt(v2(b(1.0)))
        Rall = np.sqrt(v2(b(s2)).mean())
        d3 = np.sqrt(v2(b(s2[A_3d])).mean()) - np.sqrt(v2(b(s2[~A_3d])).mean())
        dsky = np.sqrt(v2(b(s2[A_sky])).mean()) - np.sqrt(v2(b(s2[~A_sky])).mean())
        rows[(name, useQ)] = dsky
        print(f"{name:30s} Q={'yes' if useQ else 'no '}: v2(0)/v2(90)={v2(b(0.0))/v2(b(1.0)):.4f}"
              f"  R(0)-R(90)={R0-R90:+.4f}  <R>-1={Rall-1:+.4f}  dR 3D-median={d3:+.4f}"
              f"  dR sky-median={dsky:+.4f}  surviving sky/extreme={dsky/(R0-R90):.3f}")

# power upper bound with the published strict-cut sigma_R (WIDE_BINARY_FINAL_2026-10-04.md
# text, orientation-blind; no sample file read).  Halving N per arm -> sigma_dR = 2 sigma_R.
for cut, sR in (("strict", np.array([0.017, 0.023, 0.086])), ("loose", np.array([0.011, 0.017, 0.050]))):
    sd = 2 * sR; scomb = 1 / np.sqrt(np.sum(1 / sd**2)); w = (1 / sd**2) / np.sum(1 / sd**2)
    print(f"\n{cut}: sigma_dR per bin {sd}, inverse-variance weights {np.round(w,3)}, combined sigma_dR = {scomb:.4f};"
          f" 2-sigma Gate-1 needs dR >= {2*scomb:.4f}")
    for (name, useQ), d in rows.items():
        z = d / scomb
        print(f"   {name:30s} Q={'yes' if useQ else 'no '}: upper-bound z = {z:+.3f}  (N multiplier for |z|=2: {(2/abs(z))**2:6.1f}x)")
    # even with no projection loss and the 3D extreme contrast in every bin:
    b = models["QUMOND B&Z eq15, code y_e"]
    ext = np.sqrt(1 + Q * (b(0.0) - 1)) - np.sqrt(1 + Q * (b(1.0) - 1))
    print(f"   absolute ceiling (theta=0 vs 90 exactly, QUMOND, Q): dR={ext:.4f} -> z={ext/scomb:.2f}")
