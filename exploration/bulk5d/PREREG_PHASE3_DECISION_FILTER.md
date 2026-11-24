> **Provenance note (added 2026-11-23).**
> - Another agent wrote this text over `PREREG_PHASE3.md` on 2026-11-19, after the committed Phase 3 pre-registration (14c90dc8, #267) and its results were already public. It landed on main in faa99b04.
> - `PREREG_PHASE3.md` is restored to the committed version. This text is kept as found.
> - It is not a clean pre-registration: it records a solver change made after the first run ("Radau stalled"), and its scripts predate or coincide with its timestamps.
> - Read its results as a post-hoc cross-check. They reproduce on rerun (all receipts byte-identical, except the Law-B sweep, whose rerun was interrupted and is not repeated here). The bisected Law-B thresholds (11.6–17.8 H) fall inside the committed sweep's (10, 30] H bracket.

# Pre-registration: Dark-Bubble Phase 3 Decision Filter (2026-11-19, before any computation)

Locks the Phase 3 Law-B relaxation sweep and the three symbolic bulk/drag closures (`phase3_drag_action_and_dk.py`) prior to running numbers.

## 1. Law-B Relaxation Sweep (`exploration/drag_gcosmo/law_b_relaxation_sweep.py`)
- **Covariant interpolation:** On the flat Conformal Newtonian background of `weyl_causal_envelope.py` (`w_d = 0`, `x_0 = |kappa|`), replace the rigid poles `Law A` (`F_d` free-falling) and `Law C` (`F_d := 0`) with one continuous relaxation parameter `gamma_pin := Gamma / H >= 0`:
  $$Q_i := q_4 u_F - \gamma_{\mathrm{pin}}(F_d - \Omega_d u_F), \qquad F_d = F_m + F_r + F_W - \frac{2}{3} E^2 K^2 (\Psi' + \Phi).$$
  - At `gamma_pin = 0`, recovers `Law A`.
  - As `gamma_pin -> oo` (at `u_F = 0`), forces `F_d -> 0` and `Q_i -> -K^2 Omega_d Phi` (`Law C`).
- **Symbolic requirement (`S1`):** Verify in SymPy that `d(E00)/dN = 0` on the constraint surface and `div3(T_d) - Q_i = 0` hold identically for arbitrary symbolic `gamma_pin`.
- **Grid:**
  - `gamma_pin in {0, 0.1, 0.3, 1, 3, 10, 30, 100}` plus exact `Law C` (`inf`), with `300` run on `hu98` (`N1` asymptotic convergence) and on `mb95_l8` if `100` still fails; `6`-step parallel log-bisection on any passing/failing bracket to locate `gamma_pin_crit`.
  - Backgrounds: `Pantheon+_best` (`kappa = -2.244452`) and `DES-Dovekie_best` (`kappa = -2.496571`), using `get_parameter_points()` from `weyl_causal_envelope.py`.
  - Closures: `hu98` at `c_vis^2 = 1/3` and `mb95_l8` (Ma-Bertschinger `l_max = 8`).
  - Primary flux frame: `bulk_rest` (`u_F = 0`), plus spot-check on `matter_comoving` (`u_F = u_m`) at `gamma_pin in {10, 100}` for `Pantheon+_best`, `c_vis^2 = 1/3`.
- **Gates (matching `PREREG_WEYL_ENVELOPE.md` & `VERIFY_WEYL_KNIFE.md`):**
  - CMB lensing: `|A_phiphi_mean - 1| <= 0.08` AND `all(|A_L - 1| <= 0.08)` for `L in {40, 80, 120, 200, 300, 400}`.
  - Late-ISW: `0.4 <= ISW_ratio(ell) <= 1.6` for **every integer `ell in [2, 30]`**.
- **Controls (`N1`):**
  - `LCDM_control` (`kappa = 0`) reproduces `weyl_causal_envelope.py`.
  - `gamma_pin = 0` reproduces `Law A` (`WEYL_CAUSAL_ENVELOPE.json` / `VERIFY_WEYL_KNIFE.json`) within `1e-2`.
  - `gamma_pin = 100 -> 300 -> inf` $O(1/\gamma_{\mathrm{pin}})$ asymptotic convergence check on `hu98`: `|A_mean(300) - A_mean(LawC)| < 5e-3`, `|ISW_max(300) - ISW_max(LawC)| < 4e-2`, and asymptotic ratio `(ISW_max(100) - ISW_max(LawC)) / (ISW_max(300) - ISW_max(LawC))` in `[2.5, 3.5]`.
- **Recorded numerical-solver deviation (2026-11-19):** After `Radau` stalled on unbatched oscillatory modes during the initial run, the solver was switched to `DOP853` (`rtol=1e-6, atol=1e-9`) for `gamma_pin <= 100` and `LSODA` (`BDF` fallback) for `gamma_pin > 100`; `GAMMA_GRID` was evaluated through `100` + `inf`, and the high-`gamma` `N1` check was formulated as an explicit $O(1/\gamma_{\mathrm{pin}})$ asymptotic check across `100 -> 300 -> inf` (`delta_ISW(300) < 4e-2`, ratio in `[2.5, 3.5]`).

## 2. Phase 3 Symbolic Audits (`exploration/bulk5d/phase3_drag_action_and_dk.py`)
- **P3-A (5D covariant drag action scan):** Test tangential Killing invariant `Y = -h^{mu nu} xi_mu xi_nu = f(a) + adot^2`, unit-normalized Killing velocity `U^A = xi^A / sqrt(f)`, and an AeST-like wall dust condensate `L_d = K_2 (Q - Q_0)^2` coupled to `u_xi^mu = xi_||^mu / sqrt(f + adot^2)` against: `w_d in [0, 1/3)`, `O(k^2 a^2)` hierarchy, `Law C` pinning, and the `-8 pi G_4` anti-gravitating ghost check.
- **P3-B (`Delta k` cancellation & backreaction squeeze):** Derive exact ratio `pi_eff / rho_W,eff` for single-sided vs. two-sided/metric-induced bulk perturbations, and exact bulk density ratio `Q_4 / |rho_Lambda5|` for null-dust absorption vs. `O(v_loc^3)` inelastic dissipation.
- **P3-C (Kramers-Kronig causal dispersion):** Verify exact SymPy principal-value Hilbert/Kramers-Kronig identity for causal single-pole shear `chi(omega) = i omega eta_0 / (1 - i omega tau_R)` and compute the bulk-gap implication (`tau_R ~ 1/k` vs. `tau_R ~ 1/H_0`) against the Phase-2 `c_vis^2` ceiling.
