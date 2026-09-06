# Can light source the expansion? — the EM–χ coupling, closed

**Status:** `[P]` — the mechanism is excluded by 18.8 orders of magnitude.
**Date:** 2026-09-06
**Scripts:** `reproducibility/chi_em/disformal_em_coupling.py`, `reproducibility/chi_em/coupling_bound.py`
**Origin:** conversation "Light and Cosmic Expansion", archived in full at
`Chyren_Second_Brain/80_Archive/Antigravity_Transcripts/light_and_cosmic_expansion_FULL_2026-09-06.md`

## The question

Does an electromagnetic coupling to the information-tension field produce the negative
pressure needed for accelerated expansion — i.e. can `p_γχ < −ρ_γχ/3`?

## The coupling is not free

The premise that one may *choose* `L_int = λ f(χ) F_μν F^μν` is wrong for this theory.
Photons are matter, and matter couples to the physical metric (D7, D8):

    g̃_μν = A(φ) g_μν + B(φ) u_μ u_ν ,      u·u = −1

so `f` is **fixed** by `(A, B)`. Deriving the induced Maxwell term (script 1, verified
symbolically) gives

    L_EM = −(1/4)·√((A−B)/A)·F²  +  [B / (2√A·√(A−B))]·E²          E_μ ≡ F_μν u^ν

Both structures depend on `(A, B)` only through the ratio `B/A`; expanding,
`f = 1 − (1/2)(B/A) + O((B/A)²)`. The algebra reproduces D8 independently: for
Res-Nova's own map `A = e^{−2φ}, B = −2sinh2φ` it returns `A − B = e^{2φ}` and
`c_γ² = e^{4φ}`, matching §1.3 of D8 exactly.

## Two results, and they close the question together

**1. In the conformal branch the coupling is identically zero.**
Set `B = 0`: `f → 1` and the `E²` coefficient `→ 0`. The Lagrangian is pure Maxwell.
This is 4D conformal invariance of electromagnetism — under `g̃ = A g`, the factor
`√−g̃ = A²√−g` cancels against `g̃^{μα}g̃^{νβ} = A^{−2}g^{μα}g^{νβ}` exactly. **The
conformal factor cannot reach the photon at all.** No `f(χ)F²` term exists to generate,
so `p_γχ ≡ 0`. There is no mechanism.

**2. Rescaling `F²` cannot produce negative pressure even when `f ≠ 1`.**
For `L = −(f/4)F²`, the stress tensor is `T_μν = f(F_μα F_ν{}^α − (1/4)g_μν F²)`, whose
trace is `f(F_μαF^μα − F²) = 0`. It stays **traceless**, hence `w = +1/3` exactly, for
*any* `f(χ)`. A χ-dependent `f` exchanges energy between χ and radiation; it does not
give the photon sector negative pressure. Only the `E²` term breaks conformal invariance
— and that term is proportional to `B`.

**3. The `B ≠ 0` branch fails quantitatively.** Every departure from Maxwell is `O(B/A)`,
so the EM interaction energy is `ρ_γχ ~ (B/A)·ρ_γ`. Reaching dark-energy density requires
`|B/A| ≳ ρ_Λ/ρ_γ`:

| quantity | value |
|---|---|
| Ω_γ (Planck γ density, h = 0.6827) | 5.300 × 10⁻⁵ |
| Ω_Λ (Res-Nova, ln 2) | 0.6931 |
| **required** \|B/A\| | **≥ 1.31 × 10⁴** |
| **allowed** \|B/A\| — GW170817, \|c_T/c_γ − 1\| ≤ 10⁻¹⁵ | **≤ 2 × 10⁻¹⁵** |
| **gap** | **6.5 × 10¹⁸ — 18.8 orders of magnitude** |

The requirement is not merely unsatisfied, it has the wrong sign in the exponent: the
mechanism needs a *large* disformal factor, and luminality forces a vanishing one.

## Correction to the constraint I previously recorded

I earlier listed α_fs drift as a gate on this coupling. It is not the binding one.
`f = 1 − (B/A)/2` gives `|Δα/α| ≲ (1/4)|B/A| ≤ 5 × 10⁻¹⁶` at the GW bound — about
10⁹ times inside the ~10⁻⁶ quasar/Oklo limit. **GW170817 is the constraint that closes
this, by nine orders over α_fs.** The earlier note is superseded by this file.

## Scope — what this does NOT exclude

"Light drives geometry" is **true and untouched**. Radiation has nonvanishing `T_μν`;
result 2 above proves that tensor is traceless but not zero. Light curves spacetime
through Einstein's equation exactly as in GR, with `w = +1/3`.

Two channels must be kept apart:

| channel | status |
|---|---|
| `light → T_μν → g_μν` | **alive** — ordinary GR, unmodified |
| `light → χ → g_μν` | **dead** — conformal invariance + GW170817 |

What is excluded is (a) light driving *accelerated* expansion, and (b) light coupling to
the information-tension field at all. Any downstream argument needing only "EM activity
modifies geometry" — e.g. a `ψ → F_μν → g_μν → Ĥ → ψ` feedback loop — survives this
result intact; it simply cannot be routed through χ.

## What survives

Nothing here touches the χ sector's own vacuum energy `ρ_vac = e^{−2χ}V₀`, which remains
whatever the χ dynamics make it. The result is narrower and sharper: **light contributes
nothing to it.** The intuition that photon propagation drives expansion is excluded in
this framework — not by the `w = +1/3` objection alone, but because the only channel by
which light could couple to χ is switched off by the same luminality condition the theory
already imposes for gravitational waves.

That is a genuine constraint, not a null: the theory's own `c_T = c` requirement and a
light-driven expansion sector are mutually exclusive. One forbids the other.
