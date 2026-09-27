import sympy as sp
src=open('aest_ppn_pipeline.py').read().split("ph = sp.exp(")[0]
exec(src)
def test(Lm, label):
    tr = {UZ: UZ + sp.diff(Lm, z), P: P - Q0 * Lm}
    bad = 0
    for eq in eqs:
        dlt = sp.simplify(sp.expand(eq.lhs.subs(tr).doit() - eq.lhs))
        if dlt != 0:
            bad += 1
            if bad <= 2: print("   change:", sp.factor(dlt))
    print(f"{label}: field equations changed in {bad} of {len(eqs)}")
test(sp.Function('Lam')(z), "static shift  du_z += dLam/dz, phi -= Q0*Lam")
test(sp.Function('Lam2')(t, z), "time-dependent shift")
