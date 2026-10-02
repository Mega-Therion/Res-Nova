#!/usr/bin/env python3
"""Export the claim registry to the public visualizer.

The Vercel visualizer (visualizer/, deployed with visualizer/ as its root) used to
carry a hand-typed "Sovereign Epistemic Ledger" of eight v1.4.0 claims. It was
never updated: in September 2026 it still presented the falsified dual-channel
closure as [P] and quoted the superseded a0 = 9.433e-11. A hand-typed copy of
the registry is a second registry, and a second registry drifts.

This writes visualizer/claims.json from assurance/claims.json (the CI-gated
registry), so the public ledger is a projection of the real one.

It also writes visualizer/lean_modules.json: the verbatim source of the Lean
modules the page's proof panel shows. That panel used to display hand-written
pseudo-Lean -- including a `sorry` -- captioned "[Kernel Proof Verified]". The
page now shows only files that exist in 05_lean_formalization/ and are built by
verify_all_proofs.sh.

    python3 scripts/export_visualizer_ledger.py           # write
    python3 scripts/export_visualizer_ledger.py --check   # exit 1 if stale
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assurance" / "claims.json"
DST = ROOT / "visualizer" / "claims.json"

LEAN_DST = ROOT / "visualizer" / "lean_modules.json"
LEAN_DIR = ROOT / "05_lean_formalization"

FIELDS = ("id", "wording", "state", "claim_type", "limitations", "source_locator")

# (key, file, status shown on the page)
LEAN_MODULES = (
    ("sz", "SZStdEmbedding.lean", "live: mu_std embedded in AeST (CLM-D9-02)"),
    ("mustd", "MuStdFoundations.lean", "live: F_std calculus, P(X) speed, monopole tail"),
    ("speed", "TensorSpeed.lean", "live: c_T = c"),
    ("stability", "RelativisticStability.lean", "stability conditions"),
    ("dual", "DualChannelDerivation.lean",
     "RETIRED branch: mu = x/(1+x) falsified 2026-09-12; mathematics kept as record"),
)


def build() -> str:
    reg = json.loads(SRC.read_text(encoding="utf-8"))
    claims = reg["claims"] if isinstance(reg, dict) else reg
    out = {
        "source": "assurance/claims.json",
        "generator": "scripts/export_visualizer_ledger.py",
        "claims": [{k: c.get(k, "") for k in FIELDS} for c in claims],
    }
    return json.dumps(out, indent=1, ensure_ascii=False) + "\n"


def build_lean() -> str:
    gate = (LEAN_DIR / "verify_all_proofs.sh").read_text(encoding="utf-8")
    mods = {}
    for key, fname, status in LEAN_MODULES:
        if fname not in gate:
            raise SystemExit(f"{fname} is not a verify_all_proofs.sh target; refusing to display it")
        mods[key] = {"file": f"05_lean_formalization/{fname}", "status": status,
                     "source": (LEAN_DIR / fname).read_text(encoding="utf-8")}
    return json.dumps({"generator": "scripts/export_visualizer_ledger.py", "modules": mods},
                      indent=1, ensure_ascii=False) + "\n"


def main() -> int:
    outputs = ((DST, build()), (LEAN_DST, build_lean()))
    if "--check" in sys.argv:
        stale = [d for d, text in outputs
                 if (d.read_text(encoding="utf-8") if d.exists() else "") != text]
        if stale:
            print("visualizer ledger: FAIL -- stale: "
                  + ", ".join(str(d.relative_to(ROOT)) for d in stale)
                  + "; run python3 scripts/export_visualizer_ledger.py")
            return 1
        n = len(json.loads(outputs[0][1])["claims"])
        print(f"visualizer ledger: PASS ({n} claims, {len(LEAN_MODULES)} Lean modules)")
        return 0
    for d, text in outputs:
        d.write_text(text, encoding="utf-8")
        print(f"wrote {d.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
