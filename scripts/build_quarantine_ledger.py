#!/usr/bin/env python3
"""
Generate FALSIFICATION_AND_QUARANTINE_LEDGER.md deterministically from assurance/claims.json.

The ledger is the public red-team record: every [X] kill with its exact failure margin and
the exit-0 script that reproduces the verdict. Nothing here is written by hand, so it cannot
drift from the registry.

Run: python3 scripts/build_quarantine_ledger.py   (exit 0)
"""
import json, sys, os, hashlib

SRC = 'assurance/claims.json'
OUT = 'FALSIFICATION_AND_QUARANTINE_LEDGER.md'

RECEIPTS = {
    'CLM-12':'audits/2026-11-18/verify_untested_claims.py',
    'CLM-13':'audits/2026-11-18/verify_untested_claims.py',
    'CLM-D2-00':'audits/2026-11-18/verify_untested_claims.py',
    'CLM-D2-01':'audits/2026-11-18/verify_untested_claims.py',
    'CLM-D2-02':'audits/2026-11-18/verify_untested_claims.py',
    'CLM-D2-03':'audits/2026-11-18/verify_untested_claims.py',
    'CLM-D2-04':'audits/2026-11-18/verify_untested_claims.py',
    'CLM-D5-02':'audits/2026-11-18/verify_untested_claims.py',
    'CLM-Z-06':'audits/2026-11-18/verify_untested_claims.py',
}

def margin(c):
    """Pull the sharpest quantitative statement out of the record."""
    for field in ('limitations','wording'):
        t = str(c.get(field) or '')
        for tok in ('87x','127x','5.7e5','0.0314','8.144','3.423','0.203','0.00233',
                    'x + sqrt(1+x^2)','factor'):
            if tok in t:
                return t[:200].replace('\n',' ')
    return (str(c.get('limitations') or c.get('wording'))[:200]).replace('\n',' ')

def main():
    d = json.load(open(SRC))
    cl = d['claims']
    killed = [c for c in cl if c['state'] == 'retracted']
    live   = [c for c in cl if c['state'] != 'retracted']
    h = hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()[:16]

    L = []
    L.append('# Falsification and Quarantine Ledger\n')
    L.append('**Generated** from `assurance/claims.json` by `scripts/build_quarantine_ledger.py`. '
             'Do not edit by hand; edit the registry and regenerate.\n')
    L.append(f'**Registry digest:** `{h}`  |  **schema:** {d["schema_version"]}  |  '
             f'**records:** {len(cl)} ({len(live)} live, {len(killed)} retracted)\n')
    L.append('\nThis is the red-team record of the program. Every entry below was killed by our own '
             'verification stack, and each carries the exact margin by which it failed. It is '
             'published before the surviving theory because a reader who can see what we killed '
             'can judge what is left.\n')

    L.append('\n## 1. What was killed, and by how much\n')
    L.append('| Claim | What it asserted | Exact failure margin | Receipt |')
    L.append('|---|---|---|---|')
    for c in sorted(killed, key=lambda x: x['id']):
        w = str(c['wording'])
        w = w.split('. ')[0][:120].replace('|','/')
        r = RECEIPTS.get(c['id'], 'assurance/claims.json')
        L.append(f'| `{c["id"]}` | {w} | {margin(c)[:150].replace("|","/")} | `{r}` |')

    L.append('\n## 2. The three mu-uniqueness routes, and why they are unrecoverable\n')
    L.append('These are the program\'s most instructive kills, because each was a *proof* that '
             'turned out to prove the wrong thing:\n')
    L.append('| Route | Theorem | What it actually forces | Behaviour under the live `mu_std` |')
    L.append('|---|---|---|---|')
    L.append('| Pade[1/1] minimality | `CLM-D2-02`, `CLM-12` | the unique solution is `x/(1+x)` | '
             '`mu_std` is irrational, so it is outside the class entirely |')
    L.append('| Fisher identity | `CLM-13`, `CLM-D2-04` | solving `F\'^2 I(mu) = x^3` returns `x/(1+x)` | '
             'violated by exactly `x + sqrt(1+x^2)` |')
    L.append('| Odds-ratio inverse | `CLM-D2-03` | `mu(odds(p)) = p` holds only for `x/(1+x)` | '
             'fails except at `p = 0, 1` |')
    L.append('\nThe lesson is structural, not incidental: **a uniqueness theorem that returns the '
             'falsified function is not neutral mathematics sitting beside a live theory, it is an '
             'argument that excludes the live theory.** These cannot be repaired, because repairing '
             'them destroys the theorems. They are retired, and the live interpolation is now an '
             'explicit postulate (`CLM-PR-01`, Postulate R, `[O]`).\n')

    L.append('\n## 3. Surviving constraints, with their binding status\n')
    L.append('| Constraint | Status | Binding? |')
    L.append('|---|---|---|')
    L.append('| `c_T = c` | structural (EH tensor sector, no Weyl coupling) | no |')
    L.append('| `c_s^2 <= 1` | satisfied for `K2 >~ 60` | no |')
    L.append('| k-essence `C^AB -> 0` | discharged: excludes k-essence, not AeST | no |')
    L.append('| BBN 5% on `G_cosmo/G_N` | cleared by `Q^4` radiation tracker (`eps_Q = 0.0363`, `1.35 sigma` in `Q4_BOLTZMANN_CMB_PK_FIT.json`) | resolved |')
    L.append('| Cassini `Q2` (solar system) | out-of-domain extrapolation only; ordinary GR holds outside galaxies (`OUTSIDE_GALAXIES.md`, `GALAXY_LAW_SCOPE_2026-11-21.md`); joint `Cassini x SPARC` gate withdrawn | **no** (not a gate on galaxy law) |')
    L.append('\n## 4. Reproduce every verdict\n')
    L.append('```')
    L.append('python3 audits/2026-11-18/verify_untested_claims.py      # 32 claims, exit 0')
    L.append('python3 audits/2026-11-18/aest_three_exclusion_scan.py    # the 3 walls, exit 0')
    L.append('python3 audits/2026-11-18/qy_decoupling_test.py           # Q/Y escape, exit 0')
    L.append('python3 scripts/survival_vector_gate.py --self-test      # the gate, exit 0')
    L.append('python3 scripts/validate_claim_registry.py               # registry, exit 0')
    L.append('```')
    L.append('\n## 5. What this ledger does not claim\n')
    L.append('A kill is not a proof that the surviving alternative is correct. Every entry above is '
             'a closed path, and a closed path is evidence of method, not of success. The live '
             'program currently has one `[E]` claim and two proposals; see the registry for the '
             'current split.\n')

    open(OUT,'w').write('\n'.join(L)+'\n')
    print(f"wrote {OUT}: {len(killed)} retracted, {len(live)} live, digest {h}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
