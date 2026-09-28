#!/usr/bin/env python3
"""When does cosmic acceleration end under the dark-energy ceiling? (RY 2026-09-28: the universe "tries to stabilize".)
In the ceiling model the share approaches kappa and w -> 0, so the total equation of state tends to 0 and the
deceleration parameter q = -1 - d ln E / d ln a tends to +1/2: acceleration is transient, unlike LCDM (q -> -1).
The share equation d ln r / d ln a = 3 (1 - g(s)) is integrated past today (to s -> 1) by the quadrature of
ceiling_factorial_law.py, for the approach laws the data accept at Omega_f = kappa: the power law at n = 1.25 and the
factorial counting laws at mu = 1. Validation: the power-law quadrature must match the closed form for a > 1.
Usage: ceiling_future.py   Output: CEILING_FUTURE.json"""

import json, math
import numpy as np
import ceiling_model_cmb_bao_sn as m
import ceiling_factorial_law as cf
import cosmo_data as cd

H_FIT = (
    0.68  # time conversion only; a_end does not depend on h beyond the radiation term
)
GYR_PER_UNIT = 977.8  # 1 / (1 km/s/Mpc) in Gyr


def future(law, p, h=H_FIT, of=m.KAPPA):
    orad = m.OR / h**2
    om0 = 1 - m.LN2 - orad
    r0 = m.LN2 / om0
    rf = of / (1 - of)
    s0 = r0 / rf
    u = np.linspace(math.log(s0) - 75.0, math.log(1 - 1e-9), 400001)
    f = 1.0 / (3.0 * (1.0 - cf.LAWS[law](np.exp(u), p)))
    tau = np.concatenate(([0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(u))))
    tau -= np.interp(math.log(s0), u, tau)
    a = np.geomspace(1, 50, 200001)
    r = rf * np.exp(np.interp(np.log(a), tau, u))
    E = np.sqrt(orad * a**-4 + om0 * a**-3 * (1 + r))
    q = -1 - np.gradient(np.log(E), np.log(a))
    t = (
        np.concatenate(
            (
                [0],
                np.cumsum(
                    0.5 * (1 / (a[1:] * E[1:]) + 1 / (a[:-1] * E[:-1])) * np.diff(a)
                ),
            )
        )
        * GYR_PER_UNIT
        / (100 * h)
    )
    i = int(np.argmax(q > 0))
    share = om0 * a**-3 * r / E**2
    adot = a * E  # expansion speed, units of H0 (a = 1 today)
    cross = lambda lvl: (
        float(t[int(np.argmax(share >= lvl))]) if share[-1] >= lvl else None
    )
    return (
        {
            "q_today": float(q[0]),
            "a_end_of_acceleration": float(a[i]),
            "gyr_from_now": float(t[i]),
            "share_at_end": float(r[i] / (1 + r[i])),
            "q_at_a50": float(q[-1]),
            # RY: the chiral band [0.707, kappa] as the Goldilocks zone; the ceiling is its top
            "gyr_share_enters_band_0707": cross(0.7071),
            "gyr_share_reaches_0.9": cross(0.9),
            "share_at_a50": float(share[-1]),
            "expansion_speed_vs_today_at_a2.4_a10_a50": [
                float(np.interp(x, a, adot) / adot[0]) for x in (2.4, 10, 50)
            ],
        },
        a,
        E,
    )


def main():
    _, a, Eq = future("power", 1.25)
    Ec, _ = m.make_E("ceil", H_FIT, None, m.KAPPA, 1.25)
    dev = np.abs(Eq / Ec(1 / a - 1) - 1)
    val = float(dev[a <= 10].max())  # grid resolution near s -> 1 limits a > 10
    print("power-law quadrature vs closed form for 1 <= a <= 10, max |dE/E|:", val)
    assert val < 1e-5
    out = {
        "h_for_time": H_FIT,
        "omega_f": m.KAPPA,
        "validation_max_rel_dE_future_a_le_10": val,
        "rel_dE_at_a50": float(dev[-1]),
        "laws": {},
    }
    for law, p in (
        ("power", 1.25),
        ("power", 1.0),
        ("shifted_poisson", 1.0),
        ("truncated_poisson", 1.0),
    ):
        res, _, _ = future(law, p)
        out["laws"][f"{law} p={p}"] = res
        print(law, p, res)
    json.dump(out, open(cd.out("CEILING_FUTURE.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
