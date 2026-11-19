#!/usr/bin/env python3
"""Small-Q0 dust-branch check (2026-11-18). [O]; O(1) factors dropped.
AeST background: d/dt[a^3 K'(Q)]=0, K ~ K2 (Q-Q0)^2 => 2K2(Q-Q0)=I0/a^3, rho ~ Q0*I0/a^3 (dust)
valid while (Q-Q0)/Q0 = rho/(2 K2 Q0^2) << 1. With mu^2 = 2K2 Q0^2/(2-K_B) this is
rho(z)/(mu^2 (2-K_B)) << 1: Q0 drops out; only mu (= sqrt(K2)*Q0 scale) controls the dust branch."""
import sympy as sp, json, math
K2,Q0,KB,I0,a=sp.symbols("K2 Q0 K_B I0 a",positive=True)
dQ=I0/(2*K2*a**3); mu2=2*K2*Q0**2/(2-KB)
ratio=sp.simplify((Q0*I0/a**3)/(2*K2*Q0**2)) - dQ/Q0
assert sp.simplify(ratio)==0                                  # validity = rho/(2K2Q0^2) = dQ/Q0
m=sp.Symbol("mu",positive=True)
assert sp.simplify((dQ/Q0).subs(K2,m**2*(2-KB)/(2*Q0**2)) - (Q0*I0/a**3)/(m**2*(2-KB)))==0  # = rho/(mu^2(2-K_B)): no Q0
# dQ/Q0 = rho/(mu^2 (2-K_B) Q0^2)*Q0^2/... -> in Mp^2 units: delta = 3 Om_c H^2_dm / mu^2
H0=1/4283.0; Om_c=0.26                                         # Mpc^-1
mu_min={f"z={z}":H0*math.sqrt(3*Om_c*(1+z)**3) for z in (1100,3400)}
Q0_door=2e-5
K2_need={k:v**2/(2*Q0_door**2) for k,v in mu_min.items()}      # K_B->0
out={"dust_validity_depends_on":"mu only (Q0 cancels)","mu_min_per_Mpc_for_delta<1":mu_min,
 "K2_needed_at_Q0=2e-5":K2_need,"K2_scale_vs_SZ_Q0=0.1":(0.1/Q0_door)**2,
 "galaxy_side_1_over_mu_kpc":{k:1e3/v for k,v in mu_min.items()},
 "verdict":"[O] DUST BRANCH SURVIVES small Q0: requirement is mu >~ 7.6 (z_rec) to 41 (z_eq) /Mpc, independent of Q0; "
  "Q0<=2e-5/Mpc just needs K2 ~ 1e11-1e12 (2.5e7 x SZ). Door stays OPEN.",
 "new_flags":["K2~1e11: check strong-coupling scale of Q fluctuations",
  "1/mu <~ 25-130 kpc is a galaxy-scale limit on MOND reach; inherited from SZ21, independent of this door"]}
print(json.dumps(out,indent=1)); json.dump(out,open("SMALL_Q0_DUST.json","w"),indent=1)
