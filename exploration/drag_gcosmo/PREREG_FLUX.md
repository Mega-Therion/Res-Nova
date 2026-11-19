# Pre-registration: 5D Israel–Codazzi + Vaidya bulk-flux, NEC, and Weyl backreaction test for drag variable-G cosmology (2026-11-19, before any number)

**Context.** `exploration/drag_gcosmo/` (`#247`, `#252`) established:
- Phenomenology (`[E]`): $H^2(a) = H_0^2(\Omega_m a^{-3} + \Omega_r a^{-4} + \Omega_\Lambda)/(1 + x_0 a^2)$ is favoured on DESI DR2 BAO + compressed CMB + Pantheon+ ($\Delta\chi^2 = -6.54$, $x_0 = 0.32$; $-6.24$ with $f\sigma_8$) and DES-Dovekie ($\Delta\chi^2 = -8.72$, $x_0 = 0.35$).
- Zero-flux wall (`[X]`): With $\Delta T_{rn} = 0$, the drag tension $\sigma = \sigma_0 + \frac{1}{2}\rho_b\dot{a}^2$ has adiabatic sound speed $c_s^2 < 0$ across $93.4\%$ of $z < 10$.
- Surviving `[O]` question: *"The drag model survives only if energy flows across the wall ($\Delta T_{rn} \neq 0$). ... a flux-fed wall is `[O]`."*

This pre-registration tests whether a physically consistent bulk energy flux ($\Delta T_{rn} \neq 0$) obeying the 5D Null Energy Condition (NEC) and the exact 5D AdS-Vaidya Israel–Codazzi / 4D Bianchi conservation laws can realize the drag cosmology without instability or destructive Weyl dark-radiation backreaction.

## Symbolic derivation (SymPy, exact 5D AdS-Vaidya + Israel–Codazzi)
- **(S1)** Compute the exact 5D Einstein tensor $G_{MN}$ of the flat-sliced 5D AdS-Vaidya metric $ds^2 = -f(r, v)\,dv^2 + 2\epsilon\,dv\,dr + r^2 d\mathbf{x}^2$, $f(r,v) = k^2 r^2 - \mu(v)/r^2$ ($\epsilon = \pm 1$), and derive the exact 5D NEC condition on $\dot{\mu}_\pm$ for ingoing/outgoing null fluxes across a Dark Bubble ($k_- > k_+$).
- **(S2)** Derive from the low-energy Dark Bubble Friedmann + Raychaudhuri equations (and verify against the 5D Codazzi equation) the exact coupled Weyl dark-radiation backreaction equation for a stable barotropic drag fluid $\Sigma = \Sigma_0 + \Delta\Sigma_{\mathrm{drag}}$, $P_{\mathrm{wall}} = -\Sigma_0 + w_d\,\Delta\Sigma_{\mathrm{drag}}$ ($c_s^2 = w_d \in [0, 1]$):
  $$\dot{\Sigma} + 3H(\Sigma + P_{\mathrm{wall}}) = \mathcal{Q}_4, \qquad \dot{\rho}_{\mathrm{Weyl}} + 4H\rho_{\mathrm{Weyl}} = \mathcal{Q}_4,$$
  so the net wall+Weyl contribution $\rho_{\mathrm{net}} \equiv \rho_{\mathrm{Weyl}} - \Delta\Sigma_{\mathrm{drag}}$ satisfies
  $$\frac{d}{dt}\left(a^4 \rho_{\mathrm{net}}\right) = (3 w_d - 1) a^4 H\,\Delta\Sigma_{\mathrm{drag}}.$$

## Pre-registered numerical tests

### Test F1: Required bulk flux & 5D NEC sign on the best-fit drag trajectory
- Evaluate $\mathcal{Q}_4(z)$ and its dimensionless NEC sign factor $s_{\mathrm{NEC}}(z) = \frac{3}{2}(1 + w_d) - q(z)$ across $z \in [0, 10]$ on the Pantheon+ (`DRAG_FIT.json`) and DES-Dovekie (`DOVEKIE_RERUN.json`) best-fit trajectories for $w_d \in \{0, 1/6, 1/3, 2/3, 1\}$.
- **Decision rule:** NEC-compatible energy inflow requires $\mathcal{Q}_4(z) \ge 0$ (or pure outflow $\mathcal{Q}_4(z) \le 0$ without sign-flipping if sourced by one monotonic null channel). Report whether $\mathcal{Q}_4(z)$ is strictly positive for all $z \in [0, 10]$ and check early-universe radiation safety ($\Delta\rho_{\mathrm{Weyl}}/\rho_r$ at $z_* = 1089.9$ and $z_{\mathrm{BBN}} = 10^9$ against $\Delta N_{\mathrm{eff}} < 0.3$).

### Test F2: Self-consistent coupled Friedmann + Weyl backreaction refit on DESI DR2 + Pantheon+ + CMB (and DES-Dovekie)
- Because nonzero bulk flux $\mathcal{Q}_4 \neq 0$ MUST source $\rho_{\mathrm{Weyl}}(a)$ by the 5D Gauss–Codazzi / 4D Bianchi identity, solve the exact self-consistent coupled system for $E(a)^2$ and $\Omega_{\mathrm{net}}(a) = \rho_{\mathrm{net}}(a)/\rho_{\mathrm{crit},0}$ with $\Delta\Sigma_{\mathrm{drag}}/\rho_{\mathrm{crit},0} = x_0 a^2 E(a)^2$ and $\Omega_{\mathrm{net}}(a \to 0) \to 0$ (no unphysical singular initial dark radiation):
  $$E(a)^2 = \Omega_m a^{-3} + \Omega_r a^{-4} + \Omega_\Lambda + \Omega_{\mathrm{net}}(a), \qquad \frac{d}{da}\left(a^4 \Omega_{\mathrm{net}}\right) = (3 w_d - 1) x_0 a^5 E(a)^2,$$
  with $\Omega_\Lambda$ fixed by $E(1) = 1$, across fixed stable barotropic equations of state $w_d \in \{0, 0.1, 0.2, 1/3, 0.5, 1.0\}$.
- Fit $(h, \Omega_m, x_0)$ using the **exact** `drag_fit.py` (DESI DR2 + Pantheon+ + compressed CMB, plus $+f\sigma_8$) and `dovekie_rerun.py` (DES-Dovekie) likelihoods.
- **Pre-registered verdict rule:**
  - **SURVIVES (flux-fed viable):** There exists a physically stable barotropic value $w_d \in [0, 1]$ with $x_0 > 0$, 5D NEC satisfied ($\mathcal{Q}_4(z) \ge 0$ everywhere), $\Delta N_{\mathrm{eff}}(z_*, z_{\mathrm{BBN}}) < 0.05$, AND self-consistent $\Delta\chi^2 \le -4.0$ against $\Lambda$CDM on BAO + Pantheon+ + CMB + $f\sigma_8$ (with $x_0 = 0$ outside $2\sigma$).
  - **CONFORMALLY CANCELLED / ATTENUATED / EXCLUDED:** Report exact $\Delta\chi^2(w_d)$ and whether Weyl backreaction kills the $\Delta\chi^2 \le -4$ preference (or preserves it only in $w_d \in [0, 1/3)$ with a distinct effective drag law!).
