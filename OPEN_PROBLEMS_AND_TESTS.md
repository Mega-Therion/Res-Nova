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

**Test path:** pre-registered cosmological inference against a named likelihood (Pantheon+, DESI, Planck). A number that is only compared by eye is not a test.

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

**Status:** engineering open, not a physics open. Scripts default to `/home/mega/Chyren/...` and one path under `/tmp/claude-1000/`. See `02_galaxy_dynamics/SPARC_DATA.md`.

**Closure path:** environment variable `SPARC_DATA_DIR`, a SHA-256 manifest of `*_rotmod.dat`, and a documented download of Lelli, McGaugh & Schombert 2016. Do not vendor if the license forbids it; do pin hashes if you may store them.

**Test path:** CI job that fails when `SPARC_DATA_DIR` is set and hashes drift.

---

## O6 — Fresh-clone Lean reproduction

**Status:** engineering open. `verify_all_proofs.sh` exists. The recorded PASS used a local Mathlib build (`b0ff8ab6`). `lake exe cache get` is not claimed as walked.

**Closure path:** one clean runner, pinned `lean-toolchain` + `lake-manifest.json`, saved CI log.

**Quarantine:** “verified on the author machine against Mathlib `5eec30bc` / Lean `v4.33.0-rc1`.” Never: “anyone cloning will reproduce in one command” until O6 is walked.

---

## O7 — `PAPER_01` historical arcsinh branch

**Status:** closed as false, not as a theory. See `PAPER_01_NOTICE.md`. Remaining work is hygiene: do not let agents cite it as live.

---

## What would actually finish the physics

In order, and without romance:

1. Keep D1.2, D7, D8, D9 as the formal core. They are already the publishable theorems.
2. Publish D4.3–D4.10 as the empirical core, with the superseded D4.1 method in an appendix so referees see the correction.
3. Run O1's redshift test or withdraw horizon language from the abstract.
4. Leave O3 out of the letter; it is a different paper or it is nothing.
5. Walk O5 and O6 so a referee can reproduce without `/home/mega`.
