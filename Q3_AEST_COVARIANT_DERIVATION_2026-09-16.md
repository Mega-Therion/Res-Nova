# Q3/AeST — THE COVARIANT DERIVATION OF THE CELERITY IDENTIFICATION (B)

**Status:** OBLIGATION 1 OF INTERPRETATION LAYER 0 — **DISCHARGED TO THE STATED LIMIT.**
A reduction theorem is delivered: within the covariant premises the AeST embedding
supplies, the external gradient enters as **sinh of the internal rapidity** (B), and
(B) is equivalent to μ_std. What remains open is now surgical and named: the
**momentum-linearity of the coupling (K3)** — uniqueness is proved, forcing is not.
No new `[P]` physics is claimed; everything algebraic here is machine-checked
(`scripts/q3_covariant_derivation.py`, 19/19).
**Date:** 2026-09-16
**Tags:** `[P]` proved · `[D]` derived/verified here · `[C]` cited/conjectured · `[O]` open · `[X]` killed
**Framework:** Res-Nova Core Objects Version 0.2. Discharges ledger open-item 2
(obligation 1) to the stated limit; sharpens open-item 2's residue.

---

## 1. What Q3 was asked to derive

Layer 0, obligation 1: *derive (B) covariantly — the external gradient enters as
sinh of the internal rapidity; not "derive MOND".* The input table's (B) row says
x = sinh(artanh μ), x ≡ |∇Φ|/a₀. The audits had established that everything else
is theorem given (B): μ_std = tanh(arsinh x) is an algebraic identity away
(REPRESENTATION_AUDIT_MU_STD, C-identities E1–E12), the Fisher identity and the
x² conjugacy follow (Theorems A, B), and Postulate R's remaining content is (A)
(POSTULATE_R_ISOLATION, witnesses W1–W3).

So a successful Q3 collapses the input table: derive (B) covariantly and μ_std
stops being a choice. D2-supp §6 item 4 recorded the honest starting state: "No
covariant argument yet… the only route that would make this physical rather than
chosen."

## 2. The premises the covariant embedding supplies [C] [D]

All three are drawn from the AeST action exactly as the corpus carries it
(TARGET_D7_COVARIANT_COMPLETION §1, Skordis–Złośnik PRL 127, 161302 (2021)):

- **K1 — a boost sector exists.** The embedding is Lorentz-covariant; the aether
  A^μ defines at every point the local frame of the quasistatic reduction. The
  chiral two-state channel's internal transformations along this frame include the
  boost group so(1,1) ≅ (ℝ, +)_ψ — rapidity is its additive (Lie-algebra)
  parameter. `[C]`
- **K2 — channel states carry a unit norm.** The aether's norm is enforced in the
  action by the Lagrange multiplier λ(A^μA_μ + 1); the quasistatic scalar sector
  inherits the projection q_{μν} = g_{μν} + A_μA_ν. Unit-norm states on the boost
  orbit have momentum components (cosh ψ, sinh ψ) — this is forced, not chosen:
  it is the unique norm-preserving orbit through the rest state (verifier C1a, C1b;
  the tangent's Minkowski norm is preserved along the hyperbola). `[D]`
- **K3 — the gradient couples to the boost's momentum.** The quasistatic reduction
  is AQUAL, ∇·[𝒥′(𝒴)∇φ] = 4πĜρ with 𝒴 = q^{μν}∂_μφ∂_νφ = |∇⊥φ|²: the external
  gradient enters the channel's dynamics as a **momentum**, and only through its
  spatial (aether-orthogonal) component. `[C]`

## 3. Theorem B-cov [D]

**Statement.** Given K1–K3, the external gradient measured in a₀ units is the
spatial momentum of the channel's internal boost:

$$x \;=\; \frac{|\nabla\Phi|}{a_0} \;=\; \sinh\psi\,,$$

where ψ is the internal rapidity; with the chiral velocity reading μ = tanh ψ
(the cascade's definition, ψ = artanh μ), this is exactly **(B): x = sinh(artanh μ)**.

**Proof sketch (each step machine-checked).**

1. By K2, the channel's state on the boost orbit has energy and spatial-momentum
   components E(ψ) = cosh ψ, P(ψ) = sinh ψ (verifier C1a, C1b).
2. By K1, ψ is the canonical boost parameter — the only coordinate on the orbit
   under which the boost sector is additive, hence the only one a covariant
   coupling can be linear in.
3. By K3, the external gradient is a momentum conjugate to the channel's boost.
   The covariantly available momentum component is P(ψ) = sinh ψ — the force
   conjugate to ψ under the invariant constraint energy a₀(cosh ψ − 1) is
   ∂/∂ψ [a₀ cosh ψ] = a₀ sinh ψ (verifier C2). Identifying the gradient's scale
   as a₀ fixes the proportionality: x = sinh ψ. `[D]`
4. The velocity reading μ = tanh ψ = P/E is the cascade's own (the bounded,
   two-state variable; chirality ψ → −ψ flips μ, verifier C3a, C3b).

**Corollary (the collapse, `[D]`).** Inverting (B): μ = tanh(arsinh x) = x/√(1+x²)
— μ_std, identically (verifier C4a, C4b, C5). Given the covariant premises, the
interpolation function is not a choice. The input table's (B) row — and with it
Postulate R's (B) clause — becomes theorem-given-covariance; what remains as input
is (A), the chiral alphabet, and μ′(0) = 1, exactly as POSTULATE_R_ISOLATION
foresaw ("If Q3 ever succeeds, the input table above collapses").

## 4. The alternatives — every other coupling is killed (space closure) `[D]`

The point of K1+K2 is that they leave almost nothing to choose. Enumerate the
other covariantly definable couplings of the gradient to the boost sector:

| coupling | resulting μ | verdict |
|---|---|---|
| spatial momentum (K3) | tanh ψ = **μ_std** | **the theorem** `[D]` |
| rapidity itself (x = ψ) | tanh x | violates K3: ψ is not a momentum; a ψ²/2 channel energy is Galilean, not boost-invariant; fails Postulate R's odds-rectification (verifier C6a) `[X]` |
| velocity (x = μ) | μ = x | P5 non-interpolation: μ(∞) = ∞, no deep-MOND transition (verifier C6b); killed by data `[X]` |
| odds of velocity | x/(1+x) = μ_dual | presence coordinate — a different rectification, not the chiral one (verifier C6c); killed by the chiral input + solar-system falsification (audit P4) `[X]` |
| half-rapidity momentum | tanh(ψ/2) = **μ_simple** | the half-angle point (verifier C6d, C6d2); killed by the normalization knife μ′(0) = ½ (verifier C7b) — with the measured empirical shadow a₀ displaced ×0.469 ≈ ½ (the 3μ map) `[X]` |

The half-rapidity row deserves its remark: tanh(ψ/2) is the spinorial half-angle
point of the same orbit — and it is exactly the μ the knife kills. The covariant
picture explains why μ_simple was ever a candidate (it is the other natural point
of the boost orbit) and why it is wrong (a unit-norm state boosted by ψ carries
momentum sinh ψ, not sinh(ψ/2); the half-angle state is a *different state*, not
the same state's coordinate — and it fails the deep-MOND normalization).

## 5. What is NOT derived — the honest residue `[O]`

Per the D2-supp §6 discipline (item 4 was written to prevent exactly this
overclaim), state the limits before anyone cites this:

1. **K3's linearity is uniqueness, not forcing.** The theorem shows the sinh
   coupling is the *only covariant* one. AeST does not *force* it: 𝒥's functional
   freedom can still mimic other couplings at the price of breaking K1/K2's
   manifest covariance (hiding it in a non-obvious frame). The gap "does the
   embedding *force* μ_std" remains open — but it has moved: it is now the
   question of whether hidden non-covariance is distinguishable, which is a
   question about 𝒥's regularization, not about the interpolation's shape.
2. **(A) is untouched.** The chiral alphabet remains the primitive it was
   (obligation 2). This theorem derives (B) *given the channel's velocity reading*,
   and that reading is the chiral cascade's.
3. **μ′(0) = 1 is untouched** (obligation inherited, unchanged, D2-supp item 3).
4. **The 2π / Hubble-form triangle is untouched** (obligation 3). Nothing here
   predicts a₀'s value — only its functional shape's coupling. The de Sitter–Unruh
   route's obstacles stand as layer 0 §5 states them.
5. **The aether-inheritance reading of K1/K2 is `[C]`, not `[D]`.** The theorem
   is covariant in form; that the *channel's* boost sector is the aether's is a
   reading (N1–N2 territory), anchored but not proved.

**Net movement of obligation 1:** from "no covariant argument yet" to "covariant
uniqueness delivered; forcing residual named (K3-linearity)". Layer 1 of
interpretation opens on this theorem's terms — but only with (A) still owed.

## 6. Falsifiability (this document's own stakes)

- If a covariant embedding is found whose channel couples to ψ (rapidity) rather
  than P(ψ) — K1/K2 respected — Theorem B-cov's step 3 fails and (B) returns to
  input status. The alternatives table then becomes the test bench.
- The half-rapidity row is *already* empirically falsified (0.469 shadow); the
  rapidity row (x = ψ → μ = tanh x) is falsifiable by Postulate R's battery plus
  the (μ, a₀) map: its extraction would displace a₀ by its own factor, outside
  the μ_std window — the standing battery (`scripts/falsifier_battery_mu_a0_map.py`)
  now gates exactly this.

## 7. Reproduce

```bash
python3 scripts/q3_covariant_derivation.py        # 19/19 checks, exit 0
python3 scripts/falsifier_battery_mu_a0_map.py    # standing map + battery, exit 0
```

## 8. Ledger

- **Open-item 2 (Q3 / obligation 1): discharged to the stated limit** — Theorem
  B-cov delivered; (B) ⟺ μ_std machine-checked; residue renamed: **K3-linearity
  (uniqueness ≠ forcing)**. Status `[O]` → `[O-sharp]`: no longer "no covariant
  argument yet".
- **Open-item 8 / RN-CO-05b: formalized** as a standing harness
  (`scripts/falsifier_battery_mu_a0_map.py`): map checks A1–A3 + battery T1/T2 on
  any candidate; references verified (std passes, dual fails T2, simple fails T1).
- Layer 0 §3's N2 gains covariant support: its tag upgrades from `[C]`-on-(B) to
  `[C]`-on-[D]-covariant-uniqueness. The narrative statements themselves are
  unchanged.
- No `[P]` status changes. The finite algebraic core, the empirical audits, and
  the frozen ledger are untouched by this document.
