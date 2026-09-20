#!/usr/bin/env python3
"""The single definition of "what surfaces this corpus owns".

Three separate gates were each written with their own enumeration, and all
three were born scoped to the Res_Nova_Monograph submodule alone. Every one was
therefore blind to `00_CANONICAL/` -- the directory holding the document that
calls itself "the single canonical reference for the scope, status and roadmap"
of the whole program. That is not three coincidences, it is a template defect:
`git -C <submodule> ls-files` is the obvious thing to write and it is wrong
here, because the corpus spans two repositories.

Binding the two together in one place means the next checker inherits the right
scope instead of rediscovering it the hard way. Callers should never call
`git ls-files` directly.

Surfaces come back as `(absolute path, display path)`. The display path is what
a gate prints and what a content-keyed baseline is keyed on, so it must stay
stable: files in the parent repo are shown with a `../` prefix.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

# Repo root of the monograph submodule (this file lives in <root>/scripts/).
ROOT = Path(__file__).resolve().parent.parent

# Directories in the PARENT repo that are part of this corpus. Relative to the
# submodule's parent directory.
EXTRA_SCAN_ROOTS = ("00_CANONICAL",)

# Never-scan prefixes shared by every gate: historical records, not live claims.
DEFAULT_SKIP = (
    "raw/Logs/", "raw/", "80_Archive/", "obsidian_vault_legacy/", "archive/",
    "archive", "docs/recovered/", "archive_previous_iterations/",
    "Tier_2_Physics_Attempt/",
)

_GIT_LEAK_VARS = frozenset((
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_PREFIX",
))


class SurfaceEnumerationError(RuntimeError):
    """git could not be queried, so the surface list is INCOMPLETE.

    Returning [] on a git failure is fail-open: a transient error (a stale
    index.lock from a background job, a repo mid-operation) silently collapses
    the scan to fewer files, and every gate downstream then reports a clean
    PASS over a smaller corpus. This happened for real -- a parent-repo git
    call failed during a pre-push hook and scope dropped 162 -> 147 files with
    00_CANONICAL gone entirely, while each individual check still said PASS."""


def _ls_files(repo: Path, pathspec: str) -> list[str]:
    # In git hooks (e.g. pre-push, pre-commit), git exports GIT_DIR and friends
    # pointing at the invoking repo's git dir. If we inspect another repo (like
    # parent repo's 00_CANONICAL), we must strip these so git finds the right repo.
    clean_env = {k: v for k, v in os.environ.items() if k not in _GIT_LEAK_VARS}
    r = subprocess.run(["git", "-C", str(repo), "ls-files", pathspec],
                       capture_output=True, text=True, env=clean_env)
    if r.returncode != 0:
        raise SurfaceEnumerationError(
            f"git ls-files failed in {repo} (rc={r.returncode}): "
            f"{r.stderr.strip() or 'no stderr'}. The surface list would be "
            f"INCOMPLETE, so no gate result from this run is trustworthy. "
            f"Retry; if it persists check for a stale index.lock or a "
            f"background process writing to that repository.")
    return r.stdout.splitlines()


def surfaces(globs: tuple[str, ...],
             skip: tuple[str, ...] = DEFAULT_SKIP,
             include_canonical: bool = True) -> list[tuple[Path, str]]:
    """Every tracked surface matching `globs`, across BOTH repositories."""
    def keep(rel: str) -> bool:
        return (any(Path(rel).match(g) for g in globs)
                and not any(s in rel for s in skip))

    out = [(ROOT / f, f) for f in _ls_files(ROOT, ".") if keep(f)]
    if include_canonical:
        parent = ROOT.parent
        for extra in EXTRA_SCAN_ROOTS:
            if not (parent / extra).is_dir():
                continue
            for f in _ls_files(parent, extra):
                if keep(f):
                    out.append((parent / f, f"../{f}"))
    return out


def tracked_markdown(skip: tuple[str, ...] = DEFAULT_SKIP):
    """Every live Markdown surface, submodule + 00_CANONICAL."""
    return surfaces(("*.md",), skip)


def tracked_tex(skip: tuple[str, ...] = DEFAULT_SKIP):
    """Every live LaTeX surface, submodule + 00_CANONICAL."""
    return surfaces(("*.tex",), skip)


def tracked_canonical(skip: tuple[str, ...] = DEFAULT_SKIP):
    """Only the parent repo's 00_CANONICAL surfaces (md + tex)."""
    return [s for s in surfaces(("*.md", "*.tex"), skip)
            if s[1].startswith("../00_CANONICAL/")]


def self_test() -> int:
    """The invariant that matters: canonical surfaces are never lost."""
    bad = []
    md = tracked_markdown()
    tex = tracked_tex()
    canon = tracked_canonical()

    if not md:
        bad.append("tracked_markdown() returned nothing")
    if not tex:
        bad.append("tracked_tex() returned nothing")
    parent_present = any((ROOT.parent / e).is_dir() for e in EXTRA_SCAN_ROOTS)
    if not canon and parent_present:
        bad.append("tracked_canonical() returned nothing though 00_CANONICAL "
                   "exists on disk -- the binding is broken")
    elif not canon and not EXTRA_SCAN_ROOTS:
        bad.append("EXTRA_SCAN_ROOTS is empty -- 00_CANONICAL is unscannable")

    # The defect this module exists to prevent.
    if parent_present and not any(r.startswith("../00_CANONICAL/") for _, r in md):
        bad.append("tracked_markdown() is blind to 00_CANONICAL")

    # Display paths must be unique and stable (baselines are keyed on them).
    rels = [r for _, r in md] + [r for _, r in tex]
    if len(rels) != len(set(rels)):
        bad.append("duplicate display paths")

    # Every returned path must exist.
    for p, r in md + tex:
        if not p.exists():
            bad.append(f"missing file: {r}")
            break

    # Opting out must actually opt out.
    if any(r.startswith("../") for _, r in surfaces(("*.md",), include_canonical=False)):
        bad.append("include_canonical=False still returned parent surfaces")

    # Skips must apply to both repos.
    if any("80_Archive/" in r for _, r in md):
        bad.append("skip list not applied")

    for b in bad:
        print(f"  corpus_surfaces SELF-TEST FAIL: {b}")
    print(f"corpus_surfaces self-test: {'PASS' if not bad else 'FAIL'} "
          f"({len(md)} md, {len(tex)} tex, {len(canon)} canonical)")
    return 1 if bad else 0


if __name__ == "__main__":
    import sys
    sys.exit(self_test())
