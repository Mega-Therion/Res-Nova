# LIGHT-CONE a₀ AUDIT — local physics, transport, inference (horizon-selection residue, observational side)

**Status:** COMPUTATION BUILT; no status change to obligation 3. This audit separates
what a high-z galaxy's inferred a₀ owes to (1) local physics at emission, (2) transport
of its light along our past light cone, (3) our inference today. It sharpens the a₀(z)
discriminant named in `HORIZON_SELECTION_AUDIT_2026-09-16.md` §5. It does **not** select a
horizon; that residue stays `[O]`.
**Date:** 2026-09-16
**Tags:** `[P]` proved · `[D]` derived/verified here · `[C]` cited · `[O]` open · `[X]` excluded
**Machine:** `scripts/light_cone_a0.py` — 7/7, exit 0. Sabotage-tested on copies inside the
repo (deleted before commit): adding a spurious (1+z) to the flux area → L1 fails; using
D_L¹ instead of D_L² for the BTFR mass → L2 and L3 fail; measuring R with D_L instead of
D_A → L3 fails; Planck Ω_m → 0.25 → L4 fails. (Flipping the sign of Λ in E(z) crashes the
script with a math-domain error, exit 1 — a failure, but not a clean check failure, so it
is not counted.)
**Inputs:** Planck 2018 base ΛCDM (arXiv:1807.06209, H₀ = 67.36, Ω_m = 0.3153, flat,
radiation as in `scripts/horizon_selection_audit.py`); T3 non-flow a₀ 95% interval
`02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json`; D5 background bound; D3 §8.3.

---

## 0. Posing the question on the light cone

There is no global "now". A galaxy observed at redshift z is an event on our past light
cone. "a₀ set by the horizon now vs then" has meaning only as: *which H, evaluated at which
event, in which time slicing.* The three readings from the horizon audit become three
functions a₀_local(z) at the emission event; transport maps the emitted signal to our
detectors; inference maps detector data back to a number through an assumed cosmology.

## 1. LOCAL — a₀ at the emission event `[D]` (given each reading, itself `[O]`)

**Background H(z).** The current D5 AeST 𝒦(𝒬) background is observationally ΛCDM-equivalent
at background level: `TARGET_D5_COSMOLOGICAL_SECTOR.md` §2.4 (lines 221–226): *"the
expansion history deviates from ΛCDM by |H/H_ΛCDM − 1| ≤ 3.6×10⁻³, monotonically decreasing
from a = 10⁻⁴ to exactly 0 today"* (+5×10⁻⁶ at a = 0.1). So H(z) = H₀E(z) with Planck 2018
ΛCDM; the 3.6×10⁻³ bound is 1.1% of the smallest separation below (z = 0.5; check L5) and
is carried as a systematic.

| z | Hubble/apparent (quasi-static) cH(z)/2π | de Sitter / Λ constant | Kodama–Hayward |
|---|---|---|---|
| 0.5 | 1.323 (1.378e-10) | 1.000 | 0.942 |
| 0.9 | 1.688 | 1.000 | 0.951 |
| 1.0 | 1.791 (1.866e-10) | 1.000 | 0.962 |
| 1.5 | 2.370 | 1.000 | 1.059 |
| 2.0 | 3.034 (3.160e-10) | 1.000 | 1.214 |
| 2.4 | 3.618 | 1.000 | 1.370 |

Ratios a₀(z)/a₀(0); absolute values use a₀(0) = cH₀/2π at H₀ = 67.36. The Kodama form is
the merged audit's E(z)(1−q(z))/(1−q₀) (L4 asserts the z = 1 values 1.791/0.962 match K7).
The Kodama form is already excluded at z ≈ 0 (horizon audit §2); it is listed for the shape.

**Foliation.** The Hubble reading needs a time slicing: H(z) is the expansion rate of the
comoving (CMB-rest) congruence at the emission event. The covariant action does single out
a frame kinematically: AeST carries a unit timelike vector A^μ (A^μA_μ = −1), and on FLRW
A_μ = (−N, 0, 0, 0) (`TARGET_D7_COVARIANT_COMPLETION.md` §1.1), i.e. the aether is at rest in
the cosmic frame. `[C]` (SZ action) + `[D]` (background alignment, as stated in D7). What is
**not** known is whether that preferred frame is observable locally: the PPN preferred-frame
parameters α₁, α₂ are `[O]` — `TARGET_D3_PPN_AND_SOLAR_SYSTEM.md` line 3 / §8.3: *"Foster–Jacobson's
α₁,α₂ formulas are inapplicable at AeST's couplings (c₁₂₃=0 Maxwell locus, spin-0 aether
speed zero)."* So: the frame exists in the action; its PPN consequences are uncomputed.
Galaxy peculiar velocities (~10⁻³c) change the local H by O(10⁻³), negligible here. `[D]`
The Λ reading needs no slicing (constant); the Kodama reading uses the same comoving slicing.

## 2. TRANSPORT — distances and reciprocity

**Etherington status `[C]`.** The current action is AeST with **minimal** matter coupling to
g_μν (D7 §1, verbatim from SZ arXiv:2007.00082: *"matter minimally coupled to g_μν — no
disformal metric anywhere in the theory"*; the disformal coupling was retired 2026-09-12).
In any metric theory where photons travel on null geodesics of one metric and photon number
is conserved, the reciprocity relation D_L = (1+z)² D_A holds exactly (Etherington 1933;
Ellis 1971/2007 — cited from standard use, not re-read here). **The theory's prediction is
η(z) ≡ D_L/((1+z)² D_A) = 1 at every z.** Any measured η ≠ 1 (beyond astrophysical opacity)
falsifies the current photon sector.

Implementation `[D]`: the script builds D_L from flux bookkeeping (energy redshift 1/(1+z),
arrival-rate dilation 1/(1+z), comoving sphere area 4πχ²) and D_A from proper size at
emission (a_e χ), as separate constructions; L1 asserts η = 1 to 1e-12. This is a check of
the bookkeeping, not an independent proof of reciprocity — the premise (metric, null
geodesics, number conservation) is the content, and it is `[C]`.

| z | D_A (Mpc) | D_L (Mpc) | (1+z)² | η |
|---|---|---|---|---|
| 0.5 | 1301.5 | 2928.4 | 2.25 | 1 |
| 1.0 | 1701.2 | 6804.7 | 4.00 | 1 |
| 2.0 | 1771.0 | 15939.0 | 9.00 | 1 |

D_A peaks at z = 1.59 (1795 Mpc; L6).

## 3. INFERENCE — what the observer gets `[D]`

Model: a deep-MOND galaxy with true a₀, baryonic mass M, and transition radius R_t
(G M/R_t² = a₀). Observables are distance-free: V_flat from redshift-corrected line widths,
bolometric flux F, angular radius θ_t. The observer converts with an assumed cosmology:
M = 4πF D_L,ass² (fixed, known mass-to-light), R = θ_t D_A,ass.

- **BTFR route:** a₀^B = V⁴/(G M) ∝ D_L⁻² — measured log-slope −2.000000 (L2).
- **Rotation-curve route:** a₀^R = V²/R ∝ D_A⁻¹ — measured log-slope −1.000000 (L2).

a₀_inferred / a₀_true, truth = Planck ΛCDM with Hubble-form a₀:

| z | assumed | BTFR | R | (a₀^R)²/a₀^B |
|---|---|---|---|---|
| 0.5 | H₀ = 73 | 1.1745 | 1.0837 | 1.000000 |
| 0.5 | Ω_m = 0.25 | 0.9549 | 0.9772 | 1.000000 |
| 1.0 | H₀ = 73 | 1.1744 | 1.0837 | 1.000000 |
| 1.0 | Ω_m = 0.25 | 0.9231 | 0.9608 | 1.000000 |
| 1.0 | Ω_m = 0.40 | 1.0958 | 1.0468 | 1.000000 |
| 2.0 | H₀ = 73 | 1.1744 | 1.0837 | 1.000000 |
| 2.0 | Ω_m = 0.25 | 0.8894 | 0.9431 | 1.000000 |
| 2.0 | H₀ = 73, Ω_m = 0.25 | 1.0445 | 1.0220 | 1.000000 |

**Reading.**
- An H₀ error is a z-independent offset (17% BTFR, 8% R): it cannot fake a trend *within*
  a high-z sample, but it does bias a₀(z)/a₀(0) whenever the z = 0 anchor (SPARC, local-ladder
  zero point, H₀ ≈ 73-like) and the high-z distances (Planck cosmology) sit on different
  zero points. That mismatch is ~17% for BTFR a₀ — half the z = 0.5 Hubble-vs-Λ separation.
- An Ω_m error is z-dependent: 5–11% trends by z = 2 in the BTFR route — an apparent a₀(z)
  evolution produced entirely by inference.
- **The combination exists.** Because the routes carry different distance powers (D_L² vs
  D_A) and reciprocity ties D_L to D_A with a known (1+z)², the ratio
  (a₀^R)²/a₀^B = G M/R_t² = (1+z)⁴ · 4πG F/θ_t² is **distance-free** — the baryonic
  surface-density acceleration at the transition radius, built from flux and angle only.
  It cancels **both** scale (H₀) and shape (Ω_m) errors of the assumed cosmology, bin by bin
  (L3: max deviation 6e-16), because at fixed z both D_L,ass and D_A,ass come from the same
  comoving distance. This corrects a first-pass expectation (in review) that only the scale
  would cancel; the computation says shape cancels too, given η = 1 on both sides.
- **What it does not cancel.** (i) The true photon sector: with η_true = (1+z)^0.1 the
  combination is off by −12.9% at z = 1 (L3) — so the combination is exactly where transport
  shows up; a local-evolution signal would move all three columns identically in the
  distance-free one. (ii) Mass-to-light (Υ) and its evolution: g_bar ∝ Υ, so the
  combination trades distance systematics for stellar-population/gas-mass systematics —
  for high-z disks these are large (Genzel et al. 2017 name IMF and gas-mass calibration).
  (iii) The observational definition of θ_t: if the transition is located by comparing
  g_obs (∝ 1/D) with g_bar, the distance re-enters through the location; a distance-free
  criterion (e.g. the radius where the baryonic surface density reaches a fixed value in
  flux/angle units) is needed. `[O]`

So yes: BTFR-vs-R distance dependence separates transport from local evolution, at the
price of an absolute Υ calibration and a distance-free transition criterion. `[D]` for the
algebra; `[O]` for practical realisability.

## 4. DISCRIMINANT — Hubble form vs Λ constant, 3σ `[D]`

Separation = E(z) − 1 (in units of a₀(0)); a 3σ call needs σ_tot ≤ separation/3.
Systematic budget per route (1σ, fractional): z = 0 anchor σ = 0.078 (T3 95% half-width /
1.96); zero-point mismatch |exponent|·ln(73/67.36) (BTFR 0.161, R 0.080, combination 0);
Planck σ(Ω_m) = 0.0073 through D_A(z) (≤ 0.003); D5 background 3.6e-3.

| z | separation | σ_tot allowed | BTFR sys → stat needed | R sys → stat needed | combination sys → stat needed |
|---|---|---|---|---|---|
| 0.5 | 0.323 | 0.108 | 0.179 → **impossible** | 0.112 → **impossible** | 0.079 → 0.073 |
| 1.0 | 0.791 | 0.264 | 0.179 → 0.194 | 0.112 → 0.239 | 0.079 → 0.252 |
| 2.0 | 2.034 | 0.678 | 0.179 → 0.654 | 0.113 → 0.669 | 0.079 → 0.673 |

(Υ systematics excluded — they dominate at high z and are not modeled; these are the
distance-inference floors only.) At z = 0.5 no distance-based route can make the call
without re-anchoring the z = 0 sample onto the high-z zero point; at z ≥ 1 per-bin a₀ at
~20–25% already suffices on the distance side. The local anchor itself (7.8%) is the floor
of the combination route.

**Literature (arXiv IDs resolved, titles matched on arxiv.org/abs 2026-09-16):**
- Genzel et al. 2017, arXiv:1703.04310, *"Strongly baryon-dominated disk galaxies at the peak
  of galaxy formation ten billion years ago"* (Nature): six galaxies z ≈ 0.9–2.4, outer rotation
  curves decline with radius. `[C]`
- Übler et al. 2017, arXiv:1703.04321, *"The evolution of the Tully-Fisher relation between
  z~2.3 and z~0.9 with KMOS^3D"*: negative baryonic TFR zero-point evolution z = 0 → 0.9,
  positive from 0.9 → 2.3 (non-monotonic). `[C]`
- Milgrom 2017, arXiv:1703.06110, *"High-redshift rotation curves and MOND"*: the Genzel data
  "all but exclude a value of the MOND constant of ~4a₀ at z~2, excluding, e.g.,
  a₀ ∝ (1+z)^{3/2}". `[C]`
- Tiley et al. 2019, arXiv:1811.05982, *"The Shapes of the Rotation Curves of Star-forming
  Galaxies Over the Last ≈10 Gyr"*: ~1500 galaxies z ≈ 0.6–2.2; stacked curves are
  approximately flat or rising to 6R_d, and the decline depends on the normalisation
  prescription. **Contests** the falling-curve reading. `[C]`
- Nestor Shachar et al. 2023, arXiv:2209.12199, *"RC100 …"*: 100 galaxies z = 0.6–2.5; median
  f_DM(R_e) = 0.38 (z~1), 0.27 (z~2). `[C]`
- Genzel et al. 2020, arXiv:2006.03046 (RC41, cored DM) — title verified; not used for a number.

**Do existing data already constrain the Hubble-form 1.79×?** Not decisively. `[C]`+`[O]`
- The only explicit a₀(z) statement found (Milgrom 2017) excludes ~4a₀ at z ~ 2. The Hubble
  form gives 3.03 at z = 2 and 3.62 at z = 2.4 — below that bar but approaching it at the top
  of the Genzel range. The (1+z)^{3/2} exclusion (5.2× at z = 2) does not transfer to E(z).
- The rotation-curve shape at z ~ 1–2 is itself contested (Genzel 2017 / RC100 vs Tiley 2019),
  and none of these papers fits a₀ with μ_std, fixed distances, and a stated Υ prior.
- The corpus's own a₀(z) test (`03_observer_jwst/PREREG_A0_OF_Z_V3.md`) is inconclusive
  (0.87σ) and its dataset is flagged as lacking a provenance script (PEER_REVIEW_READINESS O4).
- The Übler BTFR zero-point evolution is in the BTFR route, which (§3) carries the 17% zero-
  point and Ω_m systematics and an Υ/gas-mass calibration; it is not converted to a₀(z) here.
Net: current data bear on a₀(z) at z ~ 2 at the factor-~4 level; they do not yet separate
1.79× (z = 1) from 1.00×. **What would:** a per-bin a₀ at z ≈ 1 with ≲ 25% total error,
using the distance-free combination or a common distance zero point, with Υ and gas mass
priors stated.

## 5. Stale-doc defects (dated notes added; physics prose not rewritten)

Live docs that still put this theory's photons on a disformal metric, contradicting D7 §1
(minimal coupling) and therefore the η = 1 prediction:

| file | line | defect | action |
|---|---|---|---|
| `FIRST_PRINCIPLES_PHYSICS_MONOGRAPH.md` | 68 (§2.3); also 12, 21 | "Photons and gravitational waves propagate on the disformal metric" | dated STALE note inserted above §2.3 |
| `THEORY_CONSISTENCY_AUDIT.md` | 47–54 (§3) | "effective disformal optical metric" + d_L^eff = d_L√(1−χ/χ_crit) — an η ≠ 1 modulator | dated STALE note inserted above §3 |

Not defects: `GROUNDED_BRICKS_VS_HYPOTHESIS_MAP.md:14` and `TOE_VISUAL_GEOMETRODYNAMICS_MASTER.md:73`
cite Bekenstein 1993 as literature provenance for the concept; `RESULT_CHI_EM_COUPLING.md:60`
already states luminality forces the disformal factor to vanish. `EPISTEMIC_BOUNDARY_v1.5.0.md:25`
names a Lean theorem `disformal_gamma_ppn_unity` — a naming leftover; not audited here. `[O]`

## 6. What could not be verified

- Etherington 1933 and Ellis's reciprocity papers: no arXiv IDs; cited from standard use.
- arXiv full-text search was unreachable (API returned empty/000); a published a₀(z) or BTFR-
  evolution constraint beyond Milgrom 2017 may exist and was not found by this search —
  absence is a fact about this search, not about the literature.
- Only abstracts were read for the five high-z papers; no numbers beyond the abstracts are used.
- The 73 vs 67.36 zero-point mismatch is a bracket, not a measured correction (as in the
  horizon audit §1).
- Υ/gas-mass systematics of high-z disks are not modeled.

## 7. Reproduce

```bash
python3 scripts/light_cone_a0.py   # 7/7, exit 0
```

## 8. Ledger

Obligation 3 residue: unchanged **[O]**. Added: the light-cone separation (local / transport
/ inference), η = 1 as a named falsifier of the minimal-coupling photon sector, the distance-
free combination (a₀^R)²/a₀^B, and per-route precision floors. No `[P]` changes.
