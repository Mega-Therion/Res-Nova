# ⚠ `SPARC_DERIVED_MU_BENCHMARK_REPORT.json` — NOT A LIKE-FOR-LIKE COMPARISON

**Do not cite this file's GOD-vs-MOND comparison.** Superseded by
`02_galaxy_dynamics/PARAMETER_LEDGER.json`.

The historical artifact is left unaltered; this note sits beside it.

## The defect

The report compares:

| entry | μ | a₀ | median χ²/point |
|---|---|---|---|
| `derived_zero_param` | x/(1+x) | **1.042e-10 — DERIVED** | 30.31 |
| `legacy_control_standard_mond` | x/√(1+x²) | **1.2e-10 — FITTED** | 17.01 |

**MOND is handed an empirically fitted a₀ while GOD is held to its derived value.** The
resulting 2× gap measures the benefit of fitting a parameter, not a difference between
the theories. Read naively it says GOD loses to MOND, which is the opposite of what a
matched comparison shows.

## The correct comparison

`02_galaxy_dynamics/PARAMETER_LEDGER.json` — identical nuisance treatment (Yd, Yb, fd)
across GOD, MOND and NFW:

**Tier 0, zero free parameters:**

| | median χ²_red | mean | frac < 2 | aggregate χ²/dof |
|---|---|---|---|---|
| **GOD** | **9.20** | **35.11** | **24** | 51.45 |
| MOND | 11.35 | 37.50 | 19 | **50.22** |

GOD wins median, mean and frac<2; **MOND wins aggregate χ²/dof by 2%** — record that
honestly, it is dominated by the worst-fitting galaxies.

**Tier 1, 374 shared nuisance parameters:** effectively tied — GOD median 2.952 / mean
5.198, MOND median 2.887 / mean 5.275. Each wins one metric by ~2%.

**Tier 1 NFW:** median 1.92 — better than both, with **716 fitted parameters**.

## Why the tier-0 result is the one that counts

Per the ledger's own provenance block: GOD's a₀ is **derived** (cH₀/2π) and its
interpolation function is **derived**; MOND's a₀ is **fitted** and its interpolation
function is **chosen by hand**. GOD therefore wins tier 0 while carrying strictly less
freedom. A tie on equal footing would be a result; a win with fewer knobs is stronger.

Nothing here claims GOD beats MOND everywhere. It claims the comparison must be run at
matched parameter counts, and that when it is, the zero-parameter result favours GOD on
three of four metrics.
