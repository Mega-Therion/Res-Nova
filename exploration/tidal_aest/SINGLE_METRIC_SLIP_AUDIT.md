# Single-Metric AeST Anisotropic-Stress & Gravitational Slip Audit

**Script:** [`single_metric_slip_audit.py`](file:///home/mega/Chyren/3_research/Res-Nova/exploration/tidal_aest/single_metric_slip_audit.py) · **Receipt:** [`SINGLE_METRIC_SLIP_AUDIT.json`](file:///home/mega/Chyren/3_research/Res-Nova/exploration/tidal_aest/SINGLE_METRIC_SLIP_AUDIT.json)  
**Context:** Resolves the open calculation from [`D42_gw170817_disformal_falsification.md`](file:///home/mega/Chyren/2_knowledge/Chyren_Second_Brain/50_Mathematical_Notation/derivations/D42_gw170817_disformal_falsification.md) ("whether $T^{(\chi)}_{\mu\nu}$'s anisotropic stress reintroduces slip on one shared metric") and evaluates X-COP clusters from [`xcop_data.tsv`](file:///home/mega/Chyren/3_research/Res-Nova/exploration/d10_xcop/xcop_data.tsv).  
**Conventions:** Isotropic static metric $ds^2 = -e^{2\epsilon\Phi(r)}dt^2 + e^{-2\epsilon\Psi(r)}(dr^2 + r^2 d\Omega^2)$; slip $\delta_{\mathrm{slip}} := \Psi - \Phi$; definitions use `$:=$` and derived equalities use `$=$`.

---

## Summary Table

| Sector / Model | Anisotropic Stress & Linear $O(\epsilon)$ Slip | Nonlinear $O(\epsilon^2) = O(v^4/c^4)$ Slip | Status |
|---|---|---|---|
| **S1. Isotropic Einstein Tensor + Schwarzschild control** | $(G^r_{\;r} - G^\theta_{\;\theta})_{O(\epsilon)} = r\frac{d}{dr}\!\left(\frac{\delta_{\mathrm{slip}}'}{r}\right) = -\Phi'' + \Psi'' + \frac{\Phi'-\Psi'}{r}$ | $(G^r_{\;r} - G^\theta_{\;\theta})_{O(\epsilon^2)\big|\Psi=\Phi} = -2(\Phi')^2$; isotropic Schwarzschild ($\Phi = -M/r$, $\Psi = -M/r + M^2/(4r^2)$) vanishes to $O(M^2)$ | `[D]` |
| **S2. Naive standalone deep-MOND scalar $\chi$** (no $J\cdot\nabla\phi$ mixing) | $p_r = +2\rho_\chi$, $p_\theta = -\rho_\chi \implies T^r_{\;r} - T^\theta_{\;\theta} = 3\rho_\chi$; hydrostatic conservation selects $\rho_\chi = C_\chi/r^3$, forcing linear slip $\Phi' - \Psi' = 8\pi G_N r\rho_\chi \implies (\Phi'-\Psi')/\Psi' = 2/\ln(r/r_0) = O(1)$ (and $M_\chi \propto \ln r$, not flat $v_c$) | Already fails at $O(\epsilon)$ (`gamma != 1` and wrong potential) | `[X]` |
| **S3a. Live AeST AQUAL & S3b. Live Tidal-QUMOND AeST** ([`normalization_kb.py`](file:///home/mega/Chyren/3_research/Res-Nova/exploration/tidal_aest/normalization_kb.py)) | Exact identity between both sectors on-shell: $8\pi\tilde{G}(T^r_{\;r}-T^\theta_{\;\theta}) = -K_B(\Phi')^2 - (2-K_B)\Phi'\phi'$; linear slip vanishes identically ($\Psi = \Phi$, $\gamma_{\mathrm{PPN}} = 1$) | Combining with $-2(\Phi')^2$ cancels the $(\Phi')^2$ self-stress identically: $r\frac{d}{dr}\!\left(\frac{\delta_{\mathrm{slip}}'}{r}\right) = (2 - K_B)\Phi' g_N$. Newtonian: $\delta_{\mathrm{slip}} = (1 - \frac{K_B}{2})\frac{G_N^2 M^2}{4r^2}$ (exact Schwarzschild at $K_B=0$). Deep-MOND: $\delta_{\mathrm{slip}} = \frac{2}{3}(1 - \frac{K_B}{2})\frac{v_c^2 G_N M}{r}$ | `[D]` |
| **S4. Empirical bounds (12 X-COP clusters, SPARC, Solar System)** | Linear slip $= 0$ across all regimes | Max X-COP scale at $R_{500}/R_{200}$ (`A2319`): $|\delta_{\mathrm{slip}}/\Phi|_{\mathrm{scale}} = 6.169\times 10^{-6}$ ($K_B=0$) and $4.01\times 10^{-6}$ (deep-MOND $K_B=0.05$). SPARC ($150\,\mathrm{km/s}, 10^{10} M_\odot, 10\,\mathrm{kpc}$): $3.111\times 10^{-8}$. Solar System (1 AU): $2.406\times 10^{-9}$ | `[D]` |

---

## Takeaways for Res-Nova Live Seat
1. **Why naive single-metric $\chi$ fails while live AeST + Tidal-QUMOND succeeds (`[D]`):** Dropping $J\cdot\nabla\phi$ mixing forces a standalone $\chi$ fluid to carry $3\rho_\chi$ anisotropic stress at linear order, breaking $\gamma_{\mathrm{PPN}} = 1$ at $O(1)$. Keeping AeST's $J\cdot\nabla\phi$ mixing (`normalization_kb.py`) makes the scalar stress quadratic *and* cancels the pure-MOND $(\Phi')^2$ self-stress against Einstein's $-2(\Phi')^2$, leaving only the $O(v^4/c^4)$ cross-term $(2-K_B)\Phi' g_N$.
2. **X-COP $R_{200}$ implication (`[D]`):** Across all 12 X-COP clusters, single-metric $O(v^4/c^4)$ gravitational slip is $\le 6.2\times 10^{-6}$ — four orders of magnitude too small to explain the $\sim 21\%$ $R_{200}$ overshoot, while confirming that weak-lensing and hydrostatic X-ray masses match to $\sim 10^{-5}$ on the live single-metric seat.
