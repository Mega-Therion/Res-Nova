"""Detect drift between Res-Nova main and the pinned commit in res-nova-research-hub.

Fires a repository_dispatch to res-nova-research-hub when the hub's pinned
commit (client/src/data/research.ts releaseState.commit) falls behind main,
or when assurance/claims.json's live state summary changes. This never
rewrites the hub's curated narrative content itself -- it only notifies, so a
human/curator decides how to fold new state into the public prose. See
CLAUDE.md: no auto-rewrite of curated public content.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request

REPO = "Mega-Therion/Res-Nova"
HUB_REPO = "Mega-Therion/res-nova-research-hub"
API = "https://api.github.com"


def gh(path: str, token: str, method: str = "GET", body: dict | None = None) -> dict:
    req = urllib.request.Request(f"{API}{path}", method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, data=data) as resp:
        raw = resp.read()
        return json.loads(raw) if raw else {}


def raw_file(repo: str, path: str, token: str, ref: str = "HEAD") -> str:
    import base64

    meta = gh(f"/repos/{repo}/contents/{path}?ref={ref}", token)
    return base64.b64decode(meta["content"]).decode()


def main() -> int:
    token = os.environ["HUB_DISPATCH_TOKEN"]
    head_commit = os.environ["HEAD_SHA"]

    research_ts = raw_file(HUB_REPO, "client/src/data/research.ts", token)
    match = re.search(r'commit:\s*"([0-9a-f]{7,40})"', research_ts)
    if not match:
        print("could not find pinned commit in hub research.ts", file=sys.stderr)
        return 1
    pinned_commit = match.group(1)

    hub_claim_count = len(re.findall(r'id:\s*"CLM-', research_ts))

    compare = gh(f"/repos/{REPO}/compare/{pinned_commit}...{head_commit}", token)
    ahead_by = compare.get("ahead_by", 0)

    claims_json = json.loads(raw_file(REPO, "assurance/claims.json", token, ref=head_commit))
    registry_claims = claims_json["claims"]
    state_counts: dict[str, int] = {}
    for claim in registry_claims:
        state_counts[claim["state"]] = state_counts.get(claim["state"], 0) + 1
    retracted = [c["id"] for c in registry_claims if c["state"] == "retracted"]

    if ahead_by == 0:
        print(f"hub is current at {pinned_commit}, no drift")
        return 0

    payload = {
        "event_type": "resnova-drift",
        "client_payload": {
            "pinned_commit": pinned_commit,
            "head_commit": head_commit,
            "commits_behind": ahead_by,
            "registry_claim_count": len(registry_claims),
            "registry_state_counts": state_counts,
            "retracted_claim_ids": retracted,
            "hub_claim_count": hub_claim_count,
            "compare_url": compare.get("html_url"),
        },
    }
    gh(f"/repos/{HUB_REPO}/dispatches", token, method="POST", body=payload)
    print(f"dispatched drift notice: {ahead_by} commits behind {pinned_commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
