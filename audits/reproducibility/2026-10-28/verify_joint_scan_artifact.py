#!/usr/bin/env python3
"""Check internal row/summary consistency of the committed joint-scan JSON.

This validates the artifact's accounting only. It does not rerun QUMOND or SPARC.
Usage: python3 verify_joint_scan_artifact.py PATH/TO/CASSINI_SPARC_JOINT_SCAN.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

EXPECTED = {
    "a": {"n_rows": 74, "n_admissible_rows": 74, "n_sparc_pass": 2, "n_cassini_pass": 42, "n_joint": 0},
    "b": {"n_rows": 168, "n_admissible_rows": 146, "n_sparc_pass": 0, "n_cassini_pass": 17, "n_joint": 0},
    "c": {"n_rows": 78, "n_admissible_rows": 78, "n_sparc_pass": 18, "n_cassini_pass": 4, "n_joint": 0},
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_path", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.json_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read valid JSON: {exc}")

    rows = payload.get("rows")
    summary = payload.get("summary")
    if not isinstance(rows, list) or not isinstance(summary, dict):
        fail("expected top-level 'rows' list and 'summary' object")

    if payload.get("verdict") != "NO_JOINT_POINT":
        fail(f"unexpected verdict: {payload.get('verdict')!r}")

    observed_total_joint = 0
    for family, expected in EXPECTED.items():
        family_rows = [row for row in rows if row.get("family") == family]
        computed = {
            "n_rows": len(family_rows),
            "n_admissible_rows": sum(row.get("admissible") is True for row in family_rows),
            "n_sparc_pass": sum(row.get("sparc_gate") is True for row in family_rows),
            "n_cassini_pass": sum(row.get("cassini") == "PASS" for row in family_rows),
            "n_joint": sum(row.get("joint") is True for row in family_rows),
        }
        observed_total_joint += computed["n_joint"]
        recorded = summary.get(family)
        if not isinstance(recorded, dict):
            fail(f"missing summary for family {family}")
        for key, value in computed.items():
            if computed[key] != expected[key]:
                fail(f"family {family} computed {key}={computed[key]}, expected {expected[key]}")
            if recorded.get(key) != value:
                fail(
                    f"family {family} summary mismatch for {key}: "
                    f"summary={recorded.get(key)!r}, rows={value!r}"
                )

    expected_total_rows = sum(item["n_rows"] for item in EXPECTED.values())
    expected_admissible = sum(item["n_admissible_rows"] for item in EXPECTED.values())
    if len(rows) != expected_total_rows:
        fail(f"total rows={len(rows)}, expected {expected_total_rows}")
    if sum(row.get("admissible") is False for row in rows) != len(rows) - expected_admissible:
        fail("inadmissible-row count does not match family totals")
    if observed_total_joint != 0:
        fail(f"found {observed_total_joint} joint-pass rows despite NO_JOINT_POINT")

    print(f"PASS: {len(rows)} rows; {expected_admissible} admissible; "
          f"{len(rows) - expected_admissible} inadmissible; 0 joint passes.")
    for family in ("a", "b", "c"):
        e = EXPECTED[family]
        print(f"  {family}: rows={e['n_rows']}, admissible={e['n_admissible_rows']}, "
              f"Cassini={e['n_cassini_pass']}, SPARC={e['n_sparc_pass']}, joint={e['n_joint']}")
    print("LIMIT: accounting consistency only; no physical calculation was rerun.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
