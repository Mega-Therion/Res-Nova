# TARGET D5: Cosmological Sector

**Status:** D5_REWRITTEN_TO_AeST_K(Q) (2026-09-12). The entire pre-2026-09-12 content is
**void [X]** and retired in place below (§0). It computed cosmology from a free function of the
*vector* kinetic scalar 𝒦 and from a uniform MOND enhancement ξ; neither exists in the AeST
action that `TARGET_D7` was corrected to tonight. On FLRW, 𝒴 ≡ 0 identically, so the MOND free
function 𝒥(𝒴) — and therefore a₀ and μ(x) — **do not appear in linear cosmology at all**.
This document constructs the sector that does govern it: 𝒦(𝒬) = −½ℱ(0,𝒬).

**Non-linear structure formation — separate, still open [O]:** a pre-registered N-body campaign
(2026-09-11, before the AeST correction) tested the old ξ-based non-relativistic overgrowth
estimate: V1 negative control PASS (+22.2% vs ≥+5% gate), V2 theory arm INCONCLUSIVE (worst bin
3.03%, between the 1% consistency bound and the 5% tension threshold). That campaign's *theory
arm* input (ξ from the void vector-𝒦 sector) no longer applies post-rewrite, but the *test
infrastructure and negative control* are reusable once a non-linear AeST prediction exists to
feed them. See `04_cosmology/D5_RUN/` and CLM-D5-03 in `OPEN_PROBLEMS_AND_TESTS.md`. Non-linear
AeST structure formation itself remains unsimulated by anyone — the open item this document's
§7 identifies as the critical path.
**Last updated:** 2026-09-12
**Author:** R.W. Yett / Sovereign Architecture Group
**Tags:** `[P]` proved · `[D]` derived here · `[C]` cited · `[O]` open · `[X]` killed

---

## 0. What is retracted, and why **[X]**

| old section | claim | why it is void |
|---|---|---|
| §2 | "H₀c/a₀ ≈ 5.7 ⇒ horizon dynamics are Newtonian, cluster scales are deep-MOND" | 5.7 is the same number `TARGET_D7` §3 deleted. With 𝒴 ≡ 0 on FLRW there is **no** value of the MOND free function's argument on the background — there is no "regime" to be in. The ratio H₀c/a₀ remains a true arithmetic fact; the dynamical inference drawn from it does not. |
| §4.2–§4.3 | growth table; ξ = 2 ⇒ D(z=0) = 76.39×, ξ = 3 ⇒ 2263.8× | ξ was a *postulated uniform* G_eff/G. §3 below derives that at linear order in AeST the 𝒴-sector contributes **nothing**, so ξ = 1 exactly on linear scales. The 76×/2264× figures describe a theory this corpus does not hold. They are also the numbers `PEER_REVIEW_READINESS.md` and `04_cosmology/` still carry — see §7. |
| §5.1–§5.3 | νHDM overproduction (Russell et al.) imported as this theory's prediction | νHDM applies MOND universally at all scales in a Newtonian N-body code. AeST does not. The citation is correct about νHDM and **irrelevant to AeST**; it was doing load-bearing work here that it cannot do. |
| §6 | "at cosmological scales the dual-channel action changes nothing" | Accidentally right, for a reason the section did not give: not "deep-MOND is universal" but 𝒴 ≡ 0. Restated correctly in §3.1. |
| §6.2 | "RMOND screening" as the mitigation | There is no screening in this sector. The suppression is structural (𝒴 quadratic in perturbations), not dynamical. |

Kept: §7's task list, re-scoped in §6.

---

## 1. The background sector, from shift symmetry **[D]**

### 1.1 Reduction to 𝒦(𝒬)

On FLRW with N the lapse, φ = φ̄(t), A₀ = −N, Aᵢ = 0:

- 𝒴 = q^{μν}∇_μφ∇_νφ = 0, since ∇_μφ is purely timelike and q projects orthogonal to A. **[C]**
- J_μ = A^α∇_αA_μ is the acceleration of the unit normal to constant-t slices, which for a
  hypersurface-orthogonal normal equals ∂_μ ln N. On FLRW N = N(t) only, so J_μ has a time
  component alone, which the unit-norm constraint A^αA_α = −1 forces to vanish: J_μ ≡ 0 for
  **any** lapse N(t), not merely in a comoving gauge ⇒ the mixing term 2(2−K_B)J^μ∇_μφ drops.
  **[D]**
  *(This is load-bearing and is not in D7 §1.1: without it the background Lagrangian would not
  be 𝒦 alone. It is what makes the FLRW sector a pure k-essence.)*
- F_{μν} = 0 on the background.

Hence SZ eq. (5) → eq. (3):

$$S=\frac{1}{8\pi\tilde G}\int d^4x\,N a^3\Big[-\frac{3H^2}{N^2}+\mathcal{K}(\bar{\mathcal{Q}})\Big]+S_m[g],
\qquad \bar{\mathcal{Q}}=\dot{\bar\phi}/N,\qquad \mathcal{K}\equiv-\tfrac12\mathcal{F}(0,\bar{\mathcal{Q}})$$

**This is a shift-symmetric k-essence.** No potential; φ̄ enters only through 𝒬̄.

### 1.2 The three background equations **[D]**

δN ⇒ energy density; δa ⇒ pressure; δφ̄ ⇒ shift current conservation:

$$\boxed{\;8\pi\tilde G\bar\rho_\phi=\mathcal{Q}\mathcal{K}_{\mathcal{Q}}-\mathcal{K},\qquad
8\pi\tilde G\bar P_\phi=\mathcal{K},\qquad
\mathcal{K}_{\mathcal{Q}}=\frac{I_0}{a^3}\;}$$

(matching SZ's text verbatim **[C]**; the third is the *exact* first integral of the φ̄ equation,
valid for every 𝒦, and it is the structural fact everything below is a corollary of).

Two immediate consequences:

1. **Ω_c is an integration constant, not a prediction.** I₀ is fixed by initial data. AeST
   replaces a CDM particle with a constant of integration. Honest parameter accounting: this is
   a *relocation* of the dark-matter abundance parameter, not an elimination of it. SZ state the
   same ("the density ρ̄ is not (classically) predicted"). **[D]**+**[C]**
2. **Λ is a genuine constant** sitting in 𝒦 as a free additive −2Λ, exactly as in ΛCDM.
   ⇒ **w_DE = −1 exactly, at all redshifts.** **[D]**

### 1.3 The quadratic (minimal Higgs-phase) model, and what it costs **[D]**

SZ's eq. (4): 𝒦 = −2Λ + 𝒦₂(𝒬̄−𝒬₀)² + … . Then 𝒬 = 𝒬₀ + I₀/(2𝒦₂a³), and

$$\bar\rho=\frac{\bar\rho_0}{a^3},\quad 8\pi\tilde G\bar\rho_0=\mathcal{Q}_0I_0;\qquad
w=\frac{w_0}{a^3},\quad w_0=\frac{8\pi\tilde G\bar\rho_0}{4\mathcal{Q}_0^2\mathcal{K}_2};\qquad
c_{\rm ad}^2=\frac{2w_0}{a^3}$$

Dust + Λ. **Degenerate with ΛCDM at background level to O(w₀)** — but the degeneracy is not free.

**The two-sided squeeze, derived rather than quoted [D].** D7 §3.1 quotes SZ's μ⁻¹ ≳ 1 Mpc and
w₀ ≳ 10⁻⁸ without carrying the algebra. Carry it. The quasistatic mass is
μ = √(2𝒦₂/(2−K_B))·𝒬₀ (SZ eq. 6), so 𝒬₀²𝒦₂ = μ²(2−K_B)/2, and with 8πG̃ρ̄₀ = 3H₀²Ω₀:

$$\boxed{\;w_0=\frac{3H_0^2\Omega_0}{2\mu^2(2-K_B)}\;}\qquad
\mu^{-1}\gtrsim1\,\text{Mpc}\;\Rightarrow\;w_0\gtrsim1.1\times10^{-8}$$

against **w₀ ≲ 2×10⁻¹⁴** from w(a=10⁻⁴) = w₀·10¹² ≲ 0.02 (Kopp et al. 2018; Ilić et al. 2021).

$$\textbf{Gap} = 6.1\times10^{5}.$$

Worse than SZ state it, and the sharpening is in the **perturbations, not the background**:
c²_ad = 2w₀/a³ exceeds 1 at a = (2w₀)^{1/3} = 2.9×10⁻³ (z ≈ 340) and reaches **c²_ad = 2.5×10⁴
at a = 10⁻⁴**. Since SZ's pressure contrast is Π ∝ c²_ad (their eq. 11, reproduced in §3.2),
this means **Π ~ 10⁴·δ** through recombination — the new species is nothing like CDM, the
CMB peak structure and the MPS are destroyed. The quadratic Higgs phase is not merely "a bit
too stiff early on". **The quadratic 𝒦 is excluded. [D]** (`num.py`, §8.)

*Deliberately not claimed:* that this is a causality violation. c²_ad = dP̄/dρ̄ is a background
thermodynamic derivative, **not a propagation speed** — the perturbation speed of a
shift-symmetric k-essence has the bounded form 𝒦_𝒬/(𝒦_𝒬+𝒬𝒦_𝒬𝒬), and SZ themselves claim only
positivity ("clearly, w ≥ 0 and c²_ad ≥ 0"), not sub-luminality. The kill above needs no
causality argument; it runs entirely through Π. Deriving the actual c²_s from SZ eqs. (9)–(12)
in the k²→∞ limit (cf. their linear-stability paper arXiv:2109.13287) is **[O]**.

---

## 2. The Cosh completion: constructed, and it closes **[D]**

### 2.1 Why Cosh/Exp, and what SZ do and do not say **[C]**

SZ's own words (arXiv:2007.00082, retrieved 2026-09-12):

> "Unless the effect of the μ term in (6) is alleviated in some future theory, the Higgs phase
> cannot be extended too long in the past, and higher terms in (4) must be taken into
> consideration. Within the present setup, one can arrange this with a function 𝒦(𝒬) which
> suppresses w and c²_ad during most of the cosmic evolution. Examples are
> 𝒦 = 2𝒦₂𝒵₀²[cosh(𝒵)−1] ('Cosh function') and 𝒦 = 2𝒦₂𝒵₀²[e^{𝒵²}−1] ('Exp function'),
> where 𝒵 = (𝒬−𝒬₀)/𝒵₀."

**Answer to task item 4, stated plainly: the Higgs-phase-duration problem is *not* an open
problem in AeST. SZ pose it and solve it in the same paragraph, and then evolve Cosh and Exp
through their own Boltzmann code (their Figs. 1–2) and find Planck-consistent CMB and MPS.
What is genuinely open is narrower and different** — see §5. Forcing the phrase "open problem
in the literature" onto this would be wrong; the corpus simply never carried the resolution.

SZ do **not** recommend one over the other and do not *fit* 𝒵₀, but they do **report a working
value** — see §2.5, which turns their Fig. 1 legend into a calibration of everything below. They
report only that a "Higgs-like" quartic 𝒦 = (𝒦₂/4𝒬₀²)(𝒬²−𝒬₀²)² is "incompatible with a MOND
limit". This corpus adopts **Cosh**. **[D]**

### 2.2 The decoupling that makes it work **[D]**

$$\mathcal{K}_{\rm cosh}=-2\Lambda+2\mathcal{K}_2\mathcal{Z}_0^2\big[\cosh\mathcal{Z}-1\big]
=-2\Lambda+\mathcal{K}_2(\mathcal{Q}-\mathcal{Q}_0)^2+\frac{\mathcal{K}_2}{12\mathcal{Z}_0^2}(\mathcal{Q}-\mathcal{Q}_0)^4+\mathcal{O}(\delta\mathcal{Q}^6)$$

$$\mathcal{K}_{\mathcal{QQ}}(\mathcal{Q}_0)=2\mathcal{K}_2\quad\textbf{independently of }\mathcal{Z}_0.$$

**This is the whole mechanism.** μ = √(2𝒦₂/(2−K_B))𝒬₀ is set by the *curvature at the minimum*,
which Cosh does not touch; the early-time behaviour is set by the *width* 𝒵₀. Introduce

$$r\equiv\mathcal{Z}_0/\mathcal{Q}_0 .$$

μ constrains 𝒦₂𝒬₀²; nothing in the quasistatic sector constrains r. The two requirements that
were in direct conflict for the quadratic 𝒦 are **carried by independent parameters**. **[D]**

### 2.3 Exact background solution **[D]**

The first integral 𝒦_𝒬 = I₀/a³ gives, with A ≡ I₀/(2𝒦₂𝒵₀),

$$\sinh\mathcal{Z}=\frac{A}{a^3}\quad\Longrightarrow\quad \mathcal{Z}(a)=\operatorname{arcsinh}(A/a^3)$$

— an **exact closed-form background**, no ODE integration needed. Then

$$8\pi\tilde G\bar P_\phi=\frac{\mathcal{Z}_0I_0}{A}\big(\cosh\mathcal{Z}-1\big),\qquad
8\pi\tilde G\bar\rho_\phi=\frac{\mathcal{Q}_0I_0}{a^3}\Big[1+r\mathcal{Z}-\frac{r\,a^3(\cosh\mathcal{Z}-1)}{A}\Big]$$

$$c_{\rm ad}^2=\frac{\mathcal{K}_\mathcal{Q}}{\mathcal{Q}\,\mathcal{K}_\mathcal{QQ}}
=\frac{r\tanh\mathcal{Z}}{1+r\mathcal{Z}}$$

Matching the late-time quadratic limit fixes the crossover scale factor:

$$\boxed{\;A=\frac{2w_0}{r},\qquad a_\*\equiv A^{1/3}=\Big(\frac{2w_0}{r}\Big)^{1/3}\;}$$

**Two regimes, and the asymptotics are the result [D]:**

| regime | 𝒵 | w | c²_ad |
|---|---|---|---|
| a ≫ a_\* (quadratic) | A/a³ ≪ 1 | w₀/a³ | 2w₀/a³ |
| a ≪ a_\* (**log/ghost-condensate**) | ln(2A/a³) | r/[1+r(𝒵−1)] | r tanh𝒵/(1+r𝒵) |

The power law a⁻³ is replaced by **saturation at ≈ r, followed by logarithmic decrease**. That
is the whole fix, and it is three lines of algebra once the first integral is used.

### 2.4 Numbers: does it close? **[D]** — **yes**

At the μ-forced floor w₀ = 1.23×10⁻⁸ (μ⁻¹ = 1 Mpc, K_B = 0.1, Ω₀ = 0.26):

| r = 𝒵₀/𝒬₀ | a_\* | w(10⁻⁴) | c²_ad(10⁻⁴) | ρ̄a³ drift 10⁻⁴→1 | k_J (Mpc⁻¹) |
|---|:-:|:-:|:-:|:-:|:-:|
| 2×10⁻² | 0.0107 | 1.57×10⁻² | 1.5×10⁻² | +27.4% | 0.40 |
| 1×10⁻² | 0.0135 | 8.74×10⁻³ | 8.7×10⁻³ | +14.4% | 0.57 |
| **1×10⁻³** | 0.0291 | **9.84×10⁻⁴** | 9.8×10⁻⁴ | **+1.7%** | 1.81 |
| 1×10⁻⁴ | 0.0627 | 9.98×10⁻⁵ | 1.0×10⁻⁴ | +0.2% | 5.71 |

vs the quadratic case at the same w₀: w(10⁻⁴) = 1.2×10⁴, c²_ad = 2.5×10⁴.

**Three independent constraints on the single new parameter r [D]:**

1. **w ≲ 0.02 at a ~ 10⁻⁴** (Kopp/Ilić) ⇒ r ≲ 2×10⁻². Loosest.
2. **ρ̄_φa³ drift** between recombination and today: Ω_ch²(CMB) ≠ Ω_ch²(late). The drift is
   exactly the r𝒵 term, ρ̄a³ ∝ 1 + r ln(2A/a³). Demanding ≤1% would give r ≲ 5.8×10⁻⁴.
   **This is not in SZ, who report only w and c²_ad — and §2.5 shows it is over-tight as a
   *bound*, because their own fit absorbs it into Ω_ch². It is real as an *effect*, not as a
   constraint.** Demoted accordingly; see §2.5.
3. **Jeans/free-streaming — the softest of the three.** Using c_s ≈ √r (i.e. c_ad as a stand-in
   for a propagation speed, which §1.3 just warned against) gives λ_J ~ √r·τ_eq ~ √r·110 Mpc,
   so k_J = 1.8 Mpc⁻¹ at r = 10⁻³ and 0.40 Mpc⁻¹ at r = 2×10⁻². SZ are explicit that the system
   "does not close under the fluid variables" (it depends on α and E), so this is an
   order-of-magnitude orientation, not a derived cutoff. **[D]**-weak/**[O]**.

**Lower bound:** the model must be quadratic *today* (a_\* < 1), i.e. r ≫ 2w₀ ≈ 2.5×10⁻⁸.

$$\boxed{\;2.5\times10^{-8}\ \ll\ r\ \lesssim\ 2\times10^{-2}\;}\qquad\text{— a window spanning }\sim6\text{ decades.}$$

The headline closure rides on constraint 1 alone (w ≲ 0.02), which is the one SZ themselves use
and the one their published fit sits just inside. It does **not** depend on the contested
drift bound.

**Verdict on ΛCDM-consistency: achievable.** At a conservative r = 5×10⁻⁴ the expansion history deviates from
ΛCDM by |H/H_ΛCDM − 1| ≤ 3.6×10⁻³, monotonically decreasing from a = 10⁻⁴ to exactly 0 today:

| a | 10⁻⁴ | 10⁻³ | 10⁻² | 10⁻¹ | 1 |
|---|:-:|:-:|:-:|:-:|:-:|
| H/H_ΛCDM − 1 | +3.6×10⁻³ | +2.2×10⁻³ | +7.6×10⁻⁴ | +5×10⁻⁶ | 0 |

Sub-percent at all epochs, and the deviation sits in the *dust* sector (a slowly drifting
effective Ω_c), not in the DE sector. **[D]**

### 2.5 Calibration against SZ's own published Cosh run **[C]**+**[D]**

The parameters SZ actually used are printed in the C_ℓ^TT panel of their Fig. 1 (read from the
arXiv PDF p. 4, 2026-09-12; 𝒬₀ and 𝒵₀ in Mpc⁻¹):

$$\textbf{Cosh:}\quad K_B=0.5,\quad \mathcal{Q}_0=0.1,\quad \mathcal{K}_2=7.5\times10^{5},\quad \mathcal{Z}_0=10^{-3}$$

Feeding these through §1.3 and §2.3 **[D]**:

| quantity | SZ's Cosh run |
|---|---|
| r = 𝒵₀/𝒬₀ | **1.0×10⁻²** |
| μ = √(2𝒦₂/(2−K_B))·𝒬₀ | 100 Mpc⁻¹ ⇒ **μ⁻¹ = 10 kpc** |
| w₀ = 3H₀²Ω₀/[2μ²(2−K_B)] | 1.42×10⁻¹² (their own 3H₀²Ω₀/(4𝒬₀²𝒦₂) gives the same to 3 s.f. — an independent check that §1.3's box is right) |
| a_\* = (2w₀/r)^{1/3} | 7×10⁻⁴ |
| w(10⁻⁴) | 9.46×10⁻³ — **just inside the 0.02 bound** |
| c²_ad(10⁻⁴) | 9.40×10⁻³ |
| ρ̄a³ drift 10⁻⁴→1 | **+5.34%** |

**Three things fall out, and two of them correct this document [D]:**

1. **The construction is corroborated, not merely proposed.** SZ's Planck/SDSS-consistent run
   sits at r = 10⁻², inside §2.4's window and evidently tuned so that w(10⁻⁴) lands just under
   0.02. The Cosh mechanism is doing exactly what §2.2–§2.3 derive it does.
2. **§2.4's drift bound was over-tight, and the evidence is SZ's own caption.** Their run has a
   +5.34% drift in ρ̄a³ — 5× the 1% I demanded — and is still Planck-consistent, because the fit
   absorbs it. Strikingly, the caption reports the MOND curves deviating from the ΛCDM
   parameters by "∼{0.07, 0.33, **3.98**, 14.29, 1.57, 0.58, 2.60} percent", and 3.98% is the
   **Ω_ch²** slot. **The drift derived here is, to within the tuning, the origin of SZ's own
   reported Ω_ch² offset.** That is a much better result than a bound: it is a *mechanism* for a
   number they report without explaining. The correct statement is therefore "ρ̄a³ drifts
   logarithmically by ≈ r·ln(2A/a³), which appears as an Ω_ch²(CMB) vs Ω_ch²(late) offset of a
   few percent", **not** "r ≲ 5.8×10⁻⁴". **[D]**
3. **A tension inside SZ's own paper, which this corpus should carry [D]/[O].** Their Cosh run
   has **μ⁻¹ = 10 kpc**, a factor 100 *below* the μ⁻¹ ≳ 1 Mpc they state two paragraphs earlier
   as necessary "so that MOND behavior according to (2) may still be attained in galaxies". The
   published cosmological fit and the published quasistatic requirement are not evaluated at the
   same point in parameter space. Either the r_C ~ (r_M μ⁻²)^{1/3} estimate is looser than the
   Mpc quote suggests, or the CMB-preferred 𝒬₀, 𝒦₂ are in conflict with the galactic sector.
   **This is the one thing in this sector that is genuinely open in the literature, and it is
   not the problem the task expected** (which SZ closed). Resolving it requires evaluating r_C
   for real galaxies at SZ's own 𝒬₀, 𝒦₂. **[O]**

*(The "Exp" and "Higgs-like" legend rows are also present but the Exp 𝒵₀ digit is not
confidently legible from the render; only the Cosh row is quoted here.)*

---

## 3. Linear perturbations, redone from scratch in the correct sector **[D]**+**[C]**

### 3.1 Why the 𝒴-sector cannot contribute at linear order — the structural theorem **[D]**

This replaces the void F''/F' ≈ 0.00233 "screening factor" entirely. There is no screening
factor; there is a **selection rule**.

𝒴 = q^{μν}∇_μφ∇_νφ with φ = φ̄(t) + varphi. Because q^{μν} projects orthogonal to A^μ, and A^μ
is aligned with ∇φ̄ on the background, the background piece is annihilated:

$$\mathcal{Y}=\frac{|\vec\nabla\varphi|^2}{a^2}+\mathcal{O}(\delta A\cdot\partial\varphi)
\;=\;\mathcal{O}(\epsilon^2)$$

**𝒴 is quadratic in perturbations.** Therefore ℱ's 𝒴-dependence, expanded about the background,
contributes to the linear equations only through ℱ_𝒴(0,𝒬̄)·δ𝒴 — and δ𝒴 is second order. So:

$$\boxed{\;\textbf{a}_0,\ \tilde a_0,\ \lambda_s\text{-tail},\ \mu(x)\ \textbf{do not appear in linear cosmology.}\;}$$

SZ state exactly this: *"a₀ does not appear in the linear cosmological regime but will play a
role once nonlinear terms from ℱ(𝒴,𝒬) kick in."* **[C]**

**Consequences for the old §4 [X]:**
- ξ ≡ G_eff/G = **1** on linear scales. The postulate ξ = 2 or 3 has no realisation in AeST.
- The 76.39× and 2263.8× overgrowth figures are **void**, and so is the νHDM analogy (§0).
- The MOND enhancement is not *screened*; it is **absent by the tensor structure of 𝒴**. Any
  future statement that "AeST screens structure growth" would be wrong in the same way "branch A
  screens" is wrong in D7 §11.5. **[D]**

**Caveat, stated because it matters [D].** ℱ ~ 𝒴^{3/2} in the MOND limit is *non-analytic* at
𝒴 = 0: ℱ_𝒴 ~ √𝒴 ~ |∇varphi|/a. So the scalar sector has no linear regime in the usual sense —
the expansion is in |∇varphi|/(a·ã₀), not in an amplitude. The 𝒴 term dominates the canonical
(2−K_B)𝒴 piece only when |∇varphi|/a ≲ ã₀. The selection rule above is therefore exact as a
statement about *which terms enter δG_{μν} at O(ε)*, and the MOND sector enters as the leading
*nonlinear* correction, switching on at the scale/epoch where gradients drop below ã₀.
Quantifying that crossover in k and z is **[O]** (§5).

### 3.2 What *does* propagate: SZ's five-variable system **[C]**

The linear dynamics live entirely in the (𝒬, A_μ) sector. Newtonian gauge, A_μ = {−1−Ψ, ∇_iα},
φ = φ̄ + varphi, and the useful combinations

$$\chi\equiv\varphi+\dot{\bar\phi}\alpha,\qquad \gamma\equiv\dot\varphi-\dot{\bar\phi}\Psi,\qquad E\equiv\dot\alpha+\Psi$$

Then δG⁰₀ and δG⁰ⱼ take their **GR form** (matter couples only to g_{μν}) with a new species

$$\delta=\frac{1+w}{\dot{\bar\phi}c_{\rm ad}^2}\gamma+\frac{\nabla^2[K_BE+(2-K_B)\chi]}{8\pi\tilde Ga^2\bar\rho},
\qquad \theta=\frac{\varphi}{\dot{\bar\phi}}$$

obeying standard fluid equations but with a **non-standard pressure contrast**

$$\Pi=c_{\rm ad}^2\delta-\frac{c_{\rm ad}^2}{8\pi\tilde Ga^2\bar\rho}\nabla^2\big[K_BE+(2-K_B)\chi\big]$$

and the vector equation

$$K_B(\dot E+HE)=\mathcal{K}_\mathcal{Q}\chi-(2-K_B)\Big[\frac{\dot{\bar\phi}}{1+w}\Pi+(H+\dot{\bar\phi})\chi-3c_{\rm ad}^2H\dot{\bar\phi}\alpha\Big]$$

(SZ eqs. 7–12 **[C]**). The system does **not** close on (δ,θ) — it is not a dark fluid.

### 3.3 The CDM limit is controlled by exactly one number: c²_ad **[D]**

Read Π: every term carries a factor c²_ad. Hence

$$c_{\rm ad}^2\to0\quad\Longrightarrow\quad \Pi\to0\quad\Longrightarrow\quad
\dot\delta=(1+w)(3\dot\Phi-\tfrac{k^2}{a^2}\theta),\ \ \dot\theta=\Psi$$

which with w → 0 is **pressureless CDM exactly**. SZ: *"this relativistic MOND theory is
consistent with the CMB measurements from Planck. This happens because c²_ad and w are small
enough so that Π → 0."* **[C]**

**This is where §2's construction pays off, and it is the load-bearing link between the two
halves of this document [D]:**

| 𝒦 | c²_ad at a = 10⁻⁴ | Π | verdict |
|---|:-:|:-:|:-:|
| quadratic, at the μ-forced floor w₀ = 1.2×10⁻⁸ | **2.5×10⁴** | O(10⁴)·δ | CDM limit destroyed; MPS erased; **[X]** |
| **Cosh, SZ's published run (r = 10⁻²)** | **9.4×10⁻³** | ≲10⁻²·δ | CDM to 1% — **Planck/SDSS-verified by SZ ✓** |
| Cosh, r = 10⁻³ | 9.8×10⁻⁴ | ≲10⁻³·δ | CDM to 0.1% **✓** |
| Cosh, r = 5×10⁻⁴ | 4.9×10⁻⁴ | ≲5×10⁻⁴·δ | CDM to 0.05% **✓** |

**So the Higgs-phase-duration problem is a *perturbation-theory* problem, not a background one**
— the background w is observationally invisible at 10⁻⁸, but c²_ad = 2w sets the Jeans scale and
that is what Kopp/Ilić actually bound. The Cosh sector caps c²_ad at r and the corpus can now
state where structure formation comes from: **ordinary CDM-like growth, ξ = 1, with a
free-streaming cutoff at k_J ~ O(1) Mpc⁻¹, i.e. below the smallest scale linear MPS data probe
(§2.4 constraint 3, the softest of the three).** **[D]**

### 3.4 The μ⁻¹ ≳ 1 Mpc oscillatory regime is a *live* constraint, not a galaxy-only one **[O]**

SZ note the quasistatic Φ solution is oscillatory for r ≳ r_C ~ (r_M μ⁻²)^{1/3}. With
μ⁻¹ ~ 1 Mpc, r_C sits inside the range the matter power spectrum measures. The interface between
the μ²Φ² ghost-condensate mass term and the linear MPS at k ~ 0.1–1 Mpc⁻¹ is **not computed here**
and is not computed in SZ's PRL either (they defer to Skordis et al. 2021). **[O]**

---

## 4. DESI and the w₀–w_a question: a category error, stated plainly **[D]**

The task asks whether DESI DR1's evolving-dark-energy preference can be matched, and whether the
sibling Geometrodynamica targets w₀ = −0.831, w_a = −0.720 transfer.

1. **This repo carries no w₀/w_a target.** Grepped `PEER_REVIEW_READINESS.md`,
   `CLAIM_EVIDENCE_LEDGER.md`, this file: zero hits for `w0`, `wa`, `DESI`. Stated as a fact
   about this search. **[D]**
2. **AeST predicts w_DE = −1 exactly.** Λ enters 𝒦 as a free additive constant (§1.2), with no
   dynamics, at every order. There is no quintessence-like field to roll. **[D]**
3. **The deviation from ΛCDM in AeST lives in the *dust* sector**, as w_dust = w(a) > 0 and a
   slowly drifting ρ̄a³, not in the DE sector. Projecting that onto CPL (w₀, w_a) is **not a
   reparametrisation** — a positive-pressure dust component and an evolving DE component produce
   different H(a) *and* different growth, and they are distinguished by exactly the RSD/fσ₈
   data that CPL fits use.
4. **The Geometrodynamica pair (−0.831, −0.720) does not transfer.** It is a different
   framework's CPL fit. Importing it here would be a numerical graft. **[X]** for transferability.

**Honest DESI verdict:** AeST with the Cosh 𝒦 is degenerate with ΛCDM at background level to
|ΔH/H| ≲ 4×10⁻³ (§2.4). DESI DR1's evolving-w preference is therefore **neither predicted nor
accommodated** by this sector. If that preference firms up, it is evidence *against* AeST-with-Λ
at the same strength it is evidence against ΛCDM. Saying anything stronger in either direction
would be overclaiming. **[D]**/**[O]**

---

## 5. What is actually open **[O]**

Ranked, and deliberately *not* including the Higgs-phase-duration problem, which §2 closes.

1. **Non-linear structure formation.** ξ = 1 at linear order is a theorem about which terms
   enter δG_{μν}; it says nothing about collapse. The MOND ℱ(𝒴,𝒬) switches on precisely when
   |∇varphi|/a ≲ ã₀, which happens *first* in collapsing regions. No AeST N-body simulation has
   been run (this search, 2026-09-12 — a statement about this search). **This is now D5's single
   critical item**, and it is a genuinely different item from the old §5, which asserted the
   answer (76×) instead of leaving it open.
2. **Quantifying the linear→MOND crossover in (k, z).** §3.1's caveat. Tractable analytically.
3. **The μ²Φ² term vs the linear MPS at k ~ 0.1–1 Mpc⁻¹** (§3.4).
4. **SZ's own μ⁻¹ tension (§2.5 item 3).** Their published Cosh fit runs at μ⁻¹ = 10 kpc while
   their own text requires μ⁻¹ ≳ 1 Mpc for galactic MOND. **This is the genuinely open item in
   the literature for this sector** — not the Higgs-phase duration, which they closed. Needs
   r_C ~ (r_M μ⁻²)^{1/3} evaluated for real galaxies at SZ's (𝒬₀, 𝒦₂). **[O]**
5. **Full Planck likelihood for r.** The drift/degeneracy structure (§2.5 item 2) is a mechanism,
   not a fit; whether Ω_ch², A_s, n_s can absorb it across the full r window is unexplored.
   **[O]**
6. **The propagation speed c²_s**, as opposed to c²_ad (§1.3 caveat). SZ's linear-stability
   paper arXiv:2109.13287 is on Minkowski; the FLRW k²→∞ limit of their eqs. (9)–(12) is not
   carried out here. **[O]**
7. **𝒵₀ is a genuinely new free parameter.** Parameter accounting, stated not hidden: the
   cosmological sector carries λ_s, K_B, 𝒦₂ (≡ w₀), 𝒬₀, and now 𝒵₀ — five, against ΛCDM's
   Ω_c + Λ. AeST cosmology is *not* more economical than ΛCDM. It buys the MOND galactic law,
   not parameter parsimony.
8. **Cosh vs Exp.** SZ offer both and prefer neither. Nothing here distinguishes them; the Exp
   function 2𝒦₂𝒵₀²[e^{𝒵²}−1] gives 𝒵 ~ √ln(...) instead of ln(...), i.e. an even flatter
   early-time w. Deriving the discriminating observable is unattempted. **[O]**

---

## 6. Required computations, re-scoped

Superseding old §7. Struck items are void, not merely deprioritised.

- [x] Background 𝒦(𝒬) specified (Cosh), exact solution, ΛCDM consistency — **§2, [D]**
- [x] Two-sided w₀ squeeze derived in-house, not quoted — **§1.3, [D]**
- [x] Linear-order selection rule (𝒴 quadratic ⇒ ξ = 1) — **§3.1, [D]**
- [x] c²_ad ⇒ Π ⇒ CDM limit, with the Cosh numbers — **§3.3, [D]**
- [ ] Crossover (k, z) where ℱ(𝒴,𝒬) becomes non-negligible — **[O]**, tractable
- [ ] Modified Boltzmann run (SZ used their own code; CLASS/hi_class port) — **[O]**
- [ ] AeST N-body — **[O]**, the critical item
- [ ] ~~Compute the scale-dependent enhancement ξ(k,a) for the dual-channel μ~~ — **[X]**, μ does
  not enter linear cosmology (§3.1)
- [ ] ~~Compare linear growth against νHDM overproduction~~ — **[X]**, different theory (§0)

---

## 7. Downstream inconsistencies this rewrite creates (enumerated, not silently left)

The void numbers 76.39 / 2263.8 / "76×" / 0.00233 / 429× still appear in:

```
TARGET_D7_COVARIANT_COMPLETION.md              (already marked [X] in place — OK)
TARGET_D7_SUPPLEMENT_COUPLING_OPTIMIZATION.md
PEER_REVIEW_READINESS.md                       (D5 row updated by this pass)
GHOSTFREE_AND_SCREENING_CORRECTION_2026-09-08.md
CLAIM_EVIDENCE_LEDGER_v1.6.0_SUPPLEMENT.md
OPEN_PROBLEMS_AND_TESTS.md
CHANGELOG.md                                   (historical record — leave)
zenodo_metadata.json
res_nova_manuscript.tex                         <-- published surface, highest priority
04_cosmology/DRAFT_D5_LEDGER_ENTRY.md
04_cosmology/PREREG_D5_MG_EVOLUTION.md
SUBMISSION/COVER_LETTER_PRD.md                  <-- submission surface, highest priority
```

`res_nova_manuscript.tex` and `SUBMISSION/COVER_LETTER_PRD.md` are the two that reach readers.
Handed forward; not edited in this pass.

---

## 8. Reproduce

```
python3 - <<'EOF'
import sympy as sp
Q,Q0,K2,Z0,L=sp.symbols('Q Q0 K2 Z0 Lam',positive=True); Z=(Q-Q0)/Z0
K=-2*L+2*K2*Z0**2*(sp.cosh(Z)-1)
print(sp.series(K+2*L,Q,Q0,5))            # K2*dQ^2 + K2*dQ^4/(12 Z0^2) + ...
print(sp.diff(K,Q,2).subs(Q,Q0))          # 2*K2  -- independent of Z0
EOF
```
```
python3 - <<'EOF'
import numpy as np
Om,KB,w0=0.26,0.1,None
w0=3*(1/4282.7)**2*Om/(2*1.0**2*(2-KB)); print("w0_min (mu^-1=1Mpc) =",w0)   # 1.119e-08
print("w0_max =",0.02*(1e-4)**3, " gap =", w0/(0.02*1e-12))                   # 2e-14, 5.6e5
print("quadratic: c_ad^2=1 at a =",(2*w0)**(1/3.))                            # 2.83e-3
for r in (2e-2,1e-2,1e-3,1e-4):
    A=2*w0/r; a=1e-4; s=A/a**3; Z=np.arcsinh(s); ch=np.sqrt(1+s*s)
    rho=(1+r*Z-r*a**3*(ch-1)/A)/a**3; P=r*(ch-1)/A
    print(f"r={r:g} a_*={A**(1/3):.4f} w={P/rho:.3e} c_ad2={r*np.tanh(Z)/(1+r*Z):.3e}")
EOF
```

Full scripts: `kq.py`, `num.py`, `num2.py` (session scratchpad).

---

## 9. Summary ledger

| claim | tag | basis |
|---|:-:|---|
| Old §2 (5.7 ⇒ Newtonian horizon), §4.2–4.3 (76×/2264×), §5 (νHDM), §6.2 (RMOND screening) | **[X]** | §0 |
| J^μ∇_μφ = 0 on FLRW ⇒ background Lagrangian is 𝒦(𝒬) alone | [D] | §1.1 |
| 𝒦_𝒬 = I₀/a³ exactly, for every 𝒦 (shift symmetry) | [D]+[C] | §1.2 |
| Ω_c is an integration constant, not a prediction | [D]+[C] | §1.2 |
| w_DE = −1 exactly at all z; Λ is a free additive constant | [D] | §1.2 |
| w₀ = 3H₀²Ω₀/[2μ²(2−K_B)] ⇒ w₀ ≳ 1.1×10⁻⁸ vs w₀ ≲ 2×10⁻¹⁴; gap 6.1×10⁵ | **[D]** (SZ quote it; derived here) | §1.3 |
| Quadratic 𝒦 gives c²_ad = 2.5×10⁴ at a = 10⁻⁴ ⇒ Π ~ 10⁴·δ ⇒ CDM limit destroyed | **[D]** — sharper than SZ's w-only statement | §1.3, §3.3 |
| c²_ad is **not** a propagation speed; no causality claim is made, and none is needed | [D] | §1.3 caveat |
| Cosh 𝒦 has 𝒦_𝒬𝒬(𝒬₀) = 2𝒦₂ independent of 𝒵₀ ⇒ μ and early-time w decouple | **[D]** | §2.2, sympy |
| Exact background: 𝒵(a) = arcsinh(A/a³), A = 2w₀/r — closed form, no ODE | **[D]** | §2.3 |
| w saturates at ≈ r then falls logarithmically (vs a⁻³ for quadratic) | **[D]** | §2.3 |
| Window 2.5×10⁻⁸ ≪ r ≲ 2×10⁻², resting on w ≲ 0.02 alone | **[D]** | §2.4 |
| SZ's published Cosh run (K_B=0.5, 𝒬₀=0.1, 𝒦₂=7.5×10⁵, 𝒵₀=10⁻³) ⇒ r = 10⁻², w(10⁻⁴) = 9.5×10⁻³, w₀ = 1.4×10⁻¹² — **inside the window; construction corroborated** | **[C]**+**[D]** | §2.5 |
| ρ̄a³ drifts logarithmically by ≈ r·ln(2A/a³); = +5.34% for SZ's run, matching the **3.98% Ω_ch² offset they report without explaining** — a mechanism, **not** a bound (my earlier r ≲ 5.8×10⁻⁴ was over-tight) | **[D]** | §2.5 |
| SZ's own Cosh fit runs at μ⁻¹ = 10 kpc, 100× below the μ⁻¹ ≳ 1 Mpc their own text requires — **the genuinely open item in this sector** | **[D]**/**[O]** | §2.5 |
| \|H/H_ΛCDM − 1\| ≤ 3.6×10⁻³ for a ∈ [10⁻⁴, 1] at r = 5×10⁻⁴ | **[D]** | §2.4 |
| 𝒴 is quadratic in perturbations ⇒ a₀, μ(x), λ_s absent from linear cosmology; **ξ = 1** | **[D]**+[C] | §3.1 |
| ℱ ~ 𝒴^{3/2} non-analytic at 𝒴 = 0 ⇒ no amplitude-linear regime for the scalar | [D] | §3.1 |
| Π ∝ c²_ad ⇒ CDM limit; Cosh at r = 10⁻³ gives Π ≲ 10⁻³δ | **[D]**+[C] | §3.3 |
| Free-streaming cutoff k_J ~ O(1) Mpc⁻¹ — softest of the three constraints (uses c_ad as a stand-in speed; system does not close on fluid variables) | [D]-weak/[O] | §2.4 |
| SZ **solve** the Higgs-duration problem (Cosh/Exp + their Boltzmann runs); not an open problem | **[C]** | §2.1 |
| SZ do not fit 𝒵₀ or prefer Cosh vs Exp; "Higgs-like" quartic is MOND-incompatible | [C] | §2.1 |
| AeST predicts w_DE = −1; DESI evolving-w neither predicted nor accommodated; Geometrodynamica (−0.831,−0.720) does not transfer | [D]/**[X]** | §4 |
| 5 cosmological parameters (λ_s, K_B, 𝒦₂, 𝒬₀, 𝒵₀) vs ΛCDM's 2 | [D] | §5.5 |
| Non-linear AeST structure formation | **[O]** | §5.1 |
| c²_s (true propagation speed) on FLRW | [O] | §5.6 |
| μ²Φ² oscillatory regime vs linear MPS at k ~ 0.1–1 Mpc⁻¹ | [O] | §3.4 |
| Full Planck likelihood for r; Boltzmann port | [O] | §5.4 |

---

## 10. Verdict

**D5's cosmological sector is no longer unspecified.** Adopting SZ's Cosh function
𝒦 = −2Λ + 2𝒦₂𝒵₀²[cosh((𝒬−𝒬₀)/𝒵₀) − 1] and using the exact shift-symmetry first integral
𝒦_𝒬 = I₀/a³, the background solves in closed form as 𝒵(a) = arcsinh(2w₀/(r a³)), and the
Higgs-phase-duration problem closes because 𝒦_𝒬𝒬(𝒬₀) = 2𝒦₂ is independent of 𝒵₀ — the
quasistatic mass μ and the early-time equation of state are carried by *different* parameters.
The gap that kills the quadratic model is a factor 6.1×10⁵ (derived here, not quoted); the Cosh
model closes it with a six-decade-wide window 2.5×10⁻⁸ ≪ 𝒵₀/𝒬₀ ≲ 2×10⁻², resting on the
w ≲ 0.02 bound alone, with |ΔH/H| ≤ 3.6×10⁻³ against ΛCDM at every epoch. **The construction is
corroborated rather than merely proposed:** SZ's own published Cosh parameters (their Fig. 1
legend) give r = 10⁻², landing inside the window with w(10⁻⁴) = 9.5×10⁻³, just under the bound.
One effect derived here is not reported by SZ — the logarithmic drift of ρ̄a³ by ≈ r·ln(2A/a³),
which for their run is +5.34% and appears to be the origin of the otherwise-unexplained 3.98%
Ω_ch² offset in their own caption. It is a mechanism, not a bound. At linear
order the MOND sector is absent *by the tensor structure of* 𝒴 = q^{μν}∇_μφ∇_νφ, which is
quadratic in perturbations — so ξ = 1 exactly, the old 76×/2264× overgrowth is void rather than
screened, and growth is CDM-like with a free-streaming cutoff at k ≈ 1.8 Mpc⁻¹. The
Higgs-phase-duration problem is **not** open in the literature: SZ pose and resolve it in one
paragraph and validate it in their own Boltzmann code; what this corpus lacked was the
resolution, not the field. What *is* open in the literature, and was not expected, is smaller
and sharper: **SZ's Planck-fit Cosh run sits at μ⁻¹ = 10 kpc, a factor 100 below the μ⁻¹ ≳ 1 Mpc
their own quasistatic argument requires** — their cosmological and galactic sectors are not
evaluated at the same point in parameter space. D5 moves from **[O] void** to **[P/O]**: background and linear
perturbation theory are now derived and ΛCDM-consistent, with one honest cost (five parameters
against ΛCDM's two, and Ω_c demoted to an integration constant) and one genuinely critical
remaining item — **non-linear structure formation in AeST, which nobody has simulated** — plus
the μ⁻¹ mismatch above, which is inherited from the source rather than introduced here.
