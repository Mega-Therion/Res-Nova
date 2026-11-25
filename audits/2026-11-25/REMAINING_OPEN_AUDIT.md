# Res Nova remaining-open audit

**Repository:** `Mega-Therion/Res-Nova`  
**Audited commit:** `212b55a8da278f1363d82642b736fc7ef30dee7c`  
**Audit date:** 2026-11-25  
**Scope:** seven open GitHub issues, current physics ledgers, public-facing surfaces, external-source boundaries, and available verification gates.

## Bottom line

The repository's local Python/data/documentation gate is green at the audited commit: `bash scripts/local_gate.sh` completed with `LOCAL GATE: PASS` and all 36 listed checks passed. This is a reproducibility and claim-hygiene result, not empirical validation of the theory. The Lean gate was not freshly executable in this sandbox because `lake`/Mathlib are absent; committed CI evidence remains the basis for the repository's stated 98/98 Lean result. No new physics claim is promoted by this audit.

The remaining work is not one homogeneous backlog. Issue #183 is documentation/provenance work and is closeable after the exact source artifacts are cross-linked and the gates are rerun. Issues #184 and #214 are genuine open physics calculations. Issues #185, #186, #187, and #188 are blocked by account-side deployment access, external/unmirrored artifacts, or the need for an independent same-branch rerun. The correct end-to-end pathway is therefore staged closure, not a blanket “all open issues resolved” claim.

## Issue-by-issue closure map

### #183 — primary-source figures, a₀, and ν₆ provenance

**Status: CLOSEABLE NOW, after documentation/provenance correction.** The numerical material already exists in repository artifacts. `02_galaxy_dynamics/SECOND_FIELD_GATES.json` contains the pinned `a₀`, external-field inputs, `Q₂` values, sigma calculations, and the bare-`μ_std` result. `A0_DISTANCE_CORRECTED_2026-09-16.json` distinguishes the 175-galaxy/3,391-point T1 extraction from the 171-galaxy/3,375-point comparison subset. The ν₆ records explicitly scope the Oort, wide-binary, and dwarf results to their tested proxies rather than a complete law. `SCREENED_C_WINDOW_2026-10-16.md` and `GALAXY_LAW_SCOPE_2026-11-21.md` preserve the withdrawal of the old solar-system gate on `μ_std`.

The closure action is to make the live source-of-truth prose cite those exact artifacts, retain separate input values and catalog subsets, and label each ν₆ result by its actual proxy. Do not retune parameters and do not convert a proxy result into a full covariant closure. After the wording change, rerun the claim-consistency, registry, publication-metadata, and full local gates. This audit does not silently close the GitHub issue because the public issue and any desired source-of-truth edits remain maintainer actions.

### #184 — nonspherical AeST EFE/Cassini response for the total-law branch

**Status: OPEN PHYSICS.** The in-tree total-law correspondence is spherical, aligned-gradient, and negligible-mass-term evidence. It is not an AeST nonspherical EFE solution. A QUMOND calculation is explicitly insufficient for this issue.

The next permitted gate is a frozen total-law action and normalization, fixed boundary conditions and external field, a full-AeST numerical formulation, mesh/box and solver convergence, raw machine-readable outputs, and an independently written check. The result may be PASS, FAIL, or INCONCLUSIVE. A failure would close the tested route negatively; it would not falsify every Res Nova branch.

### #185 — Vercel checks and production alignment

**Status: BLOCKED BY EXTERNAL OPERATIONS.** The issue records Vercel `build-rate-limit` failures, absent deployment evidence for the then-current main SHA, and production projects on different source SHAs. Official Vercel documentation confirms that deployment/build quotas can require waiting for capacity to reset. This is not evidence of a source-code or physics regression.

The owner-side closure sequence is: confirm the account/project limit has reset; deploy the intended current main SHA to both named projects; verify both production deployments are `READY` and identify their source SHAs; run HTTP smoke checks; then record URLs, logs, and GitHub status conclusions. A preview deployment is not a substitute for production alignment. No account-side deployment was attempted in this audit.

### #186 — covariant screening after the C3 mass-term no-go

**Status: BLOCKED PENDING ARTIFACTS AND A NEW FROZEN GATE.** The C3 mass-term conclusion remains Muse-reported until the source artifacts are mirrored and independently audited. The old Vainshtein requirement must be recomputed because the issue identifies a retracted input in the earlier number. The remaining named route is an aether-projected/non-Horndeski operator compatible with the current tensor-speed constraint.

The next step is to mirror the C3/ν₆ records, recompute the corrected screening requirement, freeze the exact operator basis and units, and run a preregistered solar-system observable gate with an independent implementation plus a galactic/SPARC consequence check. Until then, the repository should not say that a covariant screen exists or that the remaining route is excluded.

### #187 — complete ν₆-total AeST embedding

**Status: BLOCKED PENDING EXTERNAL ARTIFACT MIRRORING AND SAME-ACTION DERIVATION.** The cited pass-2 material is not an inspectable repository checkout and is explicitly not a full covariant derivation or adoption. The in-tree spherical correspondence cannot substitute for the requested same-action derivation, non-spherical limit, stability proof, or SPARC gate.

The closure path is to mirror the exact J₆-total workspace, scripts, raw JSON, dependency versions, and source revision; freeze the action and conventions; derive all field equations and boundary terms from that action; prove the spherical and AQUAL-limit mappings; derive `c_T`, PPN, ghost, and gradient conditions on the same branch; and run the fixed-nuisance SPARC gate against MOND/NFW with independent reproduction. The λs=0.5 status remains unresolved unless both implementations converge under the stated tolerance.

### #188 — publication gate

**Status: BLOCKED; PARTIALLY PACKAGEABLE NOW, NOT CLOSABLE AS “SUBMISSION-READY.”** The repository can already assemble a narrower evidence ledger and manuscript scope, but the issue requires canonical action/convention reconciliation, an independent clean-environment rerun, same-branch C2/C3 checks, and explicit failed/tuned-branch disclosure. D7 branch selection, the total-law nonspherical gate, high-redshift calibration, cluster outskirts, and nonlinear structure formation remain outside a fully closed publication claim.

The immediate safe deliverable is a scoped manuscript package that calls the SPARC and cosmological results what they are, keeps `a₀ = cH₀/(2π)` and `ΩΛ = ln 2` quarantined as unproved conjectural/declared material, preserves `[X]` routes, and identifies the missing same-branch gates. Publication closure requires the independent rerun and the explicit decision to submit only the narrower result or to wait for those gates.

### #214 — AeST spherical boundary/source robustness

**Status: OPEN PHYSICS.** The v0.5 work is a bounded sensitivity audit using the existing point-source solver and an analytic literature estimate. It does not provide a full extended-source integration. The tested boundary perturbations still encounter negative condensate density before the nominal 5% extent, and profile scaling is only leading-order.

The next gate must freeze one D7 action/normalization and source profile, solve the full extended-source two-field boundary-value problem through the sign-change regime, test numerical stability and boundary selection, and compare scalar-channel and total-law branches under identical inputs. The output must include raw per-run data, convergence diagnostics, and a PASS/FAIL/INCONCLUSIVE verdict. A nominal sensitivity sweep is not a closure of this gate.

## Cross-cutting stale-surface findings

The Research Atlas prose had already incorporated the 2026-11-21/25 corrections, but its release pointer still named `708ddcc2`, one commit behind the audited repository. This audit updated only the pointer to the audited short SHA `212b55a8` and advanced the curated claim snapshot date to 2026-11-25. No scientific prose, model parameter, dataset, nuisance policy, or acceptance criterion was changed by that edit.

`PEER_REVIEW_READINESS.md` and `RELEASE_CHECKLIST.md` contain prominent supersession warnings. Their older historical sections should remain intact for provenance, but current-facing readers must use the dated top-level score and the 2026-11-21 scope update. The release checklist still describes a historical 43-target Lean gate in an unchecked historical context while the current state records 98/98 CI targets; this is not a fresh Lean failure, but it is a documentation debt item for a future release-cleanup pass.

The five claim-registry falsifiability warnings reported by `validate_claim_registry.py` name no matching Lean declaration for CLM-02, CLM-11, CLM-14, CLM-16, and CLM-D9-02. The registry gate passes, so these are traceability warnings rather than failed claims. They should be resolved either by naming the actual non-Lean falsifier or by adding a matching formal declaration; they must not be “fixed” by inventing theorem names.

## Verification and evidence boundaries

Freshly executed in this audit cycle: the full pinned-dependency local gate passed; individual claim-consistency, publication-metadata, HF-card, and related checks passed; the hub-drift check identified the stale release pointer and it was corrected. Fresh Lean execution was blocked by missing `lake`/Mathlib. The committed CI receipt for the stated 98/98 suite remains repository evidence, not a local rerun. No production Vercel deployment was made, no external account was changed, and no unmirrored Notion result was promoted.

The external literature supports the boundaries used here. Skordis–Złośnik establishes the scope of the published AeST construction and its reported linear-cosmology/second-order stability results, not Res Nova's unresolved branch choices. The SPARC paper establishes the 175-galaxy empirical dataset and its mass-model context, not a covariant validation. Vercel's rate-limit documentation supports the operational classification of #185. GitHub's status-check documentation supports separating CI conclusions from scientific evidence. The source ledger is in `audit-external-sources.md`.

## Recommended order of work

First, finish #183's source-of-truth cross-links and close the documentation loop. Second, obtain owner-side Vercel evidence for #185 if production alignment is still desired. Third, mirror the external artifacts required by #186 and #187 before doing any new derivation. Fourth, freeze the narrower publication ledger for #188 without waiting for every physics question, but do not label it submission-ready until the issue's independent rerun and same-branch requirements are met. Finally, treat #184 and #214 as separate preregistered numerical programs with negative results preserved as valid outcomes.

## References

[1]: https://arxiv.org/abs/2007.00082 "A new relativistic theory for Modified Newtonian Dynamics"
[2]: https://arxiv.org/abs/1606.09251 "SPARC: Mass Models for 175 Disk Galaxies with Spitzer Photometry and Accurate Rotation Curves"
[3]: https://vercel.com/docs/limits "Vercel limits"
[4]: https://docs.github.com/en/pull-requests/reference/status-checks "GitHub status checks"
