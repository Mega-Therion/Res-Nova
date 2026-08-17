<div align="center">

# RES NOVA
### Geometrically Ordered Dynamics & Information Tension Theory
**A New Thing**

---

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21969121.svg)](https://doi.org/10.5281/zenodo.21969121)
[![Release](https://img.shields.io/badge/Release-v1.6.2-0052FF.svg?style=for-the-badge&logo=github)](https://github.com/Mega-Therion/Res-Nova/releases/tag/v1.6.2)
[![Lean 4 Verified](https://img.shields.io/badge/Lean_4-17_Modules-4B32C3.svg?style=for-the-badge&logo=lean)](05_lean_formalization/)
[![Epistemic Covenant](https://img.shields.io/badge/Epistemic-v1.6.2_%5BP%5D_%5BD%5D_%5BC%5D_%5BO%5D-D4AF37.svg?style=for-the-badge)](EPISTEMIC_BOUNDARY_v1.5.0.md)
[![SPARC a0](https://img.shields.io/badge/SPARC_a0-1.116e--10_%C2%B1_14.4%25-00C781.svg?style=for-the-badge)](02_galaxy_dynamics/A0_MEASUREMENT.json)
[![Vercel Live](https://img.shields.io/badge/Observatory-Live_Deployment-000000.svg?style=for-the-badge&logo=vercel)](https://res-nova-observatory.vercel.app)

<br/>

**Author:** [Ryan W. Yett](https://orcid.org/0009-0001-1303-7190) &nbsp;|&nbsp; **Affiliation:** Independent Theoretical Research &nbsp;|&nbsp; **Release:** `v1.6.2` &nbsp;|&nbsp; **Epistemic seal:** `v1.6.2`

[**For referees**](FOR_REFEREES.md) &nbsp;•&nbsp; [**Open problems**](OPEN_PROBLEMS_AND_TESTS.md) &nbsp;•&nbsp; [**Agent covenant**](AGENT_COVENANT.md) &nbsp;•&nbsp; [**Manuscript Source**](final_manuscript.tex) &nbsp;•&nbsp; [**Observatory**](https://res-nova-observatory.vercel.app)

</div>

---

## Theoretical overview

Res-Nova is a closed variational identity for one interpolating function, plus the relativistic parents that survive gravitational-wave speed, plus a SPARC measurement that no longer pretends to 0.4% precision.

Zero free parameters is **withdrawn** as a current claim. Dual-channel `μ` is derived. The acceleration scale is measured. Horizon language is a hypothesis under test.

```
                      Bulk Kinetic Flux + Horizon Dissipation     [motivation, not a theorem]
                                              |
                                              v
                      F(x) = 1/2 x^2 - x + ln(1+x)               [P] algebraic
                                              |
                                              v
                      μ(x) = x / (1+x)                           [P] F'(x)
                                 /                    \
                                /                      \
              SPARC measurement [D]              Skordis-Zlosnik parent [P]/[C]
              a0 = 1.116e-10 ± 14.4%             c_T = c, γ_PPN = 1
```

---

## Core pillars

### 1. Dual-channel variational closure `[P]`

The single-channel map whose derivative behaves like `arcsinh` inverts the required limits and is correspondence-false (`PAPER_01` is quarantined). Balancing the two channels isolates

`F_{dual}(x) = x^2/2 - x + ln(1+x), \qquad x = |\nabla\Phi|/a0`

`\mu(x) = F_{dual}'(x) = x/(1+x)`

`\lim_{x\to 0} \mu(x) = x` (deep MOND / BTFR), `\lim_{x\to\infty} \mu(x) = 1` (Newton).

That is an identity. It is not a proof that the universe chose this action.

### 2. SPARC measurement `[D]` — current numbers from commit `3c90ef3e`

Working value (`A0_MEASUREMENT.json`, 171 galaxies, 3375 points; bootstrap over galaxies, not points):

`a0 = (1.116 \pm 0.128_{stat} \pm 0.097_{syst}) \times 10^{-10}\,\mathrm{m\,s^{-2}}` (14.4% total).

`c H_0/(2\pi)` lies `0.46\sigma` away. MOND's `1.2\times 10^{-10}` lies `0.52\sigma` away. Those two inputs are not separated at `z=0`.

Matched-parameter ledger (`PARAMETER_LEDGER.json`, `NFW_CONSTRAINED.json`):

| Specification | Free params | Median reduced `χ²` | Role |
| :--- | ---: | ---: | :--- |
| GOD Tier 0 (horizon `a0`, fixed M/L) | 0 | 9.20 | only tier that tests `a0` source |
| MOND Tier 0 (literature `a0`) | 0 | 11.35 | same |
| GOD Tier 1 | 374 | 2.95 | shared `μ`, horizon `a0` still `[O]` |
| MOND Tier 1 | 374 | 2.89 | shared `μ`, fitted `a0` |
| NFW free `c` | 716 | 1.92 | 97/171 railed at `c=1`; **not** the `Λ`CDM row |
| NFW cosmological `c` prior | 716 | 5.62 | fair `Λ`CDM-like row; 342 extra params vs GOD |

**SUPERSEDED** method (do not quote as current): 176-parameter in-sample median `χ²/N_g = 2.92` with `a0 = (9.433 \pm 0.050)\times 10^{-11}`. That error bar treated 3391 radial points as independent and the old 5-fold CV leaked one global `a0` into every test fold.

### 3. Covariant parents `[P]`

- Pure RAQUAL / k-essence is superluminal on halo backgrounds.
- Disformal `B(\phi)\ne 0` fails `|c_T/c_\gamma-1|\le 10^{-15}`.
- Dual-channel `F` embeds in Skordis–Złośnik (2021) with `c_T=c` and `γ_{PPN}=1` in the physical frame.

---

## Lean inventory

Seventeen modules, 0 `sorry`, axioms `{propext, Classical.choice, Quot.sound}`, Mathlib `5eec30bc`, Lean `v4.33.0-rc1`. Gate: `05_lean_formalization/verify_all_proofs.sh`.

O6 — walked once in a clean worktree at 07185a6 (lake exe cache get + 17/17 PASS, VERIFICATION_RUN_007). Not yet demonstrated on a cold machine with empty host cache, and not yet a CI release gate.

---

## Epistemic covenant

`[P]` proved &nbsp;|&nbsp; `[D]` computed here &nbsp;|&nbsp; `[C]` cited &nbsp;|&nbsp; `[O]` quarantined.

Full matrix: [`EPISTEMIC_BOUNDARY_v1.5.0.md`](EPISTEMIC_BOUNDARY_v1.5.0.md). Agent rules: [`AGENT_COVENANT.md`](AGENT_COVENANT.md). Opens: [`OPEN_PROBLEMS_AND_TESTS.md`](OPEN_PROBLEMS_AND_TESTS.md).

---

## Reproduction

```bash
git clone https://github.com/Mega-Therion/Res-Nova.git
cd Res-Nova
python3 scripts/check_claim_consistency.py

# Lean (see O6)
cd 05_lean_formalization
# lake exe cache get
./verify_all_proofs.sh

# SPARC regeneration needs data that is not in git (see 02_galaxy_dynamics/SPARC_DATA.md)
cd ../02_galaxy_dynamics
# python3 a0_measure.py
# python3 parameter_ledger.py

cd ..
pdflatex -interaction=nonstopmode final_manuscript.tex
bibtex final_manuscript
pdflatex -interaction=nonstopmode final_manuscript.tex
```

Python pins: `requirements.txt` / `environment.yml`. CI runs claim hygiene and `py_compile` only. It does not download Mathlib or SPARC.

---

## Repository topology

```
Res-Nova/
├── 01_foundational_action/       # variational papers; PAPER_01 is quarantined
├── 02_galaxy_dynamics/           # SPARC scripts + frozen JSON
├── 03_observer_jwst/             # high-z interface; not a completed [D] campaign
├── 04_cosmology/                 # a0 / Ω ledgers; Ω_Λ=ln2 is [O]
├── 05_lean_formalization/        # 17 Lean modules + verify_all_proofs.sh
├── FOR_REFEREES.md
├── OPEN_PROBLEMS_AND_TESTS.md
├── AGENT_COVENANT.md
├── EPISTEMIC_BOUNDARY_v1.5.0.md
├── final_manuscript.tex          # v1.5.0 technical assessment
└── visualizer/                   # observatory
```

---

## Related publications (Zenodo)

Concept DOIs below resolve to the latest record version. Several titles still say “zero-parameter.” Those titles are historical. They are not the current claim of this repository. Updating a Zenodo title is a DOI-owner decision, not a git edit.

**SPARC / dark-matter alternative — Res-Nova lineage**
- Information Tension: A Zero-Parameter Geometric Alternative to Dark Matter on SPARC — [10.5281/zenodo.21233977](https://doi.org/10.5281/zenodo.21233977)
- Information Tension: Geometric Projection Replaces Dark Matter at Low Acceleration (v3, audit-corrected) — [10.5281/zenodo.21146462](https://doi.org/10.5281/zenodo.21146462)
- Parameter-Free Acceleration Scale: A Geometric Derivation of the MOND Scale from the Cosmic Horizon — [10.5281/zenodo.21450424](https://doi.org/10.5281/zenodo.21450424)
- Pre-Registered Falsifiable Predictions — Information Tension / Geometrodynamics (v2, corrected) — [10.5281/zenodo.21864056](https://doi.org/10.5281/zenodo.21864056)

**Relativistic and cosmological completion**
- Relativistic Formulation of the Information Tension Field — [10.5281/zenodo.20822071](https://doi.org/10.5281/zenodo.20822071)
- ΩCDM: A Pre-Registered Cosmological Prediction — Ω_Λ = ln 2 as a Fixed Constant — [10.5281/zenodo.21867984](https://doi.org/10.5281/zenodo.21867984)
- Pre-Registration: Ω_Λ = ln(2) — [10.5281/zenodo.21131485](https://doi.org/10.5281/zenodo.21131485)
- Geometric Accretion Limits in Early-Universe Supermassive Black Holes — [10.5281/zenodo.20776360](https://doi.org/10.5281/zenodo.20776360)

**Broader framework**
- Universal Information Geometry (v2, corrected) — [10.5281/zenodo.20348354](https://doi.org/10.5281/zenodo.20348354)
- The Observerse as an E8 Branching — [10.5281/zenodo.20142808](https://doi.org/10.5281/zenodo.20142808)
- Geometrodynamica (v5) — [10.5281/zenodo.21539453](https://doi.org/10.5281/zenodo.21539453)
- Ars Magna: Geometrically Ordered Dynamics — [10.5281/zenodo.21302150](https://doi.org/10.5281/zenodo.21302150)
- The Law of G.O.D. — [10.5281/zenodo.20117456](https://doi.org/10.5281/zenodo.20117456)

---

<div align="center">

**Res-Nova Observatory & Research Program**

*AI proposes. Machines verify. Humans audit. Evidence persists.*

</div>
