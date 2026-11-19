/-
  CassiniSymmetronWindow.lean
  Formalizes the algebraic Cassini-SPARC symmetron screening window:
  any scale x = 2*M^2*lambda satisfying the lower galaxy bound (x >= 99 * rho_gal)
  and the upper scale bound (7413 * x + 10000 * rho_gal <= 2587 * rho_odot), which gives
  the Cassini bound 10000 * (x + rho_gal) <= 2587 * (x + rho_odot)
  simultaneously preserves galaxy rotation curves (>= 99%) and passes 2-sigma Cassini.

  [X] PHYSICAL PREMISE (2026-11-19): rho_odot here is the Sun's interior density, but Cassini measures the
  field at Saturn's orbit, where the density (~1.3e-22 kg/m^3) is below rho_gal. The algebra below is
  correct; the window it describes is not a physical window. See
  exploration/theory3_gate/symmetron_route.py and CURRENT_STATE (2026-11-19).
-/

namespace ResNova.CassiniSymmetronWindow

theorem galaxy_preservation_from_lower_bound
    (x rho_gal : Nat) (h_low : 99 * rho_gal ≤ x) :
    99 * (x + rho_gal) ≤ 100 * x := by
  omega

/-- The Cassini 2σ inequality follows from an explicit upper bound on the scale:
    `7413 x ≤ 2587 ρ_☉ − 10000 ρ_gal`. (Rewritten 2026-11-17: the earlier statement
    took the inequality itself as its hypothesis, which proves nothing.) -/
theorem cassini_2sigma_from_upper_bound
    (x rho_gal rho_odot : Nat)
    (h_up : 7413 * x + 10000 * rho_gal ≤ 2587 * rho_odot) :
    10000 * (x + rho_gal) ≤ 2587 * (x + rho_odot) := by
  omega

theorem window_nonempty_witness :
    let rho_gal : Nat := 1
    let rho_odot : Nat := 100000
    let x : Nat := 100
    99 * rho_gal ≤ x ∧ 10000 * (x + rho_gal) ≤ 2587 * (x + rho_odot) := by
  decide

def symmetronScale (lam M : Nat) : Nat := 2 * M * M * lam

theorem symmetron_window_from_lambda_M
    (lam M rho_gal rho_odot : Nat)
    (h_low : 99 * rho_gal ≤ symmetronScale lam M)
    (h_up : 7413 * symmetronScale lam M + 10000 * rho_gal ≤ 2587 * rho_odot) :
    99 * (symmetronScale lam M + rho_gal) ≤ 100 * symmetronScale lam M ∧
    10000 * (symmetronScale lam M + rho_gal) ≤
      2587 * (symmetronScale lam M + rho_odot) :=
  ⟨galaxy_preservation_from_lower_bound (symmetronScale lam M) rho_gal h_low,
   cassini_2sigma_from_upper_bound (symmetronScale lam M) rho_gal rho_odot h_up⟩

theorem symmetron_lambda_M_witness :
    let lam : Nat := 2
    let M : Nat := 5
    let rho_gal : Nat := 1
    let rho_odot : Nat := 100000
    99 * rho_gal ≤ symmetronScale lam M ∧
    10000 * (symmetronScale lam M + rho_gal) ≤
      2587 * (symmetronScale lam M + rho_odot) := by
  decide

/-- Bose–Mesner singlet-to-quadrupole VEV eigenvalue ratio μ₀ / μ₂ = 1920 / 384 = 5
    applied to the galactic-solar geometric-mean benchmark (in integer-cleared units of 10⁻²⁴ kg/m³:
    ρ_gal = 6702, ρ_☉,phot = 200000000000000000000, x_BM = 5 × 3072000000000000 = 15360000000000000)
    simultaneously satisfies both the strict SPARC galaxy bound (99 * ρ_gal ≤ x_BM) and the
    Cassini 2σ photosphere bound (10000 * (x_BM + ρ_gal) ≤ 2587 * (x_BM + ρ_☉,phot)). -/
theorem bose_mesner_vev_bridge_witness :
    let mu0 : Nat := 1920
    let mu2 : Nat := 384
    let ratio : Nat := mu0 / mu2
    let rho_gal : Nat := 6702
    let rho_odot_phot : Nat := 200000000000000000000
    let x_bm : Nat := ratio * 3072000000000000
    ratio = 5 ∧
    99 * rho_gal ≤ x_bm ∧
    10000 * (x_bm + rho_gal) ≤ 2587 * (x_bm + rho_odot_phot) := by
  decide

#print axioms galaxy_preservation_from_lower_bound
#print axioms cassini_2sigma_from_upper_bound
#print axioms window_nonempty_witness
#print axioms symmetron_window_from_lambda_M
#print axioms symmetron_lambda_M_witness
#print axioms bose_mesner_vev_bridge_witness

end ResNova.CassiniSymmetronWindow
