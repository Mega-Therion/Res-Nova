# AeST covariant variation audit: vector-sector coefficient discrepancy

**Date:** 2026-11-17  
**Scope:** Independent bulk variation of the live Skordis–Złośnik AeST action in one declared field basis; scalar, vector, multiplier, metric-variation structure, boundary terms, and the diffeomorphism identity.  
**Status:** Partial independent derivation. The scalar and multiplier equations are derived directly. A factor-of-two discrepancy is isolated between the action and the published vector equation. The metric equation is expressed as a compact Palatini variation formula; its fully expanded term-by-term match and the complete boundary prescription remain open.  
**No branch or physical model choice is promoted.**

## 1. Pinned action and conventions

Use signature \((-+++)\), \(c_{\rm light}=1\), Levi-Civita connection, and define
\[
b:=2-K_B,\qquad p_\mu:=\nabla_\mu\phi.
\]
The action under audit is the live D7 action (Skordis–Złośnik 2021, Eq. (5)):
\[
S=\frac{1}{16\pi\widetilde G}\int d^4x\sqrt{-g}\,\mathscr L_g+S_m[g,\psi],
\]
\[
\mathscr L_g=R-\frac{K_B}{2}F_{\mu\nu}F^{\mu\nu}
+2b\,J^\mu p_\mu-b\,\mathcal Y-\mathcal F(\mathcal Y,\mathcal Q)
-\lambda(A^\mu A_\mu+1),
\]
with
\[
F_{\mu\nu}=2\nabla_{[\mu}A_{\nu]},\quad
J_\mu=A^\alpha\nabla_\alpha A_\mu,\quad
A^\mu=g^{\mu\nu}A_\nu,
\]
\[
\mathcal Q=A^\mu p_\mu,\qquad
q^{\mu\nu}=g^{\mu\nu}+A^\mu A^\nu,\qquad
\mathcal Y=q^{\mu\nu}p_\mu p_\nu.
\]
Matter is minimally coupled to \(g_{\mu\nu}\). The old generalized-Einstein-aether/disformal branch is excluded.

For the primary derivation below, the independent fields are
\[
(g^{\mu\nu},\,A_\mu,\,\phi,\,\lambda).
\]
Write \(\mathcal F_{\mathcal Y}=\partial\mathcal F/\partial\mathcal Y\) and \(\mathcal F_{\mathcal Q}=\partial\mathcal F/\partial\mathcal Q\).

## 2. Scalar variation — direct derivation [D]

At fixed \(g_{\mu\nu}\) and \(A_\mu\),
\[
\delta_\phi\mathcal Q=A^\mu\nabla_\mu\delta\phi,\qquad
\delta_\phi\mathcal Y=2q^{\mu\nu}p_\nu\nabla_\mu\delta\phi.
\]
Therefore
\[
\delta_\phi\mathscr L_g=P^\mu\nabla_\mu\delta\phi,
\quad
P^\mu=2bJ^\mu-2(b+\mathcal F_{\mathcal Y})q^{\mu\nu}p_\nu
-\mathcal F_{\mathcal Q}A^\mu.
\]
After integration by parts, the scalar equation is
\[
\nabla_\mu(\mathcal F_{\mathcal Q}A^\mu)-2b\nabla_\mu J^\mu
+2\nabla_\mu\!\left[(b+\mathcal F_{\mathcal Y})q^{\mu\nu}p_\nu\right]=0.
\]
Using \(q^{\mu\nu}p_\nu=p^\mu+\mathcal Q A^\mu\), this becomes
\[
\nabla_\mu(\mathcal F_{\mathcal Q}A^\mu)-2b\nabla_\mu J^\mu
+2\nabla_\mu\!\left[\mathcal Q(b+\mathcal F_{\mathcal Y})A^\mu\right]
+2\nabla_\mu\!\left[(b+\mathcal F_{\mathcal Y})p^\mu\right]=0.
\]
This matches the scalar equation printed as Eq. (5) by Fu, He, Sui & Zhang (2024), and the independent scalar variation recorded in the Block.

The scalar boundary contribution is
\[
\delta S_{\phi,\partial}=
\frac{1}{16\pi\widetilde G}
\int_{\partial M}d\Sigma_\mu\,P^\mu\,\delta\phi.
\]

## 3. Multiplier variation — direct derivation [D]

\[
\delta_\lambda S=0\quad\Longrightarrow\quad A^\mu A_\mu=-1.
\]

## 4. Vector variation — direct derivation and discrepancy [D/O]

Keep \(g_{\mu\nu}\) fixed and vary the covector \(A_\nu\). Then
\[
\delta A^\alpha=g^{\alpha\nu}\delta A_\nu,\qquad
\delta\mathcal Q=p^\nu\delta A_\nu,\qquad
\delta\mathcal Y=2\mathcal Q\,p^\nu\delta A_\nu.
\]
Writing \(J^\mu=g^{\mu\nu}A^\alpha\nabla_\alpha A_\nu\),
\[
\delta J^\mu
=g^{\mu\nu}\!\left(g^{\alpha\rho}\delta A_\rho\nabla_\alpha A_\nu
+A^\alpha\nabla_\alpha\delta A_\nu\right).
\]
The Maxwell term varies as
\[
\delta\!\left(-\frac{K_B}{2}F_{\mu\nu}F^{\mu\nu}\right)
=-2K_B F^{\mu\nu}\nabla_\mu\delta A_\nu
\]
and hence contributes \(+2K_B\nabla_\mu F^{\mu\nu}\) to the bulk Euler derivative. The \(J^\mu p_\mu\) term contributes
\[
2b\left[p_\mu\nabla^\nu A^\mu-\nabla_\mu(A^\mu p^\nu)\right].
\]
The \(\mathcal Y,\mathcal Q,\lambda\) terms contribute
\[
-\left[2\mathcal Q(b+\mathcal F_{\mathcal Y})+\mathcal F_{\mathcal Q}\right]p^\nu
-2\lambda A^\nu.
\]
Thus the full vector Euler equation from the displayed action is
\[
2K_B\nabla_\mu F^{\mu\nu}
+2b\left[p_\mu\nabla^\nu A^\mu-\nabla_\mu(A^\mu p^\nu)\right]
-\left[2\mathcal Q(b+\mathcal F_{\mathcal Y})+\mathcal F_{\mathcal Q}\right]p^\nu
-2\lambda A^\nu=0.
\]
Dividing the entire equation by two gives the normalized form
\[
K_B\nabla_\mu F^{\mu\nu}
+b\left[p_\mu\nabla^\nu A^\mu-\nabla_\mu(A^\mu p^\nu)\right]
-\frac12\left[2\mathcal Q(b+\mathcal F_{\mathcal Y})+\mathcal F_{\mathcal Q}\right]p^\nu
-\lambda A^\nu=0. \tag{V-action}
\]

**Discrepancy:** Fu et al. (2024), Eq. (4), print the same normalized equation but with coefficient \(2b\), rather than \(b\), multiplying the bracket
\[
B^\nu:=p_\mu\nabla^\nu A^\mu-\nabla_\mu(A^\mu p^\nu).
\]
All the other terms in their Eq. (4) match the normalized direct variation above. Therefore
\[
E^\nu_{A,\mathrm{published}}-E^\nu_{A,\mathrm{action}}=b\,B^\nu.
\]
This is not the ordinary overall factor-of-two convention: the discrepancy is isolated to the \(J^\mu\nabla_\mu\phi\) contribution. It is also not resolved by choosing \(A_\mu\) versus \(A^\mu\) as the independent vector, because those are related by an invertible metric-dependent field reparametrization at fixed metric and give the same vector equation up to index placement.

An exact SymPy component regression is also committed as \`verify_aest_j_vector_variation.py\`. It isolates the \(J^\mu\nabla_\mu\phi\) term on the same constrained Minkowski background and returns the full covector Euler coefficient \(2b\), \(B^0=1\), action-normalized coefficient \(b\), and printed Eq. (4) coefficient \(2b\). The script was executed successfully with exact symbolic arithmetic. It is a focused component check, not a full tensor derivation.

A simple admissible field configuration proves that the bracket is not an algebraic identity: in Minkowski spacetime take \(A^\mu=(1,0,0,0)\) and \(\phi=t^2/2\). Then \(A^\mu A_\mu=-1\), \(p_0=t\), \(p^0=-t\), and
\[
B^0=p_\mu\partial^0 A^\mu-\partial_\mu(A^\mu p^0)
=0-\partial_t(-t)=1.
\]
This is not asserted to be a solution; it is a counterexample to the claim that \(B^\nu\) vanishes identically from the unit constraint or definitions alone.

**Disposition:** [O] A source/action-versus-vector-equation inconsistency is identified. The next check must compare the original 2021 derivation, the 2022 stability paper, and an independent symbolic component variation. Do not silently edit the published equation or the pinned action. The discrepancy may be a typographical error in the printed vector equation, a mismatch in the action normalization as transcribed, or a convention not yet located. The action and Eq. (4) cannot both be accepted unchanged unless \(bB^\nu=0\) is independently established in the intended field domain; it is not an identity for arbitrary fields.

The vector boundary contribution is
\[
\delta S_{A,\partial}=
\frac{1}{16\pi\widetilde G}
\int_{\partial M}d\Sigma_\mu
\left[-2K_BF^{\mu\nu}+2bA^\mu p^\nu\right]\delta A_\nu.
\]

## 5. Metric variation — expanded and matched [D/C]

Use the declared independent-field convention \((g^{\mu\nu},A_\mu,\phi,\lambda)\), holding the covector \(A_\mu\) fixed in the metric variation. The identity
\[
J^\alpha p_\alpha=A^\alpha p^\nu\nabla_\alpha A_\nu
\]
has two direct inverse-metric variations, because both raised vectors depend on \(g^{\mu\nu}\):
\[
\delta_g(J^\alpha p_\alpha)=
\left[p_{(\mu}B_{\nu)}+A_{(\mu}p^\rho\nabla_{\nu)}A_\rho\right]\delta g^{\mu\nu}
-A^\alpha p^\nu A_\rho\,\delta\Gamma^\rho_{\alpha\nu}.
\]
The second direct term \(A_{(\mu}p^\rho\nabla_{\nu)}A_\rho\) was omitted in the earlier compact draft; that omission is corrected here.

For the connection part of the full \(2bJ^\alpha p_\alpha\) term, define
\[
P_\rho{}^{\alpha\nu}=-2bA_\rho A^{(\alpha}p^{\nu)},\qquad
P^{\sigma\alpha\nu}=g^{\sigma\rho}P_\rho{}^{\alpha\nu}.
\]
Using the Levi-Civita variation and integrating by parts gives the coefficient of \(\delta g_{\mu\nu}\)
\[
C^{\mu\nu}=-\nabla_\alpha P^{(\mu|\alpha|\nu)}
+\frac12\nabla_\rho P^{\rho\mu\nu}
=b\nabla_\rho(A^\mu A^\nu p^\rho).
\]
Thus its contribution to the coefficient of \(\delta g^{\mu\nu}\) is
\[
E^{\rm conn}_{\mu\nu}=-b\nabla_\rho(A_\mu A_\nu p^\rho).
\]
Combining this with both direct terms, and using \(F_{\mu\nu}=2\nabla_{[\mu}A_{\nu]}\), yields
\[
\begin{aligned}
\left.\delta_g(2bJ^\alpha p_\alpha)\right|_{\rm bulk}
=2b\bigg[&
A^\sigma p_{(\mu}\nabla_\sigma A_{\nu)}
+p_\sigma A_{(\mu}F_{\nu)}{}^\sigma
-\frac12A_\mu A_\nu\Box\phi
\bigg]\delta g^{\mu\nu}.
\end{aligned}
\]
This is the derivative structure printed in Fu et al. (2024), Eq. (3).

The remaining metric terms follow directly:
\[
\begin{aligned}
E_{\mu\nu}={}&G_{\mu\nu}
-K_B\left(F_{\mu}{}^{\rho}F_{\nu\rho}
-\frac14g_{\mu\nu}F_{\rho\sigma}F^{\rho\sigma}\right)
-\lambda A_\mu A_\nu
-b g_{\mu\nu}J^\alpha p_\alpha\\
&+2b\left[
A^\sigma p_{(\mu}\nabla_\sigma A_{\nu)}
+p_\sigma A_{(\mu}F_{\nu)}{}^\sigma
-\frac12A_\mu A_\nu\Box\phi
\right]
+\frac12g_{\mu\nu}(b\mathcal Y+\mathcal F)\\
&-(b+\mathcal F_{\mathcal Y})p_\mu p_\nu
-\left[2\mathcal Q(b+\mathcal F_{\mathcal Y})+\mathcal F_{\mathcal Q}\right]
 A_{(\mu}p_{\nu)}.
\end{aligned}
\]
On the multiplier constraint \(A^\mu A_\mu=-1\), this agrees term by term with the published \(G_{\mu\nu}+\mathcal H_{\mu\nu}=8\pi\widetilde G T_{\mu\nu}\) form after matching the paper's \(\kappa=1\) normalization. The metric variation is therefore closed for this action and field basis. The vector equation discrepancy in §4 remains separate.

## 6. Diffeomorphism identity and Bianchi gate [D/O]

For independent fields \((g^{\mu\nu},A_\mu,\phi,\lambda)\), define \(E_A^\mu=(\sqrt{-g})^{-1}\delta S/\delta A_\mu\), \(E_\phi=(\sqrt{-g})^{-1}\delta S/\delta\phi\), \(E_\lambda=(\sqrt{-g})^{-1}\delta S/\delta\lambda\), and \(E_{\mu\nu}\) as the coefficient of \(\delta g^{\mu\nu}\). Diffeomorphism invariance gives
\[
2\nabla^\mu E_{\mu\nu}
+E_A^\mu F_{\nu\mu}
-A_\nu\nabla_\mu E_A^\mu
+E_\phi\nabla_\nu\phi
+E_\lambda\nabla_\nu\lambda=0.
\]
The identity is exact for the Euler derivatives of the same action. Replacing the action-derived normalized vector equation by the printed 2024 Eq. (4) changes the full vector Euler derivative by \(\Delta E_A^\mu=2bB^\mu\), and hence shifts the identity by
\[
\Delta\mathcal N_\nu=
2b\left(B^\mu F_{\nu\mu}-A_\nu\nabla_\mu B^\mu\right).
\]

This residual is not identically zero even on the unit-vector constraint. An exact constrained Minkowski test in 1+1 dimensions (embedded in 3+1) is
\[
A^\mu=(\cosh(\epsilon t),\sinh(\epsilon t),0,0),\qquad
\phi=t+x.
\]
It obeys \(A^\mu A_\mu=-1\). Direct evaluation gives
\[
B^\mu=(-\epsilon\cosh(\epsilon t),-\epsilon\sinh(\epsilon t),0,0),
\quad F_{01}=\epsilon\cosh(\epsilon t),
\quad \nabla_\mu B^\mu=-\epsilon^2\sinh(\epsilon t),
\]
and therefore
\[
B^\mu F_{0\mu}-A_0\nabla_\mu B^\mu
=-\epsilon^2\sinh(2\epsilon t),\qquad
B^\mu F_{1\mu}-A_1\nabla_\mu B^\mu
=\epsilon^2\cosh(2\epsilon t).
\]
The candidate-equation residual is consequently nonzero for generic \(b\epsilon\ne0\). This is an off-shell Noether-identity test, not a claim that this field configuration solves the equations or that the theory has no solutions. It shows that the printed vector equation cannot simply be substituted as though it were the Euler derivative of the printed action.

## 7. Boundary data and a sufficient Dirichlet variational principle [D]

The scalar and vector integrations by parts give
\[
\delta S_{\phi,\partial}=
\frac{1}{16\pi\widetilde G}\int_{\partial M}d\Sigma_\mu
\left[2bJ^\mu-2(b+\mathcal F_{\mathcal Y})q^{\mu\nu}p_\nu
-\mathcal F_{\mathcal Q}A^\mu\right]\delta\phi,
\]
\[
\delta S_{A,\partial}=
\frac{1}{16\pi\widetilde G}\int_{\partial M}d\Sigma_\mu
\left[-2K_BF^{\mu\nu}+2bA^\mu p^\nu\right]\delta A_\nu.
\]
The metric-connection contribution from the \(Jp\) term is
\[
\frac{1}{16\pi\widetilde G}\int_{\partial M}d\Sigma_\alpha
\left[P^{\sigma\alpha\nu}\delta g_{\sigma\nu}
-\frac12P^{\alpha\sigma\nu}\delta g_{\sigma\nu}\right],
\]
where \(P^{\sigma\alpha\nu}=-2bA^\sigma A^{(\alpha}p^{\nu)}\). This surface term vanishes under full metric Dirichlet data.

A sufficient (not asserted minimal or unique) well-posed boundary prescription on a smooth non-null boundary is:
- add the standard Gibbons–Hawking–York term \(S_{\rm GHY}=(8\pi\widetilde G)^{-1}\int_{\partial M}\epsilon\sqrt{|h|}K\), with the sign convention for the chosen outward normal and extrinsic curvature;
- fix all components of \(g_{\mu\nu}\), \(A_\mu\), and \(\phi\) on the boundary, so \(\delta g_{\mu\nu}=\delta A_\mu=\delta\phi=0\) there;
- leave \(\lambda\) free, since it carries no derivatives and produces no boundary flux;
- impose the matter-sector boundary conditions appropriate to \(S_m\), and include the usual joint terms if the boundary is piecewise smooth.

This is a deliberately strong Dirichlet choice. If only the induced metric is fixed (rather than all metric components), or if Neumann/mixed data are desired for \(A_\mu\) or \(\phi\), the boundary variational problem must be re-derived with the corresponding boundary terms; this report does not claim that the displayed GHY term alone handles those alternative choices.

## 6. Diffeomorphism identity and Bianchi gate [D/O]

For independent fields \((g^{\mu\nu},A_\mu,\phi,\lambda)\), define \(E_A^\mu=(\sqrt{-g})^{-1}\delta S/\delta A_\mu\), \(E_\phi=(\sqrt{-g})^{-1}\delta S/\delta\phi\), \(E_\lambda=(\sqrt{-g})^{-1}\delta S/\delta\lambda\), and \(E_{\mu\nu}\) as the coefficient of \(\delta g^{\mu\nu}\). Diffeomorphism invariance gives
\[
2\nabla^\mu E_{\mu\nu}
+E_A^\mu F_{\nu\mu}
-A_\nu\nabla_\mu E_A^\mu
+E_\phi\nabla_\nu\phi
+E_\lambda\nabla_\nu\lambda=0.
\]
Thus a candidate vector equation substituted into this identity must be the Euler derivative of the *same* action used for the metric equation. The mismatch in the *normalized* vector equation is \(bB^\mu\); because the full Euler derivative is twice that normalized equation, the full Euler-derivative mismatch is \(\Delta E_A^\mu=2bB^\mu\). It shifts the identity by
\[
2b\left(B^\mu F_{\nu\mu}-A_\nu\nabla_\mu B^\mu\right).
\]
That residual must be explicitly checked; it cannot be assumed to vanish. The matter conservation statement \(\nabla_\mu T^{\mu\nu}=0\) is conditional on the matter equations and the complete gravitational Euler system; it is not an independent proof that an inconsistent subset of printed equations satisfies the identity.
## 8. Cross-checks and boundaries

- The scalar equation and unit constraint agree with the published equations.
- The 2024 printed metric equation supplies a target for simplifying the compact metric variation; the \(A_\mu\)-fixed versus \(A^\mu\)-fixed convention must still be declared.
- The 2024 printed vector equation differs from the direct variation of the action by \(bB^\nu\).
- The 2021 and 2022 papers print the same covariant action interaction and Maxwell normalization. The 2022 paper's stability calculation is an action-level perturbative benchmark, not an independent printed covariant vector equation. The 2024 Hamiltonian paper independently repeats the same action and reports four first-class/four second-class constraints and six nonlinear physical degrees of freedom; this does not by itself resolve the isolated 2024 Eq. (4) coefficient.
- The published Hamiltonian analysis reports four first-class and four second-class constraints and six nonlinear physical degrees of freedom. These counts should be reproduced only after the exact action/equation pair is pinned.
- No spectrum, branch fit, or physical stability claim is advanced here.

## 9. Next required computations

1. Independently derive the vector Euler derivative in explicit components from the exact action (including a simple nontrivial field configuration with \(B^\nu\ne0\)).
2. Compare the 2021 action and the 2022 stability expansion with the 2024 Eqs. (1)–(5), term by term, to locate whether the discrepancy is transcription, convention, or publication error.
3. Expand \(E^{\rm conn}_{\mu\nu}\) and compare each term to the published \(\mathcal H_{\mu\nu}\).
4. Write the exact diffeomorphism Noether identity in the declared field basis and test it against both candidate vector equations.
5. Specify boundary data and derive the complete boundary action before claiming a well-posed variational principle.
6. Only after these gates, derive the metric-half/Newtonian limit, full \(K(\mathcal Q)\) cosmological branch and perturbative stability for the chosen \(\mathcal F(\mathcal Y,\mathcal Q)\).

## Sources

1. C. Skordis & T. Złośnik (2021), *A new relativistic theory for Modified Newtonian Dynamics*, Phys. Rev. Lett. 127, 161302, DOI: 10.1103/PhysRevLett.127.161302, arXiv:2007.00082.
2. Q.-M. Fu, M.-C. He, T.-T. Sui & X. Zhang (2024), *Reconstruction of aether scalar tensor theory for various cosmological scenarios*, Chinese Physics C 48, 045105, DOI: 10.1088/1674-1137/ad2360. Eqs. (1)–(5) reproduce the action and the printed metric/vector/scalar equations audited above.
3. C. Skordis & T. Złośnik (2022), *Aether scalar tensor theory: Linear stability on Minkowski space*, Phys. Rev. D 106, 104041, DOI: 10.1103/PhysRevD.106.104041, arXiv:2109.13287.
4. M. Bataki, C. Skordis & T. Złośnik (2024), *Aether scalar-tensor theory: Hamiltonian formalism*, Phys. Rev. D 110, 044015, DOI: 10.1103/PhysRevD.110.044015, arXiv:2307.15126.
5. P. Verwayen, C. Skordis & C. Bœhm (2024), *Aether Scalar Tensor (AeST) theory: quasistatic spherical solutions and their phenomenology*, MNRAS 531, 272–289, DOI: 10.1093/mnras/stae1225, arXiv:2304.05134.

**Evidence labels:** [D] direct algebraic variation under the stated action and field basis; [C] published equation/analysis; [O] unresolved comparison or physical/model choice.