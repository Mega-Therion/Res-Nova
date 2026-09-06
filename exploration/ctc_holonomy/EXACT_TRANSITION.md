# The transition radius, solved exactly

**Status:** `[O]` exploration. Held out of the manuscript.
**Script:** `exact2.py` (symbolic), confirmed against `find_transition.py` (numeric bisection).

## The eigenvalue law

The characteristic polynomial of the transport generator `M^l_m = Γ^l_{m φ}` on Gödel
factors exactly:

    det(M − λI) = λ² · (λ² − 2sinh⁴r − 2sinh²r + 1)

so the two non-trivial eigenvalues are

    λ = ± √(2 sinh⁴ r + 2 sinh² r − 1)

Writing `u = sinh² r`:

    λ² = 2u² + 2u − 1

- `λ² < 0` → eigenvalues imaginary → **elliptic**: transport is a rotation, and a
  transported frame returns periodically.
- `λ² > 0` → eigenvalues real → **hyperbolic**: transport is a boost, rapidity accumulates
  without bound, and the frame never returns at any winding number.

## The transition, in closed form

`2u² + 2u − 1 = 0` gives the positive root

    u* = (√3 − 1)/2 = 0.36602540378443865

matching the numeric bisection (0.3660254038) to every digit computed. But it simplifies
further. The condition `2u² + 2u = 1` is `u(u+1) = 1/2`, and since
`u(u+1) = sinh²r · cosh²r = (sinh 2r / 2)²`:

    sinh²(2r*) / 4 = 1/2   ⟹   **sinh(2r*) = √2**

    r* = ½ arcsinh √2 = 0.5731079173902944

(bisection: 0.5731079174 — agreement to 10 digits).

## Both thresholds are θ-conditions

| threshold | condition | in terms of θ = 1/√2 |
|---|---|---|
| elliptic → hyperbolic | `sinh(2r*) = √2` | `sinh(2r*) = 1/θ` |
| spacelike → CTC | `sinh(r_c) = 1`, `tanh(r_c) = 1/√2` | `tanh(r_c) = θ` |

And at the CTC threshold the boost eigenvalue is exactly

    λ(r_c) = ±√3        (from λ² = 2·1 + 2·1 − 1 = 3)

## What is and is not established

**Established (symbolically, exactly):** the eigenvalue law, the closed form
`sinh(2r*) = √2`, the value `u* = (√3−1)/2`, and `λ(r_c) = ±√3`. These are theorems about
the Gödel metric with the Levi-Civita connection. They do not depend on the framework.

**Not established:** that `√2 = 1/θ` here is *the same* θ as the framework's chiral floor.
Both are exact and both are simple hyperbolic conditions, which is exactly what makes the
coincidence cheap: `sinh = 1` and `sinh = √2` are the two most natural non-trivial values,
and `tanh(arcsinh 1) = 1/√2` is an identity, not a discovery. **The appearance of θ here is
arithmetic, not yet physics.**

The honest statement: Gödel's rotating geometry has two exact hyperbolic thresholds, and
they take the values `1` and `√2`. The framework's θ is `1/√2`. Whether that is a shared
origin or a shared *arithmetic* is undecided, and nothing in this computation decides it.

## What would decide it

An argument identifying the Gödel radial coordinate `r` with a spin rapidity `ψ`. Absent
that, these are two unrelated variables that happen to satisfy similar-looking conditions.
Until such an argument exists, this must not be cited as support for CLM-10 or for the
chiral floor.
