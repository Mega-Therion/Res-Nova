/* ========================================== */
/* RESEARCH PAPERS CAROUSEL + AI EXPLAINER    */
/* ========================================== */

// --- PAPER DATABASE WITH KNOWLEDGE BASE ---
const PAPERS = [
  {
    id: 'dual-channel',
    title: 'Dual-Channel Variational Closure, Covariant Completion, and a Reproducible SPARC Benchmark',
    subtitle: 'Physical Review D • v1.9.0',
    icon: '🌀',
    coverGradient: 'linear-gradient(135deg, #0369a1 0%, #0c4a6e 50%, #082f49 100%)',
    orbColor: '#38bdf8',
    tags: [
      { label: 'PRD Submission', class: 'tag-proved' },
      { label: 'Lean 4 Verified', class: 'tag-proved' },
      { label: 'SPARC Empirical', class: 'tag-empirical' }
    ],
    meta: { version: 'v1.9.0', date: 'Sep 2026', doi: '10.5281/zenodo.21539453', modules: '18 Lean modules' },
    abstract: 'We investigate the dual-channel AQUAL potential F_dual(x) = ½x² − x + ln(1+x), demonstrate that its simple constitutive ratio μ(x) = x/(1+x) is ruled out by solar-system constraints, and establish the viable covariant completion under μ_std(x) = x/√(1+x²) alongside a reproducible SPARC benchmark.',
    highlights: [
      { icon: '⚖️', title: 'Dual-Channel Closure', desc: 'F_dual(x) = ½x² − x + ln(1+x) uniquely determined by 4 structural constraints' },
      { icon: '🔭', title: 'SPARC 171 Galaxies', desc: 'a₀ = (1.116 ± 0.161) × 10⁻¹⁰ m/s² across 3,391 kinematic points' },
      { icon: '👻', title: 'Ghost-Free Completion', desc: 'c_T = c verified — tensor speed luminal, no tachyonic modes' },
      { icon: '🧮', title: 'Lean 4 Certified', desc: '18 modules, 0 sorry, 0 custom axioms — machine-checked proofs' }
    ],
    equations: [
      '\\mathcal{F}_{\\text{dual}}(x) = \\tfrac{1}{2}x^2 - x + \\ln(1+x)',
      '\\mu(x) = \\frac{\\mathcal{F}\'(x)}{x} = \\frac{x}{1+x}',
      '\\mu_{\\text{std}}(x) = \\frac{x}{\\sqrt{1+x^2}}',
      'a_0 = (1.116 \\pm 0.161) \\times 10^{-10}\\,\\text{m/s}^2'
    ],
    kb: [
      {
        keywords: ['dual', 'channel', 'closure', 'fdual', 'f_dual', 'potential', 'aqual'],
        q: 'What is the dual-channel closure?',
        a: 'The **dual-channel AQUAL potential** is the heart of the paper. It\'s defined as:\n\n$$\\mathcal{F}_{\\text{dual}}(x) = \\tfrac{1}{2}x^2 - x + \\ln(1+x)$$\n\nwhere $x = |\\nabla\\Phi|/a_0$ is the dimensionless halo gradient. This function is **uniquely determined** by four structural constraints: (1) constitutive-relation form, (2) Padé[1/1] minimality, (3) MOND boundary conditions, and (4) dual-channel splitting. It balances **bulk kinetic flux** against **horizon relative entropy dissipation** — two physical channels that must both be satisfied. The key insight is that a single-channel approach produces a no-go theorem (inverted limits), so you need exactly two channels to close the theory.'
      },
      {
        keywords: ['mu', 'interpolation', 'function', 'constitutive', 'ratio', 'simple', 'x/(1+x)'],
        q: 'What is the interpolation function μ(x)?',
        a: 'The **interpolating function** μ(x) connects the Newtonian and deep-MOND regimes. The simple form derived from the dual-channel closure is:\n\n$$\\mu(x) = \\frac{x}{1+x}$$\n\nHowever, this was **ruled out** by solar-system constraints — it produces a constant, unscreened anomalous acceleration that predicts Mercury perihelion precession ~10³× the observed bound (INPOP10a/EPM2011). The **corrected viable interpolation** is:\n\n$$\\mu_{\\text{std}}(x) = \\frac{x}{\\sqrt{1+x^2}}$$\n\nThis standard form doesn\'t have the constant-offset failure mode and passes solar-system tests. The paper is transparent about this retraction — the original μ = x/(1+x) claim was formally retracted in a correction subsection.'
      },
      {
        keywords: ['sparc', 'galaxy', 'benchmark', 'kinematic', 'rotation', 'curve', 'fit', 'chi'],
        q: 'How does the SPARC benchmark work?',
        a: 'The **SPARC benchmark** is the empirical backbone of the paper. SPARC (Spitzer Photometry and Accurate Rotation Curves) provides data for 175 galaxies with measured rotation curves. The theory fits **171 galaxies** (3,391 kinematic data points) using just **176 parameters**: 175 disk mass-to-light ratios (Υ_disk) plus one global acceleration scale a₀. The result:\n\n$$a_0 = (1.116 \\pm 0.161) \\times 10^{-10}\\,\\text{m/s}^2$$\n\nThe median in-sample χ²_data/N_g = 2.92. A **5-fold cross-validation** gives out-of-sample test median χ² = 14.33, establishing that the fit generalizes rather than overfitting. This is remarkable: MOND-like theories typically need dark matter halos with 2-3 free parameters *per galaxy* — here, a single global a₀ plus per-galaxy mass-to-light ratios suffice.'
      },
      {
        keywords: ['ghost', 'free', 'tachyon', 'tensor', 'speed', 'ct', 'luminal', 'gw', 'gravitational wave'],
        q: 'What does ghost-free completion mean?',
        a: 'A **ghost-free completion** means the relativistic extension of the theory has no tachyonic (faster-than-light) or ghost (negative-energy) modes. This is verified in Lean 4:\n\n- **Tensor speed**: $c_T = c$ exactly — gravitational waves propagate at the speed of light, in perfect concordance with GW170817 ($|c_T/c_\\gamma - 1| < 10^{-15}$)\n- **Characteristic speeds** are strictly real and positive — no tachyonic ghosts\n- This result is **independent of the interpolation function choice** — it holds for both μ = x/(1+x) and μ_std = x/√(1+x²)\n\nThe disformal metric coupling is falsified: any $B(\\phi) \\neq 0$ would split the lightcone ($|c_T/c_\\gamma - 1| \\gg 10^{-15}$), contradicting LIGO/Virgo. So the completion must set $B = 0$, preserving $c_T = c_\\gamma$.'
      },
      {
        keywords: ['lean', 'formal', 'verification', 'proof', 'machine', 'checked', 'sorry', 'axiom'],
        q: 'How is the theory formally verified?',
        a: 'The formal core is **machine-checked in Lean 4** — a proof assistant where every step is verified by the kernel. The verification comprises:\n\n- **18 modules** (expanded from 8 in earlier versions)\n- **0 sorry** — no skipped or assumed proofs\n- **0 custom axioms** — only standard Lean axioms (propext, Classical.choice, Quot.sound)\n- Verified under Lean v4.33.0-rc1 with Mathlib\n\nKey modules include:\n- `DualChannelDerivation.lean` — proves F_dual gives μ = x/(1+x)\n- `TensorSpeed.lean` — proves |c_T/c_γ − 1| ≫ 10⁻¹⁵ when B(ϕ) ≠ 0\n- `SkordisZlosnikEmbedding.lean` — proves J(𝒴) matching with zero residual\n- `MuProjection.lean` — proves the μ function properties\n\nA cold-machine verification (fresh container, genuine network fetch, no pre-existing caches) confirmed all 32 declared targets pass with exit status 0.'
      },
      {
        keywords: ['skordis', 'zlosnik', 'embedding', 'parent', 'covariant', 'rmond'],
        q: 'What is the Skordis-Zlosnik embedding?',
        a: 'The **Skordis-Złosnik RMOND** theory is a 4D covariant scalar-vector-tensor theory that serves as the **parent embedding** for the dual-channel closure. It couples to a unit timelike vector field $A^\\mu$ ($A_\\mu A^\\mu = -1$) and scalar $\\phi$.\n\nThe key result is that specifying the Skordis-Złosnik free function as $\\mathcal{F}(\\mathcal{K}) = \\mathcal{F}_{\\text{dual}}(\\sqrt{\\mathcal{K}})$:\n\n- Leaves the **Friedmann background unmodified**\n- Places the cosmological background on the **Newtonian branch**\n- Gives a linear screening ratio $\\mathcal{F}\'\'/\\mathcal{F}\' \\approx 0.00233$\n- The ~76× structure overproduction of uniform MOND falls to **0.23%** in linear growth\n\nThis is proved in Lean 4 with **zero residual** — the dual-channel closure fits perfectly into the parent theory. The embedding preserves $c_T = c_\\gamma$ and $\\Phi = \\Psi$ (no gravitational slip).'
      },
      {
        keywords: ['a0', 'acceleration', 'scale', 'constant', 'value', 'mond'],
        q: 'What is the acceleration scale a₀?',
        a: 'The **acceleration scale** $a_0$ is the fundamental constant of MOND-like theories — it marks the transition between Newtonian gravity (high acceleration) and the deep-MOND regime (low acceleration). From the SPARC fit:\n\n$$a_0 = (1.116 \\pm 0.161) \\times 10^{-10}\\,\\text{m/s}^2$$\n\nThis is close to $cH_0/(2\\pi) \\approx 1.20 \\times 10^{-10}$ m/s², suggesting a deep connection to cosmology. In the deep-MOND regime ($g \\ll a_0$), the effective acceleration becomes:\n\n$$g = \\sqrt{g_{\\text{bar}} \\cdot a_0}$$\n\nThis produces flat rotation curves naturally: $v_{\\text{flat}} = (GMa_0)^{1/4}$. The paper also tested whether $a_0$ evolves with redshift using 20 intermediate-redshift galaxies — the result was **inconclusive** ($\\Delta\\chi^2 = +4.24$, 2.06σ), so this remains an open question.'
      },
      {
        keywords: ['correction', 'retraction', 'solar', 'system', 'mercury', 'perihelion', 'falsif'],
        q: 'What was retracted in the paper?',
        a: 'The paper contains a **transparent retraction** of the original solar-system claim. The simple interpolation $\\mu(x) = x/(1+x)$ produces a **constant, unscreened anomalous acceleration** that predicts Mercury perihelion precession ~10³× the observed bound (from INPOP10a/EPM2011 ephemerides).\n\nThis is a genuine falsification — **Vainshtein screening cannot fix it** because there\'s no perturbation to act on for a constant offset. The corrected interpolation $\\mu_{\\text{std}}(x) = x/\\sqrt{1+x^2}$ does not have this failure mode.\n\nAdditionally, an earlier $5.9\\sigma$ redshift-evolution figure under $\\mu_{\\text{dual}}$ was **retracted as closure-dependent** — it depended on the falsified interpolation function. The inconclusive result under $\\mu_{\\text{std}}$ ($\\Delta\\chi^2 = +4.24$, 2.06σ) is the honest current state. This transparency is a feature of the paper\'s epistemic standard.'
      },
      {
        keywords: ['open', 'problem', 'future', 'limitation', 'cosmological', 'cluster', 'ppn', 'structure'],
        q: 'What remains open?',
        a: 'The paper is explicit about its open problems:\n\n- **Non-linear structure formation**: The linear screening ratio (~0.23%) is promising, but full N-body simulations at non-linear scales are not yet done\n- **Exact PPN parameters**: The Parameterized Post-Newtonian expansion needs precise computation beyond the Cassini γ_PPN = 1.00000 check\n- **Cluster scales**: The theory is tested on galactic scales (SPARC) but galaxy clusters remain a challenge — the missing mass at cluster scales is not fully addressed\n- **Cosmological horizon boundary**: The FLRW decoupling ($\\nabla_\\mu \\phi = 0$) and horizon entropy density $\\Omega_\\Lambda = \\ln 2 \\approx 0.693$ are quarantined as asymptotic boundary conditions\n- **Redshift evolution of a₀**: The pre-registered test was inconclusive (2.06σ)\n\nThese are marked as tier [O] (Open) in the epistemic ledger, not hidden or hand-waved.'
      }
    ]
  },

  {
    id: 'ars-magna',
    title: 'The Law of Geometrically Ordered Dynamics',
    subtitle: 'Canonical Monograph • Ars Magna v3.0',
    icon: '📜',
    coverGradient: 'linear-gradient(135deg, #7c2d12 0%, #92400e 40%, #422006 100%)',
    orbColor: '#f59e0b',
    tags: [
      { label: 'Monograph', class: 'tag-theory' },
      { label: 'Unification', class: 'tag-theory' },
      { label: 'Lean 4', class: 'tag-proved' }
    ],
    meta: { version: 'v3.0', date: 'Aug 2026', doi: '—', modules: '17 Lean modules' },
    abstract: 'A mathematical and empirical unification of Information Tension Theory, Gravitation, and Gauge Holonomy. Establishes the vacuum geometry on V₂(ℝ³) ≅ SO(3), derives exactly three matter generations from Cartan triality, and embeds an E₈ ⊃ Spin(8) Yang-Mills gauge sector.',
    highlights: [
      { icon: '🌐', title: 'Vacuum Geometry', desc: 'V₂(ℝ³) ≅ SO(3) — Stiefel manifold as the fundamental substrate' },
      { icon: '⚖️', title: 'Cartan Triality', desc: 'Out(Spin(8)) ≅ S₃ → ℤ₃ gives exactly 3 matter generations' },
      { icon: '🔮', title: 'E₈ Gauge Unification', desc: 'E₈ ⊃ Spin(8) Yang-Mills sector with topological θ-term' },
      { icon: '🧬', title: 'Chiral Resolution', desc: 'Fermion generations via Cartan triality on V₂(ℝ³)' }
    ],
    equations: [
      '\\mathcal{M}_{\\text{vac}} = V_2(\\mathbb{R}^3) \\cong SO(3)',
      '\\text{Out}(\\text{Spin}(8)) \\cong S_3 \\implies \\mathbb{Z}_3 \\text{ (3 generations)}',
      'a_0 = \\frac{cH_0}{2\\pi} \\approx 1.20 \\times 10^{-10}\\,\\text{m/s}^2',
      '\\chi_Y = \\frac{1}{\\sqrt{2}}, \\quad \\kappa_Y = \\sqrt{\\theta(2-\\theta)} \\approx 0.9539'
    ],
    kb: [
      {
        keywords: ['vacuum', 'geometry', 'stiefel', 'v2', 'so(3)', 'substrate', 'manifold'],
        q: 'What is the vacuum geometry?',
        a: 'The **vacuum geometry** is the Stiefel manifold $V_2(\\mathbb{R}^3)$ — the space of orthonormal 2-frames in $\\mathbb{R}^3$. This is isomorphic to $SO(3)$, the rotation group in 3D.\n\nThis is a radical departure from standard particle physics, which typically uses Minkowski space or Calabi-Yau manifolds. The Stiefel manifold provides a **natural chiral structure** — the orientation of a 2-frame in 3D is inherently handed, which is key to understanding parity violation and the chirality of the weak force.\n\nThe earlier formulation used $V_{240}(\\mathbb{R}^{57,600})$ (related to $E_8$ root counts), but this was **retired** in favor of $V_2(\\mathbb{R}^3)$ via Cartan triality — a structural, not cosmetic, change.'
      },
      {
        keywords: ['cartan', 'triality', 'generation', 'three', 'matter', 'fermion', 's3', 'spin(8)'],
        q: 'How does Cartan triality give 3 generations?',
        a: '**Cartan triality** is an exceptional symmetry of $\\text{Spin}(8)$ — the double cover of $SO(8)$. The outer automorphism group is:\n\n$$\\text{Out}(\\text{Spin}(8)) \\cong S_3$$\n\nThe symmetric group $S_3$ has a normal subgroup $\\mathbb{Z}_3$ (cyclic group of order 3). This $\\mathbb{Z}_3$ is the **exact origin of three matter generations** — the threefold cyclic permutation of the triality group maps to the three generations of fermions.\n\nThis is not a fitting or a coincidence — it\'s a **structural prediction** of the geometry. The three generations arise because $\\text{Spin}(8)$ has a unique triality symmetry that no other Spin group possesses. The fermions are realized via:\n\n$$\\sum_{g=1}^{3} \\bar{\\psi}_g \\left[ i e^\\mu_a \\gamma^a \\left( \\partial_\\mu + \\frac{1}{4}\\omega_\\mu^{bc}\\sigma_{bc} - igA_\\mu \\right) - M_{\\text{Pl}} e^\\phi e^{-\\lambda_g/\\kappa_Y} \\psi_g \\right]$$\n\nwhere $g = 1, 2, 3$ indexes the generations.'
      },
      {
        keywords: ['e8', 'gauge', 'yang', 'mills', 'unification', 'spin(8)', 'holonomy'],
        q: 'What is the E₈ gauge sector?',
        a: 'The theory embeds an **$E_8 \\supset \\text{Spin}(8)$ Yang-Mills gauge sector** — one of the most beautiful structures in mathematics. $E_8$ is the largest exceptional Lie group, with dimension 248. It contains $\\text{Spin}(8)$ as a maximal subgroup.\n\nThe gauge sector includes:\n\n$$-\\frac{1}{4g^2(\\mu)} g^{\\mu\\alpha} g^{\\nu\\beta} \\text{Tr}(F_{\\mu\\nu}^{E_8} F_{\\alpha\\beta}^{E_8}) + \\frac{\\theta_{\\text{QCD}}}{32\\pi^2} \\frac{\\epsilon^{\\mu\\nu\\alpha\\beta}}{2\\sqrt{-g}} \\text{Tr}(F_{\\mu\\nu}^{E_8} F_{\\alpha\\beta}^{E_8})$$\n\nThe first term is the standard Yang-Mills kinetic energy. The second is the **topological θ-term** — the same term that appears in QCD and is related to CP violation. The $E_8$ structure naturally accommodates all gauge interactions in a single unified framework, with the triality of $\\text{Spin}(8)$ providing the generation structure.'
      },
      {
        keywords: ['chiral', 'coupling', 'chi', 'kappa', 'yukawa', 'flavor'],
        q: 'What is the chiral coupling?',
        a: 'The **chiral coupling** is parameterized by two invariant constants:\n\n$$\\chi_Y = \\frac{1}{\\sqrt{2}}, \\quad \\kappa_Y = \\sqrt{\\theta(2-\\theta)} \\approx 0.9539$$\n\nwhere $\\theta = 0.7$ is a geometric parameter. These constants control the **Yukawa couplings** — the interactions between fermions and the Higgs/dilaton field that give particles their mass.\n\nThe bare UV Planck gauge matching is:\n\n$$g_{\\text{bare}}(M_{\\text{Pl}}) = \\frac{\\kappa_Y \\chi_Y}{\\pi} \\approx 0.2147$$\n\nThis is a **prediction** from the geometry — the gauge coupling at the Planck scale is determined by the chiral invariants, not fitted from data. The Yukawa sector couples the dilaton $\\phi$ to fermion mass terms via $e^{-\\lambda_g/\\kappa_Y}$, giving each generation a different mass scale.'
      },
      {
        keywords: ['information', 'tension', 'theory', 'aqual', 'functional', 'mond', 'a0'],
        q: 'What is Information Tension Theory?',
        a: '**Information Tension Theory** is the name for the modified-gravity sector of the framework. The "tension" refers to the competition between two information-theoretic channels in the action:\n\n$$\\frac{c^4 a_0^2}{8\\pi G} \\left[ \\sqrt{\\frac{g^{\\mu\\nu}\\partial_\\mu\\chi\\partial_\\nu\\chi}{a_0^2}\\left(1 + \\frac{g^{\\alpha\\beta}\\partial_\\alpha\\chi\\partial_\\beta\\chi}{a_0^2}\\right)} - \\text{asinh}\\left(\\sqrt{\\frac{g^{\\mu\\nu}\\partial_\\mu\\chi\\partial_\\nu\\chi}{a_0^2}}\\right) \\right]$$\n\nThis is the **AQUAL functional** — the covariant version of the MOND acceleration scale. The key insight is that $a_0 = cH_0/(2\\pi)$ connects the galactic acceleration scale to the cosmological horizon, suggesting that the same physics that governs galaxy rotation curves also governs the expansion of the universe.\n\nThe "information" aspect comes from the horizon entropy boundary term, which modifies the action based on the relative entropy between regions of spacetime.'
      },
      {
        keywords: ['boundary', 'horizon', 'gibbons', 'hawking', 'york', 'entropy', 'action'],
        q: 'What is the boundary action?',
        a: 'The **Gibbons-Hawking-York boundary action** completes the variational principle by adding surface terms at the boundary of spacetime:\n\n$$\\frac{c^4}{8\\pi G} \\oint_{\\partial\\mathcal{M}} d^3x \\sqrt{|\\gamma|} \\, e^{-2\\phi} K + \\frac{k_B c^3}{4G\\hbar} \\oint_{\\mathcal{H}} dA \\left(1 - \\frac{I(A:B)}{I_{\\max}}\\right)$$\n\nThe first term is the standard **Gibbons-Hawking-York term** — it ensures the variational principle is well-defined on manifolds with boundary. $K$ is the trace of the extrinsic curvature.\n\nThe second term is the novel **horizon entropy correction** — it modifies the black hole entropy based on the **mutual information** $I(A:B)$ between two regions $A$ and $B$ on the horizon, normalized by the maximum $I_{\\max}$. This is where the "Information Tension" name comes from: the horizon entropy depends on the information-theoretic correlations between spacetime regions.'
      }
    ]
  },

  {
    id: 'canonical',
    title: 'Res Nova: Geometrically Ordered Dynamics and Information Tension Theory',
    subtitle: 'Canonical Edition v2.0 • First-Principles Unification',
    icon: '✨',
    coverGradient: 'linear-gradient(135deg, #6d28d9 0%, #5b21b6 50%, #2e1065 100%)',
    orbColor: '#c084fc',
    tags: [
      { label: 'First Principles', class: 'tag-theory' },
      { label: 'No Dark Matter', class: 'tag-empirical' },
      { label: 'Conformal GR', class: 'tag-theory' }
    ],
    meta: { version: 'v2.0', date: 'Aug 2026', doi: '—', modules: 'Lean 4 Suite' },
    abstract: 'A ground-up, first-principles geometric framework unifying conformal general relativity, non-perturbative gauge fields, and galactic kinematics without non-baryonic cold dark matter halos. Establishes an explicit boundary between 85% peer-reviewed foundations and novel theoretical extensions.',
    highlights: [
      { icon: '🌀', title: 'Conformal Gravity', desc: 'Brans-Dicke conformal scalar-tensor gravity as the gravitational backbone' },
      { icon: '🚫', title: 'No Dark Matter', desc: 'Galactic kinematics explained without CDM halos via MOND-like acceleration' },
      { icon: '📐', title: 'First Principles', desc: 'Derived from geometric axioms, not phenomenological fitting' },
      { icon: '🔬', title: '85% Peer-Reviewed', desc: 'Explicit boundary between established and novel physics' }
    ],
    equations: [
      '\\mathcal{L}_{\\text{grav}} = \\frac{c^4}{16\\pi G} e^{-2\\phi}(R - 2\\Lambda_0)',
      'g = \\frac{g_{\\text{bar}}}{2}\\left(1 + \\sqrt{1 + \\frac{4a_0}{g_{\\text{bar}}}}\\right)',
      'v_{\\text{MOND}}(r) \\xrightarrow{r \\to \\infty} (GM_{\\text{tot}} a_0)^{1/4}',
      'a_0 = \\frac{cH_0}{2\\pi} \\approx 1.20 \\times 10^{-10}\\,\\text{m/s}^2'
    ],
    kb: [
      {
        keywords: ['conformal', 'gravity', 'brans', 'dicke', 'scalar', 'tensor', 'dilaton'],
        q: 'What is the conformal gravity backbone?',
        a: 'The gravitational sector uses **conformal (Brans-Dicke) scalar-tensor gravity** rather than pure Einstein gravity. The Lagrangian is:\n\n$$\\mathcal{L}_{\\text{grav}} = \\frac{c^4}{16\\pi G} e^{-2\\phi}(R - 2\\Lambda_0)$$\n\nThe conformal factor $e^{-2\\phi}$ couples the spacetime curvature $R$ to a scalar field $\\phi$ (the dilaton). This means gravity "runs" with the dilaton field — in regions where $\\phi$ is large, the effective gravitational constant changes.\n\nThis is **peer-reviewed physics** — Brans-Dicke theory is a well-established alternative to general relativity, tested against solar-system constraints (Cassini gives $\\omega_{BD} > 40,000$). The conformal coupling is what allows the theory to reproduce both the Newtonian limit and the MOND-like behavior at low accelerations without dark matter.'
      },
      {
        keywords: ['dark', 'matter', 'cdm', 'halo', 'mond', 'rotation', 'curve', 'galaxy'],
        q: 'How does it explain galaxies without dark matter?',
        a: 'Instead of invoking invisible cold dark matter halos, the theory modifies the **gravitational acceleration law** itself. In the weak-field (low acceleration) regime, the effective acceleration becomes:\n\n$$g = \\frac{g_{\\text{bar}}}{2}\\left(1 + \\sqrt{1 + \\frac{4a_0}{g_{\\text{bar}}}}\\right)$$\n\nwhere $g_{\\text{bar}}$ is the Newtonian acceleration from visible matter and $a_0 \\approx 1.2 \\times 10^{-10}$ m/s² is the acceleration scale.\n\nIn the **deep-MOND limit** ($g_{\\text{bar}} \\ll a_0$):\n$$g \\approx \\sqrt{g_{\\text{bar}} \\cdot a_0}$$\n\nThis gives flat rotation curves: $v_{\\text{flat}} = (GM_{\\text{tot}} a_0)^{1/4}$. The velocity depends only on the total baryonic mass — no dark matter needed. This is confirmed by the SPARC benchmark across 171 galaxies with just one global parameter $a_0$.'
      },
      {
        keywords: ['first', 'principle', 'axiom', 'derive', 'ground', 'up', 'geometric'],
        q: 'What does first-principles mean here?',
        a: '"First-principles" means the theory is **derived from geometric axioms**, not assembled from phenomenological fits. The derivation chain is:\n\n1. **Start** with the vacuum geometry $V_2(\\mathbb{R}^3) \\cong SO(3)$\n2. **Derive** the gauge structure from $E_8 \\supset \\text{Spin}(8)$ and Cartan triality\n3. **Derive** the gravitational sector from conformal scalar-tensor theory\n4. **Derive** the MOND acceleration scale $a_0 = cH_0/(2\\pi)$ from horizon thermodynamics\n5. **Derive** the dual-channel AQUAL functional from variational closure constraints\n6. **Verify** every step in Lean 4\n\nAt no point is a parameter "tuned to fit data" — the only empirical input is the measured Hubble constant $H_0$, which enters through $a_0 = cH_0/(2\\pi)$. Everything else follows from the geometry. This is what distinguishes Res Nova from phenomenological MOND variants.'
      },
      {
        keywords: ['85', 'percent', 'peer', 'reviewed', 'boundary', 'established', 'novel'],
        q: 'What is the 85% peer-reviewed boundary?',
        a: 'The paper is unusual in that it draws an **explicit epistemic boundary** between established and novel physics:\n\n- **~85% peer-reviewed foundations**: Brans-Dicke conformal gravity, Bekenstein entropy bounds, MOND phenomenology, SPARC data, standard gauge theory — all published and independently verified\n- **~15% novel theory**: The specific dual-channel closure, the Stiefel manifold substrate, the E₈ embedding, the Cartan triality generation mechanism — these are new and need independent verification\n\nThis boundary is not a marketing claim — it\'s a **research ethics** commitment. The paper tags every claim with an epistemic tier: [P] Proved (Lean 4), [D] Direct (empirical), [C] Computational, [O] Open. Readers can see exactly which parts are established and which are speculative. This is the "Sovereign Epistemic Ledger" system.'
      }
    ]
  },

  {
    id: 'io-oi',
    title: 'IO-OI: A Complete Theory of Sovereign Geometrodynamics',
    subtitle: 'Stoicheia → Erga → Oikodomē → Pleroma',
    icon: '🏛️',
    coverGradient: 'linear-gradient(135deg, #115e59 0%, #0f766e 40%, #042f2e 100%)',
    orbColor: '#10b981',
    tags: [
      { label: 'Geometrodynamics', class: 'tag-theory' },
      { label: 'Sovereign', class: 'tag-theory' },
      { label: 'JWST Observer', class: 'tag-empirical' }
    ],
    meta: { version: 'Sep 2026', date: 'Sep 19, 2026', doi: '—', modules: 'Observer Framework' },
    abstract: 'A complete theory of sovereign geometrodynamics tracing the arc from Stoicheia (elements) through Erga (works) and Oikodomē (building) to Pleroma (fullness). Includes a JWST observer program for measuring a₀ at intermediate redshifts.',
    highlights: [
      { icon: '🧱', title: 'Stoicheia', desc: 'Foundational elements — the geometric primitives of the theory' },
      { icon: '⚙️', title: 'Erga', desc: 'Works — the dynamical equations and physical predictions' },
      { icon: '🏗️', title: 'Oikodomē', desc: 'Building — the constructive assembly into a coherent framework' },
      { icon: '🌟', title: 'Pleroma', desc: 'Fullness — the complete unified theory' }
    ],
    equations: [
      '\\text{Stoicheia} \\to \\text{Erga} \\to \\text{Oikodom\\={e}} \\to \\text{Pleroma}',
      'a_0(z) \\stackrel{?}{=} a_0(0) \\quad \\text{(JWST test)}',
      '\\Delta\\chi^2 = +4.24 \\quad (2.06\\sigma, \\text{inconclusive})'
    ],
    kb: [
      {
        keywords: ['stoicheia', 'erga', 'oikodom', 'pleroma', 'arc', 'structure', 'framework'],
        q: 'What is the Stoicheia → Pleroma arc?',
        a: 'The paper is structured as a **four-stage arc** borrowed from Greek philosophical architecture:\n\n1. **Stoicheia** (Στοιχεῖα — "Elements"): The foundational geometric primitives — the Stiefel manifold $V_2(\\mathbb{R}^3)$, the gauge group $E_8$, the acceleration scale $a_0$. These are the "letters" of the theory.\n\n2. **Erga** (Ἔργα — "Works"): The dynamical equations derived from the elements — the action functional, the field equations, the MOND acceleration law. These are what the elements "do."\n\n3. **Oikodomē** (Οἰκοδομή — "Building"): The constructive assembly — how the works fit together into a coherent, ghost-free, covariant theory. This is where the Lean 4 verification lives.\n\n4. **Pleroma** (Πλήρωμα — "Fullness"): The complete unified theory, including empirical predictions and open questions. This is the "filled-up" theory that makes contact with observation.\n\nThe naming reflects the paper\'s commitment to **building from the ground up** rather than postulating top-down.'
      },
      {
        keywords: ['jwst', 'observer', 'redshift', 'a0', 'evolution', 'intermediate', 'high', 'z'],
        q: 'What is the JWST observer program?',
        a: 'The JWST observer program is a **pre-registered test** of whether the MOND acceleration scale $a_0$ evolves with redshift. Using 20 intermediate-redshift galaxies observed by JWST:\n\n- **Hypothesis**: $a_0(z) = a_0(0)$ — the acceleration scale is constant across cosmic time\n- **Test statistic**: $\\Delta\\chi^2$ between fixed-$a_0$ and evolving-$a_0$ fits\n- **Result**: $\\Delta\\chi^2 = +4.24$, corresponding to **2.06σ** — **inconclusive**\n\nThe earlier $5.9\\sigma$ result under $\\mu_{\\text{dual}}$ was **retracted** because it depended on the falsified interpolation function. The honest current state is that we cannot yet tell if $a_0$ evolves. More data is needed.\n\nThis pre-registration is part of the "sovereign" epistemology — the analysis was committed before looking at the data, preventing p-hacking or retrospective fitting.'
      },
      {
        keywords: ['sovereign', 'epistemology', 'epistemic', 'ledger', 'tier', 'standard'],
        q: 'What does "sovereign" mean in this context?',
        a: '"Sovereign" refers to the **epistemic standard** the paper adopts — it holds itself to its own rigorous truth-tracking system rather than deferring to authority or consensus. The **Sovereign Epistemic Ledger** tags every claim with a tier:\n\n- **[P] Proved**: Verified by Lean 4 mechanical proof (no human intuition)\n- **[D] Direct**: Established by direct empirical measurement (SPARC, JWST, LIGO)\n- **[C] Computational**: Verified by numerical computation\n- **[O] Open**: Acknowledged as unresolved — not hidden or hand-waved\n\nThe "sovereignty" means the paper doesn\'t claim more than it can prove. It doesn\'t present speculative results as established, and it doesn\'t bury failures. The retraction of the solar-system claim and the redshift-evolution result are **features** of this system, not bugs. The paper is "sovereign" over its own claims — it governs what it asserts with formal rigor.'
      }
    ]
  },

  {
    id: 'master-action',
    title: 'The Invariant Master Action of the Universe',
    subtitle: 'One-Page Universal Lagrangian',
    icon: '⚛️',
    coverGradient: 'linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #0c0a3e 100%)',
    orbColor: '#818cf8',
    tags: [
      { label: 'Universal Action', class: 'tag-theory' },
      { label: 'One Page', class: 'tag-theory' },
      { label: 'Lean 4 Roots', class: 'tag-proved' }
    ],
    meta: { version: 'One-Page', date: '2026', doi: '—', modules: '5 Lean roots' },
    abstract: 'The complete universal Lagrangian on a single page — unifying conformal gravitation, dilaton dynamics, information tension AQUAL, Stiefel V₂(ℝ³) substrate, E₈ Yang-Mills gauge sector, three-generation fermions via Cartan triality, and the Gibbons-Hawking-York horizon action.',
    highlights: [
      { icon: '🌀', title: 'Conformal Gravitation', desc: 'e^{-2φ}(R − 2Λ₀) — Brans-Dicke scalar-tensor backbone' },
      { icon: '🌊', title: 'Information Tension AQUAL', desc: 'a₀ = cH₀/2π — MOND acceleration from horizon thermodynamics' },
      { icon: '🔮', title: 'E₈ Gauge + θ-term', desc: 'Unified Yang-Mills with topological QCD θ-term' },
      { icon: '✅', title: 'GW170817 Concordance', desc: '|v_gw/c − 1| = 0 — exact luminal gravitational waves' }
    ],
    equations: [
      '\\mathcal{S}_{\\text{univ}} = \\int_{\\mathcal{M}} d^4x \\sqrt{-g}\\;\\mathcal{L}_{\\text{univ}} + \\mathcal{S}_{\\partial\\mathcal{M}}',
      'a_0 = \\frac{cH_0}{2\\pi} \\approx 1.20 \\times 10^{-10}\\,\\text{m/s}^2',
      '\\left|\\frac{v_{\\text{gw}}}{c} - 1\\right| = 0 \\quad \\text{(GW170817)}',
      'g_{\\text{bare}}(M_{\\text{Pl}}) = \\frac{\\kappa_Y \\chi_Y}{\\pi} \\approx 0.2147'
    ],
    kb: [
      {
        keywords: ['lagrangian', 'action', 'universal', 'master', 'complete', 'full', 'total'],
        q: 'What is the universal Lagrangian?',
        a: 'The **universal Lagrangian** is the complete action of the theory on a single page. It has **seven sectors**:\n\n1. **Conformal Gravitation**: $\\frac{c^4}{16\\pi G} e^{-2\\phi}(R - 2\\Lambda_0)$ — Brans-Dicke scalar-tensor gravity\n2. **Dilaton Potential**: $-\\frac{1}{2}(\\partial\\phi)^2 - \\frac{1}{2}m_\\phi^2\\phi^2 - \\frac{\\lambda_\\phi}{4!}\\phi^4$ — scalar field dynamics\n3. **Information Tension AQUAL**: The MOND acceleration functional with $a_0 = cH_0/(2\\pi)$\n4. **Stiefel Substrate**: $V_2(\\mathbb{R}^3) \\cong SO(3)$ kinetic term for the gauge field\n5. **Holonomy Curvature**: Coupling between the Stiefel field and gauge curvature\n6. **E₈ Gauge Sector**: Yang-Mills + topological θ-term\n7. **Fermions**: Three generations via Cartan triality + Yukawa couplings\n\nPlus the **Gibbons-Hawking-York boundary action** with the horizon entropy correction. Every sector is derived from the geometry — nothing is added phenomenologically.'
      },
      {
        keywords: ['a0', 'acceleration', 'scale', 'horizon', 'hubble', 'cosmological', 'mond'],
        q: 'Why is a₀ = cH₀/2π?',
        a: 'The acceleration scale $a_0 = cH_0/(2\\pi) \\approx 1.20 \\times 10^{-10}$ m/s² is **derived from horizon thermodynamics**, not fitted.\n\nThe connection is: the cosmological horizon has a characteristic acceleration $cH_0$ (the Hubble acceleration). The factor of $1/(2\\pi)$ comes from the **holographic** nature of the horizon — the entropy is distributed over a 2D surface, and the $2\\pi$ is the geometric factor relating the surface area to the radial coordinate.\n\nThis is profound: it means **the same physics that governs the expansion of the universe also governs the rotation of galaxies**. The MOND acceleration scale isn\'t a free parameter — it\'s a consequence of the cosmological horizon. This is why $a_0$ is close to $cH_0$ in every measurement.\n\nThe SPARC measurement gives $a_0 = (1.116 \\pm 0.161) \\times 10^{-10}$ m/s², consistent with $cH_0/(2\\pi) \\approx 1.20 \\times 10^{-10}$ m/s².'
      },
      {
        keywords: ['gw', 'gravitational', 'wave', 'speed', 'luminal', 'gw170817', 'ligo', 'concordance'],
        q: 'How does it match GW170817?',
        a: 'The theory predicts **exactly luminal gravitational waves**:\n\n$$\\left|\\frac{v_{\\text{gw}}}{c} - 1\\right| = 0$$\n\nThis is in **perfect concordance** with GW170817 — the LIGO/Virgo observation of gravitational waves from a neutron star merger, which constrained $|c_T/c_\\gamma - 1| < 10^{-15}$.\n\nThis is non-trivial: many modified gravity theories (especially those with extra scalar fields) predict **superluminal** gravitational waves, which would be immediately falsified by GW170817. The Res Nova theory avoids this because:\n\n- The disformal metric coupling $B(\\phi) = 0$ is enforced (proved in Lean 4)\n- The conformal factor $e^{-2\\phi}$ preserves the lightcone structure\n- The tensor speed $c_T = c$ is independent of the interpolation function choice\n\nThis is one of the strongest constraints on the theory — and it passes exactly.'
      },
      {
        keywords: ['boundary', 'constant', 'invariant', 'relation', 'vacuum', 'chiral', 'gauge'],
        q: 'What are the exact boundary constants?',
        a: 'The one-page Lagrangian lists **five exact boundary constants and invariant relations** — all derived from the geometry, not fitted:\n\n1. **Vacuum Geometry**: $\\mathcal{M}_{\\text{vac}} = V_2(\\mathbb{R}^3) \\cong SO(3)$, and $\\text{Out}(\\text{Spin}(8)) \\cong S_3 \\implies \\mathbb{Z}_3$ (exactly 3 generations)\n\n2. **Cosmic Horizon Scale**: $a_0 = cH_0/(2\\pi) \\approx 1.20 \\times 10^{-10}$ m/s², with surface density $\\Sigma_c = a_0/(2\\pi G) \\approx 857\\,M_\\odot/\\text{pc}^2$\n\n3. **Chiral Coupling Invariant**: $\\chi_Y = 1/\\sqrt{2}$, $\\kappa_Y = \\sqrt{\\theta(2-\\theta)} \\approx 0.9539$ (for $\\theta = 0.7$)\n\n4. **Bare UV Planck Gauge Matching**: $g_{\\text{bare}}(M_{\\text{Pl}}) = \\kappa_Y \\chi_Y / \\pi \\approx 0.2147$\n\n5. **Disformal GW Speed**: $|v_{\\text{gw}}/c - 1| = 0$ (exact concordance with GW170817)\n\nThese are **predictions** of the theory, not inputs. They\'re verified by Lean 4 modules: CartanTrialityGenerations.lean, GalacticAcceleration.lean, Decoherence.lean, ChiralCellularDuality.lean, StiefelHolonomy.lean.'
      }
    ]
  },

  {
    id: 'reproducibility',
    title: 'Reproducibility Appendix: Lean 4 Verification Provenance',
    subtitle: '28 Modules • Cold-Machine Verification',
    icon: '🔧',
    coverGradient: 'linear-gradient(135deg, #991b1b 0%, #7f1d1d 40%, #450a0a 100%)',
    orbColor: '#f43f5e',
    tags: [
      { label: 'Reproducibility', class: 'tag-proved' },
      { label: 'Lean 4', class: 'tag-proved' },
      { label: '28 Modules', class: 'tag-proved' }
    ],
    meta: { version: 'O6', date: 'Sep 2026', doi: '—', modules: '28 Lean modules' },
    abstract: 'Complete Lean 4 source inventory and verification provenance. Documents 28 formal verification modules, cold-machine verification runs with genuine network fetches, CI-release-gate conditions, and the full chain of trust from source code to machine-checked theorems.',
    highlights: [
      { icon: '📦', title: '28 Modules', desc: 'Complete Lean 4 source inventory with headline declarations per module' },
      { icon: '❄️', title: 'Cold-Machine', desc: 'Fresh container, no pre-existing caches, genuine network fetch' },
      { icon: '🟢', title: 'CI Green', desc: 'lean-gate workflow 3/3 green including cold scheduled run' },
      { icon: '🔗', title: 'Chain of Trust', desc: 'Full provenance from source to machine-checked theorem' }
    ],
    equations: [
      '\\text{VERIFICATION\\_RUN\\_008}: \\text{exit status } 0',
      '\\text{Axioms}: \\{\\texttt{propext}, \\texttt{Classical.choice}, \\texttt{Quot.sound}\\}',
      '\\text{Lean } 4.33.0\\text{-rc1}, \\quad \\text{Mathlib } 5eec30bc'
    ],
    kb: [
      {
        keywords: ['verification', 'run', 'cold', 'machine', 'cache', 'network', 'fresh', 'container'],
        q: 'What is a cold-machine verification?',
        a: 'A **cold-machine verification** is the gold standard for formal proof reproducibility. The VERIFICATION_RUN_008 was conducted with:\n\n- **Fresh container**: No pre-existing `.lake/packages` or Mathlib host cache\n- **Genuine network fetch**: `lake exe cache get` performed a real download, not a cache hit\n- **Clean toolchain**: Lean v4.33.0-rc1 with Mathlib commit 5eec30bc\n- **Full elaboration**: The gate `verify_all_proofs.sh` elaborated all 32 declared targets\n- **Exit status 0**: Every target passed\n\nThis matters because a "warm" verification (with cached results) could hide errors — if the cache was built with a bug, the cached proof would pass even if the source has changed. A cold run proves the theorems **actually compile from source**.\n\nThe full transcript, cache-fetch log, per-target results, toolchain revisions, and checksums are archived in `VERIFICATION_RUN_008/01_lean/`.'
      },
      {
        keywords: ['axiom', 'footprint', 'sorry', 'custom', 'propext', 'classical', 'quot'],
        q: 'What axioms are used?',
        a: 'The Lean 4 verification uses only the **standard Lean axioms** — no custom axioms are introduced:\n\n- `propext`: Propositional extensionality (if two propositions are logically equivalent, they\'re equal)\n- `Classical.choice`: The axiom of choice (needed for non-constructive proofs)\n- `Quot.sound`: Quotient types are sound (needed for set quotients)\n\nThese are the **same axioms that Mathlib uses** — they\'re the minimal set needed for classical mathematics in Lean. The verification explicitly checks that no `sorry` (skipped proof) appears in the proof code.\n\nThis is important because adding custom axioms could make any theorem "provable" — you could just axiomatize the result. By restricting to standard axioms, the proofs are **meaningful** — they\'re derived from the same logical foundation as all of Lean\'s standard library.'
      },
      {
        keywords: ['ci', 'gate', 'workflow', 'github', 'action', 'schedule', 'release'],
        q: 'How does the CI gate work?',
        a: 'The `lean-gate` GitHub Actions workflow provides **continuous verification**:\n\n- **Triggers**: Runs on every push, on schedule, and on manual dispatch\n- **3/3 green**: All three trigger types passed, including the cold scheduled run\n- **What it checks**: Elaborates all Lean targets, verifies no `sorry` in proof code, checks axiom footprint\n\nThe CI gate ensures that **every commit to the repository** is formally verified. If someone introduces a `sorry` or changes an axiom, the CI fails. This creates a **chain of trust** from the git history to the machine-checked theorems — you can verify any past commit by re-running the gate.\n\nThe release-gate condition adds an extra layer: the scheduled cold run (no cache) must pass independently, ensuring the proofs don\'t depend on any cached state.'
      },
      {
        keywords: ['module', 'inventory', 'list', 'source', 'target', 'declaration'],
        q: 'What modules are verified?',
        a: 'The Lean 4 source inventory comprises **28 modules** (expanded from 8 in earlier versions). Each module has headline declarations — the main theorems it proves. Key modules include:\n\n- **DualChannelDerivation.lean**: Proves $\\mathcal{F}_{\\text{dual}}(x) = \\frac{1}{2}x^2 - x + \\ln(1+x)$ gives $\\mu(x) = x/(1+x)$\n- **TensorSpeed.lean**: Proves $|c_T/c_\\gamma - 1| \\gg 10^{-15}$ when $B(\\phi) \\neq 0$\n- **SkordisZlosnikEmbedding.lean**: Proves $\\mathcal{J}(\\mathcal{Y})$ matching with zero residual\n- **MuProjection.lean**: Proves the μ function properties and Fisher identity\n- **RelativisticStability.lean**: Proves characteristic speeds are real and positive\n- **CartanTrialityGenerations.lean**: Proves the 3-generation structure\n- **GalacticAcceleration.lean**: Proves the MOND acceleration formula\n- **StiefelHolonomy.lean**: Proves the Stiefel manifold holonomy properties\n\nAll 32 declared targets (some modules have multiple targets) pass with exit status 0. The full per-target results are archived with checksums.'
      }
    ]
  }
];

// --- CAROUSEL STATE ---
let carouselIndex = 0;
let activePaperId = null;

// --- INIT CAROUSEL ---
function initPapersCarousel() {
  renderCarousel();
  renderDots();
}

function renderCarousel() {
  const track = document.getElementById('carouselTrack');
  if (!track) return;
  track.innerHTML = '';

  PAPERS.forEach((paper, i) => {
    const card = document.createElement('div');
    card.className = 'paper-card';
    card.dataset.index = i;
    card.innerHTML = `
      <div class="paper-cover" style="background: ${paper.coverGradient}">
        <div class="paper-cover-orb" style="background: ${paper.orbColor}; width: 120px; height: 120px; top: 20px; left: 50%; transform: translateX(-50%);"></div>
        <div class="paper-cover-orb" style="background: ${paper.orbColor}; width: 80px; height: 80px; top: 60px; left: 30%; opacity: 0.3;"></div>
        <span class="paper-cover-icon">${paper.icon}</span>
      </div>
      <div class="paper-body">
        <div class="paper-tag-row">
          ${paper.tags.map(t => `<span class="paper-tag ${t.class}">${t.label}</span>`).join('')}
        </div>
        <h3 class="paper-title">${paper.title}</h3>
        <p class="paper-subtitle">${paper.subtitle}</p>
        <p class="paper-abstract">${paper.abstract}</p>
        <div class="paper-meta-row">
          <span class="paper-meta-info">${paper.meta.version} • ${paper.meta.date}</span>
          <span class="paper-cta">Explore & Chat →</span>
        </div>
      </div>
    `;
    card.addEventListener('click', () => {
      if (i === carouselIndex) {
        openPaperDetail(i);
      } else {
        carouselIndex = i;
        updateCarouselPositions();
        updateDots();
      }
    });
    track.appendChild(card);
  });

  updateCarouselPositions();
}

function updateCarouselPositions() {
  const cards = document.querySelectorAll('.paper-card');
  const n = PAPERS.length;
  cards.forEach((card, i) => {
    card.classList.remove('pos-center', 'pos-left', 'pos-right', 'pos-far-left', 'pos-far-right');
    let offset = i - carouselIndex;
    // Normalize for wrap-around
    if (offset > n / 2) offset -= n;
    if (offset < -n / 2) offset += n;

    if (offset === 0) card.classList.add('pos-center');
    else if (offset === -1) card.classList.add('pos-left');
    else if (offset === 1) card.classList.add('pos-right');
    else if (offset < -1) card.classList.add('pos-far-left');
    else card.classList.add('pos-far-right');
  });
}

function renderDots() {
  const dotsContainer = document.getElementById('carouselDots');
  if (!dotsContainer) return;
  dotsContainer.innerHTML = '';
  PAPERS.forEach((_, i) => {
    const dot = document.createElement('button');
    dot.className = 'carousel-dot' + (i === carouselIndex ? ' active' : '');
    dot.addEventListener('click', () => {
      carouselIndex = i;
      updateCarouselPositions();
      updateDots();
    });
    dotsContainer.appendChild(dot);
  });
}

function updateDots() {
  document.querySelectorAll('.carousel-dot').forEach((dot, i) => {
    dot.classList.toggle('active', i === carouselIndex);
  });
}

function carouselPrev() {
  carouselIndex = (carouselIndex - 1 + PAPERS.length) % PAPERS.length;
  updateCarouselPositions();
  updateDots();
}

function carouselNext() {
  carouselIndex = (carouselIndex + 1) % PAPERS.length;
  updateCarouselPositions();
  updateDots();
}

// Keyboard nav for carousel
document.addEventListener('keydown', (e) => {
  const papersTab = document.getElementById('tab-papers');
  if (!papersTab || !papersTab.classList.contains('active')) return;
  const overlay = document.getElementById('paperDetailOverlay');
  if (overlay && overlay.classList.contains('active')) return;
  if (e.key === 'ArrowLeft') carouselPrev();
  if (e.key === 'ArrowRight') carouselNext();
});

// --- PAPER DETAIL + CHAT ---
function openPaperDetail(idx) {
  const paper = PAPERS[idx];
  activePaperId = paper.id;
  const overlay = document.getElementById('paperDetailOverlay');

  // Build detail content
  const contentEl = document.getElementById('paperDetailContent');
  contentEl.innerHTML = `
    <button class="detail-close" onclick="closePaperDetail()">
      <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
    </button>
    <div class="detail-header">
      <h2>${paper.icon} ${paper.title}</h2>
      <p class="detail-subtitle">${paper.subtitle}</p>
      <div class="detail-meta">
        <span>📦 ${paper.meta.version}</span>
        <span>📅 ${paper.meta.date}</span>
        <span>🔗 DOI: ${paper.meta.doi}</span>
        <span>🧮 ${paper.meta.modules}</span>
      </div>
    </div>
    <div class="detail-section">
      <h3>📝 Abstract</h3>
      <p>${paper.abstract}</p>
    </div>
    <div class="detail-section">
      <h3>🔑 Key Highlights</h3>
      <div class="detail-highlights">
        ${paper.highlights.map(h => `
          <div class="highlight-item">
            <div class="hl-icon">${h.icon}</div>
            <div class="hl-title">${h.title}</div>
            <div class="hl-desc">${h.desc}</div>
          </div>
        `).join('')}
      </div>
    </div>
    <div class="detail-section">
      <h3>📐 Key Equations</h3>
      ${paper.equations.map(eq => `<div class="detail-equation">$$${eq}$$</div>`).join('')}
    </div>
  `;

  // Build chat panel
  const chatEl = document.getElementById('paperChatPanel');
  chatEl.dataset.paperId = paper.id;
  chatEl.innerHTML = `
    <div class="chat-header">
      <div class="chat-avatar">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.171.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.45 3.348-1.388 3.452a47.541 47.541 0 00-11.828 0c-1.838-.104-2.62-2.22-1.388-3.452l1.402-1.402"/></svg>
      </div>
      <div class="chat-header-text">
        <h4>Nova AI Explainer</h4>
        <p><span class="chat-status-dot"></span> Ready • Ask about this paper</p>
      </div>
    </div>
    <div class="chat-messages" id="chatMessages"></div>
    <div class="chat-suggestions" id="chatSuggestions"></div>
    <div class="chat-input-area">
      <div class="chat-input-wrap">
        <textarea class="chat-input" id="chatInput" placeholder="Ask about the key concepts, equations, or findings..." rows="1" onkeydown="handleChatKeydown(event)"></textarea>
        <button class="chat-send-btn" id="chatSendBtn" onclick="sendChatMessage()">
          <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"/></svg>
        </button>
      </div>
    </div>
  `;

  overlay.classList.add('active');
  document.body.style.overflow = 'hidden';

  // Render KaTeX in detail content
  setTimeout(() => {
    if (window.renderMathInElement) {
      renderMathInElement(contentEl, {
        delimiters: [{ left: '$$', right: '$$', display: true }, { left: '$', right: '$', display: false }],
        throwOnError: false
      });
    }
  }, 50);

  // Initialize chat with welcome message + suggestions
  initChat(paper);
}

function closePaperDetail() {
  const overlay = document.getElementById('paperDetailOverlay');
  overlay.classList.remove('active');
  document.body.style.overflow = '';
  activePaperId = null;
}

// Close on overlay backdrop click
document.addEventListener('click', (e) => {
  const overlay = document.getElementById('paperDetailOverlay');
  if (e.target === overlay) closePaperDetail();
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closePaperDetail();
});

// --- CHAT LOGIC ---
function initChat(paper) {
  const messagesEl = document.getElementById('chatMessages');
  const suggestionsEl = document.getElementById('chatSuggestions');

  // Welcome message
  const welcomeText = `Hi! I'm **Nova**, your AI explainer for **"${paper.title}"**. I can elaborate on any of the high-level concepts, equations, or findings in this paper. Ask me anything, or tap a suggested question below to get started!`;

  appendBotMessage(welcomeText);
  renderMathInChat();

  // Suggested questions (first 4 from KB)
  suggestionsEl.innerHTML = '';
  paper.kb.slice(0, 4).forEach((entry, i) => {
    const chip = document.createElement('button');
    chip.className = 'suggestion-chip';
    chip.textContent = entry.q;
    chip.addEventListener('click', () => {
      sendChatMessage(entry.q);
    });
    suggestionsEl.appendChild(chip);
  });
}

function appendBotMessage(text) {
  const messagesEl = document.getElementById('chatMessages');
  if (!messagesEl) return;
  const msg = document.createElement('div');
  msg.className = 'chat-msg bot';
  // Convert markdown-ish formatting
  let html = text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>');
  // KaTeX inline/display will be rendered after insertion
  msg.innerHTML = `<div class="msg-bubble">${html}</div>`;
  messagesEl.appendChild(msg);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function appendUserMessage(text) {
  const messagesEl = document.getElementById('chatMessages');
  if (!messagesEl) return;
  const msg = document.createElement('div');
  msg.className = 'chat-msg user';
  msg.innerHTML = `<div class="msg-bubble">${text.replace(/</g, '&lt;')}</div>`;
  messagesEl.appendChild(msg);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function showTypingIndicator() {
  const messagesEl = document.getElementById('chatMessages');
  if (!messagesEl) return;
  const typing = document.createElement('div');
  typing.className = 'chat-typing';
  typing.id = 'chatTyping';
  typing.innerHTML = '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>';
  messagesEl.appendChild(typing);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function removeTypingIndicator() {
  const typing = document.getElementById('chatTyping');
  if (typing) typing.remove();
}

function renderMathInChat() {
  const messagesEl = document.getElementById('chatMessages');
  if (!messagesEl || !window.renderMathInElement) return;
  renderMathInElement(messagesEl, {
    delimiters: [{ left: '$$', right: '$$', display: true }, { left: '$', right: '$', display: false }],
    throwOnError: false
  });
}

function handleChatKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendChatMessage();
  }
}

function sendChatMessage(forceText) {
  const input = document.getElementById('chatInput');
  if (!input) return;
  const text = forceText || input.value.trim();
  if (!text) return;

  appendUserMessage(text);
  input.value = '';
  input.style.height = 'auto';

  // Hide suggestions after first interaction
  const suggestionsEl = document.getElementById('chatSuggestions');
  if (suggestionsEl) suggestionsEl.innerHTML = '';

  // Find best matching KB entry
  const paper = PAPERS.find(p => p.id === activePaperId);
  if (!paper) return;

  showTypingIndicator();

  setTimeout(() => {
    removeTypingIndicator();
    const response = findBestResponse(text, paper);
    appendBotMessage(response);
    renderMathInChat();
  }, 600 + Math.random() * 500);
}

function findBestResponse(query, paper) {
  const queryLower = query.toLowerCase();
  const queryWords = queryLower.split(/\s+/).filter(w => w.length > 2);

  let bestScore = -1;
  let bestEntry = null;

  paper.kb.forEach(entry => {
    let score = 0;
    // Match against keywords
    entry.keywords.forEach(kw => {
      if (queryLower.includes(kw.toLowerCase())) {
        score += kw.length > 4 ? 3 : 2;
      }
    });
    // Match against question text
    const qWords = entry.q.toLowerCase().split(/\s+/);
    queryWords.forEach(w => {
      if (qWords.some(qw => qw.includes(w) || w.includes(qw))) {
        score += 1;
      }
    });
    // Match against answer content
    if (entry.a.toLowerCase().includes(queryLower)) {
      score += 2;
    }

    if (score > bestScore) {
      bestScore = score;
      bestEntry = entry;
    }
  });

  if (bestScore <= 0 || !bestEntry) {
    // Fallback response
    const topics = paper.kb.map(k => `• ${k.q}`).join('\n');
    return `I'm not sure I caught that specific question, but I can elaborate on these topics from this paper:\n\n${topics}\n\nTry asking about any of these, or use more specific physics terms!`;
  }

  return bestEntry.a;
}

// Auto-resize textarea
document.addEventListener('input', (e) => {
  if (e.target && e.target.id === 'chatInput') {
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 80) + 'px';
  }
});
