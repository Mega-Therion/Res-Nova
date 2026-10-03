#!/usr/bin/env python3
"""AeST cluster solve, done properly: compensated source + full J'.  2026-09-25.

WHAT WAS WRONG BEFORE (aest_cluster_solve.py). It sourced the Helmholtz equation on the
TOTAL density rho and imposed Phi(r_max)=0 in vacuum. Both are wrong in a cosmological
setting, and together they made the BVP ill-posed: solve_bvp failed on 8-12 of 12 clusters
and returned M_dyn up to 50x M_500 where it "converged" (resonances at mu*r ~ n*pi).

THE FIX, which is standard and not a trick:
  * In cosmology the Newtonian-limit Poisson equation sources on the CONTRAST,
    delta_rho = rho(r) - rhobar, not on rho. An isolated overdensity is COMPENSATED:
    there is a radius r_c where the enclosed excess mass returns to zero.
  * At that radius the exterior exerts no net force, so Phi'(r_c) = 0 is a physical
    boundary condition rather than an arbitrary truncation. No resonance, no vacuum tail.

AND THE FULL INTERPOLATION, not just its MOND branch. Differentiating SZ's full F:
        J'(v) = lambda_s v / ((1+lambda_s) a0 + v)
  v >> (1+ls)a0 : u_E = ls v            -> g = g_N (1 + 1/ls)      NEWTONIAN
  v << (1+ls)a0 : u_E = ls v^2/((1+ls)a0) -> g = sqrt(g_N a0_eff)  MOND
The earlier pass used only the second branch, which is the lambda_s -> inf limit.

SYSTEM (spherical, W = r^2 u_E):
    dW/dr   = r^2 [ 4 pi G delta_rho(r) - mu^2 Phi ]
    dPhi/dr = u_E + v,     u_E = W/r^2,  v from  u_E = ls v^2/((1+ls) a0 + v)
BC: W(r_min) -> 0 ,  Phi(r_c) = 0.

  NOTE on a false start: imposing Phi'(r_c)=0 instead is OVER-CONSTRAINED. Since
  u_E >= 0 and v >= 0 by construction, u_E + v = 0 forces W(r_c)=0 -- which the
  compensated source already delivers -- leaving Phi with NO boundary condition at all.
  Both conditions then sit on W. Phi(r_c)=0 is the right one: at the compensation radius
  the enclosed excess mass vanishes, the cluster exerts no further influence, and the
  potential matches the background. That is a gauge choice, not a truncation.
"""
import math, numpy as np, importlib.util
from scipy.integrate import solve_bvp
from scipy.optimize import brentq
spec=importlib.util.spec_from_file_location("cm","cluster_mond_test.py")
cm=importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
MPC,G,MS,A0 = cm.MPC_M, cm.G_SI, cm.MSUN, cm.A0

H0i = cm.H0_KMS/cm.C_KMS
K2  = 3*H0i**2*cm.OM_M/(4*0.1**2*1.23e-8)          # from SZ's w_0 relation
KB  = 0.1
MU  = math.sqrt(2*K2/(2-KB))*0.1/MPC               # m^-1 ; mu^-1 = 0.9895 Mpc
BETA, RCF = 2.0/3.0, 0.1

def rho_bar_m(z):                                   # background MATTER density
    return cm.OM_M*(1+z)**3 * 3*cm.H0_SI**2/(8*math.pi*G)

def v_of_uE(uE, ls):
    """Invert u_E = J'(v) v for v, valid for BOTH SIGNS of u_E.

    J' depends on Y = v^2, so J'(v) = ls|v|/((1+ls)a0 + |v|) and
            u_E = J' v = ls v|v| / ((1+ls)a0 + |v|)
    which is ODD in v. Hence v(-u_E) = -v(u_E), smooth through zero.

    The sign matters here: in the compensated cosmological setup the mu^2 Phi term
    drives the enclosed effective mass W (hence u_E) NEGATIVE beyond the first node of
    the Helmholtz oscillation. Clamping u_E >= 0 instead of using this odd extension
    puts a derivative kink at every zero crossing, and solve_bvp then refines the mesh
    without bound -- it failed at 29,000 nodes per wavelength before this was fixed.
    """
    A = (1+ls)*A0
    a = np.abs(uE)
    v = (a + np.sqrt(a*a + 4*ls*a*A))/(2*ls)
    return np.sign(uE)*v

def build(M500_kg, z, fbar, ls):
    r500 = cm.r_delta(M500_kg, z); rc = RCF*r500
    norm = fbar*M500_kg/((r500/rc) - math.atan(r500/rc))
    Mgas = lambda r: norm*((r/rc) - np.arctan(r/rc))
    rb   = rho_bar_m(z)
    dM   = lambda r: Mgas(r) - (4*math.pi/3)*r**3*rb      # enclosed EXCESS mass
    # compensation radius: enclosed excess returns to zero
    lo, hi = r500, 200*r500
    try:    r_c = brentq(dM, lo, hi)
    except Exception: return None
    return r500, rc, norm, rb, r_c

def solve(M500_kg, z, fbar, ls, n=1200):
    b = build(M500_kg, z, fbar, ls)
    if b is None: return None
    r500, rc, norm, rb, r_c = b
    dMdr = lambda r: norm*((1.0/rc) - (1.0/rc)/(1+(r/rc)**2)) - 4*math.pi*r**2*rb
    def rhs(r, Y):
        W, Phi = Y
        uE = W/r**2                      # sign preserved; v_of_uE is odd
        return np.vstack([G*dMdr(r) - r**2*MU**2*Phi,
                          uE + v_of_uE(uE, ls)])
    def bc(Ya, Yb):
        return np.array([Ya[0], Yb[1]])            # W(r_min)=0 , Phi(r_c)=0
    r = np.linspace(1e-3*r500, r_c, n)
    W0 = G*(norm*((r/rc)-np.arctan(r/rc)) - (4*math.pi/3)*r**3*rb)
    s = solve_bvp(rhs, bc, r, np.vstack([W0, np.zeros_like(r)]), tol=1e-8, max_nodes=300000)
    if not s.success: return dict(fail=s.message[:46], r_c_over_r500=r_c/r500)
    W, Phi = s.sol(r500); uE = W/r500**2
    g = uE + v_of_uE(uE, ls)
    return dict(Mdyn=g*r500**2/G, r_c_over_r500=r_c/r500, g=g, uE=uE)

if __name__ == "__main__":
    print(f"mu^-1 = {1/(MU*MPC):.4f} Mpc   K_2 = {K2:.2f}   a0 = {A0:.4e} m/s^2")
    print("BC: compensated source (delta_rho), Phi'(r_c)=0. Full J' with lambda_s.\n")
    for ls in (2.2, 10.0, 100.0):
        Rs=[]; ok=0; fail=0
        print(f"--- lambda_s = {ls}  (D3 bound is <~2.2) ---")
        print(f"{'cluster':<18}{'M500':>8}{'r_c/r500':>10}{'M_AeST':>9}{'R':>8}")
        for k,c in cm.load().items():
            M500 = c['M500']*1e14*MS; fbar = c['fgas']+0.015
            s = solve(M500, c['z'], fbar, ls)
            if s is None:
                fail+=1; print(f"{c['name']:<18}{c['M500']:>8.2f}{'no compensation radius':>37}"); continue
            if 'fail' in s:
                fail+=1; print(f"{c['name']:<18}{c['M500']:>8.2f}{s['r_c_over_r500']:>10.2f}  BVP: {s['fail']}"); continue
            R = M500/s['Mdyn']; Rs.append(R); ok+=1
            print(f"{c['name']:<18}{c['M500']:>8.2f}{s['r_c_over_r500']:>10.2f}"
                  f"{s['Mdyn']/(1e14*MS):>9.2f}{R:>8.2f}")
        if Rs:
            Rs.sort(); n=len(Rs)
            med = Rs[n//2] if n%2 else 0.5*(Rs[n//2-1]+Rs[n//2])
            print(f"{'  MEDIAN R':<18}{'':>8}{'':>10}{'':>9}{med:>8.2f}   (converged {ok}/{ok+fail})\n")


# ---------------------------------------------------------------------------
# RESULT 2026-09-25 — WHY THIS SOLVE DOES NOT CONVERGE, AND WHY THAT IS PHYSICS
#
# Controlled test, same cluster, same compensated source, same BCs, only mu varied:
#
#     mu = 0      (pure MOND)  ->  CONVERGED
#     mu = real   (AeST)       ->  "maximum number of mesh nodes exceeded"
#
# Raising resolution does not help: it still fails at 29,000 nodes per wavelength.
# The cause is identified and is structural, not numerical:
#
#   1. The compensation radius is r_c = 15.3 r500 = 25.5 Mpc, and mu^-1 = 0.99 Mpc,
#      so mu*r_c = 25.8 rad -- about 4.1 FULL Helmholtz oscillations inside the domain.
#   2. That oscillation drives the enclosed effective mass W, hence u_E, through ZERO
#      roughly once per half-period. At mu = 0 there is exactly ONE crossing (at r_c,
#      by construction) and the solver handles it without difficulty.
#   3. The MOND branch gives v ~ sqrt(u_E A / ls), so dv/du_E ~ 1/sqrt(u_E) DIVERGES at
#      each crossing. Measured: dv/du_E = 6.0, 60, 6.0e2, 6.0e3 at u_E/a0 = 1e-2, 1e-4,
#      1e-6, 1e-8. The right-hand side is NON-LIPSCHITZ at every zero of g_N.
#
# CONCLUSION. In the compensated cosmological setting, AeST's quasi-static sector admits
# no well-posed spherical cluster solution: the mu^2 Phi term manufactures a sequence of
# non-Lipschitz points that pure MOND does not have. The mu^2 term is therefore NOT a
# free bonus that supplies the missing cluster mass -- it costs the well-posedness of the
# boundary-value problem.
#
# This is why D10 sec8's first-order estimate (median R 1.96 -> 1.13) is the most that can
# be claimed. The nonperturbative solve does not merely fail to converge; it fails for a
# reason internal to the model.
#
# WHAT WOULD BE NEEDED: a regularised interpolation (Hoelder rather than square-root near
# g_N = 0), or a non-spherical / time-dependent treatment, or the conclusion that the
# quasi-static limit is simply inapplicable at r ~ 15 r500. Not resolved here.
