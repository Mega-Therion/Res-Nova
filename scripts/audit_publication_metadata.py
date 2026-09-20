#!/usr/bin/env python3
"""Publication-metadata gate for Res Nova.

The repository declares DOIs in many places. This makes exactly one of them
authoritative -- docs/publication_registry.yaml -- and fails when any other
surface disagrees with it, or when the registry disagrees with DataCite.

    python3 scripts/audit_publication_metadata.py            # offline checks
    python3 scripts/audit_publication_metadata.py --online   # + DataCite
    python3 scripts/audit_publication_metadata.py --refresh  # rewrite registry
    python3 scripts/audit_publication_metadata.py --self-test

Exit 0 clean, 1 on any failure.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "docs" / "publication_registry.yaml"
ORCID = "0009-0001-1303-7190"
OWN_PREFIX = "10.5281/zenodo."

DOI_RE = re.compile(r"10\.[0-9]{4,9}/[-._;()/:A-Za-z0-9]+")
OWN_DOI_RE = re.compile(r"10\.5281/zenodo\.[0-9]+")

# Surfaces that must only ever carry live, current DOIs.
LIVE_SURFACES = ("README.md", "CITATION.cff", ".zenodo.json",
                 "FIG_TREE_ARCHITECTURE_MAP.md")
# Paths that record history and may legitimately cite superseded DOIs.
HISTORICAL = ("archive/", "docs/recovered/", "/old_", "verification_runs/",
              "CHANGELOG", "_previous_", "archive_previous_iterations/")

# First cells that name a metadata field rather than a work.
FIELD_LABEL = re.compile(
    r"^(concept|current|version|release|latest|previous|earlier|archived|"
    r"repository|repo|author|orcid|tag|date|status|doi|citation|identifier)\b",
    re.I)

SCAN_GLOBS = ("*.md", "*.tex", "*.bib", "*.json", "*.cff", "*.yml", "*.yaml", "*.txt")


# --------------------------------------------------------------- registry ---
def load_registry(path: Path = REGISTRY) -> dict:
    """Parse the registry. Deliberately a small hand-rolled reader so the gate
    has no dependency that could itself be missing in CI."""
    if not path.exists():
        return {"identity": {}, "works": []}
    identity: dict[str, str] = {}
    works: list[dict] = []
    gaps: list[dict] = []
    cur: dict | None = None
    section = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("identity:"):
            section = "identity"
            continue
        if raw.startswith("works:"):
            section = "works"
            cur = None
            continue
        if raw.startswith("known_gaps:"):
            section = "gaps"
            cur = None
            continue
        m = re.match(r"\s*-\s*doi:\s*(.*)$", raw)
        if m and section == "gaps":
            cur = {"doi": m.group(1).strip().strip('"')}
            gaps.append(cur)
            continue
        m = re.match(r"\s*-\s*work_id:\s*(\S+)", raw)
        if m:
            cur = {"work_id": m.group(1)}
            works.append(cur)
            continue
        m = re.match(r"\s+([a-z_]+):\s*(.*)$", raw)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        elif val.startswith("["):
            val = [v.strip().strip('"') for v in val[1:-1].split(",") if v.strip()]
        elif val in ("null", "~"):
            val = None
        if section == "identity" and cur is None:
            identity[key] = val
        elif cur is not None:
            cur[key] = val
    return {"identity": identity, "works": works, "known_gaps": gaps}


# ------------------------------------------------------------------ checks ---
def tracked_files() -> list[Path]:
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files"],
                         capture_output=True, text=True).stdout.splitlines()
    keep = []
    for f in out:
        if any(Path(f).match(g) for g in SCAN_GLOBS):
            keep.append(ROOT / f)
    return keep


def is_historical(rel: str) -> bool:
    return any(h in rel for h in HISTORICAL)


def check_registry_shape(reg: dict) -> list[str]:  # noqa: C901
    errs = []
    ident = reg["identity"]
    if ident.get("orcid") != ORCID:
        errs.append(f"registry identity ORCID is {ident.get('orcid')!r}, expected {ORCID!r}")
    if ident.get("name") != "R.W. Yett":
        errs.append(f"registry identity name is {ident.get('name')!r}, expected 'R.W. Yett'")
    if ident.get("location") is not None and ident.get("location") != "Arkansas":
        errs.append(f"registry location is {ident.get('location')!r}, expected 'Arkansas'")
    if ident.get("contact") is not None and \
            ident.get("contact") != "r11110001y@proton.me":
        errs.append(f"registry contact is {ident.get('contact')!r}, "
                    f"expected 'r11110001y@proton.me'")
    seen_ids, seen_dois = set(), set()
    for w in reg["works"]:
        wid, doi = w.get("work_id"), w.get("canonical_doi")
        if wid in seen_ids:
            errs.append(f"duplicate work_id: {wid}")
        seen_ids.add(wid)
        if doi in seen_dois:
            errs.append(f"duplicate canonical_doi: {doi}")
        seen_dois.add(doi)
        if not doi:
            errs.append(f"{wid}: no canonical_doi")
        author = (w.get("author") or "")
        if w.get("status") == "live" and author and "Yett" not in author:
            if doi not in {g.get("doi") for g in reg.get("known_gaps", [])}:
                errs.append(f"{wid} ({doi}): deposited under {author!r}, not the "
                            f"canonical identity 'Yett, Ryan W.'")
        if w.get("status") == "live" and w.get("orcid") != ORCID:
            if doi in {g.get("doi") for g in reg.get("known_gaps", [])}:
                continue          # tracked in known_gaps, reported separately
            errs.append(f"{wid} ({doi}): live work lacks the canonical ORCID "
                        f"(has {w.get('orcid')!r}) -- fix it on the Zenodo record")
    return errs


def check_coverage_and_surfaces(reg: dict) -> list[str]:
    known = {w["canonical_doi"] for w in reg["works"] if w.get("canonical_doi")}
    quarantined = {w["canonical_doi"] for w in reg["works"]
                   if w.get("status") in ("superseded", "retracted")}
    errs = []
    for path in tracked_files():
        rel = str(path.relative_to(ROOT))
        if rel == str(REGISTRY.relative_to(ROOT)) or rel.startswith("scripts/"):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for doi in sorted(set(OWN_DOI_RE.findall(text))):
            if doi not in known:
                errs.append(f"{rel}: {doi} has no entry in the publication registry")
            elif doi in quarantined and not is_historical(rel) and \
                    any(rel.endswith(s) or rel == s for s in LIVE_SURFACES):
                errs.append(f"{rel}: cites {doi}, which the registry marks "
                            f"superseded/retracted, on a live surface")
    return errs


def check_local_titles(reg: dict) -> list[str]:
    """A DOI written on a table row whose label contradicts the registry title
    is the exact defect that shipped in FIG_TREE_ARCHITECTURE_MAP.md."""
    by_doi = {w["canonical_doi"]: w for w in reg["works"] if w.get("canonical_doi")}
    errs = []
    for path in tracked_files():
        rel = str(path.relative_to(ROOT))
        if rel == str(REGISTRY.relative_to(ROOT)) or rel.startswith("scripts/"):
            continue
        if is_historical(rel):
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for n, line in enumerate(lines, 1):
            for doi in set(OWN_DOI_RE.findall(line)):
                w = by_doi.get(doi)
                if not w:
                    continue
                # Only a table that pairs a WORK NAME with a DOI can contradict
                # itself. A two-column key/value table ("Concept DOI | 10.x")
                # states a field name, not a title, so it is not a claim.
                if line.count("|") < 4:
                    continue
                label = line.split("|")[1].strip()
                label = re.sub(r"[*`\[\]]", "", label).strip()
                if len(label) < 6:
                    continue
                if FIELD_LABEL.search(label) or "doi.org" in label or DOI_RE.search(label):
                    continue
                title = w["title"].lower()
                key = re.sub(r"[^a-z0-9 ]", " ", label.lower()).split()
                key = [k for k in key if len(k) > 3]
                if key and not any(k in title for k in key):
                    errs.append(f"{rel}:{n}: row labelled {label!r} carries {doi}, "
                                f"which DataCite says is {w['title'][:60]!r}")
    return errs


# ------------------------------------------------------------- bylines ---
AUTHOR_CMD = re.compile(r"\\author\{", re.M)
BAD_IDENTITY = re.compile(r"Mega-Therion|Therion,\s*Mega|Chyren Sovereign Intelligence", re.I)
ABBREV = re.compile(r"\bR\.\s*W\.\s*~?Yett\b")


def check_bylines() -> list[str]:
    """The \author block is metadata. The canonical byline is "R.W. Yett" --
    the author's stated preference. The expanded "Ryan W. Yett" is a second
    surface form and must not appear in an author block. Contact is
    r11110001y@proton.me and the location is Arkansas, nothing longer."""
    errs = []
    for path in tracked_files():
        rel = str(path.relative_to(ROOT))
        if not rel.endswith(".tex") or is_historical(rel) or "05_lean" in rel:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in AUTHOR_CMD.finditer(text):
            # take the author block: from \author{ to the matching blank line
            block = text[m.start():m.start() + 400].split("\n\n")[0]
            n = text[:m.start()].count("\n") + 1
            if "Ryan W." in block:
                errs.append(f"{rel}:{n}: \\author block uses the expanded byline; "
                            f"metadata must read 'R.W. Yett'")
            if "Yett" in block and "R.W." not in block and "Ryan W." not in block:
                errs.append(f"{rel}:{n}: \\author block does not carry the "
                            f"canonical byline 'R.W. Yett'")
            if BAD_IDENTITY.search(block):
                errs.append(f"{rel}:{n}: \\author block carries a second identity "
                            f"({BAD_IDENTITY.search(block).group(0)!r})")
    return errs


def check_release_lineage(reg: dict) -> list[str]:
    """A GitHub release archive records the repository at a tag, not the text of
    a paper. Citing one as a manuscript's own DOI is the defect that shipped in
    README.md and res_nova_manuscript.tex."""
    release = {w["canonical_doi"] for w in reg["works"]
               if w.get("lineage") == "release" and w.get("canonical_doi")}
    if not release:
        return []
    context = re.compile(r"archive|historical|supersed|release|separate lineage",
                         re.I)
    errs = []
    for path in tracked_files():
        rel = str(path.relative_to(ROOT))
        if not rel.endswith(".tex") or is_historical(rel) or "05_lean" in rel:
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for n, line in enumerate(lines, 1):
            # LaTeX wraps; the qualifying wording may sit a line or two away.
            window = "\n".join(lines[max(0, n - 4):n + 3])
            for doi in set(OWN_DOI_RE.findall(line)):
                if doi in release and not context.search(window):
                    errs.append(f"{rel}:{n}: cites {doi}, a GitHub release "
                                f"archive, with no wording marking it as an "
                                f"archive -- do not cite a release as the paper")
    return errs


def check_datacite(reg: dict) -> list[str]:
    errs = []
    for w in reg["works"]:
        doi = w.get("canonical_doi")
        if not doi or not doi.startswith(OWN_PREFIX):
            continue
        try:
            with urllib.request.urlopen(
                    f"https://api.datacite.org/dois/{doi}", timeout=30) as r:
                a = json.load(r)["data"]["attributes"]
        except Exception as e:                       # network or 404
            errs.append(f"{doi}: did not resolve at DataCite ({e})")
            continue
        title = (a.get("titles") or [{}])[0].get("title", "")
        if title.strip() != w.get("title", "").strip():
            errs.append(f"{doi}: registry title differs from DataCite\n"
                        f"      registry: {w.get('title')!r}\n"
                        f"      DataCite: {title!r}")
        creators = "; ".join(c.get("name", "") for c in a.get("creators", []))
        if creators.strip() != w.get("author", "").strip():
            errs.append(f"{doi}: registry author {w.get('author')!r} "
                        f"differs from DataCite {creators!r}")
        ver = a.get("version") or ""
        if ver.strip() != (w.get("version") or "").strip():
            errs.append(f"{doi}: registry version {w.get('version')!r} "
                        f"differs from DataCite {ver!r}")
    return errs


# --------------------------------------------------------------- self-test ---
def self_test() -> int:
    import tempfile
    good = '''identity:
  name: "R.W. Yett"
  orcid: "0009-0001-1303-7190"
works:
  - work_id: a
    title: "A Paper"
    author: "Yett, R.W."
    orcid: "0009-0001-1303-7190"
    canonical_doi: "10.5281/zenodo.1"
    version: "1.0.0"
    status: live
'''
    bad_orcid = good.replace('orcid: "0009-0001-1303-7190"\nworks',
                             'orcid: "0000-0000-0000-0000"\nworks')
    dup = good + '''  - work_id: a
    title: "A Paper"
    author: "Yett, R.W."
    orcid: "0009-0001-1303-7190"
    canonical_doi: "10.5281/zenodo.1"
    version: "1.0.0"
    status: live
'''
    fails = 0
    with tempfile.TemporaryDirectory() as d:
        for name, text, want in (("good", good, 0), ("bad_orcid", bad_orcid, 1),
                                 ("dup", dup, 2)):
            p = Path(d) / f"{name}.yaml"
            p.write_text(text, encoding="utf-8")
            got = len(check_registry_shape(load_registry(p)))
            if got != want:
                print(f"SELF-TEST FAIL: {name} produced {got} errors, expected {want}",
                      file=sys.stderr)
                fails += 1
    reg = load_registry()
    if REGISTRY.exists() and len(reg["works"]) == 0:
        print("SELF-TEST FAIL: real registry parsed to zero works", file=sys.stderr)
        fails += 1
    if fails:
        return 1
    print(f"audit_publication_metadata self-test: PASS "
          f"(parser + shape checks; {len(reg['works'])} works in the live registry)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--online", action="store_true",
                    help="also verify every canonical DOI against DataCite")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--report", metavar="PATH",
                    help="also write the audit report to PATH, for archiving "
                         "alongside a release")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    reg = load_registry()
    if not reg["works"]:
        print("PUBLICATION METADATA AUDIT: no registry found at "
              f"{REGISTRY.relative_to(ROOT)}", file=sys.stderr)
        return 1

    sections = [
        ("Registry shape", check_registry_shape(reg)),
        ("DOI registry coverage", check_coverage_and_surfaces(reg)),
        ("Local title vs registry", check_local_titles(reg)),
        ("Manuscript bylines", check_bylines()),
        ("Release-vs-paper lineage", check_release_lineage(reg)),
    ]
    if args.online:
        sections.append(("DataCite agreement", check_datacite(reg)))

    import datetime
    import subprocess as sp
    head = sp.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
                  capture_output=True, text=True).stdout.strip()
    tag = sp.run(["git", "-C", str(ROOT), "describe", "--tags", "--abbrev=0"],
                 capture_output=True, text=True).stdout.strip() or "(untagged)"
    out: list[str] = []

    def emit(line: str = "") -> None:
        out.append(line)
        print(line)

    emit("PUBLICATION METADATA AUDIT")
    emit("-" * 26)
    emit(f"{'Date (UTC)':<28} {datetime.datetime.now(datetime.UTC):%Y-%m-%d %H:%M}")
    emit(f"{'Commit':<28} {head}")
    emit(f"{'Tag':<28} {tag}")
    emit(f"{'Mode':<28} {'online (DataCite)' if args.online else 'offline'}")
    emit()
    total = 0
    for name, errs in sections:
        emit(f"{name:<28} {'PASS' if not errs else f'FAIL ({len(errs)})'}")
        total += len(errs)
    if not args.online:
        emit(f"{'DataCite agreement':<28} SKIPPED (pass --online)")
    emit(f"{'Works in registry':<28} {len(reg['works'])}")
    emit(f"{'Identity':<28} {reg['identity'].get('name')} "
         f"<{reg['identity'].get('orcid')}>")
    for g in reg.get("known_gaps", []):
        emit(f"{'Known gap (WARN)':<28} {g.get('doi')} -- {g.get('issue', '')[:60]}")
    emit()
    emit(f"{'VERDICT':<28} {'PASS' if not total else f'FAIL ({total} finding(s))'}")
    if total:
        emit()
        for name, errs in sections:
            for e in errs:
                emit(f"  [{name}] {e}")
    if args.report:
        Path(args.report).write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"\nreport written to {args.report}")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
