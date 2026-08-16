# Cover Letter — Physical Review D

**To:** The Editors, Physical Review D
**Section:** Gravitation and Cosmology (Modified gravity / alternatives to dark matter)
**Manuscript:** *Dual-Channel Variational Closure, Covariant Completion, and a Reproducible SPARC Benchmark*
**Author:** Ryan W. Yett (independent researcher; ORCID 0009-0001-1303-7190)

---

Dear Editors,

I submit for your consideration the manuscript *Dual-Channel Variational Closure, Covariant Completion, and a Reproducible SPARC Benchmark*.

The paper studies a specific AQUAL-family action, F_dual(x) = ½x² − x + ln(1+x), whose constitutive ratio is the "simple" interpolation function μ(x) = x/(1+x), and carries it through to a relativistic completion with quantitative solar-system and cosmological consequences. Four results seem to me to warrant the attention of PRD's readership.

**1. A conditional uniqueness theorem for the action.** Correspondence limits alone do not select an interpolation function. I prove that, given constitutive-relation structure, Padé[1/1] minimality, the MOND boundary conditions, and dual-channel splitting, F_dual is uniquely determined. μ is exactly the inverse of the Bayesian odds ratio, and the action satisfies the identity F'(x)²·I(μ(x)) = x³ with I the Bernoulli Fisher information. I state plainly what is *not* proved: the necessity of the Padé constraint is not derived, so this is conditional uniqueness, and it relocates rather than removes the functional freedom.

**2. A screening mechanism that resolves two separate tensions with one structure.** Specifying the Skordis–Złośnik free function as F(K) = F_dual(√K) leaves the Friedmann background unmodified and places the cosmological background on the Newtonian branch. The resulting linear screening ratio F''/F' ≈ 0.004 reduces the ~76× structure overproduction of a uniform MOND enhancement to a 0.4% enhancement of linear growth. Combined with Vainshtein suppression, the same structure yields a solar-system quadrupole Q₂ ≈ 4.9 × 10⁻²⁹ s⁻², a factor of 70 below the Cassini bound recently reported by Park, Hees, Famaey, Desmond and Durakovic — at natural O(1) couplings, with no fine-tuning.

**3. A falsifiable prediction, not a consistency check.** The framework predicts a residual external-field quadrupole Q₂ ~ 10⁻²⁹ s⁻², roughly two orders of magnitude below present sensitivity and within reach of next-generation ranging. A measurement establishing |Q₂| ≲ 10⁻³⁰ s⁻² would place the theory under serious pressure.

**4. A pre-registered test that came out against the author's prior hypothesis.** I pre-registered a comparison of constant a₀ against a horizon-tied a₀(z) = ξcH(z) before evaluating the data. The result favours constant a₀ at 5.9σ. The horizon interpretation of the acceleration scale was the more attractive hypothesis for this program, and I report it as disfavoured. The manuscript scores that target as open accordingly.

**On reproducibility.** All data, analysis scripts, and verification manifests are public. The formal core is machine-checked: 17 Lean 4 modules, no `sorry`, axioms restricted to {propext, Classical.choice, Quot.sound}. Section 11 states the limits of that verification explicitly — Lean certifies that statements follow from their encoded definitions, and several modules declare assumptions rather than derive them. I have flagged each such module in the source inventory table rather than let the module count stand as an unqualified claim.

**On scope.** I have tried to be exact about what this work does not establish. Non-linear structure formation requires N-body simulation that has not been run; the linear CMB agreement is inherited from Skordis–Złośnik rather than recomputed with F_dual; exact PPN γ and β await the post-Newtonian expansion; cluster scales are untested. These are itemized as open problems O1–O9 rather than deferred to a closing paragraph.

This manuscript is not under consideration elsewhere, and it has not been published previously. I have no competing interests and no external funding to declare. AI tools assisted with drafting and code review under my direction and audit; this is stated in the manuscript's declarations.

I would be glad to suggest referees with expertise in relativistic MOND and solar-system tests of gravity if that would assist.

Thank you for your consideration.

Sincerely,
Ryan W. Yett
Independent Theoretical Research
ORCID 0009-0001-1303-7190
