#!/usr/bin/env python3
"""Job F: a0(z) high-z pressure scale test execution.

Executes a0_highz_pressure_scale_test.py via subprocess and captures
the resulting process exit code, stdout path, and numeric outputs
into the standard Argon4 Unidex receipt format.
"""

import json
from pathlib import Path
import subprocess
import sys


def run_job_f():
    base_dir = Path("/home/mega/Chyren/3_research/Res-Nova")
    script_path = base_dir / "scripts/a0_highz_pressure_scale_test.py"
    input_data_path = base_dir / "02_galaxy_dynamics/highz_data/RC100_NestorShachar2023_table3_transcribed.csv"
    out_json_path = base_dir / "02_galaxy_dynamics/A0_HIGHZ_PRESSURE_SCALE_TEST.json"

    receipt_dir = base_dir / "02_galaxy_dynamics/argon4_unidex"
    receipt_file = receipt_dir / "job_f_a0z.json"

    # Check for missing prerequisite inputs
    missing = []
    if not script_path.exists():
        missing.append(str(script_path))
    if not input_data_path.exists():
        missing.append(str(input_data_path))

    if missing:
        receipt = {
            "job": "F",
            "exit_code": 0,
            "verdict": "not_run",
            "tier": "O",
            "neighbor_constrained": "whether test prefers constant or horizon-tied shape",
            "neighbor_forbidden": "anchor a₀ = c H₀ / 2π as theorem, galaxy axiom",
            "free_symbols": [],
            "numeric_outputs": {},
            "script": "job_f_a0z.py",
            "subprocess_exit_code": None,
            "stdout_path": None,
            "missing_path": "; ".join(missing),
        }
        with open(receipt_file, "w", encoding="utf-8") as f:
            json.dump(receipt, f, indent=2)
        print(json.dumps(receipt, indent=2))
        return 0

    # Execute target test script via subprocess
    proc = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        cwd=str(base_dir),
    )

    if proc.returncode != 0:
        receipt = {
            "job": "F",
            "exit_code": 0,
            "verdict": "subprocess_failed",
            "tier": "O",
            "neighbor_constrained": "whether test prefers constant or horizon-tied shape",
            "neighbor_forbidden": "anchor a₀ = c H₀ / 2π as theorem, galaxy axiom",
            "free_symbols": [],
            "numeric_outputs": {},
            "script": "job_f_a0z.py",
            "subprocess_exit_code": proc.returncode,
            "stdout_path": None,
            "missing_path": None,
            "error_stderr": proc.stderr[:500] if proc.stderr else "",
        }
        with open(receipt_file, "w", encoding="utf-8") as f:
            json.dump(receipt, f, indent=2)
        print(json.dumps(receipt, indent=2))
        return 0

    # Parse numeric outputs from stdout or output file
    numeric_outputs = {}
    stdout_cleaned = proc.stdout.strip()
    if stdout_cleaned:
        try:
            numeric_outputs = json.loads(stdout_cleaned)
        except json.JSONDecodeError:
            if out_json_path.exists():
                with open(out_json_path, "r", encoding="utf-8") as f:
                    numeric_outputs = json.load(f)
    elif out_json_path.exists():
        with open(out_json_path, "r", encoding="utf-8") as f:
            numeric_outputs = json.load(f)

    receipt = {
        "job": "F",
        "exit_code": 0,
        "verdict": "a0z_test_complete",
        "tier": "D",
        "neighbor_constrained": "whether test prefers constant or horizon-tied shape",
        "neighbor_forbidden": "anchor a₀ = c H₀ / 2π as theorem, galaxy axiom",
        "free_symbols": [],
        "numeric_outputs": numeric_outputs,
        "script": "job_f_a0z.py",
        "subprocess_exit_code": proc.returncode,
        "stdout_path": str(out_json_path),
        "missing_path": None,
    }

    with open(receipt_file, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(run_job_f())
