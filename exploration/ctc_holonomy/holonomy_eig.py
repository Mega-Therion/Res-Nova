#!/usr/bin/env python3
"""PREP (stage 2): parallel-transport holonomy around a Godel phi-circle.

Transports a vector around a closed phi-loop at fixed (t, r, z) and returns the
holonomy matrix U_gamma in SO(1,3). Then asks the only question that matters:

    is U_gamma an involution (U^2 = 1)?

  involution      -> orientation carries no information; the arrow is NOT here
  not involution  -> forward and backward traversal are different operations

Run below, at, and above the CTC threshold sinh(r) = 1 so the answer is a
function of causal character rather than a single sample.
"""
import numpy as np, sympy as sp

t, r, phi, z, a = sp.symbols('t r phi z a', real=True, positive=True)
coords = [t, r, phi, z]
s = sp.sinh(r)

g = sp.Matrix([
    [-4*a**2,        0,      4*sp.sqrt(2)*a**2*s**2, 0],
    [0,         4*a**2,      0,                      0],
    [4*sp.sqrt(2)*a**2*s**2, 0, -4*a**2*(s**4 - s**2), 0],
    [0,              0,      0,                  4*a**2]])

ginv = g.inv()

def christoffel():
    G = [[[0]*4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                e = 0
                for k in range(4):
                    e += ginv[l,k]*(sp.diff(g[k,m],coords[n])
                                   +sp.diff(g[k,n],coords[m])
                                   -sp.diff(g[m,n],coords[k]))
                G[l][m][n] = sp.simplify(e/2)
    return G

print("computing Christoffel symbols...", flush=True)
G = christoffel()
nz = [(l,m,n) for l in range(4) for m in range(4) for n in range(4) if G[l][m][n] != 0]
print("non-zero components:", len(nz))
for l,m,n in nz:
    print(f"  Gamma^{coords[l]}_{{{coords[m]}{coords[n]}}} = {G[l][m][n]}")

# Transport equation along phi:  dV^l/dphi = -Gamma^l_{m phi} V^m
# So V(2pi) = exp(-2*pi*M) V(0) with M^l_m = Gamma^l_{m phi}, evaluated at fixed r.
M = sp.zeros(4,4)
for l in range(4):
    for m in range(4):
        M[l,m] = G[l][m][2]
print("\ntransport generator M^l_m = Gamma^l_{m phi}:")
sp.pprint(sp.simplify(M))

import scipy.linalg as la
print("\n=== holonomy U = exp(-2*pi*M) around the phi-circle ===")
print(f"{'r':>8} {'sinh r':>9} {'character':>16} {'||U^2 - I||':>13}  involution?")
for rv in [0.4, 0.7, float(sp.asinh(1)), 1.1, 1.5, 2.0]:
    Mn = np.array(sp.matrix2numpy(M.subs({r: rv, a: 1}), dtype=float))
    U  = la.expm(-2*np.pi*Mn)
    d  = np.linalg.norm(U @ U - np.eye(4))
    sh = float(sp.sinh(rv))
    ch = "spacelike" if sh < 1 else ("NULL" if abs(sh-1) < 1e-9 else "CTC (timelike)")
    print(f"{rv:8.4f} {sh:9.4f} {ch:>16} {d:13.6e}  {'YES' if d < 1e-9 else 'NO'}")
    np.save(f"U_r{rv:.3f}.npy", U)
    ev=np.linalg.eigvals(Mn)
    boost = np.any(np.abs(ev.real)>1e-9)
    print(f"        generator eigenvalues {np.round(ev,4)}  -> {'BOOST-like (real parts nonzero)' if boost else 'pure rotation'}")
