#!/usr/bin/env python3
"""Pillar IV under memory: Caputo-fractional GKSL  D_t^alpha rho = L rho,  0 < alpha <= 1.

Model (matches Res-Nova PillarIV_AntiDriftGate.lean): H = u sigma_x, jump sqrt(gamma) sigma_-,
Markov steady coherence 2|rho01| = 4x/(1+8x^2), x = u/gamma, max 1/sqrt2 at x = 1/(2 sqrt2).
Solver: L1 scheme for the Caputo derivative (implicit), rho(0) = |g><g|.
Reports the long-time coherence (does the ceiling move with memory?) and the late-time
relaxation exponent (Markov: exponential; memory: algebraic ~ t^-alpha expected).
"""
import numpy as np
from math import gamma as Gf, sqrt

sx = np.array([[0, 1], [1, 0]], complex)
sm = np.array([[0, 1], [0, 0]], complex)  # |g><e| with basis (g, e): lowers e->g


def liouvillian(u, g):
    H = u * sx
    I = np.eye(2)
    L = -1j * (np.kron(H, I) - np.kron(I, H.T))
    L += g * (np.kron(sm, sm.conj()) - 0.5 * np.kron(sm.conj().T @ sm, I) - 0.5 * np.kron(I, (sm.conj().T @ sm).T))
    return L  # acts on row-major vec(rho)


def coh(v):
    return 2 * abs(v.reshape(2, 2)[0, 1])


def evolve(L, alpha, T, N):
    h = T / N
    rho0 = np.zeros(4, complex); rho0[0] = 1.0     # ground state g = index 0
    j = np.arange(N + 1)
    b = (j + 1) ** (1 - alpha) - j ** (1 - alpha)   # L1 weights
    c = h ** alpha * Gf(2 - alpha)
    A = np.eye(4) - c * L
    Ainv = np.linalg.inv(A)
    hist = [rho0]
    diffs = np.zeros((N, 4), complex)  # row k-1 = rho_k - rho_{k-1}
    out_t, out_c = [], []
    for n in range(1, N + 1):
        # sum_{k=1}^{n-1} b_{n-k} (rho_k - rho_{k-1})
        mem = b[n - 1:0:-1] @ diffs[: n - 1] if n > 1 else np.zeros(4, complex)
        rhs = hist[-1] - mem
        new = Ainv @ rhs
        diffs[n - 1] = new - hist[-1]; hist = [new]
        if n % max(1, N // 200) == 0:
            out_t.append(n * h); out_c.append(coh(new))
    return np.array(out_t), np.array(out_c), hist[-1]


def kernel_state(L):
    w, V = np.linalg.eig(L)
    v = V[:, np.argmin(abs(w))]
    v = v / (v[0] + v[3])
    return v


def main():
    theta = 1 / sqrt(2)
    g = 1.0
    print(f"{'x=u/g':>8} {'alpha':>6} {'coh(T)':>9} {'ker-L coh':>9} {'4x/(1+8x2)':>10} {'max transient':>13} {'late slope dlog|err|/dlog t':>28}")
    for x in [1 / (2 * sqrt(2)), 1.0]:
        L = liouvillian(x * g, g)
        ks = kernel_state(L)
        for alpha in [1.0, 0.9, 0.7, 0.5]:
            T, N = 60.0, 3000
            t, cc, last = evolve(L, alpha, T, N)
            err = np.abs(cc - coh(ks)) + 1e-300
            m = t > T / 3
            slope = np.polyfit(np.log(t[m]), np.log(err[m]), 1)[0]
            print(f"{x:8.4f} {alpha:6.2f} {coh(last):9.5f} {coh(ks):9.5f} {4*x/(1+8*x*x):10.5f} {cc.max():13.5f} {slope:28.2f}")
    print(f"theta = {theta:.5f}")


if __name__ == "__main__":
    main()
