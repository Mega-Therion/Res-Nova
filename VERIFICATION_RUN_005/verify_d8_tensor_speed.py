#!/usr/bin/env python3
"""
Target D8 & D8b: Verification of Disformal Null Cone Split, PPN alpha_1, and GW170817 Falsification
Author: Ryan W. Yett (ORCID: 0009-0001-1303-7190)
Date: 2026-08-14
"""

import sympy as sp
import numpy as np
import json
import hashlib

def run_verification():
    K, phi = sp.symbols('K phi', real=True)
    
    # 1. Maxwellian vector action matching: c13 vanishes identically
    c1_val = K / 2
    c3_val = -K / 2
    c13 = c1_val + c3_val
    c_T_g = sp.sqrt(1 / (1 - c13))
    
    # 2. Foster-Jacobson alpha_1
    alpha_1 = -8 * ((-K/2)**2 + 0) / (2*(K/2) - (K/2)**2 + (-K/2)**2)
    alpha_1_simplified = sp.simplify(alpha_1)
    
    # 3. Disformal photon coordinate speed
    A = sp.exp(-2*phi)
    B = -2*sp.sinh(2*phi)
    c_gamma_sq = (A - B) / A
    c_gamma = sp.sqrt(sp.simplify(c_gamma_sq))
    
    # 4. Speed ratio
    speed_ratio = c_T_g / c_gamma
    speed_diff = sp.Abs(speed_ratio - 1)
    
    # Numerical evaluation for deep-MOND halo (phi = 1e-6) and cosmological (phi = 0.1)
    diff_halo = float(speed_diff.subs(phi, 1e-6))
    diff_cosmo = float(speed_diff.subs(phi, 0.1))
    
    report = {
        "target": "D8 & D8b",
        "title": "Disformal Cone Split & GW170817 Confrontation",
        "c13_identity": str(c13),
        "c_T_Einstein_frame": str(c_T_g),
        "foster_jacobson_alpha_1": str(alpha_1_simplified),
        "c_gamma_physical_frame": str(c_gamma),
        "speed_ratio": str(speed_ratio),
        "gw170817_bound": 1e-15,
        "eval_phi_1e_6_halo": {
            "phi": 1e-6,
            "deviation": diff_halo,
            "gw170817_satisfied": bool(diff_halo <= 1e-15)
        },
        "eval_phi_0_1_cosmo": {
            "phi": 0.1,
            "deviation": diff_cosmo,
            "gw170817_satisfied": bool(diff_cosmo <= 1e-15)
        },
        "verdict": "DISFORMAL MAP FALSIFIED [P] (c_T != c_gamma for phi != 0)"
    }
    
    out_json = "/home/mega/grand_monograph/VERIFICATION_RUN_005/TENSOR_SPEED_EVALUATION.json"
    with open(out_json, "w") as f:
        json.dump(report, f, indent=2)
        
    manifest = {
        "run_id": "VERIFICATION_RUN_005_v2",
        "description": "Target D8b Disformal Null Cone Evaluation and Lean Proof Manifest",
        "artifacts": {
            "TENSOR_SPEED_EVALUATION.json": hashlib.sha256(open(out_json, "rb").read()).hexdigest(),
            "TensorSpeed.lean": hashlib.sha256(open("/home/mega/grand_monograph/05_lean_formalization/TensorSpeed.lean", "rb").read()).hexdigest(),
            "TARGET_D8_TENSOR_SPEED.md": hashlib.sha256(open("/home/mega/grand_monograph/TARGET_D8_TENSOR_SPEED.md", "rb").read()).hexdigest()
        }
    }
    
    with open("/home/mega/grand_monograph/VERIFICATION_RUN_005/manifest_run_005.json", "w") as f:
        json.dump(manifest, f, indent=2)
        
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    run_verification()
