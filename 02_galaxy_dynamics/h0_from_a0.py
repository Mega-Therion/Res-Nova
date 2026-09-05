#!/usr/bin/env python3
"""H0 determined from the SPARC a0 measurement via a0 = c H0 / 2pi.

Section III.1 of FIG_TREE_MONOGRAPH.md. Regenerates every number printed there,
so the claim can be rechecked rather than trusted.

The relation is an equality and may be read from either end. Read forward it is
weak -- a0 lands anywhere across the H0 tension interval. Read backward it turns
the galaxy-dynamics measurement into an independent H0 probe with no CMB and no
distance ladder in it.
"""
import math
from scipy import constants as k

C = k.c                              # exact by SI definition, m/s
MPC = 3.0856775814913673e22          # m, IAU
A0, S_STAT, S_SYST = 1.116e-10, 0.128e-10, 0.097e-10   # SPARC, 171 galaxies
PLANCK, SHOES = 67.4, 73.0

kms_mpc = lambda h_si: h_si * MPC / 1000.0
si      = lambda h_kms: h_kms * 1000.0 / MPC


def a0_from_H0(h_kms):
    return C * si(h_kms) / (2 * math.pi)


def H0_from_a0(a0):
    return kms_mpc(2 * math.pi * a0 / C)


def main():
    sig = math.hypot(S_STAT, S_SYST)
    print("forward (weak: brackets, does not predict)")
    for name, h in (("Planck 2018", PLANCK), ("SH0ES", SHOES)):
        print(f"  a0(H0={h:5.1f}) [{name:11s}] = {a0_from_H0(h)*1e10:.4f}e-10 m/s^2")

    h0 = H0_from_a0(A0)
    s_h0 = h0 * sig / A0
    print(f"\ninverse (a determination)\n  H0 = 2*pi*a0/c = {h0:.2f} +/- {s_h0:.2f} km/s/Mpc")
    for name, v in (("Planck", PLANCK), ("SH0ES", SHOES)):
        print(f"  {(h0-v)/s_h0:+.2f} sigma from {name}")

    # 2-sigma separation of the two camps
    need_h0 = (SHOES - PLANCK) / 4.0
    need_rel = need_h0 / h0
    cur_rel = sig / A0
    print(f"\nfalsifiability target\n  need sigma_H0 < {need_h0:.2f}  =>  sigma_a0/a0 < {100*need_rel:.2f}%")
    print(f"  current sigma_a0/a0 = {100*cur_rel:.2f}%  ->  {cur_rel/need_rel:.1f}x improvement required")

    assert abs(a0_from_H0(h0) - A0) / A0 < 1e-12, "round trip must be exact"
    print("\nround trip a0 -> H0 -> a0 exact to 1e-12: OK")


if __name__ == "__main__":
    main()
