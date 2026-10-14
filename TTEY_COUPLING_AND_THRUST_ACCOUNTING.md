# TTEY — Coupling Constant and Thrust Accounting

> **BRANCH NOTICE (2026-09-20).** The results below concern
> $\mathcal{F}_{\text{dual}}(x) = \tfrac12 x^2 - x + \ln(1+x)$ and its constitutive
> ratio $\mu(x) = x/(1+x)$. **That branch was falsified on 2026-09-12** — it leaves
> an unscreened solar-system anomalous acceleration far above the Cassini bound —
> and the theory is rebuilt on $\mu_{\text{std}}(x) = x/\sqrt{1+x^2}$.
>
> The algebraic statements here remain **true as mathematics**: $\mathcal{F}_{\text{dual}}$
> really does have the stated constitutive structure, Padé minimality and
> ghost-freedom. What is retracted is their status as claims about the *physical*
> model. A `[P]` below should be read as "proved about $\mathcal{F}_{\text{dual}}$",
> not "proved about the theory". See `TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md`
> for the live derivation.



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

1. **Does the TTEY field equation require ρ < 0 anywhere? — ANSWERED for the scalar
   sector (2026-10-14, `[D]`, `scripts/ttey_scalar_nec.py`, 8/8).** No. The covariant
   AQUAL scalar sector `L = −(a₀²/8πG) F(𝒳)`, `𝒳 = (∂φ)²/a₀²`, has stress tensor
   `T_μν = (1/4πG) F′(𝒳) ∂_μφ ∂_νφ + g_μν L` (metric variation; sign fixed against the
   canonical scalar, which it reproduces as `ρ = ½|∇φ|²`). For a static field and any
   null `k` (`g_μν k^μ k^ν = 0`),

   > `T_μν k^μ k^ν = (1/4πG) F′(𝒳) (k·∇φ)² ≥ 0  ⟺  F′ ≥ 0`,

   and `F′ = μ_std ≥ 0` is exactly the proven ghost condition (`SZStdEmbedding.lean`,
   `J′ > 0`). The static energy density is `ρ = (a₀²/8πG) F_std ≥ 0` (since `F_std(0)=0`
   and `F_std′ = x μ_std ≥ 0`). So the IT/MOND scalar sector satisfies the null energy
   condition and carries non-negative energy density — the same positivity that makes
   AeST ghost-free. This is the thing Alcubierre-class metrics do **not** have, and it is
   why TTEY cannot source a warp bubble: a bubble needs NEC violation, and the scalar
   sector is NEC-respecting by the ghost condition, not by a numerical accident. It
   reinforces §3's sign/regime argument with a structural no-go. **Remaining:** the
   vector sector on the held branch (on the dragged/stealth branch the full source
   `𝒰^μν = 0`, `AeSTStealthSector`), and the full covariant `𝒰^μν` NEC, are not yet
   closed; this is the scalar-channel result only.

   **This does not by itself close the TTEY drive, because TTEY's own formalization uses a
   different field model.** `…/god_theory/physics_formalization/Tension_Stress_Energy_Tensor.md`
   (R.W. Yett, 2026-06-15) grants exactly the point above — a canonical scalar satisfies the
   WEC, so it "cannot drive an Alcubierre metric" — and instead takes the IT field with a
   **double-well potential** `V(𝒯) = λ(𝒯² − χ_vac²)²`, `χ_vac = 1/√2`, driven locally
   **below** `χ_vac`, and reads the negative energy off a **vacuum-relative (Casimir-type)**
   effective tensor `𝒯̃_μν = T_μν − ⟨0|T_μν|0⟩_global` against the E₈ baseline. That is a
   distinct construction from the live AQUAL sector (a kinetic function `F_std` of `(∂φ)²`,
   no double-well, no baseline subtraction), and the NEC result here does not refute it. What
   it does is sharpen the real question for TTEY:
   - **Same field, or two?** If the TTEY `𝒯` is the AQUAL `φ`, the double-well `V` and the
     `F_std` kinetic function must coexist in one Lagrangian, and NEC must be redone for the
     combined field. If it is a separate sector, that sector needs its own justification.
   - **Does the baseline subtraction survive a quantum inequality?** Casimir-type relative
     deficits are real but bounded; the Ford–Roman-type bounds are what forbid *macroscopic*
     warp. The subtraction must be shown not to hide that bound.

   So: the galaxy/AQUAL sector is NEC-respecting (new, `[D]`); the TTEY exotic-energy route is
   a separate, still-open Casimir-type construction. Neither "TTEY works" nor "TTEY is dead" is
   established. See [[Tension_Stress_Energy_Tensor]] and `papers_42/PAPER_27_*`.
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
