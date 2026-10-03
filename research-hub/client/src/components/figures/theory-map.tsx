import { useEffect, useState } from "react";
import { GitBranch } from "lucide-react";
import { StatusBadge } from "@/components/status-badge";
import type { EvidenceStatus } from "@/data/research";
import { cn } from "@/lib/cn";

type NodeId = "question" | "action" | "weak-field" | "aest" | "observable" | "falsifier";
type BridgeId = "all" | "question-action" | "action-weak-field" | "weak-field-aest" | "aest-observable" | "observable-falsifier";

const nodes: Array<{
  id: NodeId;
  number: string;
  title: string;
  detail: string;
  equation: string;
  status: EvidenceStatus;
  x: number;
  y: number;
}> = [
  { id: "question", number: "01", title: "Question", detail: "Where scale-bridges break", equation: "gap", status: "open", x: 95, y: 48 },
  { id: "action", number: "02", title: "Action", detail: "A variational object", equation: "S[φ, g]", status: "conditional", x: 285, y: 48 },
  { id: "weak-field", number: "03", title: "Weak field", detail: "AQUAL / μstd", equation: "μstd(x)=x/√(1+x²)", status: "computed", x: 475, y: 48 },
  { id: "aest", number: "04", title: "AeST", detail: "Covariant completion", equation: "scalar-sector", status: "conditional", x: 665, y: 48 },
  { id: "observable", number: "05", title: "Observable", detail: "Galaxy dynamics", equation: "V(r), g_obs", status: "computed", x: 855, y: 48 },
  { id: "falsifier", number: "06", title: "Falsifier", detail: "What could stop it", equation: "a₀(z), PN", status: "open", x: 1045, y: 48 },
];

const bridges: Array<{ id: Exclude<BridgeId, "all">; label: string; description: string; nodes: NodeId[]; from: NodeId; to: NodeId }> = [
  { id: "question-action", label: "Gap → action", description: "A conceptual gap becomes a variational object.", nodes: ["question", "action"], from: "question", to: "action" },
  { id: "action-weak-field", label: "Action → weak field", description: "The action is reduced to the galaxy-scale interpolation branch.", nodes: ["action", "weak-field"], from: "action", to: "weak-field" },
  { id: "weak-field-aest", label: "Weak field → AeST", description: "Phenomenology meets the conditional covariant completion.", nodes: ["weak-field", "aest"], from: "weak-field", to: "aest" },
  { id: "aest-observable", label: "AeST → observable", description: "A relativistic construction is connected to a measurable system.", nodes: ["aest", "observable"], from: "aest", to: "observable" },
  { id: "observable-falsifier", label: "Observable → falsifier", description: "A fit becomes meaningful only when failure modes are named.", nodes: ["observable", "falsifier"], from: "observable", to: "falsifier" },
];

const statusStroke: Record<EvidenceStatus, string> = {
  derived: "var(--color-status-teal)",
  computed: "var(--color-obs)",
  cited: "var(--color-status-slate)",
  conditional: "var(--color-status-amber)",
  open: "var(--color-band)",
  refuted: "var(--color-status-rose)",
  superseded: "var(--color-status-rose)",
};

export function TheoryMapExplorer() {
  const [activeBridge, setActiveBridge] = useState<BridgeId>("all");
  const [focusedNode, setFocusedNode] = useState<NodeId | null>(null);
  const active = bridges.find((bridge) => bridge.id === activeBridge);
  const activeNodeIds = active?.nodes ?? nodes.map((node) => node.id);
  const focused = nodes.find((node) => node.id === focusedNode);

  useEffect(() => {
    const handle = (event: Event) => {
      const detail = (event as CustomEvent<{ bridge?: BridgeId; focus?: NodeId }>).detail;
      if (detail.bridge) setActiveBridge(detail.bridge);
      if (detail.focus) setFocusedNode(detail.focus);
    };
    window.addEventListener("resnova:theory-action", handle);
    return () => window.removeEventListener("resnova:theory-action", handle);
  }, []);

  return (
    <div>
      <div className="mb-5 flex flex-col gap-4 border border-line bg-surface p-5 md:flex-row md:items-end md:justify-between">
        <div className="max-w-lg">
          <span className="eyebrow">Interactive bridge lens</span>
          <strong className="mt-2 block font-display text-2xl font-medium">{active ? active.label : "All dependencies"}</strong>
          <p className="mt-2 text-sm text-muted">{active?.description ?? "Select a bridge to isolate the conceptual handoff and its evidence obligation."}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button type="button" className={cn("btn btn-quiet min-h-10 px-3 text-[10px]", activeBridge === "all" && "border-accent text-accent")} onClick={() => { setActiveBridge("all"); setFocusedNode(null); }}>
            All bridges
          </button>
          {bridges.map((bridge) => (
            <button key={bridge.id} type="button" className={cn("btn btn-quiet min-h-10 px-3 text-[10px]", activeBridge === bridge.id && "border-accent text-accent")} onClick={() => { setActiveBridge(bridge.id); setFocusedNode(null); }}>
              {bridge.label}
            </button>
          ))}
        </div>
      </div>

      <div className="overflow-x-auto border border-line bg-paper-2">
        <svg viewBox="0 0 1140 210" className="min-w-[860px] w-full" role="img" aria-label="Theory dependency schematic">
          <title>From question to falsifier</title>
          {bridges.map((bridge) => {
            const from = nodes.find((node) => node.id === bridge.from)!;
            const to = nodes.find((node) => node.id === bridge.to)!;
            const on = activeBridge === "all" || activeBridge === bridge.id;
            return (
              <g key={bridge.id} opacity={on ? 1 : 0.22}>
                <line x1={from.x + 72} y1={from.y + 44} x2={to.x - 72} y2={to.y + 44} stroke="var(--color-accent)" strokeWidth={on && activeBridge !== "all" ? 2.4 : 1.4} />
                <polygon points={`${to.x - 76},${to.y + 40} ${to.x - 68},${to.y + 44} ${to.x - 76},${to.y + 48}`} fill="var(--color-accent)" />
              </g>
            );
          })}
          {nodes.map((node) => {
            const on = activeNodeIds.includes(node.id);
            const focusedHere = focusedNode === node.id;
            return (
              <g key={node.id} opacity={on ? 1 : 0.28} className="cursor-pointer" onClick={() => setFocusedNode(node.id)}>
                <rect
                  x={node.x - 78}
                  y={node.y}
                  width="156"
                  height="88"
                  fill="var(--color-surface)"
                  stroke={focusedHere ? "var(--color-accent)" : "var(--color-line)"}
                  strokeWidth={focusedHere ? 2 : 1}
                />
                <line x1={node.x - 78} y1={node.y} x2={node.x - 78} y2={node.y + 88} stroke={statusStroke[node.status]} strokeWidth="4" />
                <text x={node.x - 66} y={node.y + 22} fill="var(--color-muted)" fontFamily="var(--font-mono)" fontSize="10">
                  {node.number}
                </text>
                <text x={node.x - 66} y={node.y + 44} fill="var(--color-ink)" fontFamily="var(--font-display)" fontSize="20">
                  {node.title}
                </text>
                <text x={node.x - 66} y={node.y + 64} fill="var(--color-muted)" fontFamily="var(--font-sans)" fontSize="11">
                  {node.detail}
                </text>
                <text x={node.x - 66} y={node.y + 80} fill="var(--color-accent)" fontFamily="var(--font-mono)" fontSize="9">
                  {node.equation}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      <div className="mt-4 grid gap-3 md:grid-cols-[1.4fr_.6fr]">
        <div className="flex items-start gap-3 border border-line bg-surface px-4 py-3 text-sm text-muted" aria-live="polite">
          <GitBranch size={16} className="mt-0.5 shrink-0 text-accent" />
          {focused ? (
            <p>
              <span className="font-mono text-[10px] uppercase tracking-widest text-accent">Focused node · </span>
              <strong className="text-ink">{focused.title}</strong>
              {" — "}
              {focused.detail}. Live object: {focused.equation}.
            </p>
          ) : (
            <p>Click a node or ask the guide to focus a bridge. Neighboring dependencies stay in view so a handoff is never read in isolation.</p>
          )}
        </div>
        <div className="flex items-center justify-between gap-3 border border-line bg-surface px-4 py-3">
          <span className="font-mono text-[10px] uppercase tracking-widest text-muted">Node status</span>
          {focused ? <StatusBadge status={focused.status} compact /> : <span className="text-sm text-muted">select a node</span>}
        </div>
      </div>
    </div>
  );
}
