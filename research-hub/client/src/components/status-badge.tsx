import { statusMeta, type EvidenceStatus } from "@/data/research";
import { cn } from "@/lib/cn";

export function StatusBadge({ status, compact = false }: { status: EvidenceStatus; compact?: boolean }) {
  const meta = statusMeta[status];
  return (
    <span className={cn("status-badge", `status-${meta.tone}`, compact && "text-[8px] px-1.5 py-1")}>
      <span className="status-dot" aria-hidden="true" />
      {meta.label}
    </span>
  );
}
