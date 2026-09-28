# READ THIS BEFORE WRITING ANY PHYSICS CONTENT

**If you are an agent (Manus, Grok, antigravity, Claude, or anything else) about to write,
summarize, or extend any claim in this theory — stop and read this file completely first.
Do not pull from the Obsidian vault's `raw/Logs/`, `80_Archive/`, `obsidian_vault_legacy/`,
or any file described as "archived," "legacy," or "historical." Those are frozen records of
past states, kept for provenance, not current physics. This file and the two it points to
are the only current physics.**

**Last verified against the physics:** 2026-09-24 (the audit-cycle state below supersedes
any pre-2026-09-16 substrate claim not updated by it).

This line is **enforced**, not decorative: `scripts/current_state_freshness.py` fails the
gate if any physics surface — the Lean modules, the manuscript, `PEER_REVIEW_READINESS.md`
or any `TARGET_D*` — has a commit dated after this date. Documentation and tooling churn
does not trip it. It previously pinned a commit SHA, which moved on every commit and so
was stale the moment it was written; a pin that is always wrong is not a check.

If the date is more than three days old when you read it, treat every claim below as
suspect and re-derive its status from `PEER_REVIEW_READINESS.md` before using it.

---

## Why this file exists

On 2026-09-12, an external agent (Manus) was dispatched to write four standalone papers.
It built its brief from cached/legacy vault material instead of the live repo, and used:
- **μ(x) = x/(1+x)** as the theory's central interpolating function — falsified the same
  night, roughly two hours *before* Manus started writing, in `TARGET_D7_COVARIANT_COMPLETION.md`.
- **V₂₄₀(ℝ^N)**, the "big-dimension" Stiefel substrate — retired **19 days earlier**
  (2026-08-25), superseded by V₂(ℝ³) via Cartan triality.

Neither error was a timing accident. Both facts were already on disk, committed, before the
agent that used the dead version ever ran. This file exists so that never happens again:
one place, unambiguous, checked first, every time.

---

## The three things every agent gets wrong if they skip this

### 1. The interpolating function is μ_std, NOT μ_dual

- **DEAD, do not use:** μ_dual(x) = x/(1+x). Falsified 2026-09-12 — produces an
  r-independent anomalous acceleration in the solar system, ~5.7×10⁵ over the Cassini bound.
  No viable fix exists within any GW170817-safe (c_T=c) theory. See `TARGET_D7_COVARIANT_COMPLETION.md`
  §4 and §11 for the full derivation and the literature search that closed off every escape route.
- **LIVE, use this:** μ_std(x) = x/√(1+x²). Confirmed via exact 50-digit numerical solve
  to clear the same solar-system bound by ~1300×. See `TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md`.
  A structural uniqueness derivation exists (rapidity/chiral-Fisher postulate) in
  `TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md`.
- **Added 2026-09-27: the "~1300× clear" is the isolated-Sun MONOPOLE test only.** It does
  not cover the external-field-effect (EFE) quadrupole Q₂. The Milky Way's field induces Q₂, and
  Cassini bounds it at (3 ± 3)×10⁻²⁷ s⁻². With Milgrom's exact QUMOND formula (validated against
  Hees et al. 2016 Table 2 to 3 digits) at the derived a0, **μ_std gives Q₂ = 1.7×10⁻²⁶: excluded
  at ~4.6σ.** The McGaugh RAR fails at 8–11σ. Only sharp-transition functions (ν_n with n ≳ 5,
  ν̂_α with α ≳ 4) pass, and they fit SPARC worse (best passer ν̂₄: tier-1 median/agg 3.51/7.57 vs
  μ_std 3.36/6.09). Against the tighter 2026 Cassini bound (1.6 ± 1.8)×10⁻²⁷, μ_std is +8.7σ.
  AeST does not escape: it reduces to AQUAL (`sz_aqual_reduction`), and QUMOND underestimates
  AQUAL Q₂. μ_std stays the live function, but it is **not** solar-system-clean once the EFE is
  included. In total χ², SPARC prefers n = 2 over any Cassini-passing n by Δχ²/s ≈ 700–1400
  (the Cassini penalty on n = 2 is 70), so a sharper μ is **not** the fix. Keep μ_std-like
  behaviour in galaxies and find a solar-system suppression: higher-derivative screening
  (`TARGET_D7` §4.4 Branch B) or an environment-dependent mechanism [O]. Cassini also
  disfavors Postulate R as the selector of μ (it forces n = 2). **Screening window found
  (phenomenological):** μ_std plus M^{1/4} screening (BDE 2011 scaling), with a solar screening
  radius of 0.1–1 pc, passes Cassini and leaves SPARC unchanged
  (`02_galaxy_dynamics/SCREENING_WINDOW_2026-09-27.md`). No covariant AeST version exists [O];
  BDE 2011 itself is c_T-excluded (`TARGET_D7` §11) — only the §11.4 openings (aether-projected
  operators, conformal/symmetron) remain for a covariant realization.
  A size-based shield provably needs a new constant (dimensional no-go). The **parameter-free**
  environmental form S = 1 − μ_std(g_ext/a0) passes Cassini (+0.25σ / −0.10σ) and does not degrade
  SPARC (uniform and per-galaxy η from Chae 2020; per-galaxy environment NOT detected by SPARC —
  shuffled fields do as well; `ENVIRONMENT_SCREENING_2026-09-27.md`). **MW dwarfs (42, LVDB)
  reject that form** (Δχ² +50…+107); the duality form S = 1/(1+η²) = μ_std(1/η)² passes Cassini,
  is SPARC-neutral, and its dwarf penalty is not significant after MOND's own misfit
  (`DWARF_SCREENING_TEST_2026-09-27.md`). See
  `02_galaxy_dynamics/CASSINI_EFE_QUADRUPOLE_2026-09-27.md`.
- If you see μ(x)=x/(1+x) — or F_dual = x²/2 − x + ln(1+x) — anywhere in a source you're
  reading, that source predates 2026-09-12's correction and its physics content is void.
- **Added 2026-09-24 — the branches differ structurally, not just numerically.** Under the
  exchange x ↦ 1/x (i.e. a ↦ a₀²/a, Newtonian ↔ deep-MOND about the transition scale) the
  dead branch satisfies μ_dual(1/x) = 1 − μ_dual(x): the duality holds in μ itself. The live
  branch does **not**. It satisfies μ_std(1/x)² + μ_std(x)² = 1 — the duality survives one
  level down, in μ². Via `MuStdUniqueness.lean`'s `mu_std_sinh` that reads β² + γ⁻² = 1, the
  defining relation of the Lorentz factor. Machine-checked in `MuStdDuality.lean` (8 theorems,
  no sorry, standard axioms, sabotage-tested). **This is algebra, not new physics:** reading x
  as a celerity is Postulate R, still `[O]`, and nothing there selects a ↦ a₀²/a as a symmetry
  of the dynamics. Results are presented in `HAMILGRANGIAN_CANONICAL.tex`, so the module is
  scoped adjacent and is not a Table 2 result.

### 2. The substrate is V₂(ℝ³) via Cartan triality, NOT V₂₄₀(ℝ^N)

- **DEAD, do not use:** the "big-dimension" frame V_m(ℝ^N), m=240, N~57,600, tied to the
  E8 root system count 240²=57,600. Retired 2026-08-25.
- **LIVE, use this:** V₂(ℝ³) via Cartan triality. Any document still built on the retired
  substrate needs a full rebuild, not a patch — the retirement was structural, not cosmetic.
- The arithmetic 240²=57,600 remains a true E8 root-count identity. It is **not** the
  ambient dimension of anything physical in the current theory.

### 2b. AeST's CMB result is REPORTED, NOT VERIFIED — added 2026-09-24

The claim "AeST fits Planck" traces to Skordis & Zlosnik PRL 127, 161302, Figs. 1-2.
**Those figures rest on adiabatic initial conditions whose only citation is
`C. Skordis, S. Ilić, T. G. Zlosnik, in preparation (2021)` — verified on INSPIRE to
have never been published** (zero papers by all three; none of the 17 AeST-titled
papers 2021-2025 carries cosmological perturbations). Nothing suggests the result is
wrong, and those authors have published extensively on AeST since — but no one outside
that group can currently check it.

**Carry it as reported-not-verified wherever the AeST cosmology is cited.** The
initial conditions themselves were derived independently on 2026-09-24
(`TARGET_D5` §3.5-3.6, `05_Scripts_and_Tools/cmb_aest/`), which removes the dependency
for the ICs specifically but does not reproduce their Boltzmann run.

Also settled the same day: the perturbation sound speed is
**c²_s = [(2−K_B)+𝓕_𝒴]/𝒦_𝒬𝒬**, derived from the quadratic action and **not** equal to
c²_ad (which exceeds it by ~10⁶ at a = 10⁻²). Jeans cutoff k_J = 0.68 Mpc⁻¹, above the
linear MPS window. **Never substitute c_ad for a propagation speed.**

### 3. The covariant completion action is AeST, NOT generalized Einstein-aether

- D7's action was rewritten 2026-09-12 to genuine AeST (Skordis-Złośnik arXiv:2007.00082):
  scalar field 𝒴, minimal matter coupling. The prior version (vector field 𝒦, disformal
  coupling) was a different theory entirely and is retired. See `TARGET_D7_COVARIANT_COMPLETION.md` §0.
- **Added 2026-09-27: GW170817's Shapiro delay rules out photon-only lensing.** On that sightline the Milky
  Way's μ_std phantom potential delays light by 94–254 days, and photons and gravitational waves agree to
  −2.6×10⁻⁷ ≤ γ_GW − γ_EM ≤ 1.2×10⁻⁶. So a photon-only (disformal) metric cannot carry the MOND lensing,
  with or without cosmological freeze-out (Boran et al. 2018). Conformal routes (k-mouflage, symmetron)
  pass GW170817 but bend no extra light (Bekenstein & Sanders 1994). **Any covariant screening must be
  built at metric level (AeST class).** The same-day idea of a V(χ)=(χ−θ)² freeze-out rescuing disformal
  lensing is **withdrawn**. See `02_galaxy_dynamics/AETHER_DRAG_AND_SHAPIRO_2026-09-27.md` and D3 working
  note 7 §28.

---

## What is actually current, right now (check `PEER_REVIEW_READINESS.md` for live detail)

| Target | Status | One-line state |
|---|---|---|
| D1 | [P] | μ_std rebuild **complete** (`TARGET_D1_SUPPLEMENT`, re-run 2026-09-12); its '1300× solar-system clear' is monopole-only — EFE quadrupole fails at derived a0, duality screening restores a pass (2026-09-27) |
| D2 | [P] | **Closed 2026-09-27 under the two-irreducible-parameters accounting.** μ is parameter 2 (the functional choice): structurally motivated (Postulate R / chiral coordinate), empirically selected (n≈2, Δχ²/s 700–1400), ghost-free, Cassini-consistent with screening. Duality holds for all n (`MuNDuality.lean`). A covariant argument forcing μ is a research question, not a gap |
| D3 | [P] | **Closed 2026-09-27 (note 7 §34), verified symbolically.** The dragged branch completes to AeST's stealth sector (Skordis & Vokrouhlický 2024): the aether is a constant-norm clock-field gradient, i.e. the free-fall river. All field-equation residuals are 0 on PG Schwarzschild, so every PPN parameter is GR, up to external-field and cosmological-density corrections, wherever the clock field is single-valued (the planets, if v_rel ≳ 60 km/s, an estimate). c₂ lift excluded (|α₁| ≥ 4K_B). λ_s is not constrained by a dragged Sun |
| D5 | [P/O] | Cosh cosmology time-sector formalized (`CoshCosmology.lean`, 6 theorems, 0 sorry, ARITH); non-linear structure formation unsimulated |
| D6 | [P] | **Closed 2026-09-27.** Ghost-free; subluminal (spin-2 at c, spin-1 luminal front, scalar c_s < c above 𝒦₂ ≥ 3.75, met at both SZ points); J-normalization = one family J = 2λ_sã₀²F; Λ_SC not excluded (screened); EP closed (η ≲ 4×10⁻⁴⁹). The covariant screening profile is carried by D7 (`TARGET_D6` closure banner) |
| D7 | [P/O] | AeST action; the stealth sector screens the Sun (D3 §34). **Branch selection is open.** Stage 1 (linear, proxy lift) *indicates* moving dwarfs are stripped, which would contradict Crater II, Carina, Leo II and Sculptor, but it is **not decisive** (wrong source, unvalidated reference, possible non-linear held branch). Decisive check pending: the boosted-held residuals. Survival may depend on 𝒦₂ (estimate 𝒦₂v²/x: ≪1 at 75, ≫1 at 7.5×10⁵). The phenomenological law is unaffected. Do NOT cite "AeST disfavoured by satellites" |
| D8 | [P] | c_T=c — upgraded to structural, strongest result in the corpus |
| D9 | [P] | **Closed 2026-09-27.** μ_std embedding derived by calculus (`SZStdEmbedding.lean`: J_std = F_std(√𝒴) gives 2J′ = μ_std, with J′ > 0). λ_s is the family's overall scale, an AeST parameter (the Saturn bound applies only on the held branch), not a gap |

**O1 closed to [P] (2026-09-27) under the two-parameter accounting.** a₀ is the declared input anchored to cH₀/2π. The 2π is proved (KMS). μ_std a₀ = 1.10–1.16 implies H₀ ≈ 71–75, bracketing Planck and SH0ES. See the `TARGET_O1` header. **O1/O4 (2026-09-27, corrected the same evening).** The O4 20-point table is **withdrawn** as untraceable, so the old 5.9σ and 2.06σ figures are void. The real high-z data are **inconclusive**. The in-house RC100 measurement (`02_galaxy_dynamics/A0_HIGHZ_MEASUREMENT_2026-09-16.md`) and MUSE-DARK III agree that a₀ at z ~ 1–2 is ~2–2.6× local. Within z 0.6–2.6 the shape favours a constant over H(z) (not established), and the step from z = 0 is calibration-limited. No reading is excluded. Do not cite "constant a₀ excluded at 13σ" or "a₀(0) matches cH₀/2π from MUSE-DARK III"; both were withdrawn the same day.

**Full detail, always current:** `PEER_REVIEW_READINESS.md` — read its top banner before
trusting anything dated earlier.

---

## The rule for dispatching ANY external agent (Manus, Grok, antigravity, or a fresh Claude session)

Every task brief that asks an agent to write physics content **must** include, verbatim,
near the top of the prompt:

> Before writing anything, read
> `/home/mega/Chyren/Research_and_Data/Res_Nova_Monograph/CURRENT_STATE_READ_THIS_FIRST.md` in
> full. Do not use any vault file under `raw/Logs/`, `80_Archive/`, or
> `obsidian_vault_legacy/` as a source of current physics — those are historical records
> only. If anything you find elsewhere contradicts that file, the file wins.

No exceptions. If a dispatch doesn't include this line, don't send it.

**Path corrected 2026-09-20.** This rule previously pointed at
`/home/mega/Res-Nova/CURRENT_STATE_READ_THIS_FIRST.md`, which does not exist. An
agent following the rule verbatim got file-not-found and proceeded unbriefed —
the anti-drift mechanism failing in exactly the way it was written to prevent.

**Enforced since 2026-09-20** by `scripts/dead_branch_scan.py`, wired into
`scripts/local_gate.sh`: retired entities (μ_dual, F_dual, the V₂₄₀ substrate,
generalized Einstein-aether, the internal-gauge soldering, `a0_z_analysis.png`)
now fail the gate if they appear on a live surface. Reading this file is no
longer the only thing standing between a dead branch and the corpus.

## 2026-09-16 audit-cycle update (current physics since the 09-12 verification)

The chiral-cascade program's finite core and six interpretation obligations
were discharged/verified on 2026-09-16; the authoritative state is
`CORE_OBJECTS_AUDIT_LEDGER_2026-09-16.md` and
`PHYSICAL_INTERPRETATION_LAYER_0_2026-09-16.md` (with its dated correction
block). Key state changes an agent must know:

- μ_dual is `[X]` (falsified); **μ_std is the only cosmologically comparable
  μ-row** (a₀ = 1.1607e-10, 95% [9.72, 12.95]e-11).
- The substrate's reflection sector: **Pin⁻ selection is OPEN again [O]**
  (Obligation 4 reopened 2026-09-16 per the correction block below; chain (i)–(v)
  under the standard Witten dictionary selects Pin⁺, not Pin⁻; see `CORE_OBJECTS_AUDIT_LEDGER_2026-09-16.md:103`).
- a₀ = cH₀/2π is **distance-robust but its H₀ inversion is NOT independent**
  (ladder-covariant; 95% intervals only; no side taken in the Hubble
  tension; see `A0_PREDICTION_AUDIT_2026-09-16.md` VERIFICATION section).
- Program residual inputs: μ′(0) = 1, the horizon-selection reason (OPEN, no
  selecting principle; a₀(z) decides — `HORIZON_SELECTION_AUDIT_2026-09-16.md`), the `[C]`
  KMS identification.
- **a₀(z) measured 2026-09-16 (`02_galaxy_dynamics/A0_HIGHZ_MEASUREMENT_2026-09-16.md`):** high-z a₀ flat ~2.2–2.6× SPARC T3 `[C]`; cannot tell Hubble form from constancy; no reading excluded; do NOT cite `a0_z_analysis.png` (3/5 points fabricated).


> **CORRECTION 2026-09-16 (post-merge, PR #61 step v sign reversed):** the standard dictionary (Witten, *Fermion Path Integrals and Topological Phases*, arXiv:1508.04715, §1 and App. A) is Kramers T² = (−1)^F ⇔ spatial/Euclidean reflection R² = +1 ⇔ **Pin⁺**; T² = +1 ⇔ R² = (−1)^F ⇔ Pin⁻ — same convention as this corpus (Pin⁺ reflection lifts square +1). The Wick rotation supplies the factor that flips the sign; the minimal instance (iσ_yK)² = −I is the Lorentzian T, whose Euclidean reflection image squares to +I. So chain (i)–(v) as stated selects **Pin⁺**, not Pin⁻. Pin⁻ requires T² = +1 (Majorana-chain / class BDI sector). Obligation 4 is **OPEN** again; the arithmetic in `scripts/n4_action_derivation.py` is correct, the physics identification in step (v) is not.
