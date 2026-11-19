# Pre-registration addendum: D10 with measured gas density profiles (2026-11-19, before any number)
The accretion-cap test failed narrowly (8/12), with the scatter tracking the assumed cored gas profile. This addendum replaces that assumed profile with **measured** deprojected n_e(r) from ACCEPT (Cavagnolo et al. 2009), for the 11 D10 clusters in ACCEPT (RXC-J0532.9-3701 is absent).

**Gas model.**
- ρ_gas = μ_e m_p n_e, with μ_e = 1.17.
- Mass is integrated over the measured shells.
- Beyond the outermost measured radius, n_e ∝ r^(−β), with β fitted to the bins outside half the maximum measured radius.
- Stars: 0.015 M₅₀₀ distributed in proportion to the gas.
- The catalogue f_gas is not used; the gas mass comes from the measured profile.
- Everything else as in `accretion.py` (μ_std, Φ(r_v) = 0, shooting).

**Report.** Gas mass inside r₅₀₀ compared with the catalogue f_gas·M₅₀₀ (a sanity check), plus static R and supply-capped R.

**Decision** (same fraction as before, 75%):
- **Closes** if median R ∈ [0.8, 1.25] with ≥ 9/11 in [0.7, 1.4], for the capped model; the static model is reported the same way.
- Otherwise **fails**.
