# TARGET D2 SUPPLEMENT: Structural uniqueness of μ_std = x/√(1+x²)

**Status:** RESULT — a uniqueness theorem of the same *shape and rigor* as `TARGET_D2`
Theorem 9.1/9.2 is established for μ_std. It is a **postulate swap, not a derivation from
nothing** — exactly the trade `TARGET_D2` §9.2 confessed for μ_dual. Read §6 before citing.
**Last updated:** 2026-09-12
**Tags:** `[P]` proved · `[D]` derived here · `[C]` cited/conjectured · `[O]` open · `[X]` killed

Answers `TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md` §2 and §7 item 1, and
`PEER_REVIEW_READINESS.md` critical-path item #1.

---

## 0. One-sentence result

**μ_dual and μ_std are the *same* structure read in two different coordinates on the same
two-state family:** D2's odds/Fisher argument in the **presence** coordinate `p∈(0,1)` gives
`x/(1+x)`; in the **chirality** coordinate `m∈(−1,1)` — where the rectification is `artanh`,
i.e. rapidity — it gives `x/√(1+x²)` uniquely, with no rational ansatz and no degree
minimality, and with `μ′(0)=1` doing exactly the selection job it does in D2 Theorem 9.3.
The coordinate is not free (§5): it is fixed by whether `μ→0` means the channel is *absent*
or merely *unpolarized*. A chiral channel cannot be absent. That is the whole argument, and
it is `[C]`, not `[P]`.

---

## 1. Convention warning — FIX REQUIRED IN THE D1 SUPPLEMENT `[X]`

Two different objects are called `F_std` in this corpus:

| source | definition | convention |
|---|---|---|
| `TARGET_D2` §3 | `F_std(x) = ½[x√(1+x²) − arsinh x]` | `F′(x) = x·μ(x)` |
| `TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md` §1 | `F_std(x) = √(1+x²) − 1` | `F′(x) = μ(x)` |

The AQUAL action `S = −(a₀²/8πG)∫F(|∇Φ|/a₀)d³x` yields `∇·[μ∇Φ]=4πGρ` **only** under
`F′ = xμ` (D2 §4 Corollary). Measured discriminators (sympy, §7):

```
D2 : F/x² → 1/2 (C3 ✓),  F/x³ → 1/3 (C4 ✓),  J(𝒴) ~ (2λ_s/3a₀)·𝒴^{3/2}   ✓ deep-MOND
D1s: F/x² → 0   (C3 ✗),  F/x³ → ∞   (C4 ✗),  J(𝒴) ~ λ_s·𝒴                ✗ linear
```

`√(1+x²)−1` fails D2's own C3 and C4 and gives a **linear** `J(𝒴)`, i.e. no deep-MOND limit.
`TARGET_D1_SUPPLEMENT` §1, §3 (Legendre dual) and §5 (ghost-free conditions) are computed on
the wrong-normalization object. **§4 (the exact Mercury solve) is unaffected** — it uses
`μ_std(g_φ/a₀)·g_φ = ĝ` directly, which does not reference `F`'s normalization.

**§5's conclusion survives and improves — error in derivation, not in verdict `[D]`.**
Redone correctly with `J(𝒴)=2λ_s a₀²F(√𝒴/a₀)`, `u=√𝒴/a₀`, `F′=uμ` (sympy, §7):

```
F''(x)      = x(2+x²)/(1+x²)^{3/2}                  > 0  ∀x>0   (convex, ghost-free)
J'(𝒴)       = λ_s √𝒴/√(𝒴+a₀²) = λ_s μ(u)            > 0,  → λ_s as 𝒴→∞  (correct Newtonian limit)
J'+2𝒴J''    = λ_s √𝒴(𝒴+2a₀²)/(𝒴+a₀²)^{3/2}          > 0  ∀𝒴>0
```

Both `TARGET_D7` §5 conditions hold, and `J′→λ_s` is the *right* Newtonian limit where the
D1-supplement's normalization wrongly gave `J′→0`. **§3's Legendre dual is dead, not
rescaled:** `p = F′ = x²/√(1+x²) → ∞`, so the conjugate momentum is unbounded and the `(0,1)`
inversion and `H=(1−p²)^{−1/2}−1` do not survive in any form. `[X]`

Everything below uses D2's convention `F′(x) = x·μ(x)`.

---

## 2. The generating observation `[D]`

`μ_std` is exactly the composite `tanh ∘ arsinh`:

$$\mu_{\rm std}(x) = \tanh(\operatorname{arsinh} x) = \frac{x}{\sqrt{1+x^2}}$$

Set `x = sinh ψ`. Then `μ = tanh ψ`, `√(1+x²) = cosh ψ`. In Lorentz language: **`x` is the
celerity (proper velocity, `γβ`) and `μ` is the velocity (`β`) of one and the same boost of
rapidity `ψ`.** Equivalently `μ_std = x/γ(x)` — the interpolating function *is* the internal
time-dilation factor.

This is not an analogy imported from outside: the additive-rapidity structure
`ψ = artanh(·)` is already the object of `06_unification_and_spin/rapidity_uniqueness_proof.py`
and `arctanh_derivation_chain.py` (CLM-10). **Caveat, stated inline as required:** CLM-10 is
state `conditional` in `assurance/claims.json`, its own script header disclaims that Kerr spin
*is* a Lorentz rapidity, and `sinh ψ = 1` is not selected by any covariant argument. It is
cited here as evidence that the rapidity rectification is *native to this corpus*, not as proof.

---

## 3. Theorem A — rapidity conjugacy forces μ_std `[D]`

**Postulate R (rapidity conjugacy).** Let `ψ ≡ artanh μ` be the rapidity of the internal
channel. Then the dimensionless squared acceleration is conjugate to the rapidity:

$$\frac{dF}{d\psi} = x^2 .$$

(`x² = 𝒴/a₀²` is the kinetic invariant the field action actually depends on, which is why the
conjugate variable is `x²` and not `x`.)

**Theorem A `[D]`.** Postulate R together with D2's constraint 1 (`F′(x)=x μ(x)`) and
`μ′(0)=1` determines `μ` uniquely:

*Proof.* By the chain rule `dF/dψ = (dF/dx)(dx/dψ) = x·tanh ψ·x′(ψ)`. Setting this equal to
`x²` gives

$$\frac{x'(\psi)}{x(\psi)} = \coth\psi \;\Longrightarrow\; x(\psi) = C\sinh\psi .$$

(sympy `dsolve` returns `C₁ e^ψ tanh ψ/(1+tanh ψ) ≡ C₁ sinh ψ`.) `μ′(0)=1` fixes `C=1`.
Hence `μ = tanh ψ = x/√(1+x²)`, and

$$F(\psi)=\int \sinh^2\psi\,d\psi = \tfrac12(\sinh\psi\cosh\psi-\psi)
\;\Longrightarrow\; F(x)=\tfrac12\!\left[x\sqrt{1+x^2}-\operatorname{arsinh}x\right] \;\square$$

**This is verbatim `TARGET_D2` §3's own `F_std`** — written down there four weeks earlier as a
*counterexample* to C1–C5 uniqueness, now recovered as the unique solution of a structural
condition. Symbolic residual `F(ψ)|_{ψ=arsinh x} − F_std(x) = 0` (sympy, §7).

---

## 4. Theorem B — the chiral Fisher identity `[D]`

D2 §7 identity: `F′(x)²·ℐ(μ) = x³` with `ℐ(p) = 1/(p(1−p))`, the Fisher information of a
**`{0,1}` Bernoulli** in its mean. Its canonical parameter is the logit, `η = ln(p/(1−p))`,
whose exponential is the odds — hence `odds(μ)=x` and hence Padé[1/1].

Change coordinate (see §5 — this is a reparametrization of the *same* family, not a new one).
In the **chirality/magnetization** coordinate `m ∈ (−1,1)` the canonical parameter is `h` with
`m = tanh h` — *the rapidity* — and the Fisher information is

$$\mathcal I_\pm(m) = \frac{1}{1-m^2} = \gamma^2 .$$

**Theorem B `[D]`.** With `ℐ_±`, the D2 identity becomes, uniquely,

$$\boxed{\;F'(x)^2\,\mathcal I_\pm(\mu(x)) = x^4 \iff \frac{\mu^2}{1-\mu^2}=x^2
\iff \mu(x)=\frac{x}{\sqrt{1+x^2}}\;}$$

*Proof.* `F′=xμ` gives `x²μ²/(1−μ²) = x⁴`, i.e. `μ² = x²(1−μ²)`; sympy `solve` returns the
single positive root `x/√(1+x²)`. Verified forward: `F_std′(x)²/(1−μ_std²) = x⁴` exactly. `□`

No rational ansatz, no degree minimality — the exact analogue of D2 Theorem 9.2.

**Theorem C (exponent selection, analogue of D2 Thm 9.3) `[D]`.**
`F′(x)²ℐ_±(μ) = x^k ⟺ μ_k(x) = x^{(k−2)/2}/√(1+x^{k−2})`. Measured `μ′(0)`:

| k | 3 | **4** | 5 | 6 |
|---|---|---|---|---|
| μ_k | √x/√(1+x) | **x/√(1+x²)** | x^{3/2}/√(1−x+x²)√(1+x) | x²/√(1+x⁴) |
| μ′(0) | ∞ | **1** | 0 | 0 |

`μ(0)=0` and `μ(∞)=1` hold for every `k≥3`; **only `μ′(0)=1` selects `k=4`** — precisely the
role `μ′(0)=1` plays in D2 Theorem 9.3, where it selects `n=1`. The selection principle is
unchanged; only the coordinate moved.

**Theorem D (equivalence — do not double-count) `[D]`.** Postulate R, Theorem B's identity,
and the statement "`x` is the celerity of `μ`" are *the same postulate* in three dresses.
`TARGET_D2` was cautioned for presenting its §6 and §7 as independent corroborations; the same
warning applies here with equal force. **§3 and §4 are one result, not two.**

---

## 5. Why the chiral coordinate, and not the presence coordinate `[C]`

This is the one substantive physical input, and it is the honest crux. It must be stated
carefully, because the obvious framing ("a different alphabet") is **wrong**.

**`{0,1}` and `{−1,+1}` are the same two-state exponential family `[D]`**, related by
`m = 2p−1`. Fisher information is not a scalar under reparametrization:

$$\mathcal I_\pm(m)=\mathcal I(p)\left(\tfrac{dp}{dm}\right)^2=\frac{1}{p(1-p)}\cdot\tfrac14=\frac{1}{1-m^2},
\qquad \operatorname{logit}p = 2\operatorname{artanh}m .$$

So `ℐ_±` is **not a new channel's** Fisher information — it is D2's, written in a different
coordinate on the same manifold. The canonical parameters agree up to a factor 2.

**The objection this exposes, stated against ourselves `[O]`:** if the coordinate is free,
`F′²·ℐ_u(μ)=x^k` has *no invariant content*. Choose `ℐ_u(μ) := x(μ)^{k−2}/μ²` and solve
`(dp/du)² = ℐ_u/ℐ(p)` for the reparametrization, and any target `μ` can be manufactured.
**The identity selects nothing until the coordinate is independently fixed.** This objection
applies with equal force to `TARGET_D2` §7 and to §4 above; it is the sharpest form of D2's
own Q1′ and it was not visible in the Padé framing.

**What fixes the coordinate — the physical claim `[C]`:** the two coordinates differ in what
the deep-MOND limit `μ→0` *means*.

| coordinate | `μ→0` reads as | rectification | selected μ |
|---|---|---|---|
| presence `p ∈ (0,1)` | the channel is **absent** | odds `p/(1−p)` | `x/(1+x)` |
| chirality `m ∈ (−1,1)` | the channel is **unpolarized** (equal ±) | rapidity `artanh m` | `x/√(1+x²)` |

A `±1` chiral degree of freedom **cannot be absent — only unpolarized.** If the internal
channel is chiral (SU(2)→SO(3) double cover; the `V₂(ℝ³)`/Cartan-triality substrate), then
`m`, not `p`, is the physically meaningful coordinate, its `x→0` limit is the unpolarized
state, and `μ_std` follows. This is a statement about the `x→0` boundary condition, not an
aesthetic choice of parametrization — which is exactly why it can carry weight the Fisher
identity alone cannot.

> **The claim, stated exactly:** *given* that the interpolation variable is the polarization
> of a chiral `±1` channel (so that `μ→0` is *unpolarized*, not *absent*), μ_std is forced by
> the same Fisher/rectification argument that forces μ_dual under the presence reading.
> `[D]` for the implication; `[C]` for the identification of the channel as chiral.

**Not evidence — explicitly withdrawn:** `TARGET_D2` §8's "**dual-channel**" decomposition is
*not* support for this. There, "dual channel" means `F = F_Newton − F_correction`, two
**additive terms in the action**, not a ±1 polarization. Worse, `F_std` has no clean two-term
split at all (§6.1, `TARGET_D1_SUPPLEMENT` §3) — so D2 §8 is a constraint `F_std` *fails*,
not a corroboration. Equivocating on the word "dual" would be the error CLAUDE.md's D41
precedent exists to prevent.

---

## 6. What is NOT derived `[O]` — read before citing

0. **D2 constraint 4 is DROPPED, not satisfied.** Theorem 9.1 had four constraints. This
   document's theorem uses constraint 1 (constitutive), **replaces** constraint 2 (Padé
   minimality) with Postulate R, keeps constraint 3's `μ′(0)=1`, and **abandons constraint 4**
   (the additive `F = F_Newton − F_correction` split) as unsatisfiable for `F_std` — consistent
   with `TARGET_D1_SUPPLEMENT` §3's `[O]`. "Same shape as Theorem 9.1" would overclaim.
   Accurate statement: **replaces constraint 2, drops constraint 4.** `[O]`
1. **The Fisher identity alone has no invariant content** — §5's reparametrization objection.
   The coordinate must be fixed physically first; the identity then records the consequence.
   This applies retroactively to `TARGET_D2` §7. `[O]`
2. **Postulate R / the chiral coordinate is an input.** This is a postulate swap of the same kind
   D2 §9.2 performed (Padé minimality → `odds(μ)=x`). It is *smaller and better-motivated*
   than "μ is a Padé[1/1] function" — it is a statement about the channel's alphabet, which
   the substrate arguably fixes — but it is not derived from the action. `[O]`
3. **`μ′(0)=1` remains an input**, exactly as in D2 Theorem 9.3. No gain in parsimony is
   claimed. `[O]`
4. **No covariant argument yet.** D2's Q3 (does the Skordis–Złośnik/AeST embedding *force*
   `μ`?) is untouched. That remains the only route that would make this physical rather than
   chosen. `[O]`
5. **`sinh ψ = 1 → μ = 1/√2 = θ`.** True algebraically (CLM-10). **Do not build on it.** The
   `u ≥ γ ⟺ χ ≥ θ` anti-drift gate is **retracted (2026-09-03)**; `Res-Nova/CLAUDE.md` and
   §VI record that θ is a **ceiling, not a gate**, and it names `μ(x)=x/√(1+x²)` in that same
   retraction. Noting the coincidence; asserting nothing from it. `[O]`

### 6.1 Convention artifacts, logged per the D41 precedent (do not rediscover)

Two attractive readings attach to the **wrong-normalization** object `√(1+x²)−1` (§1) and are
therefore **not** results about the AQUAL action:

- **Relativistic kinetic energy / Born–Infeld:** `√(1+x²)−1 = cosh ψ − 1 = γ−1`. Elegant, and
  it is what the `dF/dψ = x` (rather than `x²`) conjugacy produces — but it fails C3/C4. `[X]`
- **Unruh–de Sitter (Milgrom 1999):** the de Sitter Unruh temperature `T(a) ∝ √(a²+a_dS²)`
  gives `2πc[T(a)−T(0)]/a₀ = √(1+x²)−1` exactly. Same wrong-normalization object; and Milgrom
  1999 is **modified inertia**, a different slot from the AQUAL field action — do not merge
  them. What *does* survive normalization-independently is the statement
  `μ_std = x/γ(x) = a/(2πc·T(a)/T(0))·...`, i.e. **μ_std is the acceleration measured in units
  of the de Sitter–Unruh temperature excess.** `[C]`, worth pursuing under Q3.
- **Score function:** `exp(−√(1+x²))` (the symmetric hyperbolic / Barndorff-Nielsen density)
  has score `−μ_std`. Also the `F′=μ` object. `[C]`, no weight placed on it.

### 6.2 Fine-structure-constant watch — NEGATIVE

**α ≈ 1/137.036 does not appear anywhere in this derivation.** No coupling, no ratio, no
exponent. The only distinguished dimensionless numbers that arise are `2` (the `x²` conjugate,
the `k=4` exponent), `1/√2` (§6 item 4), the silver ratio `1+√2` (CLM-10), and — **only if the
Unruh route of §6.1 is pursued** — a factor `2π`: the de Sitter Unruh crossover sits at
`a_dS = cH₀`, whereas this repo's canonical `a₀ = cH₀/2π`. That `2π` offset is a real,
unexplained discrepancy in the Unruh reading and is flagged as such. Nothing α-like. Reported
as a negative per the standing instruction to flag such numbers if and only if they appear.

---

## 7. Reproduce

```python
import sympy as sp
x, psi, M = sp.symbols('x psi M', positive=True)
mu = x/sp.sqrt(1+x**2)
F  = sp.Rational(1,2)*(x*sp.sqrt(1+x**2) - sp.asinh(x))

# convention discriminator (§1)
print(sp.simplify(sp.diff(F,x) - x*mu))                      # 0        -> D2 convention
print(sp.simplify(sp.diff(sp.sqrt(1+x**2)-1,x) - x*mu))      # != 0
print(sp.limit(F/x**2,x,sp.oo), sp.limit(F/x**3,x,0))        # 1/2, 1/3 (C3,C4 hold)
print(sp.limit((sp.sqrt(1+x**2)-1)/x**2,x,sp.oo))            # 0        (C3 fails)

# Theorem A (§3)
X = sp.Function('X')
print(sp.dsolve(sp.Eq(X(psi)**2, X(psi)*sp.tanh(psi)*sp.diff(X(psi),psi)), X(psi)))  # C1*sinh
print(sp.simplify(sp.expand_trig(sp.integrate(sp.sinh(psi)**2,psi)).subs(psi,sp.asinh(x)) - F))  # 0

# Theorem B/C (§4)
print(sp.simplify(sp.diff(F,x)**2 / (1-mu**2)))                        # x**4
print(sp.solve(sp.Eq(x**2*M**2/(1-M**2), x**4), M))                    # [x/sqrt(x**2+1)]
for k in (3,4,5,6):
    s = sp.solve(sp.Eq(x**2*M**2/(1-M**2), x**k), M)[0]
    print(k, s, sp.limit(sp.diff(s,x), x, 0))                          # mu'(0): oo,1,0,0

# corrected ghost-free / AeST conditions (§1)
Y, a0, lam = sp.symbols('Y a0 lambda_s', positive=True)
J = 2*lam*a0**2*F.subs(x, sp.sqrt(Y)/a0)
print(sp.simplify(sp.diff(F,x,2)))                    # x(x**2+2)/(x**2+1)**(3/2) > 0
print(sp.simplify(sp.diff(J,Y)), sp.limit(sp.diff(J,Y),Y,sp.oo))          # lam*sqrt(Y)/sqrt(Y+a0**2) ; lam
print(sp.simplify(sp.diff(J,Y) + 2*Y*sp.diff(J,Y,2)))                     # > 0
print(sp.limit(sp.diff(F,x), x, sp.oo))               # oo  -> Legendre dual of D1-supp §3 is dead
```

Run: `python3` on the block above (sympy only). All outputs above are measured, not asserted.

---

## 8. Ledger

| result | status | §|
|---|---|---|
| `TARGET_D1_SUPPLEMENT` §1/§3/§5 use `F′=μ`, failing C3/C4 and the deep-MOND `J(𝒴)` | **[X]** normalization error | §1 |
| Ghost-free conditions redone correctly: `F″>0`, `J′>0` with `J′→λ_s`, `J′+2𝒴J″>0` | **[D]** error in derivation, conclusion survives and improves | §1 |
| `TARGET_D1_SUPPLEMENT` §3 Legendre dual (`p` bounded, `H=(1−p²)^{−1/2}−1`) | **[X]** dead — `p=F′→∞` | §1 |
| `μ_std = tanh ∘ arsinh`; `x` = celerity, `μ` = velocity of one internal boost | **[D]** | §2 |
| Rapidity conjugacy `dF/dψ=x²` + `F′=xμ` + `μ′(0)=1` ⟹ `μ_std` uniquely | **[D]** | §3 |
| Recovered `F_std=½[x√(1+x²)−arsinh x]`, matching `TARGET_D2` §3 exactly | **[D]** | §3 |
| Chiral Fisher identity `F′²·ℐ_±(μ)=x⁴ ⟺ μ_std`, no rational ansatz | **[D]** | §4 |
| Family `x^k` generated; `μ′(0)=1` selects `k=4` (analogue of D2 Thm 9.3) | **[D]** | §4 |
| §3 and §4 are one postulate, not two independent corroborations | **[D]** | §4 |
| `{0,1}` and `{−1,+1}` are the same exponential family; `ℐ_±` is D2's `ℐ` reparametrized | **[D]** | §5 |
| The Fisher identity has **no invariant content** until the coordinate is fixed (hits D2 §7 too) | **[O]** objection stated against ourselves | §5 |
| Coordinate fixed physically: chiral `μ→0` is *unpolarized*, not *absent* ⟹ rapidity ⟹ μ_std | **[C]** | §5 |
| D2 §8 "dual-channel" cited as support for a ±1 channel | **[X]** equivocation, withdrawn | §5 |
| D2 constraint 4 (additive Newton−correction split) | **[X]** dropped, unsatisfiable for `F_std` | §6 |
| Postulate R / alphabet choice derived from the action | **[O]** | §6 |
| `μ′(0)=1` derived | **[O]** | §6 |
| AeST/Skordis–Złośnik embedding forces `μ` (D2 Q3) | **[O]** | §6 |
| Born–Infeld `γ−1` and Unruh–dS readings of `√(1+x²)−1` | **[X]** wrong normalization | §6.1 |
| α ≈ 1/137.036 anywhere in the chain | **NEGATIVE — does not appear** | §6.2 |
