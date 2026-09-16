#!/usr/bin/env python3
"""
Obligation 5 verifier (post-correction) — distance-corrected a0 re-extraction.

The PR #59 correction established: SPARC's Hubble-flow distances (f_D = 1,
97/175 galaxies) assume H0 = 73 km/s/Mpc (SPARC_Lelli2016c.mrt, note 2), so the
frozen a0 window carries the ladder's H0 inside it, and the window -> H0
inversion is circular. This script performs the correction's own prescription:

  T1  baseline: all 175 galaxies as-is  -> must reproduce the frozen window
      (validation of the harness against A0_REEXTRACTION_3MU_2026-09-16.json).
  T2  flow galaxies rescaled to the Planck H0 scale: D -> D * (73/67.4), i.e.
      radii x (73/67.4), accelerations x (67.4/73) for those galaxies only;
      non-flow galaxies untouched.
  T3  non-flow galaxies only (f_D in {2,3,4,5}: TRGB, Cepheids, Ursa Major
      cluster, SNe light curves — 78 galaxies): no H0=73 flow assumption at
      all. Residual ladder-calibration covariance remains (stated in the doc).

For each treatment: mu_std only, identical harness as
sparc_a0_reextract_3mu.py (grids, priors, profile likelihood, parabola
refinement, 500x bootstrap seed 42), reporting 68% AND 95% intervals, plus
the inverted H0 = 2*pi*a0/c with its 95% interval.

Checks (exit 0 iff all pass):
  C1  closure/ordering checks (module.verify_closures).
  C2  master-table provenance: 175 galaxies, 97 flow, 78 non-flow; rotmod
      header distances agree with the table.
  C3  T1 reproduces the frozen window (a0_best and 68% interval).
  C4  T2 shifts a0 DOWN (flow fraction rescaled to the smaller Planck H0).
  C5  all 95% intervals are finite and ordered.
"""
import glob
import json
import re
import sys
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "02_galaxy_dynamics"))
import sparc_a0_reextract_3mu as M  # the frozen harness: prep/fit/A0_GRID/mu_close

SPARC_DIR = "/tmp/sparc_data"
MASTER = Path("/tmp/sparc_master.mrt")
H0_FLOW, H0_PLANCK = 73.0, 67.4
MPC, KMS = 3.0856775814913673e22, 1000.0
C_LIGHT = 2.99792458e8

FAILURES = []


def note(ok, name, detail=""):
    print(f"{name}: {'PASS' if ok else 'FAIL'} {detail}")
    if not ok:
        FAILURES.append(name)


def parse_master():
    recs = {}
    for l in open(MASTER):
        m = re.match(r"^\s*([A-Za-z0-9-]+)\s+(\d+)\s+([0-9.]+)\s+([0-9.]+)\s+(\d+)\s+([0-9.]+)", l)
        if m and float(m.group(6)) > 0:
            recs[m.group(1)] = (float(m.group(3)), int(m.group(5)))
    return recs


def rescaled_copy(files_and_scale, dest):
    """Write rotmod copies with the radius column scaled (exact code path reuse)."""
    dest.mkdir(parents=True, exist_ok=True)
    n = 0
    for fp, s in files_and_scale:
        out = []
        for line in open(fp):
            if line.startswith("#") or not line.strip():
                out.append(line)
                continue
            p = line.split()
            if len(p) >= 6:
                try:
                    p[0] = repr(float(p[0]) * s)
                    out.append(" ".join(p) + "\n")
                    continue
                except ValueError:
                    pass
            out.append(line)
        (dest / fp.split("/")[-1]).write_text("".join(out))
        n += 1
    return n


def run_treatment(files):
    gal = [p for p in (M.prep(f) for f in files) if p is not None]
    prof = np.zeros((len(gal), len(M.A0_GRID)))
    for gi, (vobs, verr, r_m, gbar, pri) in enumerate(gal):
        for ai, a0 in enumerate(M.A0_GRID):
            g = M.mu_close(gbar, a0, "std")
            vp = np.sqrt(np.maximum(g * (M.FD[None, None, :, None] * r_m[None, None, None, :]), 0)) / KMS
            c2d = np.minimum(((vobs[None, None, None, :] - vp) / verr[None, None, None, :]) ** 2, 1e6).sum(axis=-1)
            prof[gi, ai] = (c2d + pri).min()
    a0 = M.fit(prof)
    rng = np.random.default_rng(42)
    boots = np.array([M.fit(prof[rng.integers(0, len(prof), len(prof))]) for _ in range(500)])
    return {
        "n_galaxies": len(gal),
        "n_points": int(sum(len(p[0]) for p in gal)),
        "a0_best": float(a0),
        "bootstrap_68": [float(x) for x in np.percentile(boots, [16, 84])],
        "bootstrap_95": [float(x) for x in np.percentile(boots, [2.5, 97.5])],
    }


def main():
    print("closure and ordering checks:")
    M.verify_closures()
    note(True, "C1 closure/ordering (module checks passed)")

    recs = parse_master()
    n_flow = sum(1 for _, fd in recs.values() if fd == 1)
    n_non = sum(1 for _, fd in recs.values() if fd != 1)
    files = sorted(glob.glob(SPARC_DIR + "/*_rotmod.dat"))
    agree = all(
        abs(recs[f.split("/")[-1].replace("_rotmod.dat", "")][0]
            - float(open(f).readline().split("=")[1].split()[0])) < 0.015
        for f in files)
    note(len(recs) == 175 and len(files) == 175 and n_flow == 97 and n_non == 78 and agree,
         "C2 provenance: 175 galaxies, 97 flow (H0=73), 78 non-flow; distances agree",
         f"flow {n_flow}, non-flow {n_non}")

    # T1: baseline
    t1 = run_treatment(files)

    # T2: flow rescaled to Planck H0 (D -> D * 73/67.4 -> radii x 73/67.4)
    scale = H0_FLOW / H0_PLANCK
    pairs = [(f, scale if recs[f.split("/")[-1].replace("_rotmod.dat", "")][1] == 1 else 1.0)
             for f in files]
    n2 = rescaled_copy(pairs, Path("/tmp/sparc_T2"))
    t2 = run_treatment(sorted(str(p) for p in Path("/tmp/sparc_T2").glob("*_rotmod.dat")))
    note(n2 == 175, "C4a T2 rescaled files written", f"{n2}")

    # T3: non-flow only
    files3 = [f for f in files if recs[f.split("/")[-1].replace("_rotmod.dat", "")][1] != 1]
    t3 = run_treatment(files3)

    # checks C3-C5
    frozen = json.load(open(BASE / "02_galaxy_dynamics/A0_REEXTRACTION_3MU_2026-09-16.json"))["std"]
    d_best = abs(t1["a0_best"] - frozen["a0_best"]) / frozen["a0_best"]
    w = frozen["bootstrap_68"]
    dw = max(abs(t1["bootstrap_68"][0] - w[0]), abs(t1["bootstrap_68"][1] - w[1])) / (w[1] - w[0])
    note(d_best < 0.01 and dw < 0.05,
         "C3 T1 reproduces the frozen window",
         f"a0 {t1['a0_best']:.4e} vs {frozen['a0_best']:.4e} ({d_best:.3%}); 68% window match {dw:.2%}")
    note(t2["a0_best"] < t1["a0_best"],
         "C4 T2 shifts a0 down (Planck-rescaled flow)",
         f"{t1['a0_best']:.4e} -> {t2['a0_best']:.4e} ({t2['a0_best']/t1['a0_best']:.4f})")
    for name, t in (("T1", t1), ("T2", t2), ("T3", t3)):
        lo68, hi68 = t["bootstrap_68"]; lo95, hi95 = t["bootstrap_95"]
        note(0 < lo95 < lo68 < t["a0_best"] < hi68 < hi95,
             f"C5 {name} interval ordering", f"95% [{lo95:.4e}, {hi95:.4e}]")

    # inverted H0 with 95% intervals
    h0 = lambda a: 2 * np.pi * a / C_LIGHT * MPC / 1e3  # 1/s -> km/s/Mpc
    for name, t in (("T1", t1), ("T2", t2), ("T3", t3)):
        t["H0_from_a0_95"] = [float(h0(t["bootstrap_95"][0]) * 1e0), float(h0(t["bootstrap_95"][1]))]
    print()
    print(f"T1 all 175 (as-is):        a0 = {t1['a0_best']:.4e}, 95% [{t1['bootstrap_95'][0]:.4e}, {t1['bootstrap_95'][1]:.4e}]")
    print(f"T2 flow->Planck scale:     a0 = {t2['a0_best']:.4e}, 95% [{t2['bootstrap_95'][0]:.4e}, {t2['bootstrap_95'][1]:.4e}]")
    print(f"T3 non-flow only ({t3['n_galaxies']}):    a0 = {t3['a0_best']:.4e}, 95% [{t3['bootstrap_95'][0]:.4e}, {t3['bootstrap_95'][1]:.4e}]")
    print(f"inverted H0 (95%): T1 [{t1['H0_from_a0_95'][0]:.1f}, {t1['H0_from_a0_95'][1]:.1f}]"
          f"  T2 [{t2['H0_from_a0_95'][0]:.1f}, {t2['H0_from_a0_95'][1]:.1f}]"
          f"  T3 [{t3['H0_from_a0_95'][0]:.1f}, {t3['H0_from_a0_95'][1]:.1f}] km/s/Mpc")

    out = {
        "generated": "2026-09-16",
        "purpose": "Distance-corrected a0 re-extraction (obligation 5, post-PR-59): "
                   "the SPARC Hubble-flow distances (f_D=1, 97/175) assume H0=73 "
                   "(SPARC_Lelli2016c.mrt note 2), so the frozen window's H0 inversion "
                   "is circular. Treatments: T1 baseline (validation), T2 flow "
                   "rescaled to Planck H0 (D x 73/67.4), T3 non-flow galaxies only.",
        "provenance": {"master": "https://astroweb.cwru.edu/SPARC/SPARC_Lelli2016c.mrt",
                        "note2": "f_D=1: Hubble-Flow assuming H0=73 km/s/Mpc with "
                                 "Virgo-centric infall correction; f_D=2 TRGB; 3 Cepheids; "
                                 "4 Ursa Major cluster; 5 SNe light curves",
                        "counts": {"flow_H0_73": 97, "non_flow": 78}},
        "mu": "std (x/sqrt(1+x^2), the live row; battery-passing)",
        "treatments": {"T1_baseline_175": t1, "T2_flow_rescaled_to_Planck_67p4": t2,
                        "T3_nonflow_only": t3},
    }
    dest = BASE / "02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json"
    json.dump(out, open(dest, "w"), indent=2)
    print("written:", dest)

    print()
    print("SUMMARY: distance-corrected re-extraction checks: 8 total,", len(FAILURES), "failures")
    if FAILURES:
        print("FAILED:", ", ".join(FAILURES))
        sys.exit(1)
    print("CIRCULARITY RESOLVED: T3 (non-flow) removes the H0=73 flow assumption;")
    print("its inverted H0 and 95% interval are the honest prediction. Residual")
    print("ladder-calibration covariance is stated in the audit doc.")


if __name__ == "__main__":
    main()
