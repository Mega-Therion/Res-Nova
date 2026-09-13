# TARGET D6 SUPPLEMENT: Λ_SC vs short-range-gravity experiments — first-pass check

**Status:** FIRST PASS 2026-09-12 (Vesper). Answers the `[O]` item in
`TARGET_D6_RELATIVISTIC_STABILITY.md` §3 and Task Board P2
"Compare Λ_SC ≈ 1.8 meV against published fifth-force/EP bounds".
**Tags:** `[C]` experimental facts · `[D]` screening estimates (this document) · `[O]` open
**Verdict in one line:** **NOT excluded — but the old "safe because inaccessible" framing is
false; the safety comes entirely from the theory's own environmental screening.**

---

## 1. The scale and its range `[D]`

$$\Lambda_{\rm SC} = \left(\frac{a_0^2}{G}\right)^{1/4}\text{restoring }\hbar c \;\Rightarrow\;
\Lambda_{\rm SC} = \left[\frac{a_0^2}{G}(\hbar c)^3\right]^{1/4}$$

| $a_0$ source | $\Lambda_{\rm SC}$ | interaction range $\lambda=\hbar c/\Lambda$ |
|---|---|---|
| D6 §3 (1.2×10⁻¹⁰) | 1.7938 meV | **110.0 μm** |
| SPARC (1.116×10⁻¹⁰) | 1.7299 meV | **114.1 μm** |
| canonical (1.2211×10⁻¹⁰) | 1.8095 meV | **109.1 μm** |

(Agree with `TARGET_D6_D8_D9_SUPPLEMENT` row 1 to the rounding of constants.)

## 2. What the experiments constrain `[C]`

Eöt-Wash torsion balances have excluded **gravitational-strength (|α|=1) Yukawa violations of
the inverse-square law for all λ ≥ 39 μm** (2020; progressively: 197 μm in 2001, 56 μm in
Kapner et al. 2007, 42 μm in 2013, 39 μm in 2020 — per the review in
arXiv:2406.13020). λ ≈ 110 μm is therefore **deep inside the probed window**: an *unscreened*
fifth force of gravitational strength at the Λ_SC range would have been seen. **Naive
comparison verdict: if Λ_SC coupled to matter unscreened at strength ≳ G, the theory is
excluded. [D — logical, conditional]**

## 3. Why that comparison does not bite: environmental screening `[D]`

The scalar does not couple unscreened — μ_std suppresses it at high ambient acceleration, and
**every terrestrial lab sits in Earth's field**:

- Earth ambient: $g_\oplus = 9.81\ \mathrm{m/s^2} \Rightarrow x_{\rm env} = g_\oplus/a_0 = 8.8\times10^{10}$
- μ_std suppression factor: $\mu_{\rm std}(x_{\rm env}) \approx 1 - \tfrac{1}{2x_{\rm env}^2}$,
  so the scalar's response to a *source* mass is suppressed by $\sim 1/(2x_{\rm env}^2)
  \approx 6.5\times10^{-23}$ relative to its Newtonian field.
- Order check: a 100-g source at 5 cm produces $g_N \approx 2.7\times10^{-9}\ \mathrm{m/s^2}
  \approx 24\,a_0$ (its MOND radius is ~0.25 m) — but the *total* field everywhere in the lab
  is ~9.8 m/s², dominated by Earth. The scalar fifth force between lab masses is therefore
  ~10⁻³¹ m/s² scale: **undetectable by any conceivable ISL, fifth-force, or EP experiment.**

This is the standard environmental-screening argument for MOND-type scalars, here evaluated
on μ_std. **[D] as an estimate — see §4a for what a rigorous version needs.**

## 4. What remains genuinely open `[O]`

a. **AeST-specific screening profile.** §3 uses the constitutive suppression only; a full
   Vainshtein/environment calculation *from the covariant action* (what is the scalar's
   effective mass and gradient profile around a lab-scale mass embedded in Earth's field?)
   is the rigorous version. Expected to strengthen, not weaken, the conclusion.
b. **Scalar quantum effects at meV.** Λ_SC ≈ 1.8 meV is where the EFT goes strongly coupled:
   scalar radiation from moving lab masses, EFT-breakdown corrections in early-universe
   (meV-temperature) epochs, and cosmological production must be bounded. Nobody has done this.
c. **EP implications.** Minimal coupling under environmental screening: the predicted
   Eötvös-parameter contributions should be derived and compared to MICROSCOPE (η ≲ 10⁻¹⁵);
   expected suppressed, but it is a free consistency check.

## 5. Bottom line

- The 2026-09-12 unit-error correction (7.25 orders) changed **why** the theory is safe, not
  **whether**: Λ_SC is fully lab-accessible (λ ≈ 110 μm, probed to |α|=1 by Eöt-Wash), and the
  protection is the theory's own screening. "Far below any experimentally accessible scale" is
  **withdrawn**; "screened below detection in all terrestrial environments" **[D]** replaces it.
- The `Λ_SC` Task Board P2 item is answered at first-pass level: **not excluded**; the rigorous
  closure is §4a, and the genuinely new questions are the meV quantum effects of §4b — which
  no MOND-type theory has ever had to face at this precision, because none had an honest Λ_SC.

## 6. Reproduce

```python
import math
hbarc = 1.0546e-34*2.998e8; G, J2eV = 6.674e-11, 1.602e-19
for a0 in (1.2e-10, 1.116e-10, 1.2211e-10):
    Lam = ((a0**2/G)*hbarc**3)**0.25
    print(f"a0={a0:.4g}: Lambda_SC = {Lam/J2eV*1000:.4f} meV, range = {hbarc/Lam*1e6:.1f} um")
x = 9.81/1.116e-10; print("Earth ambient: x =", f"{x:.2e}", "suppression 1/(2x^2) =", f"{1/(2*x**2):.2e}")
print("100 g at 5 cm: g_N =", f"{G*0.1/0.05**2:.2e} m/s^2 =", f"{G*0.1/0.05**2/1.116e-10:.0f} a0; MOND radius =", f"{math.sqrt(G*0.1/1.116e-10):.3f} m")
```
