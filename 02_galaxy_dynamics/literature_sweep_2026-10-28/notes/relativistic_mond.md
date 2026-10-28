# Relativistic (covariant) modified-gravity completions of MOND: Solar System vs galaxies

Scope: covariant modified-gravity MOND theories only (AeST, TeVeS and generalizations, BIMOND, Einstein-aether/GEA, Khronon, nonlocal metric MOND, plus brief mentions). Benchmark: Cassini/DE440 external-field quadrupole Q2 = (1.6 ± 1.8)e-27 s^-2 (Park et al. 2026). How sources were checked (2026-10-28): every arXiv ID was resolved through the arXiv API (export.arxiv.org). Journal status was cross-checked on INSPIRE. DOIs marked "resolved" returned a doi.org 302 redirect to the publisher. Key claims were checked against the full text (pdftotext plus grep of the arXiv PDFs), not only abstracts. Where I say "computes", the paper derives the result. Where I say "asserts", the paper states it without a calculation.

**Classification used throughout.** The Cassini tension carries over *unchanged* only if the theory's static non-relativistic limit is **exactly AQUAL** or **exactly QUMOND**. Other limits:
- **Two-field** (Newtonian potential plus an AQUAL-type scalar; TeVeS, AeST with m_× → 0): identical to single-field MOND in spherical symmetry, so the same RAR fit applies, but it differs in non-spherical setups such as the Sun inside the Galactic field.
- **Richer** (TRIMOND, extended BIMOND, AeST at finite m_×, nonlocal): not fixed by one interpolating function.

**PPN (γ, β, α1, α2) ≠ Q2.** Q2 is a Newtonian-order effect of the external Galactic field on the Sun's potential. PPN parameters measure 1PN corrections to the Sun's own field. Many papers say a theory "passes Solar System tests", but they mean PPN; none of them computed Q2.

---

## Q1. AeST (Skordis & Zlosnik 2021) and follow-ups: static weak-field limit; do its parameters change the Solar System quadrupole or PPN? Any Solar System/Cassini analysis of AeST?

### Takeaway
AeST's quasi-static limit is MOND-like, but *which* MOND depends on a parameter m_× = sqrt[(2−K_B)/(2K_B)]·Q0:
- **m_× → ∞:** literally AQUAL (plus a "ghost-condensate" density term).
- **m_× → 0:** a two-field (TeVeS-like) MOND.
- **Finite m_×:** interpolates between the two.

The two limits are exactly equivalent whenever curl terms vanish (e.g. spherical symmetry), so rotation curves barely depend on m_×, but external-field (non-spherical) predictions do. **Mistele expects m_× comparable to the ghost-condensate scale m ~ 1 Mpc⁻¹. On that estimate the two-field limit applies to kAU systems and to the inner parts of galaxies, so the Sun's EFE scale r_M ≈ 8 kAU sits in the two-field regime, not the AQUAL one.** No published paper computes Q2 or PPN parameters for AeST. Park et al. 2026, whose co-author Durakovic is an AeST author, cite AeST only as one of the covariant theories that "mostly" reduce to AQUAL/QUMOND in the Solar System.

### Cited Findings
**Original paper and the quasi-static limit**
- AeST original paper: PRL 127, 161302 (2021), arXiv:2007.00082, DOI 10.1103/PhysRevLett.127.161302 (peer-reviewed). It claims MOND in galaxies, agreement with CMB and matter power spectra on linear scales, and no ghosts at second order — [arXiv:2007.00082](https://arxiv.org/abs/2007.00082)
- **Quasi-static limit (computed in the PRL).**
  - Set g00 = −1−2Ψ, gij = (1−2Φ)γij, A0 = 1−Ψ, Ai = 0 (vector assumed aligned with time). The field equations give Ψ = Φ (GR-like lensing).
  - The static action becomes S = −∫d⁴x { [(2−K_B)/(16πG̃)] [|∇Φ|² − 2∇Φ·∇ϕ + |∇ϕ|² − μ²Φ² + J(Y)] + Φρ }, with J(Y) = F(Y,Q0)/(2−K_B).
  - The new "mass term" μ = sqrt[2K2/(2−K_B)]·Q0 means the MOND solution holds only for r ≲ r_C, a scale set by r_M and μ (the PRL's exact scaling did not extract cleanly from the PDF), with Φ oscillatory beyond r_C; the authors require μ⁻¹ ≳ 1 Mpc.
  - "The quasistatic limit has at least three parameters: λs, a0 and μ" — [arXiv:2007.00082 (full text)](https://arxiv.org/abs/2007.00082)
- **Solar System handling in the PRL (asserted, not computed).**
  - Corrections to r⁻² from ϕ "will compete with the post-Newtonian force" and must be < ~10⁻⁴ at Mercury.
  - Two suppression routes are named: "screening" (ϕ screened at large ∇ϕ, equivalent to λs → ∞; J terms Y^p with p ≥ 3/2, "this may be in conflict with Mercury's orbit even as p → ∞") or "tracking" (ϕ → Φ̂/λs, so G_N = (1+1/λs)Ĝ).
  - The external-field quadrupole is not discussed — [arXiv:2007.00082](https://arxiv.org/abs/2007.00082)

**The m_× result (Mistele 2024)**
- Mistele, "A new scale in the quasi-static limit of AeST", PRD 110, 024062 (2024), arXiv:2305.07742, DOI 10.1103/PhysRevD.110.024062 (peer-reviewed). It shows the earlier assumption of a vanishing vector field is "not always justified" and that the quasi-static limit depends on m_× — [arXiv:2305.07742](https://arxiv.org/abs/2305.07742)
- **Definition (computed, Eq. 21):** m_× ≡ sqrt[(2−K_B)/(2K_B)]·Q0. So the aether coupling **K_B directly controls** which MOND limit applies. Only f_G, m (ghost condensate) and m_× are physical in the quasi-static limit — [arXiv:2305.07742 full text](https://arxiv.org/abs/2305.07742)
- **m_× → ∞ (computed, Eq. 25):** ∇·[μ(|∇Φ|/a0)∇Φ] = 4πG_N(ρb+ρc). In the paper's words, "a standard single-field version of MOND … up to the ghost condensate density ρc. Without the ghost condensate, this is known as … AQUAL." — [arXiv:2305.07742](https://arxiv.org/abs/2305.07742)
- **m_× → 0 (computed, Eqs. 32–33):** Δ(Φ−α) = 4πG_N f_G(ρb+ρc) and ∇·[μ̃(|∇α|/a0)∇α] = 4πG_N f_G(ρb+ρc). This is a two-field MOND: a Newtonian-type piece plus an AQUAL-type scalar α. It is the same system as Skordis & Zlosnik's Eq. 7 with ∇ϕ replaced by ∇α — [arXiv:2305.07742](https://arxiv.org/abs/2305.07742)
- **Equivalence and its limits (computed, Sec. IV.C).** "The only place where m× enters … is as the prefactor of ∇×∇×U. In spherical symmetry, this curl term vanishes." For curl-free fields the single-field, two-field and full equations are equivalent. "Plausibly, other values of m× interpolate between these single-field and two-field limits" (asserted) — [arXiv:2305.07742](https://arxiv.org/abs/2305.07742)
- **Which regime applies at which scale (Sec. V, asserted with an order-of-magnitude estimate).** "A typical order of magnitude of m is 1 Mpc⁻¹ … m and m× can be comparable". The two-field limit (m_× l ≪ 1) "is relevant for wide binaries (l ∼ kAU), and at least the inner parts of galaxies (l ∼ kpc)". The single-field limit "happens for l ∼ Mpc or larger" — [arXiv:2305.07742 full text](https://arxiv.org/abs/2305.07742)
- **External-field effect (computed for wide binaries).**
  - "Much of the phenomenology of the quasi-static limit depends only very little on the value of m×", but for wide binaries "m× has percent-level effects".
  - Wide binaries satisfy m_× l ≪ 1 (the two-field regime). In that limit they are "much more sensitive to the details of the local Galactic field than in the single-field" limit (Sec. VII).
  - The Solar System quadrupole is not computed — [arXiv:2305.07742](https://arxiv.org/abs/2305.07742)

**Other AeST follow-ups (none touches the Solar System quadrupole)**
- Verwayen, Skordis & Bœhm, quasi-static spherical solutions: MNRAS 531, 272 (2024), DOI 10.1093/mnras/stae1225 (journal ref from INSPIRE), arXiv:2304.05134. They find Newtonian, MOND and an oscillatory third regime. Their scale r_C ~ r̂_M/μ² depends on boundary conditions. A grep of the full text finds no Solar System/Cassini/quadrupole analysis — [arXiv:2304.05134](https://arxiv.org/abs/2304.05134); [INSPIRE record](https://inspirehep.net/api/literature?q=arxiv:2304.05134)
- Durakovic & Skordis, isothermal spheres/clusters: JCAP 04 (2024) 040, DOI 10.1088/1475-7516/2024/04/040 (INSPIRE), arXiv:2312.00889. They reduce static spherical weak-field AeST to one equation for the potential. The resulting RAR can have a peak above MOND and then drop below MOND at low acceleration, depending on the mass parameter and the boundary potential — [arXiv:2312.00889](https://arxiv.org/abs/2312.00889)
- Mistele, McGaugh & Hossenfelder, A&A 676, A100 (2023), arXiv:2301.03499, DOI 10.1051/0004-6361/202346025. AeST "reproduces MOND only up to a certain maximum galactocentric radius". It shows deviations at weak-lensing radii that the data do not clearly show — [arXiv:2301.03499](https://arxiv.org/abs/2301.03499)
- **Stability:** Skordis & Zlosnik, PRD 106, 104041 (2022), arXiv:2109.13287. Minkowski space has healthy massive modes. A non-propagating mode may have an unbounded Hamiltonian for k < μ (≲ Mpc⁻¹, cosmological scales only) — [arXiv:2109.13287](https://arxiv.org/abs/2109.13287)
- **Hamiltonian analysis:** Bataki, Skordis & Zlosnik, PRD 110, 044015 (2024), arXiv:2307.15126. Six physical degrees of freedom non-linearly — [arXiv:2307.15126](https://arxiv.org/abs/2307.15126)
- **Strong field:**
  - Stealth (exact-GR-geometry) black holes: Skordis & Vokrouhlický, JCAP 03 (2025) 035, arXiv:2412.15395 — [arXiv:2412.15395](https://arxiv.org/abs/2412.15395)
  - Neutron stars "compatible with all current observations": Reyes & Sakstein, PRD 110, 084019 (2024), arXiv:2406.18225 — [arXiv:2406.18225](https://arxiv.org/abs/2406.18225)
  - Black-hole mimickers and "Shapiro-free lenses": Yang, Barker, Mistele & Durakovic, PRD 113, 024068 (2026), arXiv:2504.20144 — [arXiv:2504.20144](https://arxiv.org/abs/2504.20144); [INSPIRE](https://inspirehep.net/api/literature?q=arxiv:2504.20144)
- **Post-Newtonian equations:** Hwang & Noh write the 1PN equations of "a relativistic MOND theory" (AeST), PRD 111, 063547 (2025), arXiv:2410.10205. They present the equations but no Solar System confrontation in the abstract — [arXiv:2410.10205](https://arxiv.org/abs/2410.10205)

**What the benchmark papers say about AeST**
- Park, Hees, Famaey, Desmond & Durakovic 2026 (PRD 114, 024066; arXiv:2602.17884; DOI 10.1103/r7n8-kw38, resolved) cite AeST [14], extended BIMOND [15] and Khronon [16] among covariant formulations.
  - They state: "In the non-relativistic limit relevant for the Solar System, these modified gravity approaches mostly [but see, e.g., 6, for details] reduce to two variations: (i) AQUAL … (ii) QUMOND".
  - They compute Q2 in QUMOND and say the AQUAL effect "is predicted to be slightly larger … rendering the QUMOND computations conservative".
  - They add: "as long as the theory asymptotes to QUMOND or AQUAL at scales relevant for the Milky Way and the Solar System, [the modelling] should" hold — [arXiv:2602.17884 full text](https://arxiv.org/abs/2602.17884)
- Desmond, Hees & Famaey 2024: "our conclusions refer solely to … AQUAL and QUMOND models where the IF is necessarily universal". Generalisations "such as TRIMOND … and GQUMOND … may evade our constraints by having different IFs in galaxies, wide binaries and the SS" — [arXiv:2401.04796 full text](https://arxiv.org/abs/2401.04796)

**Citation sweep (INSPIRE)**
- Papers citing the AeST PRL with titles containing solar/Cassini/post-Newtonian/external field/quadrupole/quasi-static: 12 hits. None is an AeST-specific Solar System or Q2 computation.
- Papers citing Mistele 2024: 12. Papers citing Park et al. 2026: 2.
- No AeST Q2 calculation appears in any of these lists — [INSPIRE refersto:recid:1804537](https://inspirehep.net/api/literature?q=refersto:recid:1804537); [INSPIRE refersto:recid:2659719](https://inspirehep.net/api/literature?q=refersto:recid:2659719); [INSPIRE refersto:recid:3122154](https://inspirehep.net/api/literature?q=refersto:recid:3122154)

### Inferences
- **Only if m_× r_M ≫ 1 (m_× ≳ 1/kAU, far above Mistele's Mpc⁻¹-scale expectation; this requires K_B extremely small) would AeST's Solar System limit be AQUAL.** In that case the Desmond 2024 / Park 2026 AQUAL tension would apply essentially verbatim. AQUAL gives Q2 "slightly larger" than QUMOND, so the tension is if anything stronger. Remaining caveats: the ghost-condensate term ρc, the μ²Φ mass term (negligible at Solar System scales since μ⁻¹ ≳ Mpc) and the overall constant f_G.
- **For realistic parameters (m_× ~ Mpc⁻¹, so m_× r_M ≪ 1), the Solar System is in the two-field limit:**
  - The RAR in spherical symmetry is identical to single-field AQUAL with the implicitly defined μ.
  - The Solar System quadrupole comes entirely from the α-field: Φ−α is a linear Newtonian potential with no EFE quadrupole beyond the ordinary Galactic tide.
  - α solves an AQUAL equation with its own function μ̃, source f_Gρ, and an external boundary gradient set by the Galactic α-field, which is smaller than the total Galactic field.
  - So the free-function→RAR map and the free-function→Q2 map differ from single-field AQUAL. Q2 is therefore not guaranteed to equal the AQUAL value, but it is still an AQUAL-type EFE quadrupole of order a0/r_M-scale.
  - Mistele's wide-binary result (percent-level, larger EFE sensitivity in the two-field limit) is the only quantitative hint. It suggests changes, not elimination. **This is my inference; no paper has computed Q2 in two-field AeST.**
- The parameter that could change Q2 is K_B (through m_×), not λs. λs only rescales G (tracking) or switches off the scalar at high gradient (screening), and the screening branch already conflicts with Mercury according to the PRL itself.

### Gaps
- No published Q2, PPN γ/β, or preferred-frame α1/α2 computation for AeST was found. AeST has a unit-timelike vector, so α1/α2 are not obviously GR values. None of the full texts or INSPIRE lists checked contains an AeST PPN calculation.
- No calculation of AeST with finite m_× for a point mass in a uniform external field.
- Park et al.'s exception reference [6] is "B. Famaey and A. Durakovic, Modified Newtonian dy[namics…]", a review. Its arXiv ID was not resolved: UNVERIFIED (it may be arXiv:2501.17006, "Modified Newtonian Dynamics (MOND)", which appears in the Desmond-2024 INSPIRE citation list, but this was not checked).

---

## Q2. TeVeS (Bekenstein 2004) and generalizations (Sanders stratified/biscalar, Skordis generalized TeVeS): Solar System status and known failures

### Takeaway
- **Non-relativistic limit:** two-field (Newtonian + AQUAL scalar). PPN γ = β = 1 is computed. α1/α2 are satisfiable only in generalized (aether-type) TeVeS for small couplings.
- **The original TeVeS function is excluded by Cassini** (Hees et al. 2014; Q2 computed via the modified-Poisson framework).
- **Further failures:** unstable spherical solutions and vector caustics; insufficient lensing without dark matter; and GW170817, which falsifies the original disformal-metric TeVeS.
- A c_T = c generalization exists (Skordis & Zlosnik 2019), and it led to AeST.

### Cited Findings
**The theory and its PPN status**
- Bekenstein, PRD 70, 083509 (2004); erratum PRD 71, 069901, arXiv:astro-ph/0403694, DOI 10.1103/PhysRevD.70.083509. He calculates "the β and γ PPN coefficients showing them to agree with solar system measurements" (computed) — [arXiv:astro-ph/0403694](https://arxiv.org/abs/astro-ph/0403694)
- Giannios, PRD 71, 103511 (2005), arXiv:gr-qc/0502122. For a time-aligned vector, β and γ equal GR's (computed). For the branch with a radial vector component, β ≠ 1, which violates observations for Bekenstein's F — [arXiv:gr-qc/0502122](https://arxiv.org/abs/gr-qc/0502122)
- Tamaki, PRD 77, 124020 (2008), arXiv:0803.4309. Finds γ = 1 and β = 1 in a general (non-spherical) setting. The vector equation forces a static Newtonian potential, so "we cannot determine α1 and α2" — [arXiv:0803.4309](https://arxiv.org/abs/0803.4309)
- Sagi, PRD 80, 044032 (2009), arXiv:0905.4001.
  - In original TeVeS, the cosmological scalar value is "tightly linked to the vector coupling constant K, preventing the former from evolving as predicted".
  - In generalized (aether-action) TeVeS, β, γ, ξ are as in GR. "Solar system constraints on … α1 and α2 can be satisfied within a modest range of small values" of the couplings (computed) — [arXiv:0905.4001](https://arxiv.org/abs/0905.4001)

**Anomalous forces in the Solar System**
- Sanders, MNRAS 370, 1519 (2006), arXiv:astro-ph/0602161. Multi-field theories "can be constructed to satisfy" inner-Solar-System and preferred-frame constraints, but "lead inevitably to an anomalous non inverse-square force in the outer solar system" — [arXiv:astro-ph/0602161](https://arxiv.org/abs/astro-ph/0602161)
- Sanders, MNRAS 363, 459 (2005), arXiv:astro-ph/0502222. The biscalar TeVeS "predicts, inevitably, a constant anomalous acceleration in the outer solar system" — [arXiv:astro-ph/0502222](https://arxiv.org/abs/astro-ph/0502222)
- Sanders, ApJ 480, 492 (1997), arXiv:astro-ph/9612099. The stratified scalar-tensor framework is a "toy theory" in which the aquadratic scalar Lagrangian protects the Solar System from preferred-frame effects (asserted for the toy model) — [arXiv:astro-ph/9612099](https://arxiv.org/abs/astro-ph/9612099)

**The Cassini quadrupole**
- Hees, Folkner, Jacobson & Park, PRD 89, 102002 (2014), arXiv:1402.6950. They obtain Q2 = (3 ± 3)×10⁻²⁷ s⁻², which "excludes a large part of the relativistic MOND theories".
  - Full text: "MOND characterized by standard MOND interpolating functions like μ1,2,3, μexp or μTeVeS … are excluded by Cassini data" and "the original TeVeS interpolating function is excluded by our analysis".
  - Their prediction intervals come from the modified-Poisson (AQUAL) computation of Blanchet & Novak — [arXiv:1402.6950](https://arxiv.org/abs/1402.6950)
- Blanchet & Novak, MNRAS 412, 2530 (2011), arXiv:1010.1349, DOI 10.1111/j.1365-2966.2010.18076.x. Numerical integration of "the MOND equation" (modified Poisson) with an external field confirms the EFE quadrupole. Compatible functions need "a very rapid transition" — [arXiv:1010.1349](https://arxiv.org/abs/1010.1349)
- Zhao & Famaey, PRD 81, 087304 (2010), arXiv:1003.4753. In the static weak-field limit, BIMOND (leading to QUMOND) and TeVeS are "constructed to give the same force field for spherical symmetry, but their predictions generally differ out of it" (computed for elliptical shells) — [arXiv:1003.4753](https://arxiv.org/abs/1003.4753)

**Stability and well-posedness**
- Seifert, PRD 76, 064002 (2007), arXiv:gr-qc/0703060. The "kinetic terms" of vacuum TeVeS are indefinite on a curved background, "leading to an instability" — [arXiv:gr-qc/0703060](https://arxiv.org/abs/gr-qc/0703060)
- Contaldi, Wiseman & Withers, PRD 78, 044034 (2008), arXiv:0802.1215. The TeVeS vector "quite generically" develops caustic singularities on gravitational in-fall time scales. Einstein-aether-type kinetic terms may avoid this — [arXiv:0802.1215](https://arxiv.org/abs/0802.1215)
- Chaichian et al., PLB 735, 322 (2014), arXiv:1402.4696, argue the opposite: TeVeS "is free from ghosts". This conflicts with Seifert on stability, though the two analyses address different questions (Hamiltonian ghosts vs perturbative instability on curved backgrounds) — [arXiv:1402.4696](https://arxiv.org/abs/1402.4696)
- Bruneton & Esposito-Farèse, PRD 76, 124012 (2007), arXiv:0705.4043. "All MOND-like models proposed in the literature … present serious difficulties: … unnaturally fine tuned … fail to reproduce some experimental facts or are unstable or inconsistent as field theories". They consider TeVeS more promising than others — [arXiv:0705.4043](https://arxiv.org/abs/0705.4043)

**Lensing and cosmology**
- Lensing: Mavromatos, Sakellariadou & Yusaf, PRD 79, 081301 (2009), arXiv:0901.3932. TeVeS "requires additional dark matter" for six CASTLES lenses with common μ(y). The one μ that avoids this "is however ruled out by rotation curve data" — [arXiv:0901.3932](https://arxiv.org/abs/0901.3932)
- Cosmology, two claims:
  - Skordis et al., PRL 96, 011301 (2006), arXiv:astro-ph/0505519: "may be possible" to reproduce CMB and galaxy distributions — [arXiv:astro-ph/0505519](https://arxiv.org/abs/astro-ph/0505519)
  - Dodelson & Liguori, PRL 97, 231301 (2006), arXiv:astro-ph/0608602: the vector field drives enhanced growth — [arXiv:astro-ph/0608602](https://arxiv.org/abs/astro-ph/0608602)
  - Skordis' review, CQG 26, 143001 (2009), arXiv:0903.3602, summarizes TeVeS cosmology — [arXiv:0903.3602](https://arxiv.org/abs/0903.3602)
  - Generalized TeVeS cosmology: Skordis, PRD 77, 123502 (2008), arXiv:0801.1985 — [arXiv:0801.1985](https://arxiv.org/abs/0801.1985)

**Gravitational waves (GW170817 and before)**
- **Speed bound:** GW170817/GRB 170817A constrain the GW speed to between −3×10⁻¹⁵ and +7×10⁻¹⁶ of c. ApJL 848, L13 (2017), arXiv:1710.05834, DOI 10.3847/2041-8213/aa920c — [arXiv:1710.05834](https://arxiv.org/abs/1710.05834)
- **Boran, Desai, Kahya & Woodard**, PRD 97, 041501 (2018), arXiv:1710.06168. The joint detection "rules out a class of … 'dark matter emulators'" in which matter couples to a different metric from GWs. They estimate a ~400-day Shapiro delay difference from the dark-matter potential — [arXiv:1710.06168](https://arxiv.org/abs/1710.06168)
- **Sanders**, IJMPD 27, 1847027 (2018), arXiv:1805.06804. GW170817 "definitively rule[s] out theories, such as TeVeS". The surviving class must be "modified field equations for one universal gravitational and physical metric" — [arXiv:1805.06804](https://arxiv.org/abs/1805.06804)
- **Gong, Hou, Liang & Papantonopoulos**, PRD 97, 084040 (2018), arXiv:1801.03382. In generalized TeVeS, the GW170817 bound "forces one of the propagating modes … to travel much faster than the speed of light", which excludes it in parameter subspaces without strong coupling — [arXiv:1801.03382](https://arxiv.org/abs/1801.03382)
- **Skordis & Zlosnik**, PRD 100, 104013 (2019), arXiv:1905.09465. A "previously unknown class" of TeVeS with c_GW = c always, "without altering the usual (bimetric) MOND phenomenology in galaxies" — [arXiv:1905.09465](https://arxiv.org/abs/1905.09465)
- **Chesler & Loeb**, PRL 119, 031102 (2017), arXiv:1704.05116, written before GW170817. They argue that GEA and BIMOND "display fatal inconsistencies" with GW observations and ultra-high-energy cosmic rays (gravitational Cherenkov radiation and non-linear wave propagation) — [arXiv:1704.05116](https://arxiv.org/abs/1704.05116)

**Other**
- Bekenstein & Magueijo, PRD 73, 103513 (2006), arXiv:astro-ph/0602266, used the non-relativistic TeVeS limit to predict MOND "bubbles" at Solar System saddle points (a test separate from Q2) — [arXiv:astro-ph/0602266](https://arxiv.org/abs/astro-ph/0602266)

### Inferences
- TeVeS's non-relativistic limit is the same two-field structure as AeST with m_× → 0, so the AeST two-field inference applies. The existing Cassini exclusion of μ_TeVeS was derived in the AQUAL/modified-Poisson framework. It is a strong indicator but not a dedicated two-field computation.
- Original TeVeS fails on several independent grounds (GW170817, stability/caustics, lensing). Its Solar System status is mostly moot; only c_T = c descendants (AeST) remain live.

### Gaps
- I found no paper that solves the two-field TeVeS equations for the Sun in the Galactic field and reports Q2 directly (as opposed to applying the modified-Poisson Q2 to the TeVeS function). Sanders 2006 discusses anomalous outer-Solar-System forces, but its grep did not show an EFE quadrupole/Cassini computation.

---

## Q3. Bimetric MOND (BIMOND, Milgrom 2009 and later): Solar System limit; does the twin-matter or two-metric structure change the EFE near the Sun?

### Takeaway
- The standard BIMOND subclass reduces in the non-relativistic limit **exactly to QUMOND**, so the Park et al. QUMOND Q2 tension carries over directly.
- Twin matter couples only through the second metric. In the high-acceleration regime it does not interact with matter for the favoured β = 1.
- The later "extended BIMOND" (several scalars) still collapses to one interpolating function in the non-relativistic limit.
- Possible escapes: TRIMOND (a candidate non-relativistic limit of scalar-bimetric theories), which is named by Desmond et al. as able to evade the constraint but is untested; and the 2025–26 variable-G extension.

### Cited Findings
**Original BIMOND and its non-relativistic limit**
- Milgrom, "Bimetric MOND gravity", PRD 80, 123536 (2009), arXiv:0912.0790, DOI 10.1103/PhysRevD.80.123536.
  - It "tends simply to General Relativity in the limit a0 → 0, and to a phenomenologically valid MOND theory in the nonrelativistic limit". The same potential governs particles and lensing as in GR.
  - Full text: the non-relativistic limit is "the QUMOND formulation described by Eq.(3)", "with φ* = φ − φ̂ being the Newtonian potential, and the MOND potential φ determined from the QUMOND Eq.(3)" (computed).
  - On the Solar System: "There are indications from solar system constraints … that M′(z) decreases at least as fast…" — [arXiv:0912.0790](https://arxiv.org/abs/0912.0790)
- QUMOND itself: Milgrom, MNRAS 403, 886 (2010), arXiv:0911.5464 — [arXiv:0911.5464](https://arxiv.org/abs/0911.5464)
- Zhao & Famaey 2010 describe BIMOND as "leading for a given set of parameters to QUMOND" — [arXiv:1003.4753](https://arxiv.org/abs/1003.4753)

**Twin matter**
- Milgrom, MNRAS 405, 1129 (2010), arXiv:1001.4444.
  - In the deep-MOND regime, twin matter "behaves as if it has a negative gravitational mass" (repulsive MOND gravity between the sectors).
  - "In the high-acceleration regime … For the favored value beta=1, matter and TM do not interact"; for β < 1 they attract and for β > 1 they repel.
  - Twin-matter segregation into the voids of the matter cosmic web is speculated — [arXiv:1001.4444](https://arxiv.org/abs/1001.4444)

**Extended BIMOND and TRIMOND**
- Milgrom, "Broader view of bimetric MOND", PRD 106, 084010 (2022), arXiv:2208.10882. Theories with a "good" non-relativistic limit involve three quadratic scalars. "In the NR limit these scalars all reduce to the same acceleration scalar, and the NR theory then does hinge on one function of a single acceleration variable". A grep found no EFE/Q2/Solar System computation — [arXiv:2208.10882](https://arxiv.org/abs/2208.10882)
- Milgrom, "Tripotential MOND theories" (TRIMOND), PRD 108, 063009 (2023), arXiv:2305.19986.
  - For one-dimensional (e.g. spherical) mass distributions, all TRIMOND theories give a system-independent function of the Newtonian acceleration; "their variety appears in nonsymmetric situations".
  - They "may be the nonrelativistic limits of scalar-bimetric relativistic formulations of MOND, such as BIMOND with an added scalar" (asserted).
  - The full text names "the exact effects of the galactic field on the dynamics of the Solar System" as a case where theories differ, but no Q2 is computed — [arXiv:2305.19986](https://arxiv.org/abs/2305.19986)
- Desmond, Hees & Famaey 2024 (MNRAS 530, 1781): TRIMOND and GQUMOND "may evade our constraints by having different IFs in galaxies, wide binaries and the SS" (asserted) — [arXiv:2401.04796](https://arxiv.org/abs/2401.04796); DOI 10.1093/mnras/stae955 (resolved)

**Variable-G and fixed-gauge versions**
- Milgrom, "Bimetric MOND as a framework for variable-G theories", PRD 113, 064014 (2026), arXiv:2512.09353, DOI 10.1103/5r7x-cfqj (resolved). MOND premises "predict the standard value of G for high-acceleration systems", which ensures compliance with Solar System G-variation limits. The author "cannot yet present a consistent model that complies with all the observations in cosmology" — [arXiv:2512.09353](https://arxiv.org/abs/2512.09353)
- Milgrom, PRD 100, 084039 (2019), arXiv:1908.01691. A non-covariant f(𝓡) theory, shown to be "a fixed-gauge expression of BIMOND". Its non-relativistic potential "solves a MOND, nonlinear Poisson analog", with GR-like lensing of the MOND potential — [arXiv:1908.01691](https://arxiv.org/abs/1908.01691)

**Gravitational waves**
- Milgrom, PRD 89, 024027 (2014), arXiv:1308.5388. In the weak-field limit, the H⁺ sector is GR with GR waves; the H⁻ sector "is fully nonlinear even for the weakest" fields — [arXiv:1308.5388](https://arxiv.org/abs/1308.5388)
- Chesler & Loeb 2017 argue this non-linearity is fatal (see Q2) — [arXiv:1704.05116](https://arxiv.org/abs/1704.05116)

### Inferences
- With no twin matter near the Sun, standard BIMOND = QUMOND for Solar System Q2. The 3–15σ tension (Park 2026) applies unchanged.
- Twin matter cannot rescue the result. At high acceleration (the Sun's own field near planets) it is non-interacting for β = 1. Any twin-matter external field would add to, not cancel, the generic EFE structure. This is inference: no paper computes Q2 with twin matter.
- The only identified BIMOND-family escape route is TRIMOND-type multi-potential limits, where the EFE (non-spherical) can differ while spherical RAR predictions match. Nobody has shown that a specific member passes Cassini while fitting SPARC.

### Gaps
- No computation of Q2 in TRIMOND, extended BIMOND, or variable-G BIMOND was found.
- I did not verify a later independent paper on BIMOND stability or ghosts. I recall a Clifton–Zlosnik-type analysis, but did not find or resolve one: UNVERIFIED, omitted.

---

## Q4. Einstein-aether MOND (GEA), Khronon MOND, nonlocal metric MOND, and other covariant theories with a stated Solar System analysis

### Takeaway
- **GEA:** assumed to give an AQUAL-type modified Poisson equation, but this was not verified in the full text. Solar System constraints are limited to perihelion and Cassini time delay; a "subclass" passes. GW170817 forces c13 ≈ 0.
- **Khronon** (Blanchet–Marsat 2011; Blanchet–Skordis 2024/25): MOND for stationary systems and GR (same PPN as GR except α1, α2) at high acceleration.
  - Bonetti & Barausse computed PPN and found a viable region.
  - Flanagan found order-unity khronon corrections to MOND for non-stationary low-acceleration systems.
  - No Q2 computation exists.
- **Nonlocal MOND** (Deffayet–Esposito-Farèse–Woodard): GR in the Solar System with exponentially small deviations (asserted for the isolated Sun). The EFE is explicitly "a matter for future study", still listed as future work in Deffayet & Woodard 2026.

### Cited Findings
**Generalized Einstein-aether (GEA)**
- Zlosnik, Ferreira & Starkman, PRD 75, 044017 (2007), arXiv:astro-ph/0607411. Proposed a non-canonical aether "Modifying gravity with the Aether" and explored its Newtonian and non-Newtonian limits — [arXiv:astro-ph/0607411](https://arxiv.org/abs/astro-ph/0607411)
- TeVeS can be rewritten as a vector-tensor theory "akin to Einstein-Aether theories with non-canonical kinetic terms": PRD 74, 044037 (2006), arXiv:gr-qc/0606039 — [arXiv:gr-qc/0606039](https://arxiv.org/abs/gr-qc/0606039)
- Bonvin, Durrer, Ferreira, Starkman & Zlosnik, PRD 77, 024037 (2008), arXiv:0707.3519. They constrain corrections to the Sun's potential in positive and negative powers of r using Mercury's perihelion and the Cassini time delay: "a subclass of generalized Einstein-Aether theories are compatible" (computed for an isolated Sun). The full text says it is "unclear whether models producing MOND" survive; a more thorough treatment is needed. No external-field quadrupole — [arXiv:0707.3519](https://arxiv.org/abs/0707.3519)
- **GW170817:** for Einstein-aether, |c13| ≤ 10⁻¹⁵. Oost, Mukohyama & Wang, PRD 97, 124023 (2018), arXiv:1802.04303 — [arXiv:1802.04303](https://arxiv.org/abs/1802.04303)

**Khronon / khronometric MOND**
- Blanchet & Marsat, PRD 84, 044056 (2011), arXiv:1107.5264. A preferred time foliation (the "Khronon"), a hypersurface-orthogonal special case of non-canonical Einstein-aether. It "recovers the phenomenology of MOND in the non-relativistic limit" with the same lensing as GR but a "modified Poisson-type potential" — [arXiv:1107.5264](https://arxiv.org/abs/1107.5264)
- Sanders, PRD 84, 084024 (2011), arXiv:1105.3910. A modified low-energy Hořava gravity camouflages the preferred frame where gradients exceed cH0, giving MOND below — [arXiv:1105.3910](https://arxiv.org/abs/1105.3910)
- Bonetti & Barausse, PRD 91, 084053 (2015), arXiv:1502.05554.
  - Computed the PN expansion. If the theory reduces exactly to GR at high acceleration, "the post-Newtonian expansion breaks down at low accelerations, and the theory becomes strongly coupled".
  - They identify "a sizeable region … where the post-Newtonian expansion remains perturbative for all accelerations, and the theory passes both solar-system and pulsar gravity tests" (computed for PPN α1, α2: |α1| ≲ 10⁻⁴ etc.).
  - A grep found no Cassini Q2/EFE quadrupole computation — [arXiv:1502.05554](https://arxiv.org/abs/1502.05554)
- Flanagan, ApJ 958, 107 (2023), arXiv:2302.14846, DOI 10.3847/1538-4357/ad003d (INSPIRE). The theory has a consistent slow-motion limit and stationary MOND solutions are stable in spherical, cylindrical and planar symmetry. However, "for non-stationary systems in the low acceleration regime … the khronon field generally gives an order unity correction" to MOND (computed) — [arXiv:2302.14846](https://arxiv.org/abs/2302.14846); [INSPIRE](https://inspirehep.net/api/literature?q=arxiv:2302.14846)
- Blanchet & Skordis, JCAP 11 (2024) 040, arXiv:2404.06584, DOI 10.1088/1475-7516/2024/11/040 (resolved).
  - MOND for stationary galactic systems, GR+Λ in the strong field, and agreement with CMB at linear scales.
  - Full text: "the theory has the same PPN limit as GR and is therefore viable in the Solar System … the 'mass' term μ²ϕ is negligible … at the much smaller scale of the Solar System". In the general-coupling case, α1 = −8(α−β)/(1−β) and α2 is given by a formula (Eq. 6.6). These are quoted from earlier khronometric results; the MOND-sector EFE quadrupole is not computed.
  - The Minkowski Hamiltonian is unbounded for wavenumbers < ~10⁻³¹ eV — [arXiv:2404.06584](https://arxiv.org/abs/2404.06584)
- Blanchet & Skordis, "Khronon-Tensor theory reproducing MOND and the cosmological model", arXiv:2507.00912 — **preprint** (INSPIRE shows no journal). Same claims; it has a "Post-Newtonian limit" section, but the grep shows no Q2 — [arXiv:2507.00912](https://arxiv.org/abs/2507.00912)
- Blanchet & Seraille, JCAP 12 (2025) 036, arXiv:2502.14686. A Yang-Mills "graviphoton" EFT reproducing deep MOND, with Lorentz violation at low acceleration and covariance restored by a Khronon — [arXiv:2502.14686](https://arxiv.org/abs/2502.14686)

**Nonlocal metric MOND**
- Soussa & Woodard, CQG 20, 2737 (2003), arXiv:astro-ph/0302030. First nonlocal metric MOND. It gives GR-level lensing, i.e. "far too little lensing if no dark matter" — [arXiv:astro-ph/0302030](https://arxiv.org/abs/astro-ph/0302030)
- Deffayet, Esposito-Farèse & Woodard, PRD 84, 124054 (2011), arXiv:1106.4984. Pure-metric nonlocal models that "agree with general relativity in the weak field regime appropriate to the solar system" and give MOND plus sufficient lensing. Full text:
  - The extensions are chosen so that "the predicted deviations from general relativity are exponentially small with respect to the tightest solar-system constraints" (e.g. L ∝ y² e^(−y)). This is asserted from the large-y suppression for an isolated source.
  - On the EFE: "we cannot, at this stage, claim that our model incorporates the external field effect in a desirable way; what actually happens beyond the static, spherically symmetric limit is a matter for future study" — [arXiv:1106.4984](https://arxiv.org/abs/1106.4984)
- DEW, PRD 90, 064038 (2014), arXiv:1405.0393: full field equations and cosmology — [arXiv:1405.0393](https://arxiv.org/abs/1405.0393)
- Woodard, Can. J. Phys. (2014), arXiv:1403.6763 (DOI 10.1139/cjp-2014-0156) — [arXiv:1403.6763](https://arxiv.org/abs/1403.6763)
- Tan & Woodard, JCAP 05 (2018) 037, arXiv:1804.01669: "the MOND enhancement is not sufficient to allow ordinary matter to drive structure formation" in that model — [arXiv:1804.01669](https://arxiv.org/abs/1804.01669)
- Deffayet & Woodard, JCAP 04 (2026) 081, arXiv:2512.10513, DOI 10.1088/1475-7516/2026/04/081 (resolved). A single model interpolating between cosmology and bound-system MOND. Full text: exploring the "External Field Effect" is listed as a future project; "the key issue is how distant masses affect the nonlocal functional Z[g](x)" — [arXiv:2512.10513](https://arxiv.org/abs/2512.10513)
- **GW170817 survival:** Boran et al. 2018 list nonlocal MOND among theories that are still viable, because it is a single-metric theory with no different metric for gravitational waves — [arXiv:1710.06168](https://arxiv.org/abs/1710.06168)

**Other covariant theories (brief)**
- **Galileon k-mouflage MOND** (Babichev, Deffayet & Esposito-Farèse, PRD 84, 061502(R) (2011), arXiv:1106.2538). Passes Solar System PPN including local Lorentz invariance via Vainshtein-type screening. This is a screening theory, so I defer it to the screening researcher — [arXiv:1106.2538](https://arxiv.org/abs/1106.2538)
- **Mimetic connection:** Domènech & Ganz, JCAP 06 (2025) 059, arXiv:2503.11174. Any unit-timelike-vector relativistic MOND (TeVeS, AeST) can be recast as mimetic gravity. This is formal, with no Solar System analysis — [arXiv:2503.11174](https://arxiv.org/abs/2503.11174)
- **Verlinde emergent gravity:** not a covariant MOND theory, but its weak-field formula was ruled out by planetary perihelia "by seven orders of magnitude" (Hees, Famaey & Bertone, PRD 95, 064019 (2017), arXiv:1702.04358) — [arXiv:1702.04358](https://arxiv.org/abs/1702.04358)

### Inferences
- **Khronon is described by its authors as giving a "modified Poisson-type potential" in the stationary non-relativistic limit, and GEA is plausibly the same.** For GEA, the exact AQUAL form was not checked in the Zlosnik et al. full text, so treat it as UNVERIFIED. So the AQUAL Q2 tension should carry over for stationary configurations. The Sun–Galaxy configuration is quasi-stationary (Galactic orbit time ≫ planetary periods).
  - Flanagan's order-unity khronon correction applies to *non-stationary* low-acceleration systems. Whether it applies to the Sun in the slowly varying Galactic field is not established (inference).
  - The preferred-frame α1/α2 constraints are a separate, additional Solar System test that these theories can pass for suitable couplings.
- **Nonlocal MOND is the one family where the EFE itself is undefined.** The static spherical limit is MOND, but how distant masses enter the nonlocal scalars is unworked. In principle it could differ from AQUAL/QUMOND near the Sun. Its authors' Solar System claim covers only the isolated-Sun (large-y) suppression, which does not address Q2: Q2 is generated at r ~ r_M where y ~ 1, by the external field.

### Gaps
- No Q2 computation was found for GEA, khronometric MOND (any version) or nonlocal MOND.
- The GW170817 status of the Blanchet–Skordis Khronon is not explicitly checked in my sources beyond "usual tensor modes of GR". The abstract says the second-order action contains "the usual tensor modes of GR", which suggests c_T = c, but I did not verify an explicit statement.

---

## Q5. Does any published work compute Q2 or PPN γ/β for these theories, and how do they compare with Cassini Q2 = (1.6 ± 1.8)e-27 s^-2 and the Cassini Shapiro bound on γ?

### Takeaway
PPN γ = β = 1 (GR values) is computed for TeVeS (time-aligned branch). For generalized TeVeS and khronometric MOND, β = γ = 1 and α1, α2 are computed and can be kept within bounds. For Blanchet–Skordis Khronon, the same PPN as GR is asserted from the strong-field reduction. Q2 has been computed only in the AQUAL/QUMOND frameworks. These apply directly to standard BIMOND (= QUMOND), and to AeST only in the m_× r_M ≫ 1 limit, which Mistele's parameter estimate does not give. There, standard functions including μ_TeVeS are excluded, and the RAR-compatible functions are in 3–15σ tension with Park et al. 2026. **No paper computes Q2 natively in a two-field, multi-potential, khronon or nonlocal theory.**

### Cited Findings
**The Cassini Q2 measurement**
- Park, Hees, Famaey, Desmond & Durakovic, PRD 114, 024066 (2026) (INSPIRE), arXiv:2602.17884, DOI 10.1103/r7n8-kw38 (resolved).
  - Q2 = (1.6 ± 1.8)×10⁻²⁷ s⁻² (1σ), a 40% improvement. Tension with external galaxy rotation curves is "3–15σ depending on the detailed mass modeling or the subset of galaxies".
  - In the Milky Way, the MOND boost at the Sun is bounded at ≤ 2% (95%). Jupiter's contribution to the predicted Q2 is 0.05%.
  - Full text: "the predicted value of Q2 depends solely on the behavior of the IF at the value of the external gravitational field acting on the Sun, hence close to a0. This means that making the IF approach Newton as fast as possible above the Milky Way gravitational field … does not decrease the value of Q2" — [arXiv:2602.17884](https://arxiv.org/abs/2602.17884)
- Earlier results:
  - Hees et al. 2014: Q2 = (3 ± 3)×10⁻²⁷ s⁻², which excludes μ1,2,3, μexp and μTeVeS — [arXiv:1402.6950](https://arxiv.org/abs/1402.6950)
  - Hees, Famaey, Angus & Gentile, MNRAS 455, 449 (2016), arXiv:1510.01369. The combined rotation-curve plus Cassini analysis "rules out several classes of popular MOND transition functions, but leaves others viable". The text notes that all relativistic MOND theories are "Modified Gravity"-type in the non-relativistic regime — [arXiv:1510.01369](https://arxiv.org/abs/1510.01369)
  - Desmond, Hees & Famaey 2024: the Solar System quadrupole requires a sharper transition than the SPARC RAR allows, an 8.7σ tension in fiducial AQUAL/QUMOND, reduced to 1.9σ by removing bulge galaxies — [arXiv:2401.04796](https://arxiv.org/abs/2401.04796)
- Milgrom, MNRAS 399, 474 (2009), arXiv:0906.4817. First derivation of the quadrupole in the modified-Poisson formulation. "Predictions of the effect are not generic to the MOND paradigm, but depend on the particular MOND formulation at hand" — [arXiv:0906.4817](https://arxiv.org/abs/0906.4817)

**Cassini γ bound**
- Bertotti, Iess & Tortora, Nature 425, 374 (2003), DOI 10.1038/nature01997 (resolved via doi.org to nature.com; abstract page fetched). The fetched abstract text confirms the measurement of γ via the Cassini time delay. The fetched snippet was truncated before the numerical value. A second fetch recovered the value: "γ = 1 + (2.1 ± 2.3) × 10⁻⁵, agrees with the predictions of standard general relativity" (verified) — [Nature](https://www.nature.com/articles/nature01997)

**PPN results by theory (sources in Q2–Q4)**
- TeVeS: γ = β = 1 — [Bekenstein 2004](https://arxiv.org/abs/astro-ph/0403694); [Giannios 2005](https://arxiv.org/abs/gr-qc/0502122); [Tamaki 2008](https://arxiv.org/abs/0803.4309)
- Generalized TeVeS: α1, α2 satisfiable — [Sagi 2009](https://arxiv.org/abs/0905.4001)
- Khronometric MOND: passes Solar System tests in a region of parameter space — [Bonetti & Barausse 2015](https://arxiv.org/abs/1502.05554)
- Khronon (Blanchet–Skordis): same PPN as GR — [Blanchet & Skordis 2024](https://arxiv.org/abs/2404.06584)
- GEA (isolated Sun, Cassini time delay plus perihelion): a subclass is compatible — [Bonvin et al. 2008](https://arxiv.org/abs/0707.3519)

### Inferences
- PPN tests do not discriminate among these theories: all can be made GR-like at 1PN in the Sun's own field. **The external-field quadrupole is the decisive Solar System test.**
- For any theory whose Solar System limit is AQUAL or QUMOND with a universal IF, Park et al. note that Q2 depends on the IF near g_ext ~ a0, the regime that also shapes RAR fits. Theory-level escapes therefore require **non-universal behaviour**, which the theory sets rather than a free choice of IF:
  - two-field (Q2 set by μ̃ of the scalar at its own external gradient);
  - multi-potential (TRIMOND);
  - curl/vector effects (AeST at finite m_×);
  - nonlocal dependence on distant masses.
- Those four are exactly the cases where no Q2 calculation exists.

### Gaps
- No native Q2 computation for TeVeS/AeST two-field, AeST at finite m_×, TRIMOND/extended BIMOND, khronon (stationary or not), GEA, or nonlocal MOND. INSPIRE citation lists of Park 2026 (2 citing papers), Desmond 2024 (29) and Mistele 2024 (12) show none.
- One 2025 paper, "Negligible MOND effects on the orbits of planets" (CQG 42, 195013, 2025; DOI 10.1088/1361-6382/ae085b, seen in the Desmond-2024 citation list), was not read. Its claim and theory class are unknown, so I flag it for whoever covers non-relativistic MOND — [INSPIRE refersto list](https://inspirehep.net/api/literature?q=refersto:recid:2745269)

---

## Q6. What specific test could a research group compute for each theory?

### Takeaway
For each theory the test is the same in kind: solve the theory's own static (or quasi-static) field equations for a point-mass Sun in a uniform asymptotic Galactic field (|g_e| ≈ 1.5–2 a0), extract the traceless quadrupole of the anomalous potential at r ≪ r_M ≈ 7–8 kAU, and compare with Q2 = (1.6 ± 1.8)e-27 s⁻². At the same time, refit SPARC with the same free functions and parameters.

### Cited Findings
- **Method template.**
  - The quadrupole appears as a_p = Q2((ê·x)ê − x/3) in the inner Solar System, with r_M = (GM/a0)^1/2 ≈ 8×10³ AU — [Park et al. 2026](https://arxiv.org/abs/2602.17884); [Milgrom 2009](https://arxiv.org/abs/0906.4817)
  - The numerical AQUAL external-field solver approach is Blanchet & Novak 2011 — [arXiv:1010.1349](https://arxiv.org/abs/1010.1349)
  - The joint RAR plus Q2 inference framework is Desmond et al. 2024 — [arXiv:2401.04796](https://arxiv.org/abs/2401.04796)
- **AeST.** Mistele's quasi-static equations (Eqs. 20–22) with the curl term ∝ 1/m_×² are the system to solve. The two-field limit (Eq. 33) is a scalar AQUAL problem plus a Newtonian piece. Mistele already showed that the EFE magnitude depends on m_× at percent level for wide binaries — [arXiv:2305.07742](https://arxiv.org/abs/2305.07742)
- **BIMOND.** QUMOND Q2 (already computed) applies. TRIMOND requires a three-potential axisymmetric solve — [arXiv:0912.0790](https://arxiv.org/abs/0912.0790); [arXiv:2305.19986](https://arxiv.org/abs/2305.19986)
- **Nonlocal MOND.** First the authors must define how distant masses enter Z[g] — an open theoretical step, not just a numerical one — [arXiv:2512.10513](https://arxiv.org/abs/2512.10513)

### Inferences (proposed computations, by priority)
1. **AeST two-field limit (m_× → 0; also TeVeS-type).**
   - Solve ∇·[μ̃(|∇α|/a0)∇α] = 4πG f_G ρ_⊙ with boundary condition ∇α → ∇α_ext. Here α_ext is the Galactic α-gradient implied by the same μ̃ applied to the Milky Way's baryonic field at R0.
   - Q2 is the quadrupole of α. Φ−α is Newtonian, so only the ordinary tide contributes from it.
   - Fit SPARC with the spherical-equivalent μ (Mistele Eq. 36–37). Test whether any μ̃ passes both.
   - This is a 2D axisymmetric non-linear elliptic solve: the same cost as Blanchet & Novak's AQUAL runs.
2. **AeST at finite m_×.** Solve Mistele's coupled Φ/U system with the curl term for m_× r_M ~ 1. Map Q2(m_×, K_B). This tests whether the vector field's curl sector can suppress Q2 without changing spherical RAR fits.
3. **TRIMOND / extended BIMOND.** Pick the family of three-potential Lagrangians. Compute Q2 and the RAR for the same functions, and look for members that are RAR-equivalent but Q2-suppressed. Desmond et al. single these out as the candidate escape route.
4. **Khronon (stationary).** Confirm that the stationary non-relativistic limit is exactly AQUAL, which makes the existing Q2 apply. Then check whether Flanagan's non-stationary khronon correction is non-negligible for the Sun's ~230 Myr Galactic orbit (likely negligible: inference).
5. **Nonlocal MOND.** Theoretical step first: derive X[g], Y[g] for a point mass plus a uniform external gradient from the retarded nonlocal operators. Only then compute Q2.

### Gaps
- None of these computations exists in the literature found (INSPIRE sweep as described in Q1/Q5). This is a real open niche, not a search failure. The finding rests on citation lists of the benchmark papers plus title-filtered citations of the AeST PRL; full-text search of every citing paper was not done.
