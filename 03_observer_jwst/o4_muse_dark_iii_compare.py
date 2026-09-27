#!/usr/bin/env python3
"""O4 with real data: MUSE-DARK III (Ciocan+2026, arXiv:2604.22613) published summary numbers against a0 models.
Uses only the published a0(z) = (1.00+-0.04) + (1.59+-0.10) z and the whole-sample a0(z~1) = 2.38+-0.1 (1e-10 m/s^2)."""
import math
Om, OL = 0.315, 0.685
E = lambda z: math.sqrt(Om*(1+z)**3 + OL)
a_der = 2.998e8*(67.4e3/3.0857e22)/(2*math.pi)/1e-10
zmed, a_obs, s_obs = 0.87, 2.38, 0.10
print("MUSE-DARK III (Ciocan+2026, arXiv:2604.22613): a0(z) = (1.00+-0.04) + (1.59+-0.10) z [1e-10 m/s^2]; whole-sample a0(z~1) = 2.38+-0.1")
print(f"derived a0(0) = cH0/2pi = {a_der:.3f}e-10 (H0=67.4); implied median z = {(2.38-1.00)/1.59:.2f}")
for name, f in [("constant a0", lambda z: 1.0), ("a0 ~ H(z)", E), ("a0 ~ (1+z)^1.5", lambda z: (1+z)**1.5), ("a0 ~ (1+z)^1.3", lambda z: (1+z)**1.3)]:
    pred = a_der*f(zmed)
    print(f"  {name:16s}: a0(z={zmed}) = {pred:.2f}e-10 vs {a_obs}+-{s_obs} -> {(a_obs-pred)/s_obs:+.1f} sigma (stat only)")
