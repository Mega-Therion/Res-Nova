# PRIOR-ART PACKET: Binary Tetrahedral / McKay Block — literature verification

**Status:** RESULT — every `[P]` fingerprint of the locked finite core (RN-CO-01…03,
DIAG-01, MCKAY-01/02) is verified against the standard literature.
**Verdict, stated up front:** the block contains **no new mathematics** — every proved
fingerprint is standard, correctly reproduced, and now carries citations. Its value is
(a) audit verification (the corpus's independently-constructed finite model coincides
with the standard object), and (b) the pure-Lean-core formalization artifact. The
interpretive "chiral cascade" layer remains `[C]` and corpus-specific.
**Last updated:** 2026-09-16
**Tags:** `[P]` proved · `[D]` derived/verified here · `[C]` cited/conjectured · `[O]` open · `[X]` killed
**Framework:** Res-Nova Core Objects Version 0.2. Executes ledger item **RN-CO-MCKAY-03**.

---

## 1. Fingerprint-by-fingerprint verification

Sources verified 2026-09-16: GroupNames (Dokchitser, Bristol) page for SL(2,3);
Groupprops element-structure page for SL(2,3); nLab "character table of 2T" and
"McKay correspondence"; Steinberg, *McKay's correspondence and characters of finite
subgroups of SU(2)* (arXiv:math/0307121); the Pin-group signature convention
(arXiv:2608.14193 and standard Clifford-algebra literature).

| # | locked fingerprint (our finite model) | literature | verdict |
|---|---|---|---|
| F-1 | BT = Q8 ⋊ C3, order 24 | GroupNames aliases: "SL2(𝔽3) = SU2(𝔽3) = Spin3(𝔽3) = **Q8⋊C3** = C2.A4 = Binary tetrahedral group (2T, <2,3,3>) = SmallGroup(24,3)" | **STANDARD** — the semidirect-product identification is canonical |
| F-2 | order census {1:1, 2:1, 3:8, 4:6, 6:8} | Groupprops element structure of SL(2,3); also the A4-preimage count: 8 order-3 rotations of A4 lift to 8 elements of order 3 + 8 of order 6; 3 order-2 rotations lift to 6 elements of order 4 | **STANDARD** |
| F-3 | 7 conjugacy classes, sizes {1,1,4,4,4,4,6} | Groupprops: "conjugacy class sizes 1,1,4,4,4,4,6"; GroupNames class sizes 1,1,4,4,6,4,4 (same multiset, their column order puts the order-4 class of size 6 fourth) | **STANDARD** — identical multiset and identical assignment (the order-4 class is the single size-6 class; the 3- and 6-classes split 4+4) |
| F-4 | centre Z(BT) = {e,z}, BT/Z ≅ A4 | GroupNames: "Centre Z=C2, **G/Z=A4**", "Commutator G′=Q8", "Frattini Φ=C2, G/Φ=A4" | **STANDARD** |
| F-5 | irrep dimensions {1,1,1,2,2,2,3}; Σd²=24; 7 classes = 7 irreps | GroupNames character table (ρ1…ρ7); nLab 2T table (also gives the real-valued merged table) | **STANDARD** |
| F-6 | the character table (our χ1…χ7 with ω = e^{2πi/3}) | verified entry-by-entry against **two independent sources** (GroupNames, nLab) — see §2 | **STANDARD** (up to the non-canonical class-naming convention of §2) |
| F-7 | 2-dim irreps take −2 on the central involution (faithful binary-cover behaviour); χ7 is the inflation of A4's standard 3-dim irrep | GroupNames: ρ4 marked "symplectic faithful, Schur index 2"; ρ7 "orthogonal, **lifted from A4**" | **STANDARD** |
| F-8 | the crack: lift of a base involution has order 4, square = central sign (n²=z, π(n)²=e) | the Pin-group signature convention: **Pin(d,0) = Pin⁺, Pin(0,d) = Pin⁻** (arXiv:2608.14193 eq. 2.30 and Clifford literature); in Pin⁻(3) ⊂ Cl(0,3), a unit vector v satisfies v² = −1 ∈ Spin(3) central, so the reflection lift has order 4 with square the central sign | **STANDARD** — the crack is precisely the **Pin⁻(3) reflection behaviour**; the corpus implicitly selects the Pin⁻/Cl(0,3) convention (see §3) |
| F-9 | continuous embedding 2T ↪ SU(2); McKay graph = affine Ẽ₆ | McKay 1980/81 ("Graphs, singularities and finite groups"); Steinberg arXiv:math/0307121; nLab McKay correspondence; the standard ADE list: cyclic ↔ Ãn, binary dihedral ↔ B̃n, **binary tetrahedral ↔ Ẽ₆**, binary octahedral ↔ Ẽ₇, binary icosahedral ↔ Ẽ₈ | **STANDARD, now anchored** — previously tagged [O]-literature in our ledger; citations recorded here. Still not constructed inside the corpus [O] |

**No discrepancy was found.** Every `[P]` fingerprint survives literature comparison
exactly; the two items that were [O] (embedding, McKay graph) now have precise anchors
and remain [O] as *constructions* — which is what our ledger already said.

## 2. Class-naming convention (the one honest subtlety)

The two order-3 classes (and their negatives, the two order-6 classes) admit a
**non-canonical relabeling**: no invariant distinguishes "3A" from "3B" before a
pairing with the order-6 classes via g ↦ −g is chosen. Consequences:

- Our χ2/χ3 vs GroupNames' ρ2/ρ3 differ by swapping ζ₃ ↔ ζ₃² — this is relabeling
  plus Galois conjugation, not a discrepancy.
- Our convention pairs 6A = −(3A), 6B = −(3B); GroupNames pairs 6A = −(3B). Both
  are internally consistent; neither is "the" correct one.
- Any future citation of "our" table must state the pairing convention, or it will
  look like a character-value error. **Logged per the D41 precedent** so nobody
  rediscovers it as a bug.

Everything else in the table (values on 1A, 2A, 4A; the −2's; the zeros; the
{1,1,1,2,2,2,3} dimensions; the A4-inflation) matches both sources verbatim.

## 3. What the corpus's block actually contributes

1. **Independent reconstruction (audit value).** The corpus builds BT from its own
   substrate (explicit Q8×C3 model, own multiplication rule) and *then* checks the
   fingerprints. Finding only standard facts is the audit succeeding, not the block
   failing: it certifies the cascade's algebraic layer says nothing nonstandard.
2. **The formalization artifact.** The census/class/character material in pure Lean 4
   core — zero Mathlib, zero sorry, `native_decide`-checked — is a real, if modest,
   contribution: a machine-checkable elementary treatment of a standard object. It is
   pedagogical/formal, not mathematical novelty. (Its `[P]` status is within the
   model; this packet's citations make the standardness external.)
3. **The convention selection (Pin⁻).** The corpus's crack narrative implicitly
   selects the Pin⁻(3)/Cl(0,3) signature convention for reflections. This is a
   **choice**, not a theorem: Pin⁺(3) is equally standard and there reflections lift
   to involutions. The physical claim would have to justify the Pin⁻ selection —
   this is now recorded as an explicit open item `[O]` (it was previously invisible:
   the finite model fixes the convention silently).
4. **The interpretive layer** (chiral cascade, orientation-sensitive holonomy →
   crack → BT as "the" finite substrate) remains `[C]`, corpus-specific, and — per
   the Postulate R isolation (2026-09-16) — is compatibility-not-derivation for the
   galaxy-sector inputs. The literature packet does not and cannot support it beyond
   consistency of the group-theoretic nodes.

## 4. References (verified accessible 2026-09-16)

- GroupNames, SL(2,3): https://people.maths.bris.ac.uk/~matyd/GroupNames/1/SL(2,3).html — aliases, subgroup structure, character table, presentation.
- Groupprops, element structure of SL(2,3): https://groupprops.subwiki.org/wiki/Element_structure_of_special_linear_group:SL(2,3) — class sizes 1,1,4,4,4,4,6.
- nLab, character table of 2T: https://ncatlab.org/nlab/show/character+table+of+2T — complex and real tables, class cardinalities 1,1,6,4,4,4,4.
- J. McKay, *Graphs, singularities and finite groups* (1980/81) — the original correspondence.
- R. Steinberg, *McKay's correspondence and characters of finite subgroups of SU(2)*, arXiv:math/0307121.
- nLab, McKay correspondence: https://ncatlab.org/nlab/show/McKay+correspondence — ADE list including binary tetrahedral ↔ Ẽ₆.
- Pin signature convention: *Dirac, Majorana, and Weyl Spinors in Arbitrary Dimension*, arXiv:2608.14193 eq. (2.30): Pin(d,0)=Pin⁺, Pin(0,d)=Pin⁻; plus standard Clifford literature (Lawson–Michelsohn, *Spin Geometry*; Lounesto, *Clifford Algebras and Spinors*).
- Wikipedia, Binary tetrahedral group (standard order statistics and quaternion construction ⟨i,j,k,(1+i+j+k)/2⟩ ⊂ SU(2)).

## 5. Reproduce

Literature verification is by inspection of the cited pages (fetched 2026-09-16).
The corpus side of every comparison is `05_lean_formalization/BinaryTetrahedral.lean
plus the census computations of the Pass 1.5 audit; no new computation was needed,
and no script is added (nothing to verify numerically that was not already verified
in the μ_std audit's tooling and the Pass 1.5 enumeration).

## 6. Ledger entry

**RN-CO-MCKAY-03 (prior-art packet) — complete.** All `[P]` fingerprints of the
binary-tetrahedral/McKay block are standard mathematics, verified against GroupNames,
Groupprops, nLab, and the McKay/Steinberg literature, with citations recorded. The
block's honest content is audit verification + a pure-core formalization artifact;
no new mathematics is claimed or found. One new convention item surfaced and is now
open: **the crack corresponds to the Pin⁻(3) signature convention — a silent choice
the finite model makes, which any physical reading would have to justify** `[O]`.
The class-naming convention (3A/3B ↔ 6A/6B pairing) is logged as a citation hazard.

**Next:** RN-CO-05 — the SPARC / a₀ empirical layer under the same representation
discipline (families of a₀-representations, what data kills, F6/F7 applied).
