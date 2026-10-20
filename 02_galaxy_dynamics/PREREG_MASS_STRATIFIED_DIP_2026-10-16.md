# Pre-registration: mass-stratified dip in wide binaries

**Frozen  2026-10-16,  before Gaia  DR4.**  Tier `[O]`,  protocol.  No  Gaia catalogue  is opened under this note. The measurement quoted in earlier work, light pairs at 0.939 ± 0.028 of Newton in the 5–10 kAU bin, is not evidence for or against this test. It was read before this protocol existed, and the note that carried it attributed the offset to hidden companions. It is not a bin, not a weight, and not a prior.

## What is predicted

The  action  form has  one  screening edge,  where  the  binary's Newtonian  Frobenius tide equals x*_A = 7.035884281332817×10^{14}. For a point mass that radius is

r_edge  =  (√6 c^2  G  M /  (a0^2  x*_A))^{1/3}  = 9.728  kAU × (M / Msun)^{1/3},

with x*_A = 7.035884281332817×10^{11}. The 10^{14} figure written in an earlier draft of this line was a thousand times too large. The radius above was computed from 10^{11}.

at  a0  = 1.1607×10^{-10}  m/s^2.  The ordinary  MOND  transition,  GM/r^2 =  a0, sits at 7.148 kAU × (M / Msun)^{1/2}. The two move differently. A dip tied to the screening shell must track M^{1/3}. A dip tied to the MOND transition must track M^{1/2}.

The  existing  two-body table  may  be used  to  predict  Γ_r(M, r).  It may not be refit after DR4 is seen.

## Data, when it exists

Gaia  DR4,  expected around  December  2026. An  amendment  written  before any  R(s) number is computed must name the file, its checksum, and the release date. Until that amendment, this test has not started. DR3 and the El-Badry et al. 2021 extract are closed for this question.

## Bins and the statistic

Three  mass  bins, total  mass,  fixed now:  [0.30,  0.60),  [0.60, 1.20),  [1.20, 2.50] Msun. Inside each bin, R(s) is the same velocity ratio the frozen wide-binary pipeline already defines, in logarithmic separation bins of width 0.2 in ln(s/kAU) from 1 to 40 kAU. r_min is the separation of the bin with the lowest R(s), restricted to bins with at least 30 pairs. A bin with fewer than 30 pairs at its minimum is marked untested, not a detection.

Fit  log(r_min/kAU)  = a  +  b log(M_mid/Msun),  with  M_mid  the pair-weighted  mean mass in the bin. Use the three tested bins. If fewer than three bins are tested, the exponent test is not run.

## Decision

- Tidal  shell:  b ∈  [0.25,  0.42].
- MOND transition:  b  ∈  [0.42, 0.58].
- If  the interval on b from the three bins, taken as the range of the leave-one-bin-out slopes, lies entirely inside one of those windows and outside the other, that window is the result. If it meets both or neither, the test is inconclusive. No third function is tried after the fact.

Hidden  companions  are modelled  the  same way  in  every  mass bin,  or in none. A correction applied only to the light bin is a different test and voids this one.

## Shape, added 2026-10-16 before any DR4 number

The W term of one star is g_W = (2/√6) r^{-3} d/dr(r^3 w̃), with w̃ ≥ 0 and w̃ = 0 at r = 0 and at infinity. Then

∫_0^∞ r^3 g_W dr = (2/√6) [r^3 w̃]_0^∞ = 0.

The weight r^3 w̃ rises and then falls, so g_W is positive and then negative. In the sign used by the two-body table that is an outward push, a sub-Newton dip, and then an inward pull, a super-Newton peak, in that order. The integral balance is on g_W. It is not a statement that the two velocity-ratio bins have equal area.

This holds for any x* and any screening function that makes w̃ non-negative and zero at both ends. It does not depend on the mass slope above.

**Decision.** In a mass bin that has a bin with R(s) < 1 at ≥ 2σ and at least 30 pairs, the theory fails if no bin at larger separation in that same mass bin has R(s) > 1. A dip with no peak outside it excludes the W term whatever x* and S are. A peak with no dip inside it is the same failure read the other way. Bins under 30 pairs are untested. This uses the DR4 file named in the amendment and no earlier catalogue.

The reading of S = 1/(1+(x/x*)^2) as a Butterworth response is not part of this decision. S = |1/(1 − i x/x*)|^2 is algebra. Calling the result a second-order Butterworth filter uses ω = √|H| and is not a second free function in this test.
