#!/usr/bin/env python3
"""Silhouette test of AeST aether drag with Milky Way satellites.
Drag hypothesis: a system's MOND boost weakens with its speed through the local aether. Prediction: at fixed
Galactocentric distance, faster satellites look more Newtonian, i.e. log(sigma_obs/sigma_MOND) and
log(sigma_obs/sigma_Newton) DEcrease with speed. Speed computed two ways: (A) relative to the Milky Way rest frame,
(B) relative to the CMB frame (the cosmic aether frame). Confounder: speed and external field both correlate with
distance, so partial (distance-controlled) Spearman correlations are the discriminating numbers.
Data: LVDB (Pace 2025, CC0) positions, distances, proper motions, line-of-sight velocities; sigma predictions from
dwarf_screening_test (stars only, M/L=2, V_MW=200 km/s, derived a0)."""
import csv, json
import numpy as np
from scipy.stats import spearmanr
import astropy.units as u
from astropy.coordinates import SkyCoord, Galactocentric, CartesianDifferential
import dwarf_screening_test as D
from efe_quadrupole_q2 import A0_DERIVED

pred = {d["name"]: D.predict(d, 2.0, 200, A0_DERIVED) for d in D.load()}
obs = {d["name"]: d for d in D.load()}
rows = []
for r in csv.DictReader(open("dwarf_data/lvdb_dwarf_mw.csv")):
    nm = r["name"]
    if nm not in pred or nm in ("Large Magellanic Cloud", "LMC", "Small Magellanic Cloud", "SMC", "Sagittarius"): continue
    try:
        pmra, pmdec, vlos = float(r["pmra"]), float(r["pmdec"]), float(r["vlos_systemic"])
        dist = 10 ** (float(r["distance_modulus"]) / 5 + 1) / 1e3   # kpc
    except (ValueError, KeyError): continue
    if not all(np.isfinite([pmra, pmdec, vlos, dist])): continue
    c = SkyCoord(ra=float(r["ra"]) * u.deg, dec=float(r["dec"]) * u.deg, distance=dist * u.kpc,
                 pm_ra_cosdec=pmra * u.mas / u.yr, pm_dec=pmdec * u.mas / u.yr, radial_velocity=vlos * u.km / u.s)
    gc = c.transform_to(Galactocentric())
    v = np.array([gc.v_x.to_value(u.km / u.s), gc.v_y.to_value(u.km / u.s), gc.v_z.to_value(u.km / u.s)])
    rows.append({"name": nm, "Dgc": float(np.sqrt(gc.x**2 + gc.y**2 + gc.z**2).to_value(u.kpc)), "vGC": v})
# Milky Way velocity relative to the CMB: v_MW,CMB = v_sun,CMB - v_sun,GC (both in Galactocentric Cartesian axes)
lb = np.radians([264.021, 48.253])
dir_gal = np.array([np.cos(lb[1]) * np.cos(lb[0]), np.cos(lb[1]) * np.sin(lb[0]), np.sin(lb[1])])
# astropy Galactocentric: x axis points from the Sun toward the GC (same sense as Galactic x), y along rotation, z to NGP (tilt ignored)
v_sun_cmb = 369.82 * dir_gal
v_sun_gc = np.array(Galactocentric().galcen_v_sun.d_xyz.to_value(u.km / u.s))
v_mw_cmb = v_sun_cmb - v_sun_gc
print(f"MW velocity vs CMB: {np.linalg.norm(v_mw_cmb):.0f} km/s   (Sun vs GC {np.linalg.norm(v_sun_gc):.0f} km/s)")
out = []
for r in rows:
    nm = r["name"]; p = pred[nm]; o = obs[nm]
    vA = float(np.linalg.norm(r["vGC"])); vB = float(np.linalg.norm(r["vGC"] + v_mw_cmb))
    vf = (D.G * 2.0 * o["L"] * D.MSUN * A0_DERIVED) ** 0.25 / 1e3      # deep-MOND v_f of the stars (M/L = 2), km/s
    out.append({"name": nm, "Dgc": r["Dgc"], "vA": vA, "vB": vB, "vf": vf, "xA": vA / vf, "xB": vB / vf,
                "rN": float(np.log10(o["sig"] / p["N"])), "rM": float(np.log10(o["sig"] / p["MOND"]))})
print(f"{len(out)} satellites with sigma, proper motions and v_los\n")
print(f"{'dwarf':16s} {'D_gc':>6s} {'v_MW':>6s} {'v_CMB':>6s} {'log obs/N':>10s} {'log obs/MOND':>13s}")
for o in sorted(out, key=lambda o: o["Dgc"]):
    print(f"{o['name'][:16]:16s} {o['Dgc']:6.0f} {o['vA']:6.0f} {o['vB']:6.0f} {o['rN']:10.2f} {o['rM']:13.2f}")
lD = np.log10([o["Dgc"] for o in out])
lL = np.log10([obs[o["name"]]["L"] for o in out])
def partial(y, x, ctrl=None):   # Spearman partial correlation of y with x, controlling for log D (and optionally log L)
    from scipy.stats import rankdata
    Z = np.column_stack([np.ones(len(y)), rankdata(lD)] + ([rankdata(lL)] if ctrl == "DL" else []))
    res = lambda v: rankdata(v) - Z @ np.linalg.lstsq(Z, rankdata(v), rcond=None)[0]
    return spearmanr(res(y), res(x))
res = {}
vf = np.array([o["vf"] for o in out]); xA = np.array([o["xA"] for o in out]); xB = np.array([o["xB"] for o in out])
print(f"\nv_f (stars, M/L=2): {vf.min():.1f}-{vf.max():.1f} km/s. Linear-theory threshold C*v_f with C = 0.19-0.27 (D3 note 7).")
print(f"v_rel/(0.27 v_f): MW frame {np.min(xA)/0.27:.0f}-{np.max(xA)/0.27:.0f}, CMB frame {np.min(xB)/0.27:.0f}-{np.max(xB)/0.27:.0f}  -> every satellite is above threshold")
for vk, lab in (("vA", "speed vs MW frame"), ("vB", "speed vs CMB frame"), ("xA", "v_MW / v_f"), ("xB", "v_CMB / v_f")):
    x = np.array([o[vk] for o in out])
    for yk, ylab in (("rN", "log(obs/Newton)"), ("rM", "log(obs/MOND+EFE)")):
        y = np.array([o[yk] for o in out])
        s = spearmanr(x, y); pc = partial(y, x)
        pl = partial(y, x, "DL")
        res[f"{yk}_{vk}"] = {"spearman": [s.statistic, s.pvalue], "partial_vs_logD": [pc.statistic, pc.pvalue], "partial_vs_logD_logL": [pl.statistic, pl.pvalue]}
        print(f"{ylab:18s} vs {lab:19s}: Spearman rho={s.statistic:+.2f} (p={s.pvalue:.2f});  D-controlled {pc.statistic:+.2f} (p={pc.pvalue:.2f});  D,L-controlled {pl.statistic:+.2f} (p={pl.pvalue:.2f})")
print("\nDrag predicts NEGATIVE distance-controlled correlations (faster -> more Newtonian).")
print("v/v_f shares luminosity with the residual (log v_f = L/4 + const, log sigma_N = L/2 + ...), so its raw and D-controlled")
print("correlations are inflated by construction; the D,L-controlled column is the clean one.")
print("Caveat: proper-motion, distance and v_los errors are NOT propagated (0.1 mas/yr at 180 kpc = 85 km/s); Pisces II's speed is likely error-driven.")
json.dump({"rows": out, "correlations": res}, open("DWARF_VELOCITY_DRAG_TEST.json", "w"), indent=1)
