#!/usr/bin/env python3
"""Convergence of sup_{x,t} coherence at fixed alpha as the L1 time step shrinks (T=20),
plus a T=40 check. alpha* is only reportable if sup(alpha) converges in N."""
from math import sqrt
from scipy.optimize import minimize_scalar
from pillar_iv_fractional_gksl import liouvillian, evolve
theta = 1 / sqrt(2)
def supc(alpha, N, T=20.0):
    f = lambda x: -evolve(liouvillian(x, 1.0), alpha, T, N)[1].max()
    r = minimize_scalar(f, bounds=(0.4, 3.0), method="bounded", options={"xatol": 1e-3})
    return -r.fun, r.x
for a in (0.65, 0.70, 0.75):
    for N in (800, 1600, 3200, 6400):
        s, x = supc(a, N)
        print(f"alpha={a:.2f} N={N:5d} h={20/N:.4f} sup={s:.5f} x*={x:.3f} sup-theta={s-theta:+.5f}", flush=True)
s, x = supc(0.70, 6400, 40.0); print(f"alpha=0.70 T=40 N=6400 sup={s:.5f} x*={x:.3f}", flush=True)
