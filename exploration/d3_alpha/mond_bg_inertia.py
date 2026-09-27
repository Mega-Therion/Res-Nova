#!/usr/bin/env python3
"""Constrained zero-mode inertia in a local MOND-field background, from mond_bg_matrix.pkl.
Method: first-order degenerate perturbation theory -> omega^2 = V1 / T_c for any first-order lift V1.
Probe with a tiny Q-offset lift (V1_H = 2 K2 Q0 qbar k^2 per |Lambda|^2): s = d(omega^2)/d(qbar) = 2K2Q0 k^2/T_c.
Then the Laplacian (MOND-field) lift V1 = 2 Lap(phi) k^2 gives omega^2 = Lap(phi) * s/(K2 Q0); with
Lap(phi) = v_f^2/r^2 and k ~ 1/r:  held branch iff v_rel < C v_f,  C = sqrt(s/(K2 Q0)).
Frozen-metric reference: s_f = 2 K2 Q0 k^2/(K_B k^2 + 2 K2 Q0^2)  ->  C_f -> sqrt(2/K_B) at large k."""
import pickle, sympy as sp, mpmath as mp
mp.mp.dps = 100
import sys
DIR = sys.argv[1] if len(sys.argv) > 1 else "par"
M, (qb, Jp, Jl, g, k, w), (KBv, K2v, Q0v) = pickle.load(open(f"mond_bg_matrix_{DIR}_K275.pkl", "rb"))
R = sp.Rational
def zero_branch_w2(vals, kval, qval):
    # det(M(omega)) is a polynomial in omega of degree <= 2*N; recover its coefficients exactly-enough by
    # evaluating the numeric determinant at 2N+1 points on a circle (mpmath LU at the module dps) and inverting the DFT.
    Mn = M.subs(vals).subs({k: kval, qb: qval})
    f = sp.lambdify(w, Mn, modules="mpmath")
    N = Mn.shape[0]; D = 2 * N + 1; rad = mp.mpf(1)   # radius between the tiny zero-branch roots and the O(k) roots
    pts = [rad * mp.exp(2j * mp.pi * j / D) for j in range(D)]
    dets = [mp.det(mp.matrix(f(z))) for z in pts]
    cs = [sum(dets[j] * mp.exp(-2j * mp.pi * j * n / D) for j in range(D)) / D / rad**n for n in range(D)]
    cs = [mp.re(c) for c in cs]                       # real polynomial
    while abs(cs[-1]) < mp.mpf(10) ** -(mp.mp.dps - 10) * max(abs(c) for c in cs): cs.pop()
    roots = mp.polyroots(list(reversed(cs)), maxsteps=800, extraprec=800)
    r0 = min(roots, key=lambda r: abs(r))
    return r0 ** 2
def s_of(vals, kval, q1=R(1, 10**16), q2=R(2, 10**16)):
    return (zero_branch_w2(vals, kval, q2) - zero_branch_w2(vals, kval, q1)) / mp.mpf(float(q2 - q1))
base = {}          # parameter point baked into the matrix: K_B=1/2, K2=75, Q0=1/10
def report(label, vals, kval):
    s = s_of(vals, kval)
    K2f, Q0f, KBf = float(K2v), float(Q0v), float(KBv)
    sf = 2 * K2f * Q0f * kval**2 / (KBf * kval**2 + 2 * K2f * Q0f**2)
    C = mp.sqrt(s / (K2f * Q0f))
    print(f"{label:52s} k={kval:6d}  s={mp.nstr(s, 8):>28s}  s/s_frozen={mp.nstr(s/sf, 5):>22s}  C={mp.nstr(C, 4)}")
    return s
# validation: tracking regime (J' = lambda = 1, no longitudinal extra), vanishing background field
vv = dict(base); vv.update({Jp: 1, Jl: 0, g: R(1, 10**12)})
mu2 = 2 * 75 * R(1, 100) / R(3, 2); ks2 = 2 * mu2
for kval in (100, 1000):
    s = report("VALIDATION tracking (expect constrained formula)", vv, kval)
    pred = 75 * R(1, 10) * R(3, 2) * 1 * (kval**2 - ks2) / (R(5, 2) * kval**2 + R(3, 2) * 2 * mu2)
    print(f"{'':52s}           formula s = {float(pred):.8g}")
# deep-MOND local backgrounds: J' = lambda mu_std(x), 2Y J'' = lambda x (1+x^2)^-3/2, |grad phi| = x * a0tilde
a0t = 2 * 3.577e-5                                   # (1+lambda) a0 / c^2 in Mpc^-1, lambda = 1
for x in (0.3, 0.05):
    Jpv = x / (1 + x * x) ** 0.5; Jlv = x * (1 + x * x) ** -1.5; gv = x * a0t
    vv = dict(base); vv.update({Jp: sp.nsimplify(Jpv, rational=True), Jl: sp.nsimplify(Jlv, rational=True), g: sp.nsimplify(gv, rational=True)})
    for kval in (100, 1000):
        report(f"deep MOND x={x} (J'={Jpv:.3f}, 2YJ''={Jlv:.3f}), k {'||' if DIR=='par' else 'perp'} grad phi", vv, kval)
