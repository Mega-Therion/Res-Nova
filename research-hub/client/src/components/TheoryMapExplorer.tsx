import { useEffect, useMemo, useState } from "react";
import { CircleDot, FlaskConical, GitBranch, Layers3, Orbit, Radar, ShieldCheck } from "lucide-react";
import { statusMeta, type EvidenceStatus } from "../data/research";

type NodeId = "question" | "action" | "weak-field" | "aest" | "observable" | "falsifier";
type BridgeId = "all" | "question-action" | "action-weak-field" | "weak-field-aest" | "aest-observable" | "observable-falsifier";

const nodes: Array<{ id: NodeId; number: string; title: string; detail: string; status: EvidenceStatus; icon: React.ReactNode }> = [
  { id: "question", number: "01", title: "Question", detail: "Where scale-bridges break", status: "open", icon: <CircleDot size={18} /> },
  { id: "action", number: "02", title: "Action", detail: "A variational object", status: "conditional", icon: <FlaskConical size={18} /> },
  { id: "weak-field", number: "03", title: "Weak field", detail: "AQUAL / μstd", status: "computed", icon: <Orbit size={18} /> },
  { id: "aest", number: "04", title: "AeST", detail: "Covariant completion", status: "conditional", icon: <Layers3 size={18} /> },
  { id: "observable", number: "05", title: "Observable", detail: "Galaxy dynamics", status: "computed", icon: <Radar size={18} /> },
  { id: "falsifier", number: "06", title: "Falsifier", detail: "What could stop it", status: "open", icon: <ShieldCheck size={18} /> },
];

const bridges: Array<{ id: Exclude<BridgeId, "all">; label: string; description: string; nodes: NodeId[] }> = [
  { id: "question-action", label: "Gap → action", description: "A conceptual gap becomes a variational object.", nodes: ["question", "action"] },
  { id: "action-weak-field", label: "Action → weak field", description: "The action is reduced to the galaxy-scale interpolation branch.", nodes: ["action", "weak-field"] },
  { id: "weak-field-aest", label: "Weak field → AeST", description: "Phenomenology meets the conditional covariant completion.", nodes: ["weak-field", "aest"] },
  { id: "aest-observable", label: "AeST → observable", description: "A relativistic construction is connected to a measurable system.", nodes: ["aest", "observable"] },
  { id: "observable-falsifier", label: "Observable → falsifier", description: "A fit becomes meaningful only when failure modes are named.", nodes: ["observable", "falsifier"] },
];

export default function TheoryMapExplorer() {
  const [activeBridge, setActiveBridge] = useState<BridgeId>("all");
  const [focusedNode, setFocusedNode] = useState<NodeId | null>(null);
  const active = useMemo(() => bridges.find((bridge) => bridge.id === activeBridge), [activeBridge]);
  const activeNodeIds = active?.nodes ?? nodes.map((node) => node.id);

  useEffect(() => {
    const handleGuideAction = (event: Event) => {
      const detail = (event as CustomEvent<{ bridge?: BridgeId; focus?: NodeId }>).detail;
      if (detail.bridge) setActiveBridge(detail.bridge);
      if (detail.focus) setFocusedNode(detail.focus);
    };
    window.addEventListener("resnova:theory-action", handleGuideAction);
    return () => window.removeEventListener("resnova:theory-action", handleGuideAction);
  }, []);

  return <>
    <div className="theory-map-toolbar" aria-label="Theory map controls"><div><span className="eyebrow">Interactive bridge lens</span><strong>{active ? active.label : "All dependencies"}</strong><p>{active?.description ?? "Select a bridge to isolate the conceptual handoff and its evidence obligation."}</p></div><div className="theory-bridge-buttons"><button type="button" className={activeBridge === "all" ? "is-active" : ""} onClick={() => { setActiveBridge("all"); setFocusedNode(null); }}>All bridges</button>{bridges.map((bridge) => <button key={bridge.id} type="button" className={activeBridge === bridge.id ? "is-active" : ""} onClick={() => { setActiveBridge(bridge.id); setFocusedNode(null); }}>{bridge.label}</button>)}</div></div>
    <div className={`theory-map ${activeBridge !== "all" ? "has-selection" : ""}`} aria-label="Interactive theory dependency map"><div className={`map-line map-line-one ${activeBridge === "question-action" ? "is-active" : ""}`} /><div className={`map-line map-line-two ${activeBridge === "observable-falsifier" ? "is-active" : ""}`} /><div className={`map-line map-line-three ${activeBridge === "weak-field-aest" ? "is-active" : ""}`} />{nodes.map((node) => <button key={node.id} type="button" className={`theory-node theory-node-${node.id} node-status-${statusMeta[node.status].tone} ${activeNodeIds.includes(node.id) ? "is-connected" : "is-dimmed"} ${focusedNode === node.id ? "is-focused" : ""}`} onClick={() => setFocusedNode(node.id)}><span className="theory-node-number">{node.number}</span><span className="theory-node-icon">{node.icon}</span><strong>{node.title}</strong><small>{node.detail}</small><span className={`theory-node-status status-${node.status}`}>{node.status}</span></button>)}</div>
    <div className="theory-focus-readout" aria-live="polite">{focusedNode ? <><span className="eyebrow">Focused node</span><strong>{nodes.find((node) => node.id === focusedNode)?.title}</strong><p>{nodes.find((node) => node.id === focusedNode)?.detail}. Ask the guide to connect this node to its neighboring bridge.</p></> : <><GitBranch size={16} /><span>Click a node or ask the guide to focus a bridge. The map will keep the surrounding dependency visible.</span></>}</div>
  </>;
}
