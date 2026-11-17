"""Cross-check the E8 simple-root Gram matrix and Cartan-node ordering.

Lean proves the corresponding statements in StringTheoryBridge.lean. This script
uses exact SymPy integer matrices for the doubled-root Gram identity and NumPy
integer arrays for an independent permutation check. It is a consistency check,
not a proof of a root-space decomposition or a physical connection.
"""

from __future__ import annotations

import numpy as np
from sympy import Matrix

SIMPLE_ROOTS_DOUBLED = Matrix(
    [
        [2, -2, 0, 0, 0, 0, 0, 0],
        [0, 2, -2, 0, 0, 0, 0, 0],
        [0, 0, 2, -2, 0, 0, 0, 0],
        [0, 0, 0, 2, -2, 0, 0, 0],
        [0, 0, 0, 0, 2, -2, 0, 0],
        [0, 0, 0, 0, 0, 2, -2, 0],
        [0, 0, 0, 0, 0, 0, 2, 2],
        [-1, -1, -1, -1, -1, 1, 1, -1],
    ]
)

RESNOVA_CARTAN = Matrix(
    [
        [2, -1, 0, 0, 0, 0, 0, 0],
        [-1, 2, -1, 0, 0, 0, 0, 0],
        [0, -1, 2, -1, 0, 0, 0, 0],
        [0, 0, -1, 2, -1, 0, 0, 0],
        [0, 0, 0, -1, 2, -1, 0, -1],
        [0, 0, 0, 0, -1, 2, -1, 0],
        [0, 0, 0, 0, 0, -1, 2, 0],
        [0, 0, 0, 0, -1, 0, 0, 2],
    ]
)

MATHLIB_CARTAN_E8 = Matrix(
    [
        [2, 0, -1, 0, 0, 0, 0, 0],
        [0, 2, 0, -1, 0, 0, 0, 0],
        [-1, 0, 2, -1, 0, 0, 0, 0],
        [0, -1, -1, 2, -1, 0, 0, 0],
        [0, 0, 0, -1, 2, -1, 0, 0],
        [0, 0, 0, 0, -1, 2, -1, 0],
        [0, 0, 0, 0, 0, -1, 2, -1],
        [0, 0, 0, 0, 0, 0, -1, 2],
    ]
)

# Maps a Res-Nova simple-root index to the corresponding Mathlib matrix index.
RESNOVA_TO_MATHLIB = [7, 6, 5, 4, 3, 2, 0, 1]


def as_numpy_int64(matrix: Matrix) -> np.ndarray:
    """Convert a small exact integer matrix to a NumPy int64 array."""
    return np.asarray(
        [[int(value) for value in row] for row in matrix.tolist()], dtype=np.int64
    )


def main() -> None:
    gram = SIMPLE_ROOTS_DOUBLED * SIMPLE_ROOTS_DOUBLED.T
    assert gram == 4 * RESNOVA_CARTAN, "SymPy exact Gram-matrix identity failed"

    assert sorted(RESNOVA_TO_MATHLIB) == list(range(8)), "node map is not a permutation"
    reindexed_mathlib = MATHLIB_CARTAN_E8.extract(
        RESNOVA_TO_MATHLIB, RESNOVA_TO_MATHLIB
    )
    assert RESNOVA_CARTAN == reindexed_mathlib, "SymPy Cartan reindexing failed"

    resnova_np = as_numpy_int64(RESNOVA_CARTAN)
    mathlib_np = as_numpy_int64(MATHLIB_CARTAN_E8)
    assert np.array_equal(
        resnova_np,
        mathlib_np[np.ix_(RESNOVA_TO_MATHLIB, RESNOVA_TO_MATHLIB)],
    ), "NumPy integer Cartan reindexing failed"

    print("E8 Cartan bridge: PASS (exact SymPy Gram matrix; NumPy node reindexing)")


if __name__ == "__main__":
    main()
