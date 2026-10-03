#!/usr/bin/env python3
"""Size and SIGN of the mu^2 correction to cluster masses in AeST. 2026-09-24.

The full BVP lap(Phi) + mu^2 Phi = source with Phi(r_max)=0 is ILL-POSED here: the
operator is Helmholtz (positive mu^2), so it has resonances wherever mu*r_max ~ n*pi.
With mu^-1 = 0.99 Mpc and r_500 ~ 1.4 Mpc, the first resonance sits at ~3.1 Mpc, i.e.
INSIDE the range one would want to integrate over. Direct solve_bvp fails on 8-12 of 12
clusters, and where it "converges" it returns M_dyn up to 50x M_500. That is the
resonance, not a prediction. Recorded rather than tuned away.

So we do the well-posed thing: FIRST ORDER IN mu^2 about the MOND solution.

  W(r) = r^2 u_E = G M_bar(r) - mu^2 INT_0^r r'^2 Phi(r') dr'

Phi < 0 in a potential well, so the correction is POSITIVE -- the mu^2 term ADDS
effective mass. Evaluating the integral on the unperturbed MOND solution gives the
leading correction, with a controlled expansion parameter.

INTERPOLATION NOTE. The AeST quasi-static structure gives g = u_E + v with
u_E = v^2/a0_eff, i.e.  g = g_N + sqrt(g_N a0_eff).  This is NOT mu_std = x/sqrt(1+x^2),
which D10 sec2 used. Both are reported so the difference is visible.
"""
import math, numpy as np, importlib.util
spec=importlib.util.spec_from_file_location("cm","cluster_mond_test.py")
cm=importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
MPC,G,MS,A0 = cm.MPC_M, cm.G_SI, cm.MSUN, cm.A0

H0i = cm.H0_KMS/cm.C_KMS
K2  = 3*H0i**2*cm.OM_M/(4*0.1**2*1.23e-8)
MU  = math.sqrt(2*K2/(2-0.1))*0.1/MPC          # m^-1 ; mu^-1 = 0.9895 Mpc
A0E = A0                                        # lambda_s -> inf (SZ's MOND models)
RCF, N = 0.1, 4000

def run(rmax_fac=1.0):
    out=[]
    for k,c in cm.load().items():
        M500=c['M500']*1e14*MS; fbar=c['fgas']+0.015
        r500=cm.r_delta(M500,c['z']); rc=RCF*r500
        norm=fbar*M500/((r500/rc)-math.atan(r500/rc))
        r=np.linspace(1e-4*r500, rmax_fac*r500, N)
        Menc=norm*((r/rc)-np.arctan(r/rc))
        uE=G*Menc/r**2
        g =uE+np.sqrt(uE*A0E)                                  # AeST force law
        # unperturbed potential, zeroed at the outer edge
        Phi=-np.flip(np.cumsum(np.flip(g)*np.gradient(r)[0]))
        corr=-MU**2*np.cumsum(r**2*Phi)*np.gradient(r)[0]      # -mu^2 INT r'^2 Phi dr'
        W0=G*Menc; W=W0+corr
        i=-1
        uE1=max(W[i],0)/r[i]**2
        g1 =uE1+math.sqrt(uE1*A0E)
        # mu_std comparison at the same baryon mass (what D10 sec2 used)
        gN=G*Menc[i]/r[i]**2; s=gN/A0
        g_mustd=A0*math.sqrt((s*s+s*math.sqrt(s*s+4))/2)
        out.append(dict(name=c['name'], M500=c['M500'],
            R_mustd=M500/(g_mustd*r[i]**2/G),
            R_aest_mond=M500/(g*r[i]**2/G)[i],
            R_aest_mu2 =M500/(g1*r[i]**2/G),
            boost=W[i]/W0[i], murmax=MU*r[i]))
    return out

print(f"mu^-1 = {1/(MU*MPC):.4f} Mpc   a0_eff = {A0E:.4e} (lambda_s -> inf)")
print(f"\n{'cluster':<18}{'R(mu_std)':>11}{'R(AeST,MOND)':>14}{'R(AeST,+mu^2)':>15}{'W/W0':>8}{'mu*r500':>9}")
res=run(1.0)
for d in sorted(res,key=lambda x:-x['M500']):
    print(f"{d['name']:<18}{d['R_mustd']:>11.2f}{d['R_aest_mond']:>14.2f}"
          f"{d['R_aest_mu2']:>15.2f}{d['boost']:>8.2f}{d['murmax']:>9.2f}")
md=lambda a:(lambda s:(s[len(s)//2] if len(s)%2 else .5*(s[len(s)//2-1]+s[len(s)//2])))(sorted(a))
print(f"{'-'*75}")
print(f"{'MEDIAN':<18}{md([d['R_mustd'] for d in res]):>11.2f}"
      f"{md([d['R_aest_mond'] for d in res]):>14.2f}"
      f"{md([d['R_aest_mu2'] for d in res]):>15.2f}"
      f"{md([d['boost'] for d in res]):>8.2f}")
print(f"\nR=1 means baryons suffice.  mu*r500 ~ {md([d['murmax'] for d in res]):.2f} rad")
print("Expansion parameter W/W0 - 1 is the fractional mu^2 correction; first order is")
print("only trustworthy while it is well below 1.")
