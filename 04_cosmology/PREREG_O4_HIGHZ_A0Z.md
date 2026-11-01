# Pre-Registered Protocol: High-z Acceleration Scale Evolution Test a0(z) (O4)

**Document Status:** Immutable Pre-Registered Protocol
**Registered:** 2026-10-03
**Repository:** `Mega-Therion/Res-Nova` (`04_cosmology/`)
**Author:** R.W. Yett
**Target:** Open Problem O4 (`OPEN_PROBLEMS_AND_TESTS.md`)

---

## 1. Scope & Dataset Survey

O4 requires a frozen, pre-registered catalog, a statistic, and a public script that emits a JSON the ledger can cite for the high-z $a_0(z)$ test. Until executed, no JWST language is permitted in the abstract.

**Survey of Public Data:**
- **MAST / HEASARC JWST NIRSpec:** Hosts raw/pipeline spectra, but no public, machine-readable catalog of resolved galaxy rotation curves and mass models ($g_{\rm obs}, g_{\rm bar}$) exists across $z > 1.5$.
- **MUSE-DARK III (Ciocan+2026, arXiv:2604.22613):** Reports fit $a_0(z) = (1.00\pm0.04)+(1.59\pm0.10)\times 10^{-10}\,\mathrm{m/s^2}$ for 79 galaxies ($0.33<z<1.44$), but per-galaxy tabular data is not publicly released.
- **Frozen Benchmark Catalog (RC100):** Nestor Shachar et al. 2023 (ApJ 944, 78; arXiv:2209.12199v1; DOI:10.3847/1538-4357/acac29), 100 star-forming disk galaxies ($0.6 \le z \le 2.6$). Transcribed in `02_galaxy_dynamics/highz_data/RC100_NestorShachar2023_table3_transcribed.csv` (PDF SHA-256: `a04738e47a61b761a693ba7b156d16240fcffbb1d9252df9456ca4d209aeff22`). Verified reachable via HTTPS.

**Selection Cuts:** $z \ge 0.6$, extended disk rotation curves with valid $V_c, R_e, f_{\rm DM}$ and $\Sigma_{\rm DM}$ checks (100/100 galaxies retained).

## 2. Frozen Framework & Statistic

- **Interpolating Function:** Standard MOND interpolating function $\mu_{\rm std}(x) = x / \sqrt{1 + x^2}$ [P].
- **Hypotheses:**
  - $H_{\rm const}$: Constant acceleration scale $a_0(z) = a_0(0) = 1.116 \times 10^{-10}\,\mathrm{m\,s^{-2}}$ (SPARC baseline).
  - $H_{\rm horizon}$: Horizon-tied evolution $a_0(z) = \xi \, c H(z)$, where $\xi \equiv 0.170 \pm 0.025$ is fixed at the local value measured in `A0_MEASUREMENT.json` (O2) and is **NOT refit**.
- **Cosmology:** Planck 2018 flat $\Lambda$CDM ($H_0 = 67.36\,\mathrm{km\,s^{-1}\,Mpc^{-1}}, \Omega_m = 0.3153$).
- **Test Statistic:** Difference in profile likelihood $\chi^2$: $\Delta\chi^2 = \chi^2_{\rm const} - \chi^2_{\rm horizon}$.

## 3. Decision Rules & O4 Status

1. $\Delta\chi^2 \le -9.0$ ($3\sigma$): `H_CONST_FAVORED` — constant $a_0$ favoured. Horizon evolution $a_0(z) \propto H(z)$ rejected at $\ge 3\sigma$ (demoted to [X]-tension).
2. $\Delta\chi^2 \ge +9.0$ ($3\sigma$): `H_HORIZON_FAVORED` — horizon-tied $a_0(z)$ favoured at $\ge 3\sigma$ ([D] evidence for O4).
3. $|\Delta\chi^2| < 9.0$: `INCONCLUSIVE` — neither hypothesis favoured at $3\sigma$. O4 remains OPEN [O].

**Abstract Policy:** Until a script emits a $\ge 3\sigma$ verdict on a public catalog, no JWST language is permitted in the paper abstract.

## 4. Execution Spec & Artifacts

- **Script:** `04_cosmology/o4_highz_run.py`
- **Output:** `04_cosmology/O4_HIGHZ_RESULT.json`
- **JSON Schema:** `{"status": "completed", "dataset": "RC100_NestorShachar2023", "n_galaxies": 100, "z_range": [0.61, 2.60], "chi2_const": float, "chi2_horizon": float, "delta_chi2": float, "sigma": float, "verdict": string, "o4_status": string, "epistemic_tag": "[D]"}`

## 5. Epistemic Tags

- Protocol & Framework: `[P]`
- Computed Test Result: `[D]`
- O4 Claim Status: `[O]` (remains [O] if inconclusive)
