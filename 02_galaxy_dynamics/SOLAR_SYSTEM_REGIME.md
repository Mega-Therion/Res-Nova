# Solar-system regime, galaxy scale held fixed

**Date:** 2026-10-04

The galaxy scale \(a_0 = 1.16306\times 10^{-10}\,\mathrm{m\,s^{-2}}\) (SPARC T3) is the input. No horizon formula is used. Two actions already in the variational note are expanded here, in the regime planets actually occupy: the Sun's field is enormous compared with \(a_0\), and the Milky Way's field at the Sun is only about twice \(a_0\).

## Isolated planet **[D]**

At Mercury, \(g_N = GM_\odot/r^2 = 0.0396\,\mathrm{m\,s^{-2}}\), so \(g_N/a_0 \approx 3.4\times 10^8\).

**G.O.D., Branch B.** The dual-channel potential \(\mathcal{F}_{\rm dual} = \tfrac12 x^2 - x + \ln(1+x)\) gives \(\mu = x/(1+x)\). For a strong field the extra acceleration does not die. It tends to a constant of size \(a_0\), here \(1.16\times 10^{-10}\,\mathrm{m\,s^{-2}}\). That is the offset already known to fail planetary bounds. The algebra of this branch remains a Lean identity. The solar-system reading does not.

**ITT shape, Branch C.** \(\mu = x/\sqrt{1+x^2}\) gives an extra acceleration \(a_0^2/(2 g_N) = 1.71\times 10^{-19}\,\mathrm{m\,s^{-2}}\) at Mercury. That is \(6.8\times 10^8\) times smaller than the G.O.D. offset. The isolated-Sun monopole is not the problem for this shape.

## Sun inside the Milky Way **[D]**

The external field is \(g_e = 1.9\) to \(2.4\times 10^{-10}\,\mathrm{m\,s^{-2}}\), so \(\eta = g_e/a_0\) is 1.63 to 2.06. Neither action is in a screened limit there. The Cassini quadrupole, same integrator as `efe_quadrupole_q2.py`, at this galaxy scale:

| Action | \(Q_2\) at \(1.9\times 10^{-10}\) | \(Q_2\) at \(2.4\times 10^{-10}\) | 2014 | 2026 |
| --- | ---: | ---: | ---: | ---: |
| ITT / Branch C, \(\mu_{\rm std}\) | \(1.91\times 10^{-26}\) | \(2.01\times 10^{-26}\) | +5.4σ to +5.7σ | +9.7σ to +10.3σ |
| G.O.D. / Branch B, \(\mu_{\rm dual}\) | \(2.77\times 10^{-26}\) | \(3.60\times 10^{-26}\) | +8.2σ to +11.0σ | +14.5σ to +19.1σ |

\(Q_2\) is in \(\mathrm{s^{-2}}\). Both fail. G.O.D. fails by more. No screen was added. Numbers: `SOLAR_SYSTEM_REGIME.json`.

## What the regime is

In the solar system the galaxy-anchored theory is an external-field quadrupole on top of a tiny monopole, for the ITT shape, and a constant acceleration offset, for the G.O.D. dual channel. The quadrupole is the test that bites the shape which otherwise fits the turnover. The constant offset kills the dual channel before the quadrupole is even needed.

A screen is still not derived. **[E]** would be an extra potential or a higher-derivative term that cuts \(Q_2\) below the Cassini window while leaving the galaxy turnover alone. Nothing in Branch B or Branch C does that at \(\eta \sim 2\).
