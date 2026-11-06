#!/usr/bin/env python3
"""
Reproduce the Lelli+2016c catalogue values that BLK-1017 and
EHYEH_AUDIT_AND_SALVAGE_SKETCH_2026-11-05.md cite.

Why this exists: both audit documents compare the E.H.Y.E.H. manuscript's Table II
against `SPARC_Lelli2016c.mrt`, but that file was not in this repository and no
script reproduced the comparison. This pins the source file by SHA-256 and makes
the audit's numbers independently checkable.

Exit 0 when every pinned value matches the catalogue.
"""
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CATALOGUE = HERE / "SPARC_Lelli2016c.mrt"
EXPECTED_SHA256 = "5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243"
N_GALAXIES = 175

# Values asserted by the audits, and the manuscript's printed value where known.
PINNED = {
    "DDO154":  {"Vflat": 47.0,  "e_Vflat": 1.0, "manuscript_printed": (51.3, 1.5)},
    "NGC2841": {"Vflat": 284.8, "e_Vflat": 8.6, "manuscript_printed": None},
}

fails = 0

def check(ok, label):
    global fails
    print(("PASS " if ok else "FAIL ") + label)
    fails += 0 if ok else 1

def parse(path):
    rows = {}
    for ln in path.read_text().splitlines():
        p = ln.split()
        if len(p) < 19 or not p[0][0].isalnum():
            continue
        try:
            rows[p[0]] = {
                "T": int(p[1]),
                "distance_Mpc": float(p[2]),
                "Inc_deg": float(p[5]),
                "Rdisk_kpc": float(p[11]),
                "MHI": float(p[13]),
                "Vflat": float(p[15]),
                "e_Vflat": float(p[16]),
                "Q": int(p[17]),
            }
        except (ValueError, IndexError):
            continue
    return rows

def main():
    raw = CATALOGUE.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    check(digest == EXPECTED_SHA256, f"catalogue SHA-256 = {EXPECTED_SHA256[:16]}...")
    rows = parse(CATALOGUE)
    check(len(rows) == N_GALAXIES, f"parsed {len(rows)} galaxies (expected {N_GALAXIES})")

    for name, want in PINNED.items():
        got = rows.get(name)
        if got is None:
            check(False, f"{name} present in catalogue")
            continue
        check(got["Vflat"] == want["Vflat"],
              f"{name} Vflat = {got['Vflat']} km/s (audit: {want['Vflat']})")
        check(got["e_Vflat"] == want["e_Vflat"],
              f"{name} e_Vflat = {got['e_Vflat']} km/s (audit: {want['e_Vflat']})")
        if want["manuscript_printed"]:
            v, e = want["manuscript_printed"]
            check((got["Vflat"], got["e_Vflat"]) != (v, e),
                  f"{name} catalogue ({got['Vflat']} +/- {got['e_Vflat']}) differs from "
                  f"manuscript Table II ({v} +/- {e})")

    print(f"\n{'PASS' if fails == 0 else 'FAIL'}: {fails} failure(s)")
    return 0 if fails == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
