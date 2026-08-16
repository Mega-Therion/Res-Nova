# O5 — SPARC Data Packaging: Options Memo

> **Implemented 2026-08-16** on branch `audit/lean-inventory-o5-packaging` (commits `109d38b`, `637e60d`, and this one). Written as a proposal; the approved subset has since been applied. Nothing is merged or tagged.

**Branch:** `audit/lean-inventory-o5-packaging` (from `origin/main` @ `52d8688`)
**Date:** 2026-08-16
**Status:** Option A adopted per instruction; Option B deferred pending redistribution terms.
No SPARC data is added to git; `.gitignore:21-22` stands.

---

## 1. Repository state — confirmed

| Fact | Evidence |
|---|---|
| 175 `*_rotmod.dat` present in the working tree | `02_galaxy_dynamics/sparc_data/` |
| **Zero** of them tracked by git | `git ls-files 02_galaxy_dynamics/sparc_data` → 0 |
| Exclusion is **deliberate and documented** | `.gitignore:21` — `# SPARC rotation curves (public dataset; do not vendor)` |
| A fresh clone cannot run the data-dependent pipeline | follows from the above |

**The exclusion was a prior decision, not an oversight.** `.gitignore:21` and
`SPARC_DATA.md:41` both state the reason: avoid vendoring a public dataset without settling
license terms. Any recommendation to `git add` the data would be reversing a deliberate call.

**Executable portability vs. data reproducibility — these are separate and only one is broken.**
`sparc_paths.py` already resolves the directory through five ordered candidates (CLI → env →
repo-local → cwd → legacy fallback) and raises a `FileNotFoundError` listing every path tried.
The *code* is portable. What a clean clone lacks is the *data*, plus a verified way to get it.

---

## 2. Provenance — stronger than expected

### 2.1 A 175-line SHA-256 manifest is already committed

`VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256` (and an identical copy at
`03_sparc_nuisance_175/`). I verified the working tree against it:

```
sha256sum -c RAW_DATA_MANIFEST.sha256   →   OK: 175 / 175
```

### 2.2 All three copies of the corpus are byte-identical

| Location | Files | Matches committed manifest |
|---|---|---|
| `Res-Nova/02_galaxy_dynamics/sparc_data/` | 175 | **175 / 175** |
| `Chyren/Research_and_Data/.../Datasets/data/sparc_data/` | 175 | identical manifest hash |
| MEGA `/Chyren_Archive/Receipts/zenodo_bundle_staging/sparc_data/` | 175 | **175 / 175** (downloaded and verified) |

There is exactly one corpus. No fork, no ambiguity about which set is canonical.

### 2.3 Source is documented

`SPARC_DATA.md:23` — Lelli, McGaugh & Schombert 2016, *AJ* **152**, 157.
Official distribution: `https://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip`.
`SPARC_DATA.md:27-36` already carries working fetch commands.

### 2.4 What is still missing

- **Retrieval date** and **dataset version** are recorded nowhere.
- The manifest lives under `VERIFICATION_RUN_001/` and is **not referenced** from
  `SPARC_DATA.md`, so nobody following the documented fetch path is told to verify against it.
- **No fetch-and-verify script**, and no CI job that fails on hash drift.
- **Redistribution terms are unresolved.** The SPARC page distributes publicly; I found no
  explicit license grant. **I am not guessing at this** — it is the one open input this memo
  cannot supply, and it is the input that decides between A and B.

### 2.5 Correction to the earlier report

Two claims in `OPEN_PROBLEMS_AND_TESTS.md:69` do not survive checking:

- *"Scripts default to `/home/mega/Chyren/…`"* — **misleading**. That path is fallback
  **#5 of 5** in `sparc_paths.py:22`, reached only after CLI, env, repo-local and cwd all miss.
  It is a real remaining `/home/mega` reference, but it is not a default.
- *"and one path under `/tmp/claude-1000/`"* — **false**. No such path exists in
  `02_galaxy_dynamics/*.py`.

Also, the earlier report said two scripts lack a `--data-dir` override. The real count is
**seven**: `halo_conspiracy.py`, `nfw_constrained.py`, `phase8_btfr_slip_scales.py`,
`sparc_cross_validation.py`, `sparc_derived_closure.py`, `sparc_derived_cross_validation.py`,
`sparc_derived_mu_benchmark.py`. (`phase8_btfr_slip_scales.py` reads no SPARC data at all —
sympy only — so six of the seven matter.)

---

## 3. Option A — Keep data out of git, harden the acquisition path

Build on what already exists rather than adding anything new to the tree.

- Promote `RAW_DATA_MANIFEST.sha256` to a first-class, referenced artifact (or copy it to
  `02_galaxy_dynamics/SPARC_MANIFEST.sha256`) and link it from `SPARC_DATA.md`.
- Add source URL, retrieval date, and dataset version alongside it.
- Add `fetch_sparc.sh`: download → unpack → `sha256sum -c` → fail loudly on drift.
- Add a CI job that verifies hashes when `SPARC_DATA_DIR` is set.
- Add `--data-dir` to the six scripts that need it; move `nfw_constrained.py:37`'s
  `load(SPARC_DIR)` out of import scope into `main()` so a missing directory fails as a
  runtime error rather than an import crash.
- Rewrite O5 to state exactly what a clean clone must do.

**Preferred if** redistribution rights are unclear or repository weight matters.
**Cost:** a clean clone still depends on `astroweb.cwru.edu` staying up. Link rot is the
long-term failure mode.
**Already done:** manifest exists and verifies; source URL and fetch commands documented.
Roughly the packaging work is 80% complete — the gap is the script, the metadata, and the CI gate.

## 4. Option B — Archive the corpus as a versioned research artifact

- Deposit the exact 175-file corpus to Zenodo as a dataset record.
- Record DOI, version, and the checksum manifest in git.
- Keep raw data out of git; make the frozen input independently retrievable **and citable**.

**Preferred if** licensing permits redistribution and archival reproducibility is the goal.
**Cost:** requires the §2.4 licensing answer *before* deposit — a Zenodo deposit is a
redistribution act. Publishing without that answer converts an open question into a
public one.
**Already done:** MEGA `zenodo_bundle_staging/sparc_data/` holds a byte-identical, staged copy
that verifies 175/175 against the committed manifest. If licensing clears, Option B is
substantially pre-built.

---

## 5. What I am not doing

- Not choosing between A and B. Both are live; the licensing answer is the discriminator.
- Not `git add`-ing `sparc_data/`. That would reverse the deliberate `.gitignore:21` decision
  for local convenience, and would create redistribution, repo-weight, and provenance
  exposure without producing a citable dataset release.
- Not treating the PRD-era MEGA artifacts (`sparc_rotation.py`,
  `sparc_dynamic_chi_results.json`) as validation of any v1.5.0 number. Different generation.

## 6. Proposed O5 rewrite — after your decision, not before

Remove the two false/misleading path claims from §2.5. Preserve a narrowly worded open item:
the corpus is present and hash-verified locally, but **fresh-clone acquisition and archival
retrieval remain untested**, and the redistribution terms are unresolved.

**Nothing above is committed.** Awaiting your decision on A vs. B.

---

# E — Option A notes (per instruction: Option A only, Option B deferred)

**Authority correction.** Earlier in this audit I cited the MEGA copy at
`/Chyren_Archive/Receipts/zenodo_bundle_staging/sparc_data/` as corroboration. Per standing
instruction, MEGA is **not claim authority**. Restating on repo evidence alone:

- `VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256` is **tracked in git**
  (175 lines) and is the authority.
- The working-tree corpus verifies against it: `sha256sum -c` → **175/175 OK**.
- `03_sparc_nuisance_175/RAW_DATA_MANIFEST.sha256` is byte-identical to it.
- The MEGA and `Chyren/` copies also match, but that is corroboration only, not authority, and
  no decision below rests on it.

**No force-add.** `.gitignore:21-22` excludes the data deliberately — *"public dataset; do not
vendor"*. That decision stands; nothing here reverses it.

## Option A completion — remaining work

1. Reference the existing manifest from `02_galaxy_dynamics/SPARC_DATA.md`, which currently
   documents the source URL and fetch commands (`:23`, `:27-36`) but never tells the reader to
   verify. Add retrieval date and dataset version — both currently unrecorded.
2. Add one deterministic fetch-and-verify route: download → unpack → `sha256sum -c` → fail
   loudly on drift. Expected outcome for a clean clone stated explicitly: 175 `*_rotmod.dat`,
   manifest verifies, pipeline runs.
3. CI job that fails when `SPARC_DATA_DIR` is set and hashes drift.

## O5 language corrections (evidence-backed)

`OPEN_PROBLEMS_AND_TESTS.md:69` currently says *"Scripts default to `/home/mega/Chyren/...` and
one path under `/tmp/claude-1000/`."*

- **`/home/mega/Chyren/...` is a final fallback, not a default.** `sparc_paths.py:22` places it
  fifth, after CLI `--data-dir`, `SPARC_DATA_DIR`/`SPARC_DATA`, repo-local, and cwd-local.
- **`/tmp/claude-1000` is not a current dependency.** `grep -rE '/tmp/claude' 02_galaxy_dynamics/*.py`
  returns nothing.

## Resolver support vs. CLI flag — reported separately, as instructed

All data-reading scripts in `02_galaxy_dynamics/` go through the shared resolver, so all of them
honour `SPARC_DATA_DIR`. The gap is only the per-script CLI flag.

| Script | `--data-dir` | Uses shared resolver / `SPARC_DATA_DIR` |
|---|:---:|:---:|
| `halo_conspiracy.py` | **no** | yes (imports `SPARC_DIR` from `parameter_ledger.py`) |
| `nfw_constrained.py` | **no** | yes (same) |
| `sparc_cross_validation.py` | **no** | yes |
| `sparc_derived_closure.py` | **no** | yes |
| `sparc_derived_cross_validation.py` | **no** | yes |
| `sparc_derived_mu_benchmark.py` | **no** | yes |
| `phase8_btfr_slip_scales.py` | **no** | **n/a — reads no SPARC data (sympy only)** |

Six scripts lack the flag but remain configurable by environment variable; the seventh needs
neither. Separately, `nfw_constrained.py:37` calls `load(SPARC_DIR)` at **import** time, so a
missing directory raises on import rather than inside `main()`.

**Option B (Zenodo) deferred** pending confirmed redistribution terms. Not chosen, not staged.
