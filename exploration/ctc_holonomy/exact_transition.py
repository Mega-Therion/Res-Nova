import sympy as sp
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
            e+=gi[l,k]*(sp.diff(g[k,m],coords[2])+sp.diff(g[k,2],coords[m])-sp.diff(g[m,2],coords[k]))
        M[l,m]=sp.simplify(e/2)

# eigenvalues of the 2x2 (t,phi) block that carries the dynamics
sub = M[0:3:2, 0:3:2]          # rows/cols 0 and 2
print("active block M_(t,phi):"); sp.pprint(sp.simplify(sub))
lam = sp.symbols('lam')
cp  = sp.simplify(sp.det(sub - lam*sp.eye(2)))
print("\ncharacteristic polynomial:", sp.factor(sp.simplify(cp)))
disc = sp.simplify(sp.discriminant(sp.Poly(cp, lam)))
print("discriminant  D(r) =", sp.simplify(sp.factor(disc)))

# elliptic (rotation) when D<0 ; hyperbolic (boost) when D>0 ; transition at D=0
u = sp.symbols('u', positive=True)          # u = sinh^2 r
D_u = sp.simplify(disc.rewrite(sp.exp).subs(sp.sinh(r), sp.sqrt(u)))
D_u = sp.simplify(sp.expand(sp.simplify(disc.subs(sp.sinh(r), sp.sqrt(u)))))
print("\nD in terms of u = sinh^2(r):", sp.factor(sp.simplify(D_u)))
roots = sp.solve(sp.Eq(D_u,0), u)
print("roots u* =", [sp.nsimplify(sp.simplify(x)) for x in roots])
for x in roots:
    xv = complex(sp.N(x))
    if abs(xv.imag)<1e-12 and xv.real>0:
        print(f"  u* = {sp.simplify(x)} = {float(sp.re(x)):.10f}")
        print(f"     r* = arcsinh(sqrt(u*)) = {float(sp.asinh(sp.sqrt(sp.re(x)))):.10f}")
print("\n(sqrt(3)-1)/2 =", float((sp.sqrt(3)-1)/2))
