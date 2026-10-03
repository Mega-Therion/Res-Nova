#!/usr/bin/env python3
"""THE AeST CLUSTER PREDICTION -- solving the quasi-static system, not the MOND limit.
2026-09-24.

SZ diagonalise NT_quasi_Phi with Phi = Phi_E + varphi. The kinetic sector separates
EXACTLY (verified symbolically), leaving

    lap(Phi_E)        + mu^2 Phi = 4 pi G rho_bary
    div(J' grad phi)  + mu^2 Phi = 4 pi G rho_bary        Phi = Phi_E + phi

Subtracting gives lap(Phi_E) = div(J' grad phi), i.e. u_E = J'(v^2) v in spherical
symmetry. With SZ's MOND form J = 2 ls/(3(1+ls) a0) Y^{3/2}, J' = ls |v|/((1+ls) a0),
so u_E = v^2/a0_eff with a0_eff = a0 (1+ls)/ls  ->  a0 as ls -> inf.

mu = 0 reproduces the MOND law g = sqrt(g_N a0_eff) exactly (checked).

STATE:  W = r^2 u_E ,  Phi
    dW/dr   = r^2 [ 4 pi G rho_bary(r) - mu^2 Phi ]
    dPhi/dr = W/r^2 + sqrt( (W/r^2) a0_eff )          ( = u_E + v )
BC: W(r_min)->0 ,  Phi(r_max) = 0.

THE WEAK POINT, stated up front: the mu^2 Phi term couples to the ABSOLUTE potential, so
the answer depends on where Phi is zeroed. That is physical (ghost-condensate character),
not a gauge choice, but it means r_max matters. Sensitivity is reported.
"""
import math, json, numpy as np
from scipy.integrate import solve_bvp
import importlib.util
spec=importlib.util.spec_from_file_location("cm","cluster_mond_test.py")
cm=importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)

MPC, G, MS, A0 = cm.MPC_M, cm.G_SI, cm.MSUN, cm.A0
LAMBDA_S = float('inf')                       # SZ's MOND models use lambda_s = infinity
A0_EFF   = A0 if LAMBDA_S == float('inf') else A0*(1+LAMBDA_S)/LAMBDA_S

# mu from K_2 fixed by SZ's own w_0 relation (see D10 sec7)
H0_invMpc = cm.H0_KMS/cm.C_KMS
K2  = 3*H0_invMpc**2*cm.OM_M/(4*0.1**2*1.23e-8)
MU  = math.sqrt(2*K2/(2-0.1))*0.1 / MPC       # m^-1
BETA, RC_FRAC = 2.0/3.0, 0.1                  # beta-model gas profile

def mass_shape(r, rc):                        # enclosed mass of a beta model, unnormalised
    return np.where(r>0, (r/rc) - np.arctan(r/rc), 0.0) if BETA==2.0/3.0 else None

def solve_cluster(M500_kg, z, fbar, mu=MU, rmax_fac=3.0, n=800):
    r500 = cm.r_delta(M500_kg, z)
    rc   = RC_FRAC*r500
    Mbar_tot = fbar*M500_kg
    norm = Mbar_tot/ (r500/rc - math.atan(r500/rc))
    def Menc(r): return norm*((r/rc) - np.arctan(r/rc))
    rmin, rmax = 1e-3*r500, rmax_fac*r500
    def rhs(r, Y):
        W, Phi = Y
        uE = np.maximum(W, 0.0)/r**2
        # dW/dr = r^2 * 4 pi G rho  - r^2 mu^2 Phi ; and INT r^2 4 pi G rho = G Menc
        dMdr = norm*( (1.0/rc) - (1.0/rc)/(1+(r/rc)**2) )
        return np.vstack([ G*dMdr - r**2*mu**2*Phi,
                           uE + np.sqrt(uE*A0_EFF) ])
    def bc(Ya, Yb): return np.array([Ya[0], Yb[1]])
    r = np.linspace(rmin, rmax, n)
    W0 = G*Menc(r); Phi0 = -G*Mbar_tot/np.maximum(r,rmin)*0.0
    sol = solve_bvp(rhs, bc, r, np.vstack([W0, Phi0]), tol=1e-6, max_nodes=200000)
    if not sol.success: return None
    W, Phi = sol.sol(r500)
    uE = max(W,0.0)/r500**2
    g  = uE + math.sqrt(uE*A0_EFF)
    return dict(r500=r500, g=g, Mdyn=g*r500**2/G, Phi500=Phi, uE=uE)

if __name__ == "__main__":
    print(f"mu^-1 = {1/(MU*MPC):.4f} Mpc   a0_eff = {A0_EFF:.4e} m/s^2 (lambda_s -> inf)")
    print(f"beta-model gas profile: beta={BETA:.3f}, r_c = {RC_FRAC} r_500\n")
    for rmax_fac in (2.0, 3.0, 5.0):
        Rs=[]; Rm=[]
        print(f"--- Phi(r_max)=0 at r_max = {rmax_fac} r_500 ---")
        print(f"{'cluster':<18}{'M500':>8}{'M_MOND':>9}{'M_AeST':>9}{'R_MOND':>9}{'R_AeST':>9}")
        for k,c in cm.load().items():
            M500 = c['M500']*1e14*MS; fbar = c['fgas']+0.015
            s  = solve_cluster(M500, c['z'], fbar, rmax_fac=rmax_fac)
            s0 = solve_cluster(M500, c['z'], fbar, mu=0.0, rmax_fac=rmax_fac)
            if s is None or s0 is None:
                print(f"{c['name']:<18}{'BVP FAILED':>44}"); continue
            R  = M500/s['Mdyn']; R0 = M500/s0['Mdyn']
            Rs.append(R); Rm.append(R0)
            print(f"{c['name']:<18}{c['M500']:>8.2f}{s0['Mdyn']/(1e14*MS):>9.2f}"
                  f"{s['Mdyn']/(1e14*MS):>9.2f}{R0:>9.2f}{R:>9.2f}")
        if Rs:
            Rs.sort(); Rm.sort(); n=len(Rs)
            md=lambda a: a[n//2] if n%2 else .5*(a[n//2-1]+a[n//2])
            print(f"{'':<18}{'':>8}{'':>9}{'':>9}{'median':>9}{'':>9}")
            print(f"{'  MEDIAN':<18}{'':>8}{'':>9}{'':>9}{md(Rm):>9.2f}{md(Rs):>9.2f}\n")
