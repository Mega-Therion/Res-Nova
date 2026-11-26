# Pre-Registered Protocol: Blind Test of P-OM-1 v2 on KiDS-Legacy (DR5 Cosmic Shear) and GAMA DR4

**Status:** Immutable pre-registered protocol. Committed and frozen prior to executing the lensing estimator on isolated KiDS-Legacy / GAMA DR4 targets.
**Registered:** 2026-11-26
**Extends:** `03_observer_jwst/PREREG_POM1V2_MASS_SYSTEM_2026-11-25.md` (which tested KiDS-1000 DR4 on already-seen data and owed an independent blind run on KiDS-Legacy / Euclid).
**Author:** R.W. Yett
**Repository:** `Mega-Therion/Res-Nova` (`03_observer_jwst/`)

---

## 0. Public Survey Audit (Euclid vs KiDS-Legacy)

1. **Euclid Q1 / DR1 TAP Negative Check (2026-11-26):** Querying `eas.esac.esa.int/tap-server/tap/tables` shows zero `she_*` weak-lensing shear tables in the public Euclid TAP catalog (`mer_*`, `phz_*`, `spe_*`, and `disk_sersic_*` shape morphology only). Euclid public shear cannot yet be run.
2. **KiDS-Legacy (DR5 Cosmic Shear Gold Catalog, released Dec 2025):** `KiDS_Legacy_NS_unblind_final.fits.gz` exposes 40,894,394 gold sources across 1,347 tiles (`20,471,163` North + `20,423,231` South) with updated `Lensfit v321` shapes, second-pass `i2` photometry, and calibrated 6-bin tomographic `NZ_SOURCE` and multiplicative bias `m_gold = [-0.023, -0.016, -0.011, +0.020, +0.030, +0.045]` (Wright et al. 2025, arXiv:2503.19441 Tables 1–2).
3. **Pre-Unblinding Shear Sanity Checks (performed before computing any isolated ESD / RAR):**
   - Weighted mean ellipticities `(e1, e2)` inside `KiDS_Legacy_NS_unblind_final.fits.gz` across all 12 North/South $\times$ 6 tomographic bins are `0.00e-4` (additive `c_hat` calibration is already applied in the released FITS columns).
   - Tangent-plane sign check on non-isolated massive GAMA galaxies ($\log M_\star > 11.1$, $1.35\times 10^6$ pairs) verifies that image-frame projection $(x = -\Delta{\rm RA}\cos{\rm Dec}, y = +\Delta{\rm Dec})$, $\phi = {\rm atan2}(y, x)$, $e_t = -e_1 \cos(2\phi) - e_2 \sin(2\phi)$ recovers positive convergence $\langle e_t \rangle = +0.00423$ and cross-shear null on randoms $\langle e_t \rangle = -0.00014, \langle e_\times \rangle = -0.00013$. Flipping $e_2$ destroys the signal ($\langle e_t \rangle = +0.00013$).

---

## 1. Blind Lens Samples & Pre-Registered Mass System Conversions

All parameters of the frozen `pom1v2_mass_system.py` / `pom1_lensing_rar.py` model remain **strictly fixed** ($\mu_{\rm std}$, $a_0 = 1.1607\times 10^{-10}\,\mathrm{m\,s^{-2}}$, `point-mass DeltaSigma -> g_obs = 4 G DeltaSigma * (73/70)`). Nothing is fitted to lensing.

Two mutually disjoint **Primary Blind Samples** with zero lens or source overlap with Brouwer et al. 2021 (KiDS-1000 DR4):

### Sample A — `DR5_New329` (Strictly New KiDS-DR5 Sky Tiles Excluding G23 & DR4)
- **Footprint:** All KiDS-DR5 tiles absent from KiDS-DR4 (`dr5_new_tiles`), excluding the 4 border tiles overlapping `GAMA G23`, leaving 329 new tiles covered by KiDS-Legacy sources — **100% unseen lenses and 100% unseen background shear galaxies**.
- **Pre-unblinding photometric calibration (verified zero-shear on G09 $\to$ G23):** Because raw ESO DR5 `Z_B` BPZ redshifts overestimate bright $r<20$ redshifts by $+0.059$ (`+0.047` in G23), inflating LePhare masses via $D_L(Z_B)^2$, a 7-term linear calibration trained solely on G09 photometry $\to$ GAMA `Z_TONRY` is frozen prior to unblinding:
  `z_cal = clip([1, Z_B, Z_B^2, Z_ML, MAG_AUTO-18.5, (u-r)-2.3, MAG_GAAP_r-MAG_AUTO_raw] @ beta_z, 0.02, 0.65)`,
  where `beta_z = [-0.043490, 0.954353, -0.561158, 0.030555, 0.034788, -0.013131, 0.062737]`.
  Held-out test on G23 reduces photo-$z$ bias from `+0.0470` to `-0.0032` (`MAD = 0.0337`), and aligned DR5 stellar mass `logM*_cal = mstar_bestfit + 0.4*(MAG_GAAP_r - MAG_AUTO_raw) + 2*log10(D_L(z_cal)/D_L(Z_B)) + 0.1293` matches GAMA Taylor+2011 identically for LTGs (`-0.1275` before shift) and ETGs (`-0.1305` before shift, zero early/late tilt). Since GAMA agrees with Schombert+2014 (Mistele et al. 2024 §3), calibrated lenses use `Q_LTG = Q_ETG = 1.0`.
- **Cuts & Isolation:** `MASK=0, SG_FLAG=1, SG2DPHOT=0, CLASS_STAR<0.5, MAG_AUTO<20.0`, `0.1 < z_cal < 0.5`, `8.5 < logM*_cal < 11.0`, border-guarded against all DR5 (`r<20.5`) and DR4 (`KiDS_DR4_brightsample`) neighbors with $r_{\rm sat}(f_{M_*}>0.1) > 3\,h_{70}^{-1}\,\mathrm{Mpc}$. Color split: dust-corrected observed `u - r > 2.5` (ETG) vs `<= 2.5` (LTG).
- **Reliable Radial/Acceleration Range:** `0.03 <= R <= 0.30 Mpc/h70` AND `g_bar > GBAR_RELIABLE = 7.56e-14 m/s^2` (7 LTG + 7 ETG = 14 bins, identical to B21/v2).

### Sample B — `GAMA_G23` (Blind Spectroscopic GAMA DR4 Region)
- **Footprint:** GAMA DR4 `G23` (`RA in [338, 352], Dec in [-35.5, -29.5]`, `0.3 deg` interior border guard) paired with ~1.6M new KiDS-Legacy shear sources — **never included in Brouwer et al. 2021**.
- **Catalog:** `DistancesFramesv14.fits` (`NQ >= 3`, exact `Z_TONRY`, `0.1 < z < 0.5`) joined to `StellarMassesGKVv24.fits` (`Taylor+2011` `logmstar`, already on Schombert+2014 system so `Q_LTG = Q_ETG = 1.0` per Mistele et al. 2024 §3; `8.5 < logmstar < 11.0`).
- **Color Split:** Rest-frame `uminusr > 2.00` (mapped to observed KiDS `u - r = 2.5` on G09 prior to unblinding with `92.7%` classification agreement).
- **True 3D Spectroscopic Isolation:** $r_{\rm sat}(f_{M_*}>0.1) > 3\,h_{70}^{-1}\,\mathrm{Mpc}$ using spectroscopic comoving coordinates (eliminating photo-$z$ radial smearing). Evaluated primarily in `0.03 <= R <= 0.30 Mpc/h70`, `g_bar > 7.56e-14` (`14` joint bins) and secondarily out to `R <= 1.50 Mpc/h70`.

### Full-Survey Extension C — `GAMA_All4` (`G09 + G12 + G15 + G23`)
- All four GAMA DR4 regions (`~45,600` 3D spectroscopic isolated lenses) paired with reprocessed KiDS-Legacy shear, reported both on `R <= 0.30 Mpc` (`g_bar > 7.56e-14`, 14 bins) and extended spectroscopic deep-MOND (`0.03 <= R <= 1.50 Mpc`, bins above `log10 g_bar >= -14.5`).

---

## 2. Estimator, Calibration, Covariance & Diagnostics (Frozen)

- **Baryon mass per lens:** LTG uses `M_b = M_* * (1 + 10^(-0.69 log10 M_* + 6.63))` (Boselli+2014 / B21 Eq. 23); ETG uses `M_b = M_* + 10^-5.414 * M_*^1.47` (Chae+2021 / Mistele+2024 Eq. 4.1).
- **Lensing efficiency:** Proper $\Sigma_{\rm crit}^{-1}(z_l, \text{tomo})$ integrated numerically over exact official `KiDS-Legacy NZ_SOURCE` (`BIN1..BIN6` in `KiDS_Legacy_xipm.fits`), with foreground pair cut `z_B + 0.2 > z_l`.
- **Excess Surface Density & `H0=73` conversion:** In Brouwer+2021 `15` log-$g_{\rm bar}$ bins (`log10 g_bar` centers `-14.859 .. -11.407`, width `0.2466 dex`),
  $$\widehat{\Delta\Sigma}_k = \frac{\sum W_{ls} e_{t,ls} \Sigma_{{\rm crit},ls}}{\sum W_{ls} (1 + m_s)} - \Delta\Sigma_{{\rm rand},k}, \qquad g_{{\rm obs},k} = 4 G \widehat{\Delta\Sigma}_k \times \frac{73}{70},$$
  where $\Delta\Sigma_{{\rm rand},k}$ is measured around 5$\times$ (or >=25k) matched-footprint uniform randoms drawing `(z_l, M_b)` from the active lens distribution.
- **Covariance:** Spatial jackknife over $K = 64$ contiguous sky cells ($K = 96$ for extended $1.5\,$Mpc, retaining full off-diagonal radial and cross-type bin correlations).
- **Pre-declared Diagnostics (no verdict change):** Random ESD residual check, cross-shear B-mode null `chi2_cross / dof`, raw ESO DR5 with `Q_ETG = 1.4, Q_LTG = 1.0`, omission of `73/70` conversion, mass-matched `10.2 <= logM* <= 10.9` ETG vs LTG comparison, projected-cylinder photo-$z$ isolation sensitivity (`|dz|/(1+z)<0.02`), and `GAMA_All4` extended `1.5 Mpc` deep-MOND test.

---

## 3. Primary Statistic & Decision Rule (Frozen)

- **Headline Primary Blind Statistic:** Sum of independent block $\chi^2$ across the strictly unseen, sky-disjoint samples **`DR5_New329` + `GAMA_G23`** (`dof <= 28` retained bins in `g_bar > 7.56e-14`), using the frozen `pom1_lensing_rar.py` point-mass $\mu_{\rm std}$ model with $a_0 = 1.1607\times 10^{-10}\,\mathrm{m\,s^{-2}}$ and full jackknife covariances:
  1. **Power gate:** Newtonian point mass on converted baryons must yield $p_{\rm Newton} < 10^{-6}$, else `NO_POWER`.
  2. **PASS:** $p \ge 0.01$.
  3. **PASS_WITHIN_MASS_SYSTEMATIC:** $p < 0.01$, and a single uniform stellar-mass shift $|\delta| \le 0.2\,\mathrm{dex}$ gives $p \ge 0.01$ ($\mathrm{dof}-1$).
  4. **FAIL:** otherwise.
- Individual verdicts for `DR5_New329`, `GAMA_G23`, and `GAMA_All4` (reliable + extended) are emitted under the identical rule, alongside the early-minus-late universality test.

---

## 4. Epistemic Tags & Artifacts

- Protocol: `[P]`; Computed outcomes: `[D]`; Optical map status remains `[O]` unless P-OM-2/3 also close.
- Script: `03_observer_jwst/pom1v2_blind_kids_legacy.py`
- Outputs: `03_observer_jwst/POM1V2_BLIND_KIDS_LEGACY_2026-11-26.json`, `03_observer_jwst/POM1V2_BLIND_KIDS_LEGACY_RECORD_2026-11-26.md`
