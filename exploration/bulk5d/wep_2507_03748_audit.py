#!/usr/bin/env python3
"""Audit of arXiv:2507.03748 (Basile, Borys, Masias): dark-bubble non-abelian sign and the proton WEP.

Read from the paper's TeX source (prl_draft.tex) and arXiv:2310.15032 sec. 4.
Does not edit README.md or CURRENT_STATE. Labels: [D] derived here, [C] literature input.

C1  Sign rule: wall-localized stress gravitates with weight -1 (our B4); a bulk field linearly sourced
    by the worldvolume field adds +beta. Abelian DBI: beta = 2 -> +1. su(N): Tr T^a = 0 kills the linear
    B-coupling -> beta = 0 -> -1 at leading order in alpha'.
C2  Proton: weights +1 (quarks, paper's assumption) and -1 (gluons) with LQCD A_q, A_g (Hackett et al.).
    Robustness: RG running (asymptotic A_g = 16/(16 + 3 n_f) at a string scale), and the omitted cbar term.
C3  Electroweak check of the paper's own rule: a massive vector at rest splits its energy equally between
    field-strength and mass terms, so -T_{SU(2)} + T_Higgs gives m_grav(W) = 0, not m_W. The photon under
    "SU(2) negative, U(1)_Y positive" gravitates with cos(2 theta_W).
C4  Active vs passive: brane matter follows induced-metric geodesics, so free fall (passive mass) stays
    universal. The rule makes ACTIVE mass composition-dependent. LLR Al/Fe active/passive bound.
C5  Single-metric minimal coupling (live Res-Nova seat): weight 1 for every sector, eta_active = 0.
"""
from __future__ import annotations

import json
import math
import os

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))


def c1_sign_rule() -> dict:
    beta = sp.Symbol("beta", real=True)
    w_net = -1 + beta  # brane piece (-1, B4 / 2310.15032 sec. 4) plus linear bulk backreaction (+beta)
    assert w_net.subs(beta, 2) == 1      # abelian: "2T - T = +T" (2507.03748 sec. 3; 2310.15032 eq. after 243)
    assert w_net.subs(beta, 0) == -1     # no linear bulk source
    # Gell-Mann matrices: every su(3) generator is traceless, so B * Tr(F) has no linear gluon piece.
    I = sp.I
    lam = [
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, -I, 0], [I, 0, 0], [0, 0, 0]]),
        sp.Matrix([[1, 0, 0], [0, -1, 0], [0, 0, 0]]),
        sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 0, -I], [0, 0, 0], [I, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, -I], [0, I, 0]]),
        sp.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, -2]]) / sp.sqrt(3),
    ]
    assert all(m.trace() == 0 for m in lam)
    # sanity: they are a normalized basis, Tr(lam_a lam_b) = 2 delta_ab
    assert all(sp.simplify((lam[a] * lam[b]).trace() - (2 if a == b else 0)) == 0 for a in range(8) for b in range(8))
    # and Tr of a generic su(3) field strength F = F^a lam_a/2 vanishes identically
    Fa = sp.symbols("F1:9", real=True)
    Fmat = sum((Fa[a] * lam[a] / 2 for a in range(8)), sp.zeros(3, 3))
    assert sp.simplify(Fmat.trace()) == 0
    return {
        "rule": "w_net = -1 + beta; beta = 2 (abelian, linear Delta H ~ F) gives +1; beta = 0 (su(N), Tr F = 0) gives -1 [D]",
        "consistency_with_B4": ("PHASE3_WALL_GHOST_COUPLED B4: wall bending alone leaves wall-localized stress at Phi = +4 pi G4 rho/k^2 "
                                "(repulsive). That is the -1 the paper starts from; 2310.15032 sec. 4 states the same "
                                "(brane matter negative, overcompensated by H-field backreaction) [D]+[C]"),
        "su3_traceless_checked": True,
    }


def c2_proton() -> dict:
    Aq, sAq = 0.510, 0.025   # [C] Hackett, Pefkou, Shanahan (2507.03748 eq. for A_q(0))
    Ag, sAg = 0.501, 0.027   # [C]
    R = Aq - Ag
    sR = math.hypot(sAq, sAg)
    dev = 1.0 - R
    assert abs(R - 0.009) < 1e-12 and abs(round(sR, 3) - 0.037) < 1e-12
    assert abs(dev - 0.991) < 1e-12
    # RG: A_q and A_g mix; the split is scale dependent. At a high (string) scale A_g -> 16/(16 + 3 n_f).
    nf = sp.Symbol("n_f", positive=True)
    Ag_inf = 16 / (16 + 3 * nf)
    asym = {int(n): float(Ag_inf.subs(nf, n)) for n in (3, 5, 6)}
    assert sp.Rational(16, 34) == Ag_inf.subs(nf, 6)
    ratio_asym = {n: 1 - 2 * a for n, a in asym.items()}   # m_g/m_i with cbar = 0
    # cbar: <T_a^{00}> = (A_a + cbar_a) m at rest, cbar_q + cbar_g = 0. Scan |cbar_g| <= 0.2 (generous band).
    band = [1 - 2 * (Ag + c) - 0 for c in (-0.2, 0.2)]
    worst_case_closest_to_1 = max(abs(1 - (1 - 2 * (Ag + c))) for c in (-0.2, 0.2))
    best = min(abs(2 * (Ag + c)) for c in (-0.2, 0.2))   # |1 - m_g/m_i| = 2 f_g
    assert best > 0.5
    return {
        "Aq_minus_Ag": f"{R:.3f} +- {sR:.3f} (matches the paper's 0.009 +- 0.037) [D]",
        "fractional_deviation": f"{dev:.3f} (paper: 0.99) [D]",
        "string_scale_Ag_asymptotic": {f"n_f={n}": round(a, 4) for n, a in asym.items()},
        "string_scale_mg_over_mi_cbar0": {f"n_f={n}": round(r, 4) for n, r in ratio_asym.items()},
        "cbar_band_mg_over_mi": [round(b, 3) for b in band],
        "robust_min_deviation": f"|1 - m_g/m_i| = 2 f_g >= {best:.2f} for |cbar_g| <= 0.2 [D]",
        "verdict": ("The O(1) deviation is robust: it needs only that gluons carry O(1/2) of the proton's rest energy, which holds "
                    "at hadronic scales and at the ~11 TeV string scale of 2311.14589 (RG fixed point A_g ~ 0.47-0.52). The exact "
                    "0.009 is not robust (scheme dependent; cbar omitted; central value consistent with zero or negative)."),
        "mass_origin_link": ("Most proton mass is QCD (quark motion + gluon field + trace anomaly), not Yukawa. The sign rule splits "
                             "exactly along that decomposition, which is why the effect is O(1) and not O(1%)."),
    }


def c3_electroweak() -> dict:
    t = sp.Symbol("t", real=True)
    m, A = sp.symbols("m A", positive=True)
    Ai = A * sp.cos(m * t)                    # Proca mode at rest, A_0 = 0
    E2 = sp.diff(Ai, t) ** 2                  # F_{0i}^2
    rho_F = E2 / 2
    rho_m = m**2 * Ai**2 / 2
    T = 2 * sp.pi / m
    avg = lambda f: sp.simplify(sp.integrate(f, (t, 0, T)) / T)
    assert sp.simplify(avg(rho_F) - avg(rho_m)) == 0
    rho_inert = avg(rho_F + rho_m)
    rho_grav = avg(-rho_F + rho_m)            # -T_SU(2) (field strength) + T_Higgs (mass term)
    assert rho_grav == 0 and rho_inert != 0
    s2w = 0.2312                              # [C] sin^2 theta_W(M_Z), MSbar
    photon_weight = (1 - s2w) - s2w           # B part +1, W3 part -1
    assert abs(photon_weight - (1 - 2 * s2w)) < 1e-15
    return {
        "W_Z_at_rest": "time-averaged field-strength energy = mass-term energy; -T_SU(2) + T_Higgs gives m_grav = 0, m_inert = m [D]",
        "paper_claim_checked": ("2507.03748 sec. 3 diagonalises only the Higgs mass matrix (the inertial spectrum) and concludes "
                                "m_grav = m_inert for W, Z. Its own sign rule gives m_grav(W, Z) = 0 at tree level. [D]"),
        "photon_weight_under_paper_rule": f"cos(2 theta_W) = {photon_weight:.4f}, not 1 [D] (unless U(1)_em is the brane trace U(1); model dependent)",
        "impact": "Does not rescue the model. W, Z are unstable and irrelevant to WEP tests; it shows the EW section is incomplete.",
    }


def c4_active_passive() -> dict:
    aC, mu, me = 0.711, 931.494, 0.511        # [C] MeV: SEMF Coulomb coefficient, atomic mass unit, electron mass

    def fractions(Z: int, Aw: int) -> tuple[float, float]:
        M = Aw * mu
        return aC * Z * (Z - 1) / Aw ** (1 / 3) / M, Z * me / M

    fC_Al, fe_Al = fractions(13, 27)
    fC_Fe, fe_Fe = fractions(26, 56)
    out_rows = []
    etas = []
    for RB in (0.009 - 0.074, 0.009 - 0.037, 0.009, 0.009 + 0.037, 0.009 + 0.074):
        for we in (+1, -1):                   # electron weight: the paper is silent
            def ratio(fC, fe):
                return RB * (1 - fC - fe) + 1.0 * fC + we * fe
            rAl, rFe = ratio(fC_Al, fe_Al), ratio(fC_Fe, fe_Fe)
            mean = 0.5 * (rAl + rFe)
            eta = abs(rAl - rFe) / abs(mean)
            etas.append(eta)
            out_rows.append({"R_B": round(RB, 3), "w_e": we, "eta_active_Al_Fe": float(f"{eta:.2e}")})
    eta_min = min(etas)
    bound_llr = 3.9e-14                        # [C] Singh, Mueller et al., PRL 131, 021401 (2023)
    bound_bvb = 4e-12                          # [C] Bartlett & Van Buren, PRL 57, 21 (1986)
    assert eta_min > 1e8 * bound_llr
    return {
        "passive_mass": ("Brane fields couple minimally to the induced metric h_ab and follow its geodesics, so free fall is "
                         "universal: the rule does not by itself violate passive WEP (MICROSCOPE tests passive mass). [D]"),
        "active_mass": "The rule changes the SOURCE T^{00}: active/inertial mass becomes composition dependent. [D]",
        "paper_bounds_critique": ("2507.03748 uses MICROSCOPE (passive) and an Si-28/Avogadro comparison. Both compare baryonic matter "
                                  "with baryonic matter or test free fall, so a universal baryon factor cancels or does not enter; a universal "
                                  "factor would be absorbed into G4. The decisive test is active-mass composition dependence. [D]"),
        "coulomb_fraction": {"Al27": float(f"{fC_Al:.3e}"), "Fe56": float(f"{fC_Fe:.3e}")},
        "scan": out_rows,
        "eta_active_min_over_scan": float(f"{eta_min:.2e}"),
        "bounds": {"LLR_Singh2023": bound_llr, "LLR_BartlettVanBuren1986": bound_bvb},
        "orders_of_magnitude_excess": round(math.log10(eta_min / bound_llr), 1),
        "verdict": ("Nuclear Coulomb energy (abelian, weight +1) against QCD binding (weight ~0) makes Al and Fe differ in active "
                    "mass by eta >= 1e-2 over the whole LQCD band and either electron sign, about 11 orders above LLR. The paper's "
                    "conclusion survives, through the active-mass channel it did not use. [D]"),
    }


def c5_single_metric() -> dict:
    w = {"quarks": 1, "gluons": 1, "electroweak": 1, "photons": 1, "leptons": 1}
    assert all(v == 1 for v in w.values())
    return {"weights": w, "eta_active": 0,
            "note": ("Minimal coupling of every sector to one metric g (Res-Nova seat; disformal coupling [X] RN-GEA-RETIRED-001) gives "
                     "T^{mu nu}_total with unit weight per sector: m_active = m_passive = m_inertial identically. [D]")}


def implications() -> dict:
    return {
        "phase2_matter_sector_scope": ("PHASE2_MATTER_SECTOR's +G4 result is for stretched-string endpoints (dust of mass tau/k). SM baryons "
                                       "are not stretched strings: under 2507.03748 about half their rest energy (gluons) gravitates with -1. "
                                       "The [D] status holds for string-endpoint dust only."),
        "envelope_embedding": ("The drag_gcosmo / bulk5d envelope treats baryons and CDM as +G4 fluids. Inside the dark-bubble "
                               "embedding as currently formulated, baryons have m_g/m_i ~ 0 +- 0.04 (or ~0.06 at the string scale). "
                               "The cosmological embedding is inconsistent with its own matter coupling unless a new mechanism "
                               "(not B, C2 fields) couples gluons to induced gravity with weight +1."),
        "drag_seat": ("The drag condensate is meant to sit in the -G4 seat (B4). That is a feature for a dark component, not a WEP "
                      "problem, but it does not help the baryon sector."),
        "loopholes_open": [
            "[O] A non-B/C mechanism coupling non-abelian fields linearly to a bulk mode (e.g. non-normalizable boundary conditions, 2311.16242).",
            "[O] Quark sign: the paper assumes +1 for quarks without derivation; brane-localized fermions would naively be -1 as well.",
            "[O] Higher-order alpha' terms (Tr F^3, Tr F^4) are subleading and cannot flip the leading sign (paper's argument; not re-derived).",
        ],
    }


def main() -> int:
    res = {
        "source": "arXiv:2507.03748 TeX (prl_draft.tex) and arXiv:2310.15032 sec. 4, fetched 2026-11-20",
        "C1_sign_rule": c1_sign_rule(),
        "C2_proton": c2_proton(),
        "C3_electroweak": c3_electroweak(),
        "C4_active_passive": c4_active_passive(),
        "C5_single_metric": c5_single_metric(),
        "implications": implications(),
        "verdict": ("[D] The paper's conclusion stands and is stronger than stated: O(1) composition-dependent ACTIVE mass, excluded "
                    "by LLR by about 11 orders. Two corrections to the paper: its tests are the wrong channel (passive / baryon-vs-baryon), "
                    "and its electroweak section is incomplete (m_grav(W,Z) = 0, photon weight cos 2 theta_W under its own rule). "
                    "For bulk5d: the dark-bubble embedding cannot carry +G4 baryons as formulated."),
    }
    with open(os.path.join(HERE, "WEP_2507_03748_AUDIT.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
        f.write("\n")
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
