# Pre-registration: Phase 3, a mechanism search for the drag perturbation law (2026-11-19, before any Phase 3 number)

**Status and scope.** This is a new phase. It searches for 5D mechanisms, with kill gates fixed in advance.
- It cannot change Phase 2's conditional verdict (#264, corrected in #266).
- Any mechanism it finds stays `[O]` until its own gates pass.
- The flux source's state stays a model input whatever this phase finds.
- Prompted by a Muse "7-Muses" brainstorm. Its claims are re-derived here, not imported.

**Known before any run (from committed results).**
- At c_vis² = 0, Law A and Law C give identical numbers. A pinning sweep there measures nothing.
- Law C (F_d = 0) passes Pantheon+ at every c_vis² and DES-Dovekie only at c_vis² ≥ 0.1.
- Law A passes Pantheon+ only for c_vis² ≲ 1.5–5.5×10⁻⁴ and never passes DES-Dovekie.
- The question is therefore how strong the pinning must be, and whether any covariant mechanism supplies it.

## Test L: Law-B pinning sweep (`law_b_relaxation_sweep.py`)
- **Model.** The envelope's Law A equations plus a drag-momentum relaxation at rate γ per e-fold, with the dark-bubble sign (P0: the Weyl fluid gains what the wall gains). Concretely, F_W′ → F_W′ − γF_d, with F_d = F_m + F_r + F_W − (2/3)E²K²(Ψ′ + Φ) taken from the 0i constraint.
  - γ = 0 is Law A.
  - γ → ∞ forces F_d → 0 and turns the F_W equation into Law C's.
- **Grid.**
  - γ ∈ {0, 0.3, 1, 3, 10, 30, 100, 300, 1000};
  - closures: Hu c_vis² ∈ {0.1, 1/3} and `mb95_l8`;
  - fits: the Pantheon+ and DES-Dovekie best fits;
  - w_d = 0, bulk-rest flux frame, adiabatic initial conditions;
  - 25 k-modes, every integer ℓ ∈ [2, 30];
  - the pre-registered gates: |A_φφ − 1| ≤ 0.08, ISW ratio in [0.4, 1.6].
- **Controls (the run is void if either fails).**
  - γ = 0 reproduces the committed Law A numbers in `WEYL_CAUSAL_ENVELOPE.json` (ISW max and A_φφ mean to 10⁻³ relative).
  - γ = 1000 reproduces the committed Law C numbers to 1%.
- **Outputs.**
  - The smallest passing γ, γ_crit, for each (fit, closure).
  - Whether any single (γ, closure) passes both best fits.

## Test S: covariant drag-action scan (`phase3_drag_action_scan.py`, SymPy)
**Candidates.**
- **(i) Tangential Killing coupling.** A wall Lagrangian L(Y, r) with Y ≡ −h^{μν}ξ_μξ_ν = f(r) + X (bulk static Killing ξ; X = (ξ·n)²), including L = Λ(r) + ½M(r)(Y − f(r))².
- **(iii) Static bulk medium with friction.** Q = Cρ_med(r)v³, with v = ȧ/√f.
- **(ii) Radial string-forest pinning.** Recorded as **not tested**: no concrete action is specified.

**Pass criteria, all required.**
1. w_d ∈ [0, 1/3) for the ȧ²-dependent piece.
2. A single-sign Q₄ > 0 across z ∈ [0, 10] on the fitted background.
3. No unsuppressed O(k²a²) term. Y = f + X is dominated by f ~ k²a².
4. It reproduces the fitted energy equation ΔΣ̇ + 3HΔΣ = Q₄ with ΔΣ ∝ a²H². Failing that, it is a different model and needs its own pre-registered refit.
5. Its momentum law: free-falling (Law A), pinned (Law C), or neither.
6. Ghost / gradient stability given the −8πG₄ wall sign: stated as tested or **not tested**.

**Not claimed by this test.** Preferred-frame bounds (α₁, α₂) are a later gate. A null result reads "none of the tested candidates".

## Not in this phase
- The modern lensing gate (Planck PR4 + ACT DR6) gets its own pre-registration. It does not reopen the ±8% verdict already recorded.
