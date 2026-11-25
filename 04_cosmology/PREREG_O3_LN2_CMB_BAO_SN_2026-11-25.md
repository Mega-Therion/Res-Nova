# Pre-Registered Protocol: Ω_Λ = ln 2 (flat ΛCDM) Against CMB + BAO + SN

**Status:** Immutable pre-registered protocol. It was committed before the test script was written or run.
**Registered:** 2026-11-25
**Target:** O3 (`OPEN_PROBLEMS_AND_TESTS.md`). This is a test path, not a closure attempt. The O3 tier stays `[O]` in every outcome.

## 1. Why this test

O3 was tested against Pantheon+ alone (2026-09-09, Δχ² = 1.89, CONSISTENT). The ceiling-model runs also evaluated the ΛCDM-ln 2 point on three late-time data sets, but those results were never entered in the O3 row:

| Data | Δχ² | Source |
|---|---|---|
| DESI DR2 BAO alone | 1.14 | `CEILING_MODEL_BAO_SN.json` |
| DESI DR2 + Pantheon+ | 0.11 | `CEILING_MODEL_BAO_SN.json` |
| DES-Dovekie alone | 2.44 | `DESY5_CEILING.json` |

The strongest combination, including the CMB, has never been run for the ΛCDM-ln 2 point. The CMB distance priors pin Ω_m h² and the acoustic scale. With BAO they fix Ω_m to about 1%, so this is the sharpest available test of Ω_Λ = ln 2.

## 2. Frozen framework (reuses the validated pipeline, unchanged)

- **CMB:** Chen, Huang & Wang 2019 (arXiv:1808.05724), the Planck TT,TE,EE+lowE distance priors (R, l_A, ω_b), with their inverse covariance. The recipe is exactly as in `ceiling_model_cmb_bao_sn.py`. It reproduces the priors at Planck's best fit with χ²_CMB = 1.16.
- **BAO:** DESI DR2 (`desi_gaussian_bao_ALL_GCcomb_*`, SHA-256 in `cosmo_data.py`), with r_d from Aubourg et al. 2015 eq. 16 (Σm_ν = 0.06 eV).
- **SN, two separate combinations:** never combined, because they share low-z SNe.
  - (A) Pantheon+ with the official zHD > 0.01 cut, full STAT+SYS covariance, M marginalized.
  - (B) DES-Dovekie (1820 SNe), inverse STAT+SYS covariance, M marginalized.
- **Free ΛCDM:** parameters (Ω_m, h, ω_b).
- **Test model:** parameters (h, ω_b), with Ω_Λ = ln 2 exactly. Ω_m solves Ω_m = 1 − ln 2 − Ω_r(Ω_m, h) using CHW radiation, via `om0_ln2`.
- **Minimizer:** Nelder–Mead from (0.31, 0.68, 0.02237) and (0.68, 0.02237), with xatol 1e-6 and fatol 1e-4. Both fits are restarted once from their own optimum to confirm convergence.

## 3. Test statistic and decision rule (frozen)

For each combination (A) and (B): Δχ² = χ²_min(ln 2 point) − χ²_min(free ΛCDM). The two models differ by one degree of freedom, so σ = √Δχ².

- **Δχ² ≤ 9 → `CONSISTENT`.** ln 2 is inside the 3σ region of that combination.
- **Δχ² > 9 → `TENSION`.** The conjectured value is excluded at more than 3σ by that combination.

Both verdicts are reported. No other cut, data set, or re-fit is permitted at test stage. The script emits the verdicts from this rule.

## 4. Epistemic tags (declared in advance)

- The test outcomes are `[D]`.
- Ω_Λ = ln 2 stays `[O]` in every branch. Consistency is not promotion. A TENSION verdict demotes the boundary-condition reading to `[X]`-tension on that combination.
- The quarantine sentence stays in force: "conjectured horizon boundary condition, not a derived density."

## 5. Artifacts

- Script: `04_cosmology/o3_ln2_cmb_bao_sn.py`
- Output: `04_cosmology/O3_LN2_CMB_BAO_SN_2026-11-25.json`
- Summary: `04_cosmology/O3_LN2_CMB_BAO_SN_2026-11-25.md`
