# General relativity outside galaxies

Date: 2026-10-31. This note is block 2 of [`FRONT.md`](FRONT.md).

Outside galaxies, the gravitational law in this corpus is ordinary general relativity. That includes the solar system and the vacuum light cones. The galaxy interpolating function is not promoted into those regimes. A screen that would let one formula cover both is not the task of this note, and \(\lambda\) and \(M\) are not fitted here.

The boundary is the unscreened run \(S=1\) in [`02_galaxy_dynamics/screen_mass_cassini.json`](02_galaxy_dynamics/screen_mass_cassini.json). That file's keys `unscreened_S_eq_1_sigma_2014` and `unscreened_S_eq_1_sigma_2026` are `5.3666…` and `5.7` against the 2014 window, and `9.7222…` and `10.2777…` against the 2026 window, at the two external-field values stored beside those keys. The run fails. It is why block 3 stops at galaxies. It does not replace earlier Cassini rows in [`CURRENT_STATE_READ_THIS_FIRST.md`](CURRENT_STATE_READ_THIS_FIRST.md), which use other anchors and other screens.

What this note constrains:

- Block 3. \(\mu(x)=x/\sqrt{1+x^2}\) stays an axiom on galaxies. This note does not derive it and does not extend it.
- Block 1, [`IMPORTED_STANDARD_MODEL.md`](IMPORTED_STANDARD_MODEL.md). The imported fields couple to the general-relativistic metric in this regime. That coupling is part of the import.
- Block 4, [`SEAM.md`](SEAM.md). The seam is a general-relativistic calculation. It does not move this boundary, and this boundary does not set the mass in the yield.
