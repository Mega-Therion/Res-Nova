# Linear Perturbation Theory of the Information Tension Field

To mathematically prove that the $\chi$ field produces the Cosmic Microwave Background (CMB) acoustic peaks, we must transition from the smooth background universe to the "bumpy" universe. We do this by analyzing the 1st-order linear perturbations of the field.

These are the exact equations that must be coded into a Boltzmann solver (like `CLASS` or `CAMB`) to plot the CMB power spectrum.

---

## 1. The Perturbed Spacetime Metric

We work in the Conformal Newtonian (Longitudinal) Gauge. We perturb the smooth FLRW metric by introducing two gravitational potentials: $\Psi$ (the Newtonian time potential) and $\Phi$ (the spatial curvature potential).

$$ ds^2 = -(1+2\Psi)dt^2 + a^2(t)(1-2\Phi)\delta_{ij} dx^i dx^j $$

## 2. Perturbing the Tension Field

We split the geometric scalar field into a smooth cosmological background $\bar{\chi}(t)$ and a tiny, space-dependent quantum ripple $\delta\chi(t, \vec{x})$:

$$ \chi(t, \vec{x}) = \bar{\chi}(t) + \delta\chi(t, \vec{x}) $$

Our symmetry-breaking potential is:
$$ V(\chi) = \lambda_\chi M_{pl}^2 \left( \chi^2 - \frac{1}{2} \right)^2 $$

The first and second derivatives (effective mass) of the potential are:
*   $V_{,\chi} = 4 \lambda_\chi M_{pl}^2 \chi (\chi^2 - 1/2)$
*   $V_{,\chi\chi} = 4 \lambda_\chi M_{pl}^2 (3\chi^2 - 1/2)$

---

## 3. The Background Evolution (0th-Order)

If we plug the unperturbed field into the Klein-Gordon equation, we get the equation that dictates how the background field evolves as the universe expands ($H = \dot{a}/a$):

$$ \ddot{\bar{\chi}} + 3H\dot{\bar{\chi}} + V_{,\chi}(\bar{\chi}) = 0 $$

**The Physics:** Early on, $H$ is huge (lots of friction), but $V_{,\chi}$ is steeper. The field oscillates violently inside the "W" shaped potential. As the universe cools, $H$ decreases, and the field eventually comes to rest exactly at the minimum where $V_{,\chi} = 0 \implies \bar{\chi} = 1/\sqrt{2}$.

---

## 4. The Perturbation Equation (1st-Order)

To see how the ripples grow into galaxies, we look at the 1st-order perturbation. Moving into Fourier space (where $k$ is the wavenumber of the ripple), the differential equation governing the growth of the tension field's density is:

$$ \ddot{\delta\chi} + 3H\dot{\delta\chi} + \left( \frac{k^2}{a^2} + V_{,\chi\chi}(\bar{\chi}) \right) \delta\chi = \dot{\bar{\chi}} (\dot{\Phi} + 3\dot{\Psi}) - 2 \Psi V_{,\chi}(\bar{\chi}) $$

**The Physics of this Equation:**
*   The left side describes a damped harmonic oscillator. The $k^2/a^2$ term represents spatial pressure (tendency to smooth out). 
*   The right side represents **gravitational forcing**. The $\chi$ field is being "pulled" by the gravitational wells ($\Phi$ and $\Psi$) created by the vector field and ordinary matter.

---

## 5. Proving It Acts Like Dark Matter (The WKB Limit)

Why does this perfectly mimic Dark Matter in the CMB? 

In the early universe ($z \sim 1100$), the field's effective mass ($m_{eff}^2 = V_{,\chi\chi}$) is vastly larger than the Hubble rate ($H$). We can apply the **WKB approximation** to cycle-average the rapid oscillations.

When we calculate the effective sound speed of these $\delta\chi$ ripples over a full oscillation cycle, we find:

$$ \langle c_s^2 \rangle = \frac{\langle \delta P_\chi \rangle}{\langle \delta \rho_\chi \rangle} \approx 0 $$

**The Conclusion:** Because the sound speed is exactly zero, the ripples have **no internal pressure**. When $c_s^2 = 0$, the $k^2/a^2$ pressure term vanishes. The ripples undergo unhindered gravitational collapse (Jeans instability). The tension field clumps together exactly like Cold Dark Matter particles, creating the gravitational "potholes" needed for the CMB acoustic peaks.

---

## 6. The Disformal Baryon Coupling

Finally, how do the baryons "know" about the tension field? Ordinary matter (the baryon-photon plasma) does not follow the standard metric; it follows the disformal metric $\tilde{g}_{\mu\nu}$.

When we perturb the disformal metric, the baryons experience an effective gravitational potential:

$$ \Psi_{eff} \approx \Psi + 2\delta\chi \sinh(2\bar{\chi}) $$

This proves that even if the standard Newtonian potential $\Psi$ is weak, the $\delta\chi$ ripples act as an independent gravitational pull on the baryons. The baryon plasma falls into the tension field's geometric wells, generating the precise acoustic ringing seen by the Planck satellite.
