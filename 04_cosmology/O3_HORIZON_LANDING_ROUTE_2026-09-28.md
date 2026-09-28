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

## Status and next

`[O]`. This is a derivation *given* premises 2–4. It is not yet the closure O3 asks for, a covariant action whose
Friedmann constraint yields ln 2 on-shell. The next steps turn the premises into consequences:
1. Build the raster action with its Gibbons–Hawking-type boundary term, and show that an unlanded "bubble" costs energy
   ∝ boundary area.
2. Show that one balanced landing per cell is the action's stationary point.
3. Pick between the once-landed Λ and the event-horizon version by the acceleration history (w₀, w_a).
