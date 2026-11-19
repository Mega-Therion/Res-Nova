# 🌌 Target O1: First-Principles Horizon Acceleration Scale Derivation & KMS $2\pi$ Cancellation Audit

> **Tier relabelled 2026-10-09: O1 is [A]; [O], not [P].** Under the [P] rule a declared input is an axiom [A] (`docs/EPISTEMIC_TIER_LEGEND.md`), and the 2π identity is [O]. The closure below is unchanged.
>
> **✅ STATUS 2026-09-27: O1 → [P] under the two-irreducible-parameters accounting.** RY's framework declares
> two inputs. Input 1 is the scale a₀, a *boundary condition anchored to cH₀*; input 2 is μ. "Not derived" is
> not a defect for a declared input. The identification a₀ = cH₀/2π is therefore the framework's declared
> anchor, and what O1 must establish is in place:
> - **The normalisation is declared, not proved (corrected 2026-09-30).** This bullet previously read
>   "the 2π comes from the KMS cancellation". It does not: `HorizonScale.lean` proves that equating the
>   Unruh and Gibbons–Hawking temperatures gives a = cH, with the 2π *cancelling* (ξ = 1, [P]). The
>   anchor a₀ = cH₀/2π is a factor 2π away from that result; the divisor is the heuristic `[O]` row of
>   the table in §2.B below. The H₀ inversion that follows holds only given the declared 2π.
> - **The anchor is supported empirically.** μ_std extractions from `02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json`
>   give a₀ = 1.161 (all 175 galaxies), 1.098 (flow distances rescaled to Planck) and 1.163 (78 non-flow
>   galaxies; 95% [0.966, 1.324]) × 10⁻¹⁰ m/s².
> - Inverted through a₀ = cH₀/2π, those give H₀ ≈ 71–75 km/s/Mpc, which brackets the measured 67.4 (Planck)
>   and 73 (SH0ES). Both sit inside the 95% interval. The anchor is external: H₀ is measured in a different
>   domain, not fitted to the galaxies it explains.
> - The superseded 1.116 value (μ_dual-era `A0_MEASUREMENT.json`) is not used.
> - **The dynamical extension is a separate test.** Whether a₀ tracks H(z) is O4's question, and the real
>   data are inconclusive (`03_observer_jwst/O4_REAL_DATA_MUSE_DARK_III_2026-09-27.md`).
> - **A covariant derivation of a₀ from an action is a research question, not an O1 gap** (paper §12).


**Document Status:** Formal Mathematical Analysis & Epistemic Audit  
**Author / Investigator:** R.W. Yett
**Lean 4 Formal Proof:** [`05_lean_formalization/HorizonScale.lean`](file:///05_lean_formalization/HorizonScale.lean) (`kms_cancellation_equilibrium`, `horizon_acceleration_ratio_is_one`, `verlinde_entropic_cancellation`)  
**Epistemic Taxonomy:** `[P]` (Formal algebraic proof of $2\pi$ cancellation) / `[O]` (Horizon-scale identification with SPARC $a_0$)  

---

## 1. Thermodynamic & Holographic Setup (Stated Action and Equilibrium Condition)

### A. Cosmological Apparent Horizon Setup
Consider a spatially flat FLRW universe with time-dependent Hubble parameter $H(t) \equiv \dot{a}/a$. The cosmological apparent horizon radius is:
$$R_H = \frac{c}{H}.$$

Under quantum field theory in curved spacetime (Gibbons & Hawking 1977), the cosmological horizon radiates at the characteristic Gibbons-Hawking thermal temperature:
$$T_{\text{GH}} = \frac{\hbar H}{2\pi k_B}.$$

### B. Accelerated Observer Horizon Setup
Consider a test mass or physical observer subject to local proper acceleration $a$. In the frame of this observer, a local Rindler acceleration horizon forms with associated Davies-Unruh thermal radiation (Davies 1975; Unruh 1976):
$$T_U = \frac{\hbar a}{2\pi c k_B}.$$

### C. Stated Thermal Equilibrium Condition
The foundational thermodynamic hypothesis posited to link cosmological expansion to galactic kinematics is that the local acceleration scale $a$ reaches a non-Newtonian transition when the local Unruh horizon temperature balances the background cosmological Gibbons-Hawking horizon temperature:
$$T_U = T_{\text{GH}}.$$

---

## 2. Formal Derivation & Exact $2\pi$ Cancellation

### A. The Algebraic Evaluation
Substituting the exact expressions for $T_U$ and $T_{\text{GH}}$ into the equilibrium condition:
$$\frac{\hbar a}{2\pi c k_B} = \frac{\hbar H}{2\pi k_B}.$$

Multiplying both sides by the non-zero common factor $\frac{2\pi k_B}{\hbar}$:
$$\frac{a}{c} = H \implies a = c H.$$

### B. The $2\pi$ Cancellation Theorem
The universal KMS (Kubo-Martin-Schwinger) periodicity factor $2\pi$ appears in the denominator of **both** thermal Green's functions because both horizons share Euclidean time periodicity $\beta = 2\pi/\kappa$, where $\kappa_U = a/c$ and $\kappa_{\text{GH}} = H$. Consequently, the $2\pi$ factors cancel identically:

$$\xi_{\text{derived}} \equiv \frac{a}{c H} = 1.$$

```
========================================================================================================
EQUILIBRIUM FORMULATION           STATED EQUATION                         DERIVED COEFFICIENT ξ = a / (cH)
========================================================================================================
Unruh-de Sitter Balance           ħ a / (2π c kB) = ħ H / (2π kB)         ξ = 1.0  [P] (2π cancels)
Verlinde Entropic Force           F Δx = 2π kB T (mc/ħ) Δx, T=T_GH        ξ = 1.0  [P] (2π cancels)
Padmanabhan Surface Gravity       a = κ_horizon = c H                     ξ = 1.0  [P] (No 2π denominator)
Postulated Horizon Normalization  a_0 = c H / (2π)                        ξ = 1/(2π) ≈ 0.159  [O] (Heuristic divisor)
========================================================================================================
```

### C. Machine-Checked Proof in Lean 4
This result is formalized without heuristics or shortcuts in [`05_lean_formalization/HorizonScale.lean`](file:///05_lean_formalization/HorizonScale.lean):
- `kms_cancellation_equilibrium`: Proves `unruh_temp hbar a c kB = gibbons_hawking_temp hbar H kB ↔ a = c * H` $\mathbf{[P]}$.
- `horizon_acceleration_ratio_is_one`: Proves `a / (c * H) = 1` $\mathbf{[P]}$.
- `verlinde_entropic_cancellation`: Proves `(2 * π * kB * T_GH * c) / ħ = c * H` $\mathbf{[P]}$.

All proofs compile cleanly (`RESULT: PASS`) under standard foundational axioms `[propext, Classical.choice, Quot.sound]`.

---

## 3. Comparison with Empirical SPARC Measurement

The derived first-principles thermodynamic output is:
$$a_{\text{pred}} = 1.0 \cdot c H_0.$$

Evaluating this prediction with cosmological parameters frozen at $H_0 = 67.4\text{ km s}^{-1}\text{ Mpc}^{-1} \approx 2.1843 \times 10^{-18}\text{ s}^{-1}$ and $c = 2.99792458 \times 10^8\text{ m s}^{-1}$:
$$a_{\text{pred}} = (2.99792458 \times 10^8\text{ m s}^{-1}) \times (2.1843 \times 10^{-18}\text{ s}^{-1}) \approx \mathbf{6.548 \times 10^{-10}\text{ m s}^{-2}}.$$

### Empirical Comparison:
- **Measured SPARC acceleration (`A0_MEASUREMENT.json`):**
  $$a_0^{\text{SPARC}} = (1.116 \pm 0.128_{\text{stat}} \pm 0.097_{\text{syst}}) \times 10^{-10}\text{ m s}^{-2} = (1.116 \pm 0.161) \times 10^{-10}\text{ m s}^{-2}\quad (\pm 14.4\%).$$
- **Ratio / Discrepancy:**
  $$\frac{a_{\text{pred}}}{a_0^{\text{SPARC}}} = \frac{6.548 \times 10^{-10}}{1.116 \times 10^{-10}} \approx \mathbf{5.867}.$$
  $$\text{Relative Error} = \frac{6.548 - 1.116}{1.116} = \mathbf{+486.7\%} \quad (\approx 33.7\sigma\text{ miss}).$$

### Epistemic Assessment:
The derived first-principles thermodynamic horizon scale ($\xi = 1$) misses the empirical SPARC acceleration $a_0$ by a factor of $\approx 5.87$, failing the $14.4\%$ empirical bound. Inserting an extra divisor of $2\pi$ yields $a_0 = \frac{cH_0}{2\pi} \approx 1.042 \times 10^{-10}\text{ m s}^{-2}$ (which matches $a_0^{\text{SPARC}}$ within $0.46\sigma$ / $\xi_{\text{SPARC}} = 0.170 \pm 0.025$), but this divisor **does not arise from the action or thermal equilibrium**.

**Literature note:** the $\approx 2\pi$ (or $\approx 6$) normalization is not a divisor invented for this fit — it is the form independently reported across the MOND literature for over a decade: Milgrom (2015, *Phys. Rev. D* 91, 044009) states $a_0 \approx cH_0/2\pi$ explicitly when discussing $a_0$'s secular time-variation; Sanders (2019, *MNRAS* 485, 513) independently reports $a_0 \approx cH_0/6$; Milgrom's review (2020, arXiv:2001.09729, "The $a_0$–cosmology connection in MOND") surveys the full family of order-unity normalizations ($cH_0$, $c^2\Lambda^{1/2}$, $c^2/U$) without settling on one. So this repo's $\xi \approx 1/2\pi$ finding **reproduces the literature's standard framing of the coincidence**, not an ad hoc correction. What genuinely is new here — and remains `[O]` — is that Theorem A shows the $2\pi$ does not fall out of the Unruh/Gibbons-Hawking thermal-equilibrium action itself; the field has long noted the numerical coincidence without deriving the normalizing factor from first principles either.

Therefore, Theorem A confirms mathematically that **the $2\pi$ divisor is NOT derived** from horizon thermodynamics (`[P]`), and the relation $a_0 = \xi c H_0$ remains an open phenomenological hypothesis (`[O]`) whose empirical validity must be decided by redshift evolution (Workstream B). Note that the *direction* of that evolution is itself a fork, not a foregone conclusion: $a_0 \propto H(z)$ (kinematic, $n \approx 1.5$ in the matter era) and $a_0 \propto \sqrt{\Lambda}$ (anthropic, $n = 0$ exactly) are opposite predictions. See §4.

## 4. The Anthropic Branch: A Severable Module for the $a_0(z)$ Fork

**Tiers: `[P]` on the algebra, `[D]` on the implication, `[O]` on the selection premise.** This section adds **no new postulate**. It resolves an ambiguity already present in the anchor, and it is deliberately constructed so it can be deleted without disturbing anything else.

### A. The ambiguity in the anchor

The declared anchor $a_0 = cH_0/2\pi$ writes $H_0$ as "the Hubble rate" without specifying *which* rate. Two readings exist and they are not equivalent:

- **(i) Kinematic.** $H_0$ stands for $H(z)$, the expansion rate at the epoch in question. Then $a_0$ evolves, and in the matter era $a_0 \propto (1+z)^{3/2}$.
- **(ii) Anthropic.** $H_0$ is today's fixed rate, and since $H_0 = c\sqrt{\Lambda/3}$ in a flat $\Lambda$-dominated universe, $a_0 \propto \sqrt{\Lambda}$. Because $\Lambda$ is constant, $a_0$ is constant.

The closing sentence of this document adopts (i) implicitly. This section makes (ii) explicit so that the two branches can be discriminated rather than assumed. **That is the entire role of the anthropic principle here: it is the named alternative, not a foundation.**

### B. The module

Three lines, each already established elsewhere in the corpus:

$$H_0 = c\sqrt{\Lambda/3} \quad (\text{flat, } \Lambda\text{-dominated today, } [D])$$
$$a_0 = cH_0/2\pi \quad (\text{declared anchor, } [A] \text{ per §0})$$
$$\Longrightarrow \; a_0 \propto \sqrt{\Lambda} \quad \text{and hence} \quad n = 0 \text{ exactly, where } a_0 \propto (1+z)^n$$

One input ($\Lambda$), one output ($n = 0$). The $2\pi$ is carried through untouched.

### C. Severability test

Delete this section and ask what breaks. If **only** the $n = 0$ prediction falls, the module is correctly confined. If the $2\pi$, $\mu_{\text{std}}$, $F_{\text{std}}$, the SPARC fit, or the dark-matter question also move, the module has overreached and should be cut back. This is the operational meaning of "not more than enough."

### D. What the anthropic branch must not be allowed to touch

- **The $2\pi$.** Theorem A (`[P]`) shows the divisor cancels in the Unruh / Gibbons–Hawking equilibrium ($\xi = 1$). No selection argument produces a coefficient. Anthropic reasoning **bounds**; it does not **compute**.
- **The $\approx 11\%$ offset.** A Weinberg-type structure-formation bound admits $\rho_\Lambda$ up to roughly $10$–$10^3\times$ the observed value, hence $a_0$ up to $3.2$–$31.6\times$ observed. That is a statement about the *scale*. The observed offset ($1.0422$ vs $1.1607 \times 10^{-10}$) is $11\%$ and needs $1.11$ accuracy — two orders of magnitude tighter than selection can deliver. **Any claim that the anthropic principle explains the offset is `[X]`.**
- **$\mu_{\text{std}}$, $F_{\text{std}}$, and the $n=2$ root.** These are geometric (`audits/2026-11-19/postulate_r_membrane_derivation.py`: $\mu_{\text{std}} = \sin\theta$ is the membrane tilt sine, $F_{\text{std}}$ the Legendre transform of the antiderivative of the DBI area element). Not selection.
- **Dark matter versus MOND.** Whether $a_0$ is selected says nothing about whether MOND replaces dark matter. That is decided by SPARC, clusters and lensing, empirically.
- **The value of $\Lambda$ itself.** Weinberg's problem, not this repository's.

### E. The fork

| $z$ | $a_0 \propto H(z)$ total | $a_0 \propto \sqrt{\Lambda}$ |
|---|---|---|
| 0 | $1.042\times10^{-10}$ | $1.042\times10^{-10}$ |
| 1 | $2.948\times10^{-10}$ | $1.042\times10^{-10}$ |
| 2 | $5.416\times10^{-10}$ | $1.042\times10^{-10}$ |
| 3 | $8.338\times10^{-10}$ | $1.042\times10^{-10}$ |

The anthropic branch is **sharper** than the kinematic one: it predicts $n = 0$ *exactly*, not approximately. The kinematic branch predicts $n \approx 1.5$ in the matter era. These are opposite, not a continuum.

### F. Current data status — do not score this yet

From `audits/2026-11-18/a0z_zgt15_manifest.py` (exit 0), fits of $\ln a_0 = c + n\ln E(z) + b(\log M_{\text{bar}} - 10.5)$:

| sample | $N$ | $n$ | 95% CI | $\Delta\chi^2$ |
|---|---|---|---|---|
| full | 51 | $-0.745$ | $[-2.25,\ 0.92]$ | $6.08$ (2.47$\sigma$) |
| inclination-verified | 18 | $0.889$ | $[-1.35,\ 7.54]$ | $-0.47$ |

Both intervals admit $n = 0$. $n = 1.5$ lies nominally outside the full-sample interval, **but the full-sample central value is unphysical for either branch**, so the constraint is systematics-dominated and must not be recorded as a win for the anthropic reading. This is consistent with the standing `CURRENT_STATE` warning that the $2.4$–$3.4\times$ median offset at $z \sim 2.2$ is **not** a detection and must not be cited as evidence for $a_0 \propto H(z)$.

**Status: `[U]` — the fork is live and undecided. That is the correct state for a pre-registered test.**

### G. What would decide it

A pre-registered fit of $n$ with an explicit systematics budget (pressure support, beam smearing, $f_{\text{DM}}$ route) on a sample where inclination is measured for *every* object, evaluated against the frozen gate. Until then the anthropic branch is a named alternative with one sharp prediction, and nothing more.

**References**
- Milgrom, M. (2015). Cosmological variation of the MOND constant: Secular effects on galactic systems. *Physical Review D, 91*(4), 044009. https://doi.org/10.1103/physrevd.91.044009
- Sanders, R. H. (2019). The prediction of rotation curves in gas-dominated dwarf galaxies with modified dynamics. *Monthly Notices of the Royal Astronomical Society, 485*(1), 513–521. https://doi.org/10.1093/mnras/stz353
- Milgrom, M. (2020). The $a_0$–cosmology connection in MOND. arXiv:2001.09729. https://doi.org/10.48550/arxiv.2001.09729
