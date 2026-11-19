#!/usr/bin/env python3
"""P0 (PREREG_P0.md): effective 4D equations on the asymmetric dark-bubble wall.

C1  exact Friedmann wall in planar AdS-Schwarzschild: Gauss equation
        4G_mn = F_mn - E_mn + K K_mn - K_m^a K_an - (1/2) h_mn (K^2 - K.K),
    with F = 3 k^2 h for a pure-Lambda bulk and E_mn = C_AmBn n^A n^B from the bulk Weyl tensor.
C2  Randall-Sundrum limit (k+ = k- = k, opposite-sign K): G4 = k G5, Weyl fluid = mean of E+-.
C3  dark-bubble limit (same-sign K): G4 = 2 k+ k- G5/(k- - k+), Lambda4 ~ sigma_ext - sigma,
    dark radiation ~ (mu+/k+ - mu-/k-).
C4  Battye-Carter-Mennim-Uzan (hep-th/0105091) kappa_4 with the two-Lambda force term.
Outputs: wall-stress coupling, effective Weyl fluid, drag 00 factor, matter sector, null-dust size.
"""
from __future__ import annotations

import json
import os

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))


def c1_exact_background() -> dict:
    t, r, x, y, z = sp.symbols("t r x y z", real=True)
    k, mu = sp.symbols("k mu", positive=True)
    X = [t, r, x, y, z]
    f = k**2 * r**2 - mu / r**2
    g = sp.diag(-f, 1 / f, r**2, r**2, r**2)
    gi = g.inv()
    n = 5
    Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d]))
                             for d in range(n)) / 2) for c in range(n)] for b in range(n)] for a in range(n)]

    def riem(a, b, c, d):  # R^a_{bcd}
        e = sp.diff(Gam[a][b][d], X[c]) - sp.diff(Gam[a][b][c], X[d])
        e += sum(Gam[a][c][m] * Gam[m][b][d] - Gam[a][d][m] * Gam[m][b][c] for m in range(n))
        return e

    Rup = [[[[sp.simplify(riem(a, b, c, d)) for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    Rdn = [[[[sp.simplify(sum(g[a, m] * Rup[m][b][c][d] for m in range(n))) for d in range(n)] for c in range(n)]
            for b in range(n)] for a in range(n)]
    Ric = sp.Matrix(n, n, lambda b, d: sp.simplify(sum(Rup[a][b][a][d] for a in range(n))))
    Rs = sp.simplify(sum(gi[a, b] * Ric[a, b] for a in range(n) for b in range(n)))
    assert sp.simplify(Rs + 20 * k**2) == 0
    assert all(sp.simplify(Ric[a, b] + 4 * k**2 * g[a, b]) == 0 for a in range(n) for b in range(n))

    def weyl(a, b, c, d):
        e = Rdn[a][b][c][d]
        e -= sp.Rational(1, n - 2) * (g[a, c] * Ric[d, b] - g[a, d] * Ric[c, b] - g[b, c] * Ric[d, a] + g[b, d] * Ric[c, a])
        e += Rs / ((n - 1) * (n - 2)) * (g[a, c] * g[d, b] - g[a, d] * g[c, b])
        return sp.simplify(e)

    # wall r = a(tau), t = T(tau)
    tau = sp.Symbol("tau", real=True)
    a = sp.Function("a", positive=True)(tau)
    ad, add = sp.diff(a, tau), sp.diff(a, tau, 2)
    fa = f.subs(r, a)
    Td = sp.sqrt(fa + ad**2) / fa
    u = [Td, ad, 0, 0, 0]
    nl = [-ad, Td, 0, 0, 0]  # covariant unit normal, pointing to larger r
    sub = {r: a}
    gw = g.subs(sub)
    nu = list(gw.inv() * sp.Matrix(nl))
    ex = [0, 0, 1, 0, 0]
    assert sp.simplify(sum(gw[A, B] * u[A] * u[B] for A in range(n) for B in range(n)) + 1) == 0
    # K_ij = -Gamma^C_ij n_C ; K_tt = -n_B (du^B/dtau + Gamma^B_CD u^C u^D)
    GamW = [[[Gam[a_][b_][c_].subs(sub) for c_ in range(n)] for b_ in range(n)] for a_ in range(n)]
    Kxx = sp.simplify(-sum(GamW[C][2][2] * nl[C] for C in range(n)))
    acc = [sp.diff(u[B], tau) + sum(GamW[B][C][D] * u[C] * u[D] for C in range(n) for D in range(n)) for B in range(n)]
    Ktt = sp.simplify(-sum(nl[B] * acc[B] for B in range(n)))
    Kmix_t = sp.simplify(-Ktt)          # K^tau_tau (h^tautau = -1)
    Kmix_x = sp.simplify(Kmix_t * 0 + Kxx / a**2)
    assert sp.simplify(Kmix_x - sp.sqrt(fa + ad**2) / a) == 0
    # projected Weyl, mixed components
    W = [[[[weyl(A, B, C, D).subs(sub) for D in range(n)] for C in range(n)] for B in range(n)] for A in range(n)]
    Ett = sp.simplify(sum(W[A][B][C][D] * nu[A] * u[B] * nu[C] * u[D] for A in range(n) for B in range(n) for C in range(n) for D in range(n)))
    Exx = sp.simplify(sum(W[A][B][C][D] * nu[A] * ex[B] * nu[C] * ex[D] for A in range(n) for B in range(n) for C in range(n) for D in range(n)))
    Emix_t, Emix_x = sp.simplify(-Ett), sp.simplify(Exx / a**2)
    assert sp.simplify(Emix_t + 3 * Emix_x) == 0  # traceless
    # 4D Einstein tensor of -dtau^2 + a^2 dx^2 (mixed): G^t_t = -3 H^2, G^x_x = -(2 a''/a + H^2)
    H = ad / a
    G4t, G4x = -3 * H**2, -(2 * add / a + H**2)
    Ktr = Kmix_t + 3 * Kmix_x
    KK = Kmix_t**2 + 3 * Kmix_x**2
    Q_t = Ktr * Kmix_t - Kmix_t**2 - (Ktr**2 - KK) / 2
    Q_x = Ktr * Kmix_x - Kmix_x**2 - (Ktr**2 - KK) / 2
    res_t = sp.simplify(G4t - (3 * k**2 - Emix_t + Q_t))
    res_x = sp.simplify(G4x - (3 * k**2 - Emix_x + Q_x))
    assert res_t == 0 and res_x == 0
    return {
        "C1_bulk": "R = -20 k^2, R_AB = -4 k^2 g_AB (planar AdS-Schwarzschild, f = k^2 r^2 - mu/r^2)",
        "C1_K_x_x": "sqrt(f + adot^2)/a",
        "C1_E_tau_tau": str(sp.simplify(Emix_t)),
        "C1_E_x_x": str(sp.simplify(Emix_x)),
        "C1_gauss_identity_exact": True,
        "C1_form": "4G_mn = 3k^2 h_mn - E_mn + K K_mn - K_m^a K_an - (1/2) h_mn (K^2 - K.K), E_mn = C_AmBn n^A n^B",
    }


def linear_wall(s_p: int, s_m: int, kp, km) -> dict:
    """Linearised Gauss on both sides around a flat extremal wall, K^+-_mn = s+- k+- eta + Z+-.
    Unknowns: 4G (sym), X = <Z>. Data: tau (wall stress beyond tension), E+-, F+- (bulk-matter terms beyond 3k^2 h)."""
    eta = sp.diag(-1, 1, 1, 1)
    ei = eta.inv()
    sym = lambda nm: sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"{nm}_{min(i, j)}{max(i, j)}", real=True))
    G, Xm, tau, Ep, Em, Fp, Fm = (sym(s) for s in ("G", "X", "tau", "Ep", "Em", "Fp", "Fm"))
    kap = sp.Symbol("kappa5", positive=True)
    tr = lambda M: sum(ei[i, j] * M[i, j] for i in range(4) for j in range(4))
    Y = -kap * (tau - tr(tau) * eta / 3)          # [K] beyond tension, Israel: [K_mn - K h_mn] = -kappa5 S_mn
    Zp, Zm = Xm + Y / 2, Xm - Y / 2

    def Qlin(al, Zz):  # linear part of K K_mn - K_m^a K_an - (1/2) h (K^2 - K.K) at K = al*eta + Zz (mixed via eta)
        return 2 * al * (Zz - tr(Zz) * eta)

    eqs = []
    for (s, kk, Zz, E, F) in ((s_p, kp, Zp, Ep, Fp), (s_m, km, Zm, Em, Fm)):
        M = G - (F - E + Qlin(s * kk, Zz))
        eqs += [M[i, j] for i in range(4) for j in range(i, 4)]
    unknowns = [G[i, j] for i in range(4) for j in range(i, 4)] + [Xm[i, j] for i in range(4) for j in range(i, 4)]
    sol = sp.solve(eqs, unknowns, dict=True)[0]
    Gsol = G.subs(sol)
    return {"G": Gsol, "tau": tau, "Ep": Ep, "Em": Em, "Fp": Fp, "Fm": Fm, "kappa5": kap}


def c2_c3_c4() -> dict:
    k, kp, km, G5 = sp.symbols("k k_p k_m G5", positive=True)
    out = {}
    # C2: Randall-Sundrum (positive tension needs s+ = -1, s- = +1)
    L = linear_wall(-1, +1, k, k)
    G, kap = L["G"], L["kappa5"]
    claim = k * kap * L["tau"] - (L["Ep"] + L["Em"]) / 2 + (L["Fp"] + L["Fm"]) / 2
    assert sp.simplify(G - claim) == sp.zeros(4, 4)
    out["C2_RS"] = "4G = (k kappa5) tau - <E> + <F>:  8 pi G4 = k * 8 pi G5, G4 = k G5; Weyl fluid = mean of E+- (SMS linear terms)"
    # C3: dark bubble (same sign, s = +1 both sides; positive tension needs k- > k+)
    L = linear_wall(+1, +1, kp, km)
    G, kap = L["G"], L["kappa5"]
    G4 = 2 * kp * km / (km - kp)  # in units of G5
    claim = -kap * G4 * L["tau"] - (km * L["Ep"] - kp * L["Em"]) / (km - kp) + (km * L["Fp"] - kp * L["Fm"]) / (km - kp)
    assert sp.simplify(G - claim) == sp.zeros(4, 4)
    sigma_ext = 3 * (km - kp) / sp.Symbol("kappa5", positive=True)
    out["C3_dark_bubble"] = ("4G = -8 pi G4 tau - E_eff + F_eff, G4 = 2 k+ k- G5/(k- - k+); "
                             "E_eff = (k- E+ - k+ E-)/(k- - k+), F_eff = (k- F+ - k+ F-)/(k- - k+)")
    # tension offset: tau = -(sigma - sigma_ext) eta  ->  3H^2 = G_tautau = 8 pi G4 (sigma_ext - sigma)
    ds = sp.Symbol("dsigma", real=True)
    out["C3_Lambda4"] = "tau = -(sigma - sigma_ext) h  =>  H^2 = (8 pi G4/3)(sigma_ext - sigma): Lambda4 = sigma_ext - sigma > 0 for sub-extremal tension (1807.01570)"
    # dark radiation: with C1, E^tau_tau(+-) = 3 mu+-/a^4 -> G^tau_tau = -3H^2 picks up -E_eff^tau_tau
    mup, mum, a = sp.symbols("mu_p mu_m a", positive=True)
    Eeff_tt = (km * 3 * mup - kp * 3 * mum) / ((km - kp) * a**4)
    H2_dr = sp.simplify(Eeff_tt / 3)
    target = kp * km / (km - kp) * (mup / kp - mum / km) / a**4  # = (G4/2G5)(mu+/k+ - mu-/k-)/a^4 from the exact junction (Phase 1 A2)
    assert sp.simplify(H2_dr - target) == 0
    out["C3_dark_radiation"] = "H^2 ⊃ (k+ k-/(k- - k+)) (mu+/k+ - mu-/k-)/a^4 = (G4/2G5)(mu+/k+ - mu-/k-)/a^4: matches the exact junction expansion"
    # C4: BCMU gravconst, n = 5, force F = -[T_ba^nn] with T_ba = -(Lambda5/kappa5) g, Lambda5 = -6 k^2
    kap = sp.Symbol("kappa5", positive=True)
    sig = 3 * (km - kp) / kap
    Fforce = -(-(-6 * kp**2) / kap - (-(-6 * km**2) / kap))
    nn = 5
    kappa4 = (nn - 3) * (kap**2 * sig / (4 * (nn - 2)) - (nn - 2) * Fforce**2 / ((nn - 1) ** 2 * sig**3))
    assert sp.simplify(kappa4 + kap * 2 * kp * km / (km - kp)) == 0
    out["C4_BCMU"] = "kappa4(BCMU) = -kappa5 * 2 k+ k-/(k- - k+) = -8 pi G4: agrees in sign and magnitude (wall-localized stress anti-gravitates)"
    return out


def outputs() -> dict:
    out = {}
    out["O1_wall_stress_coupling"] = ("The explicit coupling of wall-localized stress tau_mn is -8 pi G4 (C3; BCMU C4 agrees in sign). Its NET 4D gravity "
                                      "also depends on the bulk response it induces, which sits in E_eff/F_eff and is free data in this identity. With no "
                                      "induced bulk response it anti-gravitates; dark-bubble papers show the response can overcompensate to +G4 "
                                      "(arXiv:2310.15032 sec. 4.2: worldvolume EM fields and brane-deposited mass; 1807.01570 propagator; 2001.07433 bending). "
                                      "The drag is a tension modification with no bulk field of its own, so it anti-gravitates: that is the (1 + x0 a^2) factor.")
    out["O2_weyl_fluid"] = ("The Weyl fluid is E_eff = (k- E+ - k+ E-)/(k- - k+): traceless (each E+- is), and by the 4D Bianchi identity "
                            "div E_eff = -8 pi G4 div tau + div F_eff, i.e. Bianchi-sourced by the wall's energy-momentum exchange, with the dark-bubble relative sign (O2_bianchi_check). "
                            "Its anisotropic stress is pi_eff = (k- pi+ - k+ pi-)/(k- - k+), so a bulk solve must supply BOTH sides' pi+-.")
    # O3: drag 00 factor (CN gauge, N = ln a time, envelope normalisation)
    x0, a, E, Psi_p, Phi = sp.symbols("x0 a E Psi_p Phi", real=True)
    Omd = x0 * a**2 * E**2
    Dd = -2 * Omd * (Psi_p + Phi)             # delta(Delta Sigma)/rho_c with Delta Sigma ~ local H^2 (envelope law)
    term_anti = -sp.Rational(3, 2) / E**2 * Dd   # anti-gravitating wall-localized source in the 00 constraint
    assert sp.simplify(3 * (Psi_p + Phi) + term_anti - 3 * (1 + x0 * a**2) * (Psi_p + Phi)) == 0
    term_pos = +sp.Rational(3, 2) / E**2 * Dd
    out["O3_drag_factor"] = ("The envelope's 3(1 + x0 a^2)(Psi' + Phi) follows exactly from an anti-gravitating wall-localized drag with "
                             "Delta Sigma proportional to the local H^2 (delta Delta Sigma = -2 Omega_d (Psi' + Phi)). A positively gravitating drag "
                             "would give 3(1 - x0 a^2). The perturbation law itself is not fixed by a 5D action for the w_d = 0 branch [O]; for the "
                             "covariant sigma(X) it would be delta X, which involves the wall bending (Phase 2).")
    out["O3_check"] = {"anti_gravitating_gives": "3(1 + x0 a^2)(Psi'+Phi)", "positive_would_give": str(sp.factor(3 * (Psi_p + Phi) + term_pos))}
    out["O4_matter_sector"] = ("Ordinary 4D matter gravitates with +G4 only through bulk terms: either it is bulk-sourced (string endpoints, "
                               "F_eff = (k- F+ - k+ F-)/(k- - k+), F = (2 kappa5/3)[T_mn + (T_nn - T/4) h_mn]), or it sits on the wall and its induced "
                               "bulk response (part of E_eff/F_eff) overcompensates its -8 pi G4 term. Either way the envelope's +G4 matter "
                               "fluids assume that this bulk response tracks 4D perfect-fluid perturbations. That is verified only in the Newtonian "
                               "1/p^2 limit (1807.01570, 2001.07433) [O]. It also means the 'free' Weyl fluid the envelope closes with Hu "
                               "parameters is E_eff minus the matter-induced response.")
    # O5: projected null dust T = psi l l (T = 0): F_mn = (2 kappa5/3)[psi l_m l_n + psi (l.n)^2 h_mn], tangential l along u.
    k, aa, Hh, mudot = sp.symbols("k a H mudot", positive=True)
    tau_ = sp.Symbol("tau", real=True)
    f = k**2 * aa**2
    ad = aa * Hh
    Td = sp.sqrt(f + ad**2) / f
    l_low = [-1, -1 / f]                      # l_A = -d_A v, v = t + r*, in (t, r)
    u_up = [Td, ad]
    n_up = [ad / f, f * Td]                   # n^A = g^AB n_B with n_B = (-adot, Tdot)
    l_u = sp.simplify(l_low[0] * u_up[0] + l_low[1] * u_up[1])
    l_n = sp.simplify(l_low[0] * n_up[0] + l_low[1] * n_up[1])
    Vdot = (sp.sqrt(f + ad**2) + ad) / f
    assert sp.simplify(l_u + Vdot) == 0 and sp.simplify(l_n**2 - Vdot**2) == 0   # nullness: (l.u)^2 = (l.n)^2
    psi_kap = sp.Rational(3, 2) * mudot / aa**3          # kappa5 T_vv from E_vv = 3 mudot/(2 r^3)
    F_tt_mixed = sp.simplify(-(sp.Rational(2, 3) * psi_kap * (l_u**2 - l_n**2)))   # F^tau_tau
    F_xx_mixed = sp.simplify(sp.Rational(2, 3) * psi_kap * l_n**2)                 # F^x_x
    assert F_tt_mixed == 0
    Exx_rate_over_H = mudot * Vdot / aa**4 / Hh          # |(1/H) d(E^x_x)/dtau|, E^x_x = -mu/a^4
    ratio = sp.simplify(F_xx_mixed / Exx_rate_over_H)
    eps = sp.Symbol("eps", positive=True)
    lead = sp.series(ratio.subs(Hh, eps * k), eps, 0, 3).removeO()
    out["O5_null_dust_projection"] = (f"F^tau_tau = 0 exactly (nullness forces (l.u)^2 = (l.n)^2); the null dust projects as a pure pressure "
                                      f"F^x_x = (2 kappa5/3) psi (l.n)^2. Ratio to the Weyl pressure growth per Hubble time: {sp.simplify(lead)} "
                                      f"(eps = H/k), i.e. O(H/k): negligible at the envelope's order.")
    # O2 check: background Bianchi with 4G = -8 pi G4 tau - E_eff, E_eff traceless (E^t_t = 8 pi G4 rho_W, E^x_x = -8 pi G4 rho_W/3)
    t = sp.Symbol("t", real=True)
    G4s = sp.Symbol("G4", positive=True)
    A = sp.Function("A", positive=True)(t)
    rW, rT, pT = (sp.Function(nm)(t) for nm in ("rhoW", "rhotau", "ptau"))
    Hd = sp.diff(A, t) / A
    fried = sp.Eq(3 * Hd**2, 8 * sp.pi * G4s * (rW - rT))                      # from G^t_t = -3H^2
    ray = sp.Eq(-(2 * sp.diff(A, t, 2) / A + Hd**2), -8 * sp.pi * G4s * pT + 8 * sp.pi * G4s * rW / 3)  # G^x_x
    addot = sp.solve(ray, sp.diff(A, t, 2))[0]
    dfried = sp.diff(fried.lhs - fried.rhs, t).subs(sp.diff(A, t, 2), addot)
    Hsq = sp.solve(fried, sp.diff(A, t))  # use Friedmann to remove H^2 where needed
    lawW = sp.diff(rW, t) + 4 * Hd * rW - (sp.diff(rT, t) + 3 * Hd * (rT + pT))
    chk = sp.simplify(dfried / (8 * sp.pi * G4s) + lawW)
    chk = sp.simplify(chk.subs(Hd**2, 8 * sp.pi * G4s * (rW - rT) / 3))
    assert sp.simplify(sp.expand(chk)) == 0
    out["O2_bianchi_check"] = ("Background: 3H^2 = 8 pi G4 (rho_W - rho_tau) and the Raychaudhuri equation imply "
                               "rho_W' + 4H rho_W = rho_tau' + 3H(rho_tau + p_tau) = Q4: the Weyl fluid GAINS what the wall gains, the dark-bubble "
                               "relative sign (Randall-Sundrum has the opposite: rho_W' + 4H rho_W = -Q). FLUX_CODAZZI uses the dark-bubble sign.")
    out["O2_amplification"] = ("E_eff = E+ + (k+/(k- - k+))(E+ - E-), and likewise pi_eff. For k- - k+ << k, the jump between the two sides is "
                               "amplified by k/(k- - k+): pi_eff ~ 0 needs pi+ and pi- to cancel to about (k- - k+)/k.")
    return out


def main() -> int:
    res = {"C1": c1_exact_background()}
    res.update(c2_c3_c4())
    res.update(outputs())
    res["preregistered_decision"] = (
        "CONFIRMED (in form). Outputs 1-3 match the envelope's structure at linear order and leading order in H/k: "
        "(1) the only wall-localized term in the envelope, the drag, enters with the anti-gravitating sign that gives 3(1 + x0 a^2)(Psi'+Phi); "
        "(2) the Weyl fluid is E_eff = (k- E+ - k+ E-)/(k- - k+), traceless and Bianchi-sourced with the dark-bubble sign, so the envelope's "
        "pi_E stands for pi_eff = (k- pi+ - k+ pi-)/(k- - k+); "
        "(3) the drag factor follows exactly for Delta Sigma ~ local H^2, which is a modeling choice for the w_d = 0 branch [O]. "
        "Output 4 [O]: +G4 matter is carried by bulk terms (strings, or the overcompensating bulk response to wall matter); that it "
        "perturbs like 4D fluids is verified only in the Newtonian limit, and the envelope's 'free' Weyl fluid is E_eff minus that response."
    )
    print(json.dumps(res, indent=1))
    json.dump(res, open(os.path.join(HERE, "P0_ASYMMETRIC_WALL.json"), "w"), indent=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
