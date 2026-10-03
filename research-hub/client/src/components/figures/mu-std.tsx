import { useEffect, useMemo, useState } from "react";
import { muDual, muStd } from "@/data/research";
import { linePath } from "@/lib/chart";
import { FigureFrame } from "@/components/figure-frame";

const W = 720;
const H = 420;
const P = { l: 58, r: 24, t: 22, b: 48 };

function xScale(x: number) {
  return Number((P.l + (x / 8) * (W - P.l - P.r)).toFixed(2));
}
function yScale(y: number) {
  return Number((H - P.b - y * (H - P.t - P.b)).toFixed(2));
}

export function MuStdFigure() {
  const [x, setX] = useState(1);
  const [mounted, setMounted] = useState(false);
  useEffect(() => {
    setMounted(true);
  }, []);
  const series = useMemo(() => {
    const xs = Array.from({ length: 161 }, (_, i) => (i / 160) * 8);
    return {
      std: xs.map((v) => ({ x: v, y: muStd(v) })),
      dual: xs.map((v) => ({ x: v, y: muDual(v) })),
      mond: xs.filter((v) => v <= 1.6).map((v) => ({ x: v, y: v })),
      newt: [
        { x: 0, y: 1 },
        { x: 8, y: 1 },
      ],
    };
  }, []);
  const live = muStd(x);
  const retired = muDual(x);

  return (
    <FigureFrame
      number="1"
      title="Interpolation branches"
      caption="μstd(x) = x / √(1 + x²) is the live weak-field interpolation. μdual(x) = x/(1+x) is shown only as the superseded branch that failed solar-system tests. Shaded bands mark the deep-MOND, transition, and Newtonian regimes; they are labels, not fits."
      source="TARGET_D1_SUPPLEMENT_MU_STD_REBUILD.md · structural, not empirical"
    >
      <div className="px-4 pt-4 sm:px-6">
        <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="Interpolation function μ of x for live and superseded branches">
          <title>μ(x) interpolation comparison</title>
          <rect x={xScale(0)} y={yScale(1)} width={xScale(0.5) - xScale(0)} height={yScale(0) - yScale(1)} fill="var(--color-band)" fillOpacity="0.12" />
          <rect x={xScale(0.5)} y={yScale(1)} width={xScale(2) - xScale(0.5)} height={yScale(0) - yScale(1)} fill="var(--color-status-amber)" fillOpacity="0.10" />
          <rect x={xScale(2)} y={yScale(1)} width={xScale(8) - xScale(2)} height={yScale(0) - yScale(1)} fill="var(--color-live)" fillOpacity="0.08" />
          {[0, 0.25, 0.5, 0.75, 1].map((tick) => (
            <g key={tick}>
              <line className="plot-grid" x1={P.l} x2={W - P.r} y1={yScale(tick)} y2={yScale(tick)} />
              <text className="plot-tick" x={P.l - 10} y={yScale(tick) + 4} textAnchor="end">
                {tick.toFixed(2)}
              </text>
            </g>
          ))}
          {[0, 2, 4, 6, 8].map((tick) => (
            <g key={tick}>
              <line className="plot-grid" x1={xScale(tick)} x2={xScale(tick)} y1={P.t} y2={H - P.b} />
              <text className="plot-tick" x={xScale(tick)} y={H - P.b + 20} textAnchor="middle">
                {tick}
              </text>
            </g>
          ))}
          <path d={linePath(series.newt, xScale, yScale)} fill="none" stroke="var(--color-mist)" strokeWidth="1" strokeDasharray="3 4" />
          <path d={linePath(series.mond, xScale, yScale)} fill="none" stroke="var(--color-mist)" strokeWidth="1" strokeDasharray="1 4" />
          <path d={linePath(series.dual, xScale, yScale)} fill="none" stroke="var(--color-retired)" strokeWidth="1.8" strokeDasharray="5 4" />
          <path d={linePath(series.std, xScale, yScale)} fill="none" stroke="var(--color-live)" strokeWidth="2.4" />
          <line x1={xScale(x)} x2={xScale(x)} y1={P.t} y2={H - P.b} stroke="var(--color-accent)" strokeOpacity="0.35" />
          <circle cx={xScale(x)} cy={yScale(live)} r="5" fill="var(--color-live)" />
          <circle cx={xScale(x)} cy={yScale(retired)} r="4" fill="var(--color-retired)" />
          <line className="plot-axis" x1={P.l} x2={W - P.r} y1={H - P.b} y2={H - P.b} />
          <line className="plot-axis" x1={P.l} x2={P.l} y1={P.t} y2={H - P.b} />
          <text className="plot-label" x={(P.l + W - P.r) / 2} y={H - 8} textAnchor="middle">
            x = a / a₀
          </text>
          <text className="plot-label" transform={`translate(16 ${(P.t + H - P.b) / 2}) rotate(-90)`} textAnchor="middle">
            μ(x)
          </text>
          <text x={xScale(0.08)} y={yScale(0.08) - 8} fill="var(--color-muted)" fontFamily="var(--font-mono)" fontSize="10">
            deep-MOND
          </text>
          <text x={xScale(0.7)} y={yScale(0.08) - 8} fill="var(--color-muted)" fontFamily="var(--font-mono)" fontSize="10">
            transition
          </text>
          <text x={xScale(4.4)} y={yScale(0.08) - 8} fill="var(--color-muted)" fontFamily="var(--font-mono)" fontSize="10">
            Newtonian
          </text>
          <text x={xScale(6.15)} y={yScale(0.92)} fill="var(--color-live)" fontFamily="var(--font-mono)" fontSize="11">
            live μstd
          </text>
          <text x={xScale(5.05)} y={yScale(0.68)} fill="var(--color-retired)" fontFamily="var(--font-mono)" fontSize="11">
            superseded μdual
          </text>
        </svg>
        <label className="mt-2 mb-4 flex items-center gap-4 px-1 font-mono text-[11px] uppercase tracking-wider text-muted">
          Probe x
          {mounted ? (
            <input
              className="flex-1 accent-accent"
              type="range"
              min={0.05}
              max={8}
              step={0.05}
              value={x}
              onChange={(e) => setX(Number(e.target.value))}
            />
          ) : (
            <span className="flex-1" />
          )}
          <span className="tabular-nums text-ink">
            {x.toFixed(2)} · μstd {live.toFixed(3)} · μdual {retired.toFixed(3)}
          </span>
        </label>
      </div>
    </FigureFrame>
  );
}
