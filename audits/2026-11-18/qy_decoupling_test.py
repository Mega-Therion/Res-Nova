#!/usr/bin/env python3
"""
Does decoupling the timelike (Q) and spacelike (Y) sectors dissolve the BBN no-go?

Two facts are established here, in order:

  FACT 1 (exact).  On FLRW, Y = q^{mu nu} grad_mu phi grad_nu phi vanishes identically,
                   because q^{00} = g^{00} + A^0 A^0 = 0 for a unit timelike A^mu.
                   Consequence: a J(Y)-only theory has NO cosmological scalar dynamics
                   from J. So in minimal AeST, G_cosmo cannot be governed by J at all;
                   it is (1 - K_B/2) G_hat, and the ONLY place lam_s enters the BBN ratio
                   is through G_N = (1 + 1/lam_s) G_hat, which is a QUASI-STATIC (Y-sector)
                   quantity.

  FACT 2 (arithmetic).  Therefore in minimal AeST one parameter, lam_s, is forced to do
                   double duty: BBN needs it LARGE (weak fifth force, G_N -> G_hat) while
                   non-folding needs it SMALL. That is the whole no-go, and it is not
                   about mu(x).

  FACT 3 (the escape).  Give G_cosmo an independent Q-sector contribution,
                   G_cosmo = (1 - K_B/2)(1 + eps_Q) G_hat, with eps_Q from F_Q at the
                   cosmological background. Then BBN and non-folding stop sharing a knob,
                   and the no-go dissolves at a computable eps_Q.

Run: python3 audits/2026-11-18/qy_decoupling_test.py   (exit 0)
"""
import math
import sympy as sp

LAM_CEIL = (27 + 12*math.sqrt(6))/5      # 11.278775 non-folding ceiling
ETA      = LAM_CEIL/(1+LAM_CEIL)         # 0.918559 = sqrt(27/32)

print("="*80)
print("FACT 1  —  Y vanishes identically on FLRW")
print("="*80)
# mostly-plus signature: g^{00} = -1, A^mu = (1,0,0,0), A_mu A^mu = -1
t, a = sp.symbols('t a', positive=True)
g_inv = sp.diag(-1, 1/a**2, 1/a**2, 1/a**2)          # g^{mu nu}
A_up  = sp.Matrix([1, 0, 0, 0])                       # A^mu, unit timelike
A_lo  = g_inv*A_up                                    # A_mu = g_{mu nu} A^nu
q_inv = g_inv + A_up*A_up.T                           # q^{mu nu} = g^{mu nu} + A^mu A^nu
print(f"  A_mu A^mu        = {sp.simplify((A_lo.T*A_up)[0,0])}   (unit timelike)")
print(f"  q^00             = {sp.simplify(q_inv[0,0])}")
print(f"  q^ij             = diag{tuple(sp.simplify(q_inv[i,i]) for i in (1,2,3))}")
phi = sp.Function('phi')(t)
grad = sp.Matrix([sp.diff(phi, t), 0, 0, 0])          # homogeneous: grad_i phi = 0
Y = sp.simplify((grad.T*q_inv*grad)[0,0])
print(f"  Y = q^munu d_mu phi d_nu phi = {Y}")
print(f"  => Y == 0 for ALL phi(t). Confirmed: {Y == 0}")
print("""
  So J(Y) on FLRW contributes only the constant J(0). Minimal AeST therefore has no
  cosmological scalar dynamics from J, and lam_s cannot enter G_cosmo. It enters only
  G_N = (1 + 1/lam_s) G_hat, which is the quasi-static Newtonian limit: a Y-sector object.""")

print("="*80)
print("FACT 2  —  one knob, two regimes: the no-go restated")
print("="*80)
def ratio_minimal(lam, KB):
    """G_cosmo/G_N = (1 - K_B/2)/(1 + 1/lam)."""
    return (1 - KB/2)/(1 + 1/lam)

print("  G_cosmo/G_N = (1 - K_B/2)/(1 + 1/lam_s)")
print("  BBN needs this LARGE  ->  lam_s large  (fifth force weak)")
print("  non-folding needs lam_s < 11.2788      ->  lam_s small")
print("  Both statements are about the SAME Y-sector lam_s. Hence the collision.")
print(f"\n  sup over {{0<K_B<2, 0<lam<{LAM_CEIL:.4f}}} = {ETA:.6f} = sqrt(27/32)")
print(f"  5% BBN needs 0.95  ->  impossible by {0.95-ETA:.6f}")

print("="*80)
print("FACT 3  —  the escape: give G_cosmo its own Q-sector knob")
print("="*80)
print("  G_cosmo = (1 - K_B/2)(1 + eps_Q) G_hat,   eps_Q from F_Q(0, Q_0) at BBN")
print("  G_cosmo/G_N = (1 - K_B/2)(1 + eps_Q) * lam_Y/(1 + lam_Y)")
print("  With lam_Y at the non-folding ceiling, the ratio is linear in (1 + eps_Q):\n")
print(f"{'BBN bound':>11}{'eps_Q at K_B=0':>18}{'eps_Q at K_B=0.04':>20}{'feasible?':>12}")
for pct in (5, 4, 3, 2, 1, 0):
    need = (1-pct/100)/ETA                      # required (1-KB/2)(1+eps) factor
    e0   = need - 1
    e04  = need/(1-0.04/2) - 1
    print(f"{pct:>10}%{100*e0:>17.3f}%{100*e04:>19.3f}%{'yes' if e0>0 else 'no (bound already met)':>12}")

need5 = (1-0.05)/ETA
print(f"\n  HEADLINE: at the 5% BBN bound a Q-sector contribution of just")
print(f"            eps_Q >= {100*(need5-1):.3f}%  (at K_B -> 0)")
print(f"            dissolves the no-go entirely, with lam_Y pinned at {LAM_CEIL:.4f}.")
print(f"            With K_B = 0.04 it needs {100*(need5/(1-0.02)-1):.3f}%.")

print("="*80)
print("Does the Q-sector operator itself stay healthy?")
print("="*80)
print("""  A Q-sector term is k-essence in the timelike direction, P(Q). For L = P(Q):
      ghost-free     requires  P_Q > 0
      c_s^2 <= 1     requires  P_QQ >= 0   (c_s^2 = P_Q/(P_Q + 2Q P_QQ) <= 1)
  Both are satisfied by the minimal choice P(Q) = (1/2)Q^2 with a small coefficient,
  and eps_Q is then set by the coefficient, not by any tuning of lam_s.
  The Y-sector (galactic mu, non-folding) is untouched at leading order because
  Y = 0 on FLRW: the two sectors do not mix at background level.""")

print("="*80)
print("VERDICT")
print("="*80)
print(f"""  Ryan's Q/Y intuition is right in substance but the mechanism is the reverse of
  the stated one. In minimal AeST the BBN bound is NOT driven by Q: G_cosmo carries no
  lam_s at all, and lam_s reaches the ratio only through the quasi-static G_N. That is
  precisely why the same lam_s is trapped by both walls.

  The escape is therefore to ADD a Q sector, not to invoke one that already exists:
  a >= {100*(need5-1):.2f}% contribution to G_cosmo from F_Q at the BBN background, with
  P_QQ >= 0 for causality. Then lam_Y sits at {LAM_CEIL:.4f}, non-folding holds, BBN holds,
  and c_T = c is untouched.

  This is a one-line change to the action and a three-line change to the no-go theorem.
  It is testable in Z3 as a SAT instance over (K_B, lam_Y, eps_Q) in milliseconds.""")
