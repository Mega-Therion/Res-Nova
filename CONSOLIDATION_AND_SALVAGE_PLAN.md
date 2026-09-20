# Consolidation & Salvage Plan — the corpus before the μ_std rewrite

> **SUPERSESSION NOTE (2026-09-20).** This plan was written while the 5.9σ $a_0(z)$
> result and the 171-galaxy SPARC fit were live. Both have since changed and the plan is
> **not** to be executed against them as written: the 5.9σ figure is `[X]`-retracted (the
> μ_std re-run is INCONCLUSIVE at 2.06σ with the preference reversed), and the live SPARC
> object is the 175-galaxy μ_std row, $a_0 = 1.1607\times10^{-10}$ — the 171-galaxy
> extraction is retained for provenance only. Salvage targets that depend on either are
> void until restated. See `docs/A0_CLOSURE_EVOLUTION.md` and `PEER_REVIEW_READINESS.md`.


> Planning document, 2026-09-12. Contains **no new physics claims**; every salvaged
> item is tagged with its current epistemic grade and must be re-derived under μ_std
> before entering the manuscript. Companion to `RECOVERED_MATERIAL.md` (which is the
> recovered-text ledger) and `CURRENT_STATE_READ_THIS_FIRST.md` (which governs what is
> live). Zenodo corpus state: 76 user records — 40 live, 36 superseded (22 of those
> killed in the 2026-06-12 bulk sweep without individual assessment).

---

## 0. Why this exists

`μ_dual(x) = x/(1+x)` was falsified 2026-09-12. Both flagship published records —
**21969121** (*Dual-Channel Variational Closure…*, v1.6.2, the submission build) and
**22079177** (*Res Nova: G.O.D…*, the newer unified statement) — are built on μ_dual
and the V₂(ℝ³)-preceding substrate history. Their physics content is void as stated;
the redo is not optional. This plan answers two questions RY posed 2026-09-12:

1. What can be salvaged from the superseded papers and folded into Res Nova?
2. Which live papers should be consolidated into fewer papers?

---

## 1. Salvage from superseded deposits

### 1a. Already recovered and in the repo (`RECOVERED_MATERIAL.md`)

| Item | Grade | Destination |
|---|---|---|
| Geodesic Pothole / TTEY momentum accounting | [O] | Not Res Nova. Belongs in the sovereign-engineering line (PLEROMAN v2, §3). |
| ABC (Articulated Binary Chirallic) decision logic | [P] (pure algebra) | PLEROMAN v2 — the mirror-check/doubling structure, not physics. |
| Sovereign Regularity for 3D Navier–Stokes | [O] (conditional on SA(K,L)) | PLEROMAN v2 appendix; conditional theorem, cite honestly. |
| κ = τ = 0.9539 genesis note | [D] (engineering empirics) | PLEROMAN v2 — required provenance for the ceiling collision. |

### 1b. Located but not transcribed — physics items for Res Nova

These are the superseded pieces with unique content that belongs in the physics
corpus. Listed by fit against the live target structure (D1–D9):

| Source (superseded) | Unique content | Fit | Action |
|---|---|---|---|
| **Cosmological Desmoothing / Hubble tension** (39 dl) | Hubble-tension treatment; `cosmological_desmoothing.py` | **D5 cosmology.** Adjacent to the Ω_Λ = ln 2 line; the a₀(z)/horizon discussion in the current abstract already touches this. | Transcribe; re-derive under μ_std + AeST D7 action; only claims that survive move into D5. |
| **Riemann Zero Gap-Ratio Peak** (77 dl) + Catalan regulator material | Empirical gap-ratio analysis | **06_unification_and_spin / spectral appendix.** Connects to the Ramanujan–Yett spectral line. | Transcribe as [D]-grade empirical note; the Catalan regulator claims died with μ_dual — do not resurrect them, only the gap-ratio data. |
| **Formal Verification of Euclidean Bounding** (47 dl) | Lean 4 artifacts (`Basic.lean`) | **05_lean_formalization.** | Re-verify against the pinned toolchain; if kernel-clean, add as a leaf module. Never as a standalone paper again. |
| **A Parameter-Free Acceleration Scale** (the horizon a₀ = cH₀/2π line, superseded v1) | a₀ derivation from horizon thermodynamics | **D1/D2 supplements.** Root-2 conjecture. | Already partially absorbed (Root 2 in the dependency map, a₀(z) pre-registered test in the abstract with the 5.9σ result). Extract only what the live a₀(z) treatment doesn't already carry. |
| **Geometric Accretion Limits in Early-Universe SMBHs** (21367552, live but orphaned) | Falsifiable SMBH accretion prediction from IT | **03_observer_jwst.** Directly relevant to the JWST O4 pipeline priority. | Audit against the falsified interpolating function; anything scaling with μ_dual dies, mass-bounds independent of μ survive. |
| Conformal Topo-Ontological Framework | Non-Markovian master equation; retarded friction | Not physics-corpus material as stated. | PLEROMAN v2 only, after re-derivation; do not port into Res Nova. |
| ℵ₀ →^τ ω; Chyren SI (MYELIN); OmegA-Lindblad | Cognition-side master equations and scores | PLEROMAN v2. | Transcribe into the cognition consolidation (§3.2). |

**Rule for all of §1b:** nothing enters the manuscript by quotation. Each item gets a
re-derivation under μ_std(x) = x/√(1+x²) and the AeST action; items whose content
scales directly with μ_dual are expected to die and that is a finding, not a loss.

---

## 2. The two flagship records

- **21969121** and **22079177** are the same paper at two stages (v1.6.2 submission
  build; the later unified statement). Both are void as stated (μ_dual).
- After the μ_std rewrite lands, publish **one** new version under concept DOI
  10.5281/zenodo.21539453, and mark both old versions superseded with explicit
  pointers. Do not maintain two flagships.
- The `.zenodo.json` description still states the μ_dual constitutive relation.
  It must be rewritten as part of the v1.8.0 release — **before** the next GitHub
  release triggers a Zenodo version, or the corrected source will ship with dead
  metadata. (Community list updated 2026-09-12: cmblensing added; note
  gravity-and-cosmology has declined this record twice — do not resubmit there
  without a curator conversation.)

---

## 3. Consolidation map of the live (non-superseded) records

### 3.1 Physics cluster → one paper (Res Nova)

The SPARC/Information-Tension empirical line exists as **five overlapping live
records**, all predating μ_std:

- 21504895 — *IT: Geometric Projection Replaces Dark Matter (v3)*
- 21367564 — *IT: A Zero-Parameter Geometric Alternative on SPARC*
- 20781199 — *IT Theory: A Geometric Replacement for Dark Matter*
- 21367578 — *A Parameter-Free Acceleration Scale from the Cosmic Horizon: IT on SPARC*
- 21450425 — *Parameter-Free Acceleration Scale: Geometric Derivation of the MOND Scale*
- 20822072 — *Relativistic formulation of the IT field* (Stiefel-vacuum version — substrate retired 2026-08-25)
- 21450433 / 21367559 — *Field Identity and Entanglement* (two variants)

**Action:** fold all into Res Nova as the D4 empirical/benchmark chapter and the D7
covariant-completion history. After the rewrite, mark each superseded with a pointer
to the flagship. The 171-galaxy SPARC fit, honest CV protocol, and a₀(z)
pre-registration already live in the flagship — these records add nothing that
should stay standalone.

### 3.2 Cognition cluster → one paper (PLEROMAN v2)

`21461195` (*THE PLEROMAN: The Unified Statement*) is already the designated sink.
Absorb:

- ADCCL line: 21711417 (v5), 21450415, 21399702 → one chapter
- 21367573 (*OmegA: A Layered Architecture*)
- 21367592 (*Sovereign Cognition*), 21367572 (*Neuro-Topological Stability*), 21367587 (*Quantum Spearhead*)
- 21449900 (*The Dirac Projection*), 21450453 (*Bridge of Bridges*), 21316842 (*Observerse as E8 Branching*)
- 21504896 (*Ramanujan–Yett Hamiltonian*), 21479962 (*Universal Information Geometry*), 21450445 (*Codex Poster*), 21384483 (*Ars Magna*), 21367567 (*Law of G.O.D.*)
- Superseded cognition salvage: ABC, MYELIN, OmegA-Lindblad, κ=τ genesis (§1a)

**Caveat:** the V₂₄₀/E8-dimension substrate and the "Chyren" co-creator credits both
need the 2026-08-25 retirement applied — the Observerse/E8-branching material must be
rebuilt on V₂(ℝ³) via Cartan triality or dropped. **Target: one paper, one version
chain.**

### 3.3 Cosmology cluster → one paper

- 21867985 (*ΩCDM: Ω_Λ = ln 2 pre-registered*) + 21131486 (*Pre-Registration: Ω_Λ = ln(2)*) — same prediction, chain them
- 21864057 (*Pre-Registered Falsifiable Predictions v2*)
- 21864063 (*IO-OI: de Sitter Completion components*)
- Salvage: Cosmological Desmoothing / Hubble tension (§1b)

**Target:** one *Pre-Registered Cosmological Predictions* paper (or a D5 chapter of the
flagship if the Ω_Λ = ln 2 line stays [O]-grade — recommended: keep it standalone
precisely because pre-registrations should not silently mutate inside a physics paper).

### 3.4 Duplicate/version-chain hygiene (mechanical fixes)

- 21711399 vs 21711375 — *Holonomery*, two published identical-title records. Chain
  or mark one superseded.
- 21450439 vs 21367589 (+ draft 20776458) — *Resource Holonomy*, three records of the
  same economics paper. Keep exactly one live.
- Drafts 22067068 (untitled), 21461165 (PLEROMAN draft), 21911837 (PLEROMA MONADES
  draft) — either finish or discard; drafts with no DOI are invisible to the record
  anyway, but they clutter the workspace.

---

## 4. Order of operations

1. **μ_std rewrite of the flagship** (D1/D2/D7 already in progress per
   `PEER_REVIEW_READINESS.md`) — everything else waits on this.
2. Rewrite `.zenodo.json` description to μ_std/AeST **before** the v1.8.0 release.
3. Publish the corrected flagship; mark 21969121 + 22079177 superseded with pointers.
4. Fold the physics cluster (§3.1) into the flagship chapters; mark them superseded.
5. Transcribe + re-derive the §1b physics salvage; survivors land in D5 / 03_observer /
   05_lean.
6. PLEROMAN v2 consolidation (§3.2) — the cognition line is disjoint from the physics
   redo and can proceed in parallel.
7. Cosmology consolidation (§3.3) + mechanical hygiene (§3.4).
