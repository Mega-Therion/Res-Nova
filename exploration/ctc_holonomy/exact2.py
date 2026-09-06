import sympy as sp
t,r,phi,z,a = sp.symbols('t r phi z a', real=True, positive=True)
coords=[t,r,phi,z]; s=sp.sinh(r)
g = sp.Matrix([[-4*a**2,0,4*sp.sqrt(2)*a**2*s**2,0],[0,4*a**2,0,0],
 [4*sp.sqrt(2)*a**2*s**2,0,-4*a**2*(s**4-s**2),0],[0,0,0,4*a**2]])
gi=g.inv(); M=sp.zeros(4,4)
for l in range(4):
    for m in range(4):
        e=0
        for k in range(4):
            e+=gi[l,k]*(sp.diff(g[k,m],coords[2])+sp.diff(g[k,2],coords[m])-sp.diff(g[m,2],coords[k]))
        M[l,m]=sp.simplify(e/2)
print("full M:"); sp.pprint(M)
lam=sp.Symbol('lam')
cp=sp.factor(sp.simplify(sp.det(M-lam*sp.eye(4))))
print("\ncharacteristic poly:", cp)
# reduce with u = sinh^2 r
u=sp.Symbol('u',positive=True)
cpu=sp.simplify(cp.rewrite(sp.exp))
print("\nnonzero eigenvalues solve:")
sols=sp.solve(sp.Eq(cp,0),lam)
for x in sols:
    xs=sp.simplify(x)
    if xs!=0: print("  lam =",sp.simplify(sp.trigsimp(xs)))
