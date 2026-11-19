#!/usr/bin/env python3
"""Mixed cubic + quartic Galileon on the AeST scalar (PREREG_MIXED_L3L4.md), 2026-11-18. [O], first order.

SUPERSEDED __main__: the 273-point grid used an ellipticity check that mixed perturbation orders. Its failures were
spurious; the log is kept as mixed_l3l4_INVALID_ellipticity.log. The decisive runs are mixed_stability_sparc.py,
mixed_cassini_survivors.py and mixed_high_k3.py. ellipticity() below is now the order-consistent near-Sun check.
Scope: total-law embedding (an [O] alternative to D9's scalar-channel function).

Static equation for the scalar phi (acceleration units), around the Sun inside the Milky Way:
    Z_ij d_i d_j phi + 2 k3 sigma2(H) + 6 k4 sigma3(H) + [Galactic cross terms] = 4 pi G rho
Z = A_e (I + L e e) + 2 k3 (trT I - T) + 6 k4 cof(T)   (constant: AQUAL external-field + Galaxy cofactors)
cross term 6 k4 cof(H):T  (its isotropic part is an effective cubic k3_eff = k3 + k4 trT).
Background: spherical, flux 2k4 y^3 + 2k3_eff r y^2 + Z_iso r^2 y = GM, y = phi0'.
First-order anisotropy: delta_chi = F1(r) n.Ztil.n + F2(r) n.Ttil.n, with
    M_rr F'' + M_perp (2F'/r - 6F/r^2) = S,   S1 = -(a-b),  S2 = 6 k4 b (a-b),
    M_rr = Z_iso + 4 k3_eff b + 6 k4 b^2,  M_perp = Z_iso + 2 k3_eff (a+b) + 6 k4 a b,  a = y', b = y/r.
Inner BC F = r F' (no r^0 mode); outer BC: match the decaying solution plus the exact outer particular solution.
K3 = 2 k3 a0m [m], K4 = 2 k4 a0m^2 [m^2]; galaxies: f(s) + K3 s^2/r + K4 s^3/r^2 = q.
"""
import glob, json, math, os, sys
import numpy as np
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import door_nested_solution as D

G = 6.674e-11; MSUN = 1.989e30; GM = D.GM; AU = D.AU; KPC = D.KPC; PC = D.PC
R_SUN = D.R_SUN; R_STAR = 6.957e8
RHO0 = 0.1 * MSUN / PC**3                        # local midplane baryon density
Q2_LO, Q2_HI, Q2_SCREEN = -2.0e-27, 5.2e-27, 2.6e-27
PREC_MAX = D.PREC_MAX

def eq2ecl(ra, dec, eps=math.radians(23.43928)):
    ra, dec = math.radians(ra), math.radians(dec)
    x, y, z = math.cos(dec) * math.cos(ra), math.cos(dec) * math.sin(ra), math.sin(dec)
    return np.array([x, y * math.cos(eps) + z * math.sin(eps), -y * math.sin(eps) + z * math.cos(eps)])
E_GC = eq2ecl(266.40500, -28.93617)               # Galactic centre
E_NGP = eq2ecl(192.85948, 27.12825)               # Galactic north pole
E_NGP = E_NGP - (E_NGP @ E_GC) * E_GC; E_NGP /= np.linalg.norm(E_NGP)
E_PHI = np.cross(E_NGP, E_GC)

def cof(T):
    return T @ T - np.trace(T) * T + 0.5 * (np.trace(T) ** 2 - np.trace(T @ T)) * np.eye(3)

# ---------------- Milky Way (spherical enclosed mass, McMillan-like) ----------------
def M_enc(R, fmw):
    r = R / KPC
    return fmw * (0.9e10 * (r / (r + 0.6)) ** 2 + 5.0e10 * (1 - (1 + r / 2.6) * np.exp(-r / 2.6))
                  + 1.2e10 * (1 - (1 + r / 5.0) * np.exp(-r / 5.0))) * MSUN
def solve_s(q, R, K3, K4, s_tab, f_tab):
    lo, hi = np.zeros_like(q), np.interp(q, f_tab, s_tab)
    for _ in range(90):
        m = 0.5 * (lo + hi); F = np.interp(m, s_tab, f_tab) + K3 * m**2 / R + K4 * m**3 / R**2 - q
        lo = np.where(F < 0, m, lo); hi = np.where(F >= 0, m, hi)
    return 0.5 * (lo + hi)
def milky_way(lam, K3, K4, fmw):
    eta, x, s, J1, f, L = D.tables(lam); a0m = eta * D.A0FIT
    R = R_SUN * np.array([0.99, 1.0, 1.01])
    gh = G * M_enc(R, fmw) / R**2
    sv = solve_s(gh / a0m, R, K3, K4, s, f)
    se, sp_ = sv[1], (sv[2] - sv[0]) / (R[2] - R[0])
    return {"g": gh[1] + a0m * se, "s_e": se, "s_p": sp_, "a0m": a0m, "tables": (eta, x, s, J1, f, L)}
def fmw_for_g(lam, K3, K4, g_target):
    lo, hi = 0.3, 3.0
    if milky_way(lam, K3, K4, lo)["g"] > g_target or milky_way(lam, K3, K4, hi)["g"] < g_target:
        return None
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if milky_way(lam, K3, K4, mid)["g"] < g_target else (lo, mid)
    return 0.5 * (lo + hi)

# ---------------- solar problem ----------------
def setup(lam, K3, K4, fmw, galactic=True):
    mw = milky_way(lam, K3, K4, fmw); a0m = mw["a0m"]; eta, x, s, J1, f, L = mw["tables"]
    xe = np.interp(mw["s_e"], s, x); Ae = float(np.interp(xe, x, J1)); Le = float(np.interp(xe, x, L))
    TRR = a0m * mw["s_p"]; TPP = a0m * mw["s_e"] / R_SUN; TZZ = 4 * math.pi * G * RHO0 / Ae - TRR - TPP
    T = (TRR * np.outer(E_GC, E_GC) + TPP * np.outer(E_PHI, E_PHI) + TZZ * np.outer(E_NGP, E_NGP)) if galactic else np.zeros((3, 3))
    k3 = K3 / (2 * a0m); k4 = K4 / (2 * a0m**2)
    Z = Ae * (np.eye(3) + Le * np.outer(E_GC, E_GC)) + 2 * k3 * (np.trace(T) * np.eye(3) - T) + 6 * k4 * cof(T)
    return {"mw": mw, "Ae": Ae, "Le": Le, "T": T, "k3": k3, "k4": k4, "Z": Z,
            "Ziso": np.trace(Z) / 3, "k3e": k3 + k4 * np.trace(T), "TRR": TRR, "TPP": TPP, "TZZ": TZZ}

def background(P, r):
    k4, k3e, Z = P["k4"], P["k3e"], P["Ziso"]
    cand = [GM / (Z * r**2), (GM / (2 * k4)) ** (1 / 3) * np.ones_like(r)]
    if k3e > 0:
        cand.append(np.sqrt(GM / (2 * k3e * r)))
    y = np.min(np.vstack(cand), 0)
    for _ in range(200):
        Pv = 2 * k4 * y**3 + 2 * k3e * r * y**2 + Z * r**2 * y - GM
        dP = 6 * k4 * y**2 + 4 * k3e * r * y + Z * r**2
        y = y - Pv / dP
    a = -(2 * k3e * y**2 + 2 * Z * r * y) / (6 * k4 * y**2 + 4 * k3e * r * y + Z * r**2)
    return y, a, y / r

def radii(P):
    Z, k3e, k4 = P["Ziso"], P["k3e"], P["k4"]
    r4 = (2 * k4 * GM**2 / Z**3) ** (1 / 6)
    r3 = (2 * max(k3e, 0) * GM / Z**2) ** (1 / 3)
    return r3, r4

def bg_table(P):
    if "_bg" not in P:
        r3, r4 = radii(P); r_out = 50 * max(r3, r4, 1e14)
        xg = np.linspace(math.log(R_STAR), math.log(r_out), 6000); rg = np.exp(xg)
        y, a, b = background(P, rg)
        P["_bg"] = (xg, y, a, b, r_out)
    return P["_bg"]

def solve_l2(P, which):
    xg, yg, ag, bg, r_out = bg_table(P); Z = P["Ziso"]; k4 = P["k4"]; k3e = P["k3e"]
    Mrr_g = Z + 4 * k3e * bg + 6 * k4 * bg * bg
    Mpp_g = Z + 2 * k3e * (ag + bg) + 6 * k4 * ag * bg
    S_g = -(ag - bg) if which == 1 else 6 * k4 * bg * (ag - bg)
    def coeffs(xx):
        return np.interp(xx, xg, Mrr_g), np.interp(xx, xg, Mpp_g), np.interp(xx, xg, S_g)
    def rhs_p(xx, u):
        Mrr, Mpp, S = coeffs(xx); r = math.exp(xx); F, Fx = u
        return [Fx, Fx + (r * r * S - Mpp * (2 * Fx - 6 * F)) / Mrr]
    def rhs_h(xx, u):
        Mrr, Mpp, S = coeffs(xx); F, Fx = u
        return [Fx, Fx - Mpp * (2 * Fx - 6 * F) / Mrr]
    xs = (xg[0], xg[-1])
    opts = dict(method="DOP853", rtol=1e-9, atol=1e-12, dense_output=True)
    h = solve_ivp(rhs_h, xs, [1.0, 1.0], **opts)
    p = solve_ivp(rhs_p, xs, [0.0, 0.0], **opts)
    ro = r_out
    FP = -GM / (2 * Z**2 * ro) if which == 1 else -3 * k4 * GM**2 / (Z**3 * ro**4)
    FPx = -FP if which == 1 else -4 * FP
    hp, hx = h.y[0, -1], h.y[1, -1]; pp, px = p.y[0, -1], p.y[1, -1]
    alpha = -((px - FPx) + 3 * (pp - FP)) / (hx + 3 * hp)
    def F(r):
        xx = np.log(r); return p.sol(xx)[0] + alpha * h.sol(xx)[0], (p.sol(xx)[1] + alpha * h.sol(xx)[1]) / r
    return F

def anomalous_field(P, pts, F1, F2):
    r = np.linalg.norm(pts, axis=1); y, a, b = background(P, r)
    Zt = P["Z"] - P["Ziso"] * np.eye(3); Tt = P["T"] - np.trace(P["T"]) / 3 * np.eye(3)
    f1, f1p = F1(r); f2, f2p = F2(r)
    Qx = f1[:, None] * (pts @ Zt) + f2[:, None] * (pts @ Tt)
    xQx = f1 * np.einsum("ij,jk,ik->i", pts, Zt, pts) + f2 * np.einsum("ij,jk,ik->i", pts, Tt, pts)
    xQpx = f1p * np.einsum("ij,jk,ik->i", pts, Zt, pts) + f2p * np.einsum("ij,jk,ik->i", pts, Tt, pts)
    grad_d = 2 * Qx / r[:, None]**2 + (xQpx / r**3)[:, None] * pts - 2 * (xQx / r**4)[:, None] * pts
    return -(y / r)[:, None] * pts, -grad_d          # monopole, quadrupole accelerations

def circle(rr, n=720):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.stack([rr * np.cos(t), rr * np.sin(t), 0 * t], 1)

def sun_gate(P):
    F1 = solve_l2(P, 1); F2 = solve_l2(P, 2)
    pm = circle(0.387 * AU); mono, quad = anomalous_field(P, pm, F1, F2)
    rm = 0.387 * AU; y, a, b = background(P, np.array([rm])); n = rm * a[0] / y[0]
    orbit = (100 / 0.2408) * 206264.8
    prec_mono = math.pi * (n + 2) * y[0] * rm**2 / GM * orbit
    dg2 = -np.mean(np.sum(quad * pm, 1) / np.linalg.norm(pm, axis=1))
    prec = abs(prec_mono) + abs(2 * math.pi * dg2 * rm**2 / GM * orbit)
    ps = circle(9.537 * AU); _, qs = anomalous_field(P, ps, F1, F2)
    bq = ps @ E_GC; Qb = bq[:, None] * E_GC[None, :] - ps / 3; Rb = ps / np.linalg.norm(ps, axis=1)[:, None]
    coef, *_ = np.linalg.lstsq(np.stack([Qb.ravel(), Rb.ravel()], 1), qs.ravel(), rcond=None)
    return {"mercury_prec": prec, "core_force": float(y[0]), "n_slope": float(n), "saturn_Q2_eff": float(coef[0])}

def fib_dirs(n=300):
    i = np.arange(n) + 0.5; phi = np.arccos(1 - 2 * i / n); th = math.pi * (1 + 5**0.5) * i
    return np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], 1)
def ellipticity(P):
    """Order-consistent near-Sun check (hand-derived; see README).
    Inside r_T ~ c/|T| the Galileon cancels the Galactic tide, so the inner kinetic tensor is the external-field
    AQUAL A_e(I + L e e) and the effective cubic is k3 (no k4 trT). Required: M_rr > 0 and, at O(1),
    M_perp - (Z_max - Z_iso) > 0, where the second term is the anisotropic correction (e1 sees -Z_e2e2)."""
    Zin = P["Ae"] * (np.eye(3) + P["Le"] * np.outer(E_GC, E_GC)); ev = np.linalg.eigvalsh(Zin)
    Q = dict(P); Q["Ziso"] = float(np.trace(Zin) / 3); Q["k3e"] = P["k3"]
    r3, r4 = radii(Q); rs = np.logspace(math.log10(0.1 * AU), math.log10(3 * max(r3, r4, 1e13)), 200)
    y, a, b = background(Q, rs)
    Mrr = Q["Ziso"] + 4 * Q["k3e"] * b + 6 * Q["k4"] * b * b
    Mpp = Q["Ziso"] + 2 * Q["k3e"] * (a + b) + 6 * Q["k4"] * a * b
    return float(min(Mrr.min(), (Mpp - (ev[-1] - Q["Ziso"])).min()) / Q["Ziso"])

# ---------------- SPARC with cubic + quartic ----------------
FG = np.logspace(-0.5, 0.5, 61)
GALS = [(os.path.basename(p)[:-11], np.loadtxt(p)) for p in sorted(glob.glob(os.path.join(HERE, "../../02_galaxy_dynamics/sparc_data/*_rotmod.dat")))]
def _ghat(d):
    Vg, Vd, Vb, R = d[:, 3], d[:, 4], d[:, 5], d[:, 0]
    V2 = np.abs(Vg) * Vg + FG[:, None] * (0.5 * np.abs(Vd) * Vd + 0.7 * np.abs(Vb) * Vb)
    return np.maximum(V2, 1e-3) * 1e6 / (R * KPC)
def _chi2(d, gtot):
    R, V, eV = d[:, 0], d[:, 1], np.maximum(d[:, 2], 1.0)
    Vp = np.sqrt(gtot * R * KPC) / 1e3
    return float((np.sum(((V - Vp) / eV) ** 2, 1) + (np.log10(FG) / 0.1) ** 2).min())
def _xmu_inv(yv):
    return np.sqrt((yv**2 + yv * np.sqrt(yv**2 + 4)) / 2)
BASE = {n: _chi2(d, D.A0FIT * _xmu_inv(_ghat(d) / D.A0FIT)) for n, d in GALS}
def sparc(lam, K3, K4):
    eta, x, s, J1, f, L = D.tables(lam); a0m = eta * D.A0FIT; out = {}
    for n, d in GALS:
        gh = _ghat(d); r = d[:, 0] * KPC
        sv = solve_s(gh / a0m, r, K3, K4, s, f)
        out[n] = _chi2(d, gh + a0m * sv) - BASE[n]
    v = np.array(list(out.values()))
    return {"dchi2_total": float(v.sum()), "galaxies_dchi2>25": int((v > 25).sum()),
            "worst": [(k, round(val, 1)) for k, val in sorted(out.items(), key=lambda t: -t[1])[:4]]}

# ---------------- regressions ----------------
def regression_a():
    rows = []
    for sigma in (1.05, 1.5, 2.0, 3.0, 4.0):
        Lv = sigma**2 - 1; lam, K4 = 1.0, 1e40
        P = setup(lam, 0.0, K4, 1.0, galactic=False)
        Ae = P["Ae"]; P["Z"] = Ae * (np.eye(3) + Lv * np.outer(E_GC, E_GC)); P["Ziso"] = np.trace(P["Z"]) / 3
        P["Le"] = Lv; P["k3"] = 0.0; P["k3e"] = 0.0
        ode = sun_gate(P)["saturn_Q2_eff"]
        a0m = P["mw"]["a0m"]; c = (GM * sigma * a0m**2 / K4) ** (1 / 3)
        def acc(pts):
            z = pts @ E_GC; rp_ = np.sqrt(np.sum(pts**2, 1) - z**2 + z**2 / sigma**2)
            return -c * (pts - (1 - 1 / sigma**2) * z[:, None] * E_GC[None, :]) / rp_[:, None]
        ps = circle(9.537 * AU); a_s = acc(ps); bq = ps @ E_GC
        Qb = bq[:, None] * E_GC[None, :] - ps / 3; Rb = ps / np.linalg.norm(ps, axis=1)[:, None]
        exact = float(np.linalg.lstsq(np.stack([Qb.ravel(), Rb.ravel()], 1), a_s.ravel(), rcond=None)[0][0])
        rows.append({"sigma": sigma, "Q2_ode_first_order": ode, "Q2_exact_stretched": exact, "ratio": ode / exact})
    return rows
def regression_b():
    ref = json.load(open(os.path.join(HERE, "DOOR_NESTED_SOLUTION.json")))["runs"]
    out = []
    for lam, K in ((0.5, 1e40), (1.0, 3.1622776601683795e39)):
        r0 = next(r for r in ref if r["lambda_s"] == lam and abs(r["K_m2"] / K - 1) < 1e-6)
        out.append({"lambda_s": lam, "K4": K, "ref": r0["sparc"]["dchi2_total"], "here": sparc(lam, 0.0, K)["dchi2_total"]})
    return out

if __name__ == "__main__":
    print("NOTE: this grid is superseded (see module docstring); rerunning uses the corrected ellipticity().", flush=True)
    res = {"directions": {"E_GC": E_GC.tolist(), "E_NGP": E_NGP.tolist()}}
    ra = regression_a(); res["regression_a"] = ra
    for r_ in ra: print("reg-a sigma=%.2f ode=%.3e exact=%.3e ratio=%.3f" % (r_["sigma"], r_["Q2_ode_first_order"], r_["Q2_exact_stretched"], r_["ratio"]), flush=True)
    rb = regression_b(); res["regression_b"] = rb
    for r_ in rb: print("reg-b", r_, flush=True)
    assert all(abs(r_["here"] - r_["ref"]) < 1e-6 * max(1, abs(r_["ref"])) for r_ in rb), "SPARC regression (b) failed"
    scan = []
    for lam in (0.5, 1.0, 3.0):
        for K4 in np.logspace(38, 41, 7):
            for ratio in np.logspace(-22, -16, 13):
                K3 = K4 * ratio; row = {"lambda_s": lam, "K4": float(K4), "K3": float(K3), "K3_over_K4": float(ratio)}
                gates = []
                for gt in (1.9e-10, 2.4e-10):
                    fmw = fmw_for_g(lam, K3, K4, gt)
                    if fmw is None:
                        gates.append({"g_target": gt, "fail": "g(R_sun) unreachable"}); continue
                    P = setup(lam, K3, K4, fmw)
                    ev = np.linalg.eigvalsh(P["Z"]); el = ellipticity(P) if ev[0] > 0 else -1.0
                    g = {"g_target": gt, "fmw": fmw, "Z_min_eig": float(ev[0]), "near_sun_min_rel_eig": float(el),
                         "TRR": P["TRR"], "TPP": P["TPP"], "TZZ": P["TZZ"]}
                    if ev[0] > 0 and el > 0:
                        g.update(sun_gate(P))
                        g["pass_sun"] = g["mercury_prec"] <= PREC_MAX and abs(g["saturn_Q2_eff"]) <= Q2_SCREEN
                    else:
                        g["pass_sun"] = False; g["fail"] = "non-elliptic"
                    gates.append(g)
                row["gates"] = gates
                row["candidate"] = all(isinstance(g, dict) and g.get("pass_sun") for g in gates)
                if row["candidate"]:
                    row["sparc"] = sparc(lam, K3, K4)
                    row["pass_all"] = row["sparc"]["dchi2_total"] <= 0
                scan.append(row)
                fails = ";".join(g.get("fail", "Q2=%.1e prec=%.1e" % (g.get("saturn_Q2_eff", np.nan), g.get("mercury_prec", np.nan))) for g in gates)
                print(f"lam={lam} K4={K4:.1e} K3/K4={ratio:.0e} cand={row['candidate']} {fails}" + (f" sparc={row['sparc']['dchi2_total']:.0f}" if row["candidate"] else ""), flush=True)
    res["scan"] = scan
    res["n_candidates"] = sum(r["candidate"] for r in scan)
    res["n_pass_all"] = sum(bool(r.get("pass_all")) for r in scan)
    json.dump(res, open(os.path.join(HERE, "MIXED_L3L4.json"), "w"), indent=1, default=float)
    print("candidates:", res["n_candidates"], " pass_all:", res["n_pass_all"])
