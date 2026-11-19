# SPARC-175 3-Layer Forward-Model & Distance-Scaling Ablation (`2026-11-19`)

**Script:** `audits/2026-11-19/sparc_forward_model_ablation.py` (exit 0, deterministic, 500x bootstrap `seed=42`, SHA-256 verified CWRU SPARC-175).  
**Receipt:** `audits/2026-11-19/SPARC_FORWARD_MODEL_ABLATION.json`.  
**Tag:** `[D]` / `[E]`.

---

## 1. Bug Identified and Fixed

While PR #143 fixed SPARC distance scaling in `02_galaxy_dynamics/sparc_reproduce.py` and `02_galaxy_dynamics/parameter_ledger.py` ($V_{\text{bar}}^2 \to f_d V_{\text{bar}}^2$, $R \to f_d R$, keeping $g_{\text{bar}} = V_{\text{bar}}^2/R$ invariant), the three $a_0$ re-extraction harnesses (`02_galaxy_dynamics/sparc_a0_reextract_3mu.py`, `sparc_a0_reextract_std.py`, and `scripts/a0_distance_corrected_reextract.py`) never received that fix:

1. `vb2` omitted the `FD` multiplier, making `gbar = vb2 / (FD * r_m)` scale as $1/f_d$ instead of remaining distance-invariant (canceling $f_d$ in the Newtonian limit and halving deep-MOND $a_0$ sensitivity from $f_d^{-2}$ to $f_d^{-1}$).
2. In Treatment `T2` (rescaling the 97 Hubble-flow galaxies from $H_0 = 73$ to Planck $H_0 = 67.4$), `rescaled_copy` scaled only `Rad` by $s = 73/67.4$ while leaving `Vgas`, `Vdisk`, `Vbul` unscaled (missing $\sqrt{s}$).

Both defects are now fixed by default (with `--legacy-buggy-fd` preserved solely for historical forensic reproduction of archived `02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json`) and guarded permanently in `02_galaxy_dynamics/test_sparc_parser.py`.

---

## 2. Step-by-Step Ablation Results (`mu_std`, anchor $cH_0/(2\pi) = 1.0422 \times 10^{-10}\ \mathrm{m\,s^{-2}}$)

| Step | Treatment | $N$ | Fitted $a_0$ ($\mathrm{m\,s^{-2}}$) | 95% Bootstrap CI | Gap vs $cH_0/2\pi$ | Anchor in 95% CI? | Median per-gal $a_0$ |
|---|---|---:|---:|---|---:|:---:|---:|
| **S0** (committed `d34f5c5`, buggy `FD`/`T2`) | T1 all | 175 | `1.1607e-10` | `[9.725e-11, 1.295e-10]` | `+11.37%` | Yes | `1.132e-10` |
| **S0** (exact `+0.00e+00` JSON parity) | T2 flow $\to 67.4$ | 175 | `1.0975e-10` | `[9.264e-11, 1.234e-10]` | `+5.31%` | Yes | `1.083e-10` |
| **S0** | T3 non-flow | 78 | `1.1631e-10` | `[9.664e-11, 1.324e-10]` | `+11.60%` | Yes | `1.132e-10` |
| **S1** (fix ONLY `FD` & `T2` $\sqrt{s}$) | T1 all | 175 | `1.1803e-10` | `[1.006e-10, 1.313e-10]` | `+13.25%` | Yes | `1.083e-10` |
| **S1** | T2 flow $\to 67.4$ | 175 | **`1.0749e-10`** | `[9.130e-11, 1.229e-10]` | **`+3.14%`** | Yes | `1.083e-10` |
| **S1** | T3 non-flow | 78 | `1.1810e-10` | `[9.931e-11, 1.308e-10]` | `+13.31%` | Yes | `1.083e-10` |
| **S2** (S1 + real per-gal `e_D/D`, adaptive) | T1 all | 175 | `1.1205e-10` | `[9.876e-11, 1.294e-10]` | `+7.52%` | Yes | `1.132e-10` |
| **S2** | T2 flow $\to 67.4$ | 175 | `1.1041e-10` | `[9.667e-11, 1.264e-10]` | `+5.94%` | Yes | `1.083e-10` |
| **S2** | T3 non-flow | 78 | `1.1253e-10` | `[9.735e-11, 1.321e-10]` | `+7.97%` | Yes | `1.132e-10` |
| **S3** (S2 + inclination $i \sim \mathcal{N}(\text{Inc}, e_{\text{Inc}})$) | T1 all | 175 | `1.1453e-10` | `[9.933e-11, 1.386e-10]` | `+9.89%` | Yes | `1.132e-10` |
| **S3** | T2 flow $\to 67.4$ | 175 | `1.1269e-10` | `[9.678e-11, 1.356e-10]` | `+8.12%` | Yes | `1.035e-10` |
| **S4** (S3 + `Q < 3` & `Inc >= 30°`) | T1 clean | 153 | `1.1391e-10` | `[9.823e-11, 1.354e-10]` | `+9.29%` | Yes | `1.132e-10` |
| **S4** | T2 clean flow $\to 67.4$ | 153 | `1.1198e-10` | `[9.527e-11, 1.325e-10]` | `+7.44%` | Yes | `1.083e-10` |
| **S4** | T3 clean non-flow | 70 | `1.2533e-10` | `[1.040e-10, 1.584e-10]` | `+20.26%` | Yes | `1.132e-10` |
| **Control** (`30° <= Inc <= 85°`, no edge-on) | T3 non-flow | 60 | `1.2008e-10` | `[1.037e-10, 1.353e-10]` | `+15.22%` | Yes | `1.083e-10` |
| **S5-MLE** (S4 + exact $-2\ln\mathcal{L}$ $\sigma_{\text{int}} = 7\ \mathrm{km/s}$) | T1 clean | 153 | `1.2135e-10` | `[1.041e-10, 1.411e-10]` | `+16.43%` | Yes | `1.181e-10` |
| **S5-MLE** ($\sigma_{\text{int}} = 7\ \mathrm{km/s}$) | T2 clean flow $\to 67.4$ | 153 | `1.1724e-10` | `[1.004e-10, 1.375e-10]` | `+12.50%` | Yes | `1.132e-10` |
| **S5-MLE** ($\sigma_{\text{int}} = 5\ \mathrm{km/s}$) | T3 clean non-flow | 70 | `1.3335e-10` | `[1.080e-10, 1.653e-10]` | `+27.95%` | **No** | `1.132e-10` |

---

## 3. Physical & Statistical Takeaways

1. **The `11.4%` (`f_emp = 1.114365`) gap is inside the SPARC forward-model systematic bandwidth:** Full-sample fitted $a_0$ spans **`1.075` to `1.214 × 10⁻¹⁰ m s⁻²`** (`+3.1%` to `+16.4%`) depending purely on Layer 1b/2 nuisance modeling, with $cH_0/(2\pi) = 1.0422 \times 10^{-10}$ inside the 95% CI of every full-sample treatment (`S0`–`S5`). Attempting a precision holonomy derivation of `1.114365` (`O7`) is chasing a forward-model artifact.
2. **Edge-on leverage & intrinsic scatter:** Adding inclination freedom relaxes moderate-inclination disks while leaving edge-on spirals (`Inc = 88°–90°`, where $\cos i \approx 0$ freezes $\sin i$) to dominate unweighted $\sum \chi^2$ (`NGC0891` `+128.5`, `NGC7814` `+80.1` vs `NGC5907` `-143.6`). Including an exact Gaussian log-likelihood intrinsic scatter term $\sigma_{\text{int}}$ improves $-2\ln\mathcal{L}$ by **`-6,979`** on clean SPARC-153 (peaking at $\sigma_{\text{int}} = 7.0\ \mathrm{km/s}$), while down-weighting low-error dwarfs relative to high-speed spirals and pulling $a_0$ toward `1.17–1.21 × 10⁻¹⁰` (and `1.33 × 10⁻¹⁰` on non-flow `T3`, while the per-galaxy median stays steady at `1.132 × 10⁻¹⁰`).
3. **Solar-System invariance:** None of these SPARC forward-model shifts affects the Park et al. (2026) Cassini $Q_2$ exclusion (`+7.67σ` to `+10.16σ`, see `CASSINI_GE_UNCERTAINTY_BAND.json`) or the `#228` / `#232` screening no-go theorems.
