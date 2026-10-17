# Cassini at the working Lagrangian zero

**Setup.** \(x^* = 7.035884281332817\times 10^{11}\) is held fixed. \(C = 0\) is the published action-form calibration. The working value is `C_oort_peak` at \(g_e = 1.9\times 10^{-10}\), \(C = 0.579124707982253\). Only the \(W\) tensor sees \(C\): \(P(y)\) in \(W_{ij}\) is replaced by \(P(y)-C\). \(\nu_{\rm eff}\) is not changed. The run is `cassini_at_working_c.py`, same grid as `cassini_Q2` at resolution 1.

**Tier.** The four quadrupole numbers are `[D]`, in `CASSINI_AT_WORKING_C.json`. The \(C = 0\) row reproduces the published action-form table: \(5.20\) and \(3.99\times 10^{-27}\,\mathrm{s}^{-2}\), with \(W\) parts \(4.44\) and \(3.58\).

**Result.** Both Galactic fields stay inside the two-sided \(2\sigma\) window \([-2.0, 5.2]\times 10^{-27}\,\mathrm{s}^{-2}\). At \(1.9\times 10^{-10}\), \(Q_2 = 5.200000\times 10^{-27}\) at \(C = 0\) and \(5.200000\times 10^{-27}\) at the working \(C\). At \(2.4\times 10^{-10}\), both are \(3.991075\times 10^{-27}\). The \(W\) parts differ by about \(2\times 10^{-15}\) relative. `passes_both_fields` is true.

A constant \(C\) does not source this quadrupole. On the same grid the whole \(W\) piece comes from \(2.8\times 10^3\)–\(1.25\times 10^4\) au, and the integral of the pure constant piece is \(-2.3\times 10^{-42}\,\mathrm{s}^{-2}\) against a \(P(y)\) piece of \(4.44\times 10^{-27}\). The radial variation of \(P\) through that shell is what the quadrupole sees. \(x^*\) does not have to move.
