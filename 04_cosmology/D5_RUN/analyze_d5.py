#!/usr/bin/env python3
"""
D5 verdict analysis (PREREG_D5_MG_EVOLUTION.md section 5).
Reads the matter P(k) files from the three runs (lcdm, armA, armB),
computes dP/P = P_arm/P_lcdm - 1 over k in [0.05, 2.5] h/Mpc at z = 0, 1,
and applies the frozen verdict rules:

  V1 (pipeline sensitivity, negative control): Arm B must show the
      enhancement: MEDIAN of dP/P over k <= 0.2 h/Mpc at z=0 >= +5%.
      (Clarification made 2026-09-10 BEFORE any run output existed: the
       prereg text "dP/P >= +5% at z=0 for k <= 0.2" is read as a robust
       central-value test, not all-bins, to avoid a single noisy bin
       failing a healthy pipeline.)
  V2 (theory arm): CONSISTENT iff |dP/P|_A <= max(2 x linear_pred(z), 1%)
      for every k in range at z=0 and z=1;
      TENSION iff any |dP/P|_A > 5%; else INCONCLUSIVE.

Emits D5_RUN_VERDICT.json and d5_pk_comparison.png.
"""
import json, glob, datetime
import numpy as np

RUNS = "../runs"
KMIN, KMAX = 0.05, 2.5

def load_pk(arm):
    out = {}
    for f in sorted(glob.glob(f"{RUNS}/{arm}/*delta.dat")):
        with open(f, errors='replace') as fh:
            zlines = [l for l in fh.readlines() if l.startswith('# redshift')]
        if not zlines:
            continue
        z = round(float(zlines[0].split('=')[1]), 3)
        d = np.loadtxt(f)
        out[z] = d[d[:, 4] > 0]   # occupied bins only
    return out

def main():
    params = json.load(open("../derivation/D5_MG_PARAMETERS.json"))
    lin = params["linear_predictions"]

    pk = {arm: load_pk(arm) for arm in ["lcdm", "armA", "armB"]}
    zsel = [z for z in (0.0, 1.0) if z in pk["lcdm"] and z in pk["armA"] and z in pk["armB"]]
    print("verdict redshifts:", zsel)

    results = {
        "protocol": "PREREG_D5_MG_EVOLUTION.md",
        "analysis_generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "k_range_hmpc": [KMIN, KMAX],
        "config": "reduced-resolution sanity (see prereg sec. 4)",
        "arms": {}, "verdicts": {},
    }

    for z in zsel:
        base_k, base_p = pk["lcdm"][z][:, 0], pk["lcdm"][z][:, 1]
        for arm in ["armA", "armB"]:
            ks, ps = pk[arm][z][:, 0], pk[arm][z][:, 1]
            ratio = ps / np.interp(ks, base_k, base_p)   # identical grids -> exact
            sel = (ks >= KMIN) & (ks <= KMAX)
            results["arms"].setdefault(arm, {})[f"z={z}"] = {
                "k_hmpc": ks[sel].tolist(),
                "dP_over_P": (ratio[sel] - 1.0).tolist(),
            }

    # ---- V1 ----
    v1 = None; v1_detail = None
    for z in zsel:
        if abs(z) < 0.05:
            d = results["arms"]["armB"][f"z={z}"]
            mask = np.array(d["k_hmpc"]) <= 0.2
            vals = np.array(d["dP_over_P"])[mask]
            med = float(np.median(vals))
            v1 = bool(mask.any() and med >= 0.05)
            v1_detail = {"median_dPdP_k_le_0.2": med,
                         "n_bins": int(mask.sum()),
                         "predicted": lin["armB_dP_over_P_z0"]}
    results["verdicts"]["V1_pipeline_sensitivity_PASS"] = v1
    results["verdicts"]["V1_detail"] = v1_detail

    # ---- V2 ----
    worst = {"value": -1.0, "k": None, "z": None}
    consistent, tension = True, False
    for z in zsel:
        lp = lin["armA_dP_over_P_z0"] if abs(z) < 0.05 else lin["armA_dP_over_P_z1"]
        d = results["arms"]["armA"][f"z={z}"]
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
    results["verdicts"]["V2_note"] = ("bounds: max(2*linear, 1%) per bin; TENSION threshold 5%")
    results["verdicts"]["linear_predictions"] = lin

    if v1 is False:
        results["verdicts"]["FINAL"] = "ABORT (pipeline insensitive; no D5 claim)"
    elif results["verdicts"]["V2_verdict"] == "CONSISTENT":
        results["verdicts"]["FINAL"] = ("CONSISTENT at reduced resolution "
            "(pipeline validated end-to-end; full validation config remains boundable)")
    else:
        results["verdicts"]["FINAL"] = results["verdicts"]["V2_verdict"] + " (see V2)"

    with open("D5_RUN_VERDICT.json", "w") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results["verdicts"], indent=2))

    # ---- plot ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, len(zsel), figsize=(6 * len(zsel), 4.5), squeeze=False)
        for ax, z in zip(axes[0], zsel):
            for arm, color, lbl in [("armA", "tab:blue", "Arm A (alpha=1, theory)"),
                                    ("armB", "tab:red", "Arm B (alpha=0.01, control)")]:
                d = results["arms"][arm][f"z={z}"]
                ax.plot(d["k_hmpc"], 100 * np.array(d["dP_over_P"]),
                        color=color, lw=1.2, label=lbl)
            lp = lin["armA_dP_over_P_z0"] if abs(z) < 0.05 else lin["armA_dP_over_P_z1"]
            ax.axhline(100 * lp, color="tab:blue", ls=":", lw=1, label="linear pred (A)")
            ax.axhline(100 * max(2 * lp, 0.01), color="gray", ls="--", lw=0.8, label="V2 bound")
            ax.axhline(0, color="k", lw=0.5)
            ax.set_xscale('log')
            ax.set_xlabel("k [h/Mpc]")
            ax.set_ylabel("P_arm/P_LCDM - 1  [%]")
            ax.set_title(f"z = {z}")
            ax.legend(fontsize=8)
        fig.suptitle("D5: MG-evolution parametrised runs vs LCDM (identical ICs)", y=1.02)
        fig.tight_layout()
        fig.savefig("d5_pk_comparison.png", dpi=130, bbox_inches="tight")
        print("plot -> d5_pk_comparison.png")
    except Exception as e:
        print("plot skipped:", e)

if __name__ == "__main__":
    main()
