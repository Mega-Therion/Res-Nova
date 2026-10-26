# SPARC x < 0.1 Outermost Disk Signed Residual Audit

**Date:** 2026-10-26  
**Script Provenance:** `1_engine/Codebase/python/chyren/cosmo/sparc_residual_vs_x.py`  
**Dataset:** SPARC 175 galaxies (`SPARC_175_GOD_fits.csv` + `*_rotmod.dat`)  
**Acceleration Cut:** $x = g_{\text{bar}} / a_0 < 0.1$ ($N = 1084$ data points)  
**Model Inversion:** $g \cdot \mu(g/a_0) = g_{\text{bar}}$ with Lean projection cosine $\mu(y) = y / \sqrt{1 + y^2}$. $\Upsilon_\star$ and $\mu$ frozen.

---

## 1. Executive Summary & Full Accounting ($N = 1084$)

The aggregate signed residual in the outermost acceleration bin ($x < 0.1$) is **$-6.48\%$**. Partitioning by gas fraction $f_{\text{gas}} \equiv v_{\text{gas}}^2 / v_{\text{bar}}^2$ confirms that this negative offset is driven entirely by the gas-dominated radii, while the star-dominated population is centered near zero with symmetric dispersion.

| Population | Definition | Points ($N$) | Signed Median | 16th Percentile | 84th Percentile |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Star-dominated** | $f_{\text{gas}} < 0.5$ (incl. $f_{\text{gas}} < 0$) | **598** | **−1.83%** | **−20.16%** | **+17.36%** |
| **Gas-dominated** | $f_{\text{gas}} \ge 0.5$ | **486** | **−13.79%** | **−34.63%** | **+11.98%** |
| **Complete Bin** | $x < 0.1$ | **1084** | **−6.48%** | **−28.75%** | **+15.54%** |

*Note on Hollow Gas Rows:* 56 points have $v_{\text{gas}} < 0$ in the rotmod tables (negative gas potential contribution, $f_{\text{gas}} < 0$). These sit inside the 598 star-dominated points. Their isolated median is $-7.27\%$ (16th: $-57.79\%$, 84th: $+11.53\%$). $598 + 486 = 1084$.

---

## 2. Gas Fraction Escalation Across $0 \le f_{\text{gas}} < 1$ ($N = 1028$)

| $f_{\text{gas}}$ Interval | Points ($N$) | Signed Median | 16th Percentile | 84th Percentile |
| :--- | :---: | :---: | :---: | :---: |
| $[0.0, 0.2)$ | 153 | **−3.71%** | −29.02% | +16.88% |
| $[0.2, 0.4)$ | 242 | **−1.54%** | −16.28% | +16.82% |
| $[0.4, 0.6)$ | 284 | **−5.38%** | −23.95% | +16.74% |
| $[0.6, 0.8)$ | 186 | **−10.98%** | −42.62% | +16.39% |
| $[0.8, 1.0)$ | 163 | **−17.80%** | −31.60% | +1.77% |

### Exact Partition of the Pure-Gas Bin ($f_{\text{gas}} \in [0.8, 1.0)$, $N = 163$):
* $v_{\text{cos}} > v_{\text{obs}}$ ($\text{residual} < 0$): **130 / 163 = 79.75%**
* $0 \le \text{residual} \le +1.77\%$: **7 / 163 = 4.29%**
* $\text{residual} > +1.77\%$: **26 / 163 = 15.95%**
* Sum: $130 + 7 + 26 = 163$.

---

## 3. Epistemic Invariants `[D]`

1. **Cosine Asymptotic Is Centered on Stars:**  
   The median of the 598 star-dominated points is $-1.83\%$. The pointwise spread is $[-20.16\%, +17.36\%]$ (a centered distribution with $\sim 20\%$ scatter, not a 2% pointwise fit).
2. **Systematic Overprediction Tracks Gas:**  
   The $-6.48\%$ aggregate bias is localized to $f_{\text{gas}} \ge 0.5$ (median $-13.79\%$) and reaches $-17.80\%$ in $f_{\text{gas}} \ge 0.8$ with a $79.75\%$ overprediction rate.
3. **Physical Scale of the Deficit:**  
   Helium mass-fraction uncertainty ($1.33 \to 1.40$) moves $v_{\text{cos}}$ by only $\sim 1\%$, an order of magnitude smaller than the observed $-17.80\%$ median offset. Inclination and the SPARC quality flag do not move the pure-gas median. Distance method does. The gate in section 4 is the closure test. Ionization remains untested.
4. **Parameter Invariant:**  
   $\Upsilon_\star$ and $\mu(y) = y/\sqrt{1+y^2}$ remain frozen.

---

## 4. Distance Gate

`v_cos` scales as `sqrt(fd)` in this pipeline. The compromise `fd` is the value that sets the geometric mean of the gas median and the stellar median of `f = v_cos/v_obs` to 1. Gas is `x < 0.1` and `f_gas >= 0.8`. Stars are `x < 0.1` and `f_gas < 0.5`.

A galaxy with both components closes only when both medians then lie in `[0.95, 1.05]`. A galaxy with no stellar points in the cut closes on the gas median alone. The fit grid `[0.85, 1.15]` is not widened.

TRGB or Cepheid: 6 of 11 close. The three both-component closures (IC2574, UGC04483, UGC07559) need `fd` of 0.799, 0.718, and 0.583, all below the grid. No both-component closure sits inside the grid. Five stay open as two-component residuals: NGC3741, DDO154, UGCA444, NGC2366, UGC04305.

Hubble flow: 4 of 12 close. UGC05005 and DDO170 close on both components at `fd` 0.754 and 0.765, outside the grid. DDO161 and KK98-251 are gas-only. Eight stay open. The same two-component failure appears in both distance methods.

Inside the four galaxies with the largest gas-star split, stars exist only in the inner radial bin. UGCA444 gas stays near `f = 1.11` to `1.19` at every fractional radius while its three inner stellar points sit at `0.843`. DDO154 gas stays at `1.00` across radius; its one stellar point is `1.246`. NGC2366 gas rises from `1.081` inside `0.5 R_max` to `1.324` outside `0.8 R_max`, with six inner stellar points at `1.351`. UGC04305 has one outer gas point at `2.082` and inner stellar points at `1.247`.

This sector stops on that gate. A wider `fd` search is not the next fit. Where the two medians already disagree, one distance factor moves both the same way.

## 5. Same-Radius Check

`same_radius_overlap` keeps a radial bin only when that galaxy has at least one gas point and one star point inside it. Gas remains `x < 0.1` and `f_gas >= 0.8`. Stars remain `x < 0.1` and `f_gas < 0.5`. The 23 galaxies are the section 4 sets. No `fd` retune.

Five bins qualify, all of them `[0, 0.5)`. No galaxy has both components in `[0.5, 0.8)` or in `[0.8, 1]`. Eighteen of the 23 galaxies have no shared bin.

| Galaxy | Method | n gas | n star | f gas | f star | Sides of 1 |
|---|---|---|---|---|---|---|
| NGC3741 | TRGB/Cepheid | 3 | 3 | 0.8115 | 0.9298 | both low |
| DDO154 | TRGB/Cepheid | 2 | 1 | 1.0001 | 1.2456 | gas inside `[0.95, 1.05]`, star high |
| UGCA444 | TRGB/Cepheid | 13 | 3 | 1.1532 | 0.8432 | opposite |
| NGC2366 | TRGB/Cepheid | 2 | 6 | 1.0812 | 1.3509 | both high |
| DDO170 | Hubble flow | 1 | 1 | 1.0969 | 1.2128 | both high |

One of the five shared bins has the two medians on opposite sides of 1. The galaxy-level gas-versus-star split in section 4 compares different radii for the other 18 galaxies. The same-radius subset does not turn that split into a single inner-disk rule.
