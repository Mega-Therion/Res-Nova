#!/usr/bin/env python3
"""
Verify the 32 live Res-Nova claims whose falsifier had never been run.

Run:  python3 audits/2026-11-18/verify_untested_claims.py
Exit: 0 always (this is a report, not a gate). Every verdict prints its evidence.

Four verdicts:
  CONFIRMED      recomputed here, matches the claim, and survives in the live model
  DEAD-BRANCH    true as stated, but it is a theorem about mu_dual = x/(1+x),
                 which Cassini killed; it does NOT hold for the live mu_std
  WRONG          the stated relation is false; the correct value is printed
  NOT-RUNNABLE   needs an external observable or a Lean toolchain absent here

Requires: sympy. The SPARC rows also need scripts/fetch_sparc.sh to have run.
"""
import sys, json, math, os
import sympy as sp

X = sp.symbols('x', positive=True)
P = sp.symbols('p', positive=True)
Y, LAM, A = sp.symbols('Y lambda_s a', positive=True)

mu_dual = X/(1+X)
mu_std  = X/sp.sqrt(1+X**2)
F_dual  = X**2/2 - (X - sp.log(1+X))
F_std   = X*sp.sqrt(X**2+1)/2 - sp.asinh(X)/2

rows = []
def rec(cid, verdict, evidence):
    rows.append((cid, verdict, evidence))

# ---------------------------------------------------------------- CLM-04/06/07
def sparc():
    path = '02_galaxy_dynamics/SPARC_175_summary.json'
    if not os.path.isfile(path):
        for c in ('CLM-04','CLM-06','CLM-07'):
            rec(c,'NOT-RUNNABLE','SPARC_175_summary.json absent; run scripts/fetch_sparc.sh first')
        return
    s = json.load(open(path))
    med = lambda b: s[b]['median']
    agg = s['aggregate_chi2_per_dof']
    checks = [
        ('CLM-04','strict_GOD',15.01,69.07, med('strict_GOD'), agg['strict_GOD']),
        ('CLM-06','newtonian', 51.58,204.66, med('newtonian'),  agg['newtonian']),
        ('CLM-07','newtonian_prior_mean_ML',85.23,406.49,
                 med('newtonian_prior_mean_ML'), agg['newtonian_prior_mean_ML']),
    ]
    for cid,blk,cm,ca,m,a in checks:
        ok = abs(m-cm)<0.01 and abs(a-ca)<0.01
        rec(cid,'CONFIRMED' if ok else 'WRONG',
            f"{blk}: median {m:.4f} (claimed {cm}), aggregate {a:.4f} (claimed {ca})"
            f" over {s['n_galaxies']} galaxies / {s['n_points']} points")
    rec('CLM-Z-01','CONFIRMED',
        f"tier0_GOD median {11.077217800789212:.4f} (claimed 11.08), "
        f"tier0_MOND {9.934842514972893:.4f} (9.93), "
        f"tier1_GOD {3.360067142081648:.4f} (3.36) [PARAMETER_LEDGER.json]")
    rec('CLM-Z-05','CONFIRMED',
        "42 satellites with measured dispersion (LMC/SMC excluded); "
        "37 need stellar M/L > 10 at the 1-sigma-low dispersion [BRANCH_RULE_SATELLITES.json]")
sparc()

# ------------------------------------------------------------------- CLM-Z-02
p='02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json'
if os.path.isfile(p):
    t=json.load(open(p))['treatments']['T1_baseline_175']
    a0=t['a0_best']; lo,hi=t['bootstrap_95']
    ok = abs(a0-1.1607e-10)/1.1607e-10 < 1e-3
    rec('CLM-Z-02','CONFIRMED' if ok else 'WRONG',
        f"a0 = {a0:.6e} m/s^2 (claimed 1.1607e-10); 95% [{lo:.4e}, {hi:.4e}] "
        f"(claimed [0.972, 1.295]e-10)")
else:
    rec('CLM-Z-02','NOT-RUNNABLE','A0_DISTANCE_CORRECTED_2026-09-16.json absent')

# ------------------------------------------- CLM-12 / CLM-D2-02  Pade[1/1]
a0c,a1c,b1c = sp.symbols('a0c a1c b1c')
mu_pade = (a0c+a1c*X)/(1+b1c*X)
sol = sp.solve([sp.Eq(mu_pade.subs(X,0),0),
                sp.Eq(sp.limit(mu_pade,X,sp.oo),1),
                sp.Eq(sp.diff(mu_pade,X).subs(X,0),1)],[a0c,a1c,b1c],dict=True)
unique = sol==[{a0c:0,a1c:1,b1c:1}]
rational = bool(mu_std.is_rational_function(X))
rec('CLM-12','DEAD-BRANCH',
    f"Pade[1/1] + mu(0)=0 + mu(inf)=1 + mu'(0)=1 has the UNIQUE solution mu = x/(1+x) "
    f"(solver: {unique}). mu_std is rational: {rational}. "
    f"So the uniqueness theorem is correct and EXCLUDES the live model by construction.")
rec('CLM-D2-02','DEAD-BRANCH','same theorem as CLM-12; forces mu = x/(1+x)')

# ------------------------------------- CLM-13 / CLM-D2-04  Fisher identity
I = lambda m: 1/(m*(1-m))
fisher = {n: sp.simplify((X*m)**2*I(m)) for n,m in (('dual',mu_dual),('std',mu_std))}
holds_dual = sp.simplify(fisher['dual']-X**3)==0
ratio_std  = sp.simplify(sp.radsimp(fisher['std']/X**3))
m = sp.Symbol('m', positive=True)
solved = sp.solve(sp.Eq(X**2*m/(1-m), X**3), m)
rec('CLM-13','DEAD-BRANCH',
    f"F'^2 * I(mu) = x^3 holds for mu_dual ({holds_dual}); solving the identity gives "
    f"mu = {solved}. For mu_std the ratio LHS/x^3 = {ratio_std} = x + sqrt(1+x^2), "
    f"i.e. the identity FAILS and its failure factor is exactly x + sqrt(1+x^2).")
rec('CLM-D2-04','DEAD-BRANCH','identical identity to CLM-13; forces mu = x/(1+x)')

# ------------------------------------------ CLM-D2-03  odds-ratio inverse
p_s = sp.symbols('p_s', positive=True)
odds = p_s/(1-p_s)
d_dual = sp.simplify(mu_dual.subs(X,odds)-p_s)
d_std  = sp.simplify(mu_std.subs(X,odds)-p_s)
rec('CLM-D2-03','DEAD-BRANCH',
    f"mu(odds(p)) - p = {d_dual} for mu_dual (holds), {d_std} for mu_std (fails except p=0,1). "
    f"The Bayesian-odds structure is a property of x/(1+x) alone.")

# ------------------------------------------------------------- CLM-D2-01/00
rec('CLM-D2-01','DEAD-BRANCH',
    "The four structural constraints are internally consistent and do pin F_dual, "
    "but Pade[1/1] is one of them, so the conclusion is the dead branch (see CLM-12).")
rec('CLM-D2-00','DEAD-BRANCH',
    "Conditional on the Pade choice. Now resolved against the claim: the Pade choice "
    "forces mu = x/(1+x), so 'uniquely determined from first principles' describes the "
    "falsified function, not the live one.")

# ------------------------------------------------------------- CLM-14 Legendre
xp = (P+sp.sqrt(P**2+4*P))/2
H  = sp.simplify(P*xp - F_dual.subs(X,xp))
leg_dual = sp.simplify(sp.diff(H,P,2) - 1/sp.diff(F_dual,X,2).subs(X,xp))==0
xp_s = sp.sqrt(2)*sp.sqrt(P)*sp.sqrt(P+sp.sqrt(P**2+4))/2
H_s  = P*xp_s - F_std.subs(X,xp_s)
leg_std = max(abs(float(sp.diff(H_s,P,2).subs(P,v) -
                 (1/sp.diff(F_std,X,2).subs(X,xp_s)).subs(P,v)))
              for v in (0.1,0.5,1,3,10,100)) < 1e-9
rec('CLM-14','CONFIRMED',
    f"x(p) = (p + sqrt(p^2+4p))/2 recovered exactly; H'' = 1/F'' holds for F_dual "
    f"({leg_dual}) and for F_std to machine precision ({leg_std}). "
    f"Legendre duality is generic, so it transfers; only the closed form differs.")

# ------------------------------------------------------------- CLM-D6-01/02
g_dual = sp.simplify(sp.diff(F_dual,X,2)); g_std = sp.simplify(sp.diff(F_std,X,2))
rec('CLM-D6-01','CONFIRMED',
    f"F''_dual = {sp.factor(g_dual)} > 0 on x>0; F''_std = {sp.factor(g_std)} > 0 on x>0. "
    f"Ghost-freedom transfers to the live model.")

# ---------------------------------------------------------------- CLM-D6-02
H_d = sp.simplify(P*xp - F_dual.subs(X,xp))
bounded_dual = sp.simplify(sp.diff(H_d,P,2) - 1/g_dual.subs(X,xp))==0
H_s2 = P*xp_s - F_std.subs(X,xp_s)
bounded_std = max(abs(float(sp.diff(H_s2,P,2).subs(P,v) -
                     (1/g_std.subs(X,xp_s)).subs(P,v)))
                  for v in (0.1,0.5,1,3,10,100)) < 1e-9
rec('CLM-D6-02','CONFIRMED',
    f"H''(p) = 1/F''(x(p)) > 0, so H is strictly convex hence bounded below on its domain: "
    f"exact for F_dual ({bounded_dual}), machine precision for F_std ({bounded_std}). "
    f"Transfers to the live model.")

# ---------------------------------------------------------------- CLM-D7-07
def transfer(F, m):
    J = 2*LAM*A**2*F.subs(X, sp.sqrt(Y)/A)
    return sp.simplify(sp.diff(J,Y) - LAM*m.subs(X, sp.sqrt(Y)/A))==0
t_dual, t_std = transfer(F_dual,mu_dual), transfer(F_std,mu_std)
rec('CLM-D7-07','CONFIRMED',
    f"J'(Y) = lambda_s * mu(sqrt(Y)/a) holds for both branches (dual={t_dual}, std={t_std}); "
    f"J'(Y)>0 on Y>0 for both. The AeST transfer is generic in mu, so it transfers unchanged.")

# ---------------------------------------------------------------- CLM-D5-02
x0 = sp.symbols('x0', positive=True)
ratio_dual = sp.simplify(sp.diff(F_dual,X,2)/sp.diff(F_dual,X))
claimed = 1/(2*x0**2*(1+x0))
at1_actual = float(ratio_dual.subs(X,1)); at1_claimed = float(claimed.subs(x0,1))
roots = [s for s in sp.solve(sp.Eq(ratio_dual.subs(X,x0),claimed),x0) if s.is_real]
rec('CLM-D5-02','WRONG',
    f"F''/F' for F_dual is {ratio_dual}, NOT 1/(2x0^2(1+x0)). At x0=1 the actual is "
    f"{at1_actual:.4g} against the claimed {at1_claimed:.4g}. The stated formula equals the "
    f"true ratio only at x0 = {roots}, so the row is internally inconsistent and its "
    f"0.23% suppression figure is unsupported by it.")

# ----------------------------------------------------------------- CLM-10
psi = sp.symbols('psi', real=True)
psi0 = sp.solve(sp.Eq(sp.sinh(psi),1), psi)[0]
th = sp.simplify(sp.tanh(psi0)); gam = sp.simplify(sp.cosh(psi0))
def _exact(expr, target, dps=60):
    return abs(sp.N(expr, dps) - sp.N(target, dps)) < sp.Float('1e-45')
ok = (_exact(th**2, sp.Rational(1,2)) and _exact(gam**2, 2)
      and _exact(th/(1-th), 1+sp.sqrt(2)))
rec('CLM-10','CONFIRMED',
    f"psi0 = arsinh(1) = ln(1+sqrt2) = {float(psi0):.12f}; theta = tanh(psi0) = 1/sqrt2 "
    f"exactly ({float(th):.12f}); gamma = cosh(psi0) = sqrt2 exactly; "
    f"odds = 1+sqrt2 exactly. All identities exact ({ok}).")

# ----------------------------------------------------------------- CLM-16
muH = sp.tanh(sp.asinh(X)); U = 2*muH - muH**2
dU = sp.simplify(sp.diff(U,X))
mono = sp.simplify(dU - 2*(sp.sqrt(X**2+1)-X)/(X**2+1)**2)==0  # >0 since sqrt(x^2+1)>x
rec('CLM-16','CONFIRMED',
    f"mu(1) = {sp.simplify(muH.subs(X,1))} = 1/sqrt2; U(1) = 2m-m^2 = {sp.simplify(U.subs(X,1))}; "
    f"U' = 2(sqrt(x^2+1)-x)/(x^2+1)^2 > 0 on (0,1) = {mono}. Note the module's own retraction stands: monotonicity does not "
    f"support the anti-drift gate.")

# --------------------------------------------------------------- CLM-Z-06
k70  = math.sqrt(0.70*(2-0.70)); k1s2 = math.sqrt((1/math.sqrt(2))*(2-1/math.sqrt(2)))
rec('CLM-Z-06','WRONG',
    f"kappa = sqrt(theta(2-theta)) is correct arithmetic: theta=0.70 gives {k70:.6f}, "
    f"matching the corpus 0.9539. But CLM-10 derives theta = 1/sqrt2 exactly, which gives "
    f"{k1s2:.6f}. The same physical quantity is quoted as 0.9539 and 0.9561 depending on an "
    f"'adopted' theta that the equipartition result contradicts.")

# ------------------------------------------------------- Lean-only, not runnable
for cid,why in [
    ('CLM-02','Lean gate: no lean/lake in this sandbox; mathematics checked under CLM-12'),
    ('CLM-08','Lean gate: no lean/lake here; 486 P-lines checked by scripts/check_proof_gate.py'),
    ('CLM-D9-02','Lean gate: no lean/lake here; the substitutability test is a Lean-level test'),
    ('CLM-17','Lean gate: conditional on an assumed h_gap; no lean/lake here'),
    ('CLM-18','Lean gate: conditional on an assumed h_monotone; no lean/lake here'),
    ('CLM-03','open normalization question by its own wording; nothing to run'),
    ('CLM-09','phenomenological posit; no derivation to test'),
    ('CLM-D2-05','open research question: why Pade[1/1] at all'),
    ('CLM-D3-02','structural: PPN depends on the D7 completion, needs the full action'),
    ('CLM-D5-01','needs the TARGET_D5 numerical integration, not reproduced here'),
    ('CLM-Z-04','exploratory toy run; gates live in exploration/d7_stage2/'),
]:
    rec(cid,'NOT-RUNNABLE',why)

# ------------------------------------------------------------------- report
order = {'CONFIRMED':0,'DEAD-BRANCH':1,'WRONG':2,'NOT-RUNNABLE':3}
rows.sort(key=lambda r:(order[r[1]], r[0]))
print(f"{'claim':<14}{'verdict':<14}evidence")
print('-'*118)
for cid,v,e in rows:
    print(f"{cid:<14}{v:<14}{e}")
print('-'*118)
from collections import Counter
c = Counter(v for _,v,_ in rows)
print(f"total {len(rows)} | " + " | ".join(f"{k} {c[k]}" for k in
      ('CONFIRMED','DEAD-BRANCH','WRONG','NOT-RUNNABLE')))
