# Runge–Lenz precession under μ_std — 2026-10-06

**Question (RY):** compute the Runge–Lenz (apsidal) precession rate as a function of g_N/a0 under μ_std, and check it against the Cassini bound.

**Answer.** Two terms break the Kepler symmetry, and they act in different places.
- **Radial channel:** g = ν(y)g_N. This is the term behind flat rotation curves. It turns the Runge–Lenz vector by order one per orbit at y = g_N/a0 ≲ 1, and by only 2π/y² per radial period at y ≫ 1.
- **External-field quadrupole Q₂:** at Saturn this term is about **200×** larger than the radial channel.

So the solar-system test that μ_std fails and the galactic signal it fits come from **different channels**. Script: `runge_lenz_precession.py`. Numbers: `RUNGE_LENZ_PRECESSION.json`.

## 1. Radial channel [D]

For near-circular orbits, the apsidal angle is Ψ = π/√(1 − 2n), with n(y) = d ln ν/d ln y. The pericentre therefore moves by 2Ψ − 2π per radial period, at the rate Ω − κ = Ω(1 − √(1 − 2n)).

For ν₂ (the inverse of μ_std):

  n(y) = −2 / (y² s (1 + s)),  s = √(1 + 4/y²)

The limits are −1/y² for y ≫ 1 and −1/2 in deep MOND. The closed form matches a numerical log-derivative to 10⁻⁹ relative at y ≤ 1.

| y = g_N/a0 | μ_std: advance per radial period | μ_std: rate/Ω | μ_simple (= μ_dual, [X]) |
|---|---|---|---|
| ≪ 1 (deep MOND) | −1.8403 rad (−105.4°) | −0.4142 = 1 − √2 | same limit |
| 0.1 | −1.784 rad | −0.396 | −1.656 rad |
| 1 | −1.241 rad (−71.1°) | −0.246 | −1.241 rad |
| 10 | −6.01×10⁻² rad | −9.66×10⁻³ | −0.436 rad |
| 100 | −6.28×10⁻⁴ rad | −1.00×10⁻⁴ | −6.01×10⁻² rad |
| ≫ 1 | **−2π/y²** | −1/y² | **−2π/y** |

The sign is negative: the apsides regress, as in a logarithmic potential. The 1/y² versus 1/y tail is why μ_std passes the isolated-Sun test and μ_simple does not.

**Integration check.** Planar orbits were integrated in g = ν₂(1/r²)/r² (DOP853, rtol 10⁻¹²), measuring successive pericentres.
- At e ≈ 0.02 the measured advance matches the formula to 2×10⁻⁵ (deep MOND) up to 1.5×10⁻³ (y ≳ 10). That is the expected O(e²) correction for a rate that varies as r⁴.
- At e ≈ 0.5 the formula undershoots by 31%. It is a near-circular result.

## 2. External-field quadrupole channel [D]

The perturbation is δΦ = −(Q₂/2) xⁱxʲ(eᵢeⱼ − δᵢⱼ/3). Averaging the disturbing function over a Kepler ellipse, with the field at latitude β and in-plane angle φ from perihelion, gives

  dϖ/dt = Q₂√(1−e²)/(2n) · [cos²β (5cos²φ − 1) − 1]   (β = 0: Q₂√(1−e²)/(4n)·(1 + 5 cos 2φ))

**Integration check** (ε = Q₂/n² = 10⁻⁵, 300 orbits):
- **Stationary geometries** (φ = 0°, 90°; e = 0.05, 0.2; β = 40°): agreement to ≤ 5.4×10⁻⁴.
- **φ = 30°:** the offset grows linearly with run length (2.0×10⁻³, 6.8×10⁻³, 2.1×10⁻² at 30, 100, 300 orbits). That is the field-to-perihelion angle drifting during the run, so the formula is the instantaneous secular rate.

**Inputs:**
- Q₂ comes from canon's `efe_quadrupole_q2.Q2` (QUMOND; it reproduces the 16.7/17.2 of `CASSINI_EFE_QUADRUPOLE_2026-09-27.md`).
- The field direction is toward Sgr A*, which sits at ecliptic λ = 266.85°, β = −5.61°.
- Planetary elements are JPL J2000 approximate values.
- Planetary inclinations are neglected.

**Perihelion precession under μ_std, in mas per century:**

| | EFE, a0 = cH0/2π (g_e 1.9 / 2.4) | EFE, a0 = 1.1607e-10 SPARC (1.9 / 2.4) | EFE at the 2σ bound Q₂ = 5.2e-27 | radial channel (derived / SPARC a0) |
|---|---|---|---|---|
| Mercury | +0.018 / +0.019 | +0.021 / +0.022 | +0.0057 | −3.7×10⁻⁶ / −4.6×10⁻⁶ |
| Earth | +0.070 / +0.073 | +0.080 / +0.084 | +0.022 | −4.0×10⁻⁵ / −5.0×10⁻⁵ |
| **Saturn** | **+2.33 / +2.40** | **+2.66 / +2.80** | **+0.73** | **−0.011 / −0.014** |

- Q₂(μ_std) = 16.7 / 17.2 ×10⁻²⁷ s⁻² at the derived a0, and **19.0 / 20.0 ×10⁻²⁷ s⁻² at the SPARC a0**. The SPARC values are new here; canon's table used the derived a0.
- Saturn's perihelion lies 185.7° from the Galactic-centre direction, close to the geometric maximum of the quadrupole term (geometry factor 1.454 of a possible ≈ 1.48). This is why Saturn is the sensitive planet.
- μ_std's quadrupole precession at Saturn is **3.2–3.8×** the precession the 2σ bound allows. This is the same exclusion canon reports (+8.7σ), restated as a rate.

## 3. What this settles

1. **The thread's simple form is refuted** (`10_Projects/Audits/2026-10-06 Check - Central potentials…`, "Thread worth pulling"). The proposal was that one quantity, how much the Kepler symmetry is broken, describes both the solar-system bound and the galactic signal. It does not. In the solar system the measurable breaking is about 200× dominated by the anisotropic EFE term. The radial channel that makes rotation curves flat contributes −0.011 to −0.014 mas/cy at Saturn, 52–65× below even the bound-equivalent rate.
2. **What survives `[O]`:** both channels are perturbations of the same Kepler problem, but they break different symmetries.
   - The radial channel keeps angular momentum. It breaks only the hidden Runge–Lenz symmetry: for planar motion, the SO(3) acting on the energy shell V₂(ℝ³) breaks to the in-plane SO(2).
   - The EFE quadrupole also exerts a torque, x × F = Q₂(ê·x)(x × ê). Only L·ê survives.
3. **Practical consequence:** a fix for Cassini has to suppress the anisotropic EFE channel, through a sharper transition (canon's ν̂₄, ν₅…) or screening. Changing μ_std's isolated-field behaviour cannot help, because that residual is already far below the bound.
4. **Correction.** On 2026-10-06 Claude wrote that the Cassini constraint "is itself a precession measurement". That is wrong: the bound comes from fitting Cassini's Earth–Saturn range data (Hees et al. 2014; arXiv:2602.17884). The secular perihelion drift computed here is one projection of the perturbation those fits see. Whether a precession-only test could detect 2.3–2.8 mas/cy at Saturn has not been checked.

## Scope

- QUMOND Q₂. Per Hees 2016, AQUAL's Q₂ is slightly larger, so the AQUAL rates would be higher.
- AeST is not computed (canon's caveat carries over).
- Orbit-averaged, first order in Q₂. The radial formula is near-circular.
- Wide binaries (y ~ 1) sit in the Galactic field (η ≈ 1.6–2.3), so the isolated radial formula does not apply to them without the EFE.
