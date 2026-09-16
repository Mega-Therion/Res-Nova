# OBLIGATION 2 AUDIT — THE CHIRAL ALPHABET (A) REDUCES TO THE SUBSTRATE'S DOUBLE COVER

**Status:** DISCHARGED TO THE STATED LIMIT — (A) is derived-given-Pin⁻: the
two-state chiral alphabet is literally the kernel of the substrate's double
cover, and "unpolarized, not absent" is a theorem about groups, not a reading.
The residue is obligation 4 (justify Pin⁻) — now sharp, checkable, and equipped
with a machine-verified trap: **GL(2,3), the naive matrix realization of the
reflection double cover, is the Pin⁺-type cover, not the Pin⁻ one.**
**Date:** 2026-09-16
**Tags:** `[P]` proved · `[D]` derived/verified here · `[C]` cited/conjectured · `[O]` open · `[X]` killed
**Machine:** `scripts/chiral_alphabet_substrate.py` — 16/16, exact arithmetic.
Discharges ledger open-item 5 (obligation 2 of layer 0) to the stated limit;
sharpens open-item 4 (obligation 4).
**Inputs:** PRIOR_ART_BINARY_TETRAHEDRAL_MCKAY (the frozen finite core and its
"crack = Pin⁻(3) convention"), the 2T ≅ SL(2,3) frozen audit.

---

## 1. What obligation 2 asked

Layer 0, obligation 2: *justify the chiral alphabet (A) — the channel is
two-state ±1, μ→0 is unpolarized, not absent — or accept it as primitive.* The
audits had established that (A) is what selects Postulate R's coordinate
(POSTULATE_R_ISOLATION) and that nothing in the mathematics forces it (F3
enforced three times). The question was whether the *substrate* forces it.

## 2. The reduction: the alphabet is the kernel `[D]`

Work in the exact geometric realization the frozen core already certified: the
tetrahedral substrate T_d (24 matrices preserving V = {(1,1,1), (1,−1,−1),
(−1,1,−1), (−1,−1,1)}), its rotation subgroup A₄ (12), and its six reflections
(isolated by det = −1, trace = 1 — verifier A1). Lift to the double cover in the
Clifford embedding: rotations lift to the 2T quaternions (the frozen core,
24 elements); a reflection with plane normal n lifts to i(n·σ), which **squares
to −I** (verifier A3a). The resulting cover has order 48, quotient T_d
(verifier A2). Now read (A) off it:

- **The two states ±1 are the kernel** {+I, −I} of the cover — the two sheets.
  The center of the cover is exactly these two elements (verifier A5a): there
  is no third state, and no other element commutes with the channel. `[D]`
- **"Unpolarized, not absent" is a theorem.** −I is not the identity (verifier
  A5b) — it is the 2π rotation, a *transformation*. A group has no absorbing
  element (verifier A5c): the substrate offers no "absent" slot for the channel
  to be in. The presence reading (μ_dual's coordinate) has no substrate state to
  name; the unpolarized state is the sheet-neutral one. `[D]`
- **Pin⁻ is what makes the alphabet orientation-connected.** Under the Pin⁻
  lift, every reflection has order 4 (squares to −I): an out-and-back
  orientation reversal crosses the sheets. The channel is orientation-SENSITIVE
  — N4's statement, now with its mechanism identified. Under the Pin⁺ lift the
  same reflections have order 2 and the sheets are orientation-disconnected.
  `[D]`

**Net:** (A) is no longer a free primitive. Given the substrate's double cover
and the Pin⁻ convention, the chiral alphabet, its two-state structure, and the
unpolarized reading are forced. What remains as input is exactly obligation 4:
**why Pin⁻.**

## 3. The Pin⁺ counterfactual — constructed, not cited `[D]`

The audit does not cite the Pin⁺ cover; it builds it (n·σ instead of i·n·σ) and
compares, exactly:

| | Pin⁻ cover | Pin⁺ cover |
|---|---|---|
| reflection lifts square to | −I (order 4) | +I (order 2) |
| involutions in the whole group | **1** (−I alone) | **13** |
| order census | {1:1, 2:1, 3:8, 4:18, 6:8, 8:12} | {1:1, 2:13, 3:8, 4:6, 6:8, 8:12} |
| orientation sensitivity | channel detects double reversal | insensitive |

The two covers are non-isomorphic (1 vs 13 involutions, verifier A3b/A4d) —
**the convention is not a bookkeeping choice between isomorphic options; it is
a physical selection between different groups.** A future covariant theory
touching the reflection sector picks one, and the choice is checkable by census.

## 4. The GL(2,3) trap — discovered by machine `[D]`

The obvious matrix realization of "the double cover of the tetrahedral
reflection group" is GL(2,3) (order 48, center ±I, quotient S₄). The machine
shows it is the **Pin⁺-type** cover: all 12 of its transposition lifts square
to +I, and its involution census is 13 — matching the Pin⁺ cover, not the
Pin⁻ cover's 1 (verifier A6). **GL(2,3) ≅ 2⁺S₄; the Pin⁻ cover is the
binary-octahedral-type 2⁻S₄.** Any corpus construction that reaches for GL(2,3)
to represent the substrate's reflection lifts builds the wrong group — this is
the prior-art packet's "crack = Pin⁻(3) convention" made concrete, and it is on
the record with a five-line census check so it cannot be quietly rediscovered.

## 5. What is NOT derived `[O]`

1. **Why Pin⁻ remains open** (obligation 4, now the sole residue of (A)): the
   substrate forces the alphabet given the convention; the convention itself is
   the input. What is new is that the question is now sharp — "does the channel
   detect a double orientation reversal" — and that the two answers are
   non-isomorphic groups, so no smooth interpolation of the question exists.
2. **No claim that the physical Pin group of the continuum theory is this
   finite cover.** The finite model is the substrate's fingerprint
   (frozen core); the continuum Pin⁻(3) embedding is the standing `[C]` reading.
3. **(A)'s velocity reading (μ = tanh ψ as the channel's polarization
   coordinate) is inherited from the cascade, not re-derived here.** What this
   audit fixes is the alphabet's *structure* (two states, chiral,
   never-absent), which is what Postulate R needs.

## 6. Falsifiability

- If a covariant theory selects Pin⁺, §3's table says exactly what changes:
  the sheets become orientation-disconnected, N4's finite model needs
  rebuilding on the 2⁺S₄ core, and (A)'s chiral structure loses its substrate
  forcing — (A) would return to primitive status. Layer 0 §6's third bullet
  is this test, now with the census check attached.
- The GL(2,3) trap is self-falsifying: any future document that uses GL(2,3)
  as the Pin⁻ cover fails verifier A6 by construction.

## 7. Reproduce

```bash
python3 scripts/chiral_alphabet_substrate.py    # 16/16, exit 0, exact arithmetic
```

## 8. Ledger

**Open-item 5 ((A)) discharged to the stated limit:** the alphabet is the
kernel of the substrate's double cover; unpolarized-not-absent is a group
theorem; the chiral structure is forced given Pin⁻. `[O]` → `[O-sharp]`.
**Open-item 4 (Pin⁻) sharpened:** the convention is a selection between
non-isomorphic groups (1 vs 13 involutions, machine-verified), and the
GL(2,3) trap is recorded. No `[P]` changes; the frozen finite core (BT ≅ 2T ≅
SL(2,3)) is untouched — SL(2,3) remains the rotation double cover exactly as
frozen; the trap concerns only the reflection extension.
