#!/usr/bin/env python3
"""verify_sawtooth.py -- independent check of the #257 sawtooth claim: verbatim xcop_screened_full.py model,
plain np.gradient (no polynomial), damped fixed point, convergence on max|dS| AND R200.
Optional Cosh source (r_cosh finite). Usage: verify_sawtooth.py NAME N ALPHA [r_cosh] [maxit] [static|capped]
Env SINIT=file.npz (rr, S) starts from a given screen profile (e.g. from verify_smooth_profile.py).
Env BRANCH=connected selects the BVP root continuous with the r = inf control (Cosh has two roots at r = 1e-4)."""
import json, math, importlib.util, os, sys
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
XC = os.path.dirname(os.path.abspath(__file__))
os.chdir(XC)
D = "../../02_galaxy_dynamics/clusters/"; cwd = os.getcwd(); os.chdir(D)
spec = importlib.util.spec_from_file_location("cm", "cluster_mond_test.py"); cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
os.chdir(cwd)
MPC, G, MS = cm.MPC_M, cm.G_SI, cm.MSUN; MU0 = 1.0 / (0.9895 * MPC); C2 = 299792458.0**2
law = lambda u: cm.g_mond(max(u, 0.0))
XHLOW = 154.0; Om = 0.315; H0 = 67.4e3 / MPC
Hz = lambda z: H0 * math.sqrt(Om * (1 + z) ** 3 + 1 - Om)
NAME, N, ALPHA = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
RC = float(sys.argv[4]) if len(sys.argv) > 4 else float("inf")
MAXIT = int(sys.argv[5]) if len(sys.argv) > 5 else 60
MODE = sys.argv[6] if len(sys.argv) > 6 else "static"
rows_in = [l.split("\t") for l in open("xcop_data.tsv") if not l.startswith("#") and l.strip()]
def shape_mass(x, xc, beta):
    return quad(lambda r: r**2 * (1 + (r / xc) ** 2) ** (-1.5 * beta), 0, x, limit=200)[0]
row = next(r for r in rows_in if r[0] == NAME)
nm, z, R5, R2, MH5, MH2, f5, f2, Mt5, Mt2 = row
z, R5, R2 = float(z), float(R5) * MPC, float(R2) * MPC
Mg5 = float(f5) * float(MH5) * 1e14 * MS; Mg2 = float(f2) * float(MH2) * 1e14 * MS
Mt5, Mt2 = float(Mt5) * 1e14 * MS, float(Mt2) * 1e14 * MS
xc = 0.1; x2 = R2 / R5; target = Mg2 / Mg5
beta = brentq(lambda b: shape_mass(x2, xc, b) / shape_mass(1.0, xc, b) - target, 0.3, 3.0)
rv = R2 * (200 / 177.8) ** (1 / 3); rc = xc * R5
A = 1.09 * Mg5 / (4 * math.pi * R5**3 * shape_mass(1.0, xc, beta))
rho = lambda r: A * (1 + (r / rc) ** 2) ** (-1.5 * beta)
rg = np.linspace(0, rv, 4001); Mb_g = np.concatenate([[0], np.cumsum(0.5 * (4 * math.pi * rg[1:] ** 2 * rho(rg[1:]) + 4 * math.pi * rg[:-1] ** 2 * rho(rg[:-1])) * np.diff(rg))])
Mb = lambda r: np.interp(r, rg, Mb_g)
PHIC = C2 * RC
dust = (lambda P: -P) if math.isinf(RC) else (lambda P: PHIC * math.sinh(max(min(-P / PHIC, 700.0), -700.0)))
STAB = [np.array([0.0, 1e30]), np.array([1.0, 1.0])]
def solve(mu):
    rmin = 1e-4 * R5
    Sx = lambda r: float(np.interp(r, STAB[0], STAB[1]))
    glaw = lambda u, r: u + Sx(r) * (law(u) - u)
    rhs = lambda r, y: [G * 4 * math.pi * r**2 * rho(r) + mu**2 * r**2 * dust(y[1]), glaw(y[0] / r**2, r)]
    def shoot(P0, full=False):
        s = solve_ivp(rhs, (rmin, rv), [G * Mb(rmin), P0], method="DOP853", rtol=1e-8, atol=[1e21, 1.0], dense_output=full)
        if not s.success: return float("nan") if not full else None
        return s if full else s.y[1, -1]
    g0 = -law(G * Mb(R5) / R5**2) * rv * 3
    grid = np.linspace(-6 * abs(g0), 2 * abs(g0), 41); F = [shoot(p) for p in grid]
    idx = [i for i in range(40) if np.isfinite(F[i]) and np.isfinite(F[i+1]) and F[i] * F[i + 1] < 0]
    # BRANCH=connected takes the least-negative root (the branch continuous with r = inf); default = original first-root rule
    i = (idx[-1] if os.environ.get("BRANCH") == "connected" else idx[0]) if idx else None
    if i is None: return None
    s = shoot(brentq(shoot, grid[i], grid[i + 1], xtol=1e-6 * abs(g0)), True)
    Md = lambda r: glaw(s.sol(r)[0] / r**2, r) * r**2 / G
    rr = np.linspace(1e-3 * R5, rv, N); gt = np.array([glaw(s.sol(x)[0] / x**2, x) for x in rr])
    return Mt5 / Md(R5), Mt2 / Md(R2), ((s.sol(rv)[0] - G * Mb(rv)) / G) / (5.36 * Mb(rv)), rr, gt
def iterate(mu, verbose=False):
    STAB[0], STAB[1] = np.array([0.0, 1e30]), np.array([1.0, 1.0]); S = None; hist = []
    if os.environ.get("SINIT"):
        z0 = np.load(os.environ["SINIT"]); rr0 = np.linspace(1e-3 * R5, rv, N)
        S = np.interp(rr0, z0["rr"], z0["S"]); STAB[0], STAB[1] = rr0, S
    for it in range(MAXIT):
        o = solve(mu)
        if o is None: return None
        a5, a2, dr, rr, gt = o
        gp = np.gradient(gt, rr); xh = np.sqrt(gp**2 + 2 * (gt / rr) ** 2) / Hz(z) ** 2
        Sraw = 1 / (1 + (XHLOW / xh) ** 2)
        Snew = Sraw if S is None else (1 - ALPHA) * S + ALPHA * Sraw
        dS = 1.0 if S is None else float(np.max(np.abs(Snew - S)))
        S = Snew; STAB[0], STAB[1] = rr, S
        hist.append((it, a5, a2, dS, float(np.max(np.abs(Sraw - S)))))
        if verbose: print(f"  it={it:2d} R500={a5:.4f} R200={a2:.4f} max|dS|={dS:.2e} raw_resid={hist[-1][4]:.2e} jump={np.max(np.abs(np.diff(S))):.3f}", flush=True)
        if it >= 3 and dS < 1e-4 and abs(hist[-1][2] - hist[-2][2]) < 1e-4: break
    o = solve(mu)
    a5, a2, dr, rr, gt = o
    gp = np.gradient(gt, rr); xh = np.sqrt(gp**2 + 2 * (gt / rr) ** 2) / Hz(z) ** 2
    resid = float(np.max(np.abs(1 / (1 + (XHLOW / xh) ** 2) - S)[2:-2]))
    return dict(R500=a5, R200=a2, dust=dr, iters=len(hist), last_dS=hist[-1][3], fp_resid=resid, jump=float(np.max(np.abs(np.diff(S)))))
st = iterate(MU0, verbose=(MODE == "static"))
out = dict(name=NAME, N=N, alpha=ALPHA, r_cosh=RC, static=st)
if MODE == "capped" and st is not None and st["dust"] > 1:
    sc = brentq(lambda s: (iterate(MU0 * s) or {"dust": float("nan")})["dust"] - 1.0, 1e-3, 1.0, xtol=1e-3)
    out["sc"] = sc; out["capped"] = iterate(MU0 * sc)
elif MODE == "capped":
    out["sc"] = 1.0; out["capped"] = st
print(json.dumps(out))
