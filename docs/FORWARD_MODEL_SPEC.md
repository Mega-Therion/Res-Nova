# Res-Nova 3-Layer Forward-Model & Provenance Specification

**Status:** Canonical observational pipeline standard (`2026-11-19`).  
**Scope:** Every empirical test, likelihood, and data-comparison script across `Res-Nova` (SPARC, high-$z$ / JWST, Cassini / Solar System, Gaia wide binaries, CMB / BAO / SNe, and Euclid DR1).

---

## 1. The Architectural Separation Rule

Fundamental physical laws must remain covariant and observer-independent. Telescope calibration, sky-plane projection, historical measurement precision, and pipeline software assumptions **never** enter the action $S[g_{\mu\nu}, A_\mu, \phi]$ — they sit in a strict three-layer forward model wrapped by a binary provenance gate:

$$\text{Data}_{\text{recorded}} \;=\; \underbrace{\mathcal{O}_{\text{inst}}}_{\text{Layer 2: Instrument \& Pipeline}}\!\Big(\underbrace{\mathcal{P}_{\text{light-cone}}}_{\text{Layer 1b: Light-Cone \& Projection}}\big(\underbrace{\mathcal{T}_{\text{phys}}}_{\text{Layer 1a: Physical Theory}}\big),\ \eta_{\text{sys}}\Big) + \epsilon_{\text{noise}}, \qquad \text{gated by }\underbrace{\mathcal{G}_{\text{prov}}}_{\text{Layer 3: Provenance}}$$

| Layer | Name | What Belongs Here | What Is Forbidden Here |
|---|---|---|---|
| **1a** | Fundamental Physics ($\mathcal{T}_{\text{phys}}$) | Covariant action, field equations, $\mu_{\text{std}}$, $L_{\mathrm{IT}}$, $a_0$, local physical fields ($g_e$, $\rho_b$, $H(z)$) | Telescope specs, catalog assumptions, historical dates, software bugs |
| **1b** | Light-Cone & Projection ($\mathcal{P}_{\text{light-cone}}$) | Lookback time $t(z)$, Etherington distance duality $D_L = (1+z)^2 D_A$, lensing potential $\Phi + \Psi$, sky projection ($\sin i$, 3D $\to$ 2D orbits, RV perspective), distance scaling ($L \propto D^2, R \propto D$), heliocentric vs. Hubble-flow frames (`zHEL` vs `zHD`), spin-2 shear vs. scalar magnification transfer ($T_1^2 = 0$ vs $T_1^{(\mu)} = 1$) | Silently mixing $\Lambda$CDM distances with non-$\Lambda$CDM dynamics; dropping $\sin i$ or $V_{\text{bar}} \propto \sqrt{D}$ scaling |
| **2** | Instrument, Calibration & Pipeline ($\mathcal{O}_{\text{inst}}$) | Per-object distance errors (`e_D/D`), PSF/beam smearing (`FWHM_arcsec`), spectral LSF, footprint/coverage masks, selection/Malmquist bias, non-circular velocity scatter ($\sigma_{\text{int}}$), sound-horizon $r_s/r_d$ consistent with model $\Delta N_{\text{eff}}$, contaminant mixtures (hidden triples), full `STAT+SYS` covariance | Treating pre-digested $\Lambda$CDM model outputs (e.g., NFW-fitted `fDM`) as raw observables; flat uniform priors overriding tabulated per-object errors; single median beam across mixed AO / seeing-limited instruments |
| **3** | Provenance & Quarantine Gate ($\mathcal{G}_{\text{prov}}$) | SHA-256 dataset checksums, primary arXiv/DOI verification, deduplication across overlapping releases, fail-closed `exit 2` on withdrawn/tampered inputs, `[X]` quarantine of superseded measurements/branches | Blending withdrawn or superseded data into fits with arbitrary weights; fail-open defaults on retired scripts |

---

## 2. Domain-by-Domain Compliance Matrix (`2026-11-19` Audit)

### 2.1 SPARC-175 Rotation Curves
- **Layer 1b Scaling Invariant (enforced in `02_galaxy_dynamics/test_sparc_parser.py`):** Under distance rescaling $D \to f_d D$, luminosity $L \propto f_d^2$ and radius $R \propto f_d$, so $V_{\text{bar}}^2 \to f_d V_{\text{bar}}^2$ and **$g_{\text{bar}} = V_{\text{bar}}^2 / R$ is strictly $f_d$-invariant**, while $V_{\text{pred}} = \sqrt{g(g_{\text{bar}}, a_0)\, f_d R}$.
  - *2026-11-19 Fix `[D]`:* `sparc_a0_reextract_3mu.py`, `sparc_a0_reextract_std.py`, and `scripts/a0_distance_corrected_reextract.py` previously omitted `fd` on `vb2` and $\sqrt{73/67.4}$ on `Vgas/Vdisk/Vbul` in Treatment `T2`. All three are now fixed (with `--legacy-buggy-fd` preserved solely for forensic reproduction of archived `A0_DISTANCE_CORRECTED_2026-09-16.json`) and guarded by `test_sparc_parser.py`.
- **Layer 2 Nuisance & Scatter Budget (`audits/2026-11-19/sparc_forward_model_ablation.py` `[D]`):**
  - Per-galaxy `e_D/D` (`2.3%–30.4%`) requires an adaptive per-galaxy grid (a coarse fixed step undersamples `2–3%` TRGB disks).
  - Including `e_D/D`, inclination $i \sim \mathcal{N}(\text{Inc}, e_{\text{Inc}})$ (Li et al. 2018 Eq. 4), standard cuts (`Q < 3`, `Inc >= 30°`), and exact Gaussian log-likelihood intrinsic scatter $\sigma_{\text{int}}$ (`MLE 5–7 km/s`) reveals a **`~10–15%` forward-model systematic bandwidth** on fitted $a_0$ (`1.075–1.214 × 10⁻¹⁰ m s⁻²` across full-sample treatments; median per-galaxy $a_0$ steady at `1.083–1.181 × 10⁻¹⁰`).
  - **Consequence:** The historical `11.4%` (`f_emp = 1.114365`) gap against $cH_0/(2\pi) = 1.0422 \times 10^{-10}$ sits inside this forward-model bandwidth and is **not** a 6-digit physical constant to derive from holonomy.
  - **Open Layer 1b item `[O]`:** Per-galaxy cosmic-web external field $g_{\text{ext}}(\mathbf{x})$ is not yet included in the SPARC likelihood.

### 2.2 High-$z$ / JWST $a_0(z)$ Kinematics
- **Layer 3 Fail-Closed Rule:** `03_observer_jwst/a0_of_z.py` and `a0_of_z_v2.py` now exit with code `2` by default (refusing the 2026-09-27 withdrawn 20-row table unless explicitly passed `--data` or `--allow-withdrawn-archive`), verified by `tests/test_forward_model_guards.py`.
- **Layer 2/3 Contamination Proof (`audits/2026-11-19/highz_forward_model_check.py` `[D]`):**
  - Re-analyzing the **exact same 19 $z > 1.5$ galaxies** between Genzel et al. (2020, RC41) and Nestor Shachar et al. (2023, RC100) shifts inferred $a_0$ by `0.35×` to `1.73×` (`RMS |Δ ln a0| = 0.394`) purely from analysis-pipeline updates.
  - RC41 $z > 1.5$ beam FWHMs span `0.25"` to `0.75"` (`3.0×` spread across AO and seeing-limited modes), invalidating single-beam proxies.
  - Rescaling `Re_kpc` from RC100's native `H0=70, Om=0.30` to Planck (`67.36, 0.3153`) shifts median $a_0$ by `-2.5%` (`2.821 → 2.751 × 10⁻¹⁰`); every covariance (`rho in [-0.7, +0.7]`) and inclination-error (`sigma_i in [0, 8] deg`) sweep leaves both $n=0$ and $n=1$ inside the 95% CI (status remains inconclusive).
- **Required Raw-Observable Route `[O]`:** Any future decisive JWST $z > 1.5$ test must abandon $\Lambda$CDM-modeled `fDM` proxies and ingest raw line-of-sight velocity curves $V_{\text{los}}(\theta)$, angular radii $\theta$, per-object PSF/LSF FWHM, photometric inclinations $i \pm e_i$ (`i >= 30°`), and fluxes $F$ through the cosmology-free light-cone invariant $a_{0,R}^2 / a_{0,\text{BTFR}}$ verified in `scripts/light_cone_a0.py`.

### 2.3 Solar System / Cassini $Q_2$ & Mercury Perihelion
- **Layer 3 Benchmark:** Park et al. (2026, `arXiv:2602.17884`, DE440 + full Cassini tracking through Aug 2017) $Q_2 = (1.6 \pm 1.8)\times 10^{-27}\ \mathrm{s}^{-2}$ supersedes Hees et al. (2014) `(3 ± 3) × 10⁻²⁷`. `scripts/verify_mu_std_cassini_and_limits.py` and `scripts/repro/cassini_clearance_receipt.json` are updated accordingly.
- **Layer 1b Astrophysical Band (`audits/2026-11-19/cassini_ge_uncertainty_band.py` `[D]`):** Sweeping Milky Way external field $g_e \in [1.5, 2.3]\times 10^{-10}\ \mathrm{m\,s^{-2}}$ ($\pm 21\%$) across all three $a_0$ conventions (`1.0422`, `1.1205`, `1.1607 × 10⁻¹⁰`) yields Richardson-extrapolated QUMOND $Q_2 \in [15.40, 19.89]\times 10^{-27}\ \mathrm{s}^{-2}$, excluding bare unscreened $\mu_{\text{std}}$ at **`+7.67σ` to `+10.16σ`**. Forward-model uncertainty cannot rescue bare $\mu_{\text{std}}$, nor alter the `#228` isotropic-screening or `#232` traceless-Hessian no-go theorems.

### 2.4 Cosmology (CMB, DESI DR2 BAO, Pantheon+)
- **Layer 1b & Layer 3 Strengths:** `04_cosmology/cosmo_data.py` enforces SHA-256 checksums; Pantheon+ likelihoods properly separate `zHEL` (photon redshift/rate) from `zHD` (Hubble-flow comoving distance) and use full `STAT+SYS` covariance.
- **Layer 2 Sound-Horizon Rule (`audits/2026-11-19/bao_cmb_dneff_forward_check.py` `[D]`):** Fixed-$N_{\text{eff}} = 3.046$ formulas (`rd_mpc` Aubourg+2015 Eq. 16 in `04_cosmology/ceiling_model_cmb_bao_sn.py` and GR-extracted CHW Planck priors) **must not** be used unmodified when testing models with non-zero dark radiation at recombination:
  - For the $Q^4$ radiation tracker ($w = 1/3$, $\Delta N_{\text{eff}} \in [0.255, 0.290]$), first-principles integration shrinks $r_d$ by `-0.846%` to `-0.960%`, shifting DESI $D_M/r_d$ by `+0.853%` to `+0.969%` and CMB $\ell_A$ by `+2.56` to `+2.90` (`Δχ²_CMB = +1571` to `+1949` at fixed $H_0 = 67.36$) unless $H_0$ increases by `+2.97` to `+3.38 km/s/Mpc` (`H0 ≈ 70.3–70.7`).
  - Conversely, $Q^3$ ($w = 1/2$, anchored at BBN $z \sim 4\times 10^8$) dilutes to $\Delta N_{\text{eff}}(z_*) = 4.46\times 10^{-4}$ ($\Delta r_d = -0.0047\%$), decoupling BBN from CMB/BAO.

### 2.5 Gaia Wide Binaries
- **Reference Template (`02_galaxy_dynamics/wide_binary_fish.py`, `wide_binary_final.py`):** Already implements 3D orbit projection, RV perspective subtraction, Gaia astrometric errors, `RUWE`/`R_chance_align` cuts, mass stratification, and mock injection calibration.
- **Remaining Layer 1b/2 Items `[O]`:** Fix `boost("E")` anisotropy sign & use true binary-to-Galactic-Center 3D vectors for orientation tests; replace flat-plane contaminant density `2v/VMAX^2` with realistic unresolved hierarchical-triple orbital kicks.

### 2.6 Euclid DR1 Weak Lensing & Magnification Bias
- **Layer 1b Transfer Rule (`[P]` in `EuclidWeakLensingTheory.lean`):** Spin-2 cosmic shear satisfies $T_1^2 = 0$; any mapper or forecast script multiplying $\kappa$ by a heuristic factor (e.g. `gamma = 0.90 * kappa`) to claim an $\ell = 1$ shear-dipole S/N is quarantined `[X]`.
- **Live Forward Model (`[O]` until full DR1 mid-2027):** Must propagate convergence through the observable galaxy number-count magnification-bias transfer $\delta_g(\hat{\mathbf{n}}) = (5s - 2)\,\kappa(\hat{\mathbf{n}})$ (`T_1^(mu) = 1`), explicit source redshift distribution $n(z)$, lensing kernel $W(\chi, \chi_s)$, survey footprint mask, and clustering cosmic variance $C_{\ell=1}^{gg}$.

---

## 3. Acceptance Checklist for Any New Observational Script

Before merging any new empirical comparison script into `Res-Nova`:
1. **Rawest Observable Declared:** State the exact raw observable (`V_obs`, `theta`, `F`, `zHEL`/`zHD`, `Q2`, `delta_g`) and explicitly list every assumed cosmological or astrophysical model inside upstream tables.
2. **Layer 1b Scaling Verified:** Include a deterministic synthetic unit test checking coordinate/distance/projection invariance (e.g., $g_{\text{bar}}$ invariance under $D \to f_d D$).
3. **Layer 2 Uncertainties Complete:** Use tabulated per-object errors and covariances (never flat placeholder priors when per-object errors exist), and check sensitivity to intrinsic scatter or PSF/beam heterogeneity.
4. **Layer 3 Fail-Closed Provenance:** Pin dataset SHA-256 hashes and primary arXiv/DOI citations; fail closed (`exit 2`) on missing, tampered, or withdrawn datasets.
