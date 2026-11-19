#!/usr/bin/env python3
"""Fail-closed reproduction runner for the a0(z) V3 chain.

PREREG_A0_OF_Z_V3.md was frozen and executed 2026-09-12. Its two halves have
different provenance status, and this runner is built to keep that distinction
machine-enforced instead of remembered:

  HALF 1  a0 re-extraction from SPARC 175 under mu_std.
          Provenance: VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256
          (175 files). Reproducible. Guarded here.

  HALF 2  the a0(z) discrimination on the 20-point high-z table.
          Provenance: NONE. That table was withdrawn 2026-09-27 in
          03_observer_jwst/O4_REAL_DATA_MUSE_DARK_III_2026-09-27.md §1:
          Bouche+2021 (A&A 654, A49) is a 9-galaxy angular-momentum pilot and
          "Mercier+2022 A&A 667 A75" does not exist. The V3 verdict therefore
          rests on data that has since been withdrawn. This runner REFUSES to
          emit a verdict and says why.

Exit codes
  0  extraction reproduced exactly AND a provable discrimination dataset was supplied
  1  provenance or reproduction FAILED (bad hash, missing data, drift) -> fail closed
  2  extraction reproduced, but the discrimination dataset is withdrawn/unprovenanced,
     so no verdict may be issued. This is the expected code today.

Usage
  python3 scripts/a0_z_v3_fail_closed.py --sparc /tmp/sparc_check \
      [--discrimination <manifest.json>] [--receipt out.json]
"""
from __future__ import annotations

import argparse, glob, hashlib, json, math, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / "VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256"
RECORDED = REPO / "02_galaxy_dynamics/A0_REEXTRACTION_MU_STD.json"
PREREG_V3 = REPO / "03_observer_jwst/PREREG_A0_OF_Z_V3.md"
WITHDRAWAL = REPO / "03_observer_jwst/O4_REAL_DATA_MUSE_DARK_III_2026-09-27.md"

# Tolerances: the recorded JSON stores only 5 significant figures (1.1562e-10),
# so the guard can only verify to that record's own precision -- 1e-4 relative.
# The extraction is deterministic (fixed RNG seed 42), so any real drift shows up
# far above this floor. Do not loosen this to hide a genuine mismatch.
TOL_A0 = 1e-4      # relative, = precision of the recorded figures
TOL_CI = 1e-4      # relative


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_sparc(sparc_dir: Path) -> dict:
    """Every rotmod must match the committed manifest. No manifest, no run."""
    if not MANIFEST.exists():
        return {"ok": False, "reason": f"manifest missing: {MANIFEST.relative_to(REPO)}"}
    expected = {}
    for line in MANIFEST.read_text().splitlines():
        parts = line.split()
        if len(parts) == 2:
            expected[parts[1]] = parts[0]
    files = sorted(sparc_dir.glob("*_rotmod.dat"))
    if len(files) != len(expected):
        return {"ok": False, "reason": f"file count {len(files)} != manifest {len(expected)}"}
    bad, missing = [], []
    for name, digest in expected.items():
        f = sparc_dir / name
        if not f.exists():
            missing.append(name)
            continue
        if sha256(f) != digest:
            bad.append(name)
    return {"ok": not bad and not missing, "checked": len(files),
            "mismatched": bad[:5], "missing": missing[:5],
            "manifest": str(MANIFEST.relative_to(REPO))}


def run_extraction(sparc_dir: Path, out: Path) -> dict:
    """Run the corpus's own harness. It is the authority, not this file."""
    script = REPO / "02_galaxy_dynamics/sparc_a0_reextract_std.py"
    r = subprocess.run([sys.executable, str(script), str(sparc_dir), str(out)],
                       cwd=REPO, capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        return {"ok": False, "reason": "harness failed", "stderr": r.stderr[-500:]}
    return {"ok": True, "stdout": r.stdout.strip().splitlines()[-4:], "json": json.loads(out.read_text())}


def compare_extraction(actual: dict, recorded: dict) -> dict:
    """Both mu functions are checked. A drift in the control is as fatal as one in std."""
    out, ok = {}, True
    keys = {"std": "mu_std", "dual": "mu_dual"}
    for mu, rkey in keys.items():
        a, e = actual[mu], recorded[rkey]
        d = abs(a["a0_best"] - e["a0_best"]) / e["a0_best"]
        ci = [abs(x - y) / y for x, y in zip(a["bootstrap_68"], e["bootstrap_68"])]
        good = d <= TOL_A0 and max(ci) <= TOL_CI
        ok &= good
        out[mu] = {"recorded": e["a0_best"], "reproduced": a["a0_best"],
                   "rel_diff": d, "ci_rel_diff": ci, "match": good}
    return {"ok": ok, "detail": out}


def discrimination_provenance(override: Path | None) -> dict:
    """A verdict needs a dataset whose sources can be traced. Refuse otherwise."""
    if override:
        man = json.loads(Path(override).read_text())
        req = {"source", "arxiv_or_doi", "sha256", "n_points", "redshift_range"}
        if not req <= set(man):
            return {"usable": False, "reason": f"manifest missing fields: {sorted(req - set(man))}"}
        return {"usable": True, "source": man["source"], "n": man["n_points"]}

    withdrawn = WITHDRAWAL.exists() and "withdrawn" in WITHDRAWAL.read_text()[:4000].lower()
    table_withdrawn = False
    for script in ("03_observer_jwst/a0_of_z.py", "03_observer_jwst/a0_of_z_v2.py"):
        p = REPO / script
        if p.exists() and "DATA WITHDRAWN" in p.read_text()[:600]:
            table_withdrawn = True
    return {"usable": False,
            "reason": ("the 20-point high-z table is WITHDRAWN [X] (2026-09-27) and the "
                       "V3 execution predates the withdrawal"),
            "evidence": [str(WITHDRAWAL.relative_to(REPO)) if withdrawn else None,
                         "a0_of_z.py / a0_of_z_v2.py carry a DATA WITHDRAWN header"
                         if table_withdrawn else None],
            "consequence": ("PREREG_A0_OF_Z_V3.md's INCONCLUSIVE verdict cannot be "
                            "re-issued from this table. It is retained as a record of what "
                            "was computed, not as current evidence. a0(z) stays [O]."),
            "route_forward": ("03_observer_jwst/PREREG_A0_OF_Z_V3.md already requires a "
                              "JWST-era z>1.5 dataset; the current live attempt is "
                              "audits/2026-11-18/a0z_zgt15_manifest.py (RC100, [U] INCONCLUSIVE)")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sparc", required=True)
    ap.add_argument("--discrimination", default=None)
    ap.add_argument("--receipt", default=None)
    a = ap.parse_args()

    receipt = {"runner": "a0_z_v3_fail_closed.py", "prereg": str(PREREG_V3.relative_to(REPO))}

    prov = verify_sparc(Path(a.sparc))
    receipt["sparc_provenance"] = prov
    if not prov["ok"]:
        receipt["verdict"] = "FAIL_CLOSED"
        receipt["reason"] = "SPARC provenance failed; refusing to extract."
        print(json.dumps(receipt, indent=1))
        return 1

    tmp = Path("/tmp/_a0_v3_repro.json")
    run = run_extraction(Path(a.sparc), tmp)
    receipt["extraction_run"] = {"ok": run["ok"]}
    if not run["ok"]:
        receipt["verdict"] = "FAIL_CLOSED"
        receipt["reason"] = run.get("reason")
        print(json.dumps(receipt, indent=1))
        return 1

    cmp = compare_extraction(run["json"], json.loads(RECORDED.read_text()))
    receipt["extraction_reproduction"] = cmp
    receipt["extraction_run"]["harness_tail"] = run["stdout"]
    if not cmp["ok"]:
        receipt["verdict"] = "FAIL_CLOSED"
        receipt["reason"] = "a0 re-extraction drifted from A0_REEXTRACTION_MU_STD.json."
        print(json.dumps(receipt, indent=1))
        return 1

    disc = discrimination_provenance(Path(a.discrimination) if a.discrimination else None)
    receipt["discrimination_provenance"] = disc
    if not disc["usable"]:
        receipt["verdict"] = "EXTRACTION_VERIFIED_NO_VERDICT"
        receipt["reason"] = disc["reason"]
        receipt["tier_effect"] = "none; a0(z) remains [O]; no [P]/[D] upgrade is implied"
        code = 2
    else:
        receipt["verdict"] = "VERDICT_PERMITTED"
        receipt["note"] = "a provable dataset was supplied; the V3 test may be re-run against it"
        code = 0

    print(json.dumps(receipt, indent=1))
    if a.receipt:
        Path(a.receipt).write_text(json.dumps(receipt, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
