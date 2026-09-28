#!/usr/bin/env python3
"""The dark-energy ceiling model against DES-Dovekie, the recalibrated DES 5-year supernovae (Popovic et al. 2026,
arXiv:2511.07517), the sample behind DESI's strongest evolving-dark-energy evidence. Same models and CMB/BAO machinery as
ceiling_model_cmb_bao_sn.py, with DES-Dovekie in place of Pantheon+ (the two share low-z SNe; never combine them).
Data (fetch_external_data.sh):
  DES-Dovekie_HD.csv: 1820 SNe (1623 DES + 197 low-z); an SNANA table despite the name.
  STAT+SYS.npz: the INVERSE stat+sys covariance stored as an upper triangle, unpacked as the release's
    DES-Dovekie-SN_Likelihood.py does.
  DES-Dovekie_Metadata.csv: each SN's field and host position.
SN likelihood: mu = 5 log10((1+zHEL) D_M(zHD)) + 25 with M marginalized analytically (the release's likelihood).
Validation: SN-only flat LCDM must return Omega_m = 0.330 +/- 0.015 (Popovic et al. 2026).
Direction: every DES SN lies in the hemisphere facing away from the CMB-dipole axis; along the Galactic-centre axis only
the E fields face it; and the 197 low-z SNe carry no position in this release. So no hemisphere split with cosmology on
each side is possible. Instead, with separate low-z and DES offsets and Omega_m profiled:
  (a) do the four DES field groups C, E, S, X (four sky directions, one telescope and pipeline) share one offset?
  (b) a cos(theta) dipole across the DES fields along each axis.
Output: DESY5_CEILING.json"""

import json, math
import numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2 as chi2_dist
import ceiling_model_cmb_bao_sn as m
from ceiling_model_bao_sn import load_bao
from omega_ln2_pantheonplus import chi2_marginalized
from pantheon_hemisphere_split import AXES, unit
import cosmo_data as cd

LN2, KAPPA = m.LN2, m.KAPPA
H_SN = 0.68  # SN-only fits: h enters only through the radiation term (~1e-4)
NM = {"xatol": 1e-6, "fatol": 1e-4, "maxiter": 4000}


def read_snana(path):
    names, rows = None, []
    with open(path) as f:
        for line in f:
            s = line.split()
            if s and s[0] == "VARNAMES:":
                names = s[1:]
            elif s and s[0] == "SN:":
                rows.append(s[1:])
    return {k: [r[i] for r in rows] for i, k in enumerate(names)}


def load_inv_cov(npz_path):
    d = np.load(npz_path)
    n = int(d["nsn"][0])
    inv = np.zeros((n, n))
    inv[np.triu_indices(n)] = d["cov"]
    il = np.tril_indices(n, -1)
    inv[il] = inv.T[il]
    return inv


def make_E_w0wa(h, om, w0, wa):
    orad = m.OR / h**2
    ode = 1 - om - orad
    return lambda z: np.sqrt(
        orad * (1 + z) ** 4
        + om * (1 + z) ** 3
        + ode * (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))
    )


def gls(r, X, W):
    A = X.T @ W @ X
    beta = np.linalg.solve(A, X.T @ W @ r)
    res = r - X @ beta
    return float(res @ W @ res), beta, np.linalg.inv(A)


def main():
    H = read_snana(cd.path("desy5_hd"))
    M = read_snana(cd.path("desy5_meta"))
    zhd, zhel, mu_obs = (np.array(H[k], float) for k in ("zHD", "zHEL", "MU"))
    W = load_inv_cov(cd.path("desy5_inv"))
    assert W.shape == (len(zhd), len(zhd)) and (zhd > 0).all()
    C = np.linalg.inv(W)
    ev_min = float(np.linalg.eigvalsh(W).min())
    err_ratio = float(
        np.median(
            np.sqrt(np.diag(C))
            / np.hypot(np.array(H["MUERR"], float), np.array(H["MUERR_SYS"], float))
        )
    )
    zsn = np.linspace(0, float(zhd.max()) * 1.0000001, 200001)

    def sn_mu(E):
        ez = E(zsn)
        dc = np.concatenate(
            ([0.0], np.cumsum((1 / ez)[1:] + (1 / ez)[:-1]) * 0.5 * np.diff(zsn))
        )
        return 5 * np.log10((1 + zhel) * np.interp(zhd, zsn, dc)) + 25.0

    chi_sn = lambda E: chi2_marginalized(mu_obs, sn_mu(E), W)
    out = {
        "data": cd.provenance(
            "desy5_hd", "desy5_inv", "desy5_meta", "desi_mean", "desi_cov"
        ),
        "checks": {
            "n_sne": int(len(zhd)),
            "inverse_cov_min_eigenvalue": ev_min,
            "median_sqrt_diag_cov_over_hypot_MUERR_MUERR_SYS": err_ratio,
        },
    }
    print(out["checks"], flush=True)

    # ---- SN only ----
    oms = np.round(np.arange(0.20, 0.45001, 0.001), 4)
    c = np.array([chi_sn(m.make_E("lcdm", H_SN, om)[0]) for om in oms])
    i = int(np.argmin(c))
    ok = oms[c - c[i] <= 1.0]
    sn = {
        "lcdm": {
            "omega_m": float(oms[i]),
            "omega_m_1sigma": [float(ok.min()), float(ok.max())],
            "chi2": float(c[i]),
            "published_omega_m": "0.330 +/- 0.015 (Popovic et al. 2026)",
        }
    }
    c_ln2 = chi_sn(m.make_E("lcdm", H_SN, 1 - LN2 - m.OR / H_SN**2)[0])
    sn["lcdm_ln2"] = {"chi2": c_ln2, "delta_vs_lcdm": c_ln2 - float(c[i])}
    ofs = np.round(np.arange(0.70, 0.9991, 0.002), 4)
    for n in (1.0, 2.0):
        ck = chi_sn(m.make_E("ceil", H_SN, None, KAPPA, n)[0])
        co = np.array([chi_sn(m.make_E("ceil", H_SN, None, of, n)[0]) for of in ofs])
        j = int(np.argmin(co))
        ok2 = ofs[co - co[j] <= 1.0]
        sn[f"ceiling_n={n}"] = {
            "chi2_kappa": ck,
            "delta_kappa_vs_lcdm": ck - float(c[i]),
            "omega_f_best": float(ofs[j]),
            "omega_f_1sigma": [float(ok2.min()), float(ok2.max())],
            "delta_kappa_vs_best_ceiling": ck - float(co[j]),
        }
    out["sn_only"] = sn
    print("SN only:", json.dumps(sn), flush=True)

    # ---- Planck distance priors + DESI DR2 BAO + DES-Dovekie ----
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
                {"DM_over_rs": DM[k], "DH_over_rs": DH[k], "DV_over_rs": DV[k]}[qb[k]]
                for k in range(len(zb))
            ]
        )
        r = db - pred
        return float(r @ Cbi @ r)

    def parts(E, h, om0, ob):
        return m.cmb_chi2(E, h, om0, ob)[0], chi_bao(E, h, om0, ob), chi_sn(E)

    def total(p, model, of=KAPPA, n=1.0):
        if model == "lcdm":
            om, h, ob = p
        elif model == "w0wa":
            om, h, ob, w0, wa = p
        else:
            (h, ob), om = p, None
        if not (0.5 < h < 0.9 and 0.015 < ob < 0.03) or (
            om is not None and not 0.1 < om < 0.6
        ):
            return 3e9
        if model == "w0wa":
            if not (-2 < w0 < 0 and -3 < wa < 2 and w0 + wa < 0):
                return 3e9
            return sum(parts(make_E_w0wa(h, om, w0, wa), h, om, ob))
        E, om0 = m.make_E(model, h, om, of, n)
        return sum(parts(E, h, om0, ob))

    fl = minimize(
        lambda p: total(p, "lcdm"),
        [0.31, 0.68, 0.02237],
        method="Nelder-Mead",
        options=NM,
    )
    El, _ = m.make_E("lcdm", fl.x[1], fl.x[0])
    comb = {
        "lcdm": {
            "omega_m": fl.x[0],
            "h": fl.x[1],
            "omega_b": fl.x[2],
            "chi2": fl.fun,
            "parts_cmb_bao_sn": parts(El, fl.x[1], fl.x[0], fl.x[2]),
        }
    }
    print("LCDM:", comb["lcdm"], flush=True)
    for n in (0.5, 1.0, 2.0):
        fc = minimize(
            lambda p: total(p, "ceil", KAPPA, n),
            [0.68, 0.02237],
            method="Nelder-Mead",
            options=NM,
        )
        E, om0 = m.make_E("ceil", fc.x[0], None, KAPPA, n)
        r0 = LN2 / om0
        rf = KAPPA / (1 - KAPPA)
        wfun = lambda a: -(1 - 1.0 / (1 + ((rf / r0) ** n - 1) * a ** (-3 * n)))
        comb[f"ceiling_kappa_n={n}"] = {
            "h": fc.x[0],
            "omega_b": fc.x[1],
            "chi2": fc.fun,
            "delta_vs_lcdm": fc.fun - fl.fun,
            "parts_cmb_bao_sn": parts(E, fc.x[0], om0, fc.x[1]),
            "w0": wfun(1.0),
            "wa": -(wfun(1.0) - wfun(1 - 1e-4)) / 1e-4,
        }
        print(f"ceiling kappa n={n}:", comb[f"ceiling_kappa_n={n}"], flush=True)
    for n in (1.0, 2.0):
        fo = minimize(
            lambda p: total(p[:2], "ceil", p[2], n) if 0.70 < p[2] < 0.999 else 3e9,
            [0.68, 0.02237, 0.95],
            method="Nelder-Mead",
            options={**NM, "maxiter": 6000},
        )
        comb[f"ceiling_free_n={n}"] = {
            "h": fo.x[0],
            "omega_b": fo.x[1],
            "omega_f": fo.x[2],
            "chi2": fo.fun,
            "delta_vs_lcdm": fo.fun - fl.fun,
        }
        print(f"free ceiling n={n}:", comb[f"ceiling_free_n={n}"], flush=True)
    best = None
    for start in ([0.31, 0.68, 0.02237, -1.0, 0.0], [0.32, 0.67, 0.02237, -0.8, -0.7]):
        fw = minimize(
            lambda p: total(p, "w0wa"),
            start,
            method="Nelder-Mead",
            options={**NM, "maxiter": 12000},
        )
        best = fw if best is None or fw.fun < best.fun else best
    comb["w0wa"] = {
        "omega_m": best.x[0],
        "h": best.x[1],
        "omega_b": best.x[2],
        "w0": best.x[3],
        "wa": best.x[4],
        "chi2": best.fun,
        "delta_vs_lcdm": best.fun - fl.fun,
        "published_reference": "w0 = -0.803 +/- 0.054, wa = -0.72 +/- 0.21 (DES-Dovekie + Planck/ACT/SPT + DESI DR2; Popovic et al. 2026)",
    }
    print("w0wa:", comb["w0wa"], flush=True)
    prof = {}
    grid = np.round(
        np.concatenate(
            [np.arange(0.72, 0.99, 0.01), [0.9539392, 0.985, 0.992, 0.995, 0.998]]
        ),
        7,
    )
    grid.sort()
    for n in (1.0, 2.0):
        rows = []
        start = [0.68, 0.0225]
        for of in grid:
            r = minimize(
                lambda p: total(p, "ceil", of, n),
                start,
                method="Nelder-Mead",
                options={**NM, "maxiter": 3000},
            )
            start = list(r.x)
            rows.append((float(of), float(r.fun), float(r.x[0]), float(r.x[1])))
        cc = np.array([x[1] for x in rows])
        j = int(np.argmin(cc))
        sel = [x[0] for x in rows if x[1] - cc[j] <= 1.0]
        k = [x for x in rows if abs(x[0] - 0.9539392) < 1e-6][0]
        prof[f"n={n}"] = {
            "grid": rows,
            "omega_f_best": rows[j][0],
            "chi2_best": rows[j][1],
            "omega_f_1sigma": [min(sel), max(sel)],
            "delta_chi2_kappa_vs_best": k[1] - rows[j][1],
            "best_minus_lcdm": rows[j][1] - fl.fun,
        }
        print(
            f"profile n={n}:",
            {x: v for x, v in prof[f"n={n}"].items() if x != "grid"},
            flush=True,
        )
    comb["profile_omega_f"] = prof
    out["cmb_bao_sn"] = comb

    # ---- direction ----
    meta = {(cid, s): k for k, (cid, s) in enumerate(zip(M["CID"], M["IDSURVEY"]))}
    idx = np.array([meta[(cid, s)] for cid, s in zip(H["CID"], H["IDSURVEY"])])
    field = np.array(M["FIELD"])[idx]
    ra = np.array(M["HOST_RA"], float)[idx]
    dec = np.array(M["HOST_DEC"], float)[idx]
    lowz = field == "VOID"
    des = ~lowz
    assert (np.array(H["IDSURVEY"])[des] == "10").all() and (ra[des] > -90).all()
    grp = np.array([f[0] if d else "-" for f, d in zip(field, des)])
    assert all(
        len({ch for ch in f if ch.isalpha()}) == 1 for f in field[des]
    )  # no cross-group overlaps
    groups = ["C", "E", "S", "X"]
    nhat = unit(ra, dec)
    cosax = {a: np.where(des, nhat @ unit(*AXES[a]), 0.0) for a in AXES}
    om_grid = np.round(np.arange(0.20, 0.45001, 0.005), 4)
    resid = [(om, mu_obs - sn_mu(m.make_E("lcdm", H_SN, om)[0])) for om in om_grid]

    def profile(X):
        fits = [(gls(r, X, W), om) for om, r in resid]
        (c2, beta, cov), om = min(fits, key=lambda t: t[0][0])
        return c2, beta, cov, om

    X0 = np.stack([lowz, des], 1).astype(float)
    c0, _, _, om0 = profile(X0)
    X1 = np.stack([lowz] + [grp == g for g in groups], 1).astype(float)
    c1, b1, v1, om1 = profile(X1)
    offs = b1[1:] - b1[1:].mean()
    P = np.eye(4) - 1 / 4
    voff = P @ v1[1:, 1:] @ P.T
    direc = {
        "no_hemisphere_split": {
            a: {
                "des_sne_toward": int((cosax[a][des] > 0).sum()),
                "des_cos_range": [
                    float(cosax[a][des].min()),
                    float(cosax[a][des].max()),
                ],
                "lowz_without_position": int(lowz.sum()),
            }
            for a in AXES
        },
        "fields": {
            "delta_chi2_one_offset_vs_four": c0 - c1,
            "dof": 3,
            "p_value": float(chi2_dist.sf(c0 - c1, 3)),
            "omega_m_profiled": om1,
            "per_field": {
                g: {
                    "n": int((grp == g).sum()),
                    "ra_mean": float(ra[grp == g].mean()),
                    "dec_mean": float(dec[grp == g].mean()),
                    "offset_vs_des_mean_mag": float(offs[q]),
                    "offset_err_mag": float(math.sqrt(voff[q, q])),
                    **{f"cos_{a}": float(cosax[a][grp == g].mean()) for a in AXES},
                }
                for q, g in enumerate(groups)
            },
        },
    }
    for a in AXES:
        X2 = np.stack([lowz, des, cosax[a]], 1).astype(float)
        c2, b2, v2, om2 = profile(X2)
        A, sA = float(b2[2]), float(math.sqrt(v2[2, 2]))
        direc[f"dipole_{a}"] = {
            "A_mag_per_cos": A,
            "A_err": sA,
            "delta_chi2_vs_no_dipole": c0 - c2,
            "omega_m_profiled": om2,
            "dDL_over_DL": A * math.log(10) / 5,
            "dDL_over_DL_err": sA * math.log(10) / 5,
        }
    out["direction"] = direc
    print("direction:", json.dumps(direc), flush=True)
    json.dump(out, open(cd.out("DESY5_CEILING.json"), "w"), indent=2, default=float)


if __name__ == "__main__":
    main()
