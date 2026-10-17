# Late-time HDE under the fixed CMB block, and the phantom window on DESI DR2

Pre-registration: `14cc657c48ded81a182a2b3ca48d709e1d037d2d` (`PREREG_HDE_CMB_AND_PHANTOM_2026-10-17.md`), pushed before this fit. Script: `hde_cmb_phantom_2026_10_17.py`. Numbers: `HDE_CMB_PHANTOM_2026-10-17.json`. Runtime 177 s. Tier of the two χ² comparisons: [E] on the published distance priors, DESI DR2, and Pantheon+, through the Li 2004 ODE. The coefficient ln 2 stays [O].

V0 passed. Fixed Chen, Huang & Wang block at Planck 2018 TT,TE,EE+lowE+lensing: χ²_CMB = 1.163. At TT,TE,EE+lowE: χ²_CMB = 1.121. Every pull is inside 1.

## Test 1 — the late-time edge does not survive

Joint likelihood, fixed CMB + DESI DR2 BAO + Pantheon+.

| model | parameters | χ² | CMB | BAO | SN |
|---|---|---|---|---|---|
| ΛCDM | Ω_m = 0.3018, h = 0.6840, ω_b = 0.02252 | 1421.000 | 3.133 | 12.177 | 1405.691 |
| HDE, C free | Ω_m = 0.2975, h = 0.6785, ω_b = 0.02285, C = 0.7214 | 1467.343 | 27.210 | 28.269 | 1411.863 |

Δ₁ = χ²(HDE) − χ²(ΛCDM) = +46.343. The frozen bar for a win was Δ₁ < −9. The late-time edge (Δχ² = −3.5 with no CMB) does not survive. The extra χ² is mostly CMB (27.2 against 3.1) and BAO (28.3 against 12.2). At the HDE minimum, w₀ = −1.108 and w_a = +0.383.

## Test 2 — the crossing history is excluded on DESI DR2 BAO

Radiation-free quadrature from Ω_DE0 = 0.6847 to Ω_DE = ln 2: Δ ln a = 0.013166, absolute error 3.94×10⁻⁶ against Manus's 0.01317. z_cross = −0.01308. Window: z ∈ [−0.02308, −0.00308]. w₀ = −0.9959 today, and w drops below −1 inside that future window. w_a = +0.312.

DESI DR2 BAO only, ω_b = 0.02237, Ω_DE0 fixed at 0.6847, h free.

| history | h | Ω_m | χ²_BAO |
|---|---|---|---|
| HDE, C = √(ln 2), crosses in the window | 0.6627 | 0.31521 | 32.333 |
| ΛCDM, same density, w = −1 | 0.6890 | 0.31521 | 14.393 |

Δ₂ = 17.940. The frozen bar was exclusion at Δ₂ > 9. The crossing history is excluded. Allowed would have required Δ₂ < 4.

## Not redone

The closed 4σ kill of C = √(ln 2) against free C was not rerun. ln 2 was not derived.
