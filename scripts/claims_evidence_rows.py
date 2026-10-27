#!/usr/bin/env python3
"""Build one row per claim in assurance/claims.json for the ADCCL claim scorer.

Row: {"id", "task", "response", "evidence", "evidence_files", "missing_files"}.
- response: the claim's `wording`.
- task: its id and source_locator.
- evidence: the text of every cited artifact that exists on disk (formal, computational,
  data, independent_witness). A cited directory contributes its text files.
The claim's own `limitations` and `assumptions` are left out of the evidence, so a claim
cannot support itself.

Usage: python3 scripts/claims_evidence_rows.py > claims_evidence.jsonl
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = {".md", ".json", ".py", ".lean", ".txt", ".log", ".tex", ".csv", ".yaml", ".yml", ".jsonl"}
MAX_BYTES = 2_000_000


def read(p: Path) -> str:
    if p.suffix.lower() not in TEXT or p.stat().st_size > MAX_BYTES:
        return ""
    return p.read_text(errors="replace")


def main() -> int:
    claims = json.loads((ROOT / "assurance/claims.json").read_text())["claims"]
    for c in claims:
        cited = list(c.get("formal_artifacts") or []) + list(c.get("computational_artifacts") or []) \
            + list(c.get("data_artifacts") or [])
        if c.get("independent_witness"):
            cited.append(c["independent_witness"])
        parts, found, missing = [], [], []
        for rel in cited:
            rel = str(rel).split("::")[0].split("#")[0].strip()
            p = ROOT / rel
            if p.is_file():
                parts.append(read(p))
                found.append(rel)
            elif p.is_dir():
                for q in sorted(p.rglob("*")):
                    if q.is_file():
                        parts.append(read(q))
                found.append(rel + "/")
            else:
                missing.append(rel)
        print(json.dumps({
            "id": c["id"],
            "task": f'{c["id"]}: {c.get("source_locator") or ""}',
            "response": c.get("wording") or "",
            "evidence": "\n".join(parts),
            "evidence_files": found,
            "missing_files": missing,
        }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
