# Control-only spread fit with a free velocity scale (2026-10-04)

`WIDE_BINARY_EXCESS_SPREAD.md` (33d6b6d) calls its all-bins fit "free-scale". It does not add a velocity scale. Its control-frozen fit still compares absolute ṽ histograms, and the Newtonian baseline already runs ~9% fast in the close bin. All three of its control parameters land on grid edges (f = 0.5 cap, v = 0.1 floor, σ = 0.3 floor).

This run adds the missing piece. A free scale α multiplies the model speeds in the 500–2000 AU fit only. The fit sees the control bin only. α cancels in the ratios anchored to 500–1000 AU.

| cut | f | v_med (km/s) | σ_log | α |
|---|---:|---:|---:|---:|
| clean | 0.50 (cap) | 0.8 | 0.3 | 0.65 |
| loose | 0.50 (cap) | 0.5 | 0.3 | 0.76 |

On a first grid with α ≥ 0.80, α sat on the floor (0.80) and f = 0.40. With the grid widened to 0.50–1.10, α is interior.

| bin (AU) | clean obs | clean model | loose obs | loose model |
|---|---:|---:|---:|---:|
| 1000–2000 | 0.987 | 1.147 | 0.983 | 1.094 |
| 2000–5000 | 1.018 | 1.361 | 1.039 | 1.282 |
| 5000–10000 | 1.043 | 1.745 | 1.053 | 1.554 |
| 10000–20000 | 1.086 | 2.031 | 1.107 | 1.893 |
| 20000–30000 | 1.120 | 1.455 | 1.159 | 2.102 |

With scale freedom, the close bin asks for the maximum companion rate and a ~35% downward speed scale. The extrapolation overshoots every test bin by 10–90%.
- The companion term and α trade against each other. Together they are reshaping a close-bin ṽ histogram that the Newtonian template does not match.
- The template has no measurement noise, and it uses an assumed γ(s).
- **No contaminant fit on the close bin alone is identifiable until the Newtonian template matches that bin's shape.** That holds for this run, for Amendment B (f_c, β), and for 33d6b6d's control-frozen column.
- The spread model's all-bins fit stays descriptive only. The 2–5 kAU offset is still unaccounted for. No gravity verdict changes.

Script: `wide_binary_excess_spread_alpha.py`. Numbers: `WIDE_BINARY_EXCESS_SPREAD_ALPHA.json`.
