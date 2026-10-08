import { useEffect, useMemo, useRef, useState } from "react";
import { ChevronLeft, ChevronRight, Download, Info, RotateCcw } from "lucide-react";
import { canonicalSparcCurves, sparcSource } from "@/data/sparc";
import { exportSvgAsPng, exportSvgElement, niceTicks } from "@/lib/chart";
import { cn } from "@/lib/cn";

const curves = canonicalSparcCurves.map((curve) => ({
  ...curve,
  points: curve.points.map((point) => ({
    radius: point.radius,
    observed: point.observed,
    model: point.baryonicBaseline,
    uncertainty: point.uncertainty,
  })),
}));

const W = 760;
const MAIN = 318;
const GAP = 18;
const RES = 108;
const H = MAIN + GAP + RES;
const P = { l: 58, r: 18, t: 16, b: 28 };
const PAGE = 16;
const DEFAULT_ID = curves.find((c) => c.name === "NGC3198")?.id ?? curves[0].id;

function formatVel(value: number) {
  return `${value.toFixed(0)} km/s`;
}

function Sparkline({ points, active }: { points: Array<{ radius: number; observed: number; model: number }>; active?: boolean }) {
  const xMax = Math.max(...points.map((p) => p.radius), 1);
  const yMax = Math.max(...points.map((p) => p.observed), 1);
  const d = points
    .map((p, i) => `${i === 0 ? "M" : "L"} ${((p.radius / xMax) * 88 + 4).toFixed(1)} ${(28 - (p.observed / yMax) * 22).toFixed(1)}`)
    .join(" ");
  const m = points
    .map((p, i) => `${i === 0 ? "M" : "L"} ${((p.radius / xMax) * 88 + 4).toFixed(1)} ${(28 - (p.model / yMax) * 22).toFixed(1)}`)
    .join(" ");
  return (
    <svg viewBox="0 0 96 32" className="h-8 w-24" aria-hidden="true">
      <path d={m} fill="none" stroke="var(--color-model)" strokeWidth="1.2" opacity={active ? 1 : 0.55} />
      <path d={d} fill="none" stroke="var(--color-obs)" strokeWidth="1.4" />
    </svg>
  );
}

export function RotationCurveExplorer() {
  const svgRef = useRef<SVGSVGElement>(null);
  const [galaxyId, setGalaxyId] = useState<string>(DEFAULT_ID);
  const [showModel, setShowModel] = useState(true);
  const [showUncertainty, setShowUncertainty] = useState(true);
  const [activeIndex, setActiveIndex] = useState(0);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(0);
  const galaxy = curves.find((item) => item.id === galaxyId) ?? curves[0];
  const filtered = useMemo(
    () => curves.filter((item) => item.name.toLowerCase().includes(search.toLowerCase())),
    [search],
  );
  const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE));
  const pageCurves = filtered.slice(page * PAGE, page * PAGE + PAGE);
  const activePoint = galaxy.points[activeIndex] ?? galaxy.points[0];
  const residual = activePoint.observed - activePoint.model;

  const scales = useMemo(() => {
    const xMax = Math.max(...galaxy.points.map((p) => p.radius), 1) * 1.08;
    const yMax = Math.max(...galaxy.points.map((p) => p.observed + p.uncertainty), ...galaxy.points.map((p) => p.model), 40) * 1.12;
    const rMax = Math.max(...galaxy.points.map((p) => Math.abs(p.observed - p.model) + p.uncertainty), 12) * 1.15;
    const xScale = (v: number) => Number((P.l + (v / xMax) * (W - P.l - P.r)).toFixed(2));
    const yScale = (v: number) => Number((MAIN - P.b - (Math.max(0, v) / yMax) * (MAIN - P.t - P.b)).toFixed(2));
    const rScale = (v: number) => Number((MAIN + GAP + RES / 2 - (v / rMax) * ((RES - 28) / 2)).toFixed(2));
    return {
      xMax,
      yMax,
      rMax,
      xScale,
      yScale,
      rScale,
      xt: niceTicks(0, xMax, 5),
      yt: niceTicks(0, yMax, 5),
      rt: niceTicks(-rMax, rMax, 3),
    };
  }, [galaxy]);

  const observedPath = galaxy.points
    .map((p, i) => `${i === 0 ? "M" : "L"} ${scales.xScale(p.radius).toFixed(1)} ${scales.yScale(p.observed).toFixed(1)}`)
    .join(" ");
  const modelPath = galaxy.points
    .map((p, i) => `${i === 0 ? "M" : "L"} ${scales.xScale(p.radius).toFixed(1)} ${scales.yScale(p.model).toFixed(1)}`)
    .join(" ");
  const residualPath = galaxy.points
    .map((p, i) => `${i === 0 ? "M" : "L"} ${scales.xScale(p.radius).toFixed(1)} ${scales.rScale(p.observed - p.model).toFixed(1)}`)
    .join(" ");

  const selectGalaxy = (id: string) => {
    setGalaxyId(id);
    setActiveIndex(0);
    const idx = filtered.findIndex((item) => item.id === id);
    if (idx >= 0) setPage(Math.floor(idx / PAGE));
  };

  useEffect(() => {
    const handle = (event: Event) => {
      const detail = (event as CustomEvent<{ galaxy?: string; showModel?: boolean; showUncertainty?: boolean }>).detail;
      if (detail.galaxy) {
        const requested = curves.find((item) => item.name.toLowerCase() === detail.galaxy?.toLowerCase());
        if (requested) selectGalaxy(requested.id);
      }
      if (typeof detail.showModel === "boolean") setShowModel(detail.showModel);
      if (typeof detail.showUncertainty === "boolean") setShowUncertainty(detail.showUncertainty);
    };
    window.addEventListener("resnova:guide-action", handle);
    return () => window.removeEventListener("resnova:guide-action", handle);
  }, []);

  const exportChart = (format: "svg" | "png") => {
    const svg = svgRef.current;
    if (!svg) return;
    const name = `${galaxy.name.toLowerCase()}-rotation-curve.${format}`;
    if (format === "svg") exportSvgElement(svg, name);
    else exportSvgAsPng(svg, name, "#09080c");
  };

  return (
    <section className="mt-16" aria-labelledby="rotation-explorer-title">
      <div className="mb-6 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div className="max-w-xl">
          <span className="eyebrow">Canonical evidence · {sparcSource.galaxyCount} galaxies · {sparcSource.authors}</span>
          <h2 id="rotation-explorer-title" className="mt-3 font-display text-[clamp(1.8rem,3.4vw,2.6rem)] font-medium leading-tight">
            Read the curve point by point.
          </h2>
          <p className="mt-3 text-muted">
            Hover a marker to inspect an official SPARC radius, measured velocity, uncertainty, and the published baryonic baseline. The lower panel is V_obs − V_bar. Axes autoscale per galaxy.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <label className="sr-only" htmlFor="galaxy-search">Find galaxy</label>
          <input
            id="galaxy-search"
            className="min-h-11 w-32 border border-line bg-surface px-3 font-mono text-sm"
            value={search}
            onChange={(e) => { setSearch(e.target.value); setPage(0); }}
            placeholder="NGC…"
          />
          <label className="sr-only" htmlFor="galaxy-select">Galaxy</label>
          <select
            id="galaxy-select"
            className="min-h-11 border border-line bg-surface px-3 font-mono text-sm"
            value={galaxyId}
            onChange={(e) => selectGalaxy(e.target.value)}
          >
            {(filtered.some((item) => item.id === galaxyId) ? filtered : [galaxy, ...filtered]).map((item) => (
              <option key={item.id} value={item.id}>{item.name}</option>
            ))}
          </select>
          <button type="button" className={cn("btn btn-quiet min-h-11 px-3", showModel && "border-accent text-accent")} aria-pressed={showModel} onClick={() => setShowModel(!showModel)}>
            Baseline
          </button>
          <button type="button" className={cn("btn btn-quiet min-h-11 px-3", showUncertainty && "border-accent text-accent")} aria-pressed={showUncertainty} onClick={() => setShowUncertainty(!showUncertainty)}>
            Uncertainty
          </button>
        </div>
      </div>

      <div className="grid gap-5 lg:grid-cols-[1.45fr_.55fr]">
        <div className="figure-frame rounded-xl p-4">
          <svg
            ref={svgRef}
            viewBox={`0 0 ${W} ${H}`}
            className="w-full"
            role="img"
            aria-label={`Canonical SPARC rotation curve for ${galaxy.name} with residual panel`}
            tabIndex={0}
            onKeyDown={(event) => {
              if (event.key === "ArrowRight") {
                event.preventDefault();
                setActiveIndex((index) => Math.min(galaxy.points.length - 1, index + 1));
              }
              if (event.key === "ArrowLeft") {
                event.preventDefault();
                setActiveIndex((index) => Math.max(0, index - 1));
              }
            }}
          >
            {scales.yt.map((tick) => (
              <g key={`y${tick}`}>
                <line className="plot-grid" x1={P.l} x2={W - P.r} y1={scales.yScale(tick)} y2={scales.yScale(tick)} />
                <text className="plot-tick" x={P.l - 8} y={scales.yScale(tick) + 4} textAnchor="end">
                  {Math.round(tick)}
                </text>
              </g>
            ))}
            {scales.xt.map((tick) => (
              <g key={`x${tick}`}>
                <line className="plot-grid" x1={scales.xScale(tick)} x2={scales.xScale(tick)} y1={P.t} y2={MAIN - P.b} />
              </g>
            ))}
            <line className="plot-axis" x1={P.l} x2={W - P.r} y1={MAIN - P.b} y2={MAIN - P.b} />
            <line className="plot-axis" x1={P.l} x2={P.l} y1={P.t} y2={MAIN - P.b} />
            {showUncertainty &&
              galaxy.points.map((point) => (
                <line
                  key={`e-${point.radius}`}
                  x1={scales.xScale(point.radius)}
                  x2={scales.xScale(point.radius)}
                  y1={scales.yScale(point.observed - point.uncertainty)}
                  y2={scales.yScale(point.observed + point.uncertainty)}
                  stroke="var(--color-obs)"
                  strokeOpacity="0.45"
                  strokeWidth="1.4"
                />
              ))}
            {showModel && <path d={modelPath} fill="none" stroke="var(--color-model)" strokeWidth="2.2" />}
            <path d={observedPath} fill="none" stroke="var(--color-obs)" strokeWidth="1.4" strokeOpacity="0.35" />
            {galaxy.points.map((point, index) => (
              <circle
                key={`${galaxy.id}-${point.radius}`}
                cx={scales.xScale(point.radius)}
                cy={scales.yScale(point.observed)}
                r={activeIndex === index ? 6 : 3.6}
                fill="var(--color-obs)"
                tabIndex={0}
                role="button"
                aria-label={`${galaxy.name}, radius ${point.radius} kiloparsecs, observed ${formatVel(point.observed)}`}
                onMouseEnter={() => setActiveIndex(index)}
                onFocus={() => setActiveIndex(index)}
              />
            ))}
            <text className="plot-label" transform={`translate(16 ${MAIN / 2}) rotate(-90)`} textAnchor="middle">
              V (km/s)
            </text>

            <line x1={P.l} x2={W - P.r} y1={scales.rScale(0)} y2={scales.rScale(0)} stroke="var(--color-muted)" strokeDasharray="4 4" />
            {scales.rt.map((tick) => (
              <text key={`r${tick}`} className="plot-tick" x={P.l - 8} y={scales.rScale(tick) + 4} textAnchor="end">
                {Math.round(tick)}
              </text>
            ))}
            {showUncertainty &&
              galaxy.points.map((point) => (
                <line
                  key={`re-${point.radius}`}
                  x1={scales.xScale(point.radius)}
                  x2={scales.xScale(point.radius)}
                  y1={scales.rScale(point.observed - point.model - point.uncertainty)}
                  y2={scales.rScale(point.observed - point.model + point.uncertainty)}
                  stroke="var(--color-obs)"
                  strokeOpacity="0.35"
                  strokeWidth="1.2"
                />
              ))}
            {showModel && <path d={residualPath} fill="none" stroke="var(--color-obs)" strokeWidth="1.5" />}
            {galaxy.points.map((point, index) => (
              <circle
                key={`rp-${point.radius}`}
                cx={scales.xScale(point.radius)}
                cy={scales.rScale(point.observed - point.model)}
                r={activeIndex === index ? 4.5 : 2.6}
                fill="var(--color-obs)"
                onMouseEnter={() => setActiveIndex(index)}
              />
            ))}
            {scales.xt.map((tick) => (
              <text key={`xb${tick}`} className="plot-tick" x={scales.xScale(tick)} y={H - 6} textAnchor="middle">
                {tick < 10 ? tick.toFixed(1) : Math.round(tick)}
              </text>
            ))}
            <line className="plot-axis" x1={P.l} x2={W - P.r} y1={H - 22} y2={H - 22} />
            <line className="plot-axis" x1={P.l} x2={P.l} y1={MAIN + GAP} y2={H - 22} />
            <text className="plot-label" x={(P.l + W - P.r) / 2} y={MAIN - 8} textAnchor="middle">
              radius (kpc)
            </text>
            <text className="plot-label" transform={`translate(16 ${MAIN + GAP + RES / 2}) rotate(-90)`} textAnchor="middle">
              ΔV (km/s)
            </text>
          </svg>
          <div className="mt-2 flex flex-wrap gap-4 px-1 font-mono text-[10px] uppercase tracking-wider text-muted">
            <span className="inline-flex items-center gap-2"><i className="size-2.5 rounded-full bg-obs" /> observed</span>
            <span className="inline-flex items-center gap-2"><i className="h-0.5 w-5 bg-model" /> baryonic baseline</span>
            <span className="inline-flex items-center gap-2"><i className="h-3 w-0.5 bg-obs/50" /> ± published error</span>
            <span>lower panel · residual</span>
          </div>
        </div>

        <aside className="flex flex-col border border-line bg-surface p-5">
          <span className="eyebrow">Selected point</span>
          <strong className="mt-3 font-display text-4xl font-medium tabular-nums">{formatVel(activePoint.observed)}</strong>
          <p className="mt-3 text-sm leading-relaxed text-muted">
            At <b className="text-ink">{activePoint.radius.toFixed(2)} kpc</b>, the observed curve sits{" "}
            <b className="text-ink">{Math.abs(residual).toFixed(0)} km/s {residual >= 0 ? "above" : "below"}</b> the published baryonic baseline.
          </p>
          <div className="mt-4 grid grid-cols-2 gap-2 font-mono text-[10px] uppercase tracking-wider text-muted">
            <span>error <b className="block text-ink normal-case tracking-normal">±{formatVel(activePoint.uncertainty)}</b></span>
            <span>baseline <b className="block text-ink normal-case tracking-normal">{formatVel(activePoint.model)}</b></span>
            <span>distance <b className="block text-ink normal-case tracking-normal">{galaxy.distance.replace(" Mpc Mpc", " Mpc")}</b></span>
            <span>points <b className="block text-ink normal-case tracking-normal">{galaxy.points.length}</b></span>
          </div>
          <p className="mt-4 flex gap-2 text-[12px] leading-relaxed text-muted">
            <Info size={14} className="mt-0.5 shrink-0 text-accent" />
            {galaxy.note}
          </p>
          <div className="mt-auto pt-5">
            <span className="font-mono text-[10px] uppercase tracking-widest text-muted">Publication exports</span>
            <div className="mt-2 flex gap-2">
              <button type="button" className="btn btn-quiet min-h-10 px-3" onClick={() => exportChart("png")}><Download size={12} /> PNG</button>
              <button type="button" className="btn btn-quiet min-h-10 px-3" onClick={() => exportChart("svg")}><Download size={12} /> SVG</button>
            </div>
            <a className="mt-3 inline-flex font-mono text-[10px] uppercase tracking-widest text-accent" href={sparcSource.archiveUrl} target="_blank" rel="noreferrer">
              Source archive · {sparcSource.doi}
            </a>
            <button
              className="btn btn-quiet mt-3 w-full"
              type="button"
              onClick={() => { setGalaxyId(DEFAULT_ID); setActiveIndex(0); setPage(0); setSearch(""); setShowModel(true); setShowUncertainty(true); }}
            >
              <RotateCcw size={13} /> Reset explorer
            </button>
          </div>
        </aside>
      </div>

      <div className="mt-5 grid grid-cols-2 gap-2 sm:grid-cols-4 lg:grid-cols-8">
        {pageCurves.map((item) => (
          <button
            key={item.id}
            type="button"
            onClick={() => selectGalaxy(item.id)}
            className={cn(
              "flex min-h-16 flex-col items-start border border-line bg-surface px-2 py-2 text-left",
              item.id === galaxyId && "border-accent",
            )}
          >
            <Sparkline points={item.points} active={item.id === galaxyId} />
            <span className="mt-1 font-mono text-[10px] tracking-wide">{item.name}</span>
          </button>
        ))}
      </div>

      <div className="mt-4 flex items-center justify-between font-mono text-[11px] text-muted">
        <button type="button" className="btn btn-quiet min-h-10 px-3" disabled={page === 0} onClick={() => setPage((p) => Math.max(0, p - 1))} aria-label="Previous galaxy page">
          <ChevronLeft size={14} />
        </button>
        <span>
          {filtered.length ? page * PAGE + 1 : 0}–{Math.min((page + 1) * PAGE, filtered.length)} / {filtered.length} galaxies
        </span>
        <button type="button" className="btn btn-quiet min-h-10 px-3" disabled={page >= pageCount - 1} onClick={() => setPage((p) => Math.min(pageCount - 1, p + 1))} aria-label="Next galaxy page">
          <ChevronRight size={14} />
        </button>
      </div>
    </section>
  );
}

export default RotationCurveExplorer;

