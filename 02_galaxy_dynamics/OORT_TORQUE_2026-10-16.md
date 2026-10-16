# The tidal screen and the Oort cloud: it fails the Oort peak (2026-10-16)

**Verdict  under the pre-registered  rule** (`PREREG_OORT_TORQUE_2026-10-16.md`, `8902da9`;  gate  amendment  A1, `d3501b0`): **fails like VNT**, at both g_e. The result rests on two findings, with a caveat on the benchmark.

**1.  Binding offset `[D]`.**  Comets falling in  from  rest  at infinity reach perihelion with an osculating Newtonian 1/a = +1.23×10⁻⁴ au⁻¹ (g_e = 1.9×10⁻¹⁰) or +1.61×10⁻⁴ au⁻¹ (g_e = 2.32×10⁻¹⁰). Bound comets show more. Bound comets would therefore all show original a ≤ 8,100 au. The observed Oort peak lies at original a = 10⁴–10⁵ au (VNT §4), so the model leaves it empty. This follows from energy conservation alone, not from the torque approximation, and three independent computations agree (§2).

**2.  Torques `[E]`, proxy.**  Torques reach the  inner  cloud  almost as deeply as unscreened MOND's: the jump semimajor axis a_J is 3.7–4.3 kAU, against 2.6 kAU unscreened and 26.9 kAU for Newton.

**Caveat  on the benchmark.**  The proxy does  not  reproduce  VNT's failure of the sharp μ₁₀ at g_e = 3.35×10⁻¹⁰ (their S3): it gives S3 the same a_J as Newton. The pre-registered "a_J ≤ a_J(S3)" test therefore reduces to "a_J ≤ a_J(Newton)". The failure does not depend on that test. It rests on the comparison with unscreened MOND, whose failure both VNT's simulations and this proxy reproduce, and on the binding offset.

---

## 1. Torques (`OORT_TORQUE_PROXY.json`)
Setup:  first-order ΔL per  orbit for q  =  10  au orbits, 400 isotropic orientations, McMillan 2017 Galactic tide. a_J is the smallest a where the median |ΔL| clears the Jupiter–Saturn barrier, L(15 au) − L(5 au).

| configuration | a_J (kAU) | binding offset Δ(1/a) (au⁻¹) |
|---|---|---|
| Newton (tide only) | 26.9 | 0 |
| unscreened ν_std, live a₀, g_e = 1.9 / 2.32 | 2.63 / 2.63 | −4.89 / −3.55 ×10⁻⁵ |
| unscreened ν_std, VNT S1 (a₀ = 1.2×10⁻¹⁰, g_e = 2.32) | 2.63 | −3.81×10⁻⁵ |
| μ₁₀, VNT S3 (a₀ = 1.2×10⁻¹⁰, g_e = 3.35) | 26.9 | +9×10⁻⁸ |
| **action form, x*_A = 7.04×10¹¹, g_e = 1.9 / 2.32** | **3.67 / 4.33** | **+1.23 / +1.61 ×10⁻⁴** |

- **Validation.**  Newton's a_J falls  inside the pre-registered  15–40  kAU.  Unscreened S1 gives 2.63 kAU, under the pre-registered 5 kAU, matching VNT's new comets down to a ~ 10³ au.
- **Gates.** O1 7.6×10⁻⁸; O2 0.19% (the field's quadrupole against `cassini_Q2`); O3 3.4×10⁻⁴; O4 1.6×10⁻⁵.
- **Shape of the torque.** At a = 5–20 kAU, the action form's median |ΔL_MOND| is 6–26 ΔL_crit, against 5–23 for unscreened MOND and 0.004–0.4 for the tide.

## 2. The binding offset, and a repulsive shell `[D]`
- **What  it measures.** The  offset is 2Φ_anom(0)/GM,  with  Φ_anom(0)  = ∫₀^∞ dg_r dr. A comet with true energy E arrives at perihelion with 1/a_osc = −2E/GM + 2Φ_anom(0)/GM.
- **Three computations.**

  | computation | g_e = 1.9 (au⁻¹) | g_e = 2.32 (au⁻¹) | agreement |
  |---|---|---|---|
  | (a) the map's line integral along each of 12 directions | +1.23×10⁻⁴ | +1.61×10⁻⁴ | directions agree to 0.1%, so the field is curl-free |
  | (b) the potential of the phantom sources at the Sun, from a direct volume integral: F part −1.9×10⁻⁵, W part +1.42×10⁻⁴ | +1.227×10⁻⁴ | +1.610×10⁻⁴ | — |
  | (c) analytically, W part only: 2Φ_W(0)/GM = (√6π/6) c² P(y_e)/(x* GM) | +1.39×10⁻⁴ | +1.71×10⁻⁴ | (b)'s W part to 2% and 1% |
- **Why  it is positive.**  The W push  lies  inside  the shell, which raises the potential there. The orientation-averaged ⟨dg_r⟩/g_N reaches +0.97 at 8.7 kAU, +1.27 at 10 kAU and +0.99 at 11.5 kAU. Between about 8.7 and 11.5 kAU the net radial gravity on a test body points outward.
- **Why the binaries were milder.** For the equal-mass binaries of the wide-binary table, each star's own Hessian reshapes the shell. Their dip was 5–15%.
- **Scaling.** The offset scales as 1/x*. Cassini allows only x* ≤ 7.04×10¹¹, so the smallest offset S2 can reach is the one above, 6–8 times what the Oort peak tolerates.
- **Other shapes.** For S_m = 1/(1 + (x/x*)^m), the factor ∫|S′| dx/x = (π/m)/sin(π/m) lies between π/2 (m = 2) and 1. The shape can lower the offset by at most 1.57× at fixed x*.

## 3. What would change it `[O]`
- **The  additive constant.** The  screened action contains  a  constant  the unscreened theory does not see: the zero of the MOND Lagrangian under S. Writing Qs = z + S(x)(Q(z) − z − C), the pre-registration fixed C = 0, meaning no MOND energy where there is no field.
- **What C does.** For a point mass in a uniform external field, x and the normalised Hessian are spherically symmetric, so the C part of W is isotropic. It leaves Cassini's Q₂ unchanged. The binding offset scales as P̄ − C.
- **What the data would demand.** The Oort peak would need C ≈ P(y_e,⊙) = 0.75–0.93, to within about 15%.
- **The cost.** That would be a fourth constant, and one tuned to the solar neighbourhood's external field. It is a new model: it needs its own pre-registration, and the wide-binary prediction redone, since the isotropic push-pull sets the dip and the peak.
- **Other routes.** A different coupling of S to the action is another route. None is tested here.

## 4. Scope
- This  is a proxy.  VNT's full simulation  of  comet  populations against the binding-energy data is the test.
- The binding-offset argument does not need that simulation. It needs only a static potential, energy conservation, and the observed Oort peak.
- Grok's earlier Δ(1/a) values (BLK-400, 2.7×10⁻⁵ at 10 kAU) came from the equal-mass binary table, a different system. Comets are test particles, where the push is about 10 times stronger.
