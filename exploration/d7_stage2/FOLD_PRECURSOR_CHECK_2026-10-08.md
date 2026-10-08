# D7 box: is the 1391 kpc stall a fold? Precursor check from existing data (2026-10-08)

**Tier:** `[E]` measurement from committed data. D7 stays `[O]`. No new solve was run.

**Question.** BOX_EXTENSION_SUMMARY_2026-10-06 lists a fold of the stripped branch near 1000–1400 kpc as the leading hypothesis `[O]`. At a fold in box size R, the state Jacobian goes singular, so its smallest eigenvalue, measured in the scale-free form λ_min·R³ (λ_min ∝ R⁻³ is pure geometry), should head toward 0 as R approaches the fold.

**Data.** `BOX_ZERO_MODES_C1.json`: smallest |eigenvalues| of the equilibrated Hessian at the converged state, rungs 10–1000 kpc. Output: `FOLD_PRECURSOR_CHECK_2026-10-08.txt`.

| R (kpc) | λ_min (Ω) | λ_min·R³ |
|---|---|---|
| 10 | 1.665e-8 | 1.665e-5 |
| 30 | 5.468e-10 | 1.476e-5 |
| 100 | 1.682e-11 | 1.682e-5 |
| 300 | 5.661e-13 | 1.528e-5 |
| 1000 | 1.672e-14 | 1.672e-5 |

- Fit: λ_min ∝ R^−2.996.
- λ_min·R³ is flat to ±14%, and it alternates with grid parity (16×32 / 23×46 / 30×60 vs 20×40 / 27×54). It does not drift toward 0.
- The sign pattern of the 6 softest modes (Ω+, ω+, ψ−) is unchanged from 30 to 1000 kpc.

**Reading.** Through 1000 kpc there is no softening precursor of a fold. A fold at about 1391 kpc would have to appear abruptly between 1000 and 1391 kpc, without warning in the converged states. This weakens the fold hypothesis but does not rule it out: no converged state exists at 1391, so the eigenvalue there cannot be measured.

**Cheapest next discriminator.** One converged rung between 1000 and 1391 kpc (e.g. 1150), plus the same eigsh diagnostic. If λ·R³ still sits near 1.6e-5, a fold is unlikely, and the stall points to the line-search / globalisation failure (so a trust-region Newton becomes the tool, not arclength continuation).
