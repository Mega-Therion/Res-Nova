# 🚀 Release Checklist & Reproducibility Package

**Manuscript Title:** *Conditional AQUAL Closures, Formal Verification Boundaries, and a Reproducible SPARC Benchmark: A Technical Assessment*  
**Auditor Target:** Bob / Lead Scientific Reviewers  
**Publication Status:** Verified Technical Draft / Reproducibility Reference Package (v1.5.0)  

---

### Phase 1: Mathematical & Formal Kernel Verification
- [x] **Lean 4 Proofs Build Cleanly:** 17/17 formal modules in `05_lean_formalization/` compiled with exit code 0 via `./05_lean_formalization/verify_all_proofs.sh` (O6 — walked once in a clean worktree at 07185a6 (lake exe cache get + 17/17 PASS, VERIFICATION_RUN_007). Not yet demonstrated on a cold machine with empty host cache, and not yet a CI release gate).
- [x] **Axiomatic Hygiene Checked:** Run `#print axioms` across all headline declarations; verified exclusive dependence on standard foundational axioms `[propext, Classical.choice, Quot.sound]`. (Documented structural/typeclass vacuity in `YettParadigm.lean` and `SovereignRegularity.lean` noted in `THEORY_ASSUMPTION_AUDIT.md`).
- [x] **No Forbidden Proof Shortcuts:** Zero instances of unproven `sorry` or `admit` in compiled theorems.

---

### Phase 2: Empirical SPARC Reproduction & Parameter Accounting
- [x] **Raw Input Data Authenticated:** 175 SPARC `*_rotmod.dat` files cryptographically hashed (`SHA-256: e76e6752164b80b14a20c1d6c05f96d095456e067bdd5c6da59d2be4ec70c1eb` in `VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256`).
- [x] **Working Measurement:** $a_0 = (1.116 \pm 0.128_{\text{stat}} \pm 0.097_{\text{syst}})\times 10^{-10}\text{ m/s}^2$ (total 14.4% error) across 171 galaxies (3,375 points) from `02_galaxy_dynamics/A0_MEASUREMENT.json`.
- [x] **Tier 1 Parameter Accounting:** Matched-nuisance Tier 1 GOD model has $N_{\text{par}} = 374$ parameters ($171 \times 2 + 32 = 374$), median $\chi^2_{\text{data}}/N_g = 2.95$ (`02_galaxy_dynamics/PARAMETER_LEDGER.json`).
- [x] **Constrained NFW Baseline:** NFW with cosmological concentration prior yields median $\chi^2_{\text{data}}/N_g = 5.62$ ($N_{\text{par}} = 716$, 342 extra knobs vs GOD). Unconstrained NFW rails 97/171 galaxies at $c=1$ (`02_galaxy_dynamics/NFW_CONSTRAINED.json`).
- [x] **Terminology Precision:** Per-galaxy metric consistently reported as $\chi^2_{\text{data}}/N_g$ (data-residual $\chi^2$ per kinematic point). "Zero free parameters" language withdrawn as a working model class.

---

### Phase 3: Epistemic Boundary Enforcement
- [x] **Action Variation Boundary:** Dual-channel algebraic identity $\mathcal{F}_{\text{dual}}'(x) = x/(1+x)$ proved `[P]`; single-channel $\operatorname{arcsinh}$ quarantined as correspondence-false (`01_foundational_action/PAPER_01_NOTICE.md`). Uniqueness of action in nature tagged open `[O]`.
- [x] **Acceleration Normalization:** $T_U = T_{\text{GH}} \implies a = cH_0$ derived; $a_0 = cH_0/(2\pi)$ labeled as open boundary normalization `[O]`.
- [x] **Optical and Cosmological Sectors:** Disformal optical couplings and horizon densities labeled as open research program `[O]`.
- [x] **Overclaim Purge:** No usage of "grand unified theory," "proves dark matter," "confirmed," or "all galaxies fit."

---

### Phase 4: Production Artifacts Deliverables
- [x] [`final_manuscript.tex`](final_manuscript.tex) & [`final_manuscript.pdf`](final_manuscript.pdf) (referee grade, clean compilation).
- [x] [`references.bib`](references.bib) (Authentic peer-reviewed citations).
- [x] [`reproducibility_appendix.tex`](reproducibility_appendix.tex) (Complete technical appendices).
- [x] [`CLAIM_EVIDENCE_LEDGER.md`](CLAIM_EVIDENCE_LEDGER.md) (Claim-to-evidence matrix).
- [x] [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) (Auditor sign-off checklist).
- [x] [`build/STATUS_AND_SCOPE.tex`](build/STATUS_AND_SCOPE.tex) (Front-matter summary sheet).
