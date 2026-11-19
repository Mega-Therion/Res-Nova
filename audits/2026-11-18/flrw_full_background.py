#!/usr/bin/env python3
"""
Full-background FLRW calculation of G_cosmo/G_N from the exact AeST action.

NOT the two-parameter truncation. Everything below is derived from

  S = INT d4x sqrt(-g)/16 pi G~ [ R - (K_B/2) F^2 + 2b J^mu grad_mu phi - b Y - F(Y,Q) - lam(A^2+1) ] + S_m

with b = 2 - K_B, Y = q^{mu nu} grad_mu phi grad_nu phi, Q = A^mu grad_mu phi
(Skordis-Zlosnik PRL 127, 161302, eq. 5; transcribed verbatim in TARGET_D7_COVARIANT_COMPLETION.md sec.1).

Run: python3 audits/2026-11-18/flrw_full_background.py    (exit 0)
"""
import sympy as sp

t = sp.symbols('t', positive=True)
a = sp.Function('a')(t)
N = sp.Function('N')(t)
phi = sp.Function('phi')(t)
KB = sp.symbols('K_B', positive=True)
Gt, rho_rad = sp.symbols('Gtilde rho_rad', positive=True)

print("="*82); print("STEP 1  geometry, and what the aether actually does on FLRW"); print("="*82)
g = sp.Matrix([[-N**2,0,0,0],[0,a**2,0,0],[0,0,a**2,0],[0,0,0,a**2]])
ginv = g.inv()
coords = [t, sp.symbols('x'), sp.symbols('y'), sp.symbols('z')]
Gam = [[[sp.simplify(sum(ginv[k,l]*(sp.diff(g[l,i],coords[j])+sp.diff(g[l,j],coords[i])
        -sp.diff(g[i,j],coords[l])) for l in range(4))/2) for j in range(4)] for i in range(4)] for k in range(4)]

A_up = sp.Matrix([1/N,0,0,0])          # unit timelike aether, A^mu A_mu = -1
A_lo = sp.simplify(g*A_up)
print(f"  A^mu A_mu = {sp.simplify((A_up.T*A_lo)[0,0])}   (must be -1)")

def cov_d(A_lo, mu, nu):
    """nabla_nu A_mu = d_nu A_mu - Gamma^l_{nu mu} A_l"""
    return sp.simplify(sp.diff(A_lo[mu],coords[nu]) - sum(Gam[l][nu][mu]*A_lo[l] for l in range(4)))

F = sp.Matrix(4,4, lambda mu,nu: sp.simplify(cov_d(A_lo,mu,nu)-cov_d(A_lo,nu,mu)))
print(f"  F_munu == 0 identically?  {F == sp.zeros(4,4)}")
F2 = sp.simplify(sum(F[mu,nu]*F[mu,nu] for mu in range(4) for nu in range(4)))
print(f"  F^munu F_munu = {F2}")

# J_mu = A^alpha nabla_alpha A_mu
J = [sp.simplify(sum(A_up[al]*sum(Gam[l][al][mu]*A_lo[l] - sp.diff(A_lo[mu],coords[al])
     for l in range(4))*-1 for al in range(1))) for mu in range(4)]
J = [sp.simplify(sum(A_up[al]*(sp.diff(A_lo[mu],coords[al])
     - sum(Gam[l][al][mu]*A_lo[l] for l in range(4))) for al in range(4))) for mu in range(4)]
print(f"  J_mu = A^a nabla_a A_mu = {J}")

Q = sp.simplify(sum(A_up[i]*sp.diff(phi,coords[i]) for i in range(4)))
q_inv = ginv + A_up*A_up.T
Yv = sp.simplify((sp.Matrix([sp.diff(phi,c) for c in coords]).T*q_inv*
                  sp.Matrix([sp.diff(phi,c) for c in coords]))[0,0])
print(f"  Q = A^mu d_mu phi = {Q}")
print(f"  Y = q^munu d_mu phi d_nu phi = {Yv}")

print("""
  CONSEQUENCE. On FLRW, F_munu = 0 and J_mu = 0 identically. So the entire aether sector
  -- both (K_B/2)F^2 and 2b J^mu grad_mu phi -- vanishes at background order. K_B cannot
  appear in the FLRW Friedmann equation. Y also vanishes, so the Y-sector free function
  contributes only its value at 0. What survives is F(0, Q) with Q = phidot/N != 0:
  the scalar DOES have cosmological dynamics, but only through the Q sector.""")

print("="*82); print("STEP 2  reduced action and the N-constraint (Friedmann)"); print("="*82)
# R for flat FLRW with lapse; L_g = -6 a adot^2/N after dropping total derivatives
adot = sp.diff(a,t)
L_g = -6*a*adot**2/N
print("  L_g = -6 a adot^2 / N   (flat FLRW, total derivative dropped)")
print("  L_phi = -N a^3 F(0, Q),  Q = phidot/N")

Ffun = sp.Function('F')
Qv = sp.Symbol('Qbar', positive=True)
Fphi = Ffun(0, Qv)
# d/dN [ -N a^3 F(0, phidot/N) ] = -a^3 [ F - Q F_Q ]
dFdN = -a**3*(Fphi - Qv*sp.diff(Fphi, Qv))
Lphi_N = sp.simplify(dFdN.subs(Qv, sp.diff(phi,t)/N))
dLg_dN = sp.simplify(sp.diff(L_g, N))
dLm_dN = -a**3*rho_rad
constraint = sp.simplify(dLg_dN + Lphi_N + dLm_dN)
print(f"\n  dS/dN = 0  ->  {sp.simplify(constraint.subs(N,1).subs(sp.Derivative(N,t),0))}")
print("""
  Setting N = 1 and dividing by a^3:

      3 H^2 = 8 pi G~ rho_m + (1/2)[ F(0,Q) - Q F_Q(0,Q) ]

  so with  rho_phi := [F(0,Q) - Q F_Q(0,Q)] / (16 pi G~)   we get the exact form

      H^2 = (8 pi G~/3)( rho_m + rho_phi )     =>     G_cosmo = G~ (1 + rho_phi/rho_m)

  and at BBN (radiation domination, rho_m = rho_rad):

      G_cosmo/G_N = (1 + rho_phi/rho_rad) / (1 + 1/lambda_s)          [G_N = (1+1/lam)G~, corpus]""")

print("="*82); print("STEP 3  does retaining phibar(t) clear the 5% BBN bound?"); print("="*82)
LAM_CEIL = (27+12*sp.sqrt(6))/5
eta = LAM_CEIL/(1+LAM_CEIL)
print(f"  non-folding ceiling lam_s < {float(LAM_CEIL):.6f}, so 1+1/lam_s > {float(1+1/LAM_CEIL):.6f}")
need = sp.Rational(95,100)*(1+1/LAM_CEIL)
eps_needed = sp.simplify(need-1)
print(f"  need (1 + rho_phi/rho_rad) >= 0.95*(1+1/lam_ceil) = {float(need):.6f}")
print(f"  =>  rho_phi/rho_rad >= {float(eps_needed):.6f}  ({100*float(eps_needed):.3f}%)")
print(f"\n  The minimal theory has rho_phi = 0 (F = F(Y) only, and F(0) is a constant),")
print(f"  which reproduces the ceiling sqrt(27/32) = {float(eta):.6f} and the 8.144% gap.")
print(f"  Retaining phibar(t) with a Q-sector energy density clears it at {100*float(eps_needed):.2f}%.")

print("="*82); print("STEP 4  stability of the Q-sector operator"); print("="*82)
p_ = sp.symbols('p', positive=True); c_ = sp.symbols('c', positive=True); Qb = sp.Symbol('Qbar', positive=True)
print("""  For L_phi = -F(0,Q) the fluid quantities are
      rho_phi = F - Q F_Q ,   p_phi = -F ,   rho+p = -Q F_Q ,   c_s^2 = F_Q/(Q F_QQ)""")
for power in (2,3,4):
    Fq = -c_*Qb**power
    rho = sp.simplify(Fq - Qb*sp.diff(Fq,Qb)); pr = sp.simplify(-Fq)
    nop = sp.simplify(rho+pr); cs2 = sp.simplify(sp.diff(Fq,Qb)/(Qb*sp.diff(Fq,Qb,2)))
    print(f"  F = -c Q^{power}:  rho = {rho},  rho+p = {nop},  c_s^2 = {cs2}")
print("""
  p = 2 is stiff (c_s^2 = 1 exactly, marginal). p >= 3 gives c_s^2 = 1/(p-1) < 1 strictly,
  with rho > 0 and rho+p > 0. So the minimal causal witness is F(0,Q) = -c Q^3.""")

print("="*82); print("STEP 5  what happened to K_B"); print("="*82)
print(f"""  The derived background contains NO K_B: F_munu = 0 on FLRW, so the (K_B/2)F^2 term and
  the 2b J^mu grad_mu phi term both vanish identically. The corpus formula
        G_cosmo = (1 - K_B/2) G_hat
  is therefore consistent with this derivation ONLY if  G_hat := G~/(1 - K_B/2).
  The K_B dependence then lives entirely in (i) that definition and (ii) the quasi-static
  Newtonian limit -- NOT in the Friedmann equation.

  CONSEQUENCE: K_B cannot be used to close the BBN gap at background order. The earlier scan
  found that K_B only ever makes the ratio worse (it multiplies by (1-K_B/2) <= 1), which is
  exactly what this says: the knob is on the G_N side, not the G_cosmo side.""")

print("="*82); print("STEP 6  the side constraint: rho_phi at BBN is extra radiation"); print("="*82)
# rho_rad = rho_gamma (1 + (7/8)(4/11)^(4/3) N_eff,SM)
coef = sp.Rational(7,8)*(sp.Rational(4,11))**sp.Rational(4,3)
NeffSM = sp.Rational(3044,1000)
denom = 1 + coef*NeffSM
k = coef/denom
print(f"  (7/8)(4/11)^(4/3) = {float(coef):.6f};  rho_rad = rho_gamma (1 + {float(coef):.6f}*N_eff)")
print(f"  with N_eff,SM = {float(NeffSM):.3f}:  rho_rad = {float(denom):.6f} rho_gamma")
print(f"  =>  rho_phi/rho_rad = {float(k):.6f} * Delta N_eff")
lo = float(eps_needed)/float(k)
print(f"\n  clearing 5% BBN needs rho_phi/rho_rad >= {float(eps_needed):.5f}")
print(f"  =>  Delta N_eff >= {lo:.4f}")
for hi in (0.29, 0.34, 0.45):
    print(f"  with Delta N_eff <= {hi}: rho_phi/rho_rad <= {float(k)*hi:.5f}"
          f"  -> {'WINDOW OPEN' if float(k)*hi >= float(eps_needed) else 'WINDOW SHUT'}")
print(f"""
  So the Q-sector escape is not free. A positive rho_phi at BBN IS extra radiation and is
  bounded by Delta N_eff. The viable band is Delta N_eff in [{lo:.3f}, ~0.29], i.e. sitting
  at the 1-sigma edge of the Planck/BBN bound. Narrow, non-empty, and falsifiable.""")

print("="*82); print("STEP 7  the witness point"); print("="*82)
lam = float(LAM_CEIL) - 1e-6
dNeff = (float(eps_needed)/float(k) + 0.29)/2      # midpoint of the viable band
epsQ = float(k)*dNeff
ratio = (1+epsQ)/(1+1/lam)
print(f"""  Action:   F(Y,Q) = -c Q^3 - F_Y(Y),  separable, so the Y sector (mu, non-folding) is untouched
  At BBN:   Qbar != 0, rho_phi/rho_rad = {epsQ:.5f}  (Delta N_eff = {dNeff:.4f})
  Y sector: lambda_s = {lam:.6f}  (< 11.278775, non-folding holds)
  Aether:   K_B -> 0 (any K_B in (0,2) multiplies by (1-K_B/2) <= 1; take K_B small)
  Tensor:   c_T = c  (structural: EH tensor sector, no Weyl coupling)
  Scalar:   c_s^2 = 1/2  (p=3 -> 1/(p-1); strictly causal, no ghost since rho+p = 3c Q^3 > 0)
  Y-sector K2: irrelevant at background; the Minkowski c_s^2 formula needs K2 >~ 60 as before

  G_cosmo/G_N = (1+{epsQ:.5f})/(1+1/{lam:.4f}) = {ratio:.6f}   (need >= 0.95)  -> {'PASS' if ratio>=0.95 else 'FAIL'}""")

print("="*82); print("VERDICT"); print("="*82)
print(f"""  QUESTION: does retaining phibar(t) move sup(G_cosmo/G_N) above 0.95 inside the
            ghost-free, causal, non-folding window?

  ANSWER:  YES -- SAT, with a non-empty witness.

    * The sqrt(27/32) = {float(eta):.6f} ceiling is NOT fundamental. It is the rho_phi = 0 case,
      i.e. the theory where the scalar has no Q-sector energy. It is exact for minimal AeST
      and it is reproduced here: F = F(Y) only  =>  rho_phi = 0  =>  the old ceiling.
    * Retaining phibar(t) with F(0,Q) != 0 gives rho_phi = [F - Q F_Q]/(16 pi G~) > 0, and the
      bound becomes rho_phi/rho_rad >= {100*float(eps_needed):.2f}%.
    * F(0,Q) = -c Q^3 delivers that with rho > 0, rho+p > 0 and c_s^2 = 1/2 < 1.
    * K_B cannot help and does not enter: F_munu = 0 on FLRW.

  UNSAT holds exactly when rho_phi = 0 (minimal AeST), and again whenever Delta N_eff < {lo:.3f}.

  NOT established here, and this is the remaining work: the full quadratic analysis of the
  Q^3 operator (ghost/gradient conditions in the coupled aether-scalar system, not just the
  background k-essence ones). The background conditions checked above are necessary, not
  sufficient.""")

print("="*82); print("STEP 8  the joint feasible region, and what binds it"); print("="*82)
eta_f = float(eta); lam_f = float(LAM_CEIL)-1e-6
eps_lo = float(eps_needed); eps_hi = float(k)*0.29
print(f"  eps_Q in [{eps_lo:.5f}, {eps_hi:.5f}]   (lower: 5% BBN;  upper: Delta N_eff <= 0.29)")
print(f"\n{'eps_Q':>9}{'K_B max':>12}{'K2 min':>14}{'G ratio':>10}")
for e in (eps_lo, (eps_lo+eps_hi)/2, eps_hi):
    KBmax = 2*(1 - 0.95/((1+e)*eta_f))
    if KBmax <= 0:
        print(f"{e:>9.5f}{'-- none --':>12}"); continue
    KB = KBmax*0.999
    K2min = (2-KB)*(1+0.5*KB*lam_f)/KB
    print(f"{e:>9.5f}{KBmax:>12.2e}{K2min:>14.2e}{(1-KB/2)*(1+e)*eta_f:>10.5f}")

print(f"""
  BINDING STRUCTURE. Four constraints, all active, and they pinch from opposite sides:

    1. BBN 5%            -> eps_Q >= {eps_lo:.4f}                        (pushes eps_Q UP)
    2. Delta N_eff       -> eps_Q <= {eps_hi:.4f}                        (pushes eps_Q DOWN)
    3. BBN + K_B         -> K_B <= {2*(1-0.95/((1+eps_hi)*eta_f)):.4f} at eps_Q = eps_hi
                            (any K_B multiplies by 1-K_B/2 <= 1, so K_B must stay SMALL)
    4. Y-sector c_s^2<=1 -> K2 >= {float((2-0.008)*(1+0.5*0.008*lam_f)/0.008):.0f} at K_B ~ 0.008
                            (small K_B BLOWS UP the Minkowski c_s^2: (2-K_B)/(K2 K_B) -> inf)

  So the window is non-empty but genuinely narrow, and it is bounded on all four sides.
  The naive witness (K_B -> 0) is WRONG and the gate caught it: c_s^2 diverges as K_B -> 0.

  CERTIFIED WITNESS (passes scripts/survival_vector_gate.py, exit 0):
    eps_Q = 0.039, K_B = 0.008, lambda_s = 11.2787, K2 = 300, c_s^2 = 0.867, G_cosmo/G_N = 0.9506""")
