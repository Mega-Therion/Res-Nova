# Correction: F'' and the Linear Screening Ratio

**Date:** 2026-09-08
**Severity:** one wrong formula, one wrong published number. **No conclusion changes,
and the corrected number is more favourable to the theory than the published one.**
**Affects:** `TARGET_D7` §4.1 and §7, and everything downstream of the 0.4% figure —
including `res_nova_manuscript.tex`, the Zenodo record, and the PRD cover letter.

---

## 1. What was wrong

`TARGET_D7` §7 stated

$$\mathcal{F}''(\mathcal{K}) \;=\; \frac{2\sqrt{\mathcal{K}} + \mathcal{K}}{(1+\sqrt{\mathcal{K}})^2 \cdot 2\sqrt{\mathcal{K}}}$$

This is not $d^2\mathcal{F}/d\mathcal{K}^2$. In $u=\sqrt{\mathcal{K}}$ it is
$(2u+u^2)/(2u(1+u)^2)$ — a derivative taken with respect to $u$, missing the
chain-rule factors that relate $d/d\mathcal{K}$ to $d/du$.

Differentiating $\mathcal{F}(\mathcal{K}) = \tfrac{\mathcal{K}}{2} - \sqrt{\mathcal{K}} + \ln(1+\sqrt{\mathcal{K}})$ symbolically:

$$\frac{d\mathcal{F}}{d\mathcal{K}} = \frac{\mathcal{K}^{3/2}}{2(\mathcal{K}^{3/2}+\mathcal{K})}, \qquad
\frac{d^2\mathcal{F}}{d\mathcal{K}^2} = \frac{1}{4u(1+u)^2}$$

| $\mathcal{K}$ | stated | true | ratio |
|---|---|---|---|
| 1 | 0.375 | 0.0625 | 6× |
| $10^2$ | $4.96\times10^{-2}$ | $2.07\times10^{-4}$ | 240× |
| $10^4$ | $5.00\times10^{-3}$ | $2.45\times10^{-7}$ | $\sim2\times10^{4}$ |

## 2. What it propagated into

§4.1 used the same wrong $\mathcal{F}''$ to form the screening ratio:

$$\text{stated: } \frac{\mathcal{F}''}{\mathcal{F}'} \approx \frac{1}{x_0(1+x_0)^2} \approx 0.004
\qquad
\text{true: } \frac{\mathcal{F}''}{\mathcal{F}'} = \frac{1}{2x_0^2(1+x_0)} \approx 0.00233$$

Note the structure differs, not just the value: $x_0^2$ with a single $(1+x_0)$,
rather than $x_0$ with $(1+x_0)^2$.

At $x_0 = 5.67$ the linear growth enhancement therefore becomes **0.23%**, not 0.4%.

## 3. Direction — this favours the theory

Screening is **1.7× stronger** than published. A smaller enhancement is closer to
$\Lambda$CDM, so structure-formation constraints are *easier* to satisfy, not
harder. The published figure was conservative against the theory. Nothing that was
claimed to pass now fails; the margin widens.

The ghost-free conclusion is likewise untouched: $1/(4u(1+u)^2) > 0$ for all
$u>0$, which is Skordis–Złośnik condition (1). The formula was wrong; the result
it was cited for is right — now machine-checked as
`CovariantCompletion.F_dual_ghost_free`, with `F_dual_second_deriv_antitone` for
the monotone decay. Both non-vacuous: flipping the numerator's sign breaks the
proof.

## 4. Published artifacts — NOT silently edited

The 0.4% figure appears in artifacts that are already deposited:

- `res_nova_manuscript.tex` — abstract, §on growth, and the $\xi \approx 1.004$ line
- `zenodo_metadata.json` and `.zenodo.json` — deposited record descriptions
- `SUBMISSION/COVER_LETTER_PRD.md` — journal cover letter

These are left unmodified here **on purpose**. A deposited record and a submitted
cover letter are historical documents; rewriting them in place would misrepresent
what was deposited. They need a deliberate decision — an erratum, a new version,
or a corrected resubmission — which is the author's call, not a repository edit.

**What must NOT happen:** a future version quoting 0.23% while the live DOI still
reads 0.4%, with no note connecting them.

## 4b. Follow-up: the "suppressed by ~250×" figure, and a label collision

`TARGET_D7` §4.1 also said the linear enhancement is *"suppressed by a factor of
~250×"*. That is not independent evidence: $1/0.004 = 250$, so it is the same
ratio restated as its reciprocal. With the corrected ratio it is
$1/0.00233 = 429\times$.

Separately — and this is a genuine trap for a reader — §6 uses "$\sim250\times$"
for a **different** suppression: the external-field effect,
$Q_2 \sim 10^{-21} \to 4\times10^{-24}$, which really is a factor $\sim250$ and is
unaffected by this correction. Two unrelated quantities carried the same number
and the same words. Both sites are now labelled explicitly.

## 5. Method

Both derivatives recomputed with SymPy from the action as written, cross-checked
by direct numerical evaluation at $\mathcal{K} \in \{10^{-6},\dots,10^{9}\}$. The
positivity claim is now a Lean theorem rather than an assertion. Gate: 39/39 PASS.
