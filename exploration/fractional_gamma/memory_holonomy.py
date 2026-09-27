#!/usr/bin/env python3
"""'Ant with memory': SU(2) parallel transport with a Caputo memory kernel.

Ordinary transport  dU/dt = -A(t) U  gives holonomy that is (i) unitary, (ii) independent of
how fast you walk the loop, (iii) multiplicative: Hol(a then b) = Hol(b) Hol(a).
Replace d/dt by the Caputo derivative D^alpha (the Riemann-Liouville memory kernel from the
fractional-calculus video). Measure what the ant can now detect that it couldn't before.

Loops on the flat torus (RY's donut): a = meridian, b = longitude, flat connection with
holonomies exp(-i th_a sz), exp(-i th_b sz) (flat torus connections are abelian).
"""
import numpy as np
from math import gamma as G

sz = np.array([[1, 0], [0, -1]], complex); sx = np.array([[0, 1], [1, 0]], complex)


def transport(segments, alpha, N=1500):
    """segments: list of (generator X, duration T, speed profile f on [0,1]) ; A(t) = i X * rate."""
    # build time grid and A(t)
    Ts, As = [], []
    t0 = 0.0
    for X, T, prof in segments:
        n = int(N * T)
        s = (np.arange(n) + 1) / n
        rate = prof(s)                       # d(arclength)/dt profile, integrates to 1 over the segment
        for si, ri in zip(s, rate):
            Ts.append(t0 + si * T); As.append(1j * X * ri)
        t0 += T
    h = Ts[1] - Ts[0]
    n = len(Ts); j = np.arange(n + 1)
    b = (j + 1) ** (1 - alpha) - j ** (1 - alpha); c = h**alpha * G(2 - alpha)
    U = np.eye(2, dtype=complex); diffs = np.zeros((n, 2, 2), complex)
    for k in range(1, n + 1):
        mem = np.tensordot(b[k - 1:0:-1], diffs[:k - 1], axes=1) if k > 1 else 0
        M = -As[k - 1]
        new = np.linalg.solve(np.eye(2) - c * M, U - mem)
        diffs[k - 1] = new - U; U = new
    return U


uni = lambda s: np.ones_like(s)
fast_slow = lambda s: np.where(s < 0.5, 1.6, 0.4)   # same loop, walked unevenly (still integrates to 1)
tha, thb = 0.9, 1.7
print(f"{'alpha':>6} {'unitarity':>10} {'reparam':>9} {'a.b vs b.a':>11} {'Hol(ab) vs Hol(b)Hol(a)':>24}")
for alpha in (1.0, 0.9, 0.7, 0.5):
    Ua = transport([(tha * sz, 1.0, uni)], alpha)
    Ub = transport([(thb * sz, 1.0, uni)], alpha)
    Uab = transport([(tha * sz, 1.0, uni), (thb * sz, 1.0, uni)], alpha)
    Uba = transport([(thb * sz, 1.0, uni), (tha * sz, 1.0, uni)], alpha)
    Ua2 = transport([(tha * sz, 1.0, fast_slow)], alpha)
    unit = np.linalg.norm(Ua.conj().T @ Ua - np.eye(2))
    rep = np.linalg.norm(Ua - Ua2)
    order = np.linalg.norm(Uab - Uba)
    hom = np.linalg.norm(Uab - Ub @ Ua)
    print(f"{alpha:6.2f} {unit:10.4f} {rep:9.4f} {order:11.4f} {hom:24.4f}")
