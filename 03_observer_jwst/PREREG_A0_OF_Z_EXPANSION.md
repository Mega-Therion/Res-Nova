# Pre-Registered Expansion Protocol: High-Redshift a₀(z) Test with JWST and Strong Lensing

**Document Status:** Immutable Pre-Registered Protocol Extension  
**Predecessor:** `PREREG_A0_OF_Z.md` (initial MUSE-DARK III test, completed)  
**Prior Result:** H_const favoured over H_horizon at 5.9σ (20 galaxies, 0.41 ≤ z ≤ 1.44)  
**Target:** Extend redshift leverage to z ~ 2-5 using JWST NIRSpec and strong lensing tracers  
**Repository:** `Mega-Therion/Res-Nova` (`03_observer_jwst/`)  
**Author:** Ryan W. Yett / Res-Nova Epistemic Architecture  

---

## 1. Motivation

The initial pre-registered test (PREREG_A0_OF_Z.md) on 20 MUSE-DARK III galaxies excluded the horizon evolution hypothesis H_horizon at 5.9σ. However:

1. **Sample size is small** (20 galaxies, 1 point each). A larger sample could shift the result.
2. **Redshift range is limited** (z ≤ 1.44). At z = 2, H(z)/H₀ ≈ 3.0; at z = 5, H(z)/H₀ ≈ 7.5. The predicted a₀ difference between H_const and H_horizon grows from ~2× at z=1 to ~8× at z=5, making high-z data far more discriminating.
3. **Systematics differ.** JWST/NIRSpec kinematic measurements at high z have different selection functions, resolution effects, and mass-to-light ratio priors than MUSE.

This protocol extends the test to higher redshift and larger samples while maintaining the same frozen theoretical framework.

---

## 2. Frozen Theoretical Framework (Unchanged from Initial Protocol)

- **Cosmology:** Flat ΛCDM, H₀ = 67.4 km/s/Mpc, Ω_m = 0.315, Ω_Λ = 0.685
- **Interpolation function:** μ(x) = x/(1+x) [P]
- **Kinematic law:** g = g_bar[1/2 + √(1/4 + a₀/g_bar)]
- **ξ frozen from SPARC:** ξ = a₀(0)/(cH₀) ≈ 0.1704
- **No NFW parameters permitted**
- **No re-fitting at test stage**

---

## 3. Data Tiers and Quality Cuts

### Tier 1: JWST NIRSpec 3D Kinematics (Primary)
- **Sources:** de Graaff et al. 2024; Nelson et al. 2023; Price et al. 2024
- **Redshift range:** 0.5 ≤ z ≤ 3.0
- **Quality cuts:**
  - S/N ≥ 5 per kinematic pixel
  - Inclination i ≥ 30° (to limit degeneracy)
  - Beam smearing correction applied (using BEAMSMEAR or equivalent)
  - Velocity resolution σ_v ≤ 30 km/s
  - At least 3 independent radial bins per galaxy
- **Expected sample:** 30-50 galaxies with usable rotation curves

### Tier 2: Strong Lensing Tracers (Secondary Cross-Check)
- **Sources:** SLACS, BELLS, JWST-discovered lenses
- **Method:** Einstein ring radius + velocity dispersion → projected acceleration
- **Redshift range:** 0.2 ≤ z ≤ 1.0 (lenses), source z up to 5
- **Statistic:** Compare lensing-inferred a₀ to both H_const and H_horizon predictions
- **Quality cuts:**
  - Lensing model with ≤ 2 free parameters (b, γ_lens)
  - σ_v measurement error < 15%
  - No complex merger lenses

### Tier 3: MUSE-DARK III Expansion (Consistency Check)
- Re-run initial protocol with any newly published MUSE kinematics
- Include in meta-analysis but do not double-count initial 20 galaxies

---

## 4. Pre-Registered Decision Thresholds

### Primary Test (Tier 1 JWST)
For N JWST galaxies with kinematic points {(g_bar,i, g_obs,i, σ_g,i, z_i)}:

χ²(H_const) = Σ_i [(g_obs,i - g_pred(g_bar,i, a₀(0))) / σ_g,i]²
χ²(H_horizon) = Σ_i [(g_obs,i - g_pred(g_bar,i, ξ·c·H(z_i))) / σ_g,i]²
Δχ² = χ²(H_const) - χ²(H_horizon)

**Verdict rules (unchanged from initial protocol):**
1. H_horizon validated / H_const excluded (3σ): Δχ² ≥ +9.0
2. H_const validated / H_horizon excluded (3σ): Δχ² ≤ -9.0
3. Inconclusive: |Δχ²| < 9.0 or N < 10

### Secondary Test (Tier 2 Strong Lensing)
Separate Δχ² computed independently. Must agree in direction with Tier 1 to claim a joint result.

### Combined Meta-Analysis
If both tiers independently favour the same hypothesis at ≥ 2σ, report a combined significance using Fisher's method (weighted by sample size).

---

## 5. Falsification Criteria

This protocol falsifies:
- **H_horizon** if Δχ² ≤ -9.0 on the JWST sample (confirming the initial MUSE result)
- **H_const** if Δχ² ≥ +9.0 on the JWST sample (reversing the initial MUSE result)
- **Neither** if |Δχ²| < 9.0 — in which case we report "inconclusive" and specify what data would be needed

---

## 6. Systematics to Address

1. **Mass-to-light ratio (M/L):** At high z, stellar populations are younger → different M/L. We use the same SPARC-calibrated M/L priors (Y_d ~ N(0.5, 0.125), Y_b ~ N(0.7, 0.175)) and marginalize.
2. **Beam smearing:** JWST's larger PSF at high z can flatten rotation curves. All galaxies must have beam smearing corrections applied.
3. **Selection bias:** JWST targets star-forming galaxies. The acceleration scale test is independent of star formation rate, but the baryonic mass estimation depends on SFR-dependent M/L.
4. **Adaptive optics:** If AO data is available, prefer it over seeing-limited for resolved kinematics.

---

## 7. Execution Plan

1. **Data acquisition:** Download published JWST NIRSpec kinematic catalogs as they become available
2. **Formatting:** Convert to the standardized input format defined in `a0_of_z.py`
3. **Run:** Execute `a0_of_z.py --data-dir <jwst_catalog> --output A0_OF_Z_JWST_REPORT.json`
4. **Report:** Emit JSON with the same schema as `A0_OF_Z_REPORT.json`
5. **Interpretation:** Apply pre-registered verdict rules. Report result regardless of direction.

---

## 8. What This Test Does NOT Address

- The 1/(2π) normalization problem (O1): Even if H_const is confirmed, the coincidence a₀ ≈ cH₀/(2π) remains unexplained.
- The physical mechanism behind μ(x) (O3): The dual-channel derivation stands regardless of whether a₀ is constant or horizon-tied.
- CMB/structure growth (original O4): Requires full FLRW perturbation theory, not addressed by kinematic tests.
- Cluster-scale validity (O5): Strong lensing tracers probe different scales than galaxy kinematics.

---

## 9. Timeline

- **Q3 2026:** Initial JWST catalogs from de Graaff et al. 2024 expected to be publicly released
- **Q4 2026:** Run Tier 1 test as data becomes available
- **Q1 2027:** Tier 2 strong lensing cross-check
- **Q2 2027:** Combined meta-analysis and publication

This protocol is frozen. Any deviation must be documented as a new protocol version with explicit justification.
