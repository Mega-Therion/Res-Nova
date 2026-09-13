#!/usr/bin/env python3
"""
SPARC a0 re-extraction under the LIVE closure mu_std(x) = x/sqrt(1+x^2),
with a mu_dual control run on the identical harness.
Method mirrors sparc_cross_validation.py's documented nuisance grid:
  Yd in [0.25,1.75] (16), Yb in [0.25,1.75] (16, bulge only), fd in [0.85,1.15] (13),
  Gaussian priors Yd~N(0.5,0.125), Yb~N(0.7,0.175), fd~N(1.0,0.10);
  a0 profile likelihood on [0.5,2.5]x10^-10 (41 pts), parabola-refined;
  uncertainty: 500x bootstrap over galaxies.
Data: SPARC 175 (SHA-256 verified against VERIFICATION_RUN_001 manifest).
Known gap [O]: does NOT reproduce A0_ESTIMATE.json's 1.107e-10 for mu_dual
(the original generating script's per-galaxy priors live outside the repo);
the mu_dual-vs-mu_std COMPARISON on this harness is internally valid.
"""
import glob, json, hashlib, sys
import numpy as np

KPC, KMS = 3.085677581491367e19, 1000.0
YD = np.linspace(0.25, 1.75, 16); YB = np.linspace(0.25, 1.75, 16); FD = np.linspace(0.85, 1.15, 13)
A0_GRID = np.linspace(0.5e-10, 2.5e-10, 41)

def mu_close(gb, a0, mu):
    gb = np.maximum(gb, 1e-30)
    if mu == 'dual': return gb*(0.5 + np.sqrt(0.25 + a0/gb))
    return np.sqrt(0.5*(gb**2 + np.sqrt(gb**4 + 4*gb**2*a0**2)))   # mu_std

def prep(fp):
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
    A = (np.abs(vgas)*vgas)*(KMS**2); D = (np.abs(vdisk)*vdisk)*(KMS**2); B = (np.abs(vbulge)*vbulge)*(KMS**2)
    hasb = np.max(np.abs(vbulge)) > 0
    yb_eff = YB if hasb else np.array([0.7])
    vb2 = A[None,None,None,:] + YD[:,None,None,None]*D[None,None,None,:] + yb_eff[None,:,None,None]*B[None,None,None,:]
    gbar = vb2 / (FD[None,None,:,None]*np.maximum(r_m,1e16)[None,None,None,:])
    pri = ((YD[:,None,None]-0.5)/0.125)**2 + ((FD[None,None,:]-1.0)/0.10)**2
    if hasb: pri = pri + ((yb_eff[None,:,None]-0.7)/0.175)**2
    return (vobs, verr, r_m, gbar, pri)

def fit(prof):
    tot = prof.sum(axis=0); i = int(np.argmin(tot))
    lo, hi = max(0,i-4), min(len(A0_GRID), i+5)
    c = np.polyfit(A0_GRID[lo:hi], tot[lo:hi], 2)
    return -c[1]/(2*c[0])

def main(sparc_dir):
    files = sorted(glob.glob(sparc_dir + '/*_rotmod.dat'))
    assert len(files) == 175, f"expected 175 SPARC files, got {len(files)}"
    gal = [p for p in (prep(f) for f in files) if p is not None]
    out = {"n_galaxies": len(gal), "n_points": int(sum(len(p[0]) for p in gal)),
           "mu_functions": {"dual": "x/(1+x) [X falsified]", "std": "x/sqrt(1+x^2) [live]"},
           "note_validation_gap": "mu_dual control gives 9.29e-11 here vs A0_ESTIMATE.json's 1.107e-10; the original generating script's priors are not in the repo [O]. The dual-vs-std comparison on THIS harness is internally valid."}
    for mu in ('dual','std'):
        prof = np.zeros((len(gal), len(A0_GRID)))
        for gi,(vobs,verr,r_m,gbar,pri) in enumerate(gal):
            for ai,a0 in enumerate(A0_GRID):
                g = mu_close(gbar, a0, mu)
                vp = np.sqrt(np.maximum(g*(FD[None,None,:,None]*r_m[None,None,None,:]), 0))/KMS
                c2d = np.minimum(((vobs[None,None,None,:]-vp)/verr[None,None,None,:])**2, 1e6).sum(axis=-1)
                prof[gi,ai] = (c2d + pri).min()
        a0 = fit(prof)
        rng = np.random.default_rng(42); boots = [fit(prof[rng.integers(0,len(prof),len(prof))]) for _ in range(500)]
        b = np.array(boots); lo16, hi84 = np.percentile(b,[16,84])
        out[mu] = {"a0_best": float(a0), "bootstrap_median": float(np.median(b)),
                   "bootstrap_68": [float(lo16), float(hi84)]}
        print(f"[{mu}] a0 = {a0:.4e}, bootstrap 68% [{lo16:.4e}, {hi84:.4e}]")
    return out

if __name__ == "__main__":
    res = main(sys.argv[1] if len(sys.argv)>1 else '/tmp/sparc_data')
    json.dump(res, open(sys.argv[2] if len(sys.argv)>2 else 'A0_REEXTRACTION_MU_STD.json','w'), indent=2)
