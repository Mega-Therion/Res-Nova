#!/usr/bin/env python3
"""Download and verify external Res Nova data without silently accepting drift.

SPARC is verified against the repository's frozen SHA-256 manifest. The official
Planck 2018 baseline archive is verified structurally before extraction and can
be cryptographically pinned with --planck-sha256 or PLANCK_BASELINE_SHA256.
Raw data is written only to gitignored directories.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import shutil
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

SPARC_ARCHIVE_URL = "https://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip"
SPARC_MASTER_URL = "https://astroweb.cwru.edu/SPARC/SPARC_Lelli2016c.mrt"
PLANCK_BASELINE_URL = "https://pla.esac.esa.int/pla-sl/data-action?COSMOLOGY.COSMOLOGY_OID=151902"
# Measured 2026-10-03 from PLANCK_BASELINE_URL on two separate downloads (60,323,470 bytes each). Used as the
# default pin so an upstream re-issue fails loudly instead of being accepted; override with --planck-sha256.
PLANCK_BASELINE_SHA256_MEASURED = "0b73171e3acc671c28184466a45485a2d1c1d93676b832abdfe688c7b04024e6"
PLANCK_REQUIRED_PATTERNS = {
    "high-l": "*/hi_l/plik/*TTTEEE*.clik",
    "low-l temperature": "*/low_l/commander/*.clik",
    "low-l polarization": "*/low_l/simall/*.clik",
}


@dataclass
class VerificationResult:
    ok: bool
    errors: list[str]
    required_members: list[str]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_sha256_manifest(data_dir: Path, manifest: Path) -> VerificationResult:
    errors: list[str] = []
    required: list[str] = []
    for raw in manifest.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            expected, relative = line.split(None, 1)
            relative = relative.lstrip("*").strip()
        except ValueError:
            errors.append(f"malformed manifest line: {raw}")
            continue
        path = data_dir / relative
        required.append(relative)
        if not path.is_file():
            errors.append(f"missing: {relative}")
        elif sha256_file(path) != expected.lower():
            errors.append(f"hash mismatch: {relative}")
    return VerificationResult(not errors, errors, required)


def clik_roots(names: Iterable[str]) -> set[str]:
    """Every file path plus the `.clik` directory each file sits in.

    A `.clik` likelihood is a directory (`<name>.clik/_mdb`, `<name>.clik/clik/...`), not a file. Its root is
    derived from the files under it, so a `.clik` directory only counts as present if it holds at least one
    file; an empty directory entry proves nothing."""
    roots = set()
    for name in names:
        name = name.rstrip("/")
        roots.add(name)
        parts = name.split("/")
        for i, part in enumerate(parts):
            if part.endswith(".clik"):
                roots.add("/".join(parts[: i + 1]))
    return roots


def match_required_members(names: Iterable[str]) -> tuple[list[str], list[str]]:
    candidates = clik_roots(names)
    errors: list[str] = []
    required_members: list[str] = []
    for label, pattern in PLANCK_REQUIRED_PATTERNS.items():
        matches = sorted(name for name in candidates if fnmatch.fnmatchcase(name, pattern))
        if not matches:
            errors.append(f"missing {label} likelihood member matching {pattern}")
        else:
            required_members.extend(matches)
    return errors, sorted(required_members)


def inspect_planck_archive(archive: Path) -> VerificationResult:
    errors: list[str] = []
    with tarfile.open(archive, "r:gz") as handle:
        members = handle.getmembers()
        if any(Path(member.name).is_absolute() or ".." in Path(member.name).parts for member in members):
            errors.append("archive contains an unsafe absolute or parent-traversal path")
        names = [member.name for member in members if member.isfile()]
    missing, required_members = match_required_members(names)
    errors.extend(missing)
    return VerificationResult(not errors, errors, required_members)


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix=destination.name + ".", dir=destination.parent, delete=False) as tmp:
        temporary = Path(tmp.name)
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Res-Nova reproducibility fetcher/1.0"})
        with urllib.request.urlopen(request, timeout=120) as response, temporary.open("wb") as output:
            shutil.copyfileobj(response, output, length=1024 * 1024)
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def flatten_sparc(data_dir: Path) -> int:
    nested = data_dir / "Rotmod_LTG"
    if nested.is_dir():
        for source in nested.rglob("*_rotmod.dat"):
            source.replace(data_dir / source.name)
        shutil.rmtree(nested)
    return len(list(data_dir.glob("*_rotmod.dat")))


def sparc_manifest(repo_root: Path) -> Path:
    candidates = [
        repo_root / "VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256",
        repo_root / "VERIFICATION_RUN_009/02_sparc_fetch/RAW_DATA_MANIFEST.sha256",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("no SPARC RAW_DATA_MANIFEST.sha256 found")


def fetch_sparc(repo_root: Path) -> dict:
    data_dir = repo_root / "02_galaxy_dynamics/sparc_data"
    data_dir.mkdir(parents=True, exist_ok=True)
    archive = data_dir / "Rotmod_LTG.zip"
    master = data_dir / "SPARC_Lelli2016c.mrt"
    if not archive.exists():
        download(SPARC_ARCHIVE_URL, archive)
    if not master.exists():
        download(SPARC_MASTER_URL, master)
    with zipfile.ZipFile(archive) as handle:
        handle.extractall(data_dir)
    archive.unlink(missing_ok=True)
    count = flatten_sparc(data_dir)
    if count != 175:
        raise RuntimeError(f"SPARC expected 175 *_rotmod.dat files, found {count}")
    manifest = sparc_manifest(repo_root)
    verification = verify_sha256_manifest(data_dir, manifest)
    if not verification.ok:
        raise RuntimeError("SPARC verification failed: " + "; ".join(verification.errors))
    return {
        "dataset": "SPARC Rotmod_LTG",
        "source": SPARC_ARCHIVE_URL,
        "master_table": SPARC_MASTER_URL,
        "manifest": str(manifest.relative_to(repo_root)),
        "file_count": count,
        "verified_files": len(verification.required_members),
    }


def fetch_planck(repo_root: Path, expected_sha256: str | None, url: str = PLANCK_BASELINE_URL) -> dict:
    data_dir = repo_root / "04_cosmology/planck_data"
    data_dir.mkdir(parents=True, exist_ok=True)
    archive = data_dir / "COM_Likelihood_Data-baseline_R3.00.tar.gz"
    if not archive.exists():
        download(url, archive)
    actual_sha256 = sha256_file(archive)
    if expected_sha256 and actual_sha256 != expected_sha256.lower():
        raise RuntimeError(f"Planck archive SHA-256 mismatch: {actual_sha256} != {expected_sha256}")
    inspection = inspect_planck_archive(archive)
    if not inspection.ok:
        raise RuntimeError("Planck archive verification failed: " + "; ".join(inspection.errors))
    extract_root = data_dir / "extracted"
    extract_root.mkdir(exist_ok=True)
    with tarfile.open(archive, "r:gz") as handle:
        members = handle.getmembers()
        if any(Path(member.name).is_absolute() or ".." in Path(member.name).parts for member in members):
            raise RuntimeError("refusing to extract unsafe Planck archive paths")
        if hasattr(tarfile, "data_filter"):  # Python >= 3.12 (and security backports): refuse links out of the tree
            handle.extractall(extract_root, filter="data")
        else:
            handle.extractall(extract_root)
    receipt = {
        "dataset": "Planck 2018 baseline likelihood data PR3/R3.00",
        "source": url,
        "accessed_utc": datetime.now(timezone.utc).isoformat(),
        "archive": str(archive.relative_to(repo_root)),
        "archive_sha256": actual_sha256,
        "archive_sha256_pinned": bool(expected_sha256),
        "required_members": inspection.required_members,
        "official_reference": "Planck Collaboration, Planck 2018 results V, A&A 641, A5 (2020), arXiv:1907.12875",
        "verification": "archive SHA-256 when pinned plus required plik/commander/simall member checks",
    }
    (data_dir / "PLANCK_BASELINE_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--sparc", action="store_true", help="download and verify SPARC")
    parser.add_argument("--planck", action="store_true", help="download and verify Planck baseline likelihoods")
    parser.add_argument("--all", action="store_true", help="download both datasets")
    parser.add_argument("--planck-sha256", default=os.environ.get("PLANCK_BASELINE_SHA256", PLANCK_BASELINE_SHA256_MEASURED), help="pinned Planck archive SHA-256 (default: the hash measured 2026-10-03)")
    parser.add_argument("--planck-url", default=PLANCK_BASELINE_URL, help="official Planck archive URL or approved mirror")
    args = parser.parse_args(list(argv) if argv is not None else None)
    if not (args.sparc or args.planck or args.all):
        parser.error("choose --sparc, --planck, or --all")
    repo_root = args.repo_root.resolve()
    results = []
    if args.sparc or args.all:
        results.append(fetch_sparc(repo_root))
    if args.planck or args.all:
        results.append(fetch_planck(repo_root, args.planck_sha256, args.planck_url))
    print(json.dumps({"status": "verified", "results": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
