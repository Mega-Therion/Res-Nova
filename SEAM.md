# Null seam

Date: 2026-10-31. This note is block 4 of [`FRONT.md`](FRONT.md). The index that places this seam against the other strands is [`UNIDEX.md`](UNIDEX.md). It does not select the galaxy axiom in block 3, and it does not name a Standard Model particle in block 1.

The calculated object is a radiation cosmology carried through a null seam. The mode receipt is `Chyren/state/cpt_mode_equation.json`, filed with the rest of that chain in The Hood under BLK-936. Those files are not copied into this repository.

From that receipt, Job 3:

- \(|\beta|^2=\exp(-\pi k^2/\gamma)\).
- The direct abundance integral is \(I=1/(8\pi^{3/2})\), recorded numerically as `0.02244839026564582`.
- A second number, about `0.01276`, is the half-angle minimum-excitation integral in the same file. It is a different assumption. It is not \(I\).

\(\gamma\) is not fixed. The receipt leaves it as either \(m C\) or \(y\, m C\), with the Yukawa factor \(y\), the radiation constant \(C\), and \(g_\star\) marked open. The mass expression in the same object is symbolic, including the factor \((\cdots)^{2/5}\) under the choice \(\gamma=m C\). No value of that mass is a result. A later declaration, tier `[O]`, recorded in [`UNIDEX.md`](UNIDEX.md) and in `02_galaxy_dynamics/seam_mass_symbols.json`, sets the entropy ruler of that mass root to the photon gas, \(g_\star=2\), and sets the dilution ratio to 1. Under those declarations the same file records the measured-temperature evaluation. A bound check in `02_galaxy_dynamics/seam_mass_bounds.json` holds that evaluation fixed, records that no imported limit excludes it, and names no particle. The declarations do not edit the mode receipt, that evaluation is not a result of this note, and Job B's seam row stays null. A reheating adoption in `02_galaxy_dynamics/seam_mass_reheat_mismatch.json` sets the conditional mass to the never-reheated photon bath and leaves the measured-temperature evaluation in the symbols file. It does not change \(g_\star\), does not change the dilution ratio, and names no particle. A later shot in `02_galaxy_dynamics/seam_open_bridges_shot.json` evaluates \(\gamma=m C\) on that adopted bath. The value is conditional. The shot does not edit the mode receipt, does not produce \(\eta\), and does not set \(\lambda\). `02_galaxy_dynamics/seam_remaining_five.json` records the species list as the later photon bath plus one unnamed produced field, and records an imported baryon density whose seam contribution is 0.

What this note constrains:

- Block 3. Nothing here selects \(\mu(x)=x/\sqrt{1+x^2}\). The galaxy law stays an axiom.
- Block 1, [`IMPORTED_STANDARD_MODEL.md`](IMPORTED_STANDARD_MODEL.md). Nothing here sets a neutrino mass. Calling the produced particle a right-handed neutrino is not part of the receipt.
- Block 2, [`OUTSIDE_GALAXIES.md`](OUTSIDE_GALAXIES.md). The seam is a general-relativistic calculation. It does not replace general relativity outside galaxies, and it does not move the Cassini boundary of the galaxy law.
