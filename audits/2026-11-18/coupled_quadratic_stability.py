#!/usr/bin/env python3
"""
Coupled quadratic stability of the PR #226 witness, fenced claim by claim.

Sources (primary, fetched and read):
  [SZ21] Skordis & Zlosnik, PRL 127, 161302 (2021), arXiv:2007.00082
  [SZ22] Skordis & Zlosnik, PRD 106, 104041 (2022), arXiv:2109.13287

Run: python3 audits/2026-11-18/coupled_quadratic_stability.py   (exit 0)
"""
import sympy as sp

KB, lam, K2, Gt, Gh, GN, Gcos, c = sp.symbols('K_B lambda_s K_2 Gtilde Ghat G_N G_cosmo c', positive=True)

def hdr(t): print("\n" + "="*84 + f"\n{t}\n" + "="*84)

# ---------------------------------------------------------------- TASK 1
hdr("TASK 1  normalization: G~ / (1 - K_B/2) against SZ21 and SZ22")

# [SZ21] after eq.(NT_quasi_Phi): "identifying G~ = (1 - K_B/2) G^"
Gh_expr = Gt/(1 - KB/2)
print("  [SZ21] 'identifying  G~ = (1 - K_B/2) G^'   =>   G^ = G~/(1 - K_B/2)")
print(f"         G^ = {sp.simplify(Gh_expr)}")

# [SZ21] AQUAL paragraph: "G_N = (1 + 1/lambda_s) G^"
GN_from_SZ21 = sp.simplify((1 + 1/lam)*Gh_expr)
print("\n  [SZ21] 'G_N = (1 + 1/lambda_s) G^'   with G^ substituted:")
print(f"         G_N = {GN_from_SZ21}")

# [SZ22] eq. immediately after the tracking/screening discussion
GN_from_SZ22 = sp.simplify((1 + 1/lam)/(1 - KB/2)*Gt)
print("\n  [SZ22] verbatim:  G_N = (1 + 1/lambda_s)/(1 - K_B/2) * G~")
print(f"         G_N = {sp.simplify(GN_from_SZ22)}")
agree = sp.simplify(GN_from_SZ21 - GN_from_SZ22) == 0
print(f"\n  [P] the two papers agree exactly: {agree}")

# [SZ21] "so that the usual FLRW equations are satisfied" with G~
print("\n  [SZ21] FLRW: 'we define the energy density as 8 pi G~ rho = ... so that the")
print("         usual FLRW equations are satisfied'  =>  G_cosmo = G~")
Gcos_expr = Gt
ratio = sp.simplify(Gcos_expr/GN_from_SZ22)
print(f"\n  G_cosmo/G_N = G~ / [(1+1/lambda_s)/(1-K_B/2) G~] = {ratio}")
corpus = sp.simplify((1 - KB/2)/(1 + 1/lam))
print(f"  corpus formula (1 - K_B/2)/(1 + 1/lambda_s)      = {corpus}")
print(f"  [P] identical: {sp.simplify(ratio - corpus) == 0}")
print("""
  RESULT [P]. The corpus FORMULA is correct and the witness does NOT double-count
  (1 - K_B/2). But the corpus PROSE is wrong: it says "G_cosmo = (1 - K_B/2) G^".
  In SZ21 the factor sits on the OTHER side -- G~ = (1 - K_B/2) G^, equivalently
  G_N carries a 1/(1 - K_B/2). G_cosmo = G~ with no K_B. Same ratio, wrong attribution.""")

# ---------------------------------------------------------------- witness arithmetic
hdr("WITNESS  arithmetic, with the verified normalization")
KBv, lamv, K2v = 0.008, 11.2787, 300.0
epsQ = 0.039
ratio_v = (1 - KBv/2)*(1 + epsQ)/(1 + 1/lamv)
print(f"  (1 - K_B/2) = {1-KBv/2:.6f}   (1 + eps_Q) = {1+epsQ:.6f}   1/(1+1/lambda_s) = {1/(1+1/lamv):.6f}")
print(f"  G_cosmo/G_N = {ratio_v:.6f}   (need >= 0.95)  -> {'PASS' if ratio_v>=0.95 else 'FAIL'}")
print("  Matches PR #226's 0.950564. [P] no double-counting.")

# ---------------------------------------------------------------- TASK 2/3
hdr("TASK 2/3  what SZ actually publish, and what that means for the Q^3 term")
print("""  [SZ21] FLRW scalar sector: given as an EFFECTIVE FLUID (delta, theta) plus an
         explicit alpha-evolution equation, with the authors stating verbatim that
             "the resulting system is NOT equivalent to a dark fluid: the nonstandard
              pressure ... does not close under the fluid variables but, rather,
              depends on the vector field perturbations alpha and E_alpha."
         => SZ21 does NOT publish a 2x2 K_ij / G_ij on FLRW.

  [SZ22] IS an explicit quadratic analysis with a 4x4 coefficient matrix on
         Z = {Psi, Phi, alpha, phi}, of which 2 are constraints and 2 propagate.
         But it is on MINKOWSKI, not FLRW, and for F -> (2-K_B) J(Y) (no Q dependence).

  Its scalar sound speed, eq. (speed_of_sound):
         c_s^2 = (2 - K_B)/(K_2 K_B) * (1 + K_B lambda_s/2)""")
cs2_SZ22 = (2-KBv)*(1+0.5*KBv*lamv)/(K2v*KBv)
print(f"\n  evaluated at the witness: c_s^2 = {cs2_SZ22:.6f}")
print(f"  [SZ22] also require K_B > 0 (ghosts/gradient) and 0 < K_B < 2, lambda_s > -1 (tachyons)")
print(f"    K_B = {KBv} > 0            -> {'PASS' if KBv>0 else 'FAIL'}")
print(f"    0 < K_B < 2               -> {'PASS' if 0<KBv<2 else 'FAIL'}")
print(f"    lambda_s = {lamv} > -1     -> {'PASS' if lamv>-1 else 'FAIL'}")
print(f"    0 < c_s^2 <= 1            -> {'PASS' if 0<cs2_SZ22<=1 else 'FAIL'}")

print("""
  *** THE CRITICAL CAVEAT, and it invalidates a naive reading of PR #226 ***
  [SZ22] background is Minkowski with phi = Q_0 t + delta-phi, so Qbar = Q_0 != 0.
  Therefore a Q-dependent operator is NOT invisible at quadratic order: expanding
  F(0,Q) = -c Q^3 about Qbar gives
        F = -c[ Qbar^3 + 3 Qbar^2 dQ + 3 Qbar dQ^2 + dQ^3 ]
  and the dQ^2 term is NONZERO whenever Qbar != 0. It modifies the quadratic action,
  so eq. (speed_of_sound) above is the sound speed of the Y-ONLY theory, NOT of the
  modified one. c_s^2 = 0.867 is therefore NOT established for the PR #226 witness.""")

# exact: show the quadratic coefficient
Qb, dQ = sp.symbols('Qbar deltaQ', real=True)
Fq = -c*(Qb + dQ)**3
quad = sp.expand(Fq).coeff(dQ, 2)
print(f"\n  exact quadratic coefficient:  d^2F/dQ^2 = {sp.diff(Fq,dQ,2).subs(dQ,0)}")
print(f"  i.e. the Q^3 term adds  {sp.simplify(quad)} * dQ^2  to the quadratic action  [P]")

# ---------------------------------------------------------------- isolated Q sector
hdr("The Q sector in isolation (necessary, not sufficient)")
for p in (2,3,4):
    F = -c*Qb**p
    rho = sp.simplify(F - Qb*sp.diff(F,Qb)); pr = sp.simplify(-F)
    cs2 = sp.simplify(sp.diff(F,Qb)/(Qb*sp.diff(F,Qb,2)))
    w = sp.simplify(pr/rho)
    print(f"  F = -c Q^{p}:  rho={rho}  rho+p={sp.simplify(rho+pr)}  c_s^2={cs2}  w={w}")
print("""
  p = 3 (the PR #226 choice): rho > 0, rho+p > 0, c_s^2 = 1/2, w = 1/2.
  [P] the operator is ghost-free and causal IN ISOLATION.
  [D] but w = 1/2 means rho_phi ~ a^{-3(1+w)} = a^{-4.5}: it redshifts FASTER than
      radiation (a^-4). So rho_phi/rho_rad at BBN is an INITIAL CONDITION, not a
      prediction. PR #226's eps_Q = 0.039 is therefore a TUNING, and that is a second
      unestablished assumption beyond the coupled-2x2 gap.""")

# ---------------------------------------------------------------- verdict
hdr("VERDICT")
print(f"""  [P] Normalization verified against both SZ papers. G_cosmo = G~, G_N =
      (1+1/lambda_s)/(1-K_B/2) G~, ratio = (1-K_B/2)/(1+1/lambda_s) = {ratio_v:.6f}.
      No double-counting. The corpus PROSE attribution ("G_cosmo = (1-K_B/2)G^") is wrong.

  [P] SZ22's published stability conditions hold at the witness: K_B = 0.008 > 0,
      0 < K_B < 2, lambda_s > -1, and the Y-only c_s^2 = {cs2_SZ22:.4f} in (0,1].

  [P] Tensor: c_T = 1 structural (EH tensor sector, no Weyl coupling) -- unchanged.

  [D] The Q^3 term is NOT invisible at quadratic order (Qbar = Q_0 != 0), so the Y-only
      c_s^2 does not carry over to the modified theory.

  [D] The Q sector in isolation is healthy: rho>0, rho+p>0, c_s^2=1/2. But w=1/2 makes
      its BBN abundance an initial condition, so PR #226's eps_Q is a tuning.

  [O] THE REQUESTED OBJECT IS NOT DELIVERED: the coupled 2x2 K_ij / G_ij for
      (longitudinal aether, delta-phi) around the FLRW radiation background, with the
      Q^3 term retained, and its two eigenmode sound speeds. SZ21 gives the FLRW
      scalar sector only as a non-closing effective fluid; SZ22 is Minkowski and
      Q-independent. Deriving it needs the full second-order expansion of the action
      in Newtonian gauge with the lapse/shift constraints solved, which is an
      xAct/Cadabra-scale computation. I will not fabricate the matrices.

  CONSEQUENCE: the witness is NOT certified stable. It passes every condition that is
  published and independently checkable, and fails nothing -- but the specific check
  requested has not been performed, and one of its inputs (eps_Q) is a tuning.""")

print("\n" + "="*84)
print("EXIT 0 -- partial verification, gap stated explicitly [O]")
print("="*84)
