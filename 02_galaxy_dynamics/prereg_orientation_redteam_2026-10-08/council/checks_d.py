import numpy as np
from scipy.stats import norm
rng=np.random.default_rng(3)
N=2_000_000
def unit(n): u=rng.normal(size=(n,3)); return u/np.linalg.norm(u,axis=1)[:,None]
r=unit(N); g=unit(N); n=np.tile([0,0,1.0],(N,1))      # los = z, isotropic separation and field directions
cth2=np.sum(r*g,1)**2
rs=r.copy(); rs[:,2]=0; gs=g.copy(); gs[:,2]=0
sin2lam=1-g[:,2]**2
cpsi=np.abs(np.sum(rs*gs,1))/(np.linalg.norm(rs,axis=1)*np.linalg.norm(gs,axis=1))
cos2psi=2*cpsi**2-1; w=sin2lam*cos2psi
# check E[cos^2 th | obs] = 1/3 + sin^2(lam) cos(2psi)/3
X=np.vstack([np.ones(N),w]).T; b=np.linalg.lstsq(X,cth2,rcond=None)[0]; print("D. regress cos^2(theta) on w: intercept %.4f slope %.4f (predicted 1/3, 1/3)"%tuple(b))
sig=1.0   # per-binary noise >> signal; signal s = c*cos^2(theta) -> z proportional to the following
A=cpsi>np.sqrt(.5)
z_split=(cth2[A].mean()-cth2[~A].mean())/np.sqrt(1/A.sum()+1/(~A).sum())
B=w>0; z_wsplit=(cth2[B].mean()-cth2[~B].mean())/np.sqrt(1/B.sum()+1/(~B).sum())
z_reg=np.cov(w,cth2)[0,1]/np.std(w)*np.sqrt(N)
print("   Delta<cos^2 th> between |cos psi| halves = %.4f (8/(9pi)=%.4f); fraction of 3D signal range retained"%(cth2[A].mean()-cth2[~A].mean(),8/(9*np.pi)))
print("   relative z: median split |cos psi| 1.000 | split w>0 %.3f | regression on w %.3f"%(z_wsplit/z_split,z_reg/z_split))
print("   sky fraction with lambda<30deg (psi nearly uninformative): %.3f"%np.mean(sin2lam<np.sin(np.radians(30))**2))
# F. operating characteristics of the Gate 2 rule as written, Gaussian, E-S separation D sigma
for D in (2,3,4,5):
    favE_E=1-norm.cdf(3-D); favE_S=1-norm.cdf(3)
    # 'consistent with 0' taken as |Z|<2 ; '>=2 sigma below E' : Z <= D-2
    dis_S=norm.cdf(min(2,D-2))-norm.cdf(-2) if D-2>-2 else 0
    dis_E=max(0,norm.cdf(min(2,D-2)-D)-norm.cdf(-2-D))
    print(f"F. D={D}: P(favour E|E)={favE_E:.3f} P(favour E|S)={favE_S:.4f} P(disfavour E|S)={dis_S:.3f} P(disfavour E|E)={dis_E:.4f} P(inconclusive|E)={1-favE_E-dis_E:.3f} P(inconclusive|S)={1-favE_S-dis_S:.3f}")
# G. Newtonian Galactic tide / internal gravity, and external-field tilt from GC direction
kms_kpc=1e3/3.086e19; A_,B_=15.3,-11.9
Trad=4*A_*(A_-B_)*kms_kpc**2; G=6.674e-11; Ms=1.989e30; pc=3.086e16
Tz=4*np.pi*G*0.1*Ms/pc**3
for s in (10e3,20e3,30e3):
    rm=s*1.496e11; gN=G*1.2*Ms/rm**2
    print(f"G. s={s/1e3:.0f} kAU M=1.2: radial tide/gN={Trad*rm/gN:.1e}, vertical tide/gN={Tz*rm/gN:.1e}")
for z in (50,100,200):
    Kz=Tz*z*pc
    print(f"   |z|={z} pc: K_z~{Kz:.2e} m/s^2 (linear, upper) -> tilt of g_ext from GC direction {np.degrees(np.arctan(Kz/1.9e-10)):.1f} deg, P2 amplitude factor {(3*np.cos(np.arctan(Kz/1.9e-10))**2-1)/2:.3f}")
