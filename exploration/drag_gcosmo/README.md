# Drag variable-G cosmology (Dark Bubble wall + bulk drag), 2026-11-19
Pre-registered in `PREREG.md` (commit 7c5908a, before any number). Fits: `drag_fit.py` → `DRAG_FIT.json`. Cross-checks: `drag_crosscheck.py` → `DRAG_CROSSCHECK.json`. Follow-ups: `followups.py` → `FOLLOWUPS.json`.

**Pre-registered verdict: favoured** (Δχ² ≤ −4 with fσ₈; x₀ = 0 outside 2σ).

| Data | Δχ² (drag − ΛCDM) | x₀ best | x₀ 2σ | G_cosmo/G_N today |
|---|---|---|---|---|
| BAO+SN+CMB | −6.54 | 0.32 | ≈0.07–0.72 | 0.76 (≈0.58–0.94) |
| + fσ₈, σ₈ anchored | −5.96 | 0.30 | 0.045–0.66 | 0.77 (0.60–0.96) |
| + fσ₈, amplitude free | −6.24 | 0.31 | 0.052–0.69 | 0.76 (0.59–0.95) |

**What the result means.**
- **The preference comes from BAO+SN.** fσ₈ is neutral to slightly against drag: its χ² changes by +0.53 (anchored) and +0.29 (free).
- **This is the known DESI DR2 + Pantheon+ evolving-dark-energy signal, absorbed by one parameter.** The same pipeline with CPL dark energy gives w₀ = −0.85, w_a = −0.57, Δχ² = −9.2 for two parameters. DESI DR2's DESI+CMB+Pantheon+ row is ≈ (−0.84, −0.62), recalled rather than re-fetched; the match validates the pipeline. Per parameter, drag and CPL are comparable (ΔAIC ≈ −4.5 vs −5.2).
- **It is not independent evidence for a bubble wall.**

**Wall-fluid consistency (Codazzi): the zero-flux wall is [X].**
- With no bulk energy flux, the drag tension fixes the wall's pressure. Its adiabatic sound speed is then c_s² = −4/3 − (1/3)·a·a⃛/(ȧ·ä), independent of σ₀ and ρ_b.
- At the best fit, c_s² = −1.49 (z = 0), −2.34 (z = 0.3) and −0.43 (z = 2). It lies in [0, 1] for only 6.6% of z < 10.
- That is a gradient instability.
- **The drag model survives only if energy flows across the wall (ΔT_rn ≠ 0).** That flux is then a new, unspecified ingredient [O].

**Limitations.**
- Compressed CMB (θ*, ω_m); no CMB lensing or ISW. Those are the hardest test of a 24% gap between G_cosmo and G_N.
- fσ₈ uses a diagonal covariance and no AP correction.
- Closed-bubble curvature is neglected.
- Not run: replacing Pantheon+ with DES-Dovekie, which would test whether the signal depends on the SN sample. This would be post-hoc.

**Status.**
- **Phenomenology:** the drag G_cosmo(a) fits as well as w₀w_a per parameter [E].
- **Physical realisation:** a closed (zero-flux) wall is unstable [X]; a flux-fed wall is [O].

## Post-hoc SN-sample check: DES-Dovekie in place of Pantheon+ (`dovekie_rerun.py` → `DOVEKIE_RERUN.json`)
- 1820 SNe, full inverse STAT+SYS covariance. Drag: Δχ² = **−8.72**, x₀ = 0.35 (2σ 0.10–0.72), G_cosmo/G_N today = 0.74. CPL: Δχ² = −12.46, w₀ = −0.81, w_a = −0.69.
- The drag preference **strengthens** with DES-Dovekie (Pantheon+ gave −6.54), as DESI's own dynamical-DE preference does across SN samples. The result does not hinge on the SN sample.
- DESI DR2's abstract (arXiv:2503.14738) confirms the favoured quadrant w₀ > −1, w_a < 0, which both of our CPL fits occupy. The exact table values were not re-fetched.
