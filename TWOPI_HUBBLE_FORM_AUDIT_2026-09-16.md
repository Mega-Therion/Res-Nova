# OBLIGATION 3 AUDIT — THE 2π AND THE HUBBLE-FORM SPECIFICITY

**Status:** DISCHARGED TO THE STATED LIMIT — the 2π acquires a covariant home:
it is the Euclidean period of the very boost orbit Theorem B-cov forced (K2), i.e.
the thermal circle of the channel. The Hubble-form question is sharpened from
"which form matches" to "which horizon's circle closes the orbit." Nothing here
predicts a₀'s value; the normalization caveat (D2-supp §6.1) is unchanged.
**Date:** 2026-09-16
**Tags:** `[P]` proved · `[D]` derived/verified here · `[C]` cited/conjectured · `[O]` open · `[X]` killed
**Machine:** `scripts/twopi_hubble_form_audit.py` — 11/11. Discharges ledger
open-item 3 (obligation 3 of layer 0) to the stated limit.
**Inputs:** REPRESENTATION_AUDIT_A0_SPARC (the measured dresses and factors),
Q3_AEST_COVARIANT_DERIVATION (the covariant leg), layer 0 §5 (the triangle).

---

## 1. What obligation 3 asked

Layer 0, obligation 3: *explain the 2π, and why the empirical match is
specifically the Hubble-radius form* — not the Λ/de Sitter forms, which miss by
measured 1.439× (high) and 0.831× (low), and not Milgrom's a_dS = cH₀, which
misses by exactly 2π (factor 5.66×, machine-reconfirmed = 6.28319 to 6 digits).
The audit had already fixed that the 2π is *required* (P3) and that the claim is
*specifically* the Hubble form (P2); what it could not do — pre-B-cov — was say
WHERE a 2π could covariantly come from.

## 2. The candidate sources, enumerated and discriminated `[D]`

- **S1 — the thermal circle of the boost orbit (KMS/Unruh).** The unit-norm
  orbit K2 forces, (cosh ψ, sinh ψ), closes under Wick rotation ψ → iθ into the
  unit circle — cosh(iθ) = cos θ, sinh(iθ) = i sin θ, period exactly 2π
  (verifier T1). A hyperbolic observer with proper acceleration a closes in
  imaginary proper time with period 2π/a (verifier T2) — the Unruh/KMS circle.
  **This is the only 2π that composes with B-cov**: it lives on the same orbit,
  not in a separate sector. `[D]`
- **S2 — the crossing-time winding.** c/a₀ = 2π/H₀ — the audit's own bookkeeping
  identity. Same number, no mechanism: a winding needs a clock, and the only
  covariant clock on the orbit is S1's circle. Recorded as the identity it is,
  not an explanation. `[D]`
- **S3 — the rotation-2π of the double cover.** In the substrate, a 2π rotation
  is −1 (the central sheet flip; machine-checked in
  `scripts/chiral_alphabet_substrate.py` A5b). But this 2π lives in the compact
  rotation sector; the boost sector has no real period (cosh unbounded, verifier
  T5a) — its only closure is the Euclidean one, which is S1 again. The sectors do
  not share their 2π; S3 does not transfer to a₀. `[D]`

**Finding:** the 2π has exactly one covariant home compatible with Theorem
B-cov: **the Euclidean closure of the K2 orbit itself.** The factor 2π in
cH₀/2π is the circumference of the channel's thermal circle. This upgrades the
corpus's Unruh route from "a factor 2π discrepancy" (D2-supp §6.1's framing) to
"a factor with a forced home": the discrepancy and the requirement are the same
2π, and it is S1's.

## 3. The thermal reading of μ — a structural match, honestly tagged `[C]`

Two-state channels in thermal equilibrium polarize as tanh: for gap Δ at
temperature T, the partition function is Z = 2cosh(Δ/2T) and ⟨s⟩ = tanh(Δ/2T)
(verifier T3 — algebra only). The cascade's μ = tanh ψ is *the same function*:
ψ ≡ Δ/(2T). If the channel reads a horizon temperature, then (i) the 2π enters
as the circle (S1), (ii) μ = tanh ψ is a thermal polarization, not a kinematic
accident, and (iii) the natural scale is a temperature-like a/2π — the Unruh
form — rather than a bare acceleration. This is a **structural match `[C]`**,
not a derivation: no gap Δ is derived here, and identifying the channel's
temperature with any specific horizon remains open. It is recorded because it
is the only reading that makes obligations 1 and 3 the *same* story.

## 4. The Hubble form — the question sharpened `[O]` → sharp

Given S1, the Hubble-vs-Λ discrimination (P2's 1.439×/0.831×) becomes: **which
horizon's KMS circle closes the orbit?** The candidate circles differ
measurably: the Hubble-form circle (period 2π/H₀) matches the live window
within the two-axis tension map (Planck −1.32σ_boot, SH0ES −0.32σ); the Λ/static-
patch circles are the ones the measured factors exclude. What remains open is
not the arithmetic (P2 settled it) but the *reason* the FLRW horizon's circle —
not the static patch's — is the operative one. **The triangle of layer 0 §5 is
now: covariant kinematics `[D]` (B-cov) + 2π home `[D]` (S1) + Hubble-form
selection `[O-sharp]`.** Two legs are theorems; the third is a named question
about horizon slicings.

## 5. What is NOT derived `[O]`

1. No value of a₀ is predicted. The 2π home constrains the *form* (a/2π vs a);
   it does not set the scale or its H₀ proportionality.
2. The normalization caveat (D2-supp §6.1) stands: the D2 supplement's §6.1
   warning that the Unruh route's normalization was not pinned is untouched —
   this audit pins where the 2π lives, not the prefactor's derivation.
3. The thermal reading (§3) is `[C]`: gap, temperature source, and the
   identification with a specific horizon are all open.
4. The 2π of S1 and the substrate's rotation-2π (S3) are related only by
   Wick rotation; no claim is made that they are the same number physically.

## 6. Falsifiability

- If the a₀(z) test turns conclusive against constant a₀, S1's circle becomes
  horizon-dynamics-dependent — the 2π home survives but the Hubble-form leg
  sharpens into a z-dependent statement. `[D]` (inherits the audit's a₀(z) open)
- If a covariant theory closes the orbit with a Λ-form circle instead
  (static-patch KMS), §4's discrimination kills it against P2's measured factors.
- If the channel is shown NOT to be thermal (no gap structure), §3's match is
  vestigial and S1 reduces to geometry — the 2π home survives, the Unruh route
  does not.

## 7. Reproduce

```bash
python3 scripts/twopi_hubble_form_audit.py    # 11/11, exit 0
```
Numbers recomputed from constants: cH₀/2π = 1.0422e-10 m/s² (H₀ = 67.4); the P3
ratio = 6.283185 (= 2π); √(3Ω_Λ) = 1.4387; √Ω_Λ = 0.8307.

## 8. Ledger

**Open-item 3 discharged to the stated limit:** the 2π is the Euclidean period
of the K2 orbit (machine-checked); the Hubble-form question is now the named
question "which horizon's circle"; the triangle has two theorem legs. Status
`[O]` → `[O-sharp]`. No `[P]` changes.
