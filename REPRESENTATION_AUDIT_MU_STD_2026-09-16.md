# REPRESENTATION AUDIT: μ_std = x/√(1+x²) — full 𝒞/𝒫 expansion

**Status:** RESULT — the representation-family sketch of `RN-CO-04` (Pass 1.5, Track B)
is expanded to a complete audit. Every claim below is either machine-verified
(`scripts/representation_audit_mu_std.py`, sympy/mpmath, run 2026-09-16, **13 symbolic
checks, 0 failures**) or tagged as literature/interpretation.
**Last updated:** 2026-09-16
**Tags:** `[P]` proved (Mathlib) · `[D]` derived/verified here · `[C]` cited/conjectured · `[O]` open · `[X]` killed
**Framework:** Res-Nova Core Objects Version 0.2. Answers the "next concrete action":
*"Deepen the representation audit of μ_std (full 𝒞/𝒫 expansion + failure-mode tests)."*

---

## 0. The audit frame, stated once

Two classes of representation are distinguished, and conflating them is the audit's
first failure mode:

- **𝒞 (equivalence class).** Representations of the *same mathematical object* —
  reparametrizations of one another. A 𝒞-member carries **no new selection content**:
  it can reorganize what is assumed, never add to it. Per Theorem D
  (`TARGET_D2_SUPPLEMENT` §4), Postulate R, the chiral Fisher identity, and
  "x is the celerity of μ" are 𝒞-members of each other — **one postulate in three dresses.**
- **𝒫 (projection families).** Parameterized families *containing* μ_std in which it
  is **not** generically the unique member satisfying the boundary/normalization
  conditions. Selection inside a 𝒫-family is a real constraint and must name
  **which input does the killing.**

**Failure-mode checklist (fixed once, reused for every core object).**

| # | failure mode | one-line statement |
|---|---|---|
| F1 | domain/boundary conditions unstated | every claim must pin its domain and the x→0, x→∞ limits |
| F2 | convention confusion | `F′ = xμ` (AQUAL) vs `F′ = μ` objects must never be merged (D41 precedent; §1 of the D2 supplement) |
| F3 | postulate→derivation promotion | inputs must stay inputs in every restatement |
| F4 | double-counting | equivalent results must not be counted as corroborations |
| F5 | checkability drift | the Lean file must keep compiling; the audit script must keep passing |
| F6 | empirical degeneracy | which 𝒫-members data can and cannot separate must be said explicitly |
| F7 | embedding contradiction | the covariant/SU(2) reading must not contradict what is proved |

Everything below uses the AQUAL convention `F_std(x) = ½[x√(1+x²) − arsinh x]`, `F′ = x·μ`
(F2: this is the *only* convention under which the action yields `∇·[μ∇Φ] = 4πGρ`).

---

## 1. 𝒞-class of μ_std — the complete equivalence expansion `[D]`

Each row is machine-verified (script §5, checks E1–E12). **No row adds selection
content** (F4 is enforced by this statement itself).

| # | representation | statement | reading |
|---|---|---|---|
| E1 | canonical algebraic | `μ(x) = x/√(1+x²)` | the definition |
| E2 | **unit hyperbola** | `1/μ² − 1/x² = 1` | the point `(1/μ, 1/x)` lies on the unit hyperbola `U² − V² = 1` |
| E3 | inverse / hyperbolic odds | `x = μ/√(1−μ²)`, i.e. `x = sinh(artanh μ)` | μ_dual's `odds(μ)=x` is replaced by "**hyperbolic odds**" `sinhψ(μ) = x` |
| E4 | autonomous ODE | `μ′ = (1−μ²)^{3/2}` | μ_std is the unique solution with μ(0)=0; `(1−μ²)` is the **variance of the ±1 chiral channel** at polarization μ |
| E5 | scaling ODE | `μ′ = (μ/x)³` | "the curvature is the cube of the density ratio" — coordinate-free under x↦λx |
| E6 | circle / Gudermannian | `μ = sin(gd ψ)`, `x = tan(gd ψ)`, ψ = arsinh x | the **only transcendental-free bridge** between the hyperbolic and circular readings of the same boost |
| E7 | chiral Fisher identity | `F′²·ℐ_±(μ) = x⁴` | Theorem B of the D2 supplement; ℐ_± = 1/(1−μ²) = 1/variance |
| E8 | rapidity conjugacy | `dF/dψ = x²` under `x = sinh ψ` | Postulate R; Theorem A |
| E9 | constitutive | `F′ = x·μ` with `F = ½[x√(1+x²) − arsinh x]` | the AQUAL normalization |
| E10 | logistic bridge | `tanh ψ = 2σ(2ψ) − 1` | presence and chirality coordinates are **one exponential family** (`m = 2p−1`), as the supplement §5 proved by hand |
| E11 | Barndorff–Nielsen score | score of `exp(−√(1+x²))` is `−μ` | `[C]` only — belongs to the `F′=μ` object; F2 blocks any weight (D2-supp §6.1) |
| E12 | binomial series | `μ = x − x³/2 + 3x⁵/8 − 5x⁷/16 + …` | μ_std is **not** Padé[1/1] (that is μ_dual's dress); its dress is the binomial expansion of `(1+x²)^{−1/2}` |

**What is invariant across 𝒞 (the honest summary).** The E-class is exactly the orbit of
one object under: (i) hyperbolic↔circular transcendental swap (E6), (ii) the two
coordinates of the single two-state exponential family (E10), (iii) Legendre-type
conjugation (E7/E8/E9), (iv) inversion (E3), (v) differential re-expression (E4/E5).
The §5 objection of the D2 supplement — *"the identity selects nothing until the
coordinate is independently fixed"* — is exactly the statement that 𝒞-membership is
selection-free. What survives the objection is **E4's boundary condition** (see §3):
the *reading* of μ→0 as *unpolarized* is not a 𝒞-fact, it is the chiral-coordinate
input `[C]`.

**New measured 𝒞-facts (not previously in the corpus):** E2 (hyperbola), E4, E5
(two ODE readings), E6 (Gudermannian), E3 (hyperbolic odds as the exact analogue of
μ_dual's odds). Each was verified symbolically today; none adds a postulate.

---

## 2. 𝒫-class — the projection families, and what kills each member `[D]`

μ_std sits in at least four natural families. In each, **which input does the killing
is stated explicitly** — that is the audit's content.

### P1. The exponent family `μ_n = xⁿ/√(1+x^{2n})` (Theorem C's family)

The Fisher identity generalizes to `F′²·ℐ_± = x^{2n+2}` ⟺ `μ = μ_n` (verified as pure
algebra: `x²μ_n²/(1−μ_n²) = x^{2n+2}` exactly, n = 1, 2, 3). Measured `μ_n′(0)`:

| n | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| μ′(0) | **1** | 0 | 0 | 0 |

**Killer: `μ′(0) = 1` (D2 constraint 3).** The Lean file `MuStdUniqueness.lean`
machine-checks the even branch (F5 gap: k = 3, 5 remain unformalized, recorded there).

### P2. The celerity family `μ_C = x/√(C²+x²)` (Theorem A's integration constant)

**Measured: `μ_C(x) = μ_std(x/C)` identically.** The family is therefore *not a family
of distinct models at all*: C is absorbed into `a₀` (x already carries the 1/a₀ scaling).
Consequences, stated exactly (this is a sharpening, not a repetition, of the D2
supplement):

- Theorem A's constant `C` and the MOND scale `a₀` are **the same parameter in two
  units**. Fixing `C = 1` is a units convention, not a physical selection `[D]`.
- `μ′(0) = 1` therefore does **double duty** — it is a *normalization within the
  celerity family* (no content beyond units), but a *genuine selection across the
  exponent family* (P1) and across P3 below. Collapsing these two roles would be an
  F3 error; earlier sketches of the uniqueness theorem did not distinguish them.

### P3. Milgrom's "simple" interpolation `μ_simple = x/(1+√(1+x²))` — the half-rapidity projection

**New finding of this audit `[D]`: `μ_simple = tanh(½·arsinh x)`** — verified to
50-digit precision and by the half-angle identity `tanh(ψ/2) = sinh ψ/(1+cosh ψ)`.
μ_std is `tanh(ψ)`; μ_simple is `tanh(ψ/2)` — the two standard μ-functions of the MOND
literature are the **full-rapidity and half-rapidity** points of the same rectification.

Measured on μ_simple (all numbers from the script):

| property | μ_simple | μ_std | verdict |
|---|---|---|---|
| μ(0), μ(∞) | 0, 1 | 0, 1 | both survive F1 |
| μ′(0) | **1/2** | 1 | **killed by D2 constraint 3** |
| C3: F/x² as x→∞ | 1/2 | 1/2 | both survive |
| C4: F/x³ as x→0 | **1/6** | 1/3 | **killed by C4** (same kill as μ′(0), not independent — F4) |
| Postulate R: dF/dψ | `cosh²ψ − coshψ` | `sinh²ψ` | **killed by Postulate R** (again not independent of the μ′(0) kill) |
| Fisher identity | `x⁴/(2(√(1+x²)+1))` | `x⁴` | killed (same source) |

**Killer: `μ′(0) = 1`.** One knife, three sheaths (μ′(0), C4, Postulate R fail together
on μ_simple because tanh(ψ/2) has half the slope); counting them separately would be F4.

### P4. The sibling `μ_dual = x/(1+x)` (presence coordinate)

Measured: `odds(μ_dual) = μ/(1−μ) = x` — the presence-coordinate rectification. μ′(0) = 1:
**it survives every algebraic input that kills P1(n≥2) and P3.** It is killed only by
(i) the chiral-coordinate input `[C]` (a ±1 channel cannot be absent, only unpolarized),
and (ii) empirically — the solar-system falsification recorded in the D2 supplement
addendum (2026-09-12). **This is the honest statement of what the uniqueness theorem
actually proves:** the mathematics selects μ_std *given* Postulate R; the chiral reading
of the channel is what selects Postulate R; nothing in the mathematics forces the
channel to be chiral (F3).

### P5. The non-interpolations (recorded to close the space)

- `μ = x` (no deep-MOND transition): fails C3/C4 (D2-supp §1) `[X]`.
- `√(1+x²)−1`-based objects: wrong normalization, F2 `[X]` — including their attractive
  Born–Infeld and de Sitter–Unruh readings, already logged there.

**Space-closure statement.** Within "monotone μ: [0,∞)→[0,1), odd, μ(∞)=1" the standard
literature points are μ_dual (P4), μ_std, μ_simple (P3), the exponent family (P1), and
the celerity scalings (P2, vacuous). The inputs kill exactly: exponent family and
μ_simple by μ′(0)=1; μ_dual by the chiral coordinate (+ Cassini); μ_std survives.
**No claim is made that this list is exhaustive** `[O]` — an undiscovered μ with
μ′(0)=1 that fails Postulate R would leave the selection incomplete, and the covariant
question (D2's Q3) remains the only route to closing it from below.

---

## 3. What the expansion does to the ledger — RN-CO-04, full status

| claim | status | source |
|---|---|---|
| 𝒞: E1–E12 all verified equivalent | **[D]** | script, 13/13 |
| μ_simple = tanh(½ asinh x) | **[D]** new | §2 P3 |
| celerity family redundant with a₀; μ′(0)=1 is double-duty | **[D]** new | §2 P2 |
| Selection summary: μ′(0)=1 kills P1(n≥2)+P3; chiral coordinate kills P4 | **[D]** | §2 |
| The chiral reading of μ→0 (unpolarized, not absent) remains `[C]`, not derived | unchanged | D2-supp §5 |
| Covariant forcing of μ (Q3 / AeST) | **[O]** unchanged | D2-supp §6.4 |
| Everything here assumes Postulate R or the chiral coordinate as input | **[O]** — F3 enforced | §2 P4 |

**F1–F7 applied.** F1: domains stated (ℝ, odd; all limits measured). F2: single
convention pinned at top; E11 quarantined. F3: P4 states exactly what is not derived.
F4: enforced three times (Theorem D; P3's triple kill counted once; P2's "second
parameter" exposed as units). F5: script re-runnable, 0 failures; Lean gap (odd k)
recorded in `MuStdUniqueness.lean` and unchanged. F6: μ_std vs μ_simple vs μ_dual are
**not** separated by rotation-curve data at the a₀ crossover (the D2 supplement's own
falsification criterion); separation used: solar-system precision (P4 addendum).
What separates μ_std from μ_simple **observationally** is exactly nothing available —
μ_simple dies on the normalization input, not on data; flagging this is F6's honest
output. F7: no SU(2)/covariant claim is made or used here.

---

## 4. Reproduce

```bash
python3 scripts/representation_audit_mu_std.py    # sympy 1.14 + mpmath only
```

Expected: `13 symbolic checks, 0 failures`; the P-family table prints measured
μ′(0) values (1, 0, 0, 0 for n=1,2,3,4; 1/2 for μ_simple), the Postulate-R residual
`cosh²ψ − coshψ` for μ_simple, and 50-digit confirmation of the half-rapidity identity.
All outputs are measured, not asserted.

---

## 5. Ledger entry

**RN-CO-04 (μ_std) — representation audit complete.** The 𝒞-class (12 verified
representations, selection-free by construction) and 𝒫-class (5 families, each with its
killing input named) are now fully catalogued. New measured facts: the hyperbola
identity E2, the two ODE readings E4/E5, the Gudermannian bridge E6, the half-rapidity
identification of Milgrom's μ_simple (P3), and the a₀-redundancy of the celerity family
(P2). **No new postulate was introduced and none was promoted** (F3); the covariant
route remains the only open path to a from-below derivation `[O]`.

**Next:** RN-CO-04b — controlled isolation of Postulate R (does it follow from any
proper subset of the corpus's other inputs, or is it exactly the input boundary?).
