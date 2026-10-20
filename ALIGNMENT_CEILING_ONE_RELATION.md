# The Alignment Ceiling — an independent convergence

**ADCCL is not physics.** It is an engineering threshold, found by watching autonomous
reasoning loops degrade and setting the cosine-similarity rejection boundary where they
stopped collapsing. Nothing in that procedure knows anything about Kerr geometry.

That is what makes the result worth stating:

$$\text{measured } 0.9539 \qquad\text{vs}\qquad
\sqrt{\theta(2-\theta)}\big|_{\theta=0.7} = 0.953939\ldots
\qquad \Delta = 3.9\times10^{-5}$$

**Five decimal places, from an engineering measurement that had no geometric input.**

The claim is therefore *convergence*, not identity. "Reasoning drift is black-hole
physics" would be the weak version — it invites the objection that the resemblance was
built in. "An unrelated measurement independently reproduced the value" is the strong
one, and it is what happened.

Note this also settles the direction of the earlier back-construction worry: the number
arrived from the engineering side and the expression from the geometric side. They were
not fitted to each other.

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

**Equipartition *is* the 45° split** — half aligned, half not. That number is the floor
$\chi = 1/\sqrt{2}$. The physics gate is a different input, $\theta = 0.7 = n/N$, the
active-dimension fraction. The two are 1% apart and are not the same symbol.

## The ceiling is the two-channel union of that same alignment

$$P(\ge 1 \text{ of } 2) = 1-(1-\theta)^2 = \sqrt2-\tfrac12 = 0.914213562\ldots$$
$$\chi_s=\sqrt{P}=0.956145158\ldots$$

## The two ceilings, in degrees

| | cosine | **angle** | provenance |
|---|---|---|---|
| equipartition $\theta$ | 0.707107 | **45.000°** | derived (exact) |
| derived ceiling $\chi_s$ | 0.956145 | **17.031°** | derived from $\sinh\psi=1$ |
| measured ceiling $\tau$ | 0.953900 | **17.465°** | measured on ADCCL reasoning loops |

$$\boxed{\text{measured } 0.9539 \;\text{vs}\; \sqrt{\theta(2-\theta)}\big|_{0.7}=0.953939
\qquad \Delta = 3.9\times10^{-5}}$$

The $\theta=1/\sqrt2$ branch gives $\chi_s = 0.956145$, which is $2.2\times10^{-3}$ from
the measurement — **sixty times further**. The tight convergence is to the $\theta=0.7$
evaluation, and comparisons should be made against that value, not against $\chi_s$.

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

Keep the two inputs apart. The floor is $\chi=1/\sqrt{2}=0.70710678$. The gate is
$\theta=0.7$. Rerun 2026-10-16:

| input | ceiling $\sqrt{\theta(2-\theta)}$ | angle | distance to measured $\tau=0.9539$ |
|---|---|---|---|
| $\theta=0.7$ | $0.953939201$ | $17.458^\circ$ | $3.92\times10^{-5}$ ($0.0075^\circ$) |
| $\theta=1/\sqrt{2}$ | $\chi_s=0.956145158$ | $17.031^\circ$ | $2.25\times10^{-3}$ ($0.434^\circ$) |

The $\theta=0.7$ evaluation sits on the measured ceiling. The equipartition evaluation is
57 times further from it. $\theta=0.7$ is not the floor written short. It is also not an
output of the Data Processing Inequality: that inequality gives $\theta=I/H=n/N$, and the
value is 0.7 when the active fraction is 0.7. The product of the floor and the
$\theta=0.7$ ceiling is 0.6745, which is 2.7% under $\ln 2$.

See `TWO_CHANNEL_CEILING_ANALYSIS.md`, `RECOVERED_MATERIAL.md` §4,
`06_unification_and_spin/README.md`.

## Physics, not the program

The program stores these as cosines between vectors. On a lossless line the same algebra
is a power split. Delivered power is $T = 1-|\Gamma|^2$. Rerun 2026-10-16, exact:

| role | value in the program | as a wave | reflected fraction $\|\Gamma\|^2$ | $\|\Gamma\|$ |
|---|---|---|---|---|
| floor, two equal modes | $\chi=1/\sqrt{2}$ | half the power returns | $1/2$ | $1/\sqrt{2}=0.707106781$ |
| gate, active-mode fraction | $\theta=n/N=0.7$ | 0.7 of the power stays in the forward channel | $0.3$ | $\sqrt{0.3}=0.547722558$ |
| ceiling, two-channel union | $\kappa=\sqrt{0.91}$ | delivered power $\kappa^2=0.91$ | $0.09$ | $0.3$ exactly |

The floor is the circle where the forward and backward waves carry the same power. The
gate is a smaller circle, 30% of the power coming back. The ceiling is the circle where
9% comes back. These are three radii on the reflection disk. They are not three names
for $1/\sqrt{2}$.

Reading $\theta=n/N$ as the delivered power $T$ is an identification, `[O]`. The equality
$T=1-|\Gamma|^2$ and $\kappa^2=\theta(2-\theta)$ are algebra, `[D]`. Nothing in this table
is a galaxy speed, a screening edge, or a Cassini bound. The software threshold is the
implementation of the cosine. The wave is the object.
