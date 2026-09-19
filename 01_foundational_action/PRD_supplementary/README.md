# PRD Letter Supplementary — Parameter-Free Derivation of MOND a0

Reproduces every number and figure in `../PRD_a0_geometric_derivation_Letter.md`.

## Inputs
- SPARC: `../../experiments/lab/calibration-engine/data/sparc_fortress.json`
  (VizieR J/AJ/152/157, Lelli+2016; 175 galaxies, 3389/3391 radial points)
- $a_0 = c \cdot H_0 / 2\pi$ with $H_0=67.4$ (Planck), $c$, $2\pi$ only. ZERO galaxy-fit parameters for the baseline YC.

## Run
    python rar_analysis.py      # → RAR_data.npz, model_comparison_BIC.json, figures/

## Key results (reproducible)

### 1. Zero-Parameter Baseline (Fixed M/L: $\Upsilon_{\rm disk}=0.5$, $\Upsilon_{\rm bulge}=0.7$)
- $a_0 = 1.042 \times 10^{-10}\,\mathrm{m\,s^{-2}}$ (13% off empirical MOND; 6% local $H_0$)
- RAR residual about parameter-free YC: median $+0.041$ dex, rms $0.324$ dex
- Full-curve reduced $\chi^2/N$: YC 88.6 vs MOND 83.6 vs baryonic 310 (all 0 free params)
- Per-galaxy acceptable (red. $\chi^2 < 5$): YC 73/175, MOND 64/175
- $\Delta$BIC vs $\Lambda$CDM (NFW, $\sim 270$ params): $+249$ favouring parameter-free YC

### 2. Marginalized M/L Regime (Fitted $\Upsilon \in [0.1, 2.0]$ per-galaxy)
- RAR residual about YC: median $-0.003$ dex, rms $0.233$ dex (very tight relation)
- Full-curve reduced $\chi^2/N$: YC 24.2 vs MOND 24.7 vs baryonic 74.9
- Per-galaxy acceptable (red. $\chi^2 < 5$): YC 121/175, MOND 117/175
- Under this regime, YC outperforms MOND by $\Delta\chi^2 = -1679$, leading to a $\Delta\mathrm{BIC} = +1679$ favoring YC (as the parameter space is identical).

## Figures Generated
- `figures/fig1_RAR.png`: Comparison of the Radial Acceleration Relation under fixed and optimized M/L.
- `figures/fig2_residuals.png`: Histogram of the residuals for YC and MOND in both regimes.
- `figures/fig3_example_curves.png`: Rotation curves for representative galaxies (NGC 3198, NGC 2403, DDO 154, UGC 2885).

## Honest caveats
- The 0.233 dex marginalized scatter is $\sim 2\times$ the literature RAR value ($\sim 0.11$ dex; McGaugh et al. 2016) because we keep distance and inclination fixed. The remaining scatter is the honest cost of not fitting distance and inclination parameters.
- Novelty is the DERIVATION of $a_0$, not the value ($a_0 \approx c H_0 / 2\pi$ coincidence is long noted).
- JWST formation NOT resolved (0/18).

---
## Relativistic Extension & Cosmological Perturbations

To fully supersede standard $\Lambda$CDM, the static framework is elevated to a full scalar-vector-tensor theory.
- `Cosmological_Perturbations.md`: Contains the explicit analytic derivation of the linear cosmological perturbation equations. Proves the WKB limit where the internal sound speed $\langle c_s^2 \rangle \approx 0$ (mimicking Cold Dark Matter pressureless collapse) and derives the disformal baryon potential $\Psi_{eff}$.
- `solve_background.py`: A Python script utilizing a stiff numerical ODE solver (Radau) to simulate the 13.8 billion-year cosmological background evolution of the Information Tension field. 
- `chi_evolution.png`: Proves dynamically that as Hubble friction scales the universe, the field rigorously settles to the geometric Stiefel manifold bound $\chi_0 \to 1/\sqrt{2}$, seeding the $a_0$ scale without fine-tuning.

---
## Lean 4 Formal Verification (Theorem Proving)

To ensure mathematical absolute rigor, the foundational axioms of the Stiefel manifold geometry and the derivation of the $1/\sqrt{2}$ coherence bound have been formally verified using the Lean 4 theorem prover. 
- `lean_proofs/YettParadigm.lean`: Formal Lean 4 code defining the Stiefel manifold constraints and formally proving the geometric bound.
- `lean_proofs/Q5_Formal_Bridge.lean`: The logical bridge from the geometric topology to the physical acceleration scalar $a_0$.
- `lean_proofs/MASTER_EQUATION.md`: Full documentation of the formal logic mapping.
