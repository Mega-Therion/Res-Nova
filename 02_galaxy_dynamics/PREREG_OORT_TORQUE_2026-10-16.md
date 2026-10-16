# Pre-registration: the Oort-cloud torque proxy for the tidal screen (2026-10-16)

**Frozen  before any MOND  or screened torque  number.**  The  only computation run first was a tide-only check of the machinery: with the Newtonian Galactic tide alone, the median |ΔL| per orbit crosses ΔL_crit between a = 20 and 30 kAU. Tier `[O]`, protocol.

## Why
Vokrouhlický, Nesvorný & Tremaine 2024 (arXiv:2403.09555, "VNT") simulate comets in AQUAL MOND over the Sun's lifetime. The simulations include the Galactic tide and passing stars.
- **The finding.** MOND fails the long-period-comet data. Torques at r ≳ r_M (VNT Figs. 5 and 6) make new comets with a ~ 10³–10⁴ au, so the Oort peak is under-represented.
- **How far it reaches.** The failure holds even for the sharp μ₁₀ at g_e = 3.35×10⁻¹⁰ m/s². That is their S3, with normalised χ² 3.6 against Newton's 1.5.
- **What it leaves open.** Their abstract does not rule out MOND theories "in which non-Newtonian effects are screened on small spatial scales". The tidal screen is one of those.
- **What makes this a real test.** The screen's edge (9.7 kAU) sits inside the zone of VNT's failure, and its W term pushes inside the edge and pulls outside it.

## The model and the field
- **Model.**  The action form  of `TIDAL_WIDE_BINARY_2026-10-15.md`, at  x*_A  =  7.04×10¹¹, with the live a₀ = 1.1607×10⁻¹⁰ m/s². External field g_e ∈ {1.9, 2.32}×10⁻¹⁰ m/s²; 2.32 is VNT's nominal value.
- **Field.** dg(x) = g_ph(x) − g_ph(Sun) for a lone 1 M☉ Sun in a uniform Newtonian external field. It uses `tidal_screening_two_body.py`'s fields and kernels, with source F + V through the D2 kernel and its local term.
- **Map.** Radii 0.05–300 kAU (34 values) and cos θ at 12 Gauss–Legendre nodes, with θ measured from g_e. The map is expanded in Legendre polynomials in cos θ and interpolated linearly in ln r.
- **Comparison configurations.**
  - Unscreened ν_std at the live a₀, g_e = 1.9 and 2.32;
  - unscreened ν_std at VNT's a₀ = 1.2×10⁻¹⁰ and g_e = 2.32 (their S1);
  - unscreened μ₁₀ at a₀ = 1.2×10⁻¹⁰ and g_e = 3.35 (their S3, the least-failing MOND case they tested).

## Gates
`oort_torque_proxy.py gates`  must exit 0:
- **O1.**  Isolated: the field  matches  the  validated `test_point` to 10⁻⁶.
- **O2.** External field, r = 0.5 kAU: the field's quadrupole matches `cassini_Q2` to 3%, for both the unscreened and the action form.
- **O3.** Far field (100 r_e): the field matches Banik & Zhao's QUMOND eq. 36 to 2×10⁻³ of g_N.
- **O4.** Resolution 1 and 2 agree to 2×10⁻⁴ of g_N.

Two validation conditions are asserted in the run:
- **Newton.** With the tide alone, a_J lies in 15–40 kAU.
- **VNT S1.** The unscreened VNT S1 configuration must give a_J < 5 kAU, VNT's "new comets down to 10³ au". If it does not, the proxy is reported as uninformative.

## Diagnostics
- **ΔL  per orbit.** First-order,  ΔL = ∫  x  ×  g dt along Kepler orbits with q = 10 au, 34 values of a from 0.5 to 120 kAU, and 400 isotropic orientations (seed 7). The same orientations are used for every field.
- **Fields.** Galactic tide (VNT eq. 31; McMillan 2017: A = −B = 14.2 km/s/kpc, ρ₀ = 0.11 M☉/pc³, δ = 0), dg, and their sum.
- **Jump threshold.** ΔL_crit = L(15 au) − L(5 au), the jump across the Jupiter–Saturn barrier.
- **Reported.** The medians, the fraction of orbits with |ΔL| ≥ ΔL_crit, and a_J, the smallest a where the median |ΔL_total| ≥ ΔL_crit.
- **Binding offset.** For a near-parabolic comet measured with a Newtonian orbit at perihelion, Δ(1/a) = 2Φ_anom(0)/GM, with Φ_anom(0) = ∫₀^∞ ⟨dg_r⟩ dr averaged over orientation.

## Decision rule (proxy only)
This  rule is applied  per g_e for  the  action  form.
- **Fails like VNT:** a_J ≤ a_J(μ₁₀, S3). The torques are at least as strong as in a MOND case VNT showed fails.
- **Newton-like in this proxy:** a_J ≥ 0.8 a_J(Newton) and |Δ(1/a)| ≤ 10⁻⁵ au⁻¹. VNT's demonstrated failure mechanism is absent at this level, and their full simulation would be the test.
- **Intermediate:** anything else. Inconclusive in this proxy.

The  proxy cannot say  "passes". Only a  full  simulation  of the comet population against the observed binding energies can.
