# μ_dual Solar-System Safety — Reconciliation of Two Contradictory Claims (2026-09-12)

Two documents in this corpus made contradictory claims about whether
`μ_dual(x) = x/(1+x)` is solar-system-safe. A third, independent derivation
was performed to resolve this rather than simply picking a side. **Neither
prior claim was simply correct** — both survive in part and fail in part,
and the actual falsifying mechanism was identified by neither.

## The two prior claims

- **`res_nova_manuscript.tex`** (submitted to Physical Review D, DOI
  10.5281/zenodo.21969121): claimed Vainshtein-screened Q₂ ≈ 4.9×10⁻²⁹ s⁻²,
  "a factor 70 below the Cassini bound," safe.
- **`TARGET_D7_COVARIANT_COMPLETION.md` §4** (this session, earlier today):
  claimed a ~5.7×10⁵ violation of the solar-system bound via an unscreened
  constant offset.

## What the third derivation found

**Both specific numbers are wrong, in different ways:**

- The manuscript's Q₂ *value* (4.9×10⁻²⁹) numerically coincides with a real
  quantity — the **dipole (ℓ=1) tidal scale** `2ã₀g_ext r/GM` — but the
  manuscript's *stated derivation* (Vainshtein suppression × `F″/F′`) is
  void: it depends on `x₀ = 5.67√α` from a `𝒦(𝒬)` action the same
  manuscript's covariant section elsewhere replaces with `𝒥(𝒴)=F_dual(√𝒴)`.
  Two inequivalent actions are in use in one document.
- D7's "5.7×10⁵" is a **category error** — it divides a monopole
  acceleration by a length and calls the result a tidal/quadrupole
  coefficient. The genuine ℓ=2 (true quadrupole) term is ~9 orders of
  magnitude *below* the Cassini bound, not above it. **This specific number
  in `TARGET_D7_COVARIANT_COMPLETION.md` §4 should be retracted as stated.**

**The real, fatal mechanism (found by neither prior document):**

μ_dual's large-x tail forces a **constant, radius-independent anomalous
acceleration** `ã₀ = (1+λ_s)a₀ ≥ a₀` — this is forced by matching the
deep-MOND normalization, not a free/tunable parameter. It is the *exact*
unperturbed spherical solution of the field equation (the SZ "tracking"
branch, `J′(𝒴) → λ_s ≠ 0`), not a response to a perturbation — so there is
nothing for Vainshtein screening to suppress. It has no radial 1/r²-type
falloff for a fitted `GM` to absorb.

This constant offset produces anomalous **planetary perihelion precession**
(monopole/dipole, not quadrupole — this is the category distinction that
broke both prior analyses):

| Planet | Predicted Δϖ (ã₀=a₀, λ_s=1) | Real bound (2σ) | Violation |
|---|---|---|---|
| Mercury | 1.485 arcsec/century (retrograde) | ~1.6 mas/century (INPOP10a/EPM2011) | **~900×** |
| Earth | 2.44 arcsec/century | — | — |
| Saturn | 7.52 arcsec/century | — | worse outward |

Verified by direct numerical orbit integration (Gauss planetary equations,
300 orbits, brentq perihelion location): predicted/analytic ratio
0.9999984.

For contrast, `μ_std(x) = x/√(1+x²)`'s large-x residual is `a₀²/(2g_N)` —
no constant term, decays as 1/g_N, and is ~9 orders of magnitude below the
Cassini/precession bounds. This is the fix path already adopted elsewhere
in this corpus (D5, D7 cosmological corrections, SPARC recompute).

## Open item, not resolved here `[O]`

Whether the constant acceleration could partially hide inside standard
ephemeris-fit `GM`/`a` degeneracies. Estimated unlikely (wrong radial
scaling — not ∝1/r²), but not independently verified against a real
ephemeris pipeline. Flagged for the falsifier agent, not closed.

## What needs correcting as a result (tracked, not all done in this commit)

1. `res_nova_manuscript.tex` — the §Vainshtein/solar-system-safety
   subsection's *derivation* must be replaced (the conclusion "safe" does
   not survive; the real mechanism is a ~900× Mercury precession
   violation, not a 70×-margin quadrupole). The "inner solar system is
   Newtonian by construction" line is the specific locus of the error —
   fractional smallness (`a₀/g_N ~ 2×10⁻⁸`) does not bound precession,
   because the orbital lever arm `a²/GM` converts a fractional effect into
   an absolute-acceleration bound.
2. `TARGET_D7_COVARIANT_COMPLETION.md` §4 — the "5.7×10⁵" quadrupole
   framing needs retraction/correction to the real monopole-precession
   mechanism above.
3. Downstream citations of either the manuscript's Q₂ safety claim or D7's
   quadrupole number inherit this and need review.

This document is the reconciliation source; downstream corrections should
cite this file, not re-derive from either superseded claim.
