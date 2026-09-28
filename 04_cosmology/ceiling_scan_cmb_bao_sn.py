#!/usr/bin/env python3
"""Profile chi2(Omega_f) for the dark-energy ceiling model under Planck distance priors + DESI DR2 BAO + Pantheon+,
re-minimizing (h, omega_b) at each ceiling, for approach exponents n = 1 and n = 2 (see ceiling_model_cmb_bao_sn.py).
Usage: ceiling_scan_cmb_bao_sn.py --bao-mean M --bao-cov C --dat D --cov V"""
import argparse, json, sys
import numpy as np
from scipy.optimize import minimize
import ceiling_model_cmb_bao_sn as m
from ceiling_model_bao_sn import load_bao
from omega_ln2_pantheonplus import load_data, official_mask, load_cov, chi2_marginalized

def main():
    ap = argparse.ArgumentParser()
    for k in ("--bao-mean", "--bao-cov", "--dat", "--cov"): ap.add_argument(k, required=True)
    ap.add_argument("--out", default="CEILING_SCAN_CMB_BAO_SN.json"); args = ap.parse_args()
    zb, db, qb, Cb = load_bao(args.bao_mean, args.bao_cov); Cbi = np.linalg.inv(Cb)
    zhel_all, zhd_all, mb_all = load_data(args.dat); ww = official_mask(zhd_all)
    zhel, zhd, mb = zhel_all[ww], zhd_all[ww], mb_all[ww]; sinv = np.linalg.inv(load_cov(args.cov)[np.ix_(ww, ww)])
    zsn = np.linspace(0, float(zhd.max()) * 1.0000001, 200001)
    def chi_sn(E):
        ez = E(zsn); dc = np.concatenate(([0.0], np.cumsum((1 / ez)[1:] + (1 / ez)[:-1]) * 0.5 * np.diff(zsn)))
        return chi2_marginalized(mb, 5 * np.log10((1 + zhel) * np.interp(zhd, zsn, dc)) + 25.0, sinv)
    def chi_bao(E, h, om0, ob):
        rd = m.rd_mpc(ob, om0 * h**2); dh0 = m.CKMS / (100 * h)
        DM = m.dm_over(E, zb) * dh0 / rd; DH = dh0 / E(zb) / rd; DV = (zb * DM**2 * DH)**(1 / 3)
        pred = np.array([{"DM_over_rs": DM[i], "DH_over_rs": DH[i], "DV_over_rs": DV[i]}[qb[i]] for i in range(len(zb))])
        r = db - pred; return float(r @ Cbi @ r)
    def tot(p, of, n):
        h, ob = p
        if not (0.5 < h < 0.9 and 0.015 < ob < 0.03): return 3e9
        E, om0 = m.make_E("ceil", h, None, of, n)
        return m.cmb_chi2(E, h, om0, ob)[0] + chi_bao(E, h, om0, ob) + chi_sn(E)
    out = {}
    for n in (1.0, 2.0):
        ofs = np.round(np.concatenate([np.arange(0.90, 0.99, 0.005), [0.9539392, 0.992, 0.995, 0.998]]), 7); ofs.sort()
        rows = []; start = [0.68, 0.0225]
        for of in ofs:
            r = minimize(lambda p: tot(p, of, n), start, method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-4, "maxiter": 3000})
            start = list(r.x); rows.append((float(of), float(r.fun), float(r.x[0]), float(r.x[1])))
            print(f"n={n} Omega_f={of:.4f} chi2={r.fun:.3f} h={r.x[0]:.4f}", flush=True)
        c = np.array([x[1] for x in rows]); j = int(np.argmin(c)); sel = [x[0] for x in rows if x[1] - c[j] <= 1.0]
        k = [x for x in rows if abs(x[0] - 0.9539392) < 1e-6][0]
        out[f"n={n}"] = {"grid": rows, "omega_f_best": rows[j][0], "chi2_best": rows[j][1], "omega_f_1sigma": [min(sel), max(sel)],
                         "chi2_at_kappa": k[1], "delta_chi2_kappa_vs_best": k[1] - rows[j][1]}
    json.dump(out, open(args.out, "w"), indent=2)
    print(json.dumps({kk: {x: v for x, v in vv.items() if x != "grid"} for kk, vv in out.items()}, indent=2))

if __name__ == "__main__":
    main()
