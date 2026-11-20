#!/usr/bin/env python3
"""Phase 3 Test S (PREREG_PHASE3.md): covariant drag-action scan.

(i)   Tangential Killing coupling L(Y, phi), Y = -h^{mu nu} xi_mu xi_nu (xi = d/dt, bulk static Killing).
(iii) Static bulk medium with friction, Q = C rho_med(r) v^3, v = adot/sqrt(f).
(ii)  Radial string forest: not tested (no concrete action specified).
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))


def candidate_i() -> dict:
    out = {}
    k, mu = sp.symbols("k mu", positive=True)
    tau = sp.Symbol("tau", real=True)
    a = sp.Function("a", positive=True)(tau)
    ad = sp.diff(a, tau)
    f = k**2 * a**2 - mu / a**2
    Td = sp.sqrt(f + ad**2) / f
    # xi_tau = e^A_tau g_AB xi^B = Tdot * g_tt = -f Tdot ; h^{tautau} = -1
    xi_tau = -f * Td
    Y = sp.simplify(-(-1) * xi_tau**2)
    X = ad**2
    assert sp.simplify(Y - (f + X)) == 0
    out["i_Y_identity"] = "Y = f + X on the wall (X = (xi.n)^2 = adot^2) [D]"
    # stress tensor of S = int sqrt(-h) L(Y): S_mn = 2 L_Y xi_m xi_n + L h_mn  ->  u = xi_par/sqrt(Y): rho = 2 Y L_Y - L, p = L
    Yv, Lam, M, F, rho_b, Xs, fs, dl = sp.symbols("Y Lambda M F rho_b X f delta", real=True)
    L = Lam + sp.Rational(1, 2) * M * (Yv - F) ** 2
    LY = sp.diff(L, Yv)
    rho = 2 * Yv * LY - L
    p = L
    sub = {Yv: fs + Xs, F: fs}
    rho_d = sp.expand((rho + Lam).subs(sub))          # X-dependent part (Lambda is the tension)
    p_d = sp.expand((p - Lam).subs(sub))
    w_d = sp.simplify(p_d / rho_d)
    assert sp.simplify(w_d - Xs / (4 * fs + 3 * Xs)) == 0
    out["i_w_d"] = "w_d = X/(4f + 3X) ~ (H/k)^2/4: dust-like [D]  (criterion 1: pass)"
    Msol = sp.solve(sp.Eq(rho_d, rho_b * Xs / 2), M)[0]
    out["i_M_for_drag"] = f"M = {sp.simplify(Msol)} ~ rho_b/(4 k^2 r^2) reproduces Delta Sigma = rho_b adot^2/2 [D]"
    # frame: u_xi = xi_par/sqrt(Y) has u_tau = xi_tau/sqrt(Y) = -1 on the background: the dust rides the bulk static frame
    assert sp.simplify(xi_tau / sp.sqrt(Y) + 1) == 0
    out["i_frame"] = ("The dust's 4-velocity is u_xi = xi_par/sqrt(Y), fixed by geometry: it is locked to the bulk static frame, "
                      "not free-falling. In the bulk-rest flux frame that is F_d = 0: Law C (criterion 5). [D]")
    # detuning: F = f + delta adds an X-independent dust piece rho_delta ~ -2 f M delta; it must stay below the drag (rho_b X/2)
    rho_det = sp.expand((rho + Lam).subs({Yv: fs + Xs, F: fs + dl}).subs(M, Msol)) - rho_d.subs(M, Msol)
    lead = sp.limit(rho_det / dl, dl, 0)
    out["i_detuning"] = (f"F = f + delta adds d(rho)/d(delta) = {sp.simplify(lead)} at delta -> 0 (an anti-gravitating dust term "
                         "independent of adot). Keeping it below the drag rho_b X/2 needs |delta|/f < X/f ~ (H/k)^2 [D].")
    c = 299792458.0
    Mpc = 3.0856775814913673e22
    HoK = 67.4e3 / Mpc * 5e-5 / c
    out["i_tuning_micron"] = f"micron example: required |delta|/f < (H0/k)^2 ~ {HoK**2:.1e}"
    # covariant enforcement F := -xi.xi makes Y - F = X: full 5D metric variation of X is purely normal-normal
    out.update(_normal_variation_check())
    out["i_energy"] = ("Criteria 2 and 4: with Delta Sigma = rho_b adot^2/2 by construction and w_d ~ 0, the wall energy equation gives "
                       "Q4 = Delta Sigma' + 3H Delta Sigma = 2H Delta Sigma (3/2 - q) >= 2H Delta Sigma > 0 on z in [0, 10] "
                       "(fitted q in [-0.41, 0.50], candidate_iii q_range). The exchange partner is the bulk scalar phi whose profile "
                       "carries the coupling functions F(phi), M(phi) (explicit phi-dependence plus the mixed normal-tangential source). [D]")
    out["i_verdict"] = ("(i) passes criteria 1, 2, 4 and gives Law C (criterion 5), but fails criterion 3: the O(k^2 a^2) term cancels only "
                        "if the coupling's stationary point F equals f to relative precision (H/k)^2 (~1e-61 for micron AdS). Enforcing "
                        "F = -xi.xi covariantly removes the tangential dust (the variation is purely normal-normal), reducing to "
                        "candidate (a), w = -1. Ghost/gradient stability: not tested. [D]/[X] as a natural mechanism")
    return out


def _normal_variation_check() -> dict:
    """Numerically differentiate X = Y + xi.xi w.r.t. every bulk metric component at a wall point; compare with X n^A n^B."""
    kk, muv, aa, adv = 1.3, 0.4, 2.0, 0.37
    f = kk**2 * aa**2 - muv / aa**2
    Td = math.sqrt(f + adv**2) / f
    # tangent vectors at the wall point (t, r, x, y, z): e_tau = (Td, adot, 0,0,0), e_i = d_i
    E = np.zeros((4, 5))
    E[0, 0], E[0, 1] = Td, adv
    E[1, 2] = E[2, 3] = E[3, 4] = 1.0
    xi = np.array([1.0, 0, 0, 0, 0])

    def X_of(g):
        h = E @ g @ E.T
        hinv = np.linalg.inv(h)
        xil = E @ (g @ xi)
        Y = -xil @ hinv @ xil
        return Y + xi @ g @ xi

    def nn_of(g):
        # unit normal: the covector annihilating all tangents, normalised with g
        gi = np.linalg.inv(g)
        A = E
        # null space of E (4x5) gives n_A
        u, s, vt = np.linalg.svd(A)
        nl = vt[-1]
        nl = nl / math.sqrt(nl @ gi @ nl)
        nu = gi @ nl
        return np.outer(nu, nu)

    g0 = np.diag([-f, 1 / f, aa**2, aa**2, aa**2])
    X0 = X_of(g0)
    J = np.zeros((5, 5))
    eps = 1e-6
    for A in range(5):
        for B in range(A, 5):
            dg = np.zeros((5, 5))
            dg[A, B] += eps
            if A != B:
                dg[B, A] += eps
            J[A, B] = (X_of(g0 + dg) - X_of(g0 - dg)) / (2 * eps)
            if A != B:
                J[A, B] /= 2.0
                J[B, A] = J[A, B]
    target = X0 * nn_of(g0)
    err = float(np.max(np.abs(J - target)))
    assert err < 1e-6, err
    return {"i_covariant_variation": f"d(Y + xi.xi)/d g_AB = X n^A n^B to {err:.1e} (numerical, generic wall point): purely normal-normal [D]"}


def candidate_iii() -> dict:
    sys.path.insert(0, os.path.join(HERE, "..", "drag_gcosmo"))
    cwd = os.getcwd()
    os.chdir(os.path.join(HERE, "..", "drag_gcosmo"))
    try:
        import flux_codazzi_check as Fz
    finally:
        os.chdir(cwd)
    rec = json.load(open(os.path.join(HERE, "..", "drag_gcosmo", "FLUX_CODAZZI.json")))
    h, Om, kap = rec["F2_self_consistent_coupled_refit"]["Pantheon+_BAO_CMB"]["params_coupled_h_Om_kappa"]
    z = np.linspace(0.0, 10.0, 4001)
    E, _ = Fz.E_coupled(z, h, Om, kap)
    q = -1.0 + (1.0 + z) * np.gradient(np.log(E), z)
    shape = 1.5 - q                      # Q_req / (2 H DeltaSigma) at w_d = 0
    # friction: Q = C rho_med(r) v^3, v = H/k, Delta Sigma ~ a^2 H^2  =>  required rho_med(r = a) ~ a^2 (3/2 - q(a))
    a = 1.0 / (1.0 + z)
    prof = a**2 * shape
    # best pure power law r^n fit to the required profile, and its worst deviation
    n, lnA = np.polyfit(np.log(a), np.log(prof), 1)
    dev = float(np.max(np.abs(np.exp(lnA) * a**n / prof - 1.0)))
    return {
        "iii_sign": "Q = C rho_med v^3 >= 0 at every epoch: single-sign inflow (criterion 2: pass) [D]",
        "iii_required_profile": (f"closing Delta Sigma' + 3H Delta Sigma = Q with Delta Sigma ~ a^2 H^2 needs rho_med(r) ~ r^2 (3/2 - q(r)) "
                                 f"on the wall's path; (3/2 - q) runs {shape.min():.2f}-{shape.max():.2f} on z in [0, 10]; best power law r^{n:.2f} "
                                 f"misses by up to {100*dev:.0f}%: the medium's radial profile must encode the fitted expansion history [D]"),
        "iii_heat_channel": ("Criterion 1 depends on what absorbs the dissipated energy: wall radiation (w = 1/3) is the conformal case, which "
                             "cancels the drag exactly (FLUX_CODAZZI kappa = 0); massive wall dust (w = 0) keeps it. Not fixed by friction itself."),
        "iii_backreaction": "rho_med/|rho_Lambda5| ~ 2 x0 (Delta k/k) ~ 4.6 Delta k/k at x0 = 2.24: perturbative only for Delta k/k << 0.2 (brainstorm arithmetic, re-derived)",
        "iii_momentum_law": "tangential friction against a medium at rest in the static frame pins wall matter toward that frame: a Law-B relaxation with rate set by the same coupling [O]",
        "iii_verdict": ("(iii) passes criterion 2, meets criterion 4 only with a radial profile tuned to the fitted q(z), and leaves criterion 1 "
                        "to the unspecified heat channel; criterion 6 not tested. A different model needing its own refit, not a closure [O]."),
        "q_range": [float(q.min()), float(q.max())],
    }


def main() -> int:
    res = {"candidate_i": candidate_i(), "candidate_iii": candidate_iii(),
           "candidate_ii": "Radial string-forest pinning: not tested (no concrete action specified).",
           "verdict": ("None of the tested candidates is a natural covariant source of the w_d = 0 drag. (i) gives Law C only with an "
                       "(H/k)^2 tuning, and its covariant form collapses to the w = -1 tension already excluded; (iii) needs a profile "
                       "tuned to the expansion history and an unspecified heat channel. (ii) untested.")}
    print(json.dumps(res, indent=1))
    json.dump(res, open(os.path.join(HERE, "PHASE3_DRAG_ACTION_SCAN.json"), "w"), indent=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
