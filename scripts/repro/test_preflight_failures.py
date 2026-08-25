#!/usr/bin/env python3
"""Deliberate failure tests: hash mismatch and injected Lean sorry."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREFLIGHT = ROOT / "scripts" / "repro" / "preflight.py"
SORRY = ROOT / "scripts" / "repro" / "check_sorry.py"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=False, capture_output=True, text=True)


def test_hash_mismatch() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "artifact.bin"
        path.write_bytes(b"good-bytes")
        wrong = hashlib.sha256(b"other-bytes").hexdigest()
        proc = run([sys.executable, str(PREFLIGHT), "--hash", f"{path}={wrong}"])
    assert proc.returncode == 20, proc.returncode
    assert "artifact_mismatch" in proc.stdout
    print("test_hash_mismatch PASS")


def test_injected_sorry() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        lean = Path(tmp) / "Injected.lean"
        lean.write_text("theorem bad : True := by\n  sorry\n", encoding="utf-8")
        proc = run([sys.executable, str(SORRY), "--root", tmp, "--json"])
    assert proc.returncode == 30, proc.returncode
    assert "sorry" in proc.stdout
    print("test_injected_sorry PASS")


def test_commented_sorry_is_clean() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        lean = Path(tmp) / "Clean.lean"
        lean.write_text("-- sorry is only in a comment\ntheorem ok : True := trivial\n", encoding="utf-8")
        proc = run([sys.executable, str(SORRY), "--root", tmp])
    assert proc.returncode == 0, proc.stdout
    print("test_commented_sorry_is_clean PASS")


def main() -> int:
    test_hash_mismatch()
    test_injected_sorry()
    test_commented_sorry_is_clean()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
