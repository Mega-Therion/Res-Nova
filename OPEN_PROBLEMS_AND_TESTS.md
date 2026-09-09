# Open Problems and Tests

Authority: `EPISTEMIC_BOUNDARY_v1.5.0.md`. Nothing in this file is a result unless it already has a `[P]` or `[D]` tag there.

---

## O1 — Horizon identity for `a0`

**Claim (not granted):** `a0 = c H_0 / (2π)`.

**Status:** `[O]`. SPARC prefers `a0 = 1.116\times 10^{-10}\,\mathrm{m\,s^{-2}}` with 14.4% total error (`A0_MEASUREMENT.json`). That sits `0.46\sigma` from `cH_0/(2\pi)` and `0.52\sigma` from MOND's `1.2\times 10^{-10}`. The systematic floor is about 8.7%. A 3`\sigma` split at `z=0` would need ~4.7% total uncertainty. More local galaxies cannot buy that. The limit is the distance ladder (`3c90ef3e` commit message).

**Closure path:** a derivation of the factor `1/(2\pi)` from a stated action plus a stated equilibrium condition, with the `2\pi` surviving after the same cancellations that already killed earlier KMS attempts (`CORPUS_DEPENDENCY_MAP.md` Root 2). Until that exists, do not say “derived.”

**Test path:** `a_0(z) = \xi\, c\, H(z)` on independent high-`z` dynamical tracers (strong lenses, resolved high-`z` rotation, or spacecraft-equivalent kinematic maps). One universe at one epoch cannot tell “tied to the horizon” from “happens to be constant.” This test is not in the repo.

**Quarantine:** “`a0` is an empirical acceleration scale, numerically consistent with `cH_0/(2\pi)` inside present errors.” Never: “`a0` is derived from the Hubble scale.”

---

## O2 — Reading of `\xi`

**Claim (not granted):** `\xi = a0/(c H_0)` is a fundamental order-unity coupling.

**Status:** Arithmetic `[D]`, ontology `[O]`. From `A0_MEASUREMENT.json`:

`a0 = 1.1162688655613144e-10`, `a0_horizon = cH0/(2\pi) = 1.0421152108506952e-10`, `cH0 = 2\pi \times a0_horizon`, so

`\xi = a0 / (c H_0) = 0.170 \pm 0.025` (total error propagated from `total_sigma`).

**Closure path:** none without O1 or a redshift test. Explaining `0.17` is a research problem, not a defense problem.

**Test path:** same as O1. If `\xi` is constant, `a0(z)/[c H(z)]` is flat. If `a0` is a universal constant, that ratio falls as `1/H(z)`.

**Quarantine:** “`\xi` is the measured ratio of two dimensionally identical quantities.” Never: “`\xi` proves horizon thermodynamics.”

---

## O3 — `\Omega_\Lambda = \ln 2`

**Claim (not granted):** dark-energy fraction equals the 1-qubit Shannon limit.

**Status:** `[O]`. Homogeneous FLRW decoupling of the scalar (`\hat\nabla_\mu\phi=0 \Rightarrow \rho_\phi=0`) is `[P]` and cuts the dynamical-fluid version. The boundary-condition story is not a Friedmann-equation derivation.

**Closure path:** a covariant action whose on-shell Friedmann constraint produces `\Omega_\Lambda=\ln 2` without inserting it. Absent that, it stays in the motivational annex (`CORPUS_DEPENDENCY_MAP.md` quarantine 1).

**Test path — EXECUTED 2026-09-09:** pre-registered inference against the named Pantheon+ likelihood is now run and ledgered. Protocol: `04_cosmology/PREREG_OMEGA_LN2_PANTHEONPLUS.md` (frozen before the run). Artifact: `04_cosmology/O3_PANTHEONPLUS_RESULT.json` (script: `04_cosmology/omega_ln2_pantheonplus.py`). Result: over the 1590 cosmology-sample SNe with the full STAT+SYS covariance and the official `zHD > 0.01` cut, the pre-declared test point `Ω_Λ = ln 2` sits `Δχ² = 1.89` (**1.37σ**) from the flat-ΛCDM best fit (`χ²_min = 1402.9`, `Ω_m = 0.332`, matching the published Pantheon+-only analysis). Verdict per the frozen rule: **CONSISTENT** — ln 2 lies inside the 1σ-ish neighbourhood of the named likelihood, far inside the 3σ rule. This is a `[D]` *test outcome*: it does not promote the conjecture, and the closure path above is still the only route to `[P]`. The quarantine sentence stands.

**Quarantine:** “conjectured horizon boundary condition, not a derived density.”

---

## O4 — High-`z` / JWST calibration as confirmation

**Claim (not granted):** early galaxies confirm the theory.

**Status:** `[O]`. Directory `03_observer_jwst/` is an interface, not a completed `[D]` campaign in this ledger.

**Closure path:** a frozen, pre-registered catalog, a statistic, and a public script that emits a JSON the ledger can cite.

**Test path:** same files. No script, no claim.

**Quarantine:** do not use JWST language in the abstract until O4 has a JSON.

---

## O5 — SPARC data not in the repo

**Status:** engineering target — **closed 2026-09-09.** Data remains intentionally not vendored in git (unchanged). The clean-clone walk was executed and recorded as `VERIFICATION_RUN_009/02_sparc_fetch/`: `fetch_sparc.sh` ran end-to-end from a clean clone with `SPARC_DATA_DIR` pointed outside the repository, downloaded the official CWRU `Rotmod_LTG.zip`, extracted all 175 `*_rotmod.dat` files, and verified **175/175 SHA-256 checksums against `VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256` with 0 drift, exit 0**.

Two hardening changes landed with the closure: (i) `fetch_sparc.sh` now falls back to `python3 zipfile` when the `unzip` binary is absent (the host of the RUN_009 walk had no `unzip`; the SHA-256 manifest remains the sole content authority, so the fallback cannot weaken verification); (ii) `SPARC_DATA_DIR` override confirmed honored by `fetch_sparc.sh` and by `sparc_paths.resolve_sparc_dir()` (smoke-tested, 175 files resolved).

**Caveat kept honest:** the SPARC *analysis* scripts (`a0_measure.py`, `parameter_ledger.py`) were not re-run in this walk. Their frozen JSON outputs are unchanged and remain the empirical authority (`AGENT_COVENANT.md`).

---

## O6 — Fresh-clone Lean reproduction

**Status:** `[P]` — **closed 2026-09-08.** Both remaining conditions are met. Cold machine: VERIFICATION_RUN_008 (2026-09-07) fetched all 8678 cache files from origin with no Mathlib cache anywhere on disk and the gate passed. CI release gate: the `lean-gate` job in `.github/workflows/verify.yml` runs `verify_all_proofs.sh` on push, schedule, and dispatch — 3/3 green, including the cold scheduled run at 2026-09-08T11:27Z. The gate covers **39 targets**, and its explicit `TARGETS` list has been verified set-identical to the `roots` in `lakefile.lean` (no glob, no drift).

**Residual (not O6):** the Mathlib prebuilt-cache endpoint is sometimes-cold-fetchable, not reliably so — a concurrent attempt on another host stalled and fell back to compiling from source. The daily cron exists to bound that stall rate with data instead of one-off manual walks. This is an infrastructure-availability caveat, not an open reproduction question.

**Quarantine:** the honest claim is “39/39 targets pass from a cold fetch, gated in CI on every push.” Still never: “anyone cloning will reproduce in one command” without noting the upstream cache endpoint can stall.

---

## O7 — `PAPER_01` historical arcsinh branch

**Status:** closed as false, not as a theory. See `PAPER_01_NOTICE.md`. Remaining work is hygiene: do not let agents cite it as live.

---

## Fork Lock — 2026-08-28

**Decision: Path B locked.** The RMOND completion (`final_manuscript.tex` §7–§9) implements Path B from the `gut_toe_status` fork analysis. The Skordis–Złośnik embedding with $\mathcal{F}(\mathcal{K}) = \mathcal{F}_{\text{dual}}(\sqrt{\mathcal{K}})$ provides:
- Vainshtein screening: $Q_2 \approx 4.9 \times 10^{-29}$ s⁻² (70× below Cassini) `[D]`
- Cosmological screening: $\mathcal{F}''/\mathcal{F}' = 1/(2x_0^2(1+x_0)) \approx 0.00233$ (76× → 0.23%) `[P]` — corrected 2026-09-08 from $\approx0.004$ / 0.4%
- $c_T = c$, $\gamma_{\text{PPN}} = 1$, ghost-free, FLRW decoupling `[P]`

The SVT-MOND structural block (two-scalar parent cannot simultaneously pass Cassini and SPARC) is **superseded** by the vector-tensor parent. Paths A and C are closed.

**The Hamilgrangian framework** (dual-channel Hamiltonian-Lagrangian tension formalism) is canonized as `00_CANONICAL/HAMILGRANGIAN_CANONICAL.tex`. The name captures that the physics lives in the tension between the Hamiltonian (bulk kinetic $\frac{1}{2}x^2$) and Lagrangian (boundary dissipative $x - \ln(1+x)$) channels.

---

## What would actually finish the physics

In order, and without romance:

1. Keep D1.2, D7, D8, D9 as the formal core. They are already the publishable theorems.
2. Publish D4.3–D4.10 as the empirical core, with the superseded D4.1 method in an appendix so referees see the correction.
3. Run O1's redshift test or withdraw horizon language from the abstract.
4. Leave O3 out of the letter; it is a different paper or it is nothing.
5. ~~Walk O5 and O6 so a referee can reproduce without `/home/mega`.~~ — done: O6 closed 2026-09-08 (CI gate, cold fetch, RUN_008), O5 closed 2026-09-09 (RUN_009).
