# TARGET D1 SUPPLEMENT: Rebuild onto μ_std = x/√(1+x²)

**Status:** REBUILD_UNDERWAY (2026-09-12). `TARGET_D7` §4/§11 concluded μ(x)=x/(1+x) is
falsified by its own solar-system solution and is not rescuable by any GW170817-safe
(c_T=c) screening mechanism. This document rebuilds the core algebraic machinery for the
surviving candidate, μ_std(x) = x/√(1+x²) — the "simple" interpolating function already
used inconsistently elsewhere in this corpus (`TARGET_D1`'s own "standard square-root
interpolation" aside, `TARGET_D2`, `FIRST_PRINCIPLES_PHYSICS_MONOGRAPH.md` §64,
`FIG_TREE_MONOGRAPH.md`, `MuProjection.lean`, and `AXIOMS_V2.lean:64`'s right disjunct).
**Last updated:** 2026-09-12
**Tags:** `[P]` proved · `[D]` derived here · `[C]` cited · `[O]` open · `[X]` killed

---

## 1. The action [D]

$$\mu_{\rm std}(x) = \frac{x}{\sqrt{1+x^2}} \quad\Longrightarrow\quad
F_{\rm std}(x) = \sqrt{1+x^2} - 1$$

Verified symbolically: $F_{\rm std}'(x) = x/\sqrt{1+x^2} = \mu_{\rm std}(x)$ exactly (sympy,
reproduced below). Normalization $F_{\rm std}(0)=0$ chosen to match `TARGET_D1`'s convention
for $F_{\rm dual}$.

**Asymptotics [D]:**
- Small $x$ (deep-MOND): $F_{\rm std}(x) = \tfrac12 x^2 - \tfrac18 x^4 + O(x^6)$ — same
  leading Newtonian-looking term as $F_{\rm dual}$, but the *sign structure differs at next
  order* ($-x^4/8$ vs $F_{\rm dual}$'s cubic correction). $\mu_{\rm std}(x)\to x$ as required.
- Large $x$ (Newtonian): $F_{\rm std}(x) = x - 1 + \tfrac{1}{2x} - \tfrac{1}{8x^3}+O(x^{-4})$.
  $\mu_{\rm std}(x)\to1-\tfrac{1}{2x^2}+O(x^{-4})$ — **the correction decays as $1/x^2$, not
  as $1/x$.** This single fact is the whole result: it is exactly the tail that killed
  $F_{\rm dual}$ in `TARGET_D7` §4.2, and it is why $F_{\rm std}$ survives.

**Convexity [D]:** $F_{\rm std}''(x) = (1+x^2)^{-3/2} > 0$ for all $x>0$ (sympy, verified
numerically at $x=0.1,1,10,100$). Ghost-free in the same sense `TARGET_D7` §5 required for
$F_{\rm dual}$.

```python
import sympy as sp
x = sp.symbols('x', positive=True)
F = sp.sqrt(1+x**2) - 1
print(sp.simplify(sp.diff(F,x)))          # x/sqrt(x**2 + 1)  == mu_std, confirmed
print(sp.series(F, x, 0, 6))              # x**2/2 - x**4/8 + O(x**6)
print(sp.series(F, x, sp.oo, 4))          # -1/(8x**3) + 1/(2x) - 1 + x + O(x**-4)
print(sp.simplify(sp.diff(F, x, 2)))      # (x**2+1)**(-3/2), positive for all real x
```

---

## 2. Uniqueness structure [O]

> **UPDATE 2026-09-12 — see `TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md`.** Option (a) below
> was attempted and succeeded in modified form: a uniqueness theorem of the same shape as
> `TARGET_D2` Thm 9.1/9.2 now exists for $\mu_{\rm std}$ (rapidity conjugacy $dF/d\psi=x^2$,
> equivalently the Fisher identity $F'^2\,\mathcal I_\pm(\mu)=x^4$ on a $\pm1$ **chiral**
> channel rather than D2's $\{0,1\}$ Bernoulli channel). It is a postulate swap, not a
> derivation from nothing — read that document's §6 before citing.
>
> **That document's §1 also flags a normalization error in this section's §1/§3/§5:** they use
> $F'=\mu$, whereas AQUAL requires $F'=x\mu$ (`TARGET_D2` §4). Under $F'=\mu$, $F=\sqrt{1+x^2}-1$
> fails C3/C4 and gives a linear $J(\mathcal Y)$ with no deep-MOND limit. The correct action is
> $F_{\rm std}=\tfrac12[x\sqrt{1+x^2}-\operatorname{arsinh}x]$. **§4's exact Mercury solve is
> unaffected** (it uses $\mu_{\rm std}(g_\varphi/a_0)g_\varphi=\hat g$ directly). §1/§3/§5 need
> re-running. **[X]**

$F_{\rm dual}$'s uniqueness argument (`TARGET_D2` Theorem 9.1) is Padé[1/1]-specific:
$\mu_{\rm dual}(x)=x/(1+x)$ is a ratio of two linear polynomials. $\mu_{\rm std}(x)$ is
**not** a Padé approximant in $x$ at any finite order — it is algebraic ($\sqrt{1+x^2}$ in
the denominator), not rational. It does not fall out of `TARGET_D2`'s four structural
constraints as stated; those constraints were built to select $F_{\rm dual}$ specifically.

**What this means honestly:** rebuilding μ_std does not inherit D2's uniqueness proof.
Either (a) D2's constraints need to be revisited to see if a modified constraint set forces
$\mu_{\rm std}$ instead — unattempted here — or (b) $\mu_{\rm std}$ is adopted as the
literature's standard phenomenological choice (Famaey & Binney 2005, the most common
interpolating function fit to SPARC rotation curves in the MOND literature generally) without
a first-principles derivation from this corpus's own action-selection program. This is a real
gap, not a formality — D2's whole point was deriving $\mu$ from structure rather than fitting
it. **[O]** — this is now arguably the load-bearing open problem for D2, above and beyond the
pre-existing Padé-necessity question.

---

## 3. Hamilgrangian-style decomposition, Fisher identity, Legendre dual [D]

Mirroring `CLAIM_EVIDENCE_LEDGER.md` CLM-12/13/14 (built for $F_{\rm dual}$):

**Legendre dual [D].** Conjugate momentum $p = F_{\rm std}'(x) = x/\sqrt{1+x^2} = \mu_{\rm
std}(x)$. Since $\mu_{\rm std}$ is already bounded in $(0,1)$ (unlike $F_{\rm dual}$'s
unbounded $\mu_{\rm dual}\in(0,1)$ too, actually — both map to $(0,1)$), invert:

$$x(p) = \frac{p}{\sqrt{1-p^2}}, \qquad 0<p<1$$

Dual Hamiltonian $\mathcal{H}_{\rm dual}(p) = px(p) - F_{\rm std}(x(p))$:

```python
import sympy as sp
p = sp.symbols('p', positive=True)
x_of_p = p/sp.sqrt(1-p**2)
F_of_x = sp.sqrt(1+x_of_p**2) - 1
H = sp.simplify(p*x_of_p - F_of_x)
print(H)                     # 1/sqrt(1-p**2) - 1
print(sp.simplify(sp.diff(H, p, 2)))   # check convexity
```

This gives $\mathcal{H}_{\rm dual}(p) = (1-p^2)^{-1/2} - 1$ — **[D], verified**. Strictly
convex for $p\in(0,1)$ (checked numerically; $H''(p)>0$ throughout the domain).

**Fisher identity [O] — does not transfer in the same form.** $F_{\rm dual}$'s Fisher
identity $F_{\rm dual}'(x)^2\cdot\mathcal{I}(\mu(x))=x^3$ (CLM-13) used the specific rational
structure of $\mu_{\rm dual}=x/(1+x)$ as an odds ratio ($\mu_{\rm dual}(\text{odds}(p))=p$
requires $\mu$ rational in exactly that form). $\mu_{\rm std}$ is not an odds-ratio function of
any natural Bernoulli parametrization — attempted substitution does not reproduce an
$x^3$-type identity. **This piece of the CLM-12/13/14 program is specific to the Padé
structure and does not generalize.** Flagged **[X]** for direct transfer, **[O]** for whether
a different (non-Bernoulli) statistical identity exists for $\mu_{\rm std}$.

**Hamilgrangian channel split [O].** $F_{\rm dual}(x)=\tfrac12x^2-(x-\ln(1+x))$ splits into
$\mathcal{H}=\tfrac12x^2$ (bulk kinetic) and $\mathcal{L}_{\rm corr}=x-\ln(1+x)$ (boundary
correction), because $\ln(1+x)$ is the natural antiderivative pairing with the Padé pole
structure. $F_{\rm std}(x)=\sqrt{1+x^2}-1$ has no analogous closed-form two-term split with
an equally clean physical reading (bulk vs. boundary) — the obvious candidate
$\tfrac12x^2-(\tfrac12x^2-\sqrt{1+x^2}+1)$ is definitionally true but not illuminating.
**[O]** — no natural decomposition found; may not exist for this functional form.

---

## 4. Solar-system check — exact, not asymptotic [D]

Transplanting into AeST exactly as `TARGET_D7` §2.1/§4.2 did for $F_{\rm dual}$: the
spherical scalar-field equation integrates to (Gauss's law form)

$$\mu_{\rm std}(g_\varphi/a_0)\cdot g_\varphi = \hat g \quad\Longrightarrow\quad
\frac{a_0\,x^2}{\sqrt{1+x^2}} = \hat g, \qquad g_\varphi \equiv a_0 x$$

**Solved exactly** (Newton iteration to 50 decimal digits, `mpmath`), not just via asymptotic
series, at Mercury's orbit ($\hat g = GM_\odot/r_{\rm Mercury}^2$, $a_0=1.116\times10^{-10}$
m/s² — this repo's own SPARC value):

```
ĝ (Mercury)      = 3.9574739366926450085961428952863635515080704975745e-2   m/s²
g_φ (exact)      = 3.9574739366926450243316350289484888999441685889257e-2   m/s²
residual g_φ-ĝ   = 1.5735492133662125348436098091351209753041539690503e-19  m/s²
predicted a0²/(2ĝ) = 1.5735492133662125504852613177406715293266622460667e-19 m/s²
```

**The residual matches the analytic $a_0^2/(2\hat g)$ prediction to 10 significant figures —
this is an exact confirmation, not an asymptotic hand-wave.** [D]

### 4.1 Comparison against the bounds `TARGET_D7` §4.3 used to kill $F_{\rm dual}$

| test | $\mu_{\rm std}$ residual force | bound | margin |
|---|:-:|:-:|:-:|
| Mercury, force units | $1.57\times10^{-19}$ m/s² | Cassini-equivalent $\sim2.0\times10^{-16}$ m/s² (from `TARGET_D7` §4.3's $Q_2/r$) | **$\mu_{\rm std}$ is $\sim1300\times$ *below* the bound** |
| Scaling vs. the killed $\mu_{\rm dual}$ residual ($\tilde a_0\ge a_0\approx1.1\times10^{-10}$ m/s², constant) | — | — | **$\mu_{\rm std}$'s residual is $\sim9$ orders of magnitude smaller**, matching the earlier order-of-magnitude estimate in `TARGET_D7` §4.4 Branch A, now confirmed by exact solve rather than asserted |

$\mu_{\rm std}$ clears the solar-system bound comfortably. This is the numeric confirmation
`TARGET_D7` §4.4 called for but did not itself perform.

---

## 5. Ghost-free check [D]

Transplanting via $J(\mathcal{Y})=2\lambda_s a_0^2 F_{\rm std}(\sqrt{\mathcal{Y}}/a_0)$
(same normalization pattern as `TARGET_D7` §2.1):

$$\mathcal{J}'(\mathcal{Y})=\frac{a_0\lambda_s}{\sqrt{\mathcal{Y}+a_0^2}}>0 \quad\forall\,\mathcal{Y}>0$$

$$\mathcal{J}'+2\mathcal{Y}\mathcal{J}''=\frac{a_0^3\lambda_s}{(\mathcal{Y}+a_0^2)^{3/2}}>0
\quad\forall\,\mathcal{Y}>0$$

Both `TARGET_D7` §5 conditions hold identically, verified symbolically (sympy) and spot-checked
numerically at $\mathcal{Y}=0.01,1,100,10^6$ (all positive, monotonically decreasing as
expected). **[D]** Ghost-free, same standard as $F_{\rm dual}$ met and by the same margin of
rigor.

---

## 6. What transfers, what doesn't — summary ledger

| result | for $F_{\rm dual}$ | for $F_{\rm std}$ | verdict |
|---|---|---|:-:|
| Action / $F'=\mu$ | $F_{\rm dual}=\tfrac12x^2-x+\ln(1+x)$ | $F_{\rm std}=\sqrt{1+x^2}-1$ | [D] both |
| Boundary asymptotics | $\mu\to x$ (deep), $\mu\to1$ (Newton) | same | [D] both |
| Convexity / ghost-free ($F''>0$) | proved | proved | [D] both |
| Structural uniqueness (Padé[1/1], 4 constraints) | [P] `TARGET_D2` Thm 9.1 | **does not apply** — not a Padé function | **[O]** open, unresolved |
| Legendre dual | $\mathcal{H}\sim p^2/2$ (Newton), $p^{3/2}$ (MOND) | $\mathcal{H}=(1-p^2)^{-1/2}-1$, convex, verified | [D] both, different closed forms |
| Fisher/odds-ratio identity | $F'^2\cdot\mathcal{I}=x^3$ | **no analogous identity found** | **[X]** for direct transfer |
| Hamilgrangian bulk/boundary split | clean two-term split | **no equally clean split found** | **[O]** |
| AeST transplant, $\mathcal{J}(\mathcal{Y})$ | tracking branch, constant residual $\ge a_0$ | **residual $\to0$ as $1/x^2$, exact solve confirms $a_0^2/(2\hat g)$** | **[D] survives** |
| Solar-system bound | **violated by $5.7\times10^5$** | **cleared by $\sim1300\times$** at Mercury | **[D] $\mu_{\rm std}$ survives, $\mu_{\rm dual}$ does not** |
| Ghost-free in AeST | [D] | [D], same functional form of the condition | [D] both |

---

## 7. Critical path

1. **D2's uniqueness gap is now the central open problem**, not a secondary one. This repo's
   entire "derive $\mu$ from first principles, don't fit it" program has no structural argument
   for $\mu_{\rm std}$ — it is currently adopted because it survives the solar system, which is
   a phenomenological selection, exactly the kind of reasoning this corpus's own
   `feedback_two_irreducible_parameters`-style discipline was built to flag. **[O]**
2. The Fisher-identity and Hamilgrangian-split machinery (CLM-12/13/14) does not transfer.
   Either find analogous structures for $\mu_{\rm std}$, or accept that those specific results
   are properties of the (now-falsified) Padé choice and drop them from the "what makes
   $F_{\rm dual}$ special" argument entirely.
3. D5 cosmology (`TARGET_D7` §3, void since the AeST rewrite) needs to be rebuilt on
   $\mathcal{K}(\mathcal{Q})$ regardless of which $\mu$ wins — this is independent of the D1
   rebuild and still fully open.
4. Lean follow-up (not touched here, flagged only): `MuProjection.lean` already carries
   $\mu_{\rm std}$'s properties per the original `CLM-02` entry — check whether it needs
   updating now that $\mu_{\rm std}$ is the primary candidate rather than a secondary one, and
   whether `AXIOMS_V2.lean:64`'s disjunction should be simplified to state $\mu_{\rm std}$
   directly rather than as a disjunct.
5. Every downstream target that assumed $F_{\rm dual}$ specifically (not just "the
   interpolating function") — check `TARGET_D6`, `TARGET_D8`, `TARGET_D9`'s numeric
   evaluations — needs re-running with $F_{\rm std}$. Not attempted in this document; scope is
   D1's core machinery only.
