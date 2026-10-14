# Source-matching calculation map

**Date:** 2026-10-14  
**Status:** Research specification. Not a warp-drive solution, branch selection, or model adoption.

## Goal

Determine whether a specified conventional matter source—electromagnetic fields, charged plasma, apparatus stresses, and payload—can support a proposed AeST geometry.

## 1. Fix the gravitational candidate

Choose one frozen AeST specification:

- Fields: \(g_{\mu\nu},A^\mu,\phi,\lambda\), matter.
- Action: one AeST action plus minimally coupled matter.
- Constitutive function: the actual function under test.
- Parameters and normalization.
- Boundary treatment.
- Domain of validity.

Do not mix the scalar-channel function with the total-law function. The repository currently retains D9's scalar-channel function; the total-law correspondence function is a separate, open model choice.

## 2. Specify the physical source

Use a conventional matter action:

\[
S_{\rm matter}=S_{\rm EM}+S_{\rm charged\ fluid}+S_{\rm apparatus}+S_{\rm payload}.
\]

For each component specify:

- Dynamical variables.
- Equation of state or constitutive relation.
- Currents and charge density.
- Boundary conditions.
- Energy supply and dissipation.
- Stress tensor.
- Conservation laws.

Use a distinct electromagnetic field strength, such as \(\mathsf F_{\mu\nu}\), to avoid confusion with AeST's vector field strength \(F_{\mu\nu}=2\nabla_{[\mu}A_{\nu]}\).

## 3. Write the coupled equations

The metric equation has the schematic form

\[
G_{\mu\nu}=U^{\rm AeST}_{\mu\nu}+8\pi\widetilde G\,T^{\rm matter}_{\mu\nu}.
\]

The full system is:

1. Metric equation.
2. AeST vector equation.
3. AeST scalar equation.
4. Vector normalization \(A^\mu A_\mu=-1\).
5. Maxwell equations for \(\mathsf F_{\mu\nu}\).
6. Charged-fluid equations.
7. Apparatus equations.
8. Payload equations.
9. Boundary and initial-data conditions.

## 4. Define the target diagnostic

For a proposed target metric \(g_{\rm target}\), define

\[
\mathcal R_{\mu\nu}
=
G_{\mu\nu}[g_{\rm target}]
-
U^{\rm AeST}_{\mu\nu}[g_{\rm target},A,\phi,\lambda]
-
8\pi\widetilde G\,T^{\rm matter}_{\mu\nu}.
\]

Source matching requires

\[
\mathcal R_{\mu\nu}=0
\]

together with all other field equations.

A nonzero \(\mathcal R_{\mu\nu}\) is not automatically a failure of the theory; it means the proposed source does not support that target geometry under the specified model.

## 5. Separate the calculations

| Stage | Output | Failure meaning |
|---|---|---|
| Geometry | Target metric and its curvature | No physical interpretation yet |
| AeST response | \(U^{\rm AeST}_{\mu\nu}\) and vector/scalar residuals | Geometry is not supported by the chosen AeST fields |
| Matter response | EM, plasma, apparatus, payload stress | Conventional source does not supply the remainder |
| Coupled solution | All residuals vanish | Candidate source supports the geometry in the tested regime |
| Transport | Formation, acceleration, steering, braking | No demonstrated vehicle or control mechanism |
| Stability | Perturbation and backreaction analysis | No demonstrated stable configuration |
| Observability | Metric, timing, lensing, or field signature | No experimental discriminator yet |

## 6. Start with a bounded test

Do not begin with a superluminal bubble. Begin with a subluminal, weak-field, localized configuration:

1. Choose a smooth, localized metric perturbation.
2. Choose a conventional EM/plasma source model.
3. Solve the coupled equations numerically or perturbatively.
4. Compute the required residual source.
5. Compare it with the physical source's actual stress tensor.
6. Report the deficit or excess component by component.

## 7. Conservation and accounting

Any transport claim must account for:

- Electromagnetic field energy and momentum.
- Plasma energy, momentum, and particle flux.
- Apparatus stresses and control power.
- Payload momentum.
- Radiation emitted or absorbed.
- Asymptotic gravitational field and ADM-type mass.
- Waste heat and dissipation.

A local field configuration cannot be promoted to a vehicle without this accounting.

## 8. Pass/fail criteria

A source-matching calculation passes only if:

- The AeST equations are satisfied.
- The matter equations are satisfied.
- The vector normalization is satisfied.
- The electromagnetic equations are satisfied.
- The proposed source stress tensor equals the required source, not merely one component.
- The configuration remains within the declared validity domain.
- The result is reproducible from stated inputs.

A positive energy density in one frame, a nonzero field amplitude, or a visual analogy with acoustic levitation does not satisfy these criteria.
