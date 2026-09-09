# Pre-Registered Protocol: Testing Ω_Λ = ln 2 Against the Pantheon+ Likelihood

**Document Status:** Immutable Pre-Registered Protocol
**Registered:** 2026-09-09 (before the test was run)
**Repository:** `Mega-Therion/Res-Nova` (`04_cosmology/`)
**Author:** Ryan W. Yett / Res-Nova Epistemic Architecture
**Target:** Open problem O3 (`OPEN_PROBLEMS_AND_TESTS.md`)

---

## 1. Motivation and scope

O3 states: "A number that is only compared by eye is not a test." The conjectured horizon boundary condition Ω_Λ = ln 2 has never been evaluated against a named cosmological likelihood. This protocol freezes the test before running it.

**What this test can and cannot do.** A consistency result does NOT grant the [O] conjecture: `Ω_Λ = ln 2` remains a conjectured horizon boundary condition, not a derived density (AGENT_COVENANT). The covariant-action closure path for O3 remains open regardless of the outcome. What this test delivers is the missing named-likelihood evaluation: either the conjectured value is numerically consistent with the Pantheon+ SNe likelihood, or it is in tension with it.

## 2. Frozen framework

- **Data:** Pantheon+ SH0ES sample (Scolnic et al. 2022, arXiv:2202.04077), all 1701 SNe Ia, machine-readable files `Pantheon+SH0ES.dat` and `Pantheon+SH0ES_STAT+SYS.cov` from the official data release (github.com/PantheonPlusSH0ES/DataRelease, `Pantheon+_Data/4_DISTANCES_AND_COVAR`).
- **Likelihood:** Gaussian in distance modulus using the FULL statistical+systematic covariance matrix (N = 1701), exactly as the release README mandates. Diagonal-only errors are forbidden by the release and are not used.
- **Model:** flat ΛCDM. `E(z) = sqrt(Ω_m(1+z)³ + Ω_Λ)`, `Ω_Λ = 1 − Ω_m`. Luminosity distance integrated from `z_HEL` per the release convention, `c = 299792.458 km/s`; `H_0` is absorbed into the marginalized absolute magnitude.
- **Nuisance:** the absolute magnitude `M` is marginalized analytically over the full covariance (the standard cosmology-only Pantheon+ likelihood). No other parameters are fitted.
- **Grid:** `Ω_m` ∈ [0.01, 0.99], 981 points, step 0.001.

## 3. Test statistic and decision rule (frozen)

1. `χ²_min` = minimum of the marginalized χ² over the grid (best-fit flat ΛCDM).
2. `χ²_ln2` = marginalized χ² at the pre-declared test point `Ω_Λ = ln 2` (i.e. `Ω_m = 1 − ln 2 = 0.30685…`).
3. `Δχ² = χ²_ln2 − χ²_min`, converted to an equivalent one-parameter Gaussian significance `σ = √Δχ²`.
4. The 1σ/2σ/3σ confidence intervals on Ω_Λ are the regions with `Δχ² ≤ 1 / 4 / 9`.

**Verdict rule (declared in advance):**
- `Δχ² ≤ 9` → `CONSISTENT`: ln 2 lies inside the 3σ interval of the named likelihood.
- `Δχ² > 9` → `TENSION`: the conjectured value is excluded at > 3σ by Pantheon+.

No other statistic, cut, or re-fit is permitted at test stage. The script `omega_ln2_pantheonplus.py` and its output `O3_PANTHEONPLUS_RESULT.json` are the ledgered artifacts; the script must emit the verdict from the frozen rule, not from prose.

## 4. Epistemic tags (declared in advance)

- The **test outcome** (the Δχ², σ, interval, verdict) is `[D]`: computed from named scripts and frozen data.
- The **conjecture** `Ω_Λ = ln 2` remains `[O]` in every outcome branch. Consistency is not promotion; tension would be a demotion to `[X]`-tension for the boundary-condition reading.
- The quarantine sentence stays in force: "conjectured horizon boundary condition, not a derived density."
