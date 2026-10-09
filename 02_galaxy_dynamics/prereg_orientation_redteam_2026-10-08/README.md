# Pre-look red team: wide-binary orientation pre-registration (2026-10-08)

Two independent agent passes attacked `../PREREG_WIDE_BINARY_ORIENTATION_2026-10-08.md` before Gate 1 or any orientation statistic was computed:
- a numerical check (`falsifier/`);
- a referee panel (`council/`).

Claude Code then re-ran every script on 2026-10-08. All 12 exited 0, and their verbatim outputs are in `falsifier/outputs/` and `council/outputs/`.

**No script opens a data file.** The σ values are typed in from the frozen, orientation-blind `WIDE_BINARY_FINAL_2026-10-04.md` table. `falsifier/wbf_copy.py` is byte-identical to `../wide_binary_fish.py` (sha256 `8035a1e18ba53e1b…`); it is imported only for `boost()` and constants, and it loads data only in `main()`. Everything else is synthetic.

Tier: `[O]`. These are protocol checks and expectations, not results about the sample.

## What the outputs show (file → line)
- `s3_qumond_fft.out`, `s3c_qumond_converge.out`, `council/outputs/checks_a.out`: the field solution has the force stronger along ĝ_ext (axis/perp 1.06–1.07 at q = g_N/g_ext ≈ 0.06). The pipeline's `boost('E')` has the opposite sign: aligned 0.933 vs perp 1.115 at g_N/g_ext = 0.01.
- `s6_other_checks.out`: the orientation average is identical for both (1.05391), so R(s) fits are unaffected.
- `s1_ke_symbolic.out`: the prereg's K_e = 1/(1+x²) = 0.236 at x = 1.8. That is Banik & Zhao's AQUAL L0. Their QUMOND K0 = −L0/(1+L0).
- `s2_xe_range.out`: x_e depends on a0 and on V0, R0. The pipeline uses y_e = GE/A0 = 1.823 (Newtonian ratio).
- `s4b_sigma_floor.out`:
  - Gate-1 upper bounds on the strict cut: z ≤ 0.40 (QUMOND, with Q) to z ≤ 0.62 (the prereg's AQUAL K, no Q).
  - An exact 0°/90° split, which is impossible on the sky, would reach 1.38.
- `council/outputs/checks_d.out`:
  - regression on w = sin²λ cos 2ψ gives 1.217× the z of the |cos ψ| split;
  - at a median mock separation D = 4, P(favour E | E) = 0.841 and P(disfavour E | S) = 0.954;
  - the tide is ≤ 3.2×10⁻³ g_N at 30 kAU;
  - g_ext tilts ≤ 10.4° from the Galactic-centre direction at |z| = 200 pc.
- `council/outputs/checks_c2.out`: in the orbit toy at K0 = −0.188, 93.8% of orbits were kept. The 6.2% dropped for energy drift, against none at K0 = 0.

Sources cited by the passes: Banik & Zhao, arXiv:1509.08457 (AQUAL Eq. 18, QUMOND Eq. 36, Fig. 1 caption), and Banik & Zhao 2018, arXiv:1805.12273 (Eqs. 15, 32–33). The PDF is not included.
