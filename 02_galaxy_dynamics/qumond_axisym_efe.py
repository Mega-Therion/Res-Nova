#!/usr/bin/env python3
"""Independent axisymmetric QUMOND external-field solver for the Cassini quadrupole Q2.

Pre-registration: NONSPHERICAL_EFE_SOLVER_PREREG_2026-10-27.md. Record:
NONSPHERICAL_EFE_SOLVER_2026-10-27.md. numpy/scipy only. Does NOT import
efe_quadrupole_q2.py (Milgrom's reduced double integral); the repo's numbers are
read only as JSON values by the validation driver.

Model (dimensionless: length r_M = sqrt(GM/a0), acceleration a0, potential a0 r_M)
    g_N   = -x/r^3 + y_e z^,      y_e nu(y_e) = g_e/a0
    lap Phi_a = -div V,           V = (nu(|g_N|) - nu_e) g_N
(QUMOND, a = -grad Phi. The removed piece (nu_e - 1) g_N is a point mass plus a
uniform field and carries no quadrupole.)

Method: Legendre projection in polar angle (Gauss nodes in theta), flux form of the
source so only V (a square-root cusp at the on-axis null of g_N) is sampled, never
its divergence (which is singular there). Each multipole l obeys, with s = ln r,
    u'' + u' - l(l+1) u = -e^{-s} d/ds(e^{2s} A_l) - e^{s} B_l
    A_l = (2l+1)/2 Int V_r P_l dmu,  B_l = (2l+1)/2 Int sin(theta) V_theta P_l'(mu) dmu
solved as a second-order tridiagonal BVP on a uniform s grid with the exact
source-free behaviours as boundary conditions: u ~ r^l at r_min, u ~ r^-(l+1) at r_max.
The quadrupole at the Sun is c2 = lim u_2/r^2. With Hees et al. 2014 Eq. 6
(Phi = -GM/r - (Q2/2) x^i x^j (e_i e_j - delta_ij/3), a = -grad Phi):
    Q2 = -3 c2 a0 / r_M,   and Milgrom's q = 2 c2.
"""
import numpy as np
from scipy.linalg import solve_banded
from scipy.optimize import brentq
from scipy.special import eval_legendre

GM = 1.32712e20
A0_FIT = 1.1607e-10
A0_DERIVED = 2.998e8 * (67.4e3 / 3.0857e22) / (2 * np.pi)


def nu_n(n):
    """Hees et al. 2016 eq. 5 family, exact inverse of mu_n = x/(1+x^n)^(1/n).
    Written as y^-1/2 [(y^(n/2) + sqrt(y^n + 4))/2]^(1/n): finite at the null of g_N."""
    def nu(y):
        y = np.maximum(np.asarray(y, dtype=float), 1e-300)
        a = y ** (n / 2.0)
        return y ** -0.5 * (0.5 * (a + np.sqrt(a * a + 4.0))) ** (1.0 / n)

    def nu_minus_1(y):
        """nu - 1 without cancellation at large y (needed near the Sun, where g_N ~ 1/r^2)."""
        y = np.maximum(np.asarray(y, dtype=float), 1e-300)
        scalar = y.ndim == 0
        y = np.atleast_1d(y)
        out = np.atleast_1d(nu(y) - 1.0).astype(float)
        big = y > 1e-2
        tb = 4.0 * y[big] ** (-float(n))
        out[big] = np.expm1(np.log1p(0.5 * tb / (np.sqrt(1.0 + tb) + 1.0)) / n)
        return out[0] if scalar else out

    nu.minus_1 = nu_minus_1
    return nu


def y_external(nu, eta):
    return brentq(lambda x: x * float(nu(x)) - eta, 1e-12, max(eta, 1.0) * 10, xtol=1e-15, rtol=1e-15)


def _legendre_deriv(l, mu):
    # P_l'(mu) via (1-mu^2) P_l' = l (P_{l-1} - mu P_l)
    return l * (eval_legendre(l - 1, mu) - mu * eval_legendre(l, mu)) / (1.0 - mu * mu)


def _AB(nu, nue, ye, r, th, w, l):
    """Projections A_l(r), B_l(r) of V at radii r (Gauss nodes th, weights w in theta)."""
    st, ct = np.sin(th), np.cos(th)
    mu = ct
    R = r[:, None]
    gx = -st / R**2
    gz = -ct / R**2 + ye
    y = np.hypot(gx, gz)
    # V = (nu-1) g_N + (1-nu_e) g_N; the (1-nu_e)(-x/r^3) part is divergence-free
    # off the origin and pure l=0, so it is dropped (it is huge near the Sun and would
    # only inject round-off). What is kept decays at both ends.
    f = nu.minus_1(y)
    k = (1.0 - nue) * ye
    Vr = f * (gx * st + gz * ct) + k * ct
    Vt = f * (gx * ct - gz * st) - k * st
    Pl = eval_legendre(l, mu)
    dPl = _legendre_deriv(l, mu)
    wt = w * st  # d mu = sin(theta) d theta
    A = (2 * l + 1) / 2.0 * (Vr * Pl) @ wt
    B = (2 * l + 1) / 2.0 * (Vt * st * dPl) @ wt
    return A, B


def solve_mode(nu, eta, l=2, n_r=4000, n_th=800, r_min=1e-3, r_max=1e3):
    """Return (s grid, u_l on it, y_e). u_l is the l-th Legendre coefficient of Phi_a."""
    ye = y_external(nu, eta)
    nue = float(nu(ye))
    s = np.linspace(np.log(r_min), np.log(r_max), n_r)
    h = s[1] - s[0]
    # Gauss-Legendre in theta on [0, pi]
    x, wx = np.polynomial.legendre.leggauss(n_th)
    th = 0.5 * np.pi * (x + 1.0)
    w = 0.5 * np.pi * wx
    # fluxes at half nodes (chunked to bound memory)
    sh = np.concatenate([[s[0] - h / 2], 0.5 * (s[1:] + s[:-1]), [s[-1] + h / 2]])
    Ah = np.empty_like(sh)
    for i in range(0, len(sh), 512):
        Ah[i:i + 512], _ = _AB(nu, nue, ye, np.exp(sh[i:i + 512]), th, w, l)
    Bn = np.empty_like(s)
    for i in range(0, len(s), 512):
        _, Bn[i:i + 512] = _AB(nu, nue, ye, np.exp(s[i:i + 512]), th, w, l)
    Fh = np.exp(2 * sh) * Ah
    rhs = -np.exp(-s) * (Fh[1:] - Fh[:-1]) / h - np.exp(s) * Bn
    L = l * (l + 1)
    lo = 1 / h**2 - 1 / (2 * h)
    di = -2 / h**2 - L
    up = 1 / h**2 + 1 / (2 * h)
    ab = np.zeros((3, n_r))
    ab[0, 1:] = up
    ab[1, :] = di
    ab[2, :-1] = lo
    # ghost points: u_{-1} = u_1 - 2h*l*u_0 ; u_{N} = u_{N-2} - 2h*(l+1)*u_{N-1}
    ab[1, 0] = di - lo * 2 * h * l
    ab[0, 1] = up + lo
    ab[1, -1] = di - up * 2 * h * (l + 1)
    ab[2, -2] = lo + up
    u = solve_banded((1, 1), ab, rhs)
    return s, u, ye


R_EXTRACT = 1e-2


def c2_of(nu, eta, r_ex=R_EXTRACT, **kw):
    """c2 = u_2/r^2 read at r_ex (default 0.01 r_M, ~70 au), where the l=2 source is
    already negligible. Reading at r_min instead adds the O(h^2) error of the discrete
    r^2 growth once per decade of grid between r_ex and r_min."""
    s, u, ye = solve_mode(nu, eta, l=2, **kw)
    se = np.log(r_ex)
    i = int(np.searchsorted(s, se))
    if not (0 < i < len(s)):
        raise ValueError("r_ex outside the grid")
    ue = np.interp(se, s, u * np.exp(-2 * s))
    return float(ue), ye


def Q2(nu, a0, ge, **kw):
    """Return (Q2 [s^-2], Milgrom q, y_e)."""
    c2, ye = c2_of(nu, ge / a0, **kw)
    rM = np.sqrt(GM / a0)
    return -3.0 * c2 * a0 / rM, 2.0 * c2, ye


def Q2_richardson(nu, a0, ge, n_r=2000, n_th=400, **kw):
    """Two resolutions (h, h/2 jointly in r and theta); second-order Richardson.
    Returns (Q2_extrap, Q2_fine, |fine - extrap| as the error estimate)."""
    q1 = Q2(nu, a0, ge, n_r=n_r, n_th=n_th, **kw)[0]
    q2 = Q2(nu, a0, ge, n_r=2 * n_r - 1, n_th=2 * n_th, **kw)[0]
    qx = q2 + (q2 - q1) / 3.0
    return qx, q2, abs(q2 - qx)
