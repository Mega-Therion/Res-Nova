import { a0Measurement } from "@/data/research";
import { FigureFrame } from "@/components/figure-frame";

const W = 720;
const H = 280;
const P = { l: 200, r: 36, t: 40, b: 52 };
const lo = 8.5e-11;
const hi = 14e-11;

function xScale(v: number) {
  return Number((P.l + ((v - lo) / (hi - lo)) * (W - P.l - P.r)).toFixed(2));
}

function fmt(v: number) {
  return (v * 1e10).toFixed(2);
}

export function A0IntervalFigure() {
  const { t1, t3 } = a0Measurement;
  const ticks = [9e-11, 10e-11, 11e-11, 12e-11, 13e-11];

  return (
    <FigureFrame
      number="2"
      title="Distance-corrected a₀"
      caption="T1 reports a₀ = 1.1607 × 10⁻¹⁰ m s⁻² across 175 SPARC galaxies (3,391 points) with a 95% interval. T3 non-flow is a comparison object, not a second discovery. This is an empirical scale, not a derivation from horizon thermodynamics."
      source="A0_DISTANCE_CORRECTED_2026-09-16.json · 95% interval shown"
    >
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full px-2 pt-4" role="img" aria-label="a0 measurement with 95 percent interval">
        {ticks.map((tick) => (
          <g key={tick}>
            <line className="plot-grid" x1={xScale(tick)} x2={xScale(tick)} y1={P.t} y2={H - P.b} />
            <text className="plot-tick" x={xScale(tick)} y={H - P.b + 22} textAnchor="middle">
              {fmt(tick)}
            </text>
          </g>
        ))}
        <rect x={xScale(t1.lo)} y={70} width={xScale(t1.hi) - xScale(t1.lo)} height={32} fill="var(--color-obs)" fillOpacity="0.12" />
        <line className="plot-axis" x1={P.l} x2={W - P.r} y1={H - P.b} y2={H - P.b} />
        <text className="plot-label" x={(P.l + W - P.r) / 2} y={H - 8} textAnchor="middle">
          a₀ (× 10⁻¹⁰ m s⁻²)
        </text>

        <text x={P.l - 14} y={90} textAnchor="end" className="plot-label">
          {t1.label}
        </text>
        <line x1={xScale(t1.lo)} x2={xScale(t1.hi)} y1={86} y2={86} stroke="var(--color-obs)" strokeWidth="3" />
        <line x1={xScale(t1.lo)} x2={xScale(t1.lo)} y1={76} y2={96} stroke="var(--color-obs)" strokeWidth="2" />
        <line x1={xScale(t1.hi)} x2={xScale(t1.hi)} y1={76} y2={96} stroke="var(--color-obs)" strokeWidth="2" />
        <circle cx={xScale(t1.value)} cy={86} r="6" fill="var(--color-obs)" />
        <text x={xScale(t1.value)} y={66} textAnchor="middle" fill="var(--color-obs)" fontFamily="var(--font-mono)" fontSize="11">
          {fmt(t1.value)} · 95%
        </text>
        <text x={P.l - 14} y={112} textAnchor="end" fill="var(--color-muted)" fontFamily="var(--font-mono)" fontSize="9">
          {t1.n}
        </text>

        <text x={P.l - 14} y={168} textAnchor="end" className="plot-label">
          {t3.label}
        </text>
        <circle cx={xScale(t3.value)} cy={162} r="5.5" fill="var(--color-model)" />
        <text x={xScale(t3.value) + 12} y={166} fill="var(--color-model)" fontFamily="var(--font-mono)" fontSize="11">
          {fmt(t3.value)} · comparison
        </text>
      </svg>
    </FigureFrame>
  );
}
