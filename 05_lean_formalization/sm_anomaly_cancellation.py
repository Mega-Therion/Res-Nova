#!/usr/bin/env python3
"""
Standard Model Chiral Gauge & Gravitational Anomaly Cancellation Audit
(/home/mega/Chyren/3_research/Res-Nova/05_lean_formalization/sm_anomaly_cancellation.py).

Computes all five 4D perturbative triangle anomaly sums (SU(3)^3, SU(3)^2 U(1),
SU(2)^2 U(1), U(1)^3, gravity^2 U(1)) in exact SymPy Rational arithmetic (zero floats)
plus the global Witten SU(2) doublet count for left-handed Weyl fermions, runs the
two required negative controls, and audits Res-Nova and 4Leibniz for any non-textbook
5-fermion rational hypercharge assignment.

Exit 0 means the script finished. Vanishing of the textbook SM sums is a consistency
check of the imported SM representation content, NOT a geometric derivation
(derived_from_geometry = false).
"""

import copy
import json
import os
import pathlib
import re
import sys
import sympy as sp


TEXTBOOK_GENERATION = [
    {"field": "q",  "su3": "3",     "n_weak": sp.Integer(2), "Y": sp.Rational(1, 6)},
    {"field": "uc", "su3": "3-bar", "n_weak": sp.Integer(1), "Y": sp.Rational(-2, 3)},
    {"field": "dc", "su3": "3-bar", "n_weak": sp.Integer(1), "Y": sp.Rational(1, 3)},
    {"field": "l",  "su3": "1",     "n_weak": sp.Integer(2), "Y": sp.Rational(-1, 2)},
    {"field": "ec", "su3": "1",     "n_weak": sp.Integer(1), "Y": sp.Rational(1, 1)},
]


def color_multiplicity(su3_rep: str) -> sp.Integer:
    if su3_rep in ("3", "3-bar"):
        return sp.Integer(3)
    if su3_rep == "1":
        return sp.Integer(1)
    raise ValueError(f"Unsupported SU(3) representation: {su3_rep}")


def su3_dynkin_index(su3_rep: str) -> sp.Rational:
    if su3_rep in ("3", "3-bar"):
        return sp.Rational(1, 2)
    if su3_rep == "1":
        return sp.Rational(0, 1)
    raise ValueError(f"Unsupported SU(3) representation: {su3_rep}")


def su3_cubic_coeff(su3_rep: str) -> sp.Integer:
    if su3_rep == "3":
        return sp.Integer(1)
    if su3_rep == "3-bar":
        return sp.Integer(-1)
    if su3_rep == "1":
        return sp.Integer(0)
    raise ValueError(f"Unsupported SU(3) representation: {su3_rep}")


def compute_six_checks(fermions: list[dict]) -> dict:
    """Compute the 5 continuous rational anomaly sums and the integer Witten SU(2) count."""
    su3_cubic_terms = []
    su3_sq_u1_terms = []
    su2_sq_u1_terms = []
    u1_cubic_terms = []
    grav_sq_u1_terms = []
    witten_terms = []

    for f in fermions:
        name = f["field"]
        su3_rep = f["su3"]
        n_weak = sp.Integer(f["n_weak"])
        Y = sp.Rational(f["Y"])
        assert isinstance(Y, sp.Rational) and not isinstance(Y, sp.Float)

        n_col = color_multiplicity(su3_rep)
        n_total = n_col * n_weak

        # 1. SU(3)^3: n(3) - n(3-bar), where a weak doublet counts as two triplets
        t_su3_3 = su3_cubic_coeff(su3_rep) * n_weak
        su3_cubic_terms.append({"field": name, "term": t_su3_3})

        # 2. SU(3)^2 U(1): sum Y * T(R) * n_weak, T(3) = T(3-bar) = 1/2 (color counted by T(R))
        t_su3_2_u1 = Y * su3_dynkin_index(su3_rep) * n_weak
        su3_sq_u1_terms.append({"field": name, "term": t_su3_2_u1})

        # 3. SU(2)^2 U(1): sum Y over doublets, times color multiplicity (do not count doublet twice)
        t_su2_2_u1 = (n_col * Y) if (n_weak == 2) else sp.Integer(0)
        su2_sq_u1_terms.append({"field": name, "term": t_su2_2_u1})

        # 4. U(1)^3: sum n * Y^3
        t_u1_3 = n_total * (Y**3)
        u1_cubic_terms.append({"field": name, "term": t_u1_3})

        # 5. gravity^2 U(1): sum n * Y
        t_grav_2_u1 = n_total * Y
        grav_sq_u1_terms.append({"field": name, "term": t_grav_2_u1})

        # 6. Witten SU(2): number of doublets, counting 3 colors as 3 doublets
        t_witten = int(n_col) if (n_weak == 2) else 0
        witten_terms.append({"field": name, "doublets": t_witten})

    continuous_specs = [
        ("SU(3)^3", su3_cubic_terms),
        ("SU(3)^2 U(1)", su3_sq_u1_terms),
        ("SU(2)^2 U(1)", su2_sq_u1_terms),
        ("U(1)^3", u1_cubic_terms),
        ("gravity^2 U(1)", grav_sq_u1_terms),
    ]

    sums_out = []
    all_continuous_zero = True
    for check_name, term_entries in continuous_specs:
        tot = sum((entry["term"] for entry in term_entries), sp.Integer(0))
        assert isinstance(tot, sp.Rational)
        if tot != 0:
            all_continuous_zero = False
        sums_out.append(
            {
                "name": check_name,
                "kind": "continuous_anomaly_sum",
                "term_list": [
                    {"field": entry["field"], "value": str(entry["term"])}
                    for entry in term_entries
                ],
                "total": str(tot),
                "total_exact_zero": bool(tot == 0),
            }
        )

    witten_total = sum(entry["doublets"] for entry in witten_terms)
    witten_even = (witten_total % 2 == 0)

    sums_out.append(
        {
            "name": "Witten SU(2)",
            "kind": "global_su2_doublet_parity_count",
            "term_list": [
                {"field": entry["field"], "value": entry["doublets"]}
                for entry in witten_terms
            ],
            "total": witten_total,
            "is_even": witten_even,
        }
    )

    return {
        "sums": sums_out,
        "all_continuous_zero": all_continuous_zero,
        "witten_doublet_count": {
            "count": witten_total,
            "is_even": witten_even,
        },
    }


def print_check_report(label: str, result: dict) -> None:
    print(f"=== {label} ===")
    for item in result["sums"]:
        terms_str = ", ".join(f"{t['field']}: {t['value']}" for t in item["term_list"])
        if item["kind"] == "continuous_anomaly_sum":
            print(f"  {item['name']:15s} | terms: [{terms_str}] | total = {item['total']}")
        else:
            print(
                f"  {item['name']:15s} | terms: [{terms_str}] | "
                f"count = {item['total']} (even = {item['is_even']})"
            )


def search_corpus_for_hypercharge_proposal(self_path: pathlib.Path) -> dict | None:
    """
    Search Res-Nova and 4Leibniz for any non-textbook hypercharge assignment
    attaching five rational hypercharges to named SM Weyl fermions.
    """
    roots = [
        pathlib.Path("/home/mega/Chyren/3_research/Res-Nova"),
        pathlib.Path("/home/mega/Chyren/3_research/4Leibniz"),
    ]
    skip_dirs = {".git", ".lake", "node_modules", ".claude", "_src", "__pycache__"}
    allowed_suffixes = {".md", ".tex", ".lean", ".py", ".json", ".yaml", ".yml", ".txt"}
    hc_pattern = re.compile(r"\bhypercharge\b|\bU\(1\)_Y\b", re.IGNORECASE)

    candidate_files = []
    self_json = self_path.with_suffix(".json")
    for root in roots:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]
            for fname in filenames:
                path = pathlib.Path(dirpath) / fname
                if path.suffix.lower() not in allowed_suffixes:
                    continue
                resolved = path.resolve()
                if resolved == self_path or resolved == self_json:
                    continue
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                if hc_pattern.search(text):
                    candidate_files.append(str(path))

    # Inspect any candidate file for a 5-fermion rational hypercharge table distinct from textbook.
    assign_pat = re.compile(
        r"\b(q|uc|u_R|dc|d_R|l|ec|e_R)\b[^\n]{0,60}?([+-]?\d+(?:\s*/\s*\d+)?)"
    )
    textbook_map = {
        "q": sp.Rational(1, 6),
        "uc": sp.Rational(-2, 3),
        "dc": sp.Rational(1, 3),
        "l": sp.Rational(-1, 2),
        "ec": sp.Rational(1, 1),
    }
    alias_map = {
        "q": "q",
        "uc": "uc",
        "u_R": "uc",
        "dc": "dc",
        "d_R": "dc",
        "l": "l",
        "ec": "ec",
        "e_R": "ec",
    }
    for cand in candidate_files:
        text = pathlib.Path(cand).read_text(encoding="utf-8", errors="ignore")
        found: dict[str, sp.Rational] = {}
        for raw_name, raw_rat in assign_pat.findall(text):
            canon = alias_map[raw_name]
            val = sp.Rational(raw_rat.replace(" ", ""))
            if raw_name in ("u_R", "d_R", "e_R"):
                val = -val
            found[canon] = val
        if set(found.keys()) == {"q", "uc", "dc", "l", "ec"} and found != textbook_map:
            return {
                "source_file": cand,
                "hypercharges": {k: str(found[k]) for k in ("q", "uc", "dc", "l", "ec")},
                "fermions": [
                    {**f, "Y": found[f["field"]]} for f in TEXTBOOK_GENERATION
                ],
            }
    return None


def main() -> int:
    self_path = pathlib.Path(__file__).resolve()

    # =========================================================================
    # 1. POSITIVE CONTROL: TEXTBOOK ONE-GENERATION LEFT-HANDED WEYL ASSIGNMENT
    # =========================================================================
    active_fermions = copy.deepcopy(TEXTBOOK_GENERATION)
    pos_result = compute_six_checks(active_fermions)
    print_check_report("Positive Control (1 generation, textbook SM)", pos_result)

    if (not pos_result["all_continuous_zero"]) or (
        pos_result["witten_doublet_count"]["count"] != 4
    ):
        verdict = "textbook assignment does not cancel"
        print(f"verdict: {verdict}")
        receipt = {
            "verdict": verdict,
            "sums": pos_result["sums"],
            "witten_doublet_count": pos_result["witten_doublet_count"],
            "negative_controls": [],
            "corpus_proposal": None,
            "derived_from_geometry": False,
        }
        self_path.with_suffix(".json").write_text(
            json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
        )
        return 0

    # Three identical generations note (exact rational scaling by N_gen = 3):
    n_gen = sp.Integer(3)
    three_gen_note = (
        "Three identical generations multiply every continuous anomaly sum by 3 "
        "(so 3 * 0 = 0) and multiply the Witten SU(2) doublet count by 3 "
        f"(3 * {pos_result['witten_doublet_count']['count']} = "
        f"{int(n_gen * pos_result['witten_doublet_count']['count'])}, even)."
    )
    print(three_gen_note)

    # =========================================================================
    # 2. NEGATIVE CONTROLS (ONE CHANGE AT A TIME, THEN RESTORE TEXTBOOK)
    # =========================================================================
    negative_controls_out = []

    # Negative Control A: ec hypercharge 1 replaced by 2
    mod_ec = copy.deepcopy(active_fermions)
    for entry in mod_ec:
        if entry["field"] == "ec":
            entry["Y"] = sp.Rational(2, 1)
    neg_ec_res = compute_six_checks(mod_ec)
    print_check_report("Negative Control 1 (ec hypercharge 1 -> 2)", neg_ec_res)
    if neg_ec_res["all_continuous_zero"]:
        sys.stderr.write("BUG: Negative control 1 (ec Y=2) gave all zero continuous sums.\n")
        return 1
    negative_controls_out.append(
        {
            "modification": "ec hypercharge 1 replaced by 2",
            "all_continuous_zero": neg_ec_res["all_continuous_zero"],
            "failed_continuous_sums": [
                {"name": s["name"], "total": s["total"]}
                for s in neg_ec_res["sums"]
                if s["kind"] == "continuous_anomaly_sum" and not s["total_exact_zero"]
            ],
            "sums": neg_ec_res["sums"],
            "witten_doublet_count": neg_ec_res["witten_doublet_count"],
        }
    )

    # Restore textbook assignment and verify restoration
    assert active_fermions == TEXTBOOK_GENERATION

    # Negative Control B: lepton doublet l removed
    mod_no_l = [copy.deepcopy(f) for f in active_fermions if f["field"] != "l"]
    neg_no_l_res = compute_six_checks(mod_no_l)
    print_check_report("Negative Control 2 (lepton doublet l removed)", neg_no_l_res)
    if neg_no_l_res["all_continuous_zero"]:
        sys.stderr.write("BUG: Negative control 2 (remove l) gave all zero continuous sums.\n")
        return 1
    negative_controls_out.append(
        {
            "modification": "lepton doublet removed",
            "all_continuous_zero": neg_no_l_res["all_continuous_zero"],
            "failed_continuous_sums": [
                {"name": s["name"], "total": s["total"]}
                for s in neg_no_l_res["sums"]
                if s["kind"] == "continuous_anomaly_sum" and not s["total_exact_zero"]
            ],
            "sums": neg_no_l_res["sums"],
            "witten_doublet_count": neg_no_l_res["witten_doublet_count"],
        }
    )

    # Confirm textbook assignment remains restored
    restored_res = compute_six_checks(active_fermions)
    assert restored_res["all_continuous_zero"] is True
    assert restored_res["witten_doublet_count"]["count"] == 4

    # =========================================================================
    # 3. CORPUS SEARCH ACROSS Res-Nova AND 4Leibniz
    # =========================================================================
    corpus_raw = search_corpus_for_hypercharge_proposal(self_path)
    if corpus_raw is None:
        corpus_proposal = None
        verdict = "textbook assignment cancels"
    else:
        corpus_eval = compute_six_checks(corpus_raw["fermions"])
        print_check_report(f"Corpus Proposal ({corpus_raw['source_file']})", corpus_eval)
        corpus_proposal = {
            "source_file": corpus_raw["source_file"],
            "hypercharges": corpus_raw["hypercharges"],
            "sums": corpus_eval["sums"],
            "witten_doublet_count": corpus_eval["witten_doublet_count"],
        }
        if (
            corpus_eval["all_continuous_zero"]
            and corpus_eval["witten_doublet_count"]["is_even"]
        ):
            verdict = "corpus proposal cancels"
        else:
            verdict = "corpus proposal does not cancel"

    print(f"corpus_proposal: {json.dumps(corpus_proposal)}")
    derived_from_geometry = False
    print(f"derived_from_geometry: {json.dumps(derived_from_geometry)}")
    print(f"verdict: {verdict}")

    receipt = {
        "verdict": verdict,
        "three_generations_scaling_note": three_gen_note,
        "sums": pos_result["sums"],
        "witten_doublet_count": pos_result["witten_doublet_count"],
        "negative_controls": negative_controls_out,
        "corpus_proposal": corpus_proposal,
        "derived_from_geometry": derived_from_geometry,
    }

    self_path.with_suffix(".json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
