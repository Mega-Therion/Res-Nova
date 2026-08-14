# 🌌 SPARC Claim Invalidation & Correction Ledger (Run 002)

**Audit Target:** All manuscripts, LaTeX sources, tables, and Markdown documentation in `/home/mega/grand_monograph/`  
**Protocol:** Zero Unsubstantiated Headline Toleration  

---

## 1. Retracted & Prohibited Legacy Statements

| Prohibited Legacy Formulation | File & Prior Location | Reason for Retraction | Replacement Audited Statement |
| :--- | :--- | :--- | :--- |
| *"Full 175-galaxy SPARC database accounting ... $\chi^2/\mathrm{dof} = 1.09$"* | `Res_Nova_Geometrically_Ordered_Dynamics_and_Information_Tension.tex` (Abstract L47 & Table 1 L215) | Empirically false for uncurated full sample without per-galaxy nuisance optimization. | **Strict zero-parameter:** median $\chi^2/N = 29.12$, aggregate $\chi^2/\mathrm{dof} = 144.04$.<br>**Nuisance mode (with priors):** median $\chi^2/N = 2.88$, aggregate $\chi^2/\mathrm{dof} = 7.93$. |
| *"All galaxies fit with zero parameters at $\chi^2/N \approx 1.07$"* | Legacy Notes & Summaries | Conflated curated regular disk subsets with the global un-filtered 175-galaxy SPARC database. | Citing $\chi^2/N = 1.07$ across all 175 galaxies is prohibited. |
| *"Horizon acceleration $a_0 = \frac{cH_0}{2\pi}$ yields $\chi^2 \approx 1.24$"* | `SPARC_PARAMETER_BUDGET.md` (Table 1) | Re-computed using exact SPARC $a_0$ grid sweeps. | Replaced by explicit Two-Tier benchmark table (Strict: median $29.12$ / Nuisance: median $2.88$). |

---

## 2. Definitive Two-Tier SPARC Benchmark Standard

All future monograph publications must explicitly distinguish between:

1. **Strict Zero-Parameter Tier (`[D]`)**:
   - Fixed universal scale $a_0 = \frac{cH_0}{2\pi} \approx 1.042 \times 10^{-10}\text{ m/s}^2$ ($H_0 = 67.4\text{ km/s/Mpc}$)
   - Unit stellar mass-to-light ratios $\Upsilon_{\text{disk}} = 1.0, \Upsilon_{\text{bulge}} = 1.0$
   - No distance adjustment ($f_d = 1.0$)
   - **Metrics:** $N=175$, $\text{DOF}=3,391$, **Median $\chi^2/N = 29.12$**, Aggregate $\chi^2/\text{dof} = 144.04$.

2. **Nuisance Parameter Optimization Tier (`[D]`)**:
   - Per-galaxy fit of $(\Upsilon_{\text{disk}}, \Upsilon_{\text{bulge}}, f_d)$ with SPARC standard Gaussian priors
   - **Metrics:** $N=175$, $\text{DOF}=2,977$, **Median $\chi^2/N = 2.88$**, Aggregate $\chi^2/\text{dof} = 7.93$.
