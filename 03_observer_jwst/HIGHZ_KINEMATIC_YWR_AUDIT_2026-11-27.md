# High-$z$ Spatially Resolved Kinematic `YWR` Bore-Gauge Audit ($z = 0.58\text{--}7.43$, 2026-11-27)

**Epistemic Tier:** `[E]`/`[D]` deterministic evaluation across `125` spatially resolved high-$z$ galaxies (`RC100` $N=100$, `JWST/NIRSpec MSA-3D` $N=20$, `ALPINE-CRISTAL JWST+ALMA [C II]` $N=5$, plus `6` auxiliary `JADES G395H` galaxies `[O]`) with no per-galaxy fitted dark-matter halo parameters. The 3D turbulent/triaxial factor `Q_3D = sqrt(2)` is fenced as `[O]`.

## 1. `YWR` Surface-Density Monotonicity Across `125` High-$z$ Disks ($0.58 \le z \le 5.69$)

- **Global Spearman Rank Correlation between $y = g_{\rm bar}/a_0$ and $M_{\rm dyn,N}/M_{\rm bar} = g_{\rm obs}/g_{\rm bar}$:** **`r_s = -0.7683` (`p = 1.353e-25`)** — confirming that high-surface-brightness baryonic cores approach Newtonian unity while extended lower-surface-density disks climb monotonically.

| Surface-Density Tertile ($N=125$) | $N$ | Median $g_{\rm bar}/a_0$ | Observed Median $g_{\rm obs}/g_{\rm bar}$ | Static `Block 3` `Q=1` $\nu_{\rm std}(y)$ | Static `Block 3` `Q_3D=sqrt(2)` `[O]` |
|---|---:|---:|---:|---:|---:|
| Tertile 1 | `42` | `0.366` | **`3.493x`** | `1.812x` | **`2.235x`** |
| Tertile 2 | `41` | `1.395` | **`1.721x`** | `1.172x` | **`1.557x`** |
| Tertile 3 | `42` | `3.687` | **`1.195x`** | `1.034x` | **`1.439x`** |

## 2. Redshift Evolution ($z = 0.6 \to 5.7$) vs. 3D Turbulent Dispersion Geometry

| Resolved Sample | $N$ | Median $z$ ($E(z)$) | Median $V/\sigma_0$ | Model A (`Q=1` Static $a_0$) `med g_obs/g_pred` (RMS dex) | Model B ($a_0(z)\propto E(z)$) `med g_obs/g_pred` (RMS dex) | Model C (`Q_3D=sqrt(2)` Static $a_0$ `[O]`) `med g_obs/g_pred` (RMS dex) |
|---|---:|---:|---:|---|---|---|
| `RC100_z0p6_2p5` | `100` | `1.53` (`2.41`) | `4.89` | `1.375x` (`0.216`) | `1.081x` (`0.178`) | **`1.052x` (`0.183`)** |
| `JWST_MSA3D_z0p6_1p6` | `20` | `1.05` (`1.85`) | `2.83` | `2.040x` (`0.344`) | `1.648x` (`0.264`) | **`1.626x` (`0.274`)** |
| `JWST_ALMA_ALPINE_CRISTAL_z4p4_5p7` | `5` | `5.58` (`9.51`) | `IFU+ALMA` | `0.935x` (`0.296`) | `0.707x` (`0.213`) | **`0.666x` (`0.311`)** |

## Reproducibility
```bash
python3 03_observer_jwst/highz_kinematic_ywr_audit.py --self-test
python3 03_observer_jwst/highz_kinematic_ywr_audit.py --run
```
