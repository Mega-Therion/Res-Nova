# O3 route: dark energy as the horizon's landing cost — Ω_Λ = ln 2 and Ω_m = 1 − ln 2

**Date:** 2026-09-28. **Origin:** RY's balanced-ternary / shaken-bottle picture. Superposition is the middle of the
either/or, and the side that doesn't land is dark energy. Leftover fizz gathers at the rim because a bubble's cost goes
with surface area, and least action puts it there. Vault: `10_Notes/Antimatter is the Side That Didn't Land`.
**Tags:** `[D]` computed · `[P?]` premise · `[C]` cited · `[O]` open. **Item:** O3-R1.
**Script:** `04_cosmology/horizon_landing_check.py` → `HORIZON_LANDING_CHECK.txt`.

## The chain

1. **The horizon holds the critical energy `[D]`.** For the Hubble horizon, T_H·S_H = E_c exactly, at any epoch:
   - Gibbons–Hawking temperature T_H = ħH/2πk_B;
   - entropy S_H = k_B c³A/4Għ;
   - E_c = ρ_c c² × (4π/3)(c/H)³, the critical energy inside the horizon.
2. **The horizon is a grid of cells `[C]`+`[P?]`.** S_H/k_B = A/4ℓ_P² cells of one nat each, the Bekenstein–Hawking
   count. There are about **2×10¹²² of them**.
3. **One balanced landing per cell `[P?]`, RY's input.** Each cell's superposed middle resolves into one side of a
   balanced either/or: one bit, ln 2 nats.
4. **A landing costs k_B T ln 2 `[C]`+`[P?]`.** Landauer's minimum cost of a bit, here at the horizon temperature. The
   premise is that this cost is what gravitates as dark energy (the side that didn't land).
5. **Result `[D]` given 2–4:** E_landing = (S_H/k_B)·k_B T_H ln 2 = ln 2 · T_H S_H = ln 2 · E_c, so
   - **Ω_Λ = ln 2 = 0.693147**;
   - the rest of each cell's nat, **1 − ln 2 = 0.306853, is the matter share Ω_m.** That is the flat split Ω_Λ + Ω_m = 1.

## Why it lives on the rim, not in the volume `[D]` counting

The naive vacuum sum is one Planck energy per Planck volume. The measured value is (E_Planck/E_Λ)⁴ ≈ 8×10¹²² times
smaller, and that ratio is **the number of cells on the horizon (2×10¹²²)**. Counting the leftover per surface cell
instead of per volume cell *is* the missing 10¹²⁰. This is the holographic scaling, and the least-action reading
matches it: the Gibbons–Hawking boundary term of the gravitational action is where the area law comes from.

## What stands against it (physics, not procedure)

- **All epochs vs today.**
  - Tied to the Hubble horizon at every epoch, ρ_Λ ∝ H² tracks matter: w = 0, so no acceleration. This is Hsu 2004,
    and it is observationally excluded.
  - So either the landing happened once and fixes Λ (then ln 2 is the value at the landing, and "why now" moves there),
    or the rim is the *event* horizon (Li 2004), where Ω_Λ evolves and ln 2 must come out of the dynamics.
- **The bulk cancellation is a premise.** The volume's landed/unlanded pairs are assumed to cancel pairwise; only the
  rim's leftover gravitates.
- **Data.**
  - Pantheon+: ln 2 is 1.37σ from the best fit, CONSISTENT.
  - Planck TT+TE+EE: Δχ² = +7.2 (2.7σ), under pressure (`TARGET_D11`).
  - A DESI-style evolving w would favor the event-horizon version.

## Prior art `[C]`

- Gough 2011, *Holographic Dark Information Energy* (Entropy 13, 924; arXiv:1105.4461): Landauer plus the
  holographic principle as dark energy. Here the difference is the per-cell balanced landing, which gives exactly
  ln 2, and the matter share 1 − ln 2.
- Cohen, Kaplan & Nelson 1999 (PRL 82, 4971): the area-scaled vacuum-energy bound.
- Hsu 2004 (PLB 594, 13; hep-th/0403052): the w = 0 obstruction for a Hubble cutoff.
- Li 2004 (PLB 603, 1): the event-horizon cutoff.
- Gibbons & Hawking 1977 (PRD 15, 2752): horizon entropy from the action's boundary term.
- Landauer 1961.

## The ceiling, tested against supernovae `[D]` (same night)

RY: if the dark-energy share freezes at all, it freezes near κ = √(θ(2−θ)) = 0.954, the top of the chiral band, not at 1.
Today's share is ln 2 = 0.693, just below the band's floor, 0.707.

**Minimal realization (a premise; one form of several).** The ratio r = ρ_DE/ρ_m grows logistically in ln a:
d ln r/d ln a = 3(1 − r/r_f), i.e. w(a) = −(1 − r/r_f), with r₀ = ln2/(1−ln2) and r_f = Ω_f/(1−Ω_f). So w → −1 early
and w → 0 as the share freezes. At Ω_f = κ this gives **w₀ = −0.891, w_a = −0.292** with **zero free cosmological
parameters**.

**Pantheon+** (1590 SNe, STAT+SYS covariance, zHD > 0.01, M marginalized; the likelihood of
`omega_ln2_pantheonplus.py`). Script `ceiling_model_pantheonplus.py`; output `CEILING_MODEL_PANTHEONPLUS.json`; data
SHA-256 in the JSON, not vendored.

| model | free cosmological params | χ² | Δχ² vs best ΛCDM |
|---|---|---|---|
| flat ΛCDM, Ω_m free (best 0.332) | 1 | 1402.920 | 0 |
| ΛCDM with Ω_Λ = ln 2 | 0 | 1404.831 | +1.91 |
| **ceiling: ln 2 today → κ** | **0** | **1402.570** | **−0.35** |

- With the ceiling left free (share fixed at ln 2 today), the supernovae choose **Ω_f = 0.958, 1σ range 0.936–0.984**.
  κ = 0.954 lies inside, 0.04 in χ² from the best point.
- Among ln 2-anchored models, a ceiling near 0.96 is preferred over none (no ceiling is ln 2-ΛCDM) by Δχ² = 2.3.
- **Reading.** A zero-parameter model fits the supernovae as well as the one-parameter best fit (ΔBIC ≈ −7.7 by
  parameter count), and the supernovae put the freeze at the top of the band. The direction, w₀ > −1 and w_a < 0,
  matches DESI's evolving-dark-energy hint; the model's |w_a| is smaller than DESI's central values.
- **Limits.**
  - This is supernovae only: small Δχ² values, not significant on their own.
  - The logistic approach law is my choice.
  - Part of the preference reflects Pantheon+ wanting a lower share than ln 2 (Ω_Λ = 0.668 in ΛCDM).
  - **CMB and BAO are not yet tested.** Those are the next checks: Planck distance priors and DESI BAO.

## The ceiling against CMB + BAO + supernovae `[D]` (same night)

**Data.**
- Planck 2018 TT,TE,EE+lowE distance priors (R, l_A, ω_b), using the inverse covariance of Chen, Huang & Wang 2019
  (arXiv:1808.05724), read from the paper's source.
- DESI DR2 BAO, 13 measurements with covariance (CobayaSampler/bao_data).
- Pantheon+.

Scripts `ceiling_model_bao_sn.py`, `ceiling_model_cmb_bao_sn.py` and `ceiling_scan_cmb_bao_sn.py`; outputs in
`CEILING_MODEL_BAO_SN.json`, `CEILING_MODEL_CMB_BAO_SN.json` and `CEILING_SCAN_CMB_BAO_SN.json`. Data are not vendored;
hashes are in the JSON.

**Validation.**
- BAO-only ΛCDM gives Ω_m = 0.297, against DESI DR2's published 0.2975.
- r_d = 147.05 Mpc, against Planck's 147.09.
- CMB-priors-only ΛCDM gives Ω_m = 0.3163, h = 0.6754, ω_b = 0.02236, all within 0.3σ of Planck.
- Two bugs were found and fixed on the way: a trapezoid sum on a non-uniform grid, and the massive neutrino counted as
  matter near recombination.
- The residual l_A offset at Planck's parameters (302.0 vs 301.47) is the priors' own convention: their central values
  used the chains' z*, while their likelihood uses the Hu–Sugiyama formula. It is absorbed by a 0.3σ parameter shift
  and is common to all models compared.

**BAO + SN (no CMB).** The zero-shape-parameter ceiling at κ beats best-fit ΛCDM by **Δχ² = −4.58**. The free ceiling
is best at **0.950 (1σ 0.93–0.97)**, with κ at Δχ² = 0.04 from the best.

**CMB + BAO + SN.** ΛCDM has 3 parameters (Ω_m, h, ω_b); the ceiling at κ has 2 (h, ω_b). Approach law:
w = −(1 − (r/r_f)ⁿ).

| model | χ² | Δχ² vs ΛCDM | CMB / BAO / SN χ² | w₀, w_a |
|---|---|---|---|---|
| ΛCDM (Ω_m 0.303, h 0.685) | 1419.71 | 0 | 2.47 / 11.84 / 1405.40 | −1, 0 |
| ceiling κ, n = 1 | 1420.78 | +1.07 | 8.70 / 9.51 / 1402.57 | −0.891, −0.292 |
| ceiling κ, n = 2 | 1419.62 | −0.09 | 1.63 / 13.54 / 1404.45 | −0.988, −0.071 |
| ceiling κ, n = 0.5 | 1618.36 | +198.7 | — | −0.670, −0.332 (**excluded**) |
| ceiling free, n = 1 (3 params) | 1417.37 | −2.34 | — | best Ω_f = 0.976 |

**Profile χ²(Ω_f), re-fitting (h, ω_b).**
- n = 1: best **0.975**, 1σ **0.965–0.985**; κ is Δχ² = 3.40 from the best.
- n = 2: best **≤ 0.90** (the grid edge); κ is Δχ² = 2.35 from the best.

**Reading.**
- Supernovae alone and BAO + SN put the freeze at the top of the band, at κ.
- Adding the CMB, **the preferred ceiling depends on the approach law**: 0.975 for n = 1 and ≤ 0.90 for n = 2. κ sits
  between them, about 1.5–1.8σ from either best, so it is viable but not singled out.
- A fast approach (n = 0.5) is excluded.
- κ-ceiling models tie ΛCDM with one fewer parameter, and a free ceiling is mildly preferred (Δχ² = −2.3 at equal
  parameter count).
- **The approach law is the control rod.** Deriving n from the landing dynamics would turn this into a sharp prediction.
- Limits: compressed CMB priors derived under ΛCDM (standard for late-time dark-energy tests, but approximate); r_d from
  the Aubourg fitting formula; Pantheon+ here, DES-Y5 in the next section.

## DES-Y5 in place of Pantheon+ `[D]` (same night)

DES-Dovekie is the recalibrated DES 5-year sample (Popovic et al. 2026, arXiv:2511.07517): 1,820 SNe, 1,623 from DES
and 197 low-z. It is the supernova sample behind DESI's strongest evolving-dark-energy evidence. It shares its low-z SNe
with Pantheon+, so the two are never combined. Script `desy5_ceiling.py`; output `DESY5_CEILING.json`. All data come
from `fetch_external_data.sh`, which checks each file's SHA-256 against `cosmo_data.py`.

**Validation.**
- SN-only flat ΛCDM gives Ω_m = 0.330 (1σ 0.316–0.345), against the published 0.330 ± 0.015.
- The released inverse covariance inverts to diagonal errors whose median ratio to MUERR ⊕ MUERR_SYS is 1.00000001.
- w₀w_aCDM with these Planck priors, DESI DR2 and DES-Dovekie gives w₀ = −0.825, w_a = −0.637 (Δχ² = −10.1 vs ΛCDM
  for 2 extra parameters). The published values, with the full Planck+ACT+SPT CMB, are w₀ = −0.803 ± 0.054 and
  w_a = −0.72 ± 0.21.

**Supernovae only.**

| model | free cosmological params | Δχ² vs best ΛCDM |
|---|---|---|
| flat ΛCDM (Ω_m 0.330) | 1 | 0 (χ² = 1631.42) |
| ΛCDM with Ω_Λ = ln 2 | 0 | +2.44 |
| **ceiling κ, n = 1** | **0** | **−1.53** |
| ceiling κ, n = 2 | 0 | +1.90 |

- Free ceiling, n = 1: best **0.948, 1σ 0.928–0.972**. κ is 0.05 in χ² from the best; Pantheon+ gave 0.958
  (0.936–0.984).
- Free ceiling, n = 2: best 0.842 (0.818–0.876). κ is Δχ² = 4.1 from the best.

**CMB + BAO + DES-Y5.**

| model | params | χ² | Δχ² vs ΛCDM | CMB / BAO / SN χ² | w₀, w_a |
|---|---|---|---|---|---|
| ΛCDM (Ω_m 0.304, h 0.685) | 3 | 1648.93 | 0 | 2.30 / 12.10 / 1634.53 | −1, 0 |
| **ceiling κ, n = 1** | **2** | 1648.11 | **−0.83** | 8.70 / 9.51 / 1629.90 | −0.891, −0.292 |
| ceiling κ, n = 2 | 2 | 1648.49 | −0.44 | 1.63 / 13.54 / 1633.32 | −0.988, −0.071 |
| ceiling κ, n = 0.5 | 2 | 1849.03 | +200.1 (**excluded**) | 104.0 / 84.7 / 1660.3 | −0.670, −0.332 |
| ceiling free, n = 1 | 3 | 1645.45 | −3.49 | — | best Ω_f = 0.973 |
| ceiling free, n = 2 | 3 | 1644.77 | −4.16 | — | best Ω_f = 0.879 |
| w₀w_aCDM | 5 | 1638.86 | −10.08 | — | −0.825, −0.637 |

- **Profile χ²(Ω_f), re-fitting (h, ω_b).** For n = 1 the best is 0.97 (1σ 0.97–0.985), with κ at Δχ² = 2.59. For
  n = 2 the best is 0.88 (0.86–0.90), with κ at 3.72.
- **Why the κ fits reuse the Pantheon+ (h, ω_b).** For the κ ceilings, (h, ω_b) come out identical to the Pantheon+
  run. With the share fixed at ln 2, the SN shape barely depends on them, so CMB + BAO set them and the SN term adds a
  near-constant. The Δχ² differences between the two samples are therefore pure supernova preference.

**Reading.**
- **With DES-Y5 the κ ceilings tie ΛCDM on χ², with one fewer parameter, so ΔBIC ≈ −8.**
  - n = 1: Δχ² = −0.83 (Pantheon+ gave +1.07), ΔBIC = −8.4.
  - n = 2: Δχ² = −0.44 (Pantheon+ gave −0.09), ΔBIC = −8.0.
  - ln N = 7.52 for 1,836 data points.
- The trade-off between ceiling and approach law persists: (Ω_f, n) ≈ (0.97, 1) and (0.88, 2) both fit. The data
  constrain a curve in the (Ω_f, n) plane, and κ lies on it at an intermediate n. The next section measures that n.
- **What the ceiling cannot capture is a phantom past.**
  - w₀w_aCDM does better still (Δχ² = −10.1), about 6 below the best ceiling for 2 more parameters.
  - Its best fit crosses into w < −1 before z ≈ 0.38 (w₀ + w_a = −1.46).
  - A ceiling is non-phantom by construction (w = −1 + sⁿ ≥ −1), so the remaining gap measures how much this data
    combination leans on w < −1 in the past.

## The control rod, measured: n at a κ ceiling `[D]` (same night)

RY: the threshold κ says where the share stops, and the approach law n says how it gets there, a rule rather than a
number. Here Ω_f = κ is fixed and the data choose n, with (h, ω_b) re-fit at each n. Script `ceiling_n_at_kappa.py`;
output `CEILING_N_AT_KAPPA.json`.

| SN sample (with CMB + BAO) | best n | 1σ | 2σ | Δχ² vs ΛCDM (equal count: h, ω_b, n) | w₀, w_a at best n |
|---|---|---|---|---|---|
| Pantheon+ | 1.27 | 1.10–1.57 | 0.99 – unbounded | −2.45 | −0.940, −0.214 |
| DES-Y5 | 1.23 | 1.08–1.47 | 0.98–2.52 | −3.69 | −0.934, −0.226 |

- **Both samples agree on n ≈ 1.25.**
  - n = 1 sits Δχ² = 3.5 (Pantheon+) and 2.9 (DES-Y5) above the best.
  - n = 2 sits 2.4 and 3.2 above.
  - Both are inside 2σ.
- **Parameter count.** With n fitted, the κ ceiling has three parameters, the same as ΛCDM, so these Δχ² are equal-count
  comparisons. Only the fixed-n rows in the tables above carry one fewer parameter.
- **The two sides are bounded differently.**
  - Below: n < 0.98 is excluded at 2σ by both samples. n = 0.9 costs Δχ² = 8.5–9.4.
  - Above: the bound is weak. As n → ∞ the share stays Λ-like until it meets the ceiling, which today is ΛCDM with
    Ω_Λ = ln 2. That limit sits only Δχ² ≈ 3.3 (Pantheon+) and 4.3 (DES-Y5) above the best. So Pantheon+ leaves the
    upper side open at 2σ, and DES-Y5 closes it at 2.5.
  - The scan runs n = 0.8–4.0 in steps of 0.1.
- **Prediction target.** If the ceiling is κ, the data prefer n ≈ 1.25 and require n ≳ 1.
  - First-order kinetics of independent landings gives n = 1, about 1.7–1.9σ from the best.
  - n = 2 is about 1.5–1.8σ from the best.
  - Neither is excluded. A derivation of n from the landing process would be tested at about this strength by current
    data.
- Limits:
  - The generalized-logistic form of the approach law is still a choice.
  - The CMB priors are compressed.
  - n enters only through the share's history.

## Counting landings: the factorial law `[D]` (RY: "how about n factorial", same night)

Factorials enter the landing picture through counting. If landings arrive at random, the chance of k extra landings is
μᵏe^(−μ)/k!. Suppose a unit of dark energy freezes (w → 0) only once its required landings are all present, each with
probability s = r/r_f. Then the frozen fraction g(s), which replaces sⁿ in w = −1 + g(s), is a mix of landing orders
weighted by 1/k!:
- **shifted Poisson** (1 + k landings): g(s) = s·e^(−μ(1−s));
- **zero-truncated Poisson** (k ≥ 1 landings): g(s) = (e^(μs) − 1)/(e^μ − 1).

μ = 0 is the glide (n = 1) in both. **μ = 1 weights the k-landing channels exactly by 1/k!.** That value was named
before the fit.

Method: Ω_f = κ, with (h, ω_b) re-fit, against Planck priors + DESI DR2 BAO + each SN sample. The share equation
d ln r/d ln a = 3(1 − g) is solved by quadrature. With g = sⁿ it reproduces the closed-form E(z) to 7×10⁻⁹. Script
`ceiling_factorial_law.py`; output `CEILING_FACTORIAL_LAW.json`.

| law at κ | Pantheon+: best, Δχ² vs ΛCDM | DES-Y5: best, Δχ² vs ΛCDM | μ = 1 fixed, no fitted shape: Pantheon+ / DES-Y5 |
|---|---|---|---|
| power sⁿ | n = 1.25, −2.47 | n = 1.2, −3.69 | — |
| shifted Poisson | μ = 0.75 (Δχ² ≤ 1: 0.5–1.5), −2.36 | μ = 0.5 (0.25–1.25), −3.46 | −2.21 / −3.13 |
| truncated Poisson | μ = 1.25 (0.75–2.5), −2.35 | μ = 1.0 (0.5–2.0), −3.50 | −2.22 / −3.50 |

**Reading.**
- The counting laws fit as well as the best power law, within 0.1–0.3 in χ². The data measure "a bit steeper than a
  glide", not the functional form.
- **μ = 1 lies inside Δχ² ≤ 1 of every best fit**: both variants, both samples.
- **The parameter count at μ = 1.** Fixing μ = 1 leaves the approach law with no fitted shape. The κ ceiling then has
  two parameters (h, ω_b), one fewer than ΛCDM. Its Δχ² is −2.2 (Pantheon+) and −3.1 to −3.5 (DES-Y5), so
  **ΔBIC ≈ −10 to −11**.
- At μ = 1 the truncated law is g(s) = (eˢ − 1)/(e − 1), giving (w₀, w_a) = (−0.933, −0.198) today. That is close to
  the best power law (n = 1.25: −0.937, −0.220), which is why the two fit alike.
- **Open: why μ = 1**, i.e. why the mean number of extra landings per cell would be one. One candidate is one expected
  extra landing per cell per Hubble time. Deriving it from the raster would make this a prediction. *Not yet derived.*
- **RY: "maybe it's 1/137 cells per witness."** Both readings are tested as named points (the `named` block of the
  JSON, both Poisson laws):
  - μ = α, one witness per 137 cells: witnessing is so rare that the law becomes the glide. Δχ² above the best is
    +3.3 (Pantheon+) and +2.6 (DES-Y5).
  - μ = 1/α, 137 witnesses per cell: cells lock in only at the very end, so the share stays Λ-like (ln 2-ΛCDM). Δχ²
    above the best is +3.2 and +4.1.
  - Both are disfavoured at about 1.6–2σ, not excluded. μ = 1 sits within 0.3 of the best.
  - **Reading.** The data want about one witness per cell. α remains compatible as a per-chance probability: one
    witness per cell at odds 1/137 per chance needs about 137 chances per cell. Why that many is the same open
    question as why α = 1/137. *Not yet derived.*
- **Honeycomb version (RY: the number 6, the bee's hexagon).**
  - **The rule.** Each landing hands exactly one record to a randomly chosen one of its p neighbours. Each cell then
    receives k ~ Binomial(p, 1/p) records.
  - **Two properties.** The mean is exactly one for any p, because records out equal records in. The odds tend to
    1/(e·k!) as p → ∞.
  - No shape parameter is fitted. Script `ceiling_honeycomb_law.py`; output `CEILING_HONEYCOMB_LAW.json`.

| p (neighbours) | Pantheon+ Δχ² vs ΛCDM, shifted / truncated | DES-Y5 Δχ² vs ΛCDM, shifted / truncated |
|---|---|---|
| 3 | −1.98 / −2.05 | −2.78 / −3.41 |
| 4 | −2.05 / −2.11 | −2.89 / −3.44 |
| **6 (honeycomb)** | **−2.12 / −2.15** | **−2.98 / −3.47** |
| 12 | −2.17 / −2.19 | −3.06 / −3.48 |
| ∞ (Poisson, μ = 1) | −2.21 / −2.22 | −3.13 / −3.50 |

  - **The neighbour count barely matters.** p = 3 to ∞ spans 0.2–0.4 in χ². What the data see is the mean of one
    record per cell.
  - **Parameter count.** At p = 6 the κ ceiling has two parameters, one fewer than ΛCDM, so ΔBIC ≈ −9.5 (Pantheon+)
    and −10.5 to −11.0 (DES-Y5).
  - **What this changes.** "Why μ = 1" becomes "why exactly one record per landing": a conservation statement rather
    than a tuned rate. *Not yet derived.*

## Direction matters? Hemisphere split of the supernovae `[D]` (same night)

RY: light from ahead of our motion and light from behind, or light crossing more intervening mass, need not tell the
same story. The analyses above are sky-averaged, and Pantheon+ zHD already removes our kinematic dipole and peculiar
velocities.

**Test.** Split the official Pantheon+ set by hemisphere, fit each side with its own trimmed covariance and M
marginalized, and compare. Script `pantheon_hemisphere_split.py`; output `PANTHEON_HEMISPHERE_SPLIT.json`.

| axis | side | N | Ω_m (ΛCDM) | free ceiling Ω_f (1σ) | χ²(κ) − χ²(ΛCDM) |
|---|---|---|---|---|---|
| CMB dipole (our motion) | toward | 556 | 0.318 ± 0.024 | 0.996 (0.968–0.996) | +1.99 |
| CMB dipole | away | 1034 | 0.342 ± 0.022 | 0.932 (0.908–0.960) | −1.52 |
| Galactic centre (most mass) | toward | 544 | 0.346 ± 0.030 | 0.968 (0.932–0.996) | +1.26 |
| Galactic centre | away | 1046 | 0.338 ± 0.020 | 0.944 (0.920–0.972) | −0.95 |

**Reading.**
- No significant asymmetry in Ω_m: 0.7σ along the dipole axis, 0.2σ along the Galactic-centre axis.
- One pattern to track: **along our motion, the forward hemisphere prefers no freeze (Ω_f → 1, w ≈ −1) and the
  backward hemisphere prefers a ceiling near 0.93.** The 1σ ranges do not overlap, roughly a 1.5σ hint.
- Prior art: Colin et al. 2019 (A&A 631, L13) claimed a dipole in cosmic acceleration aligned with the CMB dipole;
  Rubin & Heitlauf 2020 (ApJ 894, 68) disputed it. Pantheon+ shows at most a weak, non-significant version.
- DES-Y5 cannot repeat the split. Its deep fields give four sky directions instead (below). The one-way-light-speed
  prediction comes out as zero beyond kinematics (below).

**DES-Y5: four sky directions, one telescope `[D]`.**
- **Why no split is possible.**
  - Every DES supernova lies in the hemisphere facing away from the CMB-dipole axis (cos θ from −0.68 to −0.27).
  - Along the Galactic-centre axis only the E fields face it.
  - The 197 low-z SNe carry no positions in this release.
  - So no hemisphere split with a cosmology fit on each side is possible.
- **What the deep fields give instead.** Four sky directions, observed with the same telescope and pipeline.
- **Method.** Separate low-z and DES offsets, with Ω_m profiled (`desy5_ceiling.py`, `direction` block of the JSON):

| field group | N | RA, Dec (mean of hosts) | offset vs DES mean (mag) | cos θ to CMB dipole | cos θ to Galactic centre |
|---|---|---|---|---|---|
| C (CDF-S) | 580 | 53.6, −28.2 | −0.008 ± 0.007 | −0.30 | −0.42 |
| E (ELAIS-S1) | 283 | 8.7, −43.6 | +0.006 ± 0.008 | −0.59 | +0.20 |
| S (Stripe 82) | 240 | 41.9, −0.7 | +0.008 ± 0.009 | −0.58 | −0.62 |
| X (XMM-LSS) | 520 | 35.7, −5.1 | −0.006 ± 0.007 | −0.65 | −0.51 |

- **One common offset vs four:** Δχ² = 2.76 for 3 dof (p = 0.43). The four directions agree to better than 0.01 mag.
- **cos θ dipole across the DES fields:**
  - Along the CMB dipole, A = −0.018 ± 0.026 mag (δd_L/d_L = −0.8 ± 1.2 %).
  - Along the Galactic centre, A = +0.010 ± 0.015 mag (+0.5 ± 0.7 %).
  - Both are consistent with zero.

**What the aether wind predicts for light `[D]`, given AeST's matter coupling.**
1. In AeST all matter, light included, couples to one metric, g̃ = e^{−2φ}g − 2 sinh(2φ) A⊗A (Skordis & Złośnik 2021).
   *Premise.*
2. At any event, local coordinates make g̃ Minkowskian. The matter action then contains neither A nor φ, so every
   non-gravitational experiment (clocks, rods, light) is locally Lorentz invariant. Two-way light speed is isotropic for
   every observer, whatever their motion through the aether. *Derived.*
3. The one-way speed needs a synchronization convention (Reichenbach; Anderson, Vetharaniam & Stedman 1998, Phys. Rep.
   295, 93). With only g̃ in the matter sector, no experiment there can tell conventions apart. *Cited and derived.*
4. So light from ahead of our motion and light from behind differ only by standard kinematics: Doppler, aberration,
   and the CMB-frame redshift correction already in zHD. **At background order, the predicted Hubble-diagram dipole
   beyond kinematics is zero.** This matches the Pantheon+ split (0.7σ in Ω_m) and the DES fields above.
   Inhomogeneities in A and φ do enter light paths, through g̃, as lensing-type effects along each line of sight. They
   are not a direction-dependent light speed.
5. **Where the wind can show.** Only in gravity's own sector:
   - preferred-frame PPN α₁, α₂ (D3);
   - the dwarf-satellite response (D7).

   At cosmological scale, a tilt between the aether frame and the matter frame would be a new ingredient. It would show
   in number-count dipoles, not in light speed. The CatWISE quasar dipole (Secrest et al. 2021, arXiv:2009.14826)
   points along the CMB dipole with over twice the kinematic amplitude (4.9σ); it is the observation such a tilt would
   have to face. *Not yet derived.*

In terms of RY's blast question (one event, several waves at different speeds): light is the flash, which the wind does
not touch, and the aether's own modes are the sound.

## Status and next

`[O]`. This is a derivation *given* premises 2–4. It is not yet the closure O3 asks for, a covariant action whose
Friedmann constraint yields ln 2 on-shell. The next steps turn the premises into consequences:
1. Build the raster action with its Gibbons–Hawking-type boundary term, and show that an unlanded "bubble" costs energy
   ∝ boundary area.
2. Show that one balanced landing per cell is the action's stationary point.
3. Pick between the once-landed Λ and the event-horizon version by the acceleration history (w₀, w_a).
4. Derive the approach law n from the landing kinetics. At a κ ceiling, both supernova samples prefer n ≈ 1.25
   (1σ about 1.1–1.5; n ≳ 1 at 2σ; the upper side is weakly bounded). The factorial counting law with μ = 1 fits as
   well with no fitted shape. What remains is to derive μ = 1.
