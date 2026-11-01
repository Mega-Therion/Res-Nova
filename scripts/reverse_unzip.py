#!/usr/bin/env python3
"""Reverse compressor for one lossy projection, plus two declared parity checks.

New construction, 2026-10-31. It does not read or write the galaxy axiom,
the seam mass, or a variational free-energy identification with either.

Zip is a projection. Unzip is the minimum-norm completion of that
projection under a standard normal prior. That completion is the mode of
the variational free energy for a deterministic recognition density.
A coordinate the projection deletes stays at the prior. Inventing it
raises the energy.

The parity rows below are literals. They are fixed from the screen before
any observation or residual is formed. A row is not chosen after the score.
"""

from __future__ import annotations

import json

import numpy as np

# Declared before any score. The blind row is in the row-span of the screen
# and has a zero on z. The seeing row is the deleted coordinate. Do not
# replace either row with one picked from a residual.
P_BLIND = np.array([[1.0, 0.0, 0.0]])
P_SEE = np.array([[0.0, 0.0, 1.0]])


def energy(s: np.ndarray, o: np.ndarray, H: np.ndarray, sigma2: float) -> float:
    """Joint energy of N(0, I) prior and N(H s, sigma2 I) likelihood. Constants dropped."""
    resid = o - H @ s
    return 0.5 * float(s @ s) + 0.5 / sigma2 * float(resid @ resid)


def unzip(o: np.ndarray, H: np.ndarray, sigma2: float) -> np.ndarray:
    """Mode of the free energy. Lost directions remain at the prior mean 0."""
    prec = np.eye(H.shape[1]) + (1.0 / sigma2) * (H.T @ H)
    rhs = (1.0 / sigma2) * (H.T @ o)
    return np.linalg.solve(prec, rhs)


def row_span_distance(row: np.ndarray, screen: np.ndarray) -> float:
    """Squared distance from a row to the row-span of the screen."""
    coeff, _, _, _ = np.linalg.lstsq(screen.T, row.reshape(-1), rcond=None)
    diff = row.reshape(-1) - screen.T @ coeff
    return float(diff @ diff)


def score_parity(
    name: str,
    parity: np.ndarray,
    true: np.ndarray,
    screen: np.ndarray,
    sigma2: float,
) -> dict:
    """Stack a declared parity row under the screen and score that stack.

    The lost-coordinate probe writes the true deleted value into a copy of
    the mode. It does not choose the parity row.
    """
    stacked = np.vstack([screen, parity])
    observed = stacked @ true
    mode = unzip(observed, stacked, sigma2)
    invented = mode.copy()
    invented[2] = true[2]
    e_mode = energy(mode, observed, stacked, sigma2)
    e_invented = energy(invented, observed, stacked, sigma2)
    singular = np.linalg.svd(stacked, compute_uv=False)
    rank = int(np.sum(singular > 1e-8))
    return {
        "name": name,
        "P": parity.tolist(),
        "z_coefficient": float(parity[0, 2]),
        "distance_to_screen_row_span": row_span_distance(parity, screen),
        "stack": stacked.tolist(),
        "singular_values": singular.tolist(),
        "rank": rank,
        "nullity": int(stacked.shape[1] - rank),
        "observation": observed.tolist(),
        "unzip": mode.tolist(),
        "energy_at_unzip": e_mode,
        "energy_if_lost_coordinate_invented": e_invented,
        "energy_penalty_for_inventing": e_invented - e_mode,
    }


def main() -> None:
    sigma2 = 1e-6
    true = np.array([1.0, 2.0, 3.0])
    # One screen: keep x and y, delete z.
    H = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])

    blind_distance = row_span_distance(P_BLIND, H)
    see_distance = row_span_distance(P_SEE, H)
    if blind_distance > 1e-18:
        raise SystemExit(f"blind row left the screen span: {blind_distance}")
    if see_distance < 1e-8:
        raise SystemExit(f"seeing row stayed in the screen span: {see_distance}")

    o = H @ true
    m = unzip(o, H, sigma2)
    invented = m.copy()
    invented[2] = true[2]

    # Second view, chosen, not derived: the screen now also records z.
    H2 = np.eye(3)
    o2 = H2 @ true
    m2 = unzip(o2, H2, sigma2)

    blind = score_parity("blind_to_z", P_BLIND, true, H, sigma2)
    see = score_parity("sees_z", P_SEE, true, H, sigma2)

    receipt = {
        "construction": "reverse_unzip",
        "status": "new",
        "sigma2": sigma2,
        "true_state": true.tolist(),
        "parity_rows_declared_before_score": {
            "blind_to_z": P_BLIND.tolist(),
            "sees_z": P_SEE.tolist(),
            "chosen_from_residual": False,
        },
        "one_view": {
            "observation": o.tolist(),
            "unzip": m.tolist(),
            "lost_coordinate": 2,
            "energy_at_unzip": energy(m, o, H, sigma2),
            "energy_if_lost_coordinate_invented": energy(invented, o, H, sigma2),
            "energy_penalty_for_inventing": energy(invented, o, H, sigma2)
            - energy(m, o, H, sigma2),
        },
        "second_view_supplied": {
            "observation": o2.tolist(),
            "unzip": m2.tolist(),
            "energy": energy(m2, o2, H2, sigma2),
        },
        "parity_checks": {
            "blind_to_z": blind,
            "sees_z": see,
        },
    }
    print(json.dumps(receipt, indent=2))

    problems: list[str] = []
    if abs(blind["unzip"][2]) > 1e-8:
        problems.append(f"blind unzip z = {blind['unzip'][2]}")
    if abs(blind["energy_penalty_for_inventing"] - 4.5) > 1e-9:
        problems.append(f"blind penalty = {blind['energy_penalty_for_inventing']}")
    if abs(see["unzip"][2] - 3.0) > 1e-4:
        problems.append(f"seeing unzip z = {see['unzip'][2]}")
    if not 0.0 <= see["energy_penalty_for_inventing"] < 1e-3:
        problems.append(f"seeing penalty = {see['energy_penalty_for_inventing']}")
    if blind["nullity"] != 1 or see["nullity"] != 0:
        problems.append(f"nullity blind={blind['nullity']} see={see['nullity']}")
    if problems:
        raise SystemExit("parity score failed:\n" + "\n".join(problems))


if __name__ == "__main__":
    main()
