#!/usr/bin/env python3
"""Sensitivity of the repo reference Q2 (Milgrom reduced integral, efe_quadrupole_q2.py)
to its own (nv, nxi) quadrature, at nu_std, a0 = 1.1607e-10, g_e = 1.9e-10.
Validation only; the axisymmetric solver does not import this. ~10 min."""
import sys, numpy as np
from scipy.optimize import brentq
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import efe_quadrupole_q2 as E
nu=E.NU['mu_std (nu_2)']; a0=1.1607e-10
etaN=brentq(lambda x:x*nu(x)-1.9e-10/a0,1e-8,1.9e-10/a0); nue=nu(etaN)
for nv,nxi in ((3000,400),(3000,1600),(3000,6400),(12000,6400)):
    v=np.concatenate([np.linspace(0,1e-3,50)[:-1],np.logspace(-3,3,nv)])
    xi,w=np.polynomial.legendre.leggauss(nxi)
    inner=np.empty_like(v)
    for i in range(0,len(v),500):
        V,XI=np.meshgrid(v[i:i+500],xi,indexing='ij')
        y=np.sqrt(np.maximum(etaN**2+V**4+2*etaN*V**2*XI,1e-300))
        inner[i:i+500]=((nu(y)-nue)*(etaN*(3*XI-5*XI**3)+V**2*(1-3*XI**2)))@w
    qq=1.5*np.trapezoid(inner,v)
    print(nv,nxi,-3*qq*a0**1.5/(2*np.sqrt(E.GM)),flush=True)
