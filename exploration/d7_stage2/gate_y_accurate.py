#!/usr/bin/env python3
"""Gate for solve_fe.y_accurate: it must equal local_derivs.val_Y exactly (same function, rearranged), so compare both
float64 evaluations against a 50-digit evaluation of val_Y at random jets of the solver's size (potentials ~1e-9,
gradients up to ~1e-5, aether up to 1e-4, external-field-sized F_z), for v = 0, 1e-4, 1e-3."""
import numpy as np, mpmath as mp
import local_derivs as LD
from solve_fe import y_accurate
mp.mp.dps = 50
src = open("local_derivs.py").read()
ns = {"sqrt": mp.sqrt}
exec(src[src.index("def val_Y("):].replace("np.sqrt", "sqrt"), ns)
rng = np.random.default_rng(20260928)
worst_acc = worst_gen = 0.0
for v in (0.0, 1e-4, 1e-3):
    for trial in range(200):
        q = np.zeros(30)
        for f in range(10):
            val, gr = (1e-4, 1e-4) if f in (7, 8) else (1e-9 * 10**rng.uniform(-2, 1), 1e-5 * 10**rng.uniform(-3, 0))
            q[3*f] = val*rng.standard_normal(); q[3*f+1:3*f+3] = gr*rng.standard_normal(2)
        if trial % 2: q[21] = q[24] = 0.0          # the held state: no aether tilt
        R = 1e-3*rng.uniform(0.01, 10)
        exact = ns["val_Y"]([mp.mpf(float(t)) for t in q], mp.mpf(R), mp.mpf(v))[0]
        ya = float(y_accurate([np.float64(t) for t in q], R, v))
        yg = float(LD.val_Y([np.float64(t) for t in q], R, v)[0])
        ea, eg = float(abs(ya-exact)/abs(exact)), float(abs(yg-exact)/abs(exact))
        worst_acc, worst_gen = max(worst_acc, ea), max(worst_gen, eg)
print(f"worst relative error against 50 digits: y_accurate {worst_acc:.2e}, generated val_Y {worst_gen:.2e}")
print(f"GATE Y-ACCURATE {'PASS' if worst_acc < 1e-12 else 'FAIL'}")
