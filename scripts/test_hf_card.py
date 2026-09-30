#!/usr/bin/env python3
"""Guard the public Hugging Face dataset card against drift and overclaim.

The card is regenerated and pushed to huggingface.co/datasets/ChyRho/res-nova on
every push to main. Until 2026-09-30 it claimed that mu_std "clears Cassini Q2
quadrupole bounds" -- the opposite of CURRENT_STATE_READ_THIS_FIRST.md, where bare
mu_std is excluded by Q2 at ~4.6 sigma -- and advertised a `Lean/` directory that
never existed. Both were live on the Hub. This makes both failure modes mechanical:

    python3 scripts/test_hf_card.py              # exit 1 on a violation
    python3 scripts/test_hf_card.py --self-test  # prove each rule fires
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_huggingface as hf  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Phrases that assert a result the repository's own current-state file contradicts.
FORBIDDEN = [
    (re.compile(r"clear(s|ing)?\s+(the\s+)?Cassini", re.I),
     "mu_std does not clear Cassini: the EFE quadrupole excludes it (~4.6 sigma)"),
    (re.compile(r"100\s*%\s*verified", re.I),
     "'100% verified' conflates compiling mathematics with verified physics"),
    (re.compile(r"2\s*\\*\*?pi\s+(is\s+)?(proved|derived)|KMS[^.\n]{0,40}proves?\s+the\s+2", re.I),
     "the 2*pi is declared; KMS matching gives a = cH (2*pi cancels)"),
    (re.compile(r"mu_dual|x\s*/\s*\(1\s*\+\s*x\)"),
     "mu_dual is falsified (2026-09-12)"),
]


def violations(card: str, dirs: dict, root_files: list, root: Path) -> list[str]:
    out = []
    for pat, why in FORBIDDEN:
        m = pat.search(card)
        if m:
            out.append(f"forbidden claim {m.group(0)!r}: {why}")
    for d in dirs:
        if not (root / d).is_dir():
            out.append(f"card advertises directory {d}/ which does not exist")
    for f in root_files:
        if not (root / f).exists():
            out.append(f"card advertises file {f} which does not exist")
    # Every backticked directory in the Structure section must be one we upload.
    advertised = set(re.findall(r"^- `([^`/]+)/`", card, re.M))
    for d in advertised - set(dirs):
        out.append(f"card lists {d}/ but the sync does not upload it")
    return out


def self_test() -> int:
    good = hf.generate_hf_readme()
    assert not violations(good, hf.DIRS_TO_UPLOAD, hf.ROOT_FILES, ROOT), "live card must pass"
    cases = [
        ("Cassini overclaim", good + "\nmu_std action closure clearing Cassini Q2 bounds.\n", hf.DIRS_TO_UPLOAD),
        ("100% verified", good + "\n100% verified Lean 4 modules\n", hf.DIRS_TO_UPLOAD),
        ("2pi proved", good + "\nthe 2*pi is proved by KMS\n", hf.DIRS_TO_UPLOAD),
        ("mu_dual", good + "\nmu_dual interpolation\n", hf.DIRS_TO_UPLOAD),
        ("phantom dir in list", good, {**hf.DIRS_TO_UPLOAD, "Lean": "x"}),
        ("phantom dir in text", good + "\n- `Lean/`: modules\n", hf.DIRS_TO_UPLOAD),
    ]
    failed = 0
    for name, card, dirs in cases:
        if violations(card, dirs, hf.ROOT_FILES, ROOT):
            print(f"  ok    {name} fires")
        else:
            print(f"  FAIL  {name} did not fire")
            failed += 1
    print("self-test:", "PASS" if not failed else "FAIL")
    return 1 if failed else 0


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    v = violations(hf.generate_hf_readme(), hf.DIRS_TO_UPLOAD, hf.ROOT_FILES, ROOT)
    for line in v:
        print("  " + line)
    print("hf card:", "FAIL" if v else "PASS")
    return 1 if v else 0


if __name__ == "__main__":
    sys.exit(main())
