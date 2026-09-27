import sympy as sp
src=open('aest_ppn_pipeline.py').read().split("sol = sp.solve(alg")[0]
exec(src)
# homogeneous system: drop source R, build coefficient matrix
unk=list(amp.values())
M=sp.Matrix([[sp.diff(a.subs(R,0),u) for u in unk] for a in alg])
det=sp.factor(sp.simplify(M.det(method='berkowitz')))
print("det =", det)
