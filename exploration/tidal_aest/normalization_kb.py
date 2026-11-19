#!/usr/bin/env python3
"""Item 1: normalisation against AeST's own weights (2026-11-19). [D] static, spherical, F = F(u) (Hessian/W terms
were verified separately in aest_qumond_metric.py).
AeST action (1/16piGt)[R - K_B F^2/2 + 2(2-K_B) J.grad(phi) - (2-K_B) Y - ...] in the static limit, in 1/8piGt units:
  L = rho Phi + (1/8piGt)[ Psi'^2 - 2Phi'Psi' + (K_B/2) Phi'^2 + (2-K_B) Phi'phi' - ((2-K_B)/2) phi'^2
                           + (2-K_B) phi'psi' + ((2-K_B)/2) a0^2 F(psi'^2/a0^2) ]
Claim: Psi = Phi;  psi' = -g_N;  Phi' = nu(g_N/a0) g_N with nu = 1 + F'(u);  G_N = Gt/(1 - K_B/2),
so G_cosmo/G_N = 1 - K_B/2 (G_cosmo = Gt for c1 + c3 = 0). AeST's own ratio m/(2n) = 1 is what makes this work."""
import sympy as sp
r, Gt, a0, KB = sp.symbols("r Gt a0 K_B", positive=True)
gN = sp.Function("gN")(r); Fp = sp.Function("Fp")                     # Fp = dF/du
u = gN**2 / a0**2
GN = Gt / (1 - KB / 2)
P1 = gN * (1 + Fp(u)); S1 = P1; ph1 = P1 - gN; ps1 = -gN               # first derivatives Phi', Psi', phi', psi'
rho = -sp.diff(r**2 * gN, r) / (4 * sp.pi * GN * r**2)        # +rho*Phi coupling => lap(Phi_N) = -4 pi G_N rho
k, m, n = KB / 2, 2 - KB, (2 - KB) / 2
# Euler-Lagrange in flux form: E_f = dL/df - d/dr(dL/df'), with L = r^2 * (...)
dL_dPhi1 = r**2 * (-2 * S1 + 2 * k * P1 + m * ph1) / (8 * sp.pi * Gt)
dL_dPsi1 = r**2 * (2 * S1 - 2 * P1) / (8 * sp.pi * Gt)
dL_dph1 = r**2 * (m * P1 - 2 * n * ph1 + 2 * n * ps1) / (8 * sp.pi * Gt)
dL_dps1 = r**2 * (2 * n * ph1 + n * a0**2 * Fp(u) * 2 * ps1 / a0**2) / (8 * sp.pi * Gt)
E = {"Phi": r**2 * rho - sp.diff(dL_dPhi1, r), "Psi": -sp.diff(dL_dPsi1, r),
     "phi": -sp.diff(dL_dph1, r), "psi": -sp.diff(dL_dps1, r)}
for kname, e in E.items():
    v = sp.simplify(e); print(f"{kname}-equation residual:", v); assert v == 0
print("G_N =", sp.simplify(GN), "; G_cosmo/G_N =", sp.simplify(Gt / GN))
