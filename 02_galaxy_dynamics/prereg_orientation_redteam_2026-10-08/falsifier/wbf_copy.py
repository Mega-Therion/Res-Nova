"""Wide-binary test of the fish rule. Pre-registered in PREREG_WIDE_BINARY_FISH.md.

Input: npz produced by wide_binary_extract.py from El-Badry+2021 (Zenodo 4435257).
Output: WIDE_BINARY_FISH.json

Observable: R(s) = alpha(s)/alpha(control), where alpha is the velocity scale of
v~ = dv_sky / sqrt(G M / s_sky) relative to a per-binary Newtonian Monte Carlo
template, fitted jointly with a contaminant fraction.
"""

import json
import sys

import numpy as np

RNG = np.random.default_rng(20261004)
K = 4.740470446  # km/s per (mas/yr * kpc)
VC1 = 29.7847  # km/s, sqrt(G Msun / 1 AU)
GN_1AU = 5.9301e-3  # m/s^2, G Msun / AU^2
A0 = 1.042e-10  # derived a0 (cH0/2pi), m/s^2
GE = 1.9e-10  # MW field at the Sun, m/s^2
SIG_VR = 35.0  # km/s, unknown-RV perspective term
DMAX = 0.2  # kpc; distance limit (pre-registered 0.2)
BINS = [(500, 2000), (2000, 5000), (5000, 10000), (10000, 20000), (20000, 30000)]
VMAX = 5.0
NMC = 40

CUTS = {
    "clean": dict(rca=0.01, ruwe=1.2, sig=0.10),
    "loose": dict(rca=0.1, ruwe=1.4, sig=0.20),
}

# Main-sequence M_G -> mass (Msun), Pecaut & Mamajek 2013 dwarf sequence (approx.)
MG_TAB = np.array(
    [
        2.0,
        2.5,
        3.0,
        3.5,
        4.0,
        4.5,
        5.0,
        5.5,
        6.0,
        6.5,
        7.0,
        7.5,
        8.0,
        8.5,
        9.0,
        9.5,
        10.0,
        10.5,
        11.0,
        11.5,
        12.0,
        12.5,
        13.0,
    ]
)
M_TAB = np.array(
    [
        1.75,
        1.60,
        1.45,
        1.30,
        1.17,
        1.05,
        0.95,
        0.88,
        0.82,
        0.76,
        0.70,
        0.65,
        0.60,
        0.55,
        0.50,
        0.45,
        0.40,
        0.35,
        0.30,
        0.25,
        0.21,
        0.18,
        0.15,
    ]
)


def _rv(x):
    """Gaia stores a missing DR2 RV (and its error) as 1e20, not NaN."""
    x = np.asarray(x, dtype=float)
    return np.where(np.abs(x) < 1e10, x, np.nan)


def nu_std(y):
    return np.sqrt((1 + np.sqrt(1 + 4 / y**2)) / 2)


def q_two_body(q1):
    q2 = 1 - q1
    return (2 / 3) * (1 - q1**1.5 - q2**1.5) / (q1 * q2)


def unit_vectors(ra, dec):
    a, d = np.radians(ra), np.radians(dec)
    r = np.stack([np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)], -1)
    ea = np.stack([-np.sin(a), np.cos(a), np.zeros_like(a)], -1)
    ed = np.stack([-np.sin(d) * np.cos(a), -np.sin(d) * np.sin(a), np.cos(d)], -1)
    return r, ea, ed


def prepare(c, cut):
    """Apply cuts; return per-binary arrays for the fit."""
    p1, p2 = c["parallax1"], c["parallax2"]
    e1, e2 = c["parallax_error1"], c["parallax_error2"]
    w1, w2 = 1 / e1**2, 1 / e2**2
    plx = (p1 * w1 + p2 * w2) / (w1 + w2)
    d_kpc = 1 / plx
    MG1 = c["phot_g_mean_mag1"] + 5 * np.log10(plx / 100)
    MG2 = c["phot_g_mean_mag2"] + 5 * np.log10(plx / 100)
    ok = (
        (c["R_chance_align"] <= cut["rca"])
        & (c["ruwe1"] < cut["ruwe"])
        & (c["ruwe2"] < cut["ruwe"])
        & (p1 / e1 > 50)
        & (p2 / e2 > 50)
        & (np.abs(p1 - p2) < 3 * np.hypot(e1, e2))
        & (d_kpc < DMAX)
        & (MG1 > 4)
        & (MG1 < 12)
        & (MG2 > 4)
        & (MG2 < 12)
        & np.isfinite(c["bp_rp1"])
        & np.isfinite(c["bp_rp2"])
    )
    # empirical main-sequence locus M_G(bp_rp) from all candidate stars
    br = np.concatenate([c["bp_rp1"][ok], c["bp_rp2"][ok]])
    mg = np.concatenate([MG1[ok], MG2[ok]])
    edges = np.arange(0.4, 3.6, 0.1)
    idx = np.digitize(br, edges)
    med = np.array(
        [
            np.median(mg[idx == i]) if np.sum(idx == i) > 20 else np.nan
            for i in range(1, len(edges))
        ]
    )
    cen = 0.5 * (edges[1:] + edges[:-1])
    good = np.isfinite(med)
    loc = lambda x: np.interp(x, cen[good], med[good], left=np.nan, right=np.nan)
    ok &= (np.abs(MG1 - loc(c["bp_rp1"])) < 0.8) & (
        np.abs(MG2 - loc(c["bp_rp2"])) < 0.8
    )

    m1 = np.interp(MG1, MG_TAB, M_TAB)
    m2 = np.interp(MG2, MG_TAB, M_TAB)
    M = m1 + m2

    r1, ea1, ed1 = unit_vectors(c["ra1"], c["dec1"])
    r2, ea2, ed2 = unit_vectors(c["ra2"], c["dec2"])
    cos_t = np.clip(np.sum(r1 * r2, -1), -1, 1)
    theta = np.arccos(cos_t)  # rad
    s_au = theta * 206264.806 * (d_kpc * 1000)  # AU

    v1 = K * d_kpc[:, None] * (c["pmra1"][:, None] * ea1 + c["pmdec1"][:, None] * ed1)
    v2 = K * d_kpc[:, None] * (c["pmra2"][:, None] * ea2 + c["pmdec2"][:, None] * ed2)
    rv1, rv2 = _rv(c["dr2_radial_velocity1"]), _rv(c["dr2_radial_velocity2"])
    rve1, rve2 = _rv(c["dr2_radial_velocity_error1"]), _rv(c["dr2_radial_velocity_error2"])
    have1, have2 = np.isfinite(rv1), np.isfinite(rv2)
    rv = np.where(have1, rv1, np.where(have2, rv2, 0.0))
    rv_sig = np.where(have1, rve1, np.where(have2, rve2, SIG_VR))
    rv_sig = np.where(np.isfinite(rv_sig), rv_sig, SIG_VR)
    V = v1 + rv[:, None] * r1
    P2V = V - np.sum(V * r2, -1)[:, None] * r2
    dv = v2 - P2V
    dva = np.sum(dv * ea2, -1)
    dvd = np.sum(dv * ed2, -1)

    sig_pm2 = (
        (K * d_kpc) ** 2
        * (
            c["pmra_error1"] ** 2
            + c["pmra_error2"] ** 2
            + c["pmdec_error1"] ** 2
            + c["pmdec_error2"] ** 2
        )
        / 2
    )
    sig_comp = np.sqrt(sig_pm2 + (rv_sig * theta) ** 2 / 2)  # km/s per component
    vc = VC1 * np.sqrt(M / s_au)
    vt = np.hypot(dva, dvd) / vc
    sig_t = sig_comp / vc
    ok &= (
        np.isfinite(vt)
        & (sig_t < cut["sig"])
        & (s_au > BINS[0][0])
        & (s_au < BINS[-1][1])
    )
    return dict(vt=vt[ok], sig=sig_t[ok], s=s_au[ok], M=M[ok], q1=(m1 / M)[ok])


def kepler_mc(n, gamma):
    """Unit orbits (a=1, GM=1). Returns sky-projected r, 3D r, and sky v vector."""
    e = RNG.random(n) ** (1 / (gamma + 1))
    e = np.minimum(e, 0.999)
    Mn = RNG.random(n) * 2 * np.pi
    E = Mn.copy()
    for _ in range(30):
        E -= (E - e * np.sin(E) - Mn) / (1 - e * np.cos(E))
    den = 1 - e * np.cos(E)
    pos = np.stack([np.cos(E) - e, np.sqrt(1 - e**2) * np.sin(E), np.zeros(n)], -1)
    vel = np.stack(
        [-np.sin(E) / den, np.sqrt(1 - e**2) * np.cos(E) / den, np.zeros(n)], -1
    )
    qv = RNG.normal(size=(n, 4))
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
    return np.hypot(P[:, 0], P[:, 1]), np.linalg.norm(pos, axis=1), Vv[:, :2], P


def gamma_of_s(s):
    return np.clip(0.4 + 0.45 * np.log10(s / 100), 0.4, 1.3)


def boost(model, gN, q1, rhat_sky=None):
    """g/gN for each model; gN in m/s^2."""
    y = gN / A0
    Q = q_two_body(q1)
    if model == "N":
        return np.ones_like(gN)
    if model == "F":
        return 1 + Q * (nu_std(y) - 1)
    if model == "P":
        # nesting: a passenger whose own pull is below the host field is Newtonian
        return np.where(gN > GE, 1 + Q * (nu_std(y) - 1), 1.0)
    if model == "S":
        eta = GE / A0
        return 1 + Q * (nu_std(y) - 1) / (1 + eta**2)
    if model == "E":
        # 1D-QUMOND vector form, random external-field direction
        n = len(gN)
        u = RNG.normal(size=(n, 3))
        u /= np.linalg.norm(u, axis=1)[:, None]
        gNv = np.zeros((n, 3))
        gNv[:, 0] = gN
        gev = GE * u
        gt = gNv + gev
        gtm = np.linalg.norm(gt, axis=1)
        gint = nu_std(gtm / A0)[:, None] * gt - nu_std(GE / A0) * gev
        bE = gint[:, 0] / gN
        # deep-MOND two-body reduction applied to the boost part
        return 1 + Q * (bE - 1)
    raise ValueError(model)


def simulate(b, model, nmc=NMC, noise=True):
    """Per-binary MC of v~ under a model. Returns (vt samples, owner index)."""
    n = len(b["s"])
    idx = np.repeat(np.arange(n), nmc)
    s, M, q1, sig = b["s"][idx], b["M"][idx], b["q1"][idx], b["sig"][idx]
    rsky, r3, vsky, _ = kepler_mc(len(idx), gamma_of_s(s))
    vt_vec = vsky * np.sqrt(rsky)[:, None]
    if model != "N":
        a_au = s / rsky
        gN = GN_1AU * M / (a_au * r3) ** 2
        vt_vec = vt_vec * np.sqrt(boost(model, gN, q1))[:, None]
    if noise:
        vt_vec = vt_vec + RNG.normal(size=vt_vec.shape) * sig[:, None]
    return np.hypot(vt_vec[:, 0], vt_vec[:, 1]), idx


def template(vt):
    h, e = np.histogram(vt, bins=np.arange(0, 8.0001, 0.02), density=True)
    h = np.convolve(h, np.ones(5) / 5, mode="same") + 1e-6
    x = 0.5 * (e[1:] + e[:-1])
    cdf = np.concatenate([[0], np.cumsum(h) * 0.02])
    return lambda u: np.interp(u, x, h, left=h[0], right=1e-6), lambda u: np.interp(
        u, e, cdf, right=cdf[-1]
    )


def p_cont(v):
    return 2 * v / VMAX**2  # flat in the 2D velocity plane, normalised on [0, VMAX]


def fit_alpha(vt, pdf, cdf, fix_c=None):
    vt = vt[vt < VMAX]
    alphas = np.linspace(0.6, 2.2, 321)
    cs = np.array([0.0]) if fix_c is not None else np.linspace(0, 0.6, 61)
    L = np.full((len(alphas), len(cs)), -np.inf)
    for i, a in enumerate(alphas):
        pn = pdf(vt / a) / a / cdf(VMAX / a)
        pc = p_cont(vt)
        for j, c in enumerate(cs):
            L[i, j] = np.sum(np.log((1 - c) * pn + c * pc))
    prof = L.max(axis=1)
    i0 = np.argmax(prof)
    inside = alphas[prof > prof[i0] - 0.5]
    j0 = np.argmax(L[i0])
    return dict(
        alpha=float(alphas[i0]),
        lo=float(inside.min()),
        hi=float(inside.max()),
        c=float(cs[j0]),
        n=int(len(vt)),
    )


def run_bins(b, vt_obs, label):
    out = []
    for lo, hi in BINS:
        m = (b["s"] >= lo) & (b["s"] < hi)
        sub = {k: v[m] for k, v in b.items()}
        if m.sum() < 30:
            out.append(dict(bin=[lo, hi], n=int(m.sum()), alpha=None))
            continue
        tN, _ = simulate(sub, "N")
        pdf, cdf = template(tN)
        f = fit_alpha(vt_obs[m], pdf, cdf)
        f["bin"] = [lo, hi]
        f["models"] = {}
        for mod in ["F", "E", "S", "P"]:
            tm, _ = simulate(sub, mod, nmc=10)
            f["models"][mod] = fit_alpha(tm, pdf, cdf, fix_c=0)["alpha"]
        f["models"]["N"] = fit_alpha(simulate(sub, "N", nmc=10)[0], pdf, cdf, fix_c=0)[
            "alpha"
        ]
        out.append(f)
        print(label, lo, hi, f["n"], f["alpha"], f["c"], f["models"], flush=True)
    return out


def ratios(res):
    ctrl = res[0]
    rows = []
    for r in res[1:]:
        if r.get("alpha") is None:
            continue
        R = r["alpha"] / ctrl["alpha"]
        sR = R * np.hypot(
            (r["hi"] - r["lo"]) / 2 / r["alpha"],
            (ctrl["hi"] - ctrl["lo"]) / 2 / ctrl["alpha"],
        )
        mods = {k: r["models"][k] / ctrl["models"][k] for k in r["models"]}
        rows.append(dict(bin=r["bin"], n=r["n"], R=R, sigma=sR, c=r["c"], models=mods))
    chi2 = {
        k: float(sum(((x["R"] - x["models"][k]) / x["sigma"]) ** 2 for x in rows))
        for k in ["N", "F", "E", "S", "P"]
    }
    return rows, chi2


def inject(b, model):
    vt, idx = simulate(b, model, nmc=1)
    ncont = int(0.05 * len(vt))
    j = RNG.choice(len(vt), ncont, replace=False)
    vt[j] = VMAX * np.sqrt(RNG.random(ncont))
    return vt


def main(npz, out_json):
    c = dict(np.load(npz))
    result = {}
    for name, cut in CUTS.items():
        b = prepare(c, cut)
        print(name, "N binaries:", len(b["s"]), flush=True)
        block = {"n_total": int(len(b["s"]))}
        for inj in ["N", "F", "P"]:
            res = run_bins(b, inject(b, inj), f"{name}/inject-{inj}")
            rows, chi2 = ratios(res)
            block[f"injection_{inj}"] = dict(rows=rows, chi2=chi2)
        res = run_bins(b, b["vt"], f"{name}/DATA")
        rows, chi2 = ratios(res)
        block["data"] = dict(bins=res, rows=rows, chi2=chi2)
        result[name] = block
    result["config"] = dict(
        a0=A0,
        g_e=GE,
        sig_vr=SIG_VR,
        bins=BINS,
        vmax=VMAX,
        nmc=NMC,
        cuts=CUTS,
        exclusion_chi2_4dof=18.5,
    )
    json.dump(result, open(out_json, "w"), indent=1, default=float)
    print("wrote", out_json)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
