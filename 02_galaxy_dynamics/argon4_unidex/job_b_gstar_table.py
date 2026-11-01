#!/usr/bin/env python3
"""
Job B — g_* as a conditional table.

Computes relativistic degrees of freedom for three stated contents:
  Row 1: Photons, 3 LH neutrino species, electrons and positrons.
  Row 2: Imported 1-generation Weyl list copied 3 times, plus gluons, W, Z, photon, Higgs.
         (Hot early universe assumption above electroweak scale, not a seam result).
  Row 3: Blank seam row (g_star_seam null, tier O, because seam has not fixed
         temperature relative to symbolic mass).

Standard spin weights applied:
  - Real scalar: 1
  - Massless vector: 2
  - Weyl fermion: 7/8 of a real bosonic degree (2 helicity states per Weyl field)
  - Higgs: 4 real scalars above electroweak symmetry breaking scale

Outputs job_b_gstar_table.json and prints receipt JSON. Exits 0.
"""

from fractions import Fraction
import json
from pathlib import Path
import sys


def compute_gstar_table():
    # -------------------------------------------------------------------------
    # Row 1: Low-temperature relativistic content
    # Content: Photons, 3 LH neutrino species, electrons and positrons
    # Assumption: Standard cosmology below muon threshold and above e+e- annihilation
    # -------------------------------------------------------------------------
    row_1_content = "Photons, 3 LH neutrino species, electrons and positrons"
    row_1_assumption = "Standard cosmology below muon threshold and above electron-positron annihilation"

    # Bosons:
    # Photon: 1 massless vector gauge boson with 2 transverse polarizations
    photon_vectors = 1
    vector_spin_states = 2
    row_1_bosonic_dof = photon_vectors * vector_spin_states  # 2

    # Fermions:
    # 3 LH neutrino species: 3 Weyl fermions with 2 states each (particle + antiparticle)
    nu_species = 3
    weyl_states = 2
    nu_fermionic_dof = nu_species * weyl_states  # 6

    # Electrons and positrons: 1 Dirac charged lepton (4 states: 2 spin x particle/antiparticle)
    electron_particles = 1
    dirac_states = 4
    electron_fermionic_dof = electron_particles * dirac_states  # 4

    row_1_fermionic_dof = nu_fermionic_dof + electron_fermionic_dof  # 10

    # Arithmetic:
    # g_* = g_b + (7/8) * g_f
    row_1_fermion_weight = Fraction(7, 8)
    row_1_g_star_frac = Fraction(row_1_bosonic_dof, 1) + row_1_fermion_weight * Fraction(row_1_fermionic_dof, 1)
    row_1_g_star = float(row_1_g_star_frac)  # 2 + 0.875 * 10 = 10.75

    row_1 = {
        "row_id": 1,
        "content": row_1_content,
        "assumption": row_1_assumption,
        "attached_to_seam": False,
        "tier": "C",
        "bosonic_dof": row_1_bosonic_dof,
        "fermionic_dof": row_1_fermionic_dof,
        "g_star": row_1_g_star,
        "g_star_fraction": str(row_1_g_star_frac),
        "arithmetic_detail": f"{row_1_bosonic_dof} + (7/8) * {row_1_fermionic_dof} = {row_1_g_star}",
    }

    # -------------------------------------------------------------------------
    # Row 2: Hot early universe Standard Model content
    # Content: Imported 1-generation Weyl list copied 3 times, plus gluons, W, Z, photon, Higgs
    # Assumption: Hot early universe above electroweak scale (unbroken gauge symmetry), not a seam result
    # -------------------------------------------------------------------------
    row_2_content = "Imported 1-generation Weyl list copied 3 times, plus gluons, W, Z, photon, Higgs"
    row_2_assumption = "Hot early universe above electroweak scale (unbroken gauge symmetry), not a seam result"

    # Imported Weyl fermions per generation from IMPORTED_STANDARD_MODEL.md:
    # q  : SU(3)=3, Weak mult=2 -> 3 * 2 = 6 Weyl fields
    # u^c: SU(3)=3, Weak mult=1 -> 3 * 1 = 3 Weyl fields
    # d^c: SU(3)=3, Weak mult=1 -> 3 * 1 = 3 Weyl fields
    # ell: SU(3)=1, Weak mult=2 -> 1 * 2 = 2 Weyl fields
    # e^c: SU(3)=1, Weak mult=1 -> 1 * 1 = 1 Weyl field
    weyl_list_gen1 = [
        {"field": "q", "su3_mult": 3, "weak_mult": 2},
        {"field": "u^c", "su3_mult": 3, "weak_mult": 1},
        {"field": "d^c", "su3_mult": 3, "weak_mult": 1},
        {"field": "ell", "su3_mult": 1, "weak_mult": 2},
        {"field": "e^c", "su3_mult": 1, "weak_mult": 1},
    ]

    weyl_fields_per_gen = sum(f["su3_mult"] * f["weak_mult"] for f in weyl_list_gen1)  # 15
    generations = 3
    total_weyl_fields = weyl_fields_per_gen * generations  # 45

    # Each Weyl field accounts for 2 states (particle & antiparticle helicities in textbook count)
    row_2_fermionic_dof = total_weyl_fields * weyl_states  # 45 * 2 = 90

    # Bosons:
    # Gluons: SU(3)_c adjoint representation, 8 gauge vectors * 2 polarizations
    gluon_vectors = 8
    gluon_bosonic_dof = gluon_vectors * vector_spin_states  # 16

    # Electroweak gauge vectors: unbroken SU(2)_L x U(1)_Y has 3 + 1 = 4 gauge vectors * 2 polarizations
    # (corresponds to W+, W-, Z, photon in broken phase)
    ew_vectors = 4
    ew_bosonic_dof = ew_vectors * vector_spin_states  # 8

    # Higgs: Complex SU(2)_L doublet = 4 real scalar degrees of freedom above electroweak scale
    higgs_real_scalars = 4
    higgs_bosonic_dof = higgs_real_scalars * 1  # 4

    row_2_bosonic_dof = gluon_bosonic_dof + ew_bosonic_dof + higgs_bosonic_dof  # 16 + 8 + 4 = 28

    # Arithmetic:
    # g_* = g_b + (7/8) * g_f
    row_2_fermion_weight = Fraction(7, 8)
    row_2_g_star_frac = Fraction(row_2_bosonic_dof, 1) + row_2_fermion_weight * Fraction(row_2_fermionic_dof, 1)
    row_2_g_star = float(row_2_g_star_frac)  # 28 + 0.875 * 90 = 28 + 78.75 = 106.75

    row_2 = {
        "row_id": 2,
        "content": row_2_content,
        "assumption": row_2_assumption,
        "attached_to_seam": False,
        "tier": "C",
        "bosonic_dof": row_2_bosonic_dof,
        "fermionic_dof": row_2_fermionic_dof,
        "g_star": row_2_g_star,
        "g_star_fraction": str(row_2_g_star_frac),
        "arithmetic_detail": f"{row_2_bosonic_dof} + (7/8) * {row_2_fermionic_dof} = {row_2_g_star}",
    }

    # -------------------------------------------------------------------------
    # Row 3: Blank seam row
    # Content: Seam production degrees of freedom
    # Reason: Seam has not fixed temperature relative to symbolic mass
    # -------------------------------------------------------------------------
    row_3_content = "Blank seam row: seam relativistic degrees of freedom"
    row_3_assumption = "Seam has not fixed temperature relative to symbolic mass"

    row_3 = {
        "row_id": 3,
        "content": row_3_content,
        "assumption": row_3_assumption,
        "attached_to_seam": True,
        "tier": "O",
        "bosonic_dof": None,
        "fermionic_dof": None,
        "g_star": None,
        "g_star_seam": None,
        "arithmetic_detail": "unfixed: temperature relative to symbolic mass is open",
    }

    # -------------------------------------------------------------------------
    # Assemble Receipt Object
    # -------------------------------------------------------------------------
    receipt = {
        "job": "B",
        "exit_code": 0,
        "verdict": "gstar_conditional_table_evaluated",
        "tier": "C",
        "neighbor_constrained": "which species list is allowed to enter later count",
        "neighbor_forbidden": "seam yield, seam mass, hypercharges",
        "free_symbols": [
            "g_star_seam",
            "T_seam",
        ],
        "numeric_outputs": {
            "row_1_bosonic_dof": row_1_bosonic_dof,
            "row_1_fermionic_dof": row_1_fermionic_dof,
            "row_1_g_star": row_1_g_star,
            "row_2_bosonic_dof": row_2_bosonic_dof,
            "row_2_fermionic_dof": row_2_fermionic_dof,
            "row_2_g_star": row_2_g_star,
        },
        "script": "job_b_gstar_table.py",
        "rows": [row_1, row_2, row_3],
    }

    return receipt


def main():
    receipt = compute_gstar_table()

    # Determine output path relative to this script
    script_dir = Path(__file__).resolve().parent
    output_path = script_dir / "job_b_gstar_table.json"

    # Serialize JSON with formatting
    json_text = json.dumps(receipt, indent=2)

    # Write receipt to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json_text + "\n")

    # Print receipt to stdout
    print(json_text)

    sys.exit(0)


if __name__ == "__main__":
    main()
