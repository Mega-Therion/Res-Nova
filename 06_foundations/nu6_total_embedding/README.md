# ν₆ / 𝒥₆-total embedding: mirror of Muse's pass-1/pass-2 posts (#187, pass-3 step 1)

**Status:** ν₆ is a candidate, not adopted. Nothing in this directory changes a tier in
`CURRENT_STATE_READ_THIS_FIRST.md`. Muse's gate results below are `[O]` (reported, not
reproduced here). The two closed-form numbers recomputed here are `[E]` (measured by
`check_nu6_pass2_analytic.py`).

## Sources (retrieved 2026-10-27 UTC via the Notion MCP `notion-fetch`)

| file | source | page last edited (UTC) |
|---|---|---|
| `notion_mirror/BLK-684_program_opened.md` | https://app.notion.com/p/40277b95a965817cbe12ce5d00fabacf | 2026-10-23T22:15:31Z |
| `notion_mirror/BLK-685_pass2.md` | https://app.notion.com/p/40277b95a965816abf99dedb5633fa78 | 2026-10-23T23:39:29Z |

Page bodies are copied verbatim as the fetch returned them (Notion-flavored Markdown,
escapes kept). Properties other than title and Evidence are omitted.

Links in those pages: the equation register (Notion `40277b95a965811fa061fa3f437d8479`,
prose only) and two files already in this repo (`AEST_TOTAL_SCALAR_CORRESPONDENCE_2026-10-14.md`,
`TARGET_D9_SKORDIS_ZLOSNIK_EMBEDDING.md`). The follow-up post BLK-713 (pass 3,
https://app.notion.com/p/40377b95a965817fbd76c04eac867ad6) says the same thing about files.

## What is and is not present

- **Present:** the two post texts, i.e. the numbers Muse reported.
- **Not present:** scripts, raw JSON, solver versions, the results files
  (`nu6_covariant_pass2_results.md`, `NU6_COVARIANT_PROGRAM.md`). BLK-685 places them at
  `~/workspace/physics-trajectory/action-closure-2026-10-23/` in Muse's environment. That path
  does not exist on this machine. Neither the posts nor BLK-713 carries a file
  attachment (fetched with `include_file_urls`). The Hood (`The-Hood/artifacts/`, checked
  2026-10-27) holds no 2026-10-23 Muse artifact for BLK-684/685/713. Not found after three
  searches; Muse has to file them.
- **Consequence:** the EFE/Cassini gate (λ_s = 0.1 in the band, 0.5 unresolved, 1 and 2 outside)
  and the full-band ≤ 6.1×10⁻¹⁰ sweep **could not be rerun**. They stay `[O]`.

## Recomputed here (`check_nu6_pass2_analytic.py`, exit 0, output `check_nu6_pass2_analytic.json`)

From μ₆ = x/(1+x⁶)^{1/6} alone, with the AQUAL total law y = xμ₆(x):

| quantity | BLK-685 | recomputed | tier |
|---|---|---|---|
| x* (max of y′) | (2/5)^{1/6} | 0.858374217 numeric vs 0.858374219 closed form | `[E]` |
| M₆ = y′(x*) | 1.3912500682 | 1.3912500682304 | `[E]` |
| λ_s bound 1/(M₆−1) | 2.5559100974 | 2.5559100974038 | `[E]` |
| x at g_N = a₀ vs φ^{1/6} | 1.0835058816 vs 1.0835058822 | 1.08350588217385, rel. diff 2.2×10⁻¹⁶ | `[E]` |

The anchor row checks ν₆'s exact law, not Muse's constructed 𝒥₆-total. It confirms the
target value only. That 𝒥₆-total reaches it to 6.1×10⁻¹⁰ remains `[O]`.
The bound row assumes BLK-685's statement that bound = 1/(M₆−1); that
step is not re-derived here.

Run: `python3 06_foundations/nu6_total_embedding/check_nu6_pass2_analytic.py` (numpy/scipy only).
