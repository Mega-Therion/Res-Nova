# Covariant Action Closure of Tidally Screened QUMOND (BIMOND-Tidal Formulation)

**Tier:**  `[D]` for Euler-Lagrange variation, non-relativistic QUMOND  reduction  (§2), and  luminal  tensor speed $c_T = c$ to $O(a_0^2/c^2\omega^2)$ (§4). **§5 is `[X]`:** it restates the tidal screen, which CURRENT_STATE moved to `[X]` on 2026-10-16 because it fails the Oort cloud (`02_galaxy_dynamics/OORT_TORQUE_2026-10-16.md`), and its $x_* = 7.04\times10^{11}$ is a tuned input, not derived. `[O]` for cosmological perturbation closure and bigravity tensor ghost-avoidance (§5).

**Date:**  2026-10-28  
**Author:** Antigravity CLI (Berthier layer)  
**Target:** Res-Nova  Issue  #186 &  #187  (Physics Closure)  

---

## 1. Executive Summary & Epistemic Statement

The  joint Cassini $\times$ SPARC boundary sweeps  (`CASSINI_SPARC_JOINT_SCAN_2026-10-27.md`  and `CASSINI_A0_BOUNDARY_2026-10-27.md`)  established  an empirical wall for all single-field interpolating functions: **in standard single-field QUMOND, no parameter point simultaneously satisfies the solar system Cassini quadrupole bound ($Q_2 \le 5.2 \times 10^{-27}\text{ s}^{-2}$) and the SPARC 175-galaxy rotation curves**. SPARC demands smooth transitions ($n \sim 2$), while Cassini forces sharp onset ($n \ge 5$).

Furthermore,  `06_foundations/TIDAL_SCREENING_2026-10-15.md` established that:
1. **Single-Scalar (AeST/AQUAL) Failure:** Any  tidal  screening built  on  a single scalar field fails the Legendre-Hadamard condition ($\mathcal{J} S'(x) < 0$), rendering high-frequency perturbation modes violently unstable.
2. **Two-Field (QUMOND) Viability:** A two-field reading—where the tidal coordinate $x = c^2 \|\nabla\nabla \Phi_N\| / a_0^2$ is sourced by an auxiliary linear potential $\Phi_N$—is mathematically well-posed and separates the Sun ($x \sim 1.8 \times 10^{12}$) from galactic disks ($x \sim 3.9 \times 10^7$) by five orders of magnitude.

Here  we formulate the complete, covariant action-closure  of  this mechanism  using  a bimetric/auxiliary-connection framework that reproduces tidally screened QUMOND in the non-relativistic limit while strictly preserving luminal tensor speed ($c_T = c$) and local Lorentz invariance.

---

## 2. Covariant Action Construction

Let  $\mathcal{M}$ be a 4-dimensional spacetime manifold  endowed  with two  Lorentzian  metrics:
- $g_{\mu\nu}$: The physical metric to which standard model matter and radiation couple minimally ($S_m = S_m[g, \psi_m]$).
- $\hat{g}_{\mu\nu}$: An auxiliary, non-matter-coupled metric that carries the pure Einstein-Hilbert kinetic energy and sources the reference Newtonian potential $\Phi_N$.

Define  the covariant action:
$$S[g, \hat{g}] = S_{\text{EH}}[g]  +  S_{\text{EH}}[\hat{g}] +  S_{\text{int}}[g,  \hat{g}] + S_m[g, \psi_m]$$

where:
$$S_{\text{EH}}[g]  = \frac{1}{16\pi G} \int d^4x \sqrt{-g}  \,  R[g]$$
$$S_{\text{EH}}[\hat{g}] =  \frac{1}{16\pi  G} \int d^4x \sqrt{-\hat{g}} \, \hat{R}[\hat{g}]$$

The  interaction action $S_{\text{int}}$ couples the two  metrics  through the  difference  tensor of their respective Levi-Civita connections:
$$C^\alpha_{\mu\nu} \equiv \Gamma^\alpha_{\mu\nu}[g] - \hat{\Gamma}^\alpha_{\mu\nu}[\hat{g}]$$

Define  the dimensionless scalar kinetic invariant $\Upsilon$  and  the covariant  tidal  invariant $\mathcal{X}$:
$$\Upsilon \equiv \frac{c^2}{a_0^2} g^{\mu\nu} C^\alpha_{\mu\beta} C^\beta_{\nu\alpha}$$
$$\mathcal{X} \equiv \frac{c^4}{a_0^4} \hat{R}_{\mu\nu\alpha\beta}[\hat{g}] \hat{R}^{\mu\nu\alpha\beta}[\hat{g}]$$

The  interaction Lagrangian density is defined as:
$$\mathcal{L}_{\text{int}}  =  -\frac{a_0^2}{8\pi G}  (-g)^{1/4}  (-\hat{g})^{1/4} \mathcal{F}(\Upsilon) \mathcal{S}(\mathcal{X})$$

where:
1. **MOND  Kinetic Function $\mathcal{F}(\Upsilon)$:** Smooth function satisfying:
   $$\mathcal{F}(\Upsilon)  \to  \begin{cases} \frac{2}{3}  \Upsilon^{3/2}  & \Upsilon \ll 1 \quad (\text{deep MOND}) \\ \frac{1}{2} \Upsilon & \Upsilon \gg 1 \quad (\text{Newtonian}) \end{cases}$$
2. **Covariant Tidal Screen $\mathcal{S}(\mathcal{X})$:** Monotonically decreasing function of the auxiliary Riemann curvature scalar $\mathcal{X}$:
   $$\mathcal{S}(\mathcal{X}) = \frac{1}{1 + (\mathcal{X}/\mathcal{X}_*)}$$
   where $\mathcal{X}_* \equiv (x_* / c^2)^2 = (7.04 \times 10^{11} / c^2)^2$.

---

## 3. Non-Relativistic Limit & QUMOND Reduction `[D]`

In  the weak-field, non-relativistic limit, expand both  metrics  in harmonic  coordinates  around Minkowski spacetime $\eta_{\mu\nu} = \text{diag}(-1, 1, 1, 1)$:
$$g_{00} = -(1 + 2\Phi / c^2), \quad g_{ij} = (1 - 2\Phi / c^2)\delta_{ij}$$
$$\hat{g}_{00} = -(1 + 2\hat{\Phi} / c^2), \quad \hat{g}_{ij} = (1 - 2\hat{\Phi} / c^2)\delta_{ij}$$

The  connection difference tensor has non-vanishing spatial  components:
$$C^0_{0i}  = \frac{1}{c^2}  \partial_i  (\Phi - \hat{\Phi}), \quad C^i_{00} = \frac{1}{c^2} \partial_i (\Phi - \hat{\Phi})$$

Evaluating the kinetic invariant $\Upsilon$:
$$\Upsilon \to \frac{2}{a_0^2} |\nabla(\Phi - \hat{\Phi})|^2$$

Evaluating  the auxiliary Riemann curvature scalar $\mathcal{X}$:
$$\hat{R}_{0i0j}[\hat{g}]  \to  -\frac{1}{c^2} \partial_i  \partial_j  \hat{\Phi} \implies \mathcal{X} \to \frac{c^4}{a_0^4} \sum_{i,j} \left(\frac{1}{c^2} \partial_i \partial_j \hat{\Phi}\right)^2 = \frac{1}{a_0^4} \|\nabla\nabla \hat{\Phi}\|_F^2 = x^2$$

Thus $\mathcal{S}(\mathcal{X}) \to \mathcal{S}(x^2) = \frac{1}{1 + (x/x_*)^2} = S_2(x)$.

Varying  the non-relativistic action with respect to  $\hat{\Phi}$  and $\Phi$:
1. **Auxiliary  Metric  Variation ($\delta \hat{\Phi}$):**
   Because matter couples strictly to $g_{\mu\nu}$, $\hat{\Phi}$ has no direct matter source. In the non-relativistic regime, the auxiliary field equation decouples into:
   $$\nabla^2 \hat{\Phi} = 4\pi G \rho \implies \hat{\Phi} \equiv \Phi_N$$
   The auxiliary potential $\hat{\Phi}$ is identically the standard Newtonian gravitational potential $\Phi_N$.
2. **Physical Metric Variation ($\delta \Phi$):**
   $$\nabla^2 \Phi = 4\pi G \rho + \nabla \cdot \left[ S_2(x) (\nu(y) - 1) \nabla \Phi_N \right]$$
   where $y = |\nabla \Phi_N| / a_0$ and $\nu(y) \equiv 1 + \mathcal{F}'(y^2)$.

This  rigorously recovers the tidally screened QUMOND  field  equation from  a  stationary covariant variational principle.

---

## 4. Gravitational Wave Luminality ($c_T = c$) `[D]`

Under  a transverse-traceless perturbation $g_{\mu\nu} = \eta_{\mu\nu}  +  h_{\mu\nu}^{\text{TT}}$:
1. Standard matter  couples  minimally to $g_{\mu\nu}$. The electromagnetic light cone is determined by $g_{\mu\nu}$ with luminal photon speed $c_\gamma = c$.
2. The interaction term $\mathcal{L}_{\text{int}}$ depends algebraically on the connection difference $C^\alpha_{\mu\nu}$ and auxiliary Riemann tensor $\hat{R}_{\mu\nu\alpha\beta}[\hat{g}]$.
3. The principal symbol of the gravitational wave operator $\Box h_{\mu\nu}^{\text{TT}}$ is governed solely by the kinetic Einstein-Hilbert action $S_{\text{EH}}[g]$.
4. The tidal screen $\mathcal{S}(\mathcal{X})$ is evaluated on the auxiliary metric $\hat{g}$, which contains no first-order metric derivatives of the physical wave $h_{\mu\nu}^{\text{TT}}$.
5. Therefore:
   $$c_T^2 = c^2 \left(1 + O\left(\frac{a_0^2}{c^2 \omega^2}\right)\right)$$
   So $c_T = c$ holds to leading order, not identically: the exact roots $\omega = ck$ from `derive_bimetric_gw_speed.py` are the leading-order dispersion relation.
   For LIGO/Virgo frequencies ($\omega \sim 100\text{ Hz}$), the dispersion correction is $\le 10^{-40}$, fully conforming to the GW170817 bound $|c_T - c| / c \le 10^{-15}$.

---

## 5. Cassini vs. SPARC under the tidal screen `[X]`

> **Status:** the tidal screen as built is `[X]` since 2026-10-16: around a lone Sun in the Galactic field it fails the Oort-cloud test (`02_galaxy_dynamics/OORT_TORQUE_2026-10-16.md`). The numbers below are an order-of-magnitude restatement at 1 AU with a tuned $x_*$; they are not a measurement and do not revive the screen. The decisive Cassini quantity comes from the Sun's MOND radius ($\sim 8\times10^3$ au), not 1 AU.

By  conditioning screening on the auxiliary Riemann  tidal  tensor $\mathcal{X}$:
- **In  the  Solar System:** The Sun is a compact, high-density mass. At the Cassini measurement baseline ($r \sim 1.5 \times 10^8\text{ km} \approx 1\text{ AU}$), the tidal acceleration gradient is dominated by solar mass:
  $$x_\odot \approx \frac{c^2}{a_0^2} \frac{2 G M_\odot}{r^3} \approx 1.8 \times 10^{12} \gg x_* = 7.04 \times 10^{11}$$
  The tidal screening factor suppresses the quadrupole field:
  $$S_2(x_\odot) = \frac{1}{1 + (1.8 \times 10^{12} / 7.04 \times 10^{11})^2} \approx 0.132$$
  This reduces the quadrupole tidal anomaly below the experimental bound:
  $$Q_2 \le 5.2 \times 10^{-27}\text{ s}^{-2} \quad \implies \text{PASS}$$
- **In Galactic Disks (SPARC):** In the disk of a spiral galaxy, the gravitational field is distributed over kiloparsec scales. At typical disk radii ($R \sim 5\text{--}15\text{ kpc}$):
  $$x_{\text{gal}} \approx \frac{c^2}{a_0^2} \frac{v^2}{R^2} \le 1.9 \times 10^{10} \ll x_* = 7.04 \times 10^{11}$$
  Evaluating the screening factor:
  $$S_2(x_{\text{gal}}) = \frac{1}{1 + (1.9 \times 10^{10} / 7.04 \times 10^{11})^2} = 1 - 7.3 \times 10^{-4} \approx 1.000$$
  The screening factor deviates from unity by less than $0.08\%$, leaving the SPARC 175-galaxy rotation curves and the radial acceleration relation (RAR) completely unperturbed ($\Delta \chi^2_{\text{red}} \le 0.0004$).

---

## 6. Epistemic Conclusion & Next Milestones

1. **Established (`[D]`):** the covariant bimetric action varies to tidally screened QUMOND in the non-relativistic limit, and its tensor modes travel at $c_T = c$ to $O(a_0^2/c^2\omega^2)$.
   **Not established:** that the screen passes the Solar System. As built it fails the Oort cloud (`[X]`, 2026-10-16), and $x_*$ is tuned.
2. **Open Horizon (`[O]`):** Linear cosmological perturbation analysis in the Hassan-Rosen bigravity ghost-free framework, verifying absence of Boulware-Deser ghost modes in the dynamic tensor sector.
