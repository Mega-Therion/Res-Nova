#!/usr/bin/env python3
"""Drag variable-G cosmology vs LCDM on DESI DR2 BAO + Pantheon+ + compressed CMB, then + fsigma8. See PREREG.md."""
import json, math, sys
import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.optimize import minimize
sys.path.insert(0, "../../04_cosmology")
from omega_ln2_pantheonplus import load_data, official_mask, load_cov
C = 299792.458; ORH2 = 4.18e-5
ED = "../../04_cosmology/external_data/"
bao = [l.split() for l in open(ED + "desi_gaussian_bao_ALL_GCcomb_mean.txt") if not l.startswith("#")]
bz = np.array([float(b[0]) for b in bao]); bv = np.array([float(b[1]) for b in bao]); bq = [b[2] for b in bao]
bcinv = np.linalg.inv(np.loadtxt(ED + "desi_gaussian_bao_ALL_GCcomb_cov.txt"))
zhel, zhd, mb = load_data(ED + "Pantheon+SH0ES.dat"); m = official_mask(zhd)
cov = load_cov(ED + "Pantheon+SH0ES_STAT+SYS.cov")[np.ix_(m, m)]; scinv = np.linalg.inv(cov)
zhel, zhd, mb = zhel[m], zhd[m], mb[m]; s_one = scinv.sum()
FS = np.array([[0.02,0.428,0.0465],[0.02,0.398,0.065],[0.02,0.314,0.048],[0.10,0.370,0.130],[0.15,0.490,0.145],
 [0.17,0.510,0.060],[0.18,0.360,0.090],[0.38,0.440,0.060],[0.25,0.3512,0.0583],[0.37,0.4602,0.0378],[0.32,0.384,0.095],
 [0.59,0.488,0.060],[0.44,0.413,0.080],[0.60,0.390,0.063],[0.73,0.437,0.072],[0.60,0.550,0.120],[0.86,0.400,0.110],
 [1.40,0.482,0.116],[0.978,0.379,0.176],[1.23,0.385,0.099],[1.526,0.342,0.070],[1.944,0.364,0.106]])
zg = np.concatenate([np.linspace(0, 3, 3001), np.linspace(3.01, 1100, 20000)])
def E(z, h, Om, x0):
    a = 1 / (1 + z); Or = ORH2 / h**2; OL = 1 + x0 - Om - Or
    return np.sqrt((Om / a**3 + Or / a**4 + OL) / (1 + x0 * a**2))
def dist(h, Om, x0):
    Ez = E(zg, h, Om, x0)
    if not np.all(np.isfinite(Ez)) or np.any(Ez <= 0): return None
    DM = cumulative_trapezoid(1 / Ez, zg, initial=0) * C / (100 * h); return Ez, DM
def chi2_bg(p):
    h, Om, x0 = p
    if not (0.5 < h < 0.9 and 0.1 < Om < 0.6 and -0.9 < x0 < 3): return 1e12
    d = dist(h, Om, x0)
    if d is None: return 1e12
    Ez, DM = d; wm = Om * h**2; fac = (wm / 0.1430) ** -0.255; rd = 147.09 * fac; rs = 144.43 * fac
    dm = np.interp(bz, zg, DM); dh = C / (100 * h * np.interp(bz, zg, Ez))
    mod = np.array([(z * dmi**2 * dhi) ** (1 / 3) / rd if q == "DV_over_rs" else (dmi / rd if q == "DM_over_rs" else dhi / rd)
                    for z, dmi, dhi, q in zip(bz, dm, dh, bq)])
    r = bv - mod; cb = r @ bcinv @ r
    mu = 5 * np.log10(np.interp(zhd, zg, DM) * (1 + zhel)) + 25; dl = mb - mu
    cs = dl @ scinv @ dl - (scinv @ dl).sum() ** 2 / s_one
    th = 100 * rs / np.interp(1089.9, zg, DM); cc = ((th - 1.04110) / 0.00031) ** 2 + ((wm - 0.1430) / 0.0011) ** 2
    return cb + cs + cc
def growth(h, Om, x0):
    def rhs(N, y):
        a = math.exp(N); z = 1 / a - 1; e = E(z, h, Om, x0); dz = 1e-5
        dlnE = -(math.log(E(z + dz, h, Om, x0)) - math.log(E(z - dz, h, Om, x0))) / (2 * dz) / a  # dlnE/dlna = -(1+z) dlnE/dz
        return [y[1], -(2 + dlnE) * y[1] + 1.5 * Om / a**3 / e**2 * y[0]]
    ai = 1e-3; s = solve_ivp(rhs, (math.log(ai), 0), [ai, ai], dense_output=True, rtol=1e-6, atol=1e-10)
    return s
def fs8_model(h, Om, x0, s8_anchor=True):
    s = growth(h, Om, x0)
    D1 = s.sol(0)[0]; s80 = 0.811 * D1 / REF_D1
    out = []
    for z in FS[:, 0]:
        D, Dp = s.sol(math.log(1 / (1 + z))); out.append(s80 * Dp / D1)   # f sigma8 = sigma8_0 * dD/dlna / D(1)
    return np.array(out)
REF_D1 = growth(0.6736, 0.3153, 0.0).sol(0)[0]
def chi2_fs(p, anchor):
    f = fs8_model(*p)
    if anchor: return float(np.sum(((FS[:, 1] - f) / FS[:, 2]) ** 2)), 1.0
    w = 1 / FS[:, 2] ** 2; A = np.sum(w * FS[:, 1] * f) / np.sum(w * f * f)
    return float(np.sum(((FS[:, 1] - A * f) / FS[:, 2]) ** 2)), float(A)
def fit(fix_x0=None, with_fs=None):
    def tot(q):
        p = (q[0], q[1], q[2] if fix_x0 is None else fix_x0); v = chi2_bg(p)
        if with_fs is not None and v < 1e11: v += chi2_fs(p, with_fs)[0]
        return v
    x0g = [0.68, 0.30] + ([0.0] if fix_x0 is None else [])
    best = None
    for start in (([0.68, 0.30, 0.05], [0.68, 0.30, 0.3], [0.68, 0.30, -0.1]) if fix_x0 is None else ([0.68, 0.30, 0.0],)):
        q0 = start[:2] + ([start[2]] if fix_x0 is None else [])
        r = minimize(tot, q0, method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-4, "maxiter": 4000})
        if best is None or r.fun < best.fun: best = r
    p = (best.x[0], best.x[1], best.x[2] if fix_x0 is None else fix_x0)
    return float(best.fun), [float(v) for v in p]
def main():
    out = {}
    for label, wf in (("BAO+SN+CMB", None), ("+fs8_anchored", True), ("+fs8_free_amp", False)):
        cl, pl = fit(fix_x0=0.0, with_fs=wf); cd, pd = fit(with_fs=wf)
        prof = []
        for x in np.linspace(-0.3, 0.6, 19):
            prof.append((float(x), fit(fix_x0=x, with_fs=wf)[0]))
        px = np.array(prof); within = px[px[:, 1] <= cd + 4.0, 0]
        out[label] = {"chi2_LCDM": cl, "params_LCDM": pl, "chi2_drag": cd, "params_drag": pd, "dchi2": cd - cl,
                      "x0_2sigma": [float(within.min()), float(within.max())] if len(within) else None,
                      "Gcosmo_over_GN_today_best": 1 / (1 + pd[2]),
                      "Gcosmo_over_GN_today_2sigma": [1 / (1 + float(within.max())), 1 / (1 + float(within.min()))] if len(within) else None}
        if wf is not None:
            out[label]["fs8_chi2_LCDM"] = chi2_fs(pl, wf); out[label]["fs8_chi2_drag"] = chi2_fs(pd, wf)
        print(label, json.dumps(out[label]), flush=True)
    json.dump(out, open("DRAG_FIT.json", "w"), indent=1)

if __name__ == "__main__":
    main()
