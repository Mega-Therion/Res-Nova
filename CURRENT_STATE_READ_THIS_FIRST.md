# READ THIS BEFORE WRITING ANY PHYSICS CONTENT

**If you are an agent (Manus, Grok, antigravity, Claude, or anything else) about to write,
summarize, or extend any claim in this theory — stop and read this file completely first.
Do not pull from the Obsidian vault's `raw/Logs/`, `80_Archive/`, `obsidian_vault_legacy/`,
or any file described as "archived," "legacy," or "historical." Those are frozen records of
past states, kept for provenance, not current physics. This file and the two it points to
are the only current physics.**

**Last verified against repo HEAD:** 2026-09-12. If this date is more than a few days old
when you read it, treat every claim below as suspect and re-derive its status from
`PEER_REVIEW_READINESS.md` directly before using it.

---

## Why this file exists

On 2026-09-12, an external agent (Manus) was dispatched to write four standalone papers.
It built its brief from cached/legacy vault material instead of the live repo, and used:
- **μ(x) = x/(1+x)** as the theory's central interpolating function — falsified the same
  night, roughly two hours *before* Manus started writing, in `TARGET_D7_COVARIANT_COMPLETION.md`.
- **V₂₄₀(ℝ^N)**, the "big-dimension" Stiefel substrate — retired **19 days earlier**
  (2026-08-25), superseded by V₂(ℝ³) via Cartan triality.

Neither error was a timing accident. Both facts were already on disk, committed, before the
agent that used the dead version ever ran. This file exists so that never happens again:
one place, unambiguous, checked first, every time.

---

## The three things every agent gets wrong if they skip this

### 1. The interpolating function is μ_std, NOT μ_dual

- **DEAD, do not use:** μ_dual(x) = x/(1+x). Falsified 2026-09-12 — produces an
  r-independent anomalous acceleration in the solar system, ~5.7×10⁵ over the Cassini bound.
  No viable fix exists within any GW170817-safe (c_T=c) theory. See `TARGET_D7_COVARIANT_COMPLETION.md`
  §4 and §11 for the full derivation and the literature search that closed off every escape route.
- **LIVE, use this:** μ_std(x) = x/√(1+x²). Confirmed via exact 50-digit numerical solve
  to clear the same solar-system bound by ~1300×. See `TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md`.
  A structural uniqueness derivation exists (rapidity/chiral-Fisher postulate) in
  `TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md`.
- If you see μ(x)=x/(1+x) — or F_dual = x²/2 − x + ln(1+x) — anywhere in a source you're
  reading, that source predates 2026-09-12's correction and its physics content is void.

### 2. The substrate is V₂(ℝ³) via Cartan triality, NOT V₂₄₀(ℝ^N)

- **DEAD, do not use:** the "big-dimension" frame V_m(ℝ^N), m=240, N~57,600, tied to the
  E8 root system count 240²=57,600. Retired 2026-08-25.
- **LIVE, use this:** V₂(ℝ³) via Cartan triality. Any document still built on the retired
  substrate needs a full rebuild, not a patch — the retirement was structural, not cosmetic.
- The arithmetic 240²=57,600 remains a true E8 root-count identity. It is **not** the
  ambient dimension of anything physical in the current theory.

### 3. The covariant completion action is AeST, NOT generalized Einstein-aether

- D7's action was rewritten 2026-09-12 to genuine AeST (Skordis-Złośnik arXiv:2007.00082):
  scalar field 𝒴, minimal matter coupling. The prior version (vector field 𝒦, disformal
  coupling) was a different theory entirely and is retired. See `TARGET_D7_COVARIANT_COMPLETION.md` §0.

---

## What is actually current, right now (check `PEER_REVIEW_READINESS.md` for live detail)

| Target | Status | One-line state |
|---|---|---|
| D1 | [P] | Variational derivation — needs re-check against μ_std (in progress) |
| D2 | [P/O] | μ_std structural uniqueness exists; not yet Lean-formalized clean |
| D3 | [P/O] | γ=1 derived (F-independent); β scoped; α₁/α₂ open with named obstruction |
| D5 | [P/O] | AeST 𝒦(𝒬) cosmology rebuilt; non-linear structure formation unsimulated by anyone |
| D6 | [P/O] | Ghost-free re-check under corrected action pending |
| D7 | [P/O] | Action corrected to AeST; base solid, downstream re-checks ongoing |
| D8 | [P] | c_T=c — upgraded to structural, strongest result in the corpus |
| D9 | [P/O] | Ground-truth for D7 fix; factor-of-2 normalization bug found and fixed |

**Full detail, always current:** `PEER_REVIEW_READINESS.md` — read its top banner before
trusting anything dated earlier.

---

## The rule for dispatching ANY external agent (Manus, Grok, antigravity, or a fresh Claude session)

Every task brief that asks an agent to write physics content **must** include, verbatim,
near the top of the prompt:

> Before writing anything, read `/home/mega/Res-Nova/CURRENT_STATE_READ_THIS_FIRST.md` in
> full. Do not use any vault file under `raw/Logs/`, `80_Archive/`, or
> `obsidian_vault_legacy/` as a source of current physics — those are historical records
> only. If anything you find elsewhere contradicts that file, the file wins.

No exceptions. If a dispatch doesn't include this line, don't send it.
