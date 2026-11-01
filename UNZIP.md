# Reverse unzip

Date: 2026-10-31. New construction. It is not on [`UNIDEX.md`](UNIDEX.md). It does not modify the galaxy axiom, the seam, or the imported Standard Model.

The arrow used here is the one already marked conjecture in the corpus: a compressed initial state, and time as the unzip. The algorithm is the reverse of a projection.

Zip throws away every coordinate the screen does not record. Unzip puts back the completion that minimizes the joint energy of a standard normal prior and the screen likelihood. For one screen that keeps \(x\) and \(y\) and deletes \(z\), that completion is the mode of the variational free energy of a deterministic recognition density. The deleted coordinate stays at the prior value \(0\).

Script: `scripts/reverse_unzip.py`. Run on 2026-10-31, exit 0. State \((1, 2, 3)\), noise variance \(10^{-6}\).

| Step | Result |
| :--- | :--- |
| One screen records | \((1, 2)\) |
| Unzip returns | \((0.999999000001,\ 1.999998000002,\ 0)\) |
| Energy at that unzip | \(2.4999975000025\) |
| Energy if the deleted \(3\) is written in by hand | \(6.9999975000025\) |
| Penalty | \(4.5 = \tfrac12 \times 3^2\) |

The penalty is the prior cost of inventing the lost coordinate. The first shadow does not contain it, so the decoder does not restore it.

A second screen that records all three coordinates returns \(z = 2.999997000003\). That screen is supplied. It is not chosen by the first shadow, and no preference over screens is in the script. Until a preference is written down as its own input, there is no active-inference step, only the unzip of whatever screen was handed in.

## Two parity rows

The two rows are literals at the top of `scripts/reverse_unzip.py`, fixed before the observation is formed. Same state, same screen, same variance. Run on 2026-10-31, exit 0. The one-view table above is unchanged by that run.

| Check | Row | Distance to the screen's row-span | Rank | Nullity | Unzip of \(z\) | Penalty |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Blind to \(z\) | \((1,\ 0,\ 0)\) | \(0\) | \(2\) | \(1\) | \(0\) | \(4.5\) |
| Sees \(z\) | \((0,\ 0,\ 1)\) | \(1\) | \(3\) | \(0\) | \(2.999997000003\) | \(4.499995499784859 \times 10^{-6}\) |

The blind row repeats the screen's record of \(x\). The stacked matrix has singular values \((1.4142135623730951,\ 1,\ 0)\). The unzip leaves \(z\) at \(0\), and writing \(3\) into that coordinate still costs \(4.5\).

The seeing row is the deleted coordinate. The stacked matrix has singular values \((1,\ 1,\ 1)\). The unzip returns \(z = 2.999997000003\), and the penalty for moving that coordinate from the mode to \(3\) prints as \(4.499995499784859 \times 10^{-6}\). The value \(4.5 \times 10^{-6} / (1 + 10^{-6})\) sits \(2.2 \times 10^{-16}\) above that print.

The screen and the seeing row meet when the stack has nullity \(0\). This score does not select \(\mu_{\mathrm{std}}\), \(\eta\), \(g_*\), or a particle mass.
