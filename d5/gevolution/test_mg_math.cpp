// V0 patch-correctness test (PREREG_D5_MG_EVOLUTION.md §5 V0):
// the C++ kernel must reproduce the Python-frozen G_eff_tilde(a,k)
// to < 1e-10 relative at all sampled (a,k).
#include <cstdio>
#include "mg_math.hpp"

int main() {
#ifdef MG_ARM
  const double as[] = {1.0/101.0, 0.25, 0.5, 1.0/1.5, 1.0};
  const double ks[] = {0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 2.5, 5.0};
  printf("ARM %d\n", MG_ARM);
  for (double a : as)
    for (double k : ks)
      printf("%.17e %.17e %.17e %.17e %.17e\n",
             a, k, mg::eps_of_a(a), mg::k0_of_a(a), mg::G_eff_tilde(a, k));
#else
  printf("GR (inert)\n");
#endif
  return 0;
}
