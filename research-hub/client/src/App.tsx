import { createContext, lazy, Suspense, useContext, useMemo, useState } from "react";
import { Link, Route, Switch, useLocation } from "wouter";
import {
  ArrowDownRight,
  ArrowRight,
  ArrowUpRight,
  BookOpen,
  Check,
  ChevronDown,
  CircleDot,
  Database,
  Download,
  ExternalLink,
  FileCode2,
  FlaskConical,
  GitBranch,
  Github,
  Info,
  Layers3,
  Library,
  Menu,
  Orbit,
  Play,
  Quote,
  Radar,
  Search,
  ShieldCheck,
  Sparkles,
  X,
} from "lucide-react";
import {
  chartData,
  claims,
  claimRegistryState,
  datasets,
  glossary,
  pillars,
  publications,
  releaseState,
  stats,
  statusMeta,
  timeline,
  workstreams,
  type EvidenceStatus,
} from "./data/research";
import { ThemeProvider } from "./contexts/ThemeContext";
import ErrorBoundary from "./components/ErrorBoundary";
import ResearchGuide from "./components/ResearchGuide";
import ResearchFileLibrary from "./components/ResearchFileLibrary";
import ImportProvenancePanel from "./components/ImportProvenancePanel";
import { sparcSource } from "./data/sparc";
import { trpc } from "./lib/trpc";

const CinematicField = lazy(() => import("./experience/CinematicField"));
const RotationCurveExplorer = lazy(() => import("./components/RotationCurveExplorer"));
const TheoryMapExplorer = lazy(() => import("./components/TheoryMapExplorer"));
const AdminDashboard = lazy(() => import("./pages/AdminDashboard"));
const ComparisonChart = lazy(() => import("./components/ComparisonChart"));
const A0IntervalFigure = lazy(() => import("./components/figures/a0-interval").then((module) => ({ default: module.A0IntervalFigure })));
const Chi2Figure = lazy(() => import("./components/figures/chi2").then((module) => ({ default: module.Chi2Figure })));
const HorizonFigure = lazy(() => import("./components/figures/horizon").then((module) => ({ default: module.HorizonFigure })));
const RarFigure = lazy(() => import("./components/figures/rar").then((module) => ({ default: module.RarFigure })));
const SmallMultiplesFigure = lazy(() => import("./components/figures/small-multiples").then((module) => ({ default: module.SmallMultiplesFigure })));

type AtlasDataValue = {
  claims: typeof claims;
  workstreams: typeof workstreams;
  publications: typeof publications;
  datasets: typeof datasets;
  timeline: typeof timeline;
  release: typeof releaseState;
  isPersisted: boolean;
  loading: boolean;
};

type PersistedSnapshot = {
  claims: Array<{ id: string; status: string; tone: string; domain: string; title: string; summary: string; source: string; limitation: string }>;
  workstreams: Array<{ id: string; label: string; short: string; status: string; progress: number; color: string }>;
  publications: Array<{ id: number; type: string; year: string; title: string; summary: string; href: string; tag: string }>;
  datasets: Array<{ id: number; name: string; scope: string; artifact: string; provenance: string; color: string }>;
  timeline: Array<{ id: number; date: string; title: string; body: string }>;
  release: { version: string; researchRelease: string; commit: string; note: string; linksJson: string } | null;
};

const AtlasDataContext = createContext<AtlasDataValue>({
  claims,
  workstreams,
  publications,
  datasets,
  timeline,
  release: releaseState,
  isPersisted: false,
  loading: false,
});

function useAtlasData() {
  return useContext(AtlasDataContext);
}

function normalizeAtlasData(data: PersistedSnapshot | undefined, loading: boolean): AtlasDataValue {
  if (!data) return { claims, workstreams, publications, datasets, timeline, release: releaseState, isPersisted: false, loading };
  const persistedClaims = data.claims.map((item) => ({ ...item, status: item.status as EvidenceStatus, tone: item.tone as typeof claims[number]["tone"] }));
  const persistedWorkstreams = data.workstreams.map((item) => ({ ...item, status: item.status as EvidenceStatus }));
  const persistedRelease = data.release ? { ...releaseState, version: data.release.version, researchRelease: data.release.researchRelease, commit: data.release.commit, note: data.release.note, links: JSON.parse(data.release.linksJson) as typeof releaseState.links } : releaseState;
  return { claims: persistedClaims as typeof claims, workstreams: persistedWorkstreams as typeof workstreams, publications: data.publications as typeof publications, datasets: data.datasets as typeof datasets, timeline: data.timeline as typeof timeline, release: persistedRelease, isPersisted: true, loading };
}

const navItems = [
  { href: "/program", label: "Program" },
  { href: "/theory", label: "Theory map" },
  { href: "/evidence", label: "Evidence atlas" },
  { href: "/data", label: "Data & methods" },
  { href: "/publications", label: "Publications" },
];
function StatusBadge({ status, compact = false }: { status: EvidenceStatus; compact?: boolean }) {
  const meta = statusMeta[status];
  // make sure to consider if you need authentication for certain routes
  return (
    <span className={`status-badge status-${meta.tone} ${compact ? "status-compact" : ""}`}>
      <span className="status-dot" aria-hidden="true" />
      {meta.label}
    </span>
  );
}

function SourceLine({ children }: { children: React.ReactNode }) {
  return (
    <div className="source-line">
      <Info size={13} aria-hidden="true" />
      <span>{children}</span>
    </div>
  );
}

function downloadClaimBibtex(claim: (typeof claims)[number]) {
  const key = claim.id.toLowerCase().replace(/[^a-z0-9]+/g, "-");
  const bibtex = `@misc{${key},\n  author = {Res Nova Research Program},\n  title = {${claim.title}},\n  year = {2026},\n  howpublished = {Res Nova Research Atlas},\n  note = {Evidence status: ${statusMeta[claim.status].label}. Source: ${claim.source}. Boundary: ${claim.limitation}},\n  url = {https://resnova-hub-f4ucvy3e.manus.space/evidence#claim-${claim.id}}\n}`;
  const url = URL.createObjectURL(new Blob([bibtex], { type: "application/x-bibtex" }));
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `${key}.bib`;
  anchor.click();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function BrandMark() {
  return (
    <Link href="/" className="brand" aria-label="Res Nova home">
      <span className="brand-mark" aria-hidden="true">
        <Orbit size={19} strokeWidth={1.5} />
        <span className="brand-orbit-dot" />
      </span>
      <span>
        <strong>RES NOVA</strong>
        <small>research atlas</small>
      </span>
    </Link>
  );
}

function Layout({ children }: { children: React.ReactNode }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [location] = useLocation();
  const { release } = useAtlasData();
  const close = () => setMenuOpen(false);
  return (
    <div className="site-shell">
      <a className="skip-link" href="#main-content">Skip to content</a>
      <header className="site-header">
        <div className="nav-wrap">
          <BrandMark />
          <nav className={`main-nav ${menuOpen ? "is-open" : ""}`} aria-label="Main navigation">
            {navItems.map((item) => (
              <Link key={item.href} href={item.href} className={location === item.href ? "active" : ""} onClick={close}>
                {item.label}
              </Link>
            ))}
            <Link href="/open-problems" className={location === "/open-problems" ? "active" : ""} onClick={close}>Open problems</Link>
          </nav>
          <div className="nav-actions">
            <a className="nav-github" href={release.links.github} target="_blank" rel="noreferrer" aria-label="Open Res Nova on GitHub">
              <Github size={17} aria-hidden="true" />
              <span>Source</span>
            </a>
            <button className="menu-button" type="button" aria-expanded={menuOpen} aria-controls="main-navigation" onClick={() => setMenuOpen(!menuOpen)}>
              {menuOpen ? <X size={20} /> : <Menu size={20} />}
              <span className="sr-only">{menuOpen ? "Close menu" : "Open menu"}</span>
            </button>
          </div>
        </div>
        <div className="release-ribbon">
          <span className="release-pulse" aria-hidden="true" />
          <span><strong>Live state:</strong> corrected μstd / AeST branch</span>
          <span className="ribbon-separator">·</span>
          <span>Research release {release.commit}</span>
          <Link href="/timeline">Read the correction history <ArrowUpRight size={13} aria-hidden="true" /></Link>
        </div>
      </header>
      <main id="main-content">{children}</main>
      <ResearchGuide />
      <footer className="site-footer">
        <div className="footer-grid">
          <div>
            <BrandMark />
            <p className="footer-note">A public map of the Res Nova research program: questions, theory, evidence, data, and the next bridge to build.</p>
          </div>
          <div className="footer-links">
            <div><span className="footer-label">Explore</span><Link href="/orientation">Start here</Link><Link href="/evidence">Evidence atlas</Link><Link href="/open-problems">Open problems</Link></div>
            <div><span className="footer-label">Read</span><Link href="/publications">Publications</Link><Link href="/data">Data & methods</Link><Link href="/timeline">Timeline</Link></div>
            <div><span className="footer-label">Elsewhere</span><a href={release.links.github} target="_blank" rel="noreferrer">GitHub <ExternalLink size={12} /></a><a href={release.links.zenodo} target="_blank" rel="noreferrer">Zenodo <ExternalLink size={12} /></a><a href={release.links.orcid} target="_blank" rel="noreferrer">ORCID <ExternalLink size={12} /></a></div>
          </div>
        </div>
        <div className="footer-bottom"><span>{release.version} · {release.researchRelease}</span><span>Claims are labeled by evidence status, not by aspiration.</span></div>
      </footer>
    </div>
  );
}

function SectionIntro({ eyebrow, title, body, dark = false }: { eyebrow: string; title: string; body: string; dark?: boolean }) {
  return <div className={`section-intro ${dark ? "section-intro-dark" : ""}`}><span className="eyebrow">{eyebrow}</span><h2>{title}</h2><p>{body}</p></div>;
}

function StatStrip() {
  return <section className="stat-strip" aria-label="Research program at a glance">
    {stats.map((stat) => <div className="stat-item" key={stat.label}><strong>{stat.value}</strong><span>{stat.label}</span><small>{stat.detail}</small></div>)}
  </section>;
}

function LoadingPanel({ label = "Loading visualization…" }: { label?: string }) {
  return <div className="figure-frame loading-panel" role="status" aria-live="polite"><span className="eyebrow">Res Nova field</span><strong>{label}</strong></div>;
}

function FieldArtwork() {
  return <Suspense fallback={<LoadingPanel label="Preparing the cinematic field…" />}><CinematicField /></Suspense>;
}

function Home() {
  const { claims: atlasClaims } = useAtlasData();
  return <>
    <section className="hero-section">
      <div className="hero-grid">
        <div className="hero-copy">
          <div className="hero-kicker"><span className="kicker-line" /> A research atlas for the bridges between theory and observation</div>
          <h1>What if the missing pieces are not missing laws, but <em>missing bridges?</em></h1>
          <p className="hero-lede">Res Nova is a living research program exploring how modified gravity, information geometry, formal verification, and astronomical data can be placed in one evidence-aware conversation.</p>
          <div className="hero-actions"><Link href="/orientation" className="button button-primary">Start with the map <ArrowRight size={17} /></Link><Link href="/evidence" className="button button-quiet">Inspect the evidence <Radar size={16} /></Link></div>
          <div className="hero-footnote"><span className="tiny-check"><Check size={12} /></span><span>Current public state follows the corrected branch and labels unresolved work openly.</span></div>
        </div>
        <FieldArtwork />
      </div>
    </section>
    <StatStrip />
    <section className="intro-band section-pad">
      <SectionIntro eyebrow="Cold reading" title="A way in for people who did not arrive with the repository open." body="The program is easier to understand as a sequence than as a pile of files. Begin with the gap, follow the proposed bridge, inspect the artifact at the end of it, and then ask what still refuses to cross." />
      <div className="intro-cards"><Link href="/orientation" className="intro-card intro-card-featured"><span className="card-index">01 / begin</span><h3>Walk the question</h3><p>Why galaxy dynamics, covariant gravity, and formal proof belong in the same conversation.</p><span className="card-link">Take the guided tour <ArrowUpRight size={15} /></span></Link><Link href="/theory" className="intro-card"><span className="card-index">02 / map</span><h3>See the architecture</h3><p>Trace the route from assumptions to action, observables, and tests.</p><span className="card-link">Open the theory map <ArrowUpRight size={15} /></span></Link><Link href="/data" className="intro-card"><span className="card-index">03 / verify</span><h3>Follow the artifacts</h3><p>Find the datasets, scripts, Lean modules, hashes, and limitations behind the claims.</p><span className="card-link">Enter data & methods <ArrowUpRight size={15} /></span></Link></div>
    </section>
    <section className="program-preview section-pad section-dark">
      <div className="program-header"><SectionIntro dark eyebrow="The program in one view" title="A chain of questions, not a single leap." body="The visual language of the atlas is deliberate: each stage makes a claim, carries an evidence status, and points to the next unresolved dependency." /><Link href="/program" className="button button-outline-light">Explore the program <ArrowUpRight size={16} /></Link></div>
      <div className="bridge-line" aria-label="Research program sequence"><div className="bridge-step"><span>01</span><strong>Gap</strong><small>Where understanding thins</small></div><ArrowRight className="bridge-arrow" /><div className="bridge-step bridge-step-hot"><span>02</span><strong>Bridge</strong><small>A model or derivation</small></div><ArrowRight className="bridge-arrow" /><div className="bridge-step"><span>03</span><strong>Artifact</strong><small>Data, proof, or literature</small></div><ArrowRight className="bridge-arrow" /><div className="bridge-step"><span>04</span><strong>Falsifier</strong><small>What could change our mind</small></div></div>
      <div className="program-note"><Sparkles size={17} /><span>The long-term ToE direction is shown here as a synthesis horizon — not as a current empirical conclusion.</span></div>
    </section>
    <section className="featured-evidence section-pad"><div className="split-heading"><SectionIntro eyebrow="Featured evidence" title="The claim travels with its boundary." body="This atlas treats status as part of the result. What is derived, computed, conditional, open, or superseded stays visible at the point of reading." /><Link href="/evidence" className="text-link">View all claims <ArrowRight size={15} /></Link></div><div className="claim-grid">{atlasClaims.slice(0, 3).map((claim) => <ClaimCard key={claim.id} claim={claim} />)}</div></section>
    <section className="closing-cta"><div className="closing-orbit" aria-hidden="true"><Orbit size={126} strokeWidth={0.5} /></div><div><span className="eyebrow">The next bridge</span><h2>The work is not complete. That is why the map matters.</h2><p>Read the open problems to see which derivations, measurements, and simulations would move the program forward — or stop it.</p><Link href="/open-problems" className="button button-primary">See what remains open <ArrowRight size={16} /></Link></div></section>
  </>;
}

function ClaimCard({ claim, compact = false }: { claim: (typeof claims)[number]; compact?: boolean }) {
  const { release } = useAtlasData();
  const sourcePaths = claim.source.split(";").map((source) => source.trim());
  return <article id={`claim-${claim.id}`} className={`claim-card ${compact ? "claim-card-compact" : ""}`}><div className="claim-card-top"><StatusBadge status={claim.status} compact /><span className="claim-domain">{claim.domain}</span></div><h3>{claim.title}</h3><p>{claim.summary}</p>{!compact && <><div className="claim-limitation"><span>Boundary</span>{claim.limitation}</div><SourceLine><span className="claim-sources">{sourcePaths.map((source) => <a key={source} href={`https://github.com/Mega-Therion/Res-Nova/blob/${release.commit}/${source}`} target="_blank" rel="noreferrer">{source}</a>)}</span></SourceLine><div className="claim-citation-actions"><button type="button" onClick={() => downloadClaimBibtex(claim)}><Download size={13} /> Download BibTeX</button><a href={`https://github.com/Mega-Therion/Res-Nova/blob/${release.commit}/${sourcePaths[0]}`} target="_blank" rel="noreferrer"><ExternalLink size={13} /> Open source</a></div></>}</article>;
}

function Orientation() {
  return <div className="page-wrap"><div className="page-hero page-hero-light"><div><span className="eyebrow">01 / orientation</span><h1>Start with the question. Stay for the evidence.</h1><p>Res Nova is easiest to enter through a simple discipline: separate the place where current understanding is incomplete from the bridge proposed to cross it — and separate both from the proof that the bridge holds.</p></div><div className="page-hero-stamp"><span>READING MODE</span><strong>cold / clear</strong><small>no prior repository context required</small></div></div><div className="orientation-grid"><div className="reading-rail"><span className="rail-line" /><span>THE RESEARCH<br />IN THREE MOVES</span></div><div className="reading-body"><div className="reading-step"><span className="step-number">01</span><div><span className="eyebrow">The gap</span><h2>Physics has places where the fit is better than the explanation.</h2><p>Galaxy rotation curves, cosmological behavior, and gravitational theory are not empty territories. They are precisely where successful observations meet incomplete bridges between scales, fields, and interpretations.</p><div className="pull-quote">“A ledger of uncertainty is not a weakness. It is the part of the theory that can still be tested.”</div></div></div><div className="reading-step"><span className="step-number">02</span><div><span className="eyebrow">The bridge</span><h2>The program proposes a route from structure to dynamics.</h2><p>The current live state studies a corrected interpolation branch and a genuine AeST covariant completion. It asks whether an action can connect a weak-field phenomenology to a relativistic theory without hiding its assumptions in the seams.</p><Link href="/theory" className="inline-arrow">Follow the theory map <ArrowRight size={15} /></Link></div></div><div className="reading-step"><span className="step-number">03</span><div><span className="eyebrow">The check</span><h2>The bridge ends in an artifact — or it remains a proposal.</h2><p>SPARC fits, redshift tests, Lean modules, literature comparisons, and correction records occupy different evidence categories. The site keeps them legible as different kinds of knowledge rather than flattening them into one score.</p><Link href="/evidence" className="inline-arrow">Open the evidence atlas <ArrowRight size={15} /></Link></div></div></div></div><section className="glossary-strip"><div><span className="eyebrow">A small vocabulary</span><h2>Four terms to keep the map readable.</h2></div><div className="glossary-list">{glossary.map((item) => <details key={item.term}><summary>{item.term}<ChevronDown size={15} /></summary><p>{item.definition}</p></details>)}</div></section></div>;
}

function Program() {
  const { workstreams: atlasWorkstreams } = useAtlasData();
  return <div className="page-wrap"><div className="page-hero page-hero-dark"><div><span className="eyebrow">02 / the program</span><h1>A research program is a set of dependencies made visible.</h1><p>Each workstream below has its own pace, evidence standard, and unresolved edge. The program is not a ladder where every rung is complete; it is a network where the open edges matter.</p></div><div className="page-index-grid"><span>{atlasWorkstreams.length}</span><small>active<br />workstreams</small><span>6</span><small>evidence<br />states</small></div></div><section className="section-pad program-body"><div className="split-heading"><SectionIntro eyebrow="Workstreams" title="Five layers, one audit trail." body="Progress is shown as orientation, not as a scientific confidence score. Read the status label beside it to understand what kind of progress is being claimed." /></div><div className="workstream-list">{atlasWorkstreams.map((item, index) => <div className="workstream-row" key={item.id}><div className="workstream-number">0{index + 1}</div><div className="workstream-main"><div className="workstream-title"><h3>{item.label}</h3><StatusBadge status={item.status} compact /></div><p>{item.short}</p><div className="progress-track"><span style={{ width: `${item.progress}%`, background: item.color }} /></div></div><span className="workstream-progress">{item.progress}%<small>mapped</small></span><ArrowUpRight className="row-arrow" size={18} /></div>)}</div><div className="program-logic"><div className="logic-label"><span className="eyebrow">The logic</span><h2>Every bridge adds an obligation.</h2></div><div className="logic-cards"><div><Layers3 size={19} /><strong>Define</strong><p>Name the object and its assumptions.</p></div><div><GitBranch size={19} /><strong>Connect</strong><p>Show the derivation or model transition.</p></div><div><ShieldCheck size={19} /><strong>Test</strong><p>Attach the artifact and its failure mode.</p></div></div></div></section></div>;
}

function Theory() {
  return <div className="page-wrap"><div className="page-hero page-hero-light"><div><span className="eyebrow">03 / theory map</span><h1>From a mathematical object to a question the sky can answer.</h1><p>Use this as a map, not a proof. Each node is a conceptual handoff; the evidence atlas records whether the handoff has been derived, computed, cited, or left open.</p></div><div className="equation-hero"><span>live branch</span><strong>μstd(x) = <i>x</i> / √(1 + <i>x</i>²)</strong><small>conditional structural choice</small></div></div><section className="section-pad theory-section"><Suspense fallback={<LoadingPanel label="Loading the theory map…" />}><TheoryMapExplorer /></Suspense><div className="theory-notes"><div><span className="eyebrow">Read the map</span><h2>The hardest step is often the arrow between boxes.</h2></div><div className="note-list"><div><span>01</span><p><strong>Definitions are not discoveries.</strong> A formal object can be internally coherent while its physical interpretation remains conditional.</p></div><div><span>02</span><p><strong>Phenomenology is not completion.</strong> A fit to galaxy data does not by itself supply a covariant theory.</p></div><div><span>03</span><p><strong>A correction is part of the result.</strong> The retired branch remains visible because the route by which it failed is informative.</p></div></div></div></section></div>;
}

function TheoryNode({ number, title, detail, status, icon }: { number: string; title: string; detail: string; status: EvidenceStatus; icon: React.ReactNode }) {
  return <div className={`theory-node node-status-${statusMeta[status].tone}`}><span className="theory-node-number">{number}</span><span className="theory-node-icon">{icon}</span><strong>{title}</strong><small>{detail}</small><StatusBadge status={status} compact /></div>;
}

function Evidence() {
  const [filter, setFilter] = useState<"all" | EvidenceStatus>("all");
  const [query, setQuery] = useState("");
  const { claims: atlasClaims } = useAtlasData();
  const filtered = useMemo(() => atlasClaims.filter((claim) => (filter === "all" || claim.status === filter) && `${claim.title} ${claim.domain} ${claim.summary}`.toLowerCase().includes(query.toLowerCase())), [atlasClaims, filter, query]);
  return <div className="page-wrap"><div className="page-hero page-hero-dark"><div><span className="eyebrow">04 / evidence atlas</span><h1>The claim travels with its boundary.</h1><p>Filter the program by what kind of support it has. The atlas is designed to make the limitations as findable as the headline.</p></div><div className="evidence-legend"><span className="eyebrow">Status key</span><div><StatusBadge status="derived" compact /><StatusBadge status="computed" compact /><StatusBadge status="conditional" compact /><StatusBadge status="open" compact /><StatusBadge status="superseded" compact /></div></div></div><section className="section-pad evidence-section"><div className="evidence-toolbar"><label className="search-field"><Search size={16} /><span className="sr-only">Search claims</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search claims, domains, or artifacts" /></label><div className="filter-group" role="group" aria-label="Filter evidence status"><button className={filter === "all" ? "filter-active" : ""} onClick={() => setFilter("all")}>All <span>{atlasClaims.length}</span></button>{(["derived", "computed", "conditional", "open", "superseded"] as EvidenceStatus[]).map((status) => <button key={status} className={filter === status ? "filter-active" : ""} onClick={() => setFilter(status)}>{statusMeta[status].label} <span>{atlasClaims.filter((claim) => claim.status === status).length}</span></button>)}</div></div><div className="atlas-callout"><Quote size={18} /><p>“A claim's presence in the ledger records auditability — it does not substitute for empirical consensus.”</p><span>— Res Nova epistemic standard</span></div><div className="claim-grid evidence-grid">{filtered.map((claim) => <ClaimCard key={claim.id} claim={claim} />)}</div>{filtered.length === 0 && <div className="empty-state"><Search size={22} /><h3>No claims match that filter.</h3><button onClick={() => { setFilter("all"); setQuery(""); }}>Reset atlas</button></div>}</section></div>;
}

function ReleaseTracePanel() {
  const { claims: atlasClaims, release } = useAtlasData();
  return <div className="release-trace-panel"><div><span className="eyebrow">Release-linked artifacts</span><h2>Download the exact slice shown here.</h2><p>The explorer is generated from canonical SPARC point-level files. The claim registry and release checklist remain the source of truth for what the current Res Nova branch claims.</p><div className="registry-status"><span>release snapshot <b>{release.researchRelease}</b></span><span>release commit <b>{release.commit}</b></span><span>claims tracked <b>{atlasClaims.length}</b></span><span>source <b>database</b></span></div></div><div className="release-trace-links"><a className="button button-dark" href="/downloads/sparc-rotation-curves-slice.csv" download>Download data <ArrowDownRight size={15} /></a><a className="button button-outline" href="/downloads/sparc-rotation-curves-slice.svg" download>Download SVG chart <ArrowDownRight size={15} /></a><a className="text-link" href={release.links.claimRegistry} target="_blank" rel="noreferrer">Claim registry <ExternalLink size={14} /></a><a className="text-link" href={release.links.releaseManifest} target="_blank" rel="noreferrer">Release checklist <ExternalLink size={14} /></a></div><SourceLine>{sparcSource.authors} · {sparcSource.archiveFile} · {sparcSource.doi} · {sparcSource.license}</SourceLine></div>;
}

function DataMethods() {
  const { datasets: atlasDatasets, release } = useAtlasData();
  return <div className="page-wrap"><div className="page-hero page-hero-light"><div><span className="eyebrow">05 / data & methods</span><h1>Follow the artifacts, not just the argument.</h1><p>The public research package is a set of source datasets, transformations, formal modules, manifests, and correction records. This page is the doorway into that chain.</p></div><div className="data-stamp"><Database size={23} /><strong>OPEN<br />METHODS</strong><small>source · script · hash · limit</small></div></div><section className="section-pad data-section"><div className="data-grid"><div className="data-main"><SectionIntro eyebrow="Dataset index" title="What the current public state can show." body="These cards are intentionally compact. Each points to a deeper repository artifact and carries the caveat that should travel with it." /><div className="dataset-list">{atlasDatasets.map((dataset) => <article className="dataset-card" key={dataset.name}><span className="dataset-accent" style={{ background: dataset.color }} /><div><div className="dataset-card-top"><span className="eyebrow">Dataset / artifact</span><ArrowUpRight size={16} /></div><h3>{dataset.name}</h3><strong>{dataset.scope}</strong><p>{dataset.provenance}</p><SourceLine>{dataset.artifact}</SourceLine></div></article>)}</div></div><aside className="repro-card"><div className="repro-icon"><FileCode2 size={20} /></div><span className="eyebrow">Reproduction path</span><h2>One release should answer four questions.</h2><ol><li><span>01</span>Which model state is live?</li><li><span>02</span>Which data and version were used?</li><li><span>03</span>Which command regenerates the result?</li><li><span>04</span>What would falsify it?</li></ol><a className="button button-dark" href={release.links.github} target="_blank" rel="noreferrer">Open source repository <Github size={16} /></a></aside></div><Suspense fallback={<LoadingPanel label="Loading the rotation curve explorer…" />}><RotationCurveExplorer /></Suspense><div className="package-figure-grid"><Suspense fallback={<LoadingPanel label="Loading SPARC small multiples…" />}><SmallMultiplesFigure /></Suspense><Suspense fallback={<LoadingPanel label="Loading radial acceleration…" />}><RarFigure /></Suspense></div><div className="package-figure-grid"><Suspense fallback={<LoadingPanel label="Loading the a₀ interval…" />}><A0IntervalFigure /></Suspense><Suspense fallback={<LoadingPanel label="Loading χ² comparison…" />}><Chi2Figure /></Suspense></div><Suspense fallback={<LoadingPanel label="Loading horizon corollary…" />}><HorizonFigure /></Suspense><Suspense fallback={<LoadingPanel label="Loading comparison chart…" />}><ComparisonChart /></Suspense><ResearchFileLibrary /><ImportProvenancePanel /><ReleaseTracePanel /></section></div>;
}

function Publications() {
  const { publications: atlasPublications, release } = useAtlasData();
  return <div className="page-wrap"><div className="page-hero page-hero-dark"><div><span className="eyebrow">06 / publications</span><h1>Read the work at the depth you need.</h1><p>Start with the orientation, move into the canonical manuscript, or go directly to the source code and formal artifacts. Every item is labeled by what it is.</p></div><div className="publication-hero-icon"><BookOpen size={42} strokeWidth={1} /><span>paper / source / archive</span></div></div><section className="section-pad publication-section"><div className="publication-feature"><div className="pub-cover"><span>RES<br /><em>NOVA</em></span><small>research release / 2026</small></div><div className="pub-feature-copy"><span className="eyebrow">Featured reading</span><h2>Dual-Channel Variational Closure, Covariant Completion, and a Reproducible SPARC Benchmark</h2><p>The canonical manuscript lineage is being realigned around the corrected live branch. Read it alongside the evidence ledger and current-state correction record rather than as a standalone claim of completion.</p><div className="pub-actions"><a className="button button-primary" href={release.links.github} target="_blank" rel="noreferrer">Open source <Github size={16} /></a><a className="text-link" href={release.links.zenodo} target="_blank" rel="noreferrer">Archive / DOI <ExternalLink size={15} /></a></div></div></div><div className="publication-list"><div className="split-heading"><SectionIntro eyebrow="Library" title="A publication is one doorway into the program." body="The source repository, formalization suite, and research release are designed to be read together." /></div>{atlasPublications.map((pub) => <article className="publication-row" key={pub.title}><div className="publication-type"><span>{pub.type}</span><strong>{pub.year}</strong></div><div className="publication-content"><h3>{pub.title}</h3><p>{pub.summary}</p></div><div className="publication-meta"><span className="status-badge status-slate status-compact"><span className="status-dot" />{pub.tag}</span><a href={pub.href} target="_blank" rel="noreferrer" aria-label={`Open ${pub.title}`}>Open <ArrowUpRight size={15} /></a></div></article>)}</div></section></div>;
}

function OpenProblems() {
  const problems = [
    { n: "O1", title: "Can the acceleration scale be derived rather than fitted?", status: "open" as EvidenceStatus, body: "The thermal analogy identifies a scale relation, but the physical normalization remains a separate open question." },
    { n: "D2", title: "Why should the structural choice be physically necessary?", status: "conditional" as EvidenceStatus, body: "The uniqueness statement is conditional on its Padé / structural postulates. The postulates themselves are not derived from a deeper principle." },
    { n: "D3", title: "Can the corrected covariant branch close the full solar-system sector?", status: "open" as EvidenceStatus, body: "The current state separates tensor speed and selected weak-field results from unresolved post-Newtonian and screening calculations." },
    { n: "D5", title: "What happens in nonlinear structure formation?", status: "open" as EvidenceStatus, body: "Background and linear work do not substitute for an independent nonlinear AeST structure-formation simulation." },
  ];
  return <div className="page-wrap"><div className="page-hero page-hero-light"><div><span className="eyebrow">07 / open problems</span><h1>A theory becomes more useful when it names what could stop it.</h1><p>These are not decorative “future work” bullets. They are the next obligations in the chain, with explicit ways the program could narrow, change, or fail.</p></div><div className="stop-card"><ShieldCheck size={22} /><strong>falsifiability<br />is a feature</strong></div></div><section className="section-pad problems-section"><div className="problems-intro"><SectionIntro eyebrow="The active frontier" title="The open edges are where the next evidence belongs." body="A public program should make it easy to see the distance between a compelling idea and a completed result." /><div className="problem-quote">“What would change our mind?”<small>the question every bridge carries</small></div></div><div className="problem-list">{problems.map((problem) => <article className="problem-row" key={problem.n}><span className="problem-number">{problem.n}</span><div><div className="problem-title"><h3>{problem.title}</h3><StatusBadge status={problem.status} compact /></div><p>{problem.body}</p></div><ArrowDownRight size={19} className="problem-arrow" /></article>)}</div><div className="historical-note"><div><span className="eyebrow">Correction history</span><h2>Retired branches stay visible.</h2><p>The old μdual branch and earlier covariant calculations are preserved as a record of how the program learned. They are not used as current evidence.</p></div><Link href="/timeline" className="button button-quiet">See the timeline <ArrowRight size={16} /></Link></div></section></div>;
}

function Timeline() {
  const { timeline: atlasTimeline, release } = useAtlasData();
  return <div className="page-wrap"><div className="page-hero page-hero-dark"><div><span className="eyebrow">08 / timeline</span><h1>The route matters — especially where it changed.</h1><p>Corrections are not footnotes to hide. They are part of the epistemic architecture of a research program.</p></div><div className="timeline-mark"><span>state</span><strong>LIVE</strong><small>correction-aware</small></div></div><section className="section-pad timeline-section"><div className="timeline-intro"><SectionIntro eyebrow="Selected milestones" title="From corpus to public map." body="The timeline is intentionally selective. It shows the changes that alter how a reader should interpret the current work." /><a className="text-link" href={release.links.github} target="_blank" rel="noreferrer">View commit history <ExternalLink size={15} /></a></div><div className="timeline-list">{atlasTimeline.map((item, index) => <div className="timeline-item" key={item.date}><div className="timeline-date">{item.date}</div><div className="timeline-spine"><span className={index === atlasTimeline.length - 1 ? "timeline-dot timeline-dot-live" : "timeline-dot"} /><span className="timeline-rule" /></div><div className="timeline-copy"><h3>{item.title}</h3><p>{item.body}</p></div></div>)}</div></section></div>;
}

function About() {
  return <div className="page-wrap"><div className="page-hero page-hero-light"><div><span className="eyebrow">09 / about</span><h1>A public map for an independent research program.</h1><p>Res Nova is being developed as a transparent research object: the ideas, the code, the formal artifacts, the data, the corrections, and the questions that remain.</p></div><div className="about-seal"><Orbit size={39} strokeWidth={1} /><span>RWY<br /><small>independent researcher</small></span></div></div><section className="section-pad about-section"><div className="about-grid"><div><SectionIntro eyebrow="The researcher" title="R.W. Yett" body="Independent researcher working across theoretical physics, modified gravity, information geometry, formal verification, and reproducible computational research." /><div className="about-links"><a className="button button-dark" href={releaseState.links.orcid} target="_blank" rel="noreferrer">ORCID <ExternalLink size={15} /></a><a className="button button-outline" href={releaseState.links.github} target="_blank" rel="noreferrer">GitHub <Github size={15} /></a></div></div><div className="about-principles"><span className="eyebrow">Working principles</span><div><Check size={17} /><p>Say what is derived, measured, cited, conditional, open, or refuted.</p></div><div><Check size={17} /><p>Keep the source, data, method, and limitation close to the claim.</p></div><div><Check size={17} /><p>Let a correction update the public map instead of disappearing into history.</p></div></div></div><div className="contact-panel"><div><span className="eyebrow">A note to readers</span><h2>You do not need to agree with the theory to use the map.</h2><p>The purpose of this site is to make the research inspectable: to give a cold reader a fair route in, and a skeptical reader enough edges to test.</p></div><Link href="/orientation" className="button button-primary">Begin the guided tour <Play size={15} fill="currentColor" /></Link></div></section></div>;
}

function NotFound() {
  return <div className="not-found"><span className="eyebrow">404 / outside the atlas</span><h1>This page has not been mapped yet.</h1><p>Return to the overview or enter through the guided orientation.</p><Link className="button button-primary" href="/">Return home <ArrowRight size={16} /></Link></div>;
}

function AppRouter() {
  return <Switch><Route path="/" component={Home} /><Route path="/orientation" component={Orientation} /><Route path="/program" component={Program} /><Route path="/theory" component={Theory} /><Route path="/evidence" component={Evidence} /><Route path="/data" component={DataMethods} /><Route path="/publications" component={Publications} /><Route path="/open-problems" component={OpenProblems} /><Route path="/timeline" component={Timeline} /><Route path="/about" component={About} /><Route component={NotFound} /></Switch>;
}

export default function App() {
  const [location] = useLocation();
  const snapshot = trpc.atlas.snapshot.useQuery(undefined, { enabled: !location.startsWith("/admin"), retry: false });
  const atlas = useMemo(() => normalizeAtlasData(snapshot.data as unknown as PersistedSnapshot | undefined, snapshot.isLoading), [snapshot.data, snapshot.isLoading]);
  if (location.startsWith("/admin")) return <ErrorBoundary><ThemeProvider defaultTheme="light"><Suspense fallback={<LoadingPanel label="Loading admin workspace…" />}><AdminDashboard /></Suspense></ThemeProvider></ErrorBoundary>;
  return <ErrorBoundary><AtlasDataContext.Provider value={atlas}><ThemeProvider defaultTheme="light"><Layout><AppRouter /></Layout></ThemeProvider></AtlasDataContext.Provider></ErrorBoundary>;
}
