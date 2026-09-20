# Canonical epistemic tier legend

**This file is authoritative.** Where any document's local legend disagrees with
this one, this one wins. Established 2026-09-20 to resolve four coexisting
vocabularies found by the corpus inventory.

## The tiers

| tag | meaning | test for using it |
| :-- | :-- | :-- |
| `[P]` | **Proved.** A machine-checked theorem, in Lean with no `sorry`, on standard axioms. | Name the module and theorem. If you cannot, it is not `[P]`. |
| `[D]` | **Derived here.** Follows by explicit argument from stated premises in this corpus. Not machine-checked, but written out and checkable by a reader. | Point at the derivation. |
| `[D*]` | **Derived given one named empirical input.** The argument is complete; one external number it rests on is not yet confirmed against its source. | Name the input and what would confirm it. Clears to `[D]` when confirmed. |
| `[C]` | **Cited.** Taken from the published literature. | Give the DOI. |
| `[conj]` | **Conjectured.** Believed, not derived. | Say what would settle it. |
| `[E]` | **Empirical.** A measurement or a comparison against data. | Name the dataset. |
| `[O]` | **Open.** No result either way. | Say what is missing. |
| `[X]` | **Killed.** Falsified, retracted, or superseded. | Give the date and the reason. |
| `[A]` | **Axiom.** Assumed, not derived. | Say why it is assumed. |
| `[P/O]` | **Compound.** Some components proved, some open. A pointer, not a tier — see below; any use must say which is which. | Decompose it, or score at the weakest component. |
| `[arith]` | **Arithmetic.** A Lean module that quantifies over `ℝ` rather than over a manifold, group or operator: the kernel certifies the arithmetic, and the physics is supplied by the surrounding prose. | See `docs/grounding_ledger.yaml`. |

## The IO-OI five-tier taxonomy

`IO_OI_ACADEMIC.tex` and the documents derived from it use an older,
self-contained taxonomy. It is internally consistent and is published, so it is
retained rather than rewritten; these are its equivalents here:

| IO-OI tag | equivalent above |
| :-- | :-- |
| `[thm]` | `[P]` when machine-checked, `[C]` when taken from published literature |
| `[emp]` | `[E]` |
| `[cond]` | `[D]` with its condition stated |
| `[cited]` | `[C]` |
| `[note]` | not a claim; no tier |

New documents should use the table above rather than this one.

## Two collisions this resolves

**`[C]` was both "cited" and "conjectured."** `TARGET_D1_SUPPLEMENT` reads
"`[C]` cited"; the four 2026-09-16 audits read "`[C]` cited/conjectured";
`CLAUDE.md` reads "`[C]` conjectured". Those are different epistemic claims —
one appeals to someone else's evidence, the other to none.

**Resolved:** `[C]` means **cited**, which is the dominant usage in the D-target
chain. Conjecture is `[conj]`, which the IO-OI taxonomy already used. A tag
that can mean either is worse than no tag.

**`[P]` was both "proved" and "proposed."** The D-targets and the audit series
use it for machine-checked results; `Axiom_A4` and some planning documents use
it for proposals.

**Resolved:** `[P]` means **proved**, the dominant usage and the stronger claim,
so that misreading it errs toward scepticism rather than credulity. A proposal
is `[conj]` or `[O]`.

## `[P/O]`

Previously undefined while carrying 8 of 12 target statuses in the D-chain.

**Definition:** a compound status for a target whose components differ — some
proved, some open. It is a pointer, not a tier: any document using it **must**
say which components are `[P]` and which are `[O]`. `[P/O]` alone is not a
usable claim, and a target that cannot be decomposed should be scored at its
weakest component.

## Scope

The tiers apply to claims, not to documents. A single paper routinely contains
`[P]`, `[C]` and `[O]` statements, and marking the paper is meaningless. Mark
the claim.

Tiers move in both directions. `[C]` → `[X]` when a cited result is retracted;
`[D*]` → `[D]` when an input is confirmed; `[D]` → `[X]` when a derivation is
found to rest on a falsified premise. A demotion is a normal event and should be
recorded with its date and reason, never quietly applied.
