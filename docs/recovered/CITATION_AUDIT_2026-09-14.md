# Citation audit — `references-clean.md` from the ITT peer-review bundle

**Verdict: NOT landed.** The 52-entry reference list shipped in the
"Advancing Information Tension Theory for Peer Review Readiness" bundle contains
a misattributed citation, two duplicate-DOI/conflicting-title pairs, and four
plant-biology references with no bearing on this repository. Every DOI below was
checked against the Crossref API on 2026-09-14.

## 1. Misattributed — the serious one

| ref | claimed title | **actual work at that DOI** |
|---|---|---|
| `[12]` `10.1103/PhysRevD.93.104013` | "SPARC and the radial acceleration relation benchmark" | **"Quasilocal approach to general universal horizons"**, Phys. Rev. D 93 (2016) |

The DOI resolves to an unrelated paper on universal horizons. Nothing about
SPARC or the radial acceleration relation. A reader following this citation to
check the benchmark finds a different subject entirely.

The real sources, if a SPARC/RAR citation is wanted:
- SPARC sample — Lelli, McGaugh & Schombert, *AJ* **152**, 157 (2016)
- Radial acceleration relation — McGaugh, Lelli & Schombert, *PRL* **117**, 201101 (2016)

Neither is in the list. **Do not paste `[12]` into any manuscript.**

## 2. Duplicate DOIs carrying conflicting titles

| refs | DOI | verified title | problem |
|---|---|---|---|
| `[4]` / `[31]` | `10.1103/RevModPhys.81.1` | "Colloquium: The physics of Maxwell's demon and information" (RMP 81, 2009) | `[4]` is correct; `[31]` relabels the same DOI "Information and thermodynamics review" |
| `[6]` / `[32]` | `10.1002/wdev.231` | "Phyllotaxis: from patterns of organogenesis at the meristem to shoot architecture" | `[6]` is correct; `[32]` relabels it "Plant phyllotaxis and mathematical modeling review" |
| `[11]` / `[41]` | `10.1103/PhysRevLett.127.161302` | "New Relativistic Theory for Modified Newtonian Dynamics" (Skordis & Złośnik, PRL 127, 2021) | both descriptions are fair; duplication only |

A second title for a DOI already cited is how a single source silently becomes
two pieces of apparent support.

## 3. Off-domain references

`[5]` leaf morphogenesis, `[6]` phyllotaxis, `[30]` orchid floral development,
`[32]` plant phyllotaxis. These are real papers — `[6]`'s DOI verified above —
but they are developmental plant biology. Their presence tracks the "Orchid" in
the source document's title, i.e. **material from a different research thread
merged into this one's bibliography.**

## 4. Correctly handled by the bundle

`[26]` / `[51]` (`zenodo.20652203`) are flagged in the source as a **retracted**
record "requiring explicit citation suppression". That flag is correct and should
be preserved anywhere this list is reused.

## What was done

The reference list is recorded here and **not** merged into any manuscript or
README. `scripts/verify_mu_std.py`, `scripts/check_mu_std_certificate.py` and the
Rung-2 planning documents from the same bundle were landed on their own merits —
they carry no citations.

Checked with `api.crossref.org`, 2026-09-14.
