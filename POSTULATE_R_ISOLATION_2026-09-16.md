# POSTULATE R: CONTROLLED ISOLATION — the input boundary of the μ_std theorem

**Status:** RESULT — the attempted derivation fails, honestly, and the failure is
productive: Postulate R is shown to decompose into exactly **two independent inputs**,
neither derivable from the rest of the corpus, and is itself **redundant given them**
(a theorem, not a postulate). All claims measured by
`scripts/postulate_r_isolation.py` (sympy, run 2026-09-16, all checks pass).
**Last updated:** 2026-09-16
**Tags:** `[P]` proved · `[D]` derived/verified here · `[C]` cited/conjectured · `[O]` open · `[X]` killed
**Framework:** Res-Nova Core Objects Version 0.2. Executes ledger item **RN-CO-04b**
from `REPRESENTATION_AUDIT_MU_STD_2026-09-16.md`.

---

## 0. What "controlled isolation" means here

A derivation attempt must end in one of two states: (i) Postulate R follows from a
proper subset of the corpus's inputs — then the uniqueness theorem's price drops; or
(ii) it does not — then the witnesses that break each candidate derivation are recorded
and the **minimal independent input set** is stated exactly. This document delivers
(ii), with witnesses. **Scope caveat (F-discipline):** "isolation" here means semantic
independence *within the space of monotone interpolating functions* — witnesses are
exhibited, not a formal independence proof in any proof assistant. The Lean file
`MuStdUniqueness.lean` already formalizes the implication chains; what it cannot
formalize is the *independence*, and we do not claim it does.

**Postulate R (restated).** With `ψ ≡ artanh μ`: `dF/dψ = x²`, under the AQUAL
constitutive `F′(x) = x·μ(x)` `[P]` (D2 §4 Corollary's normalization).

---

## 1. The decomposition theorem `[D]`

Postulate R decomposes into two inputs:

- **(A) The chiral alphabet `[C]`.** The rectified coordinate of the internal channel
  is the rapidity `ψ = artanh μ`, with Fisher information `ℐ_± = 1/(1−μ²)`. Physical
  content: `μ→0` reads as *unpolarized*, not *absent* (D2-supp §5 — a ±1 channel cannot
  be absent).
- **(B) The celerity identification `[O]`.** `x = sinh ψ` — "x is the celerity
  (γβ) of the internal boost whose velocity (β) is μ" (D2-supp §2's generating
  observation, promoted here from reading to *input*).

**Isolation theorem `[D]`, machine-checked both directions.**

1. **(A)+(B)+constitutive ⟹ Postulate R** (script R1): `dF/dψ = F′·dx/dψ =
   x·tanhψ·coshψ = sinh²ψ = x²`. **Residual: 0.** Postulate R is a *theorem* given
   (A)+(B). It is not primitive.
2. **Postulate R+constitutive ⟹ (B) up to the double-duty normalization** (script R2,
   Theorem A of the D2 supplement): the ODE forces `x(ψ) = C·sinhψ`; `μ′(0)=1` fixes
   `C=1`, i.e. exactly (B).
3. **The exponent 2 in `x²` is automatic** (script R3): `dF/dψ = sinh²ψ = x²` under
   (B). The "conjugate variable is x²" clause of Postulate R carries **zero content
   beyond (B)**.

**Refinement recorded against the corpus (honest sharpening) `[D]`:** the D2
supplement motivates `x²` by "*x² = 𝒴/a₀² is the kinetic invariant the field action
actually depends on*". Two corrections: (i) as shown, the `x²` conjugacy is automatic
given (B) — it is not an independently-motivated clause; (ii) the action depends on
`F(|x|)` with `F` **odd**, i.e. on the magnitude of `x`, not on `x²`. The motivation
was a reading; the algebra shows it is not even an available extra input. The
*automaticity* is the cleaner statement, and it is what is now in the ledger.

---

## 2. Independence witnesses — neither input is derived `[D]`

**W1 — (B) is not derivable from constitutive+normalization+boundary.**
`μ_dual = x/(1+x)` satisfies **every** algebraic input of the D2 constraint set
except (A)/(B): constitutive `F′ = xμ` (residual 0), `μ(0)=0`, `μ(∞)=1`, `μ′(0)=1` —
all measured. Yet `sinh(artanh μ_dual) − x = −x + x/√(2x+1) ≠ 0`: (B) fails, and the
presence alphabet `odds(μ_dual) = x` holds instead. μ_dual is killed only by the chiral
reading `[C]` plus the Cassini solar-system falsification (2026-09-12 addendum) —
i.e. exactly by (A) and its empirical support.

**W2 — (B) is not derivable from (A).** `μ_simple` fully accepts the chiral alphabet
(`artanh μ_simple` is a well-defined rapidity) yet `sinh(artanh μ_simple) ≠ x`
(residual measured): its identification is `x = sinh(2ψ_s)` — *two* boosts, not one.
The alphabet does not fix how many boosts the external acceleration is.

**W3 — the rapidity-multiple family, and why μ_simple is not an outlier.** The natural
family of (B)-violations is `x = sinh(n·ψ_s), μ = tanh ψ_s`, measured `μ′(0) = 1/n`
(n = 1, 2, 3): **`n=1` is μ_std, `n=2` is μ_simple** (the half-rapidity identity of
the μ_std audit), and `μ′(0)=1` kills every member with `n ≠ 1`. μ_simple is not an
unrelated competitor that happens to lose; it is the n=2 point of the family the
normalization input was already known to cut.

**Consequence for the ledger.** The minimal independent input set of the μ_std
uniqueness theorem is exactly:

| input | role | status |
|---|---|---|
| constitutive `F′ = xμ` | AQUAL field-equation normalization | `[P]` literature |
| `μ′(0) = 1` | double-duty: units inside the celerity family, selection across P1/P6 | `[O]` input (D2 constraint 3) |
| (A) chiral alphabet | what μ→0 means; rapidity rectification | `[C]` — the honest crux |
| **(B) celerity identification** | x = sinh(artanh μ) | `[O]` — **the only input not previously isolated** |

Everything else in the D2 supplement's chain — Postulate R itself, the `x²` conjugacy,
the Fisher identity at k=4 — is theorem or redundancy. **(B) is the residual content of
Postulate R** once the alphabet is granted. This is the isolation result.

---

## 3. Candidate derivations of (B), examined and adjudicated

Every route the corpus offers was checked; none yields (B).

1. **CLM-10 (Kerr spin rapidity)** — `[X]` as a derivation route. `assurance/claims.json`
   records CLM-10 as state `conditional`, assurance `formal-algebraic-under-adopted-premise`;
   its own header states it "does not assert that Kerr spin is a Lorentz rapidity or that
   sinh(ψ)=1 is physically selected". An adopted premise cannot derive an input. It
   remains what the D2 supplement said: evidence the rectification is *native*, not
   proof.
2. **De Sitter–Unruh temperature reading** — `[C]`, one live candidate. The reading
   (D2-supp §6.1) would make μ_std = acceleration measured in Unruh-temperature units,
   which would *explain* (B). Measured discriminators (script U1): with H₀ = 70 km/s/Mpc,
   `cH₀/2π = 1.082×10⁻¹⁰ m/s²` vs SPARC `a₀ = 1.2×10⁻¹⁰ m/s²` — the 2π form lands at
   **ratio 1.109**; without the 2π, factor ~5.7 off. The 2π is the right order *because
   it is the corpus's own canonical choice*; its first-principles origin remains
   unexplained `[O]` (D5/RN-CO-05 territory). Verdict: motivates (B), derives nothing;
   also inherits the §6.1 normalization caveat. **Pursue only under Q3.**
3. **Covariant forcing (Q3: does the AeST / Skordis–Złośnik embedding force μ?)** —
   `[O]`, unchanged, and now sharpened: Q3's job is precisely to derive **(B)** — no
   more, no less. (A) is a question about the channel's alphabet; (B) is a question
   about the embedding's kinematics. If Q3 ever succeeds, the input table above collapses
   to two `[P]`/`[C]` rows and this document's isolation becomes a historical bound on
   what was assumed before the covariant route closed.
4. **The audited chiral cascade (RN-CO-01…03, DIAG-01, MCKAY-01/02)** — compatibility,
   not derivation `[D]`. The finite algebraic core (BT ≅ 2T by order census, conjugacy
   classes, character table; the pin-cover crack `n² = z`) establishes that a chiral
   ±1 substrate is *consistent* and *available* — the strongest corpus-internal support
   for (A). But the cascade audit is a consistency check: it constructs the substrate
   and proves its fingerprints; it does not connect the substrate to the interpolation
   variable of the galaxy-sector action. **Neither (A) nor (B) follows from it.**
   Recording this prevents the McKay material from being silently upgraded into a
   derivation later (F3/F4 guard).

---

## 4. What would change this verdict

- A corpus-internal derivation of (B) from the action or a covariant embedding
  (Q3 succeeding for the kinematic clause).
- A derivation of (A) from the SU(2)/triality substrate connecting the finite cascade
  to the field variable — the cascade→action bridge is the missing link.
- Either collapses the input table of §2; the witnesses W1–W3 would then record what
  *was* assumed en route (their role is exactly to make such a future derivation's
  additional inputs visible).

Nothing in this document weakens any `[P]` claim. The Lean file `MuStdUniqueness.lean`
is untouched and its implication theorems are unaffected (F5: it formalizes exactly the
R1/R2 implications above, which is why the isolation is *consistent* with, and not
contradicted by, the machine-checked fragment).

---

## 5. Reproduce

```bash
python3 scripts/postulate_r_isolation.py     # sympy only; all residuals printed
```

Expected: R1 residual 0; R2 dsolve `C₁·e^ψ·tanhψ/(1+tanhψ) ≡ C·sinhψ`; W1/W2 nonzero
residuals as printed; W3 μ′(0) = 1, 1/2, 1/3; U1 cH₀/2π = 1.082e-10, ratio 1.109.

---

## 6. Ledger entry

**RN-CO-04b (Postulate R isolation) — complete.** Postulate R decomposes as
(A) chiral alphabet `[C]` + (B) celerity identification `[O]`, given the constitutive
`[P]`; R is a theorem given both (machine-checked), the `x²` clause is automatic, and
each component has an independence witness (μ_dual for (B) vs. the constraint set;
μ_simple/n-family for (B) vs. (A)). The candidate derivation routes CLM-10, de
Sitter–Unruh, and the chiral cascade are adjudicated: none derives (A) or (B); Q3
targets exactly (B). **The μ_std uniqueness theorem's input boundary is now fully
mapped: no hidden inputs remain, and no derived clause is still counted as an input.**

**Next:** RN-CO-MCKAY-03 — literature prior-art packet for the binary-tetrahedral /
McKay material (does the locked finite core say anything the standard literature does
not already say, and are all our [P] fingerprints correctly standard?).
