#!/usr/bin/env python3
"""RY 2026-09-28 (honeycomb, the number 6): a neighbour version of the factorial counting law.
If every landing hands exactly one record to a randomly chosen one of its p neighbours, each cell receives
k ~ Binomial(p, 1/p) records: mean exactly one for any p (records out = records in), and the odds approach 1/(e k!)
as p -> infinity (the mu = 1 Poisson law of ceiling_factorial_law.py). With each record present with probability
s = r/r_f, the frozen fraction in w = -1 + g(s) is
  shifted (own landing + k records):   g(s) = s (1 - 1/p + s/p)^p
  truncated (k >= 1 records):          g(s) = ((1 - 1/p + s/p)^p - (1 - 1/p)^p) / (1 - (1 - 1/p)^p)
p = 6 is the hexagonal (honeycomb) tiling; p = 3 and 4 are the triangular and square tilings' edge neighbours.
No shape parameter is fitted. Fits: Omega_f = kappa, (h, omega_b) re-fit, Planck priors + DESI DR2 + each SN sample.
Usage: ceiling_honeycomb_law.py  (data: fetch_external_data.sh)   Output: CEILING_HONEYCOMB_LAW.json
"""

import json
import numpy as np
from scipy.optimize import minimize
import ceiling_model_cmb_bao_sn as m
import ceiling_factorial_law as cf
import cosmo_data as cd
from ceiling_model_bao_sn import load_bao
from ceiling_n_at_kappa import sn_likelihoods

cf.LAWS["binomial_shifted"] = lambda s, p: s * (1 - 1 / p + s / p) ** p
cf.LAWS["binomial_truncated"] = lambda s, p: (
    (1 - 1 / p + s / p) ** p - (1 - 1 / p) ** p
) / (1 - (1 - 1 / p) ** p)
POINTS = {
    "binomial_shifted": [3, 4, 6, 12],
    "binomial_truncated": [3, 4, 6, 12],
    "shifted_poisson": [1.0],
    "truncated_poisson": [1.0],
}  # mu = 1 Poisson = the p -> infinity limit


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
    for name, chi_sn in sn_likelihoods().items():

        def tot(p, law=None, q=None):
            if law is None:
                om, h, ob = p
            else:
                (h, ob), om = p, None
            if not (0.5 < h < 0.9 and 0.015 < ob < 0.03) or (
                om is not None and not 0.1 < om < 0.6
            ):
                return 3e9
            E, om0 = (
                m.make_E("lcdm", h, om) if law is None else cf.make_E_law(law, q, h)
            )
            return m.cmb_chi2(E, h, om0, ob)[0] + chi_bao(E, h, om0, ob) + chi_sn(E)

        fl = minimize(
            lambda p: tot(p), [0.31, 0.68, 0.02237], method="Nelder-Mead", options=cf.NM
        )
        out[name] = {"lcdm_chi2": fl.fun}
        for law, pts in POINTS.items():
            out[name][law] = []
            for q in pts:
                r = minimize(
                    lambda p: tot(p, law, q),
                    [0.68, 0.0225],
                    method="Nelder-Mead",
                    options=cf.NM,
                )
                w0, wa, _ = cf.w0_wa(law, q)
                out[name][law].append(
                    {
                        "p": q,
                        "chi2": float(r.fun),
                        "minus_lcdm": float(r.fun - fl.fun),
                        "w0": w0,
                        "wa": wa,
                    }
                )
                print(
                    name,
                    law,
                    f"p={q}: chi2-LCDM={r.fun - fl.fun:+.3f} w0={w0:.3f} wa={wa:.3f}",
                    flush=True,
                )
    json.dump(out, open(cd.out("CEILING_HONEYCOMB_LAW.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
