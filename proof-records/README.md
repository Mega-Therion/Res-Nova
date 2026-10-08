# Proof receipts (vkernel/0.1) for the `[P]` rows

Signed records of a Lean run on `05_lean_formalization` at the commit in the file name. They come from `4Leibniz/scripts/vkernel` (`attest.py`), and each has a vacuity-screen sidecar (`*.vacuity.json`). No tier anywhere was changed by producing them.

## Records
| record | config | theorems | result |
|---|---|---:|---|
| `ResNova_cb8ee9b.json` | `05_lean_formalization/vkernel.res-nova.json` | 44 | accepted: build 0, probe 0, 0 missing, all on the standard 3 axioms, leanchecker clean on 6 modules |
| `ResNovaD8_cb8ee9b.json` | `05_lean_formalization/vkernel.res-nova-d8.json` | 6 | accepted, same checks |

The second record is separate because `PrintAxiomsD8.lean` re-declares names from `TensorSpeed.lean`, so the two can't be imported into one probe.

Verify without Lean (Python + PyNaCl). A source change makes a record stale, and it then fails `--source`:

    V=../4Leibniz/scripts/vkernel
    python3 $V/verify.py proof-records/ResNova_cb8ee9b.json $V/trusted_signers.json --source 05_lean_formalization --require-checker

What a record establishes and what it does not is in `4Leibniz/scripts/vkernel/README.md`. It has `nonvacuity: not-established` and `statement_match: not-checked`.

## [P] rows against receipts (`p_receipt_check.py`, 2026-10-08)
Row → module map: `P_ROWS.json`. Run: `python3 ../4Leibniz/scripts/vkernel/p_receipt_check.py proof-records/P_ROWS.json proof-records 05_lean_formalization`

| row | tier | module named in row | modules | receipt verifies | vacuity screen of the row's theorems |
|---|---|---|---|---|---|
| D1 | [P] | no | none | no receipt | - |
| D2 | [P] | yes | MuNDuality | yes | PASS 6 |
| D3 | [P/O] | no | none (CAS result) | - | - |
| D5 | [P/O] | yes | CoshCosmology | yes | FIELD-ID/unfolded 2, PASS 4 |
| D6 | [P/O] | no | none | - | - |
| D7 | [P/O] | no (inferred) | AeSTStealthSector | yes | CLOSED-ARITH/unfolded 1, REFLEXIVE/unfolded 4, RING-ID/unfolded 4 |
| D8 | [P] | no (inferred) | TensorSpeed, PrintAxiomsD8 | yes | 14 of 16 flagged: RING-ID 2, RING-ID/unfolded 4, FIELD-ID 1, FIELD-ID/unfolded 3, CLOSED-ARITH/unfolded 2, HYP-RESTATED 1, HYP-PINNED/FIELD-ID 1; PASS 2 |
| D9 | [P] | yes | SZStdEmbedding | yes | PASS 4, RING-ID/unfolded 1 |
| MuStdFoundations (line ~103) | [P] | yes | MuStdFoundations | yes | PASS 7, RING-ID/unfolded 1 |

Exit 1: 1 of 5 `[P]` rows has no verifying receipt (D1).

## Findings `[O]` (for RY; no tier changed)
1. **D1 is `[P]` and names no Lean module.** The legend says: "Name the module and theorem. If you cannot, it is not `[P]`."
2. **D8 is `[P]` and its row names no module.**
   - Its modules (`TensorSpeed`, `PrintAxiomsD8`) are `ARITH` in `docs/grounding_ledger.yaml`, and the screen flags 14 of their 16 theorems.
   - The two direct catches:
     - `physical_frame_tensor_speed_unity`: `(h_lum : c_T_g = 1) : c_T_g = 1 := h_lum`;
     - `gw170817_concordance`: it assumes `c_T = 1` and `c_γ = 1`, then shows `|c_T/c_γ − 1| < ε`.
   - Under the legend this Lean is `[arith]`: the physics of c_T = c is in the prose, not in these proofs.
3. **`AeSTStealthSector` (inferred for D7): all 9 theorems are flagged.**
   - The four PPN theorems are `rfl` on a structure literal (`gamma := 1, beta := 1, alpha1 := 0, …`). The PPN values are inputs typed into the structure, not results.
   - The ledger rates the module `STRUCT`.
   - The evidence for "every PPN parameter is GR" is the symbolic check (note 7 §34), not this module.
4. **`docs/grounding_ledger.yaml` is stale.** It lists 8 theorems for `AeSTStealthSector` (the file has 9), and `MuNDuality` and `SZStdEmbedding` are absent.

## Limits of the screen
- PASS means none of its patterns fired: reflexive, closed arithmetic, ring identity, field identity, hypothesis restated, hypotheses pinning the variables, or contradictory premises. It does not establish non-vacuity.
- Classes ending in `/unfolded` are weaker. They fire only after the project's own definitions are expanded, and one genuine chyren-aeon replacement (`powerDual_involutive`) is flagged that way.
- Calibration (8/8 known-vacuous flagged, 4/4 genuine pass) is in `4Leibniz/scripts/vkernel/calibration/`.
