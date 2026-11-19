# Theory 3 gate (2026-11-18) — exploration, no tier change

Runs the panel's "Theory 3" (w=1/3 tracker replacing Q³ + p≥3/2 Vainshtein screening) as SAT/UNSAT.
`python3 theory3_gate.py` → `THEORY3_GATE.json`.

**Verdict: UNSAT as proposed.**

1. BBN, free w=1/3 field: ρ_φ∝a⁻⁴ for any amplitude, so ΔN_eff (needs ≈ +0.66 to cancel the √(27/32) deficit) is an initial condition, not a prediction. Fails the stated metric.
2. BBN, scaling attractor (amplitude fixed by a Lagrangian slope k): the RD window Ω_φ∈[0.033,0.125] forces Ω_φ≥0.0248 in matter domination, ≈7× the Planck early-DE bound (0.0036; still >1× for any bound under 0.025). Survives only if scaling exits before recombination — a new tuned scale.
3. Cassini: VAINSHTEIN_PREQ [D] needs p≥1.890. Cubic Galileon (p=1.5, the proposal) fails. Quartic (p=2) clears it but generic G4X breaks c_T=c (GW170817).

Open door left: a DHOST/beyond-Horndeski quartic with c_T=c (p=2) plus a scaling field that exits before z~1100. Both add structure; neither is derived. Per the panel's own rule, UNSAT routes to Theory 1 (two-phase), whose test is the same three gates.

## Open door, run 2 (`open_door_gate.py` → `OPEN_DOOR_GATE.json`) — [O], O(1) factors dropped
- Decay bound (Creminelli+ 2018, arXiv:1809.03484: α_H=0 + c_T=c rules out quartic/quintic GLPV) kills beyond-Horndeski/DHOST quartics. Only **pure Horndeski quartic** (α_H=0, p=2) remains, bound by |α_T|≲1e-15.
- p=2 needs the Sun's Vainshtein radius in **[1.09, 2.36] pc** (lower: Mercury precession; upper: Galactic cap). Window exists.
- α_T ≈ (4.6e-13 … 4.9e-11)·ε⁴ with ε = φ̇/(M_p H₀) → needs **ε ≲ 0.07–0.22**.
- At SZ21's reference Q₀=0.1 Mpc⁻¹, ε≈430 → α_T≈0.02–2: **closed**. Survives only if Q₀ ≲ ~2×10⁻⁵ Mpc⁻¹ AND that still gives the dust branch. That is the single deciding check.
- BBN compensator exit: one scalar mass in [1.9e-27, 2.2e-16] eV (11 decades — a loose, not fine, tune).

## Small-Q₀ dust check (`small_q0_dust_check.py` → `SMALL_Q0_DUST.json`) — [O]
- Dust validity (Q−Q₀)/Q₀ = ρ/(μ²(2−K_B)) — **Q₀ cancels** (SymPy-asserted). Only μ = √(2K₂/(2−K_B))·Q₀ matters.
- Need μ ≳ 7.6 Mpc⁻¹ (dust by z_rec) to 41 Mpc⁻¹ (by z_eq). Q₀ ≤ 2×10⁻⁵ Mpc⁻¹ just needs K₂ ≈ 7×10¹⁰–2×10¹² (2.5×10⁷ × SZ's).
- **Door stays OPEN.** New flags: (a) strong-coupling scale of Q fluctuations at K₂~10¹¹; (b) 1/μ ≲ 25–130 kpc caps MOND's reach (inherited from SZ21, not new to this door).

## SPARC reach vs 1/μ (`sparc_mu_reach.py` → `SPARC_MU_REACH.json`) — [O]
- Largest SPARC radius is 108.3 kpc. With 1/μ = 132.7 kpc (dust by recombination), 0/175 galaxies and 0/2350 low-acceleration points lie beyond: **passes**.
- With 1/μ = 24.5 kpc (dust by equality), 45 galaxies and 357/2350 (15%) low-acceleration points lie beyond: **fails**.
- So the open door is pinned to μ ≈ 7.6–9 Mpc⁻¹, a ~20% band. Deciding question: must the condensate already be dust at z_eq (CMB peak heights), or is z_rec enough? (g_bar uses Υ=1 here; counting only.)
