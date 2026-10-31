# Imported Standard Model

Date: 2026-10-31. This note is block 1 of [`FRONT.md`](FRONT.md). Tag `[C]`. Nothing on this page is a result of the repository.

The gauge group \(SU(3)_c \times SU(2)_L \times U(1)_Y\), the Higgs sector, and the measured couplings and mixing angles are taken from the textbook theory. One generation of left-handed Weyl fermions, as entered in [`05_lean_formalization/sm_anomaly_cancellation.py`](05_lean_formalization/sm_anomaly_cancellation.py), is:

| Field | \(SU(3)\) | Weak multiplicity | \(Y\) |
| :--- | :--- | :--- | :--- |
| \(q\) | \(3\) | \(2\) | \(1/6\) |
| \(u^c\) | \(\bar{3}\) | \(1\) | \(-2/3\) |
| \(d^c\) | \(\bar{3}\) | \(1\) | \(1/3\) |
| \(\ell\) | \(1\) | \(2\) | \(-1/2\) |
| \(e^c\) | \(1\) | \(1\) | \(1\) |

Right-handed fields are written as their left-handed conjugates. \(Y\) is hypercharge, not electric charge.

[`05_lean_formalization/sm_anomaly_cancellation.json`](05_lean_formalization/sm_anomaly_cancellation.json) records the verdict `textbook assignment cancels`. `corpus_proposal` is null. `derived_from_geometry` is false. Three identical generations multiply the continuous sums by 3, which keeps them at 0, and multiply the Witten doublet count from 4 to 12. A passing textbook control does not create a geometric assignment. A future assignment from this corpus has to pass the same filter.

What this note constrains:

- Block 4, [`SEAM.md`](SEAM.md). This page does not set the mass in the null-seam yield. The seam does not identify its produced particle with a neutrino.
- Block 3. This page does not select \(\mu(x)=x/\sqrt{1+x^2}\).
- Block 2. The imported fields are available for minimal coupling to the general-relativistic metric outside galaxies. That coupling is part of the import. It is not a solved solar-system test.
