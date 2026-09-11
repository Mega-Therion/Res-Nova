//////////////////////////
// mg_math.hpp — MG-evolution patch for Res-Nova (D5)
//////////////////////////
// Implements the parametrised effective gravitational coupling of
// Hassani & Lombriser (arXiv:2003.05927), their Eq. (8):
//
//   G_eff_tilde(a,k)/G = 1 + eps(a) * F_tilde(k)
//   F_tilde = b (k0/k)^af { [1 + (k/k0)^af]^(1/b) - 1 }
//
// with the Res-Nova mapping frozen in PREREG_D5_MG_EVOLUTION.md /
// D5_MG_PARAMETERS.json (SHA256 b9a939dd2b60d61ac177160ccaf7265a48c52ebd08b48359ee46aadb1af16b98):
//   eps(a) = 1/(2 x(a)^2 (1+x(a)))     [P] Lean-certified identity F''/F'
//   x(a)  = x0 sqrt(alpha) E(a),  x0 = c H0/a0 = 5.67 (manuscript-frozen)
//   af = 3, b = 2                       Vainshtein class (nDGP cast, their Eq. 27)
//   k0(a) = a h / r_MOND,  r_MOND = sqrt(G M_th/a0) = 0.4742751291427761 Mpc
//           (effective top-hat r_th = 7 Mpc/h comoving, their convention)
//
// Arms (compile-time):
//   MG_ARM_A: alpha = 1     — the theory (eps(z=0) = 0.00233)
//   MG_ARM_B: alpha = 0.01  — negative control (deep-MOND branch; code
//             sensitivity check ONLY, not a theory claim)
// No defines / MG_ARM_OFF: standard GR (this header inert).
//
// Dependency-free so it can be unit-tested standalone (V0 in the prereg).
//////////////////////////

#ifndef MG_MATH_HPP
#define MG_MATH_HPP

#include <cmath>

#if defined(MG_ARM_A)
  #define MG_ARM 1
#elif defined(MG_ARM_B)
  #define MG_ARM 2
#endif

namespace mg {

#ifdef MG_ARM
  // Frozen constants (see file header for provenance)
  const double x0_alpha1   = 5.67;                 // c H0 / a0, alpha = 1
  const double af          = 3.0;                 // Vainshtein index
  const double b_interp    = 2.0;                 // interpolation rate
  const double r_MOND_mpc  = 0.4742751291427761;  // physical, Mpc
  const double hubble_h    = 0.68;                // run cosmology (class_tk.dat)
  const double omega_m     = 0.3071;               // run cosmology (class_tk.dat)
#if MG_ARM == 1
  const double alpha_sqrt  = 1.0;
#elif MG_ARM == 2
  const double alpha_sqrt  = 0.1;
#endif

  // eps(a): the linear screening enhancement [P]
  inline double eps_of_a(double a) {
    const double E = std::sqrt(omega_m * std::pow(a, -3.0) + (1.0 - omega_m));
    const double x = x0_alpha1 * alpha_sqrt * E;
    return 1.0 / (2.0 * x * x * (1.0 + x));
  }

  // k0(a): effective Vainshtein wavenumber, comoving h/Mpc
  inline double k0_of_a(double a) {
    return a * hubble_h / r_MOND_mpc;
  }

  // G_eff_tilde(a,k)/G — their Eq. (8); k in comoving h/Mpc
  inline double G_eff_tilde(double a, double k_hmpc) {
    const double eps = eps_of_a(a);
    const double k0  = k0_of_a(a);
    const double y   = std::pow(k_hmpc / k0, af);   // y = (k/k0)^af
    // F_tilde = b (k0/k)^af { [1+(k/k0)^af]^(1/b) - 1 }  =  b y^(-1) { (1+y)^(1/b) - 1 }
    const double F   = b_interp / y
                       * (std::pow(1.0 + y, 1.0/b_interp) - 1.0);
    return 1.0 + eps * F;
  }
#endif

} // namespace mg

#endif // MG_MATH_HPP
