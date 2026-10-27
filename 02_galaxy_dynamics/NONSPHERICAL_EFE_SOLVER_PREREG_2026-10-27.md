# Pre-registration: independent axisymmetric QUMOND EFE solver for Cassini Q₂ (2026-10-27)

Written and committed before the solver produced any Q₂ number. Issue #184; ν₆ figures go to #187.

## Model (QUMOND, nonrelativistic; not AeST, not AQUAL)

∇²Φ = ∇·[ν(|∇Φ_N|/a₀) ∇Φ_N], with Φ_N = −GM/r − g_{N,e}·x, where y_e = g_{N,e}/a₀ solves
y_e ν(y_e) = g_e/a₀. The anomalous potential Φ_a = Φ − Φ_N − (ν_e − 1)Φ_N solves
∇²Φ_a = −∇·V with V = (ν − ν_e) g_N, g_N = −∇Φ_N (the dropped part only adds a point mass and a uniform field).
Solved on a log-radial grid with Legendre modes in polar angle (flux form; no use of Milgrom's
reduced double integral and no import of `efe_quadrupole_q2.py`).

Sign (Hees et al. 2014, PRD 89 102002, Eq. 6 and the line after Eq. 2): a = −∇Φ and
Φ = −GM/r − (Q₂/2) xⁱxʲ(eᵢeⱼ − δᵢⱼ/3). With Φ_a ⊃ c₂ (a₀/r_M) r² P₂(cos θ), r_M = √(GM/a₀):
**Q₂ = −3 c₂ a₀/r_M**. Derived, not matched to the repo.

## Fixed inputs

- GM = 1.32712×10²⁰ m³ s⁻² (repo value).
- a₀: fitted 1.1607×10⁻¹⁰ (μ_std SPARC fit), derived cH₀/2π = 1.0422165280763669×10⁻¹⁰ (repo formula).
- g_e: 1.90×10⁻¹⁰ (pinned) and 2.40×10⁻¹⁰ m s⁻² (the frozen Batch-1A second field).
- ν family: ν_n(y) = [(1 + √(1 + 4y⁻ⁿ))/2]^{1/n}, n = 1.0 … 8.0 step 0.5 (frozen Batch 1A); ν₂ = ν_std;
  ν₆ = ν_n at n = 6, the exact inverse of μ₆ = x/(1+x⁶)^{1/6} (checked numerically in the test).
- Cassini band: Q₂ ∈ [−2.0×10⁻²⁷, 5.2×10⁻²⁷] s⁻² (`score_switch.py`, 2026 window 1.6 ± 1.8, 2σ).

## Validation and tolerance (fixed now)

1. The reference quadrature's own error is measured first by rerunning the repo's `Q2()` at higher
   nv, nxi and v_max (validation script only; the solver never imports it).
2. Reproduction passes if |Q₂(solver, Richardson) − Q₂(pinned)| / Q₂(pinned) ≤ max(1×10⁻³,
   3 × the solver's own convergence error, 3 × the reference's error) for ν_std at a₀ = 1.1607×10⁻¹⁰,
   g_e = 1.9×10⁻¹⁰ (pinned 1.9017920213×10⁻²⁶). Same rule for every frozen Batch-1A row.
3. External anchor: Hees 2016 Table 2 (ν₂, a₀ = 1.60×10⁻¹⁰, g_e = 1.9×10⁻¹⁰: −q ≈ 0.10, Q₂ ≈ 26×10⁻²⁷),
   two-digit agreement.
4. Convergence shown in N_r, N_θ (Legendre nodes / modes), r_max and r_min (table).

## Verdict rule (fixed now)

Per (ν, a₀): PASS if both g_e give Q₂ inside the band with the band edge outside Q₂ ± 3·err;
FAIL if either g_e is outside the band by more than 3·err; otherwise INCONCLUSIVE.
No parameter is tuned. A failure stays in the ledger.
