# Pre-registration: ν₆ through the Oort binding test (2026-10-16)

**Frozen before any ν₆ Oort number.** Work order: The Block, BLK-403 (Muse). Track 1's interpolating function, not a new screen. No retune of a₀, and no new constant.

## Frozen parameters

- a₀ = 1.1607×10⁻¹⁰ m s⁻².
- ν₆(y) = (½ (1 + √(1 + 4 y⁻⁶)))^(1/6), the function in `wide_binary_fish_functions.py`.
- One Sun, 1 M☉. Galactic field g_e ∈ {1.9, 2.32}×10⁻¹⁰ m s⁻².
- No screening function and no x*. The source is the unscreened QUMOND phantom F = (ν₆ − 1) ∇Φ_N.

## What is computed

The same map and binding integral as `oort_torque_proxy.py`: radii 0.05–300 kAU (34 values), 12 Gauss–Legendre nodes in cos θ, dg = g_ph(x) − g_ph(Sun), and

Δ(1/a) = 2 Φ_anom(0) / GM, Φ_anom(0) = ∫₀^∞ ⟨dg_r⟩ dr.

Script: `nu6_oort_binding.py`. It calls that proxy's field kernel with ν swapped to ν₆. It does not refit anything.

## Decision, applied per g_e, before the number exists

- **Empties the peak** if Δ(1/a) ≥ 10⁻⁴ au⁻¹. Every bound comet would then show an original semimajor axis ≤ 10⁴ au, so the observed Oort window 10⁴–10⁵ au is empty on this energy argument. Tier of the number `[D]`. The model fails this test. Stop. Do not add a constant to save it.
- **Preserves the peak in this proxy** if |Δ(1/a)| ≤ 10⁻⁵ au⁻¹. That is the Newton-like bar already in `PREREG_OORT_TORQUE_2026-10-16.md`. It is not a pass of VNT's full simulation.
- **Shifts** if 10⁻⁵ < |Δ(1/a)| < 10⁻⁴ au⁻¹. Report the edge a = 1/Δ(1/a). Inconclusive against the peak. Not a kill and not a preservation.

Also record whether net radial gravity, g_N + ⟨dg_r⟩, points outward at any map radius. That fact does not change the three-way rule above.

The torque jump a_J is a later stage. It is not part of this decision. Wide binaries are not part of this decision.
