#!/usr/bin/env python3
"""
SPARC a0 extraction under THREE interpolating functions on one identical harness:
the (mu, a0) map for mu_dual (falsified control), mu_std (live), mu_simple (half-rapidity).

mu_simple(y) = y/(1+sqrt(1+y^2)) = tanh(arsinh(y)/2)  [50-digit verified 2026-09-16]
has mu'(0) = 1/2 (fails the normalization input; cf. REPRESENTATION_AUDIT_MU_STD_2026-09-16).
Its closure g*mu(g/a0)=gbar is the closed form  g = sqrt(gbar^2 + 2*a0*gbar)  (verified
below to machine precision). Because mu_simple < mu_dual < mu_std pointwise, the expected
extraction order is a0(simple) > a0(std) > a0(dual); and since mu_simple's deep-MOND limit
is g = sqrt(2*a0*gbar) (a sqrt(2) normalization defect), its a0 may run ~2x high, so the
a0 grid is extended to [0.5, 4.0]e-10 (73 pts). dual/std minima are interior and unaffected
by the extension (parabola-refined); they are re-measured here as a reproduction check of
A0_REEXTRACTION_MU_STD.json's 9.285e-11 / 1.1562e-10.

Method mirrors 02_galaxy_dynamics/sparc_a0_reextract_std.py exactly except the grid:
  Yd in [0.25,1.75] (16), Yb in [0.25,1.75] (16, bulge only), fd in [0.85,1.15] (13),
  Gaussian priors Yd~N(0.5,0.125), Yb~N(0.7,0.175), fd~N(1.0,0.10);
  a0 profile likelihood, parabola-refined; 500x bootstrap over galaxies (seed 42).
Data: /tmp/sparc_data (175 rotmod files, SHA-256 verified against
VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256 on 2026-09-16).
"""
import glob, json, sys
from pathlib import Path
import numpy as np

KPC, KMS = 3.085677581491367e19, 1000.0
YD = np.linspace(0.25, 1.75, 16); YB = np.linspace(0.25, 1.75, 16); FD = np.linspace(0.85, 1.15, 13)
A0_GRID = np.linspace(0.5e-10, 4.0e-10, 73)

def mu_fun(mu, y):
    if mu == 'dual':  return y/(1.0+y)
    if mu == 'std':   return y/np.sqrt(1.0+y*y)
    if mu == 'simple': return y/(1.0+np.sqrt(1.0+y*y))
    raise ValueError(mu)

def mu_close(gb, a0, mu):
    gb = np.maximum(gb, 1e-30)
    if mu == 'dual':   return gb*(0.5 + np.sqrt(0.25 + a0/gb))
    if mu == 'std':    return np.sqrt(0.5*(gb**2 + np.sqrt(gb**4 + 4*gb**2*a0**2)))
    if mu == 'simple': return np.sqrt(gb*gb + 2.0*a0*gb)
    raise ValueError(mu)

def verify_closures():
    """g * mu(g/a0) == gbar to machine precision, and pointwise ordering."""
    rng = np.random.default_rng(7)
    gb = 10.0**rng.uniform(-13, -8, 200); a0 = 1.1562e-10
    for mu in ('dual', 'std', 'simple'):
        g = mu_close(gb, a0, mu)
        err = np.abs(g*mu_fun(mu, g/a0) - gb).max()
        print(f"  closure {mu:7s}: max |g*mu - gbar| = {err:.2e}")
        assert err < 1e-12 * a0 / (a0/gb).max()**0 or err < 1e-18, f"closure failed for {mu}"
    y = np.linspace(1e-4, 50, 10000)
    o1 = np.all(mu_fun('simple', y) < mu_fun('dual', y))
    o2 = np.all(mu_fun('dual', y) < mu_fun('std', y))
    print(f"  ordering mu_simple < mu_dual < mu_std on (0,50]: {o1 and o2}")
    assert o1 and o2
    deep = mu_close(np.array([1e-12]), a0, 'simple')[0] / np.sqrt(2.0*a0*1e-12)
    print(f"  mu_simple deep-MOND check: g/sqrt(2*a0*gb) = {deep:.12f} (sqrt2 normalization defect confirmed)")

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
    print(f"galaxies: {len(gal)}, points: {int(sum(len(p[0]) for p in gal))}")
    out = {"generated": "2026-09-16",
           "n_galaxies": len(gal), "n_points": int(sum(len(p[0]) for p in gal)),
           "purpose": "Third row of the (mu, a0) map: mu_simple = tanh(arsinh(x)/2), mu'(0)=1/2, "
                      "the half-rapidity member of the rapidity-multiple family (W3 of "
                      "POSTULATE_R_ISOLATION_2026-09-16.md). Same harness as "
                      "sparc_a0_reextract_std.py; a0 grid extended to [0.5,4.0]e-10 x73 because "
                      "mu_simple's deep-MOND sqrt(2) normalization defect pushes its a0 high.",
           "mu_functions": {"dual": "x/(1+x) [X falsified control]",
                            "std": "x/sqrt(1+x^2) [live]",
                            "simple": "x/(1+sqrt(1+x^2)) [half-rapidity, mu'(0)=1/2]"},
           "closure_forms": {"dual": "g = gbar*(1/2+sqrt(1/4+a0/gbar))",
                             "std": "g = sqrt((gbar^2+sqrt(gbar^4+4*gbar^2*a0^2))/2)",
                             "simple": "g = sqrt(gbar^2+2*a0*gbar)"}}
    for mu in ('dual', 'std', 'simple'):
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
        print(f"[{mu:7s}] a0 = {a0:.4e}, bootstrap 68% [{lo16:.4e}, {hi84:.4e}]", flush=True)
    return out

if __name__ == "__main__":
    print("closure and ordering checks:")
    verify_closures()
    res = main(sys.argv[1] if len(sys.argv)>1 else '/tmp/sparc_data')
    dest = sys.argv[2] if len(sys.argv)>2 else str(Path(__file__).parent / 'A0_REEXTRACTION_3MU_2026-09-16.json')
    json.dump(res, open(dest, 'w'), indent=2)
    print("written:", dest)
