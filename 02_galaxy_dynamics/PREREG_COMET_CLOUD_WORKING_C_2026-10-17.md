# Pre-registration: comet cloud at the working screen

Filed before the map in this note is integrated. The constant is the Oort-window centre already solved, C = 0.579124707982253. a₀ = 1.1607×10⁻¹⁰ m s⁻² and x* = 7.035884281332817×10¹¹ stay frozen. g_e = 1.9×10⁻¹⁰ m s⁻². This is not a new screen and not a retune.

## Equation

Same heliocentric anomaly as `oort_torque_proxy.py` for `action|live|1.9`: dg = g_ph(x) − g_ph(Sun), source F + V with V = div W, through `tidal_screening_two_body.fields`. The only change is `c_zero` in that call. A comet that falls from rest at infinity along a ray has osculating

1/a = 2 Φ_ray(0) / GM, Φ_ray(0) = ∫₀^∞ dg_r dr

along that ray, with the same radial map, Legendre nodes, and tail as `binding_offset`. The orientation average of that integral is the published offset. At C = 0 it is 1.2309721532420575×10⁻⁴ au⁻¹ in `OORT_TORQUE_PROXY.json`.

## Gate

Recompute C = 0 on this code path first. Abort with no working-C verdict unless that offset agrees with 1.2309721532420575×10⁻⁴ au⁻¹ to a relative error below 10⁻³.

## Population

Isotropic weight is the Gauss–Legendre weight of the ray's μ = cos θ. Original a = 1 / (1/a) when 1/a > 0. A non-positive 1/a is unbound on that ray and counts as outside the window.

## Bar

The Oort window is original a ∈ [10⁴, 10⁵] au.

- Preserved iff the weighted median of a lies inside that window and at least half the weight lies inside it.
- Emptied iff the weighted median is below 10⁴ au.
- Otherwise inconclusive.

The torque jump a_J is written and does not decide. This is not VNT's catalog likelihood. A full injection against the observed binding-energy histogram is not this test.
