# OBLIGATION 5 AUDIT — THE a₀ PREDICTION, TWO-SIDED AND FALSIFIABLE

**Status:** DISCHARGED TO THE STATED LIMIT — the theory's scale relation
a₀ = cH₀/2π (the form forced by B-cov, the 2π home, and the Hubble-form
selection) is stated as a prediction **in both directions**, with every
tension quantified and the falsifiers named. The prediction takes a side: **the
SH0ES side of the Hubble tension.** What remains open is the horizon-selection
*reason* (obligation 3's residue), not the arithmetic.
**Date:** 2026-09-16
**Tags:** `[P]` proved · `[D]` derived/verified here · `[C]` cited/conjectured · `[O]` open · `[X]` killed
**Machine:** `scripts/a0_prediction_audit.py` — 8/8.
Discharges ledger open-item 9 (obligation 5 of layer 0) to the stated limit.
**Inputs:** REPRESENTATION_AUDIT_A0_SPARC (window, two-axis map, P1–P3),
TWOPI_HUBBLE_FORM_AUDIT (the 2π home), Q3_AEST_COVARIANT_DERIVATION (B-cov),
FALSIFIER_BATTERY_MU_A0_MAP (the binding rule).

---

## 1. What the theory predicts, and from what

After obligations 1–3, the scale relation is not a coincidence hunt: B-cov
forces μ_std, the 2π home fixes the form as a/2π, and the Hubble-form
discrimination (audit P2: the Λ forms miss by 1.439×/0.831×) selects the FLRW
horizon's circle. The relation is then **a₀ = cH₀/2π, with no free parameters**
(verifier F1: it inverts exactly). This audit refuses to leave that as "an
anchor near the window" — a prediction must be falsifiable in both directions.

## 2. The prediction, both sides `[D]`

**Forward (H₀ → a₀):** at Planck H₀ = 67.4 km/s/Mpc, a₀ = 1.0422e-10 m/s² —
tension −1.37σ against the measured μ_std window (audit's −1.32σ_boot
reconfirmed; verifier F2). At SH0ES H₀ the tension is −0.32σ.

**Backwards (a₀ → H₀):** the measured window inverts to (verifier F3):

$$H_0 = 75.06\ \pm 5.59\ \text{km/s/Mpc}\ (68\%), \qquad [68.51,\ 79.70].$$

This is the theory's own H₀ prediction, derived from galaxies, independent of
any ladder or the CMB.

## 3. The falsifier table `[C]` values, `[D]` tensions

| H₀ source | value | tension vs theory | verdict |
|---|---|---|---|
| Planck CMB | 67.4 ± 0.5 | **+1.36σ** | **disfavored** |
| SH0ES Cepheids | 73.04 ± 1.04 | +0.36σ | consistent |
| TRGB / Freedman | 69.6 ± 1.9 | +0.92σ | consistent |

(verifier F4). The theory's window contains both ladder values and excludes the
Planck value: **the theory predicts the late universe measures H₀ on the
SH0ES side — not a compromise value.** Hard falsifiers: any H₀ survey landing
outside [68.51, 79.70] falsifies the identity outright (verifier F4); and if a
future H₀ consensus lands near 70 with σ < 0.6, the central value 75.06
becomes a 5σ+ tension — the exact-identity version dies while the loose window
version survives. Both outcomes are stated in advance.

## 4. Why this comparison is valid — and when it would not be

The (μ, a₀) map's binding rule (RN-CO-05b): cosmological comparison of a₀ is
valid only for μ_std-shaped μ. μ_std passes the battery (verifier F5: T1 knife,
T2 celerity); the window compared here is μ_std's — not μ_simple's (which
places a₀ at 0.469× the window, verifier F6), not μ_dual's, not the legacy
1.107e-10 (μ_dual-era, exact-pipeline gap), not the μ-mixed 1.2e-10. The
obligation-5 targets are hit: the prediction lives in the μ_std window's
arithmetic, and the traps are excluded by name.

## 5. What is NOT derived `[O]`

1. **The Hubble-form reason** — why the FLRW horizon's circle is the operative
   one (obligation 3's residue) — is open. This audit *uses* the selection P2
   measured; it does not re-derive it.
2. **No z-dependence is claimed.** Open-item 6 (a₀(z), 0.87σ inconclusive)
   stands; this prediction is the constant-a₀ branch, and its verdict is tied
   to that item's resolution.
3. The numerical agreement is a *relation between two measurements*, not a
   derivation of either from first principles: the theory derives the FORM
   (cH/2π); the value follows from H₀ as input. A true derivation of the
   horizon's temperature scale remains the open triangle leg.

## 6. Reproduce

```bash
python3 scripts/a0_prediction_audit.py    # 8/8, exit 0
```

## 7. Ledger

**New open-item 9 (a₀ prediction — obligation 5) discharged to the stated
limit:** the prediction is two-sided, quantified (H₀ = 75.06 ± 5.59 from the
measured window; Planck +1.36σ disfavored; SH0ES/TRGB consistent), with hard
falsifiers named in advance. The theory takes the SH0ES side. Status: the
obligation is closed pending the H₀ landscape's resolution; the horizon-reason
(§5.1) remains open under obligation 3's residue. No `[P]` changes.

## CORRECTION 2026-09-16 (post-merge audit) — the H0 inversion is not ladder-independent

Three claims above overreach. The arithmetic in `scripts/a0_prediction_audit.py`
is correct; the interpretation is not.

1. **Circular, not "independent of any ladder or the CMB."** The a0 window is
   extracted from SPARC. SPARC (Lelli, McGaugh & Schombert 2016, arXiv:1606.09251,
   §2 group III) takes Hubble-flow distances for **97 of 175 galaxies assuming
   H0 = 73 km/s/Mpc**, and states this puts them "on a similar zero-point scale"
   as its Cepheid/TRGB distances — i.e. the whole sample is on the local distance
   ladder's zero point. Radii scale as D, so fitted accelerations scale as 1/D,
   so a0 scales ∝ H0_assumed. Inverting a0 → H0 therefore largely returns the
   ladder H0 SPARC was built on. Landing near SH0ES (73) is expected by
   construction and is **not evidence** for the SH0ES side of the tension.
2. **A 68% window is not an outright falsifier.** A true value falls outside a
   68% interval ~32% of the time by chance. "Any survey outside [68.5, 79.7]
   kills the identity" is withdrawn; at minimum a 95–99% interval is required,
   and only after (1) is fixed.
3. **"Planck disfavored" at 1.36σ is not disfavoring.** 1.36σ is statistically
   uninformative. The window (±5.6) is consistent with every current H0
   measurement at <2σ. The theory does not currently take a side.

**What survives:** a0 = cH0/2π as a stated scale relation, and its forward
consistency with Planck H0 at 1.4σ. **To make the prediction real:** re-extract
a0 with distances re-scaled to a common H0 (or restricted to the non-Hubble-flow
galaxies), propagate the distance-scale uncertainty, and quote 95% intervals.
Status of obligation 5 reverts to **OPEN (relation stated; prediction not yet
independent)**.
---

## VERIFICATION 2026-09-16 (distance-corrected re-extraction) — the correction's prescription, executed

`scripts/a0_distance_corrected_reextract.py` (8/8 checks) +
`02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json`. Provenance pulled
from source: `SPARC_Lelli2016c.mrt` note (2) confirms f_D=1 = "Hubble-Flow
assuming H0=73 km/s/Mpc with Virgo-centric infall" — **97/175 flow galaxies**
(the PR #59 citation verified exactly), 78 non-flow (45 TRGB, 28 Ursa Major
cluster, 3 Cepheids, 2 SNe). Identical frozen harness (grids, priors, profile
likelihood, parabola refinement, 500x bootstrap seed 42), mu_std only, 68% AND
95% intervals quoted.

| treatment | galaxies | a0 best | 95% interval | inverted H0 (95%) |
|---|---|---|---|---|
| T1 baseline (validation) | 175 | 1.1607e-10 | [9.72, 12.95]e-11 | 75.1 [62.9, 83.7] |
| T2 flow rescaled to Planck (D x 73/67.4) | 175 | 1.0975e-10 | [9.26, 12.34]e-11 | 71.0 [59.9, 79.8] |
| T3 non-flow only | 78 | 1.1631e-10 | [9.66, 13.24]e-11 | 75.2 [62.5, 85.6] |

**Findings, honestly stated:**

1. **T1 reproduces the frozen window to 0.000%** — the harness is validated;
   the correction changes the interpretation, not the numbers.
2. **The flow-H0=73 formula is NOT the source of the 75.** Dropping all 97
   flow galaxies moves a0 by +0.2% (well inside statistical error): the
   circularity is RELOCATED, not dissolved — T3's distances (TRGB/Cepheid/UMa/
   SNe) still sit on the local ladder's zero point. The a0 -> H0 inversion
   remains ladder-covariant, exactly as PR #59 said, now quantified.
3. **The relation itself survives every distance treatment.** The Planck
   anchor cH0(67.4)/2pi = 1.0421e-10 lies inside ALL three 95% intervals (T2,
   the Planck-rescaled treatment, contains it at <1 sigma). At 95% confidence
   nothing is excluded — the inverted intervals [59.9, 85.6] contain both
   Planck and SH0ES. **The theory does not take a side; the tension question
   is unresolved at current precision.**
4. **A genuinely independent H0 prediction requires geometric (non-ladder)
   distances** — masers, detached eclipsing binaries — which SPARC's sample
   lacks. This is the named limit of the dataset, not of the relation.

**Obligation 5 final status:** relation VERIFIED (a0 = cH0/2pi, consistent with
Planck under every distance treatment at 95%); inversion NOT independent
(ladder zero-point confirmed and quantified as the culprit; flow formula
exonerated). The 68%-window falsifier language is retired; all comparisons
quote 95%. What would move this: a maser-host a0 measurement, or TRGB
zero-point resolution.
