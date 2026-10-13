# Pillar IV: the two-level steady state written in μ_std

**Status:** `[D]` for the identities (computer algebra, solved from the generator). `[O]` for any physical identification of the drive ratio with the galaxy ratio g/a₀. No tier of any existing row changes.
**Date:** 2026-10-13
**Machine:** `scripts/pillar_iv_mu_identity.py`, 14 checks, exit 0.
**Inputs:** the GKSL generator of `05_lean_formalization/PillarIV_AntiDriftGate.lean` §2: H = u σ_x, jump operator σ₋ at rate γ.

## Result

Let y = 2√2 · u/γ and μ = μ_std(y) = y/√(1+y²). The steady state of the generator is, exactly:

| quantity | value |
|---|---|
| excited population ρ₁₁ | μ²/2 |
| Im ρ₀₁ (Re ρ₀₁ = 0) | μ√(1−μ²)/√2 |
| coherence C = 2\|ρ₀₁\| | √2 · μ · √(1−μ²) = 4x/(1+8x²), x = u/γ |
| relation free of u and γ | (Im ρ₀₁)² = ρ₁₁(1 − 2ρ₁₁) |
| maximum of C | 1/√2, at μ = 1/√2, i.e. y = 1, u/γ = 1/(2√2), ρ₁₁ = 1/4 |

Under complex conjugation (equivalently u → −u) the populations are unchanged and ρ₀₁ changes sign.

## What this corrects and what it does not claim

- The premise retracted on 2026-09-03 identified the coherence with μ(u/γ). That identification is false (check G14). The exact statement is that μ_std, at the argument 2√2·u/γ, gives the excited population as μ²/2; the coherence is √2·μ·√(1−μ²).
- The value μ = 1/√2 is where the coherence is largest. This agrees with the settled reading of Pillar IV as a ceiling, and gives the ceiling a second form: it is the point y = 1 of μ_std.
- That μ_std appears here is an algebraic fact about this generator. It does not show that the galaxy interpolating function is a two-level population, and it does not identify y with g/a₀. That reading is `[O]`.
- The identities are algebraic consequences of the steady-state formulas. A Lean statement of them would be a field identity and is not offered as `[P]`.

## Reproduce

```bash
python3 scripts/pillar_iv_mu_identity.py   # 14 checks, exit 0
```
