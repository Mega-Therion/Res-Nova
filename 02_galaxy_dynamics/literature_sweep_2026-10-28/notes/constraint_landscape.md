# Observational constraint landscape for MOND-vein theories (Solar System → galaxies), as of 2026-10-28

Verification note: every arXiv ID below was resolved through the arXiv API (export.arxiv.org/api/query, title/authors/journal_ref/DOI checked against the record). Non-arXiv DOIs were resolved through the Crossref API (api.crossref.org/works/DOI). Numbers marked "full text" were read from the arXiv PDF (pdftotext), not from memory. "PREPRINT" = no journal reference on arXiv and none found. Abbreviations: MG = modified-gravity MOND (AQUAL, QUMOND and their relativistic parents such as TeVeS/BIMOND/AeST in the quasi-static limit); MI = modified-inertia MOND (Milgrom's time-nonlocal models); IF = interpolating function; EFE = external field effect; RAR = radial acceleration relation.

## 1. Solar System tests: what is measured, and which MOND quantity each one bounds

### Takeaway
The Solar System test that matters for MOND is the Galactic-EFE quadrupole Q2. The current bound is Q2 = (1.6 ± 1.8)×10⁻²⁷ s⁻² (1σ; Park et al. 2026, PRD 114, 024066). It bounds how sharply the IF switches from MOND to Newton near g ≈ 2a0, and it applies to MG (AQUAL/QUMOND-type Poisson theories). PPN γ and β, and perihelion bounds, are all consistent with GR at the 10⁻⁵ level. For MOND, they matter mainly as the data the Q2 fit is built from and as checks on the relativistic completion; they do not themselves bound the IF shape.

### Cited Findings
**Q2 (the external-field quadrupole)**
- Origin: in the modified-Poisson (QUMOND/AQUAL) formulation, the Galactic field g_g = η·a0 produces an anomalous quadrupole field near the Sun, g_i = −q_ij u^j, with q_zz = q(η)·a0/R_M and R_M = (GM/a0)^{1/2} ≈ 8×10³ au. Milgrom found 10⁻² < −q < 0.3 across IFs. He notes the prediction is "not generic to the MOND paradigm, but depend[s] on the particular MOND formulation", and that it holds "even if the MOND interpolating function is arbitrarily close to unity at high accelerations." — [Milgrom 2009, MNRAS 399, 474, arXiv:0906.4817](https://arxiv.org/abs/0906.4817)
- Blanchet & Novak computed the effect numerically and derived the planetary perihelion precessions. The effect is "rather large for outer gaseous planets"; for Saturn it is comparable to published range-residuals; for Earth it is "in conflict for most of the MOND functions μ(y) with the very good constraint on the perihelion precession obtained from Jupiter VLBI data". Only IFs with "a very rapid transition" survive. — [Blanchet & Novak 2011, MNRAS 412, 2530, arXiv:1010.1349, DOI 10.1111/j.1365-2966.2010.18076.x](https://arxiv.org/abs/1010.1349)
- Hees et al. 2014: 9 years of Cassini range and Doppler data give **Q2 = (3 ± 3)×10⁻²⁷ s⁻²**, which "excludes a large part of the relativistic MOND theories". The bound can also be read as a limit on any external tidal potential (Galactic DM, or an unseen body). — [Hees, Folkner, Jacobson & Park 2014, PRD 89, 102002, arXiv:1402.6950](https://arxiv.org/abs/1402.6950)
- **Current bound:** Park, Hees, Famaey, Desmond & Durakovic 2026 use the full DE440 dataset plus longer Cassini arcs and estimate Q2 jointly with the ephemeris parameters. Result: **Q2 = (1.6 ± 1.8)×10⁻²⁷ s⁻² (1σ)**, a "40% improvement". Subsets: Cassini Subset 1 gives −1.6 ± 3.6 and Subset 2 gives −2.4 ± 3.9 (×10⁻²⁷ s⁻²). Jupiter's contribution to the MOND Q2 prediction is 0.05%. They state that "a large part of the signature of a non-zero Q2 has been reabsorbed in the fit due to correlations with other estimated parameters" (full text, Table I). Published: Phys. Rev. D 114, 024066 (2026-07-28), DOI 10.1103/r7n8-kw38 (Crossref-resolved). — [arXiv:2602.17884](https://arxiv.org/abs/2602.17884)
- Fienga & Minazzoli (Living Reviews 2024) give the INPOP/MOND framing. MOND adds δΦ(Q2) ∝ Q2 r²(cos²θ − 1/3) along the Galactic-centre direction. Saturn is the most affected planet, and Q2 is fitted directly to Cassini tracking. — [Fienga & Minazzoli 2024, LRR 27, 1, arXiv:2303.01821, DOI 10.1007/s41114-023-00047-0](https://arxiv.org/abs/2303.01821) (full text, Sec. 4.7)

**PPN γ (light deflection / Shapiro delay)**
- Cassini 2002 conjunction: **γ − 1 = (2.1 ± 2.3)×10⁻⁵**. Will's table lists the Cassini time-delay bound on γ − 1 as 2.3×10⁻⁵. — [Bertotti, Iess & Tortora 2003, Nature 425, 374, DOI 10.1038/nature01997](https://doi.org/10.1038/nature01997) (Crossref-resolved); value quoted from [Will 2014, LRR 17, 4, arXiv:1403.7377](https://arxiv.org/abs/1403.7377) (full text)
- Combined planetary-ephemeris constraint, taken from the common overlap of recent INPOP/EPM/DE intervals: **(γ − 1) = (0.55 ± 1.35)×10⁻⁵** and **(β − 1) = (−0.45 ± 1.75)×10⁻⁵**. — [Fienga & Minazzoli 2024, eq. 102, arXiv:2303.01821](https://arxiv.org/abs/2303.01821) (full text)

**PPN β (perihelion / ephemerides / LLR)** (the review's table, ×10⁻⁵; full text, Fienga & Minazzoli 2024)
- EPM2011 (Pitjeva & Pitjev 2013): β−1 = −2 ± 3, γ−1 = 4 ± 6. INPOP13c (Verma et al. 2014): β−1 = 0.2 ± 2.5, γ−1 = −0.3 ± 2.5. INPOP15a: β−1 = −6.7 ± 6.9 (full fit). INPOP20a (Fienga et al. 2021): β−1 = 1.9 ± 6.28, γ−1 = 2.64 ± 3.44 (partial fit). Park et al. 2017 (MESSENGER): β−1 = −2.6 ± 3.9 with γ fixed. Genova et al. 2018 (MESSENGER, Mercury-only): β−1 = −1.625 ± 1.8 with γ fixed. — [arXiv:2303.01821](https://arxiv.org/abs/2303.01821)
  - The primary papers resolve to: [Park et al. 2017, AJ 153, 121, DOI 10.3847/1538-3881/aa5be2](https://doi.org/10.3847/1538-3881/aa5be2) and [Genova et al. 2018, Nat. Commun. 9, 289, DOI 10.1038/s41467-017-02558-1](https://doi.org/10.1038/s41467-017-02558-1) (both Crossref-resolved).
- Lunar laser ranging: **β − 1 = (6.2 ± 7.2)×10⁻⁵**, **γ − 1 = (1.7 ± 1.6)×10⁻⁴**, Ġ/G = (−5.0 ± 9.6)×10⁻¹⁵ yr⁻¹. — [Biskupek, Müller & Torre 2021, Universe 7, 34, arXiv:2012.12032, DOI 10.3390/universe7020034](https://arxiv.org/abs/2012.12032)
- Nordtvedt parameter: LLR (Biskupek et al. 2021) implies η ≈ 5×10⁻⁵; MESSENGER implies η ~ 7×10⁻⁵. — Fienga & Minazzoli 2024 (full text). Will 2014 lists the Nordtvedt-effect bound 2.3×10⁻⁴ on η_N = 4β − γ − 3. — [arXiv:1403.7377](https://arxiv.org/abs/1403.7377)

**Perihelion-precession bounds**
- 1σ uncertainties on the supplementary perihelion advance (mas/yr). EPM2011 (Pitjeva & Pitjev 2013): Mercury 0.03, Venus 0.016, Earth 0.0019, Mars 0.00037, Jupiter 0.28, Saturn 0.0047. INPOP10a (Fienga et al. 2011): Mercury 0.006, Venus 0.015, Earth 0.009, Mars 0.0015, Jupiter 0.42, Saturn 0.0065. Mercury: 0.02 (Fienga et al. 2018) and 0.015 (Park et al. 2017). — [Fienga & Minazzoli 2024, Table 10](https://arxiv.org/abs/2303.01821) (full text)
- Caveat from the same review: it closes with "comments and recommendations regarding misinterpreted measurements of the advance of perihelia". One "cannot simply estimate the modification of the perihelion advance per orbit" from these numbers, because of parameter correlations such as J2⊙ with β−1. A consistent MOND test must refit the ephemeris with the anomaly included, which is what Hees 2014 and Park 2026 do for Q2. — [arXiv:2303.01821](https://arxiv.org/abs/2303.01821)
- DE440 itself: [Park, Folkner, Williams & Boggs 2021, AJ 161, 105, DOI 10.3847/1538-3881/abd414](https://doi.org/10.3847/1538-3881/abd414) (Crossref-resolved).
- Chan & Lee 2023 derive general analytic precession formulae for power-law and exponential extra forces. They constrain two IF families with Solar System data and claim the result "can be generally applied to both of the modified inertia and modified gravity versions of MOND". — [MNRAS 518, 6238, arXiv:2212.01019](https://arxiv.org/abs/2212.01019)

**Isolated-system quadrupole (not the Galactic EFE)**
- QUMOND also predicts a correction for isolated systems smaller than R_M, with a quadrupole ∝ the system's own quadrupole moment Q_ij/R_M⁵. Milgrom: "For generic MOND theories ... the predicted strength of the effect in the Solar system is rather much below present testing capabilities". It is enhanced by k² in theories that become Newtonian only beyond k·a0. — [Milgrom 2012, MNRAS 426, 673, arXiv:1205.1317](https://arxiv.org/abs/1205.1317)

### Inferences
- The MOND quantity bounded by Q2 is the IF value (1 − μ) or ν − 1 at the Sun's Galactic acceleration, g_e ≈ 2a0 (Park 2026 uses a_e = 2.32×10⁻¹⁰ m s⁻²). In other words, it bounds the transition sharpness at ~2a0, not a0 alone. The high-acceleration tail at 10⁻³–10⁻² m s⁻² is irrelevant to it.
- γ and β bound the relativistic completion: any extra scalar/vector coupling at PN order must satisfy |γ−1|, |β−1| ≲ 10⁻⁵. These are pass/fail checks for TeVeS/AeST-type parents. They are not MOND-IF constraints.

### Gaps
- I did not find a post-2021 published INPOP or EPM PPN update (e.g., INPOP21a/23 or EPM2021 numbers) in a verifiable source. The Fienga & Minazzoli table stops at INPOP20a.
- Will's 2014 entry for the perihelion β bound was not extracted. Use the Fienga & Minazzoli numbers instead.
- BepiColombo results (expected to improve β, γ and J2⊙) were not checked.

## 2. The RAR vs Solar System tension in MG-MOND: exact statements, σ levels, and what drives them

### Takeaway
Fitting IF families to SPARC requires a smoother MOND–Newton transition than Cassini Q2 allows. The tension is 8.7σ in Desmond, Hees & Famaey 2024 (fiducial). With the 2026 Q2 it is about 15σ (fiducial), 12σ with free M/L, and 3.8σ/2.8σ with bulge galaxies removed. Bulge-hosting galaxies drive it: the "only bulge" subsample gives 15.9σ. The 2025–2026 MIGHTEE-HI RAR is the main counter-datum. It prefers a sharper IF (δ = 4.10, +1.4/−0.68) that is compatible with Q2.

### Cited Findings
- Desmond, Hees & Famaey 2024 (abstract): the Solar System quadrupole "requires a significantly sharper transition between the deep-MOND and Newtonian regimes than is allowed by the RAR (an **8.7σ tension** under fiducial model assumptions)". Tension is relieved somewhat by M/L freedom, and "more significantly (to **1.9σ**) by removing galaxies with bulges". They also apply an AQUAL flattened-system correction with similar results. "The SS quadrupole constraint implies, to high precision, no deviation from Newtonian gravity in nearby wide binaries." — [MNRAS 530, 1781 (2024), arXiv:2401.04796, DOI 10.1093/mnras/stae955](https://arxiv.org/abs/2401.04796)
- IF families used (full text): n-family ν_n = [1 + (1 + 4x⁻ⁿ)^{1/2}]/2, where n = 1 is Simple and n = 2 is Standard. δ-family ν_δ = (1 − e^{−x^{δ/2}})^{−1/δ}. γ-family as in their eq. 7c. The RAR IF corresponds to δ = γ = 1. EFE models: none, "Freundlich–Oria analytic" (QUMOND) and "AQUAL numerical". Seven M/L priors: fiducial SPARC; free Gaussian hyperpriors; constrained (Υbulge > Υdisk); free uniform; constrained uniform; no-bulge (31 bulge galaxies removed); only-bulge (116 bulgeless galaxies removed). The fiducial-row predicted Q2 is ≈ 29×10⁻²⁷ s⁻², about 10× the Cassini central value. — [arXiv:2401.04796](https://arxiv.org/abs/2401.04796) (full text, Table 1 and Sec. 3)
- **2026 update (Park et al., Table II, full text)**: σ tension between RAR-predicted and measured Q2, given as (no EFE / AQUAL local EFE):
  - 1.a Fiducial: 15.0 / 15.2
  - 1.b with surface-density term: 15.8 / –
  - 2 Free hyper: 12.0 / 11.9
  - 3 Constrained hyper: 12.6 / 12.5
  - 4 Free unif: 12.6 / 12.1
  - 5 Constrained unif: 15.3 / 15.5
  - **6 No bulge: 3.8 / 2.8**
  - **7 Only bulge: 15.9 / 15.9**

  In their words: "roughly 9σ → 15σ for the fiducial SPARC M/L model and 7σ → 12σ when freeing up the M/L prior centres. The no-bulge models that gave consistency before (2.7 or 1.9σ depending on the EFE) now give moderate tension (3.8σ or 2.8σ)." The abstract summarises this as "discrepancies at the 3–15σ level depending on the detailed mass modeling or the subset of galaxies considered." — [arXiv:2602.17884](https://arxiv.org/abs/2602.17884)
- **Milky-Way self-consistency test (Park 2026)**: Q2 bounds the MOND boost a_e/a_e^N at the Sun's position to < 1.018 (n-family), < 1.01 (γ-family) and < 1.012 (δ-family) at 95% credibility. Priors: a_e = (2.32 ± 0.16)×10⁻¹⁰ m s⁻², Σ = 47 ± 3 M⊙ pc⁻², a0 flat in 0.5–2×10⁻¹⁰. The boost is "measured to be at least at the 10% level from the Milky Way rotation curve", giving "~11σ tension". The paper also notes that the RAR form a_R = ν(a_R^N/a0)a_R^N "cannot be exact within a disk in modified gravity MOND (but can be, for circular orbits, in modified inertia)". — [arXiv:2602.17884](https://arxiv.org/abs/2602.17884) (full text, Sec. IV)
- Earlier combined analysis: the EFE improves some rotation-curve fits, and Cassini plus rotation curves "rules out several classes of popular MOND transition functions, but leaves others viable". In full text, the ν̄_α family (with α ≥ 2) is singled out as the class viable for almost all α. — [Hees, Famaey, Angus & Gentile 2016, MNRAS 455, 449, arXiv:1510.01369, DOI 10.1093/mnras/stv2330](https://arxiv.org/abs/1510.01369)
- Desmond's 2025 review: "the RAR requires a shallower MOND–Newton transition than required by the Cassini measurement at ∼9σ". He calls the M/L and no-bulge relaxations "ad hoc changes without theoretical justification" and says further RAR studies must determine "whether galaxy dynamics really is incompatible with a sharp (δ ≳ 2−3) IF". — [Desmond 2025, arXiv:2505.21638](https://arxiv.org/abs/2505.21638) (PREPRINT/proceedings; full text)
- Counter-datum, MIGHTEE-HI. With 19 HI-selected galaxies and resolved SED-based M/L, a more general IF "ameliorate[s] the tension between previous RAR analyses, the Solar System quadrupole and wide-binary test". Intrinsic scatter is 0.045 ± 0.022 dex. — [Vărăşteanu et al. 2025, MNRAS, arXiv:2504.20857, DOI 10.1093/mnras/staf1079](https://arxiv.org/abs/2504.20857)
- MIGHTEE-HI/LADUMA, 130 galaxies at z ≲ 0.09: **a0 = (1.50 ± 0.05)×10⁻¹⁰ m s⁻²**, intrinsic scatter 0.096 ± 0.006 dex, **δ = 4.10 (+1.4/−0.68)** "consistent with the value required by Solar System gravitational constraints and a null Wide Binary Test". — [Vărăşteanu et al. 2026, arXiv:2608.03576](https://arxiv.org/abs/2608.03576) (PREPRINT)

### Inferences
- The driver is the RAR's curvature in the transition region, 10⁻¹⁰ to 10⁻⁹ m s⁻². That region is dominated by inner points of bulge-hosting, high-surface-brightness SPARC galaxies, so bulge M/L systematics are the lever. A theory that wants both Cassini and SPARC needs a sharp IF (δ ≳ 3–4, or n ≳ several) and must then reproduce the SPARC bulge galaxies some other way. Alternatively it must not produce the Poisson-type Galactic-EFE quadrupole at all, which is the MI / non-Poisson escape route (see Section 5).
- The MIGHTEE results show the sharpness inference depends on the sample and on M/L. They are a preprint-level (2026) or small-sample (2025) counterweight, not yet a resolution.

### Gaps
- SPARC-fit a0 and δ posterior numbers per M/L model were not transcribed from Desmond 2024 Table 1. The table text extraction was garbled; only Q2-predicted ≈ 29×10⁻²⁷ s⁻² and σ = 8.7 for the fiducial rows are reliable.

## 3. Galaxy-side tests: SPARC/RAR, EFE detections, weak-lensing RAR, and implied a0

### Takeaway
SPARC (175 galaxies) defines the RAR: g† = 1.20 ± 0.02 (random) ± 0.24 (systematic) ×10⁻¹⁰ m s⁻². Individual-galaxy fits show no credible a0 variation, with residual rms 0.057 dex. The EFE is claimed detected in SPARC at >4σ statistically and 8–11σ in two "golden" galaxies (MG-type signal). Weak lensing extends the RAR about 2.5 dex lower, with flat curves to ~1 Mpc. Newer HI samples give a0 ≈ 1.5×10⁻¹⁰.

### Cited Findings
- SPARC: 175 disk galaxies with Spitzer 3.6 µm photometry and HI/Hα rotation curves. — [Lelli, McGaugh & Schombert 2016, AJ 152, 157, arXiv:1606.09251, DOI 10.3847/0004-6256/152/6/157](https://arxiv.org/abs/1606.09251)
- RAR: 2693 points in 153 galaxies; "the observed scatter is small and largely dominated by observational uncertainties". — [McGaugh, Lelli & Schombert 2016, PRL 117, 201101, arXiv:1609.05917](https://arxiv.org/abs/1609.05917)
- **g† = (1.20 ± 0.02)×10⁻¹⁰ m s⁻²**, with a 0.24×10⁻¹⁰ systematic from Υ[3.6], quoted as "1.20 ± 0.02 (rnd) ± 0.24 (sys)". The sample is 240 galaxies: late types, early types and dSphs. Scatter < 0.13 dex. — [Lelli, McGaugh, Schombert & Pawlowski 2017, ApJ 836, 152, arXiv:1610.08981](https://arxiv.org/abs/1610.08981) (full text)
- Individual fits of 175 galaxies: rms residual 0.057 dex. Allowing the critical acceleration to vary galaxy to galaxy gives "no credible indication of variation". — [Li, Lelli, McGaugh & Schombert 2018, A&A 615, A3, arXiv:1803.00022](https://arxiv.org/abs/1803.00022)
- **EFE detection (Chae et al. 2020)**: individually detected at 8σ (NGC 5033) and 11σ (NGC 5055), and not detected in exceptionally isolated galaxies. Statistically >4σ in a blind test of 153 SPARC galaxies. A downward trend in the weak-field RAR appears "at the right acceleration predicted by the EFE of the MOND modified gravity". — [ApJ 904, 51, arXiv:2009.11525, DOI 10.3847/1538-4357/abbb96](https://arxiv.org/abs/2009.11525) (galaxy names from full text)
- Follow-up (Chae et al. 2021): >4σ again. Galaxies in underdense regions have e_N ≈ 0. Those near the CfA2 Great Wall and Perseus–Pisces have twice the SPARC median. — [ApJ 921, 104, arXiv:2109.04745, DOI 10.3847/1538-4357/ac1bba](https://arxiv.org/abs/2109.04745)
- Theory uncertainty in the EFE: AQUAL predicts a weaker EFE than earlier published AQUAL results but still a stronger one than QUMOND, "which demonstrates current theoretical uncertainties". — [Chae & Milgrom 2022, ApJ, arXiv:2201.02109, DOI 10.3847/1538-4357/ac5405](https://arxiv.org/abs/2201.02109)
- Weak-lensing RAR, KiDS-1000: extends the RAR "by 2 decades" and agrees with MG predictions. However, there is "a difference of at least 6σ between the RARs of early- and late-type galaxies". — [Brouwer et al. 2021, A&A 650, A113, arXiv:2106.11677](https://arxiv.org/abs/2106.11677)
- Mistele et al. 2024 (JCAP): the lensing RAR "smoothly continues" the kinematic RAR by ~2.5 dex. Contrary to Brouwer et al., early and late types "lie on the same joint RAR when a sufficiently strict isolation criterion is adopted". — [JCAP04(2024)020, arXiv:2310.15248](https://arxiv.org/abs/2310.15248)
- Mistele et al. 2024 (ApJL): circular velocities flat "for hundreds of kpc", "no clear hint of a decline out to 1 Mpc". The BTFR from lensing matches the kinematic one. — [ApJL 969, L3, arXiv:2406.09685](https://arxiv.org/abs/2406.09685)
- Lelli et al. 2024 review: "Combining galaxy data with Solar System data, the RAR covers about 16 orders of magnitude". — [arXiv:2411.02499](https://arxiv.org/abs/2411.02499) (PREPRINT)
- Hybrid-theory constraints from lensing:
  - Superfluid DM "is incompatible with the weak-lensing observations, at least in its current form". — [Mistele, McGaugh & Hossenfelder 2023, JCAP09(2023)004, arXiv:2303.08560](https://arxiv.org/abs/2303.08560)
  - AeST deviates from MOND at lensing radii, and "the data show no clear indication of these predicted deviations". — [Mistele et al. 2023, A&A 676, A100, arXiv:2301.03499](https://arxiv.org/abs/2301.03499)

### Inferences
- Galaxy-side a0 is 1.2×10⁻¹⁰ (SPARC, ±20% systematic from M/L) and 1.5×10⁻¹⁰ (MIGHTEE/LADUMA). Park 2026 uses a fiducial a0 = 1.02×10⁻¹⁰ m s⁻² from the SPARC δ-family fit (full text). a0 is therefore known only to ~20–30% once M/L and IF-family choices are included, and it is correlated with the IF shape.
- The EFE signals (Chae 2020/2021) favour MG-type behaviour. Any theory without an EFE must explain the outer RC declines some other way.

### Gaps
- a0 values from the weak-lensing RAR (Brouwer 2021; Mistele 2024) were not extracted. Those papers compare to MOND at fixed a0 = 1.2×10⁻¹⁰.
- No independent critique of the Chae EFE detection was found in this search.

## 4. Intermediate scales: Gaia wide binaries and the Oort cloud

### Takeaway
Wide binaries are unresolved as of October 2026. Two camps reach opposite verdicts from the same Gaia DR3 data:
- **Chae/Hernandez:** γ_g ≈ 1.3–1.6, with Newton excluded at 5–10σ.
- **Banik/Pittordis/Sutherland/Cookson/El-Badry, and Saad & Ting:** Newtonian, with MOND excluded at 16–19σ or "up to 1500× less likely".

The 2026 reanalysis of Chae's 36-pair 3D sample gives γ = 1.00 (+0.24/−0.19). The Oort-cloud test (Vokrouhlický, Nesvorný & Tremaine 2024, ApJ) fails AQUAL MOND and is robust to IF choice for comet binding energies. Both tests probe MG with the Galactic EFE; MI predictions differ.

### Cited Findings
**Pro-anomaly (MOND-like boost)**
- Chae 2023: δ_obs−newt = 0.034 ± 0.007 and 0.109 ± 0.013 at g_N ≈ 10^−8.91 and 10^−10.15 m s⁻² (26,615 binaries within 200 pc), a "10σ significance". g_obs/g_pred = 1.43 ± 0.06 at 10^−10.15. — [arXiv:2305.04613, DOI 10.3847/1538-4357/ace101](https://arxiv.org/abs/2305.04613)
- Chae 2024a: 2,463 "statistically pure" binaries. γ_g = 1.49 (+0.21/−0.19) for g ≲ 10⁻¹⁰ m s⁻², a stacked-profile deviation of ≈5.0σ, and γ_vp = 1.20 ± 0.06 (stat) ± 0.05 (sys). — [arXiv:2309.10404](https://arxiv.org/abs/2309.10404) (journal ref not on arXiv record)
- Chae 2024b: γ_g = 1.37 (+0.10/−0.09 stat, +0.16/−0.09 syst). Newton is ruled out at 5.8σ (new sample) and 9.2σ (largest sample); AQUAL is acceptable. — [arXiv:2402.05720](https://arxiv.org/abs/2402.05720) (journal status not verified)
- Chae 2025 (Bayesian 3D, 312 binaries): Γ = 0.000 ± 0.011 at high acceleration. In the MOND regime, γ_g = 1.48 (+0.33/−0.23). — [arXiv:2502.09373](https://arxiv.org/abs/2502.09373) (journal status not verified)
- Yoon, Tian & Chae 2025, out to 50 kau with perspective effects: γ_g = 1.61 (+0.37/−0.29) at g_N = 10^−11.0. For all g_N ≲ 10⁻¹⁰, γ_g = 1.32 (+0.12/−0.11). — [ApJ 992, 102, arXiv:2507.13177](https://arxiv.org/abs/2507.13177)
- Chae, Lee, Hernandez et al. 2026: 36 binaries with v_r errors < 100 m s⁻¹ give γ = 1.60 (+0.24/−0.14). The result "is dominated by two systems" whose 3D velocities exceed their Newtonian escape velocity. — [arXiv:2601.21728](https://arxiv.org/abs/2601.21728) (PREPRINT)
- Chae & Yoon 2026: quality control and triple modelling "cannot remove the low-acceleration gravitational anomaly". Null results are attributed to "bypassed calibration of the fraction of multiple-star systems", bias from quality cuts, or low statistics. — [arXiv:2607.14450](https://arxiv.org/abs/2607.14450) (PREPRINT, Jul 2026; latest from this side)
- Hernandez group:
  - Hernandez 2023 — [MNRAS, DOI 10.1093/mnras/stad2306, arXiv:2304.07322](https://arxiv.org/abs/2304.07322)
  - Hernandez et al. 2023: γ = 1.5 ± 0.2, inconsistent with Newton at 2.6σ — [arXiv:2309.10995](https://arxiv.org/abs/2309.10995)
  - Hernandez, Chae & Aguayo-Ortiz 2023 critique of the null groups — [arXiv:2312.03162](https://arxiv.org/abs/2312.03162) (PREPRINT)
  - Hernandez & Kroupa 2024 reanalysis of Cookson's data: 3.3σ — [arXiv:2410.17178](https://arxiv.org/abs/2410.17178) (PREPRINT)

**Null (Newtonian)**
- Banik et al. 2024: 8,611 binaries within 250 pc, 2–30 kau. Newton is preferred at 19σ. **α_grav = −0.021 (+0.065/−0.045)**, excluding MOND at 16σ. "Adapting the MOND interpolating function to explain this result would cause tension with rotation curve constraints." — [MNRAS 527, 4573, arXiv:2311.03436, DOI 10.1093/mnras/stad3393](https://arxiv.org/abs/2311.03436)
- Pittordis & Sutherland 2023: GR "somewhat preferred". — [OJAp, arXiv:2205.02846](https://arxiv.org/abs/2205.02846)
- Pittordis, Sutherland & Shepherd 2025: with realistic triples, Newtonian models fit "significantly better" than MOND, "though improved understanding of the triple population is necessary to make this fully decisive". — [OJAp, arXiv:2504.07569, DOI 10.33232/001c.142887](https://arxiv.org/abs/2504.07569)
- Cookson, Banik, El-Badry et al. 2026: high-purity sample within 130 pc, 1–30 kau. No 20% enhancement. Newton is "up to 1500x more likely than MOND", with constraints spanning a0/10 to 200 a0. Their meta-analysis finds "apparent MOND signals diminish as methodological rigour improves". — [MNRAS 547, stag342, arXiv:2602.24035, DOI 10.1093/mnras/stag342](https://arxiv.org/abs/2602.24035)
- Saad & Ting 2025 (C3PO): 57 bound binaries with 8–15 m/s differential RVs. Canonical a0 is excluded at 2.5σ (simple IF) and 1.5σ (standard IF). — [OJAp 9 (2026), arXiv:2512.19652, DOI 10.33232/001c.172194](https://arxiv.org/abs/2512.19652)
- **Saad & Ting 2026**, reanalysis of Chae et al.'s 36 pairs with forward-modelled 3D orbits: **γ = 1.00 (+0.24/−0.19)**. Replacing the semi-major axis with a geometric deprojection reproduces γ = 1.56 (+0.21/−0.18). — [OJAp 9 (2026), arXiv:2603.11015, DOI 10.33232/001c.170182](https://arxiv.org/abs/2603.11015)
- Boufourou 2026 (single author): a full-median estimator recovers γ = 1.08–1.13 from Newtonian mocks containing 20–30% residual triples. On the Chae (2024) 81,088-pair sample, robust estimators give γ = 1.045 [1.025, 1.068], rejecting γ = 1.4 at ~16σ. A protocol is pre-registered for Gaia DR4. — [arXiv:2608.24556](https://arxiv.org/abs/2608.24556) (PREPRINT, Aug 2026)
- Desmond 2025 summary: the wide-binary test "has produced mainly confusion". The Cassini-fit IFs predict α_grav ≈ 0, while RAR fits predict 0.8 ≲ α_grav ≲ 0.9. — [arXiv:2505.21638](https://arxiv.org/abs/2505.21638)
- Park 2026: the Q2 posterior implies α_grav ≈ 0 "to much higher precision than the Gaia wide binary data". A wide-binary deviation therefore "cannot be considered to be an effect of QUMOND or AQUAL once the Solar System constraints are taken into account". — [arXiv:2602.17884](https://arxiv.org/abs/2602.17884) (full text)

**Oort cloud / distant TNOs**
- Vokrouhlický, Nesvorný & Tremaine 2024 use AQUAL with the Galactic tide and passing stars. Newtonian runs reproduce the binding-energy distribution of long-period and Oort-cloud comets; MOND runs do not. The result is robust to migration history, the transition function, the birth cluster and comet fading. For the gradual-transition AQUAL they also fail the detached-disk TNO distribution (q > 38 au). The paper does "not rule out some MOND theories more elaborate than AQUAL, in which non-Newtonian effects are screened on small spatial scales, at small masses, or in external gravitational fields comparable in strength to the critical acceleration". Published as ApJ 968, 47, DOI 10.3847/1538-4357/ad40a3 (Crossref-resolved). — [arXiv:2403.09555](https://arxiv.org/abs/2403.09555)
- Earlier QUMOND Oort-cloud work: with the Cassini-revised IF and a0, the Milgromian cloud "is very similar to the Newtonian". — [Paučo & Klačka 2016, A&A 589, A63, arXiv:1602.03151](https://arxiv.org/abs/1602.03151)

### Inferences
- The wide-binary controversy reduces to three things: (i) the hidden-triple fraction and its calibration in the Newtonian regime; (ii) the estimator (median vs mixture/tail-robust); (iii) deprojection vs forward modelling of 3D orbits. Gaia DR4 is the stated decider.
- Only a peer-reviewed null result has been published in 2026 (Cookson; Saad & Ting ×2). The 2026 pro-anomaly papers remain preprints.
- Both wide binaries and the Oort cloud sit in the Galactic field g_e ≈ 2a0. They therefore test the same IF region as Q2, and in MG they are largely redundant with Cassini.

### Gaps
- No published modified-inertia wide-binary or Oort-cloud prediction was found in quantitative form beyond Milgrom's qualitative statements (Section 5).

## 5. Which tests apply to modified inertia, which only to modified gravity, and a master test table

### Takeaway
Q2 and the planetary/Oort/wide-binary EFE tests are derived for Poisson-type MG (AQUAL/QUMOND). Milgrom states that in some MI formulations the inner-Solar-System Galactic anomaly is "essentially not present". The wide-binary EFE in MI may be stronger, which quenches MOND, so a null wide-binary result is less damaging to MI. Galaxy tests cut the other way:
- MI predicts an exact algebraic RAR for circular orbits.
- Chae 2022's 6.9σ inner/outer RAR difference "would be inconsistent with current proposals of modified inertia".
- Petersen & Lelli 2020 mildly favour MG (within 1.5σ).

A mixed MG–MI family (Milgrom, Oct 2026) interpolates between the two.

### Cited Findings
- MI theories are time-nonlocal: "MOND effects depend on the full trajectory of a system", and "it is even possible to construct MI theories with practically no EFE". — [Milgrom 2011, Acta Phys. Pol. B 42, 2175, arXiv:1111.1611](https://arxiv.org/abs/1111.1611)
- MI models: the EFE is governed by μ(θ⟨a_ex⟩/a0), with θ > 1 depending on frequency ratios. "The θ factor can appreciably enhance the EFE in quenching MOND effects, over what is deduced in modified gravity." — [Milgrom 2022, PRD 106, 064060, arXiv:2208.07073](https://arxiv.org/abs/2208.07073)
- Milgrom 2023 has three relevant points:
  - MI models "predict a much weaker effect of the Galactic field in the inner Solar System than is predicted by AQUAL/QUMOND", and possibly a stronger EFE on wide binaries.
  - The quadrupole anomaly "is not generic; in some MI formulations it is predicted to essentially not be present". It arises from "the Poisson-like nature" of AQUAL/QUMOND field equations.
  - "There is no primary prediction of MOND for the case where g_ex ≪ g_in – such as ... the inner Solar System."

  — [arXiv:2310.14334](https://arxiv.org/abs/2310.14334) (PREPRINT; full text)
- Galaxy discriminants:
  - Q-parameter test on 15 SPARC galaxies: average and median "seem to favor MG", but MG and MI both agree "within 1.5σ". — [Petersen & Lelli 2020, A&A 636, A56, arXiv:2001.03348](https://arxiv.org/abs/2001.03348)
  - "Taken at face value there is a 6.9σ difference between the inner and outer parts on an acceleration plane which would be inconsistent with current proposals of modified inertia". The result is robust to removing bulges and special inclinations. — [Chae 2022, ApJ, arXiv:2207.11069, DOI 10.3847/1538-4357/ac93fc](https://arxiv.org/abs/2207.11069)
  - Banik et al. 2024 discuss the same point: it is "a priori not expected in the modified inertia interpretation", caveated by non-circular gas motions. — [arXiv:2311.03436](https://arxiv.org/abs/2311.03436) (full text)
  - FIRE-2 RAR "hooks" are "challenging to explain in Modified Inertia theories of MOND". — [Mercado et al. 2023, arXiv:2307.09507](https://arxiv.org/abs/2307.09507) (PREPRINT)
- Terrestrial MI-specific test: the static high-latitude equinox (SHLEM) effect predicts ~10⁻¹⁴ m mirror displacements in GW interferometers. It applies only to MI. — [Ignatiev 2008, PRD 77, 102001, arXiv:0802.1599](https://arxiv.org/abs/0802.1599)
- Hybrids, two kinds:
  - **Mixed MG–MI.** A one-parameter family 0 ≤ η ≤ 1 runs from pure MG (η = 0) to pure MI (η = 1). Different IFs appear in the kinetic and in the field equations, and "neither ... have the standard deep-MOND limit". — [Milgrom 2026, arXiv:2610.21699](https://arxiv.org/abs/2610.21699) (PREPRINT, 15 Oct 2026)
  - **DM–MOND hybrids and relativistic multi-field theories.** These are tested chiefly by weak lensing. Superfluid DM is incompatible in its current form (JCAP09(2023)004). AeST shows predicted deviations that the data do not show (A&A 676, A100). See Section 3.
- Quantised inertia (McCulloch) is falsified by the wide-binary analysis according to Banik et al. 2024 (full text: "it falsifies the quantized inertia pro[posal]"). — [arXiv:2311.03436](https://arxiv.org/abs/2311.03436)

### Master test table (for assigning each candidate theory its test)

| Test | Measured value / bound (CL) | Dataset | Source (ID/DOI) | Bounds which MOND quantity | MG (AQUAL/QUMOND, TeVeS-like) | MI (nonlocal) | Hybrids |
|---|---|---|---|---|---|---|---|
| Solar System EFE quadrupole Q2 | (1.6 ± 1.8)×10⁻²⁷ s⁻² (1σ); previously (3 ± 3)×10⁻²⁷ | Cassini range/Doppler + full DE440 data | Park+2026 PRD 114, 024066, arXiv:2602.17884; Hees+2014 arXiv:1402.6950 | IF sharpness at g_e ≈ 2a0; MW boost a_e/a_e^N < 1.01–1.018 (95%) | Applies directly; 3–15σ tension with SPARC RAR | Weak or absent ("essentially not present" in some MI) | Depends on η (mixed) or field content |
| RAR–Q2 consistency | 8.7σ (2024) → 15.0σ fiducial, 12σ free M/L, 3.8/2.8σ no-bulge, 15.9σ only-bulge | SPARC + Cassini | Desmond+2024 arXiv:2401.04796; Park+2026 Table II | IF family shape (n, δ, γ) and a0 jointly | Applies | Q2 side largely drops out | — |
| PPN γ | γ−1 = (2.1 ± 2.3)×10⁻⁵ (1σ); ephemeris combination (0.55 ± 1.35)×10⁻⁵ | Cassini 2002 conjunction; INPOP/EPM/DE | Bertotti+2003 DOI 10.1038/nature01997; Fienga & Minazzoli 2024 arXiv:2303.01821 | Relativistic completion (extra fields at 1PN) | Relativistic parents must pass | Needs a relativistic MI (none full-fledged) | AeST/SFDM must pass |
| PPN β | (−0.45 ± 1.75)×10⁻⁵ (ephemeris combination); LLR (6.2 ± 7.2)×10⁻⁵ | INPOP/EPM/DE, MESSENGER; LLR | arXiv:2303.01821; Biskupek+2021 arXiv:2012.12032 | Same as above | Same | Same | Same |
| Perihelion supplementary advance | 1σ: Mercury 0.006–0.03, Earth 0.0019, Mars 0.00037, Saturn 0.0047 mas/yr | EPM2011, INPOP10a | Fienga & Minazzoli 2024 Table 10 | Galactic-EFE anomaly (consistent use requires a refit) | Applies (Blanchet & Novak 2011) | Weak | — |
| SPARC RAR | g† = 1.20 ± 0.02 ± 0.24 ×10⁻¹⁰ m s⁻²; rms 0.057 dex; no a0 variation | 175 / 153 galaxies | arXiv:1610.08981; 1803.00022; 1609.05917 | a0, IF shape | Applies (approximate in disks) | Exact for circular orbits | Must reproduce |
| Inner vs outer RAR | 6.9σ difference ("face value") | SPARC | Chae 2022 arXiv:2207.11069 | MG vs MI discriminator | Consistent | Disfavoured | η-dependent |
| Global deep-MOND Q | MG favoured; both within 1.5σ | 15 SPARC galaxies | Petersen & Lelli 2020 arXiv:2001.03348 | MG vs MI | — | — | — |
| Galaxy EFE | >4σ statistical; 8σ/11σ in NGC 5033/5055 | SPARC + large-scale field | Chae+2020 arXiv:2009.11525; Chae+2021 arXiv:2109.04745 | e_N, SEP violation | Predicted | Differs: time-averaged, possibly stronger | — |
| Weak-lensing RAR | +2.5 dex continuation; flat to ~1 Mpc; ETG/LTG same RAR (2024) vs ≥6σ different (2021) | KiDS-1000 | arXiv:2310.15248; 2406.09685; 2106.11677 | Deep-MOND asymptote, isolation | Passes | Lensing needs a relativistic MI | SFDM fails; AeST deviations not seen |
| HI-selected RAR | a0 = (1.50 ± 0.05)×10⁻¹⁰; δ = 4.10 (+1.4/−0.68) | MIGHTEE-HI/LADUMA, 130 galaxies | arXiv:2608.03576 (PREPRINT) | a0, IF sharpness | Eases Q2 tension | — | — |
| Wide binaries (null) | α_grav = −0.021 (+0.065/−0.045) (MOND excluded 16σ); 1500× Newton preference; γ = 1.00 (+0.24/−0.19) | Gaia DR3; C3PO RVs | arXiv:2311.03436; 2602.24035; 2603.11015 | Boost at g_N < a0 inside a 2a0 external field | Tests MG with EFE | MI EFE may quench (weaker test) | — |
| Wide binaries (anomaly) | γ_g ≈ 1.3–1.6; Newton excluded 5.8–10σ | Gaia DR3 | arXiv:2305.04613; 2402.05720; 2507.13177; 2601.21728 (PREPRINT); 2607.14450 (PREPRINT) | Same | — | — | — |
| Oort cloud / LPCs | MOND (AQUAL) fails binding-energy distribution, robust to IF | Simulations vs observed LPCs | ApJ 968, 47, arXiv:2403.09555 | Sub-a0 dynamics with Galactic tide | Fails (AQUAL) | Not tested | Screened theories not ruled out |
| SHLEM terrestrial | ~10⁻¹⁴ m predicted displacement | GW interferometers (proposal) | Ignatiev 2008 arXiv:0802.1599 | Newton's 2nd law at low acceleration | N/A | MI only | — |

### Inferences
- A pure MI theory sidesteps the Cassini/Q2 and planetary-precession tests, and arguably the Oort-cloud AQUAL result. It faces the inner-vs-outer RAR test (6.9σ face value), the galaxy EFE detections, and lensing (it needs a relativistic completion).
- A pure MG theory faces Q2 (3–15σ against SPARC) and the Milky Way boost bound (~11σ).
- Mixed or hybrid theories can in principle trade between the two, which is the motivation for Milgrom's η-family.

### Gaps
- There is no quantitative MI prediction for Q2, wide binaries or the Oort cloud in a peer-reviewed source. Milgrom's 2023 MI paper is a preprint with qualitative and model-level statements.
- The Brown & Mathur 2023 "MOND as alternative to Planet Nine" paper was not resolved (UNVERIFIED; not cited above).
