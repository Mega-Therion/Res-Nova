"""Check that Lake roots, the proof gate, and Lean files agree on target scope."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LAKEFILE = ROOT / "lakefile.lean"
GATE = ROOT / "verify_all_proofs.sh"
errors: list[str] = []

lake_text = LAKEFILE.read_text()
roots_block = re.search(r"roots\s*:=\s*#\[(.*?)\n\s*\]", lake_text, re.S)
if not roots_block:
    errors.append("could not find lakefile roots block")
    roots: list[str] = []
else:
    root_lines = [line for line in roots_block.group(1).splitlines() if not line.lstrip().startswith("--")]
    roots = re.findall(r"`([A-Za-z0-9_]+)", "\n".join(root_lines))

gate_text = GATE.read_text()
targets_block = re.search(r"TARGETS=\(\s*(.*?)\n\s*\)", gate_text, re.S)
if not targets_block:
    errors.append("could not find verify_all_proofs.sh TARGETS block")
    targets: list[str] = []
else:
    targets = re.findall(r"([A-Za-z0-9_]+)\.lean", targets_block.group(1))

if sorted(roots) != sorted(targets):
    errors.append("Lake roots and gate targets differ")
    errors.append(f"lake-only: {sorted(set(roots) - set(targets))}")
    errors.append(f"gate-only: {sorted(set(targets) - set(roots))}")

on_disk = sorted(p.stem for p in ROOT.glob("*.lean") if p.name != "lakefile.lean")
if sorted(roots) != on_disk:
    errors.append("Lake roots and on-disk non-configuration Lean modules differ")
    errors.append(f"disk-only: {sorted(set(on_disk) - set(roots))}")
    errors.append(f"missing-on-disk: {sorted(set(roots) - set(on_disk))}")

if errors:
    print("FAIL")
    print("\n".join(f" - {item}" for item in errors))
    sys.exit(1)

print(f"PASS — {len(roots)} Lean targets; lakefile, gate, and on-disk modules agree")
