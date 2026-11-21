# Tidal screen with an AeST two-field (QUMOND-type) scalar sector (2026-11-19)

> **SCOPE NOTICE (2026-11-21):** Under [`../../02_galaxy_dynamics/GALAXY_LAW_SCOPE_2026-11-21.md`](../../02_galaxy_dynamics/GALAXY_LAW_SCOPE_2026-11-21.md) and [`../../OUTSIDE_GALAXIES.md`](../../OUTSIDE_GALAXIES.md) (Erratum `E-16`), `μ_std` with measured `a₀` is the galaxy law scored on galaxies and ordinary general relativity holds outside galaxies; Cassini `Q₂` is **not** a gate on `μ_std`, so the `x*`/`working-C` solar-system screen is no longer required for `μ_std`. All mathematical normalization (`normalization_kb.py`), slip (`single_metric_slip_audit.py`), and `x_H` results below remain archived intact.

Pre-registration: `PREREG.md` (committed before the run). Script: `tidal_aest_bbn.py` → `TIDAL_AEST_BBN.json`.

**Verdict: both pre-registered gates pass [D]. The model as a whole is [O]: the covariant completion is missing.**

- **BBN.** A QUMOND-type scalar sourced by Φ̂ has essentially no share of Newtonian-regime gravity: ν − 1 ≈ a₀²/(2g²) ≤ 1.6×10⁻¹² at Saturn even unscreened. S2 suppresses that further, to ~10⁻³⁰. In the D3 map c₄,eff → 0, so **G_cosmo/G_local = 1 − K_B/2**: 0.975 at K_B = 0.05, 0.95 at K_B = 0.1.
- **Why the AeST routes failed BBN.** The BBN failure of every earlier route traced to the AQUAL-type tracking 𝒥, where the scalar carries Ĝ/λ_s of Newtonian gravity. The two-field form removes that share by construction, with or without the screen.
- **Mercury.** The extra force is negligible (share·g_N underflows).
- **Well-posedness [D].** Both equations are Poisson-type with S applied to known sources (TIDAL_SCREENING §1). The single-scalar AQUAL tidal form is ill-posed and stays [X].
- **Galaxies, Cassini and the Oort cloud: unchanged from the corpus.**
  - SPARC Δχ² ≈ 0, since S = 1 for galaxies (x ≤ 1.9×10¹⁰ ≪ x*).
  - Cassini sits at the 2σ edge by calibration of x*.
  - The Oort peak holds at RY's working C.
  - GW170817 passes, since x is built from Φ̂'s Hessian.

**So the tidal screen is the first route to clear BBN, Cassini, SPARC, Oort and GW170817 together**, at quasistatic level. That makes it the corpus's live candidate.

**What stays open [O].**
1. A covariant action for a QUMOND-type scalar sourced by Φ̂ inside AeST. AeST's 𝒥(𝒴) sector is AQUAL-type; QUMOND needs an auxiliary-field construction.
2. x* (and C) are declared inputs, fixed by Cassini (x*) and the Oort window (C), not derived.
3. The c₄,eff = local-share identification in the D3 map is a modelling step, not derived.

**Next decisive item:** write the covariant QUMOND-in-AeST action (auxiliary field), and check its cosmology (ghost-freedom, c_T, and that G_cosmo is unchanged).

## Covariant step (`covariant_qumond_check.py`, SymPy Euler–Lagrange)
Aether-frame action, built only from spatial gradients q^{μν} = g^{μν} + A^μA^ν:
L = ρφ + (1/8πG)[−2 q(∂φ,∂ψ) + q(∂ψ,∂ψ) + a₀² F(q(∂ψ,∂ψ)/a₀², X(∇∇ψ))].

1. **[D]** Varying φ gives ∇²ψ = −4πGρ, so ψ is the Newtonian potential. Varying ψ gives Poisson for φ with a source built from the known ψ, including the Hessian ("W") terms, which reach fourth order in ψ. The system is **triangular**: ψ comes from ρ, then φ from ψ. That is why it is well-posed even though F depends on ∇∇ψ.
2. **[D, structural]** No time derivatives appear in the aether frame, so φ and ψ are constraints and do not propagate. The indefinite φψ cross term therefore carries no propagating ghost.
3. **[D]** On FRW the spatial gradients vanish, so the sector reduces to a₀²F(0,0)/8πG. With F(0,0) = 0, G_cosmo and Λ are unchanged, and the BBN result above stands.
4. **[D, structural]** The sector is quadratic in φ and ψ, which vanish on the background, so h_ij couples only at second order and **c_T = c**.

**Binding open requirement: how matter feels φ.**
- A ρφ (conformal) coupling gives no MOND lensing, so galaxy and cluster lensing see GR mass only.
- A disformal coupling for photons is excluded by GW170817: GWs and photons would cross the Milky Way's potential with different Shapiro delays (Boran et al. 2018).
- So the MOND potential must enter the **single metric** (both potentials, γ = 1). AeST already does this through its **J^μ∇_μφ mixing**, where J is the aether acceleration, equal to ∇Φ in the static weak field.
- **Next construction:** keep AeST's J·∇φ mixing and replace 𝒥(𝒴) with the auxiliary-ψ QUMOND sector above. Then check γ = 1 / PPN, lensing = dynamics, and that the D3 c₄,eff → 0 identification follows from the field equations instead of being assumed.

## The MOND potential enters the single metric [D] for the static reduction (`aest_qumond_metric.py`)
Static weak-field Lagrangian:
L = ρΦ + (1/8πG)[Ψ′² − 2Φ′Ψ′ (Einstein–Hilbert) + 2Φ′φ′ (AeST-type J·∇φ mixing) − φ′² + 2φ′ψ′ + a₀²F(ψ′²/a₀², ψ″)].

Verified with SymPy, on ρ = −∇²Φ_N/(4πG):
- **Ψ = Φ = Φ_N + φ** and ψ = −Φ_N. The Φ, Ψ and φ equations vanish identically.
- The ψ equation is the Poisson equation for φ, sourced by Φ_N through F. With F′ = (ν − 1)S and the Hessian ("W") terms, φ is the tidally screened QUMOND phantom potential.
- **γ = 1 and lensing equals dynamics.** Photons, GWs and matter all follow the one metric, so the Boran et al. Shapiro-delay constraint is met. The γ = 1 argument of TARGET_D3 §8.1 carries over: every sector stress is quadratic in perturbations.
- **The scalar drops out locally, as derived.** Because Φ = Φ_N + φ with φ ≈ 0 where (ν − 1)S ≈ 0, the solar-system scalar share vanishes. That is the c₄,eff → 0 used in the BBN gate.

**Status of the tidal–AeST candidate.**
- **Passes:** BBN, Mercury, Cassini (at the 2σ edge by x* calibration), SPARC, the Oort peak (working C), GW170817, γ = 1 and lensing = dynamics. Quasistatic level, with a covariant aether-frame action.
- **Still open:**
  1. Full covariant check of the mixing weight against AeST's 2(2 − K_B)J·∇φ, and the K_B normalisation of G_N.
  2. Linear cosmological perturbations with the new sector. It is non-dynamical, so this is expected to be ΛCDM-like; unchecked.
  3. x* and C remain declared inputs.

## Items 1–3 (2026-11-19)
**1. Normalisation against AeST's own weights [D] (`normalization_kb.py`, all four field equations zero).**
- With the AeST static weights (Maxwell K_B/2, mixing (2 − K_B), scalar (2 − K_B)/2), the solution is Ψ = Φ, ψ′ = −g_N, and Φ′ = ν(g_N/a₀)g_N with ν = 1 + F′.
- **G_N = G̃/(1 − K_B/2)** and G_cosmo/G_N = 1 − K_B/2.
- It works because AeST's ratio of mixing to scalar weight is exactly 1.

**2. Linear cosmology: the bare sector fails; the x_H screen fixes it.**
- **Unscreened** (`linear_cosmology.py`, `linear_growth.py`): the QUMOND source is sub-linear (ν − 1 ≈ 12–16 for linear modes), unlike AeST's second-order AQUAL term. Growth is enhanced 245–1186×.
- **Screening on x alone** (`xlow_scan.py`): growth within 2% needs x_low ≳ 10⁶, which screens 45% of SPARC points. Fails.
- **Nonlinearity screen** (`xh_screen.py`): S on x_H = ‖∇∇Φ_N‖/H², with H = θ/3 from the aether expansion. Linear modes have x_H ≲ 1; SPARC has x_H ≥ 1623. With x_H,low = 10–100, growth is within 4×10⁻³ to 4×10⁻⁵ of ΛCDM and no SPARC point is screened.
- **Natural value:** the virial scale ≈ 0.87 Ω_m Δ_vir ≈ 154 lies in the window, so MOND acts only inside collapsed structures.

**3. Constants: bounded on both sides by data, not derived [O] (`item3_windows.py`).**
- x* ∈ [1.7×10¹⁰ (SPARC), 7.04×10¹¹ (Cassini)].
- C ∈ [0.209, 0.696] (Oort window).
- x_H,low ∈ [10 (growth), 492 (SPARC)].

**Candidate after items 1–3.**
- Passes at quasistatic and linear level: BBN, Mercury, Cassini (2σ edge), SPARC, the Oort peak, GW170817, γ = 1, lensing = dynamics, and linear growth.
- Open:
  - nonlinear structure formation;
  - the full CMB (the sector is off at linear order, so it inherits AeST/D5's status);
  - deriving the constants.

## Close-out of the open items (`closeout.py` → `CLOSEOUT.json`)
- **CMB: closed at this level.** At recombination the sector's boost on linear modes is b ≤ 7.5×10⁻¹³ (x_H ≪ x_H,low). The CMB is therefore that of the underlying AeST/ΛCDM background, and this sector adds nothing. The background itself keeps AeST/D5's status.
- **Nonlinear structure: computed (spherical top-hat in ΛCDM, x_H,low = 154).**
  - Collapsing shells stay screened until near virialisation, then feel the phantom boost.
  - The collapse threshold falls: δ_c changes by −1.2% at 10¹⁴ M☉, −3.3% at 10¹¹ M☉ and −6.9% at 10⁸ M☉.
  - **Prediction:** more low-mass halos and earlier dwarf/high-z collapse. Cluster abundance moves by roughly 7% (≈1–2% in σ₈ equivalent), which is marginal against current counts and testable.
  - The absolute δ_c here uses a matter-era extrapolation (1.28 against the exact 1.686); the relative changes are the result.
- **Constants.**
  - **x_H,low is derived** from spherical-collapse virialisation: 0.866·Ω_m·18π² ≈ 154, inside the data window [10, 492]. "MOND switches on at virialisation" is the postulate; the number follows from it.
  - **x* is not derived.** It corresponds to a tidal density of 3.2×10³ M☉ pc⁻³ (a globular-cluster core) and stays a data-bounded [O] input in [1.7×10¹⁰, 7.04×10¹¹].
  - **C is not derived.** It stays inside the Oort window [0.209, 0.696], as a constant Lagrangian zero.

**Final status of the candidate.**
- Passes: BBN, Mercury, Cassini (2σ edge), SPARC, the Oort peak, GW170817, γ = 1, lensing = dynamics, linear growth, and the CMB (the sector is inert at linear order).
- Makes a testable nonlinear prediction: δ_c lowered by 1–7%, most at low mass.
- Constants: one derived (x_H,low); two data-bounded but not derived (x*, C).

## Can x* and C be derived? No, within this theory [D] (`constants_derivation.py` → `CONSTANTS_DERIVATION.json`)
- **x*.** With only {G, c, a₀, H₀, Λ} and no mass scale, every tidal scale is a power of cH₀/a₀ (= 5.64 at the fitted a₀). The data window x* ∈ [1.7×10¹⁰, 7.04×10¹¹] needs that ratio raised to the power 13.6–15.8, which is no natural construction. **x* is a genuine new constant.**
- **What x* encodes.** Cassini's calibration places the screen onset at 0.40× the tidal field at the Sun's MOND radius (r_M = 7148 au). That explains the value, but it refers to one body, so it is not a law.
- **C** is a constant zero of the screening Lagrangian. No symmetry selects a nonzero value, and C = 0 is [X] (Oort). It is a boundary datum, not derivable from the action.

**Final constant count for the candidate.**
- **Derived:** x_H,low ≈ 154, from virialisation.
- **New constants, data-bounded:** x* (a tidal scale) and C (a boundary datum).
- **Alongside the corpus's two irreducible inputs,** a₀ and the choice of function.

## Single-metric anisotropic stress & gravitational slip audit (`single_metric_slip_audit.py` → `SINGLE_METRIC_SLIP_AUDIT.json`, sheet `SINGLE_METRIC_SLIP_AUDIT.md`) `[D]`
- **Naive standalone scalar `[X]`:** without AeST's $J\cdot\nabla\phi$ mixing, a single-metric deep-MOND scalar ($F(y) := \frac{2}{3}y^{3/2}$) carries $p_r = +2\rho_\chi$, $p_\theta = -\rho_\chi$, selecting $\rho_\chi = C_\chi/r^3$ and forcing $O(1)$ linear slip $(\Phi'-\Psi')/\Psi' = 2/\ln(r/r_0)$ (plus $\ln r$ halo mass, not flat $v_c$).
- **Live AeST AQUAL & Tidal-QUMOND match identically:** both yield on-shell anisotropic stress $8\pi\tilde{G}(T^r_{\;r}-T^\theta_{\;\theta}) = -K_B(\Phi')^2 - (2-K_B)\Phi'\phi'$; linear slip vanishes ($\Psi = \Phi$, $\gamma_{\mathrm{PPN}} = 1$), and at $O(\epsilon^2)$ the pure-MOND $(\Phi')^2$ self-stress cancels identically against $(G^r_{\;r}-G^\theta_{\;\theta})_{O(\epsilon^2)} = -2(\Phi')^2$, leaving $r(\delta_{\mathrm{slip}}'/r)' = (2-K_B)\Phi' g_N$ ($\delta_{\mathrm{slip}} = (1-\frac{K_B}{2})\frac{G_N^2 M^2}{4r^2}$ Newtonian; $\frac{2}{3}(1-\frac{K_B}{2})\frac{v_c^2 G_N M}{r}$ deep MOND).
- **12 X-COP clusters & SPARC:** across all 12 clusters in `../d10_xcop/xcop_data.tsv`, $|\delta_{\mathrm{slip}}/\Phi|_{\mathrm{scale}} \le 6.17\times 10^{-6}$ at $K_B=0$ (`4.01×10⁻⁶` deep-MOND at $K_B=0.05$), and $\sim 3.1\times 10^{-8}$ in SPARC — confirming weak-lensing and X-ray HSE masses match to $\sim 10^{-5}$.
