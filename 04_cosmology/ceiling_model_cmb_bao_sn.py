#!/usr/bin/env python3
"""Dark-energy ceiling model vs Planck 2018 distance priors + DESI DR2 BAO + Pantheon+ (the full late+early test).
Ceiling model (share ln 2 today -> ceiling Omega_f; generalized logistic, exponent n):
   d ln r / d ln a = 3 (1 - (r/r_f)^n),  w = -(1 - (r/r_f)^n),  r = rho_DE/rho_m,  r0 = ln2/Omega_m0,  r_f = Of/(1-Of).
CMB: Chen, Huang & Wang 2019 (arXiv:1808.05724) Planck TT,TE,EE+lowE distance priors (R, l_A, omega_b) with their
     inverse covariance; z* from Hu-Sugiyama, r_s(z*) by direct integration (photons + 3.046 massless-equivalent nu).
BAO: DESI DR2 with r_d from Aubourg et al. 2015 eq.16 (Sum m_nu = 0.06 eV). SN: Pantheon+, M marginalized.
Parameters: LCDM (Omega_m, h, omega_b); ceiling (h, omega_b) with Omega_DE0 = ln 2 fixed.
Validation printed first: Planck best-fit LCDM must reproduce the priors.
Usage: ceiling_model_cmb_bao_sn.py --bao-mean M --bao-cov C --dat D --cov V"""
import argparse, json, math
import numpy as np
from scipy.optimize import minimize
from omega_ln2_pantheonplus import load_data, official_mask, load_cov, chi2_marginalized
from ceiling_model_bao_sn import load_bao

LN2 = math.log(2.0); KAPPA = math.sqrt(0.91); CKMS = 299792.458
OMG = 2.4728e-5            # omega_gamma for T = 2.7255 K
ONU_M = 0.06 / 93.14       # massive-nu density today (treated as matter at late times)
OR = OMG * (1 + 0.2271 * 3.046)   # radiation (early-time, massless-equivalent)
PRI = np.array([1.750235, 301.4707, 0.02235976])
PINV = np.array([[94392.3971, -1360.4913, 1664517.2916], [-1360.4913, 161.4349, 3671.6180], [1664517.2916, 3671.6180, 79719182.5162]])

def make_E(model, h, om=None, of=KAPPA, n=1.0):
    orad = OR / h**2
    if model == "lcdm":
        ol = 1 - om - orad
        return lambda z: np.sqrt(orad * (1 + z)**4 + om * (1 + z)**3 + ol), om
    om0 = 1 - LN2 - orad; r0 = LN2 / om0; rf = of / (1 - of)
    def E(z):
        a = 1 / (1 + z)
        # generalized logistic: d ln r / d ln a = 3 (1 - (r/rf)^n)  ->  (r/rf)^n = 1 / (1 + ((rf/r0)^n - 1) a^(-3n))
        x = 1.0 / (1 + ((rf / r0)**n - 1) * a**(-3 * n)); r = rf * x**(1 / n)
        return np.sqrt(orad * (1 + z)**4 + om0 * (1 + z)**3 * (1 + r))
    return E, om0

def dm_over(E, z):   # comoving distance in units of c/H0
    zs = np.concatenate([np.linspace(0, 3, 30001), np.geomspace(3.0001, max(float(np.max(z)), 3.01), 20001)]); ez = E(zs)
    dc = np.concatenate(([0.0], np.cumsum(0.5 * ((1 / ez)[1:] + (1 / ez)[:-1]) * np.diff(zs))))   # non-uniform grid: step inside the sum
    return np.interp(z, zs, dc)

def zstar(ob, om):
    g1 = 0.0783 * ob**(-0.238) / (1 + 39.5 * ob**0.763); g2 = 0.560 / (1 + 21.1 * ob**1.81)
    return 1048.0 * (1 + 0.00124 * ob**(-0.738)) * (1 + g1 * om**g2)

def rs_over(E, ob, zs_, h=None):   # sound horizon in units of c/H0 (E carries h)
    a = np.geomspace(1e-9, 1 / (1 + zs_), 40001); z = 1 / a - 1
    Rb = 3 * ob / (4 * OMG) * a
    # near recombination the massive neutrino is radiation-like: remove its late-time matter term from E^2 here
    Ez = E(z) if h is None else np.sqrt(np.maximum(E(z)**2 - (ONU_M / h**2) * (1 + z)**3, 1e-300))
    f = 1 / np.sqrt(3 * (1 + Rb)) / (a**2 * Ez)
    return float(np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(a)))

def rd_mpc(ob, omh2):
    ocb = omh2 - ONU_M
    return 55.154 * math.exp(-72.3 * (ONU_M + 0.0006)**2) / (ocb**0.25351 * ob**0.12807)

def cmb_chi2(E, h, om0, ob):
    omh2 = om0 * h**2 + ONU_M * 0 ; zs_ = zstar(ob, omh2)
    DM = dm_over(E, zs_); rs = rs_over(E, ob, zs_, h)
    R = math.sqrt(om0) * DM; lA = math.pi * DM / rs
    d = np.array([R, lA, ob]) - PRI
    return float(d @ PINV @ d), R, lA, zs_

def main():
    ap = argparse.ArgumentParser()
    for k in ("--bao-mean", "--bao-cov", "--dat", "--cov"): ap.add_argument(k, required=True)
    ap.add_argument("--out", default="CEILING_MODEL_CMB_BAO_SN.json"); args = ap.parse_args()
    zb, db, qb, Cb = load_bao(args.bao_mean, args.bao_cov); Cbi = np.linalg.inv(Cb)
    zhel_all, zhd_all, mb_all = load_data(args.dat); ww = official_mask(zhd_all)
    zhel, zhd, mb = zhel_all[ww], zhd_all[ww], mb_all[ww]; sinv = np.linalg.inv(load_cov(args.cov)[np.ix_(ww, ww)])
    zsn = np.linspace(0, float(zhd.max()) * 1.0000001, 200001)
    def chi_sn(E):
        ez = E(zsn); dc = np.concatenate(([0.0], np.cumsum((1 / ez)[1:] + (1 / ez)[:-1]) * 0.5 * np.diff(zsn)))
        mu = 5 * np.log10((1 + zhel) * np.interp(zhd, zsn, dc)) + 25.0
        return chi2_marginalized(mb, mu, sinv)
    def chi_bao(E, h, om0, ob):
        rd = rd_mpc(ob, om0 * h**2); dh0 = CKMS / (100 * h)
        DM = dm_over(E, zb) * dh0 / rd; DH = dh0 / E(zb) / rd; DV = (zb * DM**2 * DH)**(1 / 3)
        pred = np.array([{"DM_over_rs": DM[i], "DH_over_rs": DH[i], "DV_over_rs": DV[i]}[qb[i]] for i in range(len(zb))])
        r = db - pred; return float(r @ Cbi @ r)
    def total(p, model, of=KAPPA, n=1.0, parts=False):
        if model == "lcdm": om, h, ob = p
        else: (h, ob), om = p, None
        if not (0.5 < h < 0.9 and 0.015 < ob < 0.03) or (om is not None and not 0.1 < om < 0.6):
            return (1e9, 1e9, 1e9) if parts else 3e9
        E, om0 = make_E(model, h, om, of, n)
        c1 = cmb_chi2(E, h, om0, ob)[0]; c2 = chi_bao(E, h, om0, ob); c3 = chi_sn(E)
        return (c1, c2, c3) if parts else c1 + c2 + c3
    # validation: Planck 2018 best-fit LCDM
    Ev, _ = make_E("lcdm", 0.6736, 0.3153)
    cv, Rv, lAv, zv = cmb_chi2(Ev, 0.6736, 0.3153, 0.02237)
    print(f"validation (Planck LCDM 0.3153/0.6736/0.02237): R = {Rv:.5f} (prior 1.750235), l_A = {lAv:.3f} (301.4707), z* = {zv:.2f}, chi2_CMB = {cv:.2f}", flush=True)
    fl = minimize(lambda p: total(p, "lcdm"), [0.31, 0.68, 0.02237], method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-4, "maxiter": 4000})
    out = {"validation": {"R": Rv, "l_A": lAv, "z_star": zv, "chi2_cmb": cv},
           "lcdm": {"omega_m": fl.x[0], "h": fl.x[1], "omega_b": fl.x[2], "chi2": fl.fun, "parts_cmb_bao_sn": total(fl.x, "lcdm", parts=True)}}
    print("LCDM:", out["lcdm"], flush=True)
    out["ceiling"] = {}
    for n in (0.5, 1.0, 2.0):
        fc = minimize(lambda p: total(p, "ceil", KAPPA, n), [0.68, 0.02237], method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-4, "maxiter": 4000})
        E, om0 = make_E("ceil", fc.x[0], None, KAPPA, n)
        r0 = LN2 / om0; rf = KAPPA / (1 - KAPPA); x = (r0 / rf)**n
        w0 = -(1 - x); dw = 1e-4; zz = dw
        # w_a from w(a) numerically: w(a) = -(1 - (r(a)/rf)^n)
        def wa_fun(a):
            xx = 1.0 / (1 + ((rf / r0)**n - 1) * a**(-3 * n)); return -(1 - xx)
        wa = -(wa_fun(1.0) - wa_fun(1.0 - dw)) / dw
        out["ceiling"][f"n={n}"] = {"h": fc.x[0], "omega_b": fc.x[1], "chi2": fc.fun, "delta_vs_lcdm": fc.fun - fl.fun,
                                    "parts_cmb_bao_sn": total(fc.x, "ceil", KAPPA, n, parts=True), "w0": w0, "wa": wa}
        print(f"ceiling n={n}:", out["ceiling"][f"n={n}"], flush=True)
    # free ceiling (n = 1): where do CMB+BAO+SN put it?
    fo = minimize(lambda p: total(p[:2], "ceil", p[2], 1.0) if 0.72 < p[2] < 0.999 else 1e9, [0.68, 0.02237, 0.95], method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-4, "maxiter": 6000})
    out["ceiling_free_n1"] = {"h": fo.x[0], "omega_b": fo.x[1], "omega_f": fo.x[2], "chi2": fo.fun, "delta_vs_lcdm": fo.fun - fl.fun}
    print("free ceiling:", out["ceiling_free_n1"], flush=True)
    json.dump(out, open(args.out, "w"), indent=2, default=float)

if __name__ == "__main__":
    main()
