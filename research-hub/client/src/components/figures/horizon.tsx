import { useMemo } from "react";
import { horizonScale } from "@/data/research";
import { linePath } from "@/lib/chart";
import { FigureFrame } from "@/components/figure-frame";

const W = 720;
const H = 380;
const P = { l: 58, r: 22, t: 22, b: 48 };
const zMax = 1.2;
const yMax = 2.0;

function xScale(z: number) {
  return Number((P.l + (z / zMax) * (W - P.l - P.r)).toFixed(2));
}
function yScale(y: number) {
  return Number((H - P.b - (y / yMax) * (H - P.t - P.b)).toFixed(2));
}

export function HorizonFigure() {
  const curve = useMemo(() => Array.from({ length: 49 }, (_, i) => {
    const z = (i / 48) * zMax;
    return { x: z, y: horizonScale(z) };
  }), []);
  const area = `M ${xScale(0)} ${yScale(1)} ${curve.map((p) => `L ${xScale(p.x)} ${yScale(p.y)}`).join(" ")} L ${xScale(zMax)} ${yScale(1)} Z`;

  return (
    <FigureFrame
      number="4"
      title="Horizon-tied a₀(z) corollary"
      caption="If a₀ tracks the FLRW apparent horizon, the falsifiable shape is a₀(z)/a₀(0) = √(Ω_m(1+z)³ + Ω_Λ). At z = 1 the curve is ~+76–79%. RC100 currently misses both 2-bin 95% intervals in opposite directions (Δχ² = 8.9–19.8, stat-only): constrained, not excluded. No RC100 point values are invented here."
      source="HORIZON_SELECTION_AUDIT_2026-09-16.md · Ω_m=0.3, Ω_Λ=0.7 illustration of the stated functional form"
    >
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full px-3 pt-4" role="img" aria-label="Predicted a0 redshift evolution under the horizon corollary">
        <rect x={xScale(0.18)} y={P.t} width={xScale(0.55) - xScale(0.18)} height={H - P.t - P.b} fill="var(--color-status-amber)" fillOpacity="0.08" />
        <rect x={xScale(0.72)} y={P.t} width={xScale(1.05) - xScale(0.72)} height={H - P.t - P.b} fill="var(--color-status-amber)" fillOpacity="0.08" />
        <path d={area} fill="var(--color-obs)" fillOpacity="0.08" />
        {[1, 1.25, 1.5, 1.75, 2].map((tick) => (
          <g key={tick}>
            <line className="plot-grid" x1={P.l} x2={W - P.r} y1={yScale(tick)} y2={yScale(tick)} />
            <text className="plot-tick" x={P.l - 8} y={yScale(tick) + 4} textAnchor="end">
              {tick.toFixed(2)}
            </text>
          </g>
        ))}
        {[0, 0.4, 0.8, 1.2].map((tick) => (
          <g key={tick}>
            <line className="plot-grid" x1={xScale(tick)} x2={xScale(tick)} y1={P.t} y2={H - P.b} />
            <text className="plot-tick" x={xScale(tick)} y={H - P.b + 20} textAnchor="middle">
              {tick.toFixed(1)}
            </text>
          </g>
        ))}
        <line x1={P.l} x2={W - P.r} y1={yScale(1)} y2={yScale(1)} stroke="var(--color-muted)" strokeDasharray="4 4" />
        <path d={linePath(curve, xScale, yScale)} fill="none" stroke="var(--color-obs)" strokeWidth="2.4" />
        <circle cx={xScale(1)} cy={yScale(horizonScale(1))} r="5" fill="var(--color-obs)" />
        <text x={xScale(1) - 8} y={yScale(horizonScale(1)) - 12} textAnchor="end" fill="var(--color-obs)" fontFamily="var(--font-mono)" fontSize="11">
          z=1 · {horizonScale(1).toFixed(2)}×
        </text>
        <text x={xScale(0.365)} y={P.t + 18} textAnchor="middle" fill="var(--color-status-amber)" fontFamily="var(--font-mono)" fontSize="10">
          RC100 lo
        </text>
        <text x={xScale(0.885)} y={P.t + 18} textAnchor="middle" fill="var(--color-status-amber)" fontFamily="var(--font-mono)" fontSize="10">
          RC100 hi
        </text>
        <text x={xScale(0.365)} y={H - P.b - 10} textAnchor="middle" fill="var(--color-status-amber)" fontFamily="var(--font-mono)" fontSize="9">
          constrained
        </text>
        <line className="plot-axis" x1={P.l} x2={W - P.r} y1={H - P.b} y2={H - P.b} />
        <line className="plot-axis" x1={P.l} x2={P.l} y1={P.t} y2={H - P.b} />
        <text className="plot-label" x={(P.l + W - P.r) / 2} y={H - 8} textAnchor="middle">
          redshift z
        </text>
        <text className="plot-label" transform={`translate(16 ${(P.t + H - P.b) / 2}) rotate(-90)`} textAnchor="middle">
          a₀(z) / a₀(0)
        </text>
      </svg>
    </FigureFrame>
  );
}
