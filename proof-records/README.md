# Proof receipts (vkernel/0.1) for the `[P]` rows

Signed records of a Lean run on `05_lean_formalization` at the commit in the file name. They come from `4Leibniz/scripts/vkernel` (`attest.py`), and each has a vacuity-screen sidecar (`*.vacuity.json`). No tier anywhere was changed by producing them.

## Records
| record | config | theorems | result |
|---|---|---:|---|
| `ResNova_b59b56f.json` | `05_lean_formalization/vkernel.res-nova.json` | 47 | accepted: build 0, probe 0, 0 missing, all on the standard 3 axioms. Adds `MuStdUniqueness` (D1's core) to the 2026-10-08 set |
| `ResNovaD8_b59b56f.json` | `05_lean_formalization/vkernel.res-nova-d8.json` | 6 | accepted, same checks |

The Lean sources are those of `main` at `b59b56f` (the #141 merge). That merge changed one `.lean` file, so the 2026-10-08 records (`history/*_cb8ee9b.json`) stopped verifying with "source commitment mismatch". They are kept in `history/` for provenance.

The D8 record is separate because `PrintAxiomsD8.lean` re-declares names from `TensorSpeed.lean`, so the two can't be imported into one probe.

Verify without Lean (Python + PyNaCl). A source change makes a record stale, and it then fails `--source`:

    V=../4Leibniz/scripts/vkernel
    python3 $V/verify.py proof-records/ResNova_b59b56f.json $V/trusted_signers.json --source 05_lean_formalization --require-checker

What a record establishes and what it does not is in `4Leibniz/scripts/vkernel/README.md`. It has `nonvacuity: not-established` and `statement_match: not-checked`.

## [P] rows against receipts (`p_receipt_check.py`, 2026-10-09)
Row → module map: `P_ROWS.json`, rescored 2026-10-09 under RY's [P] rule. Run: `python3 ../4Leibniz/scripts/vkernel/p_receipt_check.py proof-records/P_ROWS.json proof-records 05_lean_formalization`

| row | tier | module named in row | modules | receipt | verifies | vacuity screen (row's theorems) |
|---|---|---|---|---|---|---|
| D1 | [P] | yes | MuStdUniqueness, MuStdFoundations | ResNova_b59b56f.json | yes | PASS 10, RING-ID/unfolded 1 |
| D2 | [P] | yes | MuNDuality | ResNova_b59b56f.json | yes | PASS 6 |
| D3 | [D]; [O] | no | (none) | none | - | - |
| D5 | [P/O] | yes | CoshCosmology | ResNova_b59b56f.json | yes | FIELD-ID/unfolded 2, PASS 4 |
| D6 | [D]; [O] | no | (none) | none | - | - |
| D7 | [D]; [O] | no (inferred) | AeSTStealthSector | ResNova_b59b56f.json | yes | CLOSED-ARITH/unfolded 1, REFLEXIVE/unfolded 4, RING-ID/unfolded 4 |
| D8 | [D] | no (inferred) | TensorSpeed, PrintAxiomsD8 | ResNovaD8_b59b56f.json, ResNova_b59b56f.json | yes | CLOSED-ARITH/unfolded 2, FIELD-ID 1, FIELD-ID/unfolded 3, HYP-PINNED/FIELD-ID 1, HYP-RESTATED 1, PASS 2, RING-ID 2, RING-ID/unfolded 4 |
| D9 | [P] | yes | SZStdEmbedding | ResNova_b59b56f.json | yes | PASS 4, RING-ID/unfolded 1 |
| MuStdFoundations (2026-09-30 correction, line ~103) | [P] | yes | MuStdFoundations | ResNova_b59b56f.json | yes | PASS 7, RING-ID/unfolded 1 |

[P] rows without a verifying receipt: 0 of 4.

Exit 0.

## Findings of 2026-10-08, and what the 2026-10-09 decisions did
1. **D1 was `[P]` and named no Lean module.** Since 2026-10-09 it is "[P] core; [D] rebuild". The core is `MuStdUniqueness.theorem_A_constitutive` (F′ = xμ_std as `HasDerivAt` on F_std) plus `MuStdFoundations`. Its theorems screen PASS, except `F_std_deriv_eq`, which is RING-ID/unfolded: it equates a typed formula, not a derivative.
2. **D8 was `[P]` on arithmetic Lean.** The two direct catches:
   - `physical_frame_tensor_speed_unity`: `(h_lum : c_T_g = 1) : c_T_g = 1 := h_lum`;
   - `gw170817_concordance`: it assumes `c_T = 1` and `c_γ = 1`, then shows `|c_T/c_γ − 1| < ε`.

   Since 2026-10-09 D8 is `[D]`: the structural derivation stands and the Lean is `[arith]`.
3. **`AeSTStealthSector` (D7) has all 9 theorems flagged.** The four PPN theorems are `rfl` on a structure literal (`gamma := 1, beta := 1, alpha1 := 0, …`). Since 2026-10-09 D7 reads "[D] stealth screening (the D3 §34 symbolic check); [O] branch selection". AeST is not falsified.
4. **`docs/grounding_ledger.yaml` is stale** (open): it lists 8 theorems for `AeSTStealthSector` (the file has 9), and `MuNDuality` and `SZStdEmbedding` are absent.

## Limits of the screen
- PASS means none of its patterns fired: reflexive, closed arithmetic, ring identity, field identity, hypothesis restated, hypotheses pinning the variables, or contradictory premises. It does not establish non-vacuity.
- Classes ending in `/unfolded` are weaker. They fire only after the project's own definitions are expanded, and one genuine chyren-aeon replacement (`powerDual_involutive`) is flagged that way.
- Calibration (9/9 known-vacuous flagged, 4/4 genuine pass since vacuity_screen 0.2) is in `4Leibniz/scripts/vkernel/calibration/`.
