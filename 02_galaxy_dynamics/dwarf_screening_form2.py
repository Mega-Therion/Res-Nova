#!/usr/bin/env python3
"""Second (and last) pre-declared screening form, chosen after form 1 (S = 1 - mu) failed the dwarfs:
    S2(eta) = 1 - mu_std(eta)^2 = mu_std(1/eta)^2 = 1 / (1 + eta^2)
(the MuStdDuality identity mu(x)^2 + mu(1/x)^2 = 1). Suppression ~ eta^2 instead of ~ eta.
Same three tests: Cassini (2026, 2 sigma), MW dwarfs (LVDB, LMC/SMC/Sgr excluded), SPARC per-galaxy (Chae 2020)."""
import json
import numpy as np
import dwarf_screening_test as D
import environment_screening as E
from efe_quadrupole_q2 import Q2, A0_DERIVED

S2 = lambda eta: 1 / (1 + eta**2)
UP2 = 1.6e-27 + 2 * 1.8e-27
out = {"form": "S2 = 1/(1+eta^2)", "cassini": {}, "dwarfs": {}, "sparc": {}}
for ge in (1.9e-10, 2.4e-10):
    eta = ge / A0_DERIVED; q = Q2(E.nu_std, A0_DERIVED, ge)[0] * S2(eta)
    out["cassini"][f"{ge:.1e}"] = {"eta": eta, "S": S2(eta), "Q2": q, "sigma": (q - 1.6e-27) / 1.8e-27, "pass": bool(q <= UP2)}
    print(f"Cassini g_ext={ge:.1e}: S={S2(eta):.3f}  Q2={q*1e27:.2f}e-27  ({(q-1.6e-27)/1.8e-27:+.2f} sigma) {'PASS' if q <= UP2 else 'FAIL'}")
D.S = S2
ds = [d for d in D.load() if d["name"] not in ("Large Magellanic Cloud", "LMC", "Small Magellanic Cloud", "SMC", "Sagittarius")]
for vmw in (180, 200, 220):
    for ml in (1.0, 2.0, 3.0):
        m = D.score(ds, "MOND", ml, vmw, A0_DERIVED)[0]; s = D.score(ds, "SCR", ml, vmw, A0_DERIVED)[0]
        out["dwarfs"][f"V{vmw}_ML{ml}"] = {"MOND": m, "screened": s, "delta": s - m}
        print(f"dwarfs V={vmw} M/L={ml}: MOND {m:6.1f}  screened {s:6.1f}  delta {s-m:+6.1f}")
E.S = S2
import environment_screening_pergalaxy as P   # runs its own comparison with E.S = S2 in effect
