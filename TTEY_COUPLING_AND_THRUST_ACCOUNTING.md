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

## 3. Consequence for TTEY as propulsion — negative, and decisive

The hoped-for escape was that TTEY might couple to geometry **more strongly** than
standard gravity, evading the `G/c⁵` bottleneck that makes gravitational-wave thrust
useless. It does not:

| coupling | value |
|---|---|
| gravitational-wave emission `G/c⁵` | 2.756 × 10⁻⁵³ |
| **TTEY relative coupling `2(a₀/c²)²`** | **2.689 × 10⁻⁵⁴** |

**TTEY's coupling is ~10× *weaker* than the gravitational-wave coupling.** A TTEY
thruster is harder to build than a GW thruster, not easier. **The action as written
contains no propulsion enhancement**, and any drive claim needs a mechanism the action
does not currently contain.

Stated plainly so it is not rediscovered: *the FIG Tree action does not support a
laboratory-scale thrust effect.*

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
