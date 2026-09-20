# CLAUDE.md — Res-Nova

Guidance for Claude Code working in this repository.

## READ FIRST, EVERY SESSION

**Before writing, summarizing, or extending any physics claim, read
`CURRENT_STATE_READ_THIS_FIRST.md` in full.** It exists because on 2026-09-12 an external
agent built four papers on a falsified interpolating function and a substrate retired 19
days earlier, both already corrected on disk before that agent ran. Do not treat the vault's
`raw/Logs/`, `80_Archive/`, or `obsidian_vault_legacy/` as sources of current physics — they
are historical records only. If a legacy source contradicts `CURRENT_STATE_READ_THIS_FIRST.md`,
the current-state file wins, always.

## The gate is the judge

```
cd 05_lean_formalization && bash verify_all_proofs.sh; echo $?
```

Exit 0 is the only definition of done. Not `lake build`, not a module count, not an
assessment.

- Takes ~12 min (30 targets × ~24 s). **Exceeds the 10-min Bash timeout — background it.**
- Needs Mathlib: `lake exe cache get` (~8.2 GB). Without it 30 modules read `MISSING_INPUT`.
- `lake build` alone is **not** the gate. It can pass while a sorried file sits outside the
  lakefile roots — target-drift detection is what catches that.
- Fixed 2026-09-03 (`5932b75`): the sorry check tested `uses 'sorry'` (single quotes) but
  Lean 4 emits ``uses `sorry` `` in **backticks**, so it never fired and two live sorries
  passed a green gate. `lake env lean` also exits 0 on sorries — they are warnings, not
  errors. Do not loosen either check.
- **Regression 2026-09-04:** an uncommitted working-tree edit replaced this gate body with
  a 60-lines-shorter version that grepped the Lean *source text* for `sorry` instead of
  the elaborator's output, and dropped the exit-status check, the axiom check, and the
  TARGETS-vs-lakefile-roots invariant. The same change then deleted the word `sorry` from
  prose comments in `PillarIV_AntiDriftGate.lean` so the new grep would pass. Reverted.
  Editing text so a checker stops firing is the failure mode, not the fix.

## Assurance layer

Before creating any new claim-tracking artifact (e.g. from a GitHub issue naming a
specific path like `evidence/v1/`), check `assurance/claims.json` first — it may
already be the live, CI-gated registry. Extend it in place rather than building a
parallel one.

Four cheap checks run in seconds and gate scope, not mathematics. Run them before the
Lean gate; they catch drift that the Lean gate is too slow to iterate on.

```
python3 scripts/validate_claim_registry.py            # assurance/claims.json well-formed
python3 scripts/check_claim_consistency.py            # claim surfaces match frozen JSON
python3 05_lean_formalization/check_target_inventory.py   # lakefile == gate == on-disk
python3 05_lean_formalization/check_manuscript_inventory.py  # manuscript == disk - adjacent
```

`assurance/claims.json` now covers **all 43 claims**: the 14 in `CLAIM_EVIDENCE_LEDGER.md`,
CLM-15/CLM-16 (Pillar IV), and the 27 new/rescored claims from
`CLAIM_EVIDENCE_LEDGER_v1.6.0_SUPPLEMENT.md` (D2/D3/D5/D6/D7/D9, plus CLM-AX-02 and
CLM-O1-01). Every record also carries `claim_type`, `quotation_type`, `source_locator`,
a `falsifiability` test record, and a `last_verified_commit` (issue #50's schema). A
green registry means every claim carries a state, its artifacts, its assumptions, a
verification command, a stated limitation, and a source locator — it does **not** mean
every claim is proved. `scripts/validate_claim_registry.py` fails closed if a claim's own
`falsifiability.result` is `contradicted` but its `state` still asserts current support
(`formally-verified`/`derived`/`computed`/`empirically-supported`) — such a claim must be
`retracted` or `conditional`. `scripts/test_claim_registry_fixtures.py` exercises that rule
against fixtures in `assurance/fixtures/`. Read the states:
`python3 scripts/generate_assurance_report.py` regenerates the count table in
`assurance/ASSURANCE_REPORT.md`.

Two states are load-bearing and easy to misread. `conditional` (CLM-10) means the algebra
is exact but rests on an adopted premise — `sinh(psi)=1` is not selected by any covariant
argument. `formally-verified` (CLM-11, CLM-13) means the *mathematics* is machine-checked,
not that the physical identification holds; both records say so in `limitations`.

A module in `05_lean_formalization/ADJACENT_MODULES.txt` is scoped out of the manuscript,
never out of the gate. Everything on disk is built and checked.

## Layout

TeX manuscripts live in `01_foundational_action/` and `03_observer_jwst/`.
There is **no `02_manuscript/`** — agents hallucinate that path.

`FIG_TREE_MONOGRAPH.md` is the front door; `FIG_TREE_ASSET_LEDGER.md` inventories every
asset with its measured exit code.

## Conventions

`[P]` proved · `[D]` derived · `[A]` axiom · `[C]` **cited** · `[conj]` conjectured · `[E]` empirical · `[O]` open · `[X]` killed.

`[C]` is **Cited**, not conjectured — see `docs/EPISTEMIC_TIER_LEGEND.md`, which is
canonical. This line read "`[C]` conjectured" until 2026-09-20, inverting the
evidentiary weight of every citation a reader checked against it.

Record failed identities and rejected coincidences explicitly rather than dropping them.
See `Chyren_Second_Brain/50_Mathematical_Notation/derivations/D41`, which logs a
convention artefact that looked like a result — kept so it is not rediscovered and
published.

`sorry`-free is not substantive. The test is **substitutability**: replace the physics in
a statement with nonsense and see whether the same proof still closes.

## Pillar IV — read before touching §VI

The anti-drift gate `u ≥ γ ⟺ χ ≥ θ` is **false and retracted (2026-09-03)**. The GKSL
steady-state coherence `C(x) = 4x/(1+8x²)` is non-monotonic — it peaks at θ and decays —
while `μ(x) = x/√(1+x²)` rises monotonically. θ is a **ceiling**, not a gate. See
`PillarIV_AntiDriftGate.lean` and §VI of the monograph.
