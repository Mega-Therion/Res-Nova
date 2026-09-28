import math, numpy as np, scipy.sparse as sps, scipy.sparse.linalg as spla
import solve_steady as SS
vf = 10/299792.458; b=3e-4; M = 12*math.pi*vf**4/SS.A0T
g = SS.Grid(24, 48, 1e-4, math.asinh(100.), math.asinh(100.)); rho = SS.plummer(g, M, b)
P = SS.ProblemH(g, 0.0, rho, 0.0)
fp, ok, gn = P.newton(SS.initial_guess(g, M, b, 0.0), tol=1e-12, maxit=12, verbose=False)
print("after 12 its: residual", gn, flush=True)
src_t = P.T.T @ P.src
gr, H, Y = P.grad_hess(fp)
rown = np.asarray(abs(H).sum(axis=1)).ravel(); dsc = 1/np.sqrt(np.maximum(rown, rown.max()*1e-30)); Sd = sps.diags(dsc)
Hs = (Sd @ H @ Sd).tocsc(); gs = Sd @ gr
lu = spla.splu(Hs)
x = lu.solve(-gs); r = Hs @ x + gs
print("linear solve relative residual:", np.linalg.norm(r)/np.linalg.norm(gs), flush=True)
for k in range(3):
    x = x + lu.solve(-r); r = Hs @ x + gs
    print(f"  after refinement {k+1}:", np.linalg.norm(r)/np.linalg.norm(gs), flush=True)
vals, vecs = spla.eigsh(Hs, k=6, sigma=0, which="LM")
gsn = gs / np.linalg.norm(gs)
for lam, v in sorted(zip(vals, vecs.T), key=lambda t: abs(t[0])):
    parts = {n: float(np.linalg.norm(v[SS.FIX[n]*g.ncell:(SS.FIX[n]+1)*g.ncell])**2) for n in SS.NAMES}
    top = sorted(parts.items(), key=lambda t: -t[1])[:3]
    print(f"eig {lam:+.3e}  overlap with residual {abs(v @ gsn):.3f}  fields: " + ", ".join(f"{n} {w:.2f}" for n, w in top), flush=True)
big = spla.eigsh(Hs, k=2, which="LM", return_eigenvectors=False)
print("largest |eig|:", big, flush=True)
print("--- roughness of the softest modes: sum (neighbour differences)^2 / sum values^2; 8 = pure checkerboard in 2D, ~0 = smooth", flush=True)
for lam, v in sorted(zip(vals, vecs.T), key=lambda t: abs(t[0])):
    k = max(SS.NAMES, key=lambda n: np.linalg.norm(v[SS.FIX[n]*g.ncell:(SS.FIX[n]+1)*g.ncell]))
    a = v[SS.FIX[k]*g.ncell:(SS.FIX[k]+1)*g.ncell].reshape(g.nR, g.nz)
    rough = (np.sum(np.diff(a, axis=0)**2) + np.sum(np.diff(a, axis=1)**2)) / np.sum(a**2)
    sgn = np.sign(a); alt = (np.mean(sgn[1:, :] * sgn[:-1, :] < 0) + np.mean(sgn[:, 1:] * sgn[:, :-1] < 0)) / 2
    print(f"eig {lam:+.3e} field {k}: roughness {rough:.2f}, fraction of neighbour sign flips {alt:.2f}", flush=True)
