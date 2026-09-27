# Milky Way dwarfs vs environmental screening — 2026-09-27

**Question.** `ENVIRONMENT_SCREENING_2026-09-27.md` found that the parameter-free form
S = 1 − μ_std(g_ext/a0) passes Cassini at no cost to SPARC, but galaxies cannot detect it.
Milky Way satellites sit in the Galaxy's field at η = g_ext/a0 ≈ 0.1–0.7, where the screening bites.
Do they survive it?

## Data and method — `dwarf_screening_test.py`, `dwarf_screening_form2.py`
- **Local Volume Database** (Pace 2025, CC0; `dwarf_data/lvdb_dwarf_mw.csv`). MW satellites with a
  measured (not upper-limit) velocity dispersion: 45, or **42 after excluding the LMC, SMC
  (disks) and Sagittarius (disrupting)**.
- Stars only, with M/L_V = 1, 2, 3. g_ext = V_MW²/D_gc with V_MW = 180, 200, 220 km/s. Derived a0.
- MOND predictions follow McGaugh & Milgrom 2013 (ApJ 775, 139): σ_iso = (4GMa0/81)^{1/4},
  σ_efe² = GM/(3 r_h μ(η)), σ_MOND = min. Screened: σ² = σ_N²[1 + S(η)(σ_MOND²/σ_N² − 1)].
- Score: χ² on log σ, with the measurement error plus 0.1 dex intrinsic scatter.

## Result

**Form 1, S = 1 − μ_std(η): disfavored.** It is worse than plain MOND in every configuration:

| V_MW | M/L = 1 | M/L = 2 | M/L = 3 |
|---|---|---|---|
| 180 | +73.7 | +58.6 | +50.2 |
| 200 | +90.5 | **+72.4** | +62.3 |
| 220 | +106.9 | +86.1 | +74.3 |

(Δχ² vs MOND over 42 dwarfs.) It suppresses by ~η even at small η, so classical dSphs
(η ≈ 0.1–0.3) lose 10–30% of their boost.

**Form 2 (second and last pre-declared form), S = 1 − μ_std(η)² = μ_std(1/η)² = 1/(1 + η²).**
It comes from the `MuStdDuality` identity and suppresses by ~η²:

| test | result |
|---|---|
| Cassini 2026 | Q₂ = 3.85 / 2.72 ×10⁻²⁷ (+1.25σ / +0.62σ) — **PASS** |
| SPARC per-galaxy (Chae 2020 η) | Δχ²/s = −0.8 — **neutral**; shuffle control indistinguishable |
| MW dwarfs, Δχ² vs MOND | +9.9 to +27.9 across the grid (+16.7 at M/L = 2, V = 200) |

**Calibrating the dwarf penalty.** Plain MOND itself fits these dwarfs at χ²/n = **14.7**. It
under-predicts the ultra-faints by factors of 5–10, a known problem usually attributed to binary
stars inflating σ and to tidal disturbance. Rescaled by that misfit, form 1's penalty is **4.9**
(disfavored) and form 2's is **1.1** (not significant).

## Verdict
- **Form 1 is out.**
- **Form 2 survives all three tests at the current resolution:** Cassini passes, SPARC is neutral,
  and the dwarf penalty is not significant once MOND's own misfit is accounted for. It uses no new
  constant: only a0 (derived) and μ_std (live), through the duality identity already in Lean.
- Honest limits:
  - Two forms were tried. The second was chosen after the first failed, so there is one step of
    look-elsewhere.
  - The dwarf test is dominated by MOND's pre-existing ultra-faint problem.
  - The screening is phenomenological. There is no covariant AeST version `[O]`.
- **The sharpest remaining discriminator** is dwarfs at η ≳ 0.3 with clean kinematics (binary-
  corrected dispersions). There form 2 predicts σ lower than plain MOND by roughly √S: about 4%
  at η = 0.3 (S = 0.92), rising to about 17% at η = 0.67 (S = 0.69).

## Sources
- Pace 2025, *Local Volume Database*, OJAp 8, 142 — https://github.com/apace7/local_volume_database
- McGaugh & Milgrom 2013, *Andromeda dwarfs in light of MOND. II*, ApJ 775, 139
- Chae et al. 2020 — https://arxiv.org/abs/2009.11525
- Cassini 2026 — https://arxiv.org/abs/2602.17884
