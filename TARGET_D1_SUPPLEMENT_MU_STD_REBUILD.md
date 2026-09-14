# TARGET D1 SUPPLEMENT: Rebuild onto μ_std = x/√(1+x²)

**Status:** §1/§3/§5 **RE-RUN COMPLETE 2026-09-12** (Vesper) under the corrected AQUAL convention $F'=x\mu$; §4 unaffected (μ unchanged); D2's uniqueness gap remains **[O]** and is now the load-bearing open problem. D6's ghost-free re-check is closed by §5. `TARGET_D7` §4/§11 concluded μ(x)=x/(1+x) is
falsified by its own solar-system solution and is not rescuable by any GW170817-safe
(c_T=c) screening mechanism. This document rebuilds the core algebraic machinery for the
surviving candidate, μ_std(x) = x/√(1+x²) — the "simple" interpolating function already
used inconsistently elsewhere in this corpus (`TARGET_D1`'s own "standard square-root
interpolation" aside, `TARGET_D2`, `FIRST_PRINCIPLES_PHYSICS_MONOGRAPH.md` §64,
`FIG_TREE_MONOGRAPH.md`, `MuProjection.lean`, and `AXIOMS_V2.lean:64`'s right disjunct).
**Last updated:** 2026-09-12
**Tags:** `[P]` proved · `[D]` derived here · `[C]` cited · `[O]` open · `[X]` killed

---

## 1. The action [D] — RE-RUN 2026-09-12 under the AQUAL convention F′ = xμ

> **History (do not delete):** this section originally used F′=μ and
> $F_{\rm std}=\sqrt{1+x^2}-1$; flagged **[X]** by
> `TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md` §1 — fails C3/C4 and gives a $J(\mathcal Y)$
> with no deep-MOND limit. The AQUAL convention is $F' = x\mu$ (`TARGET_D2` §4). Sections
> §1/§3/§5 below are the corrected re-run (Vesper, 2026-09-12; old text in git history at
> `52b2d31^`). **§4's exact Mercury solve is unaffected** (it uses
> $\mu_{\rm std}(g_\varphi/a_0)\,g_\varphi=\hat g$ directly, and μ is unchanged).

$$\mu_{\rm std}(x) = \frac{x}{\sqrt{1+x^2}} \quad\Longrightarrow\quad
F_{\rm std}(x) = \tfrac12\!\left[x\sqrt{1+x^2} - \operatorname{arsinh} x\right],
\qquad F_{\rm std}(0)=0$$

Verified symbolically (sympy): $F_{\rm std}'(x) = x\,\mu_{\rm std}(x) = \dfrac{x^2}{\sqrt{1+x^2}}$ exactly, and

$$F_{\rm std}''(x) = \frac{x\,(x^2+2)}{(1+x^2)^{3/2}} > 0 \quad \forall x>0 \quad\text{(convex, ghost-free in the same sense `TARGET_D7` §5 required).}$$

**Constraint check against `TARGET_D2`'s table [D]:**

- **C3 (Newtonian):** $\lim_{x\to\infty}F_{\rm std}(x)/x^2 = \tfrac12$ ✓ (symbolic limit)
- **C4 (deep-MOND):** $\lim_{x\to 0}F_{\rm std}(x)/x^3 = \tfrac13$ ✓ (symbolic limit; Taylor: $F_{\rm std} = \tfrac{x^3}{3} - \tfrac{x^5}{10} + O(x^7)$)
- Large $x$: $F_{\rm std}(x) = \tfrac{x^2}{2} - \tfrac12\ln(2x) + \tfrac14 + O(1/x)$ — verified via $\lim_{x\to\infty}\left[F_{\rm std} - \tfrac{x^2}{2} + \tfrac12\ln 2x\right] = \tfrac14$. $\mu_{\rm std}(x)\to 1-\tfrac{1}{2x^2}+O(x^{-4})$ — unchanged by the convention fix; the $1/x^2$ tail (the fact that killed $F_{\rm dual}$'s $1/x$ tail) is what makes §4's clearance survive.

The corrected action is the one $F_{\rm std}$ that satisfies C3/C4 **and** the AQUAL constitutive convention — the [X] version satisfied neither C3 nor C4.

```python
import sympy as sp
x = sp.symbols('x', positive=True)
F = sp.Rational(1,2)*(x*sp.sqrt(1+x**2) - sp.asinh(x))
print(sp.simplify(sp.diff(F,x) - x**2/sp.sqrt(1+x**2)))   # 0  == F' = x*mu
print(sp.simplify(sp.diff(F,x,2)))                        # x*(x**2+2)/(x**2+1)**(3/2)
print(sp.limit(F/x**2, x, sp.oo))                          # 1/2   (C3)
print(sp.limit(F/x**3, x, 0))                              # 1/3   (C4)
print(sp.series(F, x, 0, 7))                               # x**3/3 - x**5/10 + O(x**7)
print(sp.limit(F - x**2/2 + sp.log(2*x)/2, x, sp.oo))      # 1/4
```

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

## 3. Legendre dual, rapidity structure, Hamilgrangian split [D] — RE-RUN 2026-09-12

Mirroring `CLAIM_EVIDENCE_LEDGER.md` CLM-12/13/14 (built for $F_{\rm dual}$), rebuilt under $F'=x\mu$:

**Legendre dual [D].** Conjugate momentum $p = F_{\rm std}'(x) = x^2/\sqrt{1+x^2} \in (0,\infty)$ — **unbounded**, unlike the [X] version's $p\in(0,1)$. Inverting the quartet $x^4 - p^2x^2 - p^2 = 0$:

$$x(p) = \sqrt{\tfrac12\left[p^2 + p\sqrt{p^2+4}\right]}, \qquad \mathcal H(p) = p\,x(p) - F_{\rm std}(x(p))$$

The inversion round-trips to 30 digits (mpmath, $p = 10^{-6}\ldots10^{6}$; relative error $< 2\times10^{-31}$). No closed form as clean as the old $(1-p^2)^{-1/2}-1$ exists, but the asymptotics are exact:

- **Deep-MOND ($p\to0$):** $\mathcal H(p) = \tfrac23 p^{3/2}\,(1 + O(p))$ — the standard MOND Hamiltonian scaling (mpmath: $\mathcal H/\!\left[\tfrac23p^{3/2}\right] = 1.0000002$ at $p=10^{-6}$)
- **Newtonian ($p\to\infty$):** $\mathcal H(p) = \tfrac{p^2}{2} + \tfrac12\ln(2p) + O(1/p)$ — quadratic core with logarithmic correction (mpmath: residual $/p \to -1/(4p^2)$, i.e. next term $-1/4p$)
- **Convexity:** $\mathcal H''(p) > 0$ verified numerically at $p = 0.1, 1, 10$ (1.702, 0.920, 0.995); asymptotically $\mathcal H'' \sim \tfrac12 p^{-1/2} > 0$ as $p\to0$ and $\mathcal H''\to1$ as $p\to\infty$. Strictly convex on the full domain.

**Rapidity structure [D] — the clean form the [X] version lacked.** With $x = \sinh\psi$:

$$F_{\rm std}(\psi) = \tfrac14\sinh(2\psi) - \tfrac{\psi}{2},
\qquad \frac{dF_{\rm std}}{d\psi} = \sinh^2\psi = x^2 \;\;\text{(identically, sympy-verified)}$$

This is `TARGET_D2_SUPPLEMENT` §0's rapidity conjugacy $dF/d\psi = x^2$, now verified directly in the AQUAL convention. **The Hamilgrangian split exists after all:** hyperbolic bulk $\tfrac14\sinh 2\psi = \tfrac12 x\sqrt{1+x^2}$ (relativistic-kinetic reading) minus linear counter-term $\psi/2 = \tfrac12\operatorname{arsinh}x$ (rapidity cost). The F′=μ search for a split failed because the split is natural in $\psi$, not in $x$. Physical reading of the counter-term: **[O]** — a reinterpretation, not a derivation.

**Fisher identity [C — superseded, not open].** The [X] flag ("does not transfer") is resolved by `TARGET_D2_SUPPLEMENT` §0: the chiral ±1-channel identity $F'^2\,\mathcal I_\pm(\mu) = x^4$ with the rapidity rectification replaces CLM-13's Bernoulli/odds form. It is a postulate swap — read that document's §6 before citing. No further work in this target.

```python
import sympy as sp
x, psi, p = sp.symbols('x psi p', positive=True)
F = sp.Rational(1,2)*(x*sp.sqrt(1+x**2) - sp.asinh(x))
print(sp.simplify(F.subs(x, sp.sinh(psi))))                # sinh(psi)cosh(psi)/2 - psi/2
print(sp.simplify(sp.diff(F.subs(x, sp.sinh(psi)), psi) - sp.sinh(psi)**2))  # 0: dF/dpsi = x^2
```

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

## 5. Ghost-free check [D] — RE-RUN 2026-09-12; also closes the D6 pending item

Transplanting via $J(\mathcal{Y}) = 2\lambda_s a_0^2\, F_{\rm std}\!\left(\sqrt{\mathcal{Y}}/a_0\right)$ (the `TARGET_D7` §2.1 normalization pattern, inherited as stated, not re-derived here):

$$\mathcal J'(\mathcal{Y}) = \lambda_s\,\frac{\sqrt{\mathcal{Y}}}{\sqrt{\mathcal{Y}+a_0^2}} = \lambda_s\,\mu_{\rm std}\!\left(\tfrac{\sqrt{\mathcal{Y}}}{a_0}\right) > 0 \quad\forall\,\mathcal{Y}>0$$

$$\mathcal J''(\mathcal{Y}) = \frac{\lambda_s a_0^2}{2\sqrt{\mathcal{Y}}\,(\mathcal{Y}+a_0^2)^{3/2}} > 0 \quad\forall\,\mathcal{Y}>0$$

$$\mathcal J' + 2\mathcal{Y}\,\mathcal J'' = \frac{\lambda_s\sqrt{\mathcal{Y}}\,(\mathcal{Y}+2a_0^2)}{(\mathcal{Y}+a_0^2)^{3/2}} > 0 \quad\forall\,\mathcal{Y}>0$$

Both `TARGET_D7` §5 conditions hold **identically** (sympy; spot-checked numerically at $\mathcal{Y} = 0.01, 1, 100, 10^6$: $\mathcal J'/\lambda_s = 0.0995, 0.707, 0.995, 1.000$ and $(\mathcal J'+2\mathcal Y\mathcal J'')/\lambda_s = 0.198, 1.061, 1.005, 1.000$ — all positive, monotonically saturating).

**Limits [D]:**

- **Deep-MOND:** $\lim_{\mathcal Y\to0} J/\mathcal Y^{3/2} = \dfrac{2\lambda_s}{3a_0}$ — the standard AQUAL $\mathcal Y^{3/2}$ scaling, exactly what the [X] version's linear $J$ could not produce
- **Newtonian:** $\lim_{\mathcal Y\to\infty} J/\mathcal Y = \lambda_s$ — linear in $\mathcal Y$ with $\mathcal J'\to\lambda_s$, smoothly μ-regularized in between

**D6 closure:** `PEER_REVIEW_READINESS.md` lists D6 as "ghost-free condition needs re-verification as $J''(\mathcal Y)>0$ under the corrected action — not yet re-checked." The second line above closes it: $J'' > 0$ **identically** for all $\mathcal Y > 0$. The D6 target doc should be updated to reference this section.

## 6. What transfers, what doesn't — summary ledger

| result | for $F_{\rm dual}$ | for $F_{\rm std}$ | verdict |
|---|---|---|:-:|
| Action / convention | $F_{\rm dual}'=\mu$, $F_{\rm dual}=\tfrac12x^2-x+\ln(1+x)$ | $F_{\rm std}'=x\mu$, $F_{\rm std}=\tfrac12[x\sqrt{1+x^2}-\operatorname{arsinh}x]$ | [D] both; **C3/C4 now pass** (RE-RUN) |
| Boundary asymptotics | $\mu\to x$ (deep), $\mu\to1$ (Newton) | same | [D] both |
| Convexity / ghost-free ($F''>0$) | proved | proved | [D] both |
| Structural uniqueness (Padé[1/1], 4 constraints) | [P] `TARGET_D2` Thm 9.1 | **does not apply** — not a Padé function | **[O]** open, unresolved |
| Legendre dual | $\mathcal{H}\sim p^2/2$ (Newton), $p^{3/2}$ (MOND) | $p\in(0,\infty)$; $\mathcal H=\tfrac23p^{3/2}$ (deep) → $\tfrac{p^2}{2}+\tfrac12\ln2p$ (Newton); convex, verified | [D] both, different closed forms (RE-RUN) |
| Fisher identity | $F'^2\cdot\mathcal{I}=x^3$ (Bernoulli) | **superseded**: chiral identity $F'^2\mathcal I_\pm(\mu)=x^4$ via rapidity rectification (`TARGET_D2_SUPPLEMENT` §0, postulate swap) | **[C]** resolved (RE-RUN) |
| Hamilgrangian split | clean two-term split | **found in ψ, not x**: $\tfrac14\sinh2\psi$ (bulk) $-\psi/2$ (counter-term); reading [O] | **[D]** structure (RE-RUN) |
| AeST transplant, $\mathcal{J}(\mathcal{Y})$ | tracking branch, constant residual $\ge a_0$ | $\mathcal J'=\lambda_s\mu_{\rm std}(\sqrt{\mathcal Y}/a_0)$; residual $\to0$ as $1/x^2$, exact solve confirms $a_0^2/(2\hat g)$ | **[D] survives** (RE-RUN) |
| Solar-system bound | **violated by $5.7\times10^5$** | **cleared by $\sim1300\times$** at Mercury | **[D] $\mu_{\rm std}$ survives, $\mu_{\rm dual}$ does not** |
| Ghost-free in AeST | [D] | [D] **identically**: $\mathcal J'>0$, $\mathcal J''>0$, $\mathcal J'+2\mathcal Y\mathcal J''>0$ ∀𝒴>0 — **closes the D6 pending re-check** | [D] both (RE-RUN) |

---

## 7. Critical path

1. **D2's uniqueness gap is now the central open problem**, not a secondary one. This repo's
   entire "derive $\mu$ from first principles, don't fit it" program has no structural argument
   for $\mu_{\rm std}$ — it is currently adopted because it survives the solar system, which is
   a phenomenological selection, exactly the kind of reasoning this corpus's own
   `feedback_two_irreducible_parameters`-style discipline was built to flag. **[O]**
2. ~~The Fisher-identity and Hamilgrangian-split machinery does not transfer.~~
   **RESOLVED 2026-09-12:** the Fisher identity is superseded by the chiral rapidity form
   (`TARGET_D2_SUPPLEMENT` §0, [C]); the Hamilgrangian split exists in the rapidity
   coordinate (§3). CLM-12/13/14 should be re-pointed at these forms.
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
