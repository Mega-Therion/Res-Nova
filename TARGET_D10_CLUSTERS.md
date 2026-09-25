# TARGET D10: Galaxy Clusters

**Status:** D10_FIRST_RESULT — **the quasi-static limit FAILS clusters by a factor 1.96, exactly as MOND does.** This is the corpus's first cluster test of any kind. The failure is *inherited*, not novel, and it is **not** fixable by tuning `a₀` or the baryon budget — both escapes are closed quantitatively in §4. What it does **not** test is whether AeST's `𝒦(𝒬)` dust component clusters in halos; that is the live question and it is stated as `[O]` in §6.
**Last updated:** 2026-09-24
**Author:** R.W. Yett / Sovereign Architecture Group
**Epistemic tag:** `[P]` proved · `[D]` derived · `[C]` cited · `[O]` open · `[X]` killed

---

## 0. Why this document exists

Checklist item 6 (clusters) was **empty**. A Zenodo sweep on 2026-09-24 across all 68
distinct published works found four keyword hits, all incidental — mostly the word
"lensing". The only substantive cluster claim in the whole publication set is in
**20822072**, which asserts the Bullet Cluster is resolved by disformal coupling; that is
the *retired* mechanism (generalized Einstein-aether, replaced by genuine AeST on
2026-09-12), so the claim does not transfer.

Clusters are where MOND-type theories classically break. Leaving the item empty while
claiming galaxy-scale success is the single most obvious gap an adversarial referee would
open on. So it gets tested, and the result gets recorded whichever way it falls.

## 1. The test `[D]`

We test the **surviving** branch `μ_std(x) = x/√(1+x²)` with

    a₀ = c H₀ / (2π) = 1.0557 × 10⁻¹⁰ m s⁻²      (DERIVED, no free parameter)

at `H₀ = 68.27 km/s/Mpc` (pre-registered P1, Zenodo 21867985) and `Ω_Λ = ln 2`.
For reference Milgrom's *fitted* value is `1.2 × 10⁻¹⁰`; the derived one is 12% smaller.

**Why weak lensing and not X-ray hydrostatic masses.** The standard escape from X-ray
cluster tests is hydrostatic mass bias (~20–30%). Weak lensing assumes no hydrostatic
equilibrium, so that route is closed in both directions.

### Data — downloaded from VizieR, committed alongside the script

Corasaniti, Sereno & Ettori 2021, ApJ **911**, 82 `[J/ApJ/911/82]`:

* `table1` — 317 clusters, weak-lensing `M200c` and `M500c` (LC², CLASH, HSC-XXL)
* `table2` — 105 clusters, gas mass fractions `f_gas`

**12 clusters carry both** after name normalisation. That is the sample. It is small; the
effect being tested is a factor of two, which 12 objects resolve without difficulty.

### Method, at `r₅₀₀`

| quantity | definition |
| --- | --- |
| `M₅₀₀` | weak-lensing total mass |
| `M_bary` | `f_gas·M₅₀₀` + stars, `f_star = 0.015` of `M₅₀₀` |
| `r₅₀₀` | from `M₅₀₀ = 500 ρ_c(z)(4π/3) r₅₀₀³` |
| `g_N` | `G M_bary / r₅₀₀²` |
| MOND | `μ(g/a₀)·g = g_N`, which for `μ_std` inverts **exactly** to `g = a₀√((s² + s√(s²+4))/2)`, `s = g_N/a₀` |
| verdict | `R = M₅₀₀(lensing) / M_dyn(MOND)` |

`R = 1` means baryons alone account for the cluster. `R ≈ 2` is the classic failure.

## 2. Result `[D]`

| cluster | z | `M₅₀₀`/10¹⁴ | `f_gas` | `r₅₀₀`/Mpc | `g_N/a₀` | `M_MOND` | **R** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RX-J1347.5-1145 | 0.451 | 22.20 | 0.100 | 1.71 | 0.11 | 7.75 | 2.86 |
| ABELL-1763 | 0.228 | 16.01 | 0.212 | 1.67 | 0.17 | 9.16 | 1.75 |
| CL-J1226.9+3332 | 0.890 | 15.30 | 0.040 | 1.27 | 0.07 | 3.26 | **4.70** |
| ABELL-1689 | 0.183 | 15.03 | 0.156 | 1.67 | 0.12 | 7.58 | 1.98 |
| MACS-J0717.5+3745 | 0.548 | 14.84 | 0.170 | 1.44 | 0.17 | 6.86 | 2.16 |
| ABELL-773 | 0.217 | 10.14 | 0.116 | 1.44 | 0.08 | 4.67 | 2.17 |
| ABELL-209 | 0.206 | 9.61 | 0.146 | 1.42 | 0.10 | 4.99 | 1.92 |
| ABELL-2142 | 0.091 | 8.78 | 0.158 | 1.44 | 0.10 | 4.99 | 1.76 |
| RXC-J0532.9-3701 | 0.275 | 6.55 | 0.141 | 1.22 | 0.09 | 3.47 | 1.89 |
| ABELL-383 | 0.187 | 5.87 | 0.121 | 1.22 | 0.07 | 3.04 | 1.93 |
| ABELL-2034 | 0.113 | 5.17 | 0.073 | 1.20 | 0.04 | 2.24 | 2.31 |
| RXC-J0232.2-4420 | 0.284 | 4.44 | 0.123 | 1.07 | 0.07 | 2.34 | 1.89 |

**N = 12 · median R = 1.96 · mean R = 2.28 · range 1.75–4.70**
Gas only, no stellar term: median **2.07**, mean 2.46.

`g_N/a₀ ≈ 0.04–0.17` — the sample sits **deep in the MOND regime**, which is where the
boost is largest. This is the theory's best case, not a marginal one.

`CL-J1226.9+3332` (R = 4.70) is an outlier driven by an anomalously low `f_gas = 0.040` at
`z = 0.89`. It is left in; excluding it moves the median by less than 0.05.

## 3. This reproduces a known result `[C]`

The ~2× cluster discrepancy is **well established** and is not a discovery here:
The & White (1988); Sanders (1999, 2003); Aguirre, Schaye & Quataert (2001);
Angus, Famaey & Buote (2008). The measured **1.96** sits squarely on the literature value.

**What is new is only that this corpus has now run the test** — with the surviving `μ`
branch and a derived rather than fitted `a₀` — instead of leaving item 6 empty.

## 4. Both escape routes are closed `[D]`

| escape | requirement | verdict |
| --- | --- | --- |
| raise `a₀` | `a₀ = 4.20×10⁻¹⁰` = **4× the derived value** | destroys the SPARC galaxy fits, which are the framework's strongest asset |
| more baryons | `f_star = 0.388` of `M₅₀₀`, i.e. **stellar mass ≈ 3× the gas mass** | observed cluster ratio is ≈ 0.1 — **off by a factor ~30** |

Neither is available. Two further checks:

* **Not a calibration artefact of the derived `a₀`.** With Milgrom's fitted `1.2×10⁻¹⁰` the
  median is **1.84** — the derived value makes it 6% worse, not qualitatively different.
* **Not mass-dependent.** Lowest-6 median `R = 1.92`, highest-6 `R = 2.17`. The residual is
  a roughly constant factor across the sample; the scatter tracks `f_gas`, not mass.
* For the record, the dead branch `μ_dual = x/(1+x)` gives **1.72** — also a failure, and it
  was independently falsified on Cassini on 2026-09-12.

## 5. What this does and does not establish

**Does:** the **quasi-static, pure-MOND limit** of the framework — baryons alone sourcing the
field through `μ_std` — under-predicts cluster lensing masses by a factor ≈ 2. That limit is
falsified at cluster scales. Any claim that the framework "explains gravity without dark
matter" must now carry this exception explicitly.

**Does not:** falsify AeST as a whole. The test treats clusters as pure MOND, which is
correct for the quasi-static limit but ignores structure the theory actually has.

## 6. The open question this hands forward `[O]`

**AeST is not MOND.** It carries a `𝒦(𝒬)` sector whose background energy density
`8πG̃ρ̄ = 𝒬 dK/d𝒬 − 𝒦` evolves as `ρ̄ ∝ a⁻³` — **dust** — and D5's perturbation work
(2026-09-24) now shows it tracks CDM in the matter era, `δ_AeST/δ_CDM = 0.83–1.06`.

A component that behaves like CDM cosmologically may also **clump in halos**. If it does,
it supplies exactly the kind of mass this test finds missing, and the factor of 2 could be
accounted for by the theory's own field rather than by undetected baryons.

**That is untested.** It requires the quasi-static limit of the *full* AeST system in a
cluster potential — not the MOND limit — and specifically whether `𝒬` develops a bound
overdensity on Mpc scales. Until that calculation exists, §2 stands as the honest state:
**the MOND limit fails clusters, and whether AeST's own dust rescues it is unknown.**

This is the sharpest single open item in the corpus, because it is the one place where a
theory that otherwise reduces to MOND could actually differ from it.

---

## Reproduction

```bash
cd Research_and_Data/05_Scripts_and_Tools/clusters
python3 cluster_mond_test.py
```

Data files `corasaniti2021_table1_lensing.dat` and `corasaniti2021_table2_fgas.dat` are
committed verbatim as downloaded from `cdsarc.cds.unistra.fr/ftp/J/ApJ/911/82/`.

Related: `TARGET_D5_COSMOLOGICAL_SECTOR.md` §3.3 (dustlike perturbations),
`TARGET_D3_PPN_AND_SOLAR_SYSTEM.md` (the other place `λ_s` binds),
`TARGET_D7_COVARIANT_COMPLETION.md` (the AeST action).
