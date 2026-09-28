#!/usr/bin/env python3
"""Stage 1 of the dwarf-in-a-wind problem (D7 drag dilemma): steady linear response of the FULL constrained AeST system
(metric in de Donder gauge, aether, scalar) to a source moving at speed v through a local deep-MOND background.
The background is a dSph at x = g/a0t = 0.05 (J' = x/sqrt(1+x^2), 2YJ'' = x(1+x^2)^-3/2). The MOND-field lift
2 lap(phi) |grad Lambda|^2 of the static zero mode (D3 note 7 sec.23) is represented by the Q-offset lift at the same
strength, qbar = lap(phi)/(K2 Q0), lap(phi) = v_f^2/r^2, k = 1/r (sec.26 method). Diagnostics, per unit source:
  S_z   = i k phi + Qbar (u_z + h0z)   the MOND-channel quantity: nonzero on the held branch, zero on the dragged branch
  h00   the potential response
Held-branch prediction (sec.26): the MOND channel survives only for v < C v_f, with C = 0.270 (par) or 0.192 (perp)."""
import sys, pickle, sympy as sp, mpmath as mp
mp.mp.dps = 80
DIR = sys.argv[1] if len(sys.argv) > 1 else "par"
M, b, names, (qb, Jp, Jl, g, k, w, vs, Rs), (KB, K2, Q0) = pickle.load(open(f"mond_bg_source_{DIR}_K275.pkl", "rb"))
pars = (qb, Jp, Jl, g, k, w, vs, Rs)
fM = sp.lambdify(pars, M, "mpmath"); fb = sp.lambdify(pars, b, "mpmath")
ix = {n: i for i, n in enumerate(names)}
c_kms = mp.mpf(299792.458)
x = mp.mpf("0.05"); Jpv = x / mp.sqrt(1 + x * x); Jlv = x * (1 + x * x) ** mp.mpf(-1.5)
a0t = 2 * mp.mpf("3.577e-5"); gv = x * a0t                        # Mpc^-1 (c = 1)
vf = mp.mpf(10) / c_kms; r = mp.mpf("3e-4")                       # dSph: v_f = 10 km/s, r = 0.3 kpc
kv = 1 / r; lap = vf ** 2 / r ** 2; qv = lap / (mp.mpf(K2) * mp.mpf(Q0))
C = mp.mpf("0.270") if DIR == "par" else mp.mpf("0.192")
print(f"{DIR}: x={float(x)}, k={float(kv):.0f}/Mpc, lap(phi)={float(lap):.3e}/Mpc^2, qbar={float(qv):.3e}/Mpc, predicted v_hold = C v_f = {float(C*10):.2f} km/s")
def solve(v_kms):
    v = mp.mpf(v_kms) / c_kms
    args = (qv, Jpv, Jlv, gv, kv, kv * v, v, 1)
    X = mp.lu_solve(mp.matrix(fM(*args)), mp.matrix(fb(*args)))
    Qb = mp.mpf(Q0) + qv
    Sz = 1j * kv * X[ix["phi"]] + Qb * (X[ix["uz"]] + X[ix["h0z"]])
    return Sz, X[ix["h00"]]
S0, h0 = solve(mp.mpf("1e-4"))
print(f"{'v [km/s]':>10s} {'|S_z|/|S_z(v->0)|':>18s} {'h00/h00(v->0)':>16s}")
for v in ["0.01", "0.1", "0.3", "1", "2", "3", "5", "10", "30", "100", "300", "1000"]:
    Sz, h00 = solve(v)
    print(f"{float(v):10.2f} {float(abs(Sz)/abs(S0)):18.4e} {mp.nstr(mp.re(h00/h0), 8):>16s}")
