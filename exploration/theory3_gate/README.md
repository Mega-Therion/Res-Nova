# Theory 3 gate (2026-11-18) — exploration, no tier change

> **CURRENT VERDICT (latest, read first).** Theory 3 is UNSAT (corrected reason: see "CORRECTION — Theory 3 part (A)"). The open door (single-order quartic Galileon + scaling compensator) is **CLOSED [O]** by the nested field solution (last section). A mixed cubic+quartic Galileon is not covered and stays open. Earlier "door stays OPEN" lines are history. What survives: the exact stretched-cone solution and its angular-leak no-go for Vainshtein screening; the BBN corollary (screening the solar-system scalar removes λ_s from BBN); the D5 r_C item evaluated with D5's quoted estimate (SZ's run: 144/175 SPARC galaxies beyond r_C, [O]). Mixed L₃ + L₄ is now also closed [O] (last section): the pure quartic is gradient-unstable around the Sun, and the cubic that stabilises it leaves a Cassini leak 4–16× over the bound. The symmetron (density-melting) route is closed too (last section). That closes every standard screening class for the AeST MOND scalar on these gates.

Runs the panel's "Theory 3" (w=1/3 tracker replacing Q³ + p≥3/2 Vainshtein screening) as SAT/UNSAT.
`python3 theory3_gate.py` → `THEORY3_GATE.json`.

**Verdict: UNSAT as proposed.**

1. BBN, free w=1/3 field: ρ_φ∝a⁻⁴ for any amplitude, so ΔN_eff (needs ≈ +0.66 to cancel the √(27/32) deficit) is an initial condition, not a prediction. Fails the stated metric.
2. BBN, scaling attractor (amplitude fixed by a Lagrangian slope k): the RD window Ω_φ∈[0.033,0.125] forces Ω_φ≥0.0248 in matter domination, ≈7× the Planck early-DE bound (0.0036; still >1× for any bound under 0.025). Survives only if scaling exits before recombination — a new tuned scale.
3. Cassini: VAINSHTEIN_PREQ [D] needs p≥1.890. Cubic Galileon (p=1.5, the proposal) fails. Quartic (p=2) clears it but generic G4X breaks c_T=c (GW170817).

Open door left: a DHOST/beyond-Horndeski quartic with c_T=c (p=2) plus a scaling field that exits before z~1100. Both add structure; neither is derived. Per the panel's own rule, UNSAT routes to Theory 1 (two-phase), whose test is the same three gates.

## Open door, run 2 (`open_door_gate.py` → `OPEN_DOOR_GATE.json`) — [O], O(1) factors dropped
- Decay bound (Creminelli+ 2018, arXiv:1809.03484: α_H=0 + c_T=c rules out quartic/quintic GLPV) kills beyond-Horndeski/DHOST quartics. Only **pure Horndeski quartic** (α_H=0, p=2) remains, bound by |α_T|≲1e-15.
- p=2 needs the Sun's Vainshtein radius in **[1.09, 2.36] pc** (lower: Mercury precession; upper: Galactic cap). Window exists.
- α_T ≈ (4.6e-13 … 4.9e-11)·ε⁴ with ε = φ̇/(M_p H₀) → needs **ε ≲ 0.07–0.22**.
- At SZ21's reference Q₀=0.1 Mpc⁻¹, ε≈430 → α_T≈0.02–2: **closed**. Survives only if Q₀ ≲ ~2×10⁻⁵ Mpc⁻¹ AND that still gives the dust branch. That is the single deciding check.
- BBN compensator exit: one scalar mass in [1.9e-27, 2.2e-16] eV (11 decades — a loose, not fine, tune).

## Small-Q₀ dust check (`small_q0_dust_check.py` → `SMALL_Q0_DUST.json`) — [O]
- Dust validity (Q−Q₀)/Q₀ = ρ/(μ²(2−K_B)) — **Q₀ cancels** (SymPy-asserted). Only μ = √(2K₂/(2−K_B))·Q₀ matters.
- Need μ ≳ 7.6 Mpc⁻¹ (dust by z_rec) to 41 Mpc⁻¹ (by z_eq). Q₀ ≤ 2×10⁻⁵ Mpc⁻¹ just needs K₂ ≈ 7×10¹⁰–2×10¹² (2.5×10⁷ × SZ's).
- **Door stays OPEN.** New flags: (a) strong-coupling scale of Q fluctuations at K₂~10¹¹; (b) 1/μ ≲ 25–130 kpc caps MOND's reach (inherited from SZ21, not new to this door).

## SPARC reach vs 1/μ (`sparc_mu_reach.py` → `SPARC_MU_REACH.json`) — [O]
- Largest SPARC radius is 108.3 kpc. With 1/μ = 132.7 kpc (dust by recombination), 0/175 galaxies and 0/2350 low-acceleration points lie beyond: **passes**.
- With 1/μ = 24.5 kpc (dust by equality), 45 galaxies and 357/2350 (15%) low-acceleration points lie beyond: **fails**.
- So the open door is pinned to μ ≈ 7.6–9 Mpc⁻¹, a ~20% band. Deciding question: must the condensate already be dust at z_eq (CMB peak heights), or is z_rec enough? (g_bar uses Υ=1 here; counting only.)

## CORRECTION — superseded under Cosh 𝒦 (TARGET_D5 §2), 2026-11-18
`small_q0_dust_check.py` and `sparc_mu_reach.py` used the quadratic 𝒦, which TARGET_D5 §1.3 already excludes **[D]**. Their μ floor (7.6–41 Mpc⁻¹), the 1/μ ≤ 25–133 kpc cut, the "~20% μ band" and the "dust by z_eq or z_rec?" question are artifacts of that model. **Withdrawn.** The scripts carry a SUPERSEDED banner; the sections above stay as history.

Re-run: `door_under_cosh.py` → `DOOR_UNDER_COSH.json` ([O]; regression reproduces SZ's published Cosh run, D5 §2.5, to 1%).
- Under Cosh, μ (curvature at 𝒬₀) and early-time w (width, r = 𝒵₀/𝒬₀) are independent (D5 §2.2). The background depends on (μ, r, K_B) only, so **Q₀ drops out**. Small Q₀ costs nothing cosmologically.
- **Cosmological floor:** μ ≥ 1.1×10⁻³ Mpc⁻¹ (a_* < 1 at r = 0.02); **μ ≥ 3.4×10⁻³ Mpc⁻¹** if the ρ̄a³ drift is held to SZ's own Planck-consistent 5.34%.
- **Galactic cap** (SZ's r_C ~ (r_M μ⁻²)^{1/3} ≥ R_max, all 175 SPARC galaxies, Υ_d = 0.5, Υ_b = 0.7, signed gas): **μ ≤ 3.6 Mpc⁻¹** (binding UGC 09133, R_max = 108 kpc); ≤ 1.27 Mpc⁻¹ with r_C ≥ 2R_max.
- **Window: μ ∈ [3.4×10⁻³, 3.6] Mpc⁻¹, three decades.** At Q₀ = 2×10⁻⁵ Mpc⁻¹ this means 𝒦₂ ≈ 2.7×10⁴ – 3.1×10¹⁰.
- **By-product, closes the D5 open item "r_C evaluated for real galaxies at SZ's (𝒬₀, 𝒦₂)":** SZ's own Cosh run (μ = 100 Mpc⁻¹, 1/μ = 10 kpc) puts r_C inside the last measured point of **144/175** SPARC galaxies. If the r_C estimate holds, SZ's CMB-fit parameters conflict with the galaxy sector, as D5 §2.5 suspected. [O], because r_C is SZ's order-of-magnitude estimate.

## CORRECTION — Theory 3 part (A)
(A) said the w = 1/3 tracker's amplitude is an initial condition. That holds for a decoupled field. It is **wrong** if the tracker is AeST's own condensate (𝒦 ~ (𝒬−𝒬₀)⁴ early, which is what "replace Q³ by Q⁴" means): 𝒦_𝒬 = I₀/a³ ties the amplitude to Ω_c. The correct kill (`theory3_condensate_tracker.py`, [O]): compensating BBN needs ρ_φ/ρ_r = a_t/a_eq ∈ [0.034, 0.143], i.e. the condensate stays radiation-like until z ≈ 4×10⁴–10⁵. In AeST the condensate is all the dark matter, so structure above k ≈ 0.08–0.2 Mpc⁻¹ is erased. Cold to k = 10 Mpc⁻¹ allows at most 7.3×10⁻⁴, **47× short**. Theory 3 stays UNSAT, for a stronger reason. The compensator in the open door must be a separate field.

## Quartic screening of galaxies (`door_quartic_sparc_fit.py` → `DOOR_QUARTIC_SPARC_FIT.json`) — [O]
Λ is fixed by the Sun's Vainshtein radius, so every galaxy gets r_V(M) = r_V☉(M/M☉)^{1/3}. This uses the same heuristic as VAINSHTEIN_PREQ: spherical enclosed mass, with the MOND part of the RAR suppressed by u, where u + (r_V/r)⁶u³ = 1. It is not a field solution. Each galaxy refits Υ (prior 0.1 dex).

| r_V☉ (pc) | total Δχ² (vs 38 242 unscreened) | galaxies Δχ² > 25 | worst |
|---|---|---|---|
| 1.09 | −1076 | 9 | UGC 09133 +191 |
| 1.2 | −1137 | 9 | UGC 09133 +259 |
| 1.4 | −886 | 9 | UGC 09133 +395 |
| 1.7 | +409 | 17 | UGC 09133 +623 |
| 2.0 | +2608 | 27 | UGC 09133 +866 |
| 2.36 | +6047 | 48 | UGC 09133 +1161 |

- The unscreened χ²/N is 11.3, so the quoted errors are ~3.4× too small for this model. Per-galaxy Δχ² should be read against that.
- Up to ~1.5 pc the total *improves*. That is most likely the screening absorbing inner-disk RAR/Υ mismatch, not evidence for screening. A handful of massive high-surface-brightness discs get worse: UGC 09133, NGC 6015, NGC 5055.
- Galaxies that improve are mostly bulge-dominated: 26 with Δχ² < −9 and 16 with Δχ² < −25 at 1.09 pc; the best is UGC 06787, at −411 (`IMPROVERS_1.088pc.txt`). That is consistent with the screening absorbing an inner Υ_b/RAR mismatch.
- Above ~1.6 pc SPARC turns against it. **The Cassini-allowed range [1.09, 2.36] pc shrinks to ≈ [1.09, 1.5] pc.** This tightens GW170817 to ε ≲ 0.13–0.22, i.e. **Q₀ ≲ 3×10⁻⁵ Mpc⁻¹**.

## Where the open door stands
Open, narrow, and resting on two links nobody has shown:
1. **The p-scaling is not a field solution** (VAINSHTEIN_PREQ's own caveat). The decider is the nested AeST + L₄ field equation for the Sun inside the Galaxy's field, or a no-go.
2. **The GW170817 / GW-decay analysis is borrowed.** Creminelli+ 2018 and the α_T formula are scalar–tensor EFT-of-DE results. AeST is vector–tensor–scalar with an aether background, and whether L₄ on φ keeps c_T = c and avoids decay there is not shown.

Also open: the BBN compensator is a separate field. It needs an exit mass in [1.9×10⁻²⁷, 2.2×10⁻¹⁶] eV and must dilute at least as fast as radiation after exit (kination, or w ≥ 1/3 oscillation); a dust-like exit overcloses. Strong coupling at 𝒦₂ up to 3×10¹⁰ is unchecked. No Boltzmann run decides 1 or 2, so none was set up (`classy` is not installed; no AeST Boltzmann code exists, see D5 §5).

## Nested field solution: the door closes (`door_nested_solution.py`, `door_nested_refine.py`) [O]
Live scalar law (AEST_TOTAL_SCALAR_CORRESPONDENCE: x μ_std(x) = y, λ_s < 11.28) plus a quartic Galileon on φ. K is the Galileon strength in m².

1. **Exact reduction [D].** Around the Sun the screened scalar gradient c is ~10⁻⁴ of the Galactic scalar gradient. The AQUAL term therefore linearises to A_e(δ + L êê), and the quartic Galileon is blind to the uniform part of the Galactic field. Stretching z′ = z/√(1+L) makes the whole operator isotropic; this is checked numerically to 2×10⁻¹⁵ at 40 random points (`part_a`). Inside r_V′ the exact solution is φ = c r′, with c = (GM σ a₀ₘ²/K)^{1/3}. VAINSHTEIN_PREQ's p = 2 scaling is the spherical limit of this.
2. **Why it leaks.** Around that cone the linearised quartic operator has only radial second derivatives, so it gives no angular stiffness. The external-field anisotropy imprinted near r_V′ survives inward as a constant-magnitude quadrupolar force of size ≈ (1 − 1/σ²)c.
3. **BBN corollary, independent of the Galileon.** It is [D] inside the corpus's own Einstein-aether map (TARGET_D3_ALPHA_WORKING: c₁ = −c₃ = K_B, c₂ = 0, c₄,eff = (2−K_B)/(1+λ_s), G_N = G/(1 − c₁₄/2)).
   - G_cosmo = G/(1 + (c₁+3c₂+c₃)/2) = G. This reproduces the repo's G_cosmo/G_N = λ_s(2−K_B)/[2(1+λ_s)] exactly.
   - If screening removes c₄,eff locally (an [O] physics assumption), then c₁₄ → K_B and **G_cosmo/G_local = 1 − K_B/2**. λ_s drops out of BBN, and the ratio is ≥ 0.95 for K_B ≤ 0.1. Any such screening removes the Wave-3 BBN tension and the separate compensator field.
   - The same map gives α₁ = −4c₁₄ → −4K_B on the static branch. |α₁| < 10⁻⁴ then needs K_B ≲ 2.5×10⁻⁵, unless the solar system sits on D3's dragged branch, where α₁ = α₂ = 0. Both point to small K_B.
4. **First pass** (λ_s ∈ {0.5, 1, 3, 11}, K = 10³⁷–10⁴³, Milky Way assumed unscreened at R☉; `DOOR_NESTED_SOLUTION.json`): Mercury + Cassini + SPARC Δχ² ≤ 0 (vs live μ_std, χ² 49 866) all pass for λ_s = 0.5 (K = 10³⁹–10⁴¹), λ_s = 1 (3×10³⁹–10⁴¹) and λ_s = 3 (3×10⁴¹). λ_s = 11 fails: L = 25.8 near the folding bound.
5. **Refinement** (`DOOR_NESTED_REFINE.json`). Those K also screen the Milky Way at R☉: the Galileon/AQUAL flux ratio there is 0.2–55. The Galaxy is re-solved with the Galileon, using McMillan-like baryons and spherical enclosed mass.
   - The Sun's problem stays elliptic (A_⊥ > 0). A flat-curve shortcut said otherwise; it was wrong and is not used.
   - But the Galaxy's Galileon cofactor stiffens the Sun's kinetic tensor along the GC direction: σ = 1.7–3.7 across the SPARC-accepted window.
   - **Cassini Q₂_eff = 1.2–5.8×10⁻²⁶ against ≤ 5.2×10⁻²⁷: a 2–11× failure at every point SPARC accepts.**
   - Q₂ passes only at K ≥ 10⁴², where SPARC Δχ² is +22k to +132k and the model's own g(R☉) = 1.24–1.42×10⁻¹⁰ falls below the observed 1.9×10⁻¹⁰.
   - λ_s = 0.2 (`DOOR_NESTED_SOLUTION_lam0.2.json`, `DOOR_NESTED_REFINE_lam0.2.json`): SPARC Δχ² ≥ +18k at every K, and the refined Cassini fails wherever g(R☉) is in the observed band.
6. **Verdict: CLOSED [O] for each single Galileon order.**
   - Cubic alone: p = 1.5 needs r_V ≳ 90 pc, which screens whole galaxies.
   - Quartic alone: this section.
   - Quintic: GW170817 and GW decay.
   - **Not covered: a mixed L₃ + L₄.** Linearised around the cone, a cubic term gives coefficients ∝ (c/r)(δ + nn), so it supplies the angular stiffness the quartic lacks. It is safe for c_T and GW decay. A mixture could keep the quartic dominant at Mercury (p = 2) while the cubic damps the angular leak. Open.
7. **Caveats.**
   - The Galaxy and galaxies use spherical enclosed mass. The disc geometry makes things **worse, not better**: at R☉ the scalar's vertical curvature, ≈ 4πGρ₀/A_e with ρ₀ = 0.1 M☉/pc³, is ~30× the in-plane curvature, and it enters the azimuthal cofactor with the sign of s′.
   - In all 4 rows that pass both SPARC and the Milky Way rotation band, s′ < 0. The Galileon's azimuthal coefficient is then −6 to −10 against A_e = 0.5–0.9, so the Sun's static problem is **not elliptic** there at all (estimate, `door_nested_refine.py` inputs).
   - The mixed term κ cof(H_sun):T is not solved. It reshapes the matching at r ~ r_V′ by O(T r_V′/c) ≈ 0.3, too small to remove a 2–11× overshoot, but it is not computed.
   - Saturn's Q₂ is a least-squares proxy for the ephemeris fit.
   - PPN α₁/α₂ with a screened scalar is not checked.
8. **What survives and where it points.**
   - (a) Any Vainshtein screening whose angular kinetic terms vanish cannot hide the external-field quadrupole. A viable screen must give the angular modes a mass or stiffness as well, as density-dependent (symmetron/chameleon-type) screening does.
   - (b) The BBN corollary.
   - (c) The D5 r_C item, evaluated with D5's quoted r_C ~ (r_M μ⁻²)^{1/3}. The literature-sweep note says SZ's exact scaling did not extract cleanly, so 144/175 is [O] and should not be attributed to the PRL as stated.
   - "Two-phase information tension that melts at high density" (the panel's Theory 1) is in field-theory terms a symmetron-type screen. The corpus already has a Cassini symmetron window (`05_lean_formalization/CassiniSymmetronWindow.lean`). That is one next route; mixed L₃ + L₄ is the other. (b) carries over to both.


## Mixed cubic + quartic (`PREREG_MIXED_L3L4.md`): closed [O]
1. **The pure quartic is unstable [D] (`quartic_core_instability.py`, SymPy series).** Inside the quartic-dominated core the angular principal coefficient is M_⊥ → −Z + 2κ₃²/(3κ₄).
   - With κ₃ = 0 it is −Z < 0, so the quartic-screened solar solution is gradient-unstable in the angular directions inside its Vainshtein region.
   - This kills the pure-quartic door independently of the Cassini result above, and more strongly.
   - My first hand derivation got the sign of the cubic term wrong; the SymPy series is the record.
2. **The Galaxy's tide is cancelled near the Sun [D, order-by-order].** The Sun's induced response is H₁ = −κ₃/(3κ₄) I − T, so inside r_T ~ c/|T| the Galaxy's Galileon cofactors drop out. The Z that enters is the external-field AQUAL tensor A_e(I + L êê), with an O(1) anisotropic correction: angular direction e₁ sees −Z_e₂e₂.
   - Stability condition: **K₃ > √(3 K₄ A_e(1+L))**.
   - The first scan implementation mixed perturbation orders and reported spurious failures. Its log is kept as `mixed_l3l4_INVALID_ellipticity.log`. The scan was stopped and replaced by the order-consistent criterion.
3. **The stabilising cubic survives SPARC [O] (`mixed_stability_sparc.py`).** In deep MOND the cubic/AQUAL flux ratio is K₃/(η r), independent of mass, so every galaxy's MOND scalar is suppressed inside r ~ K₃/η (2–22 kpc here).
   - At the stability threshold, 9 rows still pass Mercury, the Milky Way g(R☉) and SPARC Δχ² ≤ 0: λ_s = 0.5 with K₄ = 3×10³⁸–3×10⁴⁰, and λ_s = 1 with K₄ = 3×10³⁸–10⁴⁰.
4. **Cassini kills it [O] (`mixed_cassini_survivors.py`).** All 18 survivor configurations (1.0× and 1.5× the threshold K₃, both g_e) give **Q₂_eff = 2.1–8.5×10⁻²⁶**, 4–16× the 2σ upper bound of 5.2×10⁻²⁷.
   - Cause: the cubic couples to the disc's vertical tidal curvature through 2κ₃(tr T − T), whose anisotropy is ~2κ₃T_zz/A_e ≫ 1. The Sun's r_V (~1–2 pc) lies outside the vertical cancellation radius (~0.2 pc), so that anisotropy is imprinted where the leak amplitude is set.
   - Raising K₃ does not help: shell angular stiffness and Galactic anisotropy both scale with κ₃, while r_V grows and SPARC worsens.
   - The first-order solver overestimates by ≤ 21% (regression a), which cannot close a 4–16× gap.
   - Caveats: the solver holds the Galaxy's cofactors constant inside r_T, where they are cancelled; the leak is set near r_V, outside r_T. The required Milky Way baryon scale f_MW = 0.72–1.62 is partly implausible.
5. **Stop rule triggered.** No candidate passes, so mixed L₃ + L₄ is closed [O] at first order. Next route: symmetron-type (density-melting) screening. The BBN corollary (λ_s drops out once the solar-system scalar is screened) carries over.


## Symmetron / density-melting screening (`symmetron_route.py` → `SYMMETRON_ROUTE.json`): closed
A density screen must act where Cassini measures, which is the field at Saturn's orbit. There the density is interplanetary, not solar.
1. **Local density [D].** Saturn's orbit has ρ ≈ 1.3×10⁻²² kg m⁻³ (solar wind), **0.019×** the galactic midplane density at R☉ (6.8×10⁻²¹) that the screen must leave unscreened (repo bound S(ρ_disk) ≥ 0.99).
   - Any screen that never increases with density then has S(Saturn) ≥ 0.99, so Q₂ ≥ 1.89×10⁻²⁶: **+9.6σ** against Park 2026.
   - The Oort-cloud region (local ISM, 0.2–1.7×10⁻²¹) is no denser.
2. **Compton-length smoothing [D].** A compact body pins σ = 0 only inside itself. The maximal (thin-shell) exterior depletion is σ = σ₀(1 − R/r), and a finite range only reduces it. At Saturn |δσ/σ₀| ≤ R☉/r = 4.9×10⁻⁴ (1.2×10⁻² at Mercury), so the screen is open at the planets.
   - Screening the whole neighbourhood through the Milky Way's own environment would also screen the disc at R☉, which the Galaxy's rotation needs MONDian.
3. **Source gating [O].** Suppressing the Sun's scalar charge (thin shell) could pass Cassini, but it screens every star alike, since the Sun is a typical star. Galaxies' MOND source then reduces to gas.
   - SPARC with a gas-only MOND source: χ² 49 865 → 126 048 (**Δχ² = +76 183**), with 88 galaxies worse by more than 25.
4. **The corpus window is an artifact.** `screen_mass_cassini.py` and `CassiniSymmetronWindow.lean` evaluate the solar-system suppression at ρ☉ = 1.4×10³–1.5×10⁵ kg m⁻³, the Sun's interior, not at Saturn's orbit. The Lean algebra is fine; its physical premise should be marked [X] on main.

**Where this leaves the AeST MOND sector.** The single-order Galileons, mixed cubic + quartic, the symmetron/density screens and the corpus's earlier tidal screen (killed by the Oort cloud, 2026-10-16) all fail. No standard screening class rescues bare μ_std at Cassini without breaking SPARC, the Oort cloud or GW170817. The surviving lever is the **interpolating function itself, tested with honest SPARC systematics**. The 10-27 a₀-boundary sweep left ν₈,₀.₂₅ a near miss (Cassini edge 1.167 vs SPARC-preferred 1.175×10⁻¹⁰). Its SPARC side used the pre-fix pipeline (S0), which today's merged forward-model audit (#235) shows carries a ~10–15% systematic band.
