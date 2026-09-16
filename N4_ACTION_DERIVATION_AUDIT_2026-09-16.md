# OBLIGATION 4 AUDIT, ROUND 2 — N4 FROM THE ACTION LEVEL

**Status:** DISCHARGED TO A STATED LIMIT — but a *different* limit than the
PR #58 parsimony claim (corrected by PR #59). N4 is no longer taken as a
premise and no longer a bespoke physics input: it is **derived** from three
structures already on the books plus ONE standard-QM step, tagged `[C]`. The
residue is named and smaller: the KMS/antiunitary identification.
**Date:** 2026-09-16 (evening, post-#59, post-#60)
**Tags:** `[P]` proved · `[D]` derived/verified here · `[C]` cited/conjectured · `[O]` open · `[X]` killed
**Machine:** `scripts/n4_action_derivation.py` — 13/13, exact arithmetic.
Updates ledger open-item 4. Replaces the PR #58 "forcing" (whose circularity
PR #59 exposed: "couples to the sheets" is the Pin^- definition).

---

## 1. The derivation chain, premise by premise

- **(i) The channel is spinorial `[P]`.** A 2*pi rotation acts as -I != +I on
  the channel's states — the frozen core's theorem (substrate audit A5b),
  re-verified (N4). Half-integer structure: the one channel property that is
  NOT a convention.
- **(ii) The sheets are thermal `[D]`.** The channel's two states are the
  antipodes of the Euclidean closure of the K2 orbit: +1 at psi = 0, -1 at
  Euclidean theta = pi (cosh(i*pi) = -1, exact; N5a). The REAL dynamics never
  connects them: cosh(psi) >= 1 on the real orbit (N5b); the rotation sector's
  -1 is a different sector (2*pi audit S3). The only sheet-connecting path in
  the whole theory is the Euclidean/KMS half-circle.
- **(iii) Parity is a PLANE reflection of the celerity axis `[D]`.** B-cov
  (theorem): x = sinh(psi) is the spatial celerity. Orientation reversal maps
  x -> -x: ONE axis flips — a plane reflection, not the point inversion (which
  flips three). Machine-checked at the O(3) level (N1): reflection x
  pi-rotation = inversion — the two improper types are distinct elements, and
  the inversion is not even in T_d (N1b).
- **(iv) The covers DISTRIBUTE the -1 phase oppositely `[D]`.** In the
  corpus's fixed convention (rotations lift to the 2T quaternions in both;
  reflections lift to i(n*sigma) in Pin^-, to n*sigma in Pin^+ — stated
  explicitly per PR #59's convention caveat): **Pin^- gives the -1 phase to
  PLANE reflections (r~^2 = -I; inversion lift squares +I); Pin^+ gives it to
  the INVERSION (i-I lifts, order 4) and leaves reflections +I** (N3a/b/c).
  "Choosing a cover" = "choosing which improper operation carries the Kramers
  phase."
- **(v) The Kramers step `[C]` + minimal instance `[D]`.** The reflection on
  the thermal circle is theta -> -theta: EUCLIDEAN TIME REVERSAL (the only
  covariant home, 2*pi audit S1). For a spinorial channel, the lift through
  the Euclidean/KMS sector is antiunitary (Wick rotation conjugates, N6c), and
  Wigner/Kramers gives square -1: machine-checked in the minimal instance
  (i*sigma_y*K)^2 = -I on the spin-1/2 space (N6a), while the purely unitary
  square of the same matrix is +I (N6b) — the -1 comes precisely from the
  conjugation, i.e. from the Euclidean passage.

**Selection (N7):** the theory's orientation operation is a plane reflection
(iii); its lift passes through the Euclidean/KMS sector (ii+v) and so carries
the -1 phase (v); the unique cover in which PLANE-reflection lifts square to
-I is **Pin^-** (iv). **Pin^+ is not rejected by parsimony — it is EXCLUDED
structurally: it would require the theory's orientation operation to be the
point inversion, which B-cov's one-axis parity forbids.**

## 2. What changed relative to PR #58 and PR #59

PR #58 claimed Pin^- "forced by parsimony" — circular (PR #59: N4 = the
conclusion). This audit takes the opposite route: N4 is the OUTPUT. The
input list for the whole program shrinks from {N4, mu'(0)=1, horizon reason}
to **{mu'(0)=1, horizon reason} + one [C] step (KMS/antiunitary) + B-cov
(theorem)**. The Kramers step is standard QM (Wigner's classification),
machine-checked in its minimal 2x2 instance — a far smaller and better-anchored
input than the bespoke "the channel is orientation-sensitive."

## 3. What is NOT derived `[O]`

1. **The KMS/modular-conjugation identification** (step v): that the
   Euclidean-time reversal relevant to the channel acts antiunitarily is
   literature-anchored (Wigner; KMS/Tomita-Takesaki), not derived from the
   finite core. If a purely unitary reading is forced instead, the square is
   +I and Pin^+ returns — the derivation is conditional on this one `[C]`.
2. **No convention-independence claim.** The Pin^+-vs-Pin^- NAMING differs
   across authors (PR #59's caveat); every statement here is in the corpus's
   fixed matrix convention (stated in (iv)). The INVARIANT content: "the
   theory's orientation operation is plane-reflection-type and its lift
   squares to the 2*pi phase."
3. Nothing here derives the channel, the gap, or any value-level physics;
   obligation 5's maser-distance limit and the horizon reason stand.

## 4. Falsifiability

- If the channel's Euclidean sector is shown purely unitary (no KMS structure),
  step (v) dies and Pin^+ returns with the inversion carrying the phase — a
  DIFFERENT finite model (the substrate audit's Pin^+ counterfactual, 13
  involutions) that the corpus can build and test.
- The chain is checkable end-to-end: `python3 scripts/n4_action_derivation.py`.

## 5. Ledger

**Open-item 4 status:** N4 derived from frozen theorems + B-cov + one [C]
Kramers step; Pin^- selected structurally, not by parsimony. Residual input
list for the program: mu'(0) = 1, the horizon-selection reason, and the [C]
KMS identification. The bespoke input "the channel is orientation-sensitive"
is retired.
