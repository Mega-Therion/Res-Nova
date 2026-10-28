# Screening / environment-dependent MOND and non-MOND alternatives vs. Cassini Q2 and SPARC

Scope: theories meant to keep MOND-like galaxy dynamics while staying Newtonian/GR-like near the Sun. Modified inertia, AeST/TeVeS/BIMOND and dark-matter hybrids (superfluid DM and similar) are out of scope; they are named here only where a paper in scope depends on them.

Verification note: every arXiv ID below was resolved through the arXiv API (export.arxiv.org/api/query) on 2026-10-28. The arXiv record gave the title, authors, journal_ref and DOI. For the papers marked [full text read], I downloaded the PDF from arxiv.org/pdf and grepped and read the relevant sections. "Computes" means the paper derives or evaluates the quantity. "Asserts" means it states the result without a calculation in that paper. Three IDs I had in mind turned out to be unrelated papers (1608.05628, 1206.1259, 1612.07809). They are not used. Anything not resolved is marked UNVERIFIED.

Reference yardsticks:
- Cassini/DE440 Q2 = (1.6 ± 1.8)×10⁻²⁷ s⁻² (1σ), 40% better than before. The paper reports 3–15σ tension with external-galaxy RCs and caps the MOND boost at the Sun's position in the Milky Way at ≤2% (95%). Jupiter contributes only 0.05% of the predicted Q2. Its conclusion: "any MOND-based modified gravity must involve another scale beyond a0, such a length or frequency [Milgrom 2023], or a screening mechanism, such as the Vainstein mechanism [Babichev et al. 2011]. Another viable possibility is for MOND to be a modification of inertia." — Park, Hees, Famaey, Desmond, Durakovic, Phys. Rev. D (2026), DOI 10.1103/r7n8-kw38, [arXiv:2602.17884](https://arxiv.org/abs/2602.17884) [full text read]
- Earlier Cassini value: Q2 = (3 ± 3)×10⁻²⁷ s⁻². Hees et al. note it also bounds any external tidal quadrupole, e.g. from Galactic mass including DM. — [Hees, Folkner, Jacobson, Park 2014, PRD 89, 102002, arXiv:1402.6950](https://arxiv.org/abs/1402.6950)
- The EFE quadrupole in modified-Poisson MOND (QUMOND/AQUAL) persists "even if the MOND interpolating function is arbitrarily close to unity at high accelerations". It is set by the phantom matter near the MOND radius R_M = (GM/a0)^{1/2} ≈ 8×10³ au. — [Milgrom 2009, MNRAS 399, 474, arXiv:0906.4817](https://arxiv.org/abs/0906.4817); numerical confirmation and perihelion precessions in [Blanchet & Novak 2011, MNRAS 412, 2530, arXiv:1010.1349](https://arxiv.org/abs/1010.1349) ("The MOND functions that are compatible with this constraint appear to have a very rapid transition").

---

## 1. Screening constructions in the MOND context (Vainshtein/galileon, k-mouflage, chameleon/symmetron, density- or potential-dependent a0)

### Takeaway
Only one published MOND-type theory computes Solar System observables under explicit screening: the Galileon "k-mouflage" model of Babichev, Deffayet & Esposito-Farèse (2011). It does so only for an isolated, spherically symmetric Sun. No external Galactic field is included, so the EFE quadrupole Q2 is never computed, and its rotation curves were never fit to SPARC. Milgrom's 2023 GQUMOND gives a mechanism (an extra length or time scale) that would suppress the Solar System EFE, but only qualitatively, with no Q2 number. Symmetron "RAR" models admit tension with Solar System tests in the regime where they fit rotation curves. I found no published paper that computes Q2 for any screened MOND theory and also fits SPARC.

### Cited Findings
**Galileon k-mouflage MOND (Babichev, Deffayet, Esposito-Farèse 2011)** [full text read]
- A scalar field with TeVeS-like disformal coupling gets a covariant Galileon term with a constant k of dimension length⁴. Field profile: ϕ′ ∝ r at small r (screened, "k-mouflage"), ϕ′ ∝ 1/r in the MOND regime, ϕ′ ∝ 1/r² asymptotically (Brans–Dicke-like). Transition radius r_V = (8kGMa0)^{1/4}/c. — [PRD 84, 061502(R), arXiv:1106.2538](https://arxiv.org/abs/1106.2538)
- **What it computes.** It solves perturbatively for a static, spherically symmetric scalar on a Schwarzschild background, i.e. an isolated point mass. It fixes k ≈ G(10³ M☉)c⁴/(8a0³) so that MOND still acts in 10³ M☉ systems. It then compares the residual scalar force ϕ′c² ≈ rc²/√(8k) with post-Newtonian forces: ratio ≈ (r/22 au)⁴, i.e. <10⁻⁵ at Earth, <10⁻⁷ at Mercury, 2×10⁻⁵ at Mars, 3×10⁻³ at Jupiter. For the Moon it is 10⁻⁸ of PN. Preferred-frame effects equal α1 ≈ 2×10⁻¹² (Mars) and ≈10⁻¹⁵ (Moon). A binary-pulsar Ṗ estimate is ≥10³² below current uncertainties, which the authors call possibly "erroneous by some large numerical coefficient." — same source
- **What it does not compute.** The paper has no Galactic external field, no EFE, no quadrupole or Q2, and no ephemeris fit. It says PPN parameters cannot even be defined, "because the PPN formalism assumes that no length scale enters the theory". It also has no rotation-curve or RAR fits: "MOND phenomenology" is assumed beyond r_V. — same source (grep of the full text finds no "external", "quadrupole" or "Cassini" in a Solar System context)
- It notes that an alternative quintic Galileon gives scalar effects ~(r/6 au)^{7/2} × PN, "about the order of magnitude of the most precise bounds", and that "a full fit of planetary data ... would thus be necessary." — same source
- Stability and well-posedness are deferred to a "forthcoming publication". — same source
- **Follow-up (g-TeVeS).** Złośnik & Skordis call this model g-TeVeS. Within an estimate of the parameter space that recovers MOND phenomenology, "the theory cannot successfully approximate the Friedmannian cosmological behavior of cold dark matter." — [PRD 95, 124023 (2017), arXiv:1702.00683](https://arxiv.org/abs/1702.00683)
- **Uptake.** Khoury's 2015 "Alternative to particle dark matter" makes Solar System safety rest entirely on this term: "This can restore consistency with solar system tests if ℓ ≲ 100 kpc [Babichev et al.]". Khoury does not compute this himself. He also notes that his k-mouflage-type kinetic term is "strictly superluminal" (c_s ≃ √2 radially in the MOND regime). — [PRD 91, 024022, arXiv:1409.0012](https://arxiv.org/abs/1409.0012) [full text read]
- Desmond, Hees & Famaey (2024) also point to this route: Galileon screening "could completely suppress all MOND effects below a Vainshtein radius ... with the length-scale proposed by Babichev et al. (2011), MOND effects would be killed in the SS and up to the typical (mass and length) scale of WBs." This is a suggestion in their discussion, not a calculation. — [MNRAS 530, 1781, arXiv:2401.04796](https://arxiv.org/abs/2401.04796) [full text read]

**Generalized QUMOND with an extra scale (Milgrom 2023)** [full text read]
- GQUMOND theories have a Lagrangian that depends on higher derivatives of the Newtonian potential ψ, and they bring in a length ℓ0, a frequency Ω0, or a potential-like scalar. In variant A, f = f[(∇ψ)²/(ℓ0² ψ,ij ψ,ij)] with f→1 (QUMOND) on large scales and f→0 (Newton) in small systems. Outside a point mass the argument is r²/6ℓ0². Variant B screens systems with short dynamical times, f = f[Ω0⁻⁴ ψ,ij ψ,ij]. Variant C is potential-dependent screening, which Milgrom links to EMOND [Zhao & Famaey 2012] and does not develop: "I shall not further discuss this choice". — [PRD 108, 084005, arXiv:2305.01589](https://arxiv.org/abs/2305.01589)
- **On the Solar System EFE.** The higher derivatives of ψ near the phantom-mass region are dominated by the Sun's own field, with scales "∼6000 au, and a timescale of ∼4.5×10⁵ years. If these are smaller than ℓ0 or Ω0⁻¹, respectively, then f(u) ≪ 1, and the MOND anomaly is greatly reduced." The paper gives no Q2 value, no ℓ0 fit and no SPARC fit. On galactic scales (≫ℓ0) the theory reduces to QUMOND by construction. Milgrom also argues the Sun–planet saddle-point MOND effects are "totally suppressed". — same source
- Park et al. (2026) cite this paper as the "another scale beyond a0" option. — [arXiv:2602.17884](https://arxiv.org/abs/2602.17884)

**Symmetron fifth force "RAR" (Burrage, Copeland, Millington 2017) and follow-ups** [full text read]
- Claim: the RAR "may be explained, in the absence of cold dark matter, by a non-minimally coupled scalar field, whose fifth forces are partially screened on galactic scales by the symmetron mechanism". Illustrative rotation curves are shown for SPARC galaxies. — [PRD 95, 064050, arXiv:1610.07529](https://arxiv.org/abs/1610.07529)
- The authors' own caveat: "In the weakly non-linear regime, the galaxies are unscreened at all radii, placing the present analysis in tension with Solar System constraints". "This alone does not eliminate the need for dark matter, and some tension with local tests of gravity remains". They suggest, without computing it, that the strongly non-linear regime may lessen the tension. — same source
- Follow-up: the same field cannot explain the baryonic-vs-lensing mass difference without extending the field content. That pushes toward a regime where the scalar also acts as a DM component. — [Burrage, Copeland, Käding, Millington 2019, PRD 99, 043539, arXiv:1811.12301](https://arxiv.org/abs/1811.12301)
- O'Hare & Burrage recompute the Solar System constraints for the DM-free symmetron, using PPN |γ−1| ≲ 10⁻⁵ (Cassini time delay) and |β−1| ≲ 10⁻⁴ (LLR) as functions of {M, μ, v}. They find "a region of parameter space not already excluded that can explain the vertical motions of local stars out to heights of 1 kpc". The test is 1-D Milky-Way-disk vertical kinematics only, not the SPARC RAR. Their Solar System constraint is PPN γ/β, not an EFE/Q2 quadrupole. — [PRD 98, 064019, arXiv:1805.05226](https://arxiv.org/abs/1805.05226)

**Density-dependent gravity: "refracted gravity" (Matsakos & Diaferio 2016)** [full text read]
- A modified Poisson equation with gravitational permittivity ε(ρ): ε→1 for ρ≫ρc and ε→ε0 for ρ≪ρc. The paper claims it describes disk-galaxy rotation curves, the Tully–Fisher relation and cluster X-ray temperature profiles. — [arXiv:1603.04943](https://arxiv.org/abs/1603.04943) (the arXiv record shows no journal_ref; treat as **preprint** unless a journal version is found)
- On the Solar System, the paper only speculates that the density-smoothing length D is "tens of astronomical units or larger, because the mass discrepancy problem appears to be relevant on scales larger than the solar system". It flags open issues: "a possible incompatibility with special relativity ... or a possible violation of the Strong Equivalence [Principle]". It contains no Solar System calculation. — same source

**Potential- or environment-dependent a0**
- EMOND makes a0 a function of the gravitational potential to fix clusters. Hodson & Zhao find that "EMOND has some success in fitting some clusters, but overall has issues when trying to explain the mass deficit fully." — [A&A 598, A127 (2017), arXiv:1701.03369](https://arxiv.org/abs/1701.03369). The original EMOND paper explores "an effective force law" where the deep-potential systems (clusters) get a larger acceleration scale. — [Zhao & Famaey 2012, PRD 86, 067301, DOI 10.1103/PhysRevD.86.067301, arXiv:1207.6232](https://arxiv.org/abs/1207.6232) (abstract only read; I found no Solar System Q2 computation for EMOND)
- "Machian MOND" promotes a0 to a variable set by mass outside the enclosed region, in spherical systems, to boost clusters "while retaining MOND predictions in galaxies". It does not address the Solar System in its abstract. — [Uruena Palomo & Santander 2026, IJMPD, DOI 10.1142/S0218271826500434, arXiv:2608.04894](https://arxiv.org/abs/2608.04894)
- Khoury (2015) says his model needs a0 to vary mildly with scale or mass (~12× higher in clusters). He suggests chameleon or symmetron dependence but leaves it "to future work". — [arXiv:1409.0012](https://arxiv.org/abs/1409.0012)

**Outer Solar System cross-check**
- AQUAL simulations of long-period/Oort comets fail to reproduce the observed binding-energy distribution. For the gradual-transition AQUAL they also fail to reproduce the detached TNO disk. The abstract states: "Our results do not rule out some MOND theories more elaborate than AQUAL, in which non-Newtonian effects are screened on small spatial scales, at small masses, or in external gravitational fields comparable in strength to the critical acceleration." — [Vokrouhlický, Nesvorný, Tremaine 2024, arXiv:2403.09555](https://arxiv.org/abs/2403.09555) (the arXiv record has no journal_ref; a web-search snippet says ApJ, **journal version UNVERIFIED**)

### Inferences
- **Inference (my arithmetic from Babichev et al.'s Eq. 9 and their chosen k).** The screened residual is an isotropic linear force a = κr with κ = √(a0³/(G·10³M☉)). With a0 = 1.2×10⁻¹⁰ m s⁻², κ ≈ 3.6×10⁻²⁷ s⁻². This reproduces their ratio of ≈0.04 to the PN force at Saturn. That κ is the same order as the Cassini Q2 sensitivity of 1.8×10⁻²⁷ s⁻². It is a monopole (r² potential, equivalent to a uniform density ≈1.3×10⁻²⁰ g cm⁻³), not the traceless quadrupole, so Q2 does not apply directly. Still, "negligible compared to PN forces" does not mean "below ephemeris sensitivity". A proper ephemeris fit of an r² term is needed, and none has been published (paper's own words: "A full fit of planetary data ... would thus be necessary", made there about the quintic variant). κ scales as M_k^{-1/2}: choosing screening at 10⁵ M☉ instead of 10³ M☉ lowers it 10×.
- In a Vainshtein/k-mouflage regime the EFE need not mimic QUMOND's. Galileon shift symmetry tends to decouple a uniform external gradient. Babichev et al.'s operator, however, contains the Riemann tensor, so this has to be computed, not assumed. This is the specific gap that makes "screening passes Cassini" unproven for MOND. It is also why the retracted in-house Vainshtein claim should not be revived on the strength of this literature: no paper computes Q2 under Vainshtein screening.
- GQUMOND is the cleanest way to decouple Q2 from the RAR interpolating function: with ℓ0 ≫ 6000 au, galaxies stay pure QUMOND. It is non-relativistic, though, and its Solar System suppression is a scaling argument.

### Gaps
- No paper found that computes Q2 (or any EFE quadrupole) for a screened MOND theory (Galileon/Vainshtein, k-mouflage, GQUMOND, symmetron, refracted gravity or EMOND).
- No paper found that fits SPARC with a screened MOND theory *and* checks Cassini at once. The symmetron work is illustrative and admits Solar System tension.
- No chameleon-based MOND construction found: arXiv abstract search "MOND AND chameleon" returned only a 2008 conference proceeding (Zhao, arXiv:0811.3465). No dedicated k-mouflage-MOND paper found beyond Babichev et al. 2011.
- Not checked: whether Babichev et al.'s promised stability paper exists, and whether Babichev & Esposito-Farèse later work on time-dependent Galileon backgrounds alters the Solar System screening.

---

## 2. Interpolating functions engineered to reach Newton fast (Hees et al. 2016 and later)

### Takeaway
Hees et al. (2016) found that, against the 2014 Cassini Q2 bound, only the ν̄_α family with α ≥ 2 fit rotation curves without too large a Solar System deviation. ν̃_α is excluded, and ν_α and ν̂_α are only marginally acceptable at large α. Later and stronger analyses reversed that "viable" verdict. Desmond, Hees & Famaey (2024) fit the transition location and sharpness to SPARC and find 8.7σ tension (fiducial) with Q2. Park et al. (2026) raise this to 3–15σ with the improved Q2. No later paper found a family that passes both within plain AQUAL/QUMOND.

### Cited Findings
- Hees et al. 2016: the EFE improves some outer rotation-curve fits. The combined RC + Cassini analysis "rules out several classes of popular MOND transition functions, but leaves others viable". LISA Pathfinder cannot improve these constraints. — [MNRAS 455, 449, DOI 10.1093/mnras/stv2330, arXiv:1510.01369](https://arxiv.org/abs/1510.01369)
- From the full text: "The functions ν̃α are completely rejected by this analysis. The transition functions να and ν̂α can ... still be viable for large values of α. The only class of functions that is compatible with both types of observations for almost all α is ν̄α, for α ≥ 2. We note however that these constraints do not apply to, e.g., modified inertia theories." — same source [full text read]
- Desmond, Hees & Famaey 2024 infer the location and sharpness of the MOND transition from the SPARC RAR. They find that the Solar System quadrupole "requires a significantly sharper transition between the deep-MOND and Newtonian regimes than is allowed by the RAR (an 8.7σ tension under fiducial model assumptions)". Freeing mass-to-light ratios relieves this somewhat, and removing galaxies with bulges brings it down to 1.9σ. An AQUAL correction for flattened systems gives similar results. The Q2 constraint implies no deviation from Newton in nearby wide binaries. — [MNRAS 530, 1781, DOI 10.1093/mnras/stae955, arXiv:2401.04796](https://arxiv.org/abs/2401.04796)
- Their discussion: staying in modified gravity and "taking the inconsistency of the RAR and Q2 results at face value necessitates a modification to the AQUAL or QUMOND weak-field limits of any such theory", e.g. screening à la Babichev et al. 2011. They also consider a sharp sigmoid transition at a new acceleration scale, which they note introduces a new scale. — same source [full text read]
- Park et al. 2026 update the tension to 3–15σ, depending on mass modelling or galaxy subset. They find a ≤2% MOND boost at the Sun (95%), "in strong tension with current observational limits", and conclude the AQUAL/QUMOND Newtonian limit is challenged. — [arXiv:2602.17884](https://arxiv.org/abs/2602.17884)
- Review context: Banik & Zhao 2022 review the MOND evidence and Solar System tests. — [Symmetry 14, 1331, DOI 10.3390/sym14071331, arXiv:2110.06936](https://arxiv.org/abs/2110.06936)

### Inferences
- The time order matters. A reader citing Hees 2016's "ν̄_α, α≥2 viable" is citing a superseded result. Desmond 2024 fits the transition sharpness to SPARC directly and finds it incompatible. This matches the user's own scan finding no passing function with a0 ∈ [0.90, 1.30]×10⁻¹⁰.
- Desmond's 1.9σ "bulge-free" relief depends on how bulges are modelled. It is a data-systematics route, not a theory route.

### Gaps
- I did not extract Hees 2016's numeric Table 2 χ² values per family beyond the quoted conclusions.
- I found no 2024–2026 paper proposing a new single-function AQUAL/QUMOND family that passes both. Desmond 2024 explicitly argues it would require a new scale.

---

## 3. MOG / Scalar–Tensor–Vector Gravity (Moffat)

### Takeaway
MOG fits rotation curves through a Yukawa-type, linear weak-field law. It therefore has no MOND-type EFE, and its Solar System safety comes from parameter scaling (a small α or long range λ for a solar mass), which Moffat and Toth do compute against Yukawa bounds. The density-screening argument for PPN tests appears only in a Moffat preprint. Independent tests are few. They are mostly outside the Solar System (S2 star, Magellanic Stream, clusters), and the theory's own parameters vary between versions: fixed α = 8.89, μ = 0.042 kpc⁻¹ versus α and μ that "run" with mass.

### Cited Findings
- Original theory: G, a vector coupling ω and a vector mass μ vary in space and time. It "can fit galaxy rotation curves and cluster data without non-baryonic dark matter" and is "consistent with solar system observational tests" (asserted in the abstract). — [Moffat 2006, JCAP 03 (2006) 004, DOI 10.1088/1475-7516/2006/03/004, arXiv:gr-qc/0506021](https://arxiv.org/abs/gr-qc/0506021)
- Rotation curves: [Brownstein & Moffat 2006, ApJ 636, 721, arXiv:astro-ph/0506370](https://arxiv.org/abs/astro-ph/0506370)
- Pioneer anomaly: Brownstein & Moffat fit the Pioneer 10/11 anomalous acceleration with "running" constants. They say the fit is consistent with inner-planet data. — [CQG 23, 3427 (2006), arXiv:gr-qc/0511026](https://arxiv.org/abs/gr-qc/0511026). (The Pioneer anomaly was later attributed to thermal recoil; I did not resolve that source in this session, so that attribution is UNVERIFIED here.)
- Weak-field law (Moffat & Rahvar 2013): a Newtonian term plus a repulsive Yukawa, with universal α = 8.89 ± 0.34 and μ = 0.042 ± 0.004 kpc⁻¹ (THINGS). Ursa Major fits give mean χ² = 1.07 with M/L as the only free parameter. — [MNRAS 436, 1439, arXiv:1306.6383](https://arxiv.org/abs/1306.6383). Clusters: inner theoretical mass profiles exceed the data, converging beyond ~300 kpc. The authors assert compatibility "from the solar system to Mega parsec scales". — [MNRAS 441, 3724 (2014), arXiv:1309.5077](https://arxiv.org/abs/1309.5077)
- Mass-dependent parameters and Solar System (Moffat & Toth 2009): μ²M = D² is constant. For the Sun they predict λ_Y ≃ 0.16 pc (~33,000 au) and |α_Y| ≃ 3×10⁻⁸; for the Earth, λ_Y ≃ 58 au and |α_Y| ≃ 9×10⁻¹⁴. They call these "clearly not in contradiction with even the most accurate experiments to date", via a plot adapted from published Yukawa bounds. This is a computed comparison against Yukawa (α, λ) limits. — [CQG 26, 085002, arXiv:0712.1796](https://arxiv.org/abs/0712.1796) [full text read]
- PPN and light bending: a conformal coupling "screens" G. The scalar acquires a density-dependent mass, heavy in the Sun and Earth, and "this guarantees that solar system tests of gravity are satisfied". Light deflection and Shapiro delay are claimed to agree with GR. — [Moffat 2014, arXiv:1410.2464](https://arxiv.org/abs/1410.2464) (**preprint**: the arXiv record has no journal_ref; mostly asserted)
- SPARC: the RAR is fit with α and μ that "run with galaxy mass", after "adjusting galaxy parameters within ±1-sigma bounds". The quoted RAR a0 = (5.4 ± 0.3)×10⁻¹¹ m s⁻². — [Green & Moffat 2019, Phys. Dark Univ. 25, 100323, arXiv:1905.09476](https://arxiv.org/abs/1905.09476) (authors' own group)
- Milky Way: MOG fits the MW rotation curve with 5×10¹⁰ M☉ and no halo, and the authors say MOND does not. — [Moffat & Toth 2015, PRD 91, 043004, arXiv:1411.6701](https://arxiv.org/abs/1411.6701) (own group)
- GW170817: the authors claim MOG is consistent (c_T = c, WEP holds). — [Green, Moffat & Toth 2018, PLB, DOI 10.1016/j.physletb.2018.03.015, arXiv:1710.11177](https://arxiv.org/abs/1710.11177) (own group)
- **Independent tests**
  - S2 orbit around Sgr A*: α ≲ 0.410 at 99.7% (arXiv v1 abstract) and "no serious tension with GR". A web-search snippet quoted α ≲ 0.662; the published value is **UNRESOLVED**, so check MNRAS 510. — [Della Monica, de Martino, de Laurentis 2022, MNRAS, DOI 10.1093/mnras/stab3727, arXiv:2105.12687](https://arxiv.org/abs/2105.12687)
  - Magellanic Stream: MOG "seems to be plausible" with appropriate parameters. — [Haghi & Rahvar 2010, IJTP, DOI 10.1007/s10773-010-0279-4, arXiv:1002.3136](https://arxiv.org/abs/1002.3136)
  - Clusters: A1689 lensing plus X-ray. Nieuwenhuizen argues that MOND, MOG, emergent gravity and f(R) without DM fail near the cluster centre. — [Fortschr. Phys. 2016, DOI 10.1002/prop.201600050, arXiv:1610.01543](https://arxiv.org/abs/1610.01543)
  - Ultra-diffuse galaxy Dragonfly 44: with α and μ fixed from THINGS, the best-fit M_dyn/L_I = 7.4 (+1.5/−1.4), "larger than plausible SPS values". The authors state "MOG is ruled out at 5.49σ ... if its free parameters are fixed at the highest values consistent with THINGS data", while MOND is acceptable at 2.40σ. MOG becomes acceptable only if α and μ are allowed to vary. — [Haghi, Amiri, Hasani Zonoozi, Banik, Kroupa, Haslbauer 2019, ApJL, DOI 10.3847/2041-8213/ab4517, arXiv:1909.07978](https://arxiv.org/abs/1909.07978)
  - Related, not MOG itself: Yukawa fifth force plus NFW DM fit to 40 SPARC galaxies gives β = 0.34 ± 0.04 and λ = 5.61 ± 0.91 kpc. This includes DM, so it does not test DM-free MOG. — [de Almeida, Amendola, Niro 2018, JCAP 08 (2018) 012, arXiv:1805.11067](https://arxiv.org/abs/1805.11067)
  - Moffat's 2026 kSZ preprint (fit parameters α ~ 9.11, μ ~ 0.196 Mpc⁻¹) uses yet another cluster-scale parameter set. — [arXiv:2604.23440](https://arxiv.org/abs/2604.23440) (**preprint**)

### Inferences
- **Q2 for MOG (my inference).** The weak-field equations are linear (Newton plus Yukawa), so there is no MOND-type EFE. The Galaxy acts on the Solar System only through its tidal field, which has Q2 ~ Ω² ~ (v_c/R0)² ≈ 10⁻³⁰ s⁻². That is three orders of magnitude below the Cassini bound, even with an O(10) MOG enhancement. MOG therefore passes Q2 trivially. Its Solar System risk lies instead in Yukawa/PPN tests. With fixed α = 8.89 and μ = 0.042 kpc⁻¹, the short-distance expansion gives an extra constant inward acceleration ≈ αGM☉μ²/2 ≈ 10⁻²¹ m s⁻² (negligible). With Moffat–Toth mass-running parameters, |α_Y| ≈ 3×10⁻⁸ at λ ≈ 33,000 au, outside planetary orbits.
- The real test for MOG on SPARC is whether one fixed (α, μ) works. Green & Moffat need mass-running parameters and ±1σ adjustments, and their fitted a0-equivalent (5.4×10⁻¹¹) is about half the usual 1.2×10⁻¹⁰. Also, a finite Yukawa range implies eventually Keplerian (non-flat) curves beyond ~1/μ. Flat lensing-inferred curves out to hundreds of kpc would test this; I have not verified a paper that makes this argument for MOG.

### Gaps
- I did not locate an independent (non-Moffat) DM-free SPARC test of MOG. The Haghi et al. 2019 DF44 test above is the strongest independent galaxy-scale test found. A separate Haghi & Amiri dwarf-spheroidal MOG paper is remembered but not resolved: UNVERIFIED. No independent PPN or ephemeris analysis of MOG found.
- Not resolved: a primary source for the Pioneer thermal explanation (Turyshev et al. 2012).

---

## 4. Verlinde's emergent gravity (2017)

### Takeaway
Emergent gravity's weak-field formula is MOND-like for a point mass but differs inside extended bodies. On the RAR it needs low M/L and predicts a radius-dependent residual that is not observed. In the Solar System, applying its spherical transition formula gives perihelion advances seven orders of magnitude too large (Hees, Famaey & Bertone 2017). That rules out the present weak-field formula, with the caveat that the theory's domain of validity is disputed. Hossenfelder's covariant version and later cluster and lensing tests do not repair the Solar System result.

### Cited Findings
- Theory: the elastic response of dark energy to baryons gives a "dark gravity" force set by a0 = cH0. Published in SciPost. — [Verlinde 2017, SciPost Phys. 2, 016, DOI 10.21468/SciPostPhys.2.3.016, arXiv:1611.02269](https://arxiv.org/abs/1611.02269)
- RAR: "EG is consistent with the observed RAR only if we substantially decrease the fiducial stellar mass-to-light ratios; the resulting values are in tension with other astronomical estimates". EG also "predicts that the residuals around the RAR should correlate with radius; such residual correlation is not observed." — [Lelli, McGaugh, Schombert 2017, MNRAS 468, L68, DOI 10.1093/mnrasl/slx031, arXiv:1702.04355](https://arxiv.org/abs/1702.04355)
- Galaxies plus Solar System: fits are "marginally acceptable with strikingly low best-fit distances, low stellar mass-to-light ratios, and a low Hubble constant", with unobserved wiggles caused by the dependence on dg_N/dr. In spherical symmetry outside matter, the perihelion predictions "are discrepant with the data by seven orders of magnitude, ruling out the present emergent gravity weak-field formula with high confidence". Tabulated predictions vs data include Mercury −1.01×10⁷ vs 0.4 ± 0.6 and Saturn −0.23×10⁷ vs 0.15 ± 0.65 (units as in their table, ephemeris-derived supplementary advances). — [Hees, Famaey, Bertone 2017, PRD 95, 064019, arXiv:1702.04358](https://arxiv.org/abs/1702.04358) [full text read]
- Lensing: the first KiDS+GAMA test (33,613 isolated galaxies) finds "good agreement" without fitting any parameters. — [Brouwer et al. 2017, MNRAS 466, 2547, arXiv:1612.03034](https://arxiv.org/abs/1612.03034). KiDS-1000 lensing RAR "agrees well with the MG predictions" for both MOND and EG, but early- and late-type galaxies differ by ≥6σ, which current MG theories "would be unable to explain" (unless circumgalactic gas differs). — [Brouwer et al. 2021, A&A 650, A113, arXiv:2106.11677](https://arxiv.org/abs/2106.11677)
- Dwarfs and clusters:
  - Dwarf spheroidals: fits are acceptable without maximal deformation; with it, M/L comes out marginally high. — [Diez-Tejedor et al. 2018, MNRAS 477, 1285, arXiv:1612.06282](https://arxiv.org/abs/1612.06282)
  - Isolated dwarfs: EG over- or under-predicts v_max away from ~100 km s⁻¹. — [Pardo 2020, JCAP 12 (2020) 012, arXiv:1706.00785](https://arxiv.org/abs/1706.00785)
  - Coma plus 58 stacked clusters: GR+CDM preferred, with strong tension at r ≳ 10 Mpc. — [Tamosiunas et al. 2019, JCAP 05 (2019) 053, arXiv:1901.05505](https://arxiv.org/abs/1901.05505)
  - 23 clusters: ruled out at >5σ with nominal profiles, but not formally excluded once systematics are included. — [Halenka & Miller 2020, PRD 102, 084007, arXiv:1807.01689](https://arxiv.org/abs/1807.01689)
- Internal consistency: "When properly done, Verlinde's elaborate procedure recovers the standard Newtonian gravity instead of MOND." — [Dai & Stojkovic 2017, JHEP 11 (2017) 007, arXiv:1710.00946](https://arxiv.org/abs/1710.00946)
- Covariant version: a vector field that drags on baryons. Correction terms are computed on a Schwarzschild background. — [Hossenfelder 2017, PRD 95, 124018, arXiv:1703.01415](https://arxiv.org/abs/1703.01415)

### Inferences
- Hees et al.'s Solar System failure comes from EG's own transition formula, which depends on g_N and dg_N/dr. A version restricted to "outside the bulk of matter, in spherical symmetry" is exactly where the authors applied it. Defenders would have to argue that the formula does not apply inside the Solar System at all, i.e. that a new screening would be needed. I found no paper that does this quantitatively.
- Q2 for EG has not been computed, as far as I found. The perihelion test already fails by about 10⁷.

### Gaps
- No post-2017 paper found that rescues EG in the Solar System.
- Cluster add-on (resolved): for A2142 and A2319 (X-COP), EG's apparent DM has a different radial shape, "with larger discrepancies (by a factor 2–3) in the inner (r<200 kpc) cluster's regions and a remarkable agreement only across R500". — [Ettori et al. 2017, MNRAS Letters, DOI 10.1093/mnrasl/slx074, arXiv:1612.07288](https://arxiv.org/abs/1612.07288)

---

## 5. Other credible 2015–2026 proposals addressing the Solar System vs rotation-curve tension

### Takeaway
The recent literature that names the tension explicitly (Desmond 2024, Park 2026, Vokrouhlický 2024) proposes three exits: a new length or time scale (GQUMOND), Vainshtein screening (Babichev 2011), or modified inertia. None has been carried through to a Q2 computation plus a SPARC fit. Non-MOND alternatives (symmetron, refracted gravity, MOG, EG) either admit Solar System tension, lack a Solar System calculation, or fail elsewhere. I found no 2015–2026 proposal that has demonstrably passed both Cassini Q2 and the SPARC RAR in a published calculation.

### Cited Findings
- Explicit statements of the exits: [Desmond, Hees, Famaey 2024, arXiv:2401.04796](https://arxiv.org/abs/2401.04796); [Park et al. 2026, arXiv:2602.17884](https://arxiv.org/abs/2602.17884); [Vokrouhlický, Nesvorný, Tremaine 2024, arXiv:2403.09555](https://arxiv.org/abs/2403.09555)
- GQUMOND (length, frequency or potential scale): [Milgrom 2023, arXiv:2305.01589](https://arxiv.org/abs/2305.01589)
- Open clusters: 2026 claim that ~90% of Gaia DR3 open clusters (N★ ≤ 250) lie near the RAR with g† ≈ 1.2×10⁻¹⁰ (±0.5 dex). Interpreted as a non-smooth Galactic field "partially mitigating the external field effect". This is a **preprint** and an observational claim, not a theory. If confirmed, it would conflict with any screening that kills MOND below ~10³ M☉ or ~pc scales. — [Huisjes & Hernandez 2026, arXiv:2603.03522](https://arxiv.org/abs/2603.03522)
- a0 time dependence (scale-invariant vacuum prediction, tested on SPARC): a weak redshift dependence with large uncertainties. — [Del Popolo & Chan 2024, Phys. Dark Univ. 43, 101393, arXiv:2405.01841](https://arxiv.org/abs/2405.01841)

### Inferences
- There is a tension between screening scales. Babichev et al. set the Vainshtein cutoff so MOND survives down to 10³ M☉; Desmond notes it would also kill MOND in wide binaries. Open-cluster RAR claims (preprint) would instead require MOND in parsec-scale ~10²–10³ M☉ systems inside the Galaxy. GQUMOND with ℓ0 ≳ 6000 au would screen wide binaries (≲0.1 pc) but not pc-scale clusters. Any screening choice must be checked against all three.

### Gaps
- Not surveyed in depth this session: conformal gravity (Mannheim), Maeder's scale-invariant vacuum, Deur's self-interaction model, gravitomagnetic GR explanations, mimetic MOND, nonlocal MOND (Deffayet–Esposito-Farèse–Woodard; covariant, possibly in another researcher's scope), and chameleon f(R) SPARC tests (Naik et al.). IDs for these are UNVERIFIED and are omitted.

---

## 6. What each theory would face, and what one needs to compute it

| Theory | Q2 status | SPARC/RAR status | To compute |
|---|---|---|---|
| AQUAL/QUMOND, any IF | Fails jointly with RAR, 3–15σ (Park 2026), 8.7σ fiducial (Desmond 2024) | Fits RAR | done |
| Galileon k-mouflage MOND (Babichev 2011) | **Not computed.** Isolated-Sun residual κ ≈ 3.6×10⁻²⁷ s⁻² (my arithmetic, monopole) | **Not fit** | Solve the screened field eq. with a uniform external gradient g_e ≈ 1.6–1.9 a0 to get the quadrupole. Fit the r² monopole term to ephemerides. Then do full SPARC fits in the MOND regime (r ≫ r_V ⇒ AQUAL-like, so the IF choice still matters) |
| GQUMOND (Milgrom 2023) | Qualitatively suppressed if ℓ0 ≳ 6000 au or Ω0⁻¹ ≳ 4.5×10⁵ yr. No number | = QUMOND on galaxy scales by construction | Solve GQUMOND numerically for Sun + external field (adapting the Blanchet–Novak setup) as a function of ℓ0. The SPARC fit inherits QUMOND's |
| Symmetron "RAR" | PPN γ/β-constrained. Authors admit tension in the RC-fitting regime | Illustrative only | Joint fit in the strongly non-linear regime |
| Refracted gravity | No Solar System calculation | RCs claimed (2016 preprint) | Choose ρc and the smoothing length D. Interplanetary ρ ≪ ρc would naively unscreen it unless D ≫ au |
| MOG | Passes trivially (linear; only the Galactic tide, ~10⁻³⁰ s⁻²; my inference) | Needs mass-running α, μ (Green & Moffat 2019) | Fixed-parameter SPARC fit. Lensing at large radius (Yukawa cutoff) |
| Emergent gravity | Not computed. Perihelia fail by ~10⁷ | Needs low M/L; residual-radius correlation not seen | Would need new screening |
