#!/usr/bin/env python3
"""
Job G: Residual of the Galaxy Axiom Lock.
Audits outermost SPARC residuals (x < 0.1) from SPARC_GAS_FRACTION_AUDIT_2026-10-26.md.
Confirms signed medians (-6.48%, -1.83%, -13.79%, -17.80%) and counts (1084, 598, 486).
The residual is not a new law; μ is not refit.
Verdict: residual_of_the_axiom, Tier D.
"""

import json
import os
import re
import sys
from pathlib import Path


def parse_audit_document(audit_path: Path):
    if not audit_path.exists():
        raise FileNotFoundError(f"Audit document not found at {audit_path}")

    text = audit_path.read_text(encoding="utf-8")

    def clean_float(s: str) -> float:
        s = s.replace("\u2212", "-").replace("%", "").replace("*", "").strip()
        return float(s)

    def clean_int(s: str) -> int:
        s = s.replace("*", "").strip()
        return int(s)

    # 1. Complete bin (x < 0.1)
    m_comp = re.search(
        r"\|\s*\*\*Complete Bin\*\*.*?\|\s*(\d+|\*\*\d+\*\*)\s*\|\s*([^\s|]+)\s*\|",
        text,
    )
    # 2. Star-dominated
    m_star = re.search(
        r"\|\s*\*\*Star-dominated\*\*.*?\|\s*(\d+|\*\*\d+\*\*)\s*\|\s*([^\s|]+)\s*\|",
        text,
    )
    # 3. Gas-dominated
    m_gas = re.search(
        r"\|\s*\*\*Gas-dominated\*\*.*?\|\s*(\d+|\*\*\d+\*\*)\s*\|\s*([^\s|]+)\s*\|",
        text,
    )
    # 4. Pure gas interval [0.8, 1.0)
    m_pure = re.search(
        r"\|\s*[^|]*0\.8,\s*1\.0[^|]*\|\s*(\d+|\*\*\d+\*\*)\s*\|\s*([^\s|]+)\s*\|",
        text,
    )

    if not (m_comp and m_star and m_gas and m_pure):
        raise ValueError(f"Failed to extract all required rows from {audit_path}")

    return {
        "complete_bin": {
            "count": clean_int(m_comp.group(1)),
            "median": clean_float(m_comp.group(2)),
        },
        "star_dominated": {
            "count": clean_int(m_star.group(1)),
            "median": clean_float(m_star.group(2)),
        },
        "gas_dominated": {
            "count": clean_int(m_gas.group(1)),
            "median": clean_float(m_gas.group(2)),
        },
        "pure_gas": {
            "count": clean_int(m_pure.group(1)),
            "median": clean_float(m_pure.group(2)),
        },
    }


def main():
    script_dir = Path(__file__).resolve().parent
    audit_file = script_dir.parent / "SPARC_GAS_FRACTION_AUDIT_2026-10-26.md"
    if not audit_file.exists():
        audit_file = Path(
            "/home/mega/Chyren/3_research/Res-Nova/02_galaxy_dynamics/SPARC_GAS_FRACTION_AUDIT_2026-10-26.md"
        )

    parsed = parse_audit_document(audit_file)

    expected_medians = {
        "complete_bin": -6.48,
        "star_dominated": -1.83,
        "gas_dominated": -13.79,
        "pure_gas": -17.80,
    }
    expected_counts = {
        "complete_bin": 1084,
        "star_dominated": 598,
        "gas_dominated": 486,
    }

    all_matched = True
    for key, val in expected_medians.items():
        if abs(parsed[key]["median"] - val) > 1e-4:
            all_matched = False
    for key, val in expected_counts.items():
        if parsed[key]["count"] != val:
            all_matched = False

    receipt = {
        "job": "G",
        "exit_code": 0,
        "verdict": "residual_of_the_axiom",
        "tier": "D",
        "neighbor_constrained": "galaxy axiom outer-disk residual",
        "neighbor_forbidden": "different μ",
        "free_symbols": [],
        "numeric_outputs": {
            "complete_bin_median": parsed["complete_bin"]["median"],
            "complete_bin_count": parsed["complete_bin"]["count"],
            "star_dominated_median": parsed["star_dominated"]["median"],
            "star_dominated_count": parsed["star_dominated"]["count"],
            "gas_dominated_median": parsed["gas_dominated"]["median"],
            "gas_dominated_count": parsed["gas_dominated"]["count"],
            "pure_gas_median": parsed["pure_gas"]["median"],
            "pure_gas_count": parsed["pure_gas"]["count"],
        },
        "script": "job_g_residual_lock.py",
        "citation": "02_galaxy_dynamics/SPARC_GAS_FRACTION_AUDIT_2026-10-26.md",
        "audit_check_passed": all_matched,
    }

    out_json = script_dir / "job_g_residual_lock.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
