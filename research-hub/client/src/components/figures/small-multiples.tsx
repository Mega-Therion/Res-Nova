import { canonicalSparcCurves } from "@/data/sparc";
import { featuredGalaxyNames } from "@/data/sparc-meta";
import { FigureFrame } from "@/components/figure-frame";

const featured = featuredGalaxyNames
  .map((name) => canonicalSparcCurves.find((curve) => curve.name.toUpperCase() === name.toUpperCase()))
  .filter((curve): curve is (typeof canonicalSparcCurves)[number] => Boolean(curve));

function MiniCurve({ curve }: { curve: (typeof canonicalSparcCurves)[number] }) {
  const W = 220;
  const H = 150;
  const P = { l: 28, r: 8, t: 10, b: 22 };
  const xMax = Math.max(...curve.points.map((p) => p.radius), 1);
  const yMax = Math.max(...curve.points.map((p) => p.observed), ...curve.points.map((p) => p.baryonicBaseline), 1) * 1.08;
  const x = (v: number) => Number((P.l + (v / xMax) * (W - P.l - P.r)).toFixed(2));
  const y = (v: number) => Number((H - P.b - (v / yMax) * (H - P.t - P.b)).toFixed(2));
  const obs = curve.points.map((p, i) => `${i === 0 ? "M" : "L"} ${x(p.radius).toFixed(1)} ${y(p.observed).toFixed(1)}`).join(" ");
  const bar = curve.points.map((p, i) => `${i === 0 ? "M" : "L"} ${x(p.radius).toFixed(1)} ${y(p.baryonicBaseline).toFixed(1)}`).join(" ");
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label={`${curve.name} rotation curve`}>
      <line className="plot-axis" x1={P.l} x2={W - P.r} y1={H - P.b} y2={H - P.b} />
      <line className="plot-axis" x1={P.l} x2={P.l} y1={P.t} y2={H - P.b} />
      <path d={bar} fill="none" stroke="var(--color-model)" strokeWidth="1.4" />
      <path d={obs} fill="none" stroke="var(--color-obs)" strokeWidth="1.6" />
      {curve.points.map((p) => (
        <circle key={p.radius} cx={x(p.radius)} cy={y(p.observed)} r="1.6" fill="var(--color-obs)" />
      ))}
      <text className="plot-tick" x={P.l} y={14} fontSize="10">
        {curve.name}
      </text>
    </svg>
  );
}

export function SmallMultiplesFigure() {
  return (
    <FigureFrame
      number="7"
      title="Canonical SPARC small multiples"
      caption="A fixed plate of well-known SPARC disks. Blue: observed rotation. Orange: published baryonic baseline (gas + disk + bulge in quadrature). These are not Res Nova fits; they show why a single interpolation scale is asked to do so much work."
      source="Lelli, McGaugh & Schombert · Rotmod_LTG · same reduction as the explorer"
    >
      <div className="grid grid-cols-2 gap-px bg-line sm:grid-cols-4">
        {featured.map((curve) => (
          <div key={curve.id} className="bg-surface p-2">
            <MiniCurve curve={curve} />
          </div>
        ))}
      </div>
    </FigureFrame>
  );
}
