#!/usr/bin/env python3
"""D7 Stage 2, step A': reduce the Cartesian steady-state Lagrangian (derive_steady.py) to axisymmetry about the wind
axis z. The external field must then point along z too.
Axisymmetric content, all functions of (R, z):
  scalars      h00 = S, phi = F;
  vectors      h0i = W_R n_i + W_z z_i,  u_i = U_R n_i + U_z z_i;
  tensor       h_ij = A delta_ij + B n_i n_j + C (n_i z_j + z_i n_j) + D z_i z_j;
with n = (x, y, 0)/R. L2 and Y2 contain fields and first derivatives only, so the density is evaluated in the
half-plane y = 0 (x = R > 0) by the chain rule. There n = (1, 0, 0), and the only surviving derivatives of n are
d_y n_y = 1/R. By SO(2) symmetric criticality the reduced action 2 pi Int L R dR dz gives the correct field equations.
Jet symbols: X, X_R, X_z for each field X in (S, W_R, W_z, A, B, C, D, U_R, U_z, F).
Output: steady_lagrangian_axisym.json with L2 and Y2 as polynomials in the jet symbols, 1/R and v_w.
"""

import json, sys, sympy as sp

sys.path.insert(0, "../d3_alpha")
from sym_json import enc, dec

x, y, z = sp.symbols("x y z", real=True)
Rs = sp.Symbol("R", positive=True)
NAMES = ["S", "W_R", "W_z", "A", "B", "C", "D", "U_R", "U_z", "F"]
J = {n: (sp.Symbol(n), sp.Symbol(n + "_R"), sp.Symbol(n + "_z")) for n in NAMES}


def val(n):
    return J[n][0]


def dR(n):
    return J[n][1]


def dzz(n):
    return J[n][2]


# value and (d_x, d_y, d_z) of each Cartesian component at y = 0, x = R
def scalar(n):
    return val(n), (dR(n), 0, dzz(n))


def vec_x(n):  # n_x * V  at y=0
    return val(n), (dR(n), 0, dzz(n))


def vec_y(n):  # n_y * V: value 0, d_y = V/R
    return 0, (0, val(n) / Rs, 0)


TABLE = {
    "h00": scalar("S"),
    "phi": scalar("F"),
    "h01": vec_x("W_R"),
    "h02": vec_y("W_R"),
    "h03": scalar("W_z"),
    "ux": vec_x("U_R"),
    "uy": vec_y("U_R"),
    "uz": scalar("U_z"),
    # h_ij = A delta + B n n + C (n z + z n) + D z z
    "h11": (val("A") + val("B"), (dR("A") + dR("B"), 0, dzz("A") + dzz("B"))),
    "h22": (val("A"), (dR("A"), 0, dzz("A"))),
    "h33": (val("A") + val("D"), (dR("A") + dR("D"), 0, dzz("A") + dzz("D"))),
    "h12": (0, (0, val("B") / Rs, 0)),
    "h13": (val("C"), (dR("C"), 0, dzz("C"))),
    "h23": (0, (0, val("C") / Rs, 0)),
}


def reduce(expr):
    """Map the Cartesian jet symbols of steady_lagrangian_v2.json (f, f_x, f_y, f_z) to axisymmetric jets at y = 0."""
    rep = {}
    for s_ in expr.free_symbols:
        nm = s_.name
        if nm == "v_w":
            continue
        base, _, der = nm.rpartition("_")
        if der in ("x", "y", "z") and base in TABLE:
            rep[s_] = TABLE[base][1]["xyz".index(der)]
        else:
            assert nm in TABLE, nm
            rep[s_] = TABLE[nm][0]
    return expr.xreplace(rep)


def main():
    d = json.load(open("steady_lagrangian_v2.json"))
    Lrest, Y = dec(d["Lrest"]), dec(d["Y"])
    La, Ya = reduce(Lrest), reduce(Y)
    left = [s for s in (La.free_symbols | Ya.free_symbols) if s.name in ("x", "y", "z")]
    assert not left, left
    print(f"reduced: Lrest {sp.count_ops(La)} ops, Y {sp.count_ops(Ya)} ops")
    json.dump(
        {"jets": NAMES, "Lrest": enc(La), "Y": enc(Ya)},
        open("steady_lagrangian_axisym.json", "w"),
    )


if __name__ == "__main__":
    main()
