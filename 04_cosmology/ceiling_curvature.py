#!/usr/bin/env python3
"""Spatial curvature inside the ceiling model (RY 2026-09-28: does gravity pull the dissolved universe back?).
Once the ceiling freezes, acceleration ends and curvature grows ~a relative to the frozen fluid, so the sign of
Omega_k decides coast (flat/open) or crunch (closed); see ceiling_future.py. The published Omega_k assumes LCDM, so
here Omega_k is fitted with the ceiling itself.
Model: E^2 = Omega_r (1+z)^4 + Omega_m (1+z)^3 (1 + r(a)) + Omega_k (1+z)^2, share today ln 2 kept
(Omega_m = 1 - ln 2 - Omega_r - Omega_k), r(a) from d ln r / d ln a = 3 (1 - g(s)) (quadrature of
ceiling_factorial_law.py). Transverse distance D_M = sinh(sqrt(Ok) D_C)/sqrt(Ok) (Ok > 0) or sin(...) (Ok < 0),
used in SN (D_L = (1+zHEL) D_M), BAO (D_M, D_V) and the CMB priors (R = sqrt(Omega_m) D_M(z*), l_A = pi D_M/r_s).
Models: LCDM + Omega_k (validation against Planck 2018 + BAO: Omega_k = 0.0007 +/- 0.0019), and the kappa ceiling
with the factorial counting law at mu = 1 (no fitted shape) + Omega_k. Profile over Omega_k, (h, omega_b) re-fit.
Caveat: the Chen-Huang-Wang distance priors are compressed under standard assumptions; curvature enters them only
through D_M(z*).
Usage: ceiling_curvature.py  (data: fetch_external_data.sh)   Output: CEILING_CURVATURE.json
"""

import json, math
import numpy as np
from scipy.optimize import minimize
import ceiling_model_cmb_bao_sn as m
import ceiling_factorial_law as cf
import cosmo_data as cd
from ceiling_model_bao_sn import load_bao

NM = {"xatol": 1e-6, "fatol": 1e-4, "maxiter": 4000}
OKS = np.round(np.arange(-0.012, 0.01201, 0.002), 4)


def dm_curved(dc, ok):
    """Transverse comoving distance from line-of-sight comoving distance (both in c/H0)."""
    if abs(ok) < 1e-12:
        return dc
    s = math.sqrt(abs(ok))
    return np.sinh(s * dc) / s if ok > 0 else np.sin(s * dc) / s


def make_E(model, h, ok, om=None, law="truncated_poisson", p=1.0, of=m.KAPPA):
    orad = m.OR / h**2
    if model == "lcdm":
        ol = 1 - om - orad - ok
        return (
            lambda z: np.sqrt(
                orad * (1 + z) ** 4 + om * (1 + z) ** 3 + ok * (1 + z) ** 2 + ol
            ),
            om,
        )
    om0 = 1 - m.LN2 - orad - ok
    r0 = m.LN2 / om0
    rf = of / (1 - of)
    s0 = r0 / rf
    u = np.linspace(math.log(s0) - 75.0, math.log(s0), 60001)
    f = 1.0 / (3.0 * (1.0 - cf.LAWS[law](np.exp(u), p)))
    tau = np.concatenate(([0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(u))))
    tau -= tau[-1]

    def E(z):
        r = rf * np.exp(np.interp(-np.log1p(z), tau, u))
        return np.sqrt(
            orad * (1 + z) ** 4 + om0 * (1 + z) ** 3 * (1 + r) + ok * (1 + z) ** 2
        )

    return E, om0


def main():
    zb, db, qb, Cb = load_bao(cd.path("desi_mean"), cd.path("desi_cov"))
    Cbi = np.linalg.inv(Cb)
    # SN likelihoods need D_M, so rebuild them here with the curvature transform (same data as ceiling_n_at_kappa.py)
    flat_ref = {
        k: json.load(open(cd.out(f)))
        for k, f in (
            ("lcdm", "CEILING_N_AT_KAPPA.json"),
            ("ceiling", "CEILING_FACTORIAL_LAW.json"),
        )
    }
    from omega_ln2_pantheonplus import (
        load_data,
        official_mask,
        load_cov,
        chi2_marginalized,
    )
    from desy5_ceiling import read_snana, load_inv_cov

    zhel_all, zhd_all, mb_all = load_data(cd.path("pantheon_dat"))
    ww = official_mask(zhd_all)
    samples = {
        "pantheon_plus": (
            zhel_all[ww],
            zhd_all[ww],
            mb_all[ww],
            np.linalg.inv(load_cov(cd.path("pantheon_cov"))[np.ix_(ww, ww)]),
        )
    }
    H = read_snana(cd.path("desy5_hd"))
    samples["des_dovekie"] = (
        np.array(H["zHEL"], float),
        np.array(H["zHD"], float),
        np.array(H["MU"], float),
        load_inv_cov(cd.path("desy5_inv")),
    )
    out = {
        "data": cd.provenance(
            "pantheon_dat",
            "pantheon_cov",
            "desy5_hd",
            "desy5_inv",
            "desi_mean",
            "desi_cov",
        ),
        "omega_k_grid": [float(x) for x in OKS],
        "approach_law": "truncated_poisson, mu = 1 (no fitted shape)",
    }
    for name, (zhel, zhd, mu_obs, W) in samples.items():
        zs = np.linspace(0, float(zhd.max()) * 1.0000001, 200001)

        def chi_sn(E, ok):
            ez = E(zs)
            dc = np.concatenate(
                ([0.0], np.cumsum((1 / ez)[1:] + (1 / ez)[:-1]) * 0.5 * np.diff(zs))
            )
            return chi2_marginalized(
                mu_obs,
                5 * np.log10((1 + zhel) * dm_curved(np.interp(zhd, zs, dc), ok)) + 25.0,
                W,
            )

        def chi_bao(E, h, om0, ob, ok):
            rd = m.rd_mpc(ob, om0 * h**2)
            dh0 = m.CKMS / (100 * h)
            DM = dm_curved(m.dm_over(E, zb), ok) * dh0 / rd
            DH = dh0 / E(zb) / rd
            DV = (zb * DM**2 * DH) ** (1 / 3)
            pred = np.array(
                [
                    {"DM_over_rs": DM[i], "DH_over_rs": DH[i], "DV_over_rs": DV[i]}[
                        qb[i]
                    ]
                    for i in range(len(zb))
                ]
            )
            r = db - pred
            return float(r @ Cbi @ r)

        def chi_cmb(E, h, om0, ob, ok):
            zs_ = m.zstar(ob, om0 * h**2)
            DM = float(dm_curved(m.dm_over(E, zs_), ok))
            rs = m.rs_over(E, ob, zs_, h)
            d = np.array([math.sqrt(om0) * DM, math.pi * DM / rs, ob]) - m.PRI
            return float(d @ m.PINV @ d)

        def tot(p, model, ok):
            if model == "lcdm":
                om, h, ob = p
            else:
                (h, ob), om = p, None
            if not (0.5 < h < 0.9 and 0.015 < ob < 0.03) or (
                om is not None and not 0.1 < om < 0.6
            ):
                return 3e9
            E, om0 = make_E(model, h, ok, om)
            return (
                chi_cmb(E, h, om0, ob, ok) + chi_bao(E, h, om0, ob, ok) + chi_sn(E, ok)
            )

        # sanity: at Omega_k = 0 the curved code must reproduce the committed flat fits
        ref = {
            "lcdm": flat_ref["lcdm"][name]["lcdm_chi2"],
            "ceiling": [
                x["chi2"]
                for x in flat_ref["ceiling"][name]["truncated_poisson"]["grid"]
                if x["p"] == 1.0
            ][0],
        }
        res = {}
        for model, start in (
            ("lcdm", [0.31, 0.68, 0.02237]),
            ("ceiling", [0.68, 0.0225]),
        ):
            rows = []
            st = list(start)
            for ok in OKS:
                r = minimize(
                    lambda p: tot(p, model, ok), st, method="Nelder-Mead", options=NM
                )
                st = list(r.x)
                rows.append((float(ok), float(r.fun)))
                print(name, model, f"Omega_k={ok:+.4f} chi2={r.fun:.3f}", flush=True)
            c = np.array([x[1] for x in rows])
            flat_gap = float(c[list(OKS).index(0.0)] - ref[model])
            print(
                name,
                model,
                f"flat check: chi2(Omega_k=0) - committed flat fit = {flat_gap:+.4f}",
                flush=True,
            )
            assert abs(flat_gap) < 0.05, flat_gap
            j = int(np.argmin(c))
            a_, b_, _ = np.polyfit(
                OKS[max(j - 2, 0) : j + 3], c[max(j - 2, 0) : j + 3], 2
            )
            okb = float(-b_ / (2 * a_))
            sig = float(1 / math.sqrt(a_)) if a_ > 0 else None
            res[model] = {
                "grid": rows,
                "omega_k_best": okb,
                "omega_k_sigma": sig,
                "chi2_min_grid": float(c[j]),
                "flat_check_gap": flat_gap,
                "p_closed": (
                    None
                    if sig is None
                    else float(0.5 * math.erfc(okb / (sig * math.sqrt(2))))
                ),
            }
            print(
                name,
                model,
                {k: v for k, v in res[model].items() if k != "grid"},
                flush=True,
            )
        out[name] = res
    json.dump(out, open(cd.out("CEILING_CURVATURE.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
