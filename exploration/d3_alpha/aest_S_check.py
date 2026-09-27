import sympy as sp
exec(open('aest_ppn_pipeline.py').read().split("def S(f):")[0])
# S_z = d_z phi + Q0 (du_z + h_0z)  (the combination whose square is Y at quadratic order), k along z
Sz = sp.I * k * sol[amp[P]] + Q0 * (sol[amp[UZ]] + sol[amp[F['h0z']]])
Sx = Q0 * (sol[amp[UX]] + sol[amp[F['h0x']]])          # d_x phi = 0 for k along z
print("moving source: S_z =", sp.simplify(Sz), "  S_x =", sp.simplify(Sx))
# delta Q = Q0*h00/2 + dphi/dt
dQ = Q0 * sol[amp[F['h00']]] / 2 + (-sp.I * w) * sol[amp[P]]
print("moving source: delta Q =", sp.simplify(dQ))
# same with lambda_s -> 0 (no tracking stiffness): does the metric stay GR?
alg0 = [sp.simplify(a.subs(lam, 0)) for a in alg]
s0 = sp.solve(alg0, list(amp.values()), dict=True)[0]
print("lambda_s=0: h00 =", sp.factor(sp.simplify(s0[amp[F['h00']]])))
