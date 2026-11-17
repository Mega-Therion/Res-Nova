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

## 5. Metric variation — compact independent formula [D/O]

For the declared \(A_\mu\)-fixed convention, set
\[
B_\nu:=A^\alpha\nabla_\alpha A_\nu,\qquad
L_{\rm nd}:=-\frac{K_B}{2}F^2+2bJ^\alpha p_\alpha-b\mathcal Y
-\mathcal F-\lambda(A^2+1).
\]
The direct inverse-metric variations are
\[
\delta\mathcal Q=A_{(\mu}p_{\nu)}\delta g^{\mu\nu},
\]
\[
\delta\mathcal Y=
\left[p_\mu p_\nu+2\mathcal Q A_{(\mu}p_{\nu)}\right]\delta g^{\mu\nu},
\qquad
\delta(A^2)=A_\mu A_\nu\delta g^{\mu\nu},
\]
\[
\delta(J^\alpha p_\alpha)
=\left[p_{(\mu}B_{\nu)}\right]\delta g^{\mu\nu}
-p^\nu A^\alpha A_\rho\,\delta\Gamma^\rho_{\alpha\nu}.
\]
The connection term can be packaged as
\[
P_\rho{}^{\alpha\nu}:=-2b\,A_\rho A^{(\alpha}p^{\nu)},\qquad
P^{\sigma\alpha\nu}:=g^{\sigma\rho}P_\rho{}^{\alpha\nu},
\]
\[
C^{\alpha\nu}:=-\nabla_\mu P^{(\alpha|\mu|\nu)}
+\frac12\nabla_\sigma P^{\sigma\alpha\nu}.
\]
After integration by parts, the contribution of this connection variation to the coefficient of \(\delta g^{\mu\nu}\) is
\[
E^{\rm conn}_{\mu\nu}=-g_{\mu\alpha}g_{\nu\beta}C^{\alpha\beta}.
\]
Consequently, before matter is added, the metric Euler tensor can be written compactly as
\[
\begin{aligned}
E_{\mu\nu}={}&G_{\mu\nu}-\frac12g_{\mu\nu}L_{\rm nd}
-K_BF_{\mu\rho}F_\nu{}^\rho
+2b\,p_{(\mu}B_{\nu)}\\
&-(b+\mathcal F_{\mathcal Y})
  (p_\mu p_\nu+2\mathcal Q A_{(\mu}p_{\nu)})
-\mathcal F_{\mathcal Q}A_{(\mu}p_{\nu)}
-\lambda A_\mu A_\nu+E^{\rm conn}_{\mu\nu}.
\end{aligned}
\]
With \(T_{\mu\nu}:=-2(\sqrt{-g})^{-1}\delta S_m/\delta g^{\mu\nu}\), the metric equation is
\[
E_{\mu\nu}=8\pi\widetilde G\,T_{\mu\nu}.
\]
This is a compact Palatini-form result, not yet a line-by-line expanded equivalence proof against the printed \(\mathcal H_{\mu\nu}\). The explicit connection boundary term before imposing boundary conditions is
\[
\int_{\partial M}d\Sigma_\mu
\left(P^{\sigma\mu\nu}\delta g_{\sigma\nu}
-\frac12P^{\mu\sigma\nu}\delta g_{\sigma\nu}\right),
\]
with indices in the first term understood exactly as in the unintegrated Palatini expression. A fully normalized boundary functional \(S_\partial\), including the Einstein–Hilbert/Gibbons–Hawking–York part and the appropriate boundary data for the vector/metric sector, remains [O].

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
## 7. Cross-checks and boundaries

- The scalar equation and unit constraint agree with the published equations.
- The 2024 printed metric equation supplies a target for simplifying the compact metric variation; the \(A_\mu\)-fixed versus \(A^\mu\)-fixed convention must still be declared.
- The 2024 printed vector equation differs from the direct variation of the action by \(bB^\nu\).
- The 2021 paper's second-order perturbative stability result and the 2024 Hamiltonian analysis are external benchmarks for the published AeST model. They do not certify the Res-Nova constitutive slice or resolve the vector-equation discrepancy.
- The published Hamiltonian analysis reports four first-class and four second-class constraints and six nonlinear physical degrees of freedom. These counts should be reproduced only after the exact action/equation pair is pinned.
- No spectrum, branch fit, or physical stability claim is advanced here.

## 8. Next required computations

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