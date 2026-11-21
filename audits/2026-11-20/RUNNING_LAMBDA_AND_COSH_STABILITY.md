# Covariant Running $\lambda_s(\mathcal{Q})$ and Cosh $\mathcal{K}(\mathcal{Q})$ Stability Audit (2026-11-20)

Closes the running-$\lambda_s(\mathcal{Q})$ open boundary from [`COUPLED_2X2_FLRW_STABILITY.json`](COUPLED_2X2_FLRW_STABILITY.json) (`C5`) via symbolic & numerical verification in [`running_lambda_and_cosh_stability.py`](running_lambda_and_cosh_stability.py) (`exit 0`, receipt [`RUNNING_LAMBDA_AND_COSH_STABILITY.json`](RUNNING_LAMBDA_AND_COSH_STABILITY.json)).

## 1. Quadratic-Order Theorem (`[D]`)
Because $\bar{\mathcal{Y}} \equiv 0$ identically on flat FLRW ($\mathcal{Y} = O(\epsilon^2)$), expanding $\mathcal{F}(\mathcal{Y},\mathcal{Q}) \supset (2-K_B)\lambda_s(\mathcal{Q})\mathcal{Y}$ eliminates $\lambda_s'(\bar{Q})$ and $\lambda_s''(\bar{Q})$ identically at $O(\epsilon^2)$:
$$\mathcal{L}^{(2)}_{\mathrm{cross}} = (2-K_B)\,\lambda_s(\bar{Q})\,(\partial_x\varphi + \bar{Q}\,\alpha_x)^2.$$
Hence at quadratic order, any covariant cross-coupling enters solely through the instantaneous background value $\lambda_s(\bar{Q})$, and the gap obeys
$$M_{\mathrm{gap}}^2(a) = \frac{(2-K_B)(1+\lambda_s(\bar{Q}))\bar{Q}^2 - 3(1+w_\phi)\Omega_\phi H^2}{K_B}.$$

## 2. Universal Existence Criterion (`[D]`)
Requiring non-tachyonic $M_{\mathrm{gap}}^2 \ge 0$ and UV subluminality $c_{s,\mathrm{UV}}^2 \le 1$ ($0 < K_B < 2$, $K_2^{\mathrm{eff}} > 0$, $\bar{Q} > 0$) traps $\lambda_s(\bar{Q})$ inside
$$\lambda_{\min}(\bar{Q}) := \frac{K_1(\bar{Q})}{2(2-K_B)\bar{Q}} - 1 \;\le\; \lambda_s(\bar{Q}) \;\le\; \frac{K_2^{\mathrm{eff}}(\bar{Q})}{2(2-K_B)} - \frac{2}{K_B} =: \lambda_{\max}(\bar{Q}).$$
This interval is non-empty **if and only if**
$$K_2^{\mathrm{eff}}(\bar{Q}) - \frac{K_1(\bar{Q})}{\bar{Q}} = K_2^{\mathrm{eff}}(\bar{Q})\big(1 - c_{s,\mathrm{IR}}^2(\bar{Q})\big) \;\ge\; \frac{2(2-K_B)^2}{K_B}.$$

## 3. Model-by-Model Verdicts (`[D]` / `[X]`)

| $\mathcal{K}(\mathcal{Q})$ candidate | Constant $\lambda_s$ | Running $\lambda_s(\mathcal{Q})$ | Key obstruction / witness |
|---|---|---|---|
| Stiff $p=2$ ($U = c\mathcal{Q}^2$) | `[X]` ($c_{s,\mathrm{UV}}^2 \le 1$ conflicts) | `[X]` everywhere | $K_2^{\mathrm{eff}} - K_1/\bar{Q} = 0$ identically ($c_{s,\mathrm{IR}}^2 = 1$). |
| Pure shifted quadratic ($2\mathcal{K}_2(\mathcal{Q}-Q_0)^2$) | `[X]` above $(\bar{Q}-Q_0)/\bar{Q} = 0.0408$ | `[X]` at $\bar{Q} \gg Q_0$ | Closes at $\bar{Q}/Q_0 = 1.2097$ (PR #226 witness $K_B=0.008, \mathcal{K}_2=300$). |
| Unshifted dust + tracker ($2\mathcal{K}_2(\mathcal{Q}-Q_0)^2 + c\mathcal{Q}^4$) | `[X]` | `[X]` at PR #226 scale | AM–GM dip requires $c Q_0^2 \ge 12.55\,\mathrm{Mpc}^{-2}$ vs. no-overclosure cap $c Q_0^2 \le 7.92\times 10^{-6}\,\mathrm{Mpc}^{-2}$ ($1.59\times 10^6\times$ gap; overcloses today by $4.1\times 10^5\times$). |
| **Cosh** ($2\mathcal{K}_2\mathcal{Z}_0^2[\cosh\mathcal{Z}-1]$) | `[D]` early $M_{\mathrm{gap}}^2 < 0$ (explains `TARGET_D5` §3.5's $\sim 1.9/e$-fold mode at SZ21 Fig 1; $\gamma_{k=0}/H = 8.20$ at PR #226 $a=10^{-4}$) | **`[D]` Globally Healthy** | $K_2^{\mathrm{eff}} - K_1/\bar{Q} \ge 4\mathcal{K}_2(1-r) = 1198.8 > 992.0 = \frac{2(2-K_B)^2}{K_B}$. Explicit ansatz $\lambda_s(\mathcal{Q}) := \lambda_{s,0} + \frac{\mathcal{K}_2}{2-K_B}(\cosh\mathcal{Z}-1)$ keeps $M_{\mathrm{gap}}^2/H^2 > 0$ and $0 \le c_{s,\mathrm{IR}}^2 < c_{s,\mathrm{UV}}^2 \in [0.50, 0.8674] < 1$ across $a \in [10^{-10}, 1]$ with BBN $G_{\mathrm{cosmo}}/G_N$ untouched ($\bar{\mathcal{Y}}=0$) and $|\delta\lambda_s/\lambda_s| = 6.68\times 10^{-6}$ in SPARC galaxies (`0.00267` in X-COP). |
