import { useMemo, useState, type MouseEvent } from "react";
import { a0Measurement, gDeepMond, gMondDual, gMondStd } from "@/data/research";
import { rarPoints, rarSource } from "@/data/rar";
import { decadeLabel, linePath, logTicks } from "@/lib/chart";
import { FigureFrame } from "@/components/figure-frame";

const A0 = a0Measurement.t1.value;
const XMIN = -12.2;
const XMAX = -8.05;
const YMIN = -12.2;
const YMAX = -8.05;

function log10(value: number) {
  return Math.log10(value);
}

function modelSeries() {
  const xs = Array.from({ length: 72 }, (_, i) => 10 ** (XMIN + ((XMAX - XMIN) * i) / 71));
  return {
    newton: xs.map((x) => ({ x: log10(x), y: log10(x) })),
    deep: xs.map((x) => ({ x: log10(x), y: log10(gDeepMond(x, A0)) })),
    std: xs.map((x) => ({ x: log10(x), y: log10(gMondStd(x, A0)) })),
    dual: xs.map((x) => ({ x: log10(x), y: log10(gMondDual(x, A0)) })),
  };
}

type RarPlotProps = {
  dark?: boolean;
  interactive?: boolean;
  width?: number;
  height?: number;
  points?: Array<[number, number]>;
};

function RarPlot({ dark = false, interactive = false, width = 720, height = 720, points = rarPoints }: RarPlotProps) {
  const W = width;
  const H = height;
  const P = dark ? { l: 58, r: 16, t: 16, b: 86 } : { l: 62, r: 18, t: 18, b: 52 };
  const [hover, setHover] = useState<{ gbar: number; gobs: number; cx: number; cy: number } | null>(null);
  const models = useMemo(modelSeries, []);

  const xScale = (logV: number) => Number((P.l + ((logV - XMIN) / (XMAX - XMIN)) * (W - P.l - P.r)).toFixed(2));
  const yScale = (logV: number) => Number((H - P.b - ((logV - YMIN) / (YMAX - YMIN)) * (H - P.t - P.b)).toFixed(2));

  const ticks = logTicks(-12, -8);
  const ink = dark ? "#d7e6e8" : "var(--color-ink-soft)";
  const grid = dark ? "rgba(126,201,212,0.12)" : "var(--color-line)";
  const axis = dark ? "rgba(215,230,232,0.55)" : "var(--color-ink-soft)";
  const tickFill = dark ? "#9bb4b8" : "var(--color-muted)";
  const a0Log = log10(A0);

  const onMove = (event: MouseEvent<SVGSVGElement>) => {
    if (!interactive) return;
    const svg = event.currentTarget;
    const box = svg.getBoundingClientRect();
    const px = ((event.clientX - box.left) / box.width) * W;
    const py = ((event.clientY - box.top) / box.height) * H;
    let best: { d: number; gbar: number; gobs: number; cx: number; cy: number } | null = null;
    for (let i = 0; i < points.length; i += 2) {
      const [gbar, gobs] = points[i];
      const cx = xScale(log10(gbar));
      const cy = yScale(log10(gobs));
      const d = (cx - px) ** 2 + (cy - py) ** 2;
      if (!best || d < best.d) best = { d, gbar, gobs, cx, cy };
    }
    if (best && best.d < 140) setHover(best);
    else setHover(null);
  };

  return (
    <svg
      viewBox={`0 0 ${W} ${H}`}
      className="w-full"
      role="img"
      aria-label="SPARC radial acceleration relation, observed versus baryonic"
      onMouseMove={onMove}
      onMouseLeave={() => setHover(null)}
    >
      <title>SPARC radial acceleration relation</title>
      <defs>
        <clipPath id={dark ? "rar-clip-dark" : "rar-clip"}>
          <rect x={P.l} y={P.t} width={W - P.l - P.r} height={H - P.t - P.b} />
        </clipPath>
      </defs>
      {ticks.map((tick) => (
        <g key={`g${tick}`}>
          <line x1={P.l} x2={W - P.r} y1={yScale(tick)} y2={yScale(tick)} stroke={grid} />
          <line x1={xScale(tick)} x2={xScale(tick)} y1={P.t} y2={H - P.b} stroke={grid} />
          <text x={P.l - 8} y={yScale(tick) + 4} textAnchor="end" fill={tickFill} fontFamily="var(--font-mono)" fontSize="11">
            {decadeLabel(tick)}
          </text>
          <text x={xScale(tick)} y={H - P.b + 20} textAnchor="middle" fill={tickFill} fontFamily="var(--font-mono)" fontSize="11">
            {decadeLabel(tick)}
          </text>
        </g>
      ))}
      <line x1={xScale(a0Log)} x2={xScale(a0Log)} y1={P.t} y2={H - P.b} stroke="var(--color-accent)" strokeOpacity="0.35" strokeDasharray="2 4" />
      <line x1={P.l} x2={W - P.r} y1={yScale(a0Log)} y2={yScale(a0Log)} stroke="var(--color-accent)" strokeOpacity="0.35" strokeDasharray="2 4" />
      <g clipPath={`url(#${dark ? "rar-clip-dark" : "rar-clip"})`}>
      {points.map(([gbar, gobs], i) => (
        <circle
          key={i}
          cx={xScale(log10(gbar))}
          cy={yScale(log10(gobs))}
          r={dark ? 1.7 : 1.85}
          fill={dark ? "#7ec9d4" : "var(--color-obs)"}
          fillOpacity={dark ? 0.38 : 0.28}
        />
      ))}
      <path d={linePath(models.newton, xScale, yScale)} fill="none" stroke={ink} strokeWidth="1.2" strokeDasharray="4 4" />
      <path d={linePath(models.deep, xScale, yScale)} fill="none" stroke={ink} strokeWidth="1.1" strokeDasharray="1 5" />
      <path d={linePath(models.dual, xScale, yScale)} fill="none" stroke="var(--color-retired)" strokeWidth="1.6" strokeDasharray="6 4" />
      <path d={linePath(models.std, xScale, yScale)} fill="none" stroke="var(--color-live)" strokeWidth="2.4" />
      </g>
      {hover ? (
        <g>
          <circle cx={hover.cx} cy={hover.cy} r="5" fill="none" stroke="var(--color-accent-2)" />
          <circle cx={hover.cx} cy={hover.cy} r="2.4" fill="var(--color-accent-2)" />
        </g>
      ) : null}
      <line x1={P.l} x2={W - P.r} y1={H - P.b} y2={H - P.b} stroke={axis} strokeWidth="1.25" />
      <line x1={P.l} x2={P.l} y1={P.t} y2={H - P.b} stroke={axis} strokeWidth="1.25" />
      <text x={(P.l + W - P.r) / 2} y={H - 8} textAnchor="middle" fill={ink} fontFamily="var(--font-sans)" fontSize="13">
        baryonic acceleration g_bar (m s⁻²)
      </text>
      <text transform={`translate(16 ${(P.t + H - P.b) / 2}) rotate(-90)`} textAnchor="middle" fill={ink} fontFamily="var(--font-sans)" fontSize="13">
        observed acceleration g_obs (m s⁻²)
      </text>
      {!dark ? (
      <g fontFamily="var(--font-mono)" fontSize="10" fill={ink}>
        <path d={`M ${P.l + 12} ${P.t + 16} h 18`} stroke={ink} strokeDasharray="4 4" />
        <text x={P.l + 34} y={P.t + 20}>Newtonian 1:1</text>
        <path d={`M ${P.l + 12} ${P.t + 34} h 18`} stroke="var(--color-live)" strokeWidth="2.2" />
        <text x={P.l + 34} y={P.t + 38} fill="var(--color-live)">live μstd</text>
        <path d={`M ${P.l + 12} ${P.t + 52} h 18`} stroke="var(--color-retired)" strokeWidth="1.6" strokeDasharray="6 4" />
        <text x={P.l + 34} y={P.t + 56} fill="var(--color-retired)">superseded μdual</text>
        <path d={`M ${P.l + 12} ${P.t + 70} h 18`} stroke={ink} strokeDasharray="1 5" />
        <text x={P.l + 34} y={P.t + 74}>deep-MOND √(g_bar a₀)</text>
      </g>
      ) : null}
      <text x={xScale(a0Log) + 6} y={P.t + 14} fill="var(--color-accent)" fontFamily="var(--font-mono)" fontSize="10">
        a₀
      </text>
      {hover ? (
        <g fontFamily="var(--font-mono)" fontSize="10" fill={dark ? "#e7f3f4" : "var(--color-ink)"}>
          <rect x={hover.cx + 10} y={hover.cy - 28} width="168" height="36" fill={dark ? "#102026" : "var(--color-surface)"} stroke={grid} />
          <text x={hover.cx + 18} y={hover.cy - 12}>{`g_bar ${hover.gbar.toExponential(2)}`}</text>
          <text x={hover.cx + 18} y={hover.cy + 2}>{`g_obs ${hover.gobs.toExponential(2)}`}</text>
        </g>
      ) : null}
    </svg>
  );
}

export function RarHero() {
  return (
    <div className="relative overflow-hidden border border-white/10 bg-[#0c181c]" role="img" aria-label="SPARC radial acceleration relation">
      <RarPlot dark width={720} height={640} points={rarPoints.filter((_, i) => i % 2 === 0)} />
      <div className="pointer-events-none absolute inset-x-0 bottom-0 flex items-end justify-between p-5">
        <div>
          <span className="font-mono text-[10px] uppercase tracking-[0.16em] text-accent-2">Fig. 0 · SPARC RAR</span>
          <p className="mt-1 max-w-[16rem] font-display text-lg leading-tight text-paper">The sky’s empirical signature, not a fitted Res Nova curve.</p>
        </div>
        <span className="font-mono text-[10px] uppercase tracking-widest text-[#8aa8ad]">
          {rarSource.nGalaxies} galaxies · {rarSource.nPoints.toLocaleString()} points
        </span>
      </div>
    </div>
  );
}

export function RarFigure() {
  return (
    <FigureFrame
      number="6"
      title="Radial acceleration relation"
      caption="Each point is one SPARC kinematic radius: g_obs = V_obs²/r against the published baryonic baseline g_bar = V_bar²/r. The green curve is the live μstd interpolating function at the T1 a₀; the grey dashed 1:1 line is Newtonian gravity; the dotted curve is the deep-MOND limit. This is a communication figure, not a new fit."
      source={`${rarSource.nGalaxies} SPARC galaxies · ${rarSource.nPoints.toLocaleString()} points · Lelli, McGaugh & Schombert · ${rarSource.note}`}
    >
      <div className="px-3 pt-3">
        <RarPlot interactive />
      </div>
    </FigureFrame>
  );
}
