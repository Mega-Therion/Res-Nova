# Second-field quasistatic equation

**Tier:** the algebra that pairs ν with μ_std is `[D]`. The decision to test this equation next is `[O]`. No Cassini number and no SPARC number is claimed here.

This  note  writes the  second-field  equation for  the  next  test. It  adds no constant. It does not turn the tidal screen back on, and it does not retune a0. The equation is the test's definition. It is not a result, and it is not a claim that Cassini is passed.

The  Newtonian  shadow is  fixed  by matter  alone.  The  second field  is the potential whose gradient is the acceleration. In spherical symmetry the two are related by the algebraic galaxy law. With a nonuniform field they are not the same function, which is the point of using two fields. AeST in the weak field reduces to the one-field reading, so this equation is not AeST. D7 is unchanged.

The  host  field is  an  input, not  a  fit.  At the  Sun it is the Milky Way field at the Sun. On a SPARC galaxy it is that galaxy's environment. No x* and no Lagrangian zero C enter.

## Equation

Matter determines the shadow. a₀ = 1.1607×10⁻¹⁰ m s⁻², the live T1 value. μ_std(x) = x/√(1+x²). Its inverse, the same function as `nu_std` in `qumond_pm.py`, is

```
∇² Φ_N = 4π G ρ

y = |∇Φ_N| / a₀

ν(y) = √[ (1 + √(1 + 4/y²)) / 2 ]

∇² Φ = ∇ · [ ν(y) ∇Φ_N ]
```

Accelerations are g_N = −∇Φ_N and g = −∇Φ. Where ν is evaluated on a spherically symmetric field, g = ν(y) g_N, and y ν(y) = x with x μ_std(x) = y.

The host is a uniform addition to the shadow, not a source in ρ:

```
∇Φ_N = ∇Φ_N,int − g_{N,ext}
```

g_{N,ext} is constant across the system being solved. The internal piece of Φ is the isolated solution of the second Poisson equation. The uniform piece ν(y_ext) g_{N,ext} has zero divergence and is not part of that solve. This is the split already stated in `qumond_pm.py`.

## What is not in the equation

S(x), x*, and C are absent. The NGC 5055 disk evaluation of W is not an input. The C = 0 tidal screen stays withdrawn.

`qumond_pm.py` checks a Plummer dwarf in units G = a₀ = M = 1. Those checks are not the Cassini quadrupole and not a SPARC fit. Those two comparisons have not been run on this equation at the live a₀.
