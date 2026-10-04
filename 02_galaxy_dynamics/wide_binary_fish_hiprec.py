"""Pre-registered wide-binary fish test, RV-fixed sample, with 8x the Monte Carlo
draws for templates and model curves (precision-only change, same statistic).
Usage: python3 wide_binary_fish_hiprec.py <npz> <seed> <out.json>
"""

import sys

import numpy as np

import wide_binary_fish as F

_sim = F.simulate


def simulate8(b, model, nmc=F.NMC, noise=True):
    return _sim(b, model, nmc=nmc if nmc == 1 else nmc * 8, noise=noise)


F.simulate = simulate8
F.RNG = np.random.default_rng(int(sys.argv[2]))
F.main(sys.argv[1], sys.argv[3])
