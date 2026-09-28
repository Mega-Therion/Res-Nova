# TARGET D7 SUPPLEMENT: branch selection, and the drag dilemma (2026-09-27)

**Status:** the central open problem of D7, stated sharply. **Tags:** `[D]` derived · `[C]` cited ·
`[E]` empirical · `[O]` open.

## 1. Two branches, both exact

AeST supports two kinds of solution around the same matter.

**Held (MOND).** The aether is at rest in the source frame, the scalar gradient has a component orthogonal
to it (𝒴 ≠ 0), and the MOND channel is on. This is the branch of the static quasistatic solutions
(Verwayen, Skordis & Bœhm 2024).

**Stealth / dragged (GR).** A_μ = −∂_μφ/𝒬₀ with |∇φ| = 𝒬₀. The aether is the free-fall congruence (the
"river"), J·∇φ = 𝒴 = 0, F = 0, and the metric is exactly GR.
- Verified: all field-equation residuals vanish on Painlevé–Gullstrand Schwarzschild
  (`exploration/d3_alpha/dragged_branch_exact_check.py`).
- Exact-GR AeST solutions are prior art: Skordis & Vokrouhlický 2024 `[C]`.
- A moving source's linear dragged branch completes to this sector (D3 note 7 §34).

A static mass admits both branches, and so does a moving one. **Which branch a system occupies is not
fixed by the field equations.**

## 2. A selection rule from AeST's own dynamics `[D]`, argued not proved

**(a) Shell crossing ends the stealth branch.** The stealth branch needs a single-valued clock field: the
free-fall congruence must not cross itself.
- In linear cosmology the aether co-moves with matter (D3 §32).
- In a collapsing, virializing region, that free-fall congruence focuses and crosses at the same epoch cold
  matter would (the same geodesics).
- A single-valued aether cannot follow the crossing, so **virialized systems at rest in their own aether
  cannot be stealth**.
- Assumption `[O]`: the held (MOND) branch is what replaces stealth. This is not proved.

**(b) A fast wind strips the hold.** Take a system moving through an ambient held aether.
- The MOND field holds the aether only if v_rel < C·v_f, with C = 0.19–0.27 for dSph backgrounds and
  0.45–0.60 for disks. This is linear theory (§26), and its validity condition v² ≫ |Ψ| holds for dwarfs.
- If in addition v_rel ≫ v_esc, the free-fall flow past it stays laminar, with caustics only far
  downstream.
- Such a system sits on the dragged branch, which is GR/Newtonian.

**The rule.** Virialized systems at rest in their aether are held (MOND). Systems moving through an ambient
held aether faster than C·v_f are dragged (Newtonian).

## 3. Confrontation with data

| system | rule predicts | data |
|---|---|---|
| Solar system (moving at ~240 km/s through the MW aether, ≫ C·v_f ≈ 0.1 km/s) | GR | ✅ Cassini, LLR |
| Wide binaries (same speed, ≫ threshold) | Newtonian | ✅ Banik+2024 (Newtonian strongly preferred); ✗ Chae 2023 (1.4× boost). Contested `[C]` |
| Isolated / field galaxies (co-moving with the large-scale aether, D3 §32) | MOND | ✅ SPARC |
| Fast cluster members (~1000 km/s ≫ C·v_f ~ 100 km/s) | outer rotation curves fall toward Keplerian | mixed: Whitmore+1988 yes, Dale+2001 no `[C]` |
| **MW satellites (100–640 km/s, ≫ C·v_f ≈ 3–4 km/s)** | **Newtonian (Ĝ, weaker than G_N)** | **✗ on the discriminating set:** Crater II, Carina, Leo II and Sculptor, where MOND+EFE fits and Newton fails, would need M/L ≈ 19 / 10 / 10 / 6 at σ − 1σ. The "37/42 need M/L > 10" count includes ultra-faints where MOND+EFE also fails 5–10×, so those do not discriminate |

The satellite numbers come from `02_galaxy_dynamics/branch_rule_satellites.py`, with output in
`BRANCH_RULE_SATELLITES.txt`.
- The LVDB dSphs, excluding the LMC and SMC, need M/L > 3 in 41 of 42 cases, M/L > 5 in 40 of 42, and
  M/L > 10 in 37 of 42, all evaluated at σ − 1σ.
- These are the classical, equilibrium dwarfs, not just ultra-faints: Draco needs M/L ≈ 39, Ursa Minor
  ≈ 43, Sextans ≈ 56, Carina ≈ 10 and Crater II ≈ 19. Old stellar populations have M/L_V ≈ 1–3. Tidal heating
  cannot supply a factor of ~20 in Draco.

## 4. The drag dilemma `[D]`

AeST is squeezed from both sides by one mechanism.
- **The solar system needs the zero mode (drag).** Lifting it with c₂(∇·A)² gives α₁ = −4c₁₄,eff, with
  |α₁| ≥ 4K_B, against LLR's 10⁻⁴ (D3 §29).
- **The same drag strips moving satellites of MOND**, contradicting 37 of 42 dSphs (§3).

The Sun and a dwarf differ only in how strongly they hold the aether, and the dwarf, deep in MOND, holds it
more weakly. So no single threshold spares the dwarfs while dragging the Sun.

**Escape routes, ranked by how much they would preserve:**
1. **Non-linear hysteresis `[O]`.** A dwarf that formed isolated (held) may keep its held aether bubble after
   falling into the Milky Way. The linear criterion says it cannot, but the held branch's non-linear
   stability against a wind has not been computed. **This is the decisive calculation:** an axisymmetric,
   time-dependent solution for a deep-MOND dwarf in an aether wind of 100–600 km/s.
   *(Update, §7: the perturbative version is closed. At satellite speeds the wind forces a correction as large as
   the dwarf's MOND field. Only a genuinely non-linear held branch remains.)*
2. **A completion whose MOND does not depend on the aether's rest frame.** This goes outside AeST. It must
   still put the phantom potential in the metric gravitational waves ride (GW170817 Shapiro, D3 note 7
   §28). No candidate is known.
3. Satellites out of equilibrium. Ruled out for the classical dSphs by the factor of ~20.

## 5. What this means for the paper

- **The phenomenological law survives the dwarf test.** μ_std with duality screening S(η) gives a dwarf
  penalty of 1.1 (`DWARF_SCREENING_TEST_2026-09-27.md`).
- **AeST, the candidate covariant completion, does not, unless escape route 1 holds.** The paper must keep
  the two separate: the empirical law with its tests on one side, and AeST's branch dynamics and the drag
  dilemma as the leading open problem of the completion on the other.

## References

- Verwayen, Skordis & Bœhm 2024, MNRAS 531, 272 (arXiv:2304.05134).
- Skordis & Vokrouhlický 2024, arXiv:2412.15395 (JCAP 03 (2025) 035).
- Banik et al. 2024, MNRAS 527, 4573 (arXiv:2311.03436).
- Chae 2023, ApJ 952 (doi:10.3847/1538-4357/ace101).
- Whitmore, Forbes & Rubin 1988, ApJ 333, 542.
- Dale et al. 2001, AJ (arXiv:astro-ph/0012388).
- Pace 2025, LVDB.

## 6. Stage 1 of the dwarf-in-a-wind calculation: full linear response `[D]`

Files: `exploration/d3_alpha/aest_mond_bg_source.py` (builder with a moving source) and `dwarf_wind_response.py`,
with output in `DWARF_WIND_RESPONSE.txt`.

**Setup.**
- The full constrained linear AeST system (metric in de Donder gauge, aether, scalar) at the galaxy-consistent
  point, on a local deep-MOND dSph background: x = 0.05, with J′ and 2𝒴J″ from μ_std.
- The MOND-field lift of the zero mode is represented at its §26 strength, q̄ = ∇²ϕ/(𝒦₂𝒬₀), with
  ∇²ϕ = v_f²/r², v_f = 10 km/s, r = 0.3 kpc and k = 1/r.
- A source moves through it at speed v. The MOND-channel response is S_z = ik φ̃ + Q̄(u_z + h₀z), which is
  nonzero when held and zero when dragged.

| v [km/s] | 0.3 | 1 | 3 | 5 | 10 | 30 | 100 | 300 | 1000 |
|---|---|---|---|---|---|---|---|---|---|
| \|S_z\|/\|S_z(0)\|, k ∥ ∇ϕ | 0.999 | 0.992 | 0.932 | 0.833 | 0.565 | 0.166 | 0.042 | 0.014 | 0.004 |
| \|S_z\|/\|S_z(0)\|, k ⊥ ∇ϕ | 0.999 | 0.992 | 0.935 | 0.839 | 0.577 | 0.172 | 0.044 | 0.014 | 0.004 |

**Reading.**
- The MOND channel begins to fail near C·v_f (2–3 km/s), halves near v_f, and falls as ≈ 4 km/s / v above
  that.
- **At satellite speeds of 100–600 km/s it keeps only 1–4% of its static value.** Satellites are dragged.
- The h₀₀ response rises about 2× from the static value toward large v in this proxy. That is attributed to
  the condensate response of the 𝒬-offset stand-in and is not interpreted.

**Why hysteresis cannot rescue it `[D]`, argued.** The dwarf's own non-linear MOND background is already in
the calculation through J′ and J″. What is left is non-linear in the aether amplitude, whose size is
v/c ≈ 10⁻³. Corrections that small cannot undo a suppression of 25–140×.
- A c₂ lift does not help either. It sets a scale-independent hold speed ~√(c₂/T_c): large c₂ would hold the
  Sun too and break LLR (α₁ = −4c₁₄,eff, independent of c₂), and small c₂ does not hold satellites.

**Status: a Stage-1 INDICATION, not a verdict (relabelled the same evening after review).** Stage 1 is not
decisive, for three reasons:
1. **It solved a different problem.** It computed a small extra source moving through a static held MOND
   background. The real problem has the dwarf itself as the source, sitting in the ambient Milky Way aether
   wind.
2. **Its v → 0 reference is not validated.** The proxy's static h₀₀ is weaker than GR (h₀₀ rises ~2.2× toward
   large v), which is not what a MOND state looks like. The same artefact may be inside S_z.
3. **A linear response around one branch cannot exclude a second, non-linear steady branch.** The static
   stealth branch (D3 §34) is exactly such a branch, and linear theory could not see it. The v/c argument
   covers only the aether's amplitude; the held-to-dragged switch changes S at O(1), inside J(𝒴).

**The decisive check `[O]`.** Build the boosted-held configuration in the dwarf frame: the deep-MOND static
field plus an ambient aether streaming at v, with φ = γ𝒬₀(t − v·x) + ϕ. Confirm the held ansatz has zero
residuals at v = 0, then measure how every Euler–Lagrange residual scales with v.
- Rough estimate: δ𝒬 ≈ −v·∇ϕ, so the condensate cost relative to the MOND term is ~𝒦₂v²/x. At 200 km/s and
  x = 0.05 that is ≈ 7×10⁻⁴ at 𝒦₂ = 75, which would let held survive, and ≈ 7 at 𝒦₂ = 7.5×10⁵, which would
  strip it.
- **The outcome may therefore depend on the parameter point.** That links to D5's tension between the
  CMB-fit and galaxy-consistent values of 𝒦₂.
  *(Update, §7: it does not, below the scalar sound speed. The controlling residual carries no 𝒦₂.)*

**The phenomenological law is unaffected either way.**

## 7. The decisive check, linear stage: the correction the wind forces on the dwarf's own field `[D]`

Files, all in `exploration/d3_alpha/`:
- `boosted_held_residuals.py` computes the residuals;
- `aest_wind_bg.py` builds the linear operator with a background aether wind, and `wind_bg_validate.py` validates it;
- `wind_correction_solve.py` solves for the correction;
- `wind_correction_{decompose,ksens,qsens}.py` run the row decomposition and the sensitivity tests.

All output is in `BOOSTED_HELD_WIND_CORRECTION.txt`.

**Setup.** Work in the dwarf frame.
- The configuration is the dwarf's own static deep-MOND field, with the ambient aether streaming through it at v.
- The clock is φ = γ𝒬₀(t + vz) + ϕ.
- The evaluation point P sits at r = 0.3 kpc, where x = 0.05.

Every Euler–Lagrange residual is evaluated at P and mapped into the operator's field basis: the aether rows, the scalar row, and, new here, the metric rows. The correction solves M(k, 0; v)·δX = −R at k = 1/r, where R is the residual minus its v = 0 value.

**Two defects of the first pass (`boosted_held_check.py`) are fixed.**
1. **It froze the metric, so it had no gravity rows.** The aether residual also feeds the h₀z row, since δA_z = δu^z + γh₀z − vγh_zz. The aether's λ-stress also carries a momentum density ~ vK_B∇²Φ.
2. **It dropped the fY″ terms.** Because 𝒴 ~ ε², fY″ ~ ε⁻², so those terms are not higher order. Its "static truncation artefact" in the scalar residual was exactly this missing term. With it restored, the static residual is ∝ fY′ − 2𝒴fY″ = (2−K_B)(𝒥′ − 2𝒴𝒥″), which vanishes in deep MOND. At x = 0.05 it is 0.25% of fY′.

**Checks.**
- All background-order residuals vanish, including the gravity rows: the condensate at its minimum carries zero stress.
- At v = 0 the operator reduces symbolically to the validated §26 operator.
- It is boost covariant: det M(k,ω;v)/det M(k′,ω′;0) = 1 − v² at every tested point, in exact rational arithmetic.
- At ω = 0 it is well conditioned, with condition number ≤ 6×10⁷ at 80 digits, and it has no null direction.
- The along-wind aether residual reproduces the first pass term for term.

**Result.** Both measures below are gauge invariant. The first is the fractional change of the MOND field strength, δ𝒴/2𝒴. The second is the rotation of its direction, (δS_⊥ − g·h_xz)/|S|.

| v [km/s] | 1 | 3 | 10 | 30 | 100 | 300 | 600 |
|---|---|---|---|---|---|---|---|
| wind ∥ field, δ\|S\|/\|S\|, 𝒦₂ = 75 | 0.10 | 0.30 | 0.74 | 0.99 | 1.04 | 1.05 | 1.05 |
| wind ⊥ field, rotation [rad], 𝒦₂ = 75 | 0.09 | 0.26 | 0.65 | 0.90 | 0.95 | 0.95 | 0.95 |
| wind ∥ field, 𝒦₂ = 7.5×10⁵ | 0.10 | 0.30 | 0.73 | 1.00 | 1.10 | 1.70 | 89 |
| wind ⊥ field, 𝒦₂ = 7.5×10⁵ | 0.09 | 0.26 | 0.65 | 0.90 | 0.94 | 0.93 | 3.6 |

- **From ~30 km/s up, the correction is as large as the MOND field itself, in both geometries.**
- **One residual drives it: the along-wind aether equation.** It reads v(12K_BĤ + (16K_B−4)H) with the wind along the field and v(−6K_BĤ + 4H) across it. This is the wind acting on the curvature of the dwarf's field.
  - The other rows contribute < 10⁻⁵ at 𝒦₂ = 75.
  - At 7.5×10⁵ the scalar row's 𝒦₂-advection term is 10⁴× larger as a residual, but it adds only 0.03 at 100 km/s.
- **The change is in the scalar, not the aether.** The aether tilt stays at 0.1–3% of the stealth tilt g/𝒬₀. What cannot persist is the MOND gradient; the aether is not dragged.

**The plateau is structural.** At high v the forcing, ∝ v·H ~ v·g/r, can be balanced only by the scalar gradient that the wind carries.
- The balancing coefficient is 2(2 + K_Bλ)·v·k, the same combination as §26's threshold. This is fitted at K_B = 1/2; its K_B-dependence was not computed.
- Both sides scale with v, so the plateau is v-independent:
  - wind along the field: δ|S|/|S| = (4 + 6𝒥′)/[(4 + λ_∥)kr] = 1.0488;
  - wind across the field: (4 − 3𝒥′)/[(4 + 𝒥′)kr] = 0.9507.
  Both match the numerics to 4 digits.
- It does not depend on the lift stand-in. Scaling q̄ by 0.1–10 moves only the crossover speed, ≈ 10 km/s × √(q̄/q̄₂₆).
- Below the scalar sound speed it does not depend on 𝒦₂. At 𝒦₂ = 7.5×10⁵, c_s ≈ 670 km/s, and the approach to that resonance amplifies the correction at 300–600 km/s.
- Its WKB normalization scales as 1/(kr): 0.35–3.1 for kr from 3 down to 1/3. It is never small.

**Escape by parameter choice: rejected `[X]`.** With the wind along the field, the deep-MOND forcing is ∝ (4K_B − 1), which vanishes at K_B = 1/4. With the wind across the field it is 4H·v, independent of K_B. Every satellite presents both geometries, so no value of K_B removes the forcing.

**Reading `[D]`: an indication, not a verdict.** Perturbation theory about the held state fails near v ~ 10 km/s. At satellite speeds, 100–600 km/s, the wind forces a correction as large as the dwarf's MOND field, in both geometries.
- This survives the WKB normalization (a factor of 3 either way), the lift stand-in (0.1–10×), 𝒦₂, and the point-to-mode phase. The phase variants are identical in 3 of 4 runs and agree within 1% in the fourth.
- It corroborates Stage 1 in the correct geometry, with the dwarf's own field as the background, so §6 objection 1 is removed.
- It is still linear and local (WKB at kr ~ 1). §6 objection 3 stands: a non-perturbative steady held branch is not excluded.
- There is no nearby steady held state at satellite speeds, so the perturbative form of §4 escape route 1 is closed.
- The §6 estimate "held survives when 𝒦₂v²/x ≪ 1" was not the controlling term. The forcing that matters carries no 𝒦₂.

**Related prior art `[C]`.** Peloso & Sorbo 2004 (PLB 593, 25): in a ghost condensate, a moving source loses its static modification of gravity. The AeST-specific content here is which quantity is lost, the MOND gradient, and the mechanism: the wind's force on the aether from the field curvature. None of the AeST papers checked treats moving sources: the abstracts of Verwayen–Skordis–Bœhm, Mistele, Bataki–Skordis–Złośnik and Reyes–Sakstein. A full literature search has not been made.

**Status.** D7 stays [P/O]. Two escapes from the drag dilemma remain:
- inside AeST, a genuinely non-linear steady held branch, for which nothing here gives evidence;
- escape route 2, a completion outside AeST.

The phenomenological law is unaffected.
