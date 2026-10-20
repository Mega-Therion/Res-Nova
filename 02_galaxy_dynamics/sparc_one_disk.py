#!/usr/bin/env python3
"""NGC 3198: algebraic nu*g_N versus the divergence-equation disk.

SPARC rotmod, distance 13.8 Mpc, standard 3.6 um masses
Upsilon_disk = 0.5, Upsilon_bul = 0.7. The baryonic curve is fit by one
exponential disk, then solved on the same grid as disk_qumond_split.py.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.optimize import least_squares
from scipy.special import i0, i1, k0, k1

import disk_qumond_split as q

DATA = Path(
    "/home/mega/Chyren/Research_and_Data/07_Domain_Tiers_and_Data/Datasets/data/sparc_data/NGC3198_rotmod.dat"
)
# (km/s)^2 / kpc
G = 4.3009172706e-6
A0 = 1.1160351336495208e-10 * 3.085677581e13  # (km/s)^2 / kpc
UPS_DISK = 0.5
UPS_BUL = 0.7


def load(
    path: Path = DATA, ups_disk: float = UPS_DISK, ups_bul: float = UPS_BUL
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rows = []
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        p = line.split()
        rows.append([float(x) for x in p[:6]])
    a = np.array(rows)
    R, Vobs, eV, Vgas, Vdisk, Vbul = (a[:, i] for i in range(6))
    Vbar = np.sqrt(np.maximum(Vgas**2 + ups_disk * Vdisk**2 + ups_bul * Vbul**2, 0.0))
    return R, Vobs, eV, Vbar


def freeman(R: np.ndarray, Rd: float, Sigma0: float) -> np.ndarray:
    y = R / (2.0 * Rd)
    # I0 K0 - I1 K1 is 0 at y=0
    bracket = i0(y) * k0(y) - i1(y) * k1(y)
    return np.sqrt(np.maximum(4.0 * np.pi * G * Sigma0 * Rd * y**2 * bracket, 0.0))


def main() -> None:
    import sys

    name = sys.argv[1] if len(sys.argv) > 1 else "NGC3198"
    zd = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1
    ups = float(sys.argv[3]) if len(sys.argv) > 3 else UPS_DISK
    path = DATA.with_name(f"{name}_rotmod.dat")
    R_obs, Vobs, eV, Vbar = load(path, ups_disk=ups)

    def resid(p):
        Rd, logS = p
        return freeman(R_obs, Rd, np.exp(logS)) - Vbar

    fit = least_squares(
        resid, np.array([3.0, np.log(400.0)]), bounds=([0.3, 0.0], [15.0, 20.0])
    )
    Rd, Sigma0 = float(fit.x[0]), float(np.exp(fit.x[1]))
    Vfit = freeman(R_obs, Rd, Sigma0)
    rms = float(np.sqrt(np.mean((Vfit - Vbar) ** 2)))
    mass = Sigma0 * 2.0 * np.pi * Rd**2

    # Grid in units of Rd. Accelerations in units of a0. G_code = 1.
    # Cubic box: the flat |z|<<R grid drove the outer speed to zero.
    Rmax = 12.0
    nR, nZ = 97, 481
    Ru = np.linspace(0.0, Rmax, nR)
    Zu = np.linspace(-Rmax, Rmax, nZ)
    dR, dZ = float(Ru[1] - Ru[0]), float(Zu[1] - Zu[0])
    RR, ZZ = np.meshgrid(Ru, Zu, indexing="ij")
    L = q.build_laplacian(nR, nZ, dR, dZ, Ru)
    # zd / Rd. rho0 so that Sigma0_code = rho0 * zd * sqrt(2pi)
    # Physical g = (km/s)^2/kpc. Code g_code * a0 = g_phys.
    # Sigma_code such that Newtonian g matches: Sigma_phys / a0_in_(km/s)^2/kpc * G?
    # V^2 = 2 pi G Sigma Rd * f(y), so the dimensionless field uses
    # g_code = g_phys / a0, and we set the code surface density from that.
    Sigma_code = (
        2.0 * np.pi * G * Sigma0 / A0
    ) * Rd  # because V^2/(Rd) / a0 = 2 pi G Sigma Rd / (Rd a0) * f = (2pi G Sigma / a0) f
    # Wait: g_phys = V^2 / R = V^2 / (y*2*Rd). Freeman V^2 = 4 pi G Sigma Rd y^2 (I0K0-I1K1)
    # g_phys = V^2 / R = 4 pi G Sigma Rd y^2 bracket / (2 Rd y) = 2 pi G Sigma y bracket
    # g_code = g_phys / a0. At the solver, Poisson uses 4 pi rho with G=1, lengths in Rd.
    # g_code ~ Sigma_code / Rd_code, Rd_code=1, so Sigma_code = g_phys/a0 * (Rd in the same algebra).
    # From g_phys = 2 pi G Sigma_phys * (y bracket), g_code = g_phys/a0.
    # In code, g = 2 pi * Sigma_code * (y bracket) if G=1 and the radial unit is Rd
    # so 2 pi Sigma_code = 2 pi G Sigma_phys * Rd / a0, because an extra length
    # entered when R was divided by Rd and g = V^2/R picked up 1/Rd.
    # V^2 has g*R = g_code*a0 * (Ru*Rd) so V^2/a0/Rd = g_code * Ru.
    # Code g_code should equal g_phys * Rd / a0? No.
    # We compare g, and v^2 = g * R_phys = (g_code * a0) * (Ru * Rd) only if g_code = g_phys/a0.
    # Poisson in code: lengths scaled by Rd, potential scaled by a0*Rd, so
    # nabla_code^2 Phi_code = 4 pi rho_code
    # nabla_phys^2 Phi_phys = nabla_code^2 Phi_code * (a0*Rd) / Rd^2 = 4 pi G rho_phys
    # rho_code = G rho_phys * Rd / a0
    # Sigma_code = integral rho_code d z_code = G Sigma_phys / a0
    rho0 = (G * Sigma0 / A0) / (zd * np.sqrt(2.0 * np.pi))
    rho = rho0 * np.exp(-RR) * np.exp(-0.5 * (ZZ / zd) ** 2)
    radius = np.sqrt(RR**2 + ZZ**2)
    # Phi_code = Phi_phys/(a0*Rd) = -GM/(a0*Rd^2*Ru)
    mass_code = G * mass / (A0 * Rd**2)
    Phi = q.solve_poisson(L, 4.0 * np.pi * rho, -mass_code / np.maximum(radius, 1e-3))
    gR = q.grad_R(Phi, dR)
    gZ = q.grad_Z(Phi, dZ)
    gmag = np.sqrt(gR**2 + gZ**2)
    nu = q.nu_simple(gmag)
    div = q.divergence(nu * gR, nu * gZ, Ru, dR, dZ)
    boundary = q.monopole_psi(np.maximum(radius, 1e-3), mass_code)
    psi = q.solve_poisson(L, div, boundary)
    j0 = int(np.argmin(np.abs(Zu)))
    g_alg = (nu * gR)[:, j0]
    g_pde = q.grad_R(psi, dR)[:, j0]

    # Convert code g (in a0, per Rd) to km/s: v^2 = g_phys * R_phys = g_code * a0 * Ru * Rd
    def v_of(g_code: np.ndarray) -> np.ndarray:
        return np.sqrt(np.maximum(g_code * A0 * Ru * Rd, 0.0))

    Vnewt = v_of(gR[:, j0])
    Valg = v_of(g_alg)
    Vpde = v_of(g_pde)
    R_phys = Ru * Rd
    # Compare on observed radii inside 4 Rd, where the sphere control was clean.
    m = (R_obs > 0.3 * Rd) & (R_obs < 2.5 * Rd)
    Valg_o = np.interp(R_obs[m], R_phys, Valg)
    Vpde_o = np.interp(R_obs[m], R_phys, Vpde)
    rel = np.abs(Vpde_o**2 - Valg_o**2) / np.maximum(Valg_o**2, 1.0)
    Vnewt_o = np.interp(R_obs[m], R_phys, Vnewt)
    boost = (Vpde_o - Vnewt_o) / np.maximum(Valg_o - Vnewt_o, 1e-6)
    print(
        f"{name} Ups_disk={ups:.3f} zd/Rd={zd:.3f} Rd={Rd:.3f} kpc Sigma0={Sigma0:.3f} Msun/kpc^2 mass={mass:.3e} Msun"
    )
    print(f"Freeman fit rms versus SPARC Vbar = {rms:.2f} km/s")
    print(f"on {int(m.sum())} SPARC radii in (0.3 Rd, 2.5 Rd):")
    print(
        f"  median |v_pde^2 - v_alg^2| / v_alg^2 = {np.median(rel):.4f} max={np.max(rel):.4f}"
    )
    print(
        f"  median v_alg={np.median(Valg_o):.1f} v_pde={np.median(Vpde_o):.1f} Vbar={np.median(Vbar[m]):.1f} Vobs={np.median(Vobs[m]):.1f}"
    )
    print(f"  median (Vpde-Vnewt)/(Valg-Vnewt) = {np.median(boost):.3f}")
    err = np.maximum(eV[m], 1.0)
    n = int(m.sum())
    chi_alg = float(np.sum(((Valg_o - Vobs[m]) / err) ** 2))
    chi_pde = float(np.sum(((Vpde_o - Vobs[m]) / err) ** 2))
    print(
        f"  chi2_alg={chi_alg:.1f} chi2_pde={chi_pde:.1f} n={n} chi2_pde/n={chi_pde / n:.2f}"
    )
    for r, vb, vo in zip(
        R_obs[m][:: max(1, m.sum() // 6)],
        Vbar[m][:: max(1, m.sum() // 6)],
        Vobs[m][:: max(1, m.sum() // 6)],
    ):
        ia = float(np.interp(r, R_phys, Valg))
        ip = float(np.interp(r, R_phys, Vpde))
        inn = float(np.interp(r, R_phys, Vnewt))
        print(
            f"  R={r:.2f} Vbar={vb:.1f} Vnewt={inn:.1f} Valg={ia:.1f} Vpde={ip:.1f} Vobs={vo:.1f}"
        )


if __name__ == "__main__":
    main()
