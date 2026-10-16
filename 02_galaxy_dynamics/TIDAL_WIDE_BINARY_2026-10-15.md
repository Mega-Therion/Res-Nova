# Tidal screening in wide binaries: the two-body computation and the R(s) kill test (2026-10-15)

**Verdict,  under the pre-registered  rule:** not excluded.
- T,  the  screened  model, passes the strict cut and fails the loose cut, as Newton does.
- The strict cut's power to tell T from Newton is Z_N = 3.0–3.5, below the pre-registered 4. Z_N is the expected separation if T were true, not a measured separation of the data from Newton.
- The frozen pipeline scales each velocity by √Γ at the orbit's current radius. For T's dip and peak this local-force step is off by up to 2% in orbit-mean speed (§5), comparable to the 10–20 kAU bin's error. T's χ² values are therefore approximate and descriptive only, and are not a pre-registered preference test.

**Tiers:**  `[D]` for the  field equation and  the  solver  (§1). `[E]` for §2–§5.

**Pre-registration:**  `PREREG_TIDAL_WIDE_BINARY_2026-10-15.md`, committed in  `b11edd3`, with amendment  A1  in  `2d095d3`. The prediction table was committed in `b3197e1`, before R(s) was run.

**Scripts:**
- `tidal_screening_two_body.py`:  gates, Cassini, table,  refinement and summary.
- `tidal_screening_wide_binary_rs.py`:  R(s).
- `tidal_screening_action_sparc.py`:  SPARC.
- `tidal_local_force_check.py`:  the local-force step (post-hoc, §5).

---

## 1. The Cassini and SPARC runs solved the wrong equation `[D]`
S(x)  depends on Φ_N's  Hessian, so varying  Φ_N  in  the action produces an extra term:

∇²Φ  = ∇·[ν_eff ∇Φ_N]  + ∂ᵢ∂ⱼWᵢⱼ, Wᵢⱼ  =  −(c²/2)  S′(x) P(y) Hᵢⱼ/‖H‖, P(y) = ∫₀^y 2t(ν − 1) dt.

The  runs of `639fa63`  solved only the  first  term,  the divergence form. Gate G0 derives the full equation symbolically from the 1D action, with residual 0.

| | Action form | Divergence form |
|---|---|---|
| Momentum, isolated binary, 0.5–8 kAU | conserved to 1.0×10⁻⁴ | imbalance of 0.07–0.94% |
| Lone star's free fall in the Galactic field, 0.1–3 M☉ | exact at every mass (0.0573 g_Ne in the shell-integrated convention) | 0.0060–0.0280 g_Ne, depending on mass |

Under  the divergence form,  stars of different  mass  would  fall differently, so it is not a consistent theory. The action form is the model.

## 2. Cassini under the action form `[E]`
The  calibration gives x*_A  = 7.04×10¹¹. That  is  4.0  times below the divergence-form value of 2.84×10¹², which the action form fails (Q₂ ≈ 12×10⁻²⁷ s⁻²).

| g_e (m/s²) | Q₂ (×10⁻²⁷ s⁻²) | divergence part | W part |
|---|---|---|---|
| 1.9×10⁻¹⁰ | 5.20 | 0.76 | 4.44 |
| 2.4×10⁻¹⁰ | 3.99 | 0.41 | 3.58 |

The  W term carries  most of the  quadrupole.  Every  grid x* ≤ 7.04×10¹¹ passes, and the passing set is contiguous. At the second resolution the result agrees to 2×10⁻⁸ relative.

## 3. SPARC at x*_A `[E]`
- **Divergence  part, 171 galaxies,  h_z = 0.1  kpc.**  The  total χ² goes from 18123.521 to 18123.521 (Δχ² = −0.0004), which passes K1. The largest change in g is 3.0×10⁻⁶, and the largest galaxy x is 1.9×10¹⁰, 37 times below x*_A.
- **W part.** This is estimated from the spherical identity, not a disk solve. It is at most 7.1×10⁻⁶ of g_N wherever g_N > 0.01 a₀, at most 7.2×10⁻⁶ of the observed g, and never above 1.7×10⁻¹⁴ m/s².

## 4. Two-body predictions `[D]`
Γ_r  is the radial  relative acceleration divided  by  GM/r²,  orientation-averaged, at q₁ = 0.5. The values come from `TIDAL_TWO_BODY_SUMMARY.json`, for the action form at x*_A on the A1 grid of 45 r points. Interpolation error at the refined midpoints is at most 0.0081.

| M (M☉) | g_e (10⁻¹⁰) | Dip: minimum, at r | Peak: maximum, at r | Γ_r < 0.99 over | Γ_r > 1.01 from |
|---|---|---|---|---|---|
| 0.45 | 1.9 | 0.846 at 7.2 kAU | 1.477 at 14.0 kAU | 3.1–9.0 kAU | 9.1 kAU |
| 0.8 | 1.9 | 0.901 at 8.0 | 1.343 at 17.5 | 4.0–10.6 | 10.9 |
| 1.4 | 1.9 | 0.934 at 10.0 | 1.258 at 19.6 | 5.3–12.6 | 13.0 |
| 2.5 | 1.9 | 0.960 at 11.2 | 1.200 at 24.5 | 7.0–14.6 | 15.5 |
| 0.8 | 2.4 | 0.865 at 8.9 | 1.389 at 17.5 | 3.8–10.9 | 11.2 |

How  this compares with  the other curves:
- **Far  field.**  Beyond  about 40 kAU the action form settles to ν_e(1 + L_e/3) = 1.088, the unscreened value.
- **Unscreened two-body curve (E₂, live a₀).** It passes 1.01 at 2.6–3.5 kAU and has no dip.
- **Divergence form.** It levels at 1.060 instead of 1.088, because a star's own screening hole breaks its free fall. At 400 kAU with the separation perpendicular to the field it gives 1.002, against an unscreened value of 1.047.

Where  the dip and  peak come from:  they  are  W's. W's source is a double divergence concentrated on the screening shell. For a single star, the shell's field is g_W,r = (2/√6) r⁻³ (r³ w̃)′. It pushes outward inside the shell's peak and pulls inward outside it. The feature's size is set by S′, so wide binaries measure the shape of the screening function, not only x*.

## 5. The R(s) kill test `[E]`
**Data.**
- El-Badry,  Rix & Heintz  2021, Zenodo 4435257,  md5  9644d53f056758fb2ab1d3d04a45e25d.
- The  extract reproduces `WIDE_BINARY_FINAL.json` exactly: n = 14,542 strict and 20,156 loose, with max |ΔR| = 0.0 and max |Δχ²| = 0.0.
- Every binary's total mass lies inside the table's 0.25–2.5 M☉ range. 2.1–2.4% have q₁ > 0.8 and were clamped to 0.8.

**C3,  with 40 injected  catalogues per model  per  cut.**  The table shows each χ² as raw / calibrated, followed by the null maximum.

| model | strict χ² | strict null max | loose χ² | loose null max | excluded |
|---|---|---|---|---|---|
| N (frozen) | 9.51 / 5.5 | 24.4 | 63.8 / 35.6 | 24.5 | no |
| T, g_e = 1.9 | 2.25 / 1.6 | 16.3 | 57.96 / 25.9 | 39.0 | no |
| T, g_e = 2.4 | 2.92 / 2.0 | 28.3 | 68.45 / 34.7 | 24.4 | no |
| E₂ (unscreened, live a₀), 1.9 / 2.4 | 9.18 / 6.3 · 9.71 / 6.0 | 20.5 · 21.5 | 17.30 / 10.7 · 32.06 / 18.5 | 19.6 · 24.4 | no |
| divergence form, 1.9 / 2.4 | 5.77 / 4.0 · 7.41 / 4.3 | 18.4 · 15.2 | 33.87 / 25.3 · 43.78 / 26.5 | 26.7 · 28.1 | no |

**Gate  1 (power).** Z_N  is the separation  from  Newton  (N) and Z_E₂ the separation from E₂, the unscreened two-body curve.

| | strict | loose |
|---|---|---|
| Z_N | 3.00 / 3.55 | 5.05 / 5.46 |
| Z_E₂ | 4.50 / 4.80 | 5.70 / 5.91 |

Z  is power: the  median, over T's  own  injected  catalogues, of √(χ²_X − χ²_T). The pre-registered "underpowered" label needs Z_N < 4 in both cuts, so it does not apply. But in the only cut T passes, Z_N is below 4.

**Strict  cut, R per  bin** (sky-projected separation;  the  model  columns are the combined curves at g_e = 1.9):

| bin (kAU) | data R | N | T | E₂ |
|---|---|---|---|---|
| 2–5 | 0.9924 ± 0.0075 | 1.000 | 0.993 | 1.008 |
| 5–10 | 1.0028 ± 0.0167 | 1.000 | 0.980 | 1.035 |
| 10–20 | 1.0640 ± 0.0231 | 1.002 | 1.051 | 1.046 |
| 20–30 | 1.095 ± 0.086 | 1.000 | 1.090 | 1.025 |

T  fails the loose  cut at 5–10  kAU,  where  the loose data sit at 1.067 ± 0.011 and T predicts 0.986. `WIDE_BINARY_FINAL_2026-10-04.md` traces that loose-cut excess to unresolved companions in heavy pairs; that tracing is `[O]`. In the divergence form, 488 and 295 Monte Carlo draws had Γ_r < 0 and were clipped to 0. No other form had any.

**The  local-force step** (`tidal_local_force_check.py`,  post-hoc). The test  builds  Φ(r)  from the orientation-averaged Γ_r at M = 1 M☉ and q₁ = 0.5. For 12 orbits with a = 6–25 kAU and e = 0.3–0.7, it compares the energy-integral speed with √Γ times the Kepler speed at the same radius. The pointwise difference reaches 10–13% for orbits that cross 7–20 kAU. The time-weighted orbit mean differs by −1.6% to +2.1%, against the 10–20 kAU bin's σ of 2.3%. Every model in the frozen pipeline uses this step, but it is least accurate for T.

## 6. What this settles and what it does not
- The  route survives its  kill test without  moving  x*.  That is a pass under RY's refined K2, not a confirmation. The strict cut's power against Newton for this model is Z = 3.0–3.5, short of the 4 the pre-registration asks for.
- A fair χ² comparison for T needs velocities from orbits integrated in its force law, not the local-force step. That is a change to the pipeline, so it needs its own pre-registration.
- The prediction to test next is the mass-dependent dip and peak (§4). The feature's position scales as M^{1/3}; MOND's onset scales as M^{1/2}. A stratified test should be pre-registered now and run on Gaia DR4.
- K3 also names the Oort cloud. The Sun's screening edge at x*_A falls at about 9,700 AU, inside the cloud, and W's inner push and outer pull straddle it. That test has not been run.
- Amendment A (orientation) was not touched. No sky orientation was used.
