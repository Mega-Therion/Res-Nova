#!/usr/bin/env python3
"""Render manuscript tables from assurance/claims.json, so the paper cannot drift from the registry.

  python3 scripts/registry_to_tables.py [--ids CLM-A,CLM-B,...] [--format md|tex] [--table status|tests]

status: claim | basis (artifacts) | evidence (independent witness) | state | limitation
tests:  claim | falsification test | scope | result | state
Default ids: the critical-assessment set (galaxy, a0, solar system, branch, dwarfs, spin)."""
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ["CLM-D9-02", "CLM-D7-07", "CLM-Z-01", "CLM-Z-02", "CLM-O1-01", "CLM-Z-03",
           "CLM-D3-10", "CLM-D7-08", "CLM-Z-04", "CLM-Z-05", "CLM-11", "CLM-Z-06"]


def rows(ids, table):
    claims = {c["id"]: c for c in json.loads((ROOT / "assurance/claims.json").read_text())["claims"]}
    missing = [i for i in ids if i not in claims]
    if missing:
        sys.exit(f"unknown claim id(s): {', '.join(missing)}")
    out = []
    for i in ids:
        c = claims[i]
        if table == "status":
            basis = "; ".join(c["formal_artifacts"] + c["computational_artifacts"] + c["data_artifacts"]) or "-"
            out.append([i, c["wording"], basis, c["independent_witness"], c["state"], c["limitations"]])
        else:
            f = c["falsifiability"]
            out.append([i, c["wording"], f.get("test") or "not specified", f.get("scope") or "-", f["result"], c["state"]])
    return out


HEAD = {"status": ["ID", "Claim", "Basis", "Evidence", "State", "Limitation"],
        "tests": ["ID", "Claim", "Falsification test", "Scope", "Result", "State"]}


TEX = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
       "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}


def tex_escape(s):
    return "".join(TEX.get(ch, ch) for ch in s)


def render(rs, table, fmt):
    h = HEAD[table]
    if fmt == "md":
        cell = lambda s: s.replace("|", "/").replace("\n", " ")
        return "\n".join(["| " + " | ".join(h) + " |", "|" + "---|" * len(h)] +
                         ["| " + " | ".join(cell(x) for x in r) + " |" for r in rs]) + "\n"
    spec = "l" + "p{3.2cm}" * (len(h) - 1)
    lines = [r"\begin{longtable}{" + spec + "}", " & ".join(r"\textbf{%s}" % x for x in h) + r" \\ \hline"]
    lines += [" & ".join(tex_escape(x) for x in r) + r" \\" for r in rs]
    return "\n".join(lines + [r"\end{longtable}"]) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", default=",".join(DEFAULT))
    ap.add_argument("--format", choices=["md", "tex"], default="md")
    ap.add_argument("--table", choices=["status", "tests"], default="status")
    a = ap.parse_args()
    sys.stdout.write(render(rows([i.strip() for i in a.ids.split(",") if i.strip()], a.table), a.table, a.format))


if __name__ == "__main__":
    main()
