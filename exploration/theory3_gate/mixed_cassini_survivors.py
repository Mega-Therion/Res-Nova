#!/usr/bin/env python3
"""Cassini leak for the rows of MIXED_STABILITY_SPARC.json that pass Mercury + MW + SPARC, at 1.0x and 1.5x the
stability-threshold K3, at g(R_sun) = 1.9 and 2.4e-10. [O], first-order l=2 solver (mixed_l3l4.sun_gate).
Caveat: the solver holds the Galaxy's cofactor terms constant; inside r_T ~ c/|T| they are cancelled. The leak is
set near r_V, which here exceeds the vertical r_T (~0.2 pc), so the estimate should be roughly right there."""
import json, os
import mixed_l3l4 as M
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, "MIXED_STABILITY_SPARC.json")))
surv = [r for r in rows if r["mercury_ok"] and r["mw_reachable"] and r["sparc"]["dchi2_total"] <= 0]
out = []
for r in surv:
    for mult in (1.0, 1.5):
        K3 = r["K3_threshold"] * mult; K4 = r["K4"]; lam = r["lambda_s"]
        rec = {"lambda_s": lam, "K4": K4, "K3": K3, "mult": mult}
        for gt in (1.9e-10, 2.4e-10):
            f = M.fmw_for_g(lam, K3, K4, gt)
            if f is None:
                rec[f"g={gt:.1e}"] = "unreachable"; continue
            P = M.setup(lam, K3, K4, f)
            sg = M.sun_gate(P)
            rec[f"g={gt:.1e}"] = {"fmw": f, "Q2_eff": sg["saturn_Q2_eff"], "prec": sg["mercury_prec"],
                                  "Z_eigs": [float(x) for x in __import__('numpy').linalg.eigvalsh(P["Z"])]}
        q = [v["Q2_eff"] for k, v in rec.items() if k.startswith("g=") and isinstance(v, dict)]
        rec["cassini_ok"] = bool(q) and all(M.Q2_LO <= x <= M.Q2_HI for x in q)
        out.append(rec)
        print(f"lam={lam} K4={K4:.1e} K3={K3:.2e} (x{mult}) Q2={['%.1e' % x for x in q]} fmw={[round(v['fmw'],2) for k,v in rec.items() if k.startswith('g=') and isinstance(v,dict)]} cassini_ok={rec['cassini_ok']}", flush=True)
json.dump(out, open(os.path.join(HERE, "MIXED_CASSINI_SURVIVORS.json"), "w"), indent=1, default=float)
print("any Cassini pass:", any(r["cassini_ok"] for r in out))
