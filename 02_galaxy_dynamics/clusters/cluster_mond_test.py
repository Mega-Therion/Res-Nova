#!/usr/bin/env python3
"""ITEM 6 (CLUSTERS) -- first real test. 2026-09-24.

THE QUESTION. In galaxy clusters, MOND-type theories are known to under-predict the
dynamical mass by a factor ~2 even after the MOND boost (Sanders 1999, 2003; The & White
1988; Angus+ 2008). That is the classic, canonical failure. This corpus has never tested it.

We test mu_std(x) = x/sqrt(1+x^2) -- the SURVIVING branch -- with a_0 = c H_0/(2 pi)
DERIVED, no free parameter, against weak-lensing cluster masses.

WHY LENSING AND NOT X-RAY HYDROSTATIC MASSES. The standard objection to X-ray cluster
tests is hydrostatic mass bias (~20-30%). Weak lensing does not assume hydrostatic
equilibrium, so it removes that escape route in both directions.

DATA (both downloaded from VizieR, committed alongside):
  Corasaniti, Sereno & Ettori 2021, ApJ 911, 82  [J/ApJ/911/82]
    table1 -- 317 clusters, weak-lensing M200c and M500c (LC^2 / CLASH / HSC-XXL)
    table2 -- 105 clusters, gas mass fractions f_gas
  12 clusters carry BOTH after name normalisation. That is the sample.

METHOD at r_500:
  M_500   : weak-lensing total mass
  M_bary  : f_gas*M_500 (gas) + stars
  r_500   : from M_500 = 500 rho_c(z) (4 pi/3) r_500^3
  g_N     : G M_bary / r_500^2
  MOND    : mu(g/a_0) g = g_N with mu = x/sqrt(1+x^2) inverts EXACTLY to
              g = a_0 * sqrt( (s^2 + s sqrt(s^2+4))/2 ),  s = g_N/a_0
  verdict : R = M_500(lensing) / M_dyn(MOND). R ~ 1 => works. R ~ 2 => classic failure.
"""
import math, re, json

# ---- cosmology: the corpus's own, pre-registered ----
OM_L = math.log(2)          # Omega_Lambda = ln 2
OM_M = 1 - OM_L             # 0.30685
H0_KMS = 68.27              # pre-registered P1 (Zenodo 21867985)
C_KMS  = 2.99792458e5
MPC_M  = 3.0856775814913673e22
G_SI   = 6.67430e-11
MSUN   = 1.98892e30

H0_SI = H0_KMS*1e3/MPC_M
A0 = C_KMS*1e3*H0_SI/(2*math.pi)         # a_0 = c H_0 / 2 pi   [m/s^2]  DERIVED
A0_MILGROM = 1.2e-10

def Ez(z): return math.sqrt(OM_M*(1+z)**3 + OM_L)
def rho_c(z): return 3*(H0_SI*Ez(z))**2/(8*math.pi*G_SI)     # kg/m^3

def r_delta(M_kg, z, delta=500.0):
    return (M_kg/(delta*rho_c(z)*(4*math.pi/3)))**(1/3)      # m

def g_mond(gN):
    """Exact inverse of mu_std(x)=x/sqrt(1+x^2):  mu(g/a0) g = gN."""
    s = gN/A0
    return A0*math.sqrt((s*s + s*math.sqrt(s*s+4))/2)

def norm(s):
    s = s.strip().upper().replace(' ','')
    s = s.replace('ABELL-','A').replace('ABELL','A')
    s = re.sub(r'^A0+','A',s); s = re.sub(r'^RXC-?J','RXCJ',s); s = re.sub(r'^MACS-?J','MACSJ',s)
    return s.replace('-','').replace('_','')

def load():
    t1={}
    for l in open('corasaniti2021_table1_lensing.dat'):
        if len(l) < 50: continue
        t1[norm(l[0:20])] = dict(name=l[0:20].strip(), z=float(l[21:26]),
                                 M500=float(l[39:44]), eM500=float(l[45:50]))
    t2={}
    for l in open('corasaniti2021_table2_fgas.dat'):
        if len(l) < 35: continue
        t2[norm(l[0:16])] = dict(fgas=float(l[24:29]), efgas=float(l[30:35]))
    return {k: {**t1[k], **t2[k]} for k in sorted(set(t1)&set(t2))}

# stellar mass fraction of M_500; cluster values cluster around 1-2 per cent.
F_STAR = 0.015

def analyse(f_star=F_STAR, label=""):
    rows=[]
    for k, c in load().items():
        M500 = c['M500']*1e14*MSUN
        Mgas = c['fgas']*M500
        Mbar = Mgas + f_star*M500
        r500 = r_delta(M500, c['z'])
        gN   = G_SI*Mbar/r500**2
        gM   = g_mond(gN)
        Mdyn = gM*r500**2/G_SI
        rows.append(dict(name=c['name'], z=c['z'], M500=c['M500'], fgas=c['fgas'],
                         r500_Mpc=r500/MPC_M, gN_a0=gN/A0, R=M500/Mdyn,
                         Mdyn=Mdyn/(1e14*MSUN)))
    rows.sort(key=lambda r: -r['M500'])
    print(f"\n{'='*94}\n{label}  (f_star = {f_star:.3f} of M_500)\n{'='*94}")
    print(f"{'cluster':<18}{'z':>6}{'M500/1e14':>11}{'f_gas':>7}{'r500/Mpc':>10}"
          f"{'g_N/a0':>9}{'M_MOND':>10}{'R=M_lens/M_MOND':>17}")
    for r in rows:
        print(f"{r['name']:<18}{r['z']:>6.3f}{r['M500']:>11.2f}{r['fgas']:>7.3f}"
              f"{r['r500_Mpc']:>10.2f}{r['gN_a0']:>9.2f}{r['Mdyn']:>10.2f}{r['R']:>17.2f}")
    Rs = sorted(r['R'] for r in rows)
    n = len(Rs); med = Rs[n//2] if n%2 else 0.5*(Rs[n//2-1]+Rs[n//2])
    mean = sum(Rs)/n
    print(f"{'-'*94}")
    print(f"  N = {n}    median R = {med:.2f}    mean R = {mean:.2f}    range {Rs[0]:.2f} - {Rs[-1]:.2f}")
    return med, mean, n, rows

if __name__ == "__main__":
    print(f"a_0 = c H_0/(2 pi) with H_0 = {H0_KMS} km/s/Mpc  ->  {A0:.4e} m/s^2")
    print(f"  (Milgrom's fitted a_0 = {A0_MILGROM:.2e};  derived/fitted = {A0/A0_MILGROM:.3f})")
    print(f"  Omega_Lambda = ln 2 = {OM_L:.5f},  Omega_m = {OM_M:.5f}")
    med, mean, n, rows = analyse(F_STAR, "mu_std with DERIVED a_0, gas + stars")
    med0, mean0, _, _   = analyse(0.0,    "gas only (no stellar contribution)")
    json.dump(rows, open('cluster_mond_results.json','w'), indent=1)
    print(f"\n{'='*94}\nVERDICT")
    print(f"  R = 1 would mean the theory accounts for clusters with baryons alone.")
    print(f"  R ~ 2 is the classic MOND cluster failure (Sanders 2003, Angus+ 2008).")
    print(f"  MEASURED median R = {med:.2f} (gas+stars), {med0:.2f} (gas only), N = {n}.")
