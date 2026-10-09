#!/usr/bin/env python3
"""Compare a regenerated JSON result file with its committed version, field by field.

    python3 scripts/compare_json_numeric.py PATH REL_TOL      # exit 0 iff equal within REL_TOL
    python3 scripts/compare_json_numeric.py --self-test

Structure (keys, list lengths), strings, booleans and integers must match exactly. Floats must agree to
REL_TOL relative difference. It prints the largest relative difference it saw, so a passing run still
says how close it was. Used by reproduce_core_results.sh for the three optimizer and bootstrap outputs.
"""
import json
import subprocess
import sys


def compare(a, b, tol):
    bad, worst = [], 0.0

    def walk(x, y, p):
        nonlocal worst
        if isinstance(x, dict) and isinstance(y, dict):
            if set(x) != set(y):
                bad.append(f"{p}: keys differ {sorted(set(x) ^ set(y))[:5]}")
            for k in sorted(set(x) & set(y)):
                walk(x[k], y[k], f"{p}.{k}")
        elif isinstance(x, list) and isinstance(y, list):
            if len(x) != len(y):
                bad.append(f"{p}: length {len(x)} vs {len(y)}")
            for i, (u, v) in enumerate(zip(x, y)):
                walk(u, v, f"{p}[{i}]")
        elif isinstance(x, float) or isinstance(y, float):
            if isinstance(x, bool) or isinstance(y, bool) or not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                bad.append(f"{p}: {x!r} vs {y!r}")
                return
            if x == y:
                return
            r = abs(x - y) / max(abs(x), abs(y))
            worst = max(worst, r)
            if r > tol:
                bad.append(f"{p}: {x!r} vs {y!r} (relative {r:.2e})")
        elif type(x) is not type(y) or x != y:
            bad.append(f"{p}: {x!r} vs {y!r}")

    walk(a, b, "$")
    return bad, worst


def self_test():
    base = {"a": 1.0, "b": [1e-26, 2.5], "n": 3, "s": "x", "t": True}
    cases = [
        ("identical", base, 1e-8, True),
        ("tiny float change", {**base, "a": 1.0 + 4e-10}, 1e-8, True),
        ("float change past tolerance", {**base, "a": 1.0 + 1e-6}, 1e-8, False),
        ("integer change", {**base, "n": 4}, 1e-8, False),
        ("string change", {**base, "s": "y"}, 1e-8, False),
        ("bool flipped", {**base, "t": False}, 1e-8, False),
        ("key removed", {k: v for k, v in base.items() if k != "s"}, 1e-8, False),
        ("list shortened", {**base, "b": [1e-26]}, 1e-8, False),
        ("float became string", {**base, "a": "1.0"}, 1e-8, False),
        ("small number, large relative change", {**base, "b": [2e-26, 2.5]}, 1e-8, False),
    ]
    fails = 0
    for name, other, tol, want in cases:
        bad, _ = compare(base, other, tol)
        if (not bad) != want:
            print(f"SELF-TEST FAIL: {name}: equal={not bad}, expected {want}")
            fails += 1
    print(f"compare_json_numeric self-test: {'PASS' if not fails else 'FAIL'} ({len(cases)} cases)")
    return 1 if fails else 0


def main(argv):
    if argv[:1] == ["--self-test"]:
        return self_test()
    if len(argv) != 2:
        print(__doc__)
        return 2
    path, tol = argv[0], float(argv[1])
    committed = json.loads(subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, text=True,
                                          check=True).stdout)
    with open(path) as f:
        regenerated = json.load(f)
    bad, worst = compare(committed, regenerated, tol)
    for line in bad[:20]:
        print(f"  {path} differs: {line}")
    print(f"  {path}: max relative difference {worst:.2e} (tolerance {tol:g}) -> {'FAIL' if bad else 'ok'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
