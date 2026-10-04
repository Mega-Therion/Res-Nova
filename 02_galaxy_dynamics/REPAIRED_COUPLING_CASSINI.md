# Repaired coupling, tested on Cassini

**Date:** 2026-10-04. **[D]** for the quadrupole numbers. **[E]** only for the sentence at the end about what would have to be added next.

The information-tension equation that added \(\partial_\mu\chi\partial^\mu\chi\), a scalar, to the metric is ill-formed. The repair is the ordinary disformal tensor

\[
\tilde g_{\mu\nu} = g_{\mu\nu} + B\,\partial_\mu\chi\,\partial_\nu\chi.
\]

`repaired_coupling_cassini.py` checks that the added term is a 4×4 tensor. That repair does not by itself change the quasi-static galaxy law. Around the galaxy scale the law in use is still \(\mu(x)=x/\sqrt{1+x^2}\).

Cassini cares about the Sun sitting in the Milky Way's field, \(g_e \approx 1.9\) to \(2.4\times 10^{-10}\,\mathrm{m\,s^{-2}}\). The galaxy anchor is \(1.163\times 10^{-10}\,\mathrm{m\,s^{-2}}\), so \(\eta = g_e/a_0\) is 1.63 and 2.06. That is not the deeply screened regime. The fractional correction \(\mu\) itself supplies there, \(a_0^2/(2g_e^2)\), is 0.19 and 0.12.

The quadrupole at that anchor, same integrator as `efe_quadrupole_q2.py`:

| \(g_e\) | \(Q_2\) | 2014 (3±3) | 2026 (1.6±1.8) |
| --- | ---: | ---: | ---: |
| \(1.9\times 10^{-10}\) | \(1.91\times 10^{-26}\,\mathrm{s^{-2}}\) | +5.4σ | +9.7σ |
| \(2.4\times 10^{-10}\) | \(2.01\times 10^{-26}\,\mathrm{s^{-2}}\) | +5.7σ | +10.3σ |

Both fail the 2014 one-sigma window and the 2026 two-sigma window. No free screen was inserted.

**[E].** A further mechanism, a potential that gives the field a mass inside the Sun, or a higher-derivative term, could still be written down. Nothing in the repaired coupling produces it. Until that extra piece is specified and run through this same quadrupole, ITT is a galaxy-scale effective description with a matching derivative, not a theory that passes the solar system.
