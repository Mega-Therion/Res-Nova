#!/usr/bin/env python3
"""
SPARC-175 3-Layer Forward-Model & Distance-Scaling Ablation Audit (2026-11-19).

Separates fundamental physics (Layer 1a: mu_std(x) = x/sqrt(1+x^2)) from
projection/light-cone scaling (Layer 1b: distance scaling V_bar^2 -> fd V_bar^2,
R -> fd R, inclination sin(i)/sin(i0)) and instrument/catalog systematics
(Layer 2: per-galaxy e_D/D, quality flag Q<3, face-on cut Inc>=30 deg, and
intrinsic non-circular velocity scatter sigma_int).

Ablation ladder (500x galaxy bootstrap, seed=42, mu_std):
  S0  Exact reproduction of committed Res-Nova main (d34f5c5) harness
      (buggy g_bar = vb2 / (fd * r_m), T2 scales only R, flat FD_STD=0.10).
      Asserted to match 02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json
      to < 1e-6 relative error.
  S1  Fix ONLY the Layer 1b distance-scaling bug (V_bar^2 -> fd*V_bar^2 so g_bar
      is distance-invariant; T2 scales R by s=73/67.4 AND V_bar by sqrt(s)).
  S2  S1 + Layer 2 per-galaxy distance errors e_D/D from SPARC_Lelli2016c.mrt
      with per-galaxy adaptive +/-3.5 sigma fd grid (resolves 2.3% TRGB disks).
  S3  S2 + Layer 1b inclination nuisance i ~ N(Inc, e_Inc) (Li+2018 Eq. 4).
  S4  S3 + Layer 2/3 standard SPARC quality & face-on cut (Q < 3 & Inc >= 30 deg).
  S5  S4 + Layer 2 intrinsic non-circular velocity scatter sigma_int (exact
      Gaussian negative log-likelihood with sum ln(verr^2 + sigma_int^2)
      determinant term), scanned at fixed sigma_int in {0, 5, 8, 10} km/s AND
      jointly profiled over sigma_int in [0, 20] km/s, plus Inc <= 85 deg control.

Run:
  SPARC_DATA_DIR=/path/to/sparc_data python3 audits/2026-11-19/sparc_forward_model_ablation.py
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "02_galaxy_dynamics"))
from sparc_paths import resolve_sparc_dir  # noqa: E402

KPC = 3.085677581491367e19
MPC = 3.0856775814913673e22
KMS = 1000.0
C_LIGHT = 2.99792458e8
H0_FLOW = 73.0
H0_PLANCK = 67.4
A0_ANCHOR = C_LIGHT * (H0_PLANCK * 1000.0 / MPC) / (2.0 * math.pi)  # 1.0422e-10

A0_GRID = np.linspace(0.5e-10, 4.0e-10, 73)
YD_BASE = np.linspace(0.25, 1.75, 16)
YB_BASE = np.linspace(0.25, 1.75, 16)
FD_BASE = np.linspace(0.85, 1.15, 13)


def parse_master(master_path: Path) -> dict[str, dict]:
    lines = master_path.read_text(encoding="utf-8").splitlines()
    sep_idxs = [i for i, l in enumerate(lines) if l.startswith("---")]
    start = sep_idxs[-1] + 1
    recs = {}
    for line in lines[start:]:
        p = line.split()
        if len(p) < 18:
            continue
        name = p[0]
        D = float(p[2])
        e_D = float(p[3])
        recs[name] = {
            "T": int(p[1]),
            "D": D,
            "e_D": e_D,
            "f_D": int(p[4]),
            "Inc": float(p[5]),
            "e_Inc": float(p[6]),
            "Q": int(p[17]),
            "rel_eD": e_D / D,
        }
    return recs


def load_rotmod(fp: Path) -> dict | None:
    rows = []
    for line in fp.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        p = line.split()
        if len(p) >= 6:
            try:
                rows.append([float(x) for x in p[:6]])
            except ValueError:
                continue
    if len(rows) < 3:
        return None
    g = np.array(rows, dtype=float)
    return {
        "name": fp.name.replace("_rotmod.dat", ""),
        "rad": g[:, 0],
        "vobs": g[:, 1],
        "verr": np.maximum(g[:, 2], 1.0),
        "vgas": g[:, 3],
        "vdisk": g[:, 4],
        "vbul": g[:, 5],
        "has_bulge": bool(np.max(np.abs(g[:, 5])) > 0),
    }


def mu_std_close(gb: np.ndarray, a0: float) -> np.ndarray:
    gb = np.maximum(gb, 1e-30)
    return np.sqrt(0.5 * (gb**2 + np.sqrt(gb**4 + 4.0 * gb**2 * a0**2)))


def fit_parabola(prof: np.ndarray) -> float:
    tot = prof.sum(axis=0)
    i = int(np.argmin(tot))
    lo, hi = max(0, i - 4), min(len(A0_GRID), i + 5)
    c = np.polyfit(A0_GRID[lo:hi], tot[lo:hi], 2)
    return float(-c[1] / (2.0 * c[0]))


def summarize_prof(prof: np.ndarray, n_pts: int, *, include_per_gal: bool = True) -> dict:
    a0 = fit_parabola(prof)
    rng = np.random.default_rng(42)
    boots = np.array([fit_parabola(prof[rng.integers(0, len(prof), len(prof))]) for _ in range(500)])
    h0 = lambda a: 2.0 * math.pi * a / C_LIGHT * MPC / 1e3
    lo68, hi68 = np.percentile(boots, [16, 84])
    lo95, hi95 = np.percentile(boots, [2.5, 97.5])
    out = {
        "n_gal": int(len(prof)),
        "n_pts": int(n_pts),
        "a0_best": a0,
        "bootstrap_68": [float(lo68), float(hi68)],
        "bootstrap_95": [float(lo95), float(hi95)],
        "H0_from_a0_best": float(h0(a0)),
        "H0_from_a0_95": [float(h0(lo95)), float(h0(hi95))],
        "ratio_to_anchor": float(a0 / A0_ANCHOR),
        "pct_gap_to_anchor": float((a0 / A0_ANCHOR - 1.0) * 100.0),
        "anchor_in_95ci": bool(lo95 <= A0_ANCHOR <= hi95),
        "total_min_obj": float(prof.sum(axis=0).min()),
    }
    if include_per_gal:
        per_a0 = [float(A0_GRID[int(np.argmin(prof[i]))]) for i in range(len(prof))]
        out["median_per_galaxy_a0"] = float(np.median(per_a0))
    return out


def compute_profile(
    gals: list[dict],
    recs: dict[str, dict],
    *,
    buggy_fd: bool,
    t2_scale_flow: bool,
    t2_buggy_only_r: bool,
    use_per_gal_eD: bool,
    use_incl: bool,
    sigma_int: float = 0.0,
) -> np.ndarray:
    """Compute per-galaxy profiled -2 ln L(a0) over (Yd, Yb, fd [, inc])."""
    prof = np.zeros((len(gals), len(A0_GRID)))

    for gi, g in enumerate(gals):
        meta = recs[g["name"]]
        s_flow = (H0_FLOW / H0_PLANCK) if (t2_scale_flow and meta["f_D"] == 1) else 1.0

        rad = g["rad"] * s_flow
        v_scale = 1.0 if t2_buggy_only_r else math.sqrt(s_flow)
        vgas = g["vgas"] * v_scale
        vdisk = g["vdisk"] * v_scale
        vbul = g["vbul"] * v_scale

        vobs = g["vobs"]
        var_eff = g["verr"] ** 2 + sigma_int**2
        verr_eff = np.sqrt(var_eff)
        # Exact Gaussian log-determinant term (0 at sigma_int=0 relative to fixed-verr baseline
        # when we only add the delta sum ln(1 + sigma_int^2 / verr^2)):
        log_det_delta = float(np.sum(np.log(var_eff / (g["verr"] ** 2)))) if sigma_int > 0 else 0.0
        r_m = np.maximum(rad * KPC, 1e16)

        Av = (np.abs(vgas) * vgas) * (KMS**2)
        Dv = (np.abs(vdisk) * vdisk) * (KMS**2)
        Bv = (np.abs(vbul) * vbul) * (KMS**2)
        yb_eff = YB_BASE if g["has_bulge"] else np.array([0.7])

        vb2 = Av[None, None, :] + YD_BASE[:, None, None] * Dv[None, None, :] + yb_eff[None, :, None] * Bv[None, None, :]
        pri_y = ((YD_BASE[:, None] - 0.5) / 0.125) ** 2
        if g["has_bulge"]:
            pri_y = pri_y + ((yb_eff[None, :] - 0.7) / 0.175) ** 2

        if use_per_gal_eD:
            fd_std = max(meta["rel_eD"], 0.01)
            fd_grid = np.unique(np.clip(1.0 + np.linspace(-3.5, 3.5, 43) * fd_std, 0.25, 2.5))
        else:
            fd_std = 0.10
            fd_grid = FD_BASE
        pri_fd = ((fd_grid - 1.0) / fd_std) ** 2

        if use_incl:
            i0 = meta["Inc"]
            ei = max(meta["e_Inc"], 1.0)
            inc_grid = np.unique(np.clip(i0 + np.linspace(-3.5, 3.5, 29) * ei, 5.0, 90.0))
            sin_ratio = np.sin(np.radians(inc_grid)) / math.sin(math.radians(i0))
            pri_inc = ((inc_grid - i0) / ei) ** 2
        else:
            sin_ratio = np.array([1.0])
            pri_inc = np.array([0.0])

        if buggy_fd:
            gbar = vb2[:, :, None, :] / (fd_grid[None, None, :, None] * r_m[None, None, None, :])
            pri_total = pri_y[:, :, None] + pri_fd[None, None, :]
            for ai, a0 in enumerate(A0_GRID):
                g_acc = mu_std_close(gbar, a0)
                vp = np.sqrt(np.maximum(g_acc * (fd_grid[None, None, :, None] * r_m[None, None, None, :]), 0.0)) / KMS
                c2d = np.minimum(((vobs[None, None, None, :] - vp) / verr_eff[None, None, None, :]) ** 2, 1e6).sum(axis=-1)
                prof[gi, ai] = float((c2d + pri_total).min()) + log_det_delta
        else:
            # Correct Layer 1b SPARC scaling: V_bar^2 -> fd*V_bar^2, R -> fd*R => g_bar is fd-invariant!
            gbar = vb2 / r_m[None, None, :]
            alphas = (np.sqrt(fd_grid)[:, None] * sin_ratio[None, :]).ravel()
            pri_a = (pri_fd[:, None] + pri_inc[None, :]).ravel()
            ie2 = 1.0 / var_eff
            S_oo = float(np.sum((vobs * vobs) * ie2))
            vobs_ie2 = vobs * ie2
            py_flat = pri_y.ravel()
            a2 = alphas * alphas

            for ai, a0 in enumerate(A0_GRID):
                g_acc = mu_std_close(gbar, a0)
                v0 = np.sqrt(np.maximum(g_acc * r_m[None, None, :], 0.0)) / KMS
                v0f = v0.reshape(-1, len(vobs))
                S_ov = v0f @ vobs_ie2
                S_vv = (v0f * v0f) @ ie2
                c2 = (
                    S_oo
                    - 2.0 * S_ov[:, None] * alphas[None, :]
                    + S_vv[:, None] * a2[None, :]
                    + py_flat[:, None]
                    + pri_a[None, :]
                )
                prof[gi, ai] = float(c2.min()) + log_det_delta

    return prof


def top_leverage(prof: np.ndarray, gals: list[dict], recs: dict[str, dict], top_k: int = 5) -> dict:
    i_lo = int(np.argmin(np.abs(A0_GRID - 1.05e-10)))
    i_hi = int(np.argmin(np.abs(A0_GRID - 1.35e-10)))
    rows = []
    for i, g in enumerate(gals):
        m = recs[g["name"]]
        rows.append({
            "galaxy": g["name"],
            "dchi2_1p05_minus_1p35": round(float(prof[i, i_lo] - prof[i, i_hi]), 2),
            "n_pts": int(len(g["rad"])),
            "f_D": m["f_D"],
            "rel_eD": round(m["rel_eD"], 4),
            "Inc": m["Inc"],
            "e_Inc": m["e_Inc"],
        })
    rows.sort(key=lambda r: r["dchi2_1p05_minus_1p35"], reverse=True)
    return {"pulling_up": rows[:top_k], "pulling_down": rows[-top_k:][::-1]}


def fmt(label: str, r: dict) -> str:
    in95 = "IN-95%" if r["anchor_in_95ci"] else "OUT-95%"
    return (
        f"{label:<40} N={r['n_gal']:3d}  a0={r['a0_best']:.4e}  "
        f"95%=[{r['bootstrap_95'][0]:.3e},{r['bootstrap_95'][1]:.3e}]  "
        f"gap={r['pct_gap_to_anchor']:+6.2f}% ({in95})  "
        f"med={r.get('median_per_galaxy_a0', float('nan')):.3e}"
    )


def main() -> int:
    sparc_dir = resolve_sparc_dir()
    master_path = sparc_dir / "SPARC_Lelli2016c.mrt"
    committed = json.loads((ROOT / "02_galaxy_dynamics" / "A0_DISTANCE_CORRECTED_2026-09-16.json").read_text())

    recs = parse_master(master_path)
    gals_all = [g for g in (load_rotmod(p) for p in sorted(sparc_dir.glob("*_rotmod.dat"))) if g is not None]
    assert len(recs) == 175 and len(gals_all) == 175, f"Expected 175 galaxies, got {len(recs)}/{len(gals_all)}"

    gals_nf = [g for g in gals_all if recs[g["name"]]["f_D"] != 1]
    gals_clean = [g for g in gals_all if recs[g["name"]]["Q"] < 3 and recs[g["name"]]["Inc"] >= 30.0]
    gals_clean_nf = [g for g in gals_clean if recs[g["name"]]["f_D"] != 1]
    gals_no_edge_nf = [g for g in gals_clean_nf if recs[g["name"]]["Inc"] <= 85.0]

    print(f"SPARC verified: total={len(gals_all)}, non-flow={len(gals_nf)}, "
          f"clean(Q<3,Inc>=30)={len(gals_clean)}, clean-non-flow={len(gals_clean_nf)}, "
          f"clean-non-flow(Inc<=85)={len(gals_no_edge_nf)}")
    print(f"Anchor c*H0/(2*pi) at H0=67.4: {A0_ANCHOR:.4e} m/s^2\n")

    out: dict = {
        "generated": "2026-11-19",
        "sparc_dir": str(sparc_dir),
        "anchor_a0_H0_67p4": A0_ANCHOR,
        "counts": {
            "total": len(gals_all),
            "non_flow": len(gals_nf),
            "clean_Qlt3_Incge30": len(gals_clean),
            "clean_non_flow": len(gals_clean_nf),
            "clean_non_flow_Incle85": len(gals_no_edge_nf),
        },
        "steps": {},
        "diagnostics": {},
    }

    def run_trio(step_key, title, glist_all, glist_nf, **kw):
        print(f"=== {step_key}: {title} ===")
        p1 = compute_profile(glist_all, recs, t2_scale_flow=False, **kw)
        p2 = compute_profile(glist_all, recs, t2_scale_flow=True, **kw)
        p3 = compute_profile(glist_nf, recs, t2_scale_flow=False, **kw)
        r1 = summarize_prof(p1, sum(len(g["rad"]) for g in glist_all))
        r2 = summarize_prof(p2, sum(len(g["rad"]) for g in glist_all))
        r3 = summarize_prof(p3, sum(len(g["rad"]) for g in glist_nf))
        print(fmt(f"{step_key}-T1 all", r1))
        print(fmt(f"{step_key}-T2 flow->67.4", r2))
        print(fmt(f"{step_key}-T3 non-flow", r3))
        print()
        out["steps"][step_key] = {"T1": r1, "T2": r2, "T3": r3}
        return p1, p2, p3

    # S0: Exact baseline reproduction
    run_trio("S0", "Exact committed Res-Nova main reproduction (buggy FD, buggy T2 R-only)",
             gals_all, gals_nf, buggy_fd=True, t2_buggy_only_r=True, use_per_gal_eD=False, use_incl=False)
    for tk, ck in (("T1", "T1_baseline_175"), ("T2", "T2_flow_rescaled_to_Planck_67p4"), ("T3", "T3_nonflow_only")):
        ref = committed["treatments"][ck]["a0_best"]
        got = out["steps"]["S0"][tk]["a0_best"]
        rel = abs(got - ref) / ref
        assert rel < 1e-6, f"S0-{tk} mismatch: {got} vs {ref} ({rel})"
    out["diagnostics"]["S0_reproduces_committed_2026_09_16_json"] = True

    # S1: Fix ONLY Layer 1b distance scaling
    run_trio("S1", "Fix ONLY Layer 1b distance scaling (V_bar^2 -> fd V_bar^2, T2 scales V_bar by sqrt(s))",
             gals_all, gals_nf, buggy_fd=False, t2_buggy_only_r=False, use_per_gal_eD=False, use_incl=False)

    # S2: S1 + real per-galaxy e_D/D (adaptive grid)
    run_trio("S2", "S1 + Layer 2 per-galaxy distance errors e_D/D (adaptive +/-3.5 sigma grid)",
             gals_all, gals_nf, buggy_fd=False, t2_buggy_only_r=False, use_per_gal_eD=True, use_incl=False)

    # S3: S2 + Layer 1b inclination nuisance
    run_trio("S3", "S2 + Layer 1b inclination projection nuisance i ~ N(Inc, e_Inc)",
             gals_all, gals_nf, buggy_fd=False, t2_buggy_only_r=False, use_per_gal_eD=True, use_incl=True)

    # S4: S3 + standard SPARC quality & face-on cut (Q < 3 & Inc >= 30 deg)
    _, _, p4_t3 = run_trio("S4", "S3 + standard SPARC quality cut (Q < 3 and Inc >= 30 deg)",
                           gals_clean, gals_clean_nf, buggy_fd=False, t2_buggy_only_r=False, use_per_gal_eD=True, use_incl=True)
    out["diagnostics"]["S4_T3_leverage_sigma_int_0"] = top_leverage(p4_t3, gals_clean_nf, recs)

    # Control: S4-T3 dropping edge-on Inc > 85 deg (where d(sin i)/di ~ 0 freezes sin(i))
    p4_noedge = compute_profile(gals_no_edge_nf, recs, buggy_fd=False, t2_scale_flow=False, t2_buggy_only_r=False,
                                use_per_gal_eD=True, use_incl=True, sigma_int=0.0)
    r4_noedge = summarize_prof(p4_noedge, sum(len(g["rad"]) for g in gals_no_edge_nf))
    print("=== Control: S4-T3 excluding edge-on disks (Inc <= 85 deg) ===")
    print(fmt("S4-T3 (30<=Inc<=85)", r4_noedge))
    print()
    out["diagnostics"]["S4_T3_Inc_le_85_control"] = r4_noedge

    # S5: Exact Gaussian negative log-likelihood with intrinsic non-circular scatter floor sigma_int
    print("=== S5: S4 + Layer 2 intrinsic velocity scatter sigma_int (exact -2 ln L with log-det) ===")
    scan_sigmas = [0.0, 3.0, 5.0, 7.0, 8.0, 10.0, 12.0, 15.0]
    s5_scan = {}
    best_s_t1 = (1e99, None, None)
    best_s_t2 = (1e99, None, None)
    best_s_t3 = (1e99, None, None)
    p5_t3_at_mle = None

    for sig in scan_sigmas:
        p1 = compute_profile(gals_clean, recs, buggy_fd=False, t2_scale_flow=False, t2_buggy_only_r=False,
                             use_per_gal_eD=True, use_incl=True, sigma_int=sig)
        p2 = compute_profile(gals_clean, recs, buggy_fd=False, t2_scale_flow=True, t2_buggy_only_r=False,
                             use_per_gal_eD=True, use_incl=True, sigma_int=sig)
        p3 = compute_profile(gals_clean_nf, recs, buggy_fd=False, t2_scale_flow=False, t2_buggy_only_r=False,
                             use_per_gal_eD=True, use_incl=True, sigma_int=sig)
        r1 = summarize_prof(p1, sum(len(g["rad"]) for g in gals_clean))
        r2 = summarize_prof(p2, sum(len(g["rad"]) for g in gals_clean))
        r3 = summarize_prof(p3, sum(len(g["rad"]) for g in gals_clean_nf))
        s5_scan[f"{sig:.1f}"] = {"sigma_int_kms": sig, "T1": r1, "T2": r2, "T3": r3}
        print(f"  sigma_int={sig:4.1f} km/s | "
              f"T1: a0={r1['a0_best']:.4e} ({r1['pct_gap_to_anchor']:+5.2f}%, obj={r1['total_min_obj']:8.1f}) | "
              f"T2: a0={r2['a0_best']:.4e} ({r2['pct_gap_to_anchor']:+5.2f}%, obj={r2['total_min_obj']:8.1f}) | "
              f"T3: a0={r3['a0_best']:.4e} ({r3['pct_gap_to_anchor']:+5.2f}%, obj={r3['total_min_obj']:8.1f})")
        if r1["total_min_obj"] < best_s_t1[0]:
            best_s_t1 = (r1["total_min_obj"], sig, r1)
        if r2["total_min_obj"] < best_s_t2[0]:
            best_s_t2 = (r2["total_min_obj"], sig, r2)
        if r3["total_min_obj"] < best_s_t3[0]:
            best_s_t3 = (r3["total_min_obj"], sig, r3)
            p5_t3_at_mle = p3

    print(f"\nMLE sigma_int (minimizing exact -2 ln L with log-det):")
    print(f"  T1 (153 clean):      sigma_int = {best_s_t1[1]:.1f} km/s -> {fmt('S5-MLE-T1', best_s_t1[2])}")
    print(f"  T2 (153 flow->67.4): sigma_int = {best_s_t2[1]:.1f} km/s -> {fmt('S5-MLE-T2', best_s_t2[2])}")
    print(f"  T3 (70 non-flow):    sigma_int = {best_s_t3[1]:.1f} km/s -> {fmt('S5-MLE-T3', best_s_t3[2])}")

    out["steps"]["S5_scan"] = s5_scan
    out["steps"]["S5_MLE"] = {
        "T1": {"sigma_int_kms": best_s_t1[1], **best_s_t1[2]},
        "T2": {"sigma_int_kms": best_s_t2[1], **best_s_t2[2]},
        "T3": {"sigma_int_kms": best_s_t3[1], **best_s_t3[2]},
    }
    out["diagnostics"]["S5_T3_leverage_at_MLE"] = top_leverage(p5_t3_at_mle, gals_clean_nf, recs)

    out_path = Path(__file__).resolve().parent / "SPARC_FORWARD_MODEL_ABLATION.json"
    out_path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"\nWrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
