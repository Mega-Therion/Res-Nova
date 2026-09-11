//////////////////////////
// mg_poisson.hpp — Fourier-space Poisson solve with G_eff(a,k) kernel
//////////////////////////
// MG-evolution patch (Hassani & Lombriser, arXiv:2003.05927, Sec. 2.4):
// the parametrised coupling multiplies the Poisson kernel per Fourier mode.
// Mirrors gevolution's solveModifiedPoissonFT (gevolution.hpp) exactly —
// same FFT normalization (coeff / -N^3), same finite-difference
// gridk2 = [2N sin(pi i / N)]^2 — with the additional per-mode factor
//   potFT(k) = sourceFT(k) * coeff * G_eff_tilde(a,k) / k_fd^2
// where the physical wavenumber is k[h/Mpc] = sqrt(k_fd^2) / boxsize,
// boxsize in Mpc/h (gevolution convention).
// Only active when MG_ARM_A or MG_ARM_B is defined; else this header is inert.
//////////////////////////

#ifndef MG_POISSON_HPP
#define MG_POISSON_HPP

#include "LATfield2.hpp"
#include "mg_math.hpp"

#ifdef MG_ARM

void solveModifiedPoissonFT_MG(Field<Cplx> & sourceFT, Field<Cplx> & potFT,
                               Real coeff, Real a, double boxsize_mpc_h)
{
	using LATfield2::rKSite;
	const int linesize = potFT.lattice().size(1);
	int i;
	Real * gridk2;
	rKSite k(potFT.lattice());

	gridk2 = (Real *) malloc(linesize * sizeof(Real));

	coeff /= -((long) linesize * (long) linesize * (long) linesize);

	for (i = 0; i < linesize; i++)
	{
		gridk2[i] = 2. * (Real) linesize * sin(M_PI * (Real) i / (Real) linesize);
		gridk2[i] *= gridk2[i];
	}

	k.first();
	if (k.coord(0) == 0 && k.coord(1) == 0 && k.coord(2) == 0)
	{
		potFT(k) = Cplx(0.,0.);   // DC mode: homogeneous (as in GR; G_eff factor irrelevant)
		k.next();
	}

	for (; k.test(); k.next())
	{
		const Real kfd2 = gridk2[k.coord(0)] + gridk2[k.coord(1)] + gridk2[k.coord(2)];
		const double k_hmpc = std::sqrt((double) kfd2) / boxsize_mpc_h;
		potFT(k) = sourceFT(k) * coeff * (Real) mg::G_eff_tilde((double) a, k_hmpc) / kfd2;
	}

	free(gridk2);
}
#endif // MG_ARM

#endif // MG_POISSON_HPP
