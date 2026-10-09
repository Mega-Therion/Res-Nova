#!/usr/bin/env python3
"""Coverage gate for docs/ERRATA.yaml.

Every retired entity the dead-branch scan enforces, and every Zenodo correction
record, must have an errata entry, and every evidence path must exist. Without
this the register drifts the moment a new entity or correction is added.

    python3 scripts/check_errata.py            # exit 1 on a gap
    python3 scripts/check_errata.py --self-test
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dead_branch_scan  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ERRATA = ROOT / "docs" / "ERRATA.yaml"
REGISTRY = ROOT / "docs" / "publication_registry.yaml"
REQUIRED = ("id", "withdrawn", "what", "replacement", "evidence", "scan_entities", "dois")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_INDEX_ROW = re.compile(r"^\|[^|]*\|\s*(10\.5281/zenodo\.\d+)\s*\|\s*$")


def correction_dois(registry: dict, index_texts: list[str]) -> set[str]:
    dois = {w["canonical_doi"] for w in registry.get("works", [])
            if "correction" in w.get("title", "").lower() and w.get("canonical_doi")}
    for text in index_texts:
        for line in text.splitlines():
            m = _INDEX_ROW.match(line.strip())
            if m:
                dois.add(m.group(1))
    return dois


def problems(errata: dict, entities: set[str], corrections: set[str], exists) -> list[str]:
    out, ids, covered_e, covered_d = [], set(), set(), set()
    for i, e in enumerate(errata.get("errata") or []):
        tag = e.get("id", f"#{i}")
        missing = [k for k in REQUIRED if k not in e]
        if missing:
            out.append(f"{tag}: missing fields {missing}")
            continue
        if tag in ids:
            out.append(f"{tag}: duplicate id")
        ids.add(tag)
        if not _DATE.match(str(e["withdrawn"])):
            out.append(f"{tag}: withdrawn date {e['withdrawn']!r} is not YYYY-MM-DD")
        if not e["evidence"]:
            out.append(f"{tag}: no evidence path")
        for p in e["evidence"]:
            if not exists(p):
                out.append(f"{tag}: evidence path does not exist: {p}")
        for s in e["scan_entities"]:
            if s not in entities:
                out.append(f"{tag}: unknown scan entity {s!r}")
            covered_e.add(s)
        covered_d.update(e["dois"])
    out += [f"retired entity without an errata entry: {s!r}" for s in sorted(entities - covered_e)]
    out += [f"correction record without an errata entry: {d}" for d in sorted(corrections - covered_d)]
    return out


def live() -> list[str]:
    entities = {label for label, _, _ in dead_branch_scan.RETIRED}
    index = [p.read_text(encoding="utf-8") for p in sorted(ROOT.glob("ZENODO_CORRECTION_INDEX_*.md"))]
    corrections = correction_dois(yaml.safe_load(REGISTRY.read_text(encoding="utf-8")), index)
    errata = yaml.safe_load(ERRATA.read_text(encoding="utf-8"))
    return problems(errata, entities, corrections, lambda p: (ROOT / p).exists())


def self_test() -> int:
    ok = {"id": "E-1", "withdrawn": "2026-01-01", "what": "w", "replacement": "r",
          "evidence": ["a.md"], "scan_entities": ["X"], "dois": ["10.5281/zenodo.1"]}
    exists = lambda p: p == "a.md"  # noqa: E731
    reg = {"works": [{"title": "Correction: z", "canonical_doi": "10.5281/zenodo.1"},
                     {"title": "Other", "canonical_doi": "10.5281/zenodo.9"}]}
    idx = ["| 10.5281/zenodo.8 (concept x) | 10.5281/zenodo.2 |"]
    cases = [
        ("clean", {"errata": [ok]}, {"X"}, correction_dois(reg, []), 0),
        ("entity uncovered", {"errata": [ok]}, {"X", "Y"}, set(), 1),
        ("index row uncovered", {"errata": [ok]}, {"X"}, correction_dois(reg, idx), 1),
        ("missing evidence", {"errata": [{**ok, "evidence": ["b.md"]}]}, {"X"}, set(), 1),
        ("bad date", {"errata": [{**ok, "withdrawn": "Sept"}]}, {"X"}, set(), 1),
        ("missing field", {"errata": [{k: v for k, v in ok.items() if k != "dois"}]}, set(), set(), 1),
        ("unknown entity", {"errata": [{**ok, "scan_entities": ["Z"]}]}, set(), set(), 1),
    ]
    fails = 0
    for name, errata, ents, corr, want in cases:
        got = len(problems(errata, ents, corr, exists))
        if (got > 0) != (want > 0):
            print(f"FAIL {name}: {got} problems"); fails += 1
    if correction_dois(reg, idx) != {"10.5281/zenodo.1", "10.5281/zenodo.2"}:
        print("FAIL correction_dois parsing"); fails += 1
    print("self-test:", "FAIL" if fails else f"PASS ({len(cases) + 1} cases)")
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    if ap.parse_args().self_test:
        return self_test()
    out = live()
    for line in out:
        print(line)
    print(f"errata: {len(out)} problem(s)")
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main())
