# One-Sheet Jacobian Split & D56 Classification Audit

**Script:** [`jacobian_split_and_d56_audit.py`](file:///home/mega/Chyren/3_research/Res-Nova/audits/2026-11-19/jacobian_split_and_d56_audit.py)  
**Receipt:** [`JACOBIAN_SPLIT_AND_D56_AUDIT.json`](file:///home/mega/Chyren/3_research/Res-Nova/audits/2026-11-19/JACOBIAN_SPLIT_AND_D56_AUDIT.json)  
**Scope & Discipline:** All definitions use `:=`. Respects the live Res-Nova seat (`V_2(R^3)`, `E_8 × E_8`, minimal matter coupling + AeST; disformal matter coupling retired `[X]` per `RN-GEA-RETIRED-001`; closed negatives stay closed).

---

## Summary Table: `(J + Jᵀ)/2` vs `(J − Jᵀ)/2`

| 2-Slot Machine (`:=`) | Symmetric Part `(J + Jᵀ)/2` | Antisymmetric Part `(J − Jᵀ)/2` | Verdict & Physics Consequence |
|---|---|---|---|
| **J1. ITT/AQUAL kinetic Hessian** $J^{\mu\nu} := \frac{\partial^2 f}{\partial v_\mu \partial v_\nu}$, $y := \ell^2 g^{\alpha\beta} v_\alpha v_\beta$ | $2\ell^2\!\left[f'(y)\,g^{\mu\nu} + 2\ell^2 f''(y)\,v^\mu v^\nu\right]$ — **not $c\,g^{\mu\nu}$** (disformal acoustic metric) | **Identically $0$** | At $f'(x^2)=\mu_{\mathrm{std}}(x)$, $f''(y) = \frac{1}{2\sqrt{y}(1+y)^{3/2}} \to +\infty$ as $y\to 0^+$ (the Postulate R non-analytic branch point). Disformal $\tilde{g}_{\mu\nu} := g_{\mu\nu} + 2\ell^2 v_\mu v_\nu$ is symmetric and retired `[X]` for matter coupling. |
| **J2a. Live AeST aether gradient** $J_{\mu\nu} := \nabla_\mu A_\nu$ | $S_{\mu\nu} = \nabla_{(\mu} A_{\nu)}$ (expansion $\theta$ + shear $\sigma_{\mu\nu}$) — **not $g_{\mu\nu}$** | $\frac{1}{2}F_{\mu\nu} = \nabla_{[\mu} A_{\nu]}$ | $-\frac{K_B}{2}F_{\mu\nu}F^{\mu\nu} = -2K_B A_{\mu\nu}A^{\mu\nu}$ has **zero dependence on $S_{\mu\nu}$** ($c_1+c_3=0 \implies c_T=c$). |
| **J2b. Hypersurface-orthogonal unit vector** $u_\mu := -N\partial_\mu T$ (dark-bubble Killing projection) | FLRW expansion $H\,h_{ij}$ | $F_{ij} \equiv 0$, $F_{\mu\nu}^{\mathrm{bg}} \equiv 0$, **$F_{0i}^{\mathrm{lin}} = \epsilon a\,\partial_i \Phi \neq 0$** | Exact covariant identity $F_{\mu\nu} = u_\nu a_\mu - u_\mu a_\nu \;\to\; F_{\mu\nu}F^{\mu\nu} = -2\epsilon^2(\nabla\Phi)^2/a^2$. Vanishes on FLRW background, **non-zero when perturbed**, carrying the AeST electric gradient energy. |
| **J3. D56 "Two Tens"** ($H_4(\mathbb{R})$ vs. $H_2(\mathbb{O})$) | Both $10$-spaces are **purely symmetric** | **Identically $0$** for both (`[X]` on brainstorm guess) | Separated by **Jordan rank / norm degree**: $\det(\lambda M) = \lambda^4\det M$ on $H_4(\mathbb{R})$ (quartic, space of metrics) vs. $N_2(\lambda v) = \lambda^2 N_2(v)$ with Hessian eigenvalues $\{+1^1, -1^1, -2^8\} \implies (1,9)$ on $H_2(\mathbb{O})$. |
| **J4. 3D Navier–Stokes velocity gradient** $J_{ij} := \partial_j u_i$ | Strain $S_{ij}$ ($\operatorname{tr}S = \nabla\cdot u$) | Vorticity $\Omega_{ij} = -\frac{1}{2}\epsilon_{ijk}\omega_k$ | Non-local 3D Biot–Savart / Calderón–Zygmund kernel couples antisymmetric $\Omega$ back into symmetric $S$. |
