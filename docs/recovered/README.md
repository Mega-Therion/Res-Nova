# Recovered Manus artifacts — 2026-09-13

Recovered from Manus task `89hNKzB8ocHzJEgLtK6DHd` (account `omnichyren`, "Advancing
Information Tension Theory for Peer Review Readiness"). That task **terminated on a Manus
internal error (code 10091, "refund this task")** at 300 credits; its output existed only
inside the Manus sandbox and had never reached this repository.

## Provenance and status

- Authored by Manus, not by a human and not by this repo's own pipeline.
- `scripts/verify_mu_std.py` was **re-run locally on 2026-09-13 and passes** — six exact
  sympy identities, exit 0. That is a measured fact about the script, not an endorsement
  of any physical claim built on it.
- `mu_std_certificate.json` carries its own honest scope line:
  `"evidence_boundary": "P_math only; no covariant action-level or empirical claim"`.
  The script's own final line: *"constitutive mathematics verified; physical action-level
  derivation remains open"*. Keep that boundary attached.
- The two `.md` plans are **Manus proposals**, unreviewed. They are filed here as recovered
  input, NOT as canon, NOT as an agreed plan. Nothing in them has been checked against
  `CURRENT_STATE_READ_THIS_FIRST.md`.

## What the script checks

`dF_std/dx = x*mu_std` exactly; `mu_std(sinh psi) = tanh psi` exactly; deep-field and
high-field series; strict monotonicity via `mu_std' = (1+x^2)^(-3/2)`; convexity of `F_std`.

Full 706-file recovery set across all six Manus accounts: `~/.chyren/manus_recovered_2026-09-13/`

---

## Second delivery — 2026-09-14 (full bundle)

A zip of the same Manus task's complete output was supplied directly, containing
15 files against the 6 recoverable through the API. What the larger bundle added:

- **`scripts/verify_mu_std.py` upgraded.** The zip's version extends both series
  to 8th order (the `-5x^7/16` and `-5/(16x^6)` tails) and, more importantly,
  **emits** `mu_std_certificate.json` instead of assuming a hand-written one.
  The certificate is now a pure function of the proof and cannot drift from it.
  Verified: regenerating produces the committed file byte-for-byte.
- **`scripts/check_mu_std_certificate.py`** — schema + exact-term assertions over
  the emitted certificate. Its hard-coded `/home/ubuntu/wide-research/` path
  (a sandbox path existing on no machine here) was replaced with a resolved one.
- **Four Rung-2 planning documents** — source normalization, the weak-field /
  quasistatic ansatz, an independent derivation plan, and the canonical bridge.
  **Unreviewed proposals, NOT canon**, same standing as the first delivery.
- **`.claude/skills/formal-research-rung-climber/SKILL.md`** — an evidence-first
  workflow skill. Landed as a skill, not as a claim.
- **`CITATION_AUDIT_2026-09-14.md`** — the bundle's 52-entry reference list was
  **rejected**. It misattributes a DOI (`[12]` claims a SPARC/RAR benchmark; the
  DOI is a paper on universal horizons), relabels two DOIs it already cites, and
  carries four plant-biology references from an unrelated thread. See the audit.

`resnova-audit.txt` (a 70KB file listing) and the three `pasted_content*.txt`
prompt dumps were not landed: they are process residue, not results.
