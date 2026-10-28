# Dark-matter / MOND hybrids: galaxy predictions, Solar System behaviour, Cassini Q2, status

Researcher notes, compiled 2026-10-28. How the citations were checked: every arXiv ID below was resolved through the arXiv API (export.arxiv.org/api/query), which returned the title, authors, journal reference and DOI. Journal data marked "(INSPIRE)" was taken from the INSPIRE-HEP API record. Statements about what a paper "computes" or "asserts" come from reading its full text (arXiv PDF converted to text), not only the abstract. Three arXiv IDs I recalled from memory were **wrong** and have been corrected: Blanchet & Novak is 1010.1349 (not 1010.1303), Hees+ 2016 is 1510.01369 (not 1510.01024), and Famaey–Khoury–Penco–Sharma is 1912.07626 (not 1912.07610).

Context anchor. Park, Hees, Famaey, Desmond & Durakovic, "Improved constraints on modified Newtonian gravity from Cassini radio tracking data", Phys. Rev. D 114, 024066 (2026), arXiv:2602.17884, DOI 10.1103/r7n8-kw38. They find Q2 = (1.6 ± 1.8)×10⁻²⁷ s⁻², which puts AQUAL/QUMOND-type modified gravity in 3–15σ tension with galaxy rotation curves. Within the Milky Way, Q2 caps the MOND boost at the Sun's position at ≤2% (95% CL). The predicted Q2 "depends solely on the behavior of the IF at the value of the external gravitational field acting on the Sun, hence close to a0" — [arXiv:2602.17884](https://arxiv.org/abs/2602.17884). INSPIRE lists only 2 citing papers so far (a growth-rate MOND test, arXiv:2608.18229, and a Yukawa/SPARC paper in RAA). **Neither concerns a DM–MOND hybrid** — [INSPIRE refersto:recid:3122154](https://inspirehep.net/api/literature?q=refersto:recid:3122154).

---

## Q1. Superfluid dark matter (SfDM): mechanism, where the force acts, Solar System, and published tests

### Takeaway
In SfDM the MOND-like force comes from superfluid phonons that couple to baryons. It acts only inside a galaxy's superfluid core (~65–105 kpc for the Milky Way, so the Sun sits inside it), and an external-field effect (EFE) operates only inside that core. For the Solar System the model's authors use one order-of-magnitude argument: the Sun's own phonon gradient destroys superfluid coherence within ~10²–10³ AU, so the planets should be "Newtonian". That is **asserted from a scaling estimate, not computed**. No paper computes an SfDM prediction for Q2. Mistele (JCAP 2021) states plainly that the naive galaxy-scale SfDM would give Solar-System anomalies "much too large", and that the high-acceleration regime is not understood. On the galaxy side, peer-reviewed tests are mixed to negative: the MW rotation curve fits; SPARC fits work but not in the MOND regime; strong lensing passes; weak lensing ("incompatible ... at least in its current form") and Cherenkov radiation from stars both count against it.

### Cited Findings
**Mechanism and parameters**
- Original proposal (Berezhiani & Khoury, PRD 92, 103510 (2015)). DM is axion-like particles with m ~ eV and strong self-interactions. These condense into a superfluid in galaxies, whose phonons have a P(X) ∝ X^{3/2} Lagrangian. Coupled to baryons, the phonons "reproduc[e] the MOND phenomenology on galactic scales", while ΛCDM is kept on cosmological scales — [arXiv:1507.01019](https://arxiv.org/abs/1507.01019), DOI [10.1103/PhysRevD.92.103510](https://doi.org/10.1103/PhysRevD.92.103510). Companion letter: Phys. Lett. B 753, 639 (2016) — [arXiv:1506.07877](https://arxiv.org/abs/1506.07877), DOI [10.1016/j.physletb.2015.12.054](https://doi.org/10.1016/j.physletb.2015.12.054).
- Fiducial follow-up (Berezhiani, Famaey & Khoury, JCAP 09 (2018) 021).
  - The phonon Lagrangian is L = (2Λ(2m)^{3/2}/3) X√|X| with baryon coupling L_int = αΛ θ ρ_b / M_Pl, giving a0 = α³Λ²/M_Pl.
  - Fiducial values: m = 1 eV, Λ = 0.05 meV, α = 5.7, and best-fit a0 = 0.87×10⁻⁸ cm/s².
  - The phonon force "only applies if both bodies reside within the superfluid region", and the EFE "is only active within the superfluid core of the host".
  - Their Table I lists **"Solar system: Newtonian"**, "Star clusters: MOND with EFE inside galaxy host core", "Galaxy-galaxy lensing: driven by DM envelope ⇒ not MOND", and "rotation curve shapes: MOND (+ small DM component making HSB curves rise)".
  - Source: [arXiv:1711.05748](https://arxiv.org/abs/1711.05748), DOI [10.1088/1475-7516/2018/09/021](https://doi.org/10.1088/1475-7516/2018/09/021).
- Variant (Khoury, PRD 93, 103533 (2016)): an "another path" version — [arXiv:1602.05961](https://arxiv.org/abs/1602.05961), DOI [10.1103/PhysRevD.93.103533](https://doi.org/10.1103/PhysRevD.93.103533).
- Lecture notes (Khoury, SciPost Phys. Lect. Notes 42 (2022)) repeat the Solar System argument word for word ("Coherence is lost within the solar system") — [arXiv:2109.10928](https://arxiv.org/abs/2109.10928), DOI [10.21468/SciPostPhysLectNotes.42](https://doi.org/10.21468/SciPostPhysLectNotes.42).
- 2025 review by Berezhiani, Cintia, De Luca & Khoury ("Superfluid Dark Matter"). **Preprint**: no journal reference on arXiv v2. It repeats that "the local superfluid velocity sourced by the Sun exceeds the BEC critical velocity ... within a distance of order O(10²) AU from the Sun. Thus coherence is lost within the solar system ... no long-range force can be mediated." It lists alternatives: "modifying P(X) at large X and/or introducing higher-derivative operators" — [arXiv:2505.23900](https://arxiv.org/abs/2505.23900).
- Later SfDM theory work (Berezhiani, Cintia & Khoury, PRD 107, 123010 (2023)) suggests whole halos thermalize, fragment, and leave a central soliton up to "a few tens of kpc" — [arXiv:2212.10577](https://arxiv.org/abs/2212.10577), DOI [10.1103/PhysRevD.107.123010](https://doi.org/10.1103/PhysRevD.107.123010).

**Solar System: what is actually derived (BK 2015, Sec. 5 "Validity of EFT and the Solar System")**
- BK estimate the superfluid velocity from the Sun as v_s ≃ 5 (m/eV)⁻¹(Λ/meV)^{−1/3}(AU/r). They take the BEC critical velocity set by the MW at 8 kpc as v_c ≃ 0.02 (m/eV)^{−2/3}(Λ/meV)^{2/9}. Coherence is therefore lost for r ≲ 250 (m/eV)^{−1/3}(Λ/meV)^{−5/9} AU, "which is larger than the solar system". Hence "the condensate is replaced by a phase of normal DM ... the usual worries about MOND and local tests of gravity do not apply" — [arXiv:1507.01019](https://arxiv.org/abs/1507.01019).
  - This is a scaling estimate.
  - Neither the transition region nor the planetary dynamics nor any Solar-System quadrupole is computed.
  - BK also say MOND's Solar-System problem could otherwise be cured by modifying P(X) at large X ("requires fine-tuning") or by a galileon operator (citing Babichev, Deffayet & Esposito-Farèse, PRD 84, 061502 (2011), [arXiv:1106.2538](https://arxiv.org/abs/1106.2538), DOI [10.1103/PhysRevD.84.061502](https://doi.org/10.1103/PhysRevD.84.061502)).
- BFK 2018 only restates this: "As argued in [55,56], the large phonon gradient induced by an individual star results in a breakdown of superfluidity in its vicinity. Coherence is lost within the solar system. Individual DM particles still interact with baryons, but no long-range force can be mediated." — [arXiv:1711.05748](https://arxiv.org/abs/1711.05748).
- Mistele, "Three problems of superfluid dark matter and their solution", JCAP 01 (2021) 025. "naively extending the galaxy-scale phenomenology of SFDM to the solar system gives additional accelerations ~a+ that are much too large [BK15]. One way to satisfy the solar system constraints could be to introduce higher-derivative terms [Babichev+ 2011] ... it makes sense to consider these constraints only after we understand the high-acceleration regime of SFDM. Studying this is left for future work." — [arXiv:2009.03003](https://arxiv.org/abs/2009.03003), DOI [10.1088/1475-7516/2021/01/025](https://doi.org/10.1088/1475-7516/2021/01/025).
- **The EFE in SfDM is not automatically MONDian.** Mistele 2021: "In SFDM, it is usually assumed that there is a standard MONDian EFE inside the superfluid core ... However, this is true only if ε ≪ 1 ... If ε is not small, there is no standard MONDian EFE in the superfluid core – even if the rotation curve is MONDian due to [a] numerical coincidence." His proposed two-field SFDM "does have a proper MOND limit, i.e. it has a MONDian phonon acceleration as well as a MONDian EFE" — [arXiv:2009.03003](https://arxiv.org/abs/2009.03003).
- Is the Sun inside the superfluid core? Yes. Hossenfelder & Mistele (MNRAS 498, 3484 (2020)) find, for the MW, an NFW radius R_NFW ≈ 65–73 kpc and a thermal radius R_T ≈ 67–105 kpc (for M200^DM = 0.5–3×10¹² M☉). The Sun at ~8 kpc is therefore inside — [arXiv:2003.07324](https://arxiv.org/abs/2003.07324), DOI [10.1093/mnras/staa2594](https://doi.org/10.1093/mnras/staa2594).
- INSPIRE joint-citation searches find **no** paper on SfDM's Solar-System quadrupole:
  - Papers citing both BK 2015 and Hees+ 2014 (Cassini, [arXiv:1402.6950](https://arxiv.org/abs/1402.6950), PRD 89, 102002) number 10. All are BFK 2018, the Famaey–Khoury–Penco papers, reviews, wide-binary papers and emergent-gravity papers.
  - Papers citing both BK 2015 and Blanchet & Novak's EFE paper ([arXiv:1010.1349](https://arxiv.org/abs/1010.1349)) number 6. None computes an SfDM Q2.
  - Source: [INSPIRE query](https://inspirehep.net/api/literature?q=refersto:recid:1381485%20and%20refersto:recid:1282876).

**Galaxy-scale tests (peer-reviewed unless noted)**
- **MW rotation curve** (Hossenfelder & Mistele, MNRAS 2020). "superfluid dark matter fits the data well with parameters in reasonable ranges" for R < 25 kpc. It needs ~20% less baryonic mass than MOND (M_b = 5.96×10¹⁰ M☉). The phonon force was switched on only inside R_NFW, with a "discontinuity" the authors say "should not be taken too seriously". On the MW vertical-force constraint they say "we cannot address this interesting constraint here" — [arXiv:2003.07324](https://arxiv.org/abs/2003.07324).
- **MW vertical vs radial acceleration** (Lisanti, Moschella, Outmezguine & Slone, PRD 100, 083009 (2019)). They find that "scalar amplifications of gravity" are disfavoured (ΔBIC ≈ 4–10) and that MOND-like-force models "struggle to simultaneously explain both the rotational velocity and vertical motion of nearby stars". Caveat: for SfDM itself they "postpone the full treatment of these models to future work" and only "expect a qualitative similarity". This is **an expectation for SfDM, not a computation** — [arXiv:1812.08169](https://arxiv.org/abs/1812.08169), DOI [10.1103/PhysRevD.100.083009](https://doi.org/10.1103/PhysRevD.100.083009). The 2025 SfDM review replies that the Jeans analysis assumes a steady-state disk, "at odds with the observed disequilibrium of disk stars" — [arXiv:2505.23900](https://arxiv.org/abs/2505.23900).
- **SPARC rotation curves** (Mistele, McGaugh & Hossenfelder, A&A 664, A40 (2022); 169 SPARC galaxies). Mass-to-light ratios are "generally acceptable", but they show "an unnatural dependence on the size of the galaxy". Best fits "often" fall "in the regime where the superfluid's force cannot resemble that of MOND without adjusting a boundary condition separately for each galaxy". Forcing the MOND regime puts "the total dark matter mass ... in tension with strong lensing data" — [arXiv:2201.07282](https://arxiv.org/abs/2201.07282), DOI [10.1051/0004-6361/202243216](https://doi.org/10.1051/0004-6361/202243216).
- **Strong lensing** (Hossenfelder & Mistele, JCAP 02 (2019) 001; SLACS lenses). "we can successfully fit all galaxies except one ... strong gravitational lensing does not pose a challenge" — [arXiv:1809.00840](https://arxiv.org/abs/1809.00840), DOI [10.1088/1475-7516/2019/02/001](https://doi.org/10.1088/1475-7516/2019/02/001).
- **Weak lensing** (Mistele, McGaugh & Hossenfelder, JCAP 09 (2023) 004). SfDM "reproduces MOND only up to a certain distance from the galactic center, and only for kinematic observables: It does not affect trajectories of light". Having "solved the equations of motion", they conclude "the SFDM model is incompatible with the weak-lensing observations, at least in its current form" — [arXiv:2303.08560](https://arxiv.org/abs/2303.08560), DOI [10.1088/1475-7516/2023/09/004](https://doi.org/10.1088/1475-7516/2023/09/004).
- **Cherenkov radiation from stars** (Mistele, JCAP 11 (2022) 008). Hybrid models "typically contain a mode that is directly coupled to matter (for MOND) and has a non-relativistic sound speed (for CDM)", so stars can lose energy to Cherenkov radiation — [arXiv:2103.16954](https://arxiv.org/abs/2103.16954), DOI [10.1088/1475-7516/2022/11/008](https://doi.org/10.1088/1475-7516/2022/11/008).
  - Follow-up (**preprint**, no journal ref on arXiv): "For the original superfluid dark matter model (SFDM), we rule out a part of the parameter space, including the most commonly used parameters. For two-field SFDM, we find no constraint ... For [Skordis–Złośnik], we find no constraint". It uses "a controlled approximation that depends only on the MOND regime" — [arXiv:2208.14308](https://arxiv.org/abs/2208.14308).
  - The SfDM review counters that this "does rely on the validity of the superfluid EFT on small scales, which ... must break down in the vicinity of stars" — [arXiv:2505.23900](https://arxiv.org/abs/2505.23900). **The two sides disagree here.** Mistele says his bound uses only the a < a0 region; the review says the EFT near stars is invalid.
- **Chemical potential / consistency** (Mistele, JCAP 11 (2019) 039). The symmetry-breaking baryon–phonon coupling means "no exactly conserved quantity" is associated with μ — [arXiv:1909.05710](https://arxiv.org/abs/1909.05710), DOI [10.1088/1475-7516/2019/11/039](https://doi.org/10.1088/1475-7516/2019/11/039).
- **Dynamical friction** is absent for subsonic motion in the core (Berezhiani, Elder & Khoury, JCAP 10 (2019) 074). This gives a distinctive test: bars and Fornax globular clusters — [arXiv:1905.09297](https://arxiv.org/abs/1905.09297), DOI [10.1088/1475-7516/2019/10/074](https://doi.org/10.1088/1475-7516/2019/10/074).

### Inferences
- If one takes BK's estimate at face value, the Cassini lever arm (Saturn at ~9.6 AU) lies deep inside the "normal-phase bubble". The bubble radius is ~250 AU for m = 1 eV and Λ = 1 meV. For the BFK fiducial Λ = 0.05 meV, the same scaling (Λ^{−5/9}) gives ~1,300 AU (my arithmetic; BK's eq. (84) may hide an α dependence). **On that assumption SfDM predicts Q2 ≈ 0 (pure GR) and passes Cassini trivially.** That pass rests entirely on an unmodelled phase boundary.
- The bubble picture leaves a real consistency question unaddressed in the papers I read:
  - If coherence is lost within ~10² AU of every star, how do stars (and the Sun) couple to the galaxy-scale phonon gradient that must supply their MOND-like rotational acceleration?
  - Is there a residual EFE-like tidal field at the bubble boundary?
  - A consistent treatment would have to model the star + bubble as an effective point source in the phonon EFT. That would also decide whether the Galactic phonon field's non-linearity leaks a quadrupole into the bubble.
- If the bubble argument were dropped and SfDM worked in a regime with a standard MONDian EFE (Mistele's ε ≪ 1 or two-field SFDM), the planets would sit in an AQUAL-like non-linear field. The Park et al. tension would then apply in the same form, with a phonon "interpolating function" fixed by P(X) plus finite-temperature corrections.

### Gaps
- No published computation of Q2 (or any planetary-ephemeris observable) in SfDM. Two INSPIRE joint-citation searches plus a full-text read of BK15, BFK18, Mistele 2021/2022 and the 2025 review all came up empty.
- No published model of the superfluid/normal-phase boundary around a star. The size and shape of the "bubble" and its effect on how the star couples to the Galactic phonon field are unknown.
- The 2025 review (arXiv:2505.23900) is still a preprint. I could not confirm any journal version.

---

## Q2. Dipolar dark matter (Blanchet & Le Tiec and successors)

### Takeaway
Dipolar DM gets MOND from "gravitational polarization" of a dipolar DM medium. The non-relativistic limit is the Bekenstein–Milgrom (AQUAL) equation, i.e. MOND as a gravitational dielectric. The Solar System is handled by assuming polarization switches off when g ≫ a0. The bimetric version computes **PPN parameters equal to GR's** for that internal regime. The Galactic EFE/Q2 was **never computed for dipolar DM**. Because the Sun sits at g_ext ~ a0, the "switch-off at g ≫ a0" argument does not remove the EFE quadrupole. If the medium at the Sun is polarized in equilibrium, the Park et al. AQUAL bound should apply. Status: peer-reviewed theory papers; no SPARC-scale fits; the first N-body equilibrium tests show a dynamical instability.

### Cited Findings
- Origin (Blanchet, CQG 24, 3529 (2007), "Gravitational polarization and the phenomenology of MOND") — [arXiv:astro-ph/0605637](https://arxiv.org/abs/astro-ph/0605637), DOI [10.1088/0264-9381/24/14/001](https://doi.org/10.1088/0264-9381/24/14/001). Dipolar particles in GR: CQG 24, 3541 (2007) — [arXiv:gr-qc/0609121](https://arxiv.org/abs/gr-qc/0609121), DOI [10.1088/0264-9381/24/14/002](https://doi.org/10.1088/0264-9381/24/14/002).
- Blanchet & Le Tiec, PRD 78, 024031 (2008).
  - The dipolar fluid is "undistinguishable from ... Λ plus standard dark matter" at first-order cosmological perturbation level.
  - "Invoking an argument of 'weak clusterisation' ... the dipolar dark matter reproduces the phenomenology of MOND at galactic scales."
  - On the Solar System, the model "may apply only at large scales ... and not at smaller scales like in the Solar System".
  - A slow MOND→Newton transition (χ ∝ g⁻¹) would give a constant "Pioneer-type" extra acceleration g ~ g_N + ε a0, "incompatible with current measurements". They conclude "the validity of the model should be limited to large scales".
  - Source: [arXiv:0804.3518](https://arxiv.org/abs/0804.3518), DOI [10.1103/PhysRevD.78.024031](https://doi.org/10.1103/PhysRevD.78.024031).
- Blanchet & Le Tiec, PRD 80, 023524 (2009): the action is reformulated as a matter action in GR. There is no Solar-System or EFE computation — [arXiv:0901.3114](https://arxiv.org/abs/0901.3114), DOI [10.1103/PhysRevD.80.023524](https://doi.org/10.1103/PhysRevD.80.023524).
- Bimetric extension (Bernard & Blanchet, PRD 91, 103536 (2015)). They choose W(X) so that polarization is suppressed for g ≫ a0 ("the dark matter medium becomes inactive"). They compute the 1PN limit and "find the same parametrized post-Newtonian (PPN) parameters as" GR — [arXiv:1410.7708](https://arxiv.org/abs/1410.7708), DOI [10.1103/PhysRevD.91.103536](https://doi.org/10.1103/PhysRevD.91.103536). The PPN result is **computed**, but only for the internal g ≫ a0 regime, not for the EFE.
- The bimetric version is ghost-unstable. Blanchet & Heisenberg write that "it is plagued by ghost instabilities in the gravitational sector". They then move to massive bigravity:
  - PRD 91, 103518 (2015) — [arXiv:1504.00870](https://arxiv.org/abs/1504.00870), DOI [10.1103/PhysRevD.91.103518](https://doi.org/10.1103/PhysRevD.91.103518).
  - JCAP 12 (2015) 026 — [arXiv:1505.05146](https://arxiv.org/abs/1505.05146), DOI [10.1088/1475-7516/2015/12/026](https://doi.org/10.1088/1475-7516/2015/12/026). This paper itself notes MOND "is also severely constrained by observations in the solar system [Milgrom 2009; Blanchet & Novak 2011]".
  - The EFT version is ghost-free in the decoupling limit: PRD 96, 083512 (2017) — [arXiv:1701.07747](https://arxiv.org/abs/1701.07747), DOI [10.1103/PhysRevD.96.083512](https://doi.org/10.1103/PhysRevD.96.083512).
- Blanchet & Novak, MNRAS 412, 2530 (2011). This is the theoretical basis of the Cassini test: a numerical integration of the MOND equation with an external field, giving the Q2 quadrupole — [arXiv:1010.1349](https://arxiv.org/abs/1010.1349), DOI [10.1111/j.1365-2966.2010.18076.x](https://doi.org/10.1111/j.1365-2966.2010.18076.x). Proceedings: "Testing MOND in the Solar System" (no journal) — [arXiv:1105.5815](https://arxiv.org/abs/1105.5815). INSPIRE finds 9 papers citing both BL09 and BN11. None computes a dipolar-DM Q2; the list includes Blanchet's own JCAP 2015 and Blanchet & Seraille 2025.
- N-body test (Stahl, Famaey, Thomas, Dubois & Ibata, MNRAS 517, 498 (2022); RAMSES).
  - They recover the analytic equilibrium "where a low density Dipolar DM halo is at rest with respect to its central galaxy, recovering the aforementioned scaling relations".
  - That equilibrium "harbours a dynamical instability with a characteristic time depending on the Dipolar DM halo density".
  - Source: [arXiv:2209.07831](https://arxiv.org/abs/2209.07831), DOI [10.1093/mnras/stac2670](https://doi.org/10.1093/mnras/stac2670). Park et al. 2026 cite this paper as ref. [30] — [arXiv:2602.17884](https://arxiv.org/abs/2602.17884).
- Newest successor (Blanchet & Seraille, JCAP 12 (2025) 036, "non-Abelian Yang-Mills graviphoton").
  - Deep MOND emerges via "gravitational polarization of the dark matter medium", with local Lorentz violation restored by a khronon field.
  - The authors concede: "the transition to the high acceleration regime is missing ... we know that the MOND interpolating function is highly constrained by observations in the Solar System [Milgrom 2009; Blanchet & Novak; Hees+ 2016; Vokrouhlický+ 2024]".
  - Source: [arXiv:2502.14686](https://arxiv.org/abs/2502.14686), DOI [10.1088/1475-7516/2025/12/036](https://doi.org/10.1088/1475-7516/2025/12/036) (INSPIRE).

### Inferences
- Park et al. say Q2 depends only on the interpolating function at g ≈ g_ext,MW ≈ a0. Dipolar DM's non-relativistic equation is AQUAL-form with χ(g) set by W. So **if** an equilibrium-polarized dipolar medium exists at the Sun's location, dipolar DM inherits the AQUAL Q2–RAR tension essentially unchanged. Its only escape is the medium being absent, unpolarized or out of equilibrium inside the heliosphere.
- The Blanchet–Seraille model has no interpolating regime yet, so it cannot currently be confronted with Q2 at all.

### Gaps
- No paper computes Q2 or any Solar-System EFE for dipolar DM, nor the local dipolar-DM density or polarization state near the Sun.
- No SPARC-scale fit of dipolar DM was found.

---

## Q3. Other hybrids where a dark component emulates MOND

### Takeaway
Several other "DM emulates MOND" constructions exist. Most avoid Solar-System constraints by **assertion**: baryon dominance, a local-only interaction, or entropy bottoming out. The Famaey–Khoury–Penco baryon-interacting DM has **no EFE at all**, so it predicts Q2 ≈ 0. That is a clean, model-distinctive Cassini pass, but it also forfeits MOND's EFE successes. Verlinde-type emergent gravity is the one case with a computed Solar-System test: it fails planetary perihelia by 7 orders of magnitude (Hees, Famaey & Bertone 2017). Hossenfelder's covariant version asserts no Solar-System effect.

### Cited Findings
- **Baryon-interacting DM (Famaey, Khoury & Penco, JCAP 03 (2018) 038).**
  - The MDAR emerges from DM–baryon interactions. "In our scenario, baryon-DM interactions are local and there is no EFE ... whether it is effectively 'MONDian' or 'Newtonian' [is set by] local quantities, such as the local DM density and velocity dispersion."
  - They also note that "consistency with post-Newtonian constraints in the Solar system should be checked" for a possible pc-range mediator force.
  - Source: [arXiv:1712.01316](https://arxiv.org/abs/1712.01316), DOI [10.1088/1475-7516/2018/03/038](https://doi.org/10.1088/1475-7516/2018/03/038).
- **BIDM heating follow-up (Famaey, Khoury, Penco & Sharma, JCAP 06 (2020) 025).** They derive BTFR and CSDR scalings from a heating rate inversely proportional to BIDM density. "One promising way of ensuring that our scenario is compatible with small-scale (e.g., solar system) constraints would be to consider interactions that involve collective excitations emerging at scales of O(pc). We leave the exploration ... for future work." — [arXiv:1912.07626](https://arxiv.org/abs/1912.07626), DOI [10.1088/1475-7516/2020/06/025](https://doi.org/10.1088/1475-7516/2020/06/025).
- **Hossenfelder's covariant emergent gravity ("imposter field"; PRD 95, 124018 (2017)).** "if the density of matter is too large, the entropy-decrease bottoms out ... With this approach one can therefore explain why one does not observe MOND-like modifications on solar-system scales." This is **asserted**, with no Solar-System computation — [arXiv:1703.01415](https://arxiv.org/abs/1703.01415), DOI [10.1103/PhysRevD.95.124018](https://doi.org/10.1103/PhysRevD.95.124018).
  - Related: Hossenfelder & Mistele, IJMPD 27, 1847010 (2018), redshift dependence of radial acceleration — [arXiv:1803.08683](https://arxiv.org/abs/1803.08683), DOI [10.1142/S0218271818470107](https://doi.org/10.1142/S0218271818470107).
  - INSPIRE finds only one paper citing both Hossenfelder 2017 and Hees+ 2014 (the Banik & Zhao review, [arXiv:2110.06936](https://arxiv.org/abs/2110.06936)).
- **Verlinde emergent gravity Solar-System test (Hees, Famaey & Bertone, PRD 95, 064019 (2017)).** Applied in spherical symmetry outside matter, "the predictions for the secular advances of Solar System planets' perihelia are discrepant with the data by seven orders of magnitude, ruling out the present emergent gravity weak-field formula" — [arXiv:1702.04358](https://arxiv.org/abs/1702.04358), DOI [10.1103/PhysRevD.95.064019](https://doi.org/10.1103/PhysRevD.95.064019). (This tests Verlinde's 2016 formula, not Hossenfelder's covariant field.)
- **Two-field SFDM (Mistele 2021).** It splits "the two roles" (energy density vs MOND force) between two fields and gives a MONDian EFE. The Solar System is explicitly deferred — [arXiv:2009.03003](https://arxiv.org/abs/2009.03003).
- **Non-minimally coupled DM / BEC DM.**
  - Bettoni, Liberati & Sindoni (JCAP 11 (2011) 007): "if we impose that ψ(0) = ξ(0) = 0 ... a purely baryonic system will be described by general relativity without corrections ... at the level of solar system ... the density of baryonic matter is much larger than the density of dark matter" (an assertion) — [arXiv:1108.1728](https://arxiv.org/abs/1108.1728), DOI [10.1088/1475-7516/2011/11/007](https://doi.org/10.1088/1475-7516/2011/11/007).
  - Bettoni, Colombo & Liberati (BEC with non-minimal coupling; JCAP 02 (2014) 004): "we argue ... at least two reasons why we expect [Solar-System compatibility]: local dynamics is dominated by baryons ... the scalar field density has to be almost constant" — [arXiv:1310.3753](https://arxiv.org/abs/1310.3753), DOI [10.1088/1475-7516/2014/02/004](https://doi.org/10.1088/1475-7516/2014/02/004).
- **Early survey (Bruneton, Liberati, Sindoni & Famaey, "Reconciling MOND and dark matter?", JCAP 03 (2009) 021)** — [arXiv:0811.3143](https://arxiv.org/abs/0811.3143), DOI [10.1088/1475-7516/2009/03/021](https://doi.org/10.1088/1475-7516/2009/03/021). (Its full text mentions Solar-System compatibility only in passing.)
- **"Modified dark matter" (MDM: Ho, Minic & Ng).** CDM profiles with MOND scaling tied to Λ: PLB 693, 567 (2010) — [arXiv:1005.3537](https://arxiv.org/abs/1005.3537), DOI [10.1016/j.physletb.2010.09.008](https://doi.org/10.1016/j.physletb.2010.09.008). Cluster test by Edmonds et al., IJMPA 32, 1750108 (2017) — [arXiv:1601.00662](https://arxiv.org/abs/1601.00662), DOI [10.1142/S0217751X17501081](https://doi.org/10.1142/S0217751X17501081). The full text has no Solar-System discussion.
- **MOND + sterile-neutrino hybrid (νHDM; Angus, MNRAS 394, 527 (2009)).** Here MOND is modified gravity and the 11 eV sterile neutrinos only fix clusters and the CMB — [arXiv:0805.4014](https://arxiv.org/abs/0805.4014), DOI [10.1111/j.1365-2966.2008.14341.x](https://doi.org/10.1111/j.1365-2966.2008.14341.x). Banik & Zhao advocate this "hybrid approach" — [arXiv:2110.06936](https://arxiv.org/abs/2110.06936), DOI [10.3390/sym14071331](https://doi.org/10.3390/sym14071331).

### Inferences
- νHDM is a hybrid with a dark component, but its Solar System is pure QUMOND. **The Park et al. 3–15σ tension applies to it in full.** It is not an escape route.
- Only two classes give a principled Cassini pass:
  - FKP/BIDM, which has no EFE because the force is local DM–baryon thermalization (Q2 ≈ 0).
  - SfDM *if* the critical-velocity bubble is right.
- Both pay on the galaxy side. BIDM loses the EFE evidence (e.g. the SPARC EFE detections cited in the 2025 SfDM review). SfDM is in tension with weak lensing.

### Gaps
- No Solar-System computation exists for BIDM, MDM, non-minimally coupled/BEC DM, or Hossenfelder's covariant field.
- I did not find a distinct, peer-reviewed "MOND from a polarizable medium" model other than Blanchet's line. The Penner (Astrophys. Space Sci. 2020/2026) "gravitational anti-screening" papers showed up in INSPIRE but were not examined.

---

## Q4. Is the Cassini Q2 constraint relevant to each hybrid, and has anyone computed the prediction?

### Takeaway
**Nobody has computed Q2 for any DM–MOND hybrid.** Its relevance depends entirely on whether the MOND-like field is active and non-linear at ~10 AU while the Galactic field acts:
- SfDM (bubble argument): predicted ≈ 0, asserted.
- Dipolar DM with a polarized medium at the Sun: AQUAL-like, so relevant and likely in tension. Not computed.
- BIDM: no EFE, so ≈ 0.
- νHDM: QUMOND, so fully constrained.

### Cited Findings
- Q2 parameter and its theory:
  - Blanchet & Novak 2011 — [arXiv:1010.1349](https://arxiv.org/abs/1010.1349).
  - First Cassini bound Q2 = (3 ± 3)×10⁻²⁷ s⁻² (Hees, Folkner, Jacobson & Park, PRD 89, 102002 (2014)) — [arXiv:1402.6950](https://arxiv.org/abs/1402.6950), DOI [10.1103/PhysRevD.89.102002](https://doi.org/10.1103/PhysRevD.89.102002).
  - Combined Cassini plus rotation curves "rules out several classes of popular MOND transition functions" (Hees, Famaey, Angus & Gentile, MNRAS 455, 449 (2016)) — [arXiv:1510.01369](https://arxiv.org/abs/1510.01369), DOI [10.1093/mnras/stv2330](https://doi.org/10.1093/mnras/stv2330).
  - 8.7σ RAR–Q2 tension in AQUAL/QUMOND, relieved to 1.9σ when bulge galaxies are removed (Desmond, Hees & Famaey, MNRAS 530, 1781 (2024)) — [arXiv:2401.04796](https://arxiv.org/abs/2401.04796), DOI [10.1093/mnras/stae955](https://doi.org/10.1093/mnras/stae955).
  - Updated Q2 = (1.6 ± 1.8)×10⁻²⁷ s⁻², with 3–15σ tension — [arXiv:2602.17884](https://arxiv.org/abs/2602.17884).
- Park et al. frame the test explicitly for "modified gravity versions" of MOND (AQUAL/QUMOND). Hybrids are not treated — [arXiv:2602.17884](https://arxiv.org/abs/2602.17884).
- The only papers citing both Desmond+ 2024 and BK 2015 are two reviews (Famaey & Durakovic, "MOND" chapter, [arXiv:2501.17006](https://arxiv.org/abs/2501.17006), preprint; Cirelli, Strumia & Zupan, "Dark Matter", [arXiv:2406.01705](https://arxiv.org/abs/2406.01705), SciPost Phys. Rev. 1 (2026) per INSPIRE). Neither computes a hybrid Q2 (I read the INSPIRE record lists only, not the full texts of these reviews).
- Summary table:

| Hybrid | MOND-like field active at ~10 AU with Galactic field? | Q2 prediction | Computed? |
|---|---|---|---|
| SfDM, BK15/BFK18 | No: coherence lost within ~10²–10³ AU ([1507.01019](https://arxiv.org/abs/1507.01019)) | ≈ 0 (GR) | Asserted from a critical-velocity estimate |
| SfDM, naive EFT extrapolation | Yes | "much too large" anomalies ([2009.03003](https://arxiv.org/abs/2009.03003)) | Stated, not quantified |
| Two-field SFDM | Unknown (MONDian EFE in galaxies) | — | Deferred ([2009.03003](https://arxiv.org/abs/2009.03003)) |
| Dipolar DM (BL08/09, bimetric, bigravity) | Only if the medium is polarized at the Sun; polarization switched off only for g ≫ a0 ([1410.7708](https://arxiv.org/abs/1410.7708)) | AQUAL-like (my inference) | No; only 1PN PPN = GR |
| Blanchet–Seraille 2025 | No interpolating regime yet ([2502.14686](https://arxiv.org/abs/2502.14686)) | Undefined | No |
| BIDM (FKP18/FKPS20) | No EFE by construction ([1712.01316](https://arxiv.org/abs/1712.01316)) | ≈ 0 | Implied by "no EFE"; Solar-System PN not checked |
| Covariant emergent gravity (Hossenfelder) | Asserted off at high density ([1703.01415](https://arxiv.org/abs/1703.01415)) | — | No |
| Verlinde formula | Yes | Perihelia off by 10⁷ ([1702.04358](https://arxiv.org/abs/1702.04358)) | Computed: fails |
| νHDM | Yes (QUMOND) | As QUMOND | Yes, via Park et al. (QUMOND) |

### Inferences
- The most valuable new calculation would be Q2 in SfDM with an explicit model of the Sun's normal-phase region and the Galactic phonon background at R ≈ 8 kpc. Fiducial parameters exist (m = 1 eV, Λ = 0.05 meV, α = 5.7), as do Milky Way superfluid solutions (Hossenfelder & Mistele 2020).
- Second most valuable: the dipolar-DM Q2 with W(X) fixed by the RAR.

### Gaps
- No primary source quantifies the size of the residual quadrupole at the SfDM bubble boundary or the dipolar-DM polarization state in the Solar System.

---

## Q5. Concrete tests each hybrid faces, and what they need

### Takeaway
Shared test battery: SPARC rotation curves and the RAR, MW radial and vertical force, weak and strong lensing (which separates "kinematic-only" MOND in SfDM from lensing), clusters, Cherenkov/stellar energy loss, dynamical friction, and the Solar System. SfDM has been tested on most of these and has problems with weak lensing, SPARC M/L trends and Cherenkov. Dipolar DM and BIDM are barely tested quantitatively.

### Cited Findings
- **SPARC / RAR:** the SfDM SPARC test used 169 galaxies and free M/L. The outcomes are an M/L–size trend and non-MOND-regime best fits — [arXiv:2201.07282](https://arxiv.org/abs/2201.07282). Desmond+ 2024 show how to infer the transition location and sharpness from the SPARC RAR in AQUAL/QUMOND. The same machinery could be applied to a hybrid's effective interpolating function — [arXiv:2401.04796](https://arxiv.org/abs/2401.04796).
- **Weak-lensing RAR at large radii:** this is the decisive SfDM test, because the phonon force "does not affect trajectories of light" and is confined to the core — [arXiv:2303.08560](https://arxiv.org/abs/2303.08560). Updated kinematic + weak-lensing RAR data: Mistele, McGaugh, Lelli, Schombert & Li, JCAP 04 (2024) 020 — [arXiv:2310.15248](https://arxiv.org/abs/2310.15248), DOI [10.1088/1475-7516/2024/04/020](https://doi.org/10.1088/1475-7516/2024/04/020). "Indefinitely flat" lensing circular velocities: ApJL 969, L3 (2024) — [arXiv:2406.09685](https://arxiv.org/abs/2406.09685), DOI [10.3847/2041-8213/ad54b0](https://doi.org/10.3847/2041-8213/ad54b0).
- **MW rotation and vertical force:** needs a full non-spherical SfDM solution including a rotating superfluid. H&M 2020 say this framework does not exist — [arXiv:2003.07324](https://arxiv.org/abs/2003.07324). The test method is in Lisanti+ 2019 — [arXiv:1812.08169](https://arxiv.org/abs/1812.08169).
- **Strong lensing (SLACS):** SfDM passes — [arXiv:1809.00840](https://arxiv.org/abs/1809.00840).
- **Stellar Cherenkov energy loss:** needs the sound speeds and matter couplings of each mode — [arXiv:2103.16954](https://arxiv.org/abs/2103.16954), [arXiv:2208.14308](https://arxiv.org/abs/2208.14308) (preprint).
- **Dynamical friction** (bars, Fornax globular clusters, black-hole binaries): Berezhiani+ 2019 [arXiv:1905.09297](https://arxiv.org/abs/1905.09297); BH binaries (preprint per arXiv) [arXiv:2311.07672](https://arxiv.org/abs/2311.07672).
- **EFE systems** (satellites and globular clusters inside versus outside the host core; ultra-diffuse galaxies in clusters): BFK predictions — [arXiv:1711.05748](https://arxiv.org/abs/1711.05748).
- **Dipolar DM:** needs simulations beyond the unstable equilibrium — [arXiv:2209.07831](https://arxiv.org/abs/2209.07831).
- **Solar System (all hybrids):**
  - Needed inputs: the hybrid's effective field equation in the regime g_int ≫ a0 with g_ext ≈ 1–2 a0, and the local DM phase, density or polarization.
  - The theory input is the Blanchet–Novak-style Q2 integral; the data input is the Park et al. Q2 posterior.
  - The MW ≤2% boost bound at the Sun also constrains any hybrid whose MOND-like force acts on stars at R0 — [arXiv:2602.17884](https://arxiv.org/abs/2602.17884).

### Inferences
- The ≤2% MW-boost corollary in Park et al. is model-independent only for theories in which the same field produces both the Galactic boost at R0 and the Solar-System EFE. SfDM's bubble breaks that link, because the Galactic phonon force acts on stars while the planets are screened. So SfDM is not bound by it unless the bubble picture fails.
- For our own QUMOND scans: none of these hybrids supplies an interpolating function that passes both Cassini and SPARC by being a better μ. The ones that pass Cassini do so by switching the field off locally (SfDM bubble, BIDM locality). That is a structural escape, not a functional one.

### Gaps
- No quantitative SPARC or RAR fits exist for dipolar DM, BIDM or MDM.
- No cluster-lensing test was found for BIDM.
- The rotating-superfluid MW model is missing.
- I did not search ADS beyond INSPIRE. Coverage of astro-ph-only works could be incomplete.
