"""SPARC data path resolution helper.

Resolves the SPARC rotation curve data directory containing *_rotmod.dat files,
in priority order:
1. Explicit CLI argument (--data-dir) if provided
2. Environment variable SPARC_DATA_DIR (or legacy SPARC_DATA)
3. 02_galaxy_dynamics/sparc_data (repo-local)
4. ./sparc_data (current working directory)
5. /home/mega/Chyren/Research_and_Data/07_Domain_Tiers_and_Data/Datasets/data/sparc_data (last fallback)

Raises FileNotFoundError listing all tried paths if no valid directory with *_rotmod.dat is found.
"""

from __future__ import annotations

import os
from pathlib import Path

_MODULE_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _MODULE_DIR.parent
_OLD_FALLBACK = Path(
    "/home/mega/Chyren/Research_and_Data/07_Domain_Tiers_and_Data/Datasets/data/sparc_data"
)


def resolve_sparc_dir(cli_dir: str | Path | None = None) -> Path:
    """Resolve the SPARC data directory.

    Searches in order:
    1. cli_dir (if provided and non-empty)
    2. env SPARC_DATA_DIR (or SPARC_DATA)
    3. 02_galaxy_dynamics/sparc_data (repo-local)
    4. ./sparc_data (cwd-local)
    5. _OLD_FALLBACK (/home/mega/...)
    """
    candidates: list[Path] = []
    tried: list[str] = []

    # 1. CLI parameter
    if cli_dir:
        p = Path(cli_dir).expanduser()
        candidates.append(p)
        tried.append(f"CLI --data-dir: {p}")

    # 2. Environment variables
    env_var = os.environ.get("SPARC_DATA_DIR") or os.environ.get("SPARC_DATA")
    if env_var:
        p = Path(env_var).expanduser()
        candidates.append(p)
        tried.append(f"env SPARC_DATA_DIR: {p}")
    else:
        tried.append("env SPARC_DATA_DIR: (not set)")

    # 3. Repo-local 02_galaxy_dynamics/sparc_data
    repo_local = _MODULE_DIR / "sparc_data"
    candidates.append(repo_local)
    tried.append(f"repo-local: {repo_local}")

    # 4. Cwd-local ./sparc_data
    cwd_local = Path.cwd() / "sparc_data"
    if cwd_local != repo_local:
        candidates.append(cwd_local)
        tried.append(f"cwd-local: {cwd_local}")

    # 5. Last fallback
    candidates.append(_OLD_FALLBACK)
    tried.append(f"legacy fallback: {_OLD_FALLBACK}")

    for candidate in candidates:
        if candidate.is_dir():
            rotmods = list(candidate.glob("*_rotmod.dat"))
            if rotmods:
                return candidate.resolve()

    tried_str = "\n  - ".join(tried)
    raise FileNotFoundError(
        f"No SPARC *_rotmod.dat files found. Tried paths:\n  - {tried_str}\n"
        "To fix: download SPARC Rotmod_LTG into 02_galaxy_dynamics/sparc_data "
        "or set SPARC_DATA_DIR."
    )


def resolve_sparc_meta(cli_meta: str | Path | None = None) -> Path | None:
    """Resolve optional SPARC metadata CSV (e.g. published D/i uncertainties).

    Priority:
    1. cli_meta (if provided)
    2. env SPARC_META_CSV
    3. None (run without per-galaxy published D/i)
    """
    if cli_meta:
        p = Path(cli_meta).expanduser()
        if p.is_file():
            return p.resolve()
        return None

    env_meta = os.environ.get("SPARC_META_CSV")
    if env_meta:
        p = Path(env_meta).expanduser()
        if p.is_file():
            return p.resolve()

    return None
