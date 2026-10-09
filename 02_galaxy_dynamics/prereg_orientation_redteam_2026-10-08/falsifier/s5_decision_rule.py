#!/usr/bin/env python3
"""Item 4: logic of the Gate-2 decision rule.  z = dR/sigma, e = E-prediction/sigma.
A: z >= 3 and 'consistent with E' (|z-e| <= k)              -> favors E
B: 'consistent with 0' and z <= e-2                         -> disfavors E
C: anything else                                            -> inconclusive
'consistent with' is not defined in the file; k and one/two-sidedness are free."""
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

def regions(z, e, k=2.0, sided="two", sE=0.0):
    st = np.sqrt(1 + sE**2)  # sigma incl. prediction uncertainty (in units of sigma)
    A = (z >= 3) and (abs(z - e) <= k * st)
    c0 = (abs(z) <= k) if sided == "two" else (z < 3)
    B = c0 and ((e - z) >= 2 * st)
    return ("A" if A else "") + ("B" if B else "") or "C"

cases = [  # (label, z, e, k, sided, sE)
    ("k=3 two-sided", 3.0, 5.5, 3, "two", 0),
    ("k=2 two-sided", 3.0, 5.5, 2, "two", 0),
    ("one-sided, negative dR", -4.0, 3.0, 2, "one", 0),
    ("two-sided, negative dR", -4.0, 3.0, 2, "two", 0),
    ("dR >> E (S and E both off)", 9.0, 4.0, 2, "two", 0),
    ("meas.-only sigma", 1.8, 4.0, 2, "two", 0),
    ("sigma incl. 15% E-uncertainty", 1.8, 4.0, 2, "two", 0.15 * 4.0),
    ("e at my upper bound 0.37", 2.5, 0.37, 2, "two", 0),
]
for lab, z, e, k, sd, sE in cases:
    print(f"{lab:32s} z={z:+5.2f} e={e:4.2f} k={k} {sd}-sided sE={sE:.2f} -> region {regions(z, e, k, sd, sE)}")

print("\nA is non-empty only if e + k >= 3 (two-sided k):", {k: f"e >= {3-k}" for k in (1, 2, 3)})
print("A and B overlap only if k >= 3 (two-sided) -- then e.g. z=3, 5<=e<=6 is both")

def probs(e, k):
    pAE = max(0.0, norm.cdf(k) - norm.cdf(max(3 - e, -k))) if e + k >= 3 else 0.0   # z~N(e,1), z in [max(3,e-k), e+k]
    lo, hi = -k, min(k, e - 2)
    pBE = max(0.0, norm.cdf(hi - e) - norm.cdf(lo - e)) if hi > lo else 0.0
    pBS = max(0.0, norm.cdf(hi) - norm.cdf(lo)) if hi > lo else 0.0                 # z~N(0,1)
    pAS = max(0.0, norm.cdf(e + k) - norm.cdf(max(3, e - k))) if e + k >= 3 else 0.0
    return pAE, pBE, pBS, pAS

print("\n  e    k | P(A|E)  P(B|E)  P(B|S)  P(A|S)")
for k in (1, 2):
    for e in (0.37, 1.0, 2.0, 2.5, 3.0, 4.0, 5.0):
        print(f" {e:4.2f}  {k} | " + "  ".join(f"{p:.4f}" for p in probs(e, k)))
for k in (1, 2):
    for target in (0.8, 0.9, 0.95):
        f = lambda e: probs(e, k)[0] - target
        try:
            print(f"k={k}: P(A|E)={target} needs e = {brentq(f, 3 - k + 1e-9, 12):.3f}")
        except ValueError:
            print(f"k={k}: P(A|E)={target} unreachable (max P(A|E)={norm.cdf(k)-norm.cdf(-k):.3f})")
print(f"one-sided 3 sigma p = {norm.sf(3):.5f}; one-sided 2 sigma p = {norm.sf(2):.5f}")
