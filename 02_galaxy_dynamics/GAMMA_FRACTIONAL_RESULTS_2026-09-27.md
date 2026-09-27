# Gamma / fractional-calculus sweep across Res-Nova — 2026-09-27

Origin: two videos (Derivia, "This Might Be The Strangest Function in Math"; BriTheMathGuy,
"The Mystery Behind This Math Miracle") on the Gamma function and fractional derivatives.
Question: can fractional order / Gamma-family functions narrow the **functional-choice
parameter** (the second of the two irreducible parameters), given the **derived**
a0 = cH0/2π?

All SPARC numbers use the ledger's own loader, 171 galaxies / 3,375 points, and the ledger's
nuisance treatment (tier 0: Yd = 0.5, Yb = 0.7, fd = 1; tier 1: Gaussian priors on Yd, Yb, fd).
The μ_std/derived-a0 baseline reproduces `PARAMETER_LEDGER.json` exactly (tier 0 median 11.08,
agg 93.65; tier 1 median 3.36, agg 6.09).

## 1. Exact identity: Giusti's length is derived

Giusti (PRD 101, 124029, 2020) fractional Poisson gravity at order s = 3/2 needs a length
ℓ = (2/π)√(GM/a0) (his eq. 23). Substituting a0 = cH0/2π:

    ℓ = √(r_s · R_H) / Γ(3/2),      r_s = 2GM/c²,  R_H = c/H0

Checked numerically to ratio 1.000000 at 10¹⁰ and 5×10¹⁰ M☉. The arithmetic is exact;
whether the Γ(3/2) carries meaning is **not yet derived**.

## 2. Fractional gravity with ℓ derived, universal order s — `fractional_gravity_sweep.py`

The matching Giusti used at s = 3/2 was generalized to every order: the point-mass fractional force
equals a0 at the MOND radius, ℓ^(2−2s) = r_M^(2−2s)/C_s (reduces to Giusti's ℓ at s = 3/2).
The result is one global number, s, shared by all galaxies. Geometry: spherical-equivalent
baryons, with exact shell averages of the fractional Green function. The Newton limit at s = 1 was
checked to 5×10⁻⁹.

| model | tier 0 median / agg | tier 1 median / agg |
|---|---|---|
| μ_std, a0 derived (ledger) | **11.08 / 93.65** | **3.36 / 6.09** |
| fractional, best universal s | 29.67 / 329 (s = 1.50) | 6.18 / 12.24 (s = 1.30) |

**A universal fractional order with derived ℓ loses to μ_std at both tiers.**

Per-galaxy free order (s and amplitude free, plus nuisance; 716 params total):
- s spreads across the whole range: median 1.20, 16–84% range [1.02, 1.40]. 27 galaxies sit at
  s = 1.00 and 9 at s = 1.50.
- Amplitude median is 10^0.50 above the derived value (16–84% range: 10^0.25 to 10^0.75).
- Fit quality: median χ²_red 1.61, agg 4.54, 94/171 < 2. At the **same 716-parameter budget**, the
  ledger's NFW halo scores median 1.92 and agg 4.58. Fractional gravity's two shape knobs fit slightly
  better than NFW's two. (The geometry treatments differ: spherical shells here, standard disk
  quadrature for NFW.)

**Verdict for parameter 2:** in this geometry, the order s does **not** come out universal, so it is
not a candidate for fixing the functional choice. Open caveat: a thin-disk Green function could move
s; this sweep does not settle that.

## 3. Mittag-Leffler generalization of the RAR — `mittag_leffler_rar.py`

The McGaugh–Lelli–Schombert RAR g = g_N / (1 − e^(−√(g_N/a0))) is the α = 1 member of the
Mittag-Leffler family E_α (the relaxation function of fractional calculus, built from Γ).
Test: g = g_N / (1 − E_α(−√(g_N/a0))). E_α numerics were validated against the series and against
E_½(−x) = e^(x²) erfc(x) to 10 digits.

| model | tier 0 median | tier 0 agg | tier 0 <2 | tier 1 median | tier 1 agg |
|---|---|---|---|---|---|
| μ_std, a0 derived | 11.08 | 93.65 | 27 | 3.36 | 6.09 |
| **RAR (α = 1), a0 derived** | **8.97** | 52.45 | 24 | 2.95 | **5.34** |
| RAR (α = 1), a0 = 1.2e-10 (literature) | 11.25 | **50.20** | 18 | 2.89 | 5.37 |
| ML α = 0.85, a0 = 1.2e-10 | 9.62 | 49.74 | 21 | 2.92 | 5.33 |
| ML α = 0.50, a0 derived | 10.85 | 52.14 | 23 | 2.85 | 5.49 |

Findings:
- **Under the RAR shape, derived a0 beats literature a0 on tier-0 median (8.97 vs 11.25) and
  frac < 2 (24 vs 18).** Literature a0 wins tier-0 aggregate by 4.5% (50.20 vs 52.45). This is the
  same median-vs-tail split the ledger reported before the μ_std recompute.
- The RAR shape improves on μ_std for **both** a0 values at both tiers.
- The Mittag-Leffler order adds nothing at derived a0: α = 1 is best on tier-0 median. With literature
  a0, α ≈ 0.85 is best. Its deep-MOND constant is Γ(1 + α)² a0 = 0.894 × 1.2e-10 = 1.07e-10, close to
  the derived 1.042e-10. The Gamma factor acts as an a0 rescaling, not a new shape.
- **Status: exploratory. μ_std remains the live interpolating function** (see
  `CURRENT_STATE_READ_THIS_FIRST.md` §1). It carries a structural uniqueness derivation
  (`TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md`) and clears the solar-system bound. The RAR row is a
  fit comparison, not a proposed replacement.
- **Caution, parameter 2:** choosing RAR over μ_std *because it fits better* is exercising the
  functional-choice parameter, not deriving it. The RAR's solar-system residual is exponentially
  screened (ν − 1 ≈ e^(−√y)). It has not been through the D7 covariant-completion checks that retired
  μ_dual.

## 4. Pillar IV under memory — `exploration/fractional_gamma/`

GKSL for H = u σx, L = √γ σ₋ (the Lean model), with a Caputo derivative of order α (L1 scheme):
- **The steady-state coherence 4x/(1+8x²) and its ceiling 1/√2 are unchanged for every α** tested
  (1, 0.9, 0.7, 0.5). The steady state is ker L, whatever the memory.
- Relaxation turns algebraic, with a late-time slope ≈ −α (−0.84, −0.67, −0.52 at α = 0.9, 0.7, 0.5).
- Memory damps the transient overshoot. Below α* ≈ 0.69, the coherence never exceeds θ at any time,
  for any drive. Converged values: α = 0.70 → sup 0.7125; α = 0.65 → sup 0.6865. A coarse run
  suggested α* ≈ θ; **that did not survive refinement**.

## 5. Memory holonomy (exploratory) — `exploration/fractional_gamma/memory_holonomy.py`

SU(2) parallel transport with a Caputo derivative, on the flat torus's two loops. At α = 1, every
defect is 0 (numerical noise ≤ 1e−3). At α < 1 the transport becomes non-unitary and
parametrization-dependent, and it stops being multiplicative. **Meridian-then-longitude differs from
longitude-then-meridian** (0.116 at α = 0.9, 0.295 at α = 0.5), even though the connection is abelian.
A transport with memory registers the *order* of loops, which ordinary holonomy cannot.

## Files
- `fractional_gravity_sweep.py` → `FRACTIONAL_GRAVITY_SWEEP.json`
- `mittag_leffler_rar.py` → `MITTAG_LEFFLER_RAR.json`
- `../exploration/fractional_gamma/` — Pillar IV fractional GKSL, α* convergence, memory holonomy

Run with `SPARC_DATA_DIR` pointing at the SPARC Rotmod_LTG directory.
