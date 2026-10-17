# Four dwarfs at the working Lagrangian zero

**Pre-registration:** `PREREG_DWARF_ML_WORKING_C_2026-10-16.md`, commit `0c52fe8`. Newton control matches `BRANCH_RULE_SATELLITES.json` with maximum relative difference \(3.16\times10^{-7}\). The run is informative.

**Tier.** The four decision values are `[D]`, in `DWARF_ML_WORKING_C.json`. The dispersion is the Wolf formula in the pre-registration, \(\sigma^2 = g_{\rm in} r_h/3\), not the McGaugh isolated branch used for \(\nu_6\).

**Verdict.** Pass. All four decision values at \(\sigma-1\sigma\) are \(\le 3\).

| Dwarf | Screen M/L at \(\sigma-1\sigma\) | \(g_W\) at that mass (m s\(^{-2}\)) |
|---|---|---|
| Crater II | 0.0599 | \(-4.3\times10^{-31}\) |
| Carina | 0.929 | \(-1.7\times10^{-22}\) |
| Leo II | 2.659 | \(-8.0\times10^{-20}\) |
| Sculptor | 1.335 | \(-1.6\times10^{-20}\) |

\(g_W\) is negligible next to \(g_N\). Leo II comes down from the \(\nu_6\) value 6.558 because this solve uses \(\nu_{\rm eff} g_N\) inside the Wolf formula, with \(S \approx 1\). It does not come down because of the \(W\) term.
