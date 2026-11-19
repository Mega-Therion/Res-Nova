"""Export the smooth_phi screen profile S(r) for one cluster (r = inf) so verify_sawtooth.py can test it on the original solver.
Usage: verify_smooth_profile.py NAME out.npz"""
import sys, os, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D); sys.path.insert(0, D)
import xcop_cosh as X
cl = next(c for c in X.load_xcop() if c["name"] == sys.argv[1])
st = X.solve_cluster_smooth(cl, X.MU0, float("inf"))
print(sys.argv[1], "smooth R500/R200", st["R500"], st["R200"], "fd_resid", st["fd_resid"], "max_dS", st["max_dS"])
np.savez(sys.argv[2], rr=st["rr"], S=st["S_arr"])
