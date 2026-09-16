# HORIZON-SELECTION AUDIT — which horizon's circle closes the orbit (obligation 3 residue)

**Status:** OPEN (sharpened). Numerically, only the FLRW Hubble/apparent-horizon
radius with the quasi-static temperature T = 1/(2πR_A) is consistent with the
distance-robust a₀ at both distance zero points. **No principle found here selects it
uniquely**: the one literature route that lands on it (apparent-horizon thermodynamics)
needs a quasi-static premise that is ~24% wrong today and is adopted *because* it
matches — a premise equivalent to the conclusion. Nothing here is "derived" or
"forced". The decider is observational: a₀(z).
**Date:** 2026-09-16
**Tags:** `[P]` proved · `[D]` derived/verified here · `[C]` cited/conjectured · `[O]` open · `[X]` excluded
**Machine:** `scripts/horizon_selection_audit.py` — 11/11, exit 0. Sabotage-tested on a
copy: flipping the Kodama sign, the sign of Λ in q, or H₀ each makes it exit 1.
**Inputs:** `TWOPI_HUBBLE_FORM_AUDIT_2026-09-16.md` (the 2π is a thermal circle, S1),
`02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json` (T3 = non-flow galaxies,
78, 95% bootstrap interval [9.664, 13.239]e-11 m/s²), Planck 2018 base ΛCDM
(arXiv:1807.06209: H₀ = 67.36, Ω_m = 0.3153; radiation included, flat).

---

## 1. The measurement, with its covariance stated

T3 drops the 97 flow galaxies but its distances (TRGB/Cepheid/UMa/SNe) still sit on the
local ladder zero point (A0_PREDICTION_AUDIT VERIFICATION §2). Since a₀ ∝ 1/D, the
whole interval moves with that zero point. Every candidate is therefore tested twice:

| zero point | T3 95% interval (m/s²) |
|---|---|
| SPARC ladder (as extracted) | [9.664, 13.239]e-11 |
| moved to Planck scale (× 67.36/73) | [8.917, 12.216]e-11 |

This rescaling is a bracket, not a measured correction; the true zero-point covariance
is not known better than this. `[D]`

## 2. Candidate horizons and the a₀ each implies `[D]`

| candidate | a₀ (m/s²) | ladder ZP | Planck ZP |
|---|---|---|---|
| Hubble radius = flat-FLRW apparent horizon R_A = c/H₀, T = 1/(2πR_A) | 1.0416e-10 | in | in |
| de Sitter static patch / asymptotic event horizon, H_Λ = H₀√Ω_Λ | 0.8618e-10 | **out** | out by 3.5% — **disfavored, not excluded** (margin < unmodeled ZP systematic) |
| ΛCDM cosmological event horizon today, R_E = 5.118 Gpc, c²/(2πR_E) | 0.9058e-10 | **out** | in |
| apparent horizon, Kodama–Hayward \|κ\|/2π = cH₀(1−q₀)/4π, q₀ = −0.527 | 0.7951e-10 | **out** | **out** |
| particle horizon today, R_P = 14.15 Gpc | 0.3277e-10 | **out** | **out** |
| c√Λ/2π = cH₀√(3Ω_Λ)/2π | 1.4927e-10 | **out** | **out** |
| Milgrom a_dS = cH₀ (no 2π) | 6.544e-10 | **out** | **out** |
| Milgrom 1999, â₀ = 2c(Λ/3)^{1/2} (arXiv:astro-ph/9805346 eq. 8–9) | 1.083e-9 | **out** | **out** |
| local Rindler horizon of the orbit | none — the acceleration is a free parameter; setting it to a₀ is circular | — | — |
| galaxy-scale horizon | none exists (Φ/c² ~ 10⁻⁶; no trapped surface) | — | — |

**Numerically consistent:** the Hubble/apparent-horizon form at both zero points; the
true ΛCDM event horizon only if the distance scale is Planck-like. The de Sitter/H_Λ
form falls outside both brackets but by only 3.5% at the Planck zero point — smaller than
the unmodeled ladder zero-point systematic (§1), so it is **disfavored, not excluded**.
Kodama, particle, cH₀, c√Λ/2π and Milgrom's â₀ are excluded at 95% at both zero points.

**Sign check `[D]`.** The Kodama surface gravity is derived in the script from the
2-metric (κ = ½□_h R at R = 1/H → κ = −(H/2)(1−q)) and matches Cai–Cao–Hu
(arXiv:0809.1554, p.7, citing Hayward): κ = −(1 − Ṙ_A/(2HR_A))/R_A. The sign is
load-bearing: the flipped variant (3+q₀)/2 would give 1.288e-10, *inside* the ladder-ZP
window. The script asserts the derived form equals the quoted one and not the flip.

## 3. Search for a selection principle

**(a) Exact KMS temperature for a geodesic observer.** Only the de Sitter static patch
has an exactly thermal (KMS) state for inertial observers (Gibbons–Hawking; for accelerated
detectors in dS, T = (a² + H_Λ²)^{1/2}/2π, Milgrom astro-ph/9805346 eq. 6 citing his refs
[27][28]; Deser & Levin arXiv:gr-qc/9706018 carries that title — reference-number match
not checked). `[C]` This criterion selects **H_Λ — the horizon the data disfavor**
(outside both brackets, marginally). The cleanest principle picks the disfavored horizon;
this argues against, not for, a unique horizon-circle reading.

**(b) Thermodynamics consistent with the actual FLRW dynamics.** Cai & Kim
(arXiv:hep-th/0501055) derive the Friedmann equations from δQ = TdS on the *apparent*
horizon with T = 1/(2πR_A); Wang, Gong & Abdalla (arXiv:gr-qc/0511051) find the first and
second laws hold on the apparent horizon and **break down on the event horizon** ("no
parameter redefinition can rescue" it). Cai, Cao & Hu (arXiv:0809.1554) obtain
T = 1/(2πR_A) by tunneling. `[C]` This selects the apparent horizon over the event,
particle and static-patch horizons — and in flat FLRW R_A = c/H, the Hubble form.

**(c) Why (b) is not a derivation — the premise check.** Cai–Cao–Hu state explicitly
that T = 1/(2πR_A) follows from the Kodama κ only under Ṙ_A = 0 (infinitesimal-interval /
instantaneous assumption). Today Ṙ_A/(2HR_A) = (1+q₀)/2 = 0.237 — not small. Keeping the
Ṙ_A term (the Kodama–Hayward temperature, which is the generally-covariant one) gives
0.795e-10, **excluded**. So the route lands on H₀ only via premise **Q: "the operative
temperature is the quasi-static 1/(2πR_A), not |κ|/2π"**, and Q has no justification
here other than that it reproduces the measured a₀. Q is equivalent to the conclusion
"the Hubble form, not the Kodama form". **Verdict: no principle selects H₀ uniquely.**
`[O]`

**(d) Milgrom's own route.** Milgrom 1999 is de Sitter, uses Λ, and identifies
â₀ = 2(Λ/3)^{1/2} (no 2π) with an interpolating function μ̂(x) = [1+(2x)⁻²]^{1/2} − (2x)⁻¹
(eq. 9), which is not μ_std; he calls the significance "anything but obvious" and notes it
does not generalize to circular orbits. His numerical identification is excluded (§2).
`[C]` (verified in the paper text). The corpus's cH₀/2π is therefore not Milgrom's
formula; it only shares the Unruh/vacuum motivation.

**(e) H₀ or H(z)?** Principle (b) is local in time: if the apparent horizon is operative,
a₀ tracks H at the galaxy's epoch, not today's H₀. `[C]` The static-patch reading gives a
constant. The Kodama reading gives yet another curve.

## 4. Stated conditionally (the most that can be said) `[C]`

*Given* P1 the 2π is a horizon thermal circle (S1, TWOPI audit, itself `[C]` for the
KMS identification); P2 the operative horizon is one whose thermodynamics is consistent
with the FLRW dynamics (Cai–Kim/Wang–Gong–Abdalla ⇒ apparent horizon); P3 = Q the
quasi-static temperature — *then* a₀ = cH/2π with H the Hubble rate of the galaxy's
epoch. P1 and P2 are independent of the a₀ data; **P3 is not** (it is chosen by it).
Hence not derived, not forced, not discharged.

## 5. The falsifiable discriminant

a₀(z)/a₀(0) at z = 1 (script K7):

| reading | a₀(z=1)/a₀(0) |
|---|---|
| apparent horizon, quasi-static (Hubble form, H(z)) | 1.791 |
| apparent horizon, Kodama–Hayward | 0.962 |
| de Sitter static patch (Λ form) / "H₀ today" | 1.000 |

The Hubble-vs-constant separation (79%) exceeds the full relative width of the local
95% interval (34%), so a z ≈ 1 rotation-curve a₀ at comparable precision decides it.
Current state (ledger item 6): a₀(z) at 0.87σ, inconclusive; the older 5.9σ
constant-a₀ verdict is `[X]` unrecoverable. Secondary discriminant: a geometric-distance
(maser) a₀ removes the zero-point bracket and would decide whether the true event
horizon (0.906e-10) is also excluded.

Note the corpus's current identification uses **H₀ today** for z ≈ 0 SPARC galaxies —
that is numerically indistinguishable from H(z) there, and it is *not* a prediction of
constancy. If a₀ is found constant in z, the Hubble/apparent-horizon reading dies and
the static-patch (Λ) circle is left as the surviving candidate, in marginal (3.5%-margin)
tension with the local a₀ — a weaker falsifier than killing the horizon reading outright.

## 6. What could not be verified

- Gibbons & Hawking 1977 (Phys. Rev. D 15, 2738) and Kodama 1980 have no arXiv IDs;
  cited from secondary use (Milgrom ref. [26]; Cai–Cao–Hu ref. [15]), not read.
- Hayward arXiv:gr-qc/9710089 exists (title verified) but its κ convention was not read
  in the primary; the sign was instead derived from the metric and matched to Cai–Cao–Hu.
- Deser & Levin gr-qc/9706018: title verified; the T(a) formula is taken from Milgrom's
  quotation of it, not re-read.
- The Planck-scale zero-point bracket (× 67.36/73) is a bracket, not a measured
  ladder correction.

## 7. Reproduce

```bash
python3 scripts/horizon_selection_audit.py   # 11/11, exit 0
```

## 8. Ledger

Obligation 3 residue ("which horizon's circle"): **[O-sharp] → [O], numerically
narrowed, no selection principle.** Consistent: Hubble/apparent (quasi-static) at both
zero points; ΛCDM event horizon only at Planck zero point. Disfavored (not excluded): static patch/H_Λ. Excluded: Kodama, particle, cH₀, c√Λ/2π, Milgrom's â₀. Decider: a₀(z). No `[P]`
changes.
