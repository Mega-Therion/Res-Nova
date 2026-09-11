# CLM-D5-03 — Non-linear structure formation (ledger draft, both branches frozen 2026-09-11 BEFORE production numbers)

To be inserted into OPEN_PROBLEMS_AND_TESTS.md upon V2 verdict at the validation
config. Claim language in each branch is frozen now; only the bracketed numbers
are to be filled from run artifacts. No other edits permitted without breaking
the prereg.

---

**Claim (not granted):** RMOND's non-linear structure formation is consistent
with observations; its ε(z=0) = 0.00233 deviation from ΛCDM does not blow up in
the non-linear regime.

**Protocol:** `PREREG_D5_MG_EVOLUTION.md` (SHA-256 `b9a939dd2b60d61ac177160ccaf7265a48c52ebd08b48359ee46aadb1af16b98`), two-arm MG-evolution mapping (Hassani–Lombriser arXiv:2003.05927 parametrization), identical ICs (seed 42), validation config 256³ particles / 256³ grid / L = 200 Mpc/h, z ∈ {0, 1}, k ∈ [0.05, 2.5] h/Mpc. Verdict rules V0–V2 frozen before any run. No re-tuning of ε, k0, af, b after seeing output (prereg §7).

**Status (pre-verdict):** Pipeline validated end-to-end at sanity config (64³/128 Mpc/h): ΛCDM/Arm A/Arm B all exit clean; V1 negative control satisfied (Arm B ΔP/P = +64% at k > 1 — far above the +5% floor). Sanity-config theory-arm signal: ΔP/P|_A = +0.26% (k > 1, 292 bins), first-order consistent with the frozen ε. `⟨VALIDATION-CONFIG NUMBERS: fill ΔP/P|_A at z=0 and z=1, per-band⟩`

**Branch 1 — V2 = CONSISTENT at validation config:**

Status becomes `[O] → [D]`: "consistent within the parametrised Vainshtein-class framework; non-linear amplification bounded." Manuscript's D5 linear-limit tcolorbox (i) discharged. This is a `[D]`-grade empirical-consistency statement inside the Hassani–Lombriser parametrization — it cannot rule out effects the parametrization does not capture, and it is NOT exact-model validation (no model-specific Res-Nova N-body exists).

**Quarantine (Branch 1):** "The mapped non-linear enhancement of RMOND is bounded by `⟨max |ΔP/P|_A⟩` over k ∈ [0.05, 2.5] h/Mpc at z = 0 and z = 1, within the frozen tolerance max(2 × linear, 1%)." Never: "RMOND validated by N-body," never "D5 proves the theory," never "the ε enhancement has been detected observationally."

**Branch 2 — V2 = TENSION:**

Status stays `[O]`, D5 open. The obstruction is documented verbatim: the non-linear regime amplifies the screened enhancement beyond 5% at k = `⟨first offending k⟩` h/Mpc, exceeding the νHDM-style blow-up threshold of prereg V2. The manuscript's 0.23% linear claim gains the non-linear caveat and CLM-D5-03 is listed as an open obstruction with the measured table attached.

**Quarantine (Branch 2):** "The parametrised non-linear response exceeds the frozen tolerance; the theory is constrained, not falsified in general (the parametrization's Vainshtein-class assumption is on trial together with the theory)." Never: "RMOND is dead" — the mapping, not the exact model, is what ran.

**Branch 3 — V2 = INCONCLUSIVE (between 2×linear/1% and 5% at some k):**

D5 stays open with the measured ΔP/P table; resolution requires either the k0-sensitivity band analysis (prereg reporting) or a model-specific solver. No grade change.

---

*Artifacts on commit: prod_lcdm/, prod_armA/, prod_armB/ spectra + logs, LATfield2/gevolution patch diff, seeds, runtimes, V0 unit-test output.*
