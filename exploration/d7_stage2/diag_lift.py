"""Does the solver's Hessian carry TARGET_D3 section 23's lift of the aether-tilt zero mode?
Zero mode (metric frozen, as in section 23): delta F = chi, delta u = -grad chi / Q0, which leaves S = grad phi + Q0 u
(the combination inside Y) unchanged. Section 23: E_lift = [-2 K2 Q0^2 Psi + K_B lap Psi + (2-K_B) lap phi] |grad Lambda|^2
with delta u = grad Lambda, i.e. |grad Lambda|^2 = |grad chi|^2 / Q0^2. The solver's quadratic form dx^T H dx along the
mode (H = Hessian of the action S = int L) should equal -2 int E_lift dV if L = -E for static fields.
Bumps chi = exp(-((r - r0)/w)^2) at several r0; static solution g_e = 0.003 a0, box asinh(300), 32x64 (cached).
lap phi and lap Psi from the spherical flux laws of the static solution: J'(g_phi) g_phi = M(<r)/(12 pi r^2),
Phihat_r = M(<r)/(12 pi r^2), Psi_r = Phihat_r + g_phi; the Psi term uses the static solution's own Psi.
"""

import math
import numpy as np
import solve_fe as FE

vf = 10 / 299792.458
b = 3e-4
M = 12 * math.pi * vf**4 / FE.A0T
g_e = 0.003 * FE.A0T
Q0, KB, K2 = 0.1, 0.5, 75.0
g, P, xs, res = FE.static_solution(32, 64, M, b, g_e, 300.0)
grad, H, Y = P.grad_hess(xs)
dm = P.dm
RR, ZZ = np.meshgrid(g.Rn, g.zn, indexing="ij")
Rn, Zn = RR.ravel(), ZZ.ravel()
rn = np.hypot(Rn, Zn)


def gphi_of(r):
    yv = (M * r**3 / (r**2 + b**2) ** 1.5 / (12 * math.pi * r**2)) / FE.A0T
    return FE.A0T * np.sqrt(0.5 * (yv**2 + np.sqrt(yv**4 + 4 * yv**2)))


def lap_radial(fr, r, h=1e-3):
    """(1/r^2) d(r^2 f_r)/dr by central difference."""
    rp, rm = r * (1 + h), r * (1 - h)
    return (rp**2 * fr(rp) - rm**2 * fr(rm)) / (2 * r * h) / r**2


phihat_r = lambda r: M * r**3 / (r**2 + b**2) ** 1.5 / (12 * math.pi * r**2)
q = (P.D @ xs).reshape(g.ng, FE.NQ)
Psi_g = -0.5 * q[:, 3 * FE.FIX["S"]]
rg = np.hypot(g.Rg, g.zg)
for r0, w in ((0.15e-3, 0.05e-3), (0.3e-3, 0.1e-3), (0.6e-3, 0.2e-3), (1.2e-3, 0.4e-3)):
    chi = np.exp(-(((rn - r0) / w) ** 2))
    dchi = -2 * (rn - r0) / w**2 * chi  # d chi / dr
    with np.errstate(invalid="ignore", divide="ignore"):
        cR = np.where(rn > 0, dchi * Rn / rn, 0.0)
        cZ = np.where(rn > 0, dchi * Zn / rn, 0.0)
    arr = np.zeros((FE.NF, g.nnode))
    arr[FE.FIX["F"]] = chi
    arr[FE.FIX["U_R"]] = -cR / Q0
    arr[FE.FIX["U_z"]] = -cZ / Q0
    dx = dm.from_nodes(arr)
    quad = float(dx @ (H @ dx))
    # section 23 prediction at the Gauss points, with |grad chi|^2 from the same FE interpolant
    qd = (P.D @ dx).reshape(g.ng, FE.NQ)
    gchi2 = qd[:, 3 * FE.FIX["F"] + 1] ** 2 + qd[:, 3 * FE.FIX["F"] + 2] ** 2
    lap_phi = lap_radial(gphi_of, rg)
    lap_Psi = lap_radial(lambda r: phihat_r(r) + gphi_of(r), rg)
    c_terms = {
        "Q-sector": -2 * K2 * Q0**2 * Psi_g,
        "K_B lap Psi": KB * lap_Psi,
        "(2-K_B) lap phi": (2 - KB) * lap_phi,
    }
    E = {k: float(np.sum(g.w * v * gchi2) / Q0**2) for k, v in c_terms.items()}
    Etot = sum(E.values())
    # the pieces of the quadratic form, to see what cancels
    off = dm.offsets
    sl = {n: slice(off[FE.FIX[n]], off[FE.FIX[n] + 1]) for n in ("F", "U_R", "U_z")}
    xF = np.zeros_like(dx)
    xF[sl["F"]] = dx[sl["F"]]
    xU = dx - xF
    print(
        f"r0 = {r0 * 1e3:.2f} kpc: dx^T H dx = {quad:+.4e}; -2 E_lift(sec 23) = {-2 * Etot:+.4e}; ratio {quad / (-2 * Etot):+.4f}"
    )
    print(
        f"      pieces: FF {xF @ (H @ xF):+.3e}, UU {xU @ (H @ xU):+.3e}, 2FU {2 * xF @ (H @ xU):+.3e}; "
        + ", ".join(f"{k} {v:+.3e}" for k, v in E.items())
    )

# locking check: the discrete curl of the FE-interpolated trial field, and its F^2 energy (local coefficient -1 on
# (U_R_z - U_z_R)^2 in HL, diag_aether_block.py), against the UU block of the quadratic form
print("locking check (same bumps):")
for r0, w in ((0.15e-3, 0.05e-3), (0.3e-3, 0.1e-3), (0.6e-3, 0.2e-3), (1.2e-3, 0.4e-3)):
    chi = np.exp(-(((rn - r0) / w) ** 2))
    dchi = -2 * (rn - r0) / w**2 * chi
    with np.errstate(invalid="ignore", divide="ignore"):
        cR = np.where(rn > 0, dchi * Rn / rn, 0.0); cZ = np.where(rn > 0, dchi * Zn / rn, 0.0)
    arr = np.zeros((FE.NF, g.nnode)); arr[FE.FIX["U_R"]] = -cR / Q0; arr[FE.FIX["U_z"]] = -cZ / Q0
    dx = dm.from_nodes(arr)
    qd = (P.D @ dx).reshape(g.ng, FE.NQ)
    curl = qd[:, 3 * FE.FIX["U_R"] + 2] - qd[:, 3 * FE.FIX["U_z"] + 1]
    grad_u2 = sum(qd[:, 3 * FE.FIX[n] + k] ** 2 for n in ("U_R", "U_z") for k in (1, 2))
    E_curl = -2 * float(np.sum(g.w * curl**2))      # x^T H x of the term -curl^2 (HL entries -1, +1, +1, -1)
    print(f"  r0 = {r0 * 1e3:.2f} kpc: UU form {float(dx @ (H @ dx)):+.4e}, curl^2 part {E_curl:+.4e}, "
          f"rms discrete curl / rms |grad u| = {math.sqrt(np.sum(g.w * curl**2) / np.sum(g.w * grad_u2)):.3f}")
