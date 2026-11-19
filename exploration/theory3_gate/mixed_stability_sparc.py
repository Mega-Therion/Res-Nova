#!/usr/bin/env python3
"""Mixed cubic+quartic: does the cubic needed to STABILISE the quartic solar core survive SPARC? (2026-11-18) [O]

quartic_core_instability.py: the quartic-dominated core is angularly stable iff 2 k3^2/(3 k4) > Z_max, where
near the Sun Z = A_e (I + L e e) (the Galactic tide is cancelled by the induced response). In K units
(k3^2/k4 = K3^2/(2 K4)) that reads K3 > sqrt(3 K4 A_e (1+L)). Take the threshold, which screens galaxies least.
In deep MOND, the cubic/AQUAL flux ratio in any galaxy is K3/(eta r), independent of mass: everything inside
r ~ K3/eta has its MOND scalar suppressed. Gates:
  Mercury, from the quartic core force (GM a0m^2/K4)^(1/3);
  Milky Way g(R_sun) reachable;
  SPARC Delta chi2 <= 0 against the live mu_std baseline.
"""
import json, math, os
import numpy as np
import mixed_l3l4 as M
import door_nested_solution as D
out = []
for lam in (0.5, 1.0, 3.0):
    eta = lam / (1 + lam); a0m = eta * D.A0FIT
    for K4 in (1.2e38, 3e38, 1e39, 3e39, 1e40, 3e40, 1e41):
        c = (D.GM * a0m**2 / K4) ** (1 / 3)
        prec = 2 * math.pi * c * (0.387 * D.AU) ** 2 / D.GM * (100 / 0.2408) * 206264.8
        K3 = math.sqrt(3 * K4)
        for _ in range(3):
            f = M.fmw_for_g(lam, K3, K4, 1.9e-10)
            if f is None:
                break
            P = M.setup(lam, K3, K4, f, galactic=False)
            K3 = math.sqrt(3 * K4 * P["Ae"] * (1 + P["Le"]))
        row = {"lambda_s": lam, "K4": K4, "K3_threshold": K3, "cubic_screen_radius_kpc": K3 / eta / D.KPC,
               "mercury_prec": prec, "mercury_ok": prec <= D.PREC_MAX, "mw_reachable": f is not None}
        if f is not None:
            row["fmw"] = f; row["Ae_1pL"] = P["Ae"] * (1 + P["Le"])
            row["sparc"] = M.sparc(lam, K3, K4)
        out.append(row)
        print(f"lam={lam} K4={K4:.1e} K3={K3:.2e} r_screen={row['cubic_screen_radius_kpc']:.1f}kpc prec={prec:.1e} "
              f"mw={'ok' if f else 'X'} sparc={row.get('sparc', {}).get('dchi2_total', float('nan')):.0f} "
              f"n>25={row.get('sparc', {}).get('galaxies_dchi2>25', '-')}", flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "MIXED_STABILITY_SPARC.json"), "w"), indent=1, default=float)
ok = [r for r in out if r["mercury_ok"] and r["mw_reachable"] and r["sparc"]["dchi2_total"] <= 0]
print("rows passing Mercury + MW + SPARC at the stability threshold:", len(ok))
