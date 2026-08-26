#!/usr/bin/env python3
"""C1 — E8 root-system algebraic-number sweep.

The C0 audit tested only 7/10 exactly. This analysis:
1. Enumerates ALL natural event probabilities from E8 root inner products
2. Tests 1/√2 (corpus θ_amplitude), 7/10 (corpus θ_gate), ln2 (Morse anchor)
3. Searches for COMPOUND events (unions, intersections, complements) whose
   probabilities equal these targets
4. Tests κ = √(θ(2-θ)) = √0.91 ≈ 0.9539 at each candidate θ
5. Explores the balanced ternary structure: E8 has 240 roots, |W(E8)| = 696729600,
   the root lattice has kissing number 240, and the Weyl chambers tile the space
"""
from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "e8_algebraic_sweep_results.json"

# ── Algebraic targets ──
TARGETS = {
    "1/sqrt(2)": 1.0 / math.sqrt(2),          # 0.70710678...
    "7/10":      0.7,                           # 0.7 exactly
    "ln2":       math.log(2),                    # 0.69314718...
    "sqrt(0.91)":math.sqrt(0.91),               # 0.95393920... = χ_s sovereign ceiling
    "2theta-theta^2_at_1/sqrt2": 2*(1/math.sqrt(2)) - (1/math.sqrt(2))**2,  # 0.91421356...
    "sqrt(2theta-theta^2)_at_1/sqrt2": math.sqrt(2*(1/math.sqrt(2)) - (1/math.sqrt(2))**2),
    "sqrt(3)/2":  math.sqrt(3)/2,               # 0.86602540...
    "1/sqrt(3)":  1/math.sqrt(3),               # 0.57735026...
    "golden_ratio_inv": 2/(1+math.sqrt(5)),     # 0.61803398...
    "pi/4":       math.pi/4,                    # 0.78539816... (quarter-turn)
    "1/e":        1/math.e,                     # 0.36787944...
}


def build_e8_roots() -> list[tuple[int, ...]]:
    """Return 2×E8 roots as integer tuples (dot/4 = true inner product)."""
    roots: set[tuple[int, ...]] = set()
    for i, j in combinations(range(8), 2):
        for si, sj in product((-2, 2), repeat=2):
            v = [0] * 8
            v[i], v[j] = si, sj
            roots.add(tuple(v))
    for signs in product((-1, 1), repeat=8):
        if sum(x == -1 for x in signs) % 2 == 0:
            roots.add(tuple(signs))
    return sorted(roots)


def dot(a: tuple[int, ...], b: tuple[int, ...]) -> Fraction:
    return Fraction(sum(x * y for x, y in zip(a, b)), 4)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    roots = build_e8_roots()
    n = len(roots)
    assert n == 240, f"Expected 240 E8 roots, got {n}"

    # ── Step 1: Complete inner-product census ──
    # Fix one root (all are Weyl-equivalent) and compute its inner products with all others
    alpha0 = roots[0]
    ip_counts: Counter[Fraction] = Counter()
    for beta in roots:
        ip_counts[dot(alpha0, beta)] += 1

    ip_probs = {str(q): float(Fraction(c, n)) for q, c in sorted(ip_counts.items())}

    # ── Step 2: Define all natural events from the inner-product partition ──
    # These are the only non-arbitrary events definable from root geometry
    events: dict[str, int] = {}
    for q in sorted(ip_counts.keys()):
        events[f"dot={q}"] = ip_counts[q]

    # Compound natural events
    events["dot>=0"] = sum(c for q, c in ip_counts.items() if q >= 0)
    events["dot>0"] = sum(c for q, c in ip_counts.items() if q > 0)
    events["dot<=0"] = sum(c for q, c in ip_counts.items() if q <= 0)
    events["dot<0"] = sum(c for q, c in ip_counts.items() if q < 0)
    events["dot>-2"] = sum(c for q, c in ip_counts.items() if q > -2)
    events["|dot|<=1"] = sum(c for q, c in ip_counts.items() if abs(q) <= 1)
    events["|dot|<2"] = sum(c for q, c in ip_counts.items() if abs(q) < 2)
    events["dot!=0"] = sum(c for q, c in ip_counts.items() if q != 0)

    # Pairwise unions/intersections of basic events
    basic_events = sorted(ip_counts.keys())
    for i, q1 in enumerate(basic_events):
        for q2 in basic_events[i+1:]:
            union_key = f"dot={q1} OR dot={q2}"
            events[union_key] = ip_counts[q1] + ip_counts[q2]

    event_probs: dict[str, float] = {
        name: count / n for name, count in events.items()
    }
    event_fractions: dict[str, str] = {
        name: str(Fraction(count, n)) for name, count in events.items()
    }

    # ── Step 3: Match against algebraic targets ──
    matches: dict[str, list[dict]] = {target_name: [] for target_name in TARGETS}
    for target_name, target_val in TARGETS.items():
        for event_name, prob in event_probs.items():
            if abs(prob - target_val) < 1e-10:
                matches[target_name].append({
                    "event": event_name,
                    "probability": prob,
                    "exact_fraction": event_fractions[event_name],
                    "match": "EXACT",
                })
            elif abs(prob - target_val) < 0.01:
                matches[target_name].append({
                    "event": event_name,
                    "probability": prob,
                    "exact_fraction": event_fractions[event_name],
                    "delta": prob - target_val,
                    "match": "NEAR (within 0.01)",
                })

    # ── Step 4: Balanced ternary structure analysis ──
    # E8 root system facts relevant to the ternary base hypothesis:
    # - 240 roots, inner products in {-2,-1,0,1,2} — a 5-valued (balanced quinary on Z) structure
    # - But restricted to {-1,0,+1} for the half-integer family (128 roots)
    # - The ±2 family (112 roots) uses {-2,0,+2} — balanced ternary × 2
    half_int_roots = [r for r in roots if all(abs(x) == 1 for x in r)]
    coord_roots = [r for r in roots if any(abs(x) == 2 for x in r)]

    # Inner product distribution within each family
    half_half_ips: Counter[Fraction] = Counter()
    for beta in half_int_roots:
        half_half_ips[dot(alpha0 if alpha0 in half_int_roots else half_int_roots[0], beta)] += 1

    coord_alpha = coord_roots[0]
    coord_coord_ips: Counter[Fraction] = Counter()
    for beta in coord_roots:
        coord_coord_ips[dot(coord_alpha, beta)] += 1

    # Cross-family inner products
    cross_ips: Counter[Fraction] = Counter()
    for beta in coord_roots:
        cross_ips[dot(half_int_roots[0], beta)] += 1

    # ── Step 5: Sovereign ceiling check at each candidate θ ──
    ceiling_analysis = {}
    for target_name, target_val in TARGETS.items():
        if 0 < target_val < 1:
            chi_s = math.sqrt(target_val * (2 - target_val))
            chi_s_sq = target_val * (2 - target_val)
            ceiling_analysis[target_name] = {
                "theta": target_val,
                "chi_s_squared": chi_s_sq,
                "chi_s": chi_s,
                "chi_s_interpretation": "sqrt(2θ - θ²) = √(1-(1-θ)²) = sovereign ceiling if θ is gate probability",
                "near_known_values": {
                    "Thorne_0.998": abs(chi_s - 0.998),
                    "sqrt(3)/2": abs(chi_s - math.sqrt(3)/2),
                    "0.9539": abs(chi_s - 0.9539),
                    "0.953": abs(chi_s - 0.953),
                }
            }

    # ── Step 6: Key structural numbers ──
    # 240 = 2⁴ × 3 × 5
    # |W(E8)| = 696729600 = 2¹⁴ × 3⁵ × 5² × 7
    # 57600 = 2⁷ × 3² × 5²  (order of W(E6))
    # Balanced ternary: {-1, 0, +1} — the natural E8 half-integer coordinate alphabet
    structural_numbers = {
        "240_factorization": "2^4 × 3 × 5",
        "weyl_order": 696729600,
        "weyl_factorization": "2^14 × 3^5 × 5^2 × 7",
        "E6_weyl_order": 51840,
        "E6_weyl_factorization": "2^7 × 3^4 × 5",
        "E7_weyl_order": 2903040,
        "E7_weyl_factorization": "2^10 × 3^4 × 5 × 7",
        "half_integer_roots_count": len(half_int_roots),
        "coordinate_roots_count": len(coord_roots),
        "128_factorization": "2^7 (half-spinor rep of Spin(16))",
        "112_factorization": "2^4 × 7 = 16 × 7 (adjoint coordinates)",
        "ratio_128_to_240": float(Fraction(128, 240)),
        "ratio_112_to_240": float(Fraction(112, 240)),
        "balanced_ternary_note": "The 128 half-integer roots use coordinates in {-1,0,+1} — balanced ternary alphabet. This is the natural digitization of E8 spinor weights.",
    }

    result = {
        "model_id": "C1",
        "gate_route": "E8 algebraic-number sweep with 1/√2 correction",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "root_count": n,
        "inner_product_support": [str(q) for q in sorted(ip_counts.keys())],
        "inner_product_counts": {str(q): c for q, c in sorted(ip_counts.items())},
        "inner_product_probabilities": ip_probs,
        "all_natural_event_probabilities": {k: f"{v:.10f}" for k, v in sorted(event_probs.items(), key=lambda x: x[1])},
        "all_natural_event_fractions": event_fractions,
        "target_matches": matches,
        "ceiling_analysis": ceiling_analysis,
        "family_structure": {
            "half_integer_128": {
                "count": len(half_int_roots),
                "example": list(half_int_roots[0]),
                "inner_products_from_own_family": {str(q): c for q, c in sorted(half_half_ips.items())},
            },
            "coordinate_112": {
                "count": len(coord_roots),
                "example": list(coord_roots[0]),
                "inner_products_from_own_family": {str(q): c for q, c in sorted(coord_coord_ips.items())},
            },
            "cross_family": {str(q): c for q, c in sorted(cross_ips.items())},
        },
        "structural_numbers": structural_numbers,
        "balanced_ternary_analysis": {
            "e8_uses_balanced_ternary": True,
            "alphabet": "{-1, 0, +1}",
            "where": "128 half-integer (spinor) roots; coordinates ∈ {±1}^8 with even parity = balanced ternary without zero",
            "note": "The 112 coordinate roots use {-2, 0, +2} = 2 × balanced ternary. The FULL E8 coordinate alphabet is thus {-2, -1, 0, +1, +2} — balanced quinary, or equivalently balanced ternary at two scales.",
        },
        "script_hash": sha256(Path(__file__)),
    }

    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    # Print summary
    print("=" * 70)
    print("E8 ALGEBRAIC-NUMBER SWEEP RESULTS")
    print("=" * 70)
    print(f"\nRoot count: {n}")
    print(f"Inner products: {[str(q) for q in sorted(ip_counts.keys())]}")
    print(f"Counts per inner product: {dict(sorted(ip_counts.items()))}")
    print()
    print("NATURAL EVENT PROBABILITIES (unique values):")
    seen = set()
    for name, prob in sorted(event_probs.items(), key=lambda x: x[1]):
        frac = event_fractions[name]
        if frac not in seen:
            seen.add(frac)
            print(f"  {prob:.6f} = {frac:>8s}  ← {name}")
    print()
    for target_name, target_val in sorted(TARGETS.items()):
        hits = matches[target_name]
        status = "EXACT MATCH" if any(h["match"] == "EXACT" for h in hits) else (
            f"NEAR ({len(hits)})" if hits else "NO MATCH"
        )
        print(f"  {target_name:>35s} = {target_val:.10f}  →  {status}")
        for h in hits:
            print(f"    {h['match']:>10s}: {h['event']} = {h['probability']:.10f}")
    print()
    print("SOVEREIGN CEILING χ_s = √(2θ−θ²) at each candidate θ:")
    for name, info in sorted(ceiling_analysis.items()):
        print(f"  θ = {name}: χ_s = {info['chi_s']:.10f}")
        for ref, delta in info["near_known_values"].items():
            if delta < 0.05:
                print(f"    → {ref}: Δ = {delta:.6f}")
    print()
    print(f"Balanced ternary: 128 spinor roots use {{±1}}^8 (even parity)")
    print(f"                  112 coordinate roots use {{±2, 0}}^8")
    print(f"                  Full E8 alphabet = balanced quinary {{-2,-1,0,+1,+2}}")


if __name__ == "__main__":
    main()
