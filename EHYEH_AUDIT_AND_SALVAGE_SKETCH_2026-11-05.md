# E.H.Y.E.H. manuscript: audit summary and salvage sketch

**Status  (2026-11-05):** proposal only.  No claim, tier  or  number  in this repository changes. Everything below is `[O]` unless it names a dated record or a script with an exit code.
**Author:** Claude Code CLI, at RY's request (2026-11-05).
**Subject:** *Entropic Harmonics of Y¹⁴ Entanglement Holonomics (E.H.Y.E.H.)*, the BLK-1009 manuscript by Antigravity CLI, `Chyren/3_research/publications/holographic_obserververse/`, PDF of 2026-11-05 02:30 CST (16 pages). It was written without this repository's current state. Its full audit is on The Block; this file keeps the part that matters here: what must not be imported, and three ideas that could extend the current branch if rebuilt on it.

## 1. What must not be imported

Each  line names the  record it contradicts.  All  were  checked against `CURRENT_STATE_READ_THIS_FIRST.md` (verified 2026-11-01).

- **E8  / Observerse foundation.**  Its §II builds  on  the  E8-dimension material retired 2026-08-25 (§2 of the current state), and uses compact Spin(14) for a fibre of Lorentzian metrics, whose DeWitt metric is indefinite. Rebuild on V₂(ℝ³) via Cartan triality, or drop it.
- **a₀ = cH₀/2π as a derivation.** Its eq. 43 sets the Unruh temperature equal to the de Sitter temperature. That gives a₀ = cH₀, and the 1/2π is then inserted by definition (eqs. 49, 91). Here the 1/2π is `[O]`, a declared anchor (`HORIZON_SELECTION_AUDIT_2026-09-16.md`: no selecting principle). The headline a₀ is 1.1607×10⁻¹⁰ m/s², not 1.20.
- **A Cassini pass for μ_std.** Its eqs. 34–35 use c²r_s²/r⁶, which is not in s⁻², to claim a 22-order margin. The binding test is the external-field quadrupole, which bare μ_std fails (`02_galaxy_dynamics/NONSPHERICAL_EFE_SOLVER_2026-10-27.md`, 9.68σ).
- **The anti-drift gate and a coherence equal to μ.** Its §VI restates the premise retracted 2026-09-03. Its steady state (eq. 68) is not stationary for its own generator. Use `PILLAR_IV_MU_IDENTITY_2026-10-13.md`: θ is a ceiling, and the exact coherence is 4x/(1+8x²).
- **Ω_Λ = ln 2 as derived.** It stays `[O]`. The horizon-tied late-time edge fails the CMB block (`04_cosmology/HDE_CMB_PHANTOM_2026-10-17.md`, Δχ² = +46.3 against ΛCDM).
- **A second relativistic completion.** Its non-local symmetric-teleparallel sector competes with D9 (AeST). Its eqs. 31–32 do not follow from its action (eq. 30), and its −∂U∂V term has a negative-norm combination.
- **"Without free parameters"** (two places). The two declared inputs, a₀ and the μ choice, stand. `check_retracted_claims.sh` fails the .tex.
- **Table II (five SPARC galaxies).** No code produced it, and its V_flat values and errors do not match `02_galaxy_dynamics/sparc_data/SPARC_Lelli2016c.mrt`. For example, DDO 154 is 51.3 ± 1.5 there and 47.0 ± 1.0 in the catalogue.

## 2. Three ideas worth rebuilding here

Each  is `[O]`. Each  must be pre-registered  before  any  data comparison, as is the convention here. Each adds only declared constants, under the 2026-10-15 rule: a constant fixed once by one system is allowed if it predicts the others without retuning, and stays `[O]` until derived.

### A. A covariant observer coupling (the Fisher metric)

**The  paper's form.** It  puts a term  ℓ²·I_IJ(σ)·∂σ^I∂σ^J  into  the matter metric (eqs. 88, 95), with I the quantum Fisher metric of the observer's state family.

**The  constraint from here.**  Matter stays on  g.  A  disformal ∂χ∂χ term in the matter metric tilts the photon cone, and GW170817 bounds its coefficient below about 10⁻¹¹ (2026-10-15 record).

**The  form that can  attach to D9.**  Matter  stays  on g, and a separate observer sector is added: S_obs = −½∫d⁴x √−g ℓ²·F(σ)·g^μν∂_μσ∂_νσ − ∫√−g V(σ; 𝒴). F is the Fisher metric, which is positive-definite, so the kinetic term is healthy and its stress tensor satisfies the null energy condition `[D]`, since T_μν k^μk^ν = ℓ²F(k·∂σ)² ≥ 0.

**First  computation (done).** The  Fisher information of  the  exact  Pillar IV family `[D]` (`scripts/ehyeh_observer_qfi.py`, 4/4 checks, exit 0) is:

    F(x) = 16/(1 + 8x²)² = 16·(1 − μ_std(2√2·x)²)²,   x = u/γ

In  θ = √2·arctan(2√2·x)  the term F(x)(∂x)²  is  exactly  (∂θ)², a free massless scalar on [0, π/√2). **On its own the observer sector does nothing physical.** Any effect has to come from V, that is, from the `[O]` identification of x with g/a₀.

**The  obstacle to test  first.** A weak  V  leaves  θ free, which is healthy but has no observable effect. A stiff V slaves θ to g/a₀, which is read off the gradient of the AeST scalar. Then the Fisher term carries second derivatives of that scalar, the same problem that sank the Hessian-built tidal screen (2026-10-15 record, Legendre–Hadamard).

- **Gate  A1:** is there  a window of  V's  strength  that is both well-posed and observable?
- **Gate A2:** if so, find the largest ℓ that the frozen Batch-1A SPARC gate and the QUMOND Cassini solver allow. That gives a bound `[E]`.
- **Kill condition:** if no window exists, record observable effects as `[X]` and keep the identity as interpretation only.

**New constants:** ℓ and V's strength.

### B. A cluster phase transition (superfluid dark matter)

**The  paper's form (§IV.B–C).**  A boson fluid  is  condensed  in galaxies (T_kin ≪ T_c), where its phonons carry the MOND force, and in the normal phase in clusters (T_kin > T_c), where it is collisionless, so lensing follows the galaxies, as in the Bullet Cluster. This is Berezhiani & Khoury, Phys. Rev. D 92, 103510 (2015) `[C]`, and the paper does not cite it. Its T_c and T_kin numbers reproduce arithmetically, for its chosen boson mass of 1 eV and densities.

**State  here.** Clusters are  open. The pure-MOND  limit  fails  by a factor 1.96 (D10 §2). AeST's μ² term has the right sign, but its size is gauge-dependent: R is 1.13 or 0.66 depending on the gauge. Inside the SZ radius the gap persists, R = 1.76 under μ_std (`TARGET_D10_CLUSTERS.md` §10, 2026-11-02).

**A  theory choice, for  RY.** Berezhiani–Khoury is  a  dark-matter  model: the condensate has its own mass. Adding it ends the program's no-dark-matter framing. The options are:
- **B1:** a separate dark sector next to AeST. In galaxies the condensate's mass then adds to the phonon force, so SPARC must be refitted without double-counting.
- **B2:** an AeST-native phase dependence. Nothing derives one yet `[O]`.

**First  test (B1), with  data already in  the  repository.**  For D10's 12 weak-lensing clusters (Corasaniti, Sereno & Ettori 2021):
1. Solve for the normal-phase mass that brings R to 1 at r₅₀₀, and at r_C = 0.54·r₅₀₀.
2. Compare it with the condensate mass that SPARC allows.
3. Compare the self-interaction thermalisation needs with the Bullet-cluster bound, σ/m ≲ 1 cm²/g (Randall et al. 2008 `[C]`).

**Other  gates.** A μ_std-like  phonon force near  the  Sun  meets the same Cassini external-field failure as bare μ_std. Whatever couples the phonon to baryons must keep c_T = c.

**Kill  conditions:** the required  normal-phase mass exceeds  the  budget  SPARC allows, or the needed σ/m violates the Bullet bound.

**New constants:** the boson mass, the self-coupling, and the phonon–baryon coupling.

### C. A covariant home for the screen (the second field)

**State here.** The tidal screen is well-posed only in QUMOND's two-field reading. AeST reduces to AQUAL, so "the screen's covariant home needs a second field, as in bimetric MOND" `[O]` (2026-10-16 record).

**The  standard any screen  must meet** (BLK-400):
- the  screen  reads  only a shadow field computed from matter alone, never the field it shapes;
- S is analytic in the shadow's Hessian;
- the field equation comes from the action, keeping the W term;
- momentum conservation (G5) and universal free fall (G10) are checked before any data comparison;
- the Galactic external field is included.

**The  paper's form fails  that standard.** Its  fields  U  = □_Q⁻¹Q and V = □_Q⁻¹U are sourced by the non-metricity scalar Q, which is geometry. The shadow would read the field it shapes.

**Adapted  form.** One auxiliary  scalar U, sourced  by  the  trace of matter only, with the retarded solution:

    □U = −(4πG/c⁴)·T_matter,     static weak field:  U → Φ_N/c²

This  is a covariant  Newtonian shadow. The  screen  variable  is built from U's Hessian projected onto AeST's own rest space, with q_μν = g_μν + A_μA_ν and x = c⁴‖q∇∇U q‖/a₀². Projecting with q keeps second time derivatives of U out of the action. The equation for U is imposed by a Lagrange multiplier λ. Varying U then puts the W term into λ's equation, which reproduces the QUMOND structure.

**Gates:**
- **C1  (ghost):** the pair  (U, λ) has  a  mixed  kinetic term. Show by constraint analysis that, under the retarded prescription, it carries no independent initial data, so no propagating ghost (Deser & Woodard 2007 `[C]` for the non-local analogue). Otherwise `[X]`.
- **C2 (static limit, regression):** reproduce the frozen QUMOND screening numbers exactly: `02_galaxy_dynamics/SCREENED_C_SOLUTIONS.json`, `CASSINI_AT_WORKING_C_2026-10-16.md`, x* = 7.04×10¹¹, and the SPARC and wide-binary records.
- **C3:** c_T = c on FRW and Schwarzschild backgrounds. U stays out of the matter metric.
- **C4:** U's background evolution must not move H(z) beyond what the CMB block and DESI DR2 BAO allow.
- **C5:** G5 and G10, inherited.

**Constants:**  none new. The  Oort result carries  over,  so  x* and the working C = 0.579124707982253 remain declared inputs.

## 3. Order

C  first. It fills  a named `[O]`  of  the  current branch, reuses frozen numbers, and adds no constant. B next: the data are already here, but it needs RY's decision on adding a dark sector. A last: its first computation shows the sector is inert unless the `[O]` identification is made physical, and the obvious way to do that runs into the problem that already killed the Hessian screen.
