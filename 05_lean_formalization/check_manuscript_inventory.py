#!/usr/bin/env python3
"""Fail if the manuscript names Lean modules that do not exist on disk.

This is the check that would have caught the five phantom Table 2 rows.
It compares every \\texttt{...lean} mention in the LaTeX sources against the
tracked contents of 05_lean_formalization/, in both directions:

  * named in the manuscript, absent from disk   -> hard failure
  * present on disk, never named in Table 2     -> hard failure

It also cross-checks any "N modules" claim against the real count, and
verifies that every #print axioms target resolves to a declaration in the
same file (the defect that makes PrintAxioms.lean unelaborable).

Exit 0 only if all three checks pass.  No Lean toolchain required.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LEAN_DIR = REPO / "05_lean_formalization"
TEX_FILES = ["final_manuscript.tex", "reproducibility_appendix.tex"]

# The gate iterates *.lean and skips lakefile.lean; mirror that exactly.
SKIP = {"lakefile.lean"}


def disk_modules() -> set[str]:
    return {p.name for p in LEAN_DIR.glob("*.lean")} - SKIP


def named_in_tex(text: str) -> set[str]:
    r"""Every \texttt{Foo.lean} mention, with LaTeX escaping undone."""
    raw = re.findall(r"\\texttt\{([A-Za-z0-9_\\]+\.lean)\}", text)
    return {m.replace("\\_", "_") for m in raw}


def check_inventory() -> list[str]:
    errors: list[str] = []
    on_disk = disk_modules()

    for tex_name in TEX_FILES:
        tex = REPO / tex_name
        if not tex.exists():
            continue
        named = named_in_tex(tex.read_text(encoding="utf-8", errors="replace"))
        for phantom in sorted(named - on_disk):
            errors.append(
                f"{tex_name}: names {phantom!r}, which does not exist on disk"
            )

    # Table 2 is the authoritative inventory surface; it must be complete.
    manuscript = REPO / "final_manuscript.tex"
    if manuscript.exists():
        named = named_in_tex(manuscript.read_text(encoding="utf-8", errors="replace"))
        for missing in sorted(on_disk - named):
            errors.append(
                f"final_manuscript.tex: never mentions {missing!r}, which exists on disk"
            )

    return errors


def check_counts() -> list[str]:
    errors: list[str] = []
    actual = len(disk_modules())
    for tex_name in TEX_FILES:
        tex = REPO / tex_name
        if not tex.exists():
            continue
        text = tex.read_text(encoding="utf-8", errors="replace")
        # The negative lookbehind keeps "Lean~4 modules" from reading as a count of 4.
        for claimed in re.findall(r"(?<!Lean~)(\d+)\}?\s+(?:Lean~4\s+)?modules", text):
            if int(claimed) != actual:
                errors.append(
                    f"{tex_name}: claims {claimed} modules, inventory has {actual}"
                )
    return errors


def check_print_axioms() -> list[str]:
    """A #print axioms target must be declared in the same file, or imported."""
    errors: list[str] = []
    decl = re.compile(
        r"^\s*(?:theorem|lemma|def|noncomputable def|abbrev)\s+(\S+)", re.M
    )

    for path in sorted(LEAN_DIR.glob("*.lean")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        targets = re.findall(r"#print\s+axioms\s+(\S+)", text)
        if not targets:
            continue
        local = set(decl.findall(text))
        # A local import of a sibling module would also bring names into scope.
        imported = set(re.findall(r"^import\s+(\S+)", text, re.M))
        siblings = {p.stem for p in LEAN_DIR.glob("*.lean")}
        imports_sibling = bool(imported & siblings)

        for t in targets:
            if t not in local and not imports_sibling:
                errors.append(
                    f"{path.name}: '#print axioms {t}' — not declared here and no "
                    f"sibling module imported; this file cannot elaborate"
                )
    return errors


def main() -> int:
    sections = [
        ("module inventory", check_inventory()),
        ("module count", check_counts()),
        ("#print axioms resolution", check_print_axioms()),
    ]

    failed = False
    for title, errors in sections:
        if errors:
            failed = True
            print(f"FAIL  {title}")
            for e in errors:
                print(f"        {e}")
        else:
            print(f"OK    {title}")

    print()
    print(f"inventory: {len(disk_modules())} module(s) on disk")
    print("RESULT: FAIL" if failed else "RESULT: PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
