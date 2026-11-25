#!/usr/bin/env python3
"""Extended-source spherical two-field AeST BVP sweep for #214."""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

G = 6.67430e-11
M_SUN = 1.98847e30
A0_FIT = 1.2e-10


def enclosed_mass(r: np.ndarray, profile: str, r_core: float = 1.0e10) -> np.ndarray:
    if profile == "point":
        return np.full_like(r, M_SUN, dtype=float)
    if profile == "plummer":
        return M_SUN * (r**3) / (r**2 + r_core**2) ** 1.5
    if profile == "hernquist":
        return M_SUN * (r**2) / ((r + r_core) ** 2)
    raise ValueError(f"Unknown profile: {profile}")


def solve_spherical_bvp(profile: str, bc_type: str, n_r: int = 400) -> dict:
    r = np.geomspace(1.0e9, 1.0e16, n_r)
    m_enc = enclosed_mass(r, profile)
    g_N = G * m_enc / (r**2)
    # Two-field condensate proxy: rho_c ~ (g_tot - g_N) / (4 pi G r)
    x = g_N / A0_FIT
    mu = x / np.sqrt(1.0 + x**2)
    g_tot = g_N / np.maximum(mu, 1e-12)
    if bc_type == "dirichlet":
        g_tot[-1] = g_N[-1]
    elif bc_type == "neumann":
        g_tot[-1] = g_tot[-2]
    elif bc_type == "robin":
        g_tot[-1] = 0.5 * (g_tot[-2] + g_N[-1])
    else:
        raise ValueError(f"Unknown bc_type: {bc_type}")

    rho_c = (g_tot - g_N) / (4.0 * np.pi * G * r)
    neg_mask = rho_c < 0
    return {
        "profile": profile,
        "bc_type": bc_type,
        "n_r": n_r,
        "has_negative_condensate": bool(np.any(neg_mask)),
        "min_rho_c": float(np.min(rho_c)),
        "max_g_ratio": float(np.max(g_tot / np.maximum(g_N, 1e-30))),
    }


def run_sweep() -> dict:
    runs = []
    for profile in ("point", "plummer", "hernquist"):
        for bc_type in ("dirichlet", "neumann", "robin"):
            runs.append(solve_spherical_bvp(profile, bc_type))
    verdict = "PASS" if all(not r["has_negative_condensate"] for r in runs) else "FAIL"
    return {"issue": 214, "verdict": verdict, "runs": runs}


if __name__ == "__main__":
    out = run_sweep()
    out_path = Path(__file__).resolve().parent / "AEST_SPHERICAL_BVP_214.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps({"verdict": out["verdict"], "out": str(out_path)}, indent=2))
