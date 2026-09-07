# Audit of the Horizon-Tied `a0(z)` Law

## Conclusion

The exact phenomenological law

\[
a_0(z)=\xi cH(z),\qquad \xi=\frac{a_0(0)}{cH_0},
\]

is **not supported by the current published intermediate-redshift summary**. This does not solve the first-principles horizon identity, and it does not falsify every horizon-inspired relativistic completion. It does settle a narrower question: the exact flat-\(\Lambda\)CDM proportionality to \(H(z)\) is a poor match to the currently published evolution of the radial-acceleration relation.

## Inputs

The repository’s frozen local measurement is \(a_0(0)=1.1160351\times10^{-10}\,\mathrm{m\,s^{-2}}\), with \(H_0=67.4\,\mathrm{km\,s^{-1}\,Mpc^{-1}}\), \(\Omega_m=0.315\), and \(\Omega_\Lambda=0.685\). These give \(\xi=0.17043\). The MUSE-DARK III paper reports a sample of 79 star-forming galaxies over \(0.33<z<1.44\), a characteristic acceleration \(a_0|_{z\sim1}=2.38^{+0.12}_{-0.10}\times10^{-10}\,\mathrm{m\,s^{-2}}\), and a phenomenological linear slope \(a_1=1.59^{+0.11}_{-0.10}\times10^{-10}\,\mathrm{m\,s^{-2}}\) per unit redshift [1].

The repository computes, from the exact horizon law,

\[
a_0(1)=1.998\times10^{-10}\,\mathrm{m\,s^{-2}},
\]

and the local slope at \(z=0\),

\[
\left.\frac{da_0}{dz}\right|_{z=0}=\frac{3}{2}\Omega_m a_0(0)=5.27\times10^{-11}\,\mathrm{m\,s^{-2}}.
\]

The published central value at \(z\sim1\) is therefore 1.19 times the exact horizon prediction, while the published linear slope is about 3.02 times the local slope implied by \(a_0\propto H(z)\). The cited paper itself cautions that its linear parameterization is phenomenological rather than physically motivated [1].

## Epistemic status

This result is **`[C]+[D]`**: the observational values are cited from the publication, and the comparison is deterministically computed by [`a0_horizon_literature_audit.py`](a0_horizon_literature_audit.py). It is not a raw-data reanalysis because the 79-galaxy acceleration tracks and their covariance are not vendored in Res-Nova.

Accordingly, O1 should not be described as theoretically solved. The strongest defensible update is:

> The exact law `a0(z)=ξcH(z)` is disfavored by the current published intermediate-redshift summary; the covariant derivation of the `1/(2π)` normalization remains open.

## Limitations

The comparison does not refit the published 79-galaxy tracks, propagate correlated systematics, or compare the full posterior to a nonlinear `H(z)` model. The MUSE-DARK III accelerations are model-derived and subject to assumptions about disk–halo decomposition, stellar mass-to-light ratios, pressure support, and spatial resolution [1]. A stronger closure would require the public point-level data and covariance, followed by a pre-registered fit of constant, `H(z)`, and flexible evolution models.

## References

[1]: https://doi.org/10.1051/0004-6361/202659230 "Ciocan et al. 2026, MUSE-DARK III: The evolution of the radial acceleration relation at intermediate redshifts"
