# Gate 1 Audit: Cosh Tracker vs. $Q^4$ Through Matter-Radiation Equality (`2026-11-21`)

- **Script:** [gate1_equality_cosh_vs_q4.py](gate1_equality_cosh_vs_q4.py)
- **Receipt:** [GATE1_EQUALITY_COSH_VS_Q4.json](GATE1_EQUALITY_COSH_VS_Q4.json)
- **Verdict:** **Cosh tracker is `[X]` (KILLED).** The stabilized **$Q^4$ radiation tracker (`PR #226` witness with covariant running $\lambda_s(\mathcal{Q})$)** survives cleanly (`[D]`/`[O]`) as the sole cosmological AeST branch earning the full multi-species Boltzmann CMB/MPS fit (`[O]`).

---

## 1. Symbolic & Continuity Verification (`[D]`)

- Extending [flrw_finite_hk_radiation_transfer.py](../2026-11-20/flrw_finite_hk_radiation_transfer.py) with pressureless CDM ($\delta_m' = -\theta_m + 3\Phi'$, $\theta_m' = -\mathcal{H}\theta_m + k^2\Phi$), exact SymPy derivation proves:
  - $E_{h_T}^{(\mathrm{AeST})} \equiv 0$ ($\Psi = \Phi$ identically at linear order), and
  - Exact contracted Bianchi conservation $\frac{d}{d\tau} E_{00} \equiv 0$ and $\frac{d}{d\tau} E_{0x} \equiv 0$ identically with CDM + radiation + arbitrary scalar $\mathcal{K}(\mathcal{Q})$ and $\lambda_s(\mathcal{Q})$.
- Exact `x = 50` continuity regression ($k = 0.2\,\mathrm{Mpc}^{-1}$ against pure-radiation GR): `GR_max_analytic_err = 5.76e-9`, `PR226_Cosh_running_lam` $\Phi/\Phi_{\mathrm{rad,GR}} = 10.493924$, $\delta_r/\delta_{r,\mathrm{rad,GR}} = 0.853832$, and `Q4_PR226_running_lam` $\Phi/\Phi_{\mathrm{rad,GR}} = 0.897430$, reproducing `FLRW_FINITE_HK_RADIATION_TRANSFER.json` identically.
- Why `10.49` appeared at `x = 50`: in `flrw_finite_hk_radiation_transfer.py`, the GR control had $\Omega_m = 0$ (pure radiation, $\Phi_{\mathrm{rad}} \propto x^{-2} = 0.002915$ at $x=50$), whereas Cosh carried $\Omega_{\phi 0} = 0.26$ dust and had already crossed equality ($a(50) = 1.54\,a_{\mathrm{eq}}$). An apples-to-apples test requires integrating to and beyond $a_{\mathrm{eq}} = \Omega_{r0}/\Omega_{\mathrm{dm},0} = 3.4615\times 10^{-4}$ against matched $\Lambda\mathrm{CDM}$ ($\Omega_{m0} = 0.26$).

---

## 2. Equality-Era Transfer ($k = 0.2\,\mathrm{Mpc}^{-1}$, $a \in [a_0, 10\,a_{\mathrm{eq}}]$, Radau Constraints $\le 2.30\times 10^{-8}$)

| Model | $a/a_{\mathrm{eq}} = 0.5$ ($\Phi/\Phi_{\Lambda}$) | $1.0\,a_{\mathrm{eq}}$ ($\Phi/\Phi_{\Lambda}$) | $3.0\,a_{\mathrm{eq}}$ ($\Phi/\Phi_{\Lambda}$) | $10.0\,a_{\mathrm{eq}}$ ($\Phi/\Phi_{\Lambda}$) | $3.0\,a_{\mathrm{eq}}$ ($\delta_{\mathrm{dm}}/\delta_{\mathrm{dm},\Lambda}$) | $10.0\,a_{\mathrm{eq}}$ ($\delta_{\mathrm{dm}}/\delta_{\mathrm{dm},\Lambda}$) | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| `LCDM_matched_Om0p26` ($\Omega_m=0.26$) | `1.0000` | `1.0000` | `1.0000` | `1.0000` | `1.0000` | `1.0000` | Control |
| `PR226_Cosh_running_lam` ($r=10^{-3}$, $c_{s,\mathrm{IR}}^2 \approx 10^{-3}$) | `0.9909` | `0.9352` | **`0.5670`** | **`-0.0342`** | **`0.5708`** | **`-0.0333`** | **`[X]` KILLED** |
| `PR226_Cosh_running_lam_r1e4` ($r=10^{-4}$, $c_{s,\mathrm{IR}}^2 \approx 10^{-4}$) | `0.9991` | `0.9934` | `0.9490` | `0.7806` | `0.9490` | `0.7801` | Damping `-22%` by $10 a_{\mathrm{eq}}$ (`[X]`) |
| `SZ21_Cosh_running_lam` ($r=10^{-2}$) | `0.8629` | **`0.4346`** | **`-0.1023`** | `0.0516` | **`-0.0765`** | `0.0526` | **`[X]` KILLED** |
| **`Q4_PR226_running_lam_with_CDM`** ($\epsilon_Q=0.039$, `PR #226` $K_B=0.008$) | `0.9765` | **`0.9955`** | **`0.9922`** | **`0.9889`** | **`0.9877`** | **`0.9852`** | **SURVIVES (`[D]`/`[O]`)** |

Cross-checks at $k = 0.1$ and $0.05\,\mathrm{Mpc}^{-1}$ show the same behavior (`PR226_Cosh_running_lam` drops to $\Phi/\Phi_{\Lambda\mathrm{CDM}} = 0.5339$ at $10\,a_{\mathrm{eq}}$ for $k=0.1$ and $0.8766$ for $k=0.05$; `SZ21_Cosh` drops to $0.6939$ even at $k=0.05$; **`Q4_PR226_running_lam_with_CDM`** stays within `0.9788–1.0159` on $\Phi/\Phi_{\Lambda\mathrm{CDM}}$ and `0.9814–0.9894` on $\delta_m/\delta_{m,\Lambda\mathrm{CDM}}$ across all tested $k$ and epochs, with $M_{\mathrm{gap}}^2/H^2 \ge 0.409 > 0$ and $c_{s,\mathrm{UV}}^2 \le 0.9616 < 1$).

### Physical Diagnosis
In the Cosh tracker (`r = Z_0/Q_0 = 10^{-3}` at `PR #226`, or `10^{-2}` at `SZ21 Fig 1`), the same infrared sound speed $c_{s,\mathrm{IR}}^2 = K_1/(K_2^{\mathrm{eff}}\bar{Q}) \approx r = 10^{-3}$ drives acoustic Jeans oscillations inside the matter-dominated horizon ($c_{s,\mathrm{IR}} k\tau \sim \mathcal{O}(1\text{--}5)$ at $3\text{--}10\,a_{\mathrm{eq}}$), suppressing $\Phi$ and $\delta_\phi$ by **43%** at $3\,a_{\mathrm{eq}}$ and driving both negative (`-0.034`) by $10\,a_{\mathrm{eq}}$ at $k = 0.2\,\mathrm{Mpc}^{-1}$. Against matched $\Lambda\mathrm{CDM}$ (`1p0_aeq` $\Phi/\Phi_{\Lambda} = 0.9352$, `3p0_aeq` $= 0.5670$), the Cosh tracker fails pre-recombination potential preservation and is marked **`[X]`**. The stabilized $Q^4$ radiation tracker (`Q4_PR226_running_lam_with_CDM`) agrees with $\Lambda\mathrm{CDM}$ to `~1%` across $k \in [0.05, 0.2]\,\mathrm{Mpc}^{-1}$ through $10\,a_{\mathrm{eq}}$ and remains the unique branch earning a full Boltzmann CMB/MPS fit (`[O]`).
