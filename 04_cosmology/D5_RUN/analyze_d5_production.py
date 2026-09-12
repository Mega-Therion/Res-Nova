#!/usr/bin/env python3
"""
D5 PRODUCTION verdict analysis — validation config (N_pcl=256^3, L=200 Mpc/h).
Faithful adaptation of analyze_d5.py (the frozen script) to the production runs:

Operational adaptations (2026-09-11, documented in DRAFT_D5_LEDGER_ENTRY.md):
  1. Run paths point at the production output dirs (prod_lcdm, prod_armA,
     GitHub-Actions prod_armB).
  2. Redshift matching: for each target z in {0.0, 1.0}, each arm's output is
     the file with the smallest |z_actual - z_target|, required within 0.05
     (the frozen script's own near-zero tolerance, `abs(z) < 0.05`, applied
     symmetrically). Actual z values are recorded in the output.
     Fact: Arm A aligns EXACTLY with LCDM at z=0 and z=1, so V2 (the primary
     verdict, which uses only Arm A) is computed on identical epochs. Arm B's
     z=1 output landed at z=0.9809 (adaptive stepping under alpha=0.01); the
     Arm B z=1 table is reported for completeness but feeds no verdict gate.
  3. V1/V2 verdict logic is copied VERBATIM from the frozen script.

Verdict rules (PREREG_D5_MG_EVOLUTION.md sec. 5, frozen before the runs):
  V0 — patch correctness (gate): verified at build time by the frozen unit
       test (max relative kernel error < 1e-10 vs G_eff_tilde).
  V1 — pipeline sensitivity (negative control): Arm B median dP/P over
       k <= 0.2 h/Mpc at z~0 must be >= +5%.
  V2 — theory arm: CONSISTENT iff |dP/P|_A <= max(2 x linear_pred, 1%) for
       every k in [0.05, 2.5] h/Mpc at z=0 and z=1;
       TENSION iff any |dP/P|_A > 5%; else INCONCLUSIVE.
"""
import json, glob, datetime
import numpy as np

RUNS = {
    "lcdm": "../runs/prod_lcdm",
    "armA": "../runs/gh2/prod_armA",
    "armB": "../runs/gh2/prod_armB",
}
KMIN, KMAX = 0.05, 2.5
Z_TARGETS = (0.0, 1.0)
Z_TOL = 0.05

def load_pk(arm):
    out = {}
    for f in sorted(glob.glob(f"{RUNS[arm]}/*delta.dat")):
        with open(f, errors='replace') as fh:
            zlines = [l for l in fh.readlines() if l.startswith('# redshift')]
        if not zlines:
            continue
        z = float(zlines[0].split('=')[1])
        d = np.loadtxt(f)
        out[z] = d[d[:, 4] > 0]   # occupied bins only
    return out

def match_z(pk_dict, z_target):
    if not pk_dict:
        return None, None
    z_act = min(pk_dict.keys(), key=lambda z: abs(z - z_target))
    if abs(z_act - z_target) > Z_TOL:
        return None, None
    return z_act, pk_dict[z_act]

def main():
    params = json.load(open("../derivation/D5_MG_PARAMETERS.json"))
    lin = params["linear_predictions"]

    pk = {arm: load_pk(arm) for arm in RUNS}

    results = {
        "protocol": "PREREG_D5_MG_EVOLUTION.md",
        "analysis_generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "analysis_script": "analyze_d5_production.py (adaptation of frozen analyze_d5.py; V1/V2 verbatim)",
        "k_range_hmpc": [KMIN, KMAX],
        "config": "validation config (N_pcl=256^3, N_grid=256^3, L=200 Mpc/h, seed 42)",
        "armB_execution": "GitHub Actions runner, run 34597681204, determinism-verified vs local attempts (cycles 0/10/20 bit-identical)",
        "z_matching": "nearest output within +/-0.05 of target; see script docstring",
        "V0_patch_correctness": "PASS (frozen unit test at build time: max relative kernel error < 1e-10 vs G_eff_tilde(a,k))",
        "arms": {}, "verdicts": {},
        "z_used": {},
    }

    for z in Z_TARGETS:
        matched = {}
        for arm in RUNS:
            z_act, data = match_z(pk[arm], z)
            if data is None:
                continue
            matched[arm] = (z_act, data)
        if len(matched) == 3:
            for arm, (z_act, _) in matched.items():
                results["z_used"].setdefault(f"z={z}", {})[arm] = round(z_act, 6)
            base = matched["lcdm"][1]
            base_k, base_p = base[:, 0], base[:, 1]
            for arm in ("armA", "armB"):
                ks, ps = matched[arm][1][:, 0], matched[arm][1][:, 1]
                ratio = ps / np.interp(ks, base_k, base_p)   # identical grids -> exact
                sel = (ks >= KMIN) & (ks <= KMAX)
                results["arms"].setdefault(arm, {})[f"z={z}"] = {
                    "k_hmpc": ks[sel].tolist(),
                    "dP_over_P": (ratio[sel] - 1.0).tolist(),
                }

    # ---- V1 ----  (verbatim logic from frozen script)
    v1 = None; v1_detail = None
    d0 = results["arms"]["armB"].get("z=0.0")
    if d0 is not None:
        mask = np.array(d0["k_hmpc"]) <= 0.2
        vals = np.array(d0["dP_over_P"])[mask]
        med = float(np.median(vals))
        v1 = bool(mask.any() and med >= 0.05)
        v1_detail = {"median_dPdP_k_le_0.2": med,
                     "n_bins": int(mask.sum()),
                     "predicted_linear": lin["armB_dP_over_P_z0"]}
    results["verdicts"]["V1_pipeline_sensitivity_PASS"] = v1
    results["verdicts"]["V1_detail"] = v1_detail

    # ---- V2 ----  (verbatim logic from frozen script)
    worst = {"value": -1.0, "k": None, "z": None}
    consistent, tension = True, False
    for z in Z_TARGETS:
        lp = lin["armA_dP_over_P_z0"] if z == 0.0 else lin["armA_dP_over_P_z1"]
        d = results["arms"]["armA"].get(f"z={z}")
        if d is None:
            continue
        for kq, dp in zip(d["k_hmpc"], d["dP_over_P"]):
            if abs(dp) > max(2.0 * lp, 0.01):
                consistent = False
            if abs(dp) > 0.05:
                tension = True
            if abs(dp) > worst["value"]:
                worst = {"value": abs(dp), "k": kq, "z": z}
    results["verdicts"]["V2_worst_armA"] = worst
    results["verdicts"]["V2_verdict"] = ("TENSION" if tension else
                                         "CONSISTENT" if consistent else "INCONCLUSIVE")
    results["verdicts"]["V2_note"] = ("bounds: max(2*linear, 1%) per bin at z=0 and z=1; TENSION threshold 5%")
    results["verdicts"]["linear_predictions"] = lin

    if v1 is False:
        results["verdicts"]["FINAL"] = "ABORT (pipeline insensitive; no D5 claim)"
    elif results["verdicts"]["V2_verdict"] == "CONSISTENT":
        results["verdicts"]["FINAL"] = "CONSISTENT (validation config: D5 MG-evolution arm is consistent with LCDM within frozen bounds)"
    else:
        results["verdicts"]["FINAL"] = results["verdicts"]["V2_verdict"] + " (see V2)"

    with open("D5_RUN_VERDICT_PRODUCTION.json", "w") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results["verdicts"], indent=2))

    # ---- plot ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
        for ax, z in zip(axes, Z_TARGETS):
            for arm, color, lbl in [("armA", "tab:blue", "Arm A (alpha=1, theory)"),
                                    ("armB", "tab:red", "Arm B (alpha=0.01, control)")]:
                d = results["arms"][arm].get(f"z={z}")
                if d is None:
                    continue
                ax.plot(d["k_hmpc"], 100 * np.array(d["dP_over_P"]),
                        color=color, lw=1.2, label=lbl)
            lp = lin["armA_dP_over_P_z0"] if z == 0.0 else lin["armA_dP_over_P_z1"]
            ax.axhline(100 * lp, color="tab:blue", ls=":", lw=1, label="linear pred (A)")
            ax.axhline(100 * max(2 * lp, 0.01), color="gray", ls="--", lw=0.8, label="V2 bound")
            ax.axhline(0, color="k", lw=0.5)
            ax.set_xscale('log')
            ax.set_xlabel("k [h/Mpc]")
            ax.set_ylabel("P_arm/P_LCDM - 1  [%]")
            ax.set_title(f"z = {z}")
            ax.legend(fontsize=8)
        fig.suptitle("D5 production: MG-evolution vs LCDM, validation config (identical ICs)", y=1.02)
        fig.tight_layout()
        fig.savefig("d5_pk_comparison_production.png", dpi=130, bbox_inches="tight")
        print("plot -> d5_pk_comparison_production.png")
    except Exception as e:
        print("plot skipped:", e)

if __name__ == "__main__":
    main()
