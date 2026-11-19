#!/usr/bin/env python3
"""(1) Extend the fsigma8 profiles beyond the pre-registered grid edge (x0 = 0.6).
(2) Codazzi wall-fluid check at the best fit: with no bulk flux, p_wall = -sigma - sigma_dot/(3H); for the drag tension
    sigma = sigma0 + (1/2) rho_b adot^2 the adiabatic sound speed c_s^2 = p_dot/sigma_dot is independent of sigma0 and rho_b:
    c_s^2 = -4/3 - (1/3) a adddot/(adot addot)."""
import json, math
import numpy as np
exec(open("drag_fit.py").read().split("out = {}")[0])
res = {}
for label, wf in (("+fs8_anchored", True), ("+fs8_free_amp", False)):
    cd = fit(with_fs=wf)[0]
    prof = [(float(x), fit(fix_x0=x, with_fs=wf)[0]) for x in np.arange(0.0, 1.25, 0.05)]
    px = np.array(prof); d = px[:, 1] - cd
    # interpolate the two Delta chi2 = 4 crossings
    xs = []
    for i in range(len(px) - 1):
        if (d[i] - 4) * (d[i + 1] - 4) < 0:
            xs.append(float(px[i, 0] + (4 - d[i]) * (px[i + 1, 0] - px[i, 0]) / (d[i + 1] - d[i])))
    res[label] = {"chi2_min": cd, "x0_2sigma_interp": xs, "Gcosmo_GN_2sigma": [1 / (1 + max(xs)), 1 / (1 + min(xs))] if len(xs) == 2 else None,
                  "dchi2_at_x0=0": float(d[0])}
    print(label, res[label], flush=True)
# Codazzi
h, Om, x0 = json.load(open("DRAG_FIT.json"))["BAO+SN+CMB"]["params_drag"]
N = np.linspace(math.log(1 / 11), 0.0, 4001); a = np.exp(N); H = E(1 / a - 1, h, Om, x0)   # units H0 = 1
t = np.concatenate([[0], np.cumsum(np.diff(N) * 0.5 * (1 / H[1:] + 1 / H[:-1]))])
ad = a * H; add = np.gradient(ad, t); addd = np.gradient(add, t)
cs2 = -4 / 3 - (1 / 3) * a * addd / (ad * add)
sel = [0, 0.3, 0.6, 1.0, 2.0, 5.0]
res["codazzi"] = {"params": [h, Om, x0], "cs2_at_z": {str(z): float(np.interp(math.log(1 / (1 + z)), N, cs2)) for z in sel},
                  "frac_of_range_z<10_with_0<=cs2<=1": float(np.mean((cs2 >= 0) & (cs2 <= 1))),
                  "note": "Valid only with zero bulk energy flux; a nonzero flux (Delta T_rn) frees p_wall."}
print(res["codazzi"]); json.dump(res, open("FOLLOWUPS.json", "w"), indent=1)
