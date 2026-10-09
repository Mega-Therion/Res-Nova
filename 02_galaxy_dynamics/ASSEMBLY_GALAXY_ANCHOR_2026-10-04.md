# Assembly: galaxy fixed, horizon not the anchor

**Date:** 2026-10-04

In this note, **[E]** means exploratory theoretical physics: a joint that fits the pieces we already have and has not been given its own measurement. It is not a Res-Nova empirical result, and it is not a proof. House tags keep their usual meaning: **[P]** Lean or exact algebra, **[D]** a derivation or a direct computation already in the tree, **[C]** a cited result, **[O]** open, **[X]** withdrawn.

## What is fixed

The anchor is the acceleration scale measured in galaxies. Locally that is the SPARC T3 value \(1.163\times 10^{-10}\,\mathrm{m\,s^{-2}}\) **[C]**, in the same neighborhood as the literature \(1.2\times 10^{-10}\,\mathrm{m\,s^{-2}}\) **[C]**. It is an input. Nothing below derives it from the expansion.

## The pieces that lock

1. **The turnover.** With that scale held fixed, the force law that survives is
   \(\mu(x) = x/\sqrt{1+x^2}\). SPARC was rerun on this function **[D]**. The other function, \(x/(1+x)\), leaves an unscreened offset and fails the solar system by about \(5.7\times 10^5\) **[X]**.
2. **The same shape falls out of the information-tension calculus.** The 2026-08-04 fact-check re-derived \(f(y)=\sqrt{y(1+y)}-\mathrm{arcsinh}\sqrt{y}\) and obtained \(f'(x^2)=x/\sqrt{1+x^2}\) **[D]**. That step does not use \(cH/2\pi\). The length in that writeup, \(\ell=c^2/a_0\), takes \(a_0\) from the galaxies.
3. **The algebra around that function checks.** The AeST embedding \(2J'=\mu_{\rm std}\) and the related identities are Lean-checked mathematics **[P]**. They certify the encoding. They do not say the sky is that theory.
4. **On SPARC the scale is not a second theory.** Same \(\mu\), 3,375 points. Tier 0: horizon declaration median reduced \(\chi^2\) 11.08, literature scale 9.93 **[D]**. Tier 1, 374 shared nuisances: 3.36 and 3.41 **[D]**. Once the nuisances are free, the two declarations are not distinguished.

## The piece that does not lock

\(cH(z)\) moves with the expansion. Held against the galaxy anchor it does not stay in ratio (`04_cosmology/GALAXY_ANCHOR_HORIZON.md`) **[D]**:

| Epoch | \(cH\) / galaxy | \((cH/2\pi)\) / galaxy |
| --- | ---: | ---: |
| \(z=0\) | 5.63 | 0.90 |
| \(z\approx 0.9\) | 3.58 | 0.57 |
| \(z\approx 2\) | 7.33 | 1.17 |

The thermal match derives \(a=cH\), and the \(2\pi\) cancels **[P]**. Putting the \(2\pi\) back by hand is a today-only near miss, about 10% low, and it wanders at earlier times. High-redshift galaxy scales are flat from \(z=0.6\) to \(2.6\) **[C]**, and the step from \(z=0\) is calibration-limited **[O]**. The horizon expression is not the anchor.

## What the screen still has to do

Unscreened \(\mu_{\rm std}\) at the galaxy scale fails Cassini's external-field quadrupole **[D]**. A phenomenological screen can be written so that a number passes. It has no covariant realization yet **[O]**. The disformal equation printed in the information-tension paper adds a scalar to a tensor and is ill-formed **[X]** as a disformal metric. The chameleon minimum that does work in the fact-check is the textbook linear coupling, not that equation. D7's branch, which would have to carry a covariant screen, is open: at one grid, \(K_B=0.25,0.5,1\) all converge and none is a held remnant **[O]**.

Unscreened, the strong-coupling range is 109–114 μm (109–118 μm once the true horizon anchor cH₀/2π is included and the live a₀ is used; `LAMBDA_SC_UNSCREENED.json`, 2026-10-09), inside the window where a gravitational-strength fifth force is quoted as excluded **[D]**. Screening is not used in that comparison.

## Exploratory assembly **[E]**

Read as one picture, the pieces that lock say this:

The galaxies set a scale. Around that scale the turnover is \(\mu(x)=x/\sqrt{1+x^2}\), which is also the derivative the information-tension function produces when the galaxy scale is used as the length. The cosmic horizon is a different scale. It is several times larger in the form the thermal match actually gives, and the hand-inserted \(2\pi\) form only neighbors the galaxies today. A screen is required at the solar system and is not yet the covariant one.

That paragraph is **[E]**. It does not add a new constant, and it does not claim the information-tension paper's disformal metric, its lensing prediction, or its old SPARC headline. Those failed their checks and stay failed. The next calculation that would promote or kill the **[E]** picture is a screen derived from the repaired coupling, tested on Cassini, without borrowing \(cH/2\pi\).
