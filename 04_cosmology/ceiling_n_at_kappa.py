#!/usr/bin/env python3
"""What approach law does a ceiling at kappa need? Profile chi2(n) at Omega_f = kappa under Planck distance priors +
DESI DR2 BAO + supernovae (Pantheon+, or DES-Dovekie), re-fitting (h, omega_b) at each n. Model and CMB/BAO machinery of
ceiling_model_cmb_bao_sn.py; the DES-Dovekie likelihood of desy5_ceiling.py.
The profiles in CEILING_SCAN_CMB_BAO_SN.json and DESY5_CEILING.json vary Omega_f at fixed n. This one varies n at fixed
Omega_f = kappa, giving the control-rod setting the data ask of a kappa ceiling.
Usage: ceiling_n_at_kappa.py  (data: fetch_external_data.sh)   Output: CEILING_N_AT_KAPPA.json
"""

import json
import numpy as np
from scipy.optimize import minimize
import ceiling_model_cmb_bao_sn as m
import cosmo_data as cd
from ceiling_model_bao_sn import load_bao
from omega_ln2_pantheonplus import load_data, official_mask, load_cov, chi2_marginalized
from desy5_ceiling import read_snana, load_inv_cov

NM = {"xatol": 1e-6, "fatol": 1e-4, "maxiter": 4000}


def sn_likelihoods():
    zhel_all, zhd_all, mb_all = load_data(cd.path("pantheon_dat"))
    ww = official_mask(zhd_all)
    pp = (
        zhel_all[ww],
        zhd_all[ww],
        mb_all[ww],
        np.linalg.inv(load_cov(cd.path("pantheon_cov"))[np.ix_(ww, ww)]),
    )
    H = read_snana(cd.path("desy5_hd"))
    des = (
        np.array(H["zHEL"], float),
        np.array(H["zHD"], float),
        np.array(H["MU"], float),
        load_inv_cov(cd.path("desy5_inv")),
    )

    def make(zhel, zhd, mu_obs, W):
        zs = np.linspace(0, float(zhd.max()) * 1.0000001, 200001)

        def chi(E):
            ez = E(zs)
            dc = np.concatenate(
                ([0.0], np.cumsum((1 / ez)[1:] + (1 / ez)[:-1]) * 0.5 * np.diff(zs))
            )
            return chi2_marginalized(
                mu_obs, 5 * np.log10((1 + zhel) * np.interp(zhd, zs, dc)) + 25.0, W
            )

        return chi

    return {"pantheon_plus": make(*pp), "des_dovekie": make(*des)}


def main():
    zb, db, qb, Cb = load_bao(cd.path("desi_mean"), cd.path("desi_cov"))
    Cbi = np.linalg.inv(Cb)

    def chi_bao(E, h, om0, ob):
        rd = m.rd_mpc(ob, om0 * h**2)
        dh0 = m.CKMS / (100 * h)
        DM = m.dm_over(E, zb) * dh0 / rd
        DH = dh0 / E(zb) / rd
        DV = (zb * DM**2 * DH) ** (1 / 3)
        pred = np.array(
            [
                {"DM_over_rs": DM[i], "DH_over_rs": DH[i], "DV_over_rs": DV[i]}[qb[i]]
                for i in range(len(zb))
            ]
        )
        r = db - pred
        return float(r @ Cbi @ r)

    out = {
        "data": cd.provenance(
            "pantheon_dat",
            "pantheon_cov",
            "desy5_hd",
            "desy5_inv",
            "desi_mean",
            "desi_cov",
        ),
        "omega_f": m.KAPPA,
    }
    ns = np.round(np.arange(0.8, 4.01, 0.1), 2)
    for name, chi_sn in sn_likelihoods().items():

        def tot(p, model, n=1.0):
            if model == "lcdm":
                om, h, ob = p
            else:
                (h, ob), om = p, None
            if not (0.5 < h < 0.9 and 0.015 < ob < 0.03) or (
                om is not None and not 0.1 < om < 0.6
            ):
                return 3e9
            E, om0 = m.make_E(model, h, om, m.KAPPA, n)
            return m.cmb_chi2(E, h, om0, ob)[0] + chi_bao(E, h, om0, ob) + chi_sn(E)

        fl = minimize(
            lambda p: tot(p, "lcdm"),
            [0.31, 0.68, 0.02237],
            method="Nelder-Mead",
            options=NM,
        )
        rows = []
        start = [0.68, 0.0225]
        for n in ns:
            r = minimize(
                lambda p: tot(p, "ceil", n), start, method="Nelder-Mead", options=NM
            )
            start = list(r.x)
            rows.append((float(n), float(r.fun), float(r.x[0]), float(r.x[1])))
            print(
                name,
                f"n={n:.1f} chi2={r.fun:.3f} (vs LCDM {r.fun - fl.fun:+.3f})",
                flush=True,
            )
        c = np.array([x[1] for x in rows])
        j = int(np.argmin(c))
        fine = np.linspace(ns[0], ns[-1], 3201)
        cf = np.interp(fine, ns, c)
        sel = fine[cf - cf.min() <= 1.0]
        sel2 = fine[cf - cf.min() <= 4.0]
        if (
            0 < j < len(ns) - 1
        ):  # parabola through the three grid points around the minimum
            a_, b_, _ = np.polyfit(ns[j - 1 : j + 2], c[j - 1 : j + 2], 2)
            n_best = float(-b_ / (2 * a_))
        else:
            n_best = float(ns[j])
        out[name] = {
            "lcdm_chi2": fl.fun,
            "grid_n_chi2_h_omegab": rows,
            "n_best": n_best,
            "chi2_best_grid": float(c[j]),
            "n_1sigma_interp": [float(sel.min()), float(sel.max())],
            "n_2sigma_interp": [float(sel2.min()), float(sel2.max())],
            "upper_2sigma_edge_inside_grid": bool(sel2.max() < ns[-1]),
            "delta_chi2_at_n1_n2": [float(c[list(ns).index(1.0)] - c[j]), float(c[list(ns).index(2.0)] - c[j])],
            "best_minus_lcdm": float(c[j] - fl.fun),
        }
        print(
            name,
            {k: v for k, v in out[name].items() if k != "grid_n_chi2_h_omegab"},
            flush=True,
        )
    json.dump(out, open(cd.out("CEILING_N_AT_KAPPA.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
