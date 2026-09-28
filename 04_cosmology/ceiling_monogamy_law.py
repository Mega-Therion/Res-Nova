#!/usr/bin/env python3
"""What monogamy of entanglement actually gives for the witness law (RY 2026-09-28: "there can be only one").
Premises (each marked in the O3 note):
  P1  a landing is one ebit (entropy ln 2);
  P2  monogamy: a maximally entangled qubit can share that entanglement with exactly one partner, so each landing
      hands its record to exactly one neighbour (one record out per landing) -- the record must be quantum, since
      classical records can be copied freely (quantum Darwinism);
  P3  a cell is one qubit, so it can hold at most one incoming record (capacity one);
  P4  the record goes to a random one of the p neighbours; if that cell already holds a record it is lost.
Derived: the fraction of cells that end up witnessed is q = 1 - (1 - 1/p)^p (p = 6: 0.665; p -> infinity: 1 - 1/e),
and the frozen fraction (own landing, plus the record if the cell was witnessed, each present with probability s) is
  g(s) = s (1 - q + q s).
Limits: q = 1 (records retried until delivered: a perfect matching) gives g = s^2, the n = 2 power law; q = 0 is the
glide. Unlike the uncapped honeycomb law (Binomial(p, 1/p), mean exactly one), capacity one makes the mean q < 1.
No shape parameter. Fits: Omega_f = kappa, (h, omega_b) re-fit, Planck priors + DESI DR2 + each SN sample.
Usage: ceiling_monogamy_law.py  (data: fetch_external_data.sh)   Output: CEILING_MONOGAMY_LAW.json
"""

import json, math
import numpy as np
from scipy.optimize import minimize
import ceiling_model_cmb_bao_sn as m
import ceiling_factorial_law as cf
import cosmo_data as cd
from ceiling_model_bao_sn import load_bao
from ceiling_n_at_kappa import sn_likelihoods

cf.LAWS["capacity_one"] = lambda s, q: s * (1 - q + q * s)


def six_neighbour_graph(L):
    """Cells of a honeycomb tiling (each hexagon has 6 neighbours: the triangular-lattice graph), periodic L x L."""
    idx = np.arange(L * L).reshape(L, L)
    shifts = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1))
    return np.stack(
        [np.roll(np.roll(idx, -dx, 0), -dy, 1).ravel() for dx, dy in shifts], 1
    )


def simulate_q(version, L=300, runs=5, seed=20260928):
    """Witnessed fraction by direct simulation. 'separate': each cell sends one record into a one-slot receiver of a
    random neighbour (first arrival kept). 'shared': one spare slot per cell used for both, so a record pairs two
    cells; cells act once, in random order, and a record aimed at a used slot is lost.
    """
    rng = np.random.default_rng(seed)
    nb = six_neighbour_graph(L)
    N = L * L
    out = []
    for _ in range(runs):
        if version == "separate":
            recv = np.zeros(N, bool)
            recv[nb[np.arange(N), rng.integers(6, size=N)]] = True
            out.append(recv.mean())
        else:
            free = np.ones(N, bool)
            picks = rng.integers(6, size=N)
            for i in rng.permutation(N):
                if free[i]:
                    j = nb[i, picks[i]]
                    if free[j]:
                        free[i] = free[j] = False
            out.append(1 - free.mean())
    return float(np.mean(out)), float(np.std(out))


Q_SEP, Q_SEP_SD = simulate_q("separate")
Q_SHARED, Q_SHARED_SD = simulate_q("shared")
POINTS = {
    "honeycomb p=6": 1
    - (5 / 6) ** 6,  # separate send/receive slots: closed form (simulation: Q_SEP)
    "p -> infinity": 1 - math.exp(-1),
    "shared slot, pairing, p=6 (simulated)": Q_SHARED,
    "perfect matching": 1.0,
}


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
        "law": "g(s) = s (1 - q + q s)",
        "q_values": POINTS,
        "q_simulation_mean_sd": {
            "separate send/receive slots": [Q_SEP, Q_SEP_SD],
            "shared slot (pairing)": [Q_SHARED, Q_SHARED_SD],
        },
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
        for label, q in POINTS.items():
            r = minimize(
                lambda p: tot(p, "capacity_one", q),
                [0.68, 0.0225],
                method="Nelder-Mead",
                options=cf.NM,
            )
            w0, wa, _ = cf.w0_wa("capacity_one", q)
            out[name][label] = {
                "q": q,
                "chi2": float(r.fun),
                "minus_lcdm": float(r.fun - fl.fun),
                "w0": w0,
                "wa": wa,
            }
            print(
                name,
                label,
                f"q={q:.4f}: chi2-LCDM={r.fun - fl.fun:+.3f} w0={w0:.3f} wa={wa:.3f}",
                flush=True,
            )
    json.dump(out, open(cd.out("CEILING_MONOGAMY_LAW.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
