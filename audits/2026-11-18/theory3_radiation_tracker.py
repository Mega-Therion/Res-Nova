#!/usr/bin/env python3
"""
Theory 3: replace the Q^3 operator with a radiation-tracking Q^4, and test whether
"p >= 3/2" screening is compatible with the MOND limit.

Two independent questions:
  A. Does F(0,Q) = -c Q^4 give w = 1/3 exactly, so that rho_phi ~ a^-4 and
     rho_phi/rho_rad is CONSTANT? (the F5 x F4 immunization rule)
  B. Does "switch the Y-sector to p >= 3/2" preserve MOND? (it does not)

Run: python3 audits/2026-11-18/theory3_radiation_tracker.py   (exit 0)
"""
import sympy as sp

Qb, c, a = sp.symbols('Qbar c a', positive=True)
p_ = sp.symbols('p', positive=True)

def hdr(t): print("\n"+"="*84+f"\n{t}\n"+"="*84)

hdr("A.  w for F(0,Q) = -c Q^p  (the operator family)")
print(f"  {'p':>3}  {'w = p/(p-1)':>14}  {'rho ~ a^?':>12}  {'c_s^2':>8}  {'tracks radiation?':>18}")
for pv in (2,3,4,5):
    F = -c*Qb**pv
    rho = sp.simplify(F - Qb*sp.diff(F,Qb)); pr = sp.simplify(-F)
    w = sp.simplify(pr/rho); cs2 = sp.simplify(sp.diff(F,Qb)/(Qb*sp.diff(F,Qb,2)))
    expo = sp.simplify(-3*(1+w))
    print(f"  {pv:>3}  {str(w):>14}  {str(expo):>12}  {str(cs2):>8}  "
          f"{'YES' if expo==-4 else 'no':>18}")
print("""
  [P] p = 4 gives w = 1/3 exactly, so rho_phi ~ a^-4: identical scaling to radiation.
      Therefore rho_phi/rho_rad is CONSTANT in time, and the BBN value equals the CMB
      value equals today's. No initial-condition tune to hit a value at a chosen epoch.
      This satisfies the F5 x F4 rule ("ban w != 1/3 during radiation domination").
  [P] p = 3 (the PR #226 choice) gives w = 1/2, rho ~ a^-4.5: redshifts away, so the
      BBN abundance IS an initial-condition tune. Confirms the panel's diagnosis.""")

hdr("A2.  the Q^4 witness through the BBN requirement")
LAM = (27+12*sp.sqrt(6))/5
eta = LAM/(1+LAM)
need = sp.Rational(95,100)*(1+1/LAM) - 1
print(f"  non-folding ceiling lambda_s < {float(LAM):.6f}")
print(f"  required eps_Q = rho_phi/rho_rad >= {float(need):.6f}  ({100*float(need):.3f}%)")
coef = sp.Rational(7,8)*(sp.Rational(4,11))**sp.Rational(4,3)
k = float(coef/(1+coef*sp.Rational(3044,1000)))
dNeff = float(need)/k
print(f"  => Delta N_eff = {dNeff:.4f}   (a constant at every epoch; eps_Q itself is still free)")
print(f"  with K_B = 0.008, lambda_s = 11.2787, c_s^2(Q-sector) = 1/3:")
for KBv in (0.0, 0.008):
    eps = (1+float(need))/(1-KBv/2) - 1
    r = (1-KBv/2)*(1+eps)*float(eta)
    print(f"    K_B = {KBv:.3f}: eps_Q = {eps:.5f}  G_cosmo/G_N = {r:.6f}  "
          f"{'PASS' if r>=0.95 else 'FAIL'}")

hdr("B.  does p >= 3/2 preserve MOND?  (it does not)")
print("""  Static limit, J(Y) = A|Y|^p with Y = |grad phi|^2. The field equation is
        grad . ( J_Y grad phi ) = source,   J_Y = A p |Y|^(p-1) = A p |grad phi|^(2p-2)
  so for a point mass, spherical symmetry gives |grad phi|^(2p-1) r^2 = const, i.e.

        force = |grad phi|  ~  r^(-2/(2p-1))""")
print(f"\n  {'p':>6}  {'force exponent':>16}  {'law':>22}")
for pv in (sp.Rational(1,1), sp.Rational(5,4), sp.Rational(3,2), sp.Rational(2,1), sp.Rational(5,2)):
    e = sp.simplify(-2/(2*pv-1))
    law = {sp.Rational(-2,1):'Newtonian 1/r^2',
           sp.Rational(-1,1):'MOND 1/r',
           sp.Rational(-4,3):'steeper than MOND',
           sp.Rational(-2,3):'SHALLOWER than MOND',
           sp.Rational(-1,2):'much shallower'}.get(e, '')
    print(f"  {str(pv):>6}  {str(e):>16}  {law:>22}")
print("""
  [P] p = 3/2 is the UNIQUE power giving the 1/r MOND force. Every p > 3/2 gives a
      SHALLOWER falloff, i.e. MORE force at large r, not less.

  [C] SZ22, verbatim: "MOND behavior emerges if J -> 2 lambda_s/(3(1+lambda_s)a_0)|Y|^{3/2}"
      and "Screening may be achieved either through terms in J ~ Y^p with p > 3/2 or
      through Galileon-type terms".

  [D] So p > 3/2 is a route that SACRIFICES the MOND limit; it is an alternative to
      MOND, not an addition to it. Replacing the p = 3/2 term with p > 3/2 to fix
      Cassini would delete the galactic phenomenology the whole programme exists for.

  [O] The correct Cassini route is therefore the OTHER branch SZ name: a Galileon-type
      term added to the action, which can screen above a_0 while leaving the p = 3/2
      MOND limit intact at galactic accelerations. That term is not written here and
      its Q2 suppression magnitude is not computed.""")

hdr("VERDICT")
print(f"""  [P] Q^4 / w = 1/3: SOUND. rho_phi ~ a^-4, eps_Q constant, Delta N_eff is
      a RANGE (~{dNeff:.2f}-0.29), not a unique number; what w = 1/3 buys is that eps_Q is
      the same constant at BBN and at the CMB instead of a drifting quantity. That is
      what satisfies the F5 x F4 rule, and it is a strict improvement on Q^3.

  [X] "p >= 3/2 screening": NOT ADOPTED AS STATED. p > 3/2 breaks the 1/r MOND force
      (only p = 3/2 gives it). The screening must come from a Galileon term instead.

  [O] Cassini Q2 remains unaddressed by either half: no suppression magnitude is
      computed anywhere in this programme.

  NET: Theory 3 is half-right. Adopt the Q^4 tracker. Replace the p >= 3/2 prescription
  with a Galileon screening term. The two changes are independent and the second is the
  harder one.""")
