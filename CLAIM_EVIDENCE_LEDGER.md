# 📋 Claim-to-Evidence Ledger: Grand Monograph Assessment

**Evaluation Standard:** NEWTON ARCHITECT Protocol & Sovereign Epistemic Covenant  
**Target Repository:** `/home/mega/grand_monograph/`  
**Evaluation Date:** 2026-08-14  

---

| ID | Exact Manuscript Claim | Epistemic Status | Mechanical / Empirical Evidence | Physical Limits & Boundaries |
| :--- | :--- | :---: | :--- | :--- |
| **CLM-01** | $\mathcal{F}(x) = x \ln(x + \sqrt{1+x^2}) - \sqrt{1+x^2}$ differentiates directly to $\operatorname{arcsinh}(x)$. | **[P] Proved** | Direct SymPy derivation & algebraic calculus identities. | Mathematical calculus statement; does not prove uniqueness of Lagrangian. |
| **CLM-02** | Transition from $\operatorname{arcsinh}(x)$ to $\mu_{\text{simple}}(x) = \frac{x}{\sqrt{1+x^2}}$ via disk planar balance. | **[O] Open** | Formalization in `MuProjection.lean` verifies properties of $\mu_{\text{simple}}(x)$ once defined. | The variational necessity or physical derivation from the action is unproved. |
| **CLM-03** | Dimensional horizon temperature matching $T_U = T_{\text{GH}}$ yields $a = cH_0$. | **[P] Proved** | Gibbons--Hawking (1977) $T_{\text{GH}}=\frac{\hbar H_0}{2\pi k_B}$ vs Unruh (1976) $T_U=\frac{\hbar a}{2\pi c k_B}$. | $2\pi$ KMS factors cancel; the $1/(2\pi)$ divisor in $a_0 = \frac{cH_0}{2\pi}$ is an open boundary normalization. |
| **CLM-04** | SPARC Strict Zero-Parameter Fit: Median $\chi^2_{\text{data}}/N_g = 29.12$, Aggregate $\sum\chi^2_{\text{data}}/\text{dof} = 144.04$. | **[D] Computed** | `sparc_reproduce.py` on 175 SPARC galaxies (3,391 data points, SHA-256: `e76e6752164b...`). | Outperforms baryons-only controls, but remains a poor absolute fit across uncurated data. |
| **CLM-05** | SPARC Canonical Nuisance Fit: Median $\chi^2_{\text{data}}/N_g = 2.88$, Aggregate $\sum\chi^2_{\text{data}}/\text{dof}_{\text{nom}} = 7.93$. | **[D] Computed** | MAP optimization ($N_{\text{par}}=382$, nominal $\text{dof}=3,009$, $\sum\chi^2_{\text{data}}=23,863.78$, $\sum\chi^2_{\text{prior}}=1,559.38$). | In-sample performance with nominal degrees of freedom; priors excluded from displayed data-residual numerator. |
| **CLM-06** | Baryons-Only Unit $M/L$ Control: Median $\chi^2_{\text{data}}/N_g = 51.58$, Aggregate $\sum\chi^2_{\text{data}}/\text{dof} = 204.65$. | **[D] Computed** | Fixed unit prescription $\Upsilon_{\text{disk}}=1.0, \Upsilon_{\text{bulge}}=1.0$ across 3,391 data points. | Poor absolute fit under this fixed prescription. |
| **CLM-07** | Baryons-Only Standard SPARC Control: Median $\chi^2_{\text{data}}/N_g = 85.23$, Aggregate $\sum\chi^2_{\text{data}}/\text{dof} = 406.49$. | **[D] Computed** | Fixed standard prescription $\Upsilon_{\text{disk}}=0.5, \Upsilon_{\text{bulge}}=0.7$ across 3,391 data points. | Poor absolute fit under this fixed prescription. |
| **CLM-08** | Lean 4 Modules (`SOCasimirGenuine.lean` through `SovereignRegularity.lean`) compile with exit code 0. | **[P] Proved** | `LEAN_BUILD_RAW.json` confirms clean build and axiom chains depending only on `[propext, Classical.choice, Quot.sound]`. | Proves only mathematical consistency of definitions and theorems; does not prove physical theory selection. |
| **CLM-09** | Optical Metric, Redshift Jacobian, and Luminosity Modulation couplings. | **[O] Open** | Phenomenological formulas posited for observational matching. | Covariant Maxwell/null-geodesic derivations and cosmological perturbation tests remain open. |
