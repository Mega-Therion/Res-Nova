#!/usr/bin/env python3
"""O3 test, pre-registered in PREREG_O3_LN2_CMB_BAO_SN_2026-11-25.md (commit 608182cb, frozen before this script).

Flat LCDM with Omega_Lambda = ln 2 exactly (parameters h, omega_b) versus free flat LCDM (Omega_m, h, omega_b) on
  (A) CHW 2019 Planck distance priors + DESI DR2 BAO + Pantheon+   and
  (B) CHW 2019 Planck distance priors + DESI DR2 BAO + DES-Dovekie.
The CMB, BAO and SN likelihoods are the validated ones of ceiling_model_cmb_bao_sn.py / desy5_ceiling.py, unchanged.
Verdict per combination (frozen rule): Delta chi2 <= 9 -> CONSISTENT; > 9 -> TENSION.
Usage: o3_ln2_cmb_bao_sn.py   (data: fetch_external_data.sh)"""
import json, math, time
import numpy as np
from scipy.optimize import minimize
import cosmo_data as cd
import ceiling_model_cmb_bao_sn as m
from ceiling_model_bao_sn import load_bao
from omega_ln2_pantheonplus import load_data, official_mask, load_cov, chi2_marginalized
from desy5_ceiling import read_snana, load_inv_cov

PREREG = "608182cb"
LN2 = math.log(2.0)


def build_sn_pantheon():
    zhel_all, zhd_all, mb_all = load_data(cd.path("pantheon_dat")); ww = official_mask(zhd_all)
    zhel, zhd, mb = zhel_all[ww], zhd_all[ww], mb_all[ww]
    sinv = np.linalg.inv(load_cov(cd.path("pantheon_cov"))[np.ix_(ww, ww)])
    zsn = np.linspace(0, float(zhd.max()) * 1.0000001, 200001)
    def chi(E):
        ez = E(zsn); dc = np.concatenate(([0.0], np.cumsum((1 / ez)[1:] + (1 / ez)[:-1]) * 0.5 * np.diff(zsn)))
        mu = 5 * np.log10((1 + zhel) * np.interp(zhd, zsn, dc)) + 25.0
        return chi2_marginalized(mb, mu, sinv)
    return chi, int(ww.sum())


def build_sn_des():
    H = read_snana(cd.path("desy5_hd"))
    zhd, zhel, mu_obs = (np.array(H[k], float) for k in ("zHD", "zHEL", "MU"))
    W = load_inv_cov(cd.path("desy5_inv"))
    zsn = np.linspace(0, float(zhd.max()) * 1.0000001, 200001)
    def chi(E):
        ez = E(zsn); dc = np.concatenate(([0.0], np.cumsum((1 / ez)[1:] + (1 / ez)[:-1]) * 0.5 * np.diff(zsn)))
        mu = 5 * np.log10((1 + zhel) * np.interp(zhd, zsn, dc)) + 25.0
        return chi2_marginalized(mu_obs, mu, W)
    return chi, int(len(zhd))


def main():
    t0 = time.time()
    zb, db, qb, Cb = load_bao(cd.path("desi_mean"), cd.path("desi_cov")); Cbi = np.linalg.inv(Cb)
    def chi_bao(E, h, om0, ob):
        rd = m.rd_mpc(ob, om0 * h**2); dh0 = m.CKMS / (100 * h)
        DM = m.dm_over(E, zb) * dh0 / rd; DH = dh0 / E(zb) / rd; DV = (zb * DM**2 * DH)**(1 / 3)
        pred = np.array([{"DM_over_rs": DM[i], "DH_over_rs": DH[i], "DV_over_rs": DV[i]}[qb[i]] for i in range(len(zb))])
        r = db - pred; return float(r @ Cbi @ r)

    # validation of the CMB block (must match the pipeline's own check, chi2_CMB ~ 1.16)
    Ev, _ = m.make_E("lcdm", 0.6736, 0.3153)
    cv, Rv, lAv, zv = m.cmb_chi2(Ev, 0.6736, 0.3153, 0.02237)
    out = {"prereg_commit": PREREG,
           "data": cd.provenance("desi_mean", "desi_cov", "pantheon_dat", "pantheon_cov", "desy5_hd", "desy5_inv"),
           "validation_planck_lcdm": {"R": Rv, "l_A": lAv, "z_star": zv, "chi2_cmb": cv}}
    print("validation:", out["validation_planck_lcdm"], flush=True)

    for label, builder in (("A_cmb_desi_pantheonplus", build_sn_pantheon), ("B_cmb_desi_desdovekie", build_sn_des)):
        chi_sn, nsn = builder()
        def total(p, model, parts=False):
            if model == "lcdm":
                om, h, ob = p
                if not (0.1 < om < 0.6): return (1e9,) * 3 if parts else 3e9
                E, om0 = m.make_E("lcdm", h, om)
            else:
                h, ob = p
                om0, _ = m.om0_ln2(h)
                E, _ = m.make_E("lcdm", h, om0)
            if not (0.5 < h < 0.9 and 0.015 < ob < 0.03): return (1e9,) * 3 if parts else 3e9
            c = (m.cmb_chi2(E, h, om0, ob)[0], chi_bao(E, h, om0, ob), chi_sn(E))
            return c if parts else sum(c)
        opts = {"xatol": 1e-6, "fatol": 1e-4, "maxiter": 4000}
        fl = minimize(lambda p: total(p, "lcdm"), [0.31, 0.68, 0.02237], method="Nelder-Mead", options=opts)
        fl = minimize(lambda p: total(p, "lcdm"), fl.x, method="Nelder-Mead", options=opts)       # restart (frozen)
        f2 = minimize(lambda p: total(p, "ln2"), [0.68, 0.02237], method="Nelder-Mead", options=opts)
        f2 = minimize(lambda p: total(p, "ln2"), f2.x, method="Nelder-Mead", options=opts)        # restart (frozen)
        d = f2.fun - fl.fun
        res = {"n_sne": nsn, "n_bao": int(len(zb)),
               "lcdm_free": {"omega_m": fl.x[0], "h": fl.x[1], "omega_b": fl.x[2], "chi2": fl.fun,
                             "parts_cmb_bao_sn": total(fl.x, "lcdm", parts=True)},
               "lcdm_ln2": {"omega_lambda": LN2, "omega_m": m.om0_ln2(f2.x[0])[0], "h": f2.x[0], "omega_b": f2.x[1],
                            "chi2": f2.fun, "parts_cmb_bao_sn": total(f2.x, "ln2", parts=True)},
               "delta_chi2": d, "sigma_equiv": math.sqrt(max(d, 0.0)),
               "verdict": "CONSISTENT" if d <= 9 else "TENSION"}
        out[label] = res
        print(label, json.dumps(res, default=float), flush=True)
    out["runtime_s"] = time.time() - t0
    json.dump(out, open(cd.out("O3_LN2_CMB_BAO_SN_2026-11-25.json"), "w"), indent=2, default=float)


if __name__ == "__main__":
    main()
