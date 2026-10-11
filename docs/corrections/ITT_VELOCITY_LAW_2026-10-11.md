# Correction: the velocity law in "Information Tension Theory: A Geometric Replacement for Dark Matter"

**Status:** correction record, 2026-10-11. Errata entry E-15 in `docs/ERRATA.yaml`.
**Author:** R.W. Yett. Recorded by the 2026-10-11 audit of the published Zenodo claims.

**Affected record.** The paper of that title, Zenodo concept DOI 10.5281/zenodo.20027634, and every record that carries `Information_Tension_Draft.tex`.

**What it states.** The galactic rotation section writes

$$v_{\text{yett}} = v_{\text{newton}} \times T(r), \qquad T(r) = 1 + \frac{1}{0.5\,\chi_{\text{local}}}.$$

**The correction.** $T(r)$ here carries the formula of $\tau = 1 + 2/\chi_{\text{local}}$. Where the τ law is stated together with its acceleration relation (the Ars Magna master spine, §8.2, and the galactic technical note, which defines $T(r)^2 = a_{\text{tot}}/a_{\text{bary}}$), that relation is $a_{\text{tot}} = g_N\,\tau$. Circular motion then gives

$$v^2 = r\,a_{\text{tot}} = r\,g_N\,\tau = v_N^2\,\tau \quad\Longrightarrow\quad v = v_N\sqrt{\tau}.$$

The published form $v = v_N\,\tau$ overstates the velocity by a factor $\sqrt{\tau}$.

**Standing.** The τ law is historical. The live galaxy law is the quasistatic AQUAL relation with $\mu_{\text{std}}$ (`CURRENT_STATE_READ_THIS_FIRST.md`; `TARGET_D7_COVARIANT_COMPLETION.md`). This record exists so that the published form is not cited as current. The entity "v_N * T(r) velocity law" in `scripts/dead_branch_scan.py` fails the gate if the published form reappears on a live surface.
