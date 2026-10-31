# Front page

Date: 2026-10-31. This page is the column the corpus hangs on. It does not replace [`CURRENT_STATE_READ_THIS_FIRST.md`](CURRENT_STATE_READ_THIS_FIRST.md), which remains the dated ledger of every claim. Where a number below and that ledger disagree, the ledger's cited file wins, and this page should be corrected.

The picture this page follows is the checked drawing in BLK-939. Two passes, wound opposite ways, add to a column whose pieces bear on each other. They are not bars nailed to one theory-of-everything spine.

## The four blocks

1. **Standard Model, imported.** See [`IMPORTED_STANDARD_MODEL.md`](IMPORTED_STANDARD_MODEL.md). The gauge group, the fermion representations, the Higgs sector, and the measured couplings and mixing angles are taken from the textbook theory and tagged `[C]`. The anomaly check records that the textbook generation cancels, that `corpus_proposal` is null, and that `derived_from_geometry` is false. Passing that control does not create a geometric assignment, and it does not set the seam mass.

2. **General relativity outside galaxies.** Unless a new screen is the explicit task, the solar system and the vacuum light cones stay on ordinary general relativity. The unscreened galaxy law is not promoted into those regimes.

3. **Galaxy law, an axiom.** On galaxies the interpolating function is \(\mu(x)=x/\sqrt{1+x^2}\), with one acceleration scale. Tag `[A]`. The action does not force it. It stays an axiom until a derivation exists outside the closed channels below. The Fisher identity that selects it is an input, not that derivation.

4. **Null-seam yield, calculated.** See [`SEAM.md`](SEAM.md). A radiation cosmology through a null seam has \(|\beta|^2=\exp(-\pi k^2/\gamma)\) and direct yield \(I=1/(8\pi^{3/2})\). \(\gamma\) is not fixed, and the mass is symbolic. The receipts live in `Chyren/state/` and in The Hood under BLK-936. They are not copied into this repository. The yield does not select the galaxy axiom and does not set a neutrino mass.

## Where the galaxy law stops

[`02_galaxy_dynamics/screen_mass_cassini.json`](02_galaxy_dynamics/screen_mass_cassini.json) evaluates the unscreened case \(S=1\). Its own keys `unscreened_S_eq_1_sigma_2014` and `unscreened_S_eq_1_sigma_2026` are about \(+5.4\sigma\) and \(+5.7\sigma\) against the 2014 window, and about \(+9.7\sigma\) and \(+10.3\sigma\) against the 2026 window, at the two external-field values in that file. That run is why block 3 does not enter the solar system. It does not replace earlier Cassini rows in the ledger, which use other anchors and other screens. \(\lambda\) and \(M\) are not fitted to move \(S\).

## Closed channels

Do not reopen these as ways to derive the galaxy law.

| Channel | Receipt | Result |
| :--- | :--- | :--- |
| Variation of the action | `02_galaxy_dynamics/q3_action_forces_mu.json` | The action does not force \(\mu_{\mathrm{std}}\). Q3 stays open as a uniqueness claim. |
| Polynomial auxiliaries | `02_galaxy_dynamics/q3_algebraic_nogo.json` | Algebraic elimination cannot produce \(\mathrm{arsinh}\). |
| Finite boost determinants | `02_galaxy_dynamics/q3_det_ratio.json` | `determinant does not equal arsinh`. |
| One-dimensional chiral determinant | `02_galaxy_dynamics/q3_chiral_det.json` | The plus projector recovers \(\mathrm{arsinh}\) only as the Maurer–Cartan identity. `matches_F_std` is false. |

\(F_{\mathrm{std}}=\frac12\bigl(x\sqrt{1+x^2}-\mathrm{arsinh}\,x\bigr)\) is the integral of the axiom. It is not an output of those operators.

## What a note in this repository is for

A live note names which of the four blocks it belongs to, and which other block it constrains. A note that only lengthens the sentence "this is a theory of everything" is a bar on the retired spine. Killed claims stay in the record as `[X]`. This page does not delete them.
