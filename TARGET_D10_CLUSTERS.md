# TARGET D10: Galaxy Clusters

**Status:** D10_FIRST_RESULT — **the pure-MOND limit fails clusters by a factor 1.96** (§2), and neither `a₀` nor the baryon budget can rescue it (§4). **But §7 shows that limit does not apply at `r₅₀₀` in the first place**: AeST's own quasi-static equation is *Helmholtz*, not Poisson, and SZ's validity radius `r_C` falls at **0.54 r₅₀₀ for 12/12 clusters** while sitting a factor ~7 outside any galaxy disc. So §2 is a correct test of **pure MOND** and is **not** the AeST prediction. **§8 then shows the `μ²Φ` term has the right sign and roughly the right size to close the gap** — median `R` falls 1.96 → 1.13 at first order — but the expansion parameter is 0.81, so that is *sign and order of magnitude, not a number*. §8 also flags that AeST's own force law is **not** `μ_std`, which bears on items 1 and 5.
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

## 7. **The MOND limit does not apply at `r₅₀₀`** `[D]` — added same day

SZ state, in the passage defining the quasi-static limit:

> *"The solution for `Φ` will be as obtained from [AQUAL] only for `r ≲ r_C` where
> `r_C ∼ (r_M μ⁻²)^(1/3)`, and oscillatory for `r ≳ r_C`. We require `μ⁻¹ ≳ 1 Mpc` so that
> MOND behavior according to [AQUAL] may still be attained **in galaxies**."*

Note the last two words. MOND behaviour is guaranteed **in galaxies**, not everywhere.

### The mass scale is fixed, not free

`μ = √(2𝒦₂/(2−K_B))·𝒬₀`, and `𝒦₂` is fixed by SZ's own `w₀ = 8πG̃ρ̄₀/(4𝒬₀²𝒦₂)`. At the
corpus's parameters (`w₀ = 1.23×10⁻⁸`, `𝒬₀ = 0.1 Mpc⁻¹`, `K_B = 0.1`, `Ω_Λ = ln 2`):

    𝒦₂ = 97.0   →   μ⁻¹ = 0.9895 Mpc

This lands on SZ's stated requirement `μ⁻¹ ≳ 1 Mpc` essentially exactly — an independent
check that the parameter identification is right, since nothing was tuned to produce it.

### Where `r_C` falls

| scale | `r_M` | `r_C` | extent probed | MOND valid? |
| --- | --- | --- | --- | --- |
| Milky-Way-scale galaxy (`M_bar = 5×10¹⁰ M☉`) | 0.008 Mpc | **0.20 Mpc** | ~0.03 Mpc | **yes**, by ~7× |
| the 12 clusters of §2 | 0.25–0.69 Mpc | 0.62–0.88 Mpc | `r₅₀₀` = 1.07–1.71 Mpc | **NO, 12/12** |

**Median `r_C/r₅₀₀` = 0.54.** Every cluster in the sample is probed at roughly **twice** the
radius where AeST's MOND solution stops being valid — while every galaxy sits comfortably
inside it. The theory has a built-in transition scale that falls precisely in the gap
between the regime where MOND works and the regime where it is known to fail.

### Why: the equation is Helmholtz, not Poisson

Varying SZ's published quasi-static action `NT_quasi_Phi` with respect to `Φ` gives

    ∇²Φ + μ²Φ − ∇²φ = 8πG̃ρ/(2 − K_B)

The `+μ²Φ` term with a **positive** sign makes this a **Helmholtz** operator — not Poisson,
and crucially **not Yukawa**. The point-mass Green's function goes as `cos(μr)/r`:
**oscillatory, not exponentially screened.** That is exactly SZ's "oscillatory for `r ≳ r_C`".

**Honest limit of this derivation.** `J(𝒴)` was dropped, which degenerates the `φ` sector
(its equation collapses to `∇²φ = ∇²Φ`, and back-substitution gives the contentless
`μ²Φ = 8πG̃ρ/(2−K_B)`). So this establishes the **operator structure only**. With `J(𝒴)`
present, `∇²φ` is replaced by the nonlinear AQUAL/MOND operator. Script:
`05_Scripts_and_Tools/clusters/quasistatic_field_equation.py`.

### What §7 does to §2

It does **not** retract §2. §2 correctly measures what the *pure-MOND* limit predicts, which
is the right thing to measure and the thing the literature reports. What §7 establishes is
that **§2 is not the AeST prediction at `r₅₀₀`**, and that the gap between them is not a
loophole invented to escape a bad result — it is a scale AeST fixes from parameters already
pinned by the cosmological background.

---

## 6. The open question this hands forward `[O]`

**AeST is not MOND.** It carries a `𝒦(𝒬)` sector whose background energy density
`8πG̃ρ̄ = 𝒬 dK/d𝒬 − 𝒦` evolves as `ρ̄ ∝ a⁻³` — **dust** — and D5's perturbation work
(2026-09-24) now shows it tracks CDM in the matter era, `δ_AeST/δ_CDM = 0.83–1.06`.

A component that behaves like CDM cosmologically may also **clump in halos**. If it does,
it supplies exactly the kind of mass this test finds missing, and the factor of 2 could be
accounted for by the theory's own field rather than by undetected baryons.

**That is untested**, and §7 now gives it a second, sharper edge: the deviation from MOND
at cluster radii is not merely *possible*, it is **required** by the `μ²Φ` term, at a radius
computed from parameters already fixed by the background.

**The calculation this corpus now owes, stated precisely:**

> Solve `∇²Φ + μ²Φ = 8πG̃ρ/(2−K_B) + ∇·[AQUAL operator on φ]` for a realistic cluster
> baryon profile, out to `r₅₀₀ ≈ 2 r_C`, and compute `M_dyn(r₅₀₀)`. Compare with the
> lensing `M₅₀₀` of §2. The question is whether the Helmholtz term supplies the missing
> factor ≈ 2, overshoots, or has the wrong sign.

Two distinct things could close the gap and they are **not** the same mechanism:
(a) the `μ²Φ` oscillatory term in the quasi-static sector (§7), and
(b) clumping of the `𝒦(𝒬)` dust component (§6 above).
Either would differentiate AeST from MOND. Both are open.

This is the sharpest single open item in the corpus, because it is the one place where a
theory that otherwise reduces to MOND is *structurally required* to differ from it, at a
scale it does not get to choose.

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

---

## 8. The `μ²Φ` term: right sign, roughly right size `[D]`/`[O]` — added same day

§7 said the MOND limit does not apply at `r₅₀₀`. This section asks what the `μ²` term
actually *does*. Script: `05_Scripts_and_Tools/clusters/aest_mu2_correction.py`.

### The system, from SZ's own diagonalisation

SZ diagonalise `NT_quasi_Phi` with `Φ = Φ_E + φ`. The kinetic sector separates **exactly**
(verified symbolically), leaving

    ∇²Φ_E          + μ²Φ = 4πG ρ_bary
    ∇·(J′ ∇φ)      + μ²Φ = 4πG ρ_bary          Φ = Φ_E + φ

Subtracting: `∇²Φ_E = ∇·(J′∇φ)`, i.e. `u_E = J′(v²)v` in spherical symmetry. With SZ's MOND
form `J = 2λ_s/(3(1+λ_s)a₀)·𝒴^{3/2}` this gives `u_E = v²/a₀ₑ𝒻𝒻`,
`a₀ₑ𝒻𝒻 = a₀(1+λ_s)/λ_s → a₀` as `λ_s → ∞`. At `μ = 0` it reproduces the MOND law
`g → √(g_N a₀ₑ𝒻𝒻)` exactly — checked symbolically.

### The nonperturbative solve is ill-posed, and that is recorded, not tuned away

`∇²Φ + μ²Φ = source` with `Φ(r_max) = 0` is **Helmholtz**, so it has resonances wherever
`μ r_max ≈ nπ`. With `μ⁻¹ = 0.99 Mpc` the first sits at ≈ 3.1 Mpc — inside the range one
wants to integrate. `solve_bvp` fails on 8–12 of 12 clusters and, where it converges,
returns `M_dyn` up to 50× `M₅₀₀`. **That is the resonance, not a prediction.**

### First order in `μ²`, which is well posed

    W(r) = r²u_E = G M_bary(r) − μ² ∫₀^r r′²Φ(r′) dr′

`Φ < 0` in a potential well, so **the correction is positive — the `μ²` term adds effective
mass.** Evaluating on the unperturbed MOND solution:

| cluster | `R(μ_std)` | `R(AeST, MOND)` | `R(AeST, +μ²)` | `W/W₀` |
| --- | --- | --- | --- | --- |
| RX-J1347.5-1145 | 2.86 | 2.20 | 1.35 | 2.13 |
| ABELL-1763 | 1.75 | 1.29 | 0.83 | 1.93 |
| CL-J1226.9+3332 | 4.70 | 3.78 | 2.68 | 1.75 |
| ABELL-1689 | 1.98 | 1.52 | 0.95 | 2.04 |
| MACS-J0717.5+3745 | 2.16 | 1.59 | 1.13 | 1.69 |
| ABELL-773 | 2.17 | 1.72 | 1.15 | 1.90 |
| ABELL-209 | 1.92 | 1.50 | 1.03 | 1.82 |
| ABELL-2142 | 1.76 | 1.37 | 0.93 | 1.84 |
| RXC-J0532.9-3701 | 1.89 | 1.48 | 1.09 | 1.62 |
| ABELL-383 | 1.93 | 1.55 | 1.13 | 1.68 |
| ABELL-2034 | 2.31 | 1.93 | 1.36 | 1.81 |
| RXC-J0232.2-4420 | 1.89 | 1.52 | 1.18 | 1.53 |
| **MEDIAN** | **1.96** | **1.54** | **1.13** | **1.81** |

**The median discrepancy falls from 1.96 to 1.13.** The `μ²` term has the **right sign** and
**approximately the right magnitude** to account for the cluster gap.

### What this is NOT `[O]`

**The expansion parameter is `W/W₀ − 1 = 0.81`. That is not small.** First order is at the
edge of its validity, so this establishes **sign and order of magnitude, not a number**.
`1.13` must not be quoted as a prediction. `μ r₅₀₀ ≈ 1.45 rad` — the sample sits about
halfway to the first resonance, which is exactly why the expansion is marginal.

A real prediction requires the nonperturbative solve with a **physical** outer condition —
the cluster embedded in the cosmological background, not `Φ → 0` in vacuum. That is the
next calculation, and it is now precisely specified.

### ~~A separate finding~~ — **CORRECTED within the hour** `[D]`

I first wrote here that "the corpus's galaxy-scale interpolation and its own action's
quasi-static limit are not the same function", on the strength of `1.96` vs `1.54`.
**That comparison was not fair and the claim is withdrawn.** I had used only the *MOND
branch* of `J` across the whole range.

Differentiating SZ's full `ℱ` (Letter, `Fcal_exp` neighbourhood) gives the exact result

    J′(v) = λ_s·v / ( (1+λ_s)·a₀ + v ) ,      v = √𝒴 = |∇φ|

so `u_E = J′v = λ_s v²/((1+λ_s)a₀ + v)`, which **interpolates properly**:

| regime | `u_E` | force law |
| --- | --- | --- |
| `v ≫ (1+λ_s)a₀` | `λ_s v` | `g = g_N(1 + 1/λ_s)` — **Newtonian**, with `G` rescaled |
| `v ≪ (1+λ_s)a₀` | `λ_s v²/((1+λ_s)a₀)` | `g = √(g_N·a₀(1+λ_s)/λ_s)` — **MOND** |

So the action *does* have a Newtonian limit at finite `λ_s`, and there is **no inconsistency
with `μ_std` to report**. What I compared was the `λ_s → ∞` limit, in which the crossover
`(1+λ_s)a₀` runs off to infinity and the MOND branch applies everywhere.

**The cluster numbers above are unaffected.** At `g_N/a₀ ≈ 0.1` and `λ_s = 2.2` (D3's bound)
one has `v ≈ 0.38 a₀` against a crossover at `3.2 a₀`, so the sample sits **well inside the
MOND branch** — which is the branch §8 used. §2 and §8 stand.

**What survives as genuinely open `[O]`.** SZ state they model screening as `λ_s → ∞`, and
their CMB/MPS models are run at `λ_s = ∞`. But `J′ → v/a₀` in that limit, i.e. the MOND
branch everywhere and **no Newtonian regime at all** — while `TARGET_D3` derives `λ_s ≲ 2.2`
from Saturn's precession, which is finite. Those two statements are in tension, and the
tension is *in the published theory*, not in this corpus's use of it. Resolving it means
pinning down what `λ_s → ∞` is doing in SZ's cosmology runs versus their quasi-static limit.
**Not resolved here**, and deliberately not asserted either way.

---

## 9. The nonperturbative solve fails — for a reason inside the model `[D]` — added 2026-09-25

§8 said a real prediction needs the nonperturbative solve with a **physical** outer
condition rather than `Φ → 0` in vacuum. That was attempted. It does not converge, and the
reason is structural.

### The setup, done correctly this time

§8's solve sourced the Helmholtz equation on the **total** density and truncated at an
arbitrary `r_max`. Both are wrong cosmologically. Corrected:

* source on the **density contrast** `δρ = ρ_gas − ρ̄_m(z)`, which is **compensated** — there
  is a radius `r_c` where the enclosed excess mass returns to zero;
* boundary conditions `W(r_min) = 0` and `Φ(r_c) = 0`. At `r_c` the cluster exerts no
  further influence, so this is a gauge choice, not a truncation;
* the **full** `J′(v) = λ_s v/((1+λ_s)a₀ + v)`, not just its MOND branch.

For ABELL-1689: `r_c = 15.3 r₅₀₀ = 25.5 Mpc`.

### The controlled test

Same cluster, same source, same boundary conditions — **only `μ` varied**:

| | result |
| --- | --- |
| `μ = 0` (pure MOND, compensated) | **converged** |
| `μ = ` real AeST value | **failed** — "maximum number of mesh nodes exceeded" |

Resolution is not the issue: it still fails at **29,000 nodes per wavelength**.

### The mechanism

1. `μ r_c = 25.8 rad` — about **4.1 full Helmholtz oscillations** inside the compensation
   radius.
2. That oscillation drives the enclosed effective mass, hence `g_N`, **through zero** about
   once per half-period. At `μ = 0` there is exactly **one** crossing (at `r_c`, by
   construction) and the solver handles it.
3. The MOND branch gives `v ∼ √(u_E A/λ_s)`, so `dv/du_E ∼ 1/√u_E` **diverges** at every
   crossing. Measured: `dv/du_E =` 6.0, 60, 6.0×10², 6.0×10³ at `u_E/a₀ =` 10⁻², 10⁻⁴,
   10⁻⁶, 10⁻⁸.

**The right-hand side is non-Lipschitz at every zero of `g_N`, and the `μ²` term manufactures
a sequence of them that pure MOND does not have.**

### What this means

The `μ²Φ` term is **not a free bonus** that supplies the missing cluster mass. It buys the
right sign and roughly the right size (§8) at the cost of the **well-posedness** of the
boundary-value problem. §8's first-order estimate — median `R` from 1.96 to 1.13, expansion
parameter 0.81 — is therefore the most that can be claimed from this sector. The
nonperturbative solve does not merely fail to converge; **it fails for a reason internal to
the model.**

**Not resolved, and the options are named:** a regularised interpolation (Hölder rather than
square-root near `g_N = 0`), a non-spherical or time-dependent treatment, or the conclusion
that the quasi-static limit is inapplicable at `r ∼ 15 r₅₀₀`. Each is a real research step;
none is a tuning knob.

Script: `05_Scripts_and_Tools/clusters/aest_cluster_compensated.py`.
