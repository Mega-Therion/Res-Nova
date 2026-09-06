# The Alignment Ceiling — one relation, two substrates

The coherence ceiling in the Anti-Drift Cognitive Control Loop and the spin ceiling in
Kerr geometry are **not two constants that happen to be close.** They are one relation
about alignment, realised in two substrates. Stated in angles rather than cosines, this
is visible immediately.

## The shared object

Both quantities are **direction cosines of an alignment**:

| substrate | quantity | what it measures |
|---|---|---|
| ADCCL (reasoning) | $\chi$ | cosine of the angle between a reasoning state and its task anchor |
| Kerr (spacetime) | $a^* = \tanh\psi$ | alignment of angular momentum with the hole |

A ceiling on a direction cosine is a **maximum permissible drift angle**. That is the
object; the decimals are its cosine.

## Equipartition is exactly 45°

The selecting condition is the same in both: relativistic momentum equal to rest mass,

$$\sinh\psi_0 = 1 \;\Longrightarrow\; \psi_0=\ln(1+\sqrt2),\quad \gamma=\sqrt2,\quad
\theta=\tanh\psi_0=\tfrac{1}{\sqrt2}$$

and

$$\tfrac{1}{\sqrt2} = \cos 45^\circ \quad\text{exactly.}$$

**Equipartition *is* the 45° split** — half aligned, half not. This is why $\theta$ is the
same number in a cognitive gate and in a black hole: both are asking when a system is
evenly divided between alignment and drift.

## The ceiling is the two-channel union of that same alignment

$$P(\ge 1 \text{ of } 2) = 1-(1-\theta)^2 = \sqrt2-\tfrac12 = 0.914213562\ldots$$
$$\chi_s=\sqrt{P}=0.956145158\ldots$$

## The two ceilings, in degrees

| | cosine | **angle** | provenance |
|---|---|---|---|
| equipartition $\theta$ | 0.707107 | **45.000°** | derived (exact) |
| derived ceiling $\chi_s$ | 0.956145 | **17.031°** | derived from $\sinh\psi=1$ |
| measured ceiling $\tau$ | 0.953900 | **17.465°** | measured on ADCCL reasoning loops |

$$\boxed{\text{measured } 17.465^\circ \quad\text{vs}\quad \text{derived } 17.031^\circ
\qquad \Delta = 0.43^\circ}$$

An empirically observed collapse boundary — found by watching autonomous reasoning loops
degrade — sits **within half a degree** of an angle derived from Kerr equipartition. In
cosine form (0.9539 vs 0.956145) the same fact reads as a 0.0022 discrepancy and invites
the wrong question, which is why the two were previously treated as rival values for one
constant.

## What this is, and what it is not

**It is:** a single relation — a two-channel alignment ceiling at $\theta=\cos45^\circ$ —
instantiated in two substrates, with an independent empirical determination in one of them
agreeing with the derivation in the other to 0.43°.

**It is not yet:** a proof that the substrates share a mechanism. Two things are needed.
First, $\sinh\psi=1$ is *adopted*, not selected by a covariant argument
(`rapidity_uniqueness_results.json` records `physical_selection_status: "NOT DERIVED"`);
the algebra beneath it is exact to 100 decimal places. Second, $\tau$ was tuned on one
pipeline — RY's own genesis note says it "has not been validated against external agent
systems or alternative LLM providers," and is "one engineering benchmark away from being
either a deep fact or a local artifact."

**The decisive test is therefore cheap and external:** measure the drift-collapse angle on
agent systems that are not Chyren. If independent pipelines also fail near 17°, the
relation is substrate-independent and the isomorphism is real. If they scatter, $\tau$ is
local and only $\chi_s$ survives.

## Consequence for the corpus

Stop presenting $\kappa_Y=\sqrt{\theta(2-\theta)}$ at $\theta=0.7$ as a derivation of
0.9539. There is one derived ceiling, $\chi_s=0.956145$ at $\theta=1/\sqrt2$, and one
measured ceiling, $\tau=0.9539$. Writing $\theta=0.7$ is the floor written short; it is not
a second value of $\theta$.

See `TWO_CHANNEL_CEILING_ANALYSIS.md`, `RECOVERED_MATERIAL.md` §4,
`06_unification_and_spin/README.md`.
