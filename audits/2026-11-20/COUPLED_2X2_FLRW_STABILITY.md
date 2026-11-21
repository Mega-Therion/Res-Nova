# Coupled 2×2 & ADM 4×4 Quadratic Stability Audit for Live AeST ($\mathcal{K}(\mathcal{Q})$)

**Script:** [`coupled_2x2_flrw_stability.py`](file:///home/mega/Chyren/3_research/Res-Nova/audits/2026-11-20/coupled_2x2_flrw_stability.py) · **Receipt:** [`COUPLED_2X2_FLRW_STABILITY.json`](file:///home/mega/Chyren/3_research/Res-Nova/audits/2026-11-20/COUPLED_2X2_FLRW_STABILITY.json)  
**Resolves:** Sub-horizon coupled $2\times 2$ (`CLM-COUPLED2X2`) flagged open in [`coupled_quadratic_stability.py`](file:///home/mega/Chyren/3_research/Res-Nova/audits/2026-11-18/coupled_quadratic_stability.py) · **Action:** $\mathcal{L}_{16\pi} = R - \frac{K_B}{2}F^2 + 2(2-K_B)J^\mu\nabla_\mu\phi - (2-K_B)(1+\lambda_s)\mathcal{Y} + K_1(\mathcal{Q}-\bar{Q}) + \frac{1}{2}K_2^{\mathrm{eff}}(\mathcal{Q}-\bar{Q})^2$, where $K_1 := \mathcal{K}'(\bar{Q})$ and $K_2^{\mathrm{eff}} := \mathcal{K}''(\bar{Q})$ (`$:=` definitions, `$=$` derived equalities).

---

## Summary Table (`[D]`)

| Check | Exact Formula / Measurement | Verdict |
|---|---|---|
| **C1. SZ22 $K_1 = 0$ Calibration** | Newtonian $4\times 4$ `[\Phi, \Psi, \varphi, \alpha]` gives $\det M_{\mathrm{N0}} = -2k^6\omega^2\big[K_2^{\mathrm{eff}}K_B\omega^2 - 4(2-K_B)(1+\frac{1}{2}K_B\lambda_s)k^2 - K_2^{\mathrm{eff}}\bar{Q}^2(2-K_B)(1+\lambda_s)\big]$; at $K_2^{\mathrm{eff}} := 4\mathcal{K}_2$, $c_s^2 = \frac{(2-K_B)(1+\frac{1}{2}K_B\lambda_s)}{\mathcal{K}_2 K_B}$ (`0.867445` at witness) and $M_{\mathrm{gap}}^2\big|_{K_1=0} = \frac{(2-K_B)(1+\lambda_s)\bar{Q}^2}{K_B}$. | `[D]` |
| **C2. Exact Coupled $2\times 2$ & 3-Gauge Invariance** | Fixed-metric `[\varphi, A_x]`, Newtonian $4\times 4$ `[\Phi, \Psi, \varphi, \alpha]`, and unitary ADM $4\times 4$ `[\Phi, B, \Psi, \varphi]` give the exact same UV speeds $\{0,\; c_{s,\mathrm{UV}}^2\}$. On $M(\omega, k)$, $K_{ij} = \operatorname{diag}(\frac{1}{2}K_2^{\mathrm{eff}}, K_B)$, gyroscopic mixing $\pm(2-K_B)k\omega$, and $\omega^4 - (M_{\mathrm{gap}}^2 + c_{s,\mathrm{UV}}^2 k^2)\omega^2 + M_{\mathrm{gap}}^2 c_{s,\mathrm{IR}}^2 k^2 = 0$, with $M_{\mathrm{gap}}^2 = \frac{\bar{Q}(2(2-K_B)(1+\lambda_s)\bar{Q} - K_1)}{2K_B}$, $c_{s,\mathrm{UV}}^2 = \frac{4(2-K_B)(1+\frac{1}{2}K_B\lambda_s)}{K_2^{\mathrm{eff}}K_B}$, and $c_{s,\mathrm{IR}}^2 = \frac{K_1}{K_2^{\mathrm{eff}}\bar{Q}} = \frac{dp_\phi}{d\rho_\phi}$. Transverse $A_y$ obeys $\omega_\perp^2 = k^2 + M_{\mathrm{gap}}^2$. | `[D]` |
| **C3. Stability Window & Power-Law Bound** | When $M_{\mathrm{gap}}^2 < 0$ and $c_{s,\mathrm{IR}}^2 > 0$, $\omega_+^2\omega_-^2 < 0$ for **all** $k > 0$ ($\omega_-^2 \to -|M_{\mathrm{gap}}^2|c_{s,\mathrm{IR}}^2/c_{s,\mathrm{UV}}^2$). Ghost-free + non-tachyonic + subluminal holds iff $0 < K_B < 2$, $K_2^{\mathrm{eff}} \ge \frac{4(2-K_B)(1+\frac{1}{2}K_B\lambda_s)}{K_B}$, and $0 \le \frac{K_1}{2\bar{Q}} \le (2-K_B)(1+\lambda_s)$. For pure $\mathcal{K}(\mathcal{Q}) := c\mathcal{Q}^p$ ($p>1$, $c_{s,\mathrm{IR}}^2 = \frac{1}{p-1}$), $\bar{Q}$ and $c$ cancel out to give $K_B \ge K_{B,\min}(p,\lambda_s) = \frac{2}{(p-1)(1+\lambda_s)-\lambda_s}$. | `[D]` |
| **C4. PR #226 Witness (`K_B = 0.008`, `lambda_s = 11.2787`, `K_2 = 300`) & Trackers** | Pure $Q^3$ needs $K_B \ge 0.150617$ (fails witness **and** BBN $K_B \le 0.10$; needs $\lambda_s \ge 38.0$ at $K_B=0.05$). Pure $Q^4$ needs $K_B \ge 0.078255$ (fails witness; narrow BBN window $K_B \in [0.0783, 0.10]$; needs $\lambda_s \ge 18.5$ at $K_B=0.05$). Combined $2\mathcal{K}_2(\mathcal{Q}-Q_0)^2 + c\mathcal{Q}^3$ has ceiling $48.9183$: at $c=0$, $\frac{\bar{Q}-Q_0}{\bar{Q}} \le 0.040765$; at $\bar{Q}=Q_0$, $c Q_0 \le 16.3061$ gives $c_{s,\mathrm{UV}}^2 \in [0.8021, 0.8674]$ and $c_{s,\mathrm{IR}}^2 \in [0, 0.0377]$, whereas $\bar{Q} \gg Q_0$ forces $M_{\mathrm{gap}}^2 < 0$ unless $\lambda_s$ runs upward with $\bar{Q}$. | `[D]` |

---

## Remaining Open Boundary (`[O]`)
1. Finite-$H/k$ horizon-crossing FLRW ODE transfer functions coupled to $\delta\rho_{\mathrm{rad}}$ with time-dependent $\dot{H}, \dot{\bar{Q}}$.
2. Whether a $\mathcal{Q}$-dependent running $\lambda_s(\mathcal{Q})$ avoids the $\bar{Q} \gg Q_0$ early-universe $M_{\mathrm{gap}}^2 < 0$ tachyon without spoiling the BBN abundance window.
