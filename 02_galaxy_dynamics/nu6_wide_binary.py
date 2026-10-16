#!/usr/bin/env python3
"""nu6 wide binaries with energy-integral orbit speeds.

Protocol: PREREG_NU6_WIDE_BINARY_2026-10-16.md. Frozen a0, no retune.
Usage: python3 nu6_wide_binary.py <eb21_cols.npz>
"""

import json
import sys
from pathlib import Path

import numpy as np

import wide_binary_final as W
import wide_binary_fish as F

HERE = Path(__file__).resolve().parent
A0 = 1.1607e-10
GE_DECISION = 1.9e-10
GE_EXTRA = 2.32e-10
SEED = 20261016
RG = np.geomspace(5.0, 4.0e5, 96)
LN = np.log(RG)
DR = np.diff(RG)


def nu6(y):
    y = np.maximum(y, 1e-100)
    return (0.5 * (1.0 + np.sqrt(1.0 + 4.0 * y**-6.0))) ** (1.0 / 6.0)


def boost(gN, q1, mu, ge):
    """g/gN for external-field QUMOND with nu6. mu = cos(angle between gN and g_e)."""
    q = F.q_two_body(q1)
    gtx = gN + ge * mu
    gtp = ge * np.sqrt(np.maximum(1.0 - mu**2, 0.0))
    gtm = np.hypot(gtx, gtp)
    bE = (nu6(gtm / A0) * gtx - nu6(ge / A0) * ge * mu) / np.maximum(gN, 1e-30)
    return 1.0 + q * (bE - 1.0)


def _phi_batch(M, q1, mu, ge, newton=False):
    """Phi/(GM) on RG for each draw. Attractive Phi is negative."""
    gN = F.GN_1AU * M[:, None] / RG[None, :] ** 2
    if newton:
        b = np.ones_like(gN)
    else:
        b = boost(gN, q1[:, None], mu[:, None], ge)
    integ = b / RG[None, :] ** 2
    piece = 0.5 * (integ[:, 1:] + integ[:, :-1]) * DR
    c = np.cumsum(piece[:, ::-1], axis=1)[:, ::-1]
    tail = b[:, -1] / RG[-1]
    phi = np.empty_like(integ)
    phi[:, :-1] = -(c + tail[:, None])
    phi[:, -1] = -tail
    return phi


def _at(phi, rval):
    lr = np.log(np.clip(rval, RG[0], RG[-1]))
    j = np.clip(np.searchsorted(LN, lr) - 1, 0, len(RG) - 2)
    t = (lr - LN[j]) / (LN[j + 1] - LN[j])
    i = np.arange(len(rval))
    return phi[i, j] * (1 - t) + phi[i, j + 1] * t


def energy_factor(a_au, e, r_au, M, q1, mu, ge, newton=False):
    """v / v_Kepler from Phi between the same periapsis and apoapsis."""
    n = len(a_au)
    out = np.empty(n)
    rp = a_au * (1 - e)
    ra = a_au * (1 + e)
    for i0 in range(0, n, 3000):
        sl = slice(i0, i0 + 3000)
        phi = _phi_batch(M[sl], q1[sl], mu[sl], ge, newton=newton)
        pp, pa, pr = _at(phi, rp[sl]), _at(phi, ra[sl]), _at(phi, r_au[sl])
        l2 = 2 * (pa - pp) / np.maximum(1 / rp[sl] ** 2 - 1 / ra[sl] ** 2, 1e-30)
        energy = pp + l2 / (2 * rp[sl] ** 2)
        v2 = np.maximum(2 * (energy - pr), 0)
        vk2 = np.maximum(2 / r_au[sl] - 1 / a_au[sl], 1e-30)
        out[sl] = np.sqrt(v2 / vk2)
    return out


def draws(b, nmc):
    n = len(b["s"])
    idx = np.repeat(np.arange(n), nmc)
    s = b["s"][idx]
    e = np.minimum(F.RNG.random(len(idx)) ** (1 / (F.gamma_of_s(s) + 1)), 0.999)
    Mn = F.RNG.random(len(idx)) * 2 * np.pi
    E = Mn.copy()
    for _ in range(30):
        E -= (E - e * np.sin(E) - Mn) / (1 - e * np.cos(E))
    den = 1 - e * np.cos(E)
    pos = np.stack(
        [np.cos(E) - e, np.sqrt(1 - e**2) * np.sin(E), np.zeros(len(idx))], -1
    )
    vel = np.stack(
        [-np.sin(E) / den, np.sqrt(1 - e**2) * np.cos(E) / den, np.zeros(len(idx))], -1
    )
    qv = F.RNG.normal(size=(len(idx), 4))
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
    rsky = np.hypot(P[:, 0], P[:, 1])
    r3 = np.linalg.norm(pos, axis=1)
    vsky = Vv[:, :2]
    return idx, s, e, rsky, r3, vsky


def samples(b, kind, nmc, ge=GE_DECISION, noise=True):
    idx, s, e, rsky, r3, vsky = draws(b, nmc)
    vt = vsky * np.sqrt(np.maximum(rsky, 1e-8))[:, None]
    if kind != "N":
        a_au = s / np.maximum(rsky, 1e-8)
        r_au = a_au * r3
        mu = F.RNG.uniform(-1, 1, len(idx))
        fac = energy_factor(
            a_au, e, r_au, b["M"][idx], b["q1"][idx], mu, ge, newton=False
        )
        vt = vt * fac[:, None]
    if noise:
        vt = vt + F.RNG.normal(size=vt.shape) * b["sig"][idx][:, None]
    return np.hypot(vt[:, 0], vt[:, 1])


def newton_self_check():
    rng = np.random.default_rng(1)
    n = 300
    a = rng.uniform(800, 20000, n)
    e = rng.uniform(0.05, 0.8, n)
    # true anomaly 1 rad
    r = a * (1 - e**2) / (1 + e * np.cos(1.0))
    M = rng.uniform(0.4, 2.0, n)
    q1 = rng.uniform(0.3, 0.7, n)
    mu = rng.uniform(-1, 1, n)
    fac = energy_factor(a, e, r, M, q1, mu, GE_DECISION, newton=True)
    err = float(np.max(np.abs(fac - 1)))
    print(f"newton energy factor max |f-1| = {err:.3e}", flush=True)
    if err > 0.02:
        raise SystemExit("Newton energy integral failed the vis-viva check")


def build(b):
    """Templates and model alphas. Models: N, nu6 at the decision field, nu6 at 2.32e-10."""
    keys = ("N", "nu6", "nu6_2.32")
    out = []
    for name, lo_m, hi_m in W.STRATA:
        ms = (b["M"] >= lo_m) & (b["M"] < hi_m)
        bins = []
        for lo, hi in F.BINS:
            m = ms & (b["s"] >= lo) & (b["s"] < hi)
            if m.sum() < W.NMIN:
                bins.append(None)
                continue
            sub = {k: v[m] for k, v in b.items()}
            pdf, cdf = F.template(samples(sub, "N", W.NT))
            mods = {
                "N": W.fit_alpha(samples(sub, "N", W.NM), pdf, cdf, fix_c=True)[0],
                "nu6": W.fit_alpha(
                    samples(sub, "nu6", W.NM, GE_DECISION), pdf, cdf, fix_c=True
                )[0],
                "nu6_2.32": W.fit_alpha(
                    samples(sub, "nu6", W.NM, GE_EXTRA), pdf, cdf, fix_c=True
                )[0],
            }
            bins.append(dict(mask=m, pdf=pdf, cdf=cdf, models=mods))
            print(
                name,
                lo,
                hi,
                int(m.sum()),
                {k: round(v, 4) for k, v in mods.items()},
                flush=True,
            )
        out.append((name, bins))
    return keys, out


def measure(vt, st, keys):
    saved = W.MODELS
    W.MODELS = list(keys)
    try:
        rows, chi2 = W.measure(vt, st)
    finally:
        W.MODELS = saved
    return rows, chi2


def injections(b, st, key, cut, n=40):
    raws = []
    ge = GE_EXTRA if key.endswith("2.32") else GE_DECISION
    kind = "N" if key == "N" else "nu6"
    for i in range(n):
        F.RNG = np.random.default_rng(
            SEED
            + 10007 * i
            + (0 if cut == "clean" else 900000)
            + (0 if key == "N" else 50)
        )
        vt = samples(b, kind, 1, ge)
        ncont = int(0.05 * len(vt))
        j = F.RNG.choice(len(vt), ncont, replace=False)
        vt[j] = F.VMAX * np.sqrt(F.RNG.random(ncont))
        _, chi2 = measure(vt, st, (key,))
        raws.append(chi2[key])
        print(f"inject {cut} {key} {i} {raws[-1]:.3f}", flush=True)
    return raws


def main(npz):
    newton_self_check()
    tab = np.loadtxt(HERE / "mamajek_mg_mass.csv", delimiter=",", comments="#")
    F.MG_TAB, F.M_TAB = tab[:, 0], tab[:, 1]
    c = dict(np.load(npz))
    out = {
        "prereg": "PREREG_NU6_WIDE_BINARY_2026-10-16.md",
        "a0": A0,
        "seed": SEED,
        "cuts": {},
    }
    held = {}
    for cut in ("clean", "loose"):
        F.RNG = np.random.default_rng(SEED if cut == "clean" else SEED + 1)
        b = F.prepare(c, F.CUTS[cut])
        print(cut, "n", len(b["s"]), flush=True)
        keys, st = build(b)
        rows, chi2 = measure(b["vt"], st, keys)
        out["cuts"][cut] = {"n": len(b["s"]), "chi2": chi2, "rows": rows}
        held[cut] = (b, st)
        print(cut, {k: round(v, 3) for k, v in chi2.items()}, flush=True)
    informative = 7.0 <= out["cuts"]["clean"]["chi2"]["N"] <= 12.0
    out["newton_control_informative"] = informative
    for key in ("nu6", "nu6_2.32"):
        cal = {}
        excluded_cuts = []
        for cut in ("clean", "loose"):
            b, st = held[cut]
            raws = injections(b, st, key, cut)
            med = float(np.median(raws))
            kappa = med / W.CHI2_4_MEDIAN
            raw = out["cuts"][cut]["chi2"][key]
            rec = {
                "injected": raws,
                "median": med,
                "null_max": float(np.max(raws)),
                "kappa": kappa,
                "chi2_raw": raw,
                "chi2_calibrated": float(raw / kappa),
            }
            cal[cut] = rec
            excluded_cuts.append(
                rec["chi2_calibrated"] > 18.5 and raw > rec["null_max"]
            )
        out[key] = {
            "calibration": cal,
            "excluded_C3": bool(all(excluded_cuts) and informative),
        }
        if not informative:
            out[key]["excluded_C3"] = False
            out[key]["note"] = "Newton control outside [7, 12]; no exclusion claimed"
    path = HERE / "NU6_WIDE_BINARY.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    print("wrote", path, flush=True)
    print(
        "informative",
        informative,
        "nu6 excluded",
        out["nu6"]["excluded_C3"],
        flush=True,
    )


if __name__ == "__main__":
    main(sys.argv[1])
