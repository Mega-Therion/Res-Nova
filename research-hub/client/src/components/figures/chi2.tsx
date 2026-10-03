import { chartData } from "@/data/research";
import { FigureFrame } from "@/components/figure-frame";

const W = 720;
const H = 360;
const P = { l: 54, r: 20, t: 36, b: 58 };
const yMax = 12;

function yScale(v: number) {
  return Number((H - P.b - (v / yMax) * (H - P.t - P.b)).toFixed(2));
}

export function Chi2Figure() {
  const groupW = (W - P.l - P.r) / chartData.length;

  return (
    <FigureFrame
      number="3"
      title="SPARC reduced χ² by model family"
      caption="The public ledger currently reports live μstd values near 3.36 for the Tier 1 fit. This chart is a communication layer, not a replacement for the full likelihood, priors, sample definition, or residual tables. The dashed line marks χ²_red = 1."
      source="PARAMETER_LEDGER.json · values to two decimal places"
    >
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full px-3 pt-4" role="img" aria-label="Bar chart of reduced chi-squared by model family">
        <rect x={P.l} y={yScale(1)} width={W - P.l - P.r} height={yScale(0) - yScale(1)} fill="var(--color-live)" fillOpacity="0.06" />
        {[0, 3, 6, 9, 12].map((tick) => (
          <g key={tick}>
            <line className="plot-grid" x1={P.l} x2={W - P.r} y1={yScale(tick)} y2={yScale(tick)} />
            <text className="plot-tick" x={P.l - 8} y={yScale(tick) + 4} textAnchor="end">
              {tick}
            </text>
          </g>
        ))}
        <line x1={P.l} x2={W - P.r} y1={yScale(1)} y2={yScale(1)} stroke="var(--color-muted)" strokeDasharray="4 4" />
        {chartData.map((row, i) => {
          const cx = P.l + i * groupW + groupW / 2;
          const bar = 22;
          return (
            <g key={row.label}>
              <rect x={cx - bar - 4} y={yScale(row.live)} width={bar} height={yScale(0) - yScale(row.live)} fill="var(--color-obs)" rx="1" />
              <rect x={cx + 4} y={yScale(row.comparison)} width={bar} height={yScale(0) - yScale(row.comparison)} fill="var(--color-model)" rx="1" />
              <text className="plot-tick" x={cx} y={H - 18} textAnchor="middle">
                {row.label}
              </text>
              <text x={cx - bar / 2 - 4} y={yScale(row.live) - 8} textAnchor="middle" fill="var(--color-obs)" fontFamily="var(--font-mono)" fontSize="10">
                {row.live.toFixed(2)}
              </text>
              <text x={cx + bar / 2 + 4} y={yScale(row.comparison) - 8} textAnchor="middle" fill="var(--color-model)" fontFamily="var(--font-mono)" fontSize="10">
                {row.comparison.toFixed(2)}
              </text>
            </g>
          );
        })}
        <line className="plot-axis" x1={P.l} x2={W - P.r} y1={H - P.b} y2={H - P.b} />
        <line className="plot-axis" x1={P.l} x2={P.l} y1={P.t} y2={H - P.b} />
        <text className="plot-label" transform={`translate(16 ${(P.t + H - P.b) / 2}) rotate(-90)`} textAnchor="middle">
          reduced χ²
        </text>
        <text x={W - P.r} y={yScale(1) - 6} textAnchor="end" fill="var(--color-muted)" fontFamily="var(--font-mono)" fontSize="10">
          χ²_red = 1
        </text>
        <g fontFamily="var(--font-mono)" fontSize="11">
          <rect x={P.l + 8} y={P.t - 6} width="10" height="10" fill="var(--color-obs)" />
          <text x={P.l + 22} y={P.t + 4} fill="var(--color-ink-soft)">
            live / primary
          </text>
          <rect x={P.l + 140} y={P.t - 6} width="10" height="10" fill="var(--color-model)" />
          <text x={P.l + 154} y={P.t + 4} fill="var(--color-ink-soft)">
            comparison
          </text>
        </g>
      </svg>
    </FigureFrame>
  );
}
