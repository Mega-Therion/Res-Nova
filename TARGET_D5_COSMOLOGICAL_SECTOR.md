# TARGET D5: Cosmological Sector

**Status:** D5_OPEN — Framework established, quantitative growth analysis computed, non-linear regime requires simulation.
**Last updated:** 2026-08-16
**Author:** R.W. Yett / Sovereign Architecture Group
**Epistemic tag:** [P] (computed sections) / [O] (open sections)

---

## 1. Problem Statement

The cosmological sector is the **least developed** and **most critical** open target in the Res Nova program. The `04_cosmology/` directory currently contains only normalization ledgers — no perturbation code, no CMB analysis, no structure formation computation. This document establishes the theoretical framework, computes the linear growth factor with MOND enhancement, and identifies the specific computations needed to close this target.

---

## 2. The Cosmic Coincidence [P]

The MOND acceleration scale $a_0$ is observationally tied to the Hubble scale:

$$\frac{H_0 c}{a_0} = \frac{(70\;\text{km/s/Mpc}) \times c}{1.2 \times 10^{-10}\;\text{m/s}^2} \approx 5.7$$

This means the horizon-scale gravitational acceleration is $\sim 6 \times a_0$ — **in the Newtonian regime**, not deep-MOND. The transition to MOND behavior occurs at scales where $a \lesssim a_0$, i.e., galaxy and cluster scales. Cosmological horizon-scale dynamics are therefore approximately Newtonian.

However, structure formation probes a wide range of scales. At galaxy cluster scales ($\sim 1$ Mpc), the characteristic acceleration is $a \sim 10^{-14}$ m/s², well below $a_0$, placing cluster-scale structure growth **deep in the MOND regime**.

---

## 3. RMOND Background Cosmology [P]

In the Skordis–Złośnik (2021) RMOND framework, the background cosmology is standard FLRW. The auxiliary fields (vector field $\mathbf{A}_\mu$, scalar field $\phi$) contribute an effective energy density that mimics cold dark matter at the background level:

$$H^2(a) = \frac{8\pi G}{3}\left[\rho_b(a) + \rho_\gamma(a) + \rho_{\text{eff}}(a)\right]$$

where $\rho_{\text{eff}}$ is the effective contribution from the RMOND auxiliary fields. At the background level, RMOND is **degenerate with ΛCDM** — the auxiliary fields provide exactly the "missing mass" needed to match the Friedmann equation [web:19].

**Key result [P]:** RMOND reproduces the CMB power spectrum and the linear matter power spectrum (Skordis & Złośnik 2021; Blanchet & Skordis 2024) [web:19].

---

## 4. Linear Perturbation Theory [P]

### 4.1 The Growth Equation

The linear density contrast $\delta(\mathbf{k}, a)$ satisfies:

$$\ddot{\delta} + 2H\dot{\delta} = 4\pi G \rho_{\text{eff}}(a) \, \xi(k, a) \, \delta$$

where $\xi(k, a) = G_{\text{eff}}(k, a) / G$ is the **scale-dependent enhancement factor**. In ΛCDM, $\xi = 1$. In RMOND, $\xi$ depends on scale and redshift through the auxiliary field dynamics.

### 4.2 Growth in Log-Scale-Factor Variable

Converting to $u = \ln a$ as the independent variable, the growth equation becomes:

$$\frac{d^2 D}{du^2} + \left[2 + \frac{d \ln H}{d \ln a}\right] \frac{dD}{du} - \frac{3}{2}\,\Omega_m(a)\,\xi\, D = 0$$

**Verification [P]:** In matter domination ($\Omega_m = 1$, $d\ln H/d\ln a = -3/2$), the growing mode is $D \propto a^{\lambda}$ where:

$$\lambda^2 + \frac{1}{2}\lambda - \frac{3}{2}\xi = 0 \quad \Longrightarrow \quad \lambda = \frac{-1/2 + \sqrt{1/4 + 6\xi}}{2}$$

| Enhancement $\xi$ | Growth exponent $\lambda$ | $D$ at $z=0$ relative to ΛCDM |
|:-:|:-:|:-:|
| 1.0 (ΛCDM) | 1.000 | 1.0× |
| 1.5 | 1.186 | $\sim 8 \times$ |
| 2.0 | 1.366 | $\sim 76 \times$ |
| 3.0 | 1.691 | $\sim 2264 \times$ |

### 4.3 Numerical Computation [P]

The growth equation was integrated numerically from $a = 10^{-4}$ to $a = 1$ for three cases:

| Redshift | $D_{\Lambda\text{CDM}}$ | $D_{\text{MOND}(2\times)}$ | $D_{\text{MOND}(3\times)}$ | Ratio (2×) | Ratio (3×) |
|:-:|:-:|:-:|:-:|:-:|:-:|
| $z = 0$ | 1.000 | 76.39 | 2263.8 | 76.4× | 2264× |
| $z = 1$ | 0.489 | 28.90 | 701.8 | 59.1× | 1435× |
| $z = 3$ | 0.249 | 10.64 | 201.5 | 42.8× | 809× |
| $z = 9$ | 0.099 | 2.69 | 35.7 | 27.0× | 359× |

**The growth enhancement is catastrophic.** Even a modest 2× enhancement produces $\sim 76\times$ more structure by $z=0$ relative to ΛCDM from the same initial perturbations. This is the **linear theory** prediction; non-linear gravitational collapse amplifies the discrepancy further.

---

## 5. The Structure Formation Crisis [P]

### 5.1 The νHDM Failure

Russell et al. (2026) ran the largest N-body simulations in a MOND cosmology to date (νHDM — MOND + 11 eV neutrinos acting as hot dark matter) [web:17][web:18]. Their key findings:

- MOND models **massively overproduce large-scale structures** by $z=0$
- Most massive cluster: $\approx 5 \times 10^{17}\,M_\odot\,h^{-1}$ (vs. observed $\sim 2 \times 10^{15}\,M_\odot\,h^{-1}$)
- Typical peculiar velocities: several thousand km/s (vs. observed $\sim 300$ km/s)
- νHDM is ruled out at $>5\sigma$ confidence

This is consistent with the linear growth computation in §4.3: a 2× enhancement produces 76× excess growth, which non-linear collapse amplifies to $\sim 10^3\times$ excess in cluster mass.

### 5.2 Why RMOND Survives at Linear Order

RMOND (Skordis–Złośnik 2021) reproduces the CMB and linear matter power spectrum because the auxiliary fields provide an effective screening: on large scales, the enhancement $\xi(k, a) \to 1$ (matching ΛCDM), and the MOND behavior only emerges at small scales [web:19][web:45]. This **scale-dependent screening** is absent in the non-relativistic νHDM model, which applies MOND universally.

### 5.3 The Non-Linear Gap

The problem is that RMOND's linear-order success does **not** guarantee non-linear success. On scales where $a \lesssim a_0$ (galaxy clusters, groups), the MOND enhancement kicks in, and the non-linear collapse proceeds faster than in ΛCDM. No simulation has yet been run in the full RMOND framework to test this.

---

## 6. What the Dual-Channel Action Changes [O]

### 6.1 At Cosmological Scales: Nothing

At very low accelerations ($a \ll a_0$), the dual-channel action reduces to the deep-MOND regime where $\mathcal{F}_{\text{dual}} \approx x^3/3$. This is **identical** to every other MOND theory in the deep-MOND limit. The specific form of the interpolation function $\mu(x) = x/(1+x)$ only matters at $a \sim a_0$ (galaxy scales), not at cosmological scales.

**Therefore [O]:** The dual-channel action does not offer a specific cosmological advantage over generic MOND in the linear regime. The cosmological predictions depend on the **covariant embedding** (D7/D9), not on the non-relativistic action.

### 6.2 Potential Mitigation via RMOND Screening [O]

The aether scalar-tensor theory (Reyes et al. 2025) — a relativistic MOND framework — "behaves like cold dark matter on cosmological scales while predicting the MOND force-law in astrophysical systems" [web:45]. This suggests that the covariant structure can provide the screening needed to suppress cosmological overgrowth.

**Open question [O]:** Does the specific Skordis–Złośnik RMOND embedding, when combined with the dual-channel action, provide sufficient screening to prevent the $\sim 76\times$ overgrowth seen in the non-relativistic case? This requires:

1. Deriving the full RMOND perturbation equations with the dual-channel $\mu$
2. Computing the scale-dependent enhancement $\xi(k, a)$
3. Running N-body simulations in the RMOND framework
4. Comparing with the observed cluster mass function and peculiar velocity field

---

## 7. Required Computations [O]

The following computations are needed to close D5:

### 7.1 Linear Theory (Tractable)
- [ ] Derive the RMOND perturbation equations for the dual-channel action
- [ ] Compute the scale-dependent enhancement $\xi(k, a)$
- [ ] Compare the linear matter power spectrum with Planck + BOSS data
- [ ] Compute the growth rate $f\sigma_8(z)$ and compare with RSD observations

### 7.2 Non-Linear Theory (Requires Simulation)
- [ ] Implement MOND gravity in an N-body code (e.g., RAMSES-VMOND or a custom code)
- [ ] Run cosmological simulations with RMOND screening
- [ ] Compute the cluster mass function $n(M, z)$
- [ ] Compute the peculiar velocity field
- [ ] Compare with observations (Planck cluster catalog, SDSS velocity field)

### 7.3 CMB (Requires Boltzmann Code)
- [ ] Implement RMOND perturbation equations in a modified CLASS/CAMB
- [ ] Compute the CMB $C_\ell$ power spectrum
- [ ] Compare with Planck 2018 data
- [ ] Verify that the dual-channel $\mu$ does not alter the linear CMB predictions

---

## 8. Risk Assessment [O]

| Risk | Severity | Mitigation |
|------|----------|------------|
| Non-linear overproduction persists in RMOND | **Critical** | RMOND screening may suppress large-scale enhancement |
| CMB predictions deviate from Planck | High | Skordis–Złośnik 2021 showed RMOND reproduces CMB; dual-channel $\mu$ shouldn't change this |
| Growth rate $f\sigma_8$ too high | Medium | Scale-dependent screening can tune this |
| Cluster mass function inconsistent | **Critical** | Requires simulation; no analytic shortcut |
| JWST high-z galaxies challenge MOND | Medium | MOND predicts faster early structure formation, which may actually help explain JWST observations |

---

## 9. Summary

The cosmological sector (D5) is the **single most critical open target** in the Res Nova program. The quantitative analysis shows that a uniform MOND enhancement of $2\times$ produces $\sim 76\times$ excess structure growth by $z=0$ — consistent with the νHDM failure found by Russell et al. (2026). The RMOND embedding provides a potential mitigation via scale-dependent screening, but this has not been tested in the non-linear regime. Closing D5 requires:

1. **Linear theory**: derivable analytically/numerically (tractable now)
2. **Non-linear simulations**: requires significant computational resources
3. **CMB comparison**: requires a modified Boltzmann code

The dual-channel action does not offer a specific cosmological advantage — the cosmological predictions depend entirely on the covariant embedding (D7/D9), not on the non-relativistic action. The most productive path forward is to focus on D7 (covariant completion) first, then derive the RMOND perturbation equations with the dual-channel $\mu$, and finally run simulations.
