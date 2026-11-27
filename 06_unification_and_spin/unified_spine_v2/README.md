# Unified Wick-CPT, Spin(8) Triality & 3x2 Matrix Formalism (v2 Audited Companion Bundle)

## Contents
- `unified_wick_cpt_triality_gaps.tex` / `unified_wick_cpt_triality_gaps.pdf` — Self-contained publication-grade LaTeX monograph & compiled PDF (lualatex verified, 0 warnings)
- `UnifiedSpineGaps.lean` — Standalone zero-Mathlib Lean 4 formalization (Gaps 1-4, 0 sorry, 0 external axioms; EXECUTED_AND_VERIFIED locally with `lean UnifiedSpineGaps.lean`, exit=0)
- `verify_unified_spine_gaps.py` — 6-block deterministic SymPy verification suite (`exit=0`, 16,384 Spin(16) weights, 6/6 E6 anomalies, 26x26 II_{25,1} Gram matrix, Z3->Z9 lift, OS/GKSL, theta/kappa quartic)
- `floor2_su3_flavor_probe.py` — Plane 5 controlled [O] probe: antisymmetric SU(3)_fam Yukawa no-go ([D]/[X]) & symmetric sextet flavon Fritzsch hierarchy ([D]/[O])

## One-Shot Local Verification
```bash
python3 verify_unified_spine_gaps.py
python3 floor2_su3_flavor_probe.py
lean UnifiedSpineGaps.lean
```
