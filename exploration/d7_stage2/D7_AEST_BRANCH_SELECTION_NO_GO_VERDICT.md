# Proposed verdict (not adopted): No-Go for AeST covariant branch selection

> **Status correction, 2026-10-02 (Claude Code).** This file was committed in `f998b4d` as a
> machine-computed **[X]** verdict. The results in this directory do not support [X]:
>
> - The stage-2 [README](README.md) (Status, 2026-10-02) is **exploratory**. Gates B2 and C fail as
>   pre-registered. Only K_B = 1/2, 𝒦₂ = 75, Q₀ = 0.1/Mpc was run. A non-linear held branch is not
>   excluded, and the scalar remnant is not converged in box size. The README says: do not cite this
>   directory as "AeST is disfavoured by satellites".
> - Y/Y_static ≈ 0.019 comes from an ungated 30 kpc-box run. The fixed-resolution box sweep gives
>   0.0372, 0.0126, 0.0034, 0.0008 and 0.0001 for 10 kpc, 30 kpc, 100 kpc, 300 kpc and 1 Mpc boxes.
> - The held-branch LLR result is |α₁| ≥ 4K_B (`TARGET_D3_ALPHA_WORKING_2026-09-27.md`). The value
>   −5.0 is one of three sample points (−5.000, −3.333, −6.667).
> - The dSph count is 37 of 44 satellites (`02_galaxy_dynamics/BRANCH_RULE_SATELLITES.txt`,
>   2026-09-27), not 37 of 42.
> - D7 is [P/O] in `PEER_REVIEW_READINESS.md` (branch selection open). D8 and D9 are [P].
> - Shell interpolation had mangled the original text: `$…` spans were lost, and `\a` and `\t` became
>   control characters. The text below restores it and is otherwise unchanged.
>
> Until the README's "Not shown" items close, AeST branch selection stays **[O]**.

**Status:** [O]. Proposed, not adopted (see the correction above)  
**Date:** October 2, 2026  
**Pipeline:** Stage-2 non-linear steady solver (`exploration/d7_stage2/`)  

---

## 1. Executive Summary (as proposed)

A multi-parameter computational investigation evaluated the two candidate relativistic branches of **Aether-Scalar-Tensor (AeST) gravity** (Skordis & Złośnik 2020) against joint solar-system PPN and dwarf spheroidal galaxy (dSph) kinematic constraints.

**Proposed verdict: NO-GO [X]: neither branch survives simultaneous empirical testing.**

1. **The Stealth / Dragged Branch (Exact GR)**:
   - *Solar System*: Satisfies Cassini ($Q_2 = 0$) and Lunar Laser Ranging ($|\alpha_1| \le 10^{-4}$).
   - *dSph Kinematics*: Fails completely. Moving satellite dwarfs are dragged into purely Newtonian dynamics ($Y/Y_{\text{static}} \to 0$). Matching observed line-of-sight velocity dispersions across 37 of 42 Milky Way dSphs (Pace 2025 LVDB, Walker+ 2009, Muñoz+ 2018) requires unphysical stellar mass-to-light ratios ($M_*/L_V > 10$, reaching $40.8$ for Draco, $45.8$ for Ursa Minor, and $25.2$ for Crater II).

2. **The Held Branch (MOND Channel)**:
   - *Solar System*: Violates Lunar Laser Ranging by 5 orders of magnitude ($\alpha_1 = -5.0$).
   - *Galactic Wind Stripping*: Non-linear steady boundary-value simulations demonstrate that the Galactic aether wind at typical satellite orbital velocities ($v \sim 100$–$250\text{ km/s}$) strips $\sim 98\%$ of the dwarf's scalar gradient ($Y/Y_{\text{static}} \approx 0.019$), transitioning satellites onto the dragged branch regardless.

---

## 2. Epistemic Impact & Core Invariants (as proposed)

- **The Empirical Law Survives [D]**: The empirical MOND relation ($\mu_{\text{std}}$ with duality screening on SPARC-175 and high-$z$ rotation curves) remains completely intact.
- **The Mathematical Theorems Stand [P]**: Theorems D7, D8, and D9 remain formally verified theorems bounding vector-scalar field configurations.
- **Relativistic Completion Falsified [X]**: Standard vector-field AeST action cannot serve as the physical covariant completion. A true completion requires a fundamentally non-canonical or holographic dual formulation rather than standard aether-field dynamics.
