# TARGET D11: The CMB fit — Ω_Λ = ln 2 against Planck

**Status:** D11_FIRST_RESULT — **the pre-registered Ω_Λ = ln 2 model survives its first contact with real Planck TT data.** Refitting under the constraint costs **Δχ² = +4.7 for one fewer fitted parameter** (2.17σ, p = 0.030), which **BIC scores as a tie (ΔBIC = +0.28)**. Two findings cut the other way: **P2 is a tautology**, not an independent prediction (§5), and the first, unrefit pass would have reported Δχ² = +120 had it not been caught (§3). Perturbations are **not** tested here.
**Last updated:** 2026-09-25
**Author:** R.W. Yett / Sovereign Architecture Group
**Epistemic tag:** `[P]` proved · `[D]` derived · `[C]` cited · `[O]` open · `[X]` killed

---

## 0. Why this document exists

Checklist item 4 (Cosmology / CMB) had **pre-registered targets but no calculation.** Zenodo
**21867985** (*ΩCDM: Pre-Registered Ω_Λ = ln 2*, deposited 2026-08-10) registers

> **P1:** `H₀ = 68.27 km/s/Mpc`  **P2:** `Ω_m = 0.306853`

as falsifiable predictions, and explicitly *refuses* to claim the Planck agreement as a
prediction because Planck measured it first. That is textbook pre-registration discipline.
What it never had was a spectrum. This computes one and scores it.

## 1. What is and is not tested `[D]`

**Tested.** Whether imposing `Ω_Λ = ln 2` — which removes one fitted parameter — still
reproduces the Planck TT acoustic peaks.

**Not tested.** AeST's **perturbations**. At background level the theory is ΛCDM-like, so
stock CLASS is the right tool for the primary peaks. Growth, lensing and the low-ℓ ISW all
feel the modification and need a modified Boltzmann code. See `TARGET_D5` §3.3 and
`cmb_aest/STATUS.md`.

**Not a claim of zero free parameters.** `𝒦(𝒬)` supplies **both** a dust component and `Λ`,
and both are free in the action. `Ω_Λ = ln 2` is a **posited relation**, not a derived
consequence — the contrary justification was withdrawn 2026-09-24.

## 2. Data and method

**Planck 2018 binned TT**, `COM_PowerSpect_CMB-TT-binned_R3.01.txt`, from the Planck Legacy
Archive — 83 bins, ℓ = 48–2499. Committed alongside the scripts.

**Limitation, stated up front:** the binned errors are **correlated** and the public file
ships no covariance. Treating bins as independent understates the uncertainty, so the
**absolute** χ² here is *not* the Planck likelihood. The method is validated by scoring
Planck's **own** best-fit column against the same data the same way: **χ² = 65.1 / 83 bins**,
χ²/N = 0.78. Differences measured identically on both sides are what this document reports;
absolute values are not.

## 3. The first pass was unfair, and is recorded as such `[X]`

Imposing `Ω_Λ = ln 2` while holding **every other Planck parameter fixed** gives

| | χ² (83 bins) |
| --- | --- |
| Ω_Λ = ln 2, nothing else refit | **218.3** |
| Planck 2018 best-fit ΛCDM | 98.3 |

**Δχ² = +120.** That number is meaningless and is **not** the model's fit — it is the cost of
moving one parameter with nothing allowed to compensate. Reporting it would have been a
false falsification. It is kept here because the mistake is instructive: a constrained model
must always be **refit** before it is scored.

## 4. The fair test `[D]`

Two fits to the same data, same free parameters, same method; the **only** difference is
whether `Ω_Λ` is imposed. `τ` is fixed to Planck's 0.0544 on **both** sides — it is
constrained by low-ℓ EE, not by TT, and in TT alone it is nearly degenerate with `A_s`.

| | free params | χ² | χ²/dof | H₀ |
| --- | --- | --- | --- | --- |
| **Ω_Λ = ln 2 imposed** | 4 (`ω_b, ω_c, n_s, A_s`; `h` tied) | **81.3** | 1.029 | 67.86 |
| ΛCDM, `h` free | 5 | **76.6** | 0.982 | 66.77 |

**Δχ² = +4.7 for one fewer fitted parameter.**

| statistic | value | reading |
| --- | --- | --- |
| nested significance | **2.17σ**, p = 0.030 | disfavoured, not excluded |
| ΔAIC | **+2.7** | mildly favours ΛCDM |
| **ΔBIC** | **+0.28** | **a tie** — `ΔBIC = 4.7 − ln 83 = 4.7 − 4.42` |

`|ΔBIC| < 2` is conventionally *"not worth more than a bare mention."* **On this data, with one
parameter fewer, the ln 2 model is statistically indistinguishable from ΛCDM.**

## 5. P2 is a tautology `[P]` — and this reduces the pre-registration's content

Under the constraint `h = √(ω_m/(1−ln 2))`,

    Ω_m = ω_m/h² = 1 − ln 2 = 0.3068528…   identically, for any ω_m.

**P2 is an algebraic restatement of `Ω_Λ = ln 2`, not an independent prediction.** It cannot
fail unless P1's premise fails. The pre-registration therefore carries **one** testable
number, not two, and any future citation should say so.

## 6. P1, and an honest caveat about it `[D]`

The refit gives `H₀ = 67.86` against the pre-registered **68.27** — apparently off by 0.41.
But this pipeline is TT-binned-only with `τ` fixed and no covariance, and it does not
reproduce Planck's own parameters: its ΛCDM fit returns `H₀ = 66.77` where Planck publishes
**67.36**, an offset of **−0.59**.

Applying the same offset to the constrained fit gives **H₀ ≈ 68.45**, against P1's **68.27** —
a difference of **−0.18**.

**Read that as consistency, not confirmation.** A pipeline offset applied as a correction is
a rough calibration, not a measurement. What is solid is the *relative* statement in §4;
P1 is **not** independently verified here, and would need the real Planck likelihood.

## 7. What this does and does not establish

**Does:** item 4 has its first actual spectrum. Imposing `Ω_Λ = ln 2` costs 4.7 in χ² and
saves a parameter, which BIC calls even. The model is **not excluded by Planck TT**.

**Does not:** verify P1, test any perturbation, or use the real Planck likelihood. And §5
removes P2 from the list of things that could ever have been falsified.

## 8. Next `[O]`

1. **The real Planck likelihood** (`plik_lite` TTTEEE + lowl + lowE) with the covariance,
   rather than binned TT with independent errors. That turns §4's Δχ² into a defensible number.
2. **Perturbations.** The whole of §1's exclusion. Needs the modified Boltzmann code; the
   matter-era piece is working (`boltzmann_units_fixed.py`, `δ_AeST/δ_CDM = 0.83–1.06`) and
   the radiation era is open.
3. **`τ` freed**, with low-ℓ EE included, since fixing it is the largest methodological
   shortcut taken here.

---

## Reproduction

```bash
cd Research_and_Data/05_Scripts_and_Tools/cmb_aest
python3 cmb_chi2_vs_planck.py      # §3, the unrefit pass
python3 cmb_refit_ln2.py           # §4, both refits  (~10 min, CLASS ~1.7 s/eval)
```

Related: `TARGET_D5_COSMOLOGICAL_SECTOR.md` (perturbations),
`TARGET_D10_CLUSTERS.md` (the other empirical item closed this week),
`cmb_aest/STATUS.md` (the full running record, including retractions).
