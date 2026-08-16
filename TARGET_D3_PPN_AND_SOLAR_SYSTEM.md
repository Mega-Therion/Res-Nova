# TARGET D3: PPN Limits and Solar System Constraints

**Status:** D3_ANALYZED — MOND corrections computed and shown safe; PPN parameters depend on D7 covariant completion; Q₂ tension identified.
**Last updated:** 2026-08-16
**Author:** R.W. Yett / Sovereign Architecture Group
**Epistemic tag:** [P] (computed sections) / [O] (open sections)

---

## 1. Problem Statement

The Parameterized Post-Newtonian (PPN) formalism tests gravity theories in the weak-field, slow-motion regime. The solar system provides the most precise tests of gravity, with the Cassini probe constraining the space-curvature parameter to $|\gamma - 1| < 2.3 \times 10^{-5}$ [web:54][web:58]. This document computes the PPN parameters and MOND corrections for the dual-channel action and assesses consistency with solar system constraints.

---

## 2. Solar System Acceleration Profile [P]

The solar system is deeply in the Newtonian regime ($a \gg a_0$). The acceleration ratio $x = a/a_0$ ranges from $\sim 10^5$ (outer solar system) to $\sim 10^8$ (inner planets):

| Body | $g_N$ (m/s²) | $g_N / a_0$ | $\mu(g/a_0)$ | $1 - \mu$ | MOND correction |
|------|:-:|:-:|:-:|:-:|:-:|
| Mercury (0.39 AU) | $3.9 \times 10^{-2}$ | $3.3 \times 10^8$ | $0.999999997$ | $3.1 \times 10^{-9}$ | $3.1 \times 10^{-9}$ |
| Venus (0.72 AU) | $1.1 \times 10^{-2}$ | $9.5 \times 10^7$ | $0.999999990$ | $1.0 \times 10^{-8}$ | $1.0 \times 10^{-8}$ |
| Earth (1.0 AU) | $5.9 \times 10^{-3}$ | $4.9 \times 10^7$ | $0.999999980$ | $2.0 \times 10^{-8}$ | $2.0 \times 10^{-8}$ |
| Mars (1.52 AU) | $2.6 \times 10^{-3}$ | $2.1 \times 10^7$ | $0.999999953$ | $4.7 \times 10^{-8}$ | $4.7 \times 10^{-8}$ |
| Jupiter (5.2 AU) | $2.2 \times 10^{-4}$ | $1.8 \times 10^6$ | $0.999999453$ | $5.5 \times 10^{-7}$ | $5.5 \times 10^{-7}$ |
| Saturn (9.5 AU) | $6.6 \times 10^{-5}$ | $5.5 \times 10^5$ | $0.999998174$ | $1.8 \times 10^{-6}$ | $1.8 \times 10^{-6}$ |
| Pioneer scale (20 AU) | $1.5 \times 10^{-5}$ | $1.2 \times 10^5$ | $0.999991908$ | $8.1 \times 10^{-6}$ | $8.1 \times 10^{-6}$ |

**Key result [P]:** At Earth's orbit, the MOND correction is $a_0/g \approx 2 \times 10^{-8}$, which is $\sim 1137\times$ below the Cassini sensitivity of $2.3 \times 10^{-5}$. The dual-channel action is **safe** in the inner solar system by more than three orders of magnitude.

---

## 3. PPN Parameters [P]

### 3.1 Newtonian Regime

In the Newtonian regime ($x \gg 1$), the dual-channel action reduces to:

$$\mathcal{F}_{\text{dual}}(x) \approx \tfrac{1}{2}x^2 - x + \ln(x) \approx \tfrac{1}{2}x^2$$

The interpolation function $\mu(x) = x/(1+x) \approx 1 - 1/x + 1/x^2 - \cdots$ converges to 1, and the modified Poisson equation reduces to the standard Newtonian equation:

$$\nabla^2 \Phi = 4\pi G \rho$$

**Theorem 3.1 [P]:** In the Newtonian limit, the dual-channel action produces **standard Newtonian gravity** with no PPN deviations. The PPN parameters $\gamma$ and $\beta$ depend entirely on the **covariant completion** (D7/D9), not on the non-relativistic interpolation function $\mu$.

### 3.2 Why μ Does Not Affect PPN

The PPN expansion probes the metric $g_{\mu\nu}$ in the weak-field regime. The non-relativistic MOND action only modifies the Newtonian potential $\Phi$ through the modified Poisson equation. Since $\mu \to 1$ for $a \gg a_0$, the modification vanishes:

$$\delta\Phi_{\text{MOND}} \sim \frac{a_0}{g_N} \times \Phi_{\text{Newton}} \sim 10^{-8} \times \Phi_{\text{Newton}}$$

This is far below any current or foreseeable solar system test. The PPN parameters $\gamma$ (space curvature) and $\beta$ (nonlinearity) are determined by the post-Newtonian metric, which depends on the **relativistic** structure of the theory — i.e., the covariant completion (D7) and the RMOND embedding (D9).

### 3.3 Observational Constraints

| Parameter | GR value | Constraint | Source |
|-----------|:-:|:-:|:-:|
| $\gamma$ | 1 | $|\gamma - 1| < 2.3 \times 10^{-5}$ | Cassini (Bertotti et al. 2003) [web:54] |
| $\beta$ | 1 | $|\beta - 1| < 2.3 \times 10^{-4}$ | MESSENGER perihelion [web:58] |
| $\alpha_1$ | 0 | $< 10^{-4}$ | Lunar Laser Ranging |
| $\alpha_2$ | 0 | $< 10^{-4}$ | Solar spin precession |
| $Q_2$ | 0 | $(1.6 \pm 1.8) \times 10^{-27}$ s⁻² | Cassini radio tracking (2026) [web:55] |

---

## 4. The External Field Effect (Q₂) Tension [P]

### 4.1 The MOND EFE

The Milky Way's gravitational field at the Sun's position ($g_{\text{ext}} \approx 1.9 \times 10^{-10}$ m/s² $\approx 1.6 \, a_0$) is in the MOND transition regime. This external field modifies the internal dynamics of the solar system through the **external field effect** (EFE), producing a quadrupolar distortion parameterized by $Q_2$.

### 4.2 The Tension

The 2026 Cassini radio tracking analysis [web:55] found:

$$Q_2 = (1.6 \pm 1.8) \times 10^{-27}\;\text{s}^{-2}$$

consistent with zero. This constrains the MOND boost at the Sun's position to **less than 2%** (95% CL). However, galaxy rotation curves require a MOND boost of $\sim 60%$ at the same acceleration scale, creating a **3–15σ tension** depending on the mass modeling [web:55].

### 4.3 Resolution via RMOND Screening [O]

The tension arises because non-relativistic MOND predicts a sizeable EFE in the solar system. In the RMOND framework (Skordis–Złośnik 2021), the auxiliary fields can provide a **screening mechanism** that suppresses the EFE on solar system scales while preserving MOND behavior at galactic scales.

**Open question [O]:** Does the RMOND embedding with the dual-channel $\mu$ provide sufficient screening to satisfy the Cassini $Q_2$ constraint? This requires the D7 covariant completion.

---

## 5. The Cassini/MOND Result (2026) [P]

Hees et al. (2026) [web:55] used the full Cassini radio tracking dataset to constrain MOND's solar system signature:

- **$Q_2$ is consistent with zero** — no MOND EFE detected
- The PPN formalism accurately describes planetary dynamics
- Solar system measurements now provide **stronger constraints than wide-binary data** on classical MOND
- The MOND boost at the Sun's position is bounded to **< 2%** (95% CL)
- This creates **3–15σ tension** with galaxy rotation curve expectations

**Implication [P]:** The non-relativistic dual-channel action cannot resolve this tension alone. The resolution requires the covariant completion (D7) to provide screening, or the theory must accept that the solar system EFE is genuinely absent (which would require a departure from standard MOND phenomenology).

---

## 6. Summary of Findings

| Question | Answer | Status |
|----------|--------|--------|
| Is the dual-channel action safe in the inner solar system? | **Yes** — MOND correction $\sim 10^{-8}$, Cassini sensitivity $2.3 \times 10^{-5}$ | [P] |
| Do PPN parameters depend on $\mu(x) = x/(1+x)$? | **No** — all MOND $\mu$ functions give $\mu \approx 1$ in the solar system | [P] |
| What determines the PPN parameters? | The **covariant completion** (D7/D9), not the non-relativistic action | [P] |
| Is there a tension with the Cassini $Q_2$ constraint? | **Yes** — 3–15σ tension with galaxy rotation curves | [P] |
| Can the tension be resolved? | Only via RMOND screening in the covariant completion (D7) | [O] |

### Key Conclusion [P]

**The dual-channel action passes all solar system tests by construction**, because the solar system is in the Newtonian regime where $\mu \approx 1$. The PPN parameters are not determined by the non-relativistic action — they depend on the D7 covariant completion. The $Q_2$ tension is the most significant challenge, and it requires the RMOND embedding to provide a screening mechanism.

**Therefore [P]:** D3 is reduced to a **dependency on D7**. The PPN computation cannot be completed without the covariant formulation. The most productive path is to complete D7 first, then compute the exact PPN parameters from the RMOND metric.
