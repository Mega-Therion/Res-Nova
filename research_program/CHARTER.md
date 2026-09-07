# Res-Nova Frontier Theoretical Physics Research Program

**Status:** Program charter — planning and governance authority. It does **not** upgrade, add, or reinterpret any physics claim.

**Claim authority:** `EPISTEMIC_BOUNDARY_v1.5.0.md` and `AGENT_COVENANT.md` remain controlling for every scientific statement in this repository. Where a manuscript, README, program document, or public communication conflicts with the claim ledger, the ledger prevails.

## 1. Mission

> **Res-Nova is a falsification-first program in relativistic modified gravity.** Its purpose is to determine whether the dual-channel nonrelativistic interpolation
>
> \[
> F_{\mathrm{dual}}(x)=\frac{x^2}{2}-x+\ln(1+x), \qquad
> \mu(x)=F_{\mathrm{dual}}'(x)=\frac{x}{1+x},
> \]
>
> can be embedded in a stable, covariant theory that survives explicitly defined galaxy-scale, local-gravity, gravitational-wave, lensing, and cosmological tests.

The program does **not** begin from the premise that gravity has been replaced, that a horizon relation has been derived, that dark matter or dark energy has been eliminated, or that a single interpolation function has a unique physical origin. Those are hypotheses or open questions until they pass the program’s gates.

A frontier program earns credibility by making its most important possible failures visible. Res-Nova will therefore prefer a clean no-go theorem, a negative replication, or a ruled-out parameter region to a broad narrative unsupported by a reproducible artifact.

## 2. Scientific position and external benchmark

Res-Nova’s immediate comparison class is relativistic MOND-like modified gravity, particularly vector–tensor constructions that are intended to recover galaxy phenomenology while confronting cosmology and stability. Skordis and Złośnik proposed a relativistic MOND construction and reported agreement with CMB and linear matter-power observations plus second-order ghost freedom; this is a field reference point, not evidence for any Res-Nova result.[1]

A credible modified-gravity program must confront distinct observational and theoretical regimes: Solar-System and binary-pulsar tests, gravitational-wave propagation and polarizations, lensing, galaxy/cluster dynamics, CMB and large-scale structure, screening, degrees of freedom, and stability.[2] A later analysis of the Skordis–Złośnik theory further highlights that time-varying local parameters and the gravitational-wave sector are independent constraints, not optional footnotes.[3]

| Res-Nova boundary | Program rule |
|---|---|
| Formal mathematics | Lean verification establishes only the theorem stated under its explicit assumptions; it does not certify physical ontology or empirical adequacy. |
| Galaxy phenomenology | A fit to SPARC or any other data is an empirical result only when code, input checksums, priors, nuisance treatment, and posterior/predictive outputs are frozen. |
| Relativistic completion | A parent theory is viable only provisionally and only after separately specified stability, PPN, wave-sector, lensing, and cosmology gates. |
| Horizon and information narratives | `a_0=cH_0/(2\pi)`, the interpretation of \(\xi\), and \(\Omega_\Lambda=\ln2\) remain open hypotheses unless independently derived and tested. |
| Public communication | No claim may be stronger than its ledger tag: `[P]` proved, `[D]` direct empirical, `[C]` cited, or `[O]` open/quarantined. |

## 3. Research questions

The program is organized around five questions. Each question can yield a publishable positive result, a publishable constraint, or a scientifically useful negative result.

| ID | Frontier question | Current posture | What counts as progress |
|---|---|---|---|
| RQ-1 | Does the dual-channel interpolation possess rigorously stated mathematical properties distinct from rejected single-channel alternatives? | Formal core partly present. | Lean theorem set with assumptions, counterexamples, and a third-party cold-run receipt. |
| RQ-2 | Does a reproducible galaxy-scale inference identify a stable acceleration-scale phenomenology after hierarchical uncertainties and out-of-sample checks? | SPARC working measurement exists; clean-clone data path remains open. | Frozen data manifest, preregistered estimator, posterior predictive diagnostics, and an independent replication. |
| RQ-3 | Can a specified covariant vector–tensor parent satisfy local, stability, lensing, and wave-sector constraints without hiding failures in an unexamined sector? | Parent membership and selected conditions are formalized. | A complete condition ledger with analytic derivations and numerical parameter scans, including excluded regions. |
| RQ-4 | Is the acceleration scale constant or does it exhibit redshift evolution tied to a specified cosmological quantity? | Open; no in-repository high-redshift campaign. | Pre-registered forward model applied to a named public data release, with blinded or held-out validation and null controls. |
| RQ-5 | Can the model class reproduce baseline cosmological observables without post-hoc tuning or selectively chosen subsets? | Open; not to be inferred from galaxy fits. | Reproduction of a published baseline likelihood followed by a separately versioned Res-Nova comparison. |

## 4. Falsification gates

No theory branch may be called a viable relativistic completion until it has reached the relevant gate with a preserved artifact. A pass at one gate is not evidence of a pass at another.

| Gate | Minimum artifact | Fail criterion | Current Res-Nova status |
|---|---|---|---|
| G0 — Formal integrity | Pinned Lean toolchain, source hash, zero-placeholder scan, cold-run CI receipt. | The theorem fails to elaborate, depends on unacknowledged axioms/assumptions, or the stated theorem differs from the proved theorem. | O6 is open: clean-worktree run exists; cold-run CI gate is not yet established. |
| G1 — Reproducible galaxy inference | Official data fetch, checksum manifest, environment lock, declared priors/nuisances, predictive diagnostics. | Results cannot be reproduced from a clean clone or collapse under declared systematic/holdout analyses. | O5 is open: SPARC is not vendored and clean-clone path is unproven. |
| G2 — Local and wave sector | Derivation and numerical bounds for PPN, preferred-frame effects, tensor speed/polarizations, radiation, and stability. | Any benchmark bound is violated in the stated parameter region, or a stability argument is incomplete. | Selected conditions are formalized; full unified parameter audit is not complete. |
| G3 — Lensing and cluster sector | Metric/light-deflection prediction and a named comparison data set. | The physical metric does not reproduce the required lensing relation or requires unstated extra matter/parameters. | Not established in this repository. |
| G4 — Cosmological background and perturbations | Reproduction of a public baseline plus CMB/LSS likelihood comparison using a frozen release. | Baseline cannot be reproduced or a claimed viable region fails predeclared goodness-of-fit criteria. | Not established in this repository. |
| G5 — Redshift-evolution discriminator | A pre-registered \(a_0(z)\) forward model, named tracer/catalog, selection function, uncertainty model, and null test. | The inferred evolution cannot be distinguished from selection/systematic effects, or falsifies the stated relation. | Not established in this repository. |

## 5. Research work packages

### WP-0 — Program integrity and reproducibility

This work package protects all other work. It will make the SPARC fetch-and-checksum pipeline and the Lean cold-run path executable on clean infrastructure; introduce environment locks, machine-readable run manifests, and release tags; and require archival of scripts, hashes, logs, and failures. Its first output is a release in which an external reader can reproduce the formal and galaxy baseline without author-specific paths.

### WP-1 — Formal dual-channel core

This work package separates mathematics from interpretation. It will state the exact assumptions behind the dual-channel identity, formalize any missing asymptotic/limit claims, preserve counterexamples to rejected branches, and publish a minimal theorem note. The research output may be a theorem/counterexample paper, not a claim that nature selected the action.

### WP-2 — Galaxy dynamics and hierarchical inference

This work package will rebuild the galaxy analysis around a reproducible data release and an explicit generative model. The essential outputs are a pre-analysis plan, a galaxy-level likelihood, priors for distances, inclination, and mass-to-light treatment, galaxy-resampled uncertainty estimates, posterior predictive checks, and held-out diagnostics. SPARC remains a baseline because it provides public mass models and high-quality HI+Hα rotation curves for 175 late-type galaxies.[4]

The program will compare like with like: the dual-channel relation, a standard MOND relation, and halo baselines must use matched nuisance freedom, stated priors, and an agreed score. A fit-quality headline without a parameter ledger and predictive checks is not an empirical milestone.

### WP-3 — Covariant completion and multi-messenger gates

This work package will treat the vector–tensor completion as a conditional theory branch. It will build a parameter and assumption map for stability, screening, PPN limits, preferred-frame effects, gravitational-wave speed and polarization, energy loss, and lensing. Every condition must be tagged as formally proved in the stated parent, cited from literature, numerically evaluated, or open.

The deliverable is a constraint atlas with three regions: **allowed under stated assumptions**, **excluded**, and **unresolved**. A constraint atlas is more scientifically useful than a single favorable benchmark point.

### WP-4 — Cosmology and redshift discrimination

This work package is prohibited from treating the numerical proximity of \(a_0\) and \(cH_0/(2\pi)\) as evidence of derivation. It will first reproduce a named public cosmological baseline, then introduce a clearly parameterized extension, and finally test redshift dependence against a predeclared tracer and catalog. DESI’s public data ecosystem provides a possible future input route, but analyses must use the appropriate official data product and likelihood rather than an informal catalog selection.[5]

The immediate output is an analysis specification, not a cosmological claim. A result becomes `[D]` only after the data release, forward model, selection criteria, calibration/systematics treatment, and code revision have been frozen.

### WP-5 — Independent criticism and scholarly exchange

The program will solicit adversarial review before promotion. Each major release should have a short “failure memo” authored by someone not responsible for the underlying calculation, who is tasked with finding missing assumptions, non-identifiability, parameter-count asymmetries, invalid comparators, or wording that exceeds the evidence. A serious negative review is an output, not an embarrassment.

## 6. Research lifecycle

Every research item moves through the same state machine:

1. **Question.** A single falsifiable question and competing hypotheses are written in the experiment registry.
2. **Pre-analysis specification.** Data version, exclusions, model, priors, metrics, calibration/systematic plan, stopping rule, and success/failure criteria are frozen before fitting.
3. **Execution.** The analysis runs in an isolated, versioned environment and produces a signed/hashed manifest.
4. **Red-team review.** A reviewer attempts to reproduce the result, runs predeclared negative controls, and checks claims against the ledger.
5. **Ledger decision.** The item receives `[P]`, `[D]`, `[C]`, `[O]`, or is explicitly withdrawn/superseded. It is never silently promoted.
6. **Release.** Code, environment, data-access instructions, result object, figure source, and a concise claim card are published together.

## 7. Standards for public papers

The first papers should be **small, separable, and falsifiable**. They should not try to present a complete theory of galaxies, cosmology, and information physics in one submission.

| Paper sequence | Provisional title | Permitted conclusion |
|---|---|---|
| P1 | *A formally verified dual-channel interpolation and its limits* | Establishes stated mathematical identities and rejected alternatives; no ontology claim. |
| P2 | *A reproducible galaxy-level inference of a dual-channel acceleration scale in SPARC* | Reports a frozen-data empirical measurement and model comparison under declared assumptions. |
| P3 | *Constraints on a vector–tensor embedding of dual-channel modified dynamics* | Maps conditional viability and exclusions in the covariant branch. |
| P4 | *A preregistered test of acceleration-scale evolution in [named data release]* | Reports a discriminating observation or a null/limited result. |
| P5 | *Cosmological baseline reproduction and constraints for [specified extension]* | Reports a scoped likelihood result, not a replacement cosmology. |

Each paper must include a one-paragraph claim boundary, a data/code availability statement, a declared competing model, a limitations section, and links to a versioned repository release.

## 8. First twelve-week operating plan

The program becomes real through small, completed gates rather than a larger manifesto.

| Window | Non-negotiable deliverable | Completion test |
|---|---|---|
| Weeks 1–2 | Clean-clone reproducibility for SPARC fetch/checksum and Lean verification. | A fresh runner produces saved logs and manifests without author-specific paths. |
| Weeks 3–4 | A public experiment registry and first preregistration for the galaxy reanalysis. | The schema, competing models, priors, metrics, and failure conditions are committed before rerunning fits. |
| Weeks 5–7 | Galaxy inference release candidate with negative controls and held-out checks. | All figures and summary JSON are regenerated from the frozen manifest. |
| Weeks 8–9 | Covariant-branch constraint atlas specification. | Every listed condition has an assumption source, calculation path, and status tag. |
| Weeks 10–12 | External critique package and P1/P2 paper outline. | An independent reader can run the core artifacts and identify every conclusion’s ledger line. |

## 9. Program identity

Use this public description until a result earns a narrower or stronger wording:

> **Res-Nova is an open, falsification-first research program studying whether a dual-channel galaxy-dynamics interpolation admits a stable relativistic completion consistent with local gravity, gravitational waves, lensing, and cosmology. Formal identities, empirical measurements, cited constraints, and open hypotheses are maintained in separate auditable ledgers.**

Do not call Res-Nova a theory of everything, a replacement for ΛCDM, a derivation of the MOND scale, or a solution to dark matter/dark energy without a ledgered result that warrants those words.

## References

[1]: https://doi.org/10.1103/PhysRevLett.127.161302 "Skordis & Złośnik (2021), New Relativistic Theory for Modified Newtonian Dynamics"
[2]: https://doi.org/10.1146/annurev-astro-091918-104423 "Ferreira (2019), Cosmological Tests of Gravity"
[3]: https://doi.org/10.1103/PhysRevD.107.044062 "Tian et al. (2023), Time evolution of local gravitational parameters and gravitational-wave polarizations in a relativistic MOND theory"
[4]: https://astroweb.case.edu/SPARC/ "SPARC galaxy database"
[5]: https://portal.nersc.gov/project/cosmo/ "NERSC Cosmology Data Repository"
