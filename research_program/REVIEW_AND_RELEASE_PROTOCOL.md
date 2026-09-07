# Res-Nova Review and Release Protocol

**Purpose.** This protocol governs how Res-Nova moves from exploratory work to a public research claim. It operationalizes the existing `AGENT_COVENANT.md`; it does not create new scientific results.

## 1. Core principle

> A claim is released at the strength of its **best reproducible artifact**, not at the strength of its most persuasive prose.

Every release must preserve a trace from statement to source inputs, computation/formal proof, result artifact, independent review, and claim-ledger line. If one link is absent, the item remains `[O]`, `[C]`, a method note, or an explicitly limited engineering result.

## 2. Roles and separation of responsibilities

A small independent program may have one person in several roles, but the artifact trail must still distinguish them.

| Role | Responsibility | May not do alone for a promoted result |
|---|---|---|
| Principal investigator | Chooses research questions, approves scope, protects scientific boundaries. | Treat an exploratory outcome as independently replicated. |
| Primary analyst/theorist | Implements calculation, proof, data pipeline, or numerical scan. | Approve their own result as independent reproduction. |
| Data steward | Records source, licensing/citation requirements, release version, checksum, and access conditions. | Replace or preprocess data without a manifest change. |
| Formal verifier | Maintains theorem inventory, toolchain pins, proof receipts, and axiom/placeholder checks. | Translate a formal theorem into a broader physical conclusion without a ledger boundary. |
| Adversarial reviewer | Attempts reproduction and actively searches for hidden assumptions, mismatched comparators, leakage, and overclaiming. | Rewrite the primary result before preserving the original review finding. |
| Release editor | Ensures manuscript, README, Zenodo metadata, plots, and ledger use the same wording and numbers. | Override the ledger or remove a negative result to simplify presentation. |

For a single-researcher period, the minimum substitute for independent review is a clean-room rerun from a separate machine/account/environment plus a signed self-review declaring that it is not independent. Before a major empirical or cosmological paper is submitted, Res-Nova should seek at least one external domain reviewer.

## 3. Evidence and release classes

| Release class | Permitted content | Required review |
|---|---|---|
| Exploratory notebook or branch | Hypothesis generation, preliminary plots, debugging, negative leads. No result language. | Internal only; clearly labelled non-citable. |
| Method release | Data fetcher, formal tooling, likelihood replication, or benchmark implementation. | Clean-run test and reproducibility artifact. |
| Formal result release | A stated theorem, assumptions, Lean source, proof receipt, and theorem-to-prose check. | Cold-run verification plus formal review. |
| Empirical result release | Frozen inputs, declared model, uncertainty method, result JSON, diagnostics, and model-comparison contract. | Independent rerun or documented failed replication. |
| Constraint/viability release | A named theory branch under explicit assumptions, conditions tested, allowed/excluded/unresolved map. | Theory review plus numerical/derivation reproduction. |
| Paper/repository release | A bounded scholarly claim combining the relevant prior artifacts. | Release-editor audit and at least one non-author critical reading for major papers. |

## 4. Mandatory release checklist

A release cannot advertise a new `[P]` or `[D]` claim without all applicable entries below.

| Requirement | Formal result | Empirical result | Both |
|---|:---:|:---:|:---:|
| Stable experiment/result ID | ✓ | ✓ | ✓ |
| Claim text with an explicit boundary sentence | ✓ | ✓ | ✓ |
| Pinned source revision and release tag | ✓ | ✓ | ✓ |
| Machine-readable manifest | ✓ | ✓ | ✓ |
| Environment/toolchain lock | ✓ | ✓ | ✓ |
| Input provenance and checksum | where applicable | ✓ | ✓ |
| Theorem inventory / assumptions / axiom report | ✓ | — | ✓ |
| Declared model, priors, comparator flexibility | — | ✓ | ✓ |
| Negative controls or failure fixtures | ✓ | ✓ | ✓ |
| Review log and reproduction result | ✓ | ✓ | ✓ |
| Ledger update in the same change set | ✓ | ✓ | ✓ |
| Manuscript/README/metadata wording audit | ✓ | ✓ | ✓ |

## 5. Adversarial review questions

The reviewer must answer each applicable question in writing.

1. **Statement drift:** Does the prose claim exactly match the theorem or result object, including assumptions and scope?
2. **Reproducibility:** Can a clean environment run the declared path using only documented inputs?
3. **Data provenance:** Are original data release, transformations, exclusions, and checksums visible and justified?
4. **Comparator fairness:** Do competing models have matched nuisance freedom, priors, data treatment, optimization budget, and score definition?
5. **Uncertainty integrity:** Are correlations, galaxy-level resampling, calibration/systematic uncertainty, and model uncertainty treated at the level implied by the claim?
6. **Leakage:** Can any global parameter, preprocessing choice, or selection rule leak from training into test/validation?
7. **Assumption completeness:** Are stability, screening, initial/boundary conditions, and regime restrictions stated rather than silently inherited?
8. **Negative evidence:** Did declared controls fail where they should fail, and do they expose any pipeline pathology?
9. **Alternative explanations:** Is the outcome distinguishable from known baselines, selection effects, or calibration choices?
10. **Communications audit:** Are titles, abstracts, figures, press language, and repository badges no stronger than the ledger?

The answer “not yet known” is acceptable and must be recorded as an open condition. It may not be edited into an affirmative claim by rhetoric.

## 6. Reproducibility artifact standard

Every completed work package receives a directory or release asset with this minimum structure:

```text
reproducibility/
  RNP-YYYY-NNN/
    README.md                 # question, claim boundary, exact execution steps
    manifest.json             # source revisions, hashes, data version, result IDs
    environment/              # lockfile, container definition, toolchain pins
    inputs/                   # checksums and retrieval instructions, not restricted data
    scripts/                  # deterministic entry points
    outputs/                  # result JSON, figures, tables, diagnostics
    logs/                     # clean-run and reviewer logs
    review/                   # review memo, reproduction status, issue log
    CITATION.cff              # if the artifact is independently citable
```

The top-level README must state whether the data are redistributed, fetched, access-controlled, or unavailable. If data cannot legally be redistributed, the manifest and retrieval script are still required.

## 7. Claim-ledger update rule

The ledger update belongs in the same pull request or release commit as the artifact. It must include:

- an identifier;
- an allowed tag (`[P]`, `[D]`, `[C]`, `[O]`, superseded, or withdrawn);
- the exact artifact path and source revision;
- the narrowest defensible claim;
- what the item **does not** establish; and
- any new dependency or open condition.

A failed replication, a negative control failure, or a retired analysis must receive a permanent, searchable record. It may be superseded but never erased from provenance.

## 8. Paper and public-communication gate

A paper may enter preprint or journal submission only after the following answer is “yes.”

| Gate question | Required answer |
|---|---|
| Is there one primary question and one primary result? | Yes; secondary ideas are explicitly separated or removed. |
| Is the central result reproducible from a versioned release? | Yes, or the paper says it is a theory/method proposal rather than a result. |
| Are competing hypotheses and negative controls described? | Yes. |
| Is every numerical statement linked to a machine-readable artifact? | Yes. |
| Does the abstract avoid claims stronger than the ledger? | Yes. |
| Is there a limitations and failure-conditions section? | Yes. |
| Has a non-author attempted a critical reading or rerun? | Yes for major formal/empirical submissions; otherwise state the limitation. |
| Have data and software citations/licenses been checked? | Yes. |

## 9. Governance cadence

The program will use a lightweight monthly cycle:

| Meeting/review | Output |
|---|---|
| Claim audit | Changes to the ledger, quarantines, and wording corrections. |
| Reproducibility audit | Status of clean-run paths, lockfile drift, data accessibility, and CI artifacts. |
| Research review | Go/no-go decision on each experiment registry item and assigned red-team task. |
| External horizon scan | Updated literature/data watch list; no result promotion from literature alone. |
| Release audit | Decision to tag a method, formal, empirical, or paper release. |

## 10. Stop conditions

Res-Nova should pause or retire a branch when: the stated theory cannot meet a declared gate under its assumptions; the evidence is not identifiable from the available data; continuing requires loosening standards after outcomes are known; the baseline cannot be reproduced; or a claimed unification adds no discriminating prediction beyond existing phenomenology. Stopping a branch is a successful act of scientific governance.
