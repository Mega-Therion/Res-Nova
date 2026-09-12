# PREREG_D5_MG_EVOLUTION.md — Pre-Registered Protocol for D5 Closure
**Frozen: 2026-09-10 (before any simulation run). Author: Mega Therion (owner) / Eshdath (agent).**

## 1. Target

Open item `CLM-D5-03` (CLAIM_EVIDENCE_LEDGER_v1.6.0_SUPPLEMENT.md):
"Non-linear structure formation in RMOND is consistent" — currently `[O]`:
"Requires N-body (Thomas et al. 2023 framework)".

This protocol lifts it to `[D]` **within the parametrised modified-gravity
framework of Hassani & Lombriser (arXiv:2003.05927, MG-evolution)**, which the
authors validated at percent level against exact model-specific N-body for the
Vainshtein class (nDGP, their Sec. 3.3) — the same screening class as Res-Nova's
RMOND embedding (suppressed response `(r/r_MOND)^{3/2}`, manuscript "Vainshtein
screening" section; nDGP's screened limit is `(r*/r)^{3/2}`, their Eq. 22/25).

**What this can and cannot prove.** No exact model-specific Res-Nova N-body code
exists (it would require solving the full Skordis–Złośnik dual-channel scalar in
an N-body code). Closure here means: within the only parametrised framework
validated for Vainshtein-class screening, the non-linear regime does not amplify
the 0.23% linear enhancement into a catastrophe (the νHDM-style >5σ overproduction
failure reported by Russell et al. 2026), and the measured non-linear response is
consistent with the linear-theory prediction. This is an `[D]`-grade empirical
consistency statement, not `[P]`. It cannot rule out effects the parametrisation
does not capture.

## 2. Frozen inputs (do not change after this file is committed)

All numerical inputs are in `../derivation/D5_MG_PARAMETERS.json` (SHA-256 of the
derivation script embedded there). Summary:

- Parametrised coupling (their Eq. 8): `G_eff_tilde(a,k)/G = 1 + eps(a)·F_tilde(k)`
- `eps(a) = 1/(2·x(a)²·(1+x(a)))`, `x(a) = x0·sqrt(alpha)·E(a)`, `x0 = 5.67`
  (manuscript-frozen; `F''/F' = 1/(2x²(1+x))` is the Lean-certified identity in
  `CovariantCompletion.lean`, sympy-verified in the derivation script).
- **Arm A (the theory):** `alpha = 1` → `eps(z=0) = 0.002332`, `eps(z=1) = 0.000446`.
- **Arm B (negative control — code sensitivity, NOT a theory claim):**
  `alpha = 0.01` → deep-MOND branch, `eps(z=0) ≈ 0.99`, late-time only.
- **Screening:** `af = 3`, `b = 2` (Vainshtein class, the nDGP cast of their
  Eq. 27), `k0(a) = a·h/r_MOND` with `r_MOND = sqrt(G·M_th/a0) = 0.4743 Mpc`
  physical, from the effective top-hat convention `r_th = 7 Mpc/h` comoving
  (their Sec. 3.2 convention) → **k0(z=0) = 1.434 h/Mpc** (inside the fitted
  nDGP range k* = 0.9–2.7 h/Mpc; a sensitivity band k0 ∈ [0.7, 2.9] h/Mpc is
  reported alongside).
- Cosmology: gevolution shipped `class_tk.dat` (h = 0.68, Ω_m = 0.3071,
  A_s = 2.085e-9, n_s = 0.9645), z_init = 100, identical seeds for all arms.

## 3. Frozen predictions (linear theory, from the growth ODE)

| Arm | ΔP/P at z=0 | ΔP/P at z=1 |
|---|---|---|
| A (alpha=1) | +0.00036 (+0.036%) | +0.00005 (+0.005%) |
| B (alpha=0.01) | +0.20365 (+20.4%) | +0.03278 (+3.3%) |

## 4. Simulation protocol

Code: Newtonian gevolution (particle-mesh), Poisson equation solved in Fourier
space, patched so the effective coupling multiplies the Poisson kernel per
Hassani & Lombriser Sec. 2.4: `G_eff_tilde(a,k)` evaluated at each timestep and
each grid mode. Patch unit-tested against `G_eff_tilde` directly (max relative
kernel error < 1e-10).

Runs (identical ICs, same seed, same phases):
1. **ΛCDM baseline** (unpatched gevolution),
2. **Arm A** (alpha=1),
3. **Arm B** (alpha=0.01).

Configurations:
- **Validation config (paper-matching):** N_pcl = 256³, L = 200 Mpc/h,
  N_grid = 256³, outputs z = 0 and z = 1, k ∈ [0.05, 2.5] h/Mpc. This is the
  Hassani–Lombriser validation ladder.
- **Sanity config (reduced, for compute-constrained environments):** smaller
  N_pcl/N_grid and/or box, same outputs and k-range (truncated at the box
  Nyquist limit). Any reduced-resolution result is labelled "reduced-resolution
  pipeline validation" and does NOT substitute for the validation config.

## 5. Verdict rules (frozen before the runs)

Compute `ΔP/P = P_arm/P_ΛCDM − 1` at z = 0 and z = 1 over k ∈ [0.05, 2.5] h/Mpc.

**V0 — Patch correctness (gate):** the patched Poisson kernel equals
`G_eff_tilde(a,k)` to < 1e-10 relative at all sampled (a,k). If V0 fails: ABORT.

**V1 — Pipeline sensitivity (negative control):** Arm B must show
`ΔP/P ≥ +5%` at z=0 for k ≤ 0.2 h/Mpc. If not, the pipeline is insensitive or
broken → ABORT; no D5 claim of any kind.

**V2 — Theory arm, primary verdict:**
- **CONSISTENT** iff for every k ∈ [0.05, 2.5] h/Mpc at z = 0 and z = 1:
  `|ΔP/P|_A ≤ max(2 × linear prediction at that (k,z), 1%)`.
- **TENSION** iff there exists any k with `|ΔP/P|_A > 5%` (νHDM-style blow-up:
  the non-linear regime amplifies the screened enhancement catastrophically).
- Anything between: **INCONCLUSIVE** — D5 stays open with the measured table.

**Reporting:** both arms' full ΔP/P tables, the exact configuration used, patch
diff, seeds, runtime, and the k0-sensitivity band. No smoothing beyond the
Gaussian σ = 2.5 mode convention of Hassani & Lombriser for figure-level
comparisons; verdict rules use raw spectra with identical ICs (their Sec. 3).

## 6. Epistemic outcome

- V2 = **CONSISTENT** at the validation config → `CLM-D5-03`: `[O] → [D]`
  ("consistent within the parametrised Vainshtein-class framework; non-linear
  amplification bounded"). D5's linear tcolorbox limit (i) in the manuscript is
  discharged; the D5 ledger entry updated with this protocol and its artifacts.
- CONSISTENT at the sanity config only → `[D]` withheld; D5 records
  "pipeline validated end-to-end at reduced resolution; full validation config
  preregistered and boundable (single command), pending compute".
- TENSION → D5 stays open, the obstruction is documented, and the manuscript's
  0.23% linear claim gains a non-linear caveat.

## 7. What must NOT happen

- No re-tuning of eps, k0, af, or b after seeing any run output.
- No claim of exact-model validation (no model-specific Res-Nova N-body exists).
- No abstract-level or manuscript-level claim from a sanity-config run.
- No silent scope change: any deviation from this protocol is versioned in the
  ledger as a new prereg with the reasons stated.
