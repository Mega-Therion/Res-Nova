# Multi-Probe CMB-Dipole Hemisphere Cross-Check: KiDS-Legacy Weak Lensing + Pantheon+ SNe Ia (2026-11-27)

**Epistemic Tier:** `[E]`/`[D]` multi-probe directional synthesis across two independent datasets (`107,139` unseen KiDS-Legacy DR5 lenses / `40.9M` shear sources + `1,590` Pantheon+ Type Ia supernovae). Physical wake/foreground attribution remains `[O]`.

## 1. Side-by-Side Forward-Apex vs. Backward-Wake Comparison (`RA = 167.94 deg, Dec = -6.94 deg`)

| Independent Probe | Sample Size | Forward Dipole Hemisphere (`cos theta_CMB > 0`) | Backward Wake Hemisphere (`cos theta_CMB < 0`) | Two-Hemisphere Unweighted Mean |
|---|---:|---|---|---|
| **KiDS-Legacy `DR5_New329` LTG Weak Lensing** (`obs / pred`) | `107,139` lenses (`40.9M` sources) | **`1.1711`** (`N_DR5`, $\langle\cos\theta\rangle = +0.871$) | **`0.7577`** (`S_DR5`, $\langle\cos\theta\rangle = -0.646$) | **`0.9644`** |
| **Pantheon+ SNe Ia Ceiling Share** ($\Omega_f^{\rm best}$) | `1,590` SNe (`STAT+SYS`) | **`0.9960`** (`1sigma: [0.968, 0.996]`) | **`0.9320`** (`1sigma: [0.908, 0.96]`) | **`0.9640`** |

- **Cross-probe directional concordance (`[E]`/`[D]`):** Both independent observables exhibit higher apparent amplitude toward the CMB dipole / Virgo–Shapley hemisphere and lower amplitude in the southern Sculptor-Void wake (`+2.17 sigma` in Pantheon+ $\Omega_f$, `+21.4%` modulation in weak lensing), while **canceling across opposite hemispheres to `0.9644` and `0.9640`** (`|\Delta| = 0.0004`).
- **Isotropic control (`[D]`):** Standard flat-$\Lambda$CDM $\Omega_m$ differs by only `0.74 sigma` across the CMB dipole and `0.22 sigma` across the Galactic Centre.

## Reproducibility
```bash
python3 04_cosmology/dipole_multiprobe_crosscheck.py --self-test
python3 04_cosmology/dipole_multiprobe_crosscheck.py --run
```
