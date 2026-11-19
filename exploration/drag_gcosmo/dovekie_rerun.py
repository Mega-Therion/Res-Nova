#!/usr/bin/env python3
"""POST-HOC robustness check (not pre-registered as decisive): replace Pantheon+ with DES-Dovekie (DES 5yr recalibrated,
full inverse STAT+SYS covariance) and refit LCDM, drag and CPL on DESI DR2 BAO + SN + compressed CMB."""
import json, math, sys
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, "../../04_cosmology")
import cosmo_data as cd
from desy5_ceiling import read_snana, load_inv_cov
import drag_fit
from drag_fit import zg, bz, bv, bq, bcinv, C
from scipy.integrate import cumulative_trapezoid
H = read_snana(cd.path("desy5_hd"))
zhd, zhel, mu_obs = (np.array(H[k], float) for k in ("zHD", "zHEL", "MU"))
W = load_inv_cov(cd.path("desy5_inv")); one = np.ones(len(zhd)); w11 = one @ W @ one
def chi2(Efun, h, Om):
    Ez = Efun(zg)
    if not np.all(np.isfinite(Ez)) or np.any(Ez <= 0): return 1e12
    DM = cumulative_trapezoid(1 / Ez, zg, initial=0) * C / (100 * h)
    wm = Om * h**2; fac = (wm / 0.1430) ** -0.255; rd = 147.09 * fac; rs = 144.43 * fac
    dm = np.interp(bz, zg, DM); dh = C / (100 * h * np.interp(bz, zg, Ez))
    mod = np.array([(z * a**2 * b) ** (1 / 3) / rd if q == "DV_over_rs" else (a / rd if q == "DM_over_rs" else b / rd)
                    for z, a, b, q in zip(bz, dm, dh, bq)])
    r = bv - mod; cb = r @ bcinv @ r
    dl = mu_obs - (5 * np.log10(np.interp(zhd, zg, DM) * (1 + zhel)) + 25)
    cs = dl @ W @ dl - (one @ W @ dl) ** 2 / w11
    th = 100 * rs / np.interp(1089.9, zg, DM)
    return cb + cs + ((th - 1.04110) / 0.00031) ** 2 + ((wm - 0.1430) / 0.0011) ** 2
def E_drag(h, Om, x0): return lambda z: drag_fit.E(z, h, Om, x0)
def E_cpl(h, Om, w0, wa):
    def f(z):
        a = 1 / (1 + z); Or = drag_fit.ORH2 / h**2; OL = 1 - Om - Or
        return np.sqrt(Om / a**3 + Or / a**4 + OL * a ** (-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a)))
    return f
def best(fun, starts):
    rs = [minimize(fun, s, method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-4, "maxiter": 8000}) for s in starts]
    r = min(rs, key=lambda r: r.fun); return float(r.fun), [float(v) for v in r.x]
ok = lambda h, Om: 0.5 < h < 0.9 and 0.1 < Om < 0.6
lc = best(lambda q: chi2(E_drag(q[0], q[1], 0.0), q[0], q[1]) if ok(*q) else 1e12, [[0.68, 0.31]])
dg = best(lambda q: chi2(E_drag(*q), q[0], q[1]) if ok(q[0], q[1]) and -0.9 < q[2] < 3 else 1e12,
          [[0.68, 0.31, 0.05], [0.68, 0.31, 0.3], [0.68, 0.31, 0.8]])
cp = best(lambda q: chi2(E_cpl(*q), q[0], q[1]) if ok(q[0], q[1]) else 1e12,
          [[0.68, 0.31, -0.9, -0.5], [0.68, 0.31, -1.0, 0.0], [0.68, 0.31, -0.7, -1.0]])
prof = []
for x in np.arange(0.0, 1.55, 0.05):
    prof.append((float(x), best(lambda q: chi2(E_drag(q[0], q[1], x), q[0], q[1]) if ok(*q) else 1e12, [[0.68, 0.31]])[0]))
px = np.array(prof); d = px[:, 1] - dg[0]
xs = [float(px[i, 0] + (4 - d[i]) * (px[i + 1, 0] - px[i, 0]) / (d[i + 1] - d[i])) for i in range(len(px) - 1) if (d[i] - 4) * (d[i + 1] - 4) < 0]
out = {"label": "POST-HOC: DES-Dovekie in place of Pantheon+", "N_SN": int(len(zhd)),
       "LCDM": {"chi2": lc[0], "h_Om": lc[1]}, "drag": {"chi2": dg[0], "h_Om_x0": dg[1], "dchi2": dg[0] - lc[0],
       "x0_2sigma": xs, "Gcosmo_GN_today": 1 / (1 + dg[1][2])},
       "CPL": {"chi2": cp[0], "h_Om_w0_wa": cp[1], "dchi2": cp[0] - lc[0]},
       "pantheon_plus_reference": {"drag_dchi2": -6.54, "x0": 0.32, "CPL_dchi2": -9.17}}
print(json.dumps(out, indent=1)); json.dump(out, open("DOVEKIE_RERUN.json", "w"), indent=1)
