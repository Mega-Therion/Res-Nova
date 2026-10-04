import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { chartData } from "@/data/research";

export default function ComparisonChart() {
  return (
    <div className="chart-section">
      <div className="chart-heading">
        <div>
          <span className="eyebrow">A live comparison, carefully bounded</span>
          <h2>SPARC reduced χ² by model family</h2>
        </div>
        <div className="chart-key">
          <span>
            <i className="key-dot key-blue" /> horizon a₀
          </span>
          <span>
            <i className="key-dot key-amber" /> literature a₀
          </span>
        </div>
      </div>
      <div className="chart-card">
        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height={320}>
            <BarChart
              data={chartData}
              margin={{ top: 10, right: 20, left: 0, bottom: 12 }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
                stroke="#dbe5e9"
              />
              <XAxis
                dataKey="label"
                tick={{ fill: "#6c7d82", fontSize: 12 }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                domain={[0, 12]}
                tick={{ fill: "#6c7d82", fontSize: 12 }}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip
                cursor={{ fill: "#eef5f7" }}
                contentStyle={{
                  border: "1px solid #dbe5e9",
                  borderRadius: 10,
                  fontSize: 12,
                }}
              />
              <Legend verticalAlign="top" height={30} />
              <ReferenceLine y={1} stroke="#a9b9bd" strokeDasharray="4 4" />
              <Bar
                dataKey="value"
                name="Horizon a₀"
                fill="#79d7e8"
                radius={[4, 4, 0, 0]}
              />
              <Bar
                dataKey="comparison"
                name="Literature a₀"
                fill="#f1b86a"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="chart-caption">
          <strong>Read with care.</strong>
          <p>
            Both bars use μ_std. Blue is the horizon anchor. Amber is the
            literature a₀ of 1.2×10⁻¹⁰ m s⁻². At tier 0 the medians are 11.08
            and 9.93: the horizon anchor fits worse. Tier-1 medians are 3.36 and
            3.41. The third pair is the tier-1 means, 5.63 and 5.63. NFW's
            tier-1 median in the same ledger is 1.92, with 716 free parameters,
            and is not a bar here. This chart does not replace the ledger.
          </p>
          <span className="source-line">
            PARAMETER_LEDGER.json · values shown to two decimal places
          </span>
        </div>
      </div>
    </div>
  );
}
