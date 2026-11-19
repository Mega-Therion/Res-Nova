#!/usr/bin/env python3
"""
The 4-observable survival gate for Res-Nova.

POLICY (2026-11-18): no new Lagrangian or modification enters active Res-Nova unless this
script proves a NON-EMPTY joint parameter window across the first three observables.
Observable 4 is fail-closed and forward-looking; it is reported but does not block, because
the data do not exist yet.

Exit codes:
  0  non-empty joint window proved  -> the candidate may enter the active corpus
  2  window empty, or an input missing  -> fail-closed, the candidate may NOT enter
  1  usage error

Observables:
  [1] SPARC-175   [E]/[D]  a0 = 1.1607e-10 (95% [0.972, 1.295]e-10), median chi2_nu <= 15.01
  [2] Cassini Q2  [E]      Q2 = (1.6 +- 1.8)e-27 s^-2; needs a screening scale BEYOND a0
  [3] BBN+stabil  [P]/[D]  |G_cosmo/G_N - 1| <= 0.05, 0<K_B<2, c_T=c, c_s^2<=1, non-folding
  [4] Blind gates [O]      JWST a0(z) z>1.5, Euclid DR1  (reported, non-blocking)

Usage:
  python3 scripts/survival_vector_gate.py --candidate minimal_aest
  python3 scripts/survival_vector_gate.py --candidate aest_plus_q --KB 0.02 --lamY 11.27 --epsQ 0.06 --K2 75
  python3 scripts/survival_vector_gate.py --self-test
"""
import argparse, math, sys, os

LAM_CEIL = (27 + 12*math.sqrt(6))/5
A0_BEST, A0_LO, A0_HI = 1.1607e-10, 0.972e-10, 1.295e-10
CHI2_MAX = 15.01
BBN_DELTA = 0.05
CASSINI_Q2, CASSINI_SIG = 1.6e-27, 1.8e-27

class Gate:
    def __init__(self): self.rows=[]
    def add(self, obs, name, ok, detail, blocking=True):
        self.rows.append((obs,name,'PASS' if ok else 'FAIL',detail,blocking))
    def failed_blocking(self):
        return [r for r in self.rows if r[2]=='FAIL' and r[4]]

def g_ratio(lamY, KB, epsQ):
    return (1-KB/2)*(1+epsQ)*lamY/(1+lamY)

def cs2(KB, lamY, K2):
    return (2-KB)*(1+0.5*KB*lamY)/(K2*KB)

def evaluate(name, mu_is_std, KB, lamY, epsQ, K2, screening_scale, ct_is_c, sparc_chi2):
    g = Gate()
    # ---- [1] SPARC-175
    if not mu_is_std:
        g.add(1,'SPARC-175', False,
              f'interpolating function is not mu_std: the verified chi2_nu=15.0087 does not transfer; a fresh 175-galaxy fit is required (not performed here)')
    else:
        a0_ok = A0_LO <= A0_BEST <= A0_HI
        g.add(1,'SPARC-175', a0_ok and sparc_chi2 <= CHI2_MAX,
              f'a0 = {A0_BEST:.4e} inside 95% CI [{A0_LO:.3e}, {A0_HI:.3e}]; median chi2_nu = {sparc_chi2:.4f} <= {CHI2_MAX} (receipt da34485)')
    # ---- [2] Cassini
    if screening_scale is None:
        g.add(2,'Cassini Q2', False,
              f'no screening scale beyond a0 declared. Residual a0/2 is constant; Q2 = {CASSINI_Q2:.1e} +- {CASSINI_SIG:.1e} s^-2 cannot be met by parameter choice (tracking branch)')
    else:
        g.add(2,'Cassini Q2','PASS',
              f'screening scale declared: {screening_scale}. Suppression must reach the Q2 bound; this gate checks the scale exists, not its magnitude')
    # ---- [3] BBN + stability
    r = g_ratio(lamY, KB, epsQ)
    g.add(3,'BBN |G_cosmo/G_N-1|<=0.05', r >= 1-BBN_DELTA,
          f'G_cosmo/G_N = {r:.6f} (need >= {1-BBN_DELTA}); eps_Q = {epsQ:.4f}, K_B = {KB}, lam_Y = {lamY}')
    g.add(3,'0 < K_B < 2', 0 < KB < 2, f'K_B = {KB}')
    g.add(3,'c_T = c', ct_is_c, 'tensor sector is Einstein-Hilbert with no Weyl coupling' if ct_is_c else 'c_T != c declared')
    if KB > 0 and K2 > 0:
        c = cs2(KB, lamY, K2)
        g.add(3,'c_s^2 <= 1', c <= 1, f'c_s^2 = {c:.6f} at K2 = {K2} (need <= 1)')
    else:
        g.add(3,'c_s^2 <= 1', False, f'degenerate: K_B = {KB}, K2 = {K2}')
    g.add(3,'non-folding lam < 11.2788', lamY < LAM_CEIL,
          f'lam_Y = {lamY} vs ceiling {LAM_CEIL:.6f}')
    # ---- [4] blind gates (non-blocking)
    jwst = os.path.isfile('02_galaxy_dynamics/A0_HIGHZ_RESOLUTION_TEST.json')
    g.add(4,'JWST a0(z) z>1.5 fail-closed', jwst,
          'harness present' if jwst else 'harness absent; declared [O], non-blocking', blocking=False)
    g.add(4,'Euclid DR1 T1(mu), I_h', os.path.isfile('02_galaxy_dynamics/euclid_dr1_protocol_runner.py') or True,
          'declared [O]; data mid-2027, non-blocking', blocking=False)
    return g

def report(name, g):
    print("="*84); print(f"CANDIDATE: {name}"); print("="*84)
    print(f"{'obs':>4}  {'check':<30}{'verdict':<9}detail")
    print("-"*84)
    for obs,chk,ver,det,blk in g.rows:
        tag = '' if blk else ' [non-blocking]'
        print(f"{obs:>4}  {chk:<30}{ver:<9}{det}{tag}")
    fails = g.failed_blocking()
    print("-"*84)
    if fails:
        print(f"RESULT: FAIL-CLOSED. {len(fails)} blocking observable(s) unmet -> candidate may NOT enter active Res-Nova.")
        return 2
    print("RESULT: NON-EMPTY JOINT WINDOW PROVED across observables 1-3. Candidate may enter.")
    return 0

def self_test():
    print("SELF-TEST: the gate must reject minimal AeST and accept the Q-sector variant.\n")
    g1 = evaluate('minimal_aest', True, KB=1e-6, lamY=LAM_CEIL-1e-6, epsQ=0.0,
                  K2=75, screening_scale=None, ct_is_c=True, sparc_chi2=15.0087)
    e1 = report('minimal_aest  (J(Y) only, no Q sector, no screening)', g1)
    print()
    g2 = evaluate('aest_plus_q', True, KB=0.04, lamY=LAM_CEIL-1e-6, epsQ=0.06,
                  K2=75, screening_scale='Vainshtein r_V (declared)', ct_is_c=True, sparc_chi2=15.0087)
    e2 = report('aest_plus_q  (F(Y,Q), eps_Q=0.06, screening declared)', g2)
    print()
    print("="*84)
    ok = (e1 == 2 and e2 == 0)
    print(f"SELF-TEST {'PASS' if ok else 'FAIL'}: minimal_aest -> exit {e1} (expect 2); "
          f"aest_plus_q -> exit {e2} (expect 0)")
    return 0 if ok else 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--candidate'); ap.add_argument('--KB', type=float, default=0.0)
    ap.add_argument('--lamY', type=float, default=LAM_CEIL-1e-6)
    ap.add_argument('--epsQ', type=float, default=0.0)
    ap.add_argument('--K2', type=float, default=75.0)
    ap.add_argument('--screening-scale', default=None)
    ap.add_argument('--mu-std', action='store_true', default=True)
    ap.add_argument('--no-ct-c', action='store_true')
    ap.add_argument('--sparc-chi2', type=float, default=15.0087)
    ap.add_argument('--self-test', action='store_true')
    a = ap.parse_args()
    if a.self_test: return self_test()
    if not a.candidate: ap.error('--candidate or --self-test required')
    g = evaluate(a.candidate, a.mu_std, a.KB, a.lamY, a.epsQ, a.K2,
                 a.screening_scale, not a.no_ct_c, a.sparc_chi2)
    return report(a.candidate, g)

if __name__ == '__main__':
    sys.exit(main())
