# Four-Bucket Porting Sort: res-extensa and Auroboryai

**Date:** 2026-11-18
**Pinned inputs:** `res-extensa` at `0cb47466926c479bf85a039ad6039db7cd37a772`; `Auroboryai` at `82045372cb63939395cde8abeeddc8cd42dbe221`; `Res-Nova` baseline at `c4a0f42cc334d9a04ea59f4f758afac257e55dd1`.

**Purpose.** The legitimacy audit in this directory answers whether each item is correct. This document answers the next question: which bucket does it go in, under the four-bucket rule fixed on 2026-11-18 (Port to Lean 4 / Keep as standalone `[P]` / CAS cross-check / Quarantine or Drop).

**Headline.** The port bucket is empty. Nothing in either audited repository is a load-bearing theorem that Res-Nova does not already hold, so the Lean CI gate blocks no porting work. Three `IMPLEMENTED_NOT_EXECUTED` rows could be closed by adding a toolchain and a `coqc` step, which needs no queue and no permission.

---

# Part 4. Four-Bucket Sort for the Porting Decision

The audit above answers "is it legitimate". This part answers the next question, which is the one that decides whether anything gets ported: **which bucket does each item go in.** The four buckets are the ones fixed in the 2026-11-18 lane directive.

The short answer: **the port bucket is empty, and that is a finding rather than a failure.** Nothing in either audited repository is a load-bearing theorem that Res-Nova does not already hold. The gate on Devin's CI queue therefore does not block any porting work, because there is no porting work to block.

## 4.1 Bucket 1: Port to Lean 4

**Contents: none.**

One candidate was evaluated and rejected on its merits.

| Candidate | Why it looked port-worthy | Why it is not |
|---|---|---|
| The polar-slope realization of `mu_std` (`mu_std(kappa/h) = kappa` on `kappa^2 + (1-theta)^2 = 1`) | It is a geometric theorem about the constitutive function, the only object in the corpus that a covariant action has to contain | It is **selection-free**. Res-Nova's `REPRESENTATION_AUDIT_MU_STD_2026-09-16.md` already proves the whole `C`-class (E1 to E12, including the Gudermannian row E6) and states of it: "No row adds selection content." A theorem that adds no selection content cannot change any equation, so it fails the "needs to compose" test. Porting it would add a line to the ledger and no physics |

Everything else that *is* load-bearing is already in Res-Nova, and the audit confirmed each by name:

| Load-bearing item | Already in Res-Nova | Status |
|---|---|---|
| Vector EOM coefficient `b B^nu` (not `2 b B^nu`) | `AeSTVectorNoetherResidual.lean` | `[P]`, and it is the one item that changes an equation |
| Stability ceiling `0 < K_B < 2`, `0 <= lambda_s < 11.2788` | `AeSTTotalScalarCorrespondence`, `Wave3BBNAndSpinCCP2Bounds.lean` | `[P]`, verifier exit 0 |
| BBN no-go `jtot_bbn_5pct_impossible` | `Wave3BBNAndSpinCCP2Bounds.lean` | `[P]`, registered in `lakefile.lean` |
| Legendre/Hessian structure and the `mu = 0` rank drop | `AeSTHamiltonianLegendre.lean` | `[P]` |
| `2T` versus `O` non-isomorphism | `GroupFacts` equivalent already proved in res-extensa; Res-Nova holds the group-theory layer | `[P]`, finite, and composes with nothing |

## 4.2 Bucket 2: Keep as standalone `[P]`

**Contents: one file, and it needs a receipt before it can be cited.**

| Item | Claim | What is missing |
|---|---|---|
| `Auroboryai/formal/coq/Dimensions.v` | Eight natural-number identities by `lia` and `reflexivity`. Zero `Admitted`, zero `Axiom`, zero `Parameter`, no external library beyond stdlib `Arith` and `Lia` | **No `coqc` receipt exists.** Neither repository records a `coqc` run, and `coqc` is absent from the audit sandbox. Under the corpus's own rule a file is not `[P]` until a build receipt exists, so this is `IMPLEMENTED_NOT_EXECUTED` until someone runs `coqc Dimensions.v` and records the exit code |
| `Auroboryai/formal/isabelle/Dimensions.thy` | The same eight identities by `simp`, no `sorry`, no `oops`, no `axiomatization` | The file **declares its own non-compilation** in its header ("written 2026-11-10; not yet compiled against an Isabelle install"). Not `[P]` |
| `res-extensa/synthesis/12_BandCircle.lean`, `13_GroupFacts.lean`, `14_SovereignConstants.lean` | 63 theorems, zero `sorry`, zero custom axioms, kernel `decide` and `linarith` only | **No `lakefile.lean`, no `lean-toolchain`, no CI.** The repo cannot build its own proofs. Two of its four recorded outputs are zero-byte files. These are `[arith]` under `docs/EPISTEMIC_TIER_LEGEND.md` and cannot be promoted without a toolchain |

**The one action this bucket needs:** add `lakefile.lean` and `lean-toolchain` to `res-extensa` and a `coqc` step to `Auroboryai`, then record the exit codes. That is cheap, and it converts three `IMPLEMENTED_NOT_EXECUTED` rows into either `[P]` or a real failure. It is not a port and does not need Devin's queue.

## 4.3 Bucket 3: Cross-check in CAS (SymPy / Wolfram / Cadabra / xAct)

**Contents: five items. This is where the genuine verification value sits.**

| Item | Tool | Why CAS and not Lean | Status |
|---|---|---|---|
| The `f(Q, Box^-1 Q)` Cassini dimensional and derivational failure | SymPy | It is a units-and-scaling argument on a specific potential, not a theorem | **Already scripted**: `res-extensa/synthesis/05_q2_recompute.py`, exit 0. The strongest artifact in either repo |
| `L_IT = 2 F_std` and `dL_IT/dy = mu_std` | SymPy, symbolic | A calculus identity between two potentials. Numerically verified here to `0.0e+00`; symbolic is the citable form | Verified numerically, symbolic form outstanding |
| The Gudermannian and polar-slope identities as one statement | SymPy | Transcendental identity; Lean would need a real-analysis library for `arsinh` and `gd` | Numerically verified to `1e-12` here; Res-Nova's script already covers the `C`-class |
| 4D tensor variation, characteristic speeds, `C^{AB}` determinant on FLRW | **xAct / Cadabra** | Index-symmetry work at the tensor level. This is the one place where a CAS genuinely beats both Lean and hand algebra | **Not attempted anywhere in the corpus.** The `c_s` and `c_T` results are stated as `[D]` from cited literature, not recomputed from the action in a CAS |
| E8 root and shell counting | SymPy | Trivial integer arithmetic | `formal/sympy/check_dimensions.py` exit 0, 8/8 |

**The single highest-value CAS job the audit identifies:** a `xAct` recomputation of the perturbation speeds `c_s^2` and the tensor speed `c_T` directly from the assembled action, at the `K_B` and `lambda_s` values the BBN ceiling leaves alive. The corpus asserts `c_T = c` structurally and `c_s < c` conditionally; nobody has run the characteristic analysis in a tensor CAS. That is `[D]` work, it belongs in Bucket 3, and it does not touch Lean.

## 4.4 Bucket 4: Quarantine `[X]` or Drop

Two distinct things live here, and the lane directive separates them correctly. **Falsified** is not the same as **out of lane**.

### 4.4.1 `[X]` Quarantined (Lane 4)

| Item | Where it appears | Verdict |
|---|---|---|
| `MuDual`, `mu = x/(1+x)` | `res-extensa` `CLM-RO0-004`, `01_resnova_ledger.md`, retraction ledger | `[X]` as physics (the `1/x` tail). The derivative identity `F_dual' = x mu_dual` is correct `[P]` mathematics and stays as historical mathematics |
| `MuExp`, `mu = 1 - e^{-x}` | Absent from both repos | `[X]`, not present. **Watch the near-collision:** `extended-works` cites a `nu`-function `nu_6(y) = (1 - e^{-sqrt y})^{-1}`, which is a `nu` in the Newtonian variable, not a `mu` in `x`. It must carry the label `nu`-function in every future citation |
| Bare unscreened `mu_std` in the Solar System | `05_cassini_recompute.md`, ledger `CAS-2` | `[X]`. Auditor recomputation gives `+8.56 sigma` from `Q_2 = 1.7e-26` against the 2026 bound; the adjudicated corpus value is `+8.73 sigma` (BLK-1516, O49, with `arXiv:2602.17884`) |
| Pure single-scalar k-essence, `C^{AB} -> 0` at `mu = 0`, `c_s^2 -> 2` | Not asserted in either repo; diagnosed in Res-Nova | `[X]`. The rank drop is *located* (`C_AB_mu_zero_shell_rank_drop`) and the Hessian is proved nondegenerate off shell, which is the correct treatment |
| Additive anti-Hermitian GKSL terms | Not asserted; `synthesis/02_hood_claim_map.md` C26 audits the gate as assumed model with `Tr = 1` | `[X]`. Any future use keeps Lindblad form |
| `CartanTrialityGenerations` as a 3-generation derivation | Res-Nova `05_lean_formalization/` | `[X]`, already retracted by Res-Nova itself (`audits/PHYSICS_FOUNDATIONS_AUDIT_2026-11-13.md` line 30) |
| `T_1^2 = 0` Euclid shear estimator | Absent | `[X]`, not present. `T_1` in the corpus is the qubit relaxation time in `T_2 <= 2 T_1` |
| Paper C's seven-sector master Lagrangian | `Auroboryai` Paper C | **Quarantine as a covariant completion.** Conformal-dilaton gravity plus a universal `f(chi) L_m` fifth force, on a "retired substrate frame". Not falsified, just not composable with the AeST baseline |
| Paper E's `xi R Phi^2` at `xi = 0.127` | `Auroboryai` Paper E | **Quarantine as fitted.** 127x the Cassini bound, as the paper itself now states |

### 4.4.2 Relocated to Lane 3, not quarantined

These are not wrong. They are **out of lane**, and mixing them into the physics build is exactly what the lane directive forbids.

| Item | Why Lane 3 |
|---|---|
| `res-extensa/synthesis/15_BioMechemicalRWHF.lean` and `15_rwhf_biomechemical_tests.py` | RWHF is named in Lane 3. It compiles and its 10 tests pass, and it has no Res-Nova attachment. It should never have been in a physics audit table as anything but "out of scope" |
| `Auroboryai` Paper B (RYTT semiotic codec) | Semiotics, Lane 3 |
| `Auroboryai` Paper F (ADCCL coherence gate) | AI tooling, Lane 3 |
| `Auroboryai` Paper H (neuro-topological stability) | Neuroscience, Lane 3 |
| `Auroboryai` Paper I (holonomery, SIMD ternary) | Infrastructure, Lane 3 |
| `Auroboryai` Paper J (ABC ternary gate) | Decision tooling, Lane 3 |
| `Auroboryai` Paper L (resource holonomy) | Economics, Lane 3 |
| `res-extensa/programme/ro0/` | Claim-registry infrastructure. Useful, but it is governance tooling, not physics |

### 4.4.3 Drop

| Item | Why |
|---|---|
| `res-extensa/synthesis/09a_chat_threads` (856 lines), `09b`, `09c`, `DRAFT_Companion_to_TUFT.md` | Chat-derived speculation. Not citable, not checkable, and it would take more work to tier line by line than the content is worth |
| `Auroboryai/papers/res-nova/res-nova-alien-superseded.tex` | Explicitly superseded |
| `Auroboryai` Paper A's Yang-Mills identification | An un-discharged named axiom, and its "spectral gap" proof is a self-declared sketch. The gap constant `0.9099` is not derived from the band constant `0.9100`; it sits near it |

## 4.5 What this means for the execution order

| Step | State after this audit |
|---|---|
| **1. Clear the Lean CI queue (BLK-1514 to BLK-1522)** | **Not cleared, and not clearing it blocks nothing.** The five dispatches (`1514`, `1515`, `1518`, `1520`, `1522`) are all addressed to Devin. The four receipts that exist (`1516`, `1517`, `1519`, `1521`) are Gemini Web closure audits, not Devin `lake build` plus `#print axioms` logs. Two Lean candidates are explicitly `IMPLEMENTED_NOT_EXECUTED` in the receipts themselves: `HamilgrangianMuStd_candidate.lean` (BLK-1513) and `WilsonPlaquetteBound_candidate.lean` (BLK-1519). Devin has no heartbeat in the agent roster. The gate is unmet, and the audit shows no port waits behind it |
| **2. Audit before porting** | **Done.** The four buckets are above. Port bucket empty; one Bucket 2 file needs a `coqc` receipt; five CAS jobs, one of which (the xAct characteristic analysis) has never been done; the rest is quarantined, relocated, or dropped |
| **3. Publish only after the physics translation pass** | The translation pass exists as Part 2 and is staged in draft PR #223. It is referee-shaped (action, symmetries, DoF, stability, regime, observables, then an explicit list of what is not established). It should not be merged to `main` until the BBN fork is resolved, because the fork changes what the paper is allowed to claim |

**The one thing worth doing next that needs nobody's permission:** add `lakefile.lean` and `lean-toolchain` to `res-extensa`, run `coqc` on `Dimensions.v`, and record the two exit codes. That closes three `IMPLEMENTED_NOT_EXECUTED` rows and costs one afternoon. It is not a port, it is not a new front, and it converts an honest gap into a receipt.
