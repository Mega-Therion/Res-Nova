#!/usr/bin/env python3
"""Run the D7 C1 steady solver on one dwarf and print the residual.

This does not select an AeST branch. The discretization gates that pass, and the
two that fail, are recorded in README.md. Default grid is the 16x32 isolated
dwarf at 100 km/s, which the box sweep already converged.

Exit 0 only when Newton reaches the requested tolerance.
"""

import argparse
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import solve_c1 as C
from stage_c_continuation import observables

C_KMS = 299792.458


def dwarf():
    vf = 10.0 / C_KMS
    b = 3e-4
    mass = 12 * math.pi * vf**4 / C.A0T
    return mass, b, vf


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--nR", type=int, default=16)
    p.add_argument("--nz", type=int, default=32)
    p.add_argument("--box-kpc", type=float, default=30.0)
    p.add_argument("--v-kms", type=float, default=100.0)
    p.add_argument("--ge-a0", type=float, default=0.0)
    p.add_argument("--tol", type=float, default=1e-10)
    p.add_argument("--maxit", type=int, default=40)
    args = p.parse_args()
    mass, b, vf = dwarf()
    box = args.box_kpc * 10.0  # stage-2 length unit: 1 = 0.1 kpc
    g_e = args.ge_a0 * C.A0T
    t0 = time.time()
    g, P0, xs, gn0 = C.static_solution(
        args.nR,
        args.nz,
        mass,
        b,
        g_e,
        box,
        tol=args.tol,
        maxit=args.maxit,
        verbose=True,
    )
    print(f"static residual {gn0:.3e}", flush=True)
    rho = C.plummer_fn(mass, b)
    P = C.ProblemC1(g, args.v_kms / C_KMS, rho, g_e)
    x, ok, gn = P.newton(xs, tol=args.tol, maxit=args.maxit, verbose=True)
    ref = observables(P0, xs)
    ob = observables(P, x)
    k = "0.3kpc"
    print(
        f"wind v={args.v_kms:g} km/s box={args.box_kpc:g} kpc grid={args.nR}x{args.nz} "
        f"converged={ok} residual={gn:.3e} "
        f"g/g_static={ob[k]['g'] / ref[k]['g']:.6f} "
        f"Y/Y_static={ob[k]['Y'] / ref[k]['Y']:.6f} "
        f"seconds={time.time() - t0:.0f}",
        flush=True,
    )
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
