# Track 1 result: `ℓ=2` and `ℓ=0` are LOCKED — a second no-go

**Date:** 2026-11-18
**Receipt:** `audits/2026-11-18/ell2_ell0_separability.py` (exit 0, deterministic)
**Verdict:** **LOCKED.** No local anisotropic / traceless-Hessian operator can suppress Cassini `Q₂` while preserving the Solar-System monopole.

---

## 1. `[P]` The algebra: the traceless Hessian is radial, not angularly selective

For a spherically symmetric field, the traceless Hessian is exactly

```
S_ij ≡ ∂_i∂_jφ − (1/3)δ_ij∇²φ = (φ'' − φ'/r)(n_i n_j − δ_ij/3)
```

so its self-contraction is

```
S_ij S^ij = (2/3)(φ'' − φ'/r)²
```

a function of `r` **alone**. Verified in sympy. The `ℓ=2` angular pattern `(n_i n_j − δ_ij/3)` is contracted away, leaving a purely radial object.

For a power law `φ = −A r^{−p}`:

```
S_ij S^ij = (2/3)A²p²(p+2)² r^{−2p−4}
|∇φ|²     = A²p² r^{−2p−2}
ratio     = (2/3)(p+2)² / r²
```

Two consequences follow directly, and they are the whole result:

1. **It carries `ℓ=0`.** Any local scalar built by self-contraction of `S_ij` is spherically symmetric on a spherical background. It is therefore *not* blind to the monopole. The intuition that "traceless ⇒ doesn't touch `ℓ=0`" is true of the tensor `S_ij` itself but false of any scalar built from it.
2. **Its radial profile is fixed at `1/r²`.** One coupling `λ` sets one crossover radius `r_cross = √λ`, and the operator's strength relative to the leading term is `(r_cross/r)²` everywhere. There is no second knob.

## 2. `[P]` The only `ℓ=0`-blind option is not covariant

To suppress `ℓ=2` while being *exactly* blind to `ℓ=0` you need an operator with no `ℓ=0` projection on a spherical background. By §1 that requires a term **linear** in `S_ij` contracted with a **fixed** external tensor — e.g. `S_ij T^ij` with `T^ij` the Milky Way tidal field held constant.

That privileges a frame and a background. It is not a covariant local Lagrangian term, and it is not in the corpus.

## 3. `[P]` The radial-profile trap, against the load-bearing Mercury test

`r_M(Sun) = √(GM☉/a₀) = 1.0693×10¹⁵ m = 7148 au`. Mercury sits at `5.79×10¹⁰ m = 0.39 au`. They are separated by `3.41×10⁸` in operator strength.

The binding constraint is Mercury **perihelion precession**, not the monopole acceleration: `1.6 mas/cy` at 2σ (INPOP10a/EPM2011). Via `Δϖ = 2π ã₀ r²/(GM)` per orbit over 415.2 orbits/century:

```
ã₀_max = 1.177×10⁻¹³ m/s²   →   at most 2.973×10⁻¹² of g_N at Mercury
r_cross ≤ 9.99×10⁴ m
strength available at r_M = 8.72×10⁻²¹
```

`[P]` Under the Mercury budget the operator is **8.7×10⁻²¹** of the leading term where `Q₂` is generated. It cannot move `Q₂` at all.

The reverse direction is equally decisive: to reach `Q₂` you need `r_cross ~ r_M`, which puts `3.41×10⁸` times the leading term at Mercury and predicts **1.38×10⁷ mas/cy** against a `1.6 mas/cy` bound — excluded by seven orders.

## 4. `[D]` The constraint that kills it is not the one the brief expected

The brief anticipated SPARC `χ²_ν` drift as the binding constraint. It is not. Because the profile is pinned at `1/r²`, tuning for `Q₂` makes the operator **negligible at galactic radii** (`r ~ 11 kpc` vs `r_M(Sun) = 7148 au`), so **SPARC rotation curves are actually protected**.

That is the one thing this operator gets right, and it is irrelevant: the Solar-System monopole dies first, by seven orders.

## 5. Verdict

| Claim | Tag |
|---|---|
| `S_ij S^ij = (2/3)(φ''−φ'/r)²`, radial | `[P]` |
| Any self-contraction of `S_ij` carries `ℓ=0` | `[P]` |
| `ℓ=0`-blind requires a fixed external tensor (non-covariant) | `[P]` |
| Operator strength ratio is `(r_cross/r)²`, one knob | `[P]` |
| Mercury precession caps `ã₀ ≤ 1.18×10⁻¹³ m/s²` | `[P]` |
| Achievable `Q₂` suppression under that cap | `~0` (`8.7×10⁻²¹` strength) |
| Local anisotropic operator separates `ℓ=2` from `ℓ=0` | **`[X]`** |
| Non-local / background-dependent `S_ij T^ij` escape | `[O]` unbuilt |

## 6. What this adds beyond #228

`#228` showed `Q₂` is not a high-acceleration problem: a perfect screen above `y=30` changes it by 0.031%. That killed *isotropic, magnitude-dependent* screening.

This is independent: it kills the *angularly selective* hope. The traceless Hessian was the natural candidate for "suppress `ℓ=2`, leave `ℓ=0`," and §1 shows the candidate was never angularly selective in the first place — its scalar invariants are radial.

Together the two results close the screening question from both directions: **there is no scale at which to place a screen, and no angular structure with which to aim one.**

The remaining `[O]` escape is the same shape as before: a non-covariant coupling to a fixed external tensor. That is a different theory, not an operator added to this one.
