# REPRESENTATION AUDIT: the empirical acceleration scale a₀ — SPARC layer

**Status:** RESULT — the SPARC/a₀ empirical layer receives the same 𝒞/𝒫
representation discipline as μ_std. Every number below is measured from the
corpus's own JSON artifacts (`A0_MEASUREMENT.json`, `A0_ESTIMATE.json`,
`A0_REEXTRACTION_MU_STD.json`) by `scripts/a0_representation_audit.py`
(run 2026-09-16, all checks pass). One new two-axis structure is surfaced (§2).
**Last updated:** 2026-09-16
**Tags:** `[P]` proved · `[D]` derived/verified here · `[C]` cited/conjectured · `[O]` open · `[X]` killed
**Framework:** Res-Nova Core Objects Version 0.2. Executes ledger item **RN-CO-05**.

---

## 0. Canonical statement, restated exactly

The working scale is `a₀` as it appears in `τ(g) = ½ + √(¼ + a₀/g)`,
`v = v_bary√τ`. Its empirical value is **extraction-μ-dependent** (§3) — the
live-closure (μ_std) value is **1.156×10⁻¹⁰ m/s²**, bootstrap 68%
[1.0615, 1.2342]×10⁻¹⁰, harness-qualified. The corpus's canonical *claimed* value is
`cH₀/2π = 1.0421×10⁻¹⁰ m/s²`, which implies `H₀ = 67.4 km/s/Mpc` (C1, measured).
Provenance, in the corpus's own words: **derived-cH₀/2π is `[O]`; the fitted a₀ is
data**. The 1/(2π) prefactor's first-principles origin remains open.

## 1. 𝒞-class: three dresses of the same claimed number `[D]`

All three are *identical* (measured, C1–C3) — no selection content, Theorem-D
discipline applies:

| dress | statement | measured |
|---|---|---|
| horizon | `a₀ = cH₀/2π` | 1.0421e-10 (H₀ = 67.4 implied) |
| crossing time | `c/a₀ = 2π/H₀` — the MOND scale's light-crossing time is one Hubble *period* | 2.877e18 s both sides |
| frequency | `a₀/c = H₀/2π` | 3.476e-19 Hz both sides |

The crossing-time dress is the cleanest: **the claim says the MOND acceleration is
the scale at which light crosses one Hubble cycle.** Same number, no new content —
but it is the dress that connects to the de Sitter–Unruh route of the μ_std audit
(there the 2π is a *discrepancy*; here it is the *content*; do not merge the two
readings — D41).

## 2. 𝒫-class, family by family — what kills what

### P1. The H₀-choice family `a₀ = cH₀/2π` at different H₀ — **new two-axis tension map `[D]`**

| H₀ | a₀ = cH₀/2π | vs μ_std window [1.0615, 1.2342]e-10 |
|---|---|---|
| Planck 67.4 | 1.0422e-10 | **OUTSIDE**, −1.32 σ_boot |
| canonical 70 | 1.0824e-10 | inside, −0.85 σ_boot |
| SH0ES 73.0 | 1.1288e-10 | inside, −0.32 σ_boot |

**The finding:** the horizon claim's health is a function of *two independent axes* —
which μ extracted a₀, and which H₀ measurement the claim is anchored to. Under the
legacy (μ_dual-era) harness the canonical claim sat at 0.46σ (measured, legacy
stat+syst). The honest μ_std re-extraction (2026-09-12) **worsens** the Planck-H₀
agreement (now outside the 68% window) and **improves** the SH0ES one. **No verdict
is drawn from this** — the Hubble tension is unresolved, and picking SH0ES to save
the coincidence (or Planck to kill it) would be F3 in either direction. The map is
the result; the map is also the warning: *any* future statement of "a₀ ≈ cH₀/2π at
Nσ" must state both its extraction μ and its H₀ anchor, or it is not a claim.

### P2. The Λ / de Sitter forms — **not equivalent to the Hubble form** `[D]`

Measured (Ω_Λ = 0.69): `c²√Λ/2π = 1.4993e-10` (factor √(3Ω_Λ) ≈ **1.439 high**),
`c·H_dS/2π = 8.657e-11` (factor √Ω_Λ ≈ **0.831 low**), vs canonical 1.0421e-10.
The canonical claim is therefore **specifically the Hubble-radius form** — not the
de Sitter-horizon form, not the bare-Λ form — and the discriminators are measured,
cosmology-dependent numbers. The corpus has never before stated which horizon the
"horizon argument" uses; the answer is now on the record: **the Hubble one** `[O]`
(as a derivation; as a numerical match, P1 above).

### P3. Milgrom's `a_dS = cH₀` (no 2π) `[X]` as a match

Measured: 6.548e-10 — factor ~2π (5.66×) off the live window. The 2π is *required*
for agreement and remains *unexplained* `[O]` (the same offset the μ_std audit
flagged on the Unruh route). What would kill or keep the 2π: a covariant derivation
of the prefactor (Q3-adjacent), or the a₀(z) test resolving (P5).

### P4. The extraction-μ dependence — **a₀ is not μ-invariant** `[D]`

Measured on the *identical* harness: μ_dual → 9.285e-11 (68% [8.487, 1.005]e-10 is
wrong — correctly [8.4872e-11, 1.0054e-10]); μ_std → 1.1562e-10 (68% [1.0615,
1.2342]e-10). **Shift +24.5%; windows do not overlap.** Direction provable
algebraically: μ_std(x) > μ_dual(x) for all x > 0 (⟺ 0 < 2x), so at fixed a₀ the
same data sits deeper in MOND and the fit compensates upward. Consequence, now
binding on every future table in the corpus: **the fitted-a₀ row must state its
extraction μ; the measured object is the pair (μ, a₀), not a₀ alone.** This also
retroactively qualifies `PARAMETER_LEDGER.json`'s "MOND_a0: FITTED (1.2e-10)" —
that literature value is a μ-mixed ensemble, and the corpus's own zero-free-parameter
tier uses μ_std, so cross-referencing them at face value is F6.

### P5. Precision / evolution constraints (F7) `[D]`, corpus's own record

The v3 a₀(z) test under the live closure: Δχ² = 0.750, **0.87σ, INCONCLUSIVE**,
never conclusive anywhere in the bootstrap 68%. The earlier 5.9σ constant-a₀
verdict was extracted under the falsified μ_dual and is **unrecoverable** — a₀(z)
remains open, not ruled out. Solar-system precision (Cassini) killed μ_dual, not a₀.
Exact-pipeline reproduction of the legacy 1.107e-10 number remains open `[O]`
(the corpus's own validation-gap note; harness qualification is part of every a₀
statement above).

## 3. F1–F7 applied

F1: domains = the 175-galaxy SPARC benchmark, 3391 points, SHA-256-verified
rotmod files; stated. F2: two harnesses (legacy / re-extraction) are never merged;
each number is harness-qualified. F3: the cH₀/2π proximity stays a coincidence
observation; the two-axis map exists precisely so no σ-verdict gets promoted from
a moving target. F4: the three 𝒞-dresses counted once; P1's three H₀ points are one
family, not three tests. F5: `scripts/a0_representation_audit.py` re-runnable, reads
only corpus artifacts; no Lean file touched. F6: the (μ, a₀) pair is the measured
object; μ_simple-extracted a₀ is unmeasured and flagged `[O]`. F7: a₀(z)
inconclusive; Cassini bounds live on the μ side and were applied in the μ_std audit.

## 4. Reproduce

```bash
python3 scripts/a0_representation_audit.py    # stdlib only; reads corpus JSONs
```

Expected output: C1–C3 identities; P1 table (−1.32 / −0.85 / −0.32 σ_boot);
P2 factors 1.439 / 0.831; P3 ratio 5.66; P4 shift +24.5%, windows not overlapping;
P5 Δχ² = 0.750, 0.87σ INCONCLUSIVE.

## 5. Ledger entry

**RN-CO-05 (a₀ representation audit) — complete.** The 𝒞-class of the horizon claim
(3 identical dresses, selection-free) and the 𝒫-class (5 families: H₀-choice,
Λ-forms, a_dS, extraction-μ, evolution) are catalogued with what kills what.
New measured structures: the **two-axis tension map** (extraction μ × H₀ anchor —
the claim's health is not a single number until both are pinned); the Λ/de Sitter
forms' measured discrimination (√(3Ω_Λ), √Ω_Λ) showing the claim is specifically the
Hubble-radius form; and the binding statement that **the SPARC-measured object is
the pair (μ, a₀)** — μ_std-extracted a₀ = 1.1562e-10, +24.5% vs μ_dual on the
identical harness, windows disjoint. The 5.9σ constant-a₀ result remains
unrecoverable `[X]`; a₀(z) stays open; the 2π origin stays open `[O]`.

**Next:** all four sequenced actions of Pass 1.5 are now complete (μ_std audit →
Postulate R isolation → McKay prior-art packet → a₀/SPARC audit). The audit cycle's
natural continuations: (i) close the exact-pipeline validation gap `[O]`;
(ii) a μ_simple-extracted a₀ row for the (μ, a₀) map; (iii) the first
physical-interpretation layer under Version 0.2 rules, now with every algebraic
and empirical input boundary mapped.
