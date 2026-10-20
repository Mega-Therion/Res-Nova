#!/usr/bin/env python3
"""Exact-Koide texture scan. List frozen before the numerical loop.

N is real symmetric. Koide is (tr N)^2 / (tr N^2) = 3/2.
Scale is fixed by setting the entry named a to 1. One remaining
ratio is scanned on the grid declared below. The other is solved
so that Koide holds to 1e-10. Eigenvalues are taken in absolute
value and sorted. r1 = λ2/λ1, r2 = λ3/λ2.

Textures:
  S2      [[d, a, a], [a, d, t a], [a, t a, d]]
  MUTAU   [[d, a, t a], [a, d, a], [t a, a, d]]
  FRITZ   [[0, a, 0], [a, 0, b], [0, b, c]]     scan b, solve c
  Z1      [[d, a, 0], [a, d, a], [0, a, b]]
  Z2      [[d, 0, a], [0, d, a], [a, a, b]]
  Z3      [[d, a, a], [a, d, 0], [a, 0, b]]
  Z4      [[b, a, 0], [a, d, a], [0, a, d]]
  Z5      [[d, a, 0], [a, b, a], [0, a, d]]
  A4      [[d+a, a, a], [a, d+a, a], [a, a, d+b]]
  NN1     [[d, a, 0], [a, d, t a], [0, t a, d]]
  NN2     [[d, t a, 0], [t a, d, a], [0, a, d]]
  NN3     [[0, a, 0], [a, d, t a], [0, t a, d]]

Scan grid, declared here: the free ratio runs over linspace(-8, 8, 1601).
The solved entry runs over linspace(-40, 40, 801), and every sign change
is refined with brentq. A texture works if both |r/r_obs - 1| are below 0.01
at the same point. Best point is the minimum of the larger of those two.
"""

import json
from pathlib import Path

import numpy as np
from scipy.constants import physical_constants
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
M_E = physical_constants["electron mass"][0]
M_MU = physical_constants["muon mass"][0]
M_TAU = physical_constants["tau mass"][0]
R1_OBS = float(np.sqrt(M_MU / M_E))
R2_OBS = float(np.sqrt(M_TAU / M_MU))
SCAN = np.linspace(-8.0, 8.0, 1601)
SOLVE = np.linspace(-40.0, 40.0, 801)


def koide(N):
    tr2 = float(np.trace(N @ N))
    if tr2 <= 0.0:
        return np.nan
    tr = float(np.trace(N))
    return tr * tr / tr2


def ratios(N):
    ev = np.sort(np.abs(np.linalg.eigvalsh(N)))
    if ev[0] <= 1e-12 * ev[-1]:
        return None
    return float(ev[1] / ev[0]), float(ev[2] / ev[1]), [float(v) for v in ev]


def score(r1, r2):
    e1 = abs(r1 / R1_OBS - 1.0)
    e2 = abs(r2 / R2_OBS - 1.0)
    return max(e1, e2), e1, e2


def build(kind, s, u):
    """s is the scanned ratio, u the solved entry. a = 1."""
    if kind == "S2":
        d, t = u, s
        return np.array([[d, 1, 1], [1, d, t], [1, t, d]], float)
    if kind == "MUTAU":
        d, t = u, s
        return np.array([[d, 1, t], [1, d, 1], [t, 1, d]], float)
    if kind == "FRITZ":
        b, c = s, u
        return np.array([[0, 1, 0], [1, 0, b], [0, b, c]], float)
    if kind == "Z1":
        d, b = u, s
        return np.array([[d, 1, 0], [1, d, 1], [0, 1, b]], float)
    if kind == "Z2":
        d, b = u, s
        return np.array([[d, 0, 1], [0, d, 1], [1, 1, b]], float)
    if kind == "Z3":
        d, b = u, s
        return np.array([[d, 1, 1], [1, d, 0], [1, 0, b]], float)
    if kind == "Z4":
        d, b = u, s
        return np.array([[b, 1, 0], [1, d, 1], [0, 1, d]], float)
    if kind == "Z5":
        d, b = u, s
        return np.array([[d, 1, 0], [1, b, 1], [0, 1, d]], float)
    if kind == "A4":
        d, b = u, s
        return np.array([[d + 1, 1, 1], [1, d + 1, 1], [1, 1, d + b]], float)
    if kind == "NN1":
        d, t = u, s
        return np.array([[d, 1, 0], [1, d, t], [0, t, d]], float)
    if kind == "NN2":
        d, t = u, s
        return np.array([[d, t, 0], [t, d, 1], [0, 1, d]], float)
    if kind == "NN3":
        d, t = u, s
        return np.array([[0, 1, 0], [1, d, t], [0, t, d]], float)
    raise KeyError(kind)


def best(kind):
    found = None
    n_roots = 0
    for s in SCAN:
        vals = []
        good = []
        for u in SOLVE:
            q = koide(build(kind, s, u))
            if np.isfinite(q):
                vals.append(q - 1.5)
                good.append(u)
            else:
                vals.append(np.nan)
                good.append(u)
        vals = np.array(vals)
        for i in range(len(vals) - 1):
            a, b = vals[i], vals[i + 1]
            if not np.isfinite(a) or not np.isfinite(b) or a == 0.0 or a * b > 0.0:
                continue
            u0, u1 = good[i], good[i + 1]
            try:
                u = brentq(lambda z, s=s: koide(build(kind, s, z)) - 1.5, u0, u1)
            except ValueError:
                continue
            N = build(kind, s, u)
            if abs(koide(N) - 1.5) > 1e-8:
                continue
            got = ratios(N)
            if got is None:
                continue
            r1, r2, ev = got
            mx, e1, e2 = score(r1, r2)
            n_roots += 1
            row = {
                "scan": float(s),
                "solved": float(u),
                "r1": r1,
                "r2": r2,
                "e1": e1,
                "e2": e2,
                "max_rel": mx,
                "works": bool(e1 < 0.01 and e2 < 0.01),
                "eigen_abs": ev,
                "koide": float(koide(N)),
            }
            if found is None or mx < found["max_rel"]:
                found = row
    if found is not None:
        found["n_exact_koide_points"] = n_roots
    return found


def main():
    q_mass = (M_E + M_MU + M_TAU) / (np.sqrt(M_E) + np.sqrt(M_MU) + np.sqrt(M_TAU)) ** 2
    kinds = [
        "S2",
        "MUTAU",
        "FRITZ",
        "Z1",
        "Z2",
        "Z3",
        "Z4",
        "Z5",
        "A4",
        "NN1",
        "NN2",
        "NN3",
    ]
    rows = {}
    print(f"observed r1={R1_OBS:.6f} r2={R2_OBS:.6f} Q={q_mass:.8f}", flush=True)
    for kind in kinds:
        row = best(kind)
        rows[kind] = row
        if row is None:
            print(kind, "NO_EXACT_KOIDE", flush=True)
        else:
            print(
                f"{kind} scan={row['scan']:.4f} solved={row['solved']:.4f} "
                f"r1={row['r1']:.4f} r2={row['r2']:.4f} "
                f"e1={row['e1']:.4e} e2={row['e2']:.4e} works={row['works']}",
                flush=True,
            )
    # Muse's quoted t, solved for d, not used to choose the grid.
    muse = []
    for kind, t in (("S2", 1.775), ("MUTAU", 1.775)):
        for i in range(len(SOLVE) - 1):
            q0 = koide(build(kind, t, SOLVE[i]))
            q1 = koide(build(kind, t, SOLVE[i + 1]))
            if (
                not np.isfinite(q0)
                or not np.isfinite(q1)
                or (q0 - 1.5) * (q1 - 1.5) > 0
            ):
                continue
            u = brentq(
                lambda z, kind=kind, t=t: koide(build(kind, t, z)) - 1.5,
                SOLVE[i],
                SOLVE[i + 1],
            )
            got = ratios(build(kind, t, u))
            if got is None:
                continue
            r1, r2, ev = got
            mx, e1, e2 = score(r1, r2)
            muse.append(
                {
                    "texture": kind,
                    "t": t,
                    "d": u,
                    "r1": r1,
                    "r2": r2,
                    "e1": e1,
                    "e2": e2,
                    "max_rel": mx,
                }
            )
    out = {
        "r1_obs": R1_OBS,
        "r2_obs": R2_OBS,
        "Q_codata": float(q_mass),
        "Q_target": 2.0 / 3.0,
        "bar": "both relative errors below 0.01, Koide exact",
        "scan": [-8.0, 8.0, 1601],
        "solve": [-40.0, 40.0, 801],
        "textures": rows,
        "muse_t_1_775": muse,
        "n_works": int(sum(1 for v in rows.values() if v and v["works"])),
    }
    path = HERE / "KOIDE_TEXTURE_SCAN.json"
    path.write_text(json.dumps(out, indent=1) + "\n")
    print("works", out["n_works"], "wrote", path)


if __name__ == "__main__":
    main()
