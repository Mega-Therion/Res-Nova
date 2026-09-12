# SPARC Comparison — μ_std Recompute and Retraction of the Prior Headline (2026-09-12)

**`SPARC_MODEL_COMPARISON.md` is deleted, not archived-in-place.** Its headline claim
("GOD wins median −19%") and its central "DERIVED interpolation vs CHOSEN interpolation"
framing are both false, for two independent reasons documented below. Git history retains
the deleted file's full prior content; this document is the honest replacement, not an edit.

## What was wrong (two separate defects)

### 1. There was never a second interpolation function
`PARAMETER_LEDGER.json`'s old provenance block claimed `MOND_interpolation: "CHOSEN by
hand; several variants in use"` as distinct from `GOD_interpolation: "DERIVED, Thm 8.7
dual-channel mu(x)=x/(1+x)"`. The code (`parameter_ledger.py:v_mond_like`) implements
exactly one function, called identically for both the "GOD" and "MOND" rows. The entire
"derived μ beats chosen μ" framing in the deleted comparison document never corresponded
to what the code tested — only `a₀` provenance (derived vs fitted) was ever a live axis.
This defect is independent of which μ is used and was present the whole time.

### 2. μ_dual (the function actually used) was already falsified elsewhere in this corpus
`TARGET_D7_COVARIANT_COMPLETION.md` §4 established `μ_dual(x) = x/(1+x)` leaks a constant,
unscreened acceleration offset (`g = g_N + a₀ − a₀²/g_N` at large x) that violates
solar-system bounds by ~5.7×10⁵. The corrected function everywhere else in this corpus is
`μ_std(x) = x/√(1+x²)` (`g = g_N + a₀²/(2g_N)`, which decays correctly). This SPARC file
was never updated to match — it kept running μ_dual after the correction landed.

## Why this matters at galaxy scale, not just the solar system
The μ_dual/μ_std difference is not solar-system-specific: it's a scale-free relative
effect, largest exactly where `g_N ~ a₀` — i.e. at the galaxy radii SPARC samples densely.
Velocity ratio √(ν_std/ν_dual) measured at 0.936 (x=0.1), 0.887 (x=1), 0.960 (x=10) across
the actual SPARC sample. Both functions agree in the deep-MOND limit, so BTFR/asymptotic
claims elsewhere are untouched — the difference lives specifically in the regime this
comparison tests.

## Recomputed numbers (171 galaxies, 3375 points, identical grids/priors/parser to the
original, only `v_mond_like` changed to μ_std)

| Tier 0 (0 free params) | μ_dual (old, wrong) | μ_std (current) |
|---|---|---|
| GOD median χ²_red | 9.200 | **11.077** |
| MOND median χ²_red | 11.352 | **9.935** |
| Headline | "GOD wins median −19%" | **GOD loses median +11.5%** |

| Tier 1 (374 shared nuisance) | μ_dual | μ_std |
|---|---|---|
| GOD median | 2.952 | 3.360 |
| MOND median | 2.887 | 3.412 |

NFW (μ-independent control) is unchanged at 1.921 in both — confirms the μ_std patch is
surgical and the shift is real, not an artifact of the re-run.

**a₀ does not rescue this.** Scanning a₀ under μ_std: the horizon-derived value
(1.0421×10⁻¹⁰, cH₀/2π) gives median 11.08; MOND's literature-fitted 1.2×10⁻¹⁰ gives 9.93
and wins. The corpus's alternative derived value (1.116×10⁻¹⁰, from
`TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md`) makes it slightly worse, not better.

## Honest current status
Under the μ this corpus now uses everywhere else, GOD's interpolation function is
identical to standard MOND's, and on the one axis that remains (a₀: derived vs fitted),
MOND's fitted value fits the SPARC tier-0 median better. This is a real, negative result
for the "GOD beats MOND" framing — not a defect to explain away. `[D]` empirical,
reproducible via `python3 parameter_ledger.py --out <path>` with `SPARC_DATA_DIR` set to
`02_galaxy_dynamics/sparc_data`.

## Open, not resolved here
Three different a₀ values are in live use across the corpus: 1.0421×10⁻¹⁰ (cH₀/2π,
scripts), 1.116×10⁻¹⁰ (D1 supplement), 1.2211×10⁻¹⁰ (5.461×10⁻¹¹·√5, canonical constants
block) — a 17% spread, not reconciled by this document.

## Any citation of the old "−19%" / "GOD wins tier 0" claim
Anywhere in the manuscript, papers, or ledgers still citing the deleted comparison's
headline (`PAPER_02`, `CLAIM_EVIDENCE_LEDGER.md` F4/F5, `RES_NOVA_VERIFICATION_LEDGER.md`
F4/F5) is now citing a retracted result and needs its own correction pass — not done in
this commit, flagged here so it isn't missed.
