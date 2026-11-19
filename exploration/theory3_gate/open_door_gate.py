#!/usr/bin/env python3
"""Open-door gate (2026-11-18). Order-of-magnitude, O(1) coefficients dropped -> verdicts are [O].
(1) Quartic Horndeski Galileon: Vainshtein p=2 (r^2 pi' + pi'^3/L^6 = M/4piMp => pi' const).
    Decay bound (Creminelli+ 1809.03484) forces alpha_H=0 -> pure Horndeski quartic, which has
    alpha_H=0 already; the binding bound is |alpha_T| <~ 1e-15 (GW170817), alpha_T ~ Xbar^2/(Mp^2 L^6).
(2) Scaling field exit: window between BBN and recombination."""
import json, math
Mp=2.435e18; H0=1.44e-42; Msun=1.116e57; pc=1.5637e32          # GeV units, reduced Mp
AU=pc/206264.8; r_merc=0.387*AU
need=2.973407407407408e-12; rV_cap=2.3609412457165018*pc          # VAINSHTEIN_PREQ.json
rV_min=r_merc*need**(-1/2)                                        # p=2 requirement
def alphaT_over_eps4(rV):
    L6=(Msun/(4*math.pi*Mp*rV**3))**2
    return (Mp*H0)**4/(Mp**2*L6)
out={"rV_min_pc":rV_min/pc,"rV_cap_pc":rV_cap/pc,"window_exists":rV_min<rV_cap}
for tag,rV in (("rV_min",rV_min),("rV_cap",rV_cap)):
    a=alphaT_over_eps4(rV); out[tag]={"alphaT_at_eps1":a,"eps_max_for_cT":(1e-15/a)**0.25}
# (2) exit between BBN (T~1 MeV, z~4e9) and recombination (z~1090): scalar mass m ~ H(z_exit)
Or=9.1e-5; Om=0.31
H=lambda z: H0*math.sqrt(Or*(1+z)**4+Om*(1+z)**3)
out["exit_mass_window_eV"]=[H(1.1e4)*1e9, H(4e9)*1e9]   # exit after z_eq-ish margin .. before BBN
out["verdict"]=("[O] MAYBE-SAT: Cassini via quartic Horndeski needs r_V in [%.2f, %.2f] pc and the "
 "screening scalar's cosmological roll eps=phidot/(Mp H0) below ~%.2f-%.2f; the BBN compensator needs "
 "one mass in [%.1e, %.1e] eV. Next obligation: compute eps from AeST's own Q0 normalization."%(
 rV_min/pc,rV_cap/pc,out["rV_cap"]["eps_max_for_cT"],out["rV_min"]["eps_max_for_cT"],*out["exit_mass_window_eV"]))
print(json.dumps(out,indent=1)); json.dump(out,open("OPEN_DOOR_GATE.json","w"),indent=1)
