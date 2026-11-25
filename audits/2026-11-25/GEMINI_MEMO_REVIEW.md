# Review of shared Gemini memo against Res Nova

**Shared artifact:** [Depth-Dependent Dispersion, Catastrophe Caustics, and Conservative Hydrodynamics on a Finite-Thickness Superfluid Bubble-Wall Cosmology](https://share.gemini.google/WSbeUhQq0q9S)  
**Review date:** 2026-11-25  
**Repository baseline:** `Mega-Therion/Res-Nova`, audited commit `212b55a8`

## Decision

Do not import the shared memo into Res Nova's live claim registry or promote its `[P]`, `[O]`, or `[X]` labels. The memo is a separate speculative architecture built around a finite-thickness superfluid bubble wall, nonlocal symmetric teleparallel gravity, AQUAL/BEC wave mechanics, and a dark-bubble embedding. Res Nova's current live seat is narrower: the galaxy law `μ_std` on galaxies, ordinary GR outside galaxies, and the corrected AeST cosmological sector. The memo does not supply repository-mirrored action files, frozen gate protocols, source-data manifests, code, hashes, independent implementations, or receipts that satisfy Res Nova's evidence rules.

The memo is still useful as a lead sheet. It contains several potentially testable mathematical or numerical ideas, and some of its negative conclusions independently point in the same direction as existing Res Nova exclusions. Those points should remain external leads until reconstructed under a named model and frozen protocol.

## Findings that agree with the repository

The memo's rejection of the minimal scalar nonlocal kernel on classical ghost and local-gravity grounds is directionally consistent with Res Nova's existing caution around nonlocal screening. It is not, however, a new Res Nova result: the memo studies an STG action that is not the live AeST action. Any ghost calculation must be checked from the exact action, boundary conditions, and allowed auxiliary-field data before it can be attached to a Res Nova claim.

Its dark-bubble warning about coupling Standard Model non-Abelian gauge fields through the proposed bulk B/C channel is also consistent in direction with the repository's existing `[X]` dark-bubble embedding record. `CURRENT_STATE_READ_THIS_FIRST.md` already records that the flux-fed drag embedding is excluded as formulated and that reopening it requires a different mechanism and a derived quark/gluon sign. The memo therefore adds no reason to change the current status; at most it provides an external restatement that should be source-checked against the repository's pinned artifacts.

The memo's warning that a phase-only non-analytic superfluid EFT is inadequate at vortex cores is a reasonable numerical-modeling caution. It is not part of the current Res Nova galaxy-law or AeST closure gates. If the project ever adopts a superfluid-vortex sector, the full complex order parameter, core regularization, and a separate gate protocol would be required.

## Findings that conflict with or exceed the live scope

The memo treats a finite-thickness `S^3` bubble wall, a superfluid phase transition between galaxies and clusters, and nonlocal STG as parts of one master action. None of those choices is the current Res Nova model identity. Importing them would create a new model version, not extend the existing AeST results. In particular, the memo's claims about bubble-wall KdV/Ostrovsky dynamics, Benjamin–Feir islands, rim dominance, caustic morphology, and thermal evaporation cannot be used to close D7, D10, O1, O3, #184, or #214.

The memo's statement that `F_std'' > 1` implies superluminal propagation is explicitly conditional on identifying the asymptotic nonrelativistic sound scale `c_0` with the vacuum light speed `c`. That identification is not a consequence of the repository's live AeST action. A scalar-sector sound speed, tensor speed, and matter/light-cone speed are distinct quantities and must be derived from the same covariant action. The repository already treats `c_T = c` as a scoped structural result while keeping branch selection and other stability questions separate. The memo therefore does not overturn the current D8/D7 status.

The memo also uses different off-center conventions in different places. Its synthesis names a canonical offset `ε = 1/2`, while the rim-dominance derivation later substitutes `ε = 1/√2` and computes values corresponding to that choice. That convention must be resolved before any numerical prediction is meaningful. More broadly, the memo often labels symbolic identities and single-run numerical checks `[P]`; Res Nova's taxonomy would label a symbolic identity `[P]` only for the exact formal statement, while physical interpretation, numerical implementation, and empirical relevance would remain separately tagged.

## Evidence and reproducibility deficiencies

The shared artifact reports many exact-looking values, including `2.274×10^-13` curl residuals, `2.6×10^-16` AMR mass drift, threshold values, lensing predictions, and observational comparisons. The shared response does not provide a repository checkout, commit IDs, input files, machine-readable outputs, dependency lockfile, random seeds, solver tolerances, or independent reproduction. Those values are therefore unverified external assertions, not Res Nova evidence.

The memo cites contemporary observational results and named papers in prose, but the shared artifact does not provide a complete primary-source ledger with exact figure/table locations, release versions, retrieval dates, transformations, or data hashes. Claims involving Dragon Arc, Euclid, ACT DR6, DESI, lensing parity, matter dipoles, and distance duality require separate source audits before being used in a repository gate. The memo's own `[O]` predictions should not be rewritten as observed facts.

## What can be salvaged

A narrow external-research branch could be opened only as a new named model, for example a finite-thickness superfluid-wall extension, with a new action and explicit relation—or non-relation—to AeST. The first admissible tasks would be dimensional analysis, independent derivation of the AQUAL Hessian identities, a convention audit for `ε`, and a manufactured-solution numerical test for the proposed conservative solver. No astrophysical prediction should be scored until the action, matter coupling, phase transition rule, boundary conditions, and nuisance/data policy are frozen.

The memo's nonlocal STG ghost argument could be recorded as an external lead against a separately specified kernel. It must not be merged with the existing AeST dark-bubble result. The dark-bubble obstruction can be cross-referenced to the existing `[X]` record after primary-source and artifact-level comparison, but it does not change the live status.

## Repository action

No physics or claim-registry changes were made in response to the memo. The correct repository correction is negative: preserve model identity, quarantine the memo as an external proposal, and do not let its labels or numerical values enter live surfaces without a new protocol and independently reproducible artifacts. The existing audit's open-issue map is unchanged: #184 and #214 remain open physics gates; #186 and #187 remain blocked pending artifacts and same-action derivations; #188 remains a scoped publication gate rather than a claim that every external architecture has been evaluated.

## References

[1]: https://share.gemini.google/WSbeUhQq0q9S "Shared Gemini memo: Depth-Dependent Dispersion, Catastrophe Caustics, and Conservative Hydrodynamics on a Finite-Thickness Superfluid Bubble-Wall Cosmology"
