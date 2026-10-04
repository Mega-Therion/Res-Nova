"""Detect drift between Res-Nova main and the commit the research hub reflects.

The hub (research-hub/, merged into this repository on 2026-10-03 from the
former res-nova-research-hub repository) pins the Res-Nova commit its curated
content reflects: releaseState.commit in research-hub/client/src/data/research.ts.
When main moves past that commit, this script emits a GitHub Actions warning
with the claim-registry summary. It never rewrites the hub's curated narrative
content -- it only reports, so a human/curator decides how to fold new state
into the public prose. See CLAUDE.md: no auto-rewrite of curated public content.

Before the merge this script sent a repository_dispatch to the separate hub
repository. That repository is archived, so the notice is now a warning and
needs no token.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESEARCH_TS = ROOT / "research-hub" / "client" / "src" / "data" / "research.ts"
CLAIMS_JSON = ROOT / "assurance" / "claims.json"


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def main() -> int:
    head_commit = os.environ.get("HEAD_SHA") or git("rev-parse", "HEAD")

    research_ts = RESEARCH_TS.read_text(encoding="utf-8")
    match = re.search(r'commit:\s*"([0-9a-f]{7,40})"', research_ts)
    if not match:
        print(f"could not find pinned commit in {RESEARCH_TS.relative_to(ROOT)}", file=sys.stderr)
        return 1
    pinned_commit = match.group(1)
    hub_claim_count = len(re.findall(r'id:\s*"CLM-', research_ts))

    try:
        behind = int(git("rev-list", "--count", f"{pinned_commit}..{head_commit}"))
    except subprocess.CalledProcessError:
        print(f"::warning::could not count commits from hub pin {pinned_commit} to {head_commit[:7]}; drift not measured")
        return 0

    if behind == 0:
        print(f"hub is current at {pinned_commit}, no drift")
        return 0

    claims = json.loads(CLAIMS_JSON.read_text(encoding="utf-8"))["claims"]
    state_counts: dict[str, int] = {}
    for claim in claims:
        state_counts[claim["state"]] = state_counts.get(claim["state"], 0) + 1
    retracted = [c["id"] for c in claims if c["state"] == "retracted"]

    print(
        f"::warning::research hub content is pinned to {pinned_commit}, "
        f"{behind} commits behind {head_commit[:7]}. Registry: {len(claims)} claims "
        f"{json.dumps(state_counts, sort_keys=True)}, retracted: {', '.join(retracted) or 'none'}; "
        f"the hub lists {hub_claim_count}. Update releaseState in "
        "research-hub/client/src/data/research.ts once the curated prose catches up."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
