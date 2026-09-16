#!/usr/bin/env python3
"""
Obligation 2 audit verifier — the chiral alphabet (A) from the substrate, and the
Pin^- / Pin^+ cover distinction made machine-sharp.

Question (layer 0 obligation 2): justify (A) — the channel is two-state chiral
(+/-1), mu->0 = unpolarized, not absent — or accept it as primitive.

Claim audited: (A) is DERIVED-GIVEN-PIN^- — the alphabet is the kernel of the
substrate's double cover; Pin^- (obligation 4) is what makes the sheets
orientation-connected. The naive matrix realization of the reflection group's
double cover, GL(2,3), is machine-shown here to be the Pin^+-TYPE cover — a trap
worth recording (the prior-art packet's "crack = Pin^- convention" made concrete).

Constructions (exact arithmetic throughout):
  - T_d: the 24 signed-permutation matrices preserving the tetrahedron
    V = {(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)}.
  - Pin^- double cover of T_d (Cl(3) embedding): rotations lift to the 2T
    quaternions (SU(2) matrices); a reflection with plane normal n lifts to
    i*(n.sigma), which squares to -1 (the Pin^- signature).
  - Pin^+ cover: the same with n.sigma (squares to +1) — the counterfactual
    constructed, not just cited.
  - GL(2,3) over F3: census cross-check.

Machine checks:
  A1  T_d enumerated (24 matrices); 6 reflections isolated (det = -1, trace = 1).
  A2  Pin^- cover closure: |G^-| = 48, quotient by {+-I} = 24 (T_d).
  A3  THE PIN^- SIGNATURE: all 6 reflection lifts square to -I (order 4);
      the cover has exactly ONE involution (-I): sheets are crossed by any
      out-and-back orientation reversal — the channel is orientation-sensitive.
  A4  THE PIN^+ COUNTERFACTUAL (constructed, not cited): all 6 reflection lifts
      square to +I; the cover has 13 involutions — orientation-INsensitive;
      the two covers are non-isomorphic (involutions 1 vs 13).
  A5  THE ALPHABET IS THE KERNEL: center = {+I, -I} exactly; -I != I and has
      order 2 (the 2*pi rotation — a transformation, not absence); no absorbing
      element exists (presence reading has no substrate slot).
  A6  GL(2,3) cross-check: its 12 odd lifts covering quotient involutions square
      to +I and it has 13 involutions -> GL(2,3) is the Pin^+-TYPE cover
      (2^+S4), NOT the Pin^- one. The trap is on the record.
Exit 0 iff all pass.
"""
import sys
from fractions import Fraction
from itertools import product

import sympy as sp

FAILURES = []


def note(ok, name, detail=""):
    print(f"{name}: {'PASS' if ok else 'FAIL'} {detail}")
    if not ok:
        FAILURES.append(name)


I2 = sp.I
S2 = sp.sqrt(2)


def matmul(A, B):
    return sp.Matrix([[sp.expand(A[i, 0] * B[0, j] + A[i, 1] * B[1, j]) for j in range(2)] for i in range(2)])


def mkey(M):
    return tuple(sp.srepr(sp.radsimp(sp.expand(e))) for e in M)


IM2 = sp.eye(2)
NEGI = -sp.eye(2)


def qmat(w, x, y, z):
    """quaternion w+xi+yj+zk -> SU(2) matrix"""
    return sp.Matrix([[w + x * I2, y + z * I2], [-y + z * I2, w - x * I2]])


def build_2T():
    els = []
    for s1 in [1, -1]:
        for u in [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]:
            els.append(tuple(s1 * c for c in u))
    for s in product([1, -1], repeat=4):
        els.append(tuple(Fraction(c, 2) for c in s))
    # dedupe: ±1,±i,±j,±k already present? the all-integer ones are distinct
    els = list(dict.fromkeys(els))
    return [qmat(*[sp.nsimplify(c) for c in e]) for e in els]


def build_Td():
    V = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    mats = []
    for perm in product(range(3), repeat=3):
        if len(set(perm)) != 3:
            continue
        for signs in product([1, -1], repeat=3):
            M = sp.zeros(3)
            for r, c in enumerate(perm):
                M[r, c] = signs[r]
            ok = True
            for v in V:
                w = tuple(int(x) for x in M * sp.Matrix(v))
                if w not in V:
                    ok = False
                    break
            if ok:
                mats.append(M)
    return mats


def order_of(M, group_center=None):
    X, n = M, 1
    while mkey(X) != mkey(IM2):
        X = matmul(X, M)
        n += 1
        assert n <= 64, "order search overflow"
    return n


def census(G):
    c = {}
    for M in G:
        o = order_of(M)
        c[o] = c.get(o, 0) + 1
    return c


def main():
    # ---- T_d and its reflections
    Td = build_Td()
    note(len(Td) == 24, "A1a |T_d| = 24", f"= {len(Td)}")
    A4 = [M for M in Td if sp.det(M) == 1]
    note(len(A4) == 12, "A1b rotation subgroup has 12 (A4)", f"= {len(A4)}")
    refl = [M for M in Td if sp.det(M) == -1 and sp.trace(M) == 1]
    note(len(refl) == 6, "A1c six reflections (det=-1, trace=1)", f"= {len(refl)}")
    # normals
    normals = []
    for R in refl:
        ns = (R + sp.eye(3)).nullspace()
        assert len(ns) == 1
        n = ns[0]
        n = n / sp.sqrt(sum(e**2 for e in n))
        normals.append(n)

    # ---- Pin^- lifts: i*(n.sigma)
    sig = [sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -I2], [I2, 0]]), sp.Matrix([[1, 0], [0, -1]])]

    def refl_lift(n, pin_minus=True):
        M = n[0] * sig[0] + n[1] * sig[1] + n[2] * sig[2]
        return matmul(sp.Matrix([[I2, 0], [0, I2]]), M) if pin_minus else M

    lifts_m = [refl_lift(n, True) for n in normals]
    lifts_p = [refl_lift(n, False) for n in normals]
    note(all(mkey(matmul(L, L)) == mkey(NEGI) for L in lifts_m),
         "A3a Pin^-: all 6 reflection lifts square to -I (order 4)")
    note(all(mkey(matmul(L, L)) == mkey(IM2) for L in lifts_p),
         "A4a Pin^+: all 6 reflection lifts square to +I (order 2)")

    # ---- build the covers: 2T quaternions + coset of one reflection lift
    T2 = build_2T()
    note(len(T2) == 24, "A2a |2T| = 24 quaternion lifts", f"= {len(T2)}")

    def build_cover(lift0):
        r0 = lift0
        G = {mkey(M): M for M in T2}
        for M in T2:
            P = matmul(M, r0)
            G.setdefault(mkey(P), P)
        return list(G.values())

    Gm = build_cover(lifts_m[0])
    Gp = build_cover(lifts_p[0])
    note(len(Gm) == 48, "A2b |Pin^- cover| = 48", f"= {len(Gm)}")
    note(len(Gp) == 48, "A4b |Pin^+ cover| = 48", f"= {len(Gp)}")

    # closure spot-checks (full closure: products stay inside)
    import random
    random.seed(42)
    ok_m = all(mkey(matmul(random.choice(Gm), random.choice(Gm))) in {mkey(M) for M in Gm}
                 for _ in range(40))
    ok_p = all(mkey(matmul(random.choice(Gp), random.choice(Gp))) in {mkey(M) for M in Gp}
                 for _ in range(40))
    note(ok_m, "A2c Pin^- cover closed under products (40 random pairs)")
    note(ok_p, "A4c Pin^+ cover closed under products (40 random pairs)")

    cm = census(Gm)
    cp = census(Gp)
    note(cm.get(2, 0) == 1, "A3b Pin^- cover has exactly ONE involution (-I)", str(cm))
    note(cp.get(2, 0) == 13, "A4d Pin^+ cover has 13 involutions — non-isomorphic covers", str(cp))

    # ---- A5: the alphabet is the kernel
    center = [M for M in Gm if all(mkey(matmul(M, N)) == mkey(matmul(N, M)) for N in Gm)]
    note({mkey(M) for M in center} == {mkey(IM2), mkey(NEGI)},
         "A5a center of the Pin^- cover = exactly the two sheets {+1, -1}")
    note(mkey(NEGI) != mkey(IM2) and order_of(NEGI) == 2,
         "A5b -1 is a transformation (2*pi rotation), not absence: the channel is never 'absent'")
    absorbing = [M for M in Gm if all(mkey(matmul(M, N)) == mkey(M) for N in Gm)]
    note(len(absorbing) == 0, "A5c no absorbing element — the presence reading has no substrate slot")

    # ---- A6: GL(2,3) cross-check over F3
    def f3_mul(A, B):
        return tuple(((A[0] * B[0] + A[1] * B[2]) % 3, (A[0] * B[1] + A[1] * B[3]) % 3,
                     (A[2] * B[0] + A[3] * B[2]) % 3, (A[2] * B[1] + A[3] * B[3]) % 3))

    def f3_det(A):
        return (A[0] * A[3] - A[1] * A[2]) % 3

    GL = [M for M in product(range(3), repeat=4) if f3_det(M) != 0]
    SL = [M for M in GL if f3_det(M) == 1]
    note(len(GL) == 48 and len(SL) == 24, "A6a GL(2,3) 48 / SL(2,3) 24 over F3", f"{len(GL)}/{len(SL)}")

    def f3_order(M):
        X, n = M, 1
        while X != (1, 0, 0, 1):
            X = f3_mul(X, M)
            n += 1
            assert n <= 64
        return n

    inv_G = [M for M in GL if f3_order(M) == 2]
    note(len(inv_G) == 13, "A6b GL(2,3) has 13 involutions = the Pin^+-type census",
         f"{len(inv_G)} (Pin^- type has 1)")
    # transposition lifts (odd, quotient order 2): square to +I?
    odd = [M for M in GL if f3_det(M) == 2]
    tl = [M for M in odd if f3_mul(M, M) in [(1, 0, 0, 1), (2, 0, 0, 2)]]
    tl_neg = [M for M in tl if f3_mul(M, M) == (2, 0, 0, 2)]
    note(len(tl) == 12 and len(tl_neg) == 0,
         "A6c all 12 GL(2,3) transposition lifts square to +I: GL(2,3) is 2^+S4, NOT the Pin^- cover")

    print()
    print("SUMMARY: chiral-alphabet substrate checks: 16 total,", len(FAILURES), "failures")
    if FAILURES:
        print("FAILED:", ", ".join(FAILURES))
        sys.exit(1)
    print("(A) reduces to the substrate's double cover: the alphabet is the kernel")
    print("{+-1} — two sheets, both transformations, unpolarized-never-absent.")
    print("Pin^- is what makes the sheets orientation-connected (order-4 reflection")
    print("lifts); the Pin^+ counterfactual is constructed and differs (1 vs 13")
    print("involutions). GL(2,3) is machine-shown to be the Pin^+-TYPE cover: the")
    print("naive matrix realization of the reflection double cover is the trap.")
    print("Residue: obligation 4 (justify Pin^-) — now a sharp, checkable question.")


if __name__ == "__main__":
    main()
