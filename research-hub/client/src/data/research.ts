export type EvidenceStatus =
  | "derived"
  | "computed"
  | "cited"
  | "conditional"
  | "open"
  | "refuted"
  | "superseded";

export type StatusTone = "blue" | "amber" | "red" | "slate";

export const releaseState = {
  version: "Public atlas v0.3",
  researchRelease: "Res Nova · correction cycle 2026-10-15",
  commit: "0cf59a0509801c38e4e9f4c79544b0af2b6fb2b5",
  note: "Aligned with main (0cf59a0) on 2026-10-15: 73 Lean targets, all passing in CI, a₀ = 1.1607 × 10⁻¹⁰ m s⁻² under μ_std, unscreened μ_std fails Cassini, D7 stays open, and the retracted-claim list matches assurance/claims.json.",
  links: {
    github: "https://github.com/Mega-Therion/Res-Nova",
    zenodo: "https://doi.org/10.5281/zenodo.21969121",
    orcid: "https://orcid.org/0009-0001-1303-7190",
    claimRegistry:
      "https://github.com/Mega-Therion/Res-Nova/blob/main/CLAIM_EVIDENCE_LEDGER.md",
    releaseManifest:
      "https://github.com/Mega-Therion/Res-Nova/blob/main/RELEASE_CHECKLIST.md",
  },
};

export const stats = [
  {
    value: "175",
    label: "SPARC galaxies in the T1 baseline",
    detail: "3,391 kinematic points",
  },
  {
    value: "73",
    label: "Lean targets in the current gate",
    detail: "73/73 in CI on 2026-10-16 (verify run 38827607035)",
  },
  { value: "6", label: "evidence states", detail: "from derived to refuted" },
  {
    value: "1",
    label: "research atlas",
    detail: "one place to read, inspect, and reproduce",
  },
];

export const pillars = [
  {
    id: "questions",
    index: "01",
    eyebrow: "The gap",
    title: "Where do the equations stop being enough?",
    description:
      "Res Nova begins with the places where established frameworks remain phenomenologically successful but conceptually or computationally incomplete: galaxy-scale dynamics, covariant completion, and the translation from mathematical structure to observation.",
    status: "open" as EvidenceStatus,
    tone: "amber" as StatusTone,
    links: ["Open problems", "Research timeline"],
  },
  {
    id: "theory",
    index: "02",
    eyebrow: "The construction",
    title: "A bridge from an effective action to measurable dynamics",
    description:
      "The live program studies a corrected interpolation branch, its weak-field behavior, and a genuine AeST covariant completion. The key distinction is not only what can be written down, but what survives the tests that follow.",
    status: "conditional" as EvidenceStatus,
    tone: "amber" as StatusTone,
    links: ["Theory map", "Evidence atlas"],
  },
  {
    id: "evidence",
    index: "03",
    eyebrow: "The test",
    title: "Every bridge must end at a checkable artifact",
    description:
      "Claims are paired with data, code, formal statements, literature, and explicit limitations. A result is never promoted merely because it appears in the corpus; its evidence status travels with it.",
    status: "computed" as EvidenceStatus,
    tone: "blue" as StatusTone,
    links: ["Data & methods", "Publications"],
  },
];

export const claims = [
  {
    id: "CLM-A0-01",
    status: "computed" as EvidenceStatus,
    tone: "blue" as StatusTone,
    domain: "galaxy dynamics",
    title: "T1 measures a₀ across all 175 SPARC galaxies",
    summary:
      "[D] The distance-corrected T1 baseline reports a₀ = 1.1607 × 10⁻¹⁰ m s⁻² across all 175 SPARC galaxies and 3,391 kinematic points, with a 95% interval [9.72, 12.95] × 10⁻¹¹. The non-flow T3 treatment is 1.16306 × 10⁻¹⁰ m s⁻². This is an empirical comparison object, not a derivation from horizon thermodynamics.",
    source:
      "02_galaxy_dynamics/A0_DISTANCE_CORRECTED_2026-09-16.json; A0_PREDICTION_AUDIT_2026-09-16.md",
    limitation:
      "The a₀ → H₀ inversion is ladder-covariant, not an independent prediction; maser-anchored geometric distances are the named path to independence.",
  },
  {
    id: "CLM-MU-01",
    status: "conditional" as EvidenceStatus,
    tone: "amber" as StatusTone,
    domain: "theory",
    title: "The surviving interpolation branch is μstd(x) = x / √(1 + x²)",
    summary:
      "The current state treats μstd as the live branch after the previous μdual(x) = x/(1+x) closure was falsified by its solar-system behavior. The structural uniqueness argument remains conditional on its stated postulates.",
    source:
      "TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md; TARGET_D2_SUPPLEMENT_MU_STD_UNIQUENESS.md",
    limitation:
      "A conditional uniqueness theorem does not explain why nature must choose the postulated structure.",
  },
  {
    id: "CLM-AEST-01",
    status: "conditional" as EvidenceStatus,
    tone: "amber" as StatusTone,
    domain: "covariant completion",
    title: "AeST is the live covariant completion under review",
    summary:
      "The corrected program uses a scalar-sector AeST action with minimal matter coupling. Tensor-speed and selected weak-field claims are separated from unresolved post-Newtonian, screening, and nonlinear cosmology work. In the spherical quasistatic limit, the scalar function whose total law is μ_std is single-valued and meets both static ghost conditions for λ_s < 11.28. D9's function stays the one in use.",
    source: "TARGET_D7_COVARIANT_COMPLETION.md; TARGET_D8_TENSOR_SPEED.md; AEST_TOTAL_SCALAR_CORRESPONDENCE_2026-10-14.md",
    limitation:
      "Downstream calculations inherited from the retired vector/disformal action are not current evidence. A stage-2 search proposed a no-go. That no-go was not adopted. D7 stays open.",
  },
  {
    id: "CLM-LEAN-01",
    status: "derived" as EvidenceStatus,
    tone: "blue" as StatusTone,
    domain: "formal verification",
    title: "Lean checks encoded mathematical statements, not physical adequacy",
    summary:
      "The formalization suite is a machine-checkable boundary around selected definitions and theorems. The repository explicitly records where assumptions enter as structure fields or hypotheses.",
    source: "05_lean_formalization/; THEORY_ASSUMPTION_AUDIT.md",
    limitation:
      "Elaboration and standard axiom footprints do not prove that the encoded definitions model nature.",
  },
  {
    id: "CLM-HORIZON-01",
    status: "conditional" as EvidenceStatus,
    tone: "amber" as StatusTone,
    domain: "horizon selection",
    title: "No principle yet selects the Hubble horizon for a₀",
    summary:
      "[O-sharp] Only the Hubble/apparent-horizon radius with the quasi-static temperature T = ħH/2π fits the distance-robust a₀. That temperature drops a term that is 0.24 today; keeping it (the Kodama–Hayward temperature) gives an excluded a₀, so the step is circular. a₀(z) decides: 1.79× (Hubble), 0.96× (Kodama) or 1.00× (Λ) at z = 1.",
    source: "HORIZON_SELECTION_AUDIT_2026-09-16.md",
    limitation:
      "A local galaxy-channel coupling to the global FLRW expansion remains open and must be tested by high-redshift data.",
  },
  {
    id: "CLM-A0Z-01",
    status: "open" as EvidenceStatus,
    tone: "amber" as StatusTone,
    domain: "redshift test",
    title: "The horizon-tied a₀(z) corollary is constrained, not excluded",
    summary:
      "[O] RC100 (100 galaxies, anchored on non-flow T3) misses both 2-bin 95% corollary intervals in opposite directions: a flat shape where H(z) rises, with Δχ² = 8.9–19.8 stat-only against the Hubble form. Verdict: CONSTRAINED, NOT EXCLUDED. Beam smearing is now tested: its allowed bias moves ln a₀ by at most −0.085 across z = 0.6–2.6, against +1.026 for the Hubble shape. The shape depends on the pressure-support correction: n = −0.28 at the published Burkert scale, and the Hubble shape enters the 95% interval only at three times that scale or more.",
    source:
      "A0_HIGHZ_MEASUREMENT_2026-09-16.md; A0_HIGHZ_COROLLARY_COMPARISON_2026-09-17.md; scripts/a0_highz_resolution_test.py; scripts/a0_highz_pressure_scale_test.py",
    limitation:
      "The live two-sided falsifier needs geometric cross-method calibration, an fDM prior independent of redshift, and a measured pressure-support scale. A first literature pass points to a correction below Burkert's, not three times above it.",
  },
  {
    id: "CLM-SPARC-TIER0",
    status: "computed" as EvidenceStatus,
    tone: "blue" as StatusTone,
    domain: "galaxy dynamics",
    title: "The horizon anchor fits SPARC worse than the literature a₀",
    summary:
      "[E] Under one μ_std, PARAMETER_LEDGER.json reports a tier-0 median reduced χ² of 11.08 for the horizon anchor and 9.93 for the literature a₀ = 1.2×10⁻¹⁰ m s⁻², on 3375 points. The comparison is the scale, not a second interpolating function.",
    source:
      "02_galaxy_dynamics/PARAMETER_LEDGER.json; 02_galaxy_dynamics/SPARC_MU_STD_RECOMPUTE_2026-09-12.md",
    limitation:
      "Tier 0 fixes distance and inclination. It is not the tier-1 nuisance fit, where the two medians are 3.36 and 3.41.",
  },
  {
    id: "CLM-CASSINI-01",
    status: "refuted" as EvidenceStatus,
    tone: "red" as StatusTone,
    domain: "solar system",
    title: "Unscreened μ_std fails the Cassini external-field test",
    summary:
      "[E] At the live a₀, unscreened μ_std gives an external-field quadrupole of 19–20 × 10⁻²⁷ s⁻², +9.7σ to +10.2σ against the 2026 bound. A phenomenological screen S = 1/(1+η²) can pass. Taking η from an external field keeps the light cone luminal, but one field cannot give the Sun and the Milky Way their different η at the same point. A screen on the tidal coordinate passes Cassini and leaves SPARC unchanged in a QUMOND form, at the price of a third constant fixed by the Solar System.",
    source:
      "02_galaxy_dynamics/CASSINI_EFE_QUADRUPOLE_2026-09-27.md; 06_foundations/SETA_EXTERNAL_FIELD_SCREENING.md; 02_galaxy_dynamics/TIDAL_SCREENING_2026-10-15.md",
    limitation:
      "The failure is of the unscreened branch. It is not a measurement of a screened covariant theory, because that theory is not in hand.",
  },
  {
    id: "CLM-MU-RETIRED",
    status: "superseded" as EvidenceStatus,
    tone: "red" as StatusTone,
    domain: "correction history",
    title: "μdual(x) = x/(1+x) is preserved as a falsified branch",
    summary:
      "The prior closure remains in the archive so the correction is auditable. It is not part of the live theory and must not be used to support current solar-system or redshift claims.",
    source: "CURRENT_STATE_READ_THIS_FIRST.md; CLAIM_EVIDENCE_LEDGER.md",
    limitation: "Historical presence is provenance, not endorsement.",
  },
];

export const claimRegistryState = {
  source: "CLAIM_EVIDENCE_LEDGER.md",
  release: releaseState.researchRelease,
  commit: releaseState.commit,
  snapshotDate: "2026-10-13",
  totalClaims: claims.length,
  statuses: {
    derived: claims.filter(claim => claim.status === "derived").length,
    computed: claims.filter(claim => claim.status === "computed").length,
    conditional: claims.filter(claim => claim.status === "conditional").length,
    open: claims.filter(claim => claim.status === "open").length,
    refuted: claims.filter(claim => claim.status === "refuted").length,
    superseded: claims.filter(claim => claim.status === "superseded").length,
  },
} as const;

/** Claims the registry (assurance/claims.json) marks `retracted`, summarized by hand.
 *  A test (retracted-claims.test.ts) fails if this list and the registry disagree. */
export const retractedClaims = [
  { id: "CLM-05", title: "The 382-parameter SPARC fit is not the current fit", detail: "It is historical. The matched Tier 1 comparison uses 374 nuisance parameters." },
  { id: "CLM-15", title: "The anti-drift gate u ≥ γ ⇔ χ ≥ θ is false", detail: "The steady-state coherence is not monotonic; θ is a ceiling on coherence, not a gate." },
  { id: "CLM-D3-01", title: "\"1137× below Cassini\"", detail: "A category error: 1 − μ and γ − 1 are not comparable. The live figure is a MOND correction of about 2 × 10⁻⁸ at Earth." },
  { id: "CLM-D3-03", title: "Vainshtein screening puts Q₂ 119× below the Cassini bound", detail: "Retracted 2026-09-30: computed with the retired F_dual action, and no GW170817-safe Vainshtein screen is available." },
  { id: "CLM-D3-05", title: "γ = β = 1 with Cassini and MESSENGER margins", detail: "Void: derived for an Einstein-aether action that was not the AeST action." },
  { id: "CLM-D6-03", title: "A strong-coupling scale of about 10⁻¹⁰ eV", detail: "A unit error. The correct scale is about 1.8 meV, a 110 μm range, which is lab-accessible." },
  { id: "CLM-D7-01", title: "The RMOND action with F_dual is written and verified", detail: "Superseded 2026-09-12: written against a vector field, not the scalar AeST field." },
  { id: "CLM-D7-02", title: "Background Friedmann equations are unmodified", detail: "Void 2026-09-12: the calculation it rested on does not apply under the corrected AeST action." },
  { id: "CLM-D7-03", title: "Linear screening factor F″/F′ ≈ 0.00233", detail: "Void 2026-09-12: computed from a field the action does not contain." },
  { id: "CLM-D7-05", title: "Natural O(1) couplings satisfy all constraints", detail: "Void 2026-09-12: those couplings do not exist in the corrected AeST action." },
  { id: "CLM-D7-06", title: "Exact PPN γ, β for specific couplings", detail: "Superseded: γ = 1 follows from Ψ = Φ in the Skordis–Złośnik embedding, not from couplings." },
  { id: "CLM-D9-01", title: "The D9 embedding normalization", detail: "Corrected 2026-09-12: a factor-of-2 prefactor disagreement, and ã₀ had been conflated with a₀." },
  { id: "CLM-Z-R1", title: "κ = 0.9539 emerges from the theory", detail: "Retracted by the 2026-10-11 Zenodo audit: κ = √(θ(2 − θ)) at θ = 0.70 is an input relation, and ξ is tuned to it." },
  { id: "CLM-Z-R2", title: "The acceleration relation is derived, and the SPARC fits use no per-galaxy freedom", detail: "Retracted by the 2026-10-11 Zenodo audit: μ is an irreducible input and the live comparison is the μ_std parameter ledger." },
  { id: "CLM-Z-R3", title: "θ or χ equals 1/√2", detail: "Retracted by the 2026-10-11 Zenodo audit: θ = 0.70 is the settled input; 1/√2 is the band's lower wall." },
];

export const workstreams = [
  {
    id: "foundations",
    label: "Foundations",
    short:
      "Definitions, assumptions, and the boundary of what is being claimed.",
    status: "conditional" as EvidenceStatus,
    progress: 72,
    color: "#79d7e8",
  },
  {
    id: "weak-field",
    label: "Weak-field dynamics",
    short:
      "Interpolation functions, AQUAL behavior, and galaxy-scale observables.",
    status: "computed" as EvidenceStatus,
    progress: 68,
    color: "#82aaff",
  },
  {
    id: "covariant",
    label: "Covariant completion",
    short:
      "AeST action, tensor speed, stability, and post-Newtonian constraints.",
    status: "conditional" as EvidenceStatus,
    progress: 46,
    color: "#f1b86a",
  },
  {
    id: "cosmology",
    label: "Cosmological sector",
    short:
      "Background and linear behavior, with nonlinear structure formation open.",
    status: "open" as EvidenceStatus,
    progress: 34,
    color: "#c49af7",
  },
  {
    id: "verification",
    label: "Formal verification",
    short:
      "Machine-checkable statements, target inventories, and assumption audits.",
    status: "derived" as EvidenceStatus,
    progress: 78,
    color: "#75d6a0",
  },
];

export const publications = [
  {
    type: "Canonical manuscript",
    year: "2026",
    title:
      "Dual-Channel Variational Closure, Covariant Completion, and a Reproducible SPARC Benchmark",
    summary:
      "The current manuscript lineage, undergoing correction and scope alignment around the live μstd/AeST state.",
    href: "https://github.com/Mega-Therion/Res-Nova",
    tag: "In correction",
  },
  {
    type: "Formalization",
    year: "2026",
    title: "Lean 4 verification suite and assumption audit",
    summary:
      "A machine-checkable layer for selected definitions and theorems, paired with explicit documentation of hypotheses.",
    href: "https://github.com/Mega-Therion/Res-Nova/tree/main/05_lean_formalization",
    tag: "Open source",
  },
  {
    type: "Research release",
    year: "2026",
    title: "Res Nova evidence and reproducibility corpus",
    summary:
      "Claims, datasets, verification runs, empirical scripts, correction records, and release metadata.",
    href: "https://doi.org/10.5281/zenodo.21969121",
    tag: "Archive",
  },
];

export const datasets = [
  {
    name: "SPARC galaxy dynamics",
    scope: "175 galaxies · 3,391 kinematic points",
    artifact:
      "A0_DISTANCE_CORRECTED_2026-09-16.json · A0_PREDICTION_AUDIT_2026-09-16.md",
    provenance:
      "T1 baseline over all 175 SPARC galaxies; T3 non-flow comparison is 1.16306 × 10⁻¹⁰ m s⁻².",
    color: "#79d7e8",
  },
  {
    name: "Intermediate-redshift test",
    scope: "RC100 · 100 galaxies · two redshift bins",
    artifact:
      "A0_HIGHZ_MEASUREMENT_2026-09-16.md · A0_HIGHZ_COROLLARY_COMPARISON_2026-09-17.md",
    provenance:
      "Horizon corollary is constrained, not excluded; calibration and beam-smearing limits remain explicit.",
    color: "#f1b86a",
  },
  {
    name: "Lean formalization",
    scope: "66 current gate targets",
    artifact: "05_lean_formalization/verify_all_proofs.sh",
    provenance:
      "Pinned modules, target inventory, verification runs, and assumption audit.",
    color: "#82aaff",
  },
];

export const timeline = [
  {
    date: "2026 · 08",
    title: "The corpus becomes an auditable research package",
    body: "Claim ledgers, verification runs, release checklists, and formal inventories become first-class artifacts.",
  },
  {
    date: "2026 · 09 · 12",
    title: "The correction changes the live branch",
    body: "The μdual solar-system failure is documented, the old covariant downstream is retired, and μstd becomes the surviving branch.",
  },
  {
    date: "2026 · 09 · 16",
    title: "The research state is realigned",
    body: "The current-state documents separate derived algebra, empirical measurements, conditional bridges, open problems, and historical results.",
  },
  {
    date: "2026 · 09 · 17",
    title: "The horizon question is sharpened",
    body: "The FLRW apparent horizon becomes the candidate home of the Hubble-form scale, while the RC100 high-z test becomes a constrained two-sided falsifier rather than an exclusion.",
  },
  {
    date: "2026 · 10 · 03",
    title: "Cassini and the tier-0 comparison are stated up front",
    body: "Unscreened μ_std fails Cassini. D7 stays open: a proposed no-go was not adopted. On SPARC, the horizon anchor's tier-0 median reduced χ² is 11.08 and the literature a₀ is 9.93, same μ_std.",
  },
  {
    date: "Now",
    title: "A public atlas makes the program legible",
    body: "This site is the cold-reading layer: a map from questions to theory to evidence to the next test.",
  },
];

export const statusMeta: Record<
  EvidenceStatus,
  { label: string; tone: StatusTone; description: string }
> = {
  derived: {
    label: "[D] Derived",
    tone: "blue",
    description: "Follows from stated definitions and assumptions.",
  },
  computed: {
    label: "[D] Computed",
    tone: "blue",
    description: "Generated from a declared dataset and analysis procedure.",
  },
  cited: {
    label: "[C] Cited",
    tone: "slate",
    description: "Imported from external literature or public source material.",
  },
  conditional: {
    label: "[C] Conditional",
    tone: "amber",
    description: "Depends on an explicit model choice or unresolved premise.",
  },
  open: {
    label: "[O] Open",
    tone: "amber",
    description: "A live question, pending derivation, data, or simulation.",
  },
  refuted: {
    label: "[X] Refuted",
    tone: "red",
    description: "A contradiction or failed test is preserved in the record.",
  },
  superseded: {
    label: "[X] Superseded",
    tone: "red",
    description: "Historical state retained for provenance, not current use.",
  },
};

export const chartData = [
  { label: "Tier 0 median", value: 11.08, live: 11.08, comparison: 9.93 },
  { label: "Tier 1 median", value: 3.36, live: 3.36, comparison: 3.41 },
  { label: "Tier 1 mean", value: 5.63, live: 5.63, comparison: 5.63 },
];

export const a0Measurement = {
  t1: {
    label: "T1 · all 175 SPARC",
    value: 1.1607e-10,
    lo: 9.72e-11,
    hi: 12.95e-11,
    n: "3,391 points",
  },
  t3: { label: "T3 · non-flow", value: 1.16306e-10 },
} as const;

export function muStd(x: number) {
  return x / Math.sqrt(1 + x * x);
}

export function muDual(x: number) {
  return x / (1 + x);
}

export function horizonScale(z: number, omegaM = 0.3, omegaL = 0.7) {
  return Math.sqrt(omegaM * (1 + z) ** 3 + omegaL);
}

export function gMondStd(gbar: number, a0 = a0Measurement.t1.value) {
  if (gbar <= 0) return 0;
  const y = gbar / a0;
  const u = (y * y + y * Math.sqrt(y * y + 4)) / 2;
  return a0 * Math.sqrt(Math.max(0, u));
}

export function gMondDual(gbar: number, a0 = a0Measurement.t1.value) {
  if (gbar <= 0) return 0;
  return 0.5 * (gbar + Math.sqrt(gbar * gbar + 4 * gbar * a0));
}

export function gDeepMond(gbar: number, a0 = a0Measurement.t1.value) {
  return Math.sqrt(Math.max(0, gbar * a0));
}

export const glossary = [
  {
    term: "AQUAL",
    definition:
      "A nonlinear weak-field formulation used here as the bridge between an effective action and galaxy-scale acceleration.",
  },
  {
    term: "AeST",
    definition:
      "The corrected covariant completion under review in the live research state.",
  },
  {
    term: "SPARC",
    definition:
      "Spitzer Photometry and Accurate Rotation Curves, a public galaxy rotation-curve dataset.",
  },
  {
    term: "Evidence status",
    definition:
      "A label describing how a claim is supported, not a score of how important it sounds.",
  },
];
