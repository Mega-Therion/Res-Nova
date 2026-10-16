#!/usr/bin/env python3
"""Wide-binary R(s) for the tidal screen with energy-integral orbit speeds (post-hoc, not pre-registered).

The frozen pipeline scales each Monte Carlo velocity by sqrt(Gamma) at the current radius (the local-force step,
TIDAL_LOCAL_FORCE_CHECK.json). Here each draw's speed comes from energy conservation instead. The draw's Kepler orbit
keeps its periapsis and apoapsis, the potential is built from the action-form table, and the speed is evaluated at
the draw's current radius. The approach follows Grok's tidal_wb_orbit_chi2.py. The Kepler part of the potential is
taken exactly (Phi = -1/r + dPhi, GM = 1, r in kAU), and only the residual is integrated and interpolated:

    dPhi_l(r) = -Int_r^inf (c_l(s) - delta_l0) / s^2 ds,   with c_l the Legendre components of Gamma_r(mu),

on a fine log-r grid (20,000 points), with c_l linear in log r between table nodes. Outside the table
(0.2-400 kAU), c_l keeps its edge value (Gamma = 1 to 1e-6 at 0.2 kAU). One mu is used per draw, as in the
local-force pipeline.

Gates: Gamma = 1 gives a factor of exactly 1; a constant Gamma gives sqrt(Gamma) (to 1e-4: the residual is linear
between fine-grid points); with the orientation average only,
the orbit-mean speed ratio matches the independent tidal_local_force_check.py. C3 calibration uses 40 injections per
key and cut, as in wide_binary_final.
Usage: tidal_wb_orbit_speed_check.py <eb21_cols.npz>     Output: TIDAL_WB_ORBIT_SPEED_CHECK.json
"""
import json
import sys

import numpy as np
from scipy.interpolate import RegularGridInterpolator

import tidal_screening_wide_binary_rs as RS
import wide_binary_fish as F
import wide_binary_final as W

KEYS = [f"action|{ge}" for ge in RS.GES]
RN = np.array(RS.TAB["forms"]["action"]["r_kau"])
UN = np.log(RN)
UF = np.linspace(UN[0], UN[-1], 20000)
AX = (np.log(RS.TAB["M_sun"]), UF, np.array(RS.TAB["q1"]))
DPHI, FEDGE = {}, {}


def residual_potential(cl, l):
    """cl (M, r_nodes, q) -> dPhi_l on (M, UF, q), and f_l at both table edges (M, q)."""
    f = cl - (1.0 if l == 0 else 0.0)
    fi = np.stack([[np.interp(UF, UN, f[a, :, b]) for b in range(f.shape[2])] for a in range(f.shape[0])])  # (M, q, UF)
    g = fi * np.exp(-UF)[None, None, :]                       # integrand in u: f e^{-u}
    seg = 0.5 * (g[..., 1:] + g[..., :-1]) * np.diff(UF)
    inner = np.concatenate([np.cumsum(seg[..., ::-1], axis=-1)[..., ::-1], np.zeros(g.shape[:-1] + (1,))], axis=-1)
    tail = fi[..., -1:] * np.exp(-UF[-1])                     # Int_{r_last}^inf f_last / s^2 ds
    return np.moveaxis(-(inner + tail), -1, 1), f[:, 0, :], f[:, -1, :]   # (M, UF, q), (M, q), (M, q)


def build(table=None):
    tab = RS.TAB if table is None else table
    for key in KEYS:
        form, ge = key.split("|")
        Gr = np.array(tab["forms"][form][ge]["Gamma_r"])      # (M, r, q, mu)
        cl = np.einsum("...k,lk,k->...l", Gr, RS.PL, RS.WMU) * (2 * np.arange(RS.LMAX) + 1) / 2
        DPHI[key], FEDGE[key] = [], []
        for l in range(RS.LMAX):
            dp, f0, f1 = residual_potential(cl[..., l], l)
            DPHI[key].append(RegularGridInterpolator(AX, dp))
            FEDGE[key].append((RegularGridInterpolator((AX[0], AX[2]), f0), RegularGridInterpolator((AX[0], AX[2]), f1)))


def phi(key, M, q1, mu, r, l0_only=False):
    """Phi in units GM = 1, r in kAU (arrays of equal length). l0_only: the orientation-averaged part alone."""
    rr = np.maximum(r, 1e-9)
    u = np.log(rr)
    lm, qq = np.clip(np.log(M), AX[0][0], AX[0][-1]), np.clip(q1, AX[2][0], AX[2][-1])
    pts = np.stack([lm, np.clip(u, UF[0], UF[-1]), qq], -1)
    P = np.polynomial.legendre.legvander(mu, RS.LMAX - 1)
    ls = [0] if l0_only else range(RS.LMAX)
    d = sum(DPHI[key][l](pts) * P[:, l] for l in ls)
    mq = np.stack([lm, qq], -1)
    r0, r1 = np.exp(UF[0]), np.exp(UF[-1])
    lo, hi = rr < r0, rr > r1
    if np.any(lo):                                            # below: c_l = edge value, dPhi_l += -f_l0 (1/r - 1/r0)
        d = d - np.where(lo, sum(FEDGE[key][l][0](mq) * P[:, l] for l in ls) * (1 / rr - 1 / r0), 0.0)
    if np.any(hi):                                            # above: dPhi_l(r) = dPhi_l(r1) r1 / r
        pts_e = pts.copy(); pts_e[:, 1] = UF[-1]
        d_e = sum(DPHI[key][l](pts_e) * P[:, l] for l in ls)
        d = np.where(hi, d_e * r1 / rr, d)
    return -1.0 / rr + d


def factor(key, a, e, r, M, q1, mu, l0_only=False):
    """Energy-integral speed over Kepler speed at radius r, for the orbit with the Kepler periapsis and apoapsis."""
    rp, ra = a * (1 - e), a * (1 + e)
    ph = lambda x: phi(key, M, q1, mu, x, l0_only)
    Pp, Pa, Pr = ph(rp), ph(ra), ph(r)
    den = 1 / rp**2 - 1 / ra**2
    circ = den < 1e-6 / rp**2
    h = 1e-4 * rp
    dphi = (ph(rp + h) - ph(rp - h)) / (2 * h)
    L2 = np.where(circ, rp**3 * dphi, 2 * (Pa - Pp) / np.where(circ, 1.0, den))
    E = Pp + L2 / (2 * rp**2)
    v2 = np.maximum(2 * (E - Pr), 0)
    vk2 = np.maximum(2 / r - 1 / a, 1e-30)
    return np.sqrt(v2 / vk2)


def kepler_with_e(n, gamma):
    """wide_binary_fish.kepler_mc, also returning e and a (same RNG calls, same order)."""
    e = np.minimum(F.RNG.random(n) ** (1 / (gamma + 1)), 0.999)
    Mn = F.RNG.random(n) * 2 * np.pi
    E = Mn.copy()
    for _ in range(30):
        E -= (E - e * np.sin(E) - Mn) / (1 - e * np.cos(E))
    den = 1 - e * np.cos(E)
    pos = np.stack([np.cos(E) - e, np.sqrt(1 - e**2) * np.sin(E), np.zeros(n)], -1)
    vel = np.stack([-np.sin(E) / den, np.sqrt(1 - e**2) * np.cos(E) / den, np.zeros(n)], -1)
    qv = F.RNG.normal(size=(n, 4))
    qv /= np.linalg.norm(qv, axis=1)[:, None]
    w, x, y, z = qv.T
    R = np.stack([np.stack([1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)], -1),
                  np.stack([2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)], -1),
                  np.stack([2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)], -1)], 1)
    P = np.einsum("nij,nj->ni", R, pos)
    Vv = np.einsum("nij,nj->ni", R, vel)
    return np.hypot(P[:, 0], P[:, 1]), np.linalg.norm(pos, axis=1), Vv[:, :2], e


def simulate_orbit(b, key, nmc, noise=True):
    n = len(b["s"])
    idx = np.repeat(np.arange(n), nmc)
    s, M, q1, sig = b["s"][idx], b["M"][idx], b["q1"][idx], b["sig"][idx]
    rsky, r3, vsky, e = kepler_with_e(len(idx), F.gamma_of_s(s))
    vt = vsky * np.sqrt(rsky)[:, None]
    a = (s / rsky) / 1e3                                      # kAU
    mu = F.RNG.uniform(-1, 1, len(idx))
    fac = np.empty(len(idx))
    for i in range(0, len(idx), 50000):
        sl = slice(i, i + 50000)
        fac[sl] = factor(key, a[sl], e[sl], a[sl] * r3[sl], M[sl], q1[sl], mu[sl])
    vt = vt * fac[:, None]
    if noise:
        vt = vt + F.RNG.normal(size=vt.shape) * sig[:, None]
    return np.hypot(vt[:, 0], vt[:, 1]), idx


def gates():
    out = {}
    one = json.loads(json.dumps(RS.TAB))
    for key in KEYS:
        form, ge = key.split("|")
        G = np.array(one["forms"][form][ge]["Gamma_r"])
        one["forms"][form][ge]["Gamma_r"] = np.ones_like(G).tolist()
    build(one)
    rng = np.random.default_rng(1)
    n = 20000
    M, q, mu = rng.uniform(0.3, 2.4, n), rng.uniform(0.5, 0.8, n), rng.uniform(-1, 1, n)
    a, e = np.exp(rng.uniform(np.log(0.3), np.log(300), n)), rng.uniform(0, 0.99, n)
    r = a * (1 - e * np.cos(rng.uniform(0, 2 * np.pi, n)))
    f1 = factor(KEYS[0], a, e, r, M, q, mu)
    out["G1_gamma1_max_abs_factor_minus_1"] = float(np.max(np.abs(f1 - 1)))
    for key in KEYS:
        form, ge = key.split("|")
        one["forms"][form][ge]["Gamma_r"] = (1.088 * np.ones_like(np.array(one["forms"][form][ge]["Gamma_r"]))).tolist()
    build(one)
    f2 = factor(KEYS[0], a, e, r, M, q, mu)
    out["G2_const_gamma_max_rel_dev_from_sqrt"] = float(np.max(np.abs(f2 / np.sqrt(1.088) - 1)))
    build()
    lf = json.load(open("TIDAL_LOCAL_FORCE_CHECK.json"))
    t = RS.TAB
    devs = []
    for ge in RS.GES:
        key = f"action|{ge}"
        G = np.array(t["forms"]["action"][ge]["Gamma_r_orientation_avg"])[:, :, 0]
        lm = np.log(np.array(t["M_sun"])); w = (0.0 - lm[2]) / (lm[3] - lm[2])
        g1 = (1 - w) * G[2] + w * G[3]                          # M = 1, q1 = 0.5, as in the local-force check
        for row in lf[ge]:
            ak, ee = row["a_kau"], row["e"]
            rp, ra = ak * (1 - ee), ak * (1 + ee)
            x = np.geomspace(rp * 1.0001, ra * 0.9999, 400)
            m = len(x)
            fac = factor(key, np.full(m, ak), np.full(m, ee), x, np.full(m, 1.0), np.full(m, 0.5), np.zeros(m), l0_only=True)
            gam = np.interp(np.log(x), UN, g1)
            rel = fac / np.sqrt(gam) - 1                       # energy-integral speed over local-force speed
            ph = phi(key, np.full(m, 1.0), np.full(m, 0.5), np.zeros(m), x, True)
            Pp = phi(key, np.ones(1), np.full(1, 0.5), np.zeros(1), np.array([rp]), True)[0]
            Pa = phi(key, np.ones(1), np.full(1, 0.5), np.zeros(1), np.array([ra]), True)[0]
            L2 = 2 * (Pa - Pp) / (1 / rp**2 - 1 / ra**2)
            E = Pp + L2 / (2 * rp**2)
            vr = np.sqrt(np.maximum(2 * (E - ph) - L2 / x**2, 1e-30))
            devs.append(abs(float(np.sum(rel / vr) / np.sum(1 / vr)) - row["time_weighted_mean_dv_over_v"]))
    out["G3_orbit_mean_vs_local_force_check_max_abs"] = max(devs)
    ok = (out["G1_gamma1_max_abs_factor_minus_1"] < 1e-6 and out["G2_const_gamma_max_rel_dev_from_sqrt"] < 1e-4
          and out["G3_orbit_mean_vs_local_force_check_max_abs"] < 2e-3)
    for k, v in out.items():
        print(f"{k}: {v:.3e}")
    return ok, out


def main(npz):
    ok, gate_out = gates()
    print("GATES", "PASS" if ok else "FAIL", flush=True)
    if not ok:
        sys.exit(1)
    c = dict(np.load(npz))
    F.RNG = np.random.default_rng(20261004)
    S = {}
    for cut in ("clean", "loose"):
        b = F.prepare(c, F.CUTS[cut])
        S[cut] = dict(b=b, st=W.setup(b))
        print(cut, "setup", len(b["s"]), flush=True)
    for key in KEYS:
        for cut in ("clean", "loose"):
            F.RNG = np.random.default_rng(20261016 + KEYS.index(key))
            b = S[cut]["b"]
            for _, bins in S[cut]["st"]:
                for bj in bins:
                    if bj is None:
                        continue
                    sub = {k: v[bj["mask"]] for k, v in b.items()}
                    bj["models"][key] = W.fit_alpha(simulate_orbit(sub, key, nmc=W.NM)[0], bj["pdf"], bj["cdf"], fix_c=True)[0]
    W.MODELS = list(W.MODELS) + KEYS
    out = {"note": "post-hoc energy-integral speeds, Kepler part exact; action form; not pre-registered", "gates": gate_out}
    for cut in ("clean", "loose"):
        rows, chi2 = W.measure(S[cut]["b"]["vt"], S[cut]["st"])
        out[cut] = {"n": len(S[cut]["b"]["s"]), "chi2": {k: chi2[k] for k in ["N", "E", "S"] + KEYS},
                    "rows": [{"bin": r["bin"], "R": r["R"], "sigma": r["sigma"],
                              "models": {m: r["models"][m] for m in ["N"] + KEYS}} for r in rows]}
        print(cut, {k: round(v, 2) for k, v in out[cut]["chi2"].items()}, flush=True)
    for key in KEYS:
        for cut in ("clean", "loose"):
            null, zn = [], []
            for i in range(W.NINJ):
                F.RNG = np.random.default_rng(910000 + 1000 * KEYS.index(key) + i + (0 if cut == "clean" else 500000))
                vt, _ = simulate_orbit(S[cut]["b"], key, nmc=1)
                ncont = int(0.05 * len(vt))
                j = F.RNG.choice(len(vt), ncont, replace=False)
                vt[j] = F.VMAX * np.sqrt(F.RNG.random(ncont))
                _, ch = W.measure(vt, S[cut]["st"])
                null.append(ch[key])
                zn.append(np.sqrt(max(0.0, ch["N"] - ch[key])))
            kappa = float(np.median(null) / W.CHI2_4_MEDIAN)
            raw = out[cut]["chi2"][key]
            out[cut].setdefault("calibration", {})[key] = {"kappa": kappa, "null_max": float(np.max(null)),
                                                           "chi2_calibrated": raw / kappa, "Z_N": float(np.median(zn))}
            print(cut, key, out[cut]["calibration"][key], flush=True)
    out["excluded_C3"] = {k: all(out[c]["calibration"][k]["chi2_calibrated"] > 18.5 and out[c]["chi2"][k] > out[c]["calibration"][k]["null_max"]
                                 for c in ("clean", "loose")) for k in KEYS}
    print("excluded", out["excluded_C3"], flush=True)
    json.dump(out, open("TIDAL_WB_ORBIT_SPEED_CHECK.json", "w"), indent=1, default=float)


if __name__ == "__main__":
    main(sys.argv[1])
