import { Link } from "wouter";
import { claims, statusMeta, type EvidenceStatus } from "@/data/research";
import { FigureFrame } from "@/components/figure-frame";

const order: EvidenceStatus[] = ["derived", "computed", "conditional", "open", "superseded"];
const colors: Record<string, string> = {
  derived: "var(--color-status-teal)",
  computed: "var(--color-obs)",
  conditional: "var(--color-status-amber)",
  open: "var(--color-band)",
  superseded: "var(--color-status-rose)",
};

export function EvidenceMixFigure() {
  const rows = order.map((status) => ({
    status,
    meta: statusMeta[status],
    items: claims.filter((claim) => claim.status === status),
  }));
  const max = Math.max(...rows.map((row) => row.items.length), 1);

  return (
    <FigureFrame
      number="5"
      title="Evidence mix of the public ledger"
      caption="n = 7 public claims. Status is a kind of support, not a score: a stacked bar would overstate a tiny ledger, so each claim is drawn as a unit cell."
      source="CLAIM_EVIDENCE_LEDGER.md · one square = one auditable claim"
    >
      <div className="space-y-3 px-5 py-5">
        {rows.map((row) => (
          <div key={row.status} className="grid grid-cols-[132px_1fr_28px] items-center gap-3">
            <span className="font-mono text-[10px] uppercase tracking-wider text-muted">{row.meta.label}</span>
            <div className="flex flex-wrap gap-1.5">
              {row.items.length ? (
                row.items.map((claim) => (
                  <Link
                    key={claim.id}
                    href={`/evidence#claim-${claim.id}`}
                    className="inline-flex min-h-9 items-center px-2 font-mono text-[10px] tracking-wide text-paper"
                    style={{ background: colors[row.status] }}
                    title={claim.title}
                  >
                    {claim.id.replace("CLM-", "")}
                  </Link>
                ))
              ) : (
                <span className="h-2 w-full max-w-[48px] bg-line" />
              )}
            </div>
            <span className="text-right font-mono text-sm tabular-nums">{row.items.length}</span>
          </div>
        ))}
        <div className="flex items-center justify-between border-t border-line pt-3 font-mono text-[10px] uppercase tracking-widest text-muted">
          <span>unit chart · max bin {max}</span>
          <span>{claims.length} claims</span>
        </div>
      </div>
    </FigureFrame>
  );
}
