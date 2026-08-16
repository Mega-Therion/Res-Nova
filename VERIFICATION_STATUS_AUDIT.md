# A — Verification-Status Correction (proposal)

> **Implemented 2026-08-16** on branch `audit/lean-inventory-o5-packaging` (commits `109d38b`, `637e60d`, and this one). Written as a proposal; the approved subset has since been applied. Nothing is merged or tagged.

Authority: `origin/main` @ `52d8688` + `git ls-files`. Date: 2026-08-16.
Covenant tiers `[P]/[D]/[C]/[O]` only (`AGENT_COVENANT.md:14-17`). No new tier introduced.

---

## 1. The premise of this workstream was wrong, and I am the one who got it wrong

I reported that `lake`, `lean`, and `elan` were absent. **They are installed**
(`~/.elan/bin/`, Lean `4.33.0-rc1`), and the pinned Mathlib is present at
`05_lean_formalization/.lake/packages/mathlib`. I inherited "NOT FOUND" from the earlier
agent's report and repeated it without testing. That single unchecked claim is what made the
suite look unverifiable.

**I ran the gate. It passes.**

```
verified: 17 / 17 target(s)
RESULT: PASS          exit_status: 0
```

Evidence archived at `VERIFICATION_RUN_003/01_lean/` — `GATE_TRANSCRIPT.txt`,
`RUN_003_RESULT.json`, `SHA256SUMS.txt`.

| O8 requirement | Status |
|---|---|
| (a) pinned toolchain | **met** — `leanprover/lean4:v4.33.0-rc1`, Lean `4.33.0-rc1` |
| (b) pinned Mathlib **from a fresh clone** | **not met** — Mathlib was already present. Rev matches `5eec30bc…` exactly, 0 dirty files, but it was not freshly fetched. **This is O6, still open.** |
| (c) reviewed source change for the gate/import error | **met** — approved and committed as `109d38b` |
| (d) every intended target runs successfully | **met** — 17/17 |
| (e) archived transcript, versions, SHA, targets, exit codes, SHA-256 | **met** — `VERIFICATION_RUN_003/` |

## 2. The PASS depends on deliverable B — verified counterfactually

Unpatched `PrintAxioms.lean` from `origin/main`, run under the pinned toolchain:

```
PrintAxioms.lean:12:14: error(lean.unknownIdentifier): Unknown constant `raqual_superluminal_obstruction`
… 6 total          lean exit status: 1
```

So on `origin/main` as it stands, the gate fails. The 17/17 result describes the **proposed**
tree, not the current one.

### 2.1 The old gate could not have detected this

Lean 4.33 formats the message as `error(lean.unknownIdentifier):` — which does **not** contain
the literal substring `error:`. Tested directly:

| Criterion | Result on the broken file |
|---|---|
| old gate, `grep -q "error:"` | **no match → would have reported `OK`** |
| new gate, Lean's exit status ≠ 0 | **caught, fails correctly** |

The old success criterion was not merely weak, as you suspected — under this Lean version it
was **blind to compilation failure**. Any module that failed to elaborate would have been
reported `OK`, and the axiom/`sorry` checks that follow would have run against error output.
This is the single strongest reason to take deliverable B.

## 3. What the earlier runs actually were

| | RUN_001 | RUN_002 | **RUN_003 (this)** |
|---|---|---|---|
| Targets | 6 | 7 | **17** |
| Exit 0 | 5 | 7 | **17** |
| Tree | `./` | same | **this repo** |
| Mathlib | unpinned, 6 pkgs dirty | same | **`5eec30bc`, 0 dirty** |
| Lean | `4.33.0` (`d8b1897`) | same | **`4.33.0-rc1` (`62eed1db`)** — the pinned one |
| Ran the gate? | no (`run_lean_verification.py`) | no | **yes** |

The `MuProjection.lean` FAIL I flagged earlier is **closed** — RUN_002 (`fa9f8ba`) fixed it, and
RUN_003 confirms. I was wrong to leave it open.

## 4. Proposed provenance language

Replacing "recorded PASS" in `final_manuscript.tex:226` — factual, no prestige language:

> **Verification provenance.** The gate `verify_all_proofs.sh` elaborates all 17 declared
> targets with exit status 0, no `sorry`, and axiom footprints confined to
> `{propext, Classical.choice, Quot.sound}`, under Lean `v4.33.0-rc1` and Mathlib `5eec30bc`
> (transcript and checksums: `VERIFICATION_RUN_003/`). The Mathlib checkout was already present
> rather than obtained by `lake exe cache get` on a blank machine; cold-clone reproduction
> remains open problem O6. Elaboration certifies that each statement follows from its encoded
> definitions. It does not certify that the encoded definitions model the physical system, nor
> that assumptions carried as typeclass or structure fields are justified — see
> `THEORY_ASSUMPTION_AUDIT.md`.

Replacing "zero custom unproven axioms":

> The suite declares no Lean global `axiom`. This is a statement about `axiom` declarations
> only. Assumptions are present, carried as typeclass fields (`AXIOMS_V2.lean` A1–A5), structure
> fields (`ChiralThresholdState`, `BKMVorticityState`), and theorem hypotheses. A theorem proved
> conditional on an assumed field is not an independent derivation of that field.

## 5. O-numbering

O1–O6 unchanged. `OPEN_PROBLEMS_AND_TESTS.md` already uses **O7** (`PAPER_01` arcsinh), so the
number you named is taken; renumbering is what you told me to avoid. If an item is still wanted
it should be **O8**, cross-referenced from O6.

But on the evidence above, O8-as-specified is largely **already closed** by RUN_003. What
remains genuinely open is narrower, and I recommend recording it against **O6** instead of
opening O8 at all:

> O6 (amended): the suite builds green in-tree under pinned dependencies
> (`VERIFICATION_RUN_003/`). Not demonstrated: `lake exe cache get` on a machine with no
> pre-existing Mathlib.

Your call. I have not edited `OPEN_PROBLEMS_AND_TESTS.md`.

---

# F — `[P]` claims to suspend

Because the gate now passes, **Ground 1 (not mechanically verified) is discharged for every
Lean-backed claim.** What remains is Ground 2: claims the cited declaration does not support.
Compilation does not fix these.

## F.1 Suspend — cited artifact does not contain the claim

| ID | File | Current | Why it fails | Proposed |
|---|---|:---:|---|:---:|
| **D3.1** | `EPISTEMIC_BOUNDARY_v1.5.0.md:22` | `[P]` | Claim is `lim_{x→∞} μ(x) = 1`. `PPNLimits.lean` contains only finite-threshold bounds (`solar_system_precision_bound` x ≥ 10⁴, `cassini_radar_delay_satisfied` x ≥ 6×10⁷). `grep 'Tendsto\|atTop'` across all 17 modules → **no asymptotic limit is formalized anywhere**. The other "limit" theorems are a bound (`mu_derived_newtonian_bound`: `μ(x) < 1`) and an identity (`sz_newtonian_limit_diff`). | `[O]` — or restate as the bound actually proved |
| **CLM-03** | `CLAIM_EVIDENCE_LEDGER.md:13` | `[P] Proved` | Horizon/KMS temperature matching. **No Lean theorem formalizes KMS or temperature anywhere.** Evidence cited is Gibbons–Hawking + Unruh literature. `EPISTEMIC_BOUNDARY` D4.4 already holds `a₀ = cH₀/2π` as `[O]`; the two ledgers contradict each other. | `[C]` for the cited results, `[O]` for the identification |

## F.2 Suspend — unsanctioned tier, not a downgrade

| ID | File | Current | Proposed |
|---|---|:---:|:---:|
| **D3.2** | `EPISTEMIC_BOUNDARY_v1.5.0.md:23` | `[P]`-cond | `[P]` with the condition stated in the boundary cell. `[P]`-cond is not a covenant tier. |
| Table 2 row | `final_manuscript.tex:238` | `[P-cond]` | same |

## F.3 Reword, do not retag — `[P]` stands, description is wrong

| ID / location | Issue |
|---|---|
| **F7** (`EPISTEMIC_BOUNDARY_v1.5.0.md:41`) | "0 `sorry`, axioms {…}" is now **supported** by RUN_003. But the boundary cell says *"Last reported PASS used a local Mathlib build"* — supersede with RUN_003 provenance. The implicit "no unproven axioms" reading needs §4 language. |
| **CLM-08** (`CLAIM_EVIDENCE_LEDGER.md:18`) | Accurate for its 7 modules and its cited artifact exists. Broaden to 17 with RUN_003, or leave and add scope note. **This was the one Lean claim in the repo that was already honest.** |
| `PPNLimits.lean` Table 2 row | Says "Newtonian and deep-MOND limits". File proves solar-system PPN precision bounds. Real file, wrong description. |
| `:215`, `:240` | γ_PPN = 1 credited to `SkordisZlosnikEmbedding.lean`; theorem is `CovariantCompletion.disformal_gamma_ppn_unity`. |
| `SovereignRegularity` row + appendix `:20` | "BKM integral boundedness" — no integral and no PDE are formalized. See `THEORY_ASSUMPTION_AUDIT.md` §3. |
| `YettParadigm` row + appendix `:19` | "Spectral gap positivity" — the gap `κ² ≤ λ₁ − λ₀` is an assumed structure field. |

## F.4 Not suspended

`D1.2`, `D2`, `D3.3`, `D5`, `D6`, `D7`, `D8`, `D9` — backing modules all elaborate in RUN_003.
`[P]` stands, subject to the §4 provenance wording. `D1.1` is not Lean-backed. All `D4.x`
empirical `[D]` claims are unaffected.

## F.5 Count claims, unchanged by verification

`reproducibility_appendix.tex:4` ("7 modules") and `RES_NOVA_VERIFICATION_LEDGER.md:184`
("all 7 modules") contradict 17. `EPISTEMIC_BOUNDARY_v1.3.0.md:31` says 7 and Lean 4.17.0, and
carries a `` link.
