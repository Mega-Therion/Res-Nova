# READ THIS BEFORE WRITING ANY PHYSICS CONTENT

**If you are an agent (Manus, Grok, antigravity, Claude, or anything else) about to write,
summarize, or extend any claim in this theory — stop and read this file completely first.
Do not pull from the Obsidian vault's `raw/Logs/`, `80_Archive/`, `obsidian_vault_legacy/`,
or any file described as "archived," "legacy," or "historical." Those are frozen records of
past states, kept for provenance, not current physics. This file and the two it points to
are the only current physics.**

**Last verified against the physics:** 2026-10-27 (UTC). The audit-cycle state below supersedes
any pre-2026-09-16 substrate claim not updated by it.

The 2026-10-27 record (no tier change). Muse's ν₆ pass-1/pass-2 posts (BLK-684/685) are mirrored verbatim in `06_foundations/nu6_total_embedding/`. Their scripts and raw JSON are not on this machine or in The Hood, so the EFE gate numbers stay `[O]`. The closed-form numbers recompute: λ_s bound 2.5559100974, anchor φ^{1/6} = 1.0835058822 `[E]`. ν₆ stays candidate, not adopted. `02_galaxy_dynamics/vainshtein_preq.py` reruns with exit 0, and its JSON is byte-identical: p_req = 1.890 (precession), 0.408 (Q₂-scaling, from Q₂ = 1.9017920213×10⁻²⁶ at g_e = 1.9×10⁻¹⁰). The stale `p ≥ 2.34` citations in `TARGET_D7` §11.3/§11.5 and the D2 supplement now point there (#186, #187).

Also 2026-10-27 (no tier change): an independent axisymmetric QUMOND external-field solver (`02_galaxy_dynamics/NONSPHERICAL_EFE_SOLVER_2026-10-27.md`, pre-registered in `3681e1c`; #184) reproduces the pinned ν_std Cassini row, Q₂ = 1.90164×10⁻²⁶ s⁻² against 1.90179×10⁻²⁶ (−8×10⁻⁵, inside the reference quadrature's own ~10⁻³ spread; 9.68σ), converges at second order, and matches all 30 frozen Batch-1A Cassini verdicts (max relative difference 2×10⁻⁴). ν₆ (= ν_n, n = 6) gives 4.36×10⁻²⁷ (fitted a₀, g_e = 1.9×10⁻¹⁰): inside the band at QUMOND level `[E]`. This is QUMOND, not AQUAL or AeST; the λ_s-dependent AeST gate stays `[O]`.

The  2026-10-15 record (no  tier or number  change):  three  foundations modules joined the Lean gate, `InitialAlgebraExecution`, `ListInitialAlgebra` and `BinaryPrefixBasis`. They had been committed as lakefile roots without gate targets, which turned CI red on `d736aa3`. They are now gate targets and are scoped adjacent in `05_lean_formalization/ADJACENT_MODULES.txt`, as three separate developments, not one proof (BLK-391). Standalone `lean_check.py` on each: exit 0, no `sorry`, only the standard three axioms behind 4, 12 and 43 public theorems. None of them touches a D-target or the MOND manuscript, whose module count stays 30. CI's `lake build`, which applies the package's `autoImplicit false`, then failed on an unbound `endo` in `InitialAlgebraExecution.finalAlgebraOnNu`; the standalone checks had run without that option. The binder is now explicit, the same one auto-binding had inserted, and no theorem statement changed. `lake build` exit 0 (2026-10-16). CI verify run 38827607035 on `c4523cc` then passed all 73 targets.

Also 2026-10-27 (no tier change): joint Cassini × SPARC scan over ν_n, ν_{γ,β} and tail-cut ν_n (`02_galaxy_dynamics/CASSINI_SPARC_JOINT_SCAN_2026-10-27.md`, pre-registered `6be3885`): no grid point passes both the QUMOND Cassini band and the frozen Batch-1A SPARC gate. Closest approach ν_{6,0.25} at derived a₀: Cassini pass, SPARC fails only tier-1 aggregate (1.298 vs 1). Family-level statement only. Stamped 2026-10-27 17:27 UTC.
Also 2026-10-27 (no tier change): Cassini a₀ boundary sweep (`02_galaxy_dynamics/CASSINI_A0_BOUNDARY_2026-10-27.md`, pre-registered `ec865aa`): with a₀ free over [0.90, 1.30]×10⁻¹⁰ across 12 shapes, no (shape, a₀) passes both Cassini and the best-a₀-relative SPARC gate. For every shape SPARC prefers an a₀ at or above that shape's Cassini edge; Cassini separates a₀ = 1.0422 from 1.1607 (allowing the derived value) only for ν₅ and ν_{6,0.25}.

Also  2026-10-15 (no tier  change): the duality  screening  with  η taken from an external field χ (`06_foundations/SETA_EXTERNAL_FIELD_SCREENING.md`; `02_galaxy_dynamics/duality_screening_cone_check.py`, exit 0). With matter on g (D9), the photon and graviton cones coincide, and neither χ nor S(η) can move them. A disformal ∂χ∂χ term in the matter metric would tilt the photon cone, and GW170817 bounds its coefficient below about 10⁻¹¹, so χ stays out of the matter metric. Putting S into the superseded `TensorSpeed.lean` map leaves that map luminal only at φ = 0 `[X]`. χ as one field is `[O]`: at the Sun's position Cassini needs the Galactic field (η = 1.64–2.07), while the Milky Way needs its environment's (η ≈ 3×10⁻³). Letting χ follow each galaxy's own field raises the SPARC χ² by about 4,200, and refitting a₀ does not recover it: 22302.0 against 18110.5, both at the best a₀ of a 1.0–1.6×10⁻¹⁰ scan (`02_galaxy_dynamics/DUALITY_SCREENING_OWN_FIELD_SPARC.json`).

Also  2026-10-15 (no tier  change): screening on  the  tidal  coordinate x = c²‖∇∇Φ‖/a₀² (`02_galaxy_dynamics/TIDAL_SCREENING_2026-10-15.md`). Built from curvature, the coordinate puts second time derivatives of the metric in the action, an Ostrogradsky ghost. Built from the scalar's Hessian in AeST's single-scalar form, it fails the Legendre–Hadamard condition. The form that survives is QUMOND with the Newtonian tidal tensor and S = 1/(1 + (x/x*)²). On the backgrounds checked it keeps c_T = c to 10⁻¹⁹ (its covariant form is open), passes Cassini at x* = 2.84×10¹² and leaves SPARC unchanged (Δχ² = −0.00; pre-registered in `639fa63`). But x* is a third constant fixed by the Solar System, alongside a₀ and the μ choice. RY ratified a refined rule on 2026-10-15 (first relayed by Muse, then confirmed by RY directly): a constant fixed once by one system is allowed if it predicts the others without retuning, and stays `[O]` until derived. Wide binaries are the kill test: if they force x* to move, the route is dead. That test is now run; see the 2026-10-16 entry below.

Also  2026-10-16 (no tier  change): the tidal  screen's  wide-binary  kill test (`02_galaxy_dynamics/TIDAL_WIDE_BINARY_2026-10-15.md`; pre-registered in `b11edd3`, amendment A1 in `2d095d3`). The 2026-10-15 Cassini and SPARC runs solved the divergence form. Varying the action with S(x(∇∇Φ_N)) adds a term ∂ᵢ∂ⱼWᵢⱼ, W = −(c²/2)S′(x)P(y)H/‖H‖. With W kept, momentum is conserved to 10⁻⁴ and every star falls with the external field. The divergence form fails both: a 0.07–0.94% momentum imbalance, and stars of different mass fall differently. With W kept, Cassini sets x* = 7.04×10¹¹, 4 times lower; W carries 4.44 of the 5.20×10⁻²⁷ s⁻² quadrupole. SPARC is unchanged (Δχ² = −0.0004). The two-body solution predicts Newton below about 3–5 kAU, a dip to 0.85–0.96 of Newton at 7–11 kAU, a peak of 1.2–1.5 at 14–25 kAU (depending on mass), and the unscreened 1.088 beyond about 40 kAU. Against Gaia EDR3 R(s) under C3 the model is not excluded; the loose cut fails, as it does for Newton. The strict cut's power to tell it from Newton is Z = 3.0–3.5, below the pre-registered 4. The pipeline's local-force velocity step is approximate for this force law: orbit-mean speeds are off by up to 2%, comparable to the 10–20 kAU bin's error. Its χ² values for T are therefore descriptive. With energy-integral speeds instead (post-hoc, `02_galaxy_dynamics/tidal_wb_orbit_speed_check.py`), T has strict χ² 0.75–1.9 against Newton's 9.51. It passes the loose cut, calibrated 12.6–16.0. The Γ_r dip washes out of R(s), so a Gaia DR4 test should target the mass-dependent onset of the rise. The screen is well-posed only in QUMOND's two-field reading. AeST reduces to AQUAL, the one-field reading where the screen fails, so the screen's covariant home needs a second field, as in bimetric MOND `[O]`. The Oort cloud test (K3) and a pre-registered mass-stratified dip test on Gaia DR4 are not done.

Standard  for any screening  term (RY agreed  2026-10-16;  BLK-400).  The screen reads only a shadow field computed from matter alone, never the field it shapes, so the who-reads-whom diagram has no loop. S is analytic in the shadow's Hessian, with no kinks. The field equation comes from the action, keeping every term that varying the shadow produces (the W term). Before any data comparison, momentum conservation and universal free fall are checked (gates G5, G10 in `02_galaxy_dynamics/tidal_screening_two_body.py`), and the Galactic external field is included for any system inside the Galaxy.

Also  2026-10-16 (tier change:  the tidal screen  as  built  is now `[X]`): **the tidal screen fails the Oort cloud** (`02_galaxy_dynamics/OORT_TORQUE_2026-10-16.md`; pre-registered in `8902da9`, gates amended in `d3501b0`). Around a lone Sun in the Galactic field, the W term's push raises the potential inside the screening shell. Between about 8.7 and 11.5 kAU, net radial gravity on a test body points outward. A comet falling in from rest therefore reaches perihelion with osculating 1/a = +1.23 to +1.61×10⁻⁴ au⁻¹, so every bound comet would show original a ≤ 8,100 au, while the observed Oort peak lies at 10⁴–10⁵ au. Three independent computations agree to 2%. The offset scales as 1/x*, and Cassini caps x* at 7.04×10¹¹, so no allowed x* reaches the Oort peak. The torque proxy puts the jump semimajor axis at 3.7–4.3 kAU (Newton 26.9, unscreened MOND 2.6), and the pre-registered verdict is 'fails like VNT'. One element of the action could change this: the zero of the screened MOND Lagrangian, C, fixed at 0 by pre-registration. The Oort peak would need C ≈ P(y_e,⊙) = 0.75–0.93, a fourth constant tuned to the solar neighbourhood `[O]`.

**Terminal status (2026-10-16), tidal screen, `C`, D7, and one-field `χ`.** The screened equation with the Lagrangian zero is `02_galaxy_dynamics/SCREENED_LAGRANGIAN_ZERO_C.md`. The solutions are `02_galaxy_dynamics/SCREENED_C_SOLUTIONS.json`, written by `screened_c_solutions.py` (the ledger quotes that file, not a hand-typed number). `C = 0` is the pre-registered model: the JSON records an outward sign change of radial gravity and a positive `1/a`, and the tier stays `[X]`. The `C` that places the W-only binding edge at the geometric centre of `10⁴–10⁵` au is the JSON key `C_oort_peak`. RY (2026-10-16) took that closed form as the working solution: the Oort window is the range of `C`, and the centre is the representative value. `C = 0` stays the failed pre-registered case `[X]`. The algebra is `[D]` (`02_galaxy_dynamics/SCREENED_C_WINDOW_2026-10-16.md`). `x*` is not retuned. D7 branch selection stays `[O]`: the checked selection rules still do not choose a branch, and this run did not add one. One-field `χ` stays `[O]`: one field still cannot supply the Sun's η and the Milky Way's η at the same point (`DUALITY_SCREENING_OWN_FIELD_SPARC.json`). `x*` stays `[O]`: Cassini fixes it and the action does not derive it.

The 2026-10-16/17 follow-ups at the working `C` (recorded 2026-10-21; each was pre-registered, and each number is `[D]` in its own record; no tier changes). With `x*` and a₀ frozen at `C = 0.579124707982253`: Cassini's Q₂ is unchanged, 5.20 and 3.99 × 10⁻²⁷ s⁻², inside the 2σ window, because a constant `C` does not source the quadrupole (`02_galaxy_dynamics/CASSINI_AT_WORKING_C_2026-10-16.md`). The wide-binary shell moves toward Newton but does not vanish (`WIDE_BINARY_AT_WORKING_C_2026-10-16.md`), and on the Gaia C3 test it is not excluded, clean calibrated χ² 2.995, loose 18.171 against the 18.5 bar (`WORKING_C_WIDE_BINARY_RS_2026-10-16.md`). SPARC is not excluded; the total equals unscreened μ_std to 0.002 (`SPARC_AT_WORKING_C_2026-10-16.md`). Four dwarfs pass under the Wolf formula, M/L ≤ 3 at σ−1σ (`DWARF_ML_WORKING_C_2026-10-16.md`). The comet-cloud rays all stay bound inside 10⁴–10⁵ au (`COMET_CLOUD_WORKING_C_2026-10-17.md`). The ν₆ runs of the same day: Oort peak preserved, wide binaries not excluded, dwarf M/L inconclusive under the BLK-39 rule. Cosmology (`04_cosmology/HDE_CMB_PHANTOM_2026-10-17.md`, `[E]`): under the fixed CMB block the late-time HDE edge does not survive (Δχ² = +46.3 against ΛCDM; the bar for a win was < −9), and DESI DR2 BAO excludes the phantom-crossing window; the ln 2 coefficient stays `[O]`. The Vainshtein exponent was recomputed without the retracted 5.7 × 10⁵ factor, p = 1.890 required, which a cubic Galileon (1.5) does not supply; `TARGET_D7` §11.3's `p ≥ 2.34` stays flagged, and Cassini is not passed by that route (`02_galaxy_dynamics/VAINSHTEIN_PREQ.md`). `C` is tuned to the solar neighbourhood, not derived: it is a declared input alongside `x*`.

The 2026-10-14 record (no tier change): `AEST_TOTAL_SCALAR_CORRESPONDENCE_2026-10-14.md` (26 checks). In the spherical quasistatic limit, the scalar function whose total law is the fitted μ_std law is 𝒥(𝒴(x)) = a₀²[2ηF_std(x) − η²y(x)²], η = λ_s/(1+λ_s), parametric in x = g/a₀. It is single-valued, and meets both static ghost conditions of `TARGET_D7` §5, exactly when λ_s < (27+12√6)/5 = 11.2788 `[D]`. D9's function puts μ_std in the scalar channel; its total law is ν_std only as λ_s → 0 (Paper I §III), and is up to 23% off at λ_s = 1. D9's function stays the one in use; replacing it with the total-law function is `[O]` (D7). Under the total-law function the spherical solar-system residual has no λ_s in it, so the λ_s ceilings below (Cassini-Q₂ 2.60; Saturn precession 2.21 and 2.68) hold for the scalar-channel function only. `TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md` §4–§5 writes a₀ where `TARGET_D7` §2.1 has ã₀ = (1+λ_s)a₀; a note there records it. Also (TTEY, `[D]`): the AQUAL scalar sector satisfies the null energy condition and carries ρ ≥ 0, both from the proven ghost condition F′ = μ_std > 0 — `T_μν k^μ k^ν = (1/4πG) F′ (k·∇φ)² ≥ 0` (`scripts/ttey_scalar_nec.py`, 8/8; `TTEY_COUPLING_AND_THRUST_ACCOUNTING.md` §5 Q1). So the galaxy sector cannot source a warp bubble; TTEY's own exotic-energy route uses a separate double-well + vacuum-relative construction (`Tension_Stress_Energy_Tensor.md`), still open. Neither "TTEY works" nor "TTEY is dead". Field-model map (`TTEY_FIELD_MODEL_RECONCILIATION_2026-10-14.md`, 7/7): the galaxy AQUAL field and the engineering Poisson field `Δ𝒯=κρ` are one field (Poisson is the μ_std→1 Newtonian limit); the TTEY warp field is a *separate, postulated, massive* double-well scalar (`m²=8λχ²`) that nothing in the action derives — so the warp route's prior gap is existence of that field, before any quantum-inequality bound.

The 2026-10-13 record (no tier or number changes): `HORIZON_SELECTION_AUDIT_2026-09-16.md` and its verifier are restored to the PR #66 version (`d0036ca`, 11/11), which this file already cited ("no selecting principle; a₀(z) decides"). Commit `f3d63b6` had replaced them with a version claiming T = ħH/2π holds "without approximations"; its cited sources (Cai–Cao–Hu 2009 p. 7; Helou 2015) state that form drops the Ṙ_A term. The core-objects ledger, layer 0 and the research-hub card CLM-HORIZON-01 now read OPEN.
Same day: residual beam smearing in the high-z a₀ sample was tested (`scripts/a0_highz_resolution_test.py`). No resolution dependence is detected, and the allowed bias moves ln a₀ by at most −0.085 across z = 0.6–2.6, against +1.026 for the Hubble shape. Systematic (ii) of `A0_HIGHZ_MEASUREMENT_2026-09-16.md` is narrowed to the Vc scale; the verdict stays [O].
Also: the fDM-prior split test is inconclusive by construction (#170, recorded null), and the estimator self-test bias is nearly constant (−0.039 vs −0.042 in ln at the two truths), so it shifts normalization, not shape. Open for a₀(z): the fDM prior and the Vc scale. The Vc-scale test (`scripts/a0_highz_pressure_scale_test.py`) shows the shape depends on the pressure-support correction: n = −0.28 at the published Burkert scale, and the Hubble shape enters the 95% interval only at three times that scale or more. Whether such a scale is physical is open and decisive.
First literature pass (abstracts only, [C]): Kretschmer et al. 2021 find the correction at R_e in simulations is about 0.3× Burkert's, and Wellons et al. 2020 bound the bias at 40%; both point away from the ≥ 3× the Hubble shape needs. Reading [O] until the papers are read in full.

Also 2026-10-13 (no tier change): `PILLAR_IV_MU_IDENTITY_2026-10-13.md`. Solved from its generator, the Pillar IV two-level steady state is exactly ρ₁₁ = μ²/2 and C = √2·μ·√(1−μ²) with μ = μ_std(2√2·u/γ); C peaks at μ = 1/√2. The retracted premise "coherence = μ(u/γ)" stays false. Identities `[D]`; any identification with g/a₀ is `[O]`.

The 2026-10-09 decisions (RY) record. **These do change tiers and one cited number:**
- **[P] rule.** A row keeps [P] only where a named Lean theorem proves its claim; otherwise it is [D] or [O].
  - D1: [P] core (`MuStdUniqueness.theorem_A_constitutive`, F′ = xμ_std as `HasDerivAt`; `MuStdFoundations`), [D] rebuild.
  - D3, D7: [D] with an [O] part (branch selection). D6: [D] with an [O] part (covariant profile). D8: [D].
  - No registry state changed: those claims were already `derived`/`computed`.
  - O1, O5 and O6 were relabelled by the same rule (they had been flagged, not changed): O1 → [A]; [O] (a declared input; the 2π identity open), O5 and O6 → [E] (reproducibility measurements). No number changed.
  - Vacuity screen 0.2: the six D1-core theorems PASS. The receipts were re-signed on the unchanged Lean sources (`proof-records/`).
- **a₀ headline: 1.1607×10⁻¹⁰ m/s²** (μ_std, 175 galaxies, `A0_DISTANCE_CORRECTED_2026-09-16.json` T1; bootstrap 95% [0.972, 1.295]).
  - Switched on README, the Zenodo metadata, FOR_REFEREES, the parameter budget, open problems, the manuscript's eq. a0_measured, checklists and ledgers. 1.116 is labelled everywhere as the superseded μ_dual fit. Pre-registrations and dated records are unchanged.
  - The front-door monograph gets a dated correction box on its H₀ inversion. At the live a₀ it gives H₀ = 75.1 (95% [62.9, 83.7]); the 78 galaxies with H₀-independent distances give 75.2. The route is not free of the distance ladder.
  - Rerun at the live a₀: the Cassini-Q₂ λ_s heuristic is ≤ 2.60 (it was 2.70 at 1.116), and the Saturn/Mercury margins are 46.7×/1157× (`02_galaxy_dynamics/LAMBDA_S_AT_LIVE_A0_2026-10-09.txt`). The quotable "λ_s ≲ 1–3" stands. These ceilings use the scalar-channel residual (1+λ_s)³a₀²/2g_N; under the total-law function of `AEST_TOTAL_SCALAR_CORRESPONDENCE_2026-10-14.md` they do not bound λ_s (2026-10-14).
  - The live Λ_SC range is 110.0–118.1 μm across the three live a₀ values: the literature value, the μ_std SPARC fit and cH₀/2π (`LAMBDA_SC_UNSCREENED.json`).
    *History (2026-10-09):* the first rerun gave 109–118 μm because it included a fourth value, 1.2211×10⁻¹⁰ (5.461×10⁻¹¹·√5, the "canonical constants block"). That value had been mislabelled "horizon anchor" and was briefly carried as unreconciled `[O]`. *Traced the same day:* 5.461×10⁻¹¹ is χ²cH₀/(2πκ) with χ² = ½ and κ = √0.91 (5.4626×10⁻¹¹ at H₀ = 67.4), and the √5 was the E8→H₄ "projection" that multiplied it back up to MOND scale. Both were retired on 2026-07-01 in favour of bare cH₀/2π (`SPARC_CHI2_FINDINGS.md`, Aeon research archive). So 1.2211×10⁻¹⁰ is a historical value, not a live fourth a₀. Without it the live Λ_SC range is 110.0–118.1 μm (literature 1.2×10⁻¹⁰ → 110.0, μ_std fit 1.1607×10⁻¹⁰ → 111.9, cH₀/2π → 118.1; `LAMBDA_SC_UNSCREENED.json`).
- **SPARC benchmark surfaces (PR #143).**
  - The canonical manuscript, `FOR_REFEREES.md`, `SPARC_PARAMETER_BUDGET.md`, the verification ledger and the release checklist were still printing the μ_dual-era benchmark: Tier 0 GOD 9.20 vs MOND 11.35, Tier 1 2.95 vs 2.89.
  - Under μ_std (`PARAMETER_LEDGER.json`, which reproduces exactly, 0 fields differing on 2026-10-09) the Tier 0 order reverses: MOND 9.93, GOD 11.08. Tier 1 is a tie: 3.36 vs 3.41, aggregate 6.09 vs 6.03.
  - These tables are now generated by `scripts/sparc_benchmark_tables.py`, and `local_gate.sh` fails on drift. The self-test detects 4/4 sabotages. The dead-branch scan also flags the old numbers.
  - `sparc_reproduce.py` had three defects: unsigned V_gas, Υ applied to V instead of V², and f_d dividing R. All three are fixed. A synthetic parity test against `parameter_ledger.py` catches each one; sabotaged copies exit 1.
  - CLM-04 now reads the μ_std strict unit-M/L median, 15.01; the old 29.12 was the μ_dual-era `VERIFICATION_RUN_001` value. CLM-06 is re-derived at 51.58 / 204.66, which reproduces RUN_001 to 0.007%.
  - The manuscript's raw-data hash `e76e6752…` has no recorded definition and none of the tested definitions reproduces it. It is replaced by the SHA-256 of `RAW_DATA_MANIFEST.sha256`, `e78c1d68…`.
  - The manuscript's Tier 0 definition and its parameter count were also wrong. Tier 0 uses M/L at the prior means, not 1. The 374 parameters are 171 Υ_disk + 32 Υ_bulge + 171 f_d, not "174 + 199 + 1".
- **Notation.** Fixed: the K₀ erratum and the `boost('E')` warning (appended to the orientation prereg; the pinned pipeline file is untouched), the "scalar field 𝒴" wording (the field is φ; 𝒴 is its invariant), φ vs ϕ on the D7 row, and CLM-02's `mu_simple` (it names μ_std).

The 2026-10-09 stamp records (none of it changes a tier or a physical result):
- **Signed vkernel receipts for the Lean modules behind the `[P]` rows** (`proof-records/`, `c6c527f`).
  - Two configs were added under `05_lean_formalization/`. No Lean source changed.
  - The receipt check finds that **D1 is `[P]` but names no Lean module**.
  - A vacuity screen flags 14 of D8's 16 Lean theorems. This includes `physical_frame_tensor_speed_unity`, which restates its hypothesis. `docs/grounding_ledger.yaml` already rates those modules ARITH.
  - The four AeSTStealthSector PPN theorems are `rfl` on a structure literal.
  - A receipt establishes build and proof-term integrity of the listed statements against the recorded source commitment (standard three axioms, independent checker). It does not establish their non-vacuity or their match to manuscript claims.
  - These go to RY as findings (`proof-records/README.md`). No tier was changed.
- **Wide-binary orientation pre-registration, Amendment A** (`8583529`), before any orientation look.
  - Four models survive C3, not two.
  - The pipeline's `boost('E')` has the anisotropy sign opposite the QUMOND field solution. Its angle average is identical, so the R(s) fits are unaffected.
  - Gate 1 is expected to stop as underpowered.
  - `WIDE_BINARY_FINAL_2026-10-04.md`'s loose-cut prose was corrected; the verdict is unchanged (`1012bca`).
- **Derivative-claim correction (PR #141).** `F_dual(x) = x^2/2 - x + ln(1+x)` has `F_dual'(x) = x - 1 + 1/(1+x) = x^2/(1+x)`, not `x/(1+x)`; the two agree only at x = 0 and x = 1.
  - The PR's first theorem did not compile at `5e89c53`: CI lean-gate and a local gate both exited 1, because the module had no calculus imports.
  - `5e1fa72` makes it elaborate and adds `F_dual_hasDerivAt_sq`, `F_dual_hasDerivAt_mu` and the refutation `F_dual_deriv_ne_mu_derived`. Gate: `verify_all_proofs.sh` exit 0, 66/66 targets, standard three axioms. Vacuity screen 0.2: PASS on all four.
  - CLM-01 now states the corrected identity and stays `formally-verified`, as it was on main under the false wording. This is a wording correction, not a tier upgrade. D1.2 stays `[X]`, and the branch stays retired (2026-09-12).
- **SPARC parser repair (PR #138), recomputed 2026-10-09** with the official files (175/175 verified).
  - The parser change leaves `SPARC_175_GOD_fits.csv` and `SPARC_175_summary.json` byte-identical, because `v_baryon` squares `v_gas`.
  - The real difference from `parameter_ledger.py` is `v_baryon`: gas unsigned, and Υ applied to V instead of V².
  - CLM-04's and CLM-06's numbers come from `VERIFICATION_RUN_001` (2026-08-14), not from the files those records list.
  - Findings are on PR #138. No committed number changed.

- **The adjacent Navier–Stokes program, PR #142.**
  - `SovereignRegularity.lean` identifiers and comments were renamed to match `THEORY_ASSUMPTION_AUDIT.md`. Its proof terms are unchanged, and F7's pin was moved.
  - `NavierStokesTarget.lean` was added and scoped in `ADJACENT_MODULES.txt`. It freezes the periodic target as a `Prop` and proves a single-time alignment step.
  - None of this touches a D-target or the MOND manuscript.
- **The adjacent Navier–Stokes program, PR #159 (2026-10-12).** `NavierStokesDomain.lean` (the T³ = (ℝ/ℤ)³ types and two quotient lemmas) and `NavierStokesSpacetimeBridge.lean` (a time-indexed alignment interface whose one theorem restates its own hypothesis) were added and scoped in `ADJACENT_MODULES.txt`. They are interfaces only. Neither proves persistence or regularity, and neither touches a D-target or the MOND manuscript.
- **Manuscript O4 withdrawal alignment (2026-10-12).** `res_nova_manuscript.tex`, `README.md`, `OPEN_PROBLEMS_AND_TESTS.md`, and `SUBMISSION/COVER_LETTER_PRD.md` were scrubbed of surviving mentions of the void 5.9σ and 2.06σ figures from the withdrawn 20-point high-z table. The text records the withdrawal under `[X]` (`03_observer_jwst/O4_REAL_DATA_MUSE_DARK_III_2026-09-27.md`), affirms the empirical status on real kinematics (RC100, MUSE-DARK III) as inconclusive, and confirms neither reading is excluded.

- **Withdrawn phrasing and swapped names, now gated (`scripts/dead_branch_scan.py`).**
  - New entity: the withdrawn "zero free parameters / parameter-free" claim. The standing accounting is two irreducible inputs, the a₀ scale and the μ choice.
  - New entity: swapped μ names. The literature's simple μ is x/(1+x) and its standard μ is x/√(1+x²) = μ_std (Famaey & McGaugh 2012, Eqs. 42, 49).
  - The μ_dual and F_dual patterns now match Unicode. That is how book chapters 12 and 15 still presented x/(1+x) as the theory's core.
  - The live surfaces that fired were fixed, and the historical ones got dated notices.
  - The fourth a₀ (1.2211×10⁻¹⁰) is traced and retired, and the live Λ_SC range is 110.0–118.1 μm; see the Λ_SC bullet above.
  - `TARGET_D10`'s a₀ line read "DERIVED, no free parameter". It now carries the `[O]` that the 1/2π normalization already had (`build/STATUS_AND_SCOPE.tex`). No D-tier and no physical result changed.

`PEER_REVIEW_READINESS.md` was re-read. At that point its D8 row was `[P]` for the structural argument (no TT piece in δA),
with arithmetic Lean behind it. The [P]-rule decision above, made the same day, relabelled D8 `[D]`. This stamp is not a new physical result.

The 2026-10-06 stamp records:
- **A comment-only correction in `PillarIV_AntiDriftGate.lean` (`f38d21a`).** Its κ docstrings now follow RY's
  2026-09-26 rejection of the 2026-09-24 "0.9561 lock": the corpus κ is 0.9539. Both `kappaBand` evaluations (7/10
  and 1/√2) are unchanged theorems; the code outside comments is byte-identical.
- **Exploratory D7 box-extension bookkeeping** (`exploration/d7_stage2/PREREG_BOX_EXTEND_2026-10-06.md`). The anchor
  passed and attempt 1 did not converge, so there is no verdict.

`PEER_REVIEW_READINESS.md` was re-read and carries no κ statement. This stamp is not a new physical result.

The 2026-10-04 stamp recorded a pointer move of the Navier–Stokes notes into `archive/legacy_root/` and the public
framing of the SPARC tier-0 comparison.

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
  A size-based shield provably needs a new constant (dimensional no-go). The environmental form
  S = 1 − μ_std(g_ext/a0), which adds no constant beyond the two irreducible ones (a0 and the μ_std choice), passes Cassini (+0.25σ / −0.10σ) and does not degrade
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
- **Corrected 2026-09-30 — the 2026-09-29 `MuStdFoundations.lean` entry overclaimed in three ways.**
  What stands `[P]`: the constitutive action $F_{\text{std}}(x) = \int_0^x s\,\mu_{\text{std}}(s)\,ds
  = \tfrac12[x\sqrt{1+x^2} - \operatorname{arsinh} x]$ (the entry had printed $\sqrt{1+x^2}-1$,
  which is $\int\mu$, not $\int s\mu$), with $F' = x\mu_{\text{std}}$ and strict convexity $F'' > 0$.
  **Retracted:** "sound speed $c_s^2 \in [1/2, 1)$, strictly subluminal". That expression,
  $\mu/(x\mu)'$, is a ratio of spatial stiffnesses and is the *reciprocal* of the actual characteristic
  speed. In the relativistic P(X) completion the speed along the gradient is
  $c_\parallel^2 = xF''/F' = (x^2+2)/(x^2+1) \in (1, 2]$ — **superluminal** (RAQUAL acausality). The
  module now proves this from `deriv F_std` (`c_long_sq_superluminal`). AeST's own scalar speed is D6's
  separate result and is unaffected. **Relabelled:** "Cassini clearance". $1-\mu_{\text{std}} \le 2\times10^{-12}$
  at Saturn (1.62×10⁻¹² at the live a₀ = 1.1607×10⁻¹⁰, not the superseded 1.116) is the isolated-Sun
  **monopole** only. It was compared with the Cassini bound on $\gamma-1$, a different observable. The
  binding Cassini test is the EFE quadrupole, which bare μ_std **fails** (see the 09-27 bullet above).
- **Corrected 2026-09-30 — `AeSTStealthSector.lean` does not contain field equations.** It proves, by
  `ring`, that $P^{00}(-1,1)=0$, $\mathcal{Y}=0$ and $Q=Q_0$ in the free-fall frame. Its PPN theorems are
  `rfl` on values it *defines* as γ = β = 1, α₁ = α₂ = 0. The "all 8 AeST field-equation residuals vanish
  on PG Schwarzschild" statement rests on the D3 note 7 §34 symbolic check `[D]` and on Skordis &
  Vokrouhlický 2024 `[C]`, not on this module, and applies only if the dragged branch is selected (D7, open).

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

**Added 2026-10-21 (no tier change; AeST CMB stays reported-not-verified, now with a named
obstruction).** SZ's linear equations (definitions of δ, θ, Π; eqs. 9–10; the vector equation)
re-derive from the AeST action with residual 0 in SZ's own sign conventions, so sign conventions
are ruled out as the cause of our mismatch `[D]`. Two of our own results are withdrawn: the
matter-era `δ_AeST/δ_CDM = 0.83–1.06` came from a dropped `φ̄̇` factor in γ
(`boltzmann_units_fixed.py:75`) `[X]`, and the old "0.001 annihilation" came from the corpus
`w₀ = 1.23×10⁻⁸`, not SZ's `1.42×10⁻¹²`. At SZ's Fig. 1 point with F_Y = 0 (their linear system),
`δ_φ/δ_CDM = 1.00 / 0.61 / −1.67` at k = 0.01 / 0.05 / 0.1 Mpc⁻¹ (r = 10⁻², stable to 3% in a_i),
driven by a k-independent (E, α) vector-sector growing mode of ~1.9 per e-fold that SZ's
Minkowski stability proof does not cover. Whether that mode is physical is `[O]`; an independent-code
cross-check is in progress. Source:
`Research_and_Data/05_Scripts_and_Tools/02_cosmology_cmb_and_chi_field/cmb_aest/SIGN_CONVENTION_REDERIVATION_2026-10-21.md`
(Chyren `d0094073e`); `TARGET_D5` §3.5, D10 §6 and D11 carry matching corrections.

### 3. The covariant completion action is AeST, NOT generalized Einstein-aether

- D7's action was rewritten 2026-09-12 to genuine AeST (Skordis-Złośnik arXiv:2007.00082):
  scalar field φ entering through its kinetic invariant 𝒴 = q^{μν}∇_μφ∇_νφ (𝒴 is not itself the field; wording corrected 2026-10-09), minimal matter coupling. The prior version (vector field 𝒦, disformal
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
| D1 | [P] core; [D] rebuild | **Relabelled 2026-10-09 under the [P] rule** ([P] only where a named Lean theorem proves the claim). [P]: F′ = xμ_std as `HasDerivAt` on F_std itself (`MuStdUniqueness.theorem_A_constitutive`), strict convexity and c_∥² > 1 (`MuStdFoundations`); all six screen PASS. [D]: the μ_std rebuild **complete** (`TARGET_D1_SUPPLEMENT`, re-run 2026-09-12); its '1300× solar-system clear' is monopole-only — EFE quadrupole fails at the horizon-anchor a₀. A phenomenological screen can pass. It has no covariant realization yet (2026-09-27) |
| D2 | [P] | **Closed 2026-09-27 under the two-irreducible-parameters accounting.** μ is parameter 2 (the functional choice): structurally motivated (Postulate R / chiral coordinate), empirically selected (n≈2, Δχ²/s 700–1400), ghost-free, Cassini-consistent with screening. Duality holds for all n (`MuNDuality.lean`). A covariant argument forcing μ is a research question, not a gap |
| D3 | [D]; [O] | **Relabelled 2026-10-09 under the [P] rule** ([P] only where a named Lean theorem proves the claim): the PPN result is a symbolic (CAS) derivation with no Lean theorem behind it, so [D]; branch selection is [O]. **Conditional on D7 branch selection (downgraded 2026-09-30 from "Closed").** Verified symbolically (note 7 §34), and exact only on the dragged branch, whose selection D7 lists as open. The dragged branch completes to AeST's stealth sector (Skordis & Vokrouhlický 2024): the aether is a constant-norm clock-field gradient, i.e. the free-fall river. All field-equation residuals are 0 on PG Schwarzschild, so every PPN parameter is GR, up to external-field and cosmological-density corrections, wherever the clock field is single-valued (the planets, if v_rel ≳ 60 km/s, an estimate). c₂ lift excluded (|α₁| ≥ 4K_B). λ_s is not constrained by a dragged Sun |
| D5 | [P/O] | Cosh cosmology time-sector formalized (`CoshCosmology.lean`, 6 theorems, 0 sorry, ARITH). A 256³ run (`04_cosmology/D5_RUN`) keeps the power-spectrum excess under 5% for ε(z=0) = 0.00233. That ε is the retired linear factor, so the run is not a closure for the live branch |
| D6 | [D]; [O] | **Relabelled 2026-10-09 under the [P] rule** ([P] only where a named Lean theorem proves the claim): no Lean module carries these results, so they are [D]; the covariant profile, on the open D7 branch, is [O]. Ghost-free and subluminal are closed (2026-09-27): spin-2 at c, spin-1 luminal front, scalar c_s < c above 𝒦₂ ≥ 3.75, met at both SZ points. J-normalization is one family, J = 2λ_sã₀²F. The old "Λ_SC far below experiments" claim stays retracted (unit error). The corrected scale is Λ_SC ≈ 1.8 meV. Unscreened, the range is 110.0–118.1 μm across the live a₀ values: literature 1.2 (110.0 μm), live μ_std SPARC fit 1.1607 (111.9) and the horizon anchor cH₀/2π = 1.042 (118.1), all ×10⁻¹⁰. The retired rigid-canon 5.461×10⁻¹¹·√5 = 1.2211 (109.1), traced 2026-10-09 to the construction retired on 2026-07-01, is kept in the JSON as history (`02_galaxy_dynamics/LAMBDA_SC_UNSCREENED.json`, rerun 2026-10-09; until then the 1.2211 value was mislabelled "horizon-anchor" and the SPARC value was the superseded 1.116), inside the Eöt-Wash window quoted at λ ≥ 39 μm. That comparison does not use screening. "Not excluded" is a screening estimate in `TARGET_D6_SUPPLEMENT_LSC` §3, not a proof, and the covariant profile sits on the D7 branch, which is open. EP closure η ≲ 4×10⁻⁴⁹ is the supplement's §4c estimate |
| D7 | [D]; [O] | **Relabelled 2026-10-09 under the [P] rule** ([P] only where a named Lean theorem proves the claim): `AeSTStealthSector.lean` is bookkeeping (all 9 theorems flagged by the vacuity screen; its four PPN theorems are `rfl` on values typed into a structure), so the stealth screening is [D] (the D3 §34 CAS check) and branch selection is [O]. This is a relabel, not a verdict: AeST is not falsified. AeST action; the stealth sector screens the Sun (D3 §34). **Branch selection is open.** The linear boosted-held check (`TARGET_D7_SUPPLEMENT` §7) uses all rows, gravity included, and validated operators. The wind's force on a dwarf's aether, R_z/v = 8K_B∇²Φ + (4−8K_B)∂_z g_z − 6K_B∂_z ĝ_z, gives a Poisson response, ∇²δφ = −R_z/[(4+λ)v], with no linear wake. At K_B = 1/2 and 𝒦₂ = 75, δφ ≈ −0.98(ϕ+Φ̂) (two glyphs, two objects: φ = γ𝒬₀(t − v·x) + ϕ is the full scalar, the clock, and ϕ is its static part; `TARGET_D7_SUPPLEMENT` §7): linear theory cancels the MOND field to O(𝒥′), pointing toward Newtonian satellites. **Not proved beyond linear order.** Open: other K_B, external-field-dominated outskirts, a non-linear held branch. **Non-linear steady state (2026-10-02/03, `exploration/d7_stage2/`, exploratory):** every converged satellite-speed solve is stripped (Newton channel at GR's 1 − K_B/2 to 0.2%). But the remnant is not box-converged, gates B2 and C fail as pre-registered, and a pre-registered deflation search at one point (K_B = 1/2, 𝒦₂ = 75) found no second steady state from six guesses `[O]`. The proposed no-go in `D7_AEST_BRANCH_SELECTION_NO_GO_VERDICT.md` is **not adopted**. Closing it needs a box-converged remnant, gates B2/C passing, and a branch scan over K_B and the outskirts. The phenomenological law is unaffected. Do NOT cite "AeST disfavoured by satellites" or a D7 no-go as proved. K_B scan 2026-10-04, one grid only (`exploration/d7_stage2/KB_SCAN_C1_16x32.json`, 16×32, 100 km/s, 10 kpc): K_B = 0.25, 0.5, and 1.0 all converge, and none is a held remnant (Y/Y_static = 0.0019, 0.0372, 0.0030). K_B = 0.5 matches the earlier box sweep to the printed digits. Box extension past 1000 kpc, 2026-10-06, pre-registered and exploratory (`exploration/d7_stage2/BOX_EXTENSION_SUMMARY_2026-10-06.md`): four solver attempts reached no converged solve beyond 1000 kpc, so the extension's verdict never fired. Arithmetic precision and diagonal scaling are measured not to be the cause. The smallest Hessian eigenvalue falls as R^−3, dominated by Ω. Across the five committed boxes the remnant decays with steepening slope and no positive floor, which is consistent with a box artefact but not box-converged `[O]`. The next tool is continuation or trust-region Newton (a fold is the open hypothesis). Box convergence, the outskirts, and uniqueness remain open. Open (2026-10-14): whether to replace D9's scalar-channel function with the total-law function of `AEST_TOTAL_SCALAR_CORRESPONDENCE_2026-10-14.md` |
| D8 | [D] | c_T=c — upgraded to structural, strongest result in the corpus. **Relabelled 2026-10-09 under the [P] rule** ([P] only where a named Lean theorem proves the claim): the result is the structural derivation (no TT piece in δA under minimal AeST coupling, `TARGET_D8_TENSOR_SPEED.md`) [D]. `TensorSpeed.lean` does not prove it: its theorems evaluate the Einstein-aether formula c_T² = 1/(1−c₁₃) at c₁₃ = 0, model the superseded disformal coupling, and evaluate Foster–Jacobson α₁, which this theory must not cite (it sits on the c₁₂₃ = 0 locus) [arith] |
| D9 | [P] | **Closed 2026-09-27.** μ_std embedding derived by calculus (`SZStdEmbedding.lean`: J_std = F_std(√𝒴) gives 2J′ = μ_std, with J′ > 0). λ_s is the family's overall scale, an AeST parameter (the Saturn bound applies only on the held branch), not a gap. Scope (2026-10-14): this embeds μ_std in the scalar channel. The function whose total law is μ_std, for λ_s < 11.2788, is in `AEST_TOTAL_SCALAR_CORRESPONDENCE_2026-10-14.md` `[D]`; replacing D9's function with it is `[O]` (D7) |

**O1 (2026-09-27; 2π wording corrected 2026-09-30).** a₀ is the declared input anchored to cH₀/2π. **The 2π is declared, not proved.** `HorizonScale.lean` proves the opposite normalisation: equating Unruh and Gibbons–Hawking temperatures gives a = cH, with the 2π *cancelling* (ξ = 1), a factor 2π ≈ 6.3 away from the anchor. The anchor a₀ = cH₀/2π is `[O]` (heuristic divisor), as the O1 file's own table says. μ_std a₀ = 1.10–1.16 implies central H₀ ≈ 71–75: above Planck's 67.4 and around SH0ES's 73, with both inside the 95% interval (T1: [62.9, 83.7]). Until 2026-10-09 this line said "bracketing Planck and SH0ES", which only the interval does. See the `TARGET_O1` header. **O1/O4 (2026-09-27, corrected the same evening).** The O4 20-point table is **withdrawn** as untraceable, so the old 5.9σ and 2.06σ figures are void. The real high-z data are **inconclusive**. The in-house RC100 measurement (`02_galaxy_dynamics/A0_HIGHZ_MEASUREMENT_2026-09-16.md`) and MUSE-DARK III agree that a₀ at z ~ 1–2 is ~2–2.6× local. Within z 0.6–2.6 the shape favours a constant over H(z) (not established), and the step from z = 0 is calibration-limited. No reading is excluded. Do not cite "constant a₀ excluded at 13σ" or "a₀(0) matches cH₀/2π from MUSE-DARK III"; both were withdrawn the same day.

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
