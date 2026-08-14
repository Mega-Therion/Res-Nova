#!/usr/bin/env python3
import subprocess, json
from pathlib import Path

MODULES = [
    "SOCasimirGenuine.lean",
    "DeSitterExtremal.lean",
    "MuProjection.lean",
    "ITActionClosure.lean",
    "YettParadigm.lean",
    "SovereignRegularity.lean",
    "GODActionKinematics.lean"
]

ROOT_DIR = Path("/home/mega/grand_monograph/05_lean_formalization")
LAKE_DIR = Path("/home/mega/Chyren/Research_and_Data/03_Formal_and_Lean/formal")

results = []

for mod in MODULES:
    fpath = ROOT_DIR / mod
    cmd = ["lake", "env", "lean", str(fpath)]
    p = subprocess.run(cmd, cwd=str(LAKE_DIR), capture_output=True, text=True)
    
    # Check axioms
    axiom_lines = [l for l in p.stdout.splitlines() if "depends on axioms:" in l]
    
    results.append({
        "module": mod,
        "exit_code": p.returncode,
        "stdout": p.stdout,
        "stderr": p.stderr,
        "axioms": axiom_lines
    })
    print(f"[{'PASS' if p.returncode == 0 else 'FAIL'}] {mod} (exit {p.returncode})")

out_file = Path("/home/mega/grand_monograph/VERIFICATION_RUN_002/01_lean/LEAN_BUILD_RAW.json")
out_file.write_text(json.dumps(results, indent=2))
print("Saved raw Lean build output to", out_file)
