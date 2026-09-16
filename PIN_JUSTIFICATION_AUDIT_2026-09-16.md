# OBLIGATION 4 AUDIT — WHY Pin⁻: FORCED BY ONE-CHANNEL PARSIMONY

**Status:** DISCHARGED TO THE STATED LIMIT — Pin⁻ is no longer a convention: it is
the unique Pin cover whose reflection sector couples to the channel's own
sheets, *given* the two structural facts the earlier audits already established.
The residue is named: a dynamical derivation of N4 itself (orientation action).
**Date:** 2026-09-16
**Tags:** `[P]` proved · `[D]` derived/verified here · `[C]` cited/conjectured · `[O]` open · `[X]` killed
**Machine:** `scripts/pin_justification_audit.py` — 6/6, exact arithmetic.
Discharges ledger open-item 4 (obligation 4 of layer 0) to the stated limit.
**Inputs:** CHIRAL_ALPHABET_SUBSTRATE_AUDIT (the kernel-as-alphabet reduction,
the two constructed covers, the GL(2,3) trap), the frozen BT core, N4's reading.

---

## 1. The forcing, stated precisely `[D]`

Both Pin covers of the tetrahedral reflection group T_d contain the same
rotation core (the frozen 2T/SL(2,3)) with the same kernel {±I} — the substrate
is the same either way; the choice is entirely about reflections. Now combine
two results already on the record:

- **(i)** The channel has exactly two states — the kernel {+I, −I}, and *nothing
  else is channel-coupled*: the center is the kernel (obligation 2 audit, A5a),
  and no absorbing/extra structure exists (A5c).
- **(ii)** Orientation reversal acts on the channel (N4's reading — the
  orientation-sensitive substrate demand).

Then ask where (ii)'s action can live. In the **Pin⁻** cover, every reflection
lift squares into the kernel — r̃² = −I: out-and-back orientation reversal
flips the channel's sheet (verifier P4: no Pin⁻ lift squares to identity).
The action uses the channel's own two states — one mechanism, no new
structure. In the **Pin⁺** cover, reflection lifts square to +I: orientation
reversal does *nothing* to the sheets (verifier P2b: all 12 reflection lifts
are involutions outside the center), and the action would have to live in the
cover's twelve non-central involutions — a *second* two-fold structure that
fact (i) excluded. **One channel forces Pin⁻.** `[D]`

The parsimony witness (verifier P3): channel-coupled reflection lifts — 6
(Pin⁻) vs 0 (Pin⁺); total involutions — 1 vs 13. Pin⁺'s reflection sector is
either invisible (then it is not a lift of the physics that acts) or a second
channel (excluded). There is no third option.

## 2. The Kramers-type doubling, honestly tagged `[C]`

Under Pin⁻, applying any reflection lift twice returns −I on the nose (P5) —
double reversal crosses the sheet and returns. This is the same algebra as
Kramers/T² = −1 doubling for fermionic time reversal (Pin⁻ is the cover that
appears there, `[C]` literature-anchored). The corpus does NOT claim the channel
is fermionic; it claims the *doubling structure* is shared, which is the
statement N4's reading always made, now with its group-theoretic home.

## 3. What is NOT derived `[O]`

1. **N4 itself.** The forcing is conditional on orientation reversal acting on
   the channel at all. If N4 is dropped, Pin⁺ is available and the channel is
   orientation-blind. The residue of obligation 4 is therefore exactly: derive
   N4 from dynamics (action level), or accept it as the substrate's one
   primitive. **The input count of the whole program is now: N4 (+ μ′(0)=1 +
   the horizon-selection question).**
2. **The continuum Pin⁻(3) identification** remains a `[C]` reading (the finite
   cover is machine-verified; the continuum embedding is literature-anchored,
   PRIOR_ART packet).
3. No claim that the extra Pin⁺ involutions are unphysical in general — only
   that *this channel* has no slot for them.

## 4. Falsifiability

- If a dynamical derivation lands on Pin⁺ (orientation-blind channel), N4 falls,
  and with it this audit's forcing and (A)'s substrate reduction — obligations 2
  and 4 return to primitive status together. The covers remain
  machine-distinguishable (1 vs 13 involutions), so the experiment is binary.
- Any construction using GL(2,3) as the reflection cover fails the substrate
  audit's A6 by construction (the trap, on the record).

## 5. Reproduce

```bash
python3 scripts/pin_justification_audit.py    # 6/6, exit 0
```

## 6. Ledger

**Open-item 4 (why Pin⁻) discharged to the stated limit:** Pin⁻ forced by
one-channel parsimony given (A)-as-derived + N4; Kramers-type doubling
`[C]`-anchored; residue renamed **N4-derivation**. Status `[O-sharp]` — the
convention question is closed; the primitive question is open and named.
