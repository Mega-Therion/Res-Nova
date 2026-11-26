# Pre-Registered Protocol: JWST/NIRSpec High-z Acceleration Scale Evolution Test a0(z) (O4)

**Document Status:** Immutable Pre-Registered Protocol
**Registered:** 2026-11-26
**Extends:** `04_cosmology/PREREG_O4_HIGHZ_A0Z.md` (which tested non-JWST KMOS/SINS `RC100` at $0.6 \le z \le 2.52$)
**Repository:** `Mega-Therion/Res-Nova` (`04_cosmology/`)
**Author:** R.W. Yett
**Target:** Open Problem O4 (`OPEN_PROBLEMS_AND_TESTS.md`) & Optical Map Dynamics-Tier Lever (`03_observer_jwst/OPTICAL_MAP_v0_2026-11-25.md` §3)

---

## 1. Motivation & Public JWST Kinematic Catalogs

Per `OPEN_PROBLEMS_AND_TESTS.md` (§O4) and `03_observer_jwst/OPTICAL_MAP_v0_2026-11-25.md` (§3), testing whether $a_0(z)$ evolves as $H(z)$ is the sole remaining tier-1 dynamical route after C1–C4 closed optical brightening. While no uniform MAST catalog of $z > 10$ resolved rotation curves exists, two homogeneous, peer-reviewed / public-table JWST/NIRSpec resolved-kinematics catalogs now provide exact $V_{\rm rot}(R)$, $\sigma_0$, $R_e$, and baryonic mass estimates spanning $z = 0.575\text{--}5.689$ ($E(z) = 1.38\text{--}9.63$, a $7\times$ baseline in Hubble expansion rate):

1. **Bin 1 — `MSA-3D` (Pastras et al. 2026, arXiv:2606.27853; Cycle 1 JWST/NIRSpec slit-stepping + NIRCam imaging):**
   - **Sample:** 30 star-forming galaxies at $0.575 \le z \le 1.685$ (24 Golden disks + 6 Good disks), tables `galaxy_parameters.tbl`, `fitted_parameters_v14.tbl`, and `fitted_parameters_stat_sys_v14.tbl`.
   - **Primary Uncensored `mbar` Subset ($N = 20$):** The 15 Golden + 5 Good galaxies with two-sided bounded $\log M_{\rm bar}$ posteriors and total (`stat` $\oplus$ `sys`) uncertainties.
   - **Dispositions for Censored $\log M_{\rm bar}$ Rows ($N = 10$):** Galaxies `[2824, 3399, 6199, 8365, 8942, 9337, 11225, 11843, 12015, 29470]` hit the lower `-0.5 dex` prior boundary (`< log M_bar`) and are excluded from the headline bounded `mbar` subset, then explicitly reinstated in two censoring/non-circularity checks (`route='fdm'` across all 30 galaxies, and halo-free catalog `M_bar,0` scaling across all 30 galaxies).

2. **Bin 2 — `ALPINE-CRISTAL-JWST` (Lee et al. 2026, arXiv:2611.07064; JWST/NIRSpec-IFU H$\alpha$ + ALMA [C II]):**
   - **Sample:** All 5 W15-confirmed rotating disks at $4.4403 \le z \le 5.6886$: `DC-494763` ($z=5.2337$), `DC-519281` ($z=5.5759$), `DC-536534` ($z=5.6886$), `DC-630594` ($z=4.4403$), `DC-742174` ($z=5.6360$, flagged in paper as borderline disk/clumpy merger and tested in sensitivity).
   - **Non-circular baryons:** $\log M_\star$ (SED) + $\log M_{\rm gas}$ (`[C II]` luminosity via Zanella+2018, propagated in linear mass with quadrature errors). Zero dark-matter halo prior enters $M_{\rm bar}$.
   - **Kinematics at $R = 2.2\,R_d = (2.2/1.67835)\,R_e \approx 1.3108\,R_e$:** Primary uses beam/PSF/LSF-deconvolved `V_circ^DYSMALpy` (Table 2 col 12); sensitivity tests non-parametric `V_circ` (col 11) and excluding `DC-742174`.

3. **Auxiliary `[O]` Reference Only (excluded from primary $\chi^2$):**
   - `de Graaff et al. 2024` (arXiv:2308.09742; 6 JADES NIRSpec G395H galaxies at $5.504 \le z \le 7.432$). Has only stellar masses (`BEAGLE`, no measured cold gas mass) and high turbulent dispersion ($\sim 3\times$ systematic gas-fraction uncertainty); checked separately for order-of-magnitude bounds only.

---

## 2. Frozen Methodology, Physical Conversions & Hypotheses

Identical physical conventions and likelihood engine (`02_galaxy_dynamics/highz_a0_method.py` `JointA0Likelihood`) to `PREREG_O4_HIGHZ_A0Z.md`:

- **Interpolating Function:** Standard MOND $\mu_{\rm std}(x) = x / \sqrt{1+x^2}$ (`[P]`).
- **Cosmology Conversion:** Both MSA-3D and ALPINE-CRISTAL-JWST publish lengths and stellar/gas masses under $(H_0=70, \Omega_m=0.30, \Omega_\Lambda=0.70)$. Converting to Planck 2018 flat $\Lambda$CDM ($H_0=67.36\,\mathrm{km\,s^{-1}\,Mpc^{-1}}, \Omega_m=0.3153, \Omega_\Lambda=0.6847$) via $f_D(z) \equiv D_{A,\rm Planck}(z)/D_{A,70}(z)$ scales $R \propto f_D$ and $M_{\rm bar} \propto f_D^2$, leaving $g_{\rm bar} \propto M_{\rm bar}/R^2$ invariant and scaling $g_{\rm obs} = V_{\rm circ}^2 / (f_D R)$.
- **Structural Geometry & Pressure Support:**
  - `MSA-3D` ($R = 2.2 R_s = 1.3108 R_e$, disk axis ratio $q=0.25$, bulge $n=4, R_{e,b}=1.0\,$kpc with $(B/T)$ from Table 3; upper-limit $B/T < u$ uses $u/2$ in baseline, $0$ and $u$ in sensitivity): finite-thickness pressure-support law from arXiv:2606.27853 Eq. (6), $V_c^2(2.2R_s) = V_{\rm rot}^2(2.2R_s) + 1.2\,(2.2)\,\sigma_0^2$, with total (`stat` $\oplus$ `sys`) symmetrized quadrature errors plus 10% $R_e$ systematic uncertainty per paper.
  - `ALPINE-CRISTAL-JWST` ($R = 2.2 R_d = 1.3108 R_e$, $q=0.20$, $B/T=0$ per arXiv:2611.07064 §3.4): $g_{\rm obs} = (V_{\rm circ}^{\rm DYSMALpy})^2 / (1.3108 R_e f_D)$, $g_{\rm bar} = k_{\rm sph}(1.3108, n=1, q=0.20)\,G M_{\rm bar} / (1.3108 R_e)^2$, with $\sigma_{R_e} = 0.01'' \times D_A(z)$ angular floor plus 10% disk-scale tolerance check.
- **Frozen Competing Hypotheses (NO per-run refitting of $a_0(0)$ or $\xi$):**
  - $H_{\rm const}$: $a_0(z) = a_0(0) = 1.116 \times 10^{-10}\,\mathrm{m\,s^{-2}}$ (SPARC T3 baseline; SPARC T1 $1.1607\times 10^{-10}$ evaluated as sensitivity).
  - $H_{\rm horizon}$: $a_0(z) = \xi\,c\,H(z)$ with $\xi = 0.170$ fixed from `A0_MEASUREMENT.json` ($a_{0,H}(0) = 1.1128 \times 10^{-10}\,\mathrm{m\,s^{-2}}$).

---

## 3. Primary Statistic & Decision Rules (Pre-Registered)

- **Headline Primary Statistic:** Joint 2-bin profile likelihood `JointA0Likelihood(route="mbar")` sum across Bin 1 (`MSA-3D`, $N=20$, $z \in [0.575, 1.567]$) and Bin 2 (`ALPINE-CRISTAL-JWST`, $N=5$, $z \in [4.440, 5.689]$):
  $$\Delta\chi^2 = \chi^2_{\rm const} - \chi^2_{\rm horizon}, \qquad \Delta\chi^2_{\rm shape} = \chi^2_{\rm shape,const} - \chi^2_{\rm shape,horizon}.$$
  Here $\chi^2_{\rm shape}$ profiles over a single free global multiplicative $a_0$-normalization factor across both bins (protecting against a flat inter-survey mass/kinematic calibration offset masquerading as cosmic evolution).
- **Verdict Criteria (matching `o4_highz_run.py` guard):**
  1. $\Delta\chi^2 \le -9.0$ ($3\sigma$): `H_CONST_FAVORED`.
  2. $\Delta\chi^2 \ge +9.0$ AND $\Delta\chi^2_{\rm shape} \ge +9.0$: `H_HORIZON_FAVORED`.
  3. $\Delta\chi^2 \ge +9.0$ AND $\Delta\chi^2_{\rm shape} < +9.0$: `CONFOUNDED` (normalization offset rather than $E(z)$ scaling drives $\Delta\chi^2$).
  4. $|\Delta\chi^2| < 9.0$: `INCONCLUSIVE` (O4 remains OPEN `[O]`).
- **Secondary Continuous-Slope & Systematic Diagnostics (must be reported alongside headline):**
  - Profiled power-law exponent $n$ in $a_0(z) = a_{0,\rm piv} (E(z)/E_{\rm piv})^n$ comparing constant ($n=0$) vs horizon ($n=1$) independent of $z=0$ calibration.
  - Full `MSA-3D` ($N=30$) uncensored checks (`f_DM(R_e)` route & catalog Tacconi+2018 `M_bar,0` scaling).
  - Confounder suite: Golden-only, outlier removal (`6430`, `9424`, `6199`, `DC-742174`), non-parametric `V_circ`, `-0.2 dex` gas-mass systematic (`Vallini+2025`/`Lee+2025`), asymmetric lower/upper bounds, SPARC T1 baseline, and combined `RC100 + JWST` 4-bin span ($0.58 \le z \le 5.69$).

---

## 4. Execution & Outputs

- **Script:** `04_cosmology/o4_jwst_a0z_run.py`
  - `--self-test`: verifies unit invariance, cosmology $f_D(z)$ scaling, ADC/geometry consistency, synthetic recovery of known $n=0$ and $n=1$ populations without touching real data decisions.
  - Default run: writes `04_cosmology/O4_JWST_A0Z_RESULT.json` and `04_cosmology/O4_JWST_A0Z_RECORD_2026-11-26.md`.
- **Epistemic Tags:** Protocol `[P]`; computed outputs `[D]`; auxiliary `de Graaff+2024` check `[O]`.
