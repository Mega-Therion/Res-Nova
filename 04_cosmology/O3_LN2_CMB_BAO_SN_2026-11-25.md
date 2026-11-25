# O3: Ω_Λ = ln 2 Against CMB + BAO + SN (2026-11-25)

- **Pre-registration:** `PREREG_O3_LN2_CMB_BAO_SN_2026-11-25.md`, commit `608182cb`, pushed before the script was written.
- **Script:** `o3_ln2_cmb_bao_sn.py`
- **Numbers:** `O3_LN2_CMB_BAO_SN_2026-11-25.json`
- **CMB-block validation:** at Planck 2018 best-fit ΛCDM, χ²_CMB = 1.163. That matches the pipeline's own check (1.16).

## Result: CONSISTENT on both combinations (the frozen rule is Δχ² ≤ 9)

| Combination | Free ΛCDM: Ω_m, h, χ² | Ω_Λ = ln 2: Ω_m, h, χ² | Δχ² | σ | Verdict |
|---|---|---|---|---|---|
| (A) CMB priors + DESI DR2 + Pantheon+ (1590 SNe) | 0.3018, 0.6840, 1421.00 | 0.3068, 0.6802, 1422.73 | **1.73** | 1.32 | **CONSISTENT** |
| (B) CMB priors + DESI DR2 + DES-Dovekie (1820 SNe) | 0.3023, 0.6836, 1650.33 | 0.3068, 0.6802, 1651.77 | **1.44** | 1.20 | **CONSISTENT** |

**The pieces at the ln 2 point (CMB / BAO / SN):**

- (A): 1.40 / 16.50 / 1404.82, against the free fit's 3.13 / 12.18 / 1405.69.
- (B): 1.40 / 16.50 / 1633.86, against the free fit's 2.93 / 12.49 / 1634.91.

The ln 2 point fits the CMB priors *better* than free ΛCDM, and DESI BAO slightly worse. The supernovae are nearly indifferent.

## Complete O3 test record

| Likelihood | Δχ² (ln 2 point − free ΛCDM) | Source |
|---|---|---|
| Pantheon+ alone | 1.89 | `O3_PANTHEONPLUS_RESULT.json` (2026-09-09) |
| DESI DR2 BAO alone | 1.14 | `CEILING_MODEL_BAO_SN.json` |
| DESI DR2 + Pantheon+ | 0.11 | `CEILING_MODEL_BAO_SN.json` |
| DES-Dovekie alone | 2.44 | `DESY5_CEILING.json` |
| CMB + DESI DR2 + Pantheon+ | **1.73** | this run |
| CMB + DESI DR2 + DES-Dovekie | **1.44** | this run |

Every named likelihood available locally puts Ω_Λ = ln 2 within about 1.6σ of its best-fit flat ΛCDM.

## Tier (declared in advance, unchanged)

- These are test outcomes, `[D]`.
- Ω_Λ = ln 2 stays `[O]`. Consistency is not promotion. The closure path (a covariant action whose Friedmann constraint outputs ln 2 without inserting it) is untouched.
- The quarantine sentence stands: "conjectured horizon boundary condition, not a derived density."
