#!/usr/bin/env python3
"""Oort population under the Galactic tide, stellar impulses, and the shell shift.

The tide is the same McMillan field as oort_torque_proxy.g_tide. Stellar
impulses use a fixed encounter model, written here before the run:
n = 0.1 pc^-3, M = 0.5 Msun, v = 40 km/s, b drawn with area weight up to
2e4 au. The shell does not torque (the radial g_W of screened_c_solutions);
it shifts the osculating 1/a by the Phi term already measured in
COMET_C_WINDOW.json. A comet is counted when q drops below 10 au.
This is not the VNT AQUAL integrator.

Writes COMET_POPULATION_C_WINDOW.json.
"""

import json
from pathlib import Path

import numpy as np

import oort_torque_proxy as O

HERE = Path(__file__).resolve().parent
AU, KAU, GM = O.AU, O.KAU, O.GM
YEAR = 365.25 * 86400.0
N = 640
MAX_ORBITS = 80
NE = 48
Q_OBS = 10.0 * AU
B_MAX = 2.0e4 * AU
B_MIN = 5.0e2 * AU
N_STAR = 0.1 / O.PC**3
M_STAR = 0.5 * O.MSUN
V_STAR = 40e3
SEED = 20261018
# 2*Phi(0)/GM in au^-1, from COMET_C_WINDOW.json. Osculating 1/a gains the negative of this.
PHI_TERM = {
    "newton": 0.0,
    "C0": -0.00013858101948569543,
    "C_centre": -3.162260065088265e-05,
    "C_high": -9.999989931213739e-06,
}


def elements(a, q):
    e = 1.0 - q / a
    return e


def dL_tide(a, e, R):
    """Angular-momentum kick of the Galactic tide over one Kepler orbit. R rotates the orbital frame."""
    E = (np.arange(NE) + 0.5) * 2 * np.pi / NE
    nmean = np.sqrt(GM / a**3)
    pos = np.stack(
        [
            a * (np.cos(E) - e),
            a * np.sqrt(max(1.0 - e * e, 0.0)) * np.sin(E),
            np.zeros(NE),
        ],
        1,
    )
    dt = (1.0 - e * np.cos(E)) / nmean * (2.0 * np.pi / NE)
    X = pos @ R.T
    g = O.g_tide(X)
    return np.einsum("e,ei->i", dt, np.cross(X, g))


def evolve(rng, stars):
    a = np.exp(rng.uniform(np.log(1.0e4 * AU), np.log(1.0e5 * AU), N))
    q = np.exp(rng.uniform(np.log(20.0 * AU), np.log(80.0 * AU), N))
    # Isotropic planes. Perihelion along the rotated x.
    R = O.random_rotations(N, rng)
    alive = np.ones(N, dtype=bool)
    hits = []
    for _step in range(MAX_ORBITS):
        for i in np.where(alive)[0]:
            e = elements(a[i], q[i])
            if e <= 0.0 or e >= 1.0:
                alive[i] = False
                continue
            Lhat = R[i, :, 2]
            Lmag = np.sqrt(GM * a[i] * (1.0 - e * e))
            L = Lhat * Lmag + dL_tide(a[i], e, R[i])
            # Stellar impulse at a random eccentric anomaly.
            period = 2.0 * np.pi * np.sqrt(a[i] ** 3 / GM)
            lam = N_STAR * V_STAR * period * np.pi * B_MAX**2
            nenc = int(rng.poisson(lam)) if stars else 0
            E = rng.uniform(0, 2 * np.pi, nenc) if nenc else []
            for Ek in E:
                b = np.sqrt(B_MIN**2 + (B_MAX**2 - B_MIN**2) * rng.random())
                rvec = R[i] @ np.array(
                    [
                        a[i] * (np.cos(Ek) - e),
                        a[i] * np.sqrt(1 - e * e) * np.sin(Ek),
                        0.0,
                    ]
                )
                vvec = R[i] @ (
                    np.sqrt(GM / (a[i] * (1 - e * e)))
                    * np.array([-np.sin(Ek), np.sqrt(1 - e * e) * np.cos(Ek), 0.0])
                )
                direction = rng.normal(size=3)
                direction -= direction.dot(rvec) * rvec / np.dot(rvec, rvec)
                nrm = np.linalg.norm(direction)
                if nrm == 0.0:
                    continue
                dv = (2.0 * O.T.G * M_STAR / (V_STAR * b)) * direction / nrm
                vvec = vvec + dv
                r = np.linalg.norm(rvec)
                v2 = np.dot(vvec, vvec)
                energy = 0.5 * v2 - GM / r
                if energy >= 0.0:
                    alive[i] = False
                    break
                a[i] = -GM / (2.0 * energy)
                h = np.cross(rvec, vvec)
                L = h
            if not alive[i]:
                continue
            Lmag = np.linalg.norm(L)
            if Lmag == 0.0 or a[i] <= 0.0:
                alive[i] = False
                continue
            h2 = Lmag**2
            if h2 >= GM * a[i]:
                q[i] = a[i]
                e = 0.0
            else:
                e = float(np.sqrt(1.0 - h2 / (GM * a[i])))
                q[i] = a[i] * (1.0 - e)
            Lhat = L / Lmag
            # Keep perihelion direction in the new plane.
            phat = R[i, :, 0]
            phat = phat - Lhat * np.dot(phat, Lhat)
            pn = np.linalg.norm(phat)
            if pn < 1e-12:
                phat = np.array([1.0, 0.0, 0.0])
                phat -= Lhat * np.dot(phat, Lhat)
                phat /= np.linalg.norm(phat)
            else:
                phat = phat / pn
            that = np.cross(Lhat, phat)
            R[i, :, 0], R[i, :, 1], R[i, :, 2] = phat, that, Lhat
            if q[i] < Q_OBS and a[i] > 1.0e3 * AU:
                hits.append(AU / a[i])
                alive[i] = False
            elif q[i] < Q_OBS:
                alive[i] = False
            elif a[i] > 5.0e5 * AU or a[i] < 5.0e2 * AU:
                alive[i] = False
    return np.array(hits) if hits else np.array([])


def summarize(inv_true, phi_term):
    inv = inv_true - phi_term if inv_true.size else inv_true
    aobs = 1.0 / inv if inv.size else np.array([])
    return {
        "n_started": N,
        "n_reached_q10": int(inv_true.size),
        "frac_reached": float(inv_true.size / N),
        "frac_a_1e3_1e4": (
            float(np.mean((aobs >= 1e3) & (aobs < 1e4))) if inv.size else 0.0
        ),
        "frac_a_1e4_1e5": (
            float(np.mean((aobs >= 1e4) & (aobs <= 1e5))) if inv.size else 0.0
        ),
        "frac_below_1e4": float(np.mean(aobs < 1e4)) if inv.size else 0.0,
        "median_a_au": float(np.median(aobs)) if inv.size else None,
        "phi_term_au": phi_term,
    }


def main():
    out = {
        "seed": SEED,
        "n": N,
        "max_orbits": MAX_ORBITS,
        "q_init_au": [20, 80],
        "encounter": {
            "n_pc3": 0.1,
            "M_sun": 0.5,
            "v_km_s": 40.0,
            "b_min_au": B_MIN / AU,
            "b_max_au": B_MAX / AU,
        },
        "models": {},
    }
    for stars in (False, True):
        inv = evolve(np.random.default_rng(SEED), stars)
        tag = "stars" if stars else "tide"
        print(tag, "arrivals", int(inv.size), flush=True)
        for name, phi in PHI_TERM.items():
            row = summarize(inv, phi)
            out["models"][f"{tag}:{name}"] = row
            print(" ", name, row["median_a_au"], row["frac_below_1e4"], flush=True)
    path = HERE / "COMET_POPULATION_C_WINDOW.json"
    path.write_text(json.dumps(out, indent=1) + "\n")
    print("wrote", path)


if __name__ == "__main__":
    main()
