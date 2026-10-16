# Pre-registration: tidal screening in wide binaries (2026-10-15)

**Frozen  before** the action-form  Cassini calibration, any  wide-binary  prediction  at that x*, and any R(s) number for the tidal model. The El-Badry catalogue was still downloading when this was committed; no wide-binary data file was open. Tier `[O]`, protocol. Amendment A of `PREREG_WIDE_BINARY_ORIENTATION_2026-10-08.md` is untouched, and no sky orientation is used anywhere.

## 1. Which equation is the model
`TIDAL_SCREENING_2026-10-15.md`  §2 states the  model by its  action:  quasistatic  QUMOND with S(x) multiplying the MOND part of the Lagrangian, and x built from Φ_N's Hessian. Varying Φ_N in that action gives

∇²Φ  = ∇·[ν_eff ∇Φ_N]  + ∂ᵢ∂ⱼWᵢⱼ, Wᵢⱼ  =  −(c²/2)  S′(x) P(y) Hᵢⱼ / ‖H‖, P(y) = Q(z) − z = ∫₀^y 2t(ν − 1) dt,

with  the normalisation P(0)  = 0, so  the  MOND  sector carries no energy where there is no field. The Cassini calibration (x* = 2.84×10¹²) and the SPARC run of `639fa63` solved the first term only, the **divergence form**. W is nonzero exactly where S′ is, so the two equations differ at the screening shell. That shell is where Cassini and wide binaries sit.

Solver  development measured the  following (`TIDAL_TWO_BODY_GATES.json`):
- **Action form.**  It  conserves  momentum: for an isolated binary, |m₁g₁ + m₂g₂| ≤ 1.0×10⁻⁴ of the total. A lone star falls with the external field for every mass from 0.1 to 3 M☉.
- **Divergence form.** It does neither. The momentum imbalance is 0.07–0.94% for an isolated binary at 0.5–8 kAU. A lone star's shell-integrated self-acceleration is 0.0060–0.0280 g_Ne over 0.1–3 M☉, where free fall gives 0.0573. Bodies of different mass therefore fall differently in the Galactic field.

**Decision  model: the action  form.** Its x*  is  calibrated  on Cassini (§2) before any wide-binary number at that x* is computed. The divergence form at x* = 2.84×10¹² is reported as a systematic, together with the two failures above.

**Disclosure.**  While the solver  was being built  and  converged,  a few two-body values were computed at x* = 2.84×10¹², for both forms. All used M = 1 M☉, q₁ = 0.7, g_e = 1.9×10⁻¹⁰ and cos θ_e = 0.6, at r = 1, 5, 10 and 100 kAU. None is at the action-form x*, and none was compared with data.

## 2. Cassini, action form
- The  rule is the  same as in  `639fa63`:  live  a₀ = 1.1607×10⁻¹⁰ m/s², and g_e ∈ {1.9, 2.4}×10⁻¹⁰ m/s².
- The bound is read two-sided, because W can change the sign of Q₂: Q₂ ∈ [−2.0, 5.2]×10⁻²⁷ s⁻², which is 1.6 ± 1.8 at 2σ.
- x*_A is the largest x* that passes at both g_e. It is found by scanning log₁₀ x* from 6.00 to 16.00 in steps of 0.05, then bisecting above the largest passing grid point.
- If no x* passes, the action form fails Cassini. §3 is then run for the divergence form only.
- Q₂ comes from direct kernel integration around the Sun. Its divergence part reproduces Milgrom's q(η) integrator to 6.6×10⁻⁵ (gate G9).

## 3. The two-body computation
- **Setup.**  Two point masses,  m₁ = q₁M  and  m₂  = (1 − q₁)M, at 3D separation r, in a uniform Newtonian field g_Ne with ν(g_Ne/a₀) g_Ne = g_e, at angle θ_e to the separation. The Galactic tide enters x as it does in the Cassini run.
- **Output.** Γ_r, the radial component of the relative acceleration divided by GM/r², and the tangential component Γ_t.
- **Table.** The grid is:
  - M ∈ {0.25, 0.45, 0.8, 1.4, 2.5} M☉;
  - 18 log-spaced r from 0.2 to 400 kAU;
  - q₁ ∈ {0.5, 0.65, 0.8};
  - cos θ_e at 4 Gauss–Legendre nodes;
  - g_e ∈ {1.9, 2.4}×10⁻¹⁰;
  - three forms: action at x*_A, divergence at 2.84×10¹², and unscreened (S ≡ 1, called E₂ below).
- **Gates.** `tidal_screening_two_body.py gates` runs G0–G11 and exits 0. G0 derives the field equation symbolically from the 1D action; its residual is 0. Five sabotaged copies exit 1, each tripping the gate aimed at it:
  - the W kernel's coefficient 15 → 14: G5, G6;
  - the F kernel's 3 → 2: G1, G2;
  - P′ halved: G2b, G6;
  - the sign of the lone-star term: G11;
  - the partition of unity dropped: G3, G4, G5.

  Each  star's acceleration is  computed in two  parts:  its  lone-star value, integrated on its own grid, plus the binary's sources minus that star's lone sources. G11 checks this split against direct integration.
- **Reported predictions.** The orientation-averaged Γ_r against r for each M, and the separations where Γ_r − 1 crosses ±1%.

## 4. The kill test: R(s) through the frozen pipeline
**Data.**
- El-Badry,  Rix & Heintz  2021: Zenodo 4435257,  file  `all_columns_catalog.fits.gz`,  md5 9644d53f056758fb2ab1d3d04a45e25d. It is extracted by `wide_binary_extract.py`.
- Before any number for T is computed, the extract must reproduce `WIDE_BINARY_FINAL.json`: its n per cut, and its data R(s) to 10⁻⁶. If it does not, the test stops there.

**Model  T.**
- T enters through  a new runner  built  around  `wide_binary_final.py`. The pinned files are not edited.
- ṽ is scaled by √Γ_r(M, r₃D, q₁, cos θ_e). θ_e is drawn isotropically at random for every Monte Carlo draw; it is never the sky orientation.
- q₁ is clamped to [0.5, 0.8], and M and r to the table's range. No `q_two_body` factor is applied.
- N, E₂ and the divergence form are run the same way.

**Criterion  C3, unchanged.** A  model is excluded  if,  in  both cuts, its calibrated χ² exceeds 18.5 and its raw χ² exceeds the null maximum. κ and the null maximum come from 40 injected catalogues of that model per cut.

**Verdict.**  If C3 excludes  T at both  g_e,  T  is excluded and the route is dead, because x* would have to move. Otherwise T is not excluded.

**Gate 1 (power), reported with the verdict.**
- Z_X is the median, over T's 40 injections, of √max(0, χ²_X − χ²_T).
- If Z_N < 4 in both cuts, the result is "underpowered against Newton at current N", not "survives".
- Z against E₂ is reported too.

**Fixed  settings.** Strata, bins  and NT/NM/NINJ are  as  in  `wide_binary_final.py`. New-model seeds are 2026101500 + index.

## 5. SPARC under the action form
- At  x*_A, SPARC is  refitted with S(x)  at  x*_A  (the divergence part, `fit_tidal`, h_z = 0.1 kpc). The K1 rule is unchanged.
- The W part is not solved for disks. At each SPARC point it is estimated from the spherical identity g_W,r = (2/√6) r⁻³ (r³ w̃)′ and reported as an estimate, not a fit.
