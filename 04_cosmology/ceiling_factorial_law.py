#!/usr/bin/env python3
"""RY 2026-09-28, 'how about n factorial': a counting law for the approach to the dark-energy ceiling.
If landings arrive at random, the chance of k extra landings is mu^k e^-mu / k! (Poisson). If a unit of dark energy
freezes (w -> 0) only once its required landings are all present, each with probability s = r/r_f, the frozen
fraction g(s) replaces the power law s^n of ceiling_model_cmb_bao_sn.py:
  shifted Poisson (1 + k landings, k ~ Poisson(mu)):  g(s) = s exp(-mu (1 - s))
  zero-truncated Poisson (k >= 1 landings):          g(s) = (e^(mu s) - 1) / (e^mu - 1)
mu = 0 is the glide (n = 1) in both; mu = 1 gives weights exactly proportional to 1/k!.
The share obeys d ln r / d ln a = 3 (1 - g(s)), solved by quadrature in u = ln s: tau(u) = int du / (3 (1 - g)).
Validation: the quadrature with g = s^n must reproduce the closed-form ceiling E(z).
Fits: Omega_f = kappa, (h, omega_b) re-fit, Planck distance priors + DESI DR2 BAO + Pantheon+ or DES-Y5.
RY, same night, 'maybe its 1/137 cells per witness': mu = alpha (one witness per 137 cells) and mu = 1/alpha
(137 witnesses per cell) are evaluated as named points for both Poisson laws.
Usage: ceiling_factorial_law.py  (data: fetch_external_data.sh)   Output: CEILING_FACTORIAL_LAW.json
"""

import json, math
from scipy.constants import fine_structure
import numpy as np
from scipy.optimize import minimize
import ceiling_model_cmb_bao_sn as m
import cosmo_data as cd
from ceiling_model_bao_sn import load_bao
from ceiling_n_at_kappa import sn_likelihoods

NM = {"xatol": 1e-6, "fatol": 1e-4, "maxiter": 4000}
NAMED = {"alpha": fine_structure, "inverse_alpha": 1 / fine_structure}
LAWS = {
    "power": lambda s, p: s**p,
    "shifted_poisson": lambda s, p: s * np.exp(-p * (1 - s)),
    "truncated_poisson": lambda s, p: s if p == 0 else np.expm1(p * s) / np.expm1(p),
}
GRIDS = {
    "power": [1.0, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.5, 1.6],
    "shifted_poisson": [
        0.0,
        0.25,
        0.5,
        0.75,
        1.0,
        1.25,
        1.5,
        2.0,
        2.5,
        3.0,
        4.0,
        5.0,
        6.0,
        8.0,
    ],
    "truncated_poisson": [
        0.0,
        0.25,
        0.5,
        0.75,
        1.0,
        1.25,
        1.5,
        2.0,
        2.5,
        3.0,
        4.0,
        5.0,
        6.0,
        8.0,
    ],
}


def make_E_law(law, p, h, of=m.KAPPA):
    orad = m.OR / h**2
    om0 = 1 - m.LN2 - orad
    r0 = m.LN2 / om0
    rf = of / (1 - of)
    s0 = r0 / rf
    u = np.linspace(
        math.log(s0) - 75.0, math.log(s0), 60001
    )  # early g ~ 0, so 75 in u ~ 25 e-folds of a
    f = 1.0 / (3.0 * (1.0 - LAWS[law](np.exp(u), p)))
    tau = np.concatenate(([0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(u))))
    tau -= tau[-1]  # tau = ln a

    def E(z):
        r = rf * np.exp(np.interp(-np.log1p(z), tau, u))
        return np.sqrt(orad * (1 + z) ** 4 + om0 * (1 + z) ** 3 * (1 + r))

    return E, om0


def w0_wa(law, p, h=0.68, of=m.KAPPA):
    om0 = 1 - m.LN2 - m.OR / h**2
    s0 = (m.LN2 / om0) / (of / (1 - of))
    g = lambda s: LAWS[law](s, p)
    g0 = g(s0)
    dg = (g(s0 * 1.000001) - g(s0 * 0.999999)) / (2e-6 * s0)
    return (
        -1 + g0,
        -3 * s0 * dg * (1 - g0),
        s0 * dg / g0,
    )  # w0, wa, local exponent d ln g / d ln s


def main():
    zt = np.concatenate([np.linspace(0, 3, 301), np.geomspace(3.01, 1100, 300)])
    val = {}
    for n in (1.0, 1.25, 2.0):
        Eq, _ = make_E_law("power", n, 0.68)
        Ec, _ = m.make_E("ceil", 0.68, None, m.KAPPA, n)
        val[f"n={n}"] = float(np.max(np.abs(Eq(zt) / Ec(zt) - 1)))
    print("quadrature vs closed form, max |dE/E|:", val, flush=True)
    assert max(val.values()) < 1e-6
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
        "validation_max_rel_dE": val,
    }
    for name, chi_sn in sn_likelihoods().items():

        def tot(p, law=None, mu=None):
            if law is None:
                om, h, ob = p
            else:
                (h, ob), om = p, None
            if not (0.5 < h < 0.9 and 0.015 < ob < 0.03) or (
                om is not None and not 0.1 < om < 0.6
            ):
                return 3e9
            E, om0 = m.make_E("lcdm", h, om) if law is None else make_E_law(law, mu, h)
            return m.cmb_chi2(E, h, om0, ob)[0] + chi_bao(E, h, om0, ob) + chi_sn(E)

        fl = minimize(
            lambda p: tot(p), [0.31, 0.68, 0.02237], method="Nelder-Mead", options=NM
        )
        out[name] = {"lcdm_chi2": fl.fun}
        for law, grid in GRIDS.items():
            rows = []
            start = [0.68, 0.0225]
            for mu in grid:
                r = minimize(
                    lambda p: tot(p, law, mu), start, method="Nelder-Mead", options=NM
                )
                start = list(r.x)
                w0, wa, nloc = w0_wa(law, mu)
                rows.append(
                    {
                        "p": mu,
                        "chi2": float(r.fun),
                        "minus_lcdm": float(r.fun - fl.fun),
                        "h": float(r.x[0]),
                        "w0": w0,
                        "wa": wa,
                        "local_exponent_today": nloc,
                    }
                )
                print(
                    name,
                    law,
                    f"p={mu}: chi2-LCDM={r.fun - fl.fun:+.3f}  w0={w0:.3f} wa={wa:.3f} n_loc={nloc:.3f}",
                    flush=True,
                )
            c = np.array([x["chi2"] for x in rows])
            j = int(np.argmin(c))
            ok = [x["p"] for x in rows if x["chi2"] - c[j] <= 1.0]
            out[name][law] = {
                "grid": rows,
                "p_best_grid": rows[j]["p"],
                "best_minus_lcdm": rows[j]["minus_lcdm"],
                "p_within_1sigma_grid": [min(ok), max(ok)],
            }
            if law != "power":
                out[name][law]["named"] = {}
                for key, mu in NAMED.items():
                    r = minimize(lambda p: tot(p, law, mu), [0.68, 0.0225], method="Nelder-Mead", options=NM)
                    w0, wa, _ = w0_wa(law, mu)
                    out[name][law]["named"][key] = {"p": mu, "chi2": float(r.fun), "minus_lcdm": float(r.fun - fl.fun),
                                                    "minus_best_grid": float(r.fun - c[j]), "w0": w0, "wa": wa}
                    print(name, law, key, out[name][law]["named"][key], flush=True)
    json.dump(out, open(cd.out("CEILING_FACTORIAL_LAW.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
