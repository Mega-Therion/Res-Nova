#!/usr/bin/env python3
"""C1 — SO(3) ≅ V₂(ℝ³) Haar measure derivation attempt.

The C0-R1 audit established V₂(ℝ³) ≅ SO(3) as the settled substrate.
The question: can θ = 1/√2 (or 0.7, or ln2) be derived from the 
natural geometry of SO(3) without using θ to define the construction?

This script systematically explores EVERY natural geometric quantity
on SO(3) that produces a dimensionless number in [0,1]:

1. Haar measure of natural subsets (geodesic balls, Voronoi cells, etc.)
2. Spectral quantities (eigenvalues of the Laplacian, Casimir, etc.)
3. Random matrix theory quantities (CDF of eigenvalue angle)
4. Representation-theoretic quantities (characters, dimensions)
5. The CARTAN TRIALITY action on roots/weights

The key insight from Chyren's corpus: the physical selection is
"via Cartan triality" — S₃ acting on the exceptional groups.
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "so3_haar_derivation_results.json"


# ═══════════════════════════════════════════════════════════════════════
# 1. SO(3) HAAR MEASURE GEOMETRY
# ═══════════════════════════════════════════════════════════════════════

# SO(3) parameterized by rotation angle φ ∈ [0,π] and axis n ∈ S².
# The Haar measure is: dμ = (1/2π²) sin²(φ/2) dφ dΩ
# where dΩ is the uniform measure on S² (area element).
# Equivalently: dμ = (1/π)(1 - cos φ)/2 dφ  (marginalized over axis)
# Or using Rodrigues: dμ = (2/π) sin²(φ/2) dφ  on [0,π]

# Normalized CDF of the rotation angle under Haar measure:
# F(φ) = ∫₀^φ (2/π) sin²(t/2) dt = (φ - sin φ) / π

def haar_cdf(phi: float) -> float:
    """CDF of rotation angle under normalized Haar measure on SO(3)."""
    return (phi - math.sin(phi)) / math.pi

def haar_pdf(phi: float) -> float:
    """PDF of rotation angle under normalized Haar measure on SO(3)."""
    return (1 - math.cos(phi)) / math.pi  # = (2/π) sin²(φ/2)

def inverse_haar_cdf(p: float) -> float:
    """Find φ such that F(φ) = p, for p ∈ [0,1]."""
    if p <= 0:
        return 0.0
    if p >= 1:
        return math.pi
    return brentq(lambda phi: haar_cdf(phi) - p, 0, math.pi)


# ═══════════════════════════════════════════════════════════════════════
# 2. NATURAL GEOMETRIC SUBSETS AND THEIR HAAR MEASURES
# ═══════════════════════════════════════════════════════════════════════

def compute_natural_measures() -> dict:
    """Compute Haar measure of every natural geometric subset of SO(3)."""
    results = {}
    
    # (a) Geodesic balls centered at identity
    # The geodesic distance on SO(3) from the identity to R(φ,n) is φ (in radians)
    # Ball of radius φ₀: B(φ₀) = {R : angle(R) ≤ φ₀}
    # μ(B(φ₀)) = F(φ₀) = (φ₀ - sin φ₀) / π
    
    special_angles = {
        "pi/6": math.pi/6,      # 30°
        "pi/4": math.pi/4,      # 45°
        "pi/3": math.pi/3,      # 60°
        "pi/2": math.pi/2,      # 90°
        "2pi/3": 2*math.pi/3,   # 120°
        "3pi/4": 3*math.pi/4,   # 135°
        "5pi/6": 5*math.pi/6,   # 150°
    }
    
    results["geodesic_ball_measures"] = {}
    for name, phi in special_angles.items():
        measure = haar_cdf(phi)
        results["geodesic_ball_measures"][name] = {
            "angle_rad": phi,
            "angle_deg": math.degrees(phi),
            "haar_measure": measure,
        }
    
    # (b) What angle gives Haar measure = 1/√2?
    phi_sqrt2 = inverse_haar_cdf(1/math.sqrt(2))
    results["angle_for_1/sqrt2"] = {
        "phi_rad": phi_sqrt2,
        "phi_deg": math.degrees(phi_sqrt2),
        "verification": haar_cdf(phi_sqrt2),
    }
    
    # (c) What angle gives Haar measure = 0.7?
    phi_07 = inverse_haar_cdf(0.7)
    results["angle_for_0.7"] = {
        "phi_rad": phi_07,
        "phi_deg": math.degrees(phi_07),
        "verification": haar_cdf(phi_07),
    }
    
    # (d) What angle gives Haar measure = ln2?
    phi_ln2 = inverse_haar_cdf(math.log(2))
    results["angle_for_ln2"] = {
        "phi_rad": phi_ln2,
        "phi_deg": math.degrees(phi_ln2),
        "verification": haar_cdf(phi_ln2),
    }
    
    # (e) Haar measure at the "balanced ternary" angles:
    # The S₃ (triality) group has natural angles 0, 2π/3, 4π/3
    # In SO(3), 2π/3 = 120° rotation
    results["triality_angles"] = {
        "2pi/3_measure": haar_cdf(2*math.pi/3),
        "note": "120° rotation is the fundamental triality angle in S₃ ⊂ SO(3)",
    }
    
    # (f) CRITICAL: Does any NATURAL subset have measure 1/√2?
    # "Natural" means: defined by representation-theoretic, geometric, or 
    # group-theoretic data, NOT by choosing a cutoff to match the target.
    
    # Natural subsets:
    # - Rotations by ≤ 90°: F(π/2) = (π/2 - 1)/π ≈ 0.1817
    # - Rotations by ≤ 120°: F(2π/3) = (2π/3 - √3/2)/π ≈ 0.3643 (actually...)
    for name, phi in special_angles.items():
        m = haar_cdf(phi)
        # Check proximity to targets
        for target_name, target_val in [("1/sqrt2", 1/math.sqrt(2)), ("0.7", 0.7), ("ln2", math.log(2))]:
            if abs(m - target_val) < 0.001:
                results[f"NEAR_MATCH_{name}_to_{target_name}"] = {
                    "angle": name,
                    "measure": m,
                    "target": target_val,
                    "delta": m - target_val,
                }
    
    return results


# ═══════════════════════════════════════════════════════════════════════
# 3. SO(3) SPECTRAL THEORY  
# ═══════════════════════════════════════════════════════════════════════

def compute_spectral_quantities() -> dict:
    """Spectral data of the Laplace-Beltrami operator on SO(3).
    
    SO(3) = SU(2)/Z₂. The spectrum of the Laplacian on SO(3) consists of
    eigenvalues λ_ℓ = ℓ(ℓ+1) for ℓ = 0, 1, 2, 3, ...
    with multiplicity (2ℓ+1)².
    
    On SU(2) ≅ S³: eigenvalues are n(n+2) with multiplicity (n+1)²,
    and SO(3) keeps only even n (integer ℓ).
    """
    results = {}
    
    # First few eigenvalues and multiplicities
    eigendata = []
    for ell in range(20):
        eigenval = ell * (ell + 1)
        mult = (2 * ell + 1) ** 2
        eigendata.append({
            "ell": ell,
            "eigenvalue": eigenval,
            "multiplicity": mult,
        })
    results["laplacian_spectrum"] = eigendata
    
    # Spectral ratios
    results["spectral_ratios"] = {
        "lambda_1/lambda_2": 2/6,  # = 1/3
        "lambda_1/lambda_3": 2/12, # = 1/6
        "lambda_2/lambda_3": 6/12, # = 1/2
        "note": "Standard ratios from ℓ(ℓ+1). None is 7/10 or 1/√2."
    }
    
    # Heat kernel trace: Z(t) = Σ (2ℓ+1)² exp(-ℓ(ℓ+1)t)
    # At specific times, this gives geometric invariants
    results["heat_kernel_at_special_times"] = {}
    for t in [0.1, 0.5, 1.0, math.log(2), 1/math.sqrt(2)]:
        Z = sum((2*ell+1)**2 * math.exp(-ell*(ell+1)*t) for ell in range(100))
        Z_normalized = Z / (8 * math.pi**2)  # Normalize by Vol(SO(3))
        results["heat_kernel_at_special_times"][f"t={t:.4f}"] = {
            "Z": Z,
            "Z_normalized": Z_normalized,
        }
    
    # Weyl's asymptotic: N(λ) ~ Vol × λ^{3/2} / (6π²)
    # For SO(3), Vol = 8π² (with standard normalization)
    results["volume_SO3"] = 8 * math.pi**2
    results["volume_SO3_approx"] = f"8π² ≈ {8*math.pi**2:.6f}"
    
    return results


# ═══════════════════════════════════════════════════════════════════════
# 4. CARTAN TRIALITY AND S₃ ACTION
# ═══════════════════════════════════════════════════════════════════════

def compute_triality_quantities() -> dict:
    """Triality-related geometric quantities.
    
    Cartan triality: the outer automorphism group of D₄ = Spin(8) is S₃.
    This S₃ permutes the three 8-dimensional representations:
    vector (8_v), left spinor (8_s), right spinor (8_c).
    
    The action on the Dynkin diagram permutes the three external nodes.
    
    When D₄ ⊂ E₈, the triality induces structure on the E₈ root system.
    """
    results = {}
    
    # S₃ structure
    results["S3_structure"] = {
        "order": 6,
        "conjugacy_classes": {
            "identity": {"size": 1, "cycle_type": "[1,1,1]"},
            "transpositions": {"size": 3, "cycle_type": "[2,1]"},
            "3-cycles": {"size": 2, "cycle_type": "[3]"},
        },
        "class_fractions": {
            "identity": "1/6",
            "transpositions": "1/2",
            "3-cycles": "1/3",
        },
    }
    
    # Key observation: S₃ has NO natural fraction equal to 7/10 or 1/√2
    # The only fractions from S₃ are: 1/6, 1/3, 1/2, 2/3, 5/6
    
    # BUT: the triality acts on the D₄ root system (24 roots)
    # and through D₄ ⊂ E₈ on the E₈ root system (240 roots)
    
    # D₄ roots: ±eᵢ±eⱼ (i<j, i,j ∈ {1,2,3,4}), total 24
    # Triality permutes the three 8-dimensional reps
    # Fixed-point set under triality: the G₂ subalgebra
    
    results["D4_to_G2_triality"] = {
        "D4_roots": 24,
        "G2_roots": 12,
        "fixed_fraction": "12/24 = 1/2",
        "note": "G₂ = fixed subalgebra of D₄ under full S₃ triality"
    }
    
    # G₂ has 12 roots: 6 short + 6 long
    # Ratio long/short root lengths: √3
    # This gives a natural geometric constant from triality!
    results["G2_geometry"] = {
        "short_roots": 6,
        "long_roots": 6,
        "long_to_short_ratio": math.sqrt(3),
        "natural_fractions": {
            "short/total": "1/2",
            "long/total": "1/2",
        },
    }
    
    # The D₄ embedding in E₈:
    # E₈ decomposes under D₄ × D₄ (one possible maximal subgroup)
    # D₄ has 24 roots; E₈ has 240 roots
    # Under triality: the 240 roots decompose into triality orbits
    
    # Crucial: what fraction of E₈ roots are FIXED under the S₃ triality?
    # This depends on HOW the triality embeds. The standard Cartan triality
    # acts on D₄, and through D₄ × D₄ ⊂ E₈, it acts on E₈.
    
    # Under the standard embedding:
    # E₈ = (28,1) + (1,28) + (8_v,8_v) + (8_s,8_s) + (8_c,8_c)
    # where 28 = adjoint of D₄
    # Triality permutes the three (8,8) pieces
    
    # Fixed under triality: (28,1) + (1,28) + diagonal of the three (8,8)
    # That diagonal = G₂ × G₂ subalgebra
    
    # Counting roots fixed by triality in E₈:
    d4_adjoint_roots = 24  # roots of D₄
    d4_d4_adjoint = 2 * 24  # (28,1) + (1,28) minus Cartan
    # Actually for root counting: D₄ has 24 roots, so (D₄)₁ + (D₄)₂ contribute 48 roots
    # The three (8,8) contribute 3 × 64 = 192 roots
    # Total: 48 + 192 = 240 ✓
    
    # Under Z₃ triality (3-cycle):
    # (D₄)₁ is fixed, (D₄)₂ is fixed (triality acts on the (8,8) pieces)
    # The 192 = 3 × 64 roots in the (8,8) sectors: only the "diagonal" 64 are fixed
    # So: 48 + 64 = 112 roots fixed by the 3-cycle
    
    results["E8_triality_fixed_counts"] = {
        "total_E8_roots": 240,
        "adjoint_D4_D4_roots": 48,
        "three_8x8_roots": 192,
        "each_8x8_sector_roots": 64,
        "fixed_under_Z3": {
            "adjoint_piece": 48,
            "diagonal_8x8": 64,
            "total": 112,
            "fraction": "112/240 = 7/15",
        },
        "moved_by_Z3": {
            "total": 128,
            "fraction": "128/240 = 8/15",
        },
        "NOTE": "112/240 = 7/15 ≈ 0.4667, NOT 7/10. But 128/240 = 8/15 ≈ 0.5333."
    }
    
    # KEY COMPUTATION: What if we look at the TRANSPOSITION (Z₂ ⊂ S₃)?
    # A transposition swaps two of the three 8-dim reps and fixes the third
    # Swaps (8_s,8_s) ↔ (8_c,8_c), fixes (8_v,8_v)
    # Fixed: 48 (adjoint) + 64 (fixed 8_v sector) + 64 (diagonal of swapped pair)
    # = 48 + 64 + 64 = 176
    # Fraction: 176/240 = 11/15 ≈ 0.7333
    
    results["E8_transposition_fixed"] = {
        "description": "Roots fixed under a Z₂ transposition within the S₃ triality",
        "adjoint_piece": 48,
        "fixed_8x8_sector": 64,
        "diagonal_of_swapped_pair": 64,
        "total_fixed": 176,
        "fraction": "176/240 = 11/15",
        "numerical": 176/240,
        "delta_from_0.7": abs(176/240 - 0.7),
        "delta_from_1/sqrt2": abs(176/240 - 1/math.sqrt(2)),
        "NOTE": f"11/15 = {11/15:.10f}, vs 7/10 = 0.7, 1/√2 = {1/math.sqrt(2):.10f}"
    }
    
    # What about: (total - fixed_by_Z3) / total ?
    # (240 - 112) / 240 = 128/240 = 8/15 ≈ 0.5333
    
    # What about complement of transposition orbit?
    # 240 - 176 = 64, 64/240 = 4/15 ≈ 0.2667
    
    # WHAT IF: the "moved" roots under the 3-cycle, restricted to ONE 8×8 sector?
    # Each sector has 64 roots. Under Z₃, one sector is mapped to the next.
    # The number of roots in a single sector = 64
    # 64/240 = 4/15 ≈ 0.2667
    
    # Let's look at it differently: 
    # The 240 E₈ roots split into triality orbits
    # Orbits of size 1 (fixed by all of S₃): G₂ × G₂ roots
    # Orbits of size 2 (fixed by one transposition): ...
    # Orbits of size 3 (fixed by nothing): ...
    # Orbits of size 6 (regular S₃ orbit): ...
    
    # Burnside: |fixed pts| avg = |orbits|
    # For S₃ on 240 roots:
    # |Fix(e)| = 240 (all)
    # |Fix(12)| = |Fix(13)| = |Fix(23)| = 176 (transposition)  
    # |Fix(123)| = |Fix(132)| = 112 (3-cycle)
    # Average = (240 + 3×176 + 2×112) / 6 = (240 + 528 + 224) / 6 = 992/6
    
    burnside_sum = 240 + 3*176 + 2*112
    n_orbits = burnside_sum / 6
    results["burnside_orbit_count"] = {
        "sum": burnside_sum,
        "n_orbits": n_orbits,
        "note": f"Number of S₃ orbits on E₈ roots = {n_orbits}",
        "if_integer": n_orbits == int(n_orbits),
    }
    
    # IMPORTANT FINDING: Let's compute actual fractions more carefully
    # The key question is whether there's a NATURAL probability space
    # on the triality orbits where some event has probability 1/√2 or 7/10
    
    # Alternative: V₂(ℝ³) ≅ SO(3) has Vol = 8π²
    # The S² base of the frame bundle has Vol = 4π
    # Ratio: 8π²/(4π) = 2π — the fiber length
    # Normalized: 4π/(8π²) = 1/(2π) ≈ 0.1592
    
    results["frame_bundle_ratios"] = {
        "Vol_SO3": 8 * math.pi**2,
        "Vol_S2": 4 * math.pi,
        "fiber_length": 2 * math.pi,
        "S2_over_SO3": 4*math.pi / (8*math.pi**2),
        "note": "V₂(ℝ³) → S² is a principal S¹ bundle with fiber S¹ of length 2π",
    }
    
    # KEY: Cartan's classification of symmetric spaces
    # SO(3)/SO(2) = S²
    # The natural "transition probability" between two random frames:
    # P(two random frames share the same first vector) = Vol(SO(2))/Vol(SO(3)) × Vol(S²)
    # = ... this gets into representation theory
    
    return results


# ═══════════════════════════════════════════════════════════════════════
# 5. THE BALANCED TERNARY CONNECTION
# ═══════════════════════════════════════════════════════════════════════

def compute_ternary_structure() -> dict:
    """Explore the balanced ternary base hypothesis.
    
    User's claim: "everything in the universe can be built from a balanced 
    ternary base just like everything in a 57,600 or 240d or e8 or e6×36"
    
    We check: what quantities arise naturally from {-1, 0, +1}³ acting on 
    the E₈ root system and SO(3)?
    """
    results = {}
    
    # Balanced ternary: base 3 with digits {-1, 0, +1}
    # The E₈ half-integer roots use exactly this alphabet!
    # 128 roots with coordinates in {±1}^8, even parity
    
    # In SO(3): the three "natural" rotations are:
    # R(0) = identity (digit 0)
    # R(+2π/3) = positive triality rotation (digit +1)  
    # R(-2π/3) = negative triality rotation (digit -1)
    
    # The Haar measure of the "positive" region [0, 2π/3]:
    pos_region = haar_cdf(2*math.pi/3)
    # The "negative" region [-2π/3, 0] = [π, π] (mapped to [4π/3, 2π] → π to π ?)
    # Actually in SO(3), angle is [0,π], so we need to think differently
    
    results["ternary_SO3"] = {
        "triality_angle": "2π/3 = 120°",
        "haar_measure_0_to_2pi/3": pos_region,
        "haar_measure_2pi/3_to_pi": 1.0 - pos_region,
        "ratio_small_to_total": pos_region,
        "note": f"F(2π/3) = {pos_region:.10f} — NOT 1/3 because Haar measure is non-uniform in angle!"
    }
    
    # The ternary structure on S³ (SU(2)):
    # SU(2) covers SO(3) 2:1. On SU(2), angle runs [0, 2π]
    # The SU(2) Haar CDF: F(θ) = (θ - sin θ cos θ) / (2π)... 
    # Actually on SU(2) ≅ S³: Haar measure is uniform on S³
    # Parameterized by (θ/2, n): dμ = (1/2π²) sin²(θ/2) d(θ/2) dΩ for θ ∈ [0, 2π]
    
    # The natural "ternary partition" of SU(2):
    # Identity neighborhood: θ ∈ [0, 2π/3]
    # Middle: θ ∈ [2π/3, 4π/3]  
    # Antipodal neighborhood: θ ∈ [4π/3, 2π]
    
    su2_sector1 = (2*math.pi/3 - math.sin(2*math.pi/3)) / (2*math.pi)  
    # Wait, the SU(2) Haar CDF for the "rotation angle" θ ∈ [0, 2π]:
    # is NOT the same as SO(3). On SU(2), the measure is
    # proportional to sin²(θ/2) dθ, normalized over [0, 2π]
    # ∫₀²π sin²(θ/2)dθ = π
    # So CDF_SU2(θ) = (1/π) ∫₀^θ sin²(t/2) dt = (θ - sin θ)/(2π)
    
    def su2_cdf(theta: float) -> float:
        return (theta - math.sin(theta)) / (2 * math.pi)
    
    # Ternary partition of SU(2) at 2π/3 intervals:
    sector_1 = su2_cdf(2*math.pi/3)
    sector_2 = su2_cdf(4*math.pi/3) - sector_1
    sector_3 = 1.0 - su2_cdf(4*math.pi/3)
    
    results["ternary_SU2"] = {
        "sector_1_measure": sector_1,
        "sector_2_measure": sector_2,
        "sector_3_measure": sector_3,
        "sum": sector_1 + sector_2 + sector_3,
        "symmetry": "The distribution is symmetric under θ → 2π-θ, so sector_1 = sector_3",
    }
    
    # CRITICAL CHECK: Does sector_2 (the "middle" ternary digit) have measure 1/√2?
    results["ternary_sector_vs_targets"] = {
        "sector_2_vs_1/sqrt2": abs(sector_2 - 1/math.sqrt(2)),
        "sector_2_vs_0.7": abs(sector_2 - 0.7),
        "sector_2_vs_ln2": abs(sector_2 - math.log(2)),
        "sector_1+sector_3_vs_targets": {
            "sum_1_3": sector_1 + sector_3,
            "vs_1/sqrt2": abs((sector_1 + sector_3) - 1/math.sqrt(2)),
            "vs_0.7": abs((sector_1 + sector_3) - 0.7),
        }
    }
    
    # The 240 E₈ roots and ternary structure:
    # 128 half-integer roots ∈ {±1}^8 — these are the "ternary" objects  
    # Their inner products: <α,β>/4 ∈ {-2,-1,0,1,2}
    # The number of (+1) coordinates per root: always 0,2,4,6,8 (even parity)
    # Distribution of (+1) count:
    from math import comb
    plus_one_dist = {}
    for k in range(0, 9, 2):
        count = comb(8, k)
        plus_one_dist[k] = count
    
    results["half_integer_root_structure"] = {
        "plus_one_count_distribution": plus_one_dist,
        "total": sum(plus_one_dist.values()),
        "note": "C(8,0)+C(8,2)+C(8,4)+C(8,6)+C(8,8) = 1+28+70+28+1 = 128",
        "ternary_note": "Each coordinate is in {-1,+1} — binary, not ternary. The ternary structure appears when we include the coordinate roots with zeros: {-2,0,+2} → {-1,0,+1}×2"
    }
    
    # The FULL 240-root system has balanced quinary {-2,-1,0,+1,+2} coordinates
    # If we map this to balanced ternary: {-1,0,+1} by |x|→sign(x), 0→0
    # Then the "zero fraction" per root:
    # Half-integer roots: 0 zeros each (all ±1) → ternary weight 0/8
    # Coordinate roots: 6 zeros each (two non-zero) → ternary weight 6/8
    
    # Mean ternary weight across all 240 roots:
    mean_zero_frac = (128 * 0 + 112 * 6) / (240 * 8)
    results["ternary_zero_fraction"] = {
        "half_integer_zeros_per_root": 0,
        "coordinate_zeros_per_root": 6,
        "mean_zero_fraction": mean_zero_frac,
        "mean_nonzero_fraction": 1 - mean_zero_frac,
        "note": f"Mean fraction of nonzero coordinates = {1-mean_zero_frac:.10f}",
        "delta_from_0.7": abs((1-mean_zero_frac) - 0.7),
        "delta_from_1/sqrt2": abs((1-mean_zero_frac) - 1/math.sqrt(2)),
    }
    
    return results


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main() -> None:
    print("=" * 70)
    print("SO(3) ≅ V₂(ℝ³) HAAR MEASURE & TRIALITY DERIVATION")
    print("=" * 70)
    
    measures = compute_natural_measures()
    spectral = compute_spectral_quantities()
    triality = compute_triality_quantities()
    ternary = compute_ternary_structure()
    
    # Summary: which quantities come closest to 1/√2, 0.7, ln2?
    print("\n" + "=" * 70)
    print("SUMMARY: NEAREST NATURAL QUANTITIES TO TARGET VALUES")
    print("=" * 70)
    
    targets = {"1/√2": 1/math.sqrt(2), "0.7": 0.7, "ln2": math.log(2)}
    
    candidates = []
    
    # From geodesic ball measures
    for name, data in measures.get("geodesic_ball_measures", {}).items():
        candidates.append((f"Geodesic ball at {name}", data["haar_measure"]))
    
    # From E8 triality
    if "E8_transposition_fixed" in triality:
        candidates.append(("E8 transposition-fixed fraction", triality["E8_transposition_fixed"]["numerical"]))
    if "E8_triality_fixed_counts" in triality:
        fixed_frac = 112/240
        candidates.append(("E8 Z₃-fixed fraction", fixed_frac))
        candidates.append(("E8 Z₃-moved fraction", 128/240))
    
    # From ternary structure
    if "ternary_zero_fraction" in ternary:
        candidates.append(("Ternary nonzero fraction", 1 - ternary["ternary_zero_fraction"]["mean_zero_frac"] if "mean_zero_frac" in ternary["ternary_zero_fraction"] else ternary["ternary_zero_fraction"]["mean_nonzero_fraction"]))
    
    # From SU(2) ternary sectors
    if "ternary_SU2" in ternary:
        candidates.append(("SU(2) ternary sector 2", ternary["ternary_SU2"]["sector_2_measure"]))
        candidates.append(("SU(2) ternary sectors 1+3", ternary["ternary_SU2"]["sector_1_measure"] + ternary["ternary_SU2"]["sector_3_measure"]))
    
    # From Burnside
    if "burnside_orbit_count" in triality:
        orbs = triality["burnside_orbit_count"]["n_orbits"]
        candidates.append(("Burnside orbits/240", orbs/240))
    
    for target_name, target_val in targets.items():
        print(f"\n  Target: {target_name} = {target_val:.10f}")
        ranked = sorted(candidates, key=lambda x: abs(x[1] - target_val))
        for name, val in ranked[:5]:
            delta = val - target_val
            print(f"    {name:50s} = {val:.10f}  Δ = {delta:+.6f}")
    
    # Highlight the 11/15 finding
    print(f"\n{'='*70}")
    print("CRITICAL FINDING: E₈ TRANSPOSITION-FIXED FRACTION")
    print(f"{'='*70}")
    print(f"  176 of 240 E₈ roots fixed by Z₂ transposition in S₃ triality")
    print(f"  Fraction: 11/15 = {11/15:.10f}")
    print(f"  vs θ_gate = 0.7:      Δ = {abs(11/15 - 0.7):+.6f}")
    print(f"  vs 1/√2 = {1/math.sqrt(2):.10f}: Δ = {abs(11/15 - 1/math.sqrt(2)):+.6f}")
    print(f"  vs ln2 = {math.log(2):.10f}: Δ = {abs(11/15 - math.log(2)):+.6f}")
    
    # Check sovereign ceiling at 11/15
    chi_s_11_15 = math.sqrt(11/15 * (2 - 11/15))
    print(f"\n  If θ = 11/15: χ_s = √(θ(2-θ)) = {chi_s_11_15:.10f}")
    print(f"  vs Thorne 0.998: Δ = {abs(chi_s_11_15 - 0.998):.6f}")
    print(f"  vs 0.9539:       Δ = {abs(chi_s_11_15 - 0.9539):.6f}")
    
    # Write results
    result = {
        "model_id": "C1",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "haar_measures": measures,
        "spectral": spectral,
        "triality": triality,
        "ternary": ternary,
        "candidates_ranked_by_proximity": {
            target_name: [
                {"name": name, "value": val, "delta": val - target_val}
                for name, val in sorted(candidates, key=lambda x: abs(x[1] - target_val))[:10]
            ]
            for target_name, target_val in targets.items()
        }
    }
    
    OUTPUT.write_text(json.dumps(result, indent=2, default=str) + "\n", encoding="utf-8")
    print(f"\nResults written to: {OUTPUT}")


if __name__ == "__main__":
    main()
