# 📜 Pre-Registration Protocol V2: Redshift Evolution of the Acceleration Scale $a_0(z)$ — under $\mu_{\rm std}$

**Document Status:** V2 pre-registered protocol — frozen 2026-09-12 and executed immediately after freezing.
**Supersedes:** `PREREG_A0_OF_Z.md` (V1, immutable, retained as history). V1 froze $\mu(x)=x/(1+x)$
— falsified 2026-09-12 (`TARGET_D7` §4/§11) — so its executed result (the 5.9σ constant-$a_0$ verdict,
`A0_OF_Z_REPORT.json`) is **superseded** and must not be cited as live evidence.
**Execution Script:** `03_observer_jwst/a0_of_z_v2.py` (self-validates against the V1 numbers first).
**Output Artifact:** `03_observer_jwst/A0_OF_Z_REPORT_V2.json`.

## What Changed From V1 (frozen before execution)

Only the interpolating function: $\mu(x) = x/(1+x)$ **[X] falsified** → $\mu_{\rm std}(x) = x/\sqrt{1+x^2}$ (live closure, `TARGET_D1_SUPPLEMENT`; empirical coordinate selection `TARGET_D2_SUPPLEMENT` §8). Everything else is byte-identical to the V1 registered design:

- Same 20 published MUSE-DARK III / HUDF kinematic points (Bouché+2021 / Mercier+2022), z = 0.413–1.440
- Same Planck 2018 cosmology (H₀ = 67.4, Ω_m = 0.315, Ω_Λ = 0.685)
- Same frozen $a_0(0) = 1.116\times10^{-10}$ m/s² (the SPARC baseline value) and $\xi = a_0(0)/(cH_0)$
- Same hypotheses: H_const ($a_0$ = const) vs H_horizon ($a_0(z) = \xi\, c H(z)$), no NFW parameters
- Same decision rule: 3σ threshold on $\Delta\chi^2 = \chi^2_{\rm const} - \chi^2_{\rm horizon}$

The $\mu_{\rm std}$ prediction solves $g\,\mu_{\rm std}(g/a_0) = g_{\rm bar}$ in closed form:
$u = g^2 = \tfrac12\left[g_{\rm bar}^2 + \sqrt{g_{\rm bar}^4 + 4 g_{\rm bar}^2 a_0^2}\right]$
(limits: $g \to g_{\rm bar}$ Newtonian; $g \to \sqrt{g_{\rm bar} a_0}$ deep-MOND ✓).

## Executed Result (recorded as found, no post-hoc selection)

| | $\chi^2$(H_const) | $\chi^2$(H_horizon) | $\Delta\chi^2$ | significance | verdict |
|---|---|---|---|---|---|
| V1 (μ_dual) [X] | 5.371 | 40.486 | −35.115 | 5.93σ | H_const |
| **V2 (μ_std) [D]** | **12.886** | **8.645** | **+4.242** | **2.06σ** | **INCONCLUSIVE** |

**The 5.9σ constant-$a_0$ result does not survive the closure swap. Under $\mu_{\rm std}$ the
registered test is inconclusive at the 3σ threshold** — and, notably, $\chi^2_{\rm horizon}$
now sits *below* $\chi^2_{\rm const}$ (8.64 vs 12.89): the horizon-tied model fits these 20
points slightly *better* under the live closure, though not significantly.

## Sensitivity Scan (exploratory, NOT part of the registered test)

Varying $a_0(0)$ (with $\xi$ co-scaled by definition) by ±30% under μ_std: the verdict sweeps
from **H_horizon favoured at 5.4σ** ($a_0\times0.7$) through inconclusive ($\times$1.0–1.1) to
**H_const favoured at 4.0σ** ($\times$1.2). The discrimination is therefore dominated by the
**extraction-μ dependence of the SPARC $a_0$ central value itself**, which was extracted under
the falsified μ_dual and has not been re-derived.

## Consequences

1. **The 5.9σ figure is retracted as live evidence** — [X]-superseded; `.zenodo.json`'s
   description citing it was corrected 2026-09-12 (v1.8.0 blocker resolved by retraction,
   not by re-confirmation).
2. The $a_0(z)$ question reverts to **OPEN [O]**. No live empirical anchor distinguishes
   constant-$a_0$ from horizon-tied $a_0(z)$ at intermediate redshift under the live closure.
3. **Required closure before any re-claim:** re-extract $a_0$ from the full SPARC 175-galaxy
   benchmark under μ_std (`02_galaxy_dynamics`), propagate its central value and error budget
   into this test, and re-freeze as V3. Task Board P1 tracks this.
