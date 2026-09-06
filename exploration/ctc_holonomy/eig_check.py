import numpy as np, sympy as sp, scipy.linalg as la
t,r,phi,z,a = sp.symbols('t r phi z a', real=True, positive=True)
coords=[t,r,phi,z]; s=sp.sinh(r)
g=sp.Matrix([[-4*a**2,0,4*sp.sqrt(2)*a**2*s**2,0],[0,4*a**2,0,0],
 [4*sp.sqrt(2)*a**2*s**2,0,-4*a**2*(s**4-s**2),0],[0,0,0,4*a**2]])
gi=g.inv()
M=sp.zeros(4,4)
for l in range(4):
    for m in range(4):
        e=0
        for k in range(4):
            e+=gi[l,k]*(sp.diff(g[k,m],phi)+sp.diff(g[k,phi],coords[m])-sp.diff(g[m,phi],coords[k]))
        M[l,m]=sp.simplify(e/2)
for rv in [0.4, float(sp.asinh(1)), 1.5]:
    Mn=np.array(sp.matrix2numpy(M.subs({r:rv,a:1}),dtype=float))
    ev=np.linalg.eigvals(Mn)
    U=la.expm(-2*np.pi*Mn)
    print(f"r={rv:.4f} sinh={np.sinh(rv):.4f}")
    print("   generator eigenvalues:", np.round(ev,5))
    print("   real parts:", np.round(ev.real,5), "-> boost-like" if np.any(np.abs(ev.real)>1e-9) else "-> pure rotation")
    print("   det U =", round(float(np.linalg.det(U)),6))
