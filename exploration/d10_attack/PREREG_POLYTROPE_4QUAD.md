# Pre-registration: D10 AeST polytrope free-boundary, 4th-quadrant screened+dust, splashback pole, and ICM slope check (2026-11-19, before any number)

**Context.** `d10_attack.py` (`#251`) and `accretion.py` (`#252`) established:
- Pure MOND ($\mu = 0$): median $R = 1.96$ (undershoots).
- Fully screened MOND ($S = 0$, baryons only): median $R = 6.83$ (fails).
- Uncapped virial-boundary BVP ($\Phi(r_v) = 0$, $\mu = 1/0.9895\,\mathrm{Mpc}$): well-posed for 12/12 clusters, median $R = 0.75$ (overshoots), dust exceeds $(\Omega_c/\Omega_b)M_b(r_v)$ in 8/12 clusters.
- Supply-capped BVP via per-cluster $\mu$-rescaling (`accretion.py`): median $R = 0.84$, 8/12 in $[0.7, 1.4]$ (fails the $\ge 9/12$ criterion narrowly).

Four physics questions left open in `d10_attack/README.md`, `bk_xh_map/README.md`, and `tidal_aest/README.md` are tested here on the exact same 12 Corasaniti+2021 clusters (`02_galaxy_dynamics/clusters/cluster_mond_test.py`) with **fixed universal** $\mu = 1/(0.9895\,\mathrm{Mpc})$ and cosmic dust ratio $\Omega_c/\Omega_b = 5.36$, and **no per-cluster parameter tuning**:

## Symbolic derivation (SymPy, exact Euler–Lagrange)
- **(S1) Two-field Tidal-QUMOND-in-AeST + dust:** Add $\mathcal{K}(\mathcal{Q}) = \mathcal{K}_2(\mathcal{Q} - Q_0)^2$ with shift-symmetry stationary ansatz $\varphi = (Q_0 + \mu_c)t + \tilde{\varphi}(\mathbf{x})$ ($\Phi_0 \equiv \mu_c/Q_0$) to `exploration/tidal_aest/normalization_kb.py`. Verify symbolically: (i) whether $\Psi = \Phi$ ($\gamma = 1$, lensing = dynamics) survives; (ii) whether $\mu^2(\Phi_0 - \Phi)$ enters the $\psi$ (shadow) equation, coupling dust into the MOND operator; (iii) exact equation of state $P(\rho) = \rho^2 / (4\mathcal{K}_2 Q_0^2)$ ($n = 1$ Lane–Emden polytrope) and exact local sound speed $c_s^2(\rho) = \delta Q/(Q_0 + \delta Q)$, distinguishing the core hydrostatic speed ($\rho \sim \rho_{500}$) from the cosmic infall speed ($\rho = \bar{\rho}_c$).

## Pre-registered numerical tests (12 Corasaniti+2021 clusters; fixed $\mu = 1/0.9895\,\mathrm{Mpc}$)

### Test 1: Free-boundary $n = 1$ polytrope with MOND ON (fixed $\mu$, chemical potential $\Phi_0$ fixed by supply)
- Instead of rescaling the Lagrangian constant $\mu$ per cluster (`accretion.py`), keep $\mu = 1/0.9895\,\mathrm{Mpc}$ fixed and vary the shift-symmetry chemical potential $\Phi_0 = \mu_c/Q_0$ so $\rho_{\mathrm{dust}}(r) = \frac{\mu^2}{4\pi G}\max(\Phi_0 - \Phi(r), 0)$ vanishes outside the free edge $R_{\mathrm{edge}} \le r_v$ where $\Phi(R_{\mathrm{edge}}) = \Phi_0$, enforcing $M_{\mathrm{dust}} \le 5.36\,M_b(r_v)$ (equality whenever the uncapped $\Phi(r_v) = 0$ solution exceeds supply; unchanged otherwise).
- **Pass gate:** median $R \in [0.80, 1.25]$ AND $\ge 9/12$ clusters in $[0.70, 1.40]$ AND zero cosmic-budget violations.

### Test 2: Untested 4th quadrant — BK potential-depth cluster screen ($S_{\mathrm{cluster}} = 0$, Newtonian) + AeST $n = 1$ polytrope dust
- In the 2×2 matrix `{MOND ON, MOND OFF} × {dust OFF, dust ON}`, the fourth quadrant (cluster MOND screened off via a BK-style potential-depth criterion while keeping AeST's own $\mathcal{K}_2(\mathcal{Q}-Q_0)^2$ dust sector) has not been computed.
- Equation: linear Newtonian Poisson + $n=1$ polytrope dust: $W' = 4\pi G r^2 \rho_b(r) + \mu^2 r^2 \max(\Phi_0 - \Phi(r), 0)$, $\Phi' = W/r^2$, $M_{\mathrm{dyn}}(r) = W(r)/G$.
- Two pre-registered variants (no tuning):
  - **(2a) Uncapped virial-boundary gauge:** $\Phi_0 = \Phi(r_v) = 0$.
  - **(2b) Conserved cosmic-supply free boundary:** $\Phi_0$ fixed so $M_{\mathrm{dust}} \le 5.36\,M_b(r_v)$ at fixed universal $\mu$.
- **Pass gate (evaluated separately for 2a and 2b):** median $R \in [0.80, 1.25]$ AND $\ge 9/12$ clusters in $[0.70, 1.40]$ AND (for 2b, guaranteed; for 2a, reported) zero cosmic-budget violations.

### Test 3: Splashback boundary & Lane–Emden pole test (`d10_attack/README.md` Open Question #2)
- Evaluate the uncapped $\mu_{\mathrm{std}}$ BVP with $\Phi(R_{\mathrm{out}}) = 0$ at splashback radii $R_{\mathrm{out}} = 1.4\,r_{200}$ and $1.8\,r_{200}$ at fixed $\mu = 1/0.9895\,\mathrm{Mpc}$.
- **Decision rule:** Report $\mu R_{\mathrm{out}}/\pi$, convergence count, and $u_E > 0$ count. If $\ge 6/12$ clusters cross the Lane–Emden pole $\mu R_{\mathrm{out}} \ge \pi$ ($R_{\mathrm{out}} \ge 3.109\,\mathrm{Mpc}$) or fail $u_E > 0$ / convergence at $1.4\,r_{200}$, record the uncapped Dirichlet boundary $\Phi(R_{\mathrm{out}}) = 0$ as structurally unstable to replacing $r_v$ by the splashback radius.

### Test 4: ICM outer-slope sensitivity (cored $\beta = 2/3$ vs realistic $\beta = 0.85, 1.0$)
- Re-run Test 1 (`MOND ON` + free-boundary conserved dust) and Test 2b (`MOND OFF` + free-boundary conserved dust) replacing the $r^{-2}$ outer-tail gas profile $\rho_b \propto (1+(r/r_c)^2)^{-3\beta/2}$ at $\beta \in \{2/3, 0.85, 1.0\}$ (each normalized identically to the observed $f_{\mathrm{bar}} M_{500}$ inside $r_{500}$).
- **Reporting:** Report $M_b(r_v)/M_b(r_{500})$, median $R$, and count in $[0.70, 1.40]$ across $\beta$ to separate profile-extrapolation artifacts from intrinsic physics.
