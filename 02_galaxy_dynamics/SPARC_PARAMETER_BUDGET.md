# SPARC parameter budget

**Source of numbers:** `PARAMETER_LEDGER.json`, `NFW_CONSTRAINED.json`, `A0_MEASUREMENT.json` (commit `3c90ef3e`).
**Script:** `parameter_ledger.py`, `nfw_constrained.py`, `a0_measure.py`.
**This file replaces the older budget prose that still spoke the withdrawn zero-parameter language.**

Shared functional form for GOD and MOND rows: `\tau=1/2+\sqrt{1/4+a0/g}`, i.e. dual-channel `\mu(x)=x/(1+x)`.

Nuisances `Y_d`, `Y_b`, `f_d` are observational, applied identically when present. They are counted in the free-parameter totals at Tier 1.

## Tier 0 — no per-galaxy freedom

| Model | `a0` source | Free params | Median reduced `χ²` | Aggregate `χ²`/`\mathrm{dof}` |
|---|---|---:|---:|---:|
| GOD | `cH0/(2π)` `[O]` | 0 | 9.20 | 51.45 |
| MOND | literature `1.2e-10` | 0 | 11.35 | 50.22 |
| NFW | — | — | cannot run | a halo with no parameters is not a halo |

This is the only tier that discriminates where `a0` came from.

## Tier 1 — matched per-galaxy nuisances

| Model | Shape params | Free params | Median reduced `χ²` | Notes |
|---|---|---:|---:|---|
| GOD | 0 | 374 | 2.95 | `a0` still horizon `[O]` |
| MOND | 0 | 374 | 2.89 | `a0` literature |
| NFW free `c` | 2 per galaxy | 716 | 1.92 | 97/171 railed at `c=1`; **not** the `Λ`CDM row |
| NFW cosmological `c` prior | 2 per galaxy + Dutton & Macciò 2014 prior | 716 | 5.62 | 3/171 railed; this is the fair `Λ`CDM-like row |

`716 - 374 = 342` extra NFW parameters versus GOD at Tier 1.

Held to its own concentration prior, NFW’s median is 5.62 against GOD’s 2.95. That is the “half as well / 342 more parameters” sentence. It is a reproduction of the cusp-core problem, not a new law of nature.

## Working `a0` (not a budget row, a measurement)

`a0 = 1.116\times 10^{-10}` ± `0.128\times 10^{-10}` (stat) ± `0.097\times 10^{-10}` (syst), `N=171`, 3375 points. Total 14.4%. Horizon `0.46\sigma`. MOND `0.52\sigma`.

## Provenance tags (`PARAMETER_LEDGER.json`)

- GOD `a0`: called “DERIVED, `cH0/2π`” in the JSON, and correctly tagged `[O]` in the same field. The word DERIVED there is historical. This budget treats it as an external cosmological input, not a theorem.
- GOD `μ`: derived, dual-channel `[P]`.
- MOND `μ`: chosen; several variants exist in the literature.
- NFW: two fitted halo numbers per galaxy.
