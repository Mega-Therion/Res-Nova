# Gemini memo: convention, dark-bubble, and speed comparison

**Memo reviewed:** [Depth-Dependent Dispersion, Catastrophe Caustics, and Conservative Hydrodynamics on a Finite-Thickness Superfluid Bubble-Wall Cosmology](https://share.gemini.google/WSbeUhQq0q9S)  
**Res Nova baseline:** `Mega-Therion/Res-Nova` at `212b55a8`

## 1. The `ε = 1/2` versus `ε = 1/√2` inconsistency

The memo defines the observer offset in its synthesis as `ε = d/ΔR = 1/2`, but immediately assigns the decimal value `0.707107`. That decimal is `1/√2`, not `1/2`:

```text
1/2       = 0.5000000000
1/√2      = 0.7071067812
```

The same paragraph then defines the observer coordinate as `ζ = 2ε − 1 = √2 − 1 ≈ 0.414214`. That equality is also compatible with `ε = 1/√2`, because `2/√2 − 1 = √2 − 1`; it is not compatible with `ε = 1/2`, which gives `ζ = 0`. Thus the paragraph simultaneously calls the point a midplane observer and uses the geometry of an off-center point.

The distance ratio makes the distinction even clearer. If `ε = d_in/ΔR` is the fraction measured from the inner rim, then:

| Convention | `d_in/ΔR` | `d_out/ΔR` | `d_in/d_out` | `ζ = 2ε − 1` |
|---|---:|---:|---:|---:|
| Midplane | `1/2 = 0.5` | `1/2 = 0.5` | `1` | `0` |
| Off-center | `1/√2 ≈ 0.7071` | `1 − 1/√2 ≈ 0.2929` | `1 + √2 ≈ 2.4142` | `√2 − 1 ≈ 0.4142` |

The memo’s rim-transfer formula is

```text
R_rim(u; ε) = cosh(2εu) / cosh(2(1−ε)u).
```

At `ε = 1/2`, the numerator and denominator are identical, so

```text
R_rim(u; 1/2) = 1
```

for every `u`. There is no outer-rim dominance under the symmetric midplane convention. This also agrees with the memo’s statement that a midplane observer receives zero sinuous potential.

At `ε = 1/√2`, the ratio is nontrivial. Direct evaluation gives:

| `u` | `R_rim(u; 1/2)` | `R_rim(u; 1/√2)` |
|---:|---:|---:|
| `0.05` | `1.0000000000` | `1.0020711905` |
| `0.5` | `1.0000000000` | `1.2083885624` |
| `1.363` | `1.0000000000` | `2.6265357322` |
| `3` | `1.0000000000` | `11.6600187372` |
| `5` | `1.0000000000` | `62.7578129953` |

These reproduce the memo’s listed values `1.0021`, `1.2084`, `2.6265`, `11.66`, and `62.76`. Therefore the memo’s numerical rim-dominance claims use `ε = 1/√2`, even though the opening convention and the later midplane discussion use `ε = 1/2`.

This is not merely a notation typo. It changes the qualitative conclusion from exact symmetry (`R_rim = 1`) to exponential outer-rim dominance. Before the result can be treated as a physical prediction, the memo must choose one convention, define whether `ε` is measured from the inner rim, outer rim, or midpoint, and regenerate every `ζ`, Jacobian, asymmetry, and observational claim from that frozen definition.

## 2. Comparison of the dark-bubble obstruction

### What the Gemini memo claims

The memo studies a stringy AdS5 dark-bubble construction in which Standard Model non-Abelian gauge fields couple through bulk B/C fields. Its stated chain is:

1. `Tr(F) = 0` for the non-Abelian SU(3) sector.
2. The sign rule therefore assigns gluons the negative gravitational-weight branch.
3. The memo quotes a proton matrix-element difference `0.009 ± 0.037` and summarizes the resulting proton gravitational/inertial ratio as approximately `0.99`.
4. It calls the resulting weak-equivalence violation roughly 13 orders above the quoted bound and concludes that viable bubble walls must avoid B/C worldvolume gauge couplings.

### What Res Nova already records

Res Nova has an existing, artifact-backed `[X]` record for this mechanism. `CURRENT_STATE_READ_THIS_FIRST.md` identifies the dark-bubble embedding as `[X]` as formulated and points to `WEP_2507_03748_AUDIT.json`, `PHASE3_WALL_GHOST_AUDIT.json`, `PHASE3_WALL_GHOST_COUPLED.json`, and related receipts. The WEP audit records the same sign rule:

```text
w_net = −1 + β;
β = 2 for the Abelian linear channel gives +1;
β = 0 for su(N), because Tr(F) = 0, gives −1.
```

It also records `Aq − Ag = 0.009 ± 0.037`, a fractional deviation of `0.991`, and a robust order-one deviation after allowing for scheme-dependent quantities. The repository’s current conclusion is that the B/C construction is excluded as formulated and that reopening it requires a different mechanism giving non-Abelian worldvolume fields weight `+1` together with a derived quark sign.

### Important difference in experiment attribution

The mechanism-level conclusion agrees, but the memo should not be copied verbatim into the repository’s evidence ledger. The Res Nova receipt explicitly distinguishes active from passive mass. It notes that MICROSCOPE primarily tests passive free fall and that a universal active factor would be absorbed into `G4`; the decisive issue is composition-dependent active mass. The current-state summary therefore describes the exclusion as an active-mass WEP problem constrained by LLR at roughly 11 orders, not as a direct 13-order MICROSCOPE result.

Accordingly:

- **Agreement:** the B/C non-Abelian coupling is excluded in the stated construction; the sign mechanism and order-one proton effect are already represented in Res Nova artifacts.
- **Not yet justified for import:** the memo’s exact “13 orders” wording and its attribution to MICROSCOPE.
- **Repository action:** none required. The existing `[X]` record is stronger provenance than the shared memo. Any update should be a source cross-reference and an explicit active/passive-WEP clarification, not a new physics claim.

## 3. Conditional superluminality and relation to `c_T = c`

### The Gemini memo’s conditional claim

The memo computes the longitudinal AQUAL stiffness as

```text
c_s²(x) = c_0² F_std''(x),
```

and states that `F_std''(x) > 1` for `x > xφ ≈ 0.7862`, with a maximum `F_std''(2) ≈ 1.0887`. It then says that if the asymptotic nonrelativistic sound scale is identified with the vacuum light speed, `c_0 = c`, the scalar/acoustic speed becomes superluminal:

```text
c_s/c = sqrt(F_std''(x))
max(c_s/c) = sqrt(1.0887) ≈ 1.0434.
```

That conclusion is conditional on two separate assumptions: the AQUAL-BEC stiffness formula is the relevant physical characteristic cone, and `c_0` equals the vacuum speed of light. If `c_0` is a nonrelativistic sound scale such as tens to hundreds of km/s, the same 8.87% stiffness overshoot does not imply propagation faster than `c`.

### What Res Nova’s `c_T = c` result says

Res Nova’s D8 result concerns the **tensor gravitational-wave mode** in the corrected minimal-coupling AeST theory. The repository derives `c_T = c` structurally from the tensor-sector kinetic identity/no transverse-traceless contribution under the stated action. The result is labelled `[D]`, not an unconditional Lean `[P]`, and it is explicitly separated from the retracted disformal/vector theory.

The repository separately records scalar-sector stability and branch questions. In `PEER_REVIEW_READINESS.md`, D6 describes a scoped scalar-speed condition `c_s < c` under its stated parameter inequality, while D7 remains conditional on branch selection. The corrected AeST action in `TARGET_D7_COVARIANT_COMPLETION.md` is scalar-sector AeST with minimal matter coupling to `gμν`; it is not the Gemini memo’s finite-thickness AQUAL-BEC wall action.

Therefore there is no direct contradiction:

- Gemini memo: conditional statement about a scalar/acoustic AQUAL-BEC characteristic speed under `c_0 = c`.
- Res Nova D8: derived statement about the tensor gravitational-wave speed in the corrected AeST action.
- They concern different modes and different model sectors.
- `c_T = c` does not imply every scalar sound speed equals `c`, and a scalar superluminality claim would not by itself refute the tensor-speed derivation.
- Conversely, Res Nova cannot use `c_T = c` to validate the Gemini memo’s scalar wave sector; that would require deriving the scalar characteristic matrix from the same covariant action and matter coupling.

The proper next gate, if the Gemini scalar claim were ever proposed for Res Nova, would be to freeze the exact action, identify the physical metric and causal cone, derive all scalar/vector/tensor principal symbols, and test hyperbolicity and observational propagation speeds without setting `c_0 = c` by assumption.

## Final classification

The `ε` issue is a reproducibility-blocking convention error: the listed rim numbers are `ε = 1/√2` numbers, not `ε = 1/2` numbers. The dark-bubble obstruction is substantially redundant with an existing Res Nova `[X]` record, but the memo overstates or misattributes the experimental bound unless its active/passive distinction is corrected. The superluminality statement is conditional and concerns a different scalar/acoustic sector; it does not contradict Res Nova’s scoped tensor result `c_T = c`.

## References

[1]: https://share.gemini.google/WSbeUhQq0q9S "Shared Gemini memo"
[2]: https://arxiv.org/abs/2507.03748 "Dark-bubble source paper cited by the Res Nova audit"
