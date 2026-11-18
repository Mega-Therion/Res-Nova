#!/usr/bin/env python3
"""Deterministic re-verification of every numeric claim in the 2026-11-18
res-extensa / Auroboryai legitimacy audit.

Run:  python3 verify_audit_identities.py
Exit: 0 if every identity holds to its stated tolerance, 1 otherwise.

Nothing here is a physics result. Every line is an exact identity, an
arithmetic check on a number quoted from the repositories, or a sigma
recomputation from a number the repositories themselves record. The
purpose is to make the audit's [D] and [arith] tags reproducible.

Pinned inputs
  res-extensa 0cb47466926c479bf85a039ad6039db7cd37a772
  Auroboryai  82045372cb63939395cde8abeeddc8cd42dbe221
  Res-Nova    c4a0f42cc334d9a04ea59f4f758afac257e55dd1
"""
import math

FAIL = []

def check(name, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + name + ("   " + detail if detail else ""))
    if not cond:
        FAIL.append(name)

def mu_std(x):
    return x / math.sqrt(1.0 + x * x)

def F_std(x):
    return 0.5 * (x * math.sqrt(1.0 + x * x) - math.asinh(x))

# ---------------------------------------------------------------- 1. band circle
print("\n[1] band circle and polar-slope realization")
for theta in (0.7, 1 / math.sqrt(2)):
    kappa = math.sqrt(theta * (2 - theta))
    h = 1 - theta
    x = kappa / h
    check(f"kappa^2+(1-theta)^2=1 at theta={theta:.6f}",
          abs(kappa ** 2 + h ** 2 - 1) < 1e-12, f"{kappa**2+h**2:.15f}")
    check(f"mu_std(kappa/h)=kappa at theta={theta:.6f}",
          abs(mu_std(x) - kappa) < 1e-12, f"mu={mu_std(x):.12f} kappa={kappa:.12f}")

kappa_floor = math.sqrt(0.5 * (2 - 0.5 * 2))  # theta=1/sqrt2 handled below
th = 1 / math.sqrt(2)
kap = math.sqrt(th * (2 - th))
check("sqrt(2)-1/2 form equals kappa(1/sqrt2)",
      abs(kap - math.sqrt(math.sqrt(2) - 0.5)) < 1e-15, f"{kap:.15f}")

# ------------------------------------------------- 2. Gudermannian / rapidity
print("\n[2] Gudermannian bridge: arctan(sinh u) = asin(tanh u)")
worst = max(abs(math.atan(math.sinh(u)) - math.asin(math.tanh(u)))
            for u in [i * 0.001 - 10 for i in range(20001)])
check("max |arctan(sinh u) - gd(u)| over u in [-10,10] < 1e-12", worst < 1e-12, f"{worst:.2e}")
check("mu_std(x)=sin(arctan x) at x=1", abs(mu_std(1.0) - math.sin(math.atan(1.0))) < 1e-15)

# ------------------------------------------------------------- 3. duality
print("\n[3] duality mu(1/x)^2 + mu(x)^2 = 1")
for x in (0.01, 0.3, 1.0, 3.0, 100.0):
    s = mu_std(x) ** 2 + mu_std(1 / x) ** 2
    check(f"duality at x={x}", abs(s - 1) < 1e-12, f"{s:.16f}")

# ------------------------------------------------------- 4. holonomy gate
print("\n[4] holonomy gate P_c = chi^2/(1+chi^2)")
chi = 1 / math.sqrt(2)
pc = chi ** 2 / (1 + chi ** 2)
check("P_c(1/sqrt2) = 1/3 exactly", abs(pc - 1 / 3) < 1e-15, f"{pc:.16f}")

# --------------------------------------------------- 5. lambda_s ceiling
print("\n[5] scalar single-valuedness ceiling")
lam = (27 + 12 * math.sqrt(6)) / 5
check("lambda_s ceiling = 11.2788", abs(lam - 11.2788) < 1e-4, f"{lam:.10f}")

# --------------------------------------------------------- 6. Cassini
print("\n[6] Cassini quadrupole sigmas from the repo's own Q2 = 1.7e-26")
Q2 = 1.7e-26
s14 = (Q2 - 3e-27) / 3e-27
s26 = (Q2 - 1.6e-27) / 1.8e-27
check("Hees 2014 (3+-3)e-27 gives about +4.6 sigma", abs(s14 - 4.6) < 0.15, f"{s14:+.2f}")
check("2026 (1.6+-1.8)e-27 gives about +8.6 sigma", abs(s26 - 8.6) < 0.15, f"{s26:+.2f}")

# --------------------------------------------------------- 7. E8 arithmetic
print("\n[7] E8, ternary and 57600 arithmetic")
check("112+128=240", 112 + 128 == 240)
check("1+56+126+56+1=240", 1 + 56 + 126 + 56 + 1 == 240)
check("78+8+81+81=248", 78 + 8 + 81 + 81 == 248)
check("3^4=81", 3 ** 4 == 81)
check("240^2=57600", 240 ** 2 == 57600)
check("58000-57600=400=20^2", 58000 - 57600 == 400 == 20 ** 2)
check("57600=24*60*40", 24 * 60 * 40 == 57600)

# --------------------------------------------- 8. Paper C L_IT = 2 F_std
print("\n[8] Paper C information-tension potential equals 2*F_std")
for x in (0.1, 0.5, 1.0, 2.0, 5.0):
    y = x * x
    bracket = math.sqrt(y * (1 + y)) - math.asinh(math.sqrt(y))
    check(f"L_IT bracket = 2F_std at x={x}", abs(bracket - 2 * F_std(x)) < 1e-15,
          f"diff={abs(bracket-2*F_std(x)):.1e}")
for x in (0.3, 1.0, 3.0):
    y = x * x
    check(f"dL_IT/dy = mu_std at x={x}", abs(math.sqrt(y / (1 + y)) - mu_std(x)) < 1e-15)

# --------------------------------------------- 9. Paper E Cassini ratio
print("\n[9] Paper E non-minimal coupling versus Cassini")
check("xi=0.127 exceeds 1e-3 by about 127x", abs(0.127 / 1e-3 - 127) < 1.0, f"{0.127/1e-3:.0f}x")

# ------------------------------------------------- 10. Omega_Lambda = ln 2
print("\n[10] Omega_Lambda = ln 2 against Planck 2018")
sig = (math.log(2) - 0.6889) / 0.0056
check("ln2 = 0.693147", abs(math.log(2) - 0.693147) < 1e-6, f"{math.log(2):.9f}")
check("ln2 is within 1 sigma of 0.6889+-0.0056", abs(sig) < 1.0, f"{sig:+.2f} sigma")
check("1-ln2 = 0.306853", abs(1 - math.log(2) - 0.306853) < 1e-6)

# ------------------------------------------------------------- 11. a0 / xi
print("\n[11] acceleration scale and horizon ratio")
a0 = 1.1607e-10
c = 2.99792458e8
H0 = 67.4e3 / 3.0856775814913673e22
cH0 = c * H0
check("cH0/2pi = 1.0422e-10", abs(cH0 / (2 * math.pi) - 1.0422e-10) < 1e-15,
      f"{cH0/(2*math.pi):.6e}")
check("xi = a0/(cH0) = 0.17725", abs(a0 / cH0 - 0.17725) < 1e-4, f"{a0/cH0:.6f}")
check("a0 is 1.11x the cH0/2pi anchor", abs(a0 / (cH0 / (2 * math.pi)) - 1.11) < 0.01,
      f"{a0/(cH0/(2*math.pi)):.4f}")

print("\n" + ("FAILURES: " + ", ".join(FAIL) if FAIL else "ALL AUDIT IDENTITIES HOLD"))
raise SystemExit(1 if FAIL else 0)
