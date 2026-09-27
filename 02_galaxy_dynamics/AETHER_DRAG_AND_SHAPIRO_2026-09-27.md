# Aether drag and the GW170817 Shapiro test (2026-09-27)

Two questions: (1) does AeST's aether drag show up in the data? (2) could light travel slightly slower
than gravitational waves, and does the mass lying along a given direction matter?
Tags: `[P]` proved · `[D]` derived · `[E]` empirical · `[C]` cited · `[O]` open · `[X]` killed.
The theory side is in `TARGET_D3_ALPHA_WORKING_2026-09-27.md`, working note 7.

---

## 1. Dwarf speed test for gradual drag `[E]`

Script: `dwarf_velocity_drag_test.py`. Output: `DWARF_VELOCITY_DRAG_TEST.json` and `.txt`.

**Prediction tested.** Suppose drag weakens the MOND boost gradually with speed through the aether. Then,
at fixed Galactocentric distance, faster satellites should look more Newtonian. That would show up as a
negative correlation between speed and log(σ_obs/σ_Newton), and likewise with log(σ_obs/σ_MOND+EFE).

**Data.** 42 LVDB Milky Way satellites (Pace 2025, CC0) with σ, proper motions and v_los. The LMC, SMC
and Sagittarius are excluded. The σ predictions come from `dwarf_screening_test.py` (stars only, M/L = 2,
derived a0).
- Velocities are Galactocentric, using astropy defaults (R0 = 8.122 kpc; solar motion (12.9, 245.6, 7.78) km/s).
- CMB frame: the Planck 2018 dipole, 369.82 km/s toward (l, b) = (264.021°, 48.253°). The Milky Way
  therefore moves at **560 km/s toward (265.5°, 28.6°)** relative to the CMB `[D]` (computed here).
- Speeds: 103–642 km/s in the Milky Way frame and 375–1000 km/s in the CMB frame. Distances run
  26–372 kpc.

**Result.** Spearman correlations. The clean column controls for both distance and luminosity (rank
partial correlation).

| residual | speed frame | raw ρ (p) | distance-controlled ρ (p) | distance + L controlled ρ (p) |
|---|---|---|---|---|
| log obs/Newton | MW | +0.35 (0.03) | +0.21 (0.19) | **−0.11 (0.47)** |
| log obs/MOND+EFE | MW | +0.45 (0.00) | +0.17 (0.29) | **−0.08 (0.61)** |
| log obs/Newton | CMB | +0.35 (0.02) | +0.17 (0.27) | **+0.05 (0.74)** |
| log obs/MOND+EFE | CMB | +0.44 (0.00) | +0.18 (0.25) | **+0.11 (0.48)** |

The raw positive correlations come from distance and luminosity, not from speed. Using v/v_f instead of
v gives large raw correlations (+0.65 to +0.76), but that is by construction: log v_f carries L/4 and
log σ_N carries L/2. After luminosity is controlled for, it reduces to the speed test (|ρ| ≤ 0.11).

**Reading.**
- **No gradual-drag signal.** At fixed distance and luminosity, a satellite's speed does not predict its
  mass discrepancy in either frame.
- **This test cannot see linear-theory drag.** Linear theory predicts a switch, not a gradient. The
  held-branch threshold is v_rel < C·v_f, with C = 0.19–0.27 for dSph backgrounds (D3 note 7, §26).
  Every satellite sits 18–716× above that threshold in the Milky Way frame and 94–1,647× above it in the
  CMB frame.
- **The discriminating test is still the level test** of D3 note 6 §24. If the satellites are dragged
  (Newtonian), Crater II, Carina, Leo II and Sculptor need stellar M/L of 8–25.

**Caveats.**
- Proper-motion, distance and v_los errors are not propagated. For scale, 0.1 mas/yr at 180 kpc is
  85 km/s.
- Pisces II's 642 km/s is probably error-driven.
- 42 objects.

## 2. The GW170817 Shapiro test of photon-only lensing `[D]`+`[C]`

Script: `shapiro_gw170817_mond.py`. Output: `SHAPIRO_GW170817_MOND.txt`.

**The effect `[C]`.** Light passing through a gravitational potential is delayed: the Shapiro delay,
Δt = (1+γ)/c³ ∫|Φ| dl. The delay depends on direction, because it counts the mass along each line of sight.

**The Milky Way's phantom halo on this sightline `[D]`, estimate.** NGC 4993 lies 61° from the
Sun-to-Galactic-Centre direction. The MOND phantom potential of the Milky Way alone adds **94–254 days** of
delay on the path to it. The range covers M_b = 5–7×10¹⁰ M☉ and g_e = 0.01–0.03 a0.
- Model: point mass, μ_std (QUMOND ν_std), and the external field in the 1D collinear approximation.
- For comparison, Boran et al. estimate ≈400 days for the dark component along this sightline, using a
  dark-matter-halo model.

**The measurement `[C]`.** GRB 170817A arrived 1.74 ± 0.05 s after GW170817. Combined with the
emission-lag window, this gives **−2.6×10⁻⁷ ≤ γ_GW − γ_EM ≤ 1.2×10⁻⁶** (LVC, Fermi GBM and INTEGRAL 2017).

**Consequence `[D]`, scoped.** Consider any theory in which photons ride a metric that carries phantom
potential the gravitational-wave propagation metric does not. In such a theory, the photon-only share
must be ≲10⁻⁶–10⁻⁷ of the phantom potential on this sightline. This is Boran et al.'s exclusion of
"dark matter emulators", applied to our options:

- **Photon-only (disformal) lensing: excluded as the source of MOND lensing, whatever happens to
  cosmological freeze-out.**
  - This covers B1's g̃ = g + (2/a0²)∂χ∂χ and any variant of it.
  - Freeze-out sets the cosmological χ̇ ≈ 0. The halo delay comes from ∇χ, which freeze-out leaves alone.
  - **Withdrawn (same day):** the suggestion that a V(χ) = (χ − θ)² freeze-out could rescue disformal
    lensing (Path A).
- **Conformal scalar routes: pass GW170817 but give no extra lensing.** This includes k-mouflage and the
  symmetron.
  - They pass because null cones, and so Shapiro delays, are conformally invariant.
  - They fail lensing because a conformal factor bends no light (Bekenstein & Sanders 1994). Weak lensing
    nonetheless shows the low-acceleration excess around isolated galaxies: the KiDS-1000 lensing RAR
    extends two decades below the dynamical data (Brouwer et al. 2021).
  - Such routes therefore need a separate lensing mechanism.
- **Metric-level routes (AeST class): pass.** In these, the phantom potential sources the metric that
  both photons and gravitational waves ride, with c_T = c. This is the class that carries the aether and
  its zero-mode drag.

**Sharpened trilemma.** MOND lensing plus GW170817 (both the speed and the Shapiro delay) together imply
that the phantom potential lives in the metric gravitational waves ride.

## 3. Frames and directions, for reference `[C]`/`[D]`

- **Our motion `[D]`.** The Milky Way moves at 560 km/s relative to the CMB, toward (265.5°, 28.6°). That is
  44° from the Great Attractor at (307°, +9°), the position given by Lynden-Bell et al. 1988. The Great
  Attractor alone does not set our direction.
- **The CMB dipole is the "ahead versus behind" signal.** The CMB is Doppler-shifted, warmer ahead and
  cooler behind, by v/c ≈ 1.2×10⁻³. Light speed is the same in both directions: in AeST, light rides the
  ordinary metric, and the aether's preferred frame acts only through gravity. The gravitational version,
  a headwind along this axis, is the α₁/α₂ question of `TARGET_D3`.
- **Geometric distances from our own motion.** Our motion through the CMB covers a 78 AU/yr baseline. That
  gives nearby galaxies a secular parallax of 78 μas/yr at 1 Mpc (Paine et al. 2020).

**Leads `[O]` (not results).**
- **Line-of-sight convergence.** Time-delay H0 corrects for the line-of-sight convergence κ_ext, estimated
  from weighted galaxy counts along each sightline (Greene et al. 2013; Rusu et al. 2017). That estimate is
  calibrated on ΛCDM ray tracing. In a MOND or AeST universe the phantom halos reach out to the
  external-field radius, so the convergence per galaxy differs. The size of that systematic has not been
  quantified.
- **Cosmic dipole anomaly.** The quasar number-count dipole points along the CMB dipole but is about twice
  the kinematic expectation. Secrest et al. 2021 reported 4.9σ; the Bashir, Chingangbam & Appleby
  reassessment (2025/26) gives ≈3.4–3.6σ. Whether faster deep-MOND structure growth changes the
  clustering dipole is open.

## Reproduce

```
cd 02_galaxy_dynamics
python3 dwarf_velocity_drag_test.py      # needs astropy; LVDB csv in dwarf_data/
python3 shapiro_gw170817_mond.py
```

## References

- Boran, Desai, Kahya & Woodard 2018, PRD 97, 041501, "GW170817 falsifies dark matter emulators",
  arXiv:1710.06168.
- LIGO/Virgo, Fermi GBM & INTEGRAL 2017, ApJL 848, L13, arXiv:1710.05834.
- Bekenstein & Sanders 1994, ApJ 429, 480, arXiv:astro-ph/9311062.
- Brouwer et al. 2021, A&A 650, A113, arXiv:2106.11677.
- Lynden-Bell et al. 1988, ApJ (Great Attractor at (307°, +9°, cz ≈ 4350 km/s)).
- Planck 2018 I (CMB dipole).
- Paine, Darling et al. 2020, ApJ, "Secular Extragalactic Parallax: Measurement Methods and Predictions for Gaia", doi:10.3847/1538-4357/ab6f00.
- Greene et al. 2013; Rusu et al. 2017, MNRAS 467, 4220 (H0LiCOW III), arXiv:1607.01047.
- Secrest et al. 2021, ApJL 908, L51; Bashir, Chingangbam & Appleby, arXiv:2511.00822.
- Pace 2025, LVDB (CC0).
