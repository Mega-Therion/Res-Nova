#!/usr/bin/env python3
"""Item 1: K_e = d ln mu / d ln x for mu_std, plus the EFE-dominated point-mass
potential forms (AQUAL, Milgrom 1986 / Banik & Zhao 2018 eq. 32; QUMOND, B&Z eq. 15).
Pure symbolic / analytic; no data."""
import numpy as np
import sympy as sp

x, y, L, K0, nue, mue, G, M = sp.symbols("x y L K0 nu_e mu_e G M", positive=True)
X, Y, Z = sp.symbols("X Y Z", real=True)

# ---- 1a. K_e for mu_std
mu = x / sp.sqrt(1 + x**2)
Ke = sp.simplify(sp.diff(sp.log(mu), x) * x)
print("mu_std(x) =", mu)
print("K_e = d ln mu/d ln x =", Ke, "  (claimed 1/(1+x^2)) -> equal:",
      sp.simplify(Ke - 1 / (1 + x**2)) == 0)
for xv in (1.8, 1.785):
    print(f"  K_e(x={xv}) = {float(Ke.subs(x, xv)):.5f}   claimed ~0.24")

# ---- 1b. QUMOND counterpart: nu_std(y) and K0 = d ln nu / d ln y
nu = sp.sqrt((1 + sp.sqrt(1 + 4 / y**2)) / 2)
K0e = sp.simplify(sp.diff(sp.log(nu), y) * y)
print("K0(y) = d ln nu/d ln y =", K0e)
# consistency: y = x mu(x)  =>  (1+L)(1+K0) = 1   (B&Z 2018 eq. 38)
for xv in (1.785, 1.8, 2.0):
    yv = xv * float(mu.subs(x, xv))
    Lv = float(Ke.subs(x, xv)); Kv = float(K0e.subs(y, yv))
    print(f"  x={xv}: y=x*mu={yv:.4f}  L={Lv:.5f}  K0={Kv:.5f}  (1+L)(1+K0)={(1+Lv)*(1+Kv):.6f}"
          f"  -L/(1+L)={-Lv/(1+Lv):.5f}  nu(y)*mu(x)={float(nu.subs(y,yv))*float(mu.subs(x,xv)):.6f}")

# ---- 1c. AQUAL EFE-dominated solution satisfies the linearised AQUAL equation
# mu_e[(1+L) d_z^2 + d_x^2 + d_y^2] phi = 4 pi G rho  (z along g_ext)
r = sp.sqrt(X**2 + Y**2 + Z**2)
sin2 = (X**2 + Y**2) / r**2
phiA = -G * M / (mue * r * sp.sqrt(1 + L * sin2))
op = sp.diff(phiA, X, 2) + sp.diff(phiA, Y, 2) + (1 + L) * sp.diff(phiA, Z, 2)
print("AQUAL: linearised operator on Phi (r != 0) simplifies to:", sp.simplify(op))
# flux normalisation: integral over a sphere of mu_e * (grad phi + L z^ d_z phi) . n dA = 4 pi G M
th, ph = sp.symbols("theta phi_az", real=True)
R0 = sp.symbols("R0", positive=True)
gradA = [sp.diff(phiA, v) for v in (X, Y, Z)]
gradA[2] = gradA[2] * (1 + L)
sub = {X: R0 * sp.sin(th) * sp.cos(ph), Y: R0 * sp.sin(th) * sp.sin(ph), Z: R0 * sp.cos(th)}
nvec = [sp.sin(th) * sp.cos(ph), sp.sin(th) * sp.sin(ph), sp.cos(th)]
flux_int = sp.simplify(sum(mue * g.subs(sub) * n for g, n in zip(gradA, nvec)) * R0**2 * sp.sin(th))
for Lv in (0.1953, 0.2389):
    f = sp.lambdify(th, flux_int.subs({L: Lv, mue: 0.9, G: 1, M: 1, R0: 1.7, ph: 0}), "numpy")
    tt = np.linspace(0, np.pi, 200001)
    val = 2 * np.pi * np.trapezoid(f(tt), tt)
    print(f"  AQUAL flux (L={Lv}) / (4 pi G M) = {val / (4 * np.pi):.6f}  (must be 1)")

# ---- 1d. QUMOND EFE-dominated solution: nabla^2 Phi = nu_e [nabla^2 phiN + K0 d_z^2 phiN]
phiN = -G * M / r
phiQ = -(G * M * nue / r) * (1 + (K0 / 2) * sin2)
lhs = sp.diff(phiQ, X, 2) + sp.diff(phiQ, Y, 2) + sp.diff(phiQ, Z, 2)
rhs = nue * K0 * sp.diff(phiN, Z, 2)          # nabla^2 phiN = 0 for r != 0
print("QUMOND: nabla^2 Phi - nu_e K0 d_z^2 phiN (r != 0) =", sp.simplify(lhs - rhs))

# ---- 1e. angular factor of the radial force / v_c^2 = r dPhi/dr, theta=0 vs 90 deg
# both forms are homogeneous of degree -1 in r, so r*g_r = -Phi; ratio(0)/ratio(90):
for nm, Lv in (("claimed x_e=1.8", float(Ke.subs(x, 1.8))),):
    print(f"  {nm}: AQUAL v_c^2(0)/v_c^2(90) = sqrt(1+K_e) = {np.sqrt(1+Lv):.5f}")

# ---- 1f. reproduce Banik & Zhao 2018 Table 3 (standard function): v_c=232.8 km/s, R=8.2 kpc
from scipy import constants as C
kpc = 1e3 * C.parsec
gext = (232.8e3) ** 2 / (8.2 * kpc)
for a0 in (1.2e-10,):
    xe = gext / a0
    me = xe / np.sqrt(1 + xe**2); Le = 1 / (1 + xe**2); Kq = -Le / (1 + Le)
    etaQ = (1 / me) * (1 + Kq / 3)
    etaA = (1 / me) * np.arctan(np.sqrt(Le)) / np.sqrt(Le)
    print(f"B&Z setup: g_ext={gext:.4e}  a0={a0:.3e}  x_e={xe:.4f}  nu_ext=1/mu={1/me:.4f} (B&Z 1.1462)"
          f"  L0={Le:.4f}  K0={Kq:.4f}  eta_QUMOND={etaQ:.4f} (1.0726)  eta_AQUAL={etaA:.4f} (1.0661)")
