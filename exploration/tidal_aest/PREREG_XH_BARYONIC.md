# Pre-registration: x_H from baryons, SPARC consistency and the cluster R₂₀₀ overshoot (2026-11-19, before any number)

**Issue found in review.** The tidal-AeST candidate screens the MOND (phantom) sector with S_lin = 1/(1 + (x_H,low/x_H)²), where x_H,low = 154 and x_H = ‖∇∇Φ_N‖/H². In a theory without dark matter, Φ_N is the **baryonic** Newtonian potential. But `xh_screen.py` computed SPARC's x_H from the *observed* rotation curve (V²/R), which is the total field. That overstates x_H in the MOND regime by up to ν ≈ 2–10.

**Test A (SPARC, decisive for the candidate).**
- Recompute x_H from g_bar = (V_gas|V_gas| + 0.5V_disk² + 0.7V_bul²)/R, using the tidal tensor of the baryonic field, √(g′² + 2(g/r)²) (spherical approximation, as before).
- Report the fraction of SPARC points with S_lin < 0.99 and < 0.5.
- **Candidate survives Test A** if ≤ 1% of points have S_lin < 0.99, matching the original claim.
- If it fails, report the largest x_H,low that keeps ≤ 1%, and whether linear growth still passes at that value (growth needs x_H,low ≥ 10).

**Test B (X-COP R₂₀₀ overshoot).**
- Apply S_lin(x_H,bar) to the MOND boost in the X-COP solve: g = u + S·(g_mond(u) − u). The AeST μ² dust term stays unscreened, since it is AeST's own sector.
- Use x_H,low = 154, or the Test-A-allowed value if A fails.
- Supply-capped. Same decision rule at R₅₀₀ and R₂₀₀: median ∈ [0.8, 1.25] and ≥ 9/12 in [0.7, 1.4].
