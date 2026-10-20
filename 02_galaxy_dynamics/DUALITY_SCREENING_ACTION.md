# Duality screening in the quasistatic action

**Tier:**  `[D]`  for the  quasistatic  action and  its  field  equation. `[O]`  for a covariant local scalar that would replace η. Not a Cassini proof beyond the multiplication already in `dwarf_screening_form2.py`.

On  one  patch the  external  acceleration is  a  constant  background, η  = |∇Φ_ext| / a₀. The factor is the constant

S(η) = 1 / (1 + η²).

The  Newtonian  potential on  that  patch obeys  ∇²Φ_N  =  4πGρ. The  physical potential is the stationary point of

S[Φ]  =  ∫ d³x  {  −ρ Φ  +  (1  / 8πG)  [ 2 ∇Φ · U − |U|² ] },

U = ν_eff ∇Φ_N,

ν_eff(y)  =  1 +  S(η)  (ν(y) −  1),  y  = |∇Φ_N|  / a₀.

Varying  Φ  gives ∇  ·  U =  4πGρ.  Where  U is  parallel to ∇Φ_N this is g = ν_eff g_N. The Newtonian piece is untouched. Only the MOND boost (ν − 1) is multiplied by S.

If  Q'(z)  = ν(√z)  −  1, the  same  equation  comes from  replacing Q by S(η) Q. S factors out because it does not depend on Φ or Φ_N inside the patch.

For  the  Sun, η  =  g_MW /  a₀  ≈  1.7–2.2, so  S ≈ 0.17–0.25. The bare μ_std quadrupole 17.2×10⁻²⁷ s⁻² becomes S times that. Against the 2026 bound (1.6 ± 1.8)×10⁻²⁷ the tension falls from (17.2 − 1.6) / 1.8 = +8.7σ to about +0.8σ to +1.5σ. That arithmetic is the whole of the screening. It is the same multiplication `dwarf_screening_form2.py` already runs.

η  cannot  be replaced  by  |∇Φ| /  a₀.  That  gradient is  the Sun's or the galaxy's own field, and S would then kill the regime the boost is supposed to describe. The covariant version that survives is a split of one potential: Φ_ext is the long-wavelength solution, held fixed while the patch potential varies. η = |∇Φ_ext| / a₀.

A  second  propagating scalar  that  enters through  the  disformal map is ruled out by `TensorSpeed.lean`. There `c_T = 1` when `c₁₃ = 0`, and the photon speed on `g̃ = e^{-2φ} g - 2 sinh(2φ) u u` gives the ratio `e^{-2φ}`. That ratio equals 1 if and only if `φ = 0`. A nonzero disformal scalar makes gravitational waves and light travel at different speeds. GW170817 closes that branch. Screening has to stay on the background split, where `φ = 0` and S is constant on the patch.

The  split  that  was  checked is  Φ  =  Φ_ext + ψ. Φ_ext is not varied. On the patch it is linear, so η = |∇Φ_ext| / a₀ does not depend on ψ and S is constant. The patch action is ∫ |∇ψ − ν_eff ∇Φ_N|² / 8πG. Its Euler-Lagrange equation is ∇²ψ = ∇ · (ν_eff ∇Φ_N). For a spherical Newtonian patch, ν_eff ∇Φ_N is a pure gradient, so the solution is ∇ψ = ν_eff ∇Φ_N, which is g = ν_eff g_N. The disformal scalar is not a variable of this action, so it stays at 0. `duality_screening_action_check.py` prints `RESULT background_split_ok` for that identity.

Off  the  sphere the  algebraic  step  stops. curl(ν_eff ∇Φ_N) = ∇ν_eff × ∇Φ_N. For Φ_N = x y that cross product is not zero, so no ψ has ∇ψ = ν_eff ∇Φ_N. A constant S multiplies the curl and does not remove it. S = 0 does remove it, because the boost is gone and the field is Newtonian. The equation that remains for any shape is ∇²ψ = ∇ · (ν_eff ∇Φ_N). The check prints `RESULT algebraic_g_fails_off_sphere` and `RESULT divergence_equation_remains`.
