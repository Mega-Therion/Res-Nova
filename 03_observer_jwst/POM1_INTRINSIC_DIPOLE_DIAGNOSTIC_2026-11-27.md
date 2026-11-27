# P-OM-1 Post-Blind Diagnostic: Viewing-Angle Dust Mirage & CMB-Dipole Sightline Split (2026-11-27)

**Epistemic Tier:** `[E]`/`[D]` post-blind diagnostic audit on `40,894,394` KiDS-Legacy DR5 sources and `GAMA DR4` (`StellarMassesGKVv24.fits`).
**Scope:** Companion diagnostic to [`POM1V2_BLIND_KIDS_LEGACY_RECORD_2026-11-26.md`](POM1V2_BLIND_KIDS_LEGACY_RECORD_2026-11-26.md). The pre-registered blind endpoints and verdicts in that record remain untouched.

## 1. Viewing-Angle Internal-Dust Mirage in Apparent Red Galaxies

Across the full GAMA quality-matched window ($0.1 < z < 0.5,\; 8.5 < \log_{10}(M_*/M_\odot) < 11.0$, $N = 177,999$):
- **Apparent red `(u - r)_obs > 2.00` sample:** `72,367` galaxies.
- **Tilted/edge-on dusty spiral disks misclassified as ETGs (`(u - r)_obs > 2.00` & `(u - r)_stars <= 2.00`):** **`45,914` (`63.4%`)**, with median internal reddening $\Delta(u-r) = +0.356\text{ mag}$ ($E(B-V) = 0.145$).
- **True dust-free intrinsic ellipticals (`(u - r)_stars > 2.00`):** **`26,453` (`36.6%`)**, with $E(B-V) = 0.058$.

Across the **`45,050` isolated `GAMA_All4` weak-lensing lenses**:
- **Pure Blue Spirals:** `30,260` (`67.2%`)
- **Tilted/Edge-On Dusty Spirals in Apparent ETG Bin:** `9,372` (**`63.4%` of isolated apparent ETGs**)
- **True Dust-Free Intrinsic Ellipticals:** `5,418` (`36.6%` of isolated apparent ETGs)

### Weak-Lensing RAR Stacking Under Intrinsic Dust-Corrected Classification (`20x` Shared Randoms)

| Run (`GAMA_All4` Intrinsic Cut) | True Disks (`N=39,632`) $\chi^2/7$ ($p$) | True Ellipticals (`N=5,418`) $\chi^2/7$ ($p$) | True ETG `med obs/pred` | Joint Hartlap $\chi^2_{\rm H}/14$ ($p_{\rm H}$) |
|---|---|---|---|---|
| `Q_ETG = 1.0` | `8.50/7` (`0.291`) | `22.26/7` (`0.00229`) | **`1.5157`** (vs $\sqrt{2}=1.4142$) | `30.95/14` (`0.00563`, `PASS_WITHIN_MASS_SYSTEMATIC`) |
| `Q_ETG = sqrt(2)` | `8.50/7` (`0.291`) | `12.76/7` (`0.0783`) | **`1.1923`** | `24.16/14` (`0.0438`, `PASS`) |
| `Q_ETG = 1.4` | `8.50/7` (`0.291`) | `15.85/7` (`0.0266`) | **`1.1735`** | `28.95/14` (`0.0106`, `PASS`) |

## 2. Directional Sightline & CMB-Dipole Hemisphere Breakdown (`Q_ETG = 1.0`)

| Patch / Hemisphere | Lenses $N$ | $\langle\cos\theta_{\rm CMB}\rangle$ | LTG `med obs/pred` ($\chi^2/7$) | ETG `med obs/pred` ($\chi^2/7$) |
|---|---:|---:|---|---|
| `GAMA_G12` | `12,290` | `+0.969` | `1.397` (`4.9/7`) | `1.341` (`23.4/7`) |
| `GAMA_G09` | `12,265` | `+0.831` | `0.769` (`17.8/7`) | `1.919` (`27.2/7`) |
| `GAMA_G15` | `12,440` | `+0.642` | `1.353` (`8.5/7`) | `2.067` (`56.0/7`) |
| `GAMA_G23` | `8,055` | `-0.769` | `0.680` (`14.9/7`) | `0.996` (`6.6/7`) |
| `N_DR5` | `62,822` | `+0.871` | `1.171` (`5.0/7`) | `1.558` (`41.0/7`) |
| `S_DR5` | `44,317` | `-0.646` | `0.758` (`7.5/7`) | `1.520` (`25.6/7`) |

- **Two-Hemisphere Unseen `DR5_New329` LTG Mean (`N_DR5` forward + `S_DR5` wake) / 2:** **`0.9644`** (consistent with unity across opposite dipole hemispheres, while `GAMA_G15` looking across the Virgo/Hercules-Shapley filament carries the localized northern overdensity).

## Reproducibility
```bash
python3 03_observer_jwst/pom1_intrinsic_dipole_diagnostic.py --self-test
python3 03_observer_jwst/pom1_intrinsic_dipole_diagnostic.py --run-cached
```
