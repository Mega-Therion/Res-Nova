# TARGET D3: PPN Limits and Solar System Constraints

**Status:** D3_PARTIAL — **γ CLOSED, β SCOPED, α₁/α₂ OPEN with a named obstruction. See §8 (2026-09-12), which supersedes §7 entirely.** γ_PPN=1 is now *derived* for AeST with F_std (and for any free function): every source of traceless anisotropic stress is O(ε²), so Φ=Ψ exactly and lensing gives GR's 4G_N M_dyn/bc² with no slip. β's free-function dependence is bounded by ε_J=2𝒴J″/J′=1/(1+x²)≲10⁻¹⁷; its (λ_s,K_B) part is a 2PN calculation nobody has done. Foster–Jacobson's α₁,α₂ formulas are **inapplicable** at AeST's couplings (c₁₂₃=0 Maxwell locus, spin-0 aether speed zero). Binding evaluable constraint: the μ_std residual δg=(1+λ_s)³a₀²/2g_N **grows as r²**, so Saturn (margin 50×), not Mercury (1251×), binds — giving the corpus's first bound **λ_s ≲ 2.7**.
**Prior status (superseded):** D3_OPEN_FAILING — μ(x)=x/(1+x) leaves a constant anomalous acceleration ≥ a₀ (D7 §4.2), failing Cassini Q₂ by 5.7×10⁵. That kill stands; §8 is built on its replacement, μ_std.
**Last updated:** 2026-09-12
**Author:** R.W. Yett / Sovereign Architecture Group
**Epistemic tag:** `[P]` proved · `[D]` derived · `[C]` cited · `[O]` open · `[X]` killed

---

## 1. Problem Statement

The Parameterized Post-Newtonian (PPN) formalism tests gravity theories in the weak-field, slow-motion regime. The solar system provides the most precise tests of gravity, with the Cassini probe constraining the space-curvature parameter to $|\gamma - 1| < 2.3 \times 10^{-5}$ [web:54][web:58]. This document computes the PPN parameters and MOND corrections for the dual-channel action and assesses consistency with solar system constraints.

---

## 2. Solar System Acceleration Profile [P]

The solar system is deeply in the Newtonian regime ($a \gg a_0$). The acceleration ratio $x = a/a_0$ ranges from $\sim 10^5$ (outer solar system) to $\sim 10^8$ (inner planets):

| Body | $g_N$ (m/s²) | $g_N / a_0$ | $\mu(g/a_0)$ | $1 - \mu$ | MOND correction |
|------|:-:|:-:|:-:|:-:|:-:|
| Mercury (0.39 AU) | $3.9 \times 10^{-2}$ | $3.3 \times 10^8$ | $0.999999997$ | $3.1 \times 10^{-9}$ | $3.1 \times 10^{-9}$ |
| Venus (0.72 AU) | $1.1 \times 10^{-2}$ | $9.5 \times 10^7$ | $0.999999990$ | $1.0 \times 10^{-8}$ | $1.0 \times 10^{-8}$ |
| Earth (1.0 AU) | $5.9 \times 10^{-3}$ | $4.9 \times 10^7$ | $0.999999980$ | $2.0 \times 10^{-8}$ | $2.0 \times 10^{-8}$ |
| Mars (1.52 AU) | $2.6 \times 10^{-3}$ | $2.1 \times 10^7$ | $0.999999953$ | $4.7 \times 10^{-8}$ | $4.7 \times 10^{-8}$ |
| Jupiter (5.2 AU) | $2.2 \times 10^{-4}$ | $1.8 \times 10^6$ | $0.999999453$ | $5.5 \times 10^{-7}$ | $5.5 \times 10^{-7}$ |
| Saturn (9.5 AU) | $6.6 \times 10^{-5}$ | $5.5 \times 10^5$ | $0.999998174$ | $1.8 \times 10^{-6}$ | $1.8 \times 10^{-6}$ |
| Pioneer scale (20 AU) | $1.5 \times 10^{-5}$ | $1.2 \times 10^5$ | $0.999991908$ | $8.1 \times 10^{-6}$ | $8.1 \times 10^{-6}$ |

**Key result [O] — retracted 2026-09-12, see correction below.** ~~At Earth's orbit, the MOND correction is $a_0/g \approx 2 \times 10^{-8}$, which is $\sim 1137\times$ below the Cassini sensitivity of $2.3 \times 10^{-5}$.~~ This comparison divides $1-\mu$ (a fractional correction to the non-relativistic force law) by $\gamma-1$ (a PPN metric parameter) — a category error, not a unit mismatch. **§3.1's own Theorem 3.1 below states that $\mu$ does not set PPN $\gamma$/$\beta$ at all**, so a ratio between the two has no physical meaning as a "margin below Cassini." What §2's table legitimately establishes is only that $1-\mu \sim 10^{-8}$–$10^{-9}$ in the inner solar system — i.e. the non-relativistic MOND correction to the Newtonian force law is small there. Whether the theory is safe against the actual Cassini $\gamma$ bound depends entirely on D7's covariant completion (§3.2), which has not yet been evaluated to produce an exact PPN $\gamma$, $\beta$ (see §6 anticipated-referee-Q in `PEER_REVIEW_READINESS.md`).

---

## 3. PPN Parameters [P]

### 3.1 Newtonian Regime

In the Newtonian regime ($x \gg 1$), the dual-channel action reduces to:

$$\mathcal{F}_{\text{dual}}(x) \approx \tfrac{1}{2}x^2 - x + \ln(x) \approx \tfrac{1}{2}x^2$$

The interpolation function $\mu(x) = x/(1+x) \approx 1 - 1/x + 1/x^2 - \cdots$ converges to 1, and the modified Poisson equation reduces to the standard Newtonian equation:

$$\nabla^2 \Phi = 4\pi G \rho$$

**Theorem 3.1 [P]:** In the Newtonian limit, the dual-channel action produces **standard Newtonian gravity** with no PPN deviations. The PPN parameters $\gamma$ and $\beta$ depend entirely on the **covariant completion** (D7/D9), not on the non-relativistic interpolation function $\mu$.

### 3.2 Why μ Does Not Affect PPN

The PPN expansion probes the metric $g_{\mu\nu}$ in the weak-field regime. The non-relativistic MOND action only modifies the Newtonian potential $\Phi$ through the modified Poisson equation. Since $\mu \to 1$ for $a \gg a_0$, the modification vanishes:

$$\delta\Phi_{\text{MOND}} \sim \frac{a_0}{g_N} \times \Phi_{\text{Newton}} \sim 10^{-8} \times \Phi_{\text{Newton}}$$

This is far below any current or foreseeable solar system test. The PPN parameters $\gamma$ (space curvature) and $\beta$ (nonlinearity) are determined by the post-Newtonian metric, which depends on the **relativistic** structure of the theory — i.e., the covariant completion (D7) and the RMOND embedding (D9).

### 3.3 Observational Constraints

| Parameter | GR value | Constraint | Source |
|-----------|:-:|:-:|:-:|
| $\gamma$ | 1 | $|\gamma - 1| < 2.3 \times 10^{-5}$ | Cassini (Bertotti et al. 2003) [web:54] |
| $\beta$ | 1 | $|\beta - 1| < 2.3 \times 10^{-4}$ | MESSENGER perihelion [web:58] |

**Update 2026-09-08 — the $\beta$ bound is now formalized.** The MOND-sector
contribution to $\beta$ is bounded in `PPNLimits.lean` by
`messenger_perihelion_satisfied` and `messenger_margin`. Evaluated at Mercury's
orbital gradient — the field point perihelion precession is actually sensitive to
— $x = g/a_0 = 3.548\times10^{8}$, giving $1-\mu(x) = 2.819\times10^{-9}$, a
margin of $8.2\times10^{4}$ against the MESSENGER bound.

Two caveats recorded in `PPN_VACUITY_AUDIT_2026-09-08.md`:

1. This bounds the **MOND-sector** contribution only. That $\gamma=\beta=1$
   exactly for the aether sector is a **[CITED]** result (Foster & Jacobson 2006,
   PRD 73 064015) for the Einstein-aether class D7's kinetic term belongs to. It
   is not proved in this corpus, and the two D7 theorems that appear to prove it
   are vacuous — verified by substitution, see the audit.
2. **Superseded 2026-09-12.** The "1137× below Cassini" figure is not merely
   missing a field point — it is a category error (dividing $1-\mu$ by
   $\gamma-1$, two physically different quantities), retracted in §2 above.
   The field-point sensitivity noted here (Earth 1222×, grazing $\sim10^7$,
   Saturn $\sim13$) was a symptom of the same underlying error, not an
   independent finding to be resolved by picking a field point.
| $\alpha_1$ | 0 | $< 10^{-4}$ | Lunar Laser Ranging |
| $\alpha_2$ | 0 | $< 10^{-4}$ | Solar spin precession |
| $Q_2$ | 0 | $(1.6 \pm 1.8) \times 10^{-27}$ s⁻² | Cassini radio tracking (2026) [web:55] |

---

## 4. The External Field Effect (Q₂) Tension [P]

### 4.1 The MOND EFE

The Milky Way's gravitational field at the Sun's position ($g_{\text{ext}} \approx 1.9 \times 10^{-10}$ m/s² $\approx 1.6 \, a_0$) is in the MOND transition regime. This external field modifies the internal dynamics of the solar system through the **external field effect** (EFE), producing a quadrupolar distortion parameterized by $Q_2$.

### 4.2 The Tension

The 2026 Cassini radio tracking analysis [web:55] found:

$$Q_2 = (1.6 \pm 1.8) \times 10^{-27}\;\text{s}^{-2}$$

consistent with zero. This constrains the MOND boost at the Sun's position to **less than 2%** (95% CL). However, galaxy rotation curves require a MOND boost of $\sim 60%$ at the same acceleration scale, creating a **3–15σ tension** depending on the mass modeling [web:55].

### 4.3 Resolution via RMOND Screening [O]

The tension arises because non-relativistic MOND predicts a sizeable EFE in the solar system. In the RMOND framework (Skordis–Złośnik 2021), the auxiliary fields can provide a **screening mechanism** that suppresses the EFE on solar system scales while preserving MOND behavior at galactic scales.

**Open question [O]:** Does the RMOND embedding with the dual-channel $\mu$ provide sufficient screening to satisfy the Cassini $Q_2$ constraint? This requires the D7 covariant completion.

---

## 5. The Cassini/MOND Result (2026) [P]

Hees et al. (2026) [web:55] used the full Cassini radio tracking dataset to constrain MOND's solar system signature:

- **$Q_2$ is consistent with zero** — no MOND EFE detected
- The PPN formalism accurately describes planetary dynamics
- Solar system measurements now provide **stronger constraints than wide-binary data** on classical MOND
- The MOND boost at the Sun's position is bounded to **< 2%** (95% CL)
- This creates **3–15σ tension** with galaxy rotation curve expectations

**Implication [P]:** The non-relativistic dual-channel action cannot resolve this tension alone. The resolution requires the covariant completion (D7) to provide screening, or the theory must accept that the solar system EFE is genuinely absent (which would require a departure from standard MOND phenomenology).

---

## 6. Summary of Findings

| Question | Answer | Status |
|----------|--------|--------|
| Is the dual-channel action safe in the inner solar system? | **Yes** — MOND correction $\sim 10^{-8}$, Cassini sensitivity $2.3 \times 10^{-5}$ | [P] |
| Do PPN parameters depend on $\mu(x) = x/(1+x)$? | **No** — all MOND $\mu$ functions give $\mu \approx 1$ in the solar system | [P] |
| What determines the PPN parameters? | The **covariant completion** (D7/D9), not the non-relativistic action | [P] |
| Is there a tension with the Cassini $Q_2$ constraint? | **Yes** — 3–15σ tension with galaxy rotation curves | [P] |
| Can the tension be resolved? | Only via RMOND screening in the covariant completion (D7) | [O] |
| What are γ and β for the covariant action? | γ = β = 1; \|γ−1\|,\|β−1\| ≲ 1/(2(1+g_N/a₀)); see §7 | [C]/[D] |
| What is the binding solar-system constraint? | Not γ/β — the preferred-frame α₁^PPN, α₂^PPN, uncomputed (§7.7) | [O] |
| Do D7 and D9 describe the same action? | **No** — GEA vs AeST; D7 §2 is the defect (§7.1) | [D] |

### Key Conclusion [P]

**The dual-channel action passes all solar system tests by construction**, because the solar system is in the Newtonian regime where $\mu \approx 1$. The PPN parameters are not determined by the non-relativistic action — they depend on the D7 covariant completion. The $Q_2$ tension is the most significant challenge, and it requires the RMOND embedding to provide a screening mechanism.

**Therefore [P]:** D3 is reduced to a **dependency on D7**. The PPN computation cannot be completed without the covariant formulation. The most productive path is to complete D7 first, then compute the exact PPN parameters from the RMOND metric.

---

## 7. γ and β from the covariant completion (added 2026-09-12)

> **§7.3–§7.7 partially superseded 2026-09-12 (same day) by the D7 rewrite.**
> §7.1's diagnosis was acted on: `TARGET_D7_COVARIANT_COMPLETION.md` is now the AeST action
> (Skordis–Złośnik arXiv:2007.00082 eq. 5), so the GEA reading below is retired.
> Under AeST, SZ derive **Ψ = Φ exactly** in the quasistatic weak field for any free function,
> so γ = 1 with **no metric slip to bound** — the Cassini 1.1×10⁸ and MESSENGER 1.6×10⁵ margins
> in §7.5 are margins on a null observable **[X]**, and Foster–Jacobson (§7.3) is a theorem about
> Einstein-aether, which has no scalar fifth force, whereas AeST does.
> **§7.7's nomination of α₁^PPN, α₂^PPN as "the tightest obstruction" is superseded [X]**
> (they remain uncomputed [O], but are no longer the first thing that breaks).
> The binding solar-system observable is **D7 §4.2**: because 1 − μ(x) = 1/(1+x) decays like
> 1/x, μ(x)=x/(1+x) leaves an *r-independent* anomalous acceleration ã₀ = (1+λ_s)a₀ ≥ a₀,
> giving 1.5 arcsec/century of Mercury perihelion precession against a ~10⁻³ arcsec/cy bound,
> and Q₂ ≈ ã₀/r = 1.9×10⁻²¹ s⁻² against Cassini's 3.4×10⁻²⁷ s⁻². **[X]** for μ = x/(1+x)
> in the solar system, independently of the covariant completion.
> §7.2's expansion parameter algebra (`K·F″/F′ = 1/(2(1+√K))`) is unchanged — it transfers
> verbatim with 𝒴 for 𝒦 — but it measures the *relative* correction to tracking, and D7 §4.2
> shows that correction is a constant *force*, not a decaying metric perturbation. Using it to
> bound |γ−1| was the error.

Replaces the retracted "1137× below Cassini" figure (§2) and the unsupported
order-of-magnitude claim in `TARGET_D7_COVARIANT_COMPLETION.md` §6.1
(`γ ≈ 1 − O(a₀²/g_N²) ≈ 1 − 10⁻¹⁶`).

### 7.1 D7 and D9 state two different theories — this must be fixed [D]

| | `TARGET_D7` §2 | `TARGET_D9` §1 |
|---|---|---|
| free function argument | `K = c₁(∇_μA_ν)(∇^μA^ν) + c₂(∇·A)² + c₃(∇_μA_ν)(∇^νA^μ)` — derivatives of the **vector** | `Y = a₀⁻² g^{μν}∇_μφ∇_νφ` — derivatives of a **scalar** |
| matter coupling | disformal, `g̃ = e^{2φ}g + σ²A_μA_ν` | minimal, to `g_μν` directly |
| vector kinetic term | absorbed into `F(K)` | separate Maxwell term `−(K_B/32πG)F_{μν}F^{μν}` |
| theory class | **generalized Einstein-aether** (Zlosnik–Ferreira–Starkman, astro-ph/0607411) | **AeST / RelMOND** (Skordis–Złośnik, PRL 127 161302, arXiv:2007.00082) |

These are not two presentations of one action. D7's is GEA; D9's is AeST.
**D9's is the load-bearing one**: the corpus's μ(x) = x/(1+x) is derived there as
`2J′(Y) = √Y/(1+√Y)`, and D9's `c_T = c` argument turns on the *absence* of the
disformal coupling that D7 §2 writes in. Per the repo's settled-decisions rule
this is a defect in D7 §2 to correct, not a fork: **D7 §2 should be rewritten to
D9's action.** Until it is, the two labels below are branch-conditional.

Two bookkeeping defects in D7 §2, independent of the above [D]:

1. **Dimensions.** `K` as written has units 1/length², so `F(K)` is ill-defined.
   The consistent GEA convention is `K ≡ (c²/a₀)²·[c₁(∇A)²+…]`, dimensionless.
   `σ²A_μA_ν` is likewise broken: σ = a₀/c² has units 1/length, set against a
   dimensionless `e^{2φ}g_{μν}`. D9's `Y = a₀⁻²(∇φ)²` has no such problem.
2. **√K vs √K/a₀.** D7 line 38 sets √K = x; line 70 sets x₀ = √K₀/a₀. Only the
   first is consistent. Below, **x ≡ √K = √Y = g/a₀** (up to an O(1) factor).

D7 §6.1's `a₀²/g_N²` appears to come from treating σ² as the small parameter. It
is not the expansion parameter of either theory. [X]

### 7.2 The expansion parameter is O(a₀/g_N), not O(a₀²/g_N²) [D]

F_dual and D9's J have the identical functional form, so one computation covers
both. With u ≡ √K (equivalently √Y), symbolically:

    F(K)   = K/2 − √K + ln(1+√K)
    F′(K)  = u / (2(1+u))
    F″(K)  = 1 / (4u(1+u)²)
    K·F″/F′ = 1 / (2(1+u))          ← dimensionless expansion parameter

The leading relative correction to the unmodified (Einstein-aether / GR) limit is
**1/(2x) = O(a₀/g_N)**. D7 §6.1 asserts the square; at x ~ 10⁸ that is wrong by
eight orders of magnitude. [X] for §6.1's exponent.

Large-K expansion in the ZFS/BDFSZ parameterisation `F′(K) = A + Σ_i α_i K^{−i/2}`:

    F′(K) = 1/2 − ½K^{−1/2} + ½K^{−1} − ½K^{−3/2} + …   ⇒  A = 1/2, α_i = (−1)^i/2

**The constant A = 1/2 is the dominant term at solar-system K.** At x ~ 10⁸ it
exceeds the α₁ piece by ~10⁸. This is why §7.3 is an Einstein-aether problem and
not a MOND-branch problem — and why BDFSZ's α₁-only branch (their §III solves
`F′ = α_{2n}K^{−n}` one power at a time, with **no constant term**) does not
apply here; see §7.6.

Reproduce:
```
python3 - <<'EOF'
import sympy as sp
K,u=sp.symbols('K u',positive=True)
F=K/2-sp.sqrt(K)+sp.log(1+sp.sqrt(K))
print(sp.simplify(sp.diff(F,K).subs(K,u**2)))                      # u/(2(u+1))
print(sp.simplify(sp.diff(F,K,2).subs(K,u**2)))                    # 1/(4u(1+u)^2)
print(sp.simplify((K*sp.diff(F,K,2)/sp.diff(F,K)).subs(K,u**2)))   # 1/(2(1+u))
print(sp.expand(sp.series(sp.diff(F,K).subs(K,1/u**2),u,0,8).removeO()))
EOF
```

### 7.3 γ = β = 1 at leading order, on either reading

**GEA reading (D7 §2).** At solar-system K, F′ → 1/2 = const, so the action *is*
Einstein-aether with `c_i^eff = c_i`, plus a relative O(1/2x) correction.
**Foster & Jacobson (gr-qc/0509083, PRD 73 064015) prove γ = β = 1 identically
for Einstein-aether at all c₁,c₂,c₃**; the only nonvanishing PPN parameters are
the preferred-frame α₁, α₂. [C]

**AeST reading (D9 §1).** Matter couples minimally to g_μν with no disformal
piece, and D9 §0.4 asserts Φ = Ψ ⇒ γ = 1. That assertion is **not derived** in
D9 and the two D7 theorems that appear to support it are vacuous
(`PPN_VACUITY_AUDIT_2026-09-08.md` §1). The published quasistatic spherical
solutions of AeST are Skordis & Złośnik / Verwayen et al., arXiv:2304.05134. [O]

**Corroboration, different branch.** Bonvin, Durrer, Ferreira, Starkman &
Zlosnik, arXiv:0707.3519 (PRD 77 024037), solve GEA for a static spherically
symmetric source in isotropic coordinates including growing terms, on the branch
`c₃ = −c₁` with `F′ = α₁K^{−1/2}` (no constant), and find

    a₁ = −1, a₂ = 1/2, a₃ = −3/16, a₄ = 1/16;  b₁ = 1, b₂ = 3/8, b₃ = 1/16, b₄ = 1/256

Matching the isotropic PPN metric `g₀₀ = −(1−2U+2βU²)`, `g_ij = (1+2γU)δ_ij`
with `U = GM/r = r_s/2r` gives `a₁ = −1`, `a₂ = β/2`, `b₁ = γ`, hence γ = β = 1.
**Check [D]:** (b₁,b₂,b₃,b₄) = (1+y)⁴ and (a₁..a₄) = −[(1−y)/(1+y)]² with
y = r_s/4r — the solution is isotropic Schwarzschild through (r_s/r)⁴ exactly.
Since this is the α₁-only branch, it is corroboration that the MOND sector does
not spoil γ,β, not the branch F_dual sits on. [C]

### 7.4 Size of the deviation [D]

Foster–Jacobson makes the leading term exactly zero, so the deviation is bounded
by the first neglected relative correction, `K·F″/F′ = 1/(2(1+x))`:

    |γ − 1| ≲ 1/(2(1+x)),   |β − 1| ≲ 1/(2(1+x)),   x = g_N/a₀

This is an upper bound derived from the expansion parameter, **not** a computed
value of γ−1; the actual coefficient multiplying it is not computed here [O].

### 7.5 Numerical evaluation, a₀ = 1.116×10⁻¹⁰ m s⁻² (SPARC) [D]

| field point | g_N (m s⁻²) | x = g_N/a₀ | 1/(2(1+x)) |
|---|:-:|:-:|:-:|
| Cassini grazing (r = R_⊙) | 2.743×10² | 2.458×10¹² | 2.03×10⁻¹³ |
| Mercury (0.387 AU) | 3.961×10⁻² | 3.549×10⁸ | 1.41×10⁻⁹ |
| Earth (1.0 AU) | 5.932×10⁻³ | 5.315×10⁷ | 9.41×10⁻⁹ |
| Saturn (9.54 AU) | 6.517×10⁻⁵ | 5.840×10⁵ | 8.56×10⁻⁷ |

**Like quantity against like quantity** — both columns are now PPN metric
parameters, which is exactly what §2's retracted ratio was not:

| test | param | field point | bound | predicted | margin |
|---|:-:|---|:-:|:-:|:-:|
| Cassini Shapiro delay | γ | grazing, r = R_⊙ | 2.3×10⁻⁵ | ≲2.0×10⁻¹³ | **1.1×10⁸** |
| MESSENGER perihelion | β | Mercury, 0.387 AU | 2.3×10⁻⁴ | ≲1.4×10⁻⁹ | **1.6×10⁵** |

γ and β are safe by 5–8 orders of magnitude — not the 10¹¹ of D7 §6.1, and not
the meaningless 1137 of §2.

### 7.6 Retracted en route: an α₁-based bound on c₁,c₂ [X]

A first version of this section applied BDFSZ's solar-system solution
`c₁ = −33.11 α₁⁻²(B̃₂/Mr_s)²` with F_dual's |α₁| = 1/2 to conclude
`|c_i| ≲ 10⁻¹⁵`, contradicting D7 §3's α = 3(c₁+3c₂+c₃) = O(1). **Retracted.**
BDFSZ derive that formula for `F′ = Σ_{i≥1} α_i K^{−i/2}` with **no constant
term** (their sum starts at i = 1; they state the n = 0 case is excluded). F_dual
has F′ → 1/2, which dominates α₁K^{−1/2} by ~10⁸ in the solar system, so the term
their formula solves for is the negligible one. Further, α₁ is not
normalisation-invariant once a constant A is present — under c_i → s·c_i,
α₁ → α₁/√s and A → A/s, so only α₁²/A is invariant, and comparing α₁ = 1/2
(A = 1/2) with BDFSZ's α₁ ≲ 10⁻⁹ (A = 0) is not like-for-like. Logged rather
than deleted: it is the same shape of error as the retracted 1137×, a number
carried across a regime boundary without checking the regime matched.

### 7.7 The tightest remaining obstruction [O]

Not γ, not β. Foster & Jacobson give, for Einstein-aether at general c_i,
**nonzero preferred-frame parameters α₁^PPN, α₂^PPN as functions of
(c₁,c₂,c₃)**, constrained by Lunar Laser Ranging (α₁ ≲ 10⁻⁴) and solar spin
precession (α₂ ≲ 10⁻⁷). Those are the parameters this theory can actually fail.
They are **not computed anywhere in this corpus** — `TensorSpeed.lean` computes
α₁ only after hard-coding the Maxwell case (c₁ = K/2, c₃ = −K/2, c₄ = 0) into
its definitions, which is an assumption, not a result
(`PPN_VACUITY_AUDIT_2026-09-08.md` §5). Closing D3 means computing
α₁^PPN(c₁,c₂,c₃) and α₂^PPN(c₁,c₂,c₃) and showing a nonempty region satisfying
them jointly with the ghost-free conditions, the rotation curves, and the CMB.

### 7.8 Claim ledger

| claim | tag | basis |
|---|:-:|---|
| D7 §2 and D9 §1 state different theories (GEA vs AeST); D7 §2 is the defect | [D] | §7.1 field-content comparison |
| `K` and `σ²A_μA_ν` dimensionally inconsistent as written in D7 §2 | [D] | §7.1 |
| K·F″/F′ = 1/(2(1+√K)); expansion parameter is O(a₀/g_N) | [D] | sympy, §7.2 |
| D7 §6.1's `γ−1 ~ O(a₀²/g_N²) ≈ 10⁻¹⁶` | **[X]** | wrong power, §7.2 |
| F′ → 1/2 dominates the α_i at solar-system K | [D] | §7.2 |
| γ = β = 1 identically for Einstein-aether, all c_i | [C] | Foster & Jacobson gr-qc/0509083 |
| BDFSZ's α₁-branch solution is isotropic Schwarzschild through (r_s/r)⁴ | [D] | §7.3 check of arXiv:0707.3519 |
| AeST reading: Φ = Ψ ⇒ γ = 1 | [O] | asserted in D9 §0.4, not derived; see arXiv:2304.05134 |
| \|γ−1\|, \|β−1\| ≲ 1/(2(1+x)) | [D] | §7.4; bound, not value |
| Cassini margin 1.1×10⁸, MESSENGER margin 1.6×10⁵ | [D] | §7.5 |
| \|c_i\| ≲ 10⁻¹⁵ from BDFSZ + α₁ = 1/2 | **[X]** | regime mismatch, §7.6 |
| α₁^PPN, α₂^PPN at general c_i | [O] | §7.7 — the binding constraint |

**Verdict.** γ and β are not where this theory is at risk. On the GEA reading of
D7 §2, the solar-system limit of F_dual is ordinary Einstein-aether (F′ → 1/2),
for which Foster–Jacobson give γ = β = 1 identically at all c_i, with deviations
bounded by the derived expansion parameter 1/(2(1+g_N/a₀)) — 2.0×10⁻¹³ at the
Cassini grazing point and 1.4×10⁻⁹ at Mercury, margins of 1.1×10⁸ and 1.6×10⁵
against Cassini and MESSENGER. On the AeST reading of D9 §1 the disformal
coupling is absent entirely and γ = 1 for the same structural reason, though
that step is asserted rather than derived in this corpus. The single tightest
obstruction is neither: it is the preferred-frame pair α₁^PPN, α₂^PPN as
functions of (c₁,c₂,c₃), bounded at 10⁻⁴ and 10⁻⁷ and uncomputed here — and,
prior to that, the fact that D7 and D9 do not currently describe the same action.

---

## 8. PPN for AeST with F_std — γ derived, β scoped, α₁/α₂ diagnosed (added 2026-09-12)

Supersedes §7 entirely (§7 kept in place per the repo's log-don't-delete rule). §7 computed
γ,β for generalized Einstein-aether and bounded them with an expansion parameter; the action
was wrong and the bound was a bound on a null observable. This section redoes the work on the
**AeST action (D7 §1) with the free function J(𝒴) built from F_std** in D2's convention
`F′(x)=x·μ(x)`, i.e.

$$F_{\rm std}(x)=\tfrac12\big[x\sqrt{1+x^2}-\operatorname{arsinh}x\big],\qquad
\mathcal J(\mathcal Y)=2\lambda_s\tilde a_0^{\,2}F_{\rm std}(\sqrt{\mathcal Y}/\tilde a_0),\qquad
\mathcal J'(\mathcal Y)=\lambda_s\frac{\sqrt{\mathcal Y}}{\sqrt{\mathcal Y+\tilde a_0^{\,2}}}$$

**Convention warning, load-bearing.** `TARGET_D1_SUPPLEMENT` §1/§3/§5 uses `F′=μ`
(`F_std=√(1+x²)−1`), which gives `J′→0` in the Newtonian limit instead of `J′→λ_s`;
`TARGET_D2_SUPPLEMENT` §1 marks that **[X]**. Everything below uses D2's convention. β and
every residual computed here depend on the Newtonian-limit behaviour of `J′`, so the two
conventions are not interchangeable.

### 8.0 Second published source for the weak-field system [C]

Verwayen, Skordis, Złośnik et al., arXiv:2304.05134 (retrieved 2026-09-12, PDF), their
eqs. (1)–(4), with `Φ = Φ̃ + χ`, `β₀ ≡ 1/λ_s`:

$$\nabla^2\tilde\Phi+\mu^2\Phi=\frac{4\pi G_N\rho_b}{1+\beta_0},\qquad
\nabla^2\tilde\Phi=\vec\nabla\!\cdot\!\Big[\frac{d\mathcal J}{d\mathcal Y}\vec\nabla\chi\Big],\qquad
\vec\nabla\!\cdot\!\Big[\frac{d\mathcal J}{d\mathcal Y}\vec\nabla\chi\Big]+\mu^2\Phi=\frac{4\pi G_N\rho_b}{1+\beta_0}$$

This is D7 §2's system with the ghost-condensate mass term `μ` restored (`μ⁻¹ ≳ 1 Mpc`, so
`μ²Φ` is utterly negligible in the solar system and is dropped below). **Their §3 states
verbatim: "In deriving (2)-(4) one also finds that the two standard weak-field metric
potentials Φ and Ψ are equal."** That is a second published source for γ=1, independent of
the free function. The paper is quasistatic-spherical only: **it contains no `g_{0i}` sector,
no PPN parameters, no β, and no α₁/α₂.** It cannot be used for §8.2 or §8.3. **[C]**

### 8.1 γ = 1 is a property of the AeST *background*, not of J — derived [D]

The discriminating object is the traceless part of the linearised `ij` Einstein equation, not
the reduction to the Poisson system. With `g_{00}=-(1+2Ψ)`, `g_{ij}=(1-2Φ)δ_{ij}`:

$$\Big(\partial_i\partial_j-\tfrac13\delta_{ij}\nabla^2\Big)(\Phi-\Psi)=-8\pi\tilde G\,\Sigma_{ij},
\qquad \Sigma_{ij}\equiv T_{ij}-\tfrac13\delta_{ij}T_{kk}$$

Background: `A_μ=(-(1+Ψ),\,\partial_i\zeta)` with `A^i=0` at zeroth order, `φ=𝒬₀t+φ̃`.
Every field perturbation `{Ψ,Φ,ζ,φ̃}` is O(ε). Enumerating **every** source of Σ_ij:

| term in D7 §1 eq. (5) | its `g^{ij}`-dependent stress | order |
|---|---|:-:|
| `S_m` (perfect fluid, minimal coupling) | `ρv_iv_j`, `p δ_ij` | O(ε²), traceless part 2PN **[standard]** |
| `−(K_B/2)F_{μν}F^{μν}` | `F_{0i}=−∂_iΨ`, `F_{ij}=0` ⇒ `∂_iΨ∂_jΨ` | **O(ε²)** |
| `−(2−K_B)𝒴−F(𝒴,𝒬)`, via `𝒴=q^{μν}∇_μφ∇_νφ` | `[(2−K_B)+F_𝒴]\,∂_iφ̃∂_jφ̃` | **O(ε²)** — the *only* place J enters |
| `F(𝒴,𝒬)` via `𝒬=g^{μν}A_μ∇_νφ` | `F_𝒬\,A_{(i}∂_{j)}φ̃` | **O(ε²)** |
| `2(2−K_B)J^μ∇_μφ`, `J_i=∂_iΨ` | `∂_{(i}Ψ∂_{j)}φ̃` | **O(ε²)** |
| `λ(A^μA_μ+1)` | `λA_iA_j` | O(ε³) |
| `−F(𝒴,𝒬)` ⊃ `½g_{ij}F` | pure trace | drops out |

**Every entry is quadratic.** Hence the traceless equation is *homogeneous at linear order for
every F(𝒴,𝒬)*; regularity plus `Φ−Ψ→0` at infinity kills the residual `a+b_ix^i` and forces

$$\boxed{\;\Phi=\Psi\ \Rightarrow\ \gamma_{\rm PPN}=1\ \text{exactly, for any }\mathcal J\;}$$

**What is actually verified, and a correction to a first draft of this section [D].** The two
statements the sympy block below establishes *without assumption* are:
(i) `𝒴 = q^{μν}∇_μφ∇_νφ` is O(ε²) **identically** (there is no background `∂_iφ̄` and `A^i=0`);
(ii) `𝒬 = g^{μν}A_μ∇_νφ` has an O(ε) piece, `−𝒬₀Ψ`, and that piece carries `g^{00}` and
**never** `g^{ij}`.
Those two alone give the boxed result: J enters only through `𝒴`, `𝒴` is quadratic, and the one
linear scalar-sector perturbation lives in the `00` sector. **Retracted from a first draft of
this section [X]:** the claim that φ reaches `g_{00}` linearly via `J^0𝒬₀` in the mixing term
`2(2−K_B)J^μ∇_μφ`. Computing `J^0` rather than positing it:
`J_0 = A^α∇_αA_0 = A^0(∂_0A_0 − Γ^j_{00}A_j) + A^i∇_iA_0`, and for static fields
`Γ^j_{00}=∂_jΨ = O(ε)` against `A_j = ∂_jζ = O(ε)`, while `A^i = O(ε)` against
`∇_iA_0 = O(ε)` — so **`J^0 = O(ε²)` and the mixing term has no linear piece at all.**
The sympy block below inserts `J^0` as a generic O(ε) symbol and is therefore *permissive*;
the true order is higher, which only strengthens the conclusion.

**So the mechanism, stated correctly [D]:** the one linear-in-ε entry of the φ/A sector into
the Einstein equations is `F_𝒬·δ𝒬 = −F_𝒬𝒬₀Ψ`, which is exactly the source of the `μ²Φ` mass
term in §8.0's eq. (2) — an independent consistency check against Verwayen et al. It requires
`𝒬₀≠0`, i.e. the Higgs/ghost-condensate phase, and it carries `g^{00}`. **There is no
background spatial vector (`A^i=0`) or background spatial gradient (`∂_iφ̄=0`) for a spatial
index to pair with, so the traceless `ij` sector has no linear source for any F.** γ=1 is a
property of the AeST background's spatial isotropy, not of J. Swapping F_dual→F_std changes
nothing here — the question posed in D7 §7 is answered: **F-independent.**

Reproduce (order counting, sympy):
```
python3 - <<'EOF'
import sympy as sp
eps=sp.symbols('epsilon',positive=True); x1,x2,x3=sp.symbols('x1 x2 x3'); X=[x1,x2,x3]
Psi=sp.Function('Psi')(x1,x2,x3); Phi=sp.Function('Phi')(x1,x2,x3)
ph=sp.Function('varphi')(x1,x2,x3); ze=sp.Function('zeta')(x1,x2,x3)
Q0,J0=sp.symbols('Q0 J0',positive=True)
Amu=[-(1+eps*Psi)]+[eps*sp.diff(ze,x) for x in X]
di=[eps*sp.diff(ph,x) for x in X]
gij=[[(1+2*eps*Phi)*sp.KroneckerDelta(i,j) for j in range(3)] for i in range(3)]
Y=sum(gij[i][j]*di[i]*di[j] for i in range(3) for j in range(3))
print(sp.Poly(sp.expand(Y),eps).monoms()[-1][0])                       # 2  -> Y is O(eps^2)
Q=-(1-2*eps*Psi)*Amu[0]*Q0+sum(gij[i][j]*Amu[i+1]*di[j] for i in range(3) for j in range(3))
print(sp.collect(sp.expand(sp.series(Q,eps,0,3).removeO()),eps))       # O(eps): -Q0*Psi (g^00 only)
mix=-(1-2*eps*Psi)*eps*J0*Q0+sum(gij[i][j]*eps*sp.diff(Psi,X[i])*di[j] for i in range(3) for j in range(3))
print(sp.collect(sp.expand(sp.series(mix,eps,0,3).removeO()),eps))     # O(eps): -J0*Q0 (no g^ij)
EOF
```

**Consequence for lensing, stated with the coefficient [D].** Photon deflection responds to
`Φ+Ψ = 2Φ`, with the *same* Φ that sets `∇Φ`-accelerations for matter. Deflection angle
`α = 4G_NM_dyn/(bc²)` with `M_dyn` the dynamical mass — GR's coefficient, no slip, no
`(1+γ)/2` factor ≠ 1. Cassini's `|γ−1|<2.3×10⁻⁵` is satisfied identically, not by a margin.
This closes the item `TARGET_D9` §0.4 asserted and `PPN_VACUITY_AUDIT` §1 flagged as vacuous.

### 8.2 β: scoped, not closed — the μ-dependence is [D], the (λ_s,K_B)-dependence is [O]

β is a 2PN coefficient (`g_{00}=-(1-2U+2βU²)`) and §8.1's table shows the AeST stress tensor
first becomes non-trivial at exactly that order. So β *is* sourced by the theory's own fields
and is not fixed by any argument in §8.1. What can be derived is **where the free function
enters, and how big that entry is.**

The only dimensionless deformation of the scalar sector away from the exactly-linear
(`J=λ_s𝒴`) case — in which the field redefinition `χ=β₀Φ̃` is exact and the system collapses
to GR with `G_N=(1+β₀)Ĝ` — is

$$\varepsilon_{\mathcal J}\equiv\frac{2\mathcal Y\mathcal J''}{\mathcal J'}
=\begin{cases}\dfrac{1}{1+x^2} & \mu_{\rm std}\\[2mm] \dfrac{1}{1+x} & \mu_{\rm dual}\end{cases}
\qquad x=\sqrt{\mathcal Y}/\tilde a_0$$

(sympy, D2 convention; `J′=λ_s√𝒴/√(𝒴+ã₀²)` and `λ_s√𝒴/(√𝒴+ã₀)` respectively).

**This is the same one-power/two-power split that decided D7 §4** — `ε_J` is O(a₀/g) for
μ_dual and O(a₀²/g²) for μ_std. Numerically:

| field point | `x=g/a₀` | `ε_J` (μ_std) | `ε_J` (μ_dual) |
|---|:-:|:-:|:-:|
| Mercury | 3.546×10⁸ | **7.95×10⁻¹⁸** | 2.82×10⁻⁹ |
| Saturn | 5.787×10⁵ | **2.99×10⁻¹²** | 1.73×10⁻⁶ |

**Statement, with the label split [D]/[C]:** `ε_J` itself is **[D]** (sympy, above). The *inference* that β's J-dependence is multiplicatively O(ε_J) is **[C]**: it rests on the premise that the exactly-linear case `J=λ_s𝒴` collapses to GR-with-rescaled-`G` at **2PN**, whereas that collapse is established here only for the **linear quasistatic** system. This is precisely the genus of error §7.4 committed, so it is labelled, not smuggled. Under that premise: *the free function's contribution to β−1 is suppressed by ε_J, i.e.
`≲10⁻¹⁷` at Mercury for μ_std, against the MESSENGER bound `|β−1|<2.3×10⁻⁴`. β is not where
the choice of μ can break this theory.* **Open [O]:** the remaining, J-independent part of
β−1 is a function of `(λ_s,K_B)` alone, and it is **not computed** here or anywhere in the
corpus. It requires the O(ε²) `00` Einstein equation with the vector stress `K_B(∇Ψ)²`, the
scalar stress `λ_s(∇χ)²` and the `𝒬`-sector `𝒦₂` term carried consistently — a genuine 2PN
AeST calculation that Verwayen et al. do not perform (§8.0) and SZ do not perform.

**Honesty note, against the §7.4 precedent.** §7.4 bounded `|γ−1|` by an expansion parameter
and was wrong, because the physically dangerous object was a *force that does not decay with
r*, not a relative metric correction. The bound above is explicitly a bound on the *relative*
J-dependence of a 2PN coefficient, and the non-decaying-force question is handled separately
and exactly in §8.4 — where it turns out the residual force **grows** as r², which is why §8.4
and not §8.2 carries the binding constraint.

### 8.3 α₁, α₂: the Foster–Jacobson formulas are **not applicable** at AeST's couplings [D]+[C]

AeST's vector sector is exactly the Maxwell combination (D7 §6 step 3):

$$c_1=\tfrac{K_B}{2},\quad c_3=-\tfrac{K_B}{2},\quad c_2=c_4=0
\ \Longrightarrow\ c_{13}=0,\ c_{123}=0,\ c_{14}=\tfrac{K_B}{2}$$

**Validation of the coupling map [D].** Einstein-aether mode speeds at this locus:
`s₂²=1/(1−c₁₃)=1` (spin-2, luminal — reproduces D7 §6's `c_T=c` independently);
`s₁²=(2c₁−c₁²+c₃²)/(2c₁₄(1−c₁₃))=2c₁/(2c₁)=1` (spin-1, luminal);
`s₀²∝c₁₂₃=0` — **the spin-0 aether mode has vanishing speed.**

Foster & Jacobson (gr-qc/0509083), as quoted in Jacobson arXiv:0801.1547 eqs. (2.2)–(2.3):

$$\alpha_1=\frac{-8(c_3^2+c_1c_4)}{2c_1-c_1^2+c_3^2},\qquad
\alpha_2=\frac{\alpha_1}{2}-\frac{(c_1+2c_3-c_4)(2c_1+3c_2+c_3+c_4)}{c_{123}(2-c_{14})}$$

Substituting AeST's values: `α₁ = −8c₁²/(2c₁) = −4c₁ = −2K_B`, and **`α₂` diverges** (`c₁₂₃=0`).

**Jacobson names this exact case and disqualifies the calculation [C].** arXiv:0801.1547 §8,
verbatim: *"The first case to be examined in detail was c₁₃=c₂=c₄=0, i.e. the 'Maxwell action'
(with the unit constraint on the vector). The PPN result for α₂ (2.3) is infinite in this case,
and the spin-0 mode speed is zero. **The perturbation series used in the PPN analysis is thus
evidently not applicable.**"*

**Therefore [D]:**
1. `α₁=−2K_B` and `α₂=∞` are **not predictions of AeST**. They are the readings of a formula
   evaluated outside its domain of validity, and the divergence is the diagnostic saying so.
   Any future use of FJ's α₁,α₂ for this corpus is an error. **[X]** for the substitution.
2. **The degeneracy is lifted in AeST, but by the scalar, not by the vector.** The vanishing
   spin-0 aether speed is exactly the gap that `φ` fills: the mixing `2(2−K_B)J^μ∇_μφ` plus
   the `𝒦₂(𝒬−𝒬₀)²` term supplies a *massive* spin-0 mode of mass `μ` (`μ⁻¹≳1` Mpc, hence
   effectively long-range across the solar system). AeST's spin-0 sector is φ. So the PPN
   perturbation series that fails for pure æ-theory at `c₁₂₃=0` is expected to exist for AeST —
   **but it is a different series, and nobody has expanded it.**
3. **α₁,α₂ remain genuinely [O], with a now-precise obstruction:** they live in the `g_{0i}`
   sector with the aether boosted at velocity `w` relative to the matter rest frame. AeST has
   a real preferred frame (the aether *and* `𝒬₀≠0` breaking boosts), so they are not expected
   to vanish identically. **No published AeST solution has a `g_{0i}` sector** — SZ's PRL is
   quasistatic-diagonal, Verwayen et al. (§8.0) is quasistatic-spherical-diagonal. A static
   spherically symmetric solution *cannot in principle* yield α₁ or α₂. Closing this needs an
   ab initio AeST 1.5PN computation, which is new work, not a citation.
4. **Conditional, if and only if the scalar's contribution to the `0i` sector turns out
   subleading [C]:** `α₁≈−2K_B` with LLR `|α₁|≲10⁻⁴` would give `K_B≲5×10⁻⁵`. `K_B→0` is a
   regular limit of AeST (`G̃=(1−K_B/2)Ĝ`), so this is *not* fatal if it holds — but item 1
   says the premise is unsupported, so this is flagged and not carried. **[C]**

### 8.4 The binding solar-system constraint, and the first bound on λ_s [D]

With `λ_s` restored, the μ_std residual is **not** `a₀²/2ĝ`. `TARGET_D1_SUPPLEMENT` §4 solved
`μ_std(g_χ/a₀)g_χ=ĝ`, which is the `λ_s→0` limit. The correct spherical first integral of the
§8.0 system (μ→0) is `J′(𝒴)χ′ = ĜM/r²` with `Ĝ=G_N/(1+β₀)`:

$$\lambda_s\frac{g_\chi^{2}}{\sqrt{g_\chi^{2}+\tilde a_0^{2}}}=\hat g,\qquad
\hat g=\frac{\lambda_s}{1+\lambda_s}g_N,\qquad g=\hat g+g_\chi$$

Matching the deep-MOND limit `g→√(G_NMa₀)/r` fixes the scale inside J:

$$\tilde a_0=(1+\lambda_s)\,a_0$$

— **the identical relation D7 §2.2 derived for F_dual; it transfers to F_std unchanged [D].**
Expanding the first integral at large `ĝ`:

$$\boxed{\;\delta g\equiv g-\frac{G_NM}{r^2}=\frac{(1+\lambda_s)^{3}a_0^{2}}{2\,g_N}
=\frac{(1+\lambda_s)^{3}a_0^{2}r^{2}}{2G_NM}\;}$$

Verified by exact 50-digit `mpmath` Newton solve (not asymptotics) at
`λ_s = 0.001, 0.1, 1, 2.695, 10`: exact/analytic ratio `1.000000000000` to 12–14 digits.

**The residual grows as r².** Expressed as a Cassini-type quadrupole scale `Q₂≈δg/r ∝ r`, the
margin therefore *shrinks linearly with orbital radius* — Mercury is the **weakest** test, not
the strongest, which inverts `TARGET_D1_SUPPLEMENT` §4's framing. At `λ_s→0` (most permissive),
`a₀=1.116×10⁻¹⁰` m s⁻² (SPARC), `Q₂ < 3.4×10⁻²⁷` s⁻²:

| field point | r (AU) | g_N (m s⁻²) | δg (m s⁻²) | Q₂ᵉᑫ=δg/r (s⁻²) | margin | **λ_s ≤** |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| Mercury | 0.387 | 3.957×10⁻² | 1.574×10⁻¹⁹ | 2.717×10⁻³⁰ | 1251 | 9.78 |
| Earth | 1.000 | 5.930×10⁻³ | 1.050×10⁻¹⁸ | 7.020×10⁻³⁰ | 484 | 6.85 |
| Mars | 1.524 | 2.554×10⁻³ | 2.438×10⁻¹⁸ | 1.070×10⁻²⁹ | 318 | 5.83 |
| Jupiter | 5.204 | 2.189×10⁻⁴ | 2.844×10⁻¹⁷ | 3.653×10⁻²⁹ | 93.1 | 3.53 |
| **Saturn (Cassini)** | **9.583** | **6.458×10⁻⁵** | **9.643×10⁻¹⁷** | **6.727×10⁻²⁹** | **50.5** | **2.70** |
| Uranus | 19.22 | 1.606×10⁻⁵ | 3.878×10⁻¹⁶ | 1.349×10⁻²⁸ | 25.2 | 1.93 |

**The Q₂ mapping is the weak link, so the bound is cross-checked by a second observable [D].**
`Q₂ᵉᑫ = δg/r` treats a *monopole* correction (`δg ∝ r²` is spherically symmetric, `∇²δΦ = −4kr ≠ 0`,
i.e. an effective source density) as if it were the *anisotropic* quadrupole coefficient Hees
et al. bound. That mapping is inherited from D7 §4.3, where it was applied to a constant force
and where a 5.7×10⁵ kill survives a factor-few error. Here the margin is 50× and `λ_s^max` is
its cube root, so the mapping carries the whole result — the same structural move as the
corpus's twice-retracted "1137×". It therefore needs an independent route.

**Route 2: anomalous perihelion precession.** For `δg = k r^n` added to `G_NM/r²`, near-circular
apsidal precession per orbit is `Δϖ = π(n+2)\,δg(r)/g_N(r)`. **Formula self-check:** at `n=0`
this is `2π ã₀r²/G_NM`, which is D7 §4.3's μ_dual formula verbatim, and evaluating it at
Mercury returns **1.517 arcsec/century** against D7 §4.3's 1.52 — the formula is validated
against the corpus's own prior calculation. For μ_std, `δg ∝ r²` so **n=2 and the coefficient
is 4π, not 2π**:

$$\Delta\varpi=\frac{4\pi\,\delta g}{g_N}=\frac{2\pi(1+\lambda_s)^{3}a_0^{2}r^{4}}{(G_NM)^{2}}
\quad\Longrightarrow\quad \dot\varpi\ \propto\ r^{5/2}$$

| field point | Δϖ̇ (arcsec/cy), λ_s→0 | ephemeris bound used | margin | **λ_s ≤** |
|---|:-:|:-:|:-:|:-:|
| Mercury | 4.28×10⁻⁹ | 3×10⁻⁵ | 7009 | 18.1 |
| Earth | 4.59×10⁻⁸ | 1×10⁻⁴ | 2179 | 12.0 |
| Mars | 1.32×10⁻⁷ | 5×10⁻⁶ | 38.0 | 2.36 |
| **Saturn** | **1.31×10⁻⁵** | **1×10⁻⁴** | **7.61** | **0.97** |

**The two routes agree on the structure and on the order [D]; they differ by ~2.8× in λ_s [C].**
Saturn binds under both (`r^{5/2}` is even more outer-planet-weighted than `Q₂ᵉᑫ ∝ r`), Mercury
is the *least* constraining point under both, and both land at `λ_s = O(1)`. **Honest labelling:
the existence of an O(1) upper bound on λ_s is [D]; the specific number is [C]** — the Q₂ route
because of the monopole/quadrupole mapping, the precession route because the supplementary-
precession bounds above are order-of-magnitude ephemeris values without provenance in this repo.
**Quote `λ_s ≲ 1–3`, binding at Saturn, and take `λ_s ≲ 1` if a single conservative number is
needed.** Handing the ephemeris bounds to the falsifier for a provenance-compliant replacement.

**Why any bound is defensible at all: the signal is not degenerate with the fitted parameters [D].**
`δg ∝ r²` has a radial profile orthogonal to everything absorbed in an ephemeris fit — a
mis-estimated `GM_⊙` is `r⁻²`, a solar `J₂` is `r⁻⁴`, a cosmological-constant term is `r¹`, and
the MOND external-field quadrupole is `r¹` *and* anisotropic. An `r²` monopole cannot be
reabsorbed into any of them, which is what makes the growth with `r` a genuine signal rather
than a fitting artefact.

**Two results [D]:**
- μ_std's margin at the field point where the Cassini `Q₂` datum actually lives (Saturn, where
  Cassini was) is **50×, not 1300×.** The 1300× figure is Mercury-specific and is the most
  favourable point in the solar system. `TARGET_D1_SUPPLEMENT` §4.1 should be read with that
  correction; the verdict (μ_std survives, μ_dual does not) is unchanged and the contrast is
  still 4–5 orders of magnitude, since μ_dual's residual is `≥a₀` at *every* radius.
- **First upper bound on λ_s in this corpus: `λ_s = O(1)`, binding at Saturn** — `≲2.7` by the
  `Q₂ᵉᑫ` route, `≲1.0` by the precession route. D7 §2.2 recorded `λ_s∈(0,∞)` unfixed by the MOND
  limit **[O]**; this closes the upper half. At `λ_s≲1`: `G_N/Ĝ = 1+1/λ_s ≳ 2` and
  `ã₀ = (1+λ_s)a₀ ≲ 2a₀`. Existence of the bound **[D]**, the number **[C]** (see above). The
  lower half is still open.

Reproduce:
```
python3 - <<'EOF'
from mpmath import mp,mpf,sqrt,findroot
mp.dps=50; a0=mpf('1.116e-10'); GM=mpf('1.32712440018e20'); AU=mpf('1.495978707e11')
def dg(r,ls):
    gN=GM/r**2; gh=gN*ls/(1+ls); at=(1+ls)*a0
    g=findroot(lambda g: ls*g**2/sqrt(g**2+at**2)-gh, gh/ls+ls*at**2/(2*gh))
    return (gh+g)-gN, (1+ls)**3*a0**2/(2*gN)
for ls in ['0.001','0.1','1','2.695','10']:
    e,a=dg(mpf('0.38710')*AU,mpf(ls)); print(ls, mp.nstr(e/a,14))          # 1.0000000000000
for nm,au in [("Mercury",'0.38710'),("Earth",'1.0'),("Jupiter",'5.2044'),("Saturn",'9.5826')]:
    r=mpf(au)*AU; d=a0**2/(2*(GM/r**2)); m=mpf('3.4e-27')/(d/r)
    print(nm, mp.nstr(d,5), mp.nstr(d/r,5), float(m), float(m**(mpf(1)/3)-1))
EOF
```

### 8.5 Ledger

| claim | tag | basis |
|---|:-:|---|
| Verwayen et al. arXiv:2304.05134 state Φ=Ψ for the general J; contains no `g_{0i}`, no PPN, no β | [C] | §8.0, PDF retrieved 2026-09-12 |
| Every source of the traceless `Σ_ij` in AeST is O(ε²); the `ij` equation is homogeneous at linear order | **[D]** | §8.1 table + sympy |
| ⇒ Φ=Ψ, γ_PPN=1 **exactly, for every F(𝒴,𝒬)** — F_dual and F_std alike | **[D]** | §8.1 |
| The mechanism is spatial isotropy of the background (`A^i=0`, `∂_iφ̄=0`), not J | **[D]** | §8.1 |
| `J^0 = O(ε²)`: the mixing term `2(2−K_B)J^μ∇_μφ` has **no** linear piece — first-draft claim retracted | **[X]**→**[D]** | §8.1 |
| The one linear φ/A entry is `F_𝒬δ𝒬 = −F_𝒬𝒬₀Ψ`, = the `μ²Φ` mass term of §8.0 eq. (2) | **[D]** | §8.1 |
| Lensing: `Φ+Ψ=2Φ`, `α=4G_NM_dyn/bc²`, no slip — Cassini γ satisfied identically | **[D]** | §8.1 |
| `ε_J=2𝒴J″/J′ = 1/(1+x²)` (μ_std) vs `1/(1+x)` (μ_dual) | **[D]** | §8.2, sympy |
| `ε_J` computed | **[D]** | §8.2, sympy |
| Inference that β's J-dependence is multiplicatively O(ε_J) ⇒ ≲10⁻¹⁷ at Mercury | **[C]** | §8.2 — premise: `J=λ_s𝒴` collapses to GR-with-rescaled-G at 2PN, shown only for the linear system |
| The (λ_s,K_B) part of β−1 | **[O]** | §8.2 — genuine 2PN AeST calc, unattempted anywhere |
| AeST vector locus `c₁=−c₃=K_B/2, c₂=c₄=0` ⇒ `c₁₃=c₁₂₃=0`; `s₁²=s₂²=1`, `s₀²=0` | **[D]** | §8.3 |
| FJ substitution gives `α₁=−2K_B`, `α₂=∞` — **not a prediction**, the series is inapplicable | **[X]** | §8.3; Jacobson arXiv:0801.1547 §8 verbatim |
| AeST lifts the degeneracy via the scalar (massive spin-0, mass μ), so a PPN series exists — but is a different one, unexpanded | **[D]**/**[O]** | §8.3 |
| α₁,α₂ need an ab initio AeST 1.5PN `g_{0i}` computation; no published AeST solution has a `g_{0i}` sector | **[O]** | §8.3 |
| `α₁≈−2K_B` ⇒ `K_B≲5×10⁻⁵`, *only if* the scalar's `0i` contribution is subleading | **[C]** | §8.3 item 4 |
| `ã₀=(1+λ_s)a₀` transfers from F_dual to F_std unchanged | **[D]** | §8.4 |
| `δg=(1+λ_s)³a₀²/(2g_N)`, confirmed by exact 50-digit solve at five λ_s | **[D]** | §8.4 |
| Residual **grows as r²**; Mercury is the weakest test, Saturn the binding one | **[D]** | §8.4 |
| μ_std margin at Saturn = **50×**, not the 1300× quoted for Mercury in `TARGET_D1_SUPPLEMENT` §4.1 | **[D]** | §8.4 |
| `Δϖ = π(n+2)δg/g_N`; at n=0 returns D7 §4.3's 1.52 arcsec/cy for μ_dual (formula self-check) | **[D]** | §8.4 |
| μ_std precession Δϖ̇ ∝ r^{5/2}; Saturn 1.31×10⁻⁵ arcsec/cy | **[D]** | §8.4 |
| `δg ∝ r²` is a **monopole**; `Q₂ᵉᑫ=δg/r` against an anisotropic-quadrupole bound is the weak link | **[D]** | §8.4 |
| `r²` profile not degenerate with `GM_⊙`(r⁻²), `J₂`(r⁻⁴), Λ(r¹) or the MOND EFE quadrupole(r¹, anisotropic) | **[D]** | §8.4 |
| **Existence of an O(1) upper bound on λ_s**, binding at Saturn — first in this corpus | **[D]** | §8.4 |
| The number: `λ_s ≲ 2.7` (Q₂ route) / `≲1.0` (precession route); quote `λ_s ≲ 1–3` | **[C]** | §8.4 — mapping + bound provenance |

### 8.6 Verdict

**γ is closed and it is closed structurally.** `Φ=Ψ` follows from the fact that every
`g^{ij}`-dependent term in the AeST action is quadratic in the perturbations, which in turn
follows from `A^i=0` and `∂_iφ̄=0` on the background — the free function J never appears in
the traceless `ij` equation at linear order. So `γ_PPN=1` exactly, the lensing amplitude is
GR's `4G_NM_dyn/bc²` with `M_dyn` the *dynamical* mass, and the answer to D7 §7's question is
**F-independent: the equality does not care whether you picked F_dual or F_std.** **[D]**,
corroborated by two published sources. **β is scoped but not closed:** the free function's
entry is suppressed by `ε_J=1/(1+x²)≲10⁻¹⁷`, so μ_std cannot break β, but the `(λ_s,K_B)`
part is a real 2PN computation nobody has done. **[O]** **α₁,α₂ are still open, and the
obstruction is now named precisely rather than merely noted:** AeST's vector couplings sit on
the `c₁₂₃=0` Maxwell locus where Foster–Jacobson's PPN expansion is, in Jacobson's own words,
"evidently not applicable" — the spin-0 aether speed vanishes — so the corpus's plan of
citing FJ was never going to work; AeST fills that mode with the scalar, and the resulting
`g_{0i}` expansion has never been written down by anyone. **The single tightest *evaluable*
obstruction is therefore §8.4**: μ_std's residual force `(1+λ_s)³a₀²/2g_N` grows as `r²`, so
the binding test is Saturn rather than Mercury, the margin there is **50×** (`Q₂ᵉᑫ` route) or **7.6×**
(perihelion-precession route) rather than the 1300× the corpus currently quotes, and requiring
it gives the first real constraint on the tracking slope, **`λ_s = O(1)`** — `≲2.7` and `≲1.0`
by the two routes. The *existence* of that bound is **[D]**; the number is **[C]**, limited by
the monopole-vs-quadrupole mapping in the first route and by ephemeris-bound provenance in the
second. Handing off: the exact numerics above to the falsifier; the
Lean statement `Φ=Ψ ⇐ A^i=0 ∧ ∂_iφ̄=0`, whose substitutability test is whether it still closes
when the background is given a spatial aether component, to the formalizer.
