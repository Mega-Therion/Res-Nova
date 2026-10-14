# Constraints-report error review

**Date:** 2026-10-14  
**Status:** Documentation review. No physics tier or repository physics source changed.

## Scope

This reviews `macroscopic_warp_drive_constraints_report.md` and the related `Alcubierre-Drive-Launch-Mechanics.md` file. The former is useful as a requirements checklist after corrections; the latter is hypothesis-generation material, not a derivation.

## Material errors

### 1. Van Den Broeck geometry is reversed

The report describes Van Den Broeck as making the external bubble macroscopic while the internal passenger volume is much smaller. That reverses the construction.

The actual construction uses a microscopically small exterior throat/surface while the interior spatial volume is enlarged. The original paper states that the exterior bubble can be microscopic while the interior can accommodate a macroscopic object.

**Consequence:** Do not repeat the reversed description in Res-Nova surfaces.

### 2. The 2026 observer-robust claim is not established for reuse

The report cites a 2026 observer-robust preprint and reports that an Eulerian reading missed about 73% of sampled WEC violations for one profile.

BLK-311 already flags that the report's description and the 73% number do not match the linked paper. Treat both the description and number as quarantined until independently checked against the primary source.

## Claims requiring qualification

### Lentz positive-energy claim

The launch-mechanics file says Lentz's construction bypasses the need for negative mass. That is too strong for Res-Nova use.

A positive energy density in one observer frame does not establish WEC, which quantifies over all timelike observers. Published counteranalysis finds energy-condition violations under its stated assumptions. This does not prove every modified-gravity warp model impossible, but it prevents using "positive energy density" as a completed solution.

### Ponderomotive-force scaling

The launch file implies that increasing electromagnetic frequency progressively bridges acoustics to spacetime control. The standard nonrelativistic ponderomotive force is

\[
\mathbf F_p=-\frac{q^2}{4m\omega^2}\nabla E_0^2.
\]

At fixed field amplitude and gradient, this decreases with \(\omega^2\). Frequency scaling by itself is not a route from plasma actuation to gravitational source control.

### Acoustic analogy

The acoustic standing-wave analogy can motivate phase-controlled actuation, but it does not supply momentum conservation, radiation accounting, or a gravitational source model. A moving acoustic trap and a moving metric profile are not the same physical mechanism.

### Energy integral

The scaling

\[
|E_{\rm wall}|\sim C\frac{c^4}{G}\frac{\beta^2R^2}{\Delta}
\]

is a useful order-of-magnitude diagnostic, but it is a profile-dependent source integral, not generator fuel consumption. It does not establish feasibility, controllability, or power requirements.

## Reusable content

The report's strongest reusable content is its requirements list:

1. Fully specified formation, acceleration, cruise, steering, braking, and shutdown.
2. Source stress tensor derived from a specified field theory.
3. Observer-complete energy-condition analysis.
4. Quantum-inequality and backreaction analysis where negative energy appears.
5. Classical and semiclassical stability analysis.
6. Causal analysis, including closed timelike curves.
7. Full energy, mass, momentum, and control-power budget.
8. Experimental discrimination from ordinary electromagnetic, plasma, or mechanical effects.

## Bottom line

Use the report as a checklist after correcting the Van Den Broeck reversal and quarantining the 2026 observer-robust claim. Do not use it as a source of settled positive-energy warp results.
