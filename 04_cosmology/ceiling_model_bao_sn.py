#!/usr/bin/env python3
"""Dark-energy ceiling model vs DESI DR2 BAO and DESI BAO + Pantheon+ (late-time expansion shape; no CMB).
BAO: D_M/r_d, D_H/r_d, D_V/r_d all scale with alpha = c/(H0 r_d), which is marginalized analytically (profiled);
SN: absolute magnitude marginalized analytically (Pantheon+ likelihood of omega_ln2_pantheonplus.py).
So the ceiling model (share ln 2 today, logistic approach to Omega_f; ceiling_model_pantheonplus.py) has ZERO free
cosmological shape parameters at Omega_f = kappa; flat LCDM has one (Omega_m).
Data: DESI DR2 (arXiv:2503.14738) Gaussian BAO, CobayaSampler/bao_data desi_bao_dr2 ALL_GCcomb (not vendored).
Usage: ceiling_model_bao_sn.py --bao-mean M --bao-cov C --dat Pantheon+SH0ES.dat --cov Pantheon+SH0ES_STAT+SYS.cov"""
import argparse, json, math
import numpy as np
from omega_ln2_pantheonplus import load_data, official_mask, load_cov, chi2_marginalized
from ceiling_model_pantheonplus import E_lcdm, E_ceiling, mu_model, LN2, KAPPA

def load_bao(mean_path, cov_path):
    rows = [l.split() for l in open(mean_path) if l.strip() and not l.startswith("#")]
    z = np.array([float(r[0]) for r in rows]); d = np.array([float(r[1]) for r in rows]); q = [r[2] for r in rows]
    return z, d, q, np.loadtxt(cov_path)

def bao_shape(z, q, Efun):
    """Predictions divided by alpha = c/(H0 r_d): D_M, D_H, D_V in units of c/H0."""
    zs = np.linspace(0.0, float(z.max()) * 1.0001, 200001); ez = Efun(zs)
    dc = np.concatenate(([0.0], np.cumsum((1 / ez)[1:] + (1 / ez)[:-1]) * 0.5 * np.diff(zs)))
    DM = np.interp(z, zs, dc); DH = 1.0 / Efun(z); DV = (z * DM**2 * DH) ** (1.0 / 3.0)
    return np.array([{"DM_over_rs": DM[i], "DH_over_rs": DH[i], "DV_over_rs": DV[i]}[q[i]] for i in range(len(z))])

def chi2_bao(z, d, q, cinv, Efun):
    f = bao_shape(z, q, Efun); a = float(f @ cinv @ d) / float(f @ cinv @ f)     # profiled alpha
    r = d - a * f
    return float(r @ cinv @ r), a

def main():
    ap = argparse.ArgumentParser()
    for k in ("--bao-mean", "--bao-cov", "--dat", "--cov"): ap.add_argument(k, required=True)
    ap.add_argument("--out", default="CEILING_MODEL_BAO_SN.json"); args = ap.parse_args()
    z, d, q, C = load_bao(args.bao_mean, args.bao_cov); Cinv = np.linalg.inv(C)
    zhel_all, zhd_all, mb_all = load_data(args.dat); ww = official_mask(zhd_all)
    zhel, zhd, mb = zhel_all[ww], zhd_all[ww], mb_all[ww]
    sinv = np.linalg.inv(load_cov(args.cov)[np.ix_(ww, ww)])
    csn = lambda Ef: chi2_marginalized(mb, mu_model(zhd, zhel, Ef), sinv)
    cb = lambda Ef: chi2_bao(z, d, q, Cinv, Ef)[0]
    grid = np.round(np.arange(0.20, 0.45001, 0.001), 4)
    bao_l = np.array([cb(lambda zz, om=om: E_lcdm(zz, om)) for om in grid])
    sn_l = np.array([csn(lambda zz, om=om: E_lcdm(zz, om)) for om in grid])
    tot_l = bao_l + sn_l
    ib, it = int(np.argmin(bao_l)), int(np.argmin(tot_l))
    E_c = lambda zz: E_ceiling(zz, LN2, KAPPA); E_l2 = lambda zz: E_lcdm(zz, 1 - LN2)
    out = {"n_bao": int(len(d)), "n_sne": int(ww.sum()),
           "bao_only": {"lcdm_best_omega_m": float(grid[ib]), "lcdm_chi2": float(bao_l[ib]),
                        "ln2_lcdm_chi2": cb(E_l2), "ceiling_kappa_chi2": cb(E_c)},
           "bao_plus_sn": {"lcdm_best_omega_m": float(grid[it]), "lcdm_chi2": float(tot_l[it]),
                           "ln2_lcdm_chi2": cb(E_l2) + csn(E_l2), "ceiling_kappa_chi2": cb(E_c) + csn(E_c)}}
    ofs = np.round(np.arange(0.70, 0.9991, 0.002), 4)
    tot_c = np.array([cb(lambda zz, of=of: E_ceiling(zz, LN2, of)) + csn(lambda zz, of=of: E_ceiling(zz, LN2, of)) for of in ofs])
    j = int(np.argmin(tot_c)); sel = np.where(tot_c - tot_c[j] <= 1.0)[0]
    out["bao_plus_sn"]["ceiling_scan"] = {"omega_f_best": float(ofs[j]), "chi2_best": float(tot_c[j]),
                                         "omega_f_1sigma": [float(ofs[sel[0]]), float(ofs[sel[-1]])],
                                         "delta_chi2_at_kappa": out["bao_plus_sn"]["ceiling_kappa_chi2"] - float(tot_c[j])}
    for blk in ("bao_only", "bao_plus_sn"):
        b = out[blk]; b["delta_ceiling_vs_lcdm"] = b["ceiling_kappa_chi2"] - b["lcdm_chi2"]; b["delta_ln2_vs_lcdm"] = b["ln2_lcdm_chi2"] - b["lcdm_chi2"]
    json.dump(out, open(args.out, "w"), indent=2); print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
