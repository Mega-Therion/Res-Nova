#!/usr/bin/env python3
"""Fail if current-claim surfaces drift off the frozen SPARC JSON or revive withdrawn language."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def need(path: Path) -> Path:
    if not path.is_file():
        errors.append(f"missing {path.relative_to(ROOT)}")
    return path


version = need(ROOT / "VERSION").read_text().strip() if (ROOT / "VERSION").is_file() else ""
if not version or not re.match(r"^\d+\.\d+\.\d+$", version):
    errors.append(f"VERSION is {version!r}, expected valid semver (e.g. '1.6.2')")

for rel in (
    "EPISTEMIC_BOUNDARY_v1.5.0.md",
    "OPEN_PROBLEMS_AND_TESTS.md",
    "FOR_REFEREES.md",
    "AGENT_COVENANT.md",
    "01_foundational_action/PAPER_01_NOTICE.md",
    "02_galaxy_dynamics/A0_MEASUREMENT.json",
    "02_galaxy_dynamics/PARAMETER_LEDGER.json",
    "02_galaxy_dynamics/NFW_CONSTRAINED.json",
):
    need(ROOT / rel)

a0_path = ROOT / "02_galaxy_dynamics" / "A0_MEASUREMENT.json"
ledger_path = ROOT / "02_galaxy_dynamics" / "PARAMETER_LEDGER.json"
nfw_path = ROOT / "02_galaxy_dynamics" / "NFW_CONSTRAINED.json"

if a0_path.is_file():
    a0 = json.loads(a0_path.read_text())
    if abs(a0["a0_best_fit"] - 1.1162688655613144e-10) > 1e-18:
        errors.append("A0_MEASUREMENT.json a0_best_fit drifted")
    if abs(a0["tension_claim_sigma"] - 0.46175003838310674) > 1e-12:
        errors.append("A0_MEASUREMENT.json tension_claim_sigma drifted")

if ledger_path.is_file() and nfw_path.is_file():
    led = json.loads(ledger_path.read_text())
    extra = led["tier1_NFW"]["total_free_params"] - led["tier1_GOD"]["total_free_params"]
    if extra != 342:
        errors.append(f"NFW-GOD parameter gap is {extra}, expected 342")

readme = (ROOT / "README.md").read_text() if (ROOT / "README.md").is_file() else ""
if "1.116" not in readme:
    errors.append("README.md does not mention the working a0 1.116e-10")
if "SUPERSEDED" not in readme:
    errors.append("README.md must mark the old a0 headline SUPERSEDED")

# Withdrawn as a live claim, allowed as a labeled historical title.
live = re.sub(r"(?is)related publications.*", "", readme)
if re.search(r"zero[- ]parameter geometric alternative", live, re.I):
    errors.append("README.md revives zero-parameter language outside the historical DOI list")
if re.search(r"zero free parameters", live, re.I) and "withdrawn" not in live.lower():
    errors.append("README.md says zero free parameters without a withdrawal")

if errors:
    print("FAIL")
    for e in errors:
        print(f" - {e}")
    sys.exit(1)

print("PASS — claim surfaces match frozen JSON and v1.5.0 hygiene")
