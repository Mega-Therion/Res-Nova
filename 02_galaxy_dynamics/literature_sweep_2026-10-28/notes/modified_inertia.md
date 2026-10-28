# Modified-inertia (MI) formulations of MOND vs. Cassini and SPARC

Compiled 2026-10-28. Every arXiv ID and DOI below was checked against arXiv API metadata (export.arxiv.org) and/or INSPIRE (inspirehep.net API). The full texts of the Milgrom MI papers, Hees et al. 2014, Hees et al. 2016, Park et al. 2026 and Milgrom 2009 were downloaded from arXiv and searched directly. "Preprint" means INSPIRE/arXiv shows no journal version as of 2026-10-28. **[computed here]** marks arithmetic I did myself from formulas in the cited paper. The paper itself does not print those numbers.

## 1. What MI formulations exist, and what is their peer-review status?

### Takeaway
Nearly all MI work is by Milgrom. It is a set of non-relativistic models built around the equations of motion, not a complete theory. The peer-reviewed core is Ann. Phys. 1994, PRL 2012 and PRD 2022. His most detailed treatment of Solar-System, wide-binary and RAR differences (arXiv:2310.14334) and his October 2026 mixed MG+MI paper are preprints. MI proposals by other authors are few, mostly local or toy constructions, and mostly untested.

### Cited Findings
**Milgrom (main line)**
- **Milgrom 1994, Ann. Phys. 229, 384**, "Dynamics with a non-standard inertia-acceleration relation". Peer-reviewed. MI is built from a nonstandard kinetic action S_k[r(t), a0], with gravity left Newtonian. The paper *derives* three results:
  - "Galilei-invariant such theories must be strongly non-local": they cannot even be the limit of a sequence of local higher-derivative theories.
  - A virial relation for bound orbits.
  - The exact circular-orbit result μ(a/a0)·a = dφ/dr with a = v²/r, where μ is fixed by the value of S_k on circular orbits.

  — [arXiv:astro-ph/9303012](https://arxiv.org/abs/astro-ph/9303012), [doi:10.1006/aphy.1994.1012](https://doi.org/10.1006/aphy.1994.1012)
- **Milgrom 1999, Phys. Lett. A 253, 273**, "The modified dynamics as a vacuum effect". Peer-reviewed. Heuristic: inertia arises from interaction with the vacuum through the Unruh effect, which links a0 to cH0 and Λ. No dynamics is derived. — [arXiv:astro-ph/9805346](https://arxiv.org/abs/astro-ph/9805346), [doi:10.1016/S0375-9601(99)00077-8](https://doi.org/10.1016/S0375-9601(99)00077-8)
- **Milgrom 2006, EAS Publ. Ser. 20, 217**, "MOND as modified inertia". Conference proceedings. A qualitative contrast of MI with MG. It proposes the Pioneer anomaly as a discriminator: the MI explanation rests on Pioneer's orbits being "close to linear and unbound" while planetary orbits are "quasi circular and bound". — [arXiv:astro-ph/0510117](https://arxiv.org/abs/astro-ph/0510117), [doi:10.1051/eas:2006074](https://doi.org/10.1051/eas:2006074)
- **Milgrom 2011, Acta Phys. Polon. B 42, 2175**, "MOND—particularly as modified inertia". Conference proceedings in a journal. Uses heuristic Fourier-space toy models, â(ω)κ[A(ω)/a0] = f̂(ω). States that "it is even possible to construct MI theories with practically no EFE". In the frequency-by-frequency version, the theory "will predict no EFE, unless the external and internal motions are of similar frequencies". — [arXiv:1111.1611](https://arxiv.org/abs/1111.1611), [doi:10.5506/APhysPolB.42.2175](https://doi.org/10.5506/APhysPolB.42.2175)
- **Milgrom 2012, PRL 109, 251103**, "Global Deep-MOND Parameter as a Theory Discriminant". Peer-reviewed. Defines Q = ⟨V²⟩/V0² for isolated, pure-disc, deep-MOND galaxies. Known MG theories give Q = 2/3 exactly. MI gives Q = 0.73 ± 0.01 over a wide range of mass distributions, about a 5% difference in rms velocity. — [arXiv:1211.4899](https://arxiv.org/abs/1211.4899), [doi:10.1103/PhysRevLett.109.251103](https://doi.org/10.1103/PhysRevLett.109.251103)
- **Milgrom 2022, PRD 106, 064060**, "Models of modified-inertia formulation of MOND". Peer-reviewed; this is the current reference model.
  - Equation of motion: m â(ω) I[{r̂}, ω, a0] = F̂(ω). Forces stay Newtonian, the inertia functional I depends on the whole trajectory, and the equations are time-nonlocal.
  - Momentum, energy and angular momentum are defined nonlocally and are conserved for isolated systems.
  - The models give correct centre-of-mass motion for composite bodies whose constituents have high internal accelerations.
  - EFE: in a simple example with a dominant external field, the EFE is set by μ(θ⟨a_ex⟩/a0). ⟨a_ex⟩ is a time average, and θ > 1 depends on the ratio of external to internal frequencies.

  — [arXiv:2208.07073](https://arxiv.org/abs/2208.07073), [doi:10.1103/PhysRevD.106.064060](https://doi.org/10.1103/PhysRevD.106.064060)
- **Milgrom 2023, "MOND as manifestation of modified inertia"**. PREPRINT, based on a talk at "MOND at 40", St Andrews, July 2023; no journal version on INSPIRE, 15 citations. Extends the 2022 models to two acceleration functionals, μ̄(A1/a0, A2/a0). A2 measures departure from circularity. It contrasts MI predictions with AQUAL/QUMOND for wide binaries, vertical disc dynamics, the inner Solar System and the RAR. — [arXiv:2310.14334](https://arxiv.org/abs/2310.14334)
- **Milgrom 2025, PRD 111, 104033**, "Is MOND necessarily nonlinear?". Peer-reviewed. Gives a linear, time-local deep-MOND model that modifies both inertia and gravity and has no EFE. Milgrom says it "suffers from important drawbacks" and that he "cannot base some acceptable MOND theory on these models". — [arXiv:2503.07106](https://arxiv.org/abs/2503.07106), [doi:10.1103/PhysRevD.111.104033](https://doi.org/10.1103/PhysRevD.111.104033)
- **Milgrom 2026, "Mixed modified-gravity–modified-inertia MOND theories"**. PREPRINT, submitted 2026-10-15. Families of models with one parameter 0 ≤ η ≤ 1: η = 0 is pure MG and η = 1 is pure MI. The kinetic equations and the field equations get different interpolating functions, and neither has the standard deep-MOND limit. — [arXiv:2610.21699](https://arxiv.org/abs/2610.21699)

**Other authors**
- **Ignatiev 2007, PRL 98, 101101**, "Is violation of Newton's second law possible?". Peer-reviewed. Proposes a laboratory test of MI at the equinoxes. — [arXiv:gr-qc/0612159](https://arxiv.org/abs/gr-qc/0612159), [doi:10.1103/PhysRevLett.98.101101](https://doi.org/10.1103/PhysRevLett.98.101101)
- **Ignatiev 2008, PRD 77, 102001**. Peer-reviewed. Develops the "Static High-Latitude Equinox Modified Inertia" (SHLEM) effect: estimated displacement of a gravitational-wave-interferometer mirror is about 1e-14 m. — [arXiv:0802.1599](https://arxiv.org/abs/0802.1599), [doi:10.1103/PhysRevD.77.102001](https://doi.org/10.1103/PhysRevD.77.102001)
- **Namouni 2015, MNRAS 452, 210**, "Towards an interpretation of MOND as a modification of inertia". arXiv metadata carries no journal reference; the journal citation comes from Milgrom 2023's reference list, and I did not open the DOI. — [arXiv:1504.00475](https://arxiv.org/abs/1504.00475)
- **Alzain 2017, J. Astrophys. Astr. 38, 59**. — [arXiv:1708.05385](https://arxiv.org/abs/1708.05385), [doi:10.1007/s12036-017-9479-0](https://doi.org/10.1007/s12036-017-9479-0)
- **Wang 2010**. Preprint. — [arXiv:1011.3618](https://arxiv.org/abs/1011.3618)
- **Costa, Franzmann & Pereira 2019**. PREPRINT. A *local* MI Lagrangian. It recovers deep-MOND circular orbits, but perturbations switch on higher-derivative, exponentially unstable modes, which the authors argue must vanish. — [arXiv:1904.07321](https://arxiv.org/abs/1904.07321)
- Milgrom 2023 judges these attempts "not very promising". — [arXiv:2310.14334](https://arxiv.org/abs/2310.14334)
- **Shariati & Jafari 2021, PRD 104, 084070**. Peer-reviewed. Recasts Milgrom's MI as Newtonian dynamics with a *non-conservative* effective gravitational field and a non-conservative tidal force. — [arXiv:2111.04768](https://arxiv.org/abs/2111.04768), [doi:10.1103/PhysRevD.104.084070](https://doi.org/10.1103/PhysRevD.104.084070)
- **Demir & Karahan 2014, EPJC 74, 3204**. Peer-reviewed. A relativistic extension "despite the absence of an explicit action functional", through a modified energy-momentum tensor. — [arXiv:1408.5787](https://arxiv.org/abs/1408.5787), [doi:10.1140/epjc/s10052-014-3204-9](https://doi.org/10.1140/epjc/s10052-014-3204-9)
- **Gillot 2025, "Quantum modified inertia"**. Listed by INSPIRE as EPJC 86, 846 (2026). — [arXiv:2507.11524](https://arxiv.org/abs/2507.11524), [doi:10.1140/epjc/s10052-026-16000-8](https://doi.org/10.1140/epjc/s10052-026-16000-8)
- **Uruena Palomo**: Machian/Sciama readings of MOND as frame effects. IJTP 63, 271 (2024) — [arXiv:2410.19007](https://arxiv.org/abs/2410.19007), [doi:10.1007/s10773-024-05808-3](https://doi.org/10.1007/s10773-024-05808-3). EPJC 86, 1215 (2026) — [arXiv:2610.09987](https://arxiv.org/abs/2610.09987), [doi:10.1140/epjc/s10052-026-16501-6](https://doi.org/10.1140/epjc/s10052-026-16501-6)
- **McCulloch "quantised inertia" (MiHsC)**. A separate, non-MOND MI-type proposal published in MNRAS / Ap&SS (e.g. [arXiv:astro-ph/0612599](https://arxiv.org/abs/astro-ph/0612599), MNRAS 376, 338). It is not one of Milgrom's MOND-MI formulations, and I did not assess it further.

### Inferences
- "MI MOND" is not one theory. Its *secondary* predictions depend on free functions that rotation curves do not fix: μ̄'s dependence on A2, the frequency kernels θ1 and θ2, and K(X). Any claim that "MI passes/fails test X" has to name the model.
- For a Res-Nova benchmark, the only fully specified, peer-reviewed MI family is Milgrom 2022 (PRD), optionally with the 2023 A2 extension.

### Gaps
- I did not open the Namouni 2015 journal DOI.
- I found no relativistic, action-based MI theory, and no MI cosmology or lensing calculation (see §4).

## 2. Inner-Solar-System predictions: the Galactic quadrupole Q2, perihelia, ephemerides

### Takeaway
**Confirmed, with a nuance.**
- Hees et al. 2014 do say the EFE quadrupole "is not present in the Modified Inertia approach". They assert it with a citation to Milgrom 2011; they do not derive it.
- Milgrom's MI models do derive a much weaker result: the Galactic field enters planetary motion only as a small addition inside μ̄'s argument. The anomaly therefore falls off as 1−μ(g⊙/a0), not as the MG phantom-matter quadrupole q·a0·(r/r_M).
- So in MI, Cassini/DE440 constrain only how fast μ → 1 at x ≫ 1. Galaxy rotation curves do not constrain that regime. Exponential-type μ (as in the RAR fitting function) passes trivially.
- The real Solar-System risks for MI are elsewhere: highly eccentric or unbound orbits (long-period comets, Oort cloud, spacecraft), where time-nonlocality lets low-acceleration arcs feed back on high-acceleration ones.

### Cited Findings
- **Hees et al. 2014**, PRD 89, 102002 (Cassini, Q2 = (3 ± 3)e-27 s⁻²), Sec. II:
  - Verbatim: "This effect is not present in the Modified Inertia approach to MOND theory [18]", where [18] is Milgrom, Acta Phys. Polon. B 42, 2175 (2011), arXiv:1111.1611.
  - The same section describes MI as "the gravitational field potential is still determined by the Newtonian Poisson equation but the particle equations of motion are modified [17, 18]" and adds "A serious drawback of this approach is that these theories are non-local [19 = Felten 1984]".

  — [arXiv:1402.6950](https://arxiv.org/abs/1402.6950), [doi:10.1103/PhysRevD.89.102002](https://doi.org/10.1103/PhysRevD.89.102002)
- **What the cited source (Milgrom 2011) actually says.** No Q2 calculation; it is a heuristic statement:
  - "High-acceleration Fourier components … such as for the planetary motions around the sun, suffer only a small MOND correction [negligibly small if κ(x) approaches 1 very fast as x ≫ 1]".
  - The frequency-by-frequency toy model "will predict no EFE, unless the external and internal motions are of similar frequencies".

  — [arXiv:1111.1611](https://arxiv.org/abs/1111.1611)
- **Milgrom 2009, MNRAS 399, 474.** The paper that introduced the MG Solar-System quadrupole q·a0/R_M.
  - Says "Probing this anomaly may also help distinguish between modified inertia and modified gravity formulations of MOND."
  - Says "it is not possible to deduce a generic modified inertia prediction of the EFE … such formulations can be constructed in which there is no EFE in the inner SS".
  - Notes that galactic dynamics probe μ "only at low values of x ≲ 5, and gives no constraint whatever on the high x behavior". It adds: "It is easy to invent forms of µ(x) with slow rise near x = 1, but very fast convergence to 1 at high x".
  - Gives the MG range 10⁻² ≲ −q ≲ 0.3.

  — [arXiv:0906.4817](https://arxiv.org/abs/0906.4817), [doi:10.1111/j.1365-2966.2009.15302.x](https://doi.org/10.1111/j.1365-2966.2009.15302.x)
- **Milgrom 2023 (preprint), Sec. V B — why the anomaly is MG-specific.** In AQUAL/QUMOND, the anomaly comes from the elliptic, Poisson-like field equation: phantom matter near the Sun–Galaxy balance point, several thousand AU away, gives an inner-Solar-System quadrupole of about q·a0·(r/r_M), with r_M ≈ 7000 AU. That anomaly "does not decrease like 1 − µ(g⊙/a0) … it does not become negligible even if µ(x) approach 1 very fast". By contrast:
  - "In MI theories … the MOND modification depends only on what happens along the trajectory itself. If all accelerations there … are high, as happens with bodies that live only in the inner Solar System – MOND approaches Newtonian dynamics as fast as 1 − µ(a/a0)."
  - The anomaly "is not generic; in some MI formulations it is predicted to essentially not be present".

  — [arXiv:2310.14334](https://arxiv.org/abs/2310.14334)
- **Milgrom 2023 (preprint), Sec. VI D 3 — derived within the MI models.** For a planet always at g⊙ ≫ a0:
  - "the exact Newtonian solution without an anomaly applies here since the values of Ai calculated for it are many orders of magnitude larger than a0 … The galactic field enters only as a small addition to the Newtonian contribution in the arguments of µ̄. So, unlike the AQUAL/QUMOND anomaly, here the anomaly does disappear if the theory tends to Newtonian dynamics fast enough".
  - Number given: with ν(y) = 1/(1 − e^{−y^{1/2}}), the Earth has ν − 1 ≈ e^{−10⁴}, "totally negligible".
  - Abstract: "These models predict a much weaker effect of the Galactic field in the inner Solar System than is predicted by AQUAL/QUMOND."

  — [arXiv:2310.14334](https://arxiv.org/abs/2310.14334)
- **Park, Hees, Famaey, Desmond & Durakovic 2026, PRD.**
  - Q2 = (1.6 ± 1.8)e-27 s⁻² (1σ) from the DE440 dataset, a 40% improvement.
  - This Q2 "encodes the external field effect predicted by modified gravity versions of … MOND".
  - Tension with rotation curves is 3–15σ.
  - Within the Milky Way, the MOND boost at the Sun's position is limited to <2% (95%).
  - Conclusion "on classical modified gravity versions of MOND".

  — [arXiv:2602.17884](https://arxiv.org/abs/2602.17884), [doi:10.1103/r7n8-kw38](https://doi.org/10.1103/r7n8-kw38)
- **Hees, Famaey, Angus & Gentile 2016, MNRAS 455, 449.** States that "In modified gravity versions of MOND, this External Field Effect also appears in the Solar System". The combined Cassini+rotation-curve exclusion is framed for MG. — [arXiv:1510.01369](https://arxiv.org/abs/1510.01369), [doi:10.1093/mnras/stv2330](https://doi.org/10.1093/mnras/stv2330)
- **The constraint that does apply to MI: the "1−μ" anomaly.** Perihelion-precession limits on interpolating-function families (power-law and exponential tails), solved analytically. Chan & Lee assert, without separate derivation, that the results "can be generally applied to both of the modified inertia and modified gravity versions of MOND".
  - Chan & Lee 2023, MNRAS 518, 6238 — [arXiv:2212.01019](https://arxiv.org/abs/2212.01019), [doi:10.1093/mnras/stac3509](https://doi.org/10.1093/mnras/stac3509)
  - Earlier: Sereno & Jetzer 2006, MNRAS 371, 626 — [arXiv:astro-ph/0606197](https://arxiv.org/abs/astro-ph/0606197), [doi:10.1111/j.1365-2966.2006.10670.x](https://doi.org/10.1111/j.1365-2966.2006.10670.x)
- **Eccentric and unbound orbits are the MI-specific Solar-System channel.**
  - Milgrom 2009: "In non-local, modified inertia formulations of MOND, anomalies may appear in the inner solar system in the motion of bodies that are on highly eccentric trajectories … Cases in point are the long-period comets, and the Pioneer spacecraft." — [arXiv:0906.4817](https://arxiv.org/abs/0906.4817)
  - Milgrom 2011: for orbits with Fourier components |â(ω)|ω ≪ a0, "such as very-long-period comets–a low frequency anomalous acceleration of order a0 may appear … even when the body is in a high acceleration region, e.g., near the sun". — [arXiv:1111.1611](https://arxiv.org/abs/1111.1611)
  - No number is given in either paper (asserted, not computed).
- **The Pioneer anomaly, once offered as an MI signature, has a thermal origin.** Milgrom 2006 named it a possible decisive test. — [doi:10.1051/eas:2006074](https://doi.org/10.1051/eas:2006074). Turyshev et al. 2012, PRL 108, 241101, "Support for the thermal origin of the Pioneer anomaly" — [arXiv:1204.2507](https://arxiv.org/abs/1204.2507), [doi:10.1103/PhysRevLett.108.241101](https://doi.org/10.1103/PhysRevLett.108.241101)
- **Experiments that separate MI from MG** (Milgrom 2023, Sec. IV):
  - Ignatiev's equinox experiment: an anomaly "is expected only in MI".
  - A spacecraft held at a Sun–planet saddle point by non-gravitational forces: an anomaly appears in MG but "practically none is expected in MI, because then the kinematic acceleration of the spacecraft is much larger than a0".
  - A free-fall fly-by of the saddle region: anomaly "in any MOND theory".

  — [arXiv:2310.14334](https://arxiv.org/abs/2310.14334)

### Inferences
- For Res-Nova: the QUMOND result (no interpolating function passes both Cassini and SPARC) does not carry over to MI. In MI, Q2 is not a MOND observable at leading order. The only inner-planet constraint is on the large-x tail of μ, a region SPARC does not probe (x ≲ 5).
  - [computed here] With the RAR ν(y) = 1/(1−e^{−√y}): at Saturn, g ≈ 6.5e-5 m s⁻², so y ≈ 5×10⁵ and √y ≈ 700. Then 1−μ ~ e^{−700}, far below any ephemeris bound.
  - [computed here] With the simple ν_1 family: 1−μ ≈ a0/g gives a constant anomaly of about a0 toward the Sun. That is excluded by planetary ephemerides in *both* MI and MG, so in MI the ν_n tail matters while the Q2 term does not.
- The MI Solar-System statement rests on Milgrom's heuristic models. They are peer-reviewed in 2022, and the explicit Solar-System derivation is preprint-only (2023). It is not a theorem about every possible MI theory.

### Gaps
- No paper gives a number for the MI anomaly on long-period comets, Oort-cloud bodies or extreme trans-Neptunian objects.
- **Vokrouhlický, Nesvorný & Tremaine 2024** (arXiv metadata lists no journal reference) checked here. They use AQUAL only: "This leaves aside the modified inertia variant of MOND." They also say that because MI is time-nonlocal, "a thorough analysis of modified-inertia models in specific astronomical problems has not been carried out so far; in particular, standard N-body techniques could not be used." Their result that the simulations "appear to rule out AQUAL" for the remote Solar System therefore does not test MI. — [arXiv:2403.09555](https://arxiv.org/abs/2403.09555)
- No MI perihelion-precession calculation for *eccentric* orbits that includes time-nonlocality exists. Chan & Lee's claim that it also applies to MI is asserted.

## 3. Rotation curves under MI: circular orbits, non-circular orbits, the MI EFE, and which galaxy data discriminate

### Takeaway
- **Exactly circular orbits** reproduce the algebraic RAR exactly, a·μ(a/a0) = g_N, in *any* MI theory. This is a general theorem (Milgrom 1994).
- **Non-circular and vertical motion** shift it: they lower the predicted speed, mostly at small radii, and add scatter that depends on the tracer.
- **The MI EFE** is μ(θ⟨a_ex⟩/a0), with θ(0) of order a few. It is set by orbit-averaged, frequency-weighted accelerations and has no directional dependence, unlike MG's μ(a_ex/a0).
- **SPARC tests disagree.** Petersen & Lelli 2020 find both MI and MG within 1.5σ; Chae 2022 finds 6.9σ against MI; Frandsen & Petersen 2018 claim >5σ (preprint). Milgrom (2023, preprint) counters that tests using the exact algebraic relation "did not test MI".

### Cited Findings
- **Circular-orbit theorem.** "In any MI theory the relation between the central gravity force, the orbital radius, and the orbital speed on circular orbits … perforce has the form μ(V²/Ra0)V²/R = −∂φ/∂R … it is specific to circular orbits." — [Milgrom 2011, arXiv:1111.1611](https://arxiv.org/abs/1111.1611); derived in [Milgrom 1994, arXiv:astro-ph/9303012](https://arxiv.org/abs/astro-ph/9303012)
- **Vertical motion lowers the predicted speed** (Milgrom 2023, preprint, Eqs. 45–47). With a vertical component, A1 = V²/R + ωz²z0·θ1(ωz/ω). The correction "reduces the value of the predicted rotational speed relative to that predicted by the algebraic relation". It is "small at large radii, becomes important at small radii, and brings the predicted MI velocities closer to those predicted by AQUAL", as illustrated with Brada & Milgrom 1995 (MNRAS 276, 453; [arXiv:astro-ph/9407071](https://arxiv.org/abs/astro-ph/9407071)). The paper also says:
  - This lowers MI's Q relative to 0.73, "diminishing the value of this parameter as a discriminant".
  - It predicts tracer-dependent speeds, with thick/old discs slower, and cites the Milky Way thick disc rotating about 5% slower than the thin disc (Vieira et al. 2022, ApJ 932, 28). Milgrom notes this may instead be asymmetric drift.
  - It adds scatter to the RAR.

  — [arXiv:2310.14334](https://arxiv.org/abs/2310.14334)
- **Vertical dynamics.** g_N^z/a_z ≈ μ(θ1(ω/ωz)·ω²R/a0) ≈ μ(θ1(0)·ω²R/a0) for ω ≪ ωz. "This is not the same factor that gives the rotation-curve anomaly … θ1(0) could be of the order of a few." — [arXiv:2310.14334](https://arxiv.org/abs/2310.14334)
- **MI EFE (Milgrom 2022, PRD, Eq. 35).** For a subsystem on a circular orbit, â(ω_in)·μ[θ(0)a_ex/a0] = â_N(ω_in). Examples: θ(y) = 2/(1+y²) gives θ(0) = 2, and θ(y) = e^{1−y} gives θ(0) = e. "It is not this factor [μ(a_ex/a0)] that enters the EFE, as is the case in the presently used modified-gravity theories." θ must fall off fast for y ≫ 1 to give correct centre-of-mass motion for composite bodies, which makes θ(0) > 1. — [arXiv:2208.07073](https://arxiv.org/abs/2208.07073)
- **MI EFE vs MG** (Milgrom 2023, preprint). Three differences:
  - (a) MI depends on "global characteristics of the external orbit, and is the same everywhere along it"; MG depends on the momentary g_ex.
  - (b) MI has no dependence on the direction of g_ex.
  - (c) MI's μ* = μ̄(x1, x2), where x2 (eccentricity) and θ1(0) are "not" fixed by rotation curves.
  - A hysteresis effect means a satellite's EFE "might be dominated … by the galaxy's field at orbital perigalacton" (Milgrom 2011).

  — [arXiv:2310.14334](https://arxiv.org/abs/2310.14334); [arXiv:1111.1611](https://arxiv.org/abs/1111.1611)
- **Two-body deep-MOND difference** (Milgrom 2023, preprint). For equal masses, V12⁴ = 2·MGa0 in MI versus ≈ 0.61·MGa0 in AQUAL/QUMOND/TRIMOND, "predicting a relative speed ≈ 25 percent lower" in MG for a given M. — [arXiv:2310.14334](https://arxiv.org/abs/2310.14334)
- **Data tests on SPARC:**
  - **Petersen & Lelli 2020, A&A 636, A56.** 15 SPARC galaxies pass quality cuts. The Q values "seem to favor MG theories, albeit both MG and MI predictions are in agreement with the data within 1.5σ". — [arXiv:2001.03348](https://arxiv.org/abs/2001.03348), [doi:10.1051/0004-6361/201936964](https://doi.org/10.1051/0004-6361/201936964)
  - **Chae 2022, ApJ 941, 55.** "Taken at face value there is a 6.9σ difference between the inner and outer parts on an acceleration plane which would be inconsistent with current proposals of modified inertia". "All aspects of rotation curves are most naturally explained by modified gravity" (with EFE). — [arXiv:2207.11069](https://arxiv.org/abs/2207.11069), [doi:10.3847/1538-4357/ac93fc](https://doi.org/10.3847/1538-4357/ac93fc)
  - **Milgrom's counter** (2023, preprint): Chae's analysis "used for the MI MOND prediction the exact algebraic relation (44). This analysis thus did not test MI MOND, and would require reevaluation". — [arXiv:2310.14334](https://arxiv.org/abs/2310.14334)
  - **Frandsen & Petersen 2018** (PREPRINT, not published per INSPIRE). "MOND modified inertia models … are disfavoured at more than 5σ independent of model details", using closed zero-area g2-space curves. — [arXiv:1805.10706](https://arxiv.org/abs/1805.10706)
  - **Petersen & Frandsen**, the earlier method paper, was published as MNRAS 496, 1077 (2020) according to INSPIRE. The arXiv abstract says the systematics were "loosely quantified" and the authors "do not underline the result". — [arXiv:1710.03096](https://arxiv.org/abs/1710.03096), [doi:10.1093/mnras/staa1541](https://doi.org/10.1093/mnras/staa1541)
  - **Eriksen, Frandsen & From 2021, A&A 656, A123.** MI yields "neutral" g2-space geometries, MG yields "cored" ones. Some cuspy and cored SPARC galaxies "deviate significantly from the MOND modified gravity and MOND modified inertia predictions". — [arXiv:1906.07823](https://arxiv.org/abs/1906.07823), [doi:10.1051/0004-6361/202040189](https://doi.org/10.1051/0004-6361/202040189)
  - **Mercado et al. 2024, MNRAS 530, 1349.** Downward "hooks" in the RAR, which appear in cored-halo FIRE-2 ΛCDM galaxies, "are challenging to explain in Modified Inertia theories of MOND". — [arXiv:2307.09507](https://arxiv.org/abs/2307.09507), [doi:10.1093/mnras/stae819](https://doi.org/10.1093/mnras/stae819)

### Inferences
- Galaxy data that can discriminate:
  - Inner-vs-outer RAR loops (the Chae / Frandsen–Petersen g2-space tests), *redone* with the non-circular corrections Milgrom says are needed.
  - Q in extremely low-surface-brightness, deep-MOND discs.
  - Thin-vs-thick disc rotation lag versus asymmetric drift.
  - Vertical velocity dispersions and disc scale heights, where MI's θ1(0) enters.
  - Outer-RC declines from the EFE, with MI's orbit-averaged and direction-free form.
  - Satellites on eccentric orbits, where MI predicts a perigalacticon-dominated EFE.
- The MI predictions that go beyond circular orbits depend on free functions (θ1, θ2, μ̄'s A2 dependence). A negative result can therefore be partly absorbed. That weakens falsifiability unless the kernels are fixed in advance.

### Gaps
- No published fit of Milgrom's 2022/2023 models, with non-circular corrections, to SPARC.
- No reanalysis of Chae 2022 answering Milgrom's objection was found in this pass.

## 4. What is known against MI

### Takeaway
- **Theory:** there is no action-based relativistic MI, so there are no lensing, cosmology or gravitational-wave predictions. The equations are time-nonlocal and strongly nonlocal. Causality is unresolved, and so is a well-posed initial-value problem. Conservation laws hold only with nonlocal redefinitions.
- **Data:** Chae 2022's 6.9σ inner/outer RAR result and a preprint >5σ claim (both disputed by Milgrom) count against MI. On wide binaries, MI models predict a *stronger* EFE, i.e. a *smaller* anomaly than AQUAL/QUMOND. A Newtonian result such as Banik et al. 2024 is therefore less damaging to MI than to MG. A ~1.4–1.6 boost (Chae) is harder for MI with θ(0) > 1.

### Cited Findings
- **Nonlocality.** Galilei-invariant MI "must be strongly non-local". — [arXiv:astro-ph/9303012](https://arxiv.org/abs/astro-ph/9303012). Hees et al. 2014 call nonlocality "a serious drawback". — [arXiv:1402.6950](https://arxiv.org/abs/1402.6950)
- **Causality, uniqueness and initial values** (Milgrom 2022):
  - Causality "perhaps … can be modified to incorporate such a requirement. But to avoid complications, I assume that we are dealing with a closed system".
  - Whether positions and velocities at one time define a unique history is shown only for harmonic and constant force fields: "But is it the case in general? … we cannot be sure that there is a choice of I that satisfies it".
  - Uniqueness requires a0⁻¹I to be monotonic in a0.

  — [arXiv:2208.07073](https://arxiv.org/abs/2208.07073)
- **Conservation laws.** In the 2022 models, momentum, energy and angular momentum are conserved only with nonlocal, Fourier-defined quantities, with no action. — [arXiv:2208.07073](https://arxiv.org/abs/2208.07073). Shariati & Jafari recast MI as a non-conservative effective field and tidal force. — [arXiv:2111.04768](https://arxiv.org/abs/2111.04768)
- **Composite bodies.** Solved in the 2022 models only by requiring θ(ζ) → 0 fast enough at high frequency ratio. — [arXiv:2208.07073](https://arxiv.org/abs/2208.07073)
- **No relativistic version.** Milgrom 2006: comparing massive bodies with light rays needs "a relativistic version of MI". — [arXiv:astro-ph/0510117](https://arxiv.org/abs/astro-ph/0510117). Milgrom 2022 restricts itself to the non-relativistic limit. — [arXiv:2208.07073](https://arxiv.org/abs/2208.07073). Milgrom 2023 on gravitational waves: "In MI it is more natural for the path followed by gravitational waves (gravitons) to be the same as that for photons", which is asserted, not derived. — [arXiv:2310.14334](https://arxiv.org/abs/2310.14334). The only claimed relativistic extension (Demir & Karahan 2014) has no action. — [arXiv:1408.5787](https://arxiv.org/abs/1408.5787)
- **Stronger EFE for wide binaries — Milgrom's own claim.** MI models "predict possibly a stronger external-field effect – e.g. … very wide binary stars". AQUAL/QUMOND give η ≈ 1/μ(2) ≈ 1.5, i.e. velocities about 1.2× Newtonian, "However, if the correct argument value for µ is several times larger, the expected velocity anomaly is even smaller (e.g., only 8% if α = 3)". — [arXiv:2310.14334](https://arxiv.org/abs/2310.14334). Also "1 − µ[2θ(0)] can be rather smaller than 1 − µ(2)". — [arXiv:2208.07073](https://arxiv.org/abs/2208.07073)
- **Wide-binary data:**
  - **Banik et al. 2024, MNRAS 527, 4573.** 8611 wide binaries within 250 pc. α_grav = −0.021 (+0.065/−0.045), where 0 is Newton and 1 is MOND with the QUMOND EFE (about a 20% velocity excess). MOND is excluded at 16σ and Newton preferred at 19σ. "MOND must be substantially modified on small scales". The test is built on MG (QUMOND) dynamics. — [arXiv:2311.03436](https://arxiv.org/abs/2311.03436), [doi:10.1093/mnras/stad3393](https://doi.org/10.1093/mnras/stad3393)
  - **Banik et al. 2024 on MI** (Sec. 7, verified in the full text):
    - They acknowledge "It has been argued that modified inertia interpretations of MOND could reduce the predicted enhancement to the Newtonian acceleration and thus remain consistent with the WBT (Milgrom 1994, 2011, 2022)".
    - They counter with Chae 2022's 6.9σ inner/outer RAR difference: "a priori not expected in the modified inertia interpretation".
    - They concede: "until we have a fully fledged formulation of modified inertia theories capable of handling somewhat eccentric orbits, it is impossible to fully conclude on whether the results of Chae (2022) indeed rule out such theories."
    - In a simple-μ fit, the effective external field needed to make local wide binaries Newtonian enough is at least 7.8a0 (simple μ) or 4.6a0 (MLS μ), against an expected value of about 1.2a0. This is a 4–6× enhancement, in the same direction as Milgrom's θ(0) factor but larger than θ(0) ≈ 2–3.
  - [Inference] Matching Banik's Newtonian result inside MI would therefore need θ(0) ≳ 4–6. Their stated expected value of about 1.2a0 is their own effective number; I did not check it against the 2a0 Milgrom uses.
  - **Chae 2023, ApJ 952, 128** (erratum ApJ 956, 69). g_obs/g_pred = 1.43 ± 0.06 at g_N ≈ 10^−10.15 m s⁻², which "agrees with … AQUAL". — [arXiv:2305.04613](https://arxiv.org/abs/2305.04613), [doi:10.3847/1538-4357/ace101](https://doi.org/10.3847/1538-4357/ace101)
  - **Chae 2024a, ApJ 960, 114.** γ_g = 1.49 (+0.21/−0.19). — [arXiv:2309.10404](https://arxiv.org/abs/2309.10404), [doi:10.3847/1538-4357/ad0ed5](https://doi.org/10.3847/1538-4357/ad0ed5)
  - **Chae 2024b, ApJ 972, 186.** γ_g = 1.37 (+0.10/−0.09 stat, +0.16/−0.09 syst). Newton ruled out at 5.8σ; AQUAL acceptable. — [arXiv:2402.05720](https://arxiv.org/abs/2402.05720), [doi:10.3847/1538-4357/ad61e9](https://doi.org/10.3847/1538-4357/ad61e9)
  - **Chae et al. 2026 (preprint).** 36 wide binaries with accurate 3D velocities, γ ≈ 1.60 (+0.17/−0.14). — [arXiv:2601.21728](https://arxiv.org/abs/2601.21728)
  - **Saad & Ting 2026, OJAp 9.** Reanalyses the same 36 binaries with a hierarchical Bayesian 3D-orbit model and finds γ = 1.00 (+0.24/−0.19). The de-projection shortcut reproduces γ ≈ 1.56. — [arXiv:2603.11015](https://arxiv.org/abs/2603.11015), [doi:10.33232/001c.170182](https://doi.org/10.33232/001c.170182)
- **Park et al. 2026** state that Solar-System Q2 now constrains classical MG MOND more strongly than wide binaries do. — [arXiv:2602.17884](https://arxiv.org/abs/2602.17884)

### Inferences
- **[computed here]** Milgrom's dominant-EFE formula G_eff = G/μ(θ(0)·a_ex/a0), with a_ex = 2a0 and the simple μ(x) = x/(1+x), gives these velocity boosts (1/μ)^{1/2}:

  | θ(0) | velocity boost |
  |---|---|
  | 1 (MG-like) | 1.22 |
  | 2 | 1.12 |
  | e | 1.09 |
  | 3 | 1.08 (matches Milgrom's "8%") |

  The matching acceleration boosts γ_g are 1.5, 1.25, 1.18 and 1.17.
  - MI with θ(0) ≥ 2 is therefore *more* compatible with Newtonian-looking results (Banik 2024; Saad & Ting 2026), but sits below Chae's γ_g ≈ 1.37–1.6.
  - Rough scaling of Banik's α_grav: MI(θ=3) ≈ 0.38 on the 0–1 scale, still several σ from α_grav = −0.02 (+0.065/−0.045). This is my extrapolation, not a published MI fit. Banik's model uses the full QUMOND radial profile, not a constant G_eff.
- **Net:** no wide-binary analysis has fitted an MI model. The wide-binary data are currently internally contested (Chae vs Banik vs Saad & Ting), so they do not yet decide MI.

### Gaps
- I found no paper that confronts Gaia wide binaries with an explicit MI model, including Milgrom's θ-EFE.
- I did not search Banik & Zhao 2022 (Symmetry 14, 1331; [arXiv:2110.06936](https://arxiv.org/abs/2110.06936), [doi:10.3390/sym14071331](https://doi.org/10.3390/sym14071331)) or Famaey & McGaugh 2012 (LRR 15, 10; [arXiv:1112.3960](https://arxiv.org/abs/1112.3960)) for their MI paragraphs in this pass.

## 5. Concrete, computable tests an MI model would face

### Takeaway
Fixing a specific MI model (μ, θ1, θ2, K) turns its predictions into a short list of computable tests.

### Cited Findings
1. **Inner-planet 1−μ tail.** Precession and constant-anomaly bounds (Chan & Lee 2023; Sereno & Jetzer 2006) with the chosen μ at x ~ 10⁵–10⁸. Q2 is not the test for MI. — [arXiv:2212.01019](https://arxiv.org/abs/2212.01019); [arXiv:astro-ph/0606197](https://arxiv.org/abs/astro-ph/0606197); [arXiv:2310.14334](https://arxiv.org/abs/2310.14334)
2. **Wide-binary EFE strength.** Predict γ_g = 1/μ̄(θ1(0)·2a0/a0, θ2(0)·e-term) for Galactic-orbit inputs, then forward-model it against the Gaia DR3 samples:
   - Banik 2024 — [arXiv:2311.03436](https://arxiv.org/abs/2311.03436)
   - Chae 2024 — [arXiv:2402.05720](https://arxiv.org/abs/2402.05720)
   - Saad & Ting 2026 — [arXiv:2603.11015](https://arxiv.org/abs/2603.11015)

   Needed: θ1(0), θ2(0), and the Sun's orbital acceleration and eccentricity. — [arXiv:2208.07073](https://arxiv.org/abs/2208.07073)
3. **Non-circular RAR corrections and tracer dependence.**
   - Eq. 47 needs per-galaxy vertical accelerations a_z, ωz/ω, and stars-vs-gas dispersions. — [arXiv:2310.14334](https://arxiv.org/abs/2310.14334)
   - Redo the Chae 2022 inner/outer test — [arXiv:2207.11069](https://arxiv.org/abs/2207.11069) — and the Q test — [arXiv:2001.03348](https://arxiv.org/abs/2001.03348).
4. **Vertical disc dynamics.** Milky Way disc scale heights and dispersions with μ(θ1(0)·ω²R/a0). — [arXiv:2310.14334](https://arxiv.org/abs/2310.14334)
5. **Long-period comets, the Oort cloud and extreme TNOs.** Eccentric orbits reaching beyond r_M ≈ 7000 AU, which MI predicts can carry anomalies of order a0 into the inner Solar System. This requires solving the nonlocal equations on such orbits; no published numbers exist. — [arXiv:0906.4817](https://arxiv.org/abs/0906.4817); [arXiv:1111.1611](https://arxiv.org/abs/1111.1611)
6. **Laboratory and space tests:**
   - Equinox SHLEM displacement of about 1e-14 m. — [arXiv:0802.1599](https://arxiv.org/abs/0802.1599)
   - Free-fall laboratory tests that could distinguish MI from MG. — Das & Patitsas 2013, PRD 87, 107101, [arXiv:1305.6633](https://arxiv.org/abs/1305.6633)
   - Saddle-point station-keeping: an anomaly only in MG. — [arXiv:2310.14334](https://arxiv.org/abs/2310.14334)
7. **Satellites and globular clusters on eccentric orbits** (EFE set at perigalacticon) and **isolated binary galaxies**: the deep-MOND two-body coefficient is 2 vs 0.61. — [arXiv:1111.1611](https://arxiv.org/abs/1111.1611); [arXiv:2310.14334](https://arxiv.org/abs/2310.14334)

### Inferences
- For Res-Nova, the cheapest decisive pair of checks:
  - Is the μ tail of the chosen SPARC-fitting family Newtonian enough at planetary x? ν_1 fails; exponential families pass.
  - What does the MI wide-binary γ_g look like for plausible θ(0) ∈ [1, 3]?
- An MI version of our SPARC fit passes Cassini essentially by construction. It then has to survive the contested wide-binary data and the inner-RAR tests, which are not yet redone for non-circular motion.

### Gaps
- No published numeric MI predictions for Oort-cloud or comet anomalies, MI lensing or MI cosmology.
