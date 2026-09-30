#!/usr/bin/env python3
"""Check references.bib against the registries its identifiers point to.

A citation is a claim that a specific document exists and says what the corpus
says it says. This corpus has shipped fabricated evidence before (the
`a0_z_analysis.png` figure: 3 of 5 points invented) and a "reported" result
whose supporting paper was never published (AeST's CMB initial conditions,
CURRENT_STATE 2b). A bibliography entry is the cheapest place for the same
failure to hide: a plausible DOI that resolves to a different paper, or an
arXiv number that does not exist.

For every entry this resolves the DOI (Crossref) and/or the arXiv id (arXiv
API) and compares the registered title and year with the .bib fields.

    python3 scripts/audit_bibliography.py            # offline: syntax only
    python3 scripts/audit_bibliography.py --online   # resolve every identifier
    python3 scripts/audit_bibliography.py --online --json out.json

Exit 1 when --online finds an identifier that does not resolve or resolves to a
document whose title does not match. Title similarity is a token-set ratio, so
LaTeX markup and word-order differences do not trip it; a mismatch is printed
with both titles for a human to judge. Year differences of one (preprint vs.
journal) are reported but are not failures.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "references.bib"
UA = "Res-Nova-bibliography-audit/1.0 (https://github.com/Mega-Therion/Res-Nova)"
TITLE_MATCH = 0.6

ENTRY = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)\n\}", re.S)
FIELD = re.compile(r"(\w+)\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|\"[^\"]*\"|\d+)", re.S)
ARXIV_ID = re.compile(r"(\d{4}\.\d{4,5}|[a-z\-]+(?:\.[A-Z]{2})?/\d{7})(v\d+)?", re.I)


def parse(text: str) -> list[dict]:
    out = []
    for kind, key, body in ENTRY.findall(text):
        fields = {}
        for name, raw in FIELD.findall(body):
            fields[name.lower()] = raw.strip("{}\"").strip()
        out.append({"type": kind.lower(), "key": key, **fields})
    return out


def arxiv_of(e: dict) -> str | None:
    for f in ("eprint", "arxiv", "journal", "note", "url"):
        v = e.get(f, "")
        if f in ("eprint", "arxiv") or "arxiv" in v.lower():
            m = ARXIV_ID.search(v)
            if m:
                return m.group(1)
    return None


def norm_tokens(s: str) -> set[str]:
    s = re.sub(r"\\[a-zA-Z]+|[{}$\\^_]", " ", s)
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) > 2}


def similarity(a: str, b: str) -> float:
    ta, tb = norm_tokens(a), norm_tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / min(len(ta), len(tb))


def get(url: str) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as err:
            if err.code == 404:
                return None
            time.sleep(2 ** attempt)
        except OSError:
            time.sleep(2 ** attempt)
    raise RuntimeError(f"network failure fetching {url}")


def crossref(doi: str) -> dict | None:
    raw = get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/"))
    if raw is None:
        return None
    msg = json.loads(raw)["message"]
    year = None
    for k in ("published-print", "published-online", "issued"):
        parts = msg.get(k, {}).get("date-parts") or [[None]]
        if parts[0][0]:
            year = parts[0][0]
            break
    return {"title": " ".join(msg.get("title") or [""]), "year": year}


def arxiv(aid: str) -> dict | None:
    raw = get("https://export.arxiv.org/api/query?id_list=" + urllib.parse.quote(aid))
    if raw is None:
        return None
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(raw)
    entry = root.find("a:entry", ns)
    if entry is None or entry.find("a:title", ns) is None:
        return None
    title = " ".join((entry.findtext("a:title", "", ns) or "").split())
    if not title or title.lower() == "error":
        return None
    pub = entry.findtext("a:published", "", ns) or ""
    return {"title": title, "year": int(pub[:4]) if pub[:4].isdigit() else None}


def check(e: dict) -> list[dict]:
    """Return one finding per identifier on the entry."""
    findings = []
    title, year = e.get("title", ""), e.get("year", "")
    year = int(year) if str(year).isdigit() else None
    for kind, ident, fetch in (("doi", e.get("doi"), crossref), ("arxiv", arxiv_of(e), arxiv)):
        if not ident:
            continue
        rec = fetch(ident)
        time.sleep(0.4 if kind == "doi" else 3.1)  # arXiv asks for >= 3 s between calls
        f = {"key": e["key"], "id_type": kind, "id": ident, "bib_title": title}
        if rec is None:
            f.update(status="UNRESOLVED")
        else:
            sim = similarity(title, rec["title"])
            f.update(registered_title=rec["title"], registered_year=rec["year"],
                     similarity=round(sim, 2))
            if sim < TITLE_MATCH:
                f["status"] = "TITLE_MISMATCH"
            elif year and rec["year"] and kind == "arxiv" and 0 <= year - rec["year"] <= 3:
                # A preprint routinely precedes its journal version by 1-3 years.
                f["status"] = "OK" if year == rec["year"] else "OK_PREPRINT_EARLIER"
            elif year and rec["year"] and abs(year - rec["year"]) > 1:
                f["status"] = "YEAR_MISMATCH"
            elif year and rec["year"] and year != rec["year"]:
                f["status"] = "OK_YEAR_OFF_BY_ONE"
            else:
                f["status"] = "OK"
        findings.append(f)
    if not findings:
        findings.append({"key": e["key"], "id_type": None, "id": None,
                         "bib_title": title, "status": "NO_IDENTIFIER"})
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--online", action="store_true", help="resolve identifiers")
    ap.add_argument("--json", type=Path, help="write findings as JSON")
    args = ap.parse_args()

    entries = parse(BIB.read_text(encoding="utf-8"))
    keys = [e["key"] for e in entries]
    dupes = sorted({k for k in keys if keys.count(k) > 1})
    problems = [f"duplicate key {k}" for k in dupes]
    problems += [f"{e['key']}: no title" for e in entries if not e.get("title")]
    print(f"{len(entries)} entries parsed from {BIB.name}")
    if not args.online:
        for p in problems:
            print("  " + p)
        print("offline check:", "FAIL" if problems else "PASS")
        return 1 if problems else 0

    findings = []
    for e in entries:
        findings.extend(check(e))
    bad = {"UNRESOLVED", "TITLE_MISMATCH", "YEAR_MISMATCH"}
    for f in findings:
        if not f["status"].startswith("OK"):
            print(f"  {f['status']:<19} {f['key']} [{f['id_type']}:{f['id']}]")
            if "registered_title" in f and not f["status"].startswith("OK"):
                print(f"      bib: {f['bib_title'][:110]}")
                print(f"      reg: {f['registered_title'][:110]} ({f.get('registered_year')})")
    counts: dict[str, int] = {}
    for f in findings:
        counts[f["status"]] = counts.get(f["status"], 0) + 1
    print("summary:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    if args.json:
        args.json.write_text(json.dumps(findings, indent=2, ensure_ascii=False) + "\n")
    failed = problems or any(f["status"] in bad for f in findings)
    print("online check:", "FAIL" if failed else "PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
