# TTEY — Coupling Constant and Thrust Accounting

**Derived 2026-09-06 from the repository's own action.** Settles what the Information
Tension coupling *is*, what it implies for propulsion, and where the framework is and
is not falsifiable. Every number below is computed, not quoted.

---

## 1. The coupling was already written down

`TARGET_D2_PHYSICAL_ACTION_DERIVATION.md:78`:

```
S = −(a₀²/8πG) ∫ F_dual(|∇Φ|/a₀) d³x
```

**The Information Tension coupling constant is `a₀²/8πG`.** It was never missing; it
had simply never been evaluated or interpreted.

| quantity | value |
|---|---|
| `a₀ = cH₀/2π` (H₀ = 67.4) | 1.0421 × 10⁻¹⁰ m/s² |
| **`a₀²/8πG`** | **6.4745 × 10⁻¹² J/m³** |
| GR's `c⁴/16πG` | 2.4081 × 10⁴² |
| **ratio = 2(a₀/c²)²** | **2.689 × 10⁻⁵⁴** |

## 2. What the coupling means: it is the horizon

```
a₀/c² = 1.159 × 10⁻²⁷ m⁻¹
```

This is an **inverse length**, and the length is

```
c²/a₀ = 8.625 × 10²⁶ m = 2π × (Hubble radius c/H₀)
```

exactly 2π, by construction from `a₀ = cH₀/2π`.

> **The thing that "creates tension" is the cosmological horizon.** The coupling is not
> a local mechanism awaiting discovery — it is a finite causal boundary imprinting an
> inverse length on local dynamics.

This is the cleanest available statement of what Information Tension *is*, and it
explains the framework's own domain: an effect set by a horizon-scale inverse length is
visible in galaxy rotation curves and cosmology, and suppressed at laboratory scale by
roughly (system size / horizon)².

## 3. Consequence for TTEY as propulsion — closed, but NOT by a coupling argument

**Correction (2026-09-06, same day).** An earlier version of this section compared
`a₀²/8πG` against GR's `c⁴/16πG` and reported a ratio of 2(a₀/c²)² ≈ 2.7e-54,
concluding TTEY "couples more weakly than gravity." **That comparison was dimensionally
invalid and is withdrawn.** The Einstein–Hilbert term integrates a curvature (1/length²)
over 4D spacetime; the IT term integrates a *dimensionless* function over 3D space. The
two prefactors are not commensurable and their ratio means nothing.

RY rejected the conclusion on its own terms — correctly — pointing out that a *weaker*
coupling to gravity would, if anything, make gravity easier to counter, not harder.

**The correct argument is about sign and regime, not coupling strength.**

**(i) Sign.** MOND-type modifications make gravity **stronger** in the low-acceleration
regime — that is their entire purpose, explaining flat rotation curves. Information
Tension therefore *adds* to the attractive acceleration. It is a gravity-enhancing
theory. The sign is wrong for cancellation before magnitude is considered at all.

**(ii) Regime.** At Earth's surface `x = g/a₀ = 9.414e10`, i.e. deep Newtonian. With
`μ(x) = x/(1+x)`:

| quantity | value |
|---|---|
| `μ(g/a₀)` | 0.999999999989377 |
| fractional deviation from Newton | 1.062e-11 |
| extra acceleration supplied | **1.042e-10 m/s²** (inward) |
| needed to cancel g | 9.81 m/s² |
| **shortfall** | **9.414e10 ×** |

The IT term is non-negligible only where `|∇Φ| ~ a₀` — roughly 12 kpc out in a
10¹¹ M☉ galaxy. That is the theory's home and it is not a laboratory.

> **Information Tension cannot counter gravity: it adds to gravity, and at Earth's
> surface its contribution is 10¹¹ times too small. This is a statement about sign and
> regime — not about coupling strength.**

The separate propulsion question (thrust via radiated momentum) is still governed by
the `G/c⁵` bottleneck in §4, and nothing in the IT action changes that number.

## 4. The thrust ledger — what any drive must satisfy

Established while testing the magnetic routes; recorded because it generalises.

**Gradient, not field.** Force on a dipole is `∇(m·B)`, not `B`. A uniform field
produces torque only. Every working concept builds a gradient and moves it; every
failed one produces a field and hopes.

| route | verdict |
|---|---|
| Static magnet in Earth's field | Dead. Gradient is 1.46 × 10⁻¹¹ T/m; a large superconducting coil lifts **1.5 mg**. Diamagnetic levitation needs `B·dB/dz ≈ 1400 T²/m`; Earth supplies 4.5 × 10⁻¹⁶ — short by 3 × 10¹⁸. |
| Ampère longitudinal force | **Nets to zero.** Verified numerically: Ampère and Grassmann force laws agree to 2 × 10⁻¹⁶ for closed circuits. Internal forces cannot thrust. |
| Coilgun / mass driver | Works — *time-varying* fields evade Earnshaw and build their own moving gradient. |
| Electrodynamic tether | Works — `F = I L × B`; 20 A over 20 km gives **12 N**, ~1 km/s per day on 1 t, propellantless. Escapes the Ampère null because the circuit closes **through the ionosphere**, outside the vehicle. Not antigravity: momentum goes into the magnetosphere. Cannot hover — 1 t needs 9,810 N, short by 818×. |
| Gravitational-wave recoil | Real but feeble. 1 N needs only **300 MW** — the barrier is not energy, it is the 10⁻⁵³ coupling. |
| Geometry (Alcubierre-class) | Escapes momentum conservation legitimately — no global translation symmetry in a dynamical spacetime, and the field carries the momentum. Pays instead with **energy-condition violation**. |

**The rule:** momentum conservation follows from spatial translation symmetry
(Noether), not from electromagnetism. Changing the force changes nothing. Only making
spacetime itself dynamical changes the board — and that route bills you in negative
energy density rather than momentum.

## 5. Open questions this leaves

1. **Does the TTEY field equation require ρ < 0 anywhere?** Compute the stress-energy
   the geometry demands and test `T_μν k^μ k^ν ≥ 0` for null k. If it stays
   non-negative, the framework has something Alcubierre-class metrics do not.
2. **Is `a₀²/8πG` derived or inherited?** It follows from `a₀ = cH₀/2π`, which is
   itself one of the two irreducible parameters. The coupling is therefore only as
   derived as a₀ is.
3. **The local/global H₀ split.** The corpus uses `H_global ≈ 67.4` for
   `Ω_Λ = ln 2` and `H_local ≈ 73.04` for the SPARC acceleration scale, via
   "local running amplification" `H_local = H_global(1+δ)`. **The coupling above is
   H₀-dependent**, so it inherits whichever H₀ is used — this must be stated wherever
   the coupling appears.

## 6. Provenance

Section 1 from `TARGET_D2_PHYSICAL_ACTION_DERIVATION.md:78`. Section 4 magnetic and
GW figures computed from CODATA constants and the dipole/quadrupole formulae. The
Ampère–Grassmann equivalence was verified by direct numerical integration over two
closed loops (400 segments each), agreeing to machine precision.

Related: [[TWO_CHANNEL_CEILING_ANALYSIS]], `PillarIV_AntiDriftGate.lean`,
`FIG_TREE_MONOGRAPH.md` §Pillar I (a₀).
