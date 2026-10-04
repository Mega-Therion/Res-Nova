# Res Nova public-abstract correction, 2026-10-03

This file corrects the abstracts of the earlier records in concept DOI
10.5281/zenodo.21539453, including 10.5281/zenodo.22079177 and
10.5281/zenodo.21969121.

Those abstracts said the dual-channel action uniquely determines the
interpolating function μ(x) = x/(1+x). That function was withdrawn on
2026-09-12 after it failed in the solar system. It is not the live branch.

The live weak-field branch is μ_std(x) = x/√(1+x²). That is the standard
MOND interpolating function, read inside the Skordis–Złośnik AeST framework.
Under that one function, on 3,375 SPARC points, the tier-0 median reduced χ²
is 11.08 for the horizon anchor a₀ = cH₀/2π and 9.93 for the literature value
1.2×10⁻¹⁰ m s⁻². The numbers are in `02_galaxy_dynamics/PARAMETER_LEDGER.json`,
included here. The horizon anchor fits worse. The factor 2π is declared, not
derived.

Unscreened μ_std fails Cassini's external-field quadrupole by about 4.6σ.
A phenomenological screen can pass. It has no covariant realization yet.
AeST branch selection (D7) is open: a proposed no-go was not adopted.
Lean 4 checks the algebra that was encoded. It does not decide the comparison.

The current statement is the GitHub README of Mega-Therion/Res-Nova, section
"For reviewers — start here":

https://github.com/Mega-Therion/Res-Nova
