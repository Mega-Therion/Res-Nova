#!/usr/bin/env python3
"""
EXACT-PIPELINE RECONSTRUCTION attempt: close the [O] validation gap between
A0_ESTIMATE.json's legacy a0 = 1.1070467107089318e-10 (mu_dual era) and the
reproduction harness's 9.29e-11.

The missing ingredient per A0_MEASUREMENT.json's method note: "per-galaxy published
SPARC distance + inclination errors". This script adds exactly those as per-galaxy
Gaussian priors, marginalized on small per-galaxy grids, on top of the EXACT method of
sparc_a0_reextract_std.py (same Yd/Yb/fd grid, same Gaussian priors, same a0 profile
likelihood + parabola refinement, same 500x bootstrap over galaxies, seed 42):

  distance prior:   f_D = D/D_pub ~ N(1, sigma_D/D_pub); R scales by f_D
                    (gbar = V_b^2 / (f_D * R)), velocities unaffected.
  inclination prior: i ~ N(i_pub, sigma_i); SPARC's V_obs is deprojected with i_pub,
                    so V_circ_true = V_obs * sin(i_pub)/sin(i) (V_err scaled likewise).

Per-galaxy grid: f_D in {1-s, 1, 1+s}, i in {i_pub-sigma_i, i_pub, i_pub+sigma_i}
(9 cells/galaxy, s = sigma_D/D_pub clipped to <= 0.5), each cell carrying its prior chi2.
Master table: /tmp/sparc_meta.csv (columns survey,galaxy,distance_mpc,e_distance_mpc,
inc_deg,e_inc_deg; fetched 2026-09-16 by the gap-investigation worker; spot-checked
against SPARC Table 1 published values).

HONEST FRAMING: the original generating script's exact optimizer is undocumented; what
is documented is the prior set. This script tests whether the documented prior set
REPRODUCES the legacy value. Verdicts: "reproduced" if the legacy value falls inside
the bootstrap 68% window; "bracketed" if the shift moves toward it by > half the gap;
otherwise "not closable with the documented ingredients" — the gap would then be
re-scoped to the optimizer, not the priors.
"""
import csv as csvmod
import glob, json, math, sys
from pathlib import Path
import numpy as np

KPC, KMS = 3.085677581491367e19, 1000.0
YD = np.linspace(0.25, 1.75, 16); YB = np.linspace(0.25, 1.75, 16); FD = np.linspace(0.85, 1.15, 13)
A0_GRID = np.linspace(0.5e-10, 2.5e-10, 41)

def mu_dual_close(gb, a0):
    gb = np.maximum(gb, 1e-30)
    return gb*(0.5 + np.sqrt(0.25 + a0/gb))

def load_meta(path):
    meta = {}
    for row in csvmod.DictReader(open(path)):
        meta[row["galaxy"]] = (float(row["distance_mpc"]), float(row["e_distance_mpc"]),
                               float(row["inc_deg"]), float(row["e_inc_deg"]))
    return meta

def prep(fp, meta):
    name = Path(fp).name.replace("_rotmod.dat", "")
    if name not in meta: return None
    D_pub, sD, i_pub, si = meta[name]
    rows = []
    for line in open(fp):
        if line.startswith('#') or not line.strip(): continue
        p = line.split()
        if len(p) >= 6:
            try: rows.append([float(x) for x in p[:6]])
            except ValueError: continue
    g = np.array(rows)
    if len(g) < 3: return None
    rad, vobs, verr, vgas, vdisk, vbulge = g[:,0],g[:,1],g[:,2],g[:,3],g[:,4],g[:,5]
    verr = np.maximum(verr, 1.0); r_m = rad*KPC
    A = (np.abs(vgas)*vgas)*(KMS**2); Dsk = (np.abs(vdisk)*vdisk)*(KMS**2); B = (np.abs(vbulge)*vbulge)*(KMS**2)
    hasb = np.max(np.abs(vbulge)) > 0
    yb_eff = YB if hasb else np.array([0.7])
    # axis layout: 0=Yd(16), 1=Yb(16 or 1), 2=fd(13), 3=fD(3), 4=i(3), 5=npts
    s = min(sD/D_pub, 0.5) if D_pub > 0 else 0.0
    fDs = np.array([1.0-s, 1.0, 1.0+s])
    i_g = np.clip(np.array([i_pub-si, i_pub, i_pub+si]), 10.0, 89.99)
    sinratio = math.sin(math.radians(i_pub)) / np.sin(np.radians(i_g))   # scale on V_obs (axis 4)
    s_norm = max(sD/D_pub if D_pub > 0 else 0.0, 1e-6)
    pri_di = ((fDs-1.0)/s_norm)[:,None]**2 + ((i_g-i_pub)/max(si,1e-6))[None,:]**2   # (3 fD, 3 i)

    vb2 = (A[None,None,None,None,None,:]
           + YD[:,None,None,None,None,None]*Dsk[None,None,None,None,None,:]
           + yb_eff[None,:,None,None,None,None]*B[None,None,None,None,None,:])       # (16,yb,1,1,1,n)
    r_eff = r_m[None,None,None,None,None,:] * fDs[None,None,None,:,None,None]           # (1,1,1,3,1,n)
    gbar = vb2 / (FD[None,None,:,None,None,None] * np.maximum(r_eff,1e16))           # (16,yb,13,3,1,n)
    vobs_eff = vobs[None,None,None,None,None,:] * sinratio[None,None,None,None,:,None]  # (1,1,1,1,3,n)
    verr_eff = verr[None,None,None,None,None,:] * sinratio[None,None,None,None,:,None]
    pri = ((YD[:,None,None]-0.5)/0.125)**2 + ((FD[None,None,:]-1.0)/0.10)**2          # (16,1,13)
    if hasb: pri = pri + ((yb_eff[None,:,None]-0.7)/0.175)**2
    pri = pri[...,None,None] + pri_di[None,None,None,:,:]                            # (16,yb,13,3,3)
    return (vobs_eff, verr_eff, r_eff, gbar, pri)

def fit(prof):
    tot = prof.sum(axis=0); i = int(np.argmin(tot))
    lo, hi = max(0,i-4), min(len(A0_GRID), i+5)
    c = np.polyfit(A0_GRID[lo:hi], tot[lo:hi], 2)
    return -c[1]/(2*c[0])

def main(sparc_dir, meta_path):
    meta = load_meta(meta_path)
    files = sorted(glob.glob(sparc_dir + '/*_rotmod.dat'))
    assert len(files) == 175, f"expected 175 SPARC files, got {len(files)}"
    gal = [p for p in (prep(f, meta) for f in files) if p is not None]
    print(f"galaxies: {len(gal)}, points: {int(sum(p[0].shape[-1] for p in gal))}", flush=True)
    prof = np.zeros((len(gal), len(A0_GRID)))
    for gi,(vobs_eff,verr_eff,r_eff,gbar,pri) in enumerate(gal):
        for ai,a0 in enumerate(A0_GRID):
            g = mu_dual_close(gbar, a0)
            fdR = FD[None,None,:,None,None,None] * r_eff                # (1,1,13,3,1,n)
            vp = np.sqrt(np.maximum(g*fdR, 0))/KMS                     # (16,yb,13,3,1,n)
            c2d = np.minimum(((vobs_eff-vp)/verr_eff)**2, 1e6).sum(axis=-1)  # (16,yb,13,3,3)
            prof[gi,ai] = (c2d + pri).min()
        if (gi+1) % 25 == 0: print(f"  galaxy {gi+1}/{len(gal)}", flush=True)
    a0 = fit(prof)
    rng = np.random.default_rng(42); boots = [fit(prof[rng.integers(0,len(prof),len(prof))]) for _ in range(500)]
    b = np.array(boots); lo16, hi84 = np.percentile(b,[16,84])
    res = {"generated": "2026-09-16", "method": "mu_dual harness of sparc_a0_reextract_std.py + per-galaxy "
           "SPARC distance+inclination Gaussian priors (3x3 marginalized grids), targeting the legacy "
           "A0_ESTIMATE 1.1070467107089318e-10",
           "n_galaxies": len(gal), "a0_best": float(a0),
           "bootstrap_median": float(np.median(b)), "bootstrap_68": [float(lo16), float(hi84)],
           "targets": {"A0_ESTIMATE": 1.1070467107089318e-10, "A0_MEASUREMENT": 1.1162688655613144e-10,
                        "harness_without_DI_priors": 9.285e-11}}
    print(f"a0 = {a0:.4e}, bootstrap 68% [{lo16:.4e}, {hi84:.4e}]", flush=True)
    return res

if __name__ == "__main__":
    res = main(sys.argv[1] if len(sys.argv)>1 else '/tmp/sparc_data',
               sys.argv[2] if len(sys.argv)>2 else '/tmp/sparc_meta.csv')
    dest = Path(__file__).parent / 'A0_PIPELINE_RECONSTRUCTION_2026-09-16.json'
    json.dump(res, open(dest, 'w'), indent=2)
    print("written:", dest)
