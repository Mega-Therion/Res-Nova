#!/usr/bin/env python3
"""CMB-lensing (sigma8 Om^0.25) and late-ISW proxies for the flux-fed drag wall (PREREG_LENS_ISW.md)."""
import json
import numpy as np
import flux_codazzi_check as F
from drag_fit import REF_D1
d = json.load(open("FLUX_CODAZZI.json"))["F2_self_consistent_coupled_refit"]
def amp(h, Om, kappa):
    D, v = F.growth_coupled(h, Om, kappa); a = F._A_GROWTH; z = 1 / a - 1
    s8 = 0.811 * D[-1] / REF_D1
    m = z <= 3; zz, y = z[m][::-1], (D[m] * (1 + z[m]))[::-1]
    isw = float(np.trapezoid(np.abs(np.gradient(y, zz)), zz)) / D[-1]
    return s8, s8 * Om ** 0.25, isw
out = {}
for k, v in d.items():
    if not isinstance(v, dict) or "params_coupled_h_Om_kappa" not in v: continue
    h, Om, ka = v["params_coupled_h_Om_kappa"]; hl, Oml = v["params_LCDM_h_Om"]
    s8, S, isw = amp(h, Om, ka); s8l, Sl, iswl = amp(hl, Oml, 0.0)
    r = isw / iswl
    out[k] = {"sigma8": float(s8), "S_lens": float(S), "S_lens_LCDM": float(Sl), "lens_pull_sigma": float((S - 0.589) / 0.020),
              "ISW_ratio": float(r), "lens_pass": bool(abs(S - 0.589) <= 0.040), "isw_pass": bool(0.4 <= r <= 1.6)}
    print(k, {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in out[k].items()})
out["verdict"] = "SURVIVES proxies" if all(o["lens_pass"] and o["isw_pass"] for o in out.values() if isinstance(o, dict)) else "FAILS a proxy"
print(out["verdict"]); json.dump(out, open("LENS_ISW_PROXY.json", "w"), indent=1)
