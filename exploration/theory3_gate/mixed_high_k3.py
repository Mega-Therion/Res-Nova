#!/usr/bin/env python3
"""Mixed cubic+quartic: the high-K3 corner the pre-registered grid reached but the threshold runs did not
(10x, 100x, 1000x the stability-threshold K3), for the K4 values whose threshold rows passed SPARC.
Gates as before: MW g(R_sun) reachable, Cassini Q2 (first-order l=2 solver, both g_e), Mercury, SPARC. [O]
Scope: total-law embedding (AEST_TOTAL_SCALAR_CORRESPONDENCE), an [O] alternative to D9's function."""
import json, os
import mixed_l3l4 as M
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, "MIXED_STABILITY_SPARC.json")))
surv = [r for r in rows if r["mercury_ok"] and r["mw_reachable"] and r["sparc"]["dchi2_total"] <= 0]
out = []
for r in surv:
    for mult in (10.0, 100.0, 1000.0):
        lam, K4 = r["lambda_s"], r["K4"]; K3 = r["K3_threshold"] * mult
        rec = {"lambda_s": lam, "K4": K4, "K3": K3, "mult": mult}
        q2 = []; prec = []
        for gt in (1.9e-10, 2.4e-10):
            f = M.fmw_for_g(lam, K3, K4, gt)
            if f is None:
                rec[f"g={gt:.1e}"] = "unreachable"; continue
            sg = M.sun_gate(M.setup(lam, K3, K4, f))
            rec[f"g={gt:.1e}"] = {"fmw": f, **sg}; q2.append(sg["saturn_Q2_eff"]); prec.append(sg["mercury_prec"])
        rec["cassini_ok"] = len(q2) == 2 and all(M.Q2_LO <= x <= M.Q2_HI for x in q2)
        rec["mercury_ok"] = len(prec) == 2 and all(p <= M.PREC_MAX for p in prec)
        rec["sparc"] = M.sparc(lam, K3, K4)
        rec["pass_all"] = rec["cassini_ok"] and rec["mercury_ok"] and rec["sparc"]["dchi2_total"] <= 0
        out.append(rec)
        print(f"lam={lam} K4={K4:.1e} x{mult:g}: Q2={['%.1e' % x for x in q2]} prec={['%.1e' % p for p in prec]} "
              f"fmw={[round(rec[k]['fmw'], 2) for k in rec if k.startswith('g=') and isinstance(rec[k], dict)]} "
              f"sparc={rec['sparc']['dchi2_total']:.0f} pass={rec['pass_all']}", flush=True)
json.dump(out, open(os.path.join(HERE, "MIXED_HIGH_K3.json"), "w"), indent=1, default=float)
print("any pass:", any(r["pass_all"] for r in out))
