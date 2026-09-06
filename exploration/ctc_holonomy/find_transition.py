import numpy as np, sympy as sp
t,r,phi,z,a = sp.symbols('t r phi z a', real=True, positive=True)
coords=[t,r,phi,z]; s=sp.sinh(r)
g = sp.Matrix([
 [-4*a**2, 0, 4*sp.sqrt(2)*a**2*s**2, 0],
 [0, 4*a**2, 0, 0],
 [4*sp.sqrt(2)*a**2*s**2, 0, -4*a**2*(s**4-s**2), 0],
 [0, 0, 0, 4*a**2]])
gi=g.inv()
M=sp.zeros(4,4)
for l in range(4):
    for m in range(4):
        e=0
        for k in range(4):
            e+=gi[l,k]*(sp.diff(g[k,m],coords[2])+sp.diff(g[k,coords[2]] if False else g[k,2],coords[m])-sp.diff(g[m,2],coords[k]))
        M[l,m]=sp.simplify(e/2)
def maxreal(rv):
    Mn=np.array(sp.matrix2numpy(M.subs({r:rv,a:1}),dtype=float))
    return np.max(np.abs(np.linalg.eigvals(Mn).real))
lo,hi=0.40,0.70
for _ in range(60):
    mid=(lo+hi)/2
    if maxreal(mid)>1e-7: hi=mid
    else: lo=mid
print("elliptic -> hyperbolic transition  r* =", round(hi,10))
for nm,v in [("sinh(r*)",sp.sinh(hi)),("tanh(r*)",sp.tanh(hi)),("cosh(r*)",sp.cosh(hi)),("sinh^2(r*)",sp.sinh(hi)**2)]:
    print(f"   {nm} = {float(v):.10f}")
print()
print("CTC threshold arcsinh(1) =", round(float(sp.asinh(1)),10), "(sinh=1, tanh=0.70710678)")
print("candidates:  ln(1+sqrt2)/2 =", round(float(sp.log(1+sp.sqrt(2))/2),10),
      "  arcsinh(1/sqrt2) =", round(float(sp.asinh(1/sp.sqrt(2))),10),
      "  arcsinh(0.5) =", round(float(sp.asinh(0.5)),10))
