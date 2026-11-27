# Unified Wick-CPT, Spin(8) Triality & 3x2 Matrix Formalism (v2.1 Audited Companion Bundle)

## Contents
- `unified_wick_cpt_triality_gaps.tex` / `unified_wick_cpt_triality_gaps.pdf` — Self-contained publication-grade LaTeX monograph & compiled PDF (lualatex verified, 0 warnings; harmonized with `POSTULATE_LAYER_DIRECTIVE_2026-11-24` Stage 1 & `ERRATA E-13`)
- `UnifiedSpineGaps.lean` — Standalone zero-Mathlib Lean 4 formalization (`05_lean_formalization/UnifiedSpineGaps.lean`: Gaps 1-4, admit-free, 26/26 `#print axioms` checks with zero external axioms; `EXECUTED_AND_VERIFIED` locally with `lean`, `exit=0`)
- `verify_unified_spine_gaps.py` — 6-block deterministic SymPy verification suite (`exit=0`, 16,384 `Spin(16)` weights, 6/6 `E6` anomalies, 26x26 `II_{25,1}` Gram matrix, `Z3->Z9` lift, OS/GKSL, module-local `1/sqrt(2)` & `chi_s` quartic `4*chi_s^4 + 4*chi_s^2 - 7 = 0`)
- `floor2_su3_flavor_probe.py` — Controlled `[D]`/`[O]` flavor & null-seam probe: antisymmetric `SU(3)_fam` Yukawa no-go (`[D]`/`[X]`), symmetric sextet flavon `(27_H, 6bar)` full 3-generation CKM + Jarlskog invariant + charged-lepton hierarchy (`[D]`/`[O]`), and exact `SEAM.md` null-seam radiation yield `I = 1/(8*pi^(3/2))` (`[D]`)
- `mushroom_toroidal_vortex_probe.py` — Deterministic SymPy audit (`[D]`/`[O]`): 5D `AdS5` static Dark Bubble `1/(2*pi)` exclusion (`[D]`/`[X]`) vs. Hill's spherical vortex exact Euler solution (`Delta* psi`, central stalk -> polar `theta=pi` crown eversion -> outer drumskin stretch, stationary vortex ring core at `r_core / R = 1/sqrt(2)`, `2*pi` circulation period, and dipole projection)

## One-Shot Local Verification
```bash
python3 verify_unified_spine_gaps.py
python3 floor2_su3_flavor_probe.py
python3 mushroom_toroidal_vortex_probe.py
/home/mega/.elan/bin/lean ../../05_lean_formalization/UnifiedSpineGaps.lean
```
