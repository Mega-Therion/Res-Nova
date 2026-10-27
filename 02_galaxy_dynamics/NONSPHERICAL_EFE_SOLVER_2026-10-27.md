# Independent axisymmetric QUMOND EFE solver: Cassini Q₂ (2026-10-27)

Issue #184 (ν₆ figure also on #187). Pre-registration: `NONSPHERICAL_EFE_SOLVER_PREREG_2026-10-27.md`,
committed before any solver number. No tier changes. Every number here is `[E]` (measured by the
scripts named), at QUMOND level only.

## Scope

- **Model.** QUMOND with a uniform external field: ∇²Φ = ∇·[ν(|∇Φ_N|/a₀)∇Φ_N], Φ_N = point mass + uniform
  Newtonian field with y_e ν(y_e) = g_e/a₀. Nonrelativistic. It is **not** AeST and **not** AQUAL. The two differ
  away from spherical symmetry, so this reproduces neither Muse's AQUAL-level ν₆ gate nor any λ_s dependence. The
  records give no QUMOND-level mapping of λ_s, so λ_s is out of scope.
- **ν₆** here is ν_n at n = 6, the exact inverse of μ₆ = x/(1+x⁶)^{1/6} (checked to < 10⁻¹² in the test). It is
  not Muse's 𝒥₆-total AeST embedding.

## Method (`qumond_axisym_efe.py`)

- **Variables.** Dimensionless units: r_M = √(GM/a₀), a₀, and potential a₀r_M. The anomalous potential solves
  ∇²Φ_a = −∇·V with V = (ν−1)g_N + (1−ν_e)y_e ẑ. That is (ν−ν_e)g_N less its divergence-free, pure-monopole
  point-mass part. ν−1 is computed without cancellation near the Sun.
- **Discretisation.** Legendre projection in polar angle (Gauss nodes) in flux form, so only V is sampled. V has a
  √-cusp at the on-axis null of g_N; its divergence would be singular there. Each multipole is a radial BVP in
  s = ln r, second-order finite differences, with exact source-free boundary behaviour: r^l inside, r^−(l+1)
  outside. c₂ = u₂/r² is read at r = 0.01 r_M.
- **Sign, from Hees et al. 2014 (PRD 89, 102002, Eq. 6; a = −∇Φ).** Q₂ = −3c₂a₀/r_M and Milgrom's q = 2c₂.
  The sign is derived from that equation, not matched to the repo.
- **Independence.** The solver does not import `efe_quadrupole_q2.py`, which implements Milgrom's reduced double
  integral. The repo's values enter only as JSON numbers in the driver.

## Validation

**The pinned row: ν_std, a₀ = 1.1607×10⁻¹⁰, g_e = 1.9×10⁻¹⁰.**

| | Q₂ (s⁻²) |
|---|---|
| pinned (SECOND_FIELD_GATES.json) | 1.9017920213×10⁻²⁶ |
| this solver, Richardson (n_r 4000 → 7999) | 1.9016367423×10⁻²⁶ ± 8×10⁻³² |
| relative difference | −8.2×10⁻⁵ |
| σ vs 2026 window (1.6 ± 1.8)×10⁻²⁷ | 9.6758 (pinned 9.6766) |

**The reference's own quadrature error, measured.** Script: `nonspherical_efe_reference_sensitivity.py`. It reruns
the repo integrand at higher resolution.

| (nv, nxi) | reference Q₂ |
|---|---|
| (3000, 400) | 1.9017920213×10⁻²⁶ |
| (3000, 1600) | 1.9023344544×10⁻²⁶ |
| (3000, 6400) | 1.8988369371×10⁻²⁶ |
| (12000, 6400) | 1.8988305360×10⁻²⁶ |

- **What it shows.** The reference moves by up to 1.6×10⁻³ (relative) with its ξ quadrature and does not settle
  monotonically. Its error is therefore ≳10⁻³. The solver's −8.2×10⁻⁵ offset is inside that.
- **v_max sensitivity.** Raising the reference's v_max to 10⁴ at nv 12000, nxi 1600 gave 2.59×10⁻²⁶. That is
  round-off in the large-v integrand, not physics, so it is not used. It is recorded so nobody reads it as a
  result.
- **Verdict on the pre-registered tolerance.** The tolerance was max(10⁻³, 3× either error). The pinned row is
  **reproduced**.

**Convergence of this solver at the pinned row** (`NONSPHERICAL_EFE_SOLVER.json` → `convergence`):

| n_r | n_θ | r_min | r_max (r_M) | Q₂ (10⁻²⁶ s⁻²) |
|---|---|---|---|---|
| 1000 | 200 | 10⁻³ | 10³ | 1.9021655680 |
| 2000 | 200 | 10⁻³ | 10³ | 1.9017689013 |
| 4000 | 200 | 10⁻³ | 10³ | 1.9016697847 |
| 8000 | 200 | 10⁻³ | 10³ | 1.9016450025 |
| 16000 | 200 | 10⁻³ | 10³ | 1.9016388065 |
| 4000 | 50 / 100 / 400 | 10⁻³ | 10³ | 1.9016697833 / …847 / …847 |
| 2985 | 200 | 10⁻³ | 30 | 1.9016295141 |
| 3333 | 200 | 10⁻³ | 10² | 1.9016687218 |
| 4667 | 200 | 10⁻³ | 10⁴ | 1.9016697757 |
| 3682 | 200 | 3×10⁻³ | 10³ | 1.9016697935 |
| 4667 | 200 | 10⁻⁴ | 10³ | 1.9016697882 |

- **Radial resolution.** Successive-difference ratios are 4.002, 3.9995 and 3.9997: clean second order. The
  Richardson limit is 1.9016367×10⁻²⁶.
- **Angular resolution.** Converged to 10⁻⁹ by n_θ = 100.
- **Domain.** Rows 9–13 hold the grid spacing h fixed. With r_max ≥ 10² and any r_min in 10⁻⁴…3×10⁻³, Q₂ moves
  by ≤ 6×10⁻⁷ (relative).

**External anchor: Hees et al. 2016, Table 2.**

| case | this solver | Hees |
|---|---|---|
| ν₂, a₀ = 1.60×10⁻¹⁰ | −q = 0.1001, Q₂ = 2.64×10⁻²⁶ | −q = 0.10, Q₂ = 26×10⁻²⁷ |
| RAR ν̄₀.₅, a₀ = 1.48×10⁻¹⁰ | −q = 0.1316, Q₂ = 3.09×10⁻²⁶ | −q = 0.131, Q₂ = 31×10⁻²⁷ |

## Frozen Batch-1A family and ν₆

- **Grid.** All 15 n × 2 a₀ × 2 g_e rows were run. The fitted a₀ is 1.1607×10⁻¹⁰ and the derived a₀ is
  1.0422×10⁻¹⁰. The band is [−2.0, 5.2]×10⁻²⁷ s⁻².
- **Agreement with the frozen file.** The largest relative difference from `FROZEN_BATCH1A.json` is 2.0×10⁻⁴,
  at n = 1. Every pre-registered verdict matches the frozen `cassini_gate` (30/30).
- **Solver error.** Richardson errors are ≤ 10⁻⁵ relative, so no row lands in INCONCLUSIVE.

| n | a₀ | Q₂(1.9) ×10⁻²⁷ | Q₂(2.4) ×10⁻²⁷ | verdict |
|---|---|---|---|---|
| 1.0 | fit / der | 27.689 / 26.652 | 35.994 / 34.338 | FAIL / FAIL |
| 1.5 | fit / der | 23.472 / 21.575 | 27.503 / 24.902 | FAIL / FAIL |
| 2.0 (ν_std) | fit / der | 19.016 / 16.661 | 20.008 / 17.170 | FAIL / FAIL |
| 2.5 | fit / der | 15.303 / 12.780 | 14.466 / 11.777 | FAIL / FAIL |
| 3.0 | fit / der | 12.374 / 9.863 | 10.543 / 8.160 | FAIL / FAIL |
| 3.5 | fit / der | 10.098 / 7.698 | 7.794 / 5.752 | FAIL / FAIL |
| 4.0 | fit / der | 8.332 / 6.091 | 5.863 / 4.141 | FAIL / FAIL |
| 4.5 | fit / der | 6.957 / 4.893 | 4.498 / 3.052 | FAIL / PASS |
| 5.0 | fit / der | 5.880 / 3.993 | 3.522 / 2.307 | FAIL / PASS |
| 5.5 | fit / der | 5.033 / 3.312 | 2.817 / 1.790 | PASS / PASS |
| **6.0 (ν₆)** | fit / der | **4.361 / 2.792** | **2.302 / 1.426** | **PASS / PASS** |
| 6.5 | fit / der | 3.824 / 2.391 | 1.921 / 1.166 | PASS / PASS |
| 7.0 | fit / der | 3.393 / 2.079 | 1.636 / 0.977 | PASS / PASS |
| 7.5 | fit / der | 3.043 / 1.834 | 1.420 / 0.838 | PASS / PASS |
| 8.0 | fit / der | 2.758 / 1.641 | 1.254 / 0.734 | PASS / PASS |

- **Near-edge rows.** n = 5.5 fitted sits 3.2% under the 5.2×10⁻²⁷ edge; n = 4.5 and n = 5.0 derived sit 6% and
  23% under it. Those margins are far above the solver error (≤ 10⁻⁵). They are well below the reference
  quadrature's ~10⁻³, but the two methods agree on the side of the edge.
- **ν₆ at QUMOND level.** Q₂ = 4.361×10⁻²⁷ s⁻² at g_e = 1.9×10⁻¹⁰ with the fitted a₀: **PASS**, 16% inside the
  upper edge. This says nothing about AeST, about λ_s, or about SPARC. Batch 1A's SPARC gate fails for ν₆
  (frozen file).

## What this changes

- The Cassini gate's QUMOND numbers no longer rest on one quadrature. An independent field solve reproduces the
  pinned ν_std failure (9.68σ) and all 30 Batch-1A verdicts.
- The AeST gate of #184 (𝒥_total, 𝒥_D9 and ν₆-total with λ_s) is still Muse's unreproduced `[O]`. This solver does
  not represent the AeST system, and it stops at QUMOND as #184 requires.

## Reproduce

```
python3 02_galaxy_dynamics/test_qumond_axisym_efe.py          # ~6 s, in local_gate.sh
python3 02_galaxy_dynamics/nonspherical_efe_run.py            # ~13 min, writes NONSPHERICAL_EFE_SOLVER.json
python3 02_galaxy_dynamics/nonspherical_efe_reference_sensitivity.py   # ~10 min, reference quadrature table
```

The test checks the ν_n inversions, a manufactured Poisson problem with a known quadrupole (−1 to 10⁻⁴), and a
coarse reproduction of the pinned value. A sabotaged copy that flipped the sign of the angular flux term failed
the test (exit 1).
