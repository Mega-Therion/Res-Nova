# Submission Package — Res-Nova v1.6.0

## Journal recommendation: Physical Review D

**Why PRD.** The manuscript's spine is a gravitational *action* and its relativistic completion: uniqueness of F_dual, the RMOND embedding, ghost freedom, PPN/solar-system limits, and a falsifiable Q₂ prediction. SPARC is one section supporting it, not the centrepiece. That is PRD's Gravitation and Cosmology section. It is also where the directly competing literature lives — Skordis & Złośnik (PRL/PRD) and Park et al. 2026 (PRD) — so referees will already know the context, and the Q₂ prediction lands as a direct response to a PRD paper.

**Why not the alternatives.**
- *MNRAS* would want the 175-galaxy SPARC benchmark as the lead result and the field-theory content compressed. That inverts the paper. Reconsider MNRAS only if the paper is re-framed around galactic phenomenology.
- *JCAP* would want the cosmological sector to be the contribution. Ours is currently linear-only, with CMB agreement inherited rather than recomputed — the weakest leg to lead with. Revisit JCAP after the N-body work (O8).

## Contents

The  PDF  inputs these  three  sources, so  they  travel  with the  TeX: `publication/jewel_scope.tex`, `publication/canonical_citation.tex`, and `reproducibility_appendix.tex`.

| File | Purpose |
|---|---|
| `COVER_LETTER_PRD.md` | Cover letter, PRD |
| `../res_nova_manuscript.pdf` | Compiled manuscript. The 2026-10-17 rebuild is the file to send. |
| `../res_nova_manuscript.tex` | Source |
| `../publication/jewel_scope.tex` | In/out box, printed before the title |
| `../publication/canonical_citation.tex` | Concept DOI and the historical v1.6.2 pointer |
| `../reproducibility_appendix.tex` | Lean inventory appendix |
| `../references.bib` | Bibliography |
| `../FOR_REFEREES.md` | Referee index |
| `../PEER_REVIEW_READINESS.md` | Readiness matrix. Quote only the 2026-10-09 score at the top. |
| `../CURRENT_STATE_READ_THIS_FIRST.md` | Live ledger. It wins if the PDF disagrees. |
| `../02_galaxy_dynamics/PARAMETER_LEDGER.json` | Tier 0 and Tier 1 medians printed in the table |
| `../02_galaxy_dynamics/NFW_CONSTRAINED.json` | NFW rows 1.92 and 5.62 |
| `../02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json` | T1 a₀ and the 95% interval |
| `../02_galaxy_dynamics/CASSINI_EFE_QUADRUPOLE_2026-09-27.md` | Quadrupole behind the abstract's ≈4.6σ |
| `../02_galaxy_dynamics/fetch_sparc.sh` | Fetches the rotation curves. They are not in git. |
| `../VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256` | SHA-256 list the fetch checks |
| `../05_lean_formalization/` and `verify_all_proofs.sh` | Formal modules the appendix points at |

Left  out  on purpose:  `SPARC_MODEL_COMPARISON.md`,  `COVARIANT_DUALITY_SCREENING_ACTION.md`, `DUALITY_SCREENING_ACTION.md`,  the  RYTT  treatises, and  the separate tidal-screen Zenodo notes.

## Pre-submission checklist

- [x]  Repo  is public
- [x]  Manuscript  compiles in  REVTeX  4.2.  The 2026-10-17  `latexmk` run exited 0 and wrote 34 pages. The log has overfull boxes and three floats that do not fit the page.
- [x] Chyren Collab seal (ƆC watermark) on all pages — behind `\sealtrue`; see warning below
- [x] Author: R.W. Yett, ORCID 0009-0001-1303-7190
- [x] Affiliation: Independent Researcher, Arkansas, USA — see note below
- [x] No AI in author list; AI use disclosed explicitly in acknowledgments
- [x] Acknowledgments contain no non-human or institutional co-credit
- [x] Cover letter has 4 suggested referees
- [x] Data Availability Statement points to the public repo
- [x] `.zenodo.json` in repo root
- [x] All external citations verified against primary sources
- [x] Constitutive-relation error from v1.5.0 corrected and disclosed in-text
- [x] v1.6.1 tagged and GitHub release created with PDF asset
- [ ] **Zenodo DOI minted** — requires RY's Zenodo login; see below
- [ ] **Zenodo communities** (Gravity and Cosmology, CMBlensing) — same
- [ ] **ORCID auto-link via DataCite** — same
- [ ] **DOI badge in README** — blocked on the DOI existing
- [ ] **Submission itself** — held. See below.

## Two things to decide before you upload

**The seal.** It is on by default for the repo and Zenodo copies. For the APS upload I recommend building with `\sealfalse` (one word in the preamble). A watermark on every page of a submitted manuscript reads as a draft stamp or a rights mark to production staff, and some journals bounce decorated submissions at technical check. Your call; the switch makes it trivial either way.

**Affiliation.** Recorded as "Independent Researcher, Arkansas, USA". You said you were formerly a UofA student without current .edu access. An affiliation line asserts *current* institutional standing to the publisher and to DataCite, so a past enrolment does not support it — and it is the kind of thing that gets checked. If you want the connection visible and accurate, the normal form is a sentence in the acknowledgments ("the author was formerly a student at the University of Arkansas"), not the affiliation field.

## On submitting

Submission is not automated here and was not performed. It is an irreversible, outward-facing action under RY's name and ORCID, it requires his APS account credentials, and it is governed by the standing publish gate. The package above is complete and ready for him to upload; the four unchecked items above should be settled first.
