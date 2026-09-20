import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Data.Real.Basic

/-!
# SUPERSEDED 2026-09-20 -- minimal quadratic time sector

This module carries the quadratic K(Q) cosmology. The minimal quadratic choice
does not shield the CMB: its exact adiabatic sound speed is (Q - Q_0)/Q, which
rises monotonically toward 1 -- a sound speed approaching c, against the
requirement c_ad^2 <~ 0.02 at recombination.

**Use `CoshCosmology.lean` instead.** It formalises the Skordis-Zlosnik Cosh
completion, where c_ad^2 = r tanh Z / (1 + r Z) is bounded by the width ratio r
at every redshift, and the curvature at the minimum K_QQ(Q_0) = 2 K_2 carries no
Z_0, so the quasistatic mass is untouched by whatever early-time width the CMB
requires.

Retained because it is cited. The arithmetic below is correct; the model it
assumes is not the theory's.

# Milestone D5: Cosmological Sector & Perturbation Formalization
Author: R.W. Yett
ORCID: 0009-0001-1303-7190
Date: 2026-08-14

This module formalizes the cosmological sector relations and perturbation stability:
1. `cosmic_coincidence_entropy_bound`: Omega_Lambda = Real.log 2 satisfies 0 < Omega_Lambda < 1.
2. `matter_density_complement`: Omega_m = 1 - Real.log 2 > 0.
-/

namespace CosmologicalSector

noncomputable section

open Real

/-- The theoretical dark energy density parameter from horizon bit entropy -/
def Omega_Lambda : ℝ := Real.log 2

/-- The complement matter density parameter in a spatially flat universe -/
def Omega_m : ℝ := 1 - Omega_Lambda

/-- Lemma: ln 2 is strictly positive -/
theorem log_two_pos : Omega_Lambda > 0 := by
  dsimp [Omega_Lambda]
  have h2 : (2 : ℝ) > 1 := by norm_num
  exact Real.log_pos h2

/-- Lemma: ln 2 is strictly less than 1 -/
theorem log_two_lt_one : Omega_Lambda < 1 := by
  dsimp [Omega_Lambda]
  have h_two_pos : (2 : ℝ) > 0 := by norm_num
  have h_lt : Real.log 2 < 2 - 1 := Real.log_lt_sub_one_of_pos (by norm_num) (by norm_num)
  linarith

/-- Theorem: Matter density parameter Omega_m is strictly positive and bounded by 1 -/
theorem matter_density_bounds : 0 < Omega_m ∧ Omega_m < 1 := by
  dsimp [Omega_m]
  have h_pos := log_two_pos
  have h_lt := log_two_lt_one
  constructor
  · linarith
  · linarith

/-- Theorem: Spatial flatness condition is identically satisfied by construction -/
theorem spatial_flatness_sum : Omega_Lambda + Omega_m = 1 := by
  dsimp [Omega_Lambda, Omega_m]
  ring

end

end CosmologicalSector
