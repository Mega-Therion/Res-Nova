# Gate 2 Audit: D10 X-COP Clusters on Measured Outer ICM Profiles to $R_{200}$ (`2026-11-21`)

- **Script:** [gate2_xcop_measured_icm.py](gate2_xcop_measured_icm.py)
- **Receipt:** [GATE2_XCOP_MEASURED_ICM.json](GATE2_XCOP_MEASURED_ICM.json)
- **Verdict:** **D10 unscreened hydrostatic AeST dust cluster route is `[X]` (KILLED).**

---

## 1. Strict Seat & Data Provenance

- **Unscreened live single-metric AeST only:** `S(r) == 1` everywhere (no $x_H$ / tidal screen, no Cassini screen), quadratic AeST dust $-\mu_0^2 r^2 \Phi$ (no Cosh concentration), single metric ($\Psi = \Phi$), universal $\mu_0 = 1 / (0.9895\,\mathrm{Mpc})$, cosmic dust allowance $5.36\,M_b(r_v)$, canonical $\mu_{\mathrm{std}}$.
- **Published X-COP ICM radial data:**
  - Global radii & masses: Ettori et al. 2019 (A&A 621, A39, `arXiv:1805.00035`) + Eckert et al. 2019 (A&A 621, A40, `arXiv:1805.00034` Table 2; direct $R_{200}$ gas measurement for 11/12 clusters, `A3266` excluded in `direct11` check).
  - Radial ICM electron density to $1.899\,R_{500}$: Ghirardini et al. 2019 (A&A 621, A41, `arXiv:1805.00042`), **Table 5** (`tab:stack`, 49 radial bins from `0.01058` to `1.899 R500`, median + 68% envelope), **Table 1** (CC/NCC classification: `A1644`, `A1795`, `A2029`, `A85` CC; remaining 8 NCC), and **Table 3** (`eq:vikh_density`, $\gamma = 3$ Vikhlinin density parameters; verified to `2–6%` against Table 5 that `log()` is natural log).

---

## 2. Unscreened Live AeST Results Across Measured ICM Models (`[D]` / `[X]`)

Pre-registered criteria ([PREREG.md](PREREG.md)): $0.80 \le \mathrm{median}(R) \le 1.25$ and $\ge 9/12$ (or $\ge 8/11$ for direct-$R_{200}$) in $[0.7, 1.4]$ at **both** $R_{500}$ and $R_{200}$. Here $R_\Delta \equiv M_{\mathrm{tot},\Delta} / M_{\mathrm{dyn}}(\Delta)$.

| Baryon Profile Model | Solver | All 12 $R_{500}$ (in $[0.7,1.4]$) | All 12 $R_{200}$ (in $[0.7,1.4]$) | Direct-11 $R_{500}$ | Direct-11 $R_{200}$ | Verdict |
|---|---|---:|---:|---:|---:|---|
| `M0_beta_control` (2-pt $\beta$ control) | `static_rv` | `0.7960` (`9/12`) | `0.6021` (`1/12`) | — | — | FAILS |
| `M0_beta_control` (`XCOP_RESULT.json` match) | `capped_mu_rv` | `0.8323` (`12/12`) | `0.6196` (`1/12`) | `0.8172` (`11/11`) | `0.6164` (`1/11`) | FAILS (`R200`) |
| `M1_stacked_measured` (Ghirardini+19 Tab. 5 med) | `static_rv` | `0.7980` (`9/12`) | `0.6048` (`1/12`) | — | — | FAILS (`R200`) |
| `M1_stacked_measured` | `capped_mu_rv` | `0.8143` (`12/12`) | **`0.6083`** (`1/12`) | `0.8181` (`11/11`) | **`0.6087`** (`1/11`) | **`[X]` FAILS (`R200`)** |
| `M1_stacked_measured` | `free_boundary` | `0.7993` (`12/12`) | **`0.6083`** (`1/12`) | `0.8105` (`11/11`) | **`0.6087`** (`1/11`) | **`[X]` FAILS (`R200`)** |
| `M1_stacked_low` / `M1_stacked_high` (68% env.) | `capped_mu_rv` | `0.8152` / `0.8137` (`12/12`) | `0.6097` / `0.6067` (`1/12`) | `0.8190` / `0.8175` | `0.6102` / `0.6071` (`1/11`) | **`[X]` FAILS (`R200`)** |
| `M2_vikhlinin_CCNCC` (Tab. 3 CC/NCC) | `capped_mu_rv` | `0.8148` (`12/12`) | **`0.6104`** (`1/12`) | `0.8188` (`11/11`) | **`0.6109`** (`1/11`) | **`[X]` FAILS (`R200`)** |
| `M2_vikhlinin_CCNCC` | `free_boundary` | `0.7985` (`12/12`) | **`0.6104`** (`1/12`) | `0.8108` (`11/11`) | **`0.6109`** (`1/11`) | **`[X]` FAILS (`R200`)** |
| **`M3_per_cluster_exact_vikhlinin`** (hits $M_{g500},M_{g200}$) | `static_rv` | `0.7967` (`9/12`) | **`0.6024`** (`1/12`) | — | — | **`[X]` FAILS (`R200`)** |
| **`M3_per_cluster_exact_vikhlinin`** | `capped_mu_rv` | **`0.8338`** (`12/12`) | **`0.6209`** (`1/12`) | `0.8187` (`11/11`) | **`0.6175`** (`1/11`) | **`[X]` FAILS (`R200`)** |
| **`M3_per_cluster_exact_vikhlinin`** | `free_boundary` | **`0.8141`** (`12/12`) | **`0.6197`** (`1/12`) | `0.8187` (`11/11`) | **`0.6175`** (`1/11`) | **`[X]` FAILS (`R200`)** |
| `M4a_eckert_fstar_concentrated` ($f_\star=0.015$, $c=5$) | `capped_mu_rv` | `0.8286` (`12/12`) | `0.6166` (`1/12`) | `0.8169` (`11/11`) | `0.6160` (`1/11`) | **`[X]` FAILS (`R200`)** |
| `M4b_gas_only_no_stars` ($f_\star = 0$) | `capped_mu_rv` | `0.8511` (`12/12`) | `0.6366` (`2/12`) | `0.8352` (`11/11`) | `0.6292` (`2/11`) | **`[X]` FAILS (`R200`)** |
| `M4c_hard_trunc_at_R200` ($\rho_b(r>R_{200})=0$) | `capped_mu_rv` | `0.8339` (`12/12`) | `0.6241` (`2/12`) | `0.8188` (`11/11`) | `0.6176` (`2/11`) | **`[X]` FAILS (`R200`)** |

- **Boundary diagnostic on `M3`:** Even setting the uncapped Dirichlet gauge boundary inward at $\Phi(R_{200}) = 0$ (zeroing dust density at $R_{200}$) leaves `med_R500 = 0.8381 (11/12)` and `med_R200 = 0.6583 (3/12)` — still failing $R_{200}$ by $\sim 34\%$!

---

## 3. Per-Cluster `M3_per_cluster_exact_vikhlinin` Breakdown

| Cluster | Type | Direct $R_{200}$ | $\epsilon_{\mathrm{fit}}$ | Outer $\frac{d\ln\rho_g}{d\ln r}(R_{200})$ | $M_b(r_v)/M_b(R_{500})$ | Capped $\mu$ ($R_{500}/R_{200}$) | Free-Boundary ($R_{500}/R_{200}$) |
|---|---|---:|---:|---:|---:|---:|---:|
| `A1644` | CC | Yes | `2.682` | `-2.465` | `1.9728` | `0.784 / 0.595` | `0.784 / 0.595` |
| `A1795` | CC | Yes | `6.591` | `-3.708` | `1.5002` | `0.856 / 0.618` | `0.856 / 0.618` |
| `A2029` | CC | Yes | `5.366` | `-3.297` | `1.5748` | `0.748 / 0.559` | `0.727 / 0.557` |
| `A2142` | NCC | Yes | `2.798` | `-2.492` | `1.6826` | `0.789 / 0.595` | `0.772 / 0.593` |
| `A2255` | NCC | Yes | `2.290` | `-2.265` | `1.9539` | `0.752 / 0.552` | `0.752 / 0.552` |
| `A2319` | NCC | Yes | `1.764` | `-1.999` | `1.8345` | `1.048 / 0.931` | `1.048 / 0.931` |
| `A3158` | NCC | Yes | `2.610` | `-2.405` | `1.7306` | `0.849 / 0.649` | `0.849 / 0.649` |
| `A3266` | NCC | No | `4.680` | `-3.396` | `1.4358` | `0.851 / 0.624` | `0.757 / 0.622` |
| `A644` | NCC | Yes | `3.849` | `-2.977` | `1.4689` | `0.875 / 0.633` | `0.875 / 0.633` |
| `A85` | CC | Yes | `4.618` | `-3.070` | `1.6493` | `0.819 / 0.610` | `0.819 / 0.610` |
| `RXC1825` | NCC | Yes | `2.001` | `-2.115` | `1.8398` | `0.810 / 0.672` | `0.810 / 0.672` |
| `ZwCl1215` | NCC | Yes | `4.081` | `-3.110` | `1.5146` | `0.914 / 0.700` | `0.826 / 0.697` |

### Conclusion (`[X]`)
Even with real measured X-COP radial ICM profiles out to $R_{200}$ (whose steep measured outer slopes reach `-2.0` to `-3.7`), and even under zero-star (`M4b`) or hard-truncated (`M4c`) lower bounds on outer baryons, unscreened live AeST reproduces $R_{500}$ (`0.814–0.851`, `12/12`) while persistently overshooting $R_{200}$ (`0.602–0.637`, only `1–2/12` in `[0.7, 1.4]`). The hydrostatic $n=1$ AeST dust halo set by $\mu_0^{-1} \approx 0.99\,\mathrm{Mpc}$ is intrinsically too extended at $R_{200}$, closing this D10 cluster route as **`[X]`**.
