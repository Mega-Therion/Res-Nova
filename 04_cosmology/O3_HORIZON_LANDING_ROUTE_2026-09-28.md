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
  the Aubourg fitting formula; Pantheon+ only (DES-Y5 or Union3 would shift toward stronger evolution).

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
- Next: the same split on DES-Y5 and Union3, and the one-way-light-speed prediction (c/(1±β), β ~ 10⁻³) turned into
  a Hubble-diagram dipole amplitude to compare with the split.

## Status and next

`[O]`. This is a derivation *given* premises 2–4. It is not yet the closure O3 asks for, a covariant action whose
Friedmann constraint yields ln 2 on-shell. The next steps turn the premises into consequences:
1. Build the raster action with its Gibbons–Hawking-type boundary term, and show that an unlanded "bubble" costs energy
   ∝ boundary area.
2. Show that one balanced landing per cell is the action's stationary point.
3. Pick between the once-landed Λ and the event-horizon version by the acceleration history (w₀, w_a).
