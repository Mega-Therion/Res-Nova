#!/usr/bin/env python3
"""Post-hoc wide-binary chi^2 with orbit speeds from the energy integral.

The frozen pipeline multiplies each Monte Carlo velocity by sqrt(Gamma) at the
current radius. Here Gamma(r) is integrated to Phi, and the speed on the orbit
with the same periapsis and apoapsis replaces that factor. Action form only.
This is not a new pre-registration. Output: TIDAL_WB_ORBIT_CHI2.json
"""

import json
import sys

import numpy as np

import tidal_screening_wide_binary_rs as RS
import wide_binary_final as W
import wide_binary_fish as F

KEYS = [f"action|{ge}" for ge in RS.GES]
RNODE = np.array(RS.TAB["forms"]["action"]["r_kau"])
# Phi_l(M, r, q) such that Phi = sum Phi_l P_l(mu). GM = 1, r in kAU.
PHI = {}


def _integrate(cl):
    """cl (M, r, q) -> Phi with Phi(r_last) = -cl_last/r_last and inward integral."""
    r = RNODE
    acc = cl / r[None, :, None] ** 2
    dr = np.diff(r)
    piece = 0.5 * (acc[:, 1:, :] + acc[:, :-1, :]) * dr[None, :, None]
    integ = np.cumsum(piece[:, ::-1, :], axis=1)[:, ::-1, :]
    tail = cl[:, -1, :] / r[-1]
    Phi = np.empty_like(cl)
    Phi[:, :-1, :] = -(integ + tail[:, None, :])
    Phi[:, -1, :] = -tail
    return Phi


def build_phi():
    for key in KEYS:
        form, ge = key.split("|")
        Gr = np.array(RS.TAB["forms"][form][ge]["Gamma_r"])  # (M, r, q, mu)
        cl = (
            np.einsum("...k,lk,k->...l", Gr, RS.PL, RS.WMU)
            * (2 * np.arange(RS.LMAX) + 1)
            / 2
        )
        PHI[key] = [_integrate(cl[..., l]) for l in range(RS.LMAX)]


def eval_phi(key, M, q1, mu, r_kau):
    """Phi at physical radii r_kau (kAU), one value per draw."""
    ax = RS.AXES[key]
    pts = np.stack(
        [
            np.clip(np.log(M), ax[0][0], ax[0][-1]),
            np.clip(np.log(r_kau), np.log(RNODE[0]), np.log(RNODE[-1])),
            np.clip(q1, ax[2][0], ax[2][-1]),
        ],
        -1,
    )
    # log-r interpolation: the stored Phi is on linear r nodes, queried in log r
    # by rebuilding the interpolator axes as (log M, log r, q).
    P = np.polynomial.legendre.legvander(mu, RS.LMAX - 1)
    acc = 0
    for l in range(RS.LMAX):
        acc = acc + PHI_IP[key][l](pts) * P[:, l]
    r = np.clip(r_kau, 1e-8, None)
    below = r_kau < RNODE[0]
    above = r_kau > RNODE[-1]
    # 1/r tails using Gamma = -r Phi near the edge, evaluated at the edge
    return acc, below, above


PHI_IP = {}


def build_interp():
    ax = (np.log(RS.TAB["M_sun"]), np.log(RNODE), np.array(RS.TAB["q1"]))
    from scipy.interpolate import RegularGridInterpolator

    for key in KEYS:
        PHI_IP[key] = [
            RegularGridInterpolator(
                ax, PHI[key][l], bounds_error=False, fill_value=None
            )
            for l in range(RS.LMAX)
        ]


def phi_at(key, M, q1, mu, r_kau):
    val, below, above = eval_phi(key, M, q1, mu, np.clip(r_kau, RNODE[0], RNODE[-1]))
    # correct the outside using the edge value's implied Gamma
    if np.any(below):
        edge, _, _ = eval_phi(key, M, q1, mu, np.full(len(M), RNODE[0]))
        g = -edge * RNODE[0]
        val = np.where(
            below, edge - g * (1 / np.maximum(r_kau, 1e-8) - 1 / RNODE[0]), val
        )
    if np.any(above):
        edge, _, _ = eval_phi(key, M, q1, mu, np.full(len(M), RNODE[-1]))
        g = -edge * RNODE[-1]
        val = np.where(above, -g / np.maximum(r_kau, 1e-8), val)
    return val


def kepler_with_e(n, gamma):
    e = np.minimum(F.RNG.random(n) ** (1 / (gamma + 1)), 0.999)
    Mn = F.RNG.random(n) * 2 * np.pi
    E = Mn.copy()
    for _ in range(30):
        E -= (E - e * np.sin(E) - Mn) / (1 - e * np.cos(E))
    den = 1 - e * np.cos(E)
    pos = np.stack([np.cos(E) - e, np.sqrt(1 - e**2) * np.sin(E), np.zeros(n)], -1)
    vel = np.stack(
        [-np.sin(E) / den, np.sqrt(1 - e**2) * np.cos(E) / den, np.zeros(n)], -1
    )
    qv = F.RNG.normal(size=(n, 4))
    qv /= np.linalg.norm(qv, axis=1)[:, None]
    w, x, y, z = qv.T
    R = np.stack(
        [
            np.stack(
                [1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)], -1
            ),
            np.stack(
                [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)], -1
            ),
            np.stack(
                [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)], -1
            ),
        ],
        1,
    )
    P = np.einsum("nij,nj->ni", R, pos)
    Vv = np.einsum("nij,nj->ni", R, vel)
    return np.hypot(P[:, 0], P[:, 1]), np.linalg.norm(pos, axis=1), Vv[:, :2], e


def factor(key, a_au, e, r_au, M, q1, mu):
    a = np.maximum(a_au / 1e3, 1e-8)
    r = np.maximum(r_au / 1e3, 1e-6)
    rp = a * (1 - e)
    ra = a * (1 + e)
    Pr = phi_at(key, M, q1, mu, r)
    Pp = phi_at(key, M, q1, mu, rp)
    Pa = phi_at(key, M, q1, mu, ra)
    L2 = 2 * (Pa - Pp) / np.maximum(1 / rp**2 - 1 / ra**2, 1e-30)
    E = Pp + L2 / (2 * rp**2)
    v2 = np.maximum(2 * (E - Pr), 0)
    vk2 = np.maximum(2 / r - 1 / a, 1e-30)
    return np.sqrt(v2 / vk2)


def simulate_orbit(b, key, nmc, noise=True):
    n = len(b["s"])
    idx = np.repeat(np.arange(n), nmc)
    s, M, q1, sig = b["s"][idx], b["M"][idx], b["q1"][idx], b["sig"][idx]
    rsky, r3, vsky, e = kepler_with_e(len(idx), F.gamma_of_s(s))
    vt = vsky * np.sqrt(np.maximum(rsky, 1e-8))[:, None]
    a_au = s / np.maximum(rsky, 1e-8)
    r_au = a_au * r3
    mu = F.RNG.uniform(-1, 1, len(idx))
    fac = np.empty(len(idx))
    for i in range(0, len(idx), 20000):
        sl = slice(i, i + 20000)
        fac[sl] = factor(key, a_au[sl], e[sl], r_au[sl], M[sl], q1[sl], mu[sl])
    vt = vt * fac[:, None]
    if noise:
        vt = vt + F.RNG.normal(size=vt.shape) * sig[:, None]
    return np.hypot(vt[:, 0], vt[:, 1]), idx


def main(npz):
    build_phi()
    build_interp()
    # constant-Gamma check at large separation, where the table is flat
    M = np.array([1.0, 1.0])
    q = np.array([0.5, 0.5])
    mu = np.array([0.0, 0.0])
    a = np.array([80e3, 80e3])
    e = np.array([0.3, 0.5])
    r = a * (1 - e**2) / (1 + e * 0)  # true anomaly 90 deg-ish, just a point inside
    r = np.array([70e3, 60e3])
    f = factor(KEYS[0], a, e, r, M, q, mu)
    g = RS.boost_new(KEYS[0], M, r, q, mu)
    print("flat-region factor", f, "sqrtGamma", np.sqrt(np.maximum(g, 0)), flush=True)
    c = dict(np.load(npz))
    F.RNG = np.random.default_rng(20261004)
    S = {}
    for cut in ("clean", "loose"):
        b = F.prepare(c, F.CUTS[cut])
        print(cut, "setup", len(b["s"]), flush=True)
        S[cut] = dict(b=b, st=W.setup(b))
    for key in KEYS:
        for cut in ("clean", "loose"):
            b = S[cut]["b"]
            F.RNG = np.random.default_rng(20261016)
            for _, bins in S[cut]["st"]:
                for bj in bins:
                    if bj is None:
                        continue
                    sub = {k: v[bj["mask"]] for k, v in b.items()}
                    bj["models"][key] = W.fit_alpha(
                        simulate_orbit(sub, key, nmc=W.NM)[0],
                        bj["pdf"],
                        bj["cdf"],
                        fix_c=True,
                    )[0]
            print(cut, key, "curve done", flush=True)
    W.MODELS = list(W.MODELS) + KEYS
    out = {
        "note": "post-hoc energy-integral speeds; action form; not the pre-registered pipeline"
    }
    for cut in ("clean", "loose"):
        rows, chi2 = W.measure(S[cut]["b"]["vt"], S[cut]["st"])
        out[cut] = {
            "n": len(S[cut]["b"]["s"]),
            "chi2": chi2,
            "rows": [
                {
                    "bin": r["bin"],
                    "R": r["R"],
                    "sigma": r["sigma"],
                    "models": {m: r["models"][m] for m in ("N",) + tuple(KEYS)},
                }
                for r in rows
            ],
        }
        print(cut, {k: round(chi2[k], 3) for k in ("N",) + tuple(KEYS)}, flush=True)
    # C3: 40 injections per model per cut. kappa = median(null chi2) / 3.357.
    # Excluded only if both cuts have calibrated chi2 > 18.5 and raw chi2 > null maximum.
    for key in KEYS:
        for cut in ("clean", "loose"):
            null, z_n = [], []
            for i in range(W.NINJ):
                F.RNG = np.random.default_rng(
                    900000
                    + 1000 * KEYS.index(key)
                    + i
                    + (0 if cut == "clean" else 500000)
                )
                vt, _ = simulate_orbit(S[cut]["b"], key, nmc=1)
                ncont = int(0.05 * len(vt))
                j = F.RNG.choice(len(vt), ncont, replace=False)
                vt[j] = F.VMAX * np.sqrt(F.RNG.random(ncont))
                _, chi = W.measure(vt, S[cut]["st"])
                null.append(chi[key])
                z_n.append(np.sqrt(max(0.0, chi["N"] - chi[key])))
            med = float(np.median(null))
            kappa = med / W.CHI2_4_MEDIAN
            raw = out[cut]["chi2"][key]
            out[cut].setdefault("calibration", {})[key] = {
                "null_median": med,
                "null_max": float(np.max(null)),
                "kappa": float(kappa),
                "chi2_calibrated": float(raw / kappa),
                "Z_N": float(np.median(z_n)),
                "n_inj": len(null),
            }
            print(
                cut,
                key,
                "cal",
                round(raw / kappa, 2),
                "null_max",
                round(max(null), 2),
                "Z_N",
                round(float(np.median(z_n)), 2),
                flush=True,
            )
    out["excluded_C3"] = {
        key: all(
            out[cut]["calibration"][key]["chi2_calibrated"] > 18.5
            and out[cut]["chi2"][key] > out[cut]["calibration"][key]["null_max"]
            for cut in ("clean", "loose")
        )
        for key in KEYS
    }
    out["verdict"] = (
        "EXCLUDED at both external fields"
        if all(out["excluded_C3"].values())
        else "NOT EXCLUDED"
    )
    print("excluded", out["excluded_C3"], out["verdict"], flush=True)
    json.dump(out, open("TIDAL_WB_ORBIT_CHI2.json", "w"), indent=1)
    print("wrote TIDAL_WB_ORBIT_CHI2.json", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
