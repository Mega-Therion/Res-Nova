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

## Pre-registered 5D AdS-Vaidya Israel–Codazzi bulk-flux, NEC, and Weyl backreaction test (`PREREG_FLUX.md` a4db5e0b, `flux_codazzi_check.py` → `FLUX_CODAZZI.json`)

> **Read first (review note, 2026-11-19).** The surviving sub-conformal branch needs a large bare drag. At w_d = 0 the best fit is x₀ ≈ 2.24, so the bare G_cosmo/G_N today is 1/(1 + x₀) ≈ 0.31: a 69% bare mismatch, offset by Weyl dark radiation (Ω_Weyl(0) ≈ 1.75).
>
> This is a much stronger cancellation than the naive drag fit's 24%. The fit quality rests on that cancellation, and CMB lensing and ISW are where it would be tested.
>
> Independently reproduced: the rerun of `flux_codazzi_check.py` matches the committed `FLUX_CODAZZI.json`; see the PR.


**Symbolic `[D]` (SymPy exact 5D AdS-Vaidya + 4D Bianchi identity):**
- On flat-sliced 5D AdS-Vaidya $ds^2 = -f(r,v)\,dv^2 + 2\epsilon\,dv\,dr + r^2 d\mathbf{x}^2$, $f = k^2 r^2 - \mu(v)/r^2$, $R = -20 k^2$ and every component of $G_{AB} - 6 k^2 g_{AB}$ vanishes except $E_{vv} = \frac{3\epsilon}{2r^3}\dot{\mu}(v)$.
- By the 5D Null Energy Condition, both bulk-to-wall inflows ($\dot{\mu}_+ \ge 0$ from outside, $\dot{\mu}_- \le 0$ from inside) strictly increase the 4D Weyl dark-radiation density $\rho_{\mathrm{Weyl}} \propto (\mu_+/k_+ - \mu_-/k_-)/a^4$.
- For a barotropically stable wall drag fluid $P_{\mathrm{wall}} = -\Sigma_0 + w_d\,\Delta\Sigma_{\mathrm{drag}}$ ($c_s^2 = w_d \in [0, 1]$), the 4D Dark Bubble Bianchi identity forces the exact coupled Weyl backreaction
  $$\dot{\rho}_{\mathrm{Weyl}} + 4H\rho_{\mathrm{Weyl}} = \mathcal{Q}_4 = \dot{\Delta\Sigma} + 3(1+w_d)H\Delta\Sigma \quad \Longrightarrow \quad \frac{d}{dt}\!\left(a^4 \rho_{\mathrm{net}}\right) = (3 w_d - 1) a^4 H\,\Delta\Sigma_{\mathrm{drag}},$$
  where $\rho_{\mathrm{net}} \equiv \rho_{\mathrm{Weyl}} - \Delta\Sigma_{\mathrm{drag}}$. The exact coupled Friedmann system admits a closed-form integrating-factor solution depending on $(w_d, x_0)$ **only through the single combination $\kappa \equiv (3 w_d - 1) x_0$** (verified against DOP853 to `2.3e-13`).

**Three exact regimes across $w_d \in [0, 1]$ (`[D]`/`[E]`):**
- **$w_d = 1/3$ (conformal wall fluid): `[X]` exact cancellation.** $\kappa = 0$ identically; Weyl dark radiation cancels $\Delta\Sigma_{\mathrm{drag}}$ at all $z$, reducing $H(z)$ to exact $\Lambda$CDM ($\Delta\chi^2 = 0$).
- **$w_d \in (1/3, 1]$ (super-conformal): `[X]` sign-reversed anti-drag.** $\kappa = (3 w_d - 1) x_0 > 0$ overpowers drag and flips the sign; with $x_0 \ge 0$, best fit collapses to $x_0 = 0$ ($\Lambda$CDM).
- **$w_d \in [0, 1/3)$ (sub-conformal stable wall fluid, $0 \le c_s^2 < 1/3$): PRE-REGISTERED VERDICT `SURVIVES` (`[E]`/`[D]`).**

| Dataset (1 parameter $\kappa = (3 w_d - 1) x_0$) | $\Delta\chi^2$ (coupled − $\Lambda$CDM) | $\kappa$ best (2$\sigma$) | $x_0$ at $w_d = 0$ | $w_{\mathrm{eff}}(0) \to w_{\mathrm{eff}}(1)$ | Compare: naive drag / 2-param CPL |
|---|---:|---|---:|---|---|
| DESI DR2 + Pantheon+ + CMB | **−10.38** | −2.24 (−3.75, −0.83) | 2.24 | −0.88 → −1.15 | −6.54 / −9.17 |
| + $f\sigma_8$ (anchored) | **−8.55** | −2.00 (−3.46, −0.62) | 2.00 | −0.89 → −1.14 | −5.96 / — |
| + $f\sigma_8$ (free amp) | **−10.40** | −2.24 (−3.74, −0.83) | 2.24 | −0.88 → −1.15 | −6.24 / — |
| DESI DR2 + DES-Dovekie + CMB | **−12.74** | −2.50 (−3.99, −1.08) | 2.50 | −0.87 → −1.17 | −8.72 / −12.46 |

- **5D NEC & early universe:** Strictly positive bulk inflow $\mathcal{Q}_4(z) > 0$ for all $z \in [0, 10]$ ($\min s_{\mathrm{NEC}} = +0.996$), positive Weyl density $\Omega_{\mathrm{Weyl}}(z) \ge 1.24 > 0$, and negligible early dark radiation ($\Delta N_{\mathrm{eff}}(z_*) = 3.6\times 10^{-5}$ at $w_d = 0$, $\sim 10^{-18}$ at BBN).
- **Ghost-free effective phantom crossing:** The deceleration-to-acceleration turnover ($\ddot{a} = 0$) of $\Delta\Sigma_{\mathrm{drag}} \propto \dot{a}^2$ coupled to $\rho_{\mathrm{Weyl}}$ produces $w_{\mathrm{eff}}(z=1) = -1.15$ crossing $-1$ to $w_{\mathrm{eff}}(z=0) = -0.88$ with $0 \le c_s^2 < 1/3$ and zero NEC violation.
- **Honest limitations & sharpest remaining `[O]` kill-test:**
  1. Reproducing the signal after Weyl cancellation requires an $O(1)$ bare drag amplitude ($x_0 \approx 2.24$ at $w_d = 0$, with $\Omega_{\mathrm{Weyl}}(0) \approx 1.75$ partially cancelling $\Delta\Sigma_{\mathrm{drag}}(0) \approx 2.24$, so the effective dark-energy rewrite $\Omega_\Lambda + \Omega_{\mathrm{net}}$ turns negative for $z \gtrsim 2$ while $E(z)^2 > 0$ remains within $0.6\%$ of $\Lambda$CDM at $z = 10$).
  2. Like naive drag, this absorbs the DESI DR2 + SN evolving-DE signal rather than supplying independent evidence for a Dark Bubble.
  3. Linear growth used $G_{\mathrm{local}} = G_N$; full 5D perturbative clustering of $\rho_{\mathrm{Weyl}}$ + wall drag, CMB lensing, and ISW remain uncomputed `[O]` and are the decisive physical test of an $O(1)$ Weyl + drag sector.

## CMB-lensing and late-ISW proxies for the flux-fed wall (`PREREG_LENS_ISW.md`, `lens_isw_proxy.py` → `LENS_ISW_PROXY.json`)
Pre-registered before running. Computed at each dataset's best fit from the model's own background and growth.

| Fit | σ₈ | σ₈Ω_m^0.25 (Planck lensing 0.589 ± 0.020) | ΛCDM, same data | ISW ratio vs ΛCDM |
|---|---|---|---|---|
| Pantheon+ / BAO / CMB | 0.817 | 0.609 (+1.0σ) | 0.596 | 0.96 |
| + fσ₈ anchored | 0.815 | 0.606 (+0.9σ) | 0.595 | 0.97 |
| + fσ₈ free | 0.817 | 0.609 (+1.0σ) | 0.596 | 0.96 |
| DES-Dovekie / BAO / CMB | 0.819 | 0.611 (+1.1σ) | 0.596 | 0.96 |

**Verdict: survives both proxies** (lensing within 2σ, ISW within [0.4, 1.6]).
- Lensing sits about 0.7σ higher than ΛCDM's on the same data, a mild but real tilt.
- **These are proxies, not a Boltzmann calculation.** The lensing potential is assumed to be sourced by G_N ρ_m δ, and the lensing-kernel shift from the modified D_A(z) is ignored.
- The Weyl dark radiation's own perturbations (Ω_Weyl ≈ 1.75 today) are not modelled, and they are exactly where a full CMB lensing/ISW calculation could still break it. That remains [O].

## The large bare drag is a floor, not a fixable choice [D] (from `FLUX_CODAZZI.json`, no new fit)
> **Scope (2026-11-19, `exploration/bulk5d/`).** The floor assumes w_d ≥ 0, a sound-speed condition. The covariant velocity-dependent tension is a w = −1 component with no momentum, for which a sound speed means nothing. It is excluded only by `PREREG_FLUX.md`'s single-channel rule. The floor holds while that exclusion stands; without it the bare drag would be x₀ = |κ|/4.
The data constrain only κ = (3w_d − 1)x₀. On the stable sub-conformal branch 0 ≤ w_d < 1/3, x₀ = |κ|/(1 − 3w_d) ≥ |κ|, with the minimum at w_d = 0. Any w_d > 0 needs *more* drag, which diverges as w_d → 1/3.

| Fit | best x₀ (floor) | 2σ floor on x₀ | bare G_cosmo/G_N today, 1/(1 + x₀): best / 2σ upper |
|---|---|---|---|
| Pantheon+ / BAO / CMB | 2.24 | 0.83 | 0.31 / 0.55 |
| + fσ₈ anchored | 2.00 | 0.62 | 0.33 / 0.62 |
| + fσ₈ free | 2.24 | 0.83 | 0.31 / 0.55 |
| DES-Dovekie / BAO / CMB | 2.50 | 1.08 | 0.29 / 0.48 |

So within this model the bare drag cannot be brought below x₀ ≈ 0.6–1.1 at 2σ. Bare G_cosmo/G_N is at most about 0.5–0.6 today, offset by Weyl radiation. This is a property of the flux-fed branch, recorded as a derived floor. Whether the Weyl sector's perturbations tolerate it is the open Boltzmann question [O].

## Why the full Boltzmann test is blocked: a closure problem, not effort [C]
A full CMB lensing/ISW calculation needs the perturbations of the Weyl dark radiation (Ω_Weyl(0) ≈ 1.75). In braneworld cosmology the brane equations evolve the dark radiation's energy and momentum densities, "but there is no evolution equation for the dark radiative anisotropic stress" (Maartens & Koyama, *Brane-World Gravity*, Living Rev. Rel. 13, 5 (2010), arXiv:1004.3962, verified in the source text). Those nonlocal corrections "cannot be determined purely from data on the brane".

So any Boltzmann run that closes the Weyl sector on the brane, for example by setting its anisotropic stress to zero, imposes an assumption, not a prediction. The decisive test therefore needs the 5D bulk perturbations solved for this flux-fed AdS-Vaidya geometry. That is a research step [O], and the lensing/ISW proxies above are the most that brane-only data can claim.

Because Ω_Weyl here is O(1) and not a small correction, the undetermined anisotropic stress is expected to matter at leading order. This item should be treated as the flux branch's main vulnerability.

## Causal Weyl anisotropic-stress envelope (`PREREG_WEYL_ENVELOPE.md` 7ea3f668, `weyl_causal_envelope.py` → `WEYL_CAUSAL_ENVELOPE.json`)
Pre-registered before any numerical output. Rather than waiting on a full 1+1D 5D AdS-Vaidya bulk perturbation solver if all causal brane closures already fail, this brackets Hu (1998) causal Generalized Dark Matter closures ($c_s^2 = 1/3$, $c_{\mathrm{vis}}^2 \in \{0.0, 0.1, 1/3, 0.6, 1.0\}$) plus the exact Ma–Bertschinger (1995) $\ell_{\max} = 8$ free-streaming Boltzmann hierarchy (`mb95_l8` with Eq. 51 spherical-Bessel truncation) coupled to the exact linearized 4D Einstein + perturbed drag + Weyl-flux system across $k \in [10^{-4}, 0.2]\,\mathrm{Mpc}^{-1}$ (25 modes, $a_i = 10^{-3} \to 1$), computing exact Limber CMB lensing $A_{\phi\phi,\mathrm{eff}}(L)$ ($L \in \{40, 80, 120, 200, 300, 400\}$, Planck 2018 $3\sigma$ gate $|A - 1| \le 0.08$) and exact spherical-Bessel late-ISW $C_\ell^{\mathrm{ISW}}/C_\ell^{\mathrm{ISW}}(\Lambda\mathrm{CDM})$ ($\ell \in \{2, 5, 10, 20, 30\}$, $z \in [0, 5]$, gate $[0.4, 1.6]$).

1. **SymPy & numerical controls (`[D]`):**
   - Exact Conformal Newtonian gauge + contracted Bianchi identities verified symbolically (`S1`): exact $2 E^2 E'$, exact $\Lambda$CDM control ($\kappa = 0$, $k = 0.2$: $\Phi - \Psi = 0.0$, $E_{03}$ residual `1.21e-10`, late growth match `9.70e-6`, `REF_D1` match `1.15e-3`), and numerical `E33` consistency `4.31e-9` (`Pantheon+`, $k=0.05$).
   - **Bifurcation between the two exact covariant realizations of $\delta\theta = -3H(\Psi'+\Phi)$:**
     - **Formulation I (`Law C`, geometric zero-momentum wall drag $F_d \equiv 0 \implies Q_i = -K^2 \Omega_d \Phi$):** satisfies $d(E_{03})/dN = E_{33}$ identically in SymPy; the $-K^2 \Omega_d \Phi$ term cancels part of the Weyl photon pressure gradient and keeps free-streaming shear bounded.
     - **Formulation II (`Law A`, free-falling pressureless drag fluid with $\nabla_\mu T_d^\mu{}_i = Q_i = q_4 u_F$):** satisfies $d(E_{00})/dN = 0$ and $\mathrm{div}_3(T_d) = q_4 u_F$ identically in SymPy; without the $-K^2 \Omega_d \Phi$ counter-term, bulk inflow pumps $O(500)$ Weyl shear whenever $c_{\mathrm{vis}}^2 > 0$.

2. **Causal envelope results at $w_d = 0$, $x_0 = |\kappa|$ (2σ floor `(h, Ω_m)` refitted via `fit_coupled`):**

| Realization & Background | Closure ($c_{\mathrm{vis}}^2$) | $A_{\phi\phi,\mathrm{eff}}$ mean [min, max] | ISW ratio [min, max] | Pre-reg. Verdict (`±8%`, `[0.4,1.6]`) |
|---|---|---|---:|---|
| `Law C` ($F_d=0$), `Pantheon+` (`κ = -2.2445`) | `0.0` | `1.0485` [1.0418, 1.0544] | [0.898, 1.593] | **PASS** |
| `Law C` ($F_d=0$), `Pantheon+` (`κ = -2.2445`) | `0.1` | `1.0487` [1.0424, 1.0544] | [0.887, 1.398] | **PASS** |
| `Law C` ($F_d=0$), `Pantheon+` (`κ = -2.2445`) | `1/3` | `1.0488` [1.0429, 1.0544] | [0.880, 1.169] | **PASS** |
| `Law C` ($F_d=0$), `Pantheon+` (`κ = -2.2445`) | `mb95_l8` | `1.0488` [1.0426, 1.0544] | [0.881, 1.190] | **PASS** |
| `Law C` ($F_d=0$), `Pantheon+` (`κ = -2.2445`) | `1.0` | `1.0489` [1.0432, 1.0544] | [0.877, 0.949] | **PASS** |
| `Law C` ($F_d=0$), `DES-Dovekie` (`κ = -2.4966`) | `0.0` | `1.0543` [1.0466, 1.0609] | [0.890, 1.663] | FAILS ($\ell=2$ ISW `1.663`) |
| `Law C` ($F_d=0$), `DES-Dovekie` (`κ = -2.4966`) | `1/3` / `mb95_l8` | `1.0546` / `1.0545` | [0.87, 1.19] / [0.87, 1.21] | **PASS** (all $c_{\mathrm{vis}}^2 \ge 0.1$) |
| `Law C` ($F_d=0$), 2σ floor (`κ = -0.8317`) | all `0.0..1.0`, `mb95` | `1.0182–1.0183` | [0.943, 1.212] | **PASS** |
| `Law A` ($Q_i = q_4 u_F$), `Pantheon+` (`bulk_rest`) | `0.0` | `1.0485` [1.0418, 1.0544] | [0.898, 1.593] | **PASS** |
| `Law A` ($Q_i = q_4 u_F$), `Pantheon+` (`bulk_rest`) | `0.1` / `1/3` / `mb95_l8` | `0.992` / `0.955` / `0.987` | `[2.52,2.63]` / `[3.57,4.07]` / `[3.17,3.23]` | **FAILS** (ISW `2.5–4.1×`) |
| `Law A` (`matter_comoving`), `Pantheon+` (`1/3`) | `1/3` | `0.8321` [0.7197, 0.9014] | [12.85, 15.65] | **FAILS** (ISW `13–16×`, $L=40$ `0.72`) |
| `Law A` (`bulk_rest`), 2σ floor (`κ = -0.8317`) | `0.0` / `0.1` / `1/3` | `1.018` / `0.997` / `0.983` | `[0.95,1.21]` / `[1.52,1.53]` / `[1.84,1.94]` | `0.0, 0.1` PASS; $\ge 1/3$ FAILS |

**Pre-registered verdict: `SURVIVES ENVELOPE` (`5D PDE justified`) `[D]`/`[O]`:**
- Because causal closures pass on `Pantheon+_best` (and for `Law C`, across all $c_{\mathrm{vis}}^2 \ge 0.1$ and `mb95_l8` on both `Pantheon+` and `DES-Dovekie`, insensitive to `ic_W = unperturbed`), the flux-fed wall is **not** eliminated model-independently and the 1+1D 5D AdS-Vaidya bulk perturbation solve remains justified `[O]`.
- Even better, the causal bracket pinpoints the exact 5D question: under geometric zero-momentum drag (`Law C`, $F_d=0$), free-streaming Weyl radiation ($c_{\mathrm{vis}}^2 = 1/3$, `mb95_l8`) passes cleanly at $+4.9\%$ (`Pantheon+`) / $+5.5\%$ (`Dovekie`) CMB lensing (`~1.9–2.1σ` of Planck `1.000 ± 0.026`); whereas if 5D junction dynamics yields free-falling drag (`Law A`, $Q_i = q_4 u_F$), every free-streaming/viscous shear closure ($c_{\mathrm{vis}}^2 \ge 0.1$) is ruled out `[X]` by $2.5\text{–}20\times$ late-ISW excess at best fit unless the bulk enforces near-zero anisotropic stress ($c_{\mathrm{vis}}^2 = 0$).

### Independent verification (Claude Code CLI, 2026-11-19)
- **Reproduction.** `weyl_causal_envelope.py` reruns byte-identical to `WEYL_CAUSAL_ENVELOPE.json` (only `elapsed_seconds` differs).
- **ℓ sampling.** The script samples ISW only at ℓ ∈ {2, 5, 10, 20, 30}, but the pre-registration says ℓ ∈ [2, 30]. Rerun at every integer ℓ in [2, 30], the reported ranges hold: the c_vis² = 0 maximum is at ℓ = 2, and the Law A c_vis² ≥ 0.1 maxima fall at ℓ = 18–30 and match the reported brackets to the third decimal.
- **Knife edge.** Under the pre-registration's primary convention (bulk-rest flux), free-falling drag (Law A) passes at a best fit only for c_vis² = 0. That closure has zero Weyl anisotropic stress, and Law A and Law C give identical numbers there. Its ℓ = 2 ISW ratio is 1.5934 with 25 k-modes and 1.5944 with 50, against the 1.6 gate: a numerically stable pass, 0.4% inside the gate.
- **Law C is post-hoc.** The pre-registration names the flux-frame conventions but not the drag-momentum law. Law C (F_d = 0) was introduced in the run. Its robust passes for free-streaming closures (c_vis² = 1/3, `mb95_l8`) are a post-hoc result: they sharpen the 5D junction question but do not carry the pre-registered verdict.
- **Verdict wording.** SURVIVES ENVELOPE under the pre-registered rule, narrowly: only through the zero-stress closure, 0.4% inside the ISW gate. Robustly only under the post-hoc Law C. The 5D bulk-perturbation solve stays justified `[O]`, and its first job is to decide which drag-momentum law the junction gives.

### 5D follow-up (2026-11-19)
- Phase 1 of the bulk solve (`exploration/bulk5d/`): the covariant velocity-dependent tension reproduces this drag background but is `[X]` as the flux-fed branch, because its flux flips sign at z ≈ 0.73. Absorbed bulk null dust gives Law A with a computed flux frame. Law C has no covariant realization from either candidate.
- Phase 2 (`exploration/bulk5d/`): under any closure, DES-Dovekie fails the ISW gate. Pantheon+ passes only if the bulk flux source keeps the effective Weyl viscosity below c_vis² ≈ 1.5–5.5×10⁻⁴ (Hu family, two tested frames). The flux frame drops out at zero viscosity.

## 4D Effective Law Freeze & Domain Statement (2026-11-21)
The 5D origin of the flux-fed drag is closed `[X]`: the dark-bubble sign rule (`arXiv:2507.03748`, `exploration/bulk5d/WEP_2507_03748_AUDIT.json`) excludes non-abelian gluon matter by ~11 orders against lunar laser ranging ($\eta_{\mathrm{active}} \ge 9\times 10^{-3}$ vs. $3.9\times 10^{-14}$), neither covariant candidate supplies Law C, and the Weyl dark-radiation anisotropic stress has no brane evolution equation (`arXiv:1004.3962`) while $\Omega_{\mathrm{Weyl}}(0) \approx 1.75$. Inside its surviving 4D domain, the drag is frozen solely as a 4D effective parameterization (`drag_gcosmo`): Pantheon+ passes only for free-falling drag (`Law A`) at $c_{\mathrm{vis}}^2 = 0$ on the $\ell = 2$ late-ISW gate by a slim margin (`1.593` against `1.6`), whereas DES-Dovekie needs momentum pinning $\Gamma \gtrsim 30H$ that no tested covariant source supplies. A frictional bulk medium with a tuned $q(z)$ stays `[O]` and is not required, radial string forests stay untested and are not required, and the full Boltzmann calculation for this wall is **blocked** (not pending) by the missing 5D bulk closure.
