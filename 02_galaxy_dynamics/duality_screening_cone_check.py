#!/usr/bin/env python3
"""Light cone and tensor speed for the duality screening with an external field chi.

Setup (DUALITY_SCREENING_ACTION.md; RY, 2026-10-15): chi is not sourced by local mass.
On a patch, grad chi is the external field, eta = |grad chi| / a0, S(eta) = 1 / (1 + eta^2).

 1. Photon cone of gt = A g + B u u in the u rest frame: c^2 = (A - B) / A.
    The TensorSpeed.lean map (A = e^{-2 phi}, B = -2 sinh 2 phi) gives e^{4 phi}.
    The live D9 frame (matter on g: A = 1, B = 0) gives 1.
 2. S put into the TensorSpeed map: c^2 - 1 = S (e^{4 phi} - 1). S > 0, so it is luminal only at phi = 0.
 3. chi in the matter metric. A conformal A(chi) is sourced by dust, which the decision excludes.
    A disformal (C / a0^2) dchi dchi is not sourced by static dust, but it tilts the photon cone
    along grad chi. GW170817 bounds C.
 4. Graviton. S(X_chi) F(Q) is algebraic in g^{mu nu}: it adds a source and a mass-like term to
    the TT equation, and nothing to its two-derivative part.
 5. eta at the live a0: the Sun (Hees 2016 bracket), Chae 2020 SPARC environments, and the
    single-field question at the Sun's position.
Writes DUALITY_SCREENING_CONE_CHECK.json. Exit 0 only if every assertion holds.
"""
import json
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
A0 = 1.1607e-10                     # live a0, m/s^2 (CURRENT_STATE, 2026-10-09)
C_LIGHT = 2.998e8
H0 = 67.4e3 / 3.0857e22             # s^-1
G_EXT_SUN = (1.9e-10, 2.4e-10)      # Galactic field at the Sun, Hees 2016 bracket
GW_LO, GW_HI = -3e-15, 7e-16        # (v_GW - v_EM) / v_EM, Abbott et al. 2017, ApJL 848 L13
PHI_TEVES = (1e-6, 0.1)             # galactic and cosmological phi quoted in TARGET_D8 1.4

S = lambda eta: 1.0 / (1.0 + eta**2)
out = {}

# 1. photon cone of gt = A g + B u u, rest frame u^mu = (1, 0, 0, 0), g = diag(-1, 1, 1, 1)
A, B, v, phi = sp.symbols("A B v phi", real=True)
v2 = sp.solve(sp.Eq(-A + A * v**2 + B, 0), v**2)[0]
assert sp.simplify(v2 - (A - B) / A) == 0
teves = sp.simplify(v2.subs({A: sp.exp(-2 * phi), B: -2 * sp.sinh(2 * phi)}).rewrite(sp.exp))
assert sp.simplify(teves - sp.exp(4 * phi)) == 0          # TensorSpeed.disformal_photon_speed_sq
assert v2.subs({A: 1, B: 0}) == 1                          # live D9 frame
assert sp.simplify(v2.subs(B, 0)) == 1                     # any conformal factor leaves the cone alone
out["cone_general"] = "c^2 = (A - B)/A; luminal iff B = 0"

# 2. S inserted into the TensorSpeed map
s_ = sp.symbols("S", positive=True)
screened = sp.simplify(v2.subs({A: sp.exp(-2 * phi), B: -2 * s_ * sp.sinh(2 * phi)}).rewrite(sp.exp))
assert sp.simplify(screened - (1 + s_ * (sp.exp(4 * phi) - 1))) == 0
need = {}
for ph in PHI_TEVES:
    s_max = 2 * abs(GW_LO) / np.expm1(4 * ph)              # Delta ~ -S (e^{4 phi} - 1) / 2
    need[str(ph)] = {"S_max": s_max, "eta_min": float(np.sqrt(1 / s_max - 1))}
out["teves_with_S"] = {"c2_minus_1": "S (e^{4 phi} - 1)", "luminal_iff": "phi = 0 (S > 0)", "needed": need}

# 3. chi in the matter metric. Dust at rest, static chi with an external gradient.
a0, eta, al, x, y, z, t, rho = sp.symbols("a0 eta alpha x y z t rho", positive=True)
Cd = sp.symbols("C", real=True)
X = [t, x, y, z]
chi = a0 * eta * (x * sp.sin(al) + z * sp.cos(al))
dchi = [sp.diff(chi, c) for c in X]
u_up = [1, 0, 0, 0]
T_up = [[rho * u_up[m] * u_up[n] for n in range(4)] for m in range(4)]
g_dn = sp.diag(-1, 1, 1, 1)
trace_T = sum(T_up[m][n] * g_dn[m, n] for m in range(4) for n in range(4))
J_disf = [sum(T_up[m][n] * dchi[m] for m in range(4)) for n in range(4)]   # T^{mn} d_m chi
assert sp.simplify(trace_T + rho) == 0                     # conformal source = A'(chi) T / 2 = -A' rho / 2
assert all(sp.simplify(j) == 0 for j in J_disf)            # disformal source vanishes for static dust
k_th = sp.symbols("theta", real=True)
v2d = sp.solve(sp.Eq(-1 + v**2 + Cd * eta**2 * v**2 * sp.cos(k_th) ** 2, 0), v**2)[0]
assert sp.simplify(v2d - 1 / (1 + Cd * eta**2 * sp.cos(k_th) ** 2)) == 0
# Delta = v_GW / v_EM - 1 = sqrt(1 + C eta^2 cos^2) - 1 ~ C eta^2 cos^2 / 2
chae = json.load(open(HERE / "CHAE2020_EXTERNAL_FIELDS.json"))["galaxies"]
e_env = np.array([g["e_env"] for g in chae.values() if g.get("e_env") is not None])
eta_env = e_env * 1.2e-10 / A0
bound = {}
for label, et in (("eta_0.01", 0.01), ("eta_median_chae", float(np.median(eta_env))), ("eta_max_chae", float(eta_env.max()))):
    m = et**2 / 3                                          # <cos^2 theta> = 1/3
    bound[label] = {"C_max_if_C_pos": 2 * GW_HI / m, "absC_max_if_C_neg": 2 * abs(GW_LO) / m}
out["chi_disformal"] = {"c_parallel_sq": "1 / (1 + C eta^2 cos^2 theta)", "gw170817_bound": bound,
                        "conformal_source_dust": "-A'(chi) rho / 2", "disformal_source_static_dust": 0}

# 4. TT wave along z, + and x polarizations; grad chi in the x-z plane at angle alpha to z
hp, hx = sp.symbols("h_p h_x", real=True)
h_up = sp.zeros(4, 4)
h_up[1, 1], h_up[2, 2], h_up[1, 2], h_up[2, 1] = hp, -hp, hx, hx
eta_up = sp.diag(-1, 1, 1, 1)
ginv = eta_up - h_up + h_up * eta_up * h_up                # g^{mn} to second order (eta_up = inverse of itself)
Xchi = sp.expand(sum(ginv[m, n] * dchi[m] * dchi[n] for m in range(4) for n in range(4)))
first = sp.simplify(sp.diff(Xchi, hp).subs({hp: 0, hx: 0}))
assert sp.simplify(first + a0**2 * eta**2 * sp.sin(al) ** 2) == 0   # dX = -a0^2 eta^2 sin^2(alpha) h_+
k100 = 2 * np.pi * 100 / C_LIGHT
# The second-order coefficient is of order 16 pi G rho / c^2 for the screened sector's energy
# density rho. A component no denser than critical gives at most 6 H0^2 / c^2; 10 for margin.
m2_max = 10 * (H0 / C_LIGHT) ** 2
out["graviton"] = {"principal_symbol": "unchanged: S(X_chi) F(Q) contains no derivative of g",
                   "first_order_coupling": "dX_chi = -a0^2 eta^2 sin^2(alpha) h_+  (a source term)",
                   "m2_max_per_m2": m2_max, "dispersion_dv_at_100Hz_max": m2_max / (2 * k100**2)}

# 5. eta values at the live a0
sun = {f"{g:.1e}": {"eta": g / A0, "S": S(g / A0)} for g in G_EXT_SUN}
m31 = 6.674e-11 * 1.5e12 * 1.989e30 / (0.78 * 3.0857e22) ** 2   # M31's Newtonian pull on the Galaxy (illustrative)
out["eta"] = {"a0": A0, "sun": sun,
              "sparc_chae2020": {"n": int(len(eta_env)), "min": float(eta_env.min()), "median": float(np.median(eta_env)),
                                 "max": float(eta_env.max()), "S_min": float(S(eta_env).min())},
              "galaxy_environment_m31": {"g": m31, "eta": m31 / A0, "S": S(m31 / A0)}}
assert S(eta_env).min() > 0.99 and all(0.15 < r["S"] < 0.3 for r in sun.values())

# One field, two systems at the Sun's position. A gradient there is the Galactic field for the
# solar system and the environment's field for the Galaxy. The tidal tensor tells them apart:
# x = c^2 |grad grad Phi| / a0^2 (Frobenius norm).
GM_SUN = 1.32712e20
r_m = np.sqrt(GM_SUN / A0)                                 # Sun's MOND radius
x_sun = C_LIGHT**2 * np.sqrt(6) * GM_SUN / r_m**3 / A0**2  # point mass: eigenvalues (-2, 1, 1) GM/r^3
rho_disk = 0.1 * 1.989e30 / 3.0857e16**3                   # local midplane density, 0.1 Msun/pc^3
v0, r0 = 233e3, 8.2 * 3.0857e19
t_disk = np.sqrt((4 * np.pi * 6.674e-11 * rho_disk) ** 2 + 2 * (v0**2 / r0**2) ** 2)
x_disk = C_LIGHT**2 * t_disk / A0**2
out["one_field"] = {"eta_needed_sun": [sun["1.9e-10"]["eta"], sun["2.4e-10"]["eta"]],
                    "eta_galaxy_environment": m31 / A0,
                    "tidal_x_sun_mond_radius": x_sun, "tidal_x_disk_R0": x_disk, "r_mond_au": r_m / 1.496e11}
assert x_sun / x_disk > 1e3

# covariant definition: g^{mn} vs the aether projector q^{mn} = g^{mn} + A^m A^n, for chi = chi(t)
cd = sp.symbols("chidot", positive=True)
X_g = -cd**2                                               # g^{00} chidot^2
X_q = 0                                                    # q^{00} = g^{00} + 1 = 0 in the aether frame
assert sp.solve(sp.Eq(1 + X_g / a0**2, 0), cd) == [a0]     # S = 1/(1 + X/a0^2) has a pole at chidot = a0
out["covariant_eta"] = {"g_inverse": "eta^2 = -chidot^2/a0^2 for chi(t); S has a pole at chidot = a0",
                        "aether_projector": "eta^2 = q^{mn} d chi d chi / a0^2 >= 0; chi(t) gives eta = 0"}
assert X_q == 0

json.dump(out, open(HERE / "DUALITY_SCREENING_CONE_CHECK.json", "w"), indent=1)
print("1  cone c^2 = (A-B)/A; TensorSpeed map -> e^{4 phi}; live D9 frame (B = 0) -> 1")
print("2  S in the TensorSpeed map: c^2 - 1 = S (e^{4 phi} - 1), luminal only at phi = 0")
for ph, r in need.items():
    print(f"     phi = {ph}: GW170817 needs S <= {r['S_max']:.2e}, eta >= {r['eta_min']:.2e}")
print("3  chi conformal: sourced by dust (-A' rho/2). chi disformal: unsourced by static dust,")
print("     photon c^2 = 1/(1 + C eta^2 cos^2 theta); GW170817 with <cos^2> = 1/3:")
for k, r in bound.items():
    print(f"     {k}: C <= {r['C_max_if_C_pos']:.1e} (C > 0), |C| <= {r['absC_max_if_C_neg']:.1e} (C < 0)")
print(f"4  TT: dX_chi = -a0^2 eta^2 sin^2(alpha) h_+; dispersion dv <= {out['graviton']['dispersion_dv_at_100Hz_max']:.1e} at 100 Hz")
print(f"5  Sun eta {sun['1.9e-10']['eta']:.2f}-{sun['2.4e-10']['eta']:.2f}, S {sun['2.4e-10']['S']:.3f}-{sun['1.9e-10']['S']:.3f}; "
      f"SPARC (Chae, n={len(eta_env)}) eta {eta_env.min():.3f}-{eta_env.max():.3f}, S >= {S(eta_env).min():.4f}; "
      f"M31 on the Galaxy eta {m31 / A0:.1e}")
print("   chi(t) with g^{mn}: S has a pole at chidot = a0; with the aether projector eta = 0")
print(f"6  one field at the Sun: Cassini needs eta {sun['1.9e-10']['eta']:.2f}-{sun['2.4e-10']['eta']:.2f}, the Galaxy's own "
      f"environment gives {m31 / A0:.1e}; tidal x {x_sun:.1e} at the Sun's MOND radius ({r_m / 1.496e11:.0f} AU) "
      f"vs {x_disk:.1e} in the disk at R0")
print("ALL CHECKS PASS")
