# Peer Review Readiness Assessment

**Date:** 2026-08-16 (revised)
**Author:** R.W. Yett / Sovereign Architecture Group
**Version:** v1.5.0+ (post-D2/D3/D5/D6/D7 push, post-O1/D2 rescore)
**Revision note:** O1 and D2 rescored from [P] to [P/O] after audit of target docs and commit c47e7c6. PR #16 merged correcting HorizonScale.lean audit.

**⚠️ MAJOR REVISION 2026-09-12 — read this before trusting anything below dated before today.** D7's action was found to be generalized Einstein-aether (vector field), not the AeST (scalar field) action D9 claims to embed — two different theories sharing a section number. D7 was rewritten to genuine AeST (Skordis-Złośnik arXiv:2007.00082). Consequences:
- c_T=c is now *stronger* (structural, not asserted) — the one clean upgrade.
- D7's background cosmology, screening mechanism, and coupling-constant table (§3, §4, TARGET_D7_SUPPLEMENT) are **void**, not just wrong — they were computed from a field (𝒦) that isn't in the actual action (𝒴≡0 on FLRW identically).
- The γ=β=1 Foster-Jacobson result in TARGET_D3 §7 (written earlier today) is **void** for the same reason.
- **New finding, potentially serious:** solving the corrected AeST field equations exactly with this repo's own F_dual gives an r-independent anomalous acceleration ã₀=(1+λ_s)a₀ added to Newtonian gravity in the solar system — not screened. At the Cassini scale this is ~5.7×10⁵ **above** the Q₂ bound. This is an apparent falsification of μ(x)=x/(1+x) within standard two-derivative AeST/AQUAL, independently corroborated by Milgrom (arXiv:1205.1317) and Desmond (arXiv:2401.04796). `AXIOMS_V2.lean:64`'s disjunction (μ=x/(1+x) ∨ μ=x/√(1+x²)) has one branch now falsified by this repo's own derivation. Escape route: Skordis-Złośnik's higher-derivative screening — **run down and closed 2026-09-12, `TARGET_D7` §11** `[X]`: it requires a Vainshtein exponent p ≥ 2.34 while the GW170817-safe Horndeski sector caps at p → 2⁻, and the one published construction that reaches p=3 (Babichev-Deffayet-Esposito-Farèse arXiv:1106.2538) does so via a Riemann-coupled G₄(X)/G₅ operator excluded by c_T=c. BDEF also independently prove that the ghost conditions themselves force the constant ≈a₀ residual for *any* free function. μ=x/√(1+x²) is the surviving branch.
- Full detail: `CLAIM_EVIDENCE_LEDGER_v1.6.0_SUPPLEMENT.md` CLM-D7-01 through CLM-D7-08, CLM-D3-05, CLM-D9-01, CLM-AX-02.

---

## 1. Completion Matrix

| Target | Status | Evidence | Peer-Reviewable? |
|--------|--------|----------|:-:|
| **D1** Variational Derivation | ✅ [P] | `DualChannelDerivation.lean`, PAPER_01 | ✓ |
| **D2** Physical Action Origin | ⚠️ [P/O] | Conditional uniqueness proved; Padé necessity open | ⚠️ |
| **D3** PPN / Solar System | ⚠️ [P/O] | **Moved off [O] 2026-09-12 (`TARGET_D3` §8, supersedes §7).** γ **closed and derived**, not cited: every source of traceless anisotropic stress in AeST is O(ε²) (7-entry enumeration + sympy order-count), so Φ=Ψ exactly **for any free function** — γ=1, lensing = GR's 4G_N M_dyn/bc², no slip; the mechanism is the background's spatial isotropy (A^i=0, ∂_iφ̄=0), *not* a property of J, which answers D7 §7's question. β **scoped**: free-function entry bounded by ε_J=2𝒴J″/J′=1/(1+x²)≲10⁻¹⁷ at Mercury (vs 1/(1+x)~10⁻⁹ for the dead μ_dual) — μ_std cannot break β; the (λ_s,K_B) part is an unattempted 2PN calc **[O]**. α₁,α₂ **[O] with a named obstruction**: AeST sits on the c₁₂₃=0 "Maxwell" locus where Jacobson (0801.1547 §8) states verbatim the FJ PPN series is "evidently not applicable" (spin-0 aether speed = 0) — so citing FJ was never going to work; new ab initio 1.5PN g_{0i} work required, and no published AeST solution has a g_{0i} sector. **New numerics:** δg=(1+λ_s)³a₀²/2g_N (exact 50-digit solve, 5 values of λ_s) **grows as r²** ⇒ Saturn binds, not Mercury (1251×, the figure `TARGET_D1_SUPPLEMENT` §4.1 quotes) ⇒ **first upper bound on λ_s in the corpus, λ_s = O(1)**: 50× margin ⇒ λ_s≲2.7 via Q₂ᵉᑫ=δg/r, 7.6× ⇒ λ_s≲1.0 via perihelion precession (Δϖ=π(n+2)δg/g_N, self-checked by reproducing D7 §4.3's 1.52 arcsec/cy at n=0). Existence of the bound **[D]**, the number **[C]** (monopole-vs-quadrupole mapping; ephemeris-bound provenance) | ⚠️ |
| **D5** Cosmological Sector | ⚠️ [P/O] | **Rebuilt 2026-09-12** on the correct AeST 𝒦(𝒬) sector. Old content ([O] void: 0.23%/429× screening, ξ=2⇒76×/2264× overgrowth, νHDM import) retired in place. Now: SZ Cosh function adopted, exact closed-form background 𝒵(a)=arcsinh(2w₀/(r a³)), Higgs-duration problem **closed** (𝒦_𝒬𝒬(𝒬₀)=2𝒦₂ independent of 𝒵₀ ⇒ μ and early-time w decouple; window 2.5×10⁻⁸≪𝒵₀/𝒬₀≲2×10⁻², and SZ's own published run sits inside it at 10⁻²), \|ΔH/H\|≤3.6×10⁻³ vs ΛCDM. Linear order: 𝒴 is quadratic in perturbations ⇒ **ξ=1 exactly**, a₀/μ(x) absent from linear cosmology [D]. Costs: 5 parameters vs ΛCDM's 2; Ω_c demoted to an integration constant. Open: **non-linear AeST structure formation (unsimulated by anyone)** | ⚠️ |
| **D6** Relativistic Stability | ⚠️ [P/O] | Ghost-free condition was proved for F''(𝒦)>0; needs re-verification as J''(𝒴)>0 under the corrected action — not yet re-checked | ⚠️ |
| **D7** Covariant Completion | ⚠️ [P/O] | Action corrected to genuine AeST 2026-09-12 (scalar 𝒴, Skordis-Złośnik verbatim) — the base action is now [D] solid. But this surfaced the D3/D5 voids above plus the new μ=x/(1+x) tracking-branch problem (CLM-D7-08). Net: more honest, less complete | ⚠️ |
| **D8** Tensor Speed | ✅ [P] | c_T = c — upgraded 2026-09-12 from asserted-via-citation to structural (no TT piece in δA under minimal AeST coupling) | ✓ |
| **D9** Skordis-Złośnik Embedding | ⚠️ [P/O] | Was ground-truth for the D7 fix, but a factor-of-2 normalization bug (μ=𝒥′ vs 2𝒥′) and ã₀≠a₀ were found and fixed in the header 2026-09-12; not yet re-verified against `SkordisZlosnikEmbedding.lean` | ⚠️ |
| **O1** Horizon Scale | ⚠️ [P/O] | 2π KMS cancellation proved [P]; a₀=cH identification open [O] (5.67× discrepancy, consistent with the literature's own cH₀/2π≈6× framing — see §2 below; O4's 5.9σ disfavouring is itself rescored [P/O], pending dataset provenance) | ⚠️ |
| **O4** Redshift Test | ⚠️ [P/O] | H_const preferred over H_horizon, σ=√Δχ²=5.93 reproduces exactly (rescored 2026-09-12: dataset in `a0_of_z.py` is hardcoded with no provenance/fetch script — flagged by the repo's own `gate2_inference.py` as non-Gate-1-compliant; χ²/N=0.27 is under-dispersed for 0 free params; the √Δχ² formula assumes nested models, but these are two point-hypotheses with no parameter difference); JWST expansion pre-registered | ⚠️ |
| **O5** SPARC Automation | ✅ [P] | clean-clone walk closed 2026-09-09: 175/175 checksums, 0 drift (VERIFICATION_RUN_009) | ✓ |
| **O6** Clean Reproduction | ✅ [P] | 39/39 PASS at closure; 43/43 since #39 (SU(2) envelope rungs); CI `lean-gate` green at `d130413`; gate list ≡ lakefile roots | ✓ |

**Score: 4/12 fully peer-reviewable ([P]), 8/12 partially ready ([P/O]), 0/12 open ([O]) — rescored 2026-09-12 (D3 [O]→[P/O] on the §8 AeST PPN derivation: γ closed structurally, β scoped, α₁/α₂ open with a named obstruction, λ_s ≲ 2.7 derived; D5 [O]→[P/O] on the evening rebuild of the 𝒦(𝒬) sector), earlier after fixing the D7/D9 action mismatch, which voided D5's screening calculation and D3's just-derived PPN margins, and surfaced an apparent falsification of μ=x/(1+x) within two-derivative AeST. This is the most significant single-day rescore in the project's history. The drop is the correction working as intended, not new damage — every one of these was already false before today; today is when it got caught.**

---

## 2. O1 Rescore Rationale

**Previous scoring:** ✅ [P]
**Corrected scoring:** ⚠️ [P/O]

**What is proved [P]:**
- The 2π KMS cancellation is formally proved in `HorizonScale.lean` (ξ = 1, not 1/2π)
- The Lean proof is verified: 18 modules, RESULT: PASS

**What is open [O]:**
- The physical identification a₀ = cH is NOT proved. The SPARC-measured a₀ = 1.116 × 10⁻¹⁰ m/s² gives cH₀/a₀ ≈ 5.67, not 1.
- The 5.67× discrepancy was identified in the earlier O1 audit and never retired.
- The O4 redshift test (commit `3d1355b`) found H_const (a₀ = constant) favoured over H_horizon (a₀ = ξcH(z)) at 5.9σ — the horizon interpretation is **disfavoured by data**.
- Commit `c47e7c6` explicitly states "O1 remains D0_PROPOSED."
- `TARGET_O1_A0_HORIZON_DERIVATION.md` tags the horizon-scale ↔ SPARC a₀ identification as [O].

**Honest framing:** The theory does not require the horizon identification. a₀ is treated as a fundamental constant throughout the empirical analysis (SPARC, D3, D5, D7). The coincidence a₀ ~ cH₀/5.7 is noted but not claimed as a derivation. The 2π cancellation is a mathematical result; the physical identification is a separate, open question.

**Literature grounding (added 2026-09-12):** the ~2π (equivalently ~5.7–6×) normalization is not unique to this repo — Milgrom (2015, *Phys. Rev. D* 91, 044009) and Sanders (2019, *MNRAS* 485, 513) independently report a₀ ≈ cH₀/2π and a₀ ≈ cH₀/6 respectively; Milgrom's review (2020, arXiv:2001.09729) surveys the whole a₀–cosmology coincidence family. So TARGET_O1's 5.67× finding reproduces a factor the field has long noted, rather than exposing a defect unique to this derivation. See `04_cosmology/TARGET_O1_A0_HORIZON_DERIVATION.md` §3 for the full citation trail. This does not change O1's [P/O] score — the 2π is still not derived from the Unruh/Gibbons-Hawking action — but it changes the framing from "unexplained miss" to "reproduces a known, still-unexplained coincidence."

---

## 3. D2 Rescore Rationale

**Previous scoring:** ✅ [P]
**Corrected scoring:** ⚠️ [P/O]

**What is proved [P]:**
- Theorem 9.1: Given four structural constraints (constitutive-relation structure, Padé[1/1] minimality, MOND boundary conditions, dual-channel structure), F_dual is uniquely determined.
- Theorems 4.1–8.2: All component theorems verified symbolically.
- The Fisher information identity F'²·I = x³ is a non-trivial structural result.

**What is open [O]:**
- The Padé necessity (constraint 2) is not derived from a more fundamental principle. Why should μ be a rational function at all?
- The two-irreducible-parameters rule: the Padé choice relocates the functional freedom from "which μ" to "which rational order + which boundary conditions" — it does not eliminate it.
- The target doc itself reads "D2_PROPOSED" with the necessity question tagged [O].
- Questions Q1–Q4 in §9 of the D2 document remain open.

**Honest framing:** D2 proves that F_dual is the unique action *given* the Padé[1/1] choice. It does not prove that the Padé choice itself is necessary. This is a conditional uniqueness result, not an unconditional derivation from first principles.

---

## 4. PR #16 — Merged

PR #16 ("docs(audit): correct HorizonScale.lean presence claim on main") merged via squash at `f82bfc1`. The PR:
- Adds a dated superseding note to `AUDIT_LEAN_INVENTORY.md` (does not rewrite audit history)
- Correctly states that `HorizonScale.lean` is now on main but NOT in `lakefile.lean` roots
- Preserves F7 scoping to 17 tracked modules
- `verify_all_proofs.sh:34` is an explicit 17-target list (not a glob) — the gate genuinely covers 17 modules
- Flags the O1 scoring discrepancy (now corrected in this revision)

---

## 5. check_retracted_claims.sh

Still exits FAIL, but only on pre-existing surfaces:
- Quarantined PAPER_01 (arcsinh action, tombstoned)
- Historical VERIFICATION_RUN_001
- The repo's own guard-rail files that quote the banned phrase in order to ban it

Diff `f13cf75..4af94c4` confirms: the D-series pushes added **no new** "zero free parameters" text. The failure is pre-existing and does not affect the new content.

---

## 6. Anticipated Referee Questions (Updated)

- Q: "Is a₀ = cH?"
  A: The 2π KMS cancellation is proved (ξ=1). But cH₀/a₀ ≈ 5.67, and the O4 redshift test disfavours the horizon interpretation at 5.9σ. The theory treats a₀ as a fundamental constant; the horizon coincidence is noted but not claimed as a derivation.

- Q: "Why μ = x/(1+x)?"
  A: D2 proves it's the unique Padé[1/1] satisfying MOND boundary conditions, and it's the inverse of the odds ratio (Bayesian structure). The Padé choice itself is a structural assumption, not a derivation — acknowledged as [O].

- Q: "What about non-linear structure formation?"
  A: Linear theory is screened (0.23% enhancement, a 429× suppression; corrected 2026-09-08 from 0.4% / 250× — see GHOSTFREE_AND_SCREENING_CORRECTION_2026-09-08.md). Non-linear requires N-body with Thomas et al. (2023) equations — future work.

- Q: "Is the Vainshtein estimate rigorous?"
  A: The (r/r_MOND)^(3/2) scaling is standard; exact Q₂ requires solving the RMOND PDEs in the solar system. The 119× margin below Cassini (corrected 2026-09-12 from a misstated 70×) provides robustness to the estimate's uncertainty.

- Q: "Can you compute exact PPN γ and β?"
  A: Framework complete (D7); exact values need post-Newtonian expansion with specific c₁,c₂,c₃ — tractable but not yet done.

---

## 7. Readiness Verdict (Revised)

**The Res Nova manuscript is NOT yet ready for peer review on D3/D7.** D1, D2, D6, D8, D9, O1, O4, O5, O6 can be submitted with honest scoping. **D5 was rebuilt 2026-09-12** on the correct AeST 𝒦(𝒬) sector and moves [O]→[P/O]: background and linear perturbations are derived and ΛCDM-consistent, with non-linear structure formation the one critical open item. D3 still rests on void calculations and needs either a real fix or an honest statement that μ=x/(1+x) may be falsified within two-derivative AeST.

Count (rescored 2026-09-12 after fixing the D7/D9 action mismatch — see `CLAIM_EVIDENCE_LEDGER_v1.6.0_SUPPLEMENT.md` CLM-D7-01 through CLM-D7-08, CLM-D3-05, CLM-D9-01, CLM-AX-02):
- **[P] (fully proved):** D1, D8, O5, O6 = **4 targets**
- **[P/O] (partially proved):** D2, D5, D6, D7, D9, O1, O4 = **7 targets**
- **[O] (open):** none = **0 targets** (D3 moved to [P/O] 2026-09-12, `TARGET_D3` §8)

**Score: 4/12 fully reviewable, 8/12 partially ready, 0/12 fully open** (D3 §8 added and D5 rebuilt, both 2026-09-12).

- Present D1, D8 as completed framework; D8 (c_T=c) is now stronger than before today's fix
- Present O5, O6 as completed empirical/CI infrastructure
- Present D2 as conditional uniqueness (honestly scoped)
- Present D6, D7, D9 as "framework corrected, re-verification pending" — D7's action is now genuinely AeST, but the ghost-free condition (D6) needs re-checking as J''(𝒴)>0, and D9's factor-of-2 normalization fix needs re-verification against its own Lean file
- **D3 may now be presented, scoped to §8.** (D5 likewise, with its §5 open items stated.) §8's γ result is derived and F-independent; β and α₁/α₂ must be presented as scoped/open, not as computed. Present the Saturn margin (50×) as the binding solar-system number, **not** Mercury's 1251× — the μ_std residual grows as r², so Mercury is the most favourable point, not the most constraining. Do **not** cite Foster–Jacobson α₁,α₂ for this theory: AeST sits on the c₁₂₃=0 locus Jacobson explicitly disqualifies. §1–§7 of `TARGET_D3` are superseded and must not be presented — the 1137× was a category error, the γ=β=1 Foster–Jacobson result was derived for the wrong action, and μ=x/(1+x) is dead (D7 §4/§11).
- Present O1 honestly: 2π cancellation proved, horizon identification open; the 5.67× discrepancy matches the literature's own cH₀/2π framing (Milgrom 2015; Sanders 2019), not a repo-specific miss
- Present O4 honestly: H_const vs H_horizon reproduces its stated σ arithmetically, but the underlying 20-point dataset lacks provenance (flagged by the repo's own `gate2_inference.py` Gate-1 requirement) and the σ formula's nested-model assumption doesn't strictly apply to two point-hypotheses — rescored [P/O] pending a provenance-compliant dataset

**The critical path changed today.** It is no longer "compute exact PPN γ,β" — it is: does this theory survive contact with its own solar-system solution? (Update, later 2026-09-12: with μ_std installed the answer at γ is **yes, structurally** — see item 3. The residue is β, α₁/α₂, and the λ_s bound.) Open items, most severe first:
1. **D7/D3 anomalous acceleration — RESOLVED NEGATIVELY 2026-09-12 (`TARGET_D7` §11).** SZ's higher-derivative screening does **not** save μ=x/(1+x). Three findings: (a) Babichev–Deffayet–Esposito-Farèse arXiv:1106.2538 already built this escape route (on TeVeS), and in doing so proved that the ghost conditions f′>0, 2sf″+f′>0 — this repo's own §5 conditions — force φ″(r)<0 and hence the constant ≈a₀ residual for *any* free function, so CLM-D7-08 is a theorem about the two-derivative sector, not an artefact of F_dual; (b) suppressing that residual to the solar-system bound while leaving galaxies unscreened requires a Vainshtein exponent p ≥ 2.34 (3.00 for 10³ M_⊙ systems), whereas the post-GW170817 Horndeski sector (G₂, G₃□φ, G₄ const) supplies at most p → 2⁻ — cubic Galileon at maximal r_V gains only a factor 4 and is still 1.4×10⁵ over bound; (c) the only operator that reaches p=3 is BDEF's explicit Riemann×(∇φ)²∇∇φ coupling, i.e. Horndeski G₄(X)/G₅, excluded by GW170817. **Branch B costs c_T=c, which is D7's strongest result. Branch A (μ=x/√(1+x²)) is the live route** — `AXIOMS_V2.lean:64`'s disjunction should collapse to the right disjunct. Residual `[O]`: a non-Horndeski aether-projected operator (q^{μν}∇_μ∇_νφ, A^μ) reaching p ≥ 2.34 with c_T=c is not formally excluded; that is the only remaining branch-B derivation. **Branch A rebuild underway 2026-09-12 (`TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md`):** exact 50-digit solve confirms μ_std clears the Mercury/Cassini bound by ~1300× (residual matches a₀²/(2ĝ) to 10 sig figs, vs. μ_dual's constant ≥a₀ residual — a 9-order-of-magnitude difference, not asserted but computed). Ghost-free conditions hold identically. **But D2's Padé[1/1] uniqueness proof does not apply to μ_std** (it's not a rational function) — nor does the Fisher-identity/Hamilgrangian-split machinery (CLM-12/13/14). Does the dual-channel construction *derive* x/√(1+x²), or is it adopted only because it survives the solar system? That gap, not RAR-fit survival, is now the sharpest open question. **Partially closed 2026-09-12 — `TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md`:** μ_std *is* forced by a D2-shaped structural argument once D2's `{0,1}` Bernoulli channel is replaced by a `±1` **chiral** channel — rapidity conjugacy `dF/dψ=x²`, equivalently `F′²·ℐ_±(μ)=x⁴` with `ℐ_±=1/(1−μ²)`, yields `μ=x/√(1+x²)` uniquely with no rational ansatz, and `μ′(0)=1` selects the exponent exactly as in D2 Thm 9.3. It also recovers `F_std=½[x√(1+x²)−arsinh x]`, D2 §3's own object. This is a postulate swap (alphabet choice), not a derivation from the action — the covariant question (D2 Q3) is still `[O]`. That document also flags a **normalization error** (`F′=μ` instead of `F′=xμ`) in `TARGET_D1_SUPPLEMENT` §1/§3/§5; its §4 solar-system solve is unaffected.
2. **D5 cosmology — linear sector CLOSED 2026-09-12 (`TARGET_D5_COSMOLOGICAL_SECTOR.md`).** The 𝒦(𝒬) ghost-condensate sector is now specified (SZ Cosh function), the background solves in closed form via the shift-symmetry first integral 𝒦_𝒬=I₀/a³, and the Higgs-phase-duration problem closes because 𝒦_𝒬𝒬(𝒬₀)=2𝒦₂ is independent of the Cosh width 𝒵₀ — the quasistatic mass μ and the early-time equation of state are carried by different parameters, so μ⁻¹≳1 Mpc and w(10⁻⁴)≲0.02 are no longer in conflict. Derived in-house rather than quoted: w₀=3H₀²Ω₀/[2μ²(2−K_B)] ⇒ w₀≳1.1×10⁻⁸ vs w₀≲2×10⁻¹⁴, a 6.1×10⁵ gap; the quadratic 𝒦 gives c²_ad=2.5×10⁴ at a=10⁻⁴, hence Π~10⁴·δ in SZ's own pressure-contrast equation, destroying the CDM limit (no causality claim is made: c²_ad=dP̄/dρ̄ is a thermodynamic derivative, not a propagation speed). Cosh closes it over 2.5×10⁻⁸≪r≲2×10⁻² with \|ΔH/H\|≤3.6×10⁻³ vs ΛCDM. **Corroborated, not merely proposed:** SZ's own published Cosh parameters (Fig. 1 legend: K_B=0.5, 𝒬₀=0.1, 𝒦₂=7.5×10⁵, 𝒵₀=10⁻³) give r=10⁻², inside the window, with w(10⁻⁴)=9.5×10⁻³. A drift effect derived here and *not* reported by SZ — ρ̄a³ drifting logarithmically by ≈r·ln(2A/a³), = +5.34% for their run — appears to be the origin of the unexplained 3.98% Ω_ch² offset in their own caption. **The old 76×/2264× overgrowth is void, not screened**: 𝒴=q^{μν}∇_μφ∇_νφ is quadratic in perturbations, so a₀, μ(x) and λ_s do not enter linear cosmology at all and ξ≡G_eff/G=1 exactly (SZ say the same). Growth is CDM-like with a free-streaming cutoff at k≈1.8 Mpc⁻¹. **Not open in the literature:** SZ pose *and resolve* the Higgs-duration problem in one paragraph and validate Cosh/Exp in their own Boltzmann code — this corpus lacked the resolution, not the field. Remaining `[O]`, most severe first: (a) **non-linear AeST structure formation — no simulation exists**; (b) the (k,z) crossover where ℱ(𝒴,𝒬) switches on; (c) the μ²Φ² oscillatory regime vs the linear MPS at k~0.1–1 Mpc⁻¹; (d) a full Planck likelihood for r; (e) **the one item genuinely open in the literature, and not the one expected: SZ's published Cosh fit runs at μ⁻¹=10 kpc, a factor 100 below the μ⁻¹≳1 Mpc their own text requires for galactic MOND** — their cosmological and quasistatic sectors are not evaluated at the same parameter point. Honest cost: five cosmological parameters (λ_s, K_B, 𝒦₂, 𝒬₀, 𝒵₀) against ΛCDM's two, and Ω_c demoted to an integration constant. Also: AeST predicts w_DE=−1 exactly, so DESI DR1's evolving-w preference is neither predicted nor accommodated, and Geometrodynamica's (w₀,w_a)=(−0.831,−0.720) does **not** transfer.
3. **D3 PPN — γ CLOSED, β/α₁/α₂ the new residue (`TARGET_D3` §8, 2026-09-12).** γ_PPN=1 is now *derived*, not cited: every `g^{ij}`-dependent term in the AeST action is quadratic in the perturbations (7-entry enumeration of Σ_ij + sympy order-count), so the traceless `ij` Einstein equation is homogeneous at linear order, Φ=Ψ exactly, and lensing gives GR's `4G_N M_dyn/bc²` with no slip — **for every free function**. The mechanism is spatial isotropy of the AeST background (A^i=0, ∂_iφ̄=0); φ reaches g_00 linearly only through 𝒬₀≠0 (the Higgs phase) and carries g^{00}, never g^{ij}. So the swap F_dual→F_std is irrelevant to γ. Corroborated by Verwayen–Skordis–Złośnik arXiv:2304.05134 §3 verbatim. Residue, most severe first: (a) **α₁,α₂ still [O], but the obstruction is now named** — AeST's vector couplings (c₁=−c₃=K_B/2, c₂=c₄=0) sit on the c₁₂₃=0 "Maxwell" locus where Jacobson arXiv:0801.1547 §8 states the Foster–Jacobson PPN series is "evidently not applicable" (spin-0 aether speed = 0); naive substitution returns α₁=−2K_B and α₂=∞, which is a diagnostic, not a prediction. AeST fills that mode with the scalar, so a PPN series should exist, but no published AeST solution has a g_{0i} sector at all, so this needs new ab initio 1.5PN work. (b) **β [O]** — the free-function entry is suppressed by ε_J=2𝒴J″/J′=1/(1+x²)≲10⁻¹⁷ at Mercury (vs 1/(1+x)~10⁻⁹ for μ_dual), so μ_std cannot break β; the (λ_s,K_B) part is a real 2PN AeST calculation nobody has done. (c) **The evaluable constraint moved**: δg=(1+λ_s)³a₀²/2g_N (exact 50-digit solve at five λ_s) **grows as r²**, so Saturn binds at **50×**, not Mercury at 1251× — `TARGET_D1_SUPPLEMENT` §4.1's "~1300×" is the most favourable field point in the solar system and should not be quoted alone. That gives the corpus's **first upper bound on the tracking slope, λ_s = O(1)** — ≲2.7 by the Q₂ᵉᑫ route, ≲1.0 by an independent perihelion-precession route (Saturn binds under both; the precession formula is self-checked by reproducing D7 §4.3's 1.52 arcsec/cy at n=0). Existence [D], number [C]. D7 §2.2 had λ_s wholly unfixed.
4. D6 ghost-free re-verification — J''(𝒴)>0 under the corrected action, not yet checked.
5. D9 re-verification against `SkordisZlosnikEmbedding.lean` after the factor-of-2 fix.
6. **D2 Padé necessity — superseded by a sharper problem.** D2's uniqueness proof (Theorem 9.1) was built specifically for the now-falsified μ_dual=x/(1+x). It does not apply to the surviving μ_std=x/√(1+x²) at all (not a Padé function). D2 is not just "necessity of Padé[1/1] unproven" anymore — it's "no structural derivation exists for the function this repo now needs." See `TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md` §2.
7. O1 horizon identification — the coincidence is real but its physical origin remains open; theory works without it.
7. O4 dataset provenance — the 20 hardcoded points in `a0_of_z.py` need a traceable source before the 5.9σ claim can be presented as [P].
8. ~~O6 CI automation~~ — **closed 2026-09-08.** `lean-gate` runs `verify_all_proofs.sh` on push/schedule/dispatch; 39/39 targets, gate list verified identical to lakefile roots. Residual is not the gate but the Mathlib cache endpoint's stall rate, which the daily cron now samples automatically (3/3 green so far) instead of via one-off manual walks.
