# Falsification and Quarantine Ledger

**Generated** from `assurance/claims.json` by `scripts/build_quarantine_ledger.py`. Do not edit by hand; edit the registry and regenerate.

**Registry digest:** `1e3c0900c8151fcf`  |  **schema:** 1.1  |  **records:** 62 (38 live, 24 retracted)


This is the red-team record of the program. Every entry below was killed by our own verification stack, and each carries the exact margin by which it failed. It is published before the surviving theory because a reader who can see what we killed can judge what is left.


## 1. What was killed, and by how much

| Claim | What it asserted | Exact failure margin | Receipt |
|---|---|---|---|
| `CLM-05` | The superseded historical 382-parameter SPARC fit must not be presented as the current canonical fit; the current matche | This record governs wording and comparison scope; it is not itself a new fit. | `assurance/claims.json` |
| `CLM-12` | RETIRED | The uniqueness theorem is correct and, precisely because it is, it excludes the live theory: Pade[1/1] + mu(0)=0 + mu(inf)=1 + mu'(0)=1 has the unique | `audits/2026-11-18/verify_untested_claims.py` |
| `CLM-13` | RETIRED | Solving F'^2 I(mu) = x^3 gives mu = x/(1+x) exactly, so the identity CHARACTERISES the retired branch rather than merely describing it. Substituting m | `audits/2026-11-18/verify_untested_claims.py` |
| `CLM-15` | RETRACTED: the anti-drift gate 'u >= gamma <=> chi >= theta' is false | The ceiling C_max = theta is a standard optical-Bloch result. What remains a framework claim, and is not established here, is the identification of th | `assurance/claims.json` |
| `CLM-19` | mass-claim retraction (state retracted) | Mass predictions withdrawn 2026-10-03; the Lean mass modules (LeptonMassCollar, QuarkMassLadder) fit measured masses and do not predict them. | `assurance/claims.json` |
| `CLM-D2-00` | RETIRED | The uniqueness is real but its conclusion is the falsified function. 'First principles' here means four adopted constraints, one of which is the very  | `audits/2026-11-18/verify_untested_claims.py` |
| `CLM-D2-01` | RETIRED | Internally consistent and correctly proved, and that is the problem: the constraint set is satisfiable by exactly one function and it is not the one t | `audits/2026-11-18/verify_untested_claims.py` |
| `CLM-D2-02` | RETIRED | mu_std = x/sqrt(1+x^2) is irrational, so no member of the Pade[1/1] class is the live model and this theorem cannot be a derivation of it. Retired 202 | `audits/2026-11-18/verify_untested_claims.py` |
| `CLM-D2-03` | RETIRED | mu(odds(p)) - p = 0 for x/(1+x) and equals -p - p/((p-1) sqrt(p^2/(p-1)^2 + 1)) for mu_std. The Bayesian-odds property is a property of x/(1+x) alone, | `audits/2026-11-18/verify_untested_claims.py` |
| `CLM-D2-04` | RETIRED | Algebraic identity that characterises mu = x/(1+x). See CLM-13 for the exact failure factor x + sqrt(1+x^2) under mu_std. Retired 2026-11-18 on audits | `audits/2026-11-18/verify_untested_claims.py` |
| `CLM-D3-01` | MOND correction at Earth is approximately 2e-8 (1-mu, non-relativistic force law); the previously stated '1137x below Ca | The retracted '1137x below Cassini' framing must not be cited; only the corrected ~2e-8 (1-mu) figure and TARGET_D3 Theorem 3.1 are live. | `assurance/claims.json` |
| `CLM-D3-03` | Vainshtein screening resolves the Q2 tension: the screened Q2 sits 119x below the Cassini bound (corrected 2026-09-12 fr | RETRACTED 2026-09-30. The 119x figure was computed with F''/F' of the retired F_dual action, and TARGET_D7 sec.11.3 shows the c_T = c-safe Vainshtein  | `assurance/claims.json` |
| `CLM-D3-05` | gamma = beta = 1 exactly, Cassini margin 1.1e8, MESSENGER margin 1.6e5 (TARGET_D3 Sec.7). | Void: derived for a generalized Einstein-aether action (D7-as-originally-written), which was not D9's actual AeST action. Under the corrected AeST, Ps | `assurance/claims.json` |
| `CLM-D5-02` | RETIRED | Two independent defects. (1) The formula 1/(2x0^2(1+x0)) is not F''/F' for any branch; the correct ratio is (x+2)/(x(x+1)) for F_dual and (x^2+2)/(x^3 | `audits/2026-11-18/verify_untested_claims.py` |
| `CLM-D6-03` | The strong-coupling scale is approximately 1e-10 eV, far below the energy scales of current experiments. | RETRACTED (unit error found 2026-09-12): a0^2/G is an energy density, so its bare fourth root is not an energy. The dimensionally correct scale is Lam | `assurance/claims.json` |
| `CLM-D7-01` | RMOND action with F_dual is written and verified. | Superseded 2026-09-12: this was written against a vector-field (generalized Einstein-aether) K, not D9's actual scalar AeST field Y. See CLM-D7-07 for | `assurance/claims.json` |
| `CLM-D7-02` | Background Friedmann equations are unmodified. | Void as of 2026-09-12: Y is identically zero on FLRW under the corrected AeST action, so the entire background-acceleration-ratio calculation this cla | `assurance/claims.json` |
| `CLM-D7-03` | Linear screening factor F''/F' ~= 0.00233 at the background Newtonian level. | Void as of 2026-09-12, same root cause as CLM-D7-02: computed from a vector K field that is not the action's actual field content. The derived 429x an | `assurance/claims.json` |
| `CLM-D7-05` | Natural O(1) coupling constants satisfy all constraints. | Void as of 2026-09-12: c1, c2, c3 do not exist in the corrected AeST action (K_B is the only aether coupling). TARGET_D7_SUPPLEMENT needs a full rewri | `assurance/claims.json` |
| `CLM-D7-06` | Exact PPN gamma, beta for specific coupling values. | Superseded: gamma=1 now follows from the Skordis-Zlosnik embedding's own Psi=Phi identity (see CLM-D3-05, itself void), not from computing couplings.  | `assurance/claims.json` |
| `CLM-D9-01` | D9 embedding normalization: mu = J' vs 2J'; a0tilde vs a0. | Corrected 2026-09-12: TARGET_D9 Sec.1 and Sec.2 disagreed by a factor of 2 in the prefactor (1/8 pi G_hat); a0tilde=(1+lambda_s) a0 != a0 was previous | `assurance/claims.json` |
| `CLM-Z-R1` | RETRACTED: kappa = 0.9539 is a hypersurface average of T_mu_nu, a curvature scalar of the GOD substrate, a 3-sphere trac | Affected surfaces: the published records listed in published_in. Corrections reach Zenodo only as new versions. Audit provenance: Zenodo claim audit 2 | `assurance/claims.json` |
| `CLM-Z-R2` | RETRACTED: the Information Tension acceleration relation is derived from the weak-field limit of T_mu_nu, and its SPARC  | Affected surfaces: the published records listed in published_in. Corrections reach Zenodo only as new versions. Audit provenance: Zenodo claim audit 2 | `assurance/claims.json` |
| `CLM-Z-R3` | RETRACTED: the boundary theta, or the dephasing limit chi, equals 1/sqrt2 = 0.707 | Affected surfaces: the published records listed in published_in. Corrections reach Zenodo only as new versions. Audit provenance: Zenodo claim audit 2 | `assurance/claims.json` |

## 2. The three mu-uniqueness routes, and why they are unrecoverable

These are the program's most instructive kills, because each was a *proof* that turned out to prove the wrong thing:

| Route | Theorem | What it actually forces | Behaviour under the live `mu_std` |
|---|---|---|---|
| Pade[1/1] minimality | `CLM-D2-02`, `CLM-12` | the unique solution is `x/(1+x)` | `mu_std` is irrational, so it is outside the class entirely |
| Fisher identity | `CLM-13`, `CLM-D2-04` | solving `F'^2 I(mu) = x^3` returns `x/(1+x)` | violated by exactly `x + sqrt(1+x^2)` |
| Odds-ratio inverse | `CLM-D2-03` | `mu(odds(p)) = p` holds only for `x/(1+x)` | fails except at `p = 0, 1` |

The lesson is structural, not incidental: **a uniqueness theorem that returns the falsified function is not neutral mathematics sitting beside a live theory, it is an argument that excludes the live theory.** These cannot be repaired, because repairing them destroys the theorems. They are retired, and the live interpolation is now an explicit postulate (`CLM-PR-01`, Postulate R, `[O]`).


## 3. Surviving constraints, with their binding status

| Constraint | Status | Binding? |
|---|---|---|
| `c_T = c` | structural (EH tensor sector, no Weyl coupling) | no |
| `c_s^2 <= 1` | satisfied for `K2 >~ 60` | no |
| k-essence `C^AB -> 0` | discharged: excludes k-essence, not AeST | no |
| BBN 5% on `G_cosmo/G_N` | **fails exactly**; opens above 8.144% | on the bound |
| Cassini `Q2` | **fails**; tracking branch, constant residual `a0/2` | **yes** |

## 4. Reproduce every verdict

```
python3 audits/2026-11-18/verify_untested_claims.py      # 32 claims, exit 0
python3 audits/2026-11-18/aest_three_exclusion_scan.py    # the 3 walls, exit 0
python3 audits/2026-11-18/qy_decoupling_test.py           # Q/Y escape, exit 0
python3 scripts/survival_vector_gate.py --self-test      # the gate, exit 0
python3 scripts/validate_claim_registry.py               # registry, exit 0
```

## 5. What this ledger does not claim

A kill is not a proof that the surviving alternative is correct. Every entry above is a closed path, and a closed path is evidence of method, not of success. The live program currently has one `[E]` claim and two proposals; see the registry for the current split.

