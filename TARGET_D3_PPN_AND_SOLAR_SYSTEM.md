# TARGET D3: PPN Limits and Solar System Constraints

**Status:** D3_OPEN_FAILING — the D7/D9 action mismatch flagged in §7.1 is now **fixed** (D7 rewritten to AeST, 2026-09-12). Under AeST, Ψ=Φ exactly ⇒ γ=1 with no slip, so §7.3–§7.5's γ,β margins bound a null observable [X]. The binding constraint is **not** α₁,α₂ but the interpolation tail: μ(x)=x/(1+x) leaves a constant anomalous acceleration ≥ a₀ (D7 §4.2), failing Mercury by ~10³ and Cassini Q₂ by 5.7×10⁵.
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
