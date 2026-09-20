# Cover Letter — Physical Review D

**To:** The Editors, Physical Review D
**Section:** Gravitation and Cosmology (Modified gravity / alternatives to dark matter)
**Manuscript:** *Dual-Channel Variational Closure, Covariant Completion, and a Reproducible SPARC Benchmark*
**Author:** R.W. Yett (independent researcher; ORCID 0009-0001-1303-7190)

---

> **SUBMISSION REVISION NOTE (2026-09-20 · v1.9.0):**
> This cover letter documents the original submission under $\mu_{\text{dual}}(x) = x/(1+x)$.
> Following the repository's internal audits on 2026-09-12 and 2026-09-20:
> 1. $\mu_{\text{dual}}$ produced an unscreened solar-system anomalous acceleration ($10^3\times$ Cassini bound) and was **falsified [X]**; the manuscript and theory are rebuilt on $\mu_{\text{std}}(x) = x/\sqrt{1+x^2}$ where the $1/(2x^2)$ tail satisfies the solar-system bounds. The binding constraint is planetary perihelion precession, giving $\lambda_s \lesssim 2.2$; an earlier $\lambda_s \lesssim 1.0$ is **withdrawn** (it required a 0.10 mas/cy ceiling, tighter than the INPOP10a 1$\sigma$ of 0.65 and than its central value of 0.15). The Cassini $Q_2$ comparison gives $\lambda_s \lesssim 2.7$ but is a magnitude heuristic only — it reads an isotropic monopole residual against an anisotropic quadrupole datum.
> 2. The $5.9\sigma$ preference for constant $a_0$ is **retracted [X]** as closure-sensitive; the pre-registered intermediate-$z$ test under $\mu_{\text{std}}$ is inconclusive ($\Delta\chi^2 = +4.24$, $2.06\sigma$), leaving $a_0(z)$ open.
> 3. The formal Lean 4 verification suite has expanded from 17 to 28 core manuscript modules (58 total gated monorepo modules), all verified with 0 sorry.

Dear Editors,

I submit for your consideration the manuscript *Dual-Channel Variational Closure, Covariant Completion, and a Reproducible SPARC Benchmark*.

The paper studies a specific AQUAL-family action and carries it through to a relativistic completion with quantitative solar-system and cosmological consequences. The version submitted here is built on $\mu_{\text{std}}(x) = x/\sqrt{1+x^2}$ with $F_{\text{std}}(x) = \tfrac12\!\left[x\sqrt{1+x^2} - \operatorname{arsinh} x\right]$; the earlier dual-channel branch is retracted for the reason given above. Four results seem to me to warrant the attention of PRD's readership.

**1. A structural selection of the interpolation function.** Correspondence limits alone do not select an interpolation function. Under $\mu_{\text{std}}$ the selection runs through a rapidity conjugacy — $\mu_{\text{std}}(\sinh\psi) = \tanh\psi$, so the constitutive relation is the hyperbolic tangent of the rapidity — together with a chiral Fisher-information identity that fixes the exponent. Both are machine-checked. I state plainly what this is and is not: it is a postulate swap, not a derivation from nothing. The functional freedom has been relocated into the conjugacy postulate rather than eliminated, and I say so in the text rather than claiming uniqueness.

A separate result closes a gap that the axiom system left open. The framework's variational closure admitted either $x/(1+x)$ or $x/\sqrt{1+x^2}$. I prove that an inverse-square approach to the Newtonian limit — the formal content of a solar-system screening bound — is satisfied by $\mu_{\text{std}}$ and cannot be satisfied by $x/(1+x)$ for any constant, so the disjunction collapses. The dead branch is now excluded inside the formal system rather than by editorial note.

**2. Solar-system consequences, with the binding constraint identified.** $\gamma_{\text{PPN}} = 1$ is *derived* rather than fitted, and free-function-independently: every source of traceless anisotropic stress enters at $O(\varepsilon^2)$, so $\Phi = \Psi$ exactly and lensing returns GR's $4G_N M/bc^2$ with no slip. The free-function dependence of $\beta$ is bounded by $\varepsilon_J = 1/(1+x^2) \lesssim 10^{-17}$ at planetary gradients.

The interesting feature is which datum binds. The residual acceleration $\delta g = (1+\lambda_s)^3 a_0^2 r^2 / 2G_NM$ *grows* as $r^2$, so the constraint tightens outward: Mercury, conventionally the sharpest solar-system test, is the weakest point here, and Saturn is the strongest. Applying Gauss's perturbation equations to an isotropic $r^2$ perturbation gives an orbit-averaged precession $\dot\varpi = (1+\lambda_s)^3 a_0^2 r^{5/2}/(G_NM)^{3/2}$, which against the Cassini limit on Saturn's anomalous precession yields $\lambda_s \lesssim 2.2$ — the first upper bound on this parameter in the programme. The monotonicity is machine-checked, not asserted.

I should be explicit that $\alpha_1$ and $\alpha_2$ remain open, with a named obstruction: the Foster–Jacobson formulas are inapplicable at this theory's couplings, since the $c_{123} = 0$ Maxwell locus sends the spin-0 aether speed to zero, and no static spherical solution can determine them in any case.

**3. A cosmological sector that shields the CMB structurally.** On an FLRW background the spatial gradient scalar vanishes identically, so the MOND function and $a_0$ drop out of linear cosmology and what remains is a shift-symmetric $K(Q)$ sector. The minimal quadratic choice fails: its adiabatic sound speed rises monotonically toward $c$, against a requirement of $c_{\text{ad}}^2 \lesssim 0.02$ at recombination. The Skordis–Złośnik Cosh completion does not fail, and the reason is structural rather than tuned — the sound speed is exactly $c_{\text{ad}}^2 = r\tanh Z/(1 + rZ)$ with $r$ the width ratio, bounded above by $r$ at every redshift. The curvature at the minimum carries no width parameter, so the quasistatic mass is untouched by whatever early-time width the CMB requires. Both statements are machine-checked.

**4. A pre-registered test that came out inconclusive, reported as such.** I pre-registered a comparison of constant $a_0$ against a horizon-tied $a_0(z) = \xi cH(z)$ before evaluating the data. An earlier analysis reported $5.9\sigma$ in favour of constant $a_0$; that result was closure-sensitive and is **retracted**. Under the live $\mu_{\text{std}}$ closure the same test is inconclusive: $\Delta\chi^2 = +4.24$, $2.06\sigma$, which excludes neither reading. The horizon interpretation was the more attractive hypothesis for this programme and I would have preferred to report it settled in either direction; it is not, and the manuscript scores the target as open.

**On reproducibility.** All data, analysis scripts, and verification manifests are public. The formal core is machine-checked: 28 core manuscript modules within 58 gated monorepo roots, no `sorry`, axioms restricted to {propext, Classical.choice, Quot.sound}. Section 11 states the limits of that verification explicitly — Lean certifies that statements follow from their encoded definitions, and several modules declare assumptions rather than derive them. I have flagged each such module in the source inventory table rather than let the module count stand as an unqualified claim. A per-module grounding ledger records, for each one, what its symbols are claimed to denote physically, which observable it touches, and what measurement would falsify it — including the modules whose honest answer is "none", because they quantify over $\mathbb{R}$ rather than over a manifold or operator.

**On scope.** I have tried to be exact about what this work does not establish. Non-linear structure formation requires N-body simulation that has not been run; the linear CMB agreement is inherited from Skordis–Złośnik rather than recomputed with $F_{\text{std}}$; $\alpha_1$ and $\alpha_2$ await a treatment that does not rest on the inapplicable Foster–Jacobson formulas; cluster scales are untested. These are itemized as open problems O1–O9 rather than deferred to a closing paragraph.

This manuscript is not under consideration elsewhere, and it has not been published previously. I have no competing interests and no external funding to declare. AI tools assisted with drafting and code review under my direction and audit; this is stated in the manuscript's declarations.

**Suggested referees.** I have no personal or professional connection to any of the following, and none has seen this work:

1. **Constantinos Skordis** (CEICO, Institute of Physics, Czech Academy of Sciences) — co-author of the RMOND framework this paper specifies a free function for; best placed to judge whether the embedding and the screening argument are correct.
2. **Tom Złośnik** (University of Gdańsk) — the other RMOND author, and a co-author of the structure-formation equations the cosmological section relies on.
3. **Aurélien Hees** (LTE, Observatoire de Paris) — co-author of the Cassini Q₂ constraint that the solar-system section addresses directly; best placed to assess the Vainshtein estimate and the Q₂ prediction.
4. **Indranil Banik** (University of St Andrews) — works on MOND cosmology and N-body structure formation; well placed to judge the linear-growth argument and the limits I claim for it.

I would understand if the editors prefer referees at greater remove from the cited work.

Thank you for your consideration.

Sincerely,
R.W. Yett
Independent Theoretical Research
ORCID 0009-0001-1303-7190
