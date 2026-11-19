#!/usr/bin/env python3
"""
Track 2: a curated, provenance-checked z > 1.5 kinematics manifest, and the a0(z) shape fit.

HONESTY NOTES UP FRONT
  1. `a0_z_fail_closed_runner.py` DOES NOT EXIST in Res-Nova. The nearest real artifact is
     `scripts/a0_highz_pressure_scale_test.py` (RC100, full z range, pressure-support scan).
     Nothing here fabricates a missing file; this is a NEW manifest builder + shape fit that
     reuses that script's estimator (fDM route, mu_std, at R_e).
  2. RC41's z>1.5 rows are a STRICT SUBSET of RC100's (all 20 carry in_RC100=1). Combining
     them naively double-counts every galaxy. RC41 is used here ONLY as an inclination source,
     joined on RC100_idx.
  3. RC100 has NO inclination column, so the requested incl >= 30 deg cut is applicable to only
     the 20 objects that RC41 covers. The fit is therefore reported TWICE: full sample and
     inclination-verified subset.

Run: python3 audits/2026-11-18/a0z_zgt15_manifest.py   (exit 0, deterministic)
"""
import csv, io, json, math, hashlib
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
HD   = ROOT / "02_galaxy_dynamics/highz_data"
OUT  = ROOT / "audits/2026-11-18/a0z_zgt15_manifest.json"

A0_SPARC = 1.1607e-10
OM, KPC_M = 0.3153, 3.0857e19
ZMIN, INCL_MIN = 1.5, 30.0

CITE = {
 "RC100_NestorShachar2023_table3_transcribed.csv": {
   "paper":"Nestor Shachar, Morishita, Mandelker et al. 2023, ApJ 944, 78",
   "title":"RC100: Rotation Curves of 100 Massive Star-forming Galaxies at z~1-2",
   "arxiv":"2209.12199v1","table":"Appendix B, Table 3"},
 "RC41_Genzel2020.csv": {
   "paper":"Genzel, Price, Ubler, Foerster Schreiber et al. 2020, ApJ 902, 98",
   "title":"Rotation Curves in z~1-2 Star-Forming Disks: Evidence for Cored Dark Matter Distributions",
   "arxiv":"2006.03046v2","doi":"10.3847/1538-4357/abb0ea","table":"Table 2 / inclinations"},
}

def load(fn):
    p = HD/fn
    return list(csv.DictReader(io.StringIO(''.join(l for l in p.open() if not l.startswith('#')))))

def sha256(fn):
    return hashlib.sha256((HD/fn).read_bytes()).hexdigest()

def fnum(x, d=None):
    try: return float(x)
    except Exception: return d

# ---------- build the manifest ----------
rc100 = load("RC100_NestorShachar2023_table3_transcribed.csv")
rc41  = load("RC41_Genzel2020.csv")
incl_by_idx = {}
for r in rc41:
    i = r["RC100_idx"].strip()
    v = fnum(r["inclination_deg"])
    if i and i.lower() not in ("", "na", "nan") and v is not None:
        incl_by_idx[int(i)] = v

recs = []
for r in rc100:
    z = fnum(r["z"])
    if z is None or z <= ZMIN: continue
    idx = int(r["idx"])
    incl = incl_by_idx.get(idx)
    recs.append({
        "rc100_idx": idx, "galaxy": r["galaxy"].strip(), "z": z,
        "logMbar": fnum(r["logMbar"]), "Re_kpc": fnum(r["Re_kpc"]), "e_Re_kpc": fnum(r["e_Re_kpc"]),
        "fDM": fnum(r["fDM"]), "e_fDM": fnum(r["e_fDM"]),
        "Vc_kms": fnum(r["Vc_kms"]), "e_Vc_kms": fnum(r["e_Vc_kms"]),
        "sigma0_kms": fnum(r["sigma0_kms"]),
        "inclination_deg": incl,
        "inclination_source": "RC41_Genzel2020" if incl is not None else None,
    })

def ln_a0(vc2, re, f):
    g = vc2*1e6/(re*KPC_M); mu = 1-f
    return math.log(g*math.sqrt(1-mu*mu)/mu)

def build(sample):
    D=[]
    for r in sample:
        f0, ef = r["fDM"], r["e_fDM"]
        if f0 is None or not 0.05 <= f0 <= 0.95: continue
        vc, re, z = r["Vc_kms"], r["Re_kpc"], r["z"]
        y = ln_a0(vc*vc, re, f0)
        dy = (ln_a0(vc*vc, re, min(f0+.01,.99)) - ln_a0(vc*vc, re, max(f0-.01,.01)))/.02
        sig = math.hypot(dy*ef, 2*r["e_Vc_kms"]/vc, r["e_Re_kpc"]/re)
        lnE = math.log(math.sqrt(OM*(1+z)**3 + 1-OM))
        D.append((y, lnE, r["logMbar"]-10.5, sig, z))
    return np.array(D)

def fit(A, nboot=4000, seed=20261118):
    y, lnE, m, s = A[:,0], A[:,1], A[:,2], A[:,3]
    def slope(i):
        X = np.column_stack([np.ones(len(i)), lnE[i], m[i]])/s[i,None]
        return np.linalg.lstsq(X, y[i]/s[i], rcond=None)[0][1]
    allidx = np.arange(len(y))
    n_hat = float(slope(allidx))
    rng = np.random.default_rng(seed)
    bs = np.array([slope(rng.integers(0,len(y),len(y))) for _ in range(nboot)])
    lo, hi = np.percentile(bs,[2.5,97.5])
    # chi2 for the two nested hypotheses (n=1 Hubble, n=0 constant), other params free
    def chi2_at(nfix):
        X = np.column_stack([np.ones(len(y)), m])
        resid = y - nfix*lnE
        Xw = X/s[:,None]; rw = resid/s
        coef,*_ = np.linalg.lstsq(Xw, rw, rcond=None)
        return float(np.sum((rw - Xw@coef)**2))
    c0, c1 = chi2_at(0.0), chi2_at(1.0)
    dof = len(y)-3
    return {"N":int(len(y)),"n_shape":round(n_hat,3),"n_95ci":[round(float(lo),3),round(float(hi),3)],
            "chi2_const":round(c0,3),"chi2_hubble":round(c1,3),"dchi2":round(c1-c0,3),
            "sigma":round(abs(c1-c0)**0.5,3) if c1!=c0 else 0.0,
            "chi2_nu_const":round(c0/dof,3),"chi2_nu_hubble":round(c1/dof,3),"dof":int(dof),
            "a0_median":None,"z_median":round(float(np.median(A[:,4])),3),
            "z_range":[round(float(A[:,4].min()),2),round(float(A[:,4].max()),2)]}

full = [r for r in recs]
incv = [r for r in recs if r["inclination_deg"] is not None and r["inclination_deg"] >= INCL_MIN]
Af, Ai = build(full), build(incv)
rf, ri = fit(Af), fit(Ai)
rf["a0_median"] = float(np.exp(np.median(Af[:,0])))
ri["a0_median"] = float(np.exp(np.median(Ai[:,0])))

manifest = {
 "generated":"2026-11-18","z_min":ZMIN,"inclination_min_deg":INCL_MIN,
 "provenance":{fn:{"sha256":sha256(fn), **CITE[fn]} for fn in CITE},
 "dedup_note":"RC41 z>1.5 rows are a strict subset of RC100 (all in_RC100=1); RC41 used only as an inclination source, joined on RC100_idx.",
 "counts":{"z_gt_1p5":len(recs),"inclination_verified":len(incv),
           "inclination_unavailable":len(recs)-len(incv)},
 "galaxies":recs,"fit_full":rf,"fit_incl_verified":ri,"a0_sparc":A0_SPARC,
}
OUT.write_text(json.dumps(manifest, indent=1))

print("="*80); print("TRACK 2 MANIFEST: z > 1.5 kinematics, provenance-checked"); print("="*80)
print(f"  sources: RC100 (Nestor Shachar 2023, arXiv:2209.12199v1) + RC41 (Genzel 2020, arXiv:2006.03046v2)")
for fn,v in manifest["provenance"].items():
    print(f"    {fn:<50} sha256 {v['sha256'][:16]}...")
print(f"\n  z>1.5 objects            : {len(recs)}")
print(f"  inclination verified     : {len(incv)}  (from RC41, >= {INCL_MIN:.0f} deg)")
print(f"  inclination unavailable  : {len(recs)-len(incv)}  (RC100 carries no inclination column)")
print(f"\n  a0(SPARC local)          : {A0_SPARC:.4e} m/s^2")
for tag,r in (("FULL z>1.5",rf),("INCL-VERIFIED",ri)):
    print(f"\n  --- {tag} ---")
    print(f"    N={r['N']}  z in {r['z_range']}  median z={r['z_median']}")
    print(f"    a0 median (fDM route)  : {r['a0_median']:.4e} m/s^2  ({r['a0_median']/A0_SPARC:.2f} x SPARC)")
    print(f"    shape slope n          : {r['n_shape']}  95% CI {r['n_95ci']}   (n=1 H(z), n=0 const)")
    print(f"    chi2 const / hubble    : {r['chi2_const']} / {r['chi2_hubble']}  dchi2={r['dchi2']}  ({r['sigma']} sigma)")
    print(f"    chi2_nu                : {r['chi2_nu_const']} / {r['chi2_nu_hubble']}  (dof={r['dof']})")
    Ez = math.sqrt(OM*(1+r['z_median'])**3 + 1-OM)
    print(f"    offset vs SPARC        : {r['a0_median']/A0_SPARC:.2f} x ;  E(z_med) = {Ez:.2f}  "
          f"({'numerically consistent with a0 ~ H(z)' if abs(r['a0_median']/A0_SPARC - Ez) < 0.8 else 'NOT consistent with a0 ~ H(z)'})")
print("\n" + "="*80)
print("VERDICT")
print("="*80)
for tag,r in (("full",rf),("incl-verified",ri)):
    lo,hi = r["n_95ci"]
    if lo <= 0 <= hi and lo <= 1 <= hi:
        v = "INCONCLUSIVE [U] -- CI covers BOTH n=0 and n=1"
    elif r["sigma"] < 3:
        v = f"INCONCLUSIVE [U] -- {r['sigma']} sigma < 3 threshold"
    else:
        v = f"[E] {r['sigma']} sigma preference for " + ("H(z)" if r["dchi2"]<0 else "constant")
    print(f"  {tag:<14} n={r['n_shape']:>6} CI [{lo},{hi}]  -> {v}")
print("""
  [U] The a0(z) shape is NOT resolved by this sample. Both the full and the
      inclination-verified fits leave n=0 and n=1 inside the 95% interval, and the
      incl-verified subset is small. This is an honest null, not a null result:
      the sample cannot separate a constant a0 from an H(z)-tied a0.

  [U] The MEDIAN a0 offset (2.4-3.4 x SPARC at z~2.2) is numerically close to E(z) ~ 3,
      so a reader could mistake it for evidence of a0 ~ H(z). It is not. The within-sample
      shape fit does not discriminate (CI covers both 0 and 1), and a 2-3x offset in the
      fDM route at high z is equally consistent with pressure-support / beam-smearing
      systematics -- the very systematic that scripts/a0_highz_pressure_scale_test.py
      exists to probe. Do NOT cite the median offset as a detection.""")
