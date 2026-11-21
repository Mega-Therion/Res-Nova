# Two-Domain X-COP Hydrostatic-Core ($r \le R_{500}$) BVP & Expansion-Scalar Rule Audit

> **SCOPE NOTICE (2026-11-21):** The extragalactic X-COP cluster results and symbolic expansion-scalar math below stand as recorded; per [`../../02_galaxy_dynamics/GALAXY_LAW_SCOPE_2026-11-21.md`](../../02_galaxy_dynamics/GALAXY_LAW_SCOPE_2026-11-21.md) and [`../../OUTSIDE_GALAXIES.md`](../../OUTSIDE_GALAXIES.md) (Erratum `E-16`), ordinary GR holds outside galaxies and any Cassini $Q_2$ comparison line is an out-of-domain extrapolation check, not a gate on the galaxy law `μ_std`.

- **Date:** 2026-11-21
- **Script:** `audits/2026-11-21/nested_holographic_boundary_inheritance.py` (exit 0)
- **Receipt:** `audits/2026-11-21/NESTED_HOLOGRAPHIC_BOUNDARY_INHERITANCE.json`

---

## 1. What This Run Computes (`DOP853` Two-Domain X-COP BVP)

For each of the 12 X-COP clusters and 3 measured ICM density models (`M1_stacked_measured` from Ghirardini+19 Table 5, `M2_vikhlinin_CCNCC` from Ghirardini+19 Table 3, and `M3_per_cluster_exact_vikhlinin` matching Eckert+19 Table 2 $M_{\mathrm{gas}}(R_{500})$ and $M_{\mathrm{gas}}(R_{200})$), we solve the two-segment BVP with outer virial potential boundary $\Phi(r_v) = 0$ at $r_v = R_{200}(200/177.8)^{1/3}$, universal $\mu_0 = 1/(0.9895\,\mathrm{Mpc})$, and cosmic dust cap $5.36\,M_b(r_v)$:
- **Hydrostatic core ($r \le R_{500}$):**
  $$\frac{dW}{dr} = G\,\frac{dM_b}{dr} - \mu_0^2 r^2 \Phi(r), \qquad \frac{d\Phi}{dr} = g_{\mathrm{MOND}}\!\left(\frac{W}{r^2}\right).$$
- **Outer infall shell ($R_{500} < r \le r_v$):**
  $$\frac{dW}{dr} = G\,\frac{dM_b}{dr} \quad (\text{no new hydrostatic dust added outside } R_{500}), \qquad \frac{d\Phi}{dr} = g_{\mathrm{MOND}}\!\left(\frac{W}{r^2}\right).$$

### Summary Across All 12 X-COP Clusters (and Direct-11 Excluding `A3266`)

| Measured X-COP ICM Model | Median $R_{500}$ | Median $R_{200}$ | In `[0.80, 1.25]` ($R_{500}$ / $R_{200}$ / Both) | In `[0.70, 1.40]` ($R_{500}$ / $R_{200}$) | Direct-11 Median ($R_{500}$ / $R_{200}$) | Direct-11 in `[0.80, 1.25]` ($R_{500}$ / $R_{200}$) | Max Dust / Cosmic Cap | Budget Caps |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`M1_stacked_measured`** | **`0.8685`** | **`0.8533`** | `9/12` / `9/12` / `8/12` | `12/12` / `12/12` | `0.8692` / `0.8537` | `9/11` / `9/11` | `0.5591` | `0/12` |
| **`M2_vikhlinin_CCNCC`** | **`0.8692`** | **`0.8546`** | `9/12` / `9/12` / `8/12` | `12/12` / `12/12` | `0.8702` / `0.8570` | `9/11` / `9/11` | `0.5489` | `0/12` |
| **`M3_per_cluster_exact_vikhlinin`** | **`0.8669`** | **`0.8560`** | `9/12` / `9/12` / `8/12` | `12/12` / `12/12` | `0.8671` / `0.8567` | `9/11` / `9/11` | `0.6786` | `0/12` |

- **Medians:** All medians at both $R_{500}$ (`0.8669–0.8692`) and $R_{200}$ (`0.8533–0.8560`) pass `[0.80, 1.25]`, with $\mu_{\mathrm{eff}}/\mu_0 = 1.0000$ for every cluster and a maximum core-dust ratio of `0.6786` (`0/12` budget caps triggered).
- **Four clusters outside `[0.80, 1.25]` in all three ICM models:**
  1. **`A2029`:** $R_{500} = 0.7757\text{--}0.7768$, $R_{200} = 0.7552\text{--}0.7613$ (both below `0.80`).
  2. **`A2319`:** $R_{500} = 1.1452\text{--}1.1477$ (inside `[0.80, 1.25]`), $R_{200} = 1.2806\text{--}1.3072$ (above `1.25`).
  3. **`A3266`:** $R_{500} = 0.7102\text{--}0.7137$, $R_{200} = 0.7213\text{--}0.7428$ (both below `0.80`).
  4. **`ZwCl1215`:** $R_{500} = 0.7907\text{--}0.7935$ (below `0.80`), $R_{200} = 0.8312\text{--}0.8494$ (inside `[0.80, 1.25]`).

### Per-Cluster Table (`M3_per_cluster_exact_vikhlinin`)

| Cluster | $R_{500}$ | In `[0.80, 1.25]` ($R_{500}$) | $R_{200}$ | In `[0.80, 1.25]` ($R_{200}$) | Core Dust / Cosmic Cap | $\mu_{\mathrm{eff}}/\mu_0$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `A1644` | `0.8671` | `True` | `0.8866` | `True` | `0.2491` | `1.0000` |
| `A1795` | `0.9138` | `True` | `0.8233` | `True` | `0.3016` | `1.0000` |
| `A2029` | `0.7768` | **`False`** | `0.7613` | **`False`** | `0.5017` | `1.0000` |
| `A2142` | `0.8495` | `True` | `0.8554` | `True` | `0.4467` | `1.0000` |
| `A2255` | `0.8625` | `True` | `0.8817` | `True` | `0.2987` | `1.0000` |
| `A2319` | `1.1452` | `True` | `1.2806` | **`False`** | `0.2954` | `1.0000` |
| `A3158` | `0.9138` | `True` | `0.8880` | `True` | `0.2579` | `1.0000` |
| `A3266` | `0.7137` | **`False`** | `0.7428` | **`False`** | `0.6786` | `1.0000` |
| `A644` | `0.9401` | `True` | `0.8514` | `True` | `0.3617` | `1.0000` |
| `A85` | `0.8941` | `True` | `0.8567` | `True` | `0.3265` | `1.0000` |
| `RXC1825` | `0.8668` | `True` | `0.9022` | `True` | `0.2425` | `1.0000` |
| `ZwCl1215` | `0.7935` | **`False`** | `0.8494` | `True` | `0.6425` | `1.0000` |

---

## 2. Scope & Limitations of the Expansion-Scalar Rule $a_{\mathrm{hor}} := c\,\theta/(6\pi)$

1. **What SymPy checks:** Evaluating $a_{\mathrm{hor}} = c\,\theta/(6\pi)$ at $\theta = 3H_0$ gives $a_0 = cH_0/(2\pi)$, and taking $\theta \to 0^+$ gives $\lim_{a_{\mathrm{hor}}\to 0^+}\nu_{\mathrm{std}}(g_N/a_{\mathrm{hor}}) = 1$.
2. **Why Level 3 ($\theta = 0$) does NOT resolve the Cassini EFE quadrupole:**
   - Setting $\theta = 0$ inside a stationary galactic disk defines the internal solar MOND term to zero by hypothesis.
   - The Newtonian Milky Way tidal gradient $v_{\mathrm{circ,MW}}^2/R_\odot^2 = 7.560\times 10^{-31}\,\mathrm{s}^{-2}$ is only the smooth background tide of the galaxy; it is **not** the Cassini quadrupole measurement.
   - The measurement that failed (`Q_2 = 15.40–19.89e-27 s^-2` vs. the `5.2e-27 s^-2` cap) is the solar quadrupole induced by the galactic external acceleration $g_e = |\nabla\Phi_{\mathrm{MW}}| \approx 1.9\times 10^{-10}\,\mathrm{m/s^2}$, which remains present in a stationary disk even when $\theta = \nabla_\mu A^\mu = 0$.
3. **What is not recomputed in this run:**
   - The 175 SPARC rotation curves and the 626-bin Planck `plik_lite` + DESI DR2 BAO forecast are existing results from their own receipts, not fits performed by this script.
