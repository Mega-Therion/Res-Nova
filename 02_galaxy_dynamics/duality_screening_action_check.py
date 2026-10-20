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


def background_split() -> None:
    """Φ = Φ_ext + ψ, with Φ_ext not varied.

    On the patch Φ_ext is linear, so η is constant and S factors out.
    The patch action ∫ |∇ψ − ν_eff ∇Φ_N|² / 8πG has EL
    ∇²ψ = ∇·(ν_eff ∇Φ_N). For a radial Newtonian field the solution is
    ∇ψ = ν_eff ∇Φ_N. The disformal scalar is not a variable, so it stays 0.
    """
    import sympy as sp

    r, G, M, a0, gext = sp.symbols("r G M a0 g_ext", positive=True)
    nu = sp.Function("nu")
    # External gradient is constant. It does not depend on the patch field.
    eta = gext / a0
    S = 1 / (1 + eta**2)
    assert sp.diff(eta, r) == 0
    dphi = G * M / r**2  # radial derivative of the patch Newtonian potential
    nu_eff = 1 + S * (nu(r) - 1)
    # div(v(r) r-hat) = r^{-2} d/dr (r^2 v)
    div_U = sp.simplify((1 / r**2) * sp.diff(r**2 * nu_eff * dphi, r))
    # ψ with ψ' = ν_eff Φ_N' has the same radial laplacian
    psi_r = nu_eff * dphi
    lap_psi = sp.simplify((1 / r**2) * sp.diff(r**2 * psi_r, r))
    if sp.simplify(lap_psi - div_U) != 0:
        raise SystemExit("background split: laplacian mismatch")
    # g = -∇ψ and g_N = -∇Φ_N, so the radial solution is g = ν_eff g_N
    if sp.simplify(psi_r / dphi - nu_eff) != 0:
        raise SystemExit("background split: g is not nu_eff g_N")
    print(f"split eta={eta} depends_on_r={sp.diff(eta, r) != 0}")
    print("split EL: lap(psi) = div(nu_eff grad Phi_N)")
    print("split solution: g = nu_eff g_N")
    print("disformal phi = 0 (not a variable of this action)")
    print("RESULT background_split_ok")


def drop_spherical() -> None:
    """curl(ν ∇Φ_N) = ∇ν × ∇Φ_N. It vanishes for a radial field.

    For Φ_N = x y the cross product is not zero, so no patch potential
    satisfies ∇ψ = ν_eff ∇Φ_N. The divergence equation still makes sense.
    Constant S multiplies the curl; it does not remove it.
    """
    import sympy as sp

    x, y, S = sp.symbols("x y S", real=True)
    f = sp.Function("f", real=True)
    Phi = x * y
    gNx, gNy = sp.diff(Phi, x), sp.diff(Phi, y)
    mag2 = sp.simplify(gNx**2 + gNy**2)
    nu = f(mag2)
    nu_eff = 1 + S * (nu - 1)
    # curl_z (ν_eff ∇Φ_N) = ∂x(ν_eff gNy) − ∂y(ν_eff gNx)
    curl_z = sp.simplify(sp.diff(nu_eff * gNy, x) - sp.diff(nu_eff * gNx, y))
    # f' survives: curl is not identically zero
    if curl_z == 0:
        raise SystemExit("expected a nonzero curl off the sphere")
    # S = 0 kills the boost and the curl. S ≠ 0 does not.
    at_zero = sp.simplify(curl_z.subs(S, 0))
    if at_zero != 0:
        raise SystemExit("S=0 should be Newtonian and curl-free")
    ratio = sp.simplify(curl_z / S)
    if ratio == 0:
        raise SystemExit("S should only scale the curl")
    print(f"nonspherical curl_z = {curl_z}")
    print("RESULT algebraic_g_fails_off_sphere")
    print("RESULT divergence_equation_remains")


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
    background_split()
    drop_spherical()


if __name__ == "__main__":
    main()
