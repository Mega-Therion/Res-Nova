# Res Nova / G.O.D. / ITT — foundations audit (2026-11-13)

**Purpose.** This is a dated, review-only audit of the current mathematical and physical foundations. It does not replace `CURRENT_STATE_READ_THIS_FIRST.md`, rewrite the frozen Euclid prediction record, or declare a new physical model accepted. It separates (i) statements that are mathematically proved, (ii) statements imported from established physics, (iii) model assumptions, and (iv) open physical bridges.

**Bottom line.** There are real mathematical results in the repository, but the current material does not yet constitute one closed covariant theory. The highest-priority work is to specify one field content and one action, derive its equations and conserved currents, and connect its internal geometry to a genuine four-dimensional chiral index. The current three-generation claim is not established by the existing Lean generation modules.

## 1. Epistemic rules for this audit

- A Lean theorem proves its formal statement. It proves a physical claim only if its definitions encode the relevant physical structures and the assumptions are physically justified.
- A named action or Lagrangian is not a derived action merely because its terms can be written down. The field spaces, units, symmetries, boundary terms, matter coupling, and variation must all be specified.
- A group branching multiplicity is not a chiral index. A dimension-three multiplicity is not, on its own, three unpaired four-dimensional fermion generations.
- A necessary phenomenological condition may reject a model, but imposing that condition as an axiom does not derive the model's constitutive law from first principles.

## 2. E8, triality, and the three-generation claim

### 2.1 What the group theory does establish

The standard branching
[
\mathbf{248}_{E_8}
=(\mathbf{78},\mathbf 1)
+(\mathbf 1,\mathbf 8)
+(\mathbf{27},\mathbf 3)
+(\overline{\mathbf{27}},\overline{\mathbf 3})
]
under (E_8\supset E_6\times SU(3)) is a valid representation-theoretic decomposition. It exhibits a triplet factor, but the adjoint contains the conjugate partner as well. This decomposition alone does not yield a net chiral four-dimensional spectrum.

Likewise, (\operatorname{Out}(\operatorname{Spin}(8))\cong S_3) is standard Cartan triality. The physical statement that this outer automorphism produces exactly three chiral fermion families requires additional structure: a specified action on the actual fermion bundle/zero-mode space, a chiral projection, and an index or equivalent zero-mode calculation.

The current `05_lean_formalization/CartanTrialityGenerations.lean` expressly retracts the earlier claim that it machine-proved three physical generations. It states that the file does not construct Spin(8), its outer automorphism group, representations, a Stiefel frame, a Berry phase, or a fermion-generation type. Its remaining results are a hand-set value 3 and generic arithmetic. Thus the mathematical fact of triality remains available; the claimed physical generation derivation does not.

The same distinction applies to (V_2(\mathbb R^3)\cong SO(3)): this is a legitimate geometric identification for orthonormal two-frames in three dimensions. It does not by itself construct an action of Spin(8) triality on that space, nor a map from its modes to the observed chiral fermion spectrum. That map remains an explicit obligation.

### 2.2 The two current generation-index files

The live `05_lean_formalization/GenerationIndex.lean` has an unusually clear in-file correction. It explicitly identifies its two statements as vacuous literal arithmetic:

- `z3NetChirality_takes_defined_literals_VACUOUS_D47` proves that a function whose branches were defined to return (0,3,-3) returns one of those values. The substitution probe replacing the literals by arbitrary alternatives leaves the proof shape intact.
- `mckayArrowsPerNode_eq_three_DEFINITIONAL_PLACEHOLDER` proves a hand-entered (3=3). It does not construct a McKay quiver.

The separate `05_lean_formalization/DiagonalConeIndex.lean` contains one genuine finite-combinatorics theorem:
[
( a+b+c\equiv0\pmod 3)\quad\text{and}\quad
a,b,c\ne0
\quad\Longrightarrow\quad
(a,b,c)=(1,1,1)\;\text{or}\;(2,2,2),
]
for (a,b,c\in\mathbb Z_3). This is a valid exhaustive result over 27 triples.

But that file defines `net` by a case table that already assigns (-3) to ((1,1,1)), (+3) to ((2,2,2)), and (0) otherwise. Its `QuantizationTheorem`, `IsolatedGivesThree`, and `AbsNetThree` then prove properties of that stipulated function. They do not derive the table from a Dirac operator, a Lefschetz fixed-point formula, a D-brane quiver constructed in the model, or a physical bundle. The `CenterLadder` and Coxeter-number entries in this file are also declared as literals and proved by computation/reflexivity; the independent root-system calculation is external to the Lean proof.

**Retain:** the finite theorem `DiagonalForced`, clearly labeled as local (\mathbb C^3/\mathbb Z_3) combinatorics.

**Do not claim yet:** that the theorem derives the Standard Model family count, that the current substrate selects its isolated premise, or that the `net` case table is a physical index computation.

### 2.3 A correction to the archived SO(10) anomaly argument

The July 2026 E8 Stiefel index notes claim that an SO(10) spinor (mathbf{16}) has a nonzero cubic gauge anomaly, while E6 representations do not, and use this to prefer the SO(10) route. This is incorrect.

The four-dimensional local non-Abelian cubic anomaly is governed by the symmetric tensor
[
D_R^{abc}=\operatorname{tr}_R\!\left(T^{(a}T^bT^{c)}\right).
]
Among compact simple Lie algebras, the relevant independent cubic invariant occurs for (\mathfrak{su}(N)), (N\ge3). Complex representations of E6 still have zero such tensor; SO(10) likewise has no independent cubic invariant. The fact that the SO(10) (mathbf{16}) is a complex chiral representation does **not** make its (SO(10)^3) perturbative anomaly nonzero. Anomaly cancellation and chiral generation counting are different questions.

This correction is supported by Bilal's graduate-level review, *Lectures on Anomalies*, arXiv:0802.0634, and the trace-tensor classification summarized in the reference below. The archived claim “(A(16)=+1) for SO(10)” must not be used.

### 2.4 A legitimate, but not yet model-specific, route to three generations

A standard heterotic compactification provides a genuine index-theoretic route. For a six-dimensional Calabi–Yau threefold (X) with a stable holomorphic (SU(n)) bundle (V) embedded in the visible (E_8), the net chiral generation number is
[
N_{\rm gen}(V)=\frac12\int_X c_3(V)
]
(up to the orientation/chirality sign convention). Three net generations require
[
\int_X c_3(V)=\pm6.
]
The construction must also satisfy the heterotic Bianchi/anomaly constraint, conventionally written
[
c_2(TX)=c_2(V)+W,
]
where (W) accounts for the five-brane class or hidden-sector contribution.

This is a real route to investigate, not a result of Res Nova. The current theory has not specified the required (X), stable bundle (V), embedding, cohomology classes, or resulting four-dimensional zero modes. The former (V_{240}(\mathbb R^{57600})) construction is retired. Its 239-sphere APS proposal is not a six-dimensional Calabi–Yau compactification: a 240-dimensional index calculation uses the degree-240 part of its index density, not a six-form (\mathrm{ch}_3) transplanted from a six-dimensional internal space. No physical dimensional reduction bridges that old construction to four-dimensional fermions.

**Generation gate:** derive the physical chiral index from a current internal geometry and a specified fermion/gauge bundle, or demote the three-generation statement to a conjecture. Do not splice the retired (V_{240}) index into the current (V_2(\mathbb R^3)) geometry without a new construction.

## 3. Information tension, the interpolation law, and the Hamilgrangian

### 3.1 Current and historical branches must remain separate

The current galaxy-domain constitutive function is
[
\mu_{\rm std}(x)=\frac{x}{\sqrt{1+x^2}},
\qquad
F_{\rm std}(x)=\frac12\left[x\sqrt{1+x^2}-\operatorname{arsinh}x\right],
]
with the exact scalar identity (F'_{\rm std}(x)=x\mu_{\rm std}(x)). The identity is a proved calculus result for the defined functions.

The older Hamilgrangian file uses
[
F_{\rm dual}(x)=\frac12x^2-x+\ln(1+x),
\qquad
\mu_{\rm dual}(x)=\frac{x}{1+x}.
]
Its algebraic identities do not make this the current live galaxy law. The (mu_{\rm dual}) branch has been rejected for the solar-system extension because its Newtonian tail falls as (1/x), leaving too large a residual. Keep the old derivation as historical mathematics, not as the current constitutive law.

### 3.2 What the (mu_{\rm std}) uniqueness work actually assumes

`MuStdUniqueness.lean` explicitly labels the inputs that are not derived:
1. Postulate R, the rapidity-conjugacy condition (dF/d\psi=x^2);
2. the physical interpretation of the chiral coordinate;
3. the normalization (mu'(0)=1);
4. it drops the older additive (F=F_{\rm Newton}-F_{\rm correction}) split, which is incompatible with (F_{\rm std}).

The file itself states that Theorem A (rapidity conjugacy) and Theorem B (the chiral Fisher identity) are the same postulate in two forms, not independent corroborations. The resulting uniqueness theorem is conditional. It is not a derivation of (mu_{\rm std}) from a complete covariant ITT action.

`MuStdSelection.lean` adds the inverse-square tail condition
[
\exists C>0\;\forall x\ge1:\quad 1-\mu(x)\le C/x^2.
]
It proves (mu_{\rm std}) satisfies this condition and (mu_{\rm dual}) does not. This is useful conditional mathematics. But `ScreenedTail` is explicitly a postulate motivated by solar-system bounds, and the global theorem `screening_selects_mu_std` additionally assumes a uniform branch choice. The pointwise A4 disjunction alone yields only eventual selection at high (x), not a global derivation.

The current state ledger is therefore correct to classify (mu_{\rm std}) as an axiom/constitutive input on the galaxy domain until the physical action and its variation produce it.

### 3.3 The (2\pi) in (a_0) is not obtained by the current thermal argument

`HorizonScale.lean` defines
[
T_{\rm GH}=\frac{\hbar H}{2\pi k_B},
\qquad
T_U=\frac{\hbar a}{2\pi c k_B}.
]
Its theorem `kms_cancellation_equilibrium` proves
[
T_U=T_{\rm GH}\quad\Longleftrightarrow\quad a=cH.
]
The (2\pi) factors cancel. Its theorem `two_pi_divisor_not_derived` further proves, under the same assumptions and positive (c,H), that (a\ne cH/(2\pi)).

Thus the thermal-equality argument supports (a=cH), not (a_0=cH_0/(2\pi)). The latter may remain a phenomenological relation or follow from a different physical mechanism, but that mechanism has not been derived in this proof. The extra (1/(2\pi)) must be named as an independent input until derived. Do not use a sorry-free Lean build to upgrade that input into a physical result.

## 4. Covariant action and Noether structure

The repository's current equation inventory (`MasterEquationTerms.csv`) usefully distinguishes definitions, model assumptions, and open obligations. It explicitly says the AQUAL PDE is a model assumption whose variation/boundary terms are not established, and the candidate covariant terms still need a consistent field definition, units, symmetries, and variation.

`TARGET_D7_COVARIANT_COMPLETION.md` cites the Skordis–Złośnik AeST action as the current relativistic scaffold and retracts the earlier generalized-Einstein-aether/disformal action. That is an imported framework, not an ITT derivation. The free function, scalar cosmology sector, galaxy scalar sector, parameters, screening, and matter coupling must be one internally consistent model; a separately postulated (mu_{\rm std}) law cannot simply be attached to an unrelated scalar action.

A valid action package must include, at minimum:
- spacetime signature, curvature convention, coordinate and field dimensions;
- all dynamical fields, configuration spaces, gauge redundancies, and transformation rules;
- a single scalar density with dimensions ([L^{-4}]) in natural units, or an explicitly stated SI convention;
- boundary terms and allowed variations;
- matter coupling and the physical metric;
- Euler–Lagrange equations, constraints, and stress-energy tensor from metric variation;
- Noether identities/currents for each declared global symmetry, and gauge constraints for each gauged symmetry;
- linearized degrees of freedom, ghost/gradient stability, characteristic cones, and causal propagation.

A Noether claim must state whether E8 is global, gauged, or only a geometric organizing group. An exact global continuous E8 symmetry of a specified local action would give currents conditionally; gauged E8 gives gauge identities and constraints, not 248 independent observable global charges. The 240 roots are not themselves Noether charges.

## 5. The frozen Euclid record

Keep DOI 10.5281/zenodo.24109539 untouched as the dated prediction record. The existing audit identifies unresolved reproducibility issues (including the S/N scaling prose and response/weighting choices) and notes that the November 2026 Euclid DR1 Foundation release does not yet contain the full high-level weak-lensing products needed for the advertised shear test; those are expected with the Complete release in 2027. The failed triangulation gate remains a failed gate. A later corrected version must preserve the original forecast and show what changed; it must not retroactively rewrite the frozen prediction.

## 6. Required closure order

The following order avoids deriving phenomenology from a model whose fields or action are still undefined.

1. **Canonical model identity.** Publish a versioned manifest naming the spacetime, internal geometry, gauge group, physical fields, matter metric, units, symmetry group, and the boundary between established framework and novel hypotheses. Resolve the present conflict between the four-block current front page and the requested single flagship synthesis.
2. **Geometry-to-spectrum bridge.** Choose one current route: (a) construct the (V_2(\mathbb R^3))/triality action on actual bundles and modes, or (b) specify a heterotic (X,V) compactification and compute its index. No mixing with the retired (V_{240}) substrate. The output must be the full four-dimensional chiral spectrum and anomaly checks, not just a multiplicity.
3. **One covariant action.** Write the complete action and fix all units, fields, symmetries, matter coupling, and boundary terms. Derive the equations, stress-energy, Noether identities, and constraints from it.
4. **Constitutive law and horizon scale.** Derive (mu(x)), its asymptotic tails, screening, and (a_0) from that same action or label each as a separate measured/model input. Prove that the same branch works in galaxy, Solar System, binary, and cosmological regimes without patching.
5. **Consistency gates.** Calculate tensor/scalar/vector modes, stability, positivity, characteristic cones, PPN parameters, gravitational-wave speed, cosmological perturbations, and conservation/free-fall identities.
6. **Phenomenology.** Only then make new, versioned predictions with frozen inputs, public code/data, blind or hold-out targets, look-elsewhere control, and an independent reproduction path.
7. **Formal verification.** Formalize the already-defined objects and theorem hypotheses. Bind each Lean theorem to a specific equation and physical claim; add substitutability/sabotage tests so a proof cannot pass after changing the claimed physics literals.

## 7. Immediate open questions (do not answer by assumption)

- Is E8×E8 the actual heterotic gauge group, a four-dimensional global symmetry, or a geometric scaffold only?
- What is the current internal space (X) or equivalent compactification object, and what fermion bundle/operator lives on it?
- Where is the explicit map from Cartan triality on Spin(8) to the current (V_2(\mathbb R^3)) geometry and then to four-dimensional chiral zero modes?
- What single action yields the observed galaxy interpolation while remaining consistent with the Solar System and the AeST/cosmological sector?
- What independent mechanism, if any, yields the (1/(2\pi)) in (a_0)?
- What is the dynamical selection rule for the sign/orientation of the chiral spectrum?

## References and source files

- Bilal, *Lectures on Anomalies*, arXiv:0802.0634: https://arxiv.org/abs/0802.0634
- Andreas & Curio, *On possible Chern Classes of stable Bundles on Calabi–Yau threefolds*, arXiv:1010.1644: https://arxiv.org/abs/1010.1644
- Current Res-Nova `GenerationIndex.lean`: https://github.com/Mega-Therion/Res-Nova/blob/main/05_lean_formalization/GenerationIndex.lean
- Current Res-Nova `DiagonalConeIndex.lean`: https://github.com/Mega-Therion/Res-Nova/blob/main/05_lean_formalization/DiagonalConeIndex.lean
- Current Res-Nova `CartanTrialityGenerations.lean`: https://github.com/Mega-Therion/Res-Nova/blob/main/05_lean_formalization/CartanTrialityGenerations.lean
- Current `HorizonScale.lean`: https://github.com/Mega-Therion/Res-Nova/blob/main/05_lean_formalization/HorizonScale.lean
- Current `MuStdUniqueness.lean`: https://github.com/Mega-Therion/Res-Nova/blob/main/05_lean_formalization/MuStdUniqueness.lean
- Current `MuStdSelection.lean`: https://github.com/Mega-Therion/Res-Nova/blob/main/05_lean_formalization/MuStdSelection.lean
- Current `TARGET_D7_COVARIANT_COMPLETION.md`: https://github.com/Mega-Therion/Res-Nova/blob/main/TARGET_D7_COVARIANT_COMPLETION.md
- Current `MasterEquationTerms.csv`: https://github.com/Mega-Therion/Res-Nova/blob/main/MasterEquationTerms.csv

**Status:** audit only. No existing claim, prediction, branch, or published record has been deleted or edited. The next physical milestone is the canonical model identity and the geometry-to-four-dimensional-spectrum bridge.