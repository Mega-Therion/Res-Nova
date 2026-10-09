#!/usr/bin/env python3
"""Lower bound on sigma(dR) if the control bin is shared by both arms: the control term in
sigma_R is at most the 2-5 kAU sigma_R (0.007), so sigma_test >= sqrt(sigma_R^2 - 0.007^2)."""
import numpy as np
sR = np.array([0.017, 0.023, 0.086]); sc = 0.007
st = np.sqrt(sR**2 - sc**2); sd = 2 * st
scomb = 1 / np.sqrt(np.sum(1 / sd**2))
print("sigma_test", np.round(st, 4), "sigma_dR floor per bin", np.round(sd, 4), f"combined floor {scomb:.4f}; Gate-1 2sigma needs dR >= {2*scomb:.4f}")
for lab, d in (("QUMOND sky-split Q", 0.0099), ("prereg AQUAL sky-split noQ", 0.0154), ("ceiling theta 0 vs 90, Q", 0.0346), ("ceiling noQ prereg K", 0.0551)):
    print(f"  {lab:28s} dR={d:.4f} -> z <= {d/scomb:.2f}")
