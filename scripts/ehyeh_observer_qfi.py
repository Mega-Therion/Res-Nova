#!/usr/bin/env python3
"""Quantum Fisher information of the exact Pillar IV steady-state family (mechanism A of
EHYEH_AUDIT_AND_SALVAGE_SKETCH_2026-11-05.md).

Input: the steady state of PILLAR_IV_MU_IDENTITY_2026-10-13.md (H = u sigma_x, jump sigma_- at
rate gamma, x = u/gamma, mu = mu_std(2 sqrt2 x)): Bloch vector r = (0, -sqrt2 mu sqrt(1-mu^2), 1-mu^2).

Checks (exit 0 when all pass):
  Q1  the qubit QFI  F = |dr|^2 + (r.dr)^2/(1-|r|^2)  equals 16/(1+8x^2)^2 exactly
  Q2  F = 16 (1 - mu^2)^2                                  (the same, written in mu_std)
  Q3  theta = sqrt2 * atan(2 sqrt2 x) has (dtheta/dx)^2 = F: in theta the Fisher kinetic term
      F(x)(dx)^2 is a free massless scalar on [0, pi/sqrt2)
  Q4  symbolic F agrees with a density-matrix QFI by finite differences at four points
"""
import sys

import sympy as sp

x = sp.symbols("x", positive=True)
y = 2 * sp.sqrt(2) * x
mu = y / sp.sqrt(1 + y**2)
r = sp.Matrix([0, -sp.sqrt(2) * mu * sp.sqrt(1 - mu**2), 1 - mu**2])
dr = r.diff(x)
F = sp.simplify(dr.dot(dr) + r.dot(dr) ** 2 / (1 - r.dot(r)))

fails = 0


def check(ok, label):
    global fails
    print(("PASS " if ok else "FAIL ") + label)
    fails += 0 if ok else 1


check(sp.simplify(F - 16 / (1 + 8 * x**2) ** 2) == 0, "Q1 F(x) = 16/(1+8x^2)^2")
check(sp.simplify(F - 16 * (1 - mu**2) ** 2) == 0, "Q2 F = 16 (1 - mu_std(2 sqrt2 x)^2)^2")
theta = sp.sqrt(2) * sp.atan(2 * sp.sqrt(2) * x)
check(sp.simplify(sp.diff(theta, x) ** 2 - F) == 0, "Q3 (dtheta/dx)^2 = F with theta = sqrt2 atan(2 sqrt2 x)")


def rho(xv):
    m = float(mu.subs(x, xv))
    c = m * (1 - m * m) ** 0.5 / 2**0.5
    return [[1 - m * m / 2, 1j * c], [-1j * c, m * m / 2]]


def qfi_numeric(xv, h=1e-6):
    import cmath

    a, b = rho(xv - h), rho(xv + h)
    R = rho(xv)
    dR = [[(b[i][j] - a[i][j]) / (2 * h) for j in range(2)] for i in range(2)]
    # 2x2 Hermitian eigen-decomposition by hand
    tr = (R[0][0] + R[1][1]).real
    det = (R[0][0] * R[1][1] - R[0][1] * R[1][0]).real
    disc = cmath.sqrt(tr * tr / 4 - det).real
    lam = [tr / 2 + disc, tr / 2 - disc]
    vecs = []
    for L in lam:
        v = [R[0][1], L - R[0][0]] if abs(R[0][1]) > 1e-15 else [1, 0]
        n = (abs(v[0]) ** 2 + abs(v[1]) ** 2) ** 0.5
        vecs.append([v[0] / n, v[1] / n])
    s = 0.0
    for i in range(2):
        for j in range(2):
            if lam[i] + lam[j] > 1e-14:
                vi, vj = vecs[i], vecs[j]
                el = sum(vi[k].conjugate() * dR[k][l] * vj[l] for k in range(2) for l in range(2))
                s += 2 * abs(el) ** 2 / (lam[i] + lam[j])
    return s


worst = max(abs(qfi_numeric(v) - float(F.subs(x, v))) / float(F.subs(x, v)) for v in (0.1, 0.5, 1.0, 3.0))
check(worst < 1e-5, f"Q4 density-matrix QFI matches the closed form (max relative difference {worst:.1e})")
print(f"F(x) = {sp.factor(F)}")
sys.exit(1 if fails else 0)
