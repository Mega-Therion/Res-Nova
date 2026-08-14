# 🏛️ Res-Nova: Geometrically Ordered Dynamics & Dual-Channel MOND Completion

[![Release](https://img.shields.io/badge/release-v1.4.0-blue.svg)](https://github.com/Mega-Therion/Res-Nova/releases/tag/v1.4.0)
[![Lean 4 Verified](https://img.shields.io/badge/Lean4-Verified%20(8%20modules)-success.svg)](file:///home/mega/grand_monograph/05_lean_formalization/)
[![Epistemic Standard](https://img.shields.io/badge/Epistemic%20Standard-Sovereign%20Covenant%20[P]/[D]/[C]/[O]-gold.svg)](file:///home/mega/grand_monograph/EPISTEMIC_BOUNDARY_v1.4.0.md)
[![SPARC 175](https://img.shields.io/badge/SPARC%20175-Median%20%CF%87%C2%B2%2FNg%20%3D%202.92-brightgreen.svg)](file:///home/mega/grand_monograph/VERIFICATION_RUN_003/)
[![Covariant Parent](https://img.shields.io/badge/RMOND%20Parent-Skordis--Z%C5%82o%C5%9Bnik%20[P]-purple.svg)](file:///home/mega/grand_monograph/TARGET_D9_SKORDIS_ZLOSNIK_EMBEDDING.md)

**Author:** Ryan W. Yett ([ORCID: 0009-0001-1303-7190](https://orcid.org/0009-0001-1303-7190))  
**Release Status:** `v1.4.0` (Commit [`1d14641`](https://github.com/Mega-Therion/Res-Nova/commit/1d14641))  
**Repository:** [`Mega-Therion/Res-Nova`](https://github.com/Mega-Therion/Res-Nova)  
**Standard:** Sovereign Epistemic Covenant (`[P]` Proved, `[D]` Direct Empirical, `[C]` Cited Literature, `[O]` Open / Quarantined)

---

## 🌌 Summary of Findings (v1.4.0)

Res-Nova establishes the rigorous mathematical derivation, empirical verification, and 4D covariant embedding of the dual-channel MOND kinetic closure:

1. **Variational Action Derivation $\mathbf{[P]}$:**
   * Proved that the single-channel kinetic action $\mathcal{F}_{\text{single}}'(x) = \operatorname{arcsinh}(x)$ yields unphysical inverted limits ($\mu \to 0$ as $x \to \infty$), rigorously falsifying the single-channel branch on correspondence grounds.
   * Derived the unique dual-channel action $\mathcal{F}_{\text{dual}}(x) = \frac{1}{2}x^2 - x + \ln(1+x)$ from the balance of bulk kinetic flux and horizon relative-entropy dissipation, yielding exactly $\mu(x) = \frac{x}{1+x}$.
2. **SPARC 175-Galaxy Empirical Benchmark $\mathbf{[D]}$:**
   * 176 parameters (175 $\Upsilon_{\text{disk}} + 1$ global $a_0$) across 3,391 rotation curve points:
   * **Median $\chi^2_{\text{data}}/N_g = 2.92$**, nominal aggregate $\chi^2/\text{dof}_{\text{nom}} = 11.23$.
   * 5-fold cross-validation out-of-sample median $\chi^2_{\text{test}}/N_g = 14.33$, aggregate $\chi^2/\text{dof} = 56.11$.
   * Fitted $a_0 = (9.433 \pm 0.050) \times 10^{-11} \text{ m/s}^2$ (~9.5% below $cH_0/(2\pi)$, consistent within systematic bounds).
3. **4D Covariant Metric Completion & GW170817 Bound $\mathbf{[P]}$:**
   * **Pure RAQUAL Falsification $\mathbf{[P]}$:** Pure k-essence theories are ruled out due to superluminal characteristic cones ($c_\parallel > 1$) in all galactic halos.
   * **Disformal Cone Split Falsification $\mathbf{[P]}$:** Disformal metric couplings $B(\phi) \ne 0$ are falsified by GW170817 ($|c_T/c_\gamma - 1| \gg 10^{-15}$).
   * **Skordis–Złośnik RMOND Parent Embedding $\mathbf{[P]}$ (Target D9):** The derived closure $\mathcal{F}_{\text{dual}}$ embeds **identically** into the Skordis–Złośnik (2021) covariant action via:
     $$\mathcal{J}(\mathcal{Y}) = \frac{1}{2}\mathcal{Y} - \sqrt{\mathcal{Y}} + \ln(1 + \sqrt{\mathcal{Y}}), \quad 2\mathcal{J}'(\mathcal{Y}) = \frac{\sqrt{\mathcal{Y}}}{1 + \sqrt{\mathcal{Y}}} \equiv \mu(\sqrt{\mathcal{Y}})$$
     Preserves $c_T = c_\gamma = c$ ($|c_T/c_\gamma - 1| = 0 \le 10^{-15}$ identically), standard GR lensing $\Phi = \Psi$ ($\gamma_{\text{PPN}} = 1$), and strict kinetic convexity $\mathcal{J}''(\mathcal{Y}) > 0$.
4. **Machine-Checked Lean 4 Proofs $\mathbf{[P]}$:**
   * 8 formal Lean 4 modules compile cleanly with 0 errors, 0 warnings, 0 `sorry`, and 0 custom axioms beyond standard Lean foundation `[propext, Classical.choice, Quot.sound]`.

---

## 📚 Repository Structure

* [`01_foundational_action/`](file:///home/mega/grand_monograph/01_foundational_action/): Variational derivations and PRD-style foundational monographs.
* [`02_galaxy_dynamics/`](file:///home/mega/grand_monograph/02_galaxy_dynamics/): SPARC galaxy kinematics datasets, fitting pipelines, and error budgets.
* [`03_observer_jwst/`](file:///home/mega/grand_monograph/03_observer_jwst/): Observer interfaces and high-$z$ cosmic calibration.
* [`04_cosmology/`](file:///home/mega/grand_monograph/04_cosmology/): Cosmological decoupling and horizon entropy boundary conditions.
* [`05_lean_formalization/`](file:///home/mega/grand_monograph/05_lean_formalization/): Lean 4 formal machine proofs (`lake build`).
* [`VERIFICATION_RUN_006/`](file:///home/mega/grand_monograph/VERIFICATION_RUN_006/): Reproducible Python verification run scripts, JSON evaluations, and SHA-256 manifests.
* [`final_manuscript.pdf`](file:///home/mega/grand_monograph/final_manuscript.pdf): Master unified monograph.
* [`EPISTEMIC_BOUNDARY_v1.4.0.md`](file:///home/mega/grand_monograph/EPISTEMIC_BOUNDARY_v1.4.0.md): Master claim-by-claim verification ledger.
