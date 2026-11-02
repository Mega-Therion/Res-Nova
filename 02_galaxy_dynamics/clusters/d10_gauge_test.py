"""Is the first-order expansion parameter gauge-dependent?
Same source, same mu, same r500 evaluation. Only the zero-point of Phi differs:
  A: Phi(r_max)=0  (repo's aest_mu2_correction.py)
  B: Phi(0)=0      (forward integration, as in an ODE solve)
W = W0 - mu^2 INT_0^r r'^2 Phi(r') dr'  depends on that choice because Phi enters the source.
"""
import math, numpy as np, importlib.util
spec=importlib.util.spec_from_file_location("cm","cluster_mond_test.py")
cm=importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
MPC,G,MS,A0 = cm.MPC_M, cm.G_SI, cm.MSUN, cm.A0
H0i = cm.H0_KMS/cm.C_KMS
K2  = 3*H0i**2*cm.OM_M/(4*0.1**2*1.23e-8)
MU  = math.sqrt(2*K2/(2-0.1))*0.1/MPC
RCF, N = 0.1, 4000

def run(gauge):
    boosts, r_mu2 = [], []
    for k,c in cm.load().items():
        M500=c['M500']*1e14*MS; fbar=c['fgas']+0.015
        r500=cm.r_delta(M500,c['z']); rc=RCF*r500
        norm=fbar*M500/((r500/rc)-math.atan(r500/rc))
        r=np.linspace(1e-4*r500, r500, N)
        Menc=norm*((r/rc)-np.arctan(r/rc))
        uE=G*Menc/r**2
        g=uE+np.sqrt(uE*A0)
        dr=np.gradient(r)[0]
        if gauge=='A':   Phi=-np.flip(np.cumsum(np.flip(g)*dr))
        else:            Phi=-np.cumsum(g*dr)
        corr=-MU**2*np.cumsum(r**2*Phi)*dr
        W0=G*Menc; W=W0+corr
        boosts.append(W[-1]/W0[-1])
        uE1=max(W[-1],0)/r[-1]**2
        g1=uE1+math.sqrt(uE1*A0)
        r_mu2.append(M500/(g1*r[-1]**2/G))
    md=lambda a:(lambda s:(s[len(s)//2] if len(s)%2 else .5*(s[len(s)//2-1]+s[len(s)//2])))(sorted(a))
    return md(boosts), md(r_mu2), boosts

for gname,label in [('A','Phi(r_max)=0  [repo]'),('B','Phi(0)=0      [ODE]')]:
    med_b, med_R, bl = run(gname)
    print(f"{label}:  median W/W0 = {med_b:.2f}  -> expansion param = {med_b-1:.2f}   median R(+mu^2) = {med_R:.2f}")
print("\nper-cluster W/W0 (A vs B):")
bA=run('A')[2]; bB=run('B')[2]
names=list(cm.load().keys())
for n,a,b in list(zip(names,bA,bB))[:6]:
    print(f"  {n:<20} A={a:.2f}  B={b:.2f}")
