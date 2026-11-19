#!/usr/bin/env python3
"""SUPERSEDED 2026-11-18: uses the quadratic K that TARGET_D5 §1.3 excludes [D]. See door_under_cosh.py.
SPARC reach vs 1/mu (2026-11-18). If MOND switches off beyond r ~ 1/mu, count SPARC galaxies
and low-acceleration points (g_bar < a0) lying beyond 1/mu = 132.7 kpc (dust by z_rec) and
24.5 kpc (dust by z_eq), from SMALL_Q0_DUST.json."""
import glob, json, os
D=os.path.join(os.path.dirname(__file__),"../../02_galaxy_dynamics/sparc_data")
a0=1.1607e-10; kms2=1e6/3.0857e19                        # (km/s)^2/kpc -> m/s^2
cut=json.load(open(os.path.join(os.path.dirname(__file__),"SMALL_Q0_DUST.json")))["galaxy_side_1_over_mu_kpc"]
gals=[]
for f in sorted(glob.glob(D+"/*_rotmod.dat")):
    rows=[l.split() for l in open(f) if l.strip() and not l.startswith("#")]
    R=[float(r[0]) for r in rows]
    gb=[(float(r[3])**2+float(r[4])**2+float(r[5])**2*(1 if len(r)>5 else 0))*kms2/float(r[0]) if float(r[0])>0 else 0 for r in rows]
    gals.append((os.path.basename(f)[:-11],R,gb))
out={"N_galaxies":len(gals),"R_max_kpc_max":max(max(g[1]) for g in gals)}
for k,c in cut.items():
    ng=sum(max(g[1])>c for g in gals)
    lowpts=sum(1 for g in gals for r,b in zip(g[1],g[2]) if b<a0)
    beyond=sum(1 for g in gals for r,b in zip(g[1],g[2]) if b<a0 and r>c)
    names=[g[0] for g in gals if max(g[1])>c]
    out[k]={"one_over_mu_kpc":c,"galaxies_extending_beyond":ng,"lowacc_points_total":lowpts,
            "lowacc_points_beyond":beyond,"frac_beyond":beyond/lowpts,"examples":names[:8]}
out["verdict"]=("[O] z_rec bound (132.7 kpc): only %d galaxies reach it -> door survives SPARC. "
 "z_eq bound (24.5 kpc): %d galaxies / %.0f%% of MOND-regime points lie beyond -> would fail if dust is needed by z_eq."
 %(out["z=1100"]["galaxies_extending_beyond"],out["z=3400"]["galaxies_extending_beyond"],100*out["z=3400"]["frac_beyond"]))
print(json.dumps(out,indent=1)); json.dump(out,open("SPARC_MU_REACH.json","w"),indent=1)
