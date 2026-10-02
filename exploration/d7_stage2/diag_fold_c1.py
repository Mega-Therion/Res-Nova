"""Fold check along the stripped branch (16x32, g_e = 0.003 a0, box asinh(300)): the 30 eigenvalues of the equilibrated
Hessian nearest zero at each saved speed, keeping those that change with v (the speed-independent structural modes -
Omega and the paired omega/psi curl modes - filled the k = 6 list and hid any physical mode)."""
import math, numpy as np, scipy.sparse as sps, scipy.sparse.linalg as spla
import solve_c1 as C
vf = 10/299792.458; b = 3e-4; M = 12*math.pi*vf**4/C.A0T; g_e = 0.003*C.A0T
g = C.GridC1(16, 32, 1e-4, math.asinh(300.), math.asinh(300.))
rho = C.plummer_fn(M, b)
lab = {"W_R": "Om", "W_z": "om", "U_R": "Lam", "U_z": "psi", "F": "s"}
spec = {}
for v in (100, 50, 30, 25, 20):
    x = np.load(f"cache_branch/stripped_ge0.003_16x32_v{v}.npy")
    P = C.ProblemC1(g, v/299792.458, rho, g_e)
    _, H, _ = P.grad_hess(x)
    Sd = sps.diags(1/np.sqrt(np.asarray(abs(H).sum(axis=1)).ravel()))
    A = (Sd @ H @ Sd).tocsc(); A = (0.5*(A + A.T)).tocsc()
    ev, V = spla.eigsh(A, k=30, sigma=0, which="LM")
    rows = []
    for i in np.argsort(np.abs(ev)):
        fw = {}
        for n in C.NAMES:
            m = P.dm.index[C.FIX[n]]; fw[lab.get(n, n)] = float(np.linalg.norm(V[np.unique(m[m >= 0]), i])**2)
        top = max(fw, key=fw.get)
        rows.append((ev[i], top, fw[top]))
    spec[v] = rows
    print(f"v = {v}: done", flush=True)
base = [e for e, _, _ in spec[100]]
for v, rows in spec.items():
    moving = [(e, f, w) for e, f, w in rows if min(abs(e - b0) for b0 in base) > 1e-3*abs(e)] if v != 100 else rows
    print(f"v = {v:3d}: " + "  ".join(f"{e:+.2e}{f}({w:.2f})" for e, f, w in moving[:12]))
