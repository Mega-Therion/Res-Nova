# a0(z) COROLLARY vs HIGH-Z MEASUREMENT — first encounter (2026-09-17)

**Status:** the apparent-horizon corollary is CONSTRAINED, not confirmed, not
excluded `[O]`. Its first encounter with high-z data leans AGAINST it in
shape, with every reading calibration-limited.
**Date:** 2026-09-17 (follows PR #68 `02_galaxy_dynamics/A0_HIGHZ_MEASUREMENT_2026-09-16.md` and
PR #69 `HORIZON_SELECTION_AUDIT_2026-09-16.md`).
**Tags:** `[P]` proved · `[D]` derived/verified here · `[C]` cited/calibration-dependent · `[O]` open · `[X]` killed
**Machine:** `scripts/a0_highz_corollary_comparison.py` — 11/11, exit 0.

---

## 1. The corollary under test

From the horizon-selection audit (PR #69): if the channel's thermal circle is
the FLRW apparent horizon, then a0(z) = a0(0)·√(Ω_m(1+z)³ + Ω_Λ) `[D]`. At
z = 1 the ratio is 1.790 (+79%); the ln-separation from constancy is 0.582 —
the single number that separates the two readings.

## 2. The measurement (PR #68, all values `[C]`)

RC100 (Nestor-Shachar 2023, 100 galaxies, anchored on T3 = non-flow SPARC
μ_std, a0_T3 = 1.16306e-10), fDM route, 2 bins, statistical intervals:

| bin | z_eff | a0/a0_T3 (95%) | corollary | stat-only deviation |
|---|---|---|---|---|
| z < 1.2 | 0.867 | 2.597 [1.954, 3.427] | 1.654 | −3.1σ BELOW the point (outside the interval) |
| z ≥ 1.2 | 1.960 | 2.286 [1.930, 2.685] | 2.976 | +3.2σ ABOVE the point (outside the interval) |

Statistically the corollary misses BOTH bins in OPPOSITE directions — that is
the flatness tension, and it is what the shape-only Δχ² 8.9–19.8 against the
Hubble form records. The free power-law slope n has a 95% interval containing
0 in every nominal variant: shape favors CONSTANCY.

## 3. Why this is NOT an exclusion

All of PR #68's own caveats stand, and each one is the size of the tension:

1. **Cross-method calibration `[C]`.** The high-z value depends on the
   Genzel-team dynamical-fit calibration (fDM from GR+NFW fits); a 0.5-ln
   cross-method nuisance (≈ the size of each listed systematic) absorbs the
   entire z=0 step AND the bin-2 gap: the corollary's ln-deviations here are
   0.45 and 0.27, both < 0.5.
2. **The fDM prior confound.** The photometric prior's own z-trend (+0.53) is
   near the fitted trend (+0.38): if fDM is overestimated at high z, a0 is
   artificially flattened — precisely the failure mode that would fake
   constancy against the corollary.
3. **Untested z-dependent systematics.** Beam-smearing and a z-dependent Vc
   bias were not tested; the estimator fails its own bias/coverage self-tests
   (S6: |Δln a0| ≤ 0.0418; S8: −0.0392/−0.0416 at 1× and 1.791× injections).
4. **Anchor variance.** The anchored power law fits badly (p ≈ 0.002–0.009);
   anchored σ values are indicative, not calibrated.

A technical note in the corollary's favor: the S8 self-test injected exactly
the corollary's z=1 ratio (1.791×) and the estimator's bias was −0.0416 ln —
an order of magnitude below the 0.582 separation. The flatness is NOT an
estimator-resolution artifact; if it survives, it is physics.

## 4. Verdict

The corollary is doing what a falsifier should: it is now CONSTRAINED rather
than idle. The falsifier is LIVE and two-sided:

- **If the flatness survives** the three named confounds (calibration, fDM
  prior trend, beam-smearing), the H(z)-coupling leg of the apparent-horizon
  reading dies — the channel would have to couple to something other than
  H(z) (a frozen epoch, conformal-time structure), and
  `HORIZON_SELECTION_AUDIT_2026-09-16.md` must reopen.
- **If the confounds explain the flatness** (each is the right size), the
  corollary stands, untested until the systematics paths close.

**Paths that close it:** (i) maser/geometry-anchored cross-method calibration
(the same named mover as the distance ladder); (ii) a tested beam-smearing
treatment across z; (iii) low-mass, high-z disks (x < 1 regime) where a0 is
not degenerate with fDM.

## 5. Ledger

The corollary of PR #69 enters the falsifier battery as CONSTRAINED-`[O]`:
high-z RC100 shape leans constancy (Δχ² 8.9–19.8 stat-only against the Hubble
form) but every reading is calibration-limited; no reading is excluded; the
test is live with named systematics paths. External row: Ciocan+2026
a0(z≈1) = 2.38e-10 = 2.05× a0_T3 (ΛCDM decomposition) — 0.14 ln from the
corollary's 1.79, within its CI.
