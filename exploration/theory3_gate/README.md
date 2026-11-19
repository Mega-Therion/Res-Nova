# Theory 3 gate (2026-11-18) — exploration, no tier change

Runs the panel's "Theory 3" (w=1/3 tracker replacing Q³ + p≥3/2 Vainshtein screening) as SAT/UNSAT.
`python3 theory3_gate.py` → `THEORY3_GATE.json`.

**Verdict: UNSAT as proposed.**

1. BBN, free w=1/3 field: ρ_φ∝a⁻⁴ for any amplitude, so ΔN_eff (needs ≈ +0.66 to cancel the √(27/32) deficit) is an initial condition, not a prediction. Fails the stated metric.
2. BBN, scaling attractor (amplitude fixed by a Lagrangian slope k): the RD window Ω_φ∈[0.033,0.125] forces Ω_φ≥0.0248 in matter domination, ≈7× the Planck early-DE bound (0.0036; still >1× for any bound under 0.025). Survives only if scaling exits before recombination — a new tuned scale.
3. Cassini: VAINSHTEIN_PREQ [D] needs p≥1.890. Cubic Galileon (p=1.5, the proposal) fails. Quartic (p=2) clears it but generic G4X breaks c_T=c (GW170817).

Open door left: a DHOST/beyond-Horndeski quartic with c_T=c (p=2) plus a scaling field that exits before z~1100. Both add structure; neither is derived. Per the panel's own rule, UNSAT routes to Theory 1 (two-phase), whose test is the same three gates.
