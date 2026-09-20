#!/usr/bin/env python3
"""Validate YAML frontmatter across tracked markdown files.

Checks:
1. If a markdown file opens with `---`, it must have a valid closing `---`.
2. The frontmatter block must be syntactically valid YAML.
3. No rogue characters or unclosed delimiters.

Usage:
    python3 scripts/check_frontmatter.py            # report
    python3 scripts/check_frontmatter.py --check    # exit 1 on errors
    python3 scripts/check_frontmatter.py --self-test
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus_surfaces  # noqa: E402
import yaml

ROOT = Path(__file__).resolve().parent.parent

# Enumeration is shared -- see scripts/corpus_surfaces.py. PHYSICS_CORE.md, the
# file whose frontmatter this check exists to protect, lives in 00_CANONICAL in
# the PARENT repo, which a submodule-only ls-files never saw.
SKIP = ("raw/", "80_Archive/", "docs/recovered/", "archive")


def tracked_md_files() -> list[tuple[Path, str]]:
    return corpus_surfaces.tracked_markdown(SKIP)


def check_content(content: str, rel: str) -> list[str]:
    """Validate one file's frontmatter. Split from check_file so the
    regression fixtures can drive the real logic."""
    issues = []

    # A DISPLACED frontmatter block is the failure this check was built for:
    # text inserted above the opening '---' leaves a file that no longer
    # startswith('---'), so a startswith-only guard skips it silently and the
    # YAML is dead. Detect a fence that looks like frontmatter but is not at
    # the top of the file.
    if not content.startswith("---"):
        lines = content.splitlines()
        for i, line in enumerate(lines[:12]):
            if line.strip() != "---":
                continue
            body = lines[i + 1:i + 40]
            closing = next((j for j, l in enumerate(body) if l.strip() == "---"), None)
            if closing is None:
                break
            block = "\n".join(body[:closing])
            try:
                data = yaml.safe_load(block)
            except Exception:
                break
            if isinstance(data, dict) and data:
                issues.append(
                    f"{rel}: YAML frontmatter is present but does NOT start the "
                    f"file (opens at line {i + 1}); anything above it makes the "
                    f"frontmatter inert")
            break

    # Only validate files that attempt to use YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) < 3:
            issues.append(f"{rel}: frontmatter opens with '---' but has no closing '---'")
        else:
            frontmatter_text = parts[1]
            try:
                data = yaml.safe_load(frontmatter_text)
                if data is not None and not isinstance(data, (dict, list)):
                    issues.append(f"{rel}: frontmatter must parse to mapping or sequence")
            except Exception as e:
                issues.append(f"{rel}: invalid YAML frontmatter: {e}")

    return issues


def check_file(path: Path, rel: str) -> list[str]:
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return [f"{rel}: could not read ({e})"]
    return check_content(content, rel)


def self_test() -> int:
    """Drives the REAL check_content() path. The previous self-test
    reimplemented the logic inline, so it could pass while check_content()
    rotted -- and it did: it asserted nothing about displaced frontmatter,
    which is the failure this script exists to catch."""
    cases = [
        ("valid mapping",
         "---\ntitle: Valid\n---\nBody text", True),
        ("valid sequence value",
         "---\nfoo: [1, 2, 3]\n---\nMore text", True),
        ("unclosed fence",
         "---\nunclosed frontmatter\nBody text", False),
        ("invalid yaml",
         "---\n: invalid: yaml: [}\n---\nBody", False),
        ("horizontal rule is not frontmatter",
         "# No frontmatter\nJust a normal header\n---\nHorizontal rule", True),
        # The regression: PHYSICS_CORE.md had a notice inserted above its
        # opening '---', which left the YAML inert and invisible.
        ("displaced frontmatter (blockquote above the fence)",
         "\n> **BRANCH NOTICE.** injected\n---\ntype: canonical\nversion: 1.0.0\n---\nBody",
         False),
        ("displaced frontmatter (prose above the fence)",
         "Some stray line\n---\ntitle: x\nstatus: y\n---\nBody", False),
    ]
    fails = 0
    for name, text, should_pass in cases:
        issues = check_content(text, "fixture.md")
        passed = not issues
        if passed != should_pass:
            want = "pass" if should_pass else "fail"
            print(f"  SELF-TEST FAIL: {name} -- expected to {want}, did not",
                  file=sys.stderr)
            fails += 1
    if fails == 0:
        print(f"check_frontmatter self-test: PASS ({len(cases)} cases)")
        return 0
    print("check_frontmatter self-test: FAIL", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="YAML Frontmatter Validator")
    parser.add_argument("--check", action="store_true", help="Exit with code 1 if issues found")
    parser.add_argument("--self-test", action="store_true", help="Run internal unit tests")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    files = tracked_md_files()
    all_issues = []
    for path, rel in files:
        all_issues.extend(check_file(path, rel))

    if all_issues:
        print(f"FAIL: {len(all_issues)} frontmatter issue(s) detected:")
        for iss in all_issues:
            print(f"  • {iss}")
        return 1 if args.check else 0

    print(f"check_frontmatter: PASS ({len(files)} markdown files scanned, 0 errors)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
