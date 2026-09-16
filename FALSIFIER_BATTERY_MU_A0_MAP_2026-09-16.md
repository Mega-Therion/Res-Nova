# RN-CO-05b — THE STANDING FALSIFIER BATTERY (the (μ, a₀) map as a permanent test)

**Status:** DELIVERED. Ledger open-item 8 formalized: the empirical finding — any
theory whose μ is not μ_std-shaped is displaced ~2× in a₀ — is now a standing,
re-runnable harness check, not a recorded observation. Part A guards the measured
map; Part B is the battery that any candidate μ must survive.
**Date:** 2026-09-16
**Tags:** `[D]` machine-checked here · data from the frozen 3μ extraction
**Framework:** Res-Nova Core Objects Version 0.2. Companion deliverable to
`Q3_AEST_COVARIANT_DERIVATION_2026-09-16.md` (obligations 1 and 6).

---

## 1. What the battery asserts

**Part A — the standing map (exit 1 on any failure):**
- A1 the three extraction windows (simple, dual, std) are pairwise disjoint;
- A2 the deep-MOND ratio a₀(simple)/a₀(std) lies in [0.45, 0.55] — pure
  prediction ½, measured 0.4690 (mid-regime residual −3.1%);
- A3 the ordering a₀(simple) < a₀(dual) < a₀(std) holds.

Source of record: `02_galaxy_dynamics/A0_REEXTRACTION_3MU_2026-09-16.json`
(175 galaxies, 3391 points, SHA-256-verified SPARC data; harness
`sparc_a0_reextract_3mu.py`). If a future re-extraction breaks A1–A3, the map's
claim — and layer 0 §2 with it — is falsified, not "re-interpreted".

**Part B — the battery on a candidate μ:**
- **T1, the normalization knife:** μ′(0) = 1. Failing candidates extract a₀
  displaced ~2× (μ_simple's measured shadow: ×0.469).
- **T2, the celerity identification:** sinh(artanh μ(x)) = x — equivalently
  μ = x/√(1+x²) for monotone μ; i.e. the candidate is μ_std-shaped. This is (B)
  itself, now the covariant-uniqueness point (Q3 doc §3).

The binding rule (layer 0 §2) is enforced: **cosmological comparison of a₀ is
valid only for a candidate passing T1 and T2** — its extraction is comparable
with the μ_std window [1.059, 1.232]e-10; every other candidate's a₀ lands
elsewhere and its "cosmological coincidence" claims are void.

**Reference behaviour (B4, enforced):** μ_std passes both; μ_dual passes T1, fails
T2 (presence coordinate); μ_simple fails T1 (½) and T2. The harness exits 0 only
when the references behave exactly as the frozen record says — the battery cannot
silently rot into passing a candidate it should kill.

## 2. Use

```bash
python3 scripts/falsifier_battery_mu_a0_map.py    # standing check, exit 0
# on a new candidate:
#   from scripts.falsifier_battery_mu_a0_map import battery
#   battery(lambda x: <candidate>, name="mu_cand", record=True)
```

## 3. What the battery is NOT

It is not an extraction harness: it does not re-fit SPARC; it gates on the frozen
measured map (Part A) and on algebraic shape (Part B). A full falsification run
for a new candidate still requires the extraction (`sparc_a0_reextract_3mu.py`)
to confirm the predicted displacement — the battery predicts it, the extraction
measures it. `[D]` on the algebra; the map's numbers remain the 2026-09-16
measurement.

## 4. Ledger

Closes ledger open-item 8's "formalize as a standing test" clause: **formalized,
verified, standing.** No `[P]` claims touched.
