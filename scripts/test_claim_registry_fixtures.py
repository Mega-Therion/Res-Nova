#!/usr/bin/env python3
"""Exercise validate_claim_registry.validate() against fixed valid/invalid fixtures.

Not a pytest suite -- follows this repo's script-based check convention
(scripts/check_claim_consistency.py, scripts/validate_claim_registry.py) so it
slots into local_gate.sh and verify.yml the same way. Exit 0 means every
fixture behaved as its filename promises; exit 1 prints which one didn't.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_claim_registry import validate  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "assurance" / "fixtures"

CASES = [
    ("valid_minimal.json", True),
    ("invalid_missing_fields.json", False),
    ("invalid_status_upgrade.json", False),
    ("valid_open_and_retracted.json", True),
]

failures: list[str] = []

for name, should_pass in CASES:
    path = FIXTURES / name
    if not path.is_file():
        failures.append(f"{name}: fixture file missing")
        continue
    payload = json.loads(path.read_text())
    errors = validate(payload, root=ROOT)
    passed = not errors
    if passed != should_pass:
        want = "PASS" if should_pass else "FAIL"
        got = "PASS" if passed else "FAIL"
        detail = "" if passed else f" ({'; '.join(errors)})"
        failures.append(f"{name}: expected {want}, got {got}{detail}")

# Deterministic ordering / stable IDs: re-running validate() on the same
# payload must not reorder or duplicate anything.
main_registry = json.loads((ROOT / "assurance" / "claims.json").read_text())
ids_first = [c["id"] for c in main_registry["claims"]]
ids_second = [
    c["id"]
    for c in json.loads((ROOT / "assurance" / "claims.json").read_text())["claims"]
]
if ids_first != ids_second:
    failures.append("claims.json claim ordering is not stable across reads")
if len(ids_first) != len(set(ids_first)):
    failures.append("claims.json has duplicate claim ids")

if failures:
    print("FAIL")
    for f in failures:
        print(f" - {f}")
    sys.exit(1)

print(
    f"PASS — {len(CASES)} fixtures behaved as expected; {len(ids_first)} live claim ids are stable and unique"
)
