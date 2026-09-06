# SPARC Model Comparison — canonical statement

**Cite this and `PARAMETER_LEDGER.json`.** 175 galaxies, 3,375 points, identical
nuisance treatment (Yd, Yb, fd) across every model. Any other GOD-vs-MOND figure in this
repository is superseded — see `VERIFICATION_RUN_002/02_sparc/README_SUPERSEDED_BENCHMARK.md`.

## Tier 0 — zero free parameters

| model | median χ²_red | mean | frac < 1 | frac < 2 | aggregate χ²/dof |
|---|---|---|---|---|---|
| **GOD** | **9.200** | **35.11** | 9 | **24** | 51.45 |
| MOND | 11.352 | 37.50 | 9 | 19 | **50.22** |

GOD wins **median (−19%)**, **mean (−6%)** and **frac<2 (24 vs 19)**.
MOND wins **aggregate χ²/dof by 2.4%** (50.22 vs 51.45).

**State the loss as well as the wins.** Aggregate χ²/dof is dominated by the few
worst-fitting galaxies, so the split between it and the median says GOD fits the typical
galaxy better while MOND handles the tail marginally better. That is a real and
interesting difference, not a rounding artifact, and it is a lead worth chasing: which
galaxies drive it, and do they share a property?

## Tier 1 — 374 shared nuisance parameters

| model | median χ²_red | mean | frac < 1 | frac < 2 | free params |
|---|---|---|---|---|---|
| GOD | 2.952 | **5.198** | 21 | 59 | 374 |
| MOND | **2.887** | 5.275 | 23 | **60** | 374 |
| NFW | **1.921** | **3.933** | **53** | **88** | **716** |

GOD and MOND are **statistically tied** — each takes one metric by ~2%. NFW fits best
and uses **716 fitted parameters against GOD's zero**.

## The comparison that matters, and why

From the ledger's provenance block:

| | a₀ | interpolation |
|---|---|---|
| **GOD** | **DERIVED**, cH₀/2π | **DERIVED**, Thm 8.7, μ(x)=x/(1+x) |
| MOND | **FITTED** to rotation curves (1.2e-10) | **CHOSEN by hand**; several variants in use |
| NFW | — | 2 **FITTED** shape params per galaxy (c, V200) |

> **GOD wins tier 0 on three of four metrics while carrying strictly less freedom than
> MOND.** MOND's a₀ was fitted to this class of data; GOD's was derived from a horizon
> argument before the fit. A tie under those conditions would already be a result.

## What must NOT be claimed

- **Not** "GOD beats MOND." It beats MOND on three tier-0 metrics and loses one; at
  tier 1 they are tied.
- **Not** "GOD beats dark matter on fit quality." NFW fits better. The claim is about
  **parameter cost**: 716 fitted parameters versus zero.
- **Not** that a₀ = cH₀/2π is unconditionally derived. It rests on the horizon argument,
  epistemic tag `[O]` in the ledger, and is one of the two irreducible parameters.

## Open

1. Identify which galaxies drive MOND's tier-0 aggregate advantage. A shared property
   would be a physical lead; no shared property makes it noise in the tail.
2. Tier-1 parity means the nuisance parameters absorb the difference between the two
   interpolation functions. Worth stating explicitly in any paper: at 374 parameters,
   rotation curves do not discriminate μ.
