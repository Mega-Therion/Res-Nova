import sympy as sp
KB, lam, K2, Q0, qb, k, w = sp.symbols('K_B lambda_s K_2 Q_0 qbar k omega', real=True)
Gs = sp.Symbol('G', positive=True)
det = sp.sympify(open('AEST_DISPERSION_OFFSET.txt').read(), locals={'K_B':KB,'lambda_s':lam,'K_2':K2,'Q_0':Q0,'qbar':qb,'k':k,'omega':w,'G':Gs})
num, den = sp.fraction(sp.together(det))
fac = sp.factor_list(num)
big = None
for f, m in fac[1]:
    deg = sp.degree(f, w) if f.has(w) else 0
    print(f"factor (mult {m}, deg_w {deg}):", str(f)[:160] + ("..." if len(str(f)) > 160 else ""))
    if deg > 4: big = f
W2 = sp.Symbol('W2')                      # omega^2
P = sp.expand(big.subs(w, sp.sqrt(W2)))
P = sp.Poly(sp.expand(P), W2)
print("big factor degree in omega^2:", P.degree())
# roots at qbar -> 0: the zero-mode branch should start at W2 = 0
P0 = sp.Poly(sp.expand(P.as_expr().subs(qb, 0)), W2)
print("qbar=0 limit of big factor:", sp.factor(P0.as_expr()))
# leading-order zero branch: W2 = s*qbar + O(qbar^2)
s = sp.Symbol('s')
lead = sp.expand(P.as_expr().subs(W2, s * qb))
# lowest power of qbar with nonzero coefficient
for n in range(0, 8):
    cn = sp.simplify(lead.coeff(qb, n))
    if cn != 0:
        print(f"lowest nonvanishing order qbar^{n}: coefficient =", sp.factor(cn))
        sol = sp.solve(sp.Eq(cn, 0), s)
        print("zero-branch omega^2 / qbar =", [sp.factor(x) for x in sol])
        break
frozen = 2 * K2 * Q0 * k**2 / (KB * k**2 + 2 * K2 * Q0**2)
print("frozen-metric prediction omega^2/qbar =", frozen)
for x in sol:
    print("ratio constrained/frozen =", sp.factor(sp.simplify(x / frozen)))
