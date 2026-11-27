# Multi-Tier Evaluation of the 3D Phase-Space Dispersion Quadrature Law $Q_{\rm 3D}(V_{\rm rot}/\sigma_0)$ (2026-11-27)

**Epistemic Tier:** `[P]` algebraic bounds & endpoint theorems in [`05_lean_formalization/DispersionQuadrature.lean`](../05_lean_formalization/DispersionQuadrature.lean); `[D]`/`[E]` evaluation on `RC100` ($N=100$), `JWST MSA-3D` ($N=20$), and `GAMA/KiDS-Legacy` ($N=45,050$) with no per-galaxy fitted parameters; `[O]` physical covariant Jeans / effective baryon coupling identification.

## 1. Closed-Form Law & Exact Endpoints (Fixed Phase-Space DoF Ratio: $1$ Azimuthal vs. $3$ Dispersion)

$$Q_{\rm 3D}(\xi) = \sqrt{1 + \frac{3}{\xi^2 + 3}} = \sqrt{\frac{\xi^2 + 6}{\xi^2 + 3}}, \qquad \xi \equiv \frac{V_{\rm rot}}{\sigma_0} \in [0, \infty)$$

| Physical Regime | $\xi = V_{\rm rot}/\sigma_0$ | $Q_{\rm 3D}(\xi)$ | $Q_{\rm 3D}^2(\xi)$ | Observational Anchor |
|---|---:|---:|---:|---|
| Ultra-cold thin spiral (`SPARC` high-$V$) | `15.0000` | **`1.0066`** | `1.0132` | — |
| Cold spiral disk (`SPARC` typical) | `12.0000` | **`1.0102`** | `1.0204` | — |
| Cold disk `<1.5%` Lean enclosure (`Theorem 10`) | `10.0000` | **`1.0145`** | `1.0291` | — |
| Warm spiral disk | `8.0000` | **`1.0221`** | `1.0448` | — |
| Exact equipartition midpoint (`Theorem 9`, $V^2 = 3\sigma_0^2$) | `1.7321` | **`1.2247`** | `1.5000` | — |
| Pure dispersion sphere (`Theorem 7`, `GAMA` true ETGs) | `0.0000` | **`1.4142`** | `2.0000` | — |

## 2. Per-Galaxy Kinematic Evaluation (`RC100` $N=100$ & `JWST MSA-3D` $N=20$, Fixed Static $a_0$)

Both constitutive prescriptions are reported side-by-side without selection bias:
- **Prescription I (`g_MOND(Q_3D(xi) * g_bar; a0)` `[O]`):** Effective baryon coupling (identical in form to weak-lensing `Q_ETG`).
- **Prescription II (`Q_3D(xi)^2 * g_MOND(g_bar; a0)` `[O]`):** Direct 3D phase-space virial trace projection.

| Sample | $N$ | Med $V_{\rm rot}/\sigma_0$ (IQR) | Med $Q_{\rm 3D}(\xi_i)$ | Thin-Disk `Q=1` `med g_obs/g_pred` (`<z^2>`) | Presc. I `g_MOND(Q_3D g_bar)` `med` (`<z^2>`) | Presc. II `Q_3D^2 g_MOND(g_bar)` `med` (`<z^2>`) |
|---|---:|---:|---:|---|---|---|
| `RC100 (z = 0.60--2.53)` | `100` | `4.54` (`3.13–6.86`) | **`1.0617`** | `1.375x` (`0.47`) | `1.335x` (`0.44`) | **`1.155x` (`0.45`)** |
| `JWST MSA-3D (z = 0.58--1.57)` | `20` | `2.83` (`2.17–3.92`) | **`1.1280`** | `2.040x` (`1.03`) | `1.877x` (`0.90`) | **`1.534x` (`0.67`)** |

## 3. Exact $\xi \to 0$ Endpoint Match on `GAMA DR4 / KiDS-Legacy DR5` Weak Lensing (`40.9M` Sources)

- For dispersion-supported intrinsic ellipticals ($\xi = V_{\rm rot}/\sigma_0 \to 0$, $N = 5,418$ isolated lenses), $Q_{\rm 3D}(0) = \sqrt{2} = 1.414214$ reduces ETG weak-lensing $\chi^2/\mathrm{ndof}$ from `22.256/7` ($p = 0.00229$) to **`12.757/7` ($p = 0.0783$)**, achieving a joint Hartlap **`PASS`** ($p_{\rm H} = 0.0438$) while leaving cold spirals ($N = 39,632$) invariant.

## Reproducibility
```bash
/home/mega/.elan/bin/lean 05_lean_formalization/DispersionQuadrature.lean
python3 02_galaxy_dynamics/dispersion_quadrature_audit.py --self-test
python3 02_galaxy_dynamics/dispersion_quadrature_audit.py --run
```
