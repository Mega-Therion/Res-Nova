# Information Tension Theory, Geometrically Ordered Dynamics, Orchid, Zenodo, and Res Nova
## Wide research synthesis and peer-review hardening plan

**Prepared:** 13 September 2026  
**Scope:** Connected Notion corpus, Zenodo catalog and current records, `Mega-Therion/Res-Nova`, adjacent information/geometric-dynamics literature, and an adversarial peer-review audit.

## Executive conclusion

The research program contains a potentially publishable core, but it is not yet ready for serious peer review as a unified theory. The strongest defensible core is a **modified-gravity and reproducibility package** centered on the surviving `mu_std(x) = x/sqrt(1+x^2)` branch, its action-level derivation, its covariant AeST/Skordis–Złośnik embedding, solar-system constraints, and a reproducible SPARC benchmark. The broader Information Tension Theory and Geometrically Ordered Dynamics claims remain a layered research program rather than one established theory.

The most important finding is epistemic, not rhetorical: the corpus already contains the ingredients for a strong paper, but the evidence is distributed across many names, versions, Zenodo records, formal modules, and interpretive extensions. A referee will therefore ask first whether the authors can state exactly **which model is live**, **which claims are proved**, **which are fitted or postulated**, **which published records are obsolete**, and **which computational artifacts reproduce the headline numbers**.

Three immediate priorities dominate:

1. **Freeze and reconcile the current model.** The repository’s current `.zenodo.json` says that `mu_dual` was falsified on 12 September 2026 and that the theory was rebuilt on `mu_std`; older manuscripts and Lean modules still contain `mu_dual`. The publication catalog contains many superseded records, and the Notion adjudication ledger records unresolved gaps. No new unifying claims should be added until the canonical branch and version graph are machine-checkable.
2. **Correct the verification and publication claims.** Notion’s latest validity report says the Ars Magna monograph’s claim of “17/17 sorry-free” Lean modules and a three-axiom budget conflicts with the project’s own later audit, which reportedly found one `sorry` and a custom axiom. The current Res Nova `.zenodo.json` instead claims 17 modules, zero `sorry`, and only standard axioms. This is a release-blocking provenance contradiction.
3. **Narrow the first peer-reviewed submission.** Do not submit the entire ontology, E8 interpretation, cognition bridge, Orchid analogy, and cosmology as one claim. Submit a falsifiable and reproducible modified-gravity paper first. Treat the Information Tension–Fisher bridge, Geometrically Ordered Dynamics, Orchid work, and cognition applications as separate hypotheses or follow-on papers until they have domain-specific actions, observables, and controls.

The targeted audit below is not a completed ten-agent wide run. The requested orchestration was attempted, but the session stopped because the available agent-credit limit was reached before usable subagent results were returned. The report therefore uses a direct evidence pass over the connected Notion workspace, the public GitHub repository, Zenodo records, and opened scholarly sources. It preserves this limitation rather than presenting the result as broader than it is.

## 1. Corpus inventory and current state

### 1.1 Notion corpus

The connected workspace contains canonical or near-canonical pages for **Information Tension**, **Geometrically Ordered Dynamics**, the **Ars Magna** monograph, the **Zenodo publication catalog**, the **Res Nova** program, the **Theory Adjudication System**, and an attempted **Fisher identity versus ADCCL** bridge. The most useful pages are the following:

| Corpus component | What the current record establishes | Peer-review implication |
|---|---|---|
| Information Tension pages | The program uses an information/geometry vocabulary for modified gravity, dark-sector replacement, and coherence constraints. | Definitions must be rewritten as equations, units, domains, and observables rather than slogans. |
| Ars Magna / G.O.D. page | The monograph links an Einstein–Hilbert/AQUAL/symmetron/disformal construction with SPARC, CMB targets, E8/Stiefel language, and Lean artifacts. | The manuscript mixes distinct theorem, model, and interpretation layers. These need separate sections and claim labels. |
| Fisher bridge note | The identity involving `F_dual`, `mu`, and Bernoulli Fisher information is treated as a genuine algebraic result, while the ADCCL cross-domain extension is explicitly labeled conjectural. | This is a good example of the desired epistemic style: preserve the exact identity, state the missing action, and do not call the analogy a unification. |
| Theory adjudication ledger | A 12-question comparison against Standard Model and GR was prepared, but all 36 theory cells remain unscored and await a human judge. Important source gaps include PPN, GW, FLRW/ΛCDM, SM Lagrangian, electroweak precision, and g−2. | The adjudication system is infrastructure, not evidence of superiority. It should be completed with human-scored cells and source-complete comparison packs. |
| Zenodo catalog | The catalog reports 64 public records at its 27 July snapshot: 27 latest-version records, 36 superseded records, and 1 retracted record. | The citation policy must force use of concept DOIs or latest-version DOIs and must expose supersession/retraction status automatically. |

### 1.2 Res Nova repository

The public repository is unusually well structured for a private research program. It includes a technical manuscript, explicit claim-evidence ledgers, SPARC data and fit artifacts, preregistration notes, cosmology calculations, PPN scripts, a Lean formalization directory, verification runs, and a peer-review readiness package. The README explicitly distinguishes `derived`, `empirically_supported`, `conditional`, `proposal/open`, and `refuted` claims, which is the correct foundation for serious scrutiny [1].

The current repository metadata is materially more informative than the older “zero-parameter unified theory” framing. Its `.zenodo.json` states that `mu_dual(x)=x/(1+x)` was falsified by an internal solar-system analysis and that the surviving branch is `mu_std(x)=x/sqrt(1+x^2)`. It also states that the covariant completion is genuine AeST/Skordis–Złośnik, that `c_T=c` is structural, that the cosmological background uses published SZ Cosh parameters, that the intermediate-redshift `a_0(z)` test is inconclusive, and that non-linear AeST structure formation remains unsimulated [2]. These admissions strengthen the project when they are synchronized with all manuscripts, formal modules, Zenodo metadata, and public web pages.

The repository also shows the correct direction for formal work: the Lean directory contains modules for the dual-channel derivation, the standard branch, PPN limits, tensor speed, covariant completion, and finite SU(2) carrier rungs. However, formal compilation proves only the formal statements under their imported assumptions. It does not prove that the chosen action describes nature, that a physical interpretation follows from a typeclass structure, or that a numerical benchmark is correctly designed. The repository’s own formal-methods guidance should remain explicit on this boundary.

## 2. What is strongest, and what remains open

### 2.1 Strongest candidate claims

The most promising claims are narrow and testable:

| Candidate claim | Evidence class | Current status | Required hardening |
|---|---|---|---|
| A specified action yields a particular interpolation function | `[P]` conditional on the action and regularity assumptions | The `mu_std` branch is formalized in dedicated Lean modules and described as the surviving branch. | Publish the exact action, boundary conditions, function spaces, and a clean theorem statement. State every imported assumption. |
| The covariant completion belongs to the AeST/Skordis–Złośnik family | `[C]` plus model construction | The repository claims an embedding and structural `c_T=c`. | Provide a line-by-line map from symbols to the published AeST action, including matter coupling and free functions. |
| Solar-system safety distinguishes `mu_std` from `mu_dual` | `[E]` model comparison | The repository metadata says the old branch produced an anomalous acceleration far above Cassini bounds and that the new tail clears the solar system. | Reproduce the perturbative calculation from a clean clone, publish scripts and raw inputs, and show sensitivity to all nuisance choices. |
| SPARC benchmark is reproducible | `[E]` within a defined sample and model tier | The repository contains SPARC files, fit tables, parameter ledgers, and cross-validation scripts. | Use standard metrics, identical data cuts, uncertainty propagation, held-out evaluation, and direct comparison with published MOND and ΛCDM baselines. |
| `F_dual'(x)^2 I(mu(x))` identity | `[P]` algebraic identity | The bridge note says it was re-verified and distinguishes it from the physical unification claim. | Put the identity in a standalone theorem with domain assumptions and prove whether any uniqueness claim is actually discharged. |

### 2.2 Major unresolved claims

The project should not currently present the following as established results:

- A full E8 dynamical realization. The current evidence appears to use an `su(2)` subgroup in the worked soldering theorem while asserting a larger E8 structure. A referee will require either a complete E8 construction or a precise statement that E8 is a proposed substrate rather than a proved dynamical ingredient.
- A complete replacement for dark matter and dark energy. The SPARC result addresses a restricted galactic-rotation problem. It does not by itself settle clusters, CMB peak amplitudes, structure growth, BAO, BBN, lensing surveys, or the full cosmological background.
- A universal Information Tension law across gravity, cognition, biology, and AI. The Fisher/ADCCL note correctly says that an action for the agent-side coherence variable does not yet exist. The same limitation applies to the Orchid bridge unless a biological state variable, action or dynamical law, and discriminating experiment are specified.
- A formal proof of physical truth. Lean artifacts can establish algebraic identities, closure properties, and deductions from explicitly represented assumptions. They cannot validate empirical fit quality or the physical adequacy of the assumptions.
- A parameter-free model in the observational sense. The repository’s own accounting distinguishes a parameter-free law from fits using observational nuisance parameters and from model choices such as the interpolating function, screening functions, and cosmological parameters. The latter wording should be used everywhere.

## 3. Adjacent research that can materially improve the program

### 3.1 Information geometry and thermodynamics

Information geometry supplies established mathematical language for statistical manifolds, Fisher metrics, divergences, and curvature. It can help the program if “information tension” is defined as a specific scalar, functional, or metric on a state space. It will hurt the program if the phrase is used as a broad synonym for any trade-off between order and uncertainty. The information-bottleneck literature already formalizes a predictive-information versus compression trade-off, and the thermodynamics-of-information literature already studies how information constraints interact with entropy and physical work [3] [4].

The useful research question is therefore not “is information fundamental?” It is: **what quantity in the proposed gravitational action is mathematically identical to a known information-geometric object, and what new prediction follows from that identity?** The Fisher bridge note is a promising starting point because it states an exact identity and an explicit missing conjecture. The next step is to define a state manifold and prove invariance properties, not to extend the metaphor.

### 3.2 Geometric dynamics

Geometric mechanics, symplectic and contact geometry, optimal transport, and gradient-flow methods provide mature alternatives for expressing “ordered dynamics.” Their value is methodological: they force the author to state the state space, tangent/cotangent variables, symplectic or contact form, Hamiltonian or dissipation functional, and evolution law. Optimal-transport geometry is especially relevant when the proposed dynamics are gradient flows over probability distributions. Contact geometry is relevant when dissipation or thermodynamic variables are intrinsic rather than perturbative.

The paper should include a terminology map showing which parts of G.O.D. are new definitions, which are translations into existing geometric mechanics, and which are conjectural physical interpretations. A claim of novelty should be reserved for a theorem or prediction that cannot be obtained from the established framework by a change of notation.

### 3.3 Orchid and biological testing

The most defensible Orchid connection is as an **empirical pattern-formation test domain**, not as evidence that the same universal law already governs plants. Plant morphogenesis literature gives concrete measurable variables: auxin concentration and transport, PIN1 orientation, meristem geometry, cell-wall stiffness, growth anisotropy, and organ-initiation timing [5]. Phyllotaxis research combines mathematical modeling with experimental biology and treats regular organ patterns as emerging from growth, inhibitory fields, auxin distribution, and mechanical regulation [6].

A useful Orchid experiment would define a candidate tension observable from image sequences and molecular or mechanical measurements, preregister a model-free baseline, compare against established auxin/mechanical models, and ask whether the proposed geometric quantity predicts an out-of-sample event such as primordium initiation, orientation, or symmetry breaking. Without this design, Orchid remains an analogy rather than evidence for ITT or G.O.D.

## 4. Adversarial referee findings

A skeptical referee is likely to focus on the following points:

| Referee objection | Why it matters | Repair |
|---|---|---|
| Which branch is current? | Older `mu_dual` records coexist with the newer `mu_std` rebuild. | Create a canonical branch manifest with model hash, manuscript hash, DOI, and explicit supersession map. |
| Are the verification claims true? | Notion and repository metadata disagree about `sorry` count and axiom budget. | Run one clean-clone audit, publish its log, correct every manuscript and DOI metadata, and delete or label stale claims. |
| Is “zero parameter” misleading? | Observational nuisance parameters and model choices remain. | Report fixed-law, fitted-nuisance, and total model parameter counts in separate columns. |
| Does the SPARC statistic compare to literature metrics? | `chi²/N`, dex scatter, and marginalized fits are not interchangeable. | Recompute a common metric table with the same sample, weights, distance assumptions, and likelihood. |
| Does CMB agreement test the right observable? | Peak positions are less discriminating than odd/even peak heights and full spectra. | Run a Boltzmann-code comparison including peak amplitudes, lensing, BAO, and growth, or label the result as a target only. |
| Where are PPN and GW predictions? | Modified gravity is constrained by solar-system and multimessenger data. | Publish a complete weak-field expansion, PPN parameters, polarizations, generation, and propagation predictions. |
| Does E8 do dynamical work? | A large group name is not a derivation. | Either derive the full representation/action or reduce the claim to the explicitly used subgroup. |
| Are the cross-domain links causal? | Shape similarity is not a shared mechanism. | Derive separate domain actions and test transfer predictions against independent baselines. |
| Is the publication graph reliable? | Many superseded records and one retracted record create citation risk. | Use concept DOI plus latest-version DOI; mark old records in every index and release artifact. |
| Can an outsider reproduce it? | Internal scripts and cached data are insufficient. | Provide clean-clone commands, pinned dependencies, raw-data hashes, expected outputs, and CI artifacts. |

## 5. Prioritized 30/60/90-day hardening roadmap

### Days 0–30: establish one canonical, falsifiable model

Freeze the surviving model in a release branch. Produce `MODEL_MANIFEST.json` containing the exact action, branch name, equations, units, parameter list, data hashes, code commit, Lean toolchain, and current Zenodo concept/version DOIs. Mark all `mu_dual` material as superseded or historical unless it is used as a falsified control.

Reconcile the formal corpus. Run the target inventory, proof gate, and full Lean build in a clean clone. Count `sorry`, `admit`, custom axioms, imported axioms, and uncompiled modules from the actual filesystem. Correct `.zenodo.json`, manuscripts, ledgers, README, Notion pages, and release notes to the same numbers. Do not publish or cite a new version until this reconciliation is complete.

Write a 10–15 page core manuscript with only: action, field content, derivation of `mu_std`, weak-field/solar-system limits, covariant completion, SPARC data and benchmark, limitations, and reproducibility appendix. Remove cognition, E8 grand claims, Orchid, and universal ontology from the main result unless they are needed for a precise equation.

### Days 31–60: reproduce and stress-test the empirical claims

Reproduce SPARC from raw data in a fresh environment. Report fixed-prescription, nuisance-fitted, and cross-validated results separately. Include a predeclared likelihood, uncertainty model, data exclusions, mass-to-light assumptions, distance/inclination treatment, and comparison against strict MOND, a standard ΛCDM halo model, and at least one contemporary modified-gravity baseline.

Complete the weak-field package. Derive PPN parameters, light deflection, Shapiro delay, perihelion advance, binary-pulsar implications, and the scalar/vector/tensor radiation content. For every result, state whether it is a theorem from the action, a numerical solution, or an assumption.

Resolve the `mu_std` uniqueness status. The current Lean module should be described as proving uniqueness under a stated conjugacy/Fisher/rapidity postulate, not as deriving the function from no assumptions. Put the postulate in the theorem boundary and test alternative families such as `k=3,5` or other admissible closures.

### Days 61–90: independent scrutiny and publication package

Create an artifact-evaluation package with a one-command reproduction, container or lockfile, raw-data checksums, expected tables, and CI. Add a machine-readable claim ledger with fields for claim, evidence class, source locator, assumptions, numerical artifact, falsifier, status, and last verification commit.

Ask two independent reviewers to audit different layers: one mathematical physicist for action/limits and one computational statistician for SPARC/model comparison. Do not ask them whether the theory is “true.” Ask whether each headline claim is correctly stated, reproducible, and empirically discriminating.

Only after these gates should the project update the primary Zenodo record. Cite the latest-version DOI, retain the concept DOI, and include a machine-readable supersession table. Submit the narrow core first. Treat the broader G.O.D./ITT synthesis as a roadmap paper or perspective only after its domain-specific predictions are independently developed.

## 6. Peer-review readiness matrix

| Area | Current assessment | Readiness gate |
|---|---|---|
| Definitions and notation | Partial | One glossary with equations, dimensions, domains, and symbol uniqueness. |
| Action and variation | Promising but incomplete | Independent derivation from the canonical action with boundary conditions. |
| Formal verification | Substantial infrastructure, status inconsistency | Clean-clone audit, reconciled axiom/sorry ledger, no stale headline claims. |
| Galactic data | Substantial artifacts | Common metrics and independent reproduction. |
| Solar-system tests | Active and high priority | Full PPN and perturbative bound derivation. |
| Cosmology | Incomplete | CMB amplitudes, growth, BAO, SN, and parameter accounting. |
| E8/Stiefel claims | Not ready as a full physical claim | Complete dynamical construction or narrow the claim to the used subgroup. |
| Fisher/information bridge | Good algebraic seed, open physical bridge | State-space/action definition and a discriminating prediction. |
| Orchid program | Potential empirical test domain | Species, variables, protocol, baselines, preregistration, and out-of-sample test. |
| Publication metadata | High provenance risk | Latest-version/concept DOI map and removal of contradictory metadata. |
| Broad unification | Not ready | Separate papers or explicit `[O]` research program status. |

## 7. Recommended next research questions

1. Can the corrected covariant action reproduce the required galactic limit while satisfying the complete PPN and multimessenger constraints without hidden tuning?
2. Which exact assumptions select `mu_std`, and do alternative admissible closures survive the same assumptions?
3. Does the proposed information-geometric quantity have a coordinate-invariant definition and a measurable relation to an observable beyond a relabeling of the acceleration ratio?
4. Can the CMB claim be tested against peak amplitudes and the full transfer spectrum rather than peak positions alone?
5. Does the E8 structure enter the equations of motion, or is it only a representation-theoretic interpretation of a smaller active sector?
6. Can an Orchid experiment produce a quantitative prediction that differs from auxin/mechanical morphogenesis models before observing the data?
7. Which claims in the theory-adjudication ledger become `HIT`, `MISS`, or `OPEN` after the missing Standard Model and GR source packs are filled and a human judge scores all cells?
8. Can an outsider reproduce every headline table from a clean clone without access to Notion, private paths, or undocumented cached state?

## Bottom-line recommendation

The project should proceed, but as a **disciplined decomposition**. The immediate objective should be a corrected, narrow, reproducible modified-gravity paper whose strongest claims survive independent checking. Information Tension should be formalized as a precise mathematical object rather than used as a universal explanatory label. Geometrically Ordered Dynamics should be presented as a proposed organizing framework with a theorem ladder. The Orchid work should become a preregistered biological test program. The AI/cognition and E8 extensions should remain explicitly open until they have independent actions, observables, and falsifiers.

That strategy does not diminish the larger vision. It gives the vision a credible path through peer review: one exact model, one audited evidence chain, one reproducible artifact, and one honest boundary between what is proved, what is measured, what is assumed, and what remains conjectural.

## References

[1]: https://github.com/Mega-Therion/Res-Nova "Mega-Therion/Res-Nova repository"

[2]: https://zenodo.org/records/21504895 "Information Tension: Geometric Projection Replaces Dark Matter at Low Acceleration, v3 audit-corrected"

[3]: https://arxiv.org/abs/2310.03884 "Information geometry for the working information theorist"

[4]: https://doi.org/10.1103/RevModPhys.81.1 "Colloquium: The physics of Maxwell’s demon and information"

[5]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7404056/ "Molecular and Hormonal Regulation of Leaf Morphogenesis"

[6]: https://doi.org/10.1002/wdev.231 "Phyllotaxis: from patterns of organogenesis at the meristem to shoot architecture"

[7]: https://app.notion.com/p/3c777b95a96581ff809cd5cedc74f155?pvs=204 "The Law of Geometrically Ordered Dynamics — Ars Magna v3.0"

[8]: https://app.notion.com/p/3aa77b95a9658182a435d08dc3265f8f?pvs=204 "Zenodo Publications Catalog"

[9]: https://app.notion.com/p/3da77b95a96581a2bd13d966aa43d32c?pvs=204 "Theory Adjudication System — Final Results & Completed Ledger"

[10]: https://app.notion.com/p/3d877b95a965816eb08f2653a273e8a?pvs=204 "ITT Bridge Attempt: Fisher Identity vs. ADCCL Chi"

[11]: https://doi.org/10.1103/PhysRevLett.127.161302 "The Skordis–Złośnik relativistic modified-gravity model"

[12]: https://doi.org/10.1103/PhysRevD.93.104013 "SPARC and the radial acceleration relation benchmark"

[13]: https://github.com/Mega-Therion/Res-Nova/blob/main/PEER_REVIEW_READINESS.md "Res Nova peer-review readiness document"

[14]: https://github.com/Mega-Therion/Res-Nova/blob/main/OPEN_PROBLEMS_AND_TESTS.md "Res Nova open problems and tests"

[15]: https://github.com/Mega-Therion/Res-Nova/blob/main/CLAIM_EVIDENCE_LEDGER.md "Res Nova claim-evidence ledger"

[16]: https://github.com/Mega-Therion/Res-Nova/blob/main/05_lean_formalization/MuStdUniqueness.lean "Res Nova MuStdUniqueness Lean module"

[17]: https://github.com/Mega-Therion/Res-Nova/blob/main/.zenodo.json "Res Nova Zenodo metadata"

[18]: https://zenodo.org/api/records?q=creators.orcid%3A0009-0001-1303-7190 "Zenodo public records API query for the author’s ORCID"

[19]: https://github.com/Mega-Therion/Res-Nova/blob/main/RES_NOVA_VERIFICATION_LEDGER.md "Res Nova verification ledger"

[20]: https://github.com/Mega-Therion/Res-Nova/blob/main/RELEASE_CHECKLIST.md "Res Nova release checklist"

[21]: https://github.com/Mega-Therion/Res-Nova/tree/main/02_galaxy_dynamics "Res Nova SPARC galaxy-dynamics artifacts"

[22]: https://github.com/Mega-Therion/Res-Nova/tree/main/05_lean_formalization "Res Nova Lean formalization artifacts"

[23]: https://github.com/Mega-Therion/Res-Nova/tree/main/04_cosmology "Res Nova cosmology artifacts"

[24]: https://github.com/Mega-Therion/Res-Nova/tree/main/03_observer_jwst "Res Nova JWST and intermediate-redshift artifacts"

[25]: https://github.com/Mega-Therion/Res-Nova/tree/main/06_unification_and_spin "Res Nova unification and spin exploratory artifacts"

[26]: https://zenodo.org/records/20652203 "Retracted Trinity Survey Replication record listed in the catalog"

[27]: https://doi.org/10.5281/zenodo.21969121 "Res Nova reproducibility package record identified in the repository release checklist"

[28]: https://doi.org/10.1146/annurev-statistics-030718-104938 "Statistical aspects of Wasserstein distances"

[29]: https://doi.org/10.1038/s41567-021-01283-7 "Landauer principle and information thermodynamics review"

[30]: https://doi.org/10.1186/s12864-017-3756-9 "Transcriptome variation in orchid floral development"

[31]: https://doi.org/10.1103/RevModPhys.81.1 "Information and thermodynamics review"

[32]: https://doi.org/10.1002/wdev.231 "Plant phyllotaxis and mathematical modeling review"

[33]: https://github.com/Mega-Therion/Res-Nova/blob/main/CONSOLIDATION_AND_SALVAGE_PLAN.md "Res Nova consolidation and salvage plan"

[34]: https://github.com/Mega-Therion/Res-Nova/blob/main/THEORY_ASSUMPTION_AUDIT.md "Res Nova theory assumption audit"

[35]: https://github.com/Mega-Therion/Res-Nova/blob/main/VERIFICATION_STATUS_AUDIT.md "Res Nova verification status audit"

[36]: https://github.com/Mega-Therion/Res-Nova/blob/main/05_lean_formalization/REPRODUCE.md "Res Nova Lean reproduction instructions"

[37]: https://github.com/Mega-Therion/Res-Nova/blob/main/05_lean_formalization/PPNLimits.lean "Res Nova PPN formalization module"

[38]: https://github.com/Mega-Therion/Res-Nova/blob/main/05_lean_formalization/TensorSpeed.lean "Res Nova tensor-speed formalization module"

[39]: https://github.com/Mega-Therion/Res-Nova/blob/main/05_lean_formalization/SkordisZlosnikEmbedding.lean "Res Nova Skordis–Złośnik embedding module"

[40]: https://github.com/Mega-Therion/Res-Nova/blob/main/05_lean_formalization/PillarIV_AntiDriftGate.lean "Res Nova anti-drift formalization module and open-premise notes"

[41]: https://doi.org/10.1103/PhysRevLett.127.161302 "Skordis–Złośnik AeST model source"

[42]: https://zenodo.org/records/21461195 "The Pleroman: The Unified Statement of Geometrically Ordered Dynamics"

[43]: https://zenodo.org/records/21623111 "Geometrodynamica: Geometrically Ordered Dynamics"

[44]: https://doi.org/10.5281/zenodo.21504895 "Current Information Tension record"

[45]: https://doi.org/10.5281/zenodo.21384483 "Current Ars Magna record"

[46]: https://doi.org/10.5281/zenodo.21479962 "Universal Information Geometry catalog record"

[47]: https://doi.org/10.5281/zenodo.21450453 "The Bridge of Bridges catalog record"

[48]: https://doi.org/10.5281/zenodo.21450433 "Field Identity and Entanglement catalog record"

[49]: https://doi.org/10.5281/zenodo.21367552 "Geometric accretion limits record"

[50]: https://doi.org/10.5281/zenodo.21367564 "Earlier Information Tension SPARC record"

[51]: https://doi.org/10.5281/zenodo.20652203 "Retracted record requiring explicit citation suppression"

[52]: https://orcid.org/0009-0001-1303-7190 "Ryan W. Yett ORCID profile"
