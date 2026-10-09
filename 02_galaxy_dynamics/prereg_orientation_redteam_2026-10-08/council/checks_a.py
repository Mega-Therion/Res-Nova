import numpy as np
# A. K_e (prereg) = L0 (AQUAL, d ln mu/d ln x at true g_ext) ; K0 (QUMOND, d ln nu/d ln y at Newtonian g_N,ext)
mu_std=lambda x: x/np.sqrt(1+x*x)
mu_sim=lambda x: x/(1+x)
def dlog(f,x,h=1e-6): return (np.log(f(x*(1+h)))-np.log(f(x*(1-h))))/(np.log(1+h)-np.log(1-h))
print("A. prereg check: 1/(1+1.8^2) =",1/(1+1.8**2))
for name,mu in (("std",mu_std),("simple",mu_sim)):
  for a0 in (1.042e-10,1.2e-10):
    for ge in (1.9e-10,2.2e-10):
      x=ge/a0; L0=dlog(mu,x); mue=mu(x); y=x*mue
      nu=lambda yy,mu=mu: 1/mu(np.array([__import__('scipy.optimize',fromlist=['brentq']).brentq(lambda xx: xx*mu(xx)-v,1e-9,1e3) for v in np.atleast_1d(yy)]))
      K0=dlog(lambda yy: nu(yy)[0],y)
      print(f"  mu_{name:6s} a0={a0:.3e} ge={ge:.2e} x_e={x:.3f} mu_e={mue:.4f} L0(=prereg K_e)={L0:.4f} K0(BZ QUMOND)={K0:.4f} (1+L0)(1+K0)={(1+L0)*(1+K0):.4f} "
            f"perp/along force: QUMOND {1+K0/2:.4f} AQUAL {1/np.sqrt(1+L0):.4f}")
# B. the pipeline's E boost (copied formula from wide_binary_fish.boost 'E', Q=1), fixed external-field direction
A0,GE=1.042e-10,1.9e-10
nu_std=lambda y: np.sqrt((1+np.sqrt(1+4/y**2))/2)
def bE(gN,u):
    gNv=np.array([gN,0,0]); gev=GE*np.array(u); gt=gNv+gev
    gint=nu_std(np.linalg.norm(gt)/A0)*gt-nu_std(GE/A0)*gev
    return gint[0]/gN
for f in (0.01,0.1,0.5,1.5):
    gN=f*GE
    al=0.5*(bE(gN,[1,0,0])+bE(gN,[-1,0,0])); pe=bE(gN,[0,1,0])
    print(f"B. pipeline-E  gN/ge={f:4.2f}: radial boost aligned={al:.4f} perp={pe:.4f} aligned-perp={al-pe:+.4f}  (BZ field-equation sign: aligned > perp)")
y=GE/A0; K0c=dlog(nu_std,y); print(f"   pipeline treats GE as Newtonian: nu_e={nu_std(y):.4f}, K0={K0c:.4f}; algebraic predicts aligned/perp = 1+K0 = {1+K0c:.4f}; BZ Eq.37 predicts perp/aligned = 1+K0/2 = {1+K0c/2:.4f}")
