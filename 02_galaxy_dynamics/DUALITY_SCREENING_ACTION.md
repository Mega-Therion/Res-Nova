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

η  cannot  be replaced  by  |∇Φ| /  a₀.  That  gradient is  the Sun's or the galaxy's own field, and S would then kill the regime the boost is supposed to describe. A covariant completion has to keep the external piece as a background solution, or add a second field whose gradient is that piece. Neither is in this action.
