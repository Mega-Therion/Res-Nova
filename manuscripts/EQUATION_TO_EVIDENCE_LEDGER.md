# Equation-to-evidence ledger — publication gate

**State:** Initial ledger assembled from the canonical current-state record (last verified there: 2026-10-21). Not an independent reproduction. Update with pinned commit, exact commands, logs, and reviewers before submission.

| Claim / object | Current status | Evidence recorded in repository | What this evidence establishes | Remaining gate |
|---|---|---|---|---|
| Standard interpolation \(\mu_{std}(x)=x/\sqrt{1+x^2}\) | [D] / formal core partly [P] | Lean theorem named `MuStdUniqueness.theorem_A_constitutive`; `MuStdFoundations`; current-state record | Formal result for the stated mathematical proposition under theorem assumptions | Verify theorem-to-manuscript correspondence and include assumptions |
| Primitive \(F_{std}(x)=\frac12[x\sqrt{1+x^2}-\operatorname{arsinh}x]\) with \(F' = x\mu_{std}\) | [D] | Analytic differentiation; convex-duality work note / associated tests | Variational primitive identity for the constitutive law | Include exact conventions, dimensions, and reproducible symbolic/numerical check |
| Convex conjugate / inverse mapping | [D] | Derived parametric expressions and floating-point spot checks reported in research notes | Mathematical duality identity on the specified monotone branch | Re-run tests and distinguish a scalar constitutive dual from a physical Hamiltonian |
| SPARC Tier 0, \(\mu_{std}\) | [C] | Current state reports MOND 9.93 vs G.O.D. 11.08; generated tables / parameter ledger | Current benchmark record favors MOND under this tier | Clean-environment reproduction; state metric, masks, exact commands, uncertainties |
| SPARC Tier 1, \(\mu_{std}\) | [C] | Current state reports MOND 3.36 vs G.O.D. 3.41; aggregate 6.09 vs 6.03 | Near tie in the reported aggregate | Reproduce; clarify aggregation and statistical significance; no superiority claim yet |
| Current parameter count | [C] | Current state: 374 = 171 disk M/L + 32 bulge M/L + 171 gas-distance factors | Recorded budget definition | Verify generated benchmark table uses this budget and state which parameters are active per tier |
| SPARC sample and NFW comparison | [C] | `RESULTS.md`: 171/175 galaxies, 3,375 points; NFW Tier 1 median 1.92 with 716 parameters vs 374 for each \(\mu_{std}\) row | NFW has lower reported Tier-1 median with 342 additional parameters; this is not a matched-complexity claim | Reproduce pipeline; report parameter budget and model-selection caveats |
| Spherical AeST scalar/total-law correspondence | [D] for derived mapping; branch choice [O] | `AEST_TOTAL_SCALAR_CORRESPONDENCE_2026-10-14.md`, 26 checks per current-state record | Parametric correspondence and static ghost conditions under stated assumptions | Resolve D7/D9 choice; do not conflate scalar-channel function and total acceleration law |
| D7/D9 normalization and action selection | [O] | Current-state record notes \(a_0\) vs \(\tilde a_0=(1+\lambda_s)a_0\), and no selection rule choosing D7 branch | Identifies a live convention/branch ambiguity | Freeze one action, dimensions, normalization, metric variation and boundary terms |
| QUMOND-level Cassini check for selected screening | [C] at surrogate level | Muse/Block report for \(\nu_6\) route; current state documents separate tidal-screen analyses | A particular quasistatic calculation meets a numerical criterion | Does not establish full covariant-theory Cassini pass; own-theory C2/C3 and full action required |
| C2 spherical anchor / C3 axisymmetric own-theory solution | [O] / pending | Block handoff identifies these as next gates | No final result asserted here | Run with frozen inputs; save residuals, convergence, solver logs and machine-readable output; independent rerun |
| Tidal screen with preregistered \(C=0\) | [X] | `OORT_TORQUE_2026-10-16.md` and `SCREENED_C_SOLUTIONS.json` cited by current-state record | Current record says preregistered branch fails Oort-cloud criterion | Preserve as failed branch; do not erase with later parameter choices |
| Tidal screen with working \(C\approx0.579124707982253\) | [C] / [O] | Current-state record reports several follow-up comparisons and labels \(C\) tuned, not derived | Some comparisons improve at an additional declared input | Count parameter honestly; independent reproduce; pass all constraints without retuning; derive \(C\) or keep phenomenological |
| One-field environmental \(\chi\) screen | [O] | Current-state record reports incompatible required environmental values and worsened SPARC fit under own-field variant | Tested construction does not solve both environmental demands | No promotion without a new derivation and full tests |
| GW170817 tensor speed / matter coupling | [O] pending full model | Current-state record discusses cone coincidence for matter on \(g\), and strong bound on disformal matter-metric term | Constrains candidate couplings in stated setup | Derive from the exact canonical action and show branch-wide result |
| High-redshift \(a_0(z)\) trend | [O] | Current-state record notes pressure-support scale sensitivity and unresolved systematics | Not a secure prediction at present | Keep outside core manuscript pending decisive independent analysis |
| HDE / \(\ln2\) cosmological branch | [X] for the tested late-time edge; \(\ln2\) [O] | Current-state record reports \(\Delta\chi^2=+46.3\) against \(\Lambda\)CDM under the fixed CMB block and DESI DR2 exclusion of phantom-crossing window | Tested edge fails stated criterion; coefficient remains underived | Do not advertise as a success; separate paper only if new evidence changes verdict |
| ITT curvature claim | [O] | Not established by galaxy-sector evidence | No validated bridge currently asserted | Require action, normalization, variation, conservation, weak-field limit and independent test |
| Warp-drive / TTEY route | [O] | Current-state record says proposed massive double-well scalar is separate and not derived by galaxy action | The galaxy-sector NEC result does not provide the needed exotic-energy source | Exclude from this manuscript unless separate field existence and energy accounting are derived |

## Release rules

1. No claim is upgraded by prose alone. Each row needs a pinned source commit and exact evidence artifact.
2. Keep [P], [D], [C], [O], and [X] distinctions in the manuscript.
3. A pass on a surrogate equation is not a pass for the covariant model.
4. Do not mix branches or parameters across tests.
5. Report every failed preregistered test and all post-hoc changes.
6. If C2/C3 or full covariant constraints remain open, publish only a narrower benchmark/variational paper with explicit limitations.
