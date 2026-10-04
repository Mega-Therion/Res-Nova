# Wide-binary test of the fish rule: result (2026-10-04)

Pre-registration: `PREREG_WIDE_BINARY_FISH.md` (dcca5d0) + Amendment A (096c8a8), committed before any fit.
Data `[E]`: El-Badry, Rix & Heintz 2021, Gaia EDR3 wide binaries, Zenodo 4435257. 1,817,594 pairs read.
Scripts: `wide_binary_extract.py`, `wide_binary_fish.py`, `wide_binary_fish_sensitivity.py` (exploratory).
Outputs: `WIDE_BINARY_FISH.json`, `WIDE_BINARY_FISH_SENSITIVITY.json`.

## Validation (pre-registered injection recovery)
χ² of the injected model, 4 dof, threshold 18.5:

| cut | N-injection χ²(N) | F-injection χ²(F) | P-injection χ²(P) | F on N-injection |
|---|---|---|---|---|
| clean | 3.7 | 0.9 | 7.1 | 608.5 |
| loose | 9.2 | 4.8 | 6.1 | 1362.7 |

Every injected model was recovered below threshold, and F separates from N by >300 in χ². The run counts as a verdict run.

## Measured R(s) = α(s)/α(0.5–2 kAU)

| bin (kAU) | clean n | clean R | loose n | loose R | F | S | E | P | N |
|---|---|---|---|---|---|---|---|---|---|
| 2–5 | 1943 | 1.045 ± 0.011 | 2558 | 1.063 ± 0.009 | 1.015 | 1.005 | 1.005 | 1.01 | 1.005 |
| 5–10 | 691 | 1.040 ± 0.023 | 1004 | 1.072 ± 0.018 | 1.106 | 1.02 | 1.015 | 1.01 | 1.005 |
| 10–20 | 301 | 1.099 ± 0.035 | 534 | 1.130 ± 0.025 | 1.332 | 1.075 | 1.005 | 1.00 | 1.015 |
| 20–30 | 62 | 1.109 ± 0.057 | 154 | 1.063 ± 0.025 | 1.724 | 1.171 | 1.015 | 1.005 | 1.015 |

Model columns are the clean-cut predictions. The loose-cut predictions differ by ≤0.05.

## Pre-registered χ² (4 dof; excluded if > 18.5)

| cut | N | F | E | S | P |
|---|---|---|---|---|---|
| clean | 23.2 | **174.8** | 23.6 | 14.9 | 22.5 |
| loose | 93.7 | **732.1** | 59.4 | 76.0 | 96.8 |

## Verdict under the pre-registered rule
- **F (pure fish: the binary is its own system, full internal boost) is EXCLUDED under both cuts.** `[E]`
  - Robustness: across the exploratory eccentricity shifts (γ ± 0.3) and both anchorings, χ²(F) ranges 147–1191. The data never rise toward 1.33/1.72.
- **N, E, S and P: no verdict.**
  - None is excluded under both cuts. S passes clean (14.9) and fails loose (76.0).
  - N, E and P fail both, but see the systematic below. Re-running the same pipeline with a different random seed moved these χ² values by up to ~10 (clean N: 23.2 vs 32.8). Near-threshold values are not stable at NMC = 40.

## Unmodelled systematic `[E]`
- R is already 1.045 (clean, 4σ) and 1.063 (loose, 7σ) in the 2–5 kAU bin.
- There g_N ≈ 10 a0, and every model predicts ≤ 1.015.
- No gravity model in this test produces that offset, so it is a sample or forward-model systematic. Candidates are the eccentricity prior γ(s), hidden companions growing with s, and the M_G→mass relation. It dominates the N/E/P/S χ².

## Exploratory, NOT pre-registered: anchor R to the 2–5 kAU bin (3 dof)

| variant | N | F | E | S | P |
|---|---|---|---|---|---|
| clean, γ nominal | 0.8 | 174.3 | 0.4 | 7.6 | 1.3 |
| loose, γ nominal | 7.4 | 683.4 | 5.0 | **51.0** | 6.9 |
| clean, γ − 0.3 | 11.3 | 1116.7 | 7.3 | 35.3 | 20.0 |
| clean, γ + 0.3 | 4.4 | 208.3 | 4.1 | 4.4 | 3.2 |
| loose, γ − 0.3 | 24.9 | 1191.5 | 10.8 | 70.1 | 29.2 |
| loose, γ + 0.3 | 12.7 | 742.8 | 5.8 | 55.9 | 14.6 |

Once the 2–5 kAU offset is removed:
- N, E and P (Newton / EFE / nesting) fit.
- S (Form-2 screen) is disfavoured in the loose cut in every γ variant (51–70).

This is a lean, not a verdict, because the anchoring was chosen after seeing the data.

## Robustness to the interpolating function and a0 (`wide_binary_fish_functions.py`)
The measured R(s) does not depend on the model. Only the model curves were recomputed (NMC = 40), using the same pre-registered χ² and threshold. Output: `WIDE_BINARY_FISH_FUNCTIONS.json`.

| function | a0 | χ²(F) clean / loose | χ²(E) clean / loose | χ²(S) clean / loose | χ²(P) clean / loose |
|---|---|---|---|---|---|
| μ_std (ν₂) | 1.042e-10 | 155.5 / 713.0 | 18.4 / 71.8 | 14.7 / 79.5 | 27.2 / 86.0 |
| μ_std (ν₂) | 1.2e-10 | 198.0 / 876.8 | 19.3 / 59.2 | 14.7 / 105.0 | 26.3 / 91.1 |
| simple (ν₁) | 1.042e-10 | 274.7 / 981.3 | **5.9 / 9.5** | 11.9 / 72.1 | 13.6 / 46.8 |
| simple (ν₁) | 1.2e-10 | 314.7 / 1098.2 | **8.5 / 8.2** | 20.8 / 88.9 | 13.5 / 55.8 |
| RAR (ν̄₀.₅) | 1.042e-10 | 269.4 / 979.5 | **5.6 / 10.5** | 12.6 / 68.8 | 16.0 / 50.8 |
| RAR (ν̄₀.₅) | 1.2e-10 | 317.4 / 1246.4 | **6.3 / 12.5** | 21.9 / 119.0 | 11.7 / 38.4 |
| ν₆ | 1.042e-10 | 141.8 / 751.1 | 27.4 / 85.0 | 20.7 / 95.7 | 29.9 / 89.2 |
| ν̂₄ | 1.042e-10 | 150.9 / 681.1 | 31.6 / 113.9 | 23.6 / 87.2 | 33.6 / 108.7 |

- **F is excluded for every function and both a0 values: χ² from 141.8 to 1246.4.** The exclusion does not depend on the function. At 20–30 kAU, y ≈ 0.1 and every family is in deep MOND.
- **Standard EFE with a slow-return function (simple or RAR) is the only model under 18.5 in BOTH cuts (5.6–12.5).**
  - Those functions keep a 4–10% boost already at 2–5 kAU (E = 1.035–1.055), which matches the unexplained offset.
  - Under μ_std, E ≈ N, because μ_std returns to Newton fast. That is why the pre-registered E (μ_std) looked Newtonian. It does **not** mean standard MOND is Newtonian here.
  - This is post-hoc (the function was not pre-registered) and it cannot be separated from a triple/mass systematic.
  - These same functions fail Cassini at 8–11σ (`CASSINI_EFE_QUADRUPOLE_2026-09-27.md`). Inside one universal law, a wide-binary fit by RAR-EFE and a Cassini pass are in tension.

## Caveats
- "Loose" is not a true Banik-style fit. Its only contaminant is flat in 2D (fitted c = 0.02–0.04). Banik et al. 2024 fit a hidden-triple population whose ṽ excess sits near 1–2. A flat term cannot absorb that, so it leaks into α.
- A triple fraction that rises with s, or a mass bias that depends on s, would produce the 2–5 kAU offset. That is the leading non-gravitational explanation, and it is why every lean above is soft.
- Bins share the control α, so they are correlated. The χ² treats them as independent. Model-curve MC noise is ±0.03–0.09 in the 20–30 kAU bin (F: 1.625 vs 1.715 for the same 62 binaries between passes).
- Source attributions in the script are **approximate and not checked against source**:
  - mass table "Pecaut & Mamajek 2013";
  - γ(s) "Hwang+2022";
  - Q(q) "Milgrom deep-MOND two-body".
  
  Mass errors that do not depend on s cancel in R. The γ(s) sensitivity is shown above.

## Status against CURRENT_STATE / README (28bef58)
- The README holds the theory's domain to the galaxy regime: ordinary gravity keeps the solar system, and no screen is in either action.
- Wide binaries in the solar neighbourhood sit inside that "ordinary gravity" domain. P (nesting) and S (Form-2) are phenomenological `[O]` and in no action.
- P's prediction (Newtonian passengers) has the same direction as D7's linear held-branch result. That result: linear theory cancels the MOND field for satellites, pointing toward Newtonian satellites. It is not proved beyond linear order.

## What this means for the fish idea `[O]`
- The binary-as-its-own-system reading ("system = gravitationally bound", model F) is dead in Gaia.
- The surviving readings are the ones where a wide binary feels Newtonian inside, with the boost suppressed to the percent level:
  - nesting (P: passenger of the dominant field);
  - EFE;
  - plain Newton.
- Form-2 screening (S ≈ 0.2 at the Sun) predicts a 7–17% rise at 10–30 kAU. Clean data allow it; the loose cut, after re-anchoring, does not.
- Next test to separate P from S cleanly: model the 2–5 kAU systematic (Hwang+2022 γ(s) with its errors, a triple fraction rising with s), raise NMC, and rerun the pre-registered statistic.
