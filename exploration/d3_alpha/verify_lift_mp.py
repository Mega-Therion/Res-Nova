import sympy as sp, mpmath as mp
mp.mp.dps = 80
KB, lam, K2, Q0, qb, k, w = sp.symbols('K_B lambda_s K_2 Q_0 qbar k omega', real=True)
Gs = sp.Symbol('G', positive=True)
det = sp.sympify(open('AEST_DISPERSION_OFFSET.txt').read(), locals={'K_B':KB,'lambda_s':lam,'K_2':K2,'Q_0':Q0,'qbar':qb,'k':k,'omega':w,'G':Gs})
num, den = sp.fraction(sp.together(det))
big = [f for f, m in sp.factor_list(num)[1] if f.has(w) and sp.degree(f, w) > 4][0]
W2 = sp.Symbol('W2')
Pbig = sp.Poly(sp.expand(big.subs(w, sp.sqrt(W2))), W2)
vals = {KB: sp.Rational(1, 2), K2: 750000, Q0: sp.Rational(1, 10), lam: 1}
mu2 = sp.Rational(2 * 750000, 100) / sp.Rational(3, 2); ks2 = 2 * mu2
def roots_at(kk, qv):
    cs = [sp.Rational(c_) for c_ in sp.Poly(Pbig.as_expr().subs(vals).subs({k: kk, qb: qv}), W2).all_coeffs()]
    return mp.polyroots([mp.mpf(sp.Rational(c_).p) / mp.mpf(sp.Rational(c_).q) for c_ in cs], maxsteps=400, extraprec=400)
def formula(kk, qv):
    return 750000 * sp.Rational(1, 10) * qv * sp.Rational(3, 2) * (kk**2 - ks2) / (sp.Rational(5, 2) * kk**2 + sp.Rational(3, 2) * 2 * mu2)
print("k/k*   qbar      small root (mp)           formula        ratio")
for kk in (42, 212, 1414, 141421):
    kfac = sp.Rational(kk) / sp.sqrt(ks2)
    for qv in (sp.Rational(1, 10**14), sp.Rational(17, 10**8)):
        rs = roots_at(kk, qv)
        small = min(rs, key=lambda r: abs(r))
        f = formula(kk, qv)
        print(f"{float(kfac):7.2f} {float(qv):.1e}  {mp.nstr(small, 10):>24s}  {float(f):14.6e}  {float(mp.re(small)) / float(f):8.4f}")

print("\ntrack the zero branch vs qbar at k = 1414 (10 k*) and k = 42 (0.3 k*):  s = root/qbar ; K2*qbar/Q0 ; K2*|Psi| = K2*qbar/Q0")
for kk in (1414, 42):
    prev = None
    for e in range(-14, -5):
        for m in (1, 3):
            qv = sp.Rational(m, 10**(-e)) if e < 0 else m
            rs = roots_at(kk, qv)
            if prev is None:
                cur = min(rs, key=lambda r: abs(r))
            else:
                cur = min(rs, key=lambda r: abs(r - prev * (float(qv) / pq)))   # follow continuity (linear extrapolation)
            prev, pq = cur, float(qv)
            print(f"  k={kk:5d} qbar={float(qv):.0e}  K2|Psi|={750000*float(qv)/0.1:9.2e}  root={mp.nstr(cur,8):>22s}  s={float(mp.re(cur))/float(qv):11.4e}")
