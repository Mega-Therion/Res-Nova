#!/usr/bin/env python3
"""Field equation of the quasistatic duality-screening action.

S[Phi] variation gives div U = 4 pi G rho with U = nu_eff grad Phi_N
and nu_eff = 1 + S(eta) * (nu - 1), S = 1 / (1 + eta**2).
Prints the Sun's screened Cassini tension from the recorded bare Q2.
"""


def s_of(eta: float) -> float:
    return 1.0 / (1.0 + eta * eta)


def nu_eff(nu: float, eta: float) -> float:
    return 1.0 + s_of(eta) * (nu - 1.0)


def main() -> None:
    # Algebra: d/dz [S Q] = S Q' when S is constant on the patch.
    # Q' = nu - 1, so 1 + d/dz [S Q] = nu_eff.
    for eta, nu in ((0.1, 3.0), (2.0, 3.0)):
        got = nu_eff(nu, eta)
        assert got == 1.0 + s_of(eta) * (nu - 1.0)
        print(f"eta={eta} S={s_of(eta):.4f} nu={nu} nu_eff={got:.4f}")
    bare = 17.2e-27  # mu_std at g_ext = 2.4e-10, CASSINI_EFE_QUADRUPOLE_2026-09-27
    a0 = 1.1e-10
    for ge in (1.9e-10, 2.4e-10):
        q = s_of(ge / a0) * bare
        sigma = (q - 1.6e-27) / 1.8e-27
        print(f"g_ext={ge:.3e} eta={ge/a0:.3f} Q2={q:.3e} sigma={sigma:+.3f}")


if __name__ == "__main__":
    main()
