# Submission Package — Res-Nova v1.6.0

## Journal recommendation: Physical Review D

**Why PRD.** The manuscript's spine is a gravitational *action* and its relativistic completion: uniqueness of F_dual, the RMOND embedding, ghost freedom, PPN/solar-system limits, and a falsifiable Q₂ prediction. SPARC is one section supporting it, not the centrepiece. That is PRD's Gravitation and Cosmology section. It is also where the directly competing literature lives — Skordis & Złośnik (PRL/PRD) and Park et al. 2026 (PRD) — so referees will already know the context, and the Q₂ prediction lands as a direct response to a PRD paper.

**Why not the alternatives.**
- *MNRAS* would want the 175-galaxy SPARC benchmark as the lead result and the field-theory content compressed. That inverts the paper. Reconsider MNRAS only if the paper is re-framed around galactic phenomenology.
- *JCAP* would want the cosmological sector to be the contribution. Ours is currently linear-only, with CMB agreement inherited rather than recomputed — the weakest leg to lead with. Revisit JCAP after the N-body work (O8).

## Contents

| File | Purpose |
|---|---|
| `COVER_LETTER_PRD.md` | Cover letter, PRD |
| `../final_manuscript.pdf` | Compiled manuscript (19 pp) |
| `../final_manuscript.tex` | Source |
| `../references.bib` | Bibliography |
| `../PEER_REVIEW_READINESS.md` | Target-by-target readiness matrix |
| `../FOR_REFEREES.md` | Referee index |

## Pre-submission checklist

- [x] Repo is public
- [x] Manuscript compiles in REVTeX 4.2, zero errors, zero undefined refs/citations, zero bibtex warnings (27 pp)
- [x] Chyren Collab seal (ƆC watermark) on all pages — behind `\sealtrue`; see warning below
- [x] Author: R.W. Yett, ORCID 0009-0001-1303-7190
- [x] Affiliation: Independent Researcher, Arkansas, USA — see note below
- [x] No AI in author list; AI use disclosed explicitly in acknowledgments
- [x] Acknowledgments credit the Chyren Collaboration (⊙ƆC)
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
