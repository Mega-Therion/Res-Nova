# Pre-registration: joint Cassini × SPARC scan over interpolating-function shape families (2026-10-27)

Committed before any number of this scan is computed. Issues #184, #187. Record to follow:
`CASSINI_SPARC_JOINT_SCAN_2026-10-27.md`, `CASSINI_SPARC_JOINT_SCAN.json`, `cassini_sparc_joint_scan.py`.

## Question

The frozen Batch-1A gates (`frozen_batch1a.py`, `FROZEN_BATCH1A.json`) find no ν_n, n = 1…8 step 0.5, that
passes both Cassini and SPARC. Cassini wants a sharp transition (n ≳ 5); the SPARC gate fails ν₆. Is there any
interpolating function in a reasonable two-parameter shape family that passes both gates?

## Gates (unchanged from Batch 1A)

- **a₀.** Both conventions, handled exactly as Batch 1A: fitted a₀ = 1.1607×10⁻¹⁰ m s⁻² and derived
  a₀ = cH₀/2π = 1.0422×10⁻¹⁰ (H₀ = 67.4), each held fixed (not refitted per function).
- **Cassini.** QUMOND Q₂ at g_e = 1.9×10⁻¹⁰ and 2.4×10⁻¹⁰ m s⁻²; pass iff both lie in [−2.0, 5.2]×10⁻²⁷ s⁻².
  Computed with `qumond_axisym_efe.py` (PR #194), reused unchanged.
- **SPARC.** `cassini_sparc_joint.fit` / `summ` (the frozen scorer: ledger loader, tier 0 at prior-mean M/L, tier 1
  with the Gaussian Υ_disk/Υ_bulge/f_d priors, 171 galaxies). Δ = statistic − `FROZEN_BATCH1A.json`
  `baseline_nu2[a₀ name]` (read, not recomputed) for tier0 median, tier0 agg, tier1 median, tier1 agg; pass iff all
  four |Δ| < 1. Data, nuisance policy and gate unchanged.
- **Joint.** Per (shape parameters, a₀) row, SPARC gate and Cassini gate both true. Reported two ways: any row
  passes, and passes at both a₀.

## Families

**(a) ν_n** (Famaey & McGaugh 2012, LRR 15, 10, eq. ν_n; Hees et al. 2016 eq. 5) `[C]`:
ν_n(y) = [(1 + (1 + 4y⁻ⁿ)^{1/2})/2]^{1/n}, n continuous. Grid n = 1.00…10.00 step 0.25 (37 points).

**(b) ν_{γ,β}**, the two-parameter union of the Milgrom–Sanders / McGaugh families:
ν_{γ,β}(y) = (1 − e^{−y^{γ/2}})^{−1/γ} + β e^{−y^{γ/2}}.
Every one-parameter slice is a literature family `[C]` (read from the LaTeX source of Famaey & McGaugh 2012, §6.2):
β = 1 − 1/γ is the γ-family (Milgrom & Sanders 2008, ApJ 678, 131); γ = 1 is the ν_β family of the same paper;
β = 0 is the δ-family (McGaugh 2008, ApJ 683, 137); γ = 2α, β = 1 − 1/(2α) is Hees et al. 2016's ν̄_α. Why this
family: γ sets the transition sharpness and the exponential Newtonian approach; β moves ν at intermediate y
(y ~ 0.3–3) with no effect on either asymptote, so the two parameters act on different y-ranges. Famaey & McGaugh
(2012) state that the γ = δ = 1 function fits galaxies and that "slightly higher exponents … might still be needed …
to pass Solar system tests involving the external field" — the exact tension tested here.
Limitation stated in advance: this family does not contain ν₂ (its Newtonian approach is exponential, ν₂'s is a
power law). If no member passes SPARC, the empty intersection in (b) is reported as uninformative about the
ν₂-anchored gate, not as evidence.
Grid γ ∈ {0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8} × β ∈ {−0.5, −0.25, 0, 0.25, 0.5, 0.75, 1.0} (84 points).

**(c) Diagnostic, constructed here (not a literature family; tier `[D]` only as a construction):** the tail-cut ν_n,
ν_{n,y_c}(y) = 1 + (ν_n(y) − 1) exp(−(y/y_c)²). It contains ν₂ exactly (y_c → ∞) and leaves ν unchanged where
y ≪ y_c, so it isolates whether Cassini can be fixed by changing only the Newtonian-side tail while SPARC (which
probes y ≲ y_c) stays at ν₂. Grid n ∈ {1.5, 2, 2.5} × y_c = 10^{0, 0.25, …, 3} (39 points).

**Admissibility.** A member is admissible iff, on y ∈ [10⁻¹², 10⁸] (log grid, 20001 points), ν is finite, ν ≥ 1 − 10⁻¹²,
and y ν(y) is strictly increasing (the invertibility condition, FM2012 eq. 39). Inadmissible members are recorded and
excluded from the verdict.

## Numerics

- Q₂: `Q2_richardson(nu, a0, ge, n_r=2000, n_th=100)` (n_r 2000 → 3999, n_θ 100 → 200). PR #194's convergence
  table puts n_r = 2000 within 7×10⁻⁵ of the limit before extrapolation and n_θ = 100 converged to 10⁻⁹ at ν_std.
  Spot checks at production resolution (n_r 4000, n_θ 200, Richardson): n = 10 in (a); (γ, β) = (8, −0.5) and
  (8, 1.0) in (b); smallest y_c at each n in (c). Pre-registered tolerance: relative difference ≤ 10⁻³.
- Verdict per Q₂ with error e: in if inside the band by > 3e, out if outside by > 3e, else INCONCLUSIVE (PR #194 rule).
  Any point within 2×10⁻³ (relative) of a band edge is also run through `efe_quadrupole_q2.Q2` (the frozen gate's own
  integrator); disagreement on side is flagged.
- The ν callables are vectorised with an accurate ν − 1 (`minus_1`) for the solver; no NaN chi² is allowed into
  `summ` (asserted).
- Tier 0 and tier 1 are computed at every grid point at both a₀.

## Boundaries (root-finding)

- (a): per a₀, brentq on max(Q₂(1.9), Q₂(2.4)) = 5.2×10⁻²⁷ in n (Cassini edge n_C), and brentq on each SPARC
  component Δ = ±1 bracketing n = 2 (SPARC window [n_lo, n_hi], using tier-0 agg, the expected binding component,
  then checking all four components at the window edges).
- (b), (c): gate boundaries reported from the grid (linear interpolation between adjacent passing/failing points).

## Decision rule and closest approach

- Joint region = set of admissible grid points (and, in (a), the continuum between roots) where the joint gate holds.
  NON-EMPTY if any row passes; the record then gives the passing points.
- If empty, within each family separately:
  1. min over the SPARC-pass set of Q₂,max (how far above 5.2×10⁻²⁷ the best SPARC-passing member sits);
  2. min over the Cassini-pass set of max|Δ|, naming the binding component;
  3. the Pareto front between Q₂,max and max|Δ|.
  For (a), the separation n_C − n_hi.
- Tier: the computed statement is `[D]` within the stated family and grid only. No statement is made about functions
  outside these families, about AQUAL or AeST (λ_s), or about other SPARC statistics.
