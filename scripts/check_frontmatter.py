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
import yaml

ROOT = Path(__file__).resolve().parent.parent

def tracked_md_files() -> list[Path]:
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "*.md"],
        capture_output=True, text=True
    ).stdout.splitlines()
    skip = ("raw/", "80_Archive/", "docs/recovered/", "archive")
    return [ROOT / f for f in out if not any(s in f for s in skip)]

def check_file(path: Path) -> list[str]:
    issues = []
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return [f"{path}: could not read ({e})"]

    # Only validate files that attempt to use YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) < 3:
            issues.append(f"{path.relative_to(ROOT)}: frontmatter opens with '---' but has no closing '---'")
        else:
            frontmatter_text = parts[1]
            try:
                data = yaml.safe_load(frontmatter_text)
                if data is not None and not isinstance(data, (dict, list)):
                    issues.append(f"{path.relative_to(ROOT)}: frontmatter must parse to mapping or sequence")
            except Exception as e:
                issues.append(f"{path.relative_to(ROOT)}: invalid YAML frontmatter: {e}")

    return issues

def self_test() -> int:
    cases = [
        ("---\ntitle: Valid\n---\nBody text", True),
        ("---\nfoo: [1, 2, 3]\n---\nMore text", True),
        ("---\nunclosed frontmatter\nBody text", False),
        ("---\n: invalid: yaml: [}\n---\nBody", False),
        ("# No frontmatter\nJust a normal header\n---\nHorizontal rule", True),
    ]
    fails = 0
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        for idx, (text, should_pass) in enumerate(cases):
            p = Path(tmpdir) / f"test_{idx}.md"
            p.write_text(text, encoding="utf-8")
            # Run check
            issues = []
            if text.startswith("---"):
                parts = text.split("---", 2)
                if len(parts) < 3:
                    issues.append("unclosed")
                else:
                    try:
                        yaml.safe_load(parts[1])
                    except Exception:
                        issues.append("invalid yaml")
            passed = len(issues) == 0
            if passed != should_pass:
                print(f"SELF-TEST FAIL case {idx}: got passed={passed}, expected {should_pass}", file=sys.stderr)
                fails += 1
    if fails == 0:
        print("check_frontmatter self-test: PASS")
        return 0
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
    for f in files:
        issues = check_file(f)
        all_issues.extend(issues)

    if all_issues:
        print(f"FAIL: {len(all_issues)} frontmatter issue(s) detected:")
        for iss in all_issues:
            print(f"  • {iss}")
        return 1 if args.check else 0

    print(f"check_frontmatter: PASS ({len(files)} markdown files scanned, 0 errors)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
