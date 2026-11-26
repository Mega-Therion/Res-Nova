#!/usr/bin/env python3
"""Deterministic receipt for one run of 05_lean_formalization/verify_all_proofs.sh.

The fresh-clone nightly (.github/workflows/fresh-clone-nightly.yml) builds the
Lean suite in a bare container, runs the proof gate, and turns the gate's log
into this receipt. The receipt's sha256 is compared with a committed known-good
value, so a fresh clone that verifies a different target set, or a different
axiom footprint, than the one on record fails loudly instead of going green.

    python3 scripts/lean_receipt.py --write --log GATE_LOG --out DIR
    python3 scripts/lean_receipt.py --check --log GATE_LOG
    python3 scripts/lean_receipt.py --self-test

--write  writes DIR/LEAN_RECEIPT.txt and DIR/LEAN_RECEIPT.sha256 (sha256sum -c
         format) and prints the sha256.
--check  compares the receipt's sha256 with the committed known-good,
         05_lean_formalization/LEAN_RECEIPT.sha256 (--known-dir points
         elsewhere). Exit 0 on a match; 1 on a mismatch, with a unified diff
         against the committed LEAN_RECEIPT.txt when that file is committed
         too; 2 when the log is refused or the committed files are malformed or
         disagree with each other. With no committed LEAN_RECEIPT.sha256 it
         prints a BOOTSTRAP notice and exits 0: nothing was compared.
The two flags combine (the comparison reads the committed files before
anything is written). --lean-dir (default 05_lean_formalization) is where
lean-toolchain, lake-manifest.json and the target sources are read. Under
GitHub Actions both modes also write step outputs (sha256, verdict, expected)
and a step summary.

RECORDING THE KNOWN-GOOD
Copy LEAN_RECEIPT.txt and LEAN_RECEIPT.sha256 from a green fresh-clone run's
artifact into 05_lean_formalization/ and commit both. Re-record after every
Lean-facing change (a new target, a new `#print axioms`, a toolchain or
manifest bump): the receipt is meant to change then. 05_lean_formalization is
a physics path for scripts/current_state_freshness.py, so that commit also
needs CURRENT_STATE's verified date refreshed.

WHAT THE RECEIPT CONTAINS (format 1; UTF-8, LF endings, one trailing newline)
  * the toolchain named by lean-toolchain;
  * the mathlib rev pinned in lake-manifest.json, then every other package pin;
  * the targets the gate printed as OK, sorted;
  * one line per declaration whose axioms the build printed:
        <file> '<decl>' depends on axioms: [a, b, c]
        <file> '<decl>' does not depend on any axioms
    sorted, de-duplicated on (file, decl).
Line:column positions, timings, warnings and the commit are left out on purpose:
the receipt records WHAT was verified, so moving a proof down a few lines, or a
commit that changes nothing Lean-facing, keeps the same hash. Sorting is done
here, in Python, so the hash does not depend on anyone's locale.

WHERE THE AXIOM LINES COME FROM
verify_all_proofs.sh keeps each target's own `lake env lean` output to itself
unless the target fails. The `#print axioms` messages reach its stdout through
the `lake build` it runs first: Lake prints a module's info messages when it
builds the module ("Built X") and again when it replays an up-to-date one
("Replayed X"). Only the log after the gate's own `[gate] TARGETS == lakefile
roots` line is read, so a log that also holds an earlier `lake build` (as
`lake build && verify_all_proofs.sh | tee` produces) still carries each message
exactly once. Lean wraps a long axiom list over several lines; the parser joins
the continuation lines.

FAIL-CLOSED CHECKS (the log is refused: exit 2, nothing written)
  * the log holds exactly one `[gate] ... (N modules)` line and, after it,
    exactly one `RESULT: PASS` and one `verified: N / N` line, N equal to the
    number of OK lines, and the OK targets equal the .lean files on disk;
  * per target, the number of axiom messages equals the number of `#print
    axioms` commands in its source outside comments and strings. A log that
    lost messages is refused rather than recorded;
  * every footprint uses only propext, Classical.choice and Quot.sound. This
    repeats a gate check on purpose: the gate greps one line at a time, so an
    axiom list that Lean wrapped across lines never reaches its check.
"""

from __future__ import annotations

import argparse
import contextlib
import difflib
import hashlib
import io
import json
import os
import re
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path

FORMAT = 1
RECEIPT_NAME = "LEAN_RECEIPT.txt"
HASH_NAME = "LEAN_RECEIPT.sha256"
STANDARD_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
REPO = Path(__file__).resolve().parent.parent
DEFAULT_LEAN_DIR = REPO / "05_lean_formalization"
MAX_WRAP_LINES = 64  # continuation lines allowed for one wrapped axiom list
DIFF_SUMMARY_LINES = 200
GITHUB_ENV_KEYS = ("GITHUB_ACTIONS", "GITHUB_OUTPUT", "GITHUB_STEP_SUMMARY")

ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
OK_RE = re.compile(r"^OK\s+(\S+\.lean)\s*$")
VERIFIED_RE = re.compile(r"^verified:\s*(\d+)\s*/\s*(\d+)\s+target")
RESULT_RE = re.compile(r"^RESULT:\s*(\S+)")
# The count comes from `wc -l`, which pads with spaces on some platforms.
GATE_RE = re.compile(r"^\[gate\] TARGETS == lakefile roots \(\s*(\d+) modules\)")
# Lake prints `info: F.lean:L:C: msg`; the position may also precede the
# severity. The declaration name may itself contain primes (foo').
MSG_RE = re.compile(
    r"^(?:info:\s*)?(?P<file>[^\s:]+\.lean):\d+:\d+:\s*(?:info:\s*)?"
    r"'(?P<decl>.+?)'\s+"
    r"(?P<rest>depends on axioms:.*|does not depend on any axioms\s*)$"
)
PRINT_AXIOMS_RE = re.compile(r"(?m)^[ \t]*#print[ \t]+axioms\b")
EXIT_RE = re.compile(r"(?m)^[ \t]*#exit\b")
CHAR_LIT_RE = re.compile(r"'(?:[^'\\\n]|\\.)'")
HASH_LINE_RE = re.compile(r"^([0-9a-fA-F]{64})(?:\s+\*?(\S+))?$")


class ReceiptError(Exception):
    """The log or the committed known-good cannot be trusted as given."""


# ----------------------------------------------------------------- parsing ---
def clean_lines(text: str) -> list[str]:
    text = ANSI_RE.sub("", text).replace("\r\n", "\n").replace("\r", "\n")
    return text.split("\n")


def norm_file(path: str) -> str:
    """Targets are top-level files of the Lean directory; keep the file name."""
    return path.replace("\\", "/").rsplit("/", 1)[-1]


def parse_footprints(lines: list[str]) -> list[tuple[str, str, tuple[str, ...]]]:
    """(file, decl, axioms) for every `#print axioms` message, in log order.

    `axioms` is empty for "does not depend on any axioms".
    """
    found = []
    i = 0
    while i < len(lines):
        m = MSG_RE.match(lines[i])
        if not m:
            i += 1
            continue
        file, decl, rest = norm_file(m.group("file")), m.group("decl"), m.group("rest")
        if rest.startswith("does not depend"):
            found.append((file, decl, ()))
            i += 1
            continue
        text = rest[len("depends on axioms:"):]
        j = i
        while "]" not in text:
            j += 1
            if j >= len(lines) or j - i > MAX_WRAP_LINES or not lines[j][:1].isspace():
                raise ReceiptError(
                    f"log line {i + 1}: axiom list for {file} '{decl}' never closes")
            text += " " + lines[j].strip()
        body = text.strip()
        if not body.startswith("[") or body.count("[") != 1 or not body.endswith("]"):
            raise ReceiptError(f"log line {i + 1}: cannot read the axiom list {body!r}")
        axioms = tuple(a.strip() for a in body[1:-1].split(",") if a.strip())
        if not axioms:
            raise ReceiptError(f"log line {i + 1}: empty axiom list for {file} '{decl}'")
        found.append((file, decl, axioms))
        i = j + 1
    return found


def lean_code_only(src: str) -> str:
    """Blank out comments and string/char literals, keeping line structure.

    Handles `--` line comments, nested `/- -/` block comments (doc comments
    included) and `"..."` strings with escapes. A prime inside a name (foo')
    is not a char literal: only 'x' and '\\x' forms are skipped.
    """
    out = []
    i, n, depth = 0, len(src), 0
    while i < n:
        c = src[i]
        if depth:
            if src.startswith("/-", i):
                depth += 1
                out.append("  ")
                i += 2
            elif src.startswith("-/", i):
                depth -= 1
                out.append("  ")
                i += 2
            else:
                out.append("\n" if c == "\n" else " ")
                i += 1
        elif src.startswith("/-", i):
            depth = 1
            out.append("  ")
            i += 2
        elif src.startswith("--", i):
            j = src.find("\n", i)
            j = n if j < 0 else j
            out.append(" " * (j - i))
            i = j
        elif c == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
            j = min(j + 1, n)
            out.append("".join("\n" if ch == "\n" else " " for ch in src[i:j]))
            i = j
        elif c == "'" and (lit := CHAR_LIT_RE.match(src, i)):
            out.append(" " * len(lit.group(0)))
            i = lit.end()
        else:
            out.append(c)
            i += 1
    return "".join(out)


def count_print_axioms(src: str) -> int:
    """`#print axioms` commands Lean will actually run (none after `#exit`)."""
    code = lean_code_only(src)
    stop = EXIT_RE.search(code)
    return len(PRINT_AXIOMS_RE.findall(code[:stop.start()] if stop else code))


def render(file: str, decl: str, axioms: tuple[str, ...]) -> str:
    if not axioms:
        return f"{file} '{decl}' does not depend on any axioms"
    return f"{file} '{decl}' depends on axioms: [{', '.join(axioms)}]"


# ------------------------------------------------------------------- build ---
def read_pins(lean_dir: Path) -> tuple[str, dict[str, str]]:
    """(toolchain, {package: rev}) from lean-toolchain and lake-manifest.json."""
    toolchain = (lean_dir / "lean-toolchain").read_text(encoding="utf-8").strip()
    if not toolchain or "\n" in toolchain:
        raise ReceiptError(f"unexpected lean-toolchain contents: {toolchain!r}")
    manifest = json.loads((lean_dir / "lake-manifest.json").read_text(encoding="utf-8"))
    pins: dict[str, str] = {}
    for pkg in manifest.get("packages", []):
        name, rev = pkg.get("name"), pkg.get("rev")
        if not isinstance(name, str) or not name or not isinstance(rev, str) or not rev:
            raise ReceiptError(f"lake-manifest.json package without a name and rev: {pkg!r}")
        if any(ch.isspace() for ch in name + rev) or name in pins:
            raise ReceiptError(f"lake-manifest.json: unusable or repeated pin {name!r} {rev!r}")
        pins[name] = rev
    if "mathlib" not in pins:
        raise ReceiptError("lake-manifest.json pins no mathlib package")
    return toolchain, pins


def build_receipt(log_text: str, lean_dir: Path) -> str:
    lines = clean_lines(log_text)

    starts = [i for i, ln in enumerate(lines) if GATE_RE.match(ln)]
    if len(starts) != 1:
        raise ReceiptError(
            f"expected one '[gate] TARGETS == lakefile roots' line, found {len(starts)}: "
            "the log must hold exactly one verify_all_proofs.sh run")
    n_gate = int(GATE_RE.match(lines[starts[0]]).group(1))
    lines = lines[starts[0] + 1:]  # the gate's own output; an earlier build is ignored

    results = [m.group(1) for ln in lines if (m := RESULT_RE.match(ln))]
    if results != ["PASS"]:
        raise ReceiptError(
            f"expected exactly one 'RESULT: PASS' in the gate log, found {results or 'none'}")
    ok = [m.group(1) for ln in lines if (m := OK_RE.match(ln))]
    dupes = sorted(t for t, c in Counter(ok).items() if c > 1)
    if dupes:
        raise ReceiptError(f"targets reported OK more than once: {dupes}")
    verified = [m.groups() for ln in lines if (m := VERIFIED_RE.match(ln))]
    if len(verified) != 1:
        raise ReceiptError(f"expected one 'verified: N / M' line, found {len(verified)}")
    n_ok, n_declared = (int(x) for x in verified[0])
    if not n_ok == n_declared == len(ok) == n_gate:
        raise ReceiptError(
            f"verified {n_ok} / {n_declared}, {len(ok)} OK lines, {n_gate} lakefile roots: "
            "not a clean full pass")

    on_disk = sorted(p.name for p in lean_dir.glob("*.lean") if p.name != "lakefile.lean")
    if sorted(ok) != on_disk:
        raise ReceiptError(
            "OK targets differ from the .lean files on disk: "
            f"log-only {sorted(set(ok) - set(on_disk))}, disk-only {sorted(set(on_disk) - set(ok))}")

    toolchain, pins = read_pins(lean_dir)

    footprints = parse_footprints(lines)
    strays = sorted({f for f, _, _ in footprints} - set(ok))
    if strays:
        raise ReceiptError(f"axiom messages from files that are not OK targets: {strays}")
    seen_count = Counter(f for f, _, _ in footprints)
    gaps = []
    for t in sorted(ok):
        want = count_print_axioms((lean_dir / t).read_text(encoding="utf-8"))
        if seen_count.get(t, 0) != want:
            gaps.append(f"{t}: {want} '#print axioms' in source, {seen_count.get(t, 0)} in log")
    if gaps:
        raise ReceiptError(
            "axiom messages in the log do not match the sources:\n  " + "\n  ".join(gaps))
    bad = [render(f, d, a) for f, d, a in footprints if set(a) - STANDARD_AXIOMS]
    if bad:
        raise ReceiptError("non-standard axiom footprint(s):\n  " + "\n  ".join(sorted(bad)))
    unique: dict[tuple[str, str], tuple[str, ...]] = {}
    for f, d, a in footprints:
        if unique.setdefault((f, d), a) != a:
            raise ReceiptError(f"conflicting footprints for {f} '{d}' in one log")
    axiom_lines = sorted(render(f, d, a) for (f, d), a in unique.items())

    out = [f"res-nova-lean-receipt: format {FORMAT}",
           f"lean-toolchain: {toolchain}",
           f"mathlib-rev: {pins['mathlib']}"]
    out += [f"package: {name} {rev}" for name, rev in sorted(pins.items()) if name != "mathlib"]
    out.append(f"targets-verified: {len(ok)}")
    out += [f"target: {t}" for t in sorted(ok)]
    out.append(f"axiom-footprints: {len(axiom_lines)}")
    out += [f"axioms: {line}" for line in axiom_lines]
    return "\n".join(out) + "\n"


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_receipt(data: bytes, out_dir: Path) -> str:
    digest = sha256_hex(data)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / RECEIPT_NAME).write_bytes(data)
    (out_dir / HASH_NAME).write_bytes(f"{digest}  {RECEIPT_NAME}\n".encode("ascii"))
    return digest


def receipt_counts(data: bytes) -> list[str]:
    return [ln for ln in data.decode("utf-8").splitlines()
            if ln.startswith(("lean-toolchain:", "mathlib-rev:", "targets-verified:",
                              "axiom-footprints:"))]


# ------------------------------------------------------------------- check ---
def read_known_hash(path: Path) -> str:
    """The sha256 in a committed `<sha256>  LEAN_RECEIPT.txt` (or bare `<sha256>`) file."""
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    m = HASH_LINE_RE.match(lines[0]) if len(lines) == 1 else None
    if not m or m.group(2) not in (None, RECEIPT_NAME):
        raise ReceiptError(f"{path} is not one '<sha256>  {RECEIPT_NAME}' line")
    return m.group(1).lower()


def check_receipt(data: bytes, known_dir: Path) -> tuple[str, int, str, list[str]]:
    """(verdict, exit code, expected sha256, report lines) against the known-good."""
    got = sha256_hex(data)
    known_hash, known_text = known_dir / HASH_NAME, known_dir / RECEIPT_NAME
    report = [f"receipt sha256:   {got}"]
    if not known_hash.exists():
        report.append(
            f"BOOTSTRAP - no comparison: {known_hash} is not committed, so nothing was compared "
            "and this run does not count toward the clean track record. To start it, commit "
            f"this run's {RECEIPT_NAME} and {HASH_NAME} into {known_dir}.")
        if known_text.exists():
            report.append(f"WARNING: {known_text} is committed without {HASH_NAME}.")
        return "bootstrap", 0, "", report
    try:
        expected = read_known_hash(known_hash)
    except (ReceiptError, OSError, UnicodeDecodeError) as e:
        return "error", 2, "", report + [f"ERROR: {e}"]
    report.append(f"committed sha256: {expected} ({known_hash})")
    if known_text.exists() and sha256_hex(known_text.read_bytes()) != expected:
        return "error", 2, expected, report + [
            f"ERROR: the committed {known_text} does not hash to the committed {HASH_NAME}: "
            "the known-good pair is inconsistent. Re-record both files together."]
    if got == expected:
        report.append("MATCH - the fresh-clone receipt equals the committed known-good.")
        return "match", 0, expected, report
    report.append("DIVERGED - the fresh-clone receipt differs from the committed known-good.")
    if known_text.exists():
        old = known_text.read_text(encoding="utf-8").splitlines()
        new = data.decode("utf-8").splitlines()
        report += difflib.unified_diff(old, new, f"committed/{RECEIPT_NAME}",
                                       f"this-run/{RECEIPT_NAME}", lineterm="")
    else:
        report.append(f"(no committed {RECEIPT_NAME} to diff against; compare the run artifact)")
    return "diverged", 1, expected, report


# ------------------------------------------------------------ github hooks ---
def in_actions() -> bool:
    return os.environ.get("GITHUB_ACTIONS") == "true"


def gh_outputs(**values: str) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if in_actions() and path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("".join(f"{k}={v}\n" for k, v in values.items()))


def gh_summary(lines: list[str]) -> None:
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if in_actions() and path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n\n")


def gh_annotate(level: str, title: str, message: str) -> None:
    if in_actions():
        print(f"::{level} title={title}::{message}")


HEADLINES = {
    "match": "**MATCH** - this fresh-clone run reproduced the committed known-good receipt.",
    "diverged": "**DIVERGED** - this fresh-clone run does NOT reproduce the committed receipt.",
    "error": "**ERROR** - the committed known-good receipt files are malformed or inconsistent.",
    "bootstrap": "**BOOTSTRAP - no comparison.** No committed known-good receipt yet; "
                 "this run does not count toward the clean track record.",
}


def publish_check(verdict: str, got: str, expected: str, report: list[str],
                  data: bytes) -> None:
    gh_outputs(verdict=verdict, sha256=got, expected=expected)
    level = {"match": "notice", "bootstrap": "warning"}.get(verdict, "error")
    headline = next((ln for ln in report if ln.startswith(
        ("MATCH", "DIVERGED", "BOOTSTRAP", "ERROR:"))), verdict)
    gh_annotate(level, f"Lean receipt {verdict.upper()}", headline)
    body = [f"## Fresh-clone Lean receipt: {verdict}", "", HEADLINES[verdict], "",
            *[f"- `{c}`" for c in receipt_counts(data)], f"- receipt sha256 `{got}`"]
    if expected:
        body.append(f"- committed sha256 `{expected}`")
    diff = [ln for ln in report if ln.startswith(("---", "+++", "@@", "+", "-", " "))]
    if diff:
        body += ["", "```diff", *diff[:DIFF_SUMMARY_LINES], "```"]
        if len(diff) > DIFF_SUMMARY_LINES:
            body.append(f"(diff cut at {DIFF_SUMMARY_LINES} lines; the full diff is in the step log)")
    gh_summary(body)


# --------------------------------------------------------------------- cli ---
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="lean_receipt.py", description=__doc__.split("\n\n")[0],
        epilog="Exit codes: 0 written / match / bootstrap, 1 mismatch, 2 refused or malformed.")
    ap.add_argument("--write", action="store_true",
                    help="write DIR/LEAN_RECEIPT.txt and DIR/LEAN_RECEIPT.sha256 (needs --out)")
    ap.add_argument("--check", action="store_true",
                    help="compare with the committed known-good LEAN_RECEIPT.sha256")
    ap.add_argument("--self-test", action="store_true", help="run the built-in tests and exit")
    ap.add_argument("--log", type=Path, help="output of one verify_all_proofs.sh run")
    ap.add_argument("--out", type=Path, help="directory for the receipt files (--write)")
    ap.add_argument("--lean-dir", type=Path, default=DEFAULT_LEAN_DIR,
                    help="Lean project read for toolchain, pins and sources "
                         "(default: 05_lean_formalization)")
    ap.add_argument("--known-dir", type=Path,
                    help="directory holding the committed known-good (default: --lean-dir)")
    args = ap.parse_args(argv)

    if args.self_test:
        if args.write or args.check:
            ap.error("--self-test runs on its own")
        return self_test()
    if not (args.write or args.check):
        ap.error("give --write, --check, or both")
    if args.log is None:
        ap.error("--log is required")
    if args.write and args.out is None:
        ap.error("--write needs --out DIR")
    known = args.known_dir or args.lean_dir
    if args.write and args.check and args.out.resolve() == known.resolve():
        ap.error("--out is the known-good directory, so --check would compare the receipt "
                 "with itself; write somewhere else")

    try:
        text = build_receipt(args.log.read_text(encoding="utf-8", errors="replace"),
                             args.lean_dir)
    except (ReceiptError, OSError, ValueError) as e:
        print(f"lean receipt: REFUSED -- {e}", file=sys.stderr)
        gh_outputs(verdict="refused", sha256="", expected="")
        gh_annotate("error", "Lean receipt REFUSED", str(e).splitlines()[0])
        gh_summary(["## Fresh-clone Lean receipt: refused", "",
                    "The gate log could not be turned into a receipt:", "", "```",
                    str(e), "```"])
        return 2
    data = text.encode("utf-8")
    digest = sha256_hex(data)

    code = 0
    if args.check:  # before writing, so the committed files are read as they were
        verdict, code, expected, report = check_receipt(data, known)
    if args.write:
        write_receipt(data, args.out)
        print(f"lean receipt: wrote {args.out / RECEIPT_NAME} "
              f"({'; '.join(receipt_counts(data)[2:])})")
        print(f"sha256: {digest}")
        if not args.check:
            gh_outputs(sha256=digest)
            gh_summary(["## Fresh-clone Lean receipt: written", "",
                        *[f"- `{c}`" for c in receipt_counts(data)],
                        f"- receipt sha256 `{digest}`"])
    if args.check:
        print("\n".join(report))
        publish_check(verdict, digest, expected, report, data)
    return code


# --------------------------------------------------------------- self-test ---
def _fixture(root: Path) -> tuple[Path, str]:
    """A synthetic Lean dir plus a gate log in the real Lake/gate print format."""
    lean = root / "lean"
    lean.mkdir()
    (lean / "lean-toolchain").write_text("leanprover/lean4:v0.0.0-test\n", encoding="utf-8")
    (lean / "lake-manifest.json").write_text(json.dumps({"version": "1.2.0", "packages": [
        {"name": "mathlib", "rev": "a" * 40}, {"name": "batteries", "rev": "b" * 40}]}),
        encoding="utf-8")
    (lean / "lakefile.lean").write_text("-- not a target\n", encoding="utf-8")
    (lean / "Alpha.lean").write_text(
        "/-! Module doc. Verified by `#print axioms` below.\n"
        "#print axioms Commented.out\n"
        "/- nested -/ still inside -/\n"
        "theorem one' : True := trivial\n"
        "def s : String := \"/- not a comment\"\n"
        "def c : Char := '\"'\n"
        "-- #print axioms Also.ignored\n"
        "#print axioms Demo.one'\n"
        "#print axioms Demo.a_rather_long_declaration_name_that_lean_wraps\n"
        "#print axioms Demo.trivial_fact\n", encoding="utf-8")
    (lean / "Beta.lean").write_text("theorem b : True := trivial\n", encoding="utf-8")
    (lean / "Gamma.lean").write_text(
        "#print axioms Demo.gamma\n#exit\n#print axioms Never.elaborated\n", encoding="utf-8")
    tick, info, warn = chr(0x2714), chr(0x2139), chr(0x26A0)  # Lake's status glyphs
    alpha = [
        f"{info} [7/9] Built Alpha (1.2s)",
        "info: Alpha.lean:8:0: 'Demo.one'' depends on axioms: [propext]",
        "info: Alpha.lean:9:0: 'Demo.a_rather_long_declaration_name_that_lean_wraps' "
        "depends on axioms: [propext,",
        " Classical.choice,",
        " Quot.sound]",
        "info: Alpha.lean:10:0: 'Demo.trivial_fact' does not depend on any axioms",
    ]
    beta = [f"{tick} [8/9] Built Beta (0.4s)"]
    gamma = [
        f"{warn} [9/9] Built Gamma (0.9s)",
        "warning: Gamma.lean:1:4: unused variable `h`",
        "",
        "Note: This linter can be disabled with `set_option linter.unusedVariables false`",
        "info: Gamma.lean:1:0: 'Demo.gamma' depends on axioms:",
        " [propext, Quot.sound]",
    ]
    head = ["[gate] TARGETS == lakefile roots (3 modules)",
            "building library (required for cross-module imports)" + chr(0x2026)]
    tail = ["Build completed successfully (9 jobs).", "OK    Alpha.lean", "OK    Beta.lean",
            "OK    Gamma.lean", "", "verified: 3 / 3 target(s)", "RESULT: PASS",
            "NOTE: this certifies elaboration, absence of sorry, and a standard axiom"]
    return lean, "\n".join(head + alpha + beta + gamma + tail) + "\n"


@contextlib.contextmanager
def _sandboxed():
    """Silence output and hide the Actions environment while the self-test runs main()."""
    saved = {k: os.environ.pop(k) for k in GITHUB_ENV_KEYS if k in os.environ}
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            yield
    finally:
        os.environ.update(saved)


def _run(*argv: str) -> int:
    with _sandboxed():
        try:
            return main(list(argv))
        except SystemExit as e:  # argparse usage errors
            return int(e.code or 0)


def self_test() -> int:
    failures: list[str] = []

    def expect(cond: bool, what: str) -> None:
        if not cond:
            failures.append(what)

    def refused(log: str, lean: Path, what: str, needle: str) -> None:
        try:
            build_receipt(log, lean)
        except ReceiptError as e:
            expect(needle in str(e), f"{what}: refused for the wrong reason: {e}")
        else:
            failures.append(f"{what}: was NOT refused")

    def same(variant: str, what: str) -> None:
        try:
            expect(build_receipt(variant, lean) == text, what)
        except ReceiptError as e:
            failures.append(f"{what}: refused: {e}")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        lean, log = _fixture(root)
        try:
            text = build_receipt(log, lean)
        except ReceiptError as e:
            print(f"lean_receipt self-test: FAIL\n  - the fixture log is refused: {e}")
            return 1
        expect(text.endswith("\n") and not text.endswith("\n\n"), "one trailing newline")
        expect(text.isascii(), "fixture receipt is ASCII")
        expect(text.splitlines()[:5] == [
            "res-nova-lean-receipt: format 1",
            "lean-toolchain: leanprover/lean4:v0.0.0-test",
            f"mathlib-rev: {'a' * 40}",
            f"package: batteries {'b' * 40}",
            "targets-verified: 3"], f"receipt header: {text.splitlines()[:5]}")
        for line in [
            "target: Beta.lean",
            "axiom-footprints: 4",
            "axioms: Alpha.lean 'Demo.one'' depends on axioms: [propext]",
            "axioms: Alpha.lean 'Demo.a_rather_long_declaration_name_that_lean_wraps' "
            "depends on axioms: [propext, Classical.choice, Quot.sound]",
            "axioms: Alpha.lean 'Demo.trivial_fact' does not depend on any axioms",
            "axioms: Gamma.lean 'Demo.gamma' depends on axioms: [propext, Quot.sound]",
        ]:
            expect(line in text.splitlines(), f"receipt line missing: {line!r}")
        expect(count_print_axioms((lean / "Alpha.lean").read_text(encoding="utf-8")) == 3,
               "comment/string-aware #print axioms count")
        digest = sha256_hex(text.encode("utf-8"))

        # Same content, other block order, positions and CRLF endings: same bytes.
        blocks = log.split("\n")
        alpha, rest = blocks[2:8], blocks[8:]
        shuffled = blocks[:2] + rest[:7] + alpha + rest[7:]
        moved = "\r\n".join(shuffled).replace("Alpha.lean:8:0", "Alpha.lean:80:2")
        same(moved, "block order / positions / CRLF change the receipt")
        ok_lines = [ln for ln in blocks if ln.startswith("OK ")][::-1]
        reordered = [ln for ln in blocks if not ln.startswith("OK ")]
        at = reordered.index("verified: 3 / 3 target(s)")
        same("\n".join(reordered[:at] + ok_lines + reordered[at:]), "OK line order changes the receipt")
        same("\x1b[32m" + log.replace("RESULT: PASS", "RESULT: PASS\x1b[0m"),
             "ANSI colour changes the receipt")
        same(log.replace("(3 modules)", "(       3 modules)"), "padded `wc -l` count in the [gate] line")
        # `lake build && verify_all_proofs.sh | tee`: an earlier build replays the
        # same messages before the gate line; only the gate's own output counts.
        beta, gamma = blocks[8:9], blocks[9:15]
        expect(beta[0].endswith("Built Beta (0.4s)") and gamma[-1] == " [propext, Quot.sound]",
               f"fixture layout changed: {beta + gamma}")
        earlier = "\n".join(["info: mathlib: cloning https://example.invalid/mathlib4.git",
                             *alpha, *beta, *gamma, "Build completed successfully (9 jobs).", ""])
        same(earlier + log, "messages before the [gate] line counted")

        # A changed footprint changes the hash.
        mutated = log.replace("'Demo.one'' depends on axioms: [propext]",
                              "'Demo.one'' depends on axioms: [propext, Quot.sound]")
        mutated_text = build_receipt(mutated, lean)
        expect(sha256_hex(mutated_text.encode()) != digest, "mutated footprint, same hash")

        # Fail-closed refusals.
        refused(log.replace("RESULT: PASS", "RESULT: FAIL"), lean, "failed gate", "RESULT: PASS")
        refused(log + log, lean, "two runs in one log", "found 2")
        refused(log.replace("[gate] TARGETS", "[gaet] TARGETS"), lean, "no gate line", "found 0")
        refused(log.replace("verified: 3 / 3", "verified: 2 / 3"), lean, "partial pass", "verified")
        refused(log.replace("(3 modules)", "(4 modules)"), lean, "gate count mismatch", "4 lakefile roots")
        refused(log.replace("OK    Beta.lean\n", ""), lean, "missing OK line", "OK lines")
        refused(log.replace("info: Alpha.lean:10:0: 'Demo.trivial_fact' does not depend on any axioms\n",
                            ""), lean, "lost message", "Alpha.lean: 3")
        refused(log.replace(" Quot.sound]", " sorryAx]"), lean, "non-standard axiom (wrapped)", "sorryAx")
        refused(log.replace("[propext]", "[propext, Lean.ofReduceBool]"), lean,
                "non-standard axiom", "Lean.ofReduceBool")
        refused(log.replace(" Quot.sound]", "Quot.sound]"), lean, "unterminated list", "never closes")
        refused(log.replace("info: Gamma.lean:1:0", "info: Delta.lean:1:0"), lean,
                "message from a non-target", "Delta.lean")
        (lean / "Extra.lean").write_text("", encoding="utf-8")
        refused(log, lean, "target missing from the log", "Extra.lean")
        (lean / "Extra.lean").unlink()
        manifest = (lean / "lake-manifest.json").read_text(encoding="utf-8")
        (lean / "lake-manifest.json").write_text(manifest.replace('"mathlib"', '"mathlib5"'),
                                                 encoding="utf-8")
        refused(log, lean, "manifest without mathlib", "no mathlib")
        (lean / "lake-manifest.json").write_text(manifest, encoding="utf-8")

        # CLI: write to one directory, check against another (never against itself).
        gate, bad_gate = root / "gate.log", root / "gate-mutated.log"
        gate.write_text(log, encoding="utf-8")
        bad_gate.write_text(mutated, encoding="utf-8")
        out, known = root / "out", root / "known"
        known.mkdir()
        common = ("--lean-dir", str(lean), "--known-dir", str(known))
        expect(_run("--write", "--log", str(gate), "--out", str(out), *common) == 0, "--write exit 0")
        expect((out / RECEIPT_NAME).read_bytes() == text.encode("utf-8"), "--write receipt bytes")
        expect((out / HASH_NAME).read_text(encoding="ascii") == f"{digest}  {RECEIPT_NAME}\n",
               "--write hash file is sha256sum -c format")
        expect(_run("--check", "--log", str(gate), *common) == 0, "bootstrap --check exit 0")
        expect(not any(known.iterdir()), "--check wrote into the known-good directory")
        for name in (RECEIPT_NAME, HASH_NAME):
            shutil.copy(out / name, known / name)
        expect(_run("--check", "--log", str(gate), *common) == 0, "matching --check exit 0")
        expect(_run("--check", "--log", str(bad_gate), *common) == 1, "mismatching --check exit 1")
        expect(_run("--write", "--check", "--log", str(bad_gate), "--out", str(out), *common) == 1,
               "--write --check on a mismatch exits 1")
        expect((known / RECEIPT_NAME).read_bytes() == text.encode("utf-8")
               and (out / RECEIPT_NAME).read_bytes() != text.encode("utf-8"),
               "--write --check: run receipt in --out, known-good untouched")
        expect(_run("--write", "--check", "--log", str(gate), "--out", str(known), *common) == 2,
               "--out equal to the known-good directory is refused with --check")
        verdict, code, _, report = check_receipt(mutated_text.encode(), known)
        expect((verdict, code) == ("diverged", 1)
               and any(ln.startswith("+axioms: Alpha.lean 'Demo.one''") for ln in report),
               "a divergence report carries a unified diff")
        gate.write_text(log.replace("RESULT: PASS", "RESULT: FAIL"), encoding="utf-8")
        expect(_run("--check", "--log", str(gate), *common) == 2, "refused log exits 2")
        expect(_run("--check", "--log", str(root / "absent.log"), *common) == 2, "missing log exits 2")
        gate.write_text(log, encoding="utf-8")
        (known / HASH_NAME).write_text(digest.upper() + "\n", encoding="ascii")
        expect(_run("--check", "--log", str(gate), *common) == 0, "bare upper-case hash line matches")
        (known / RECEIPT_NAME).write_text(text + "tampered\n", encoding="utf-8")
        expect(_run("--check", "--log", str(gate), *common) == 2, "inconsistent known pair exits 2")
        (known / RECEIPT_NAME).unlink()
        (known / HASH_NAME).write_text("0" * 64 + f"  {RECEIPT_NAME}\n", encoding="ascii")
        expect(_run("--check", "--log", str(gate), *common) == 1, "hash-only known-good mismatch exits 1")
        (known / HASH_NAME).write_text("not-a-hash\n", encoding="ascii")
        expect(_run("--check", "--log", str(gate), *common) == 2, "malformed known hash exits 2")
        expect(_run("--log", str(gate), *common) == 2, "no mode is a usage error")
        expect(_run("--write", "--log", str(gate), *common) == 2, "--write without --out is a usage error")

    if failures:
        print("lean_receipt self-test: FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("lean_receipt self-test: PASS (parser, determinism, fail-closed refusals, "
          "--write/--check exit codes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
