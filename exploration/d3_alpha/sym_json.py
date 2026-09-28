"""Safe JSON serialization for the sympy expressions the D7 wind scripts exchange (operator matrices, residual rows).
Only an allowlist of node types is encoded or decoded (Symbol with its real/positive flags, Integer, Rational,
ImaginaryUnit, Add, Mul, Pow), so loading never evaluates code or unpickles objects."""

import json
import sympy as sp


def _sym(name, flags):
    return sp.Symbol(name, **{k: True for k in flags})


def enc(e):
    e = sp.sympify(e)
    if e.is_Symbol:
        flags = [f for f in ("positive", "real") if e.assumptions0.get(f)]
        return ["S", e.name, flags[:1] if "positive" in flags else flags]
    if e is sp.I:
        return ["i"]
    if e.is_Integer:
        return ["Z", int(e)]
    if e.is_Rational:
        return ["Q", int(e.p), int(e.q)]
    if isinstance(e, sp.Add):
        return ["+", [enc(a) for a in e.args]]
    if isinstance(e, sp.Mul):
        return ["*", [enc(a) for a in e.args]]
    if isinstance(e, sp.Pow):
        return ["^", enc(e.base), enc(e.exp)]
    raise TypeError(f"sym_json: unsupported node {type(e).__name__}: {e}")


def dec(n):
    tag = n[0]
    if tag == "S":
        return _sym(n[1], n[2])
    if tag == "i":
        return sp.I
    if tag == "Z":
        return sp.Integer(n[1])
    if tag == "Q":
        return sp.Rational(n[1], n[2])
    if tag == "+":
        return sp.Add(*[dec(a) for a in n[1]])
    if tag == "*":
        return sp.Mul(*[dec(a) for a in n[1]])
    if tag == "^":
        return sp.Pow(dec(n[1]), dec(n[2]))
    raise ValueError(f"sym_json: unknown tag {tag!r}")


def dump_matrix(path, M, names, params, consts):
    json.dump(
        {
            "matrix": [[enc(M[i, j]) for j in range(M.cols)] for i in range(M.rows)],
            "names": list(names),
            "params": [enc(p) for p in params],
            "consts": [enc(c) for c in consts],
        },
        open(path, "w"),
    )


def load_matrix(path):
    d = json.load(open(path))
    M = sp.Matrix([[dec(c) for c in row] for row in d["matrix"]])
    return (
        M,
        d["names"],
        tuple(dec(p) for p in d["params"]),
        tuple(dec(c) for c in d["consts"]),
    )


def dump_residuals(path, case, builder, symbols):
    json.dump(
        {
            "case": case,
            "builder": {k: enc(v) for k, v in builder.items()},
            "symbols": [enc(s) for s in symbols],
        },
        open(path, "w"),
    )


def load_residuals(path):
    d = json.load(open(path))
    return {
        "case": d["case"],
        "builder": {k: dec(v) for k, v in d["builder"].items()},
        "symbols": tuple(dec(s) for s in d["symbols"]),
    }
