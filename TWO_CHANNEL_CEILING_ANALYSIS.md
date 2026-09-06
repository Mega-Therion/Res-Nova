# The Two-Channel Ceiling — what κ can and cannot tell us

**Measured 2026-09-06.** Settles the long-standing κ_Y / χ_s collision without
reopening either constant.

## The collision

Two ceilings circulate in the corpus, both produced by the same function:

| name | expression | θ | value |
|---|---|---|---|
| band ceiling `κ_Y` | `√(θ(2−θ))` | 0.7 | **0.953939** |
| spin ceiling `χ_s` | `√(2θ−θ²)` | 1/√2 = 0.7071 | **0.956145** |

`2θ − θ² ≡ θ(2 − θ)` identically. **These are not two results. They are one function
evaluated at two arguments**, differing by 0.002206.

## Finding 1 — the map is injective, so κ does pin θ

Inverting, `θ = 1 − √(1 − κ²)`:

- κ = 0.953939 → θ = 0.699999
- κ = 0.956145 → θ = 0.707106

Each ceiling recovers its own θ exactly. So κ is **not** degenerate; quoting a ceiling
does determine a floor. The earlier worry that "any θ near 0.7 gives κ near 0.95" is
half right and needs stating precisely — see Finding 2.

## Finding 2 — κ compresses θ by ~3.2×, and that is the real problem

`f′(θ) = (1−θ)/√(θ(2−θ))` ≈ **0.31** on this interval, so differences shrink:

| θ | κ |
|---|---|
| 0.65 | 0.936750 |
| 0.68 | 0.947418 |
| **0.70** | **0.953939** |
| **0.7071** | **0.956145** |
| 0.72 | 0.960000 |
| 0.75 | 0.968246 |

A **0.0071** gap in θ produces only a **0.0022** gap in κ — the input difference is
**3.2× larger** than the output difference it creates.

**Consequence: no current observation can distinguish the two ceilings.** Separating
them requires spin measured to better than **±0.0011**. Continuum-fitting and Fe-Kα
methods deliver ~0.05–0.15 — roughly **45× short**. Any claim that black-hole spin data
selects one of these over the other is unsupportable with today's instruments.

The ceiling is therefore **not** where this framework is falsifiable. The floor is:
the same 0.0071 difference is 3.2× more visible in θ than in κ.

## Finding 3 — the two-channel union is NOT the bridge between the settled constants

The corpus settles on floor **0.707** and ceiling **0.953**. Testing whether `f` links
them:

- `f(0.707)` = **0.956112**, not 0.953 — off by 0.0031
- `f⁻¹(0.953)` = **0.697030**, not 0.707 — off by 0.0100

**`f` does not map the settled floor onto the settled ceiling.** It maps 0.707 → 0.9561
and 0.953 → 0.6970, and neither lands on the other settled value.

So one of the following is true, and the corpus should say which:

1. the two constants are **independent**, each derived on its own ground, and the
   two-channel union simply is not the relation between them; or
2. the union relates a **different** pair — e.g. `f(0.7) = 0.953939`, an internally
   consistent pair that is *not* the settled (0.707, 0.953); or
3. `f` is the right structure and one of the two settled values needs its provenance
   restated.

**Nothing here reopens either settled constant.** This is a statement about the
*function*: it cannot be presented as deriving 0.953 from 0.707, because it does not.

## What to fix in the corpus

- Stop describing `κ_Y` and `χ_s` as separate results. They are `f(0.7)` and `f(1/√2)`.
- Never claim spin observations discriminate between them (Finding 2).
- Never write "the ceiling follows from the floor via the two-channel union" while the
  quoted pair is (0.707, 0.953) — Finding 3 says it does not.

Reproduce: the arithmetic is elementary; `f(θ)=√(θ(2−θ))`, `f⁻¹(κ)=1−√(1−κ²)`.
Related: `PillarIV_AntiDriftGate.lean` (`kappaBand`, `twoChannelUnion`,
`kappaBand_at_seven_tenths`), `SovereignSpinCeiling.lean`,
`06_unification_and_spin/two_channel_ceiling_results.json`.
