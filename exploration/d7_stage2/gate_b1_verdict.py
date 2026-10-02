#!/usr/bin/env python3
"""Verdict for gate B1. Criterion fixed before the corrected run's numbers were seen (2026-09-28): PASS iff
  (a) Newton converged at both grids;
  (b) the Newton- and MOND-channel ratios are within 0.02 of 1 at every shell, at both grids;
  (c) refinement does not drift away from 1: at every shell and channel, |ratio_fine - 1| <= |ratio_coarse - 1| + 0.005;
  (d) the aether stays held: max |u| / stealth tilt < 1e-3 at both grids.
Usage: gate_b1_verdict.py <GATE_B1 json> [sharp|smooth]. The first corrected run (GATE_B1_STATIC_FE.json, g_e = 0.03 a0,
box asinh(100)) was judged with the sharp estimator and FAILED (c) at r = 0.1 kpc (GATE_B1_VERDICT.txt). The cause was
the estimator (diag_b1_flux.py); later runs are judged with the smooth estimator, which was introduced after that
failure, and say so."""

import json, sys

path = sys.argv[1] if len(sys.argv) > 1 else "GATE_B1_STATIC_FE.json"
est = sys.argv[2] if len(sys.argv) > 2 else "sharp"
suf = "" if est == "sharp" else "_smooth"
res = json.load(open(path))
coarse, fine = res[0], res[1]
fails = []
for rr in res:
    if not rr["converged"]:
        fails.append(
            f"{rr['nR']}x{rr['nz']}: Newton not converged (residual {rr['final_residual']:.1e})"
        )
    if rr["max_u_over_stealth_tilt"] >= 1e-3:
        fails.append(
            f"{rr['nR']}x{rr['nz']}: aether tilt {rr['max_u_over_stealth_tilt']:.1e}"
        )
    for sh in rr["shells"]:
        for ch in ("newton_channel_ratio", "mond_channel_ratio"):
            if abs(sh[ch + suf] - 1) > 0.02:
                fails.append(
                    f"{rr['nR']}x{rr['nz']} r={sh['r_kpc']} kpc {ch + suf} = {sh[ch + suf]:.4f}"
                )
for sc, sf in zip(coarse["shells"], fine["shells"]):
    for ch in ("newton_channel_ratio", "mond_channel_ratio"):
        if abs(sf[ch + suf] - 1) > abs(sc[ch + suf] - 1) + 0.005:
            fails.append(
                f"r={sc['r_kpc']} kpc {ch + suf} drifts away from 1: {sc[ch + suf]:.4f} -> {sf[ch + suf]:.4f}"
            )
print(
    f"{path}, {est} estimator"
    + (
        " (introduced after the sharp estimator's failure; see diag_b1_flux.py)"
        if est == "smooth"
        else ""
    )
)
for rr in res:
    print(
        f"{rr['nR']}x{rr['nz']}: converged {rr['converged']} (residual {rr['final_residual']:.1e}), u/tilt {rr['max_u_over_stealth_tilt']:.1e}"
    )
    for sh in rr["shells"]:
        print(
            f"   r = {sh['r_kpc']:.1f} kpc: Newton channel {sh['newton_channel_ratio' + suf]:.4f}, MOND channel {sh['mond_channel_ratio' + suf]:.4f}"
        )
print("GATE B1 " + ("PASS" if not fails else "FAIL:\n  " + "\n  ".join(fails)))
