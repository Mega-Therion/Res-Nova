# D7 stage 2: box extension of the stripped state, summary (option 3, descriptive) `[O]`

**Status:** exploratory. D7 branch selection stays **open `[O]`**. Nothing here is a no-go, a verdict, or a physics result. Do not cite it as "AeST disfavoured".
Full record: `PREREG_BOX_EXTEND_2026-10-06.md` (pre-registration, Amendments 1–2, attempts 1–4, diagnostics).

## The five committed boxes (fixed resolution near the dwarf; 100 km/s; g_e = 0; K_B = 1/2; 𝒦₂ = 75)
Source: `BOX_SWEEP_C1_16x32_fixed.json`. e = g/Φ̂-flux − 0.75, the excess over GR's Newton channel, at r_h = 0.3 kpc.

| box edge [kpc] | e | Y/Y_static |
|---|---|---|
| 10 | 5.0827 | 3.72e-2 |
| 30 | 2.9411 | 1.26e-2 |
| 100 | 1.5333 | 3.41e-3 |
| 300 | 0.7444 | 7.98e-4 |
| 1000 | 0.2278 | 7.32e-5 |

- **Local slopes steepen:** for e −0.50, −0.54, −0.66, −0.98; for Y/Y_static −0.99, −1.08, −1.32, −1.98.
- **No positive floor:** fits of a + b·R^−p give a = −0.52 (e) and a = −5.0e-4 (Y). The data show no positive held floor.
- **Reading `[O]`:** this is consistent with the remnant being held up by the box, decaying toward GR's channel. It is **not** box-converged. The pre-registered extension to 3745 kpc was never reached, so its rule never fired.

## Why no solve beyond 1000 kpc (all measured `[E]`)
| attempt | method | outcome |
|---|---|---|
| 1 | Newton from static, 3000 kpc | stall 0.136 (26 steps) |
| 2 | nested-grid continuation, 1391 kpc | stall 0.0333 (13 steps) |
| 3 | projected Newton (soft band removed) | fails validation: the residual moves entirely into the soft band (share 1 − 9e-12), stall 9.98e-5 at 100 kpc |
| option 1 | rescaling (row-sum, Ruiz, Jacobi) | row-sum (current) is already best: κ = 5.8e13 at 1000 kpc, 1.6e14 at 1391 kpc |
| 4 | mixed-precision Newton (long double + GMRES) | validates (100 kpc, 6 steps to 1e-11); stalls at rung 1391 kpc at 0.03325, identical to float64 to 7e-14 |

**Diagnostics.**
- **Soft band:** the smallest Hessian eigenvalue falls as **R^−3.00**, dominated by the shift's gradient part Ω (then ω, ψ). There are ≥ 24 modes within 1000× of λ_min at 100 kpc.
- **Not precision:** attempt 4 rules out arithmetic precision as the limit.
- **Not scaling:** option 1 rules out diagonal conditioning as the fix.

## What would close it (joint decision with RY)
- **Hypothesis `[O]`:** the stripped root branch folds (turns back) near ~1000–1400 kpc at this speed. A fold gives accurate Newton directions without descent at a nonzero residual.
- **Tools that test it:**
  - pseudo-arclength continuation in box size (follows a branch through a fold);
  - a trust-region / Levenberg–Marquardt Newton (globalises in the soft band without the line search's failure mode).
- Either must first reproduce a committed row exactly, as every attempt here did.
