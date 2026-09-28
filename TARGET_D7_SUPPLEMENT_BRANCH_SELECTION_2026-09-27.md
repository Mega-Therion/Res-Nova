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
| **MW satellites (100–640 km/s, ≫ C·v_f ≈ 3–4 km/s)** | **Newtonian** | **✗: 37 of 42 dSphs would need stellar M/L > 10 even at σ − 1σ** |

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
