import { FormEvent, useEffect, useMemo, useRef, useState } from "react";
import { ArrowUpRight, Bot, ChevronRight, Download, ExternalLink, Send, Sparkles, X } from "lucide-react";
import { claims } from "../data/research";
import { canonicalSparcCurves, sparcSource } from "../data/sparc";
import { trpc } from "../lib/trpc";
import { useLocation } from "wouter";

type GuideMessage = { id: number; role: "guide" | "visitor"; text: string; action?: { label: string; kind: "navigate" | "chart" | "download" | "theory"; href?: string; galaxy?: string; bridge?: string; focus?: string }; citation?: { label: string; href: string } };

const suggestedQuestions = [
  { label: "Read the data", prompt: "What does the rotation data actually show?" },
  { label: "Trace a bridge", prompt: "Show me the bridge from action to weak field" },
  { label: "Focus AeST", prompt: "Connect AeST to the observable" },
  { label: "Find the limits", prompt: "What is still open or unresolved?" },
];

const initialMessage: GuideMessage = {
  id: 1,
  role: "guide",
  text: "I can guide you through the Res Nova map: what is observed, what is computed, what is conditional, and what remains open. Ask me about a galaxy, a claim, a theory bridge, or a downloadable artifact.",
};

type GuideSearchResult = {
  claims: Array<{ id: string; status: string; domain: string; title: string; summary: string; limitation: string }>;
  datasets: Array<{ id: number; name: string; scope: string; artifact: string; provenance: string }>;
  files: Array<{ id: number; title: string; category: string; fileName: string; publicUrl: string; mimeType: string; sizeBytes: number }>;
};

function answerFromPersistedSearch(input: string, result: GuideSearchResult): GuideMessage | null {
  const [claim] = result.claims;
  const [dataset] = result.datasets;
  const [file] = result.files;
  if (file) {
    return { id: Date.now(), role: "guide", text: `I found a stored ${file.category} in the public research-file catalog: ${file.title} (${file.fileName}, ${file.mimeType}). The file bytes are served by the S3-compatible storage layer and its database record carries the public link.`, action: { label: `Open ${file.title}`, kind: "download", href: file.publicUrl }, citation: { label: `Cite stored file · ${file.fileName}`, href: file.publicUrl } };
  }
  if (claim) {
    return { id: Date.now(), role: "guide", text: `The persisted claim registry matches “${claim.title}” with status ${claim.status} in ${claim.domain}. ${claim.summary} Boundary: ${claim.limitation}`, action: { label: "Open the evidence atlas", kind: "navigate", href: `/evidence#claim-${claim.id}` }, citation: { label: `Cite claim · ${claim.id}`, href: `/evidence#claim-${claim.id}` } };
  }
  if (dataset) {
    return { id: Date.now(), role: "guide", text: `The database catalog describes ${dataset.name}: ${dataset.scope}. Provenance: ${dataset.provenance} The linked artifact is ${dataset.artifact}.`, action: { label: "Open data & methods", kind: "navigate", href: "/data" } };
  }
  return null;
}

function answerFor(input: string): GuideMessage {
  const query = input.toLowerCase();
  const galaxy = canonicalSparcCurves.find((item) => query.includes(item.name.toLowerCase()));
  if (galaxy || /rotation|curve|sparc|galax|velocity|data point/.test(query)) {
    const selected = galaxy ?? canonicalSparcCurves[0];
    const point = selected.points[Math.floor(selected.points.length / 2)];
    return { id: Date.now(), role: "guide", text: `The explorer is using canonical SPARC point-level data for ${selected.name}: ${selected.points.length} displayed points at ${selected.distance}. At the selected midpoint (${point.radius.toFixed(2)} kpc), the published observed velocity is ${point.observed.toFixed(1)} ± ${point.uncertainty.toFixed(1)} km/s. The blue comparison line is the quadrature baryonic baseline from the published gas, disk, and bulge components—not a fitted Res Nova prediction.`, action: { label: `Open ${selected.name} in the explorer`, kind: "chart", galaxy: selected.name } };
  }
  if (/download|export|csv|svg|chart file|dataset/.test(query)) {
    return { id: Date.now(), role: "guide", text: `The current public slice is downloadable as CSV and SVG from Data & Methods. It is sourced from ${sparcSource.authors} (${sparcSource.doi}) and is labeled CC BY 4.0 in the archive metadata.`, action: { label: "Open downloads & methods", kind: "navigate", href: "/data" } };
  }
  if (/open|unresolved|falsif|future|problem|gap|missing/.test(query)) {
    return { id: Date.now(), role: "guide", text: "The atlas keeps unresolved work visible: the acceleration-scale interpretation is not derived from horizon thermodynamics, the structural uniqueness argument is conditional, the post-Newtonian and screening sectors remain incomplete, and nonlinear structure formation is still open. These are boundaries, not footnotes.", action: { label: "Read the open problems", kind: "navigate", href: "/open-problems" } };
  }
  if (/claim|evidence|proof|derived|computed|conditional|status/.test(query)) {
    const computed = claims.filter((claim) => claim.status === "computed").length;
    const conditional = claims.filter((claim) => claim.status === "conditional").length;
    return { id: Date.now(), role: "guide", text: `The evidence atlas tracks ${claims.length} claims by status. The current snapshot includes ${computed} computed claim${computed === 1 ? "" : "s"} and ${conditional} conditional claims, alongside derived, open, and superseded records. A claim's presence means it is auditable; it does not mean it is established consensus.`, action: { label: "Open the evidence atlas", kind: "navigate", href: "/evidence" } };
  }
  if (/action.*weak|weak.*action|variational.*galax|bridge.*action/.test(query)) {
    return { id: Date.now(), role: "guide", text: "The action → weak-field bridge is the reduction step: a variational object is asked to produce the μstd interpolation used at galaxy scales. In the atlas this handoff is conditional—not a claim that the phenomenology alone completes the relativistic theory.", action: { label: "Highlight action → weak field", kind: "theory", bridge: "action-weak-field", focus: "weak-field" } };
  }
  if (/aest.*observ|observ.*aest|covariant.*galax/.test(query)) {
    return { id: Date.now(), role: "guide", text: "The AeST → observable bridge asks whether a covariant completion can be connected to a measurable galaxy-dynamics sector without hiding assumptions in the seam. Select it to keep both the construction and its target observable in view.", action: { label: "Highlight AeST → observable", kind: "theory", bridge: "aest-observable", focus: "observable" } };
  }
  if (/theory|bridge|physics|gravity|aest|mu|program|res nova/.test(query)) {
    return { id: Date.now(), role: "guide", text: "Res Nova is organized as a chain rather than a single conclusion: identify a gap, state a mathematical construction, connect it to an observable, attach an artifact, and name what could falsify or narrow it. The interactive theory map can isolate each bridge in that chain.", action: { label: "Open the interactive theory map", kind: "theory", bridge: "all" } };
  }
  return { id: Date.now(), role: "guide", text: "I can help with rotation curves, SPARC data, evidence statuses, theory bridges, open problems, publications, and downloadable artifacts. Try asking “what does NGC 3198 show?” or “what would falsify this program?”" };
}

export default function ResearchGuide() {
  const [, setLocation] = useLocation();
  const [retrievalQuery, setRetrievalQuery] = useState("");
  const [pendingRetrieval, setPendingRetrieval] = useState<{ id: number; text: string } | null>(null);
  const guideSearch = trpc.atlas.search.useQuery({ query: retrievalQuery || "res nova", limit: 5 }, { enabled: retrievalQuery.trim().length > 0, retry: false });
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<GuideMessage[]>([initialMessage]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const nextId = useMemo(() => messages.length + 1, [messages.length]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, [messages, isTyping]);

  useEffect(() => {
    if (!pendingRetrieval || guideSearch.isFetching) return;
    const persistedResponse = guideSearch.data ? answerFromPersistedSearch(pendingRetrieval.text, guideSearch.data) : null;
    const response = persistedResponse ?? answerFor(pendingRetrieval.text);
    const timer = window.setTimeout(() => {
      setMessages((current) => [...current, response]);
      setIsTyping(false);
      setPendingRetrieval(null);
    }, 420);
    return () => window.clearTimeout(timer);
  }, [guideSearch.data, guideSearch.isFetching, guideSearch.isError, pendingRetrieval]);

  const runAction = (action: GuideMessage["action"]) => {
    if (!action) return;
    if (action.kind === "navigate" && action.href) setLocation(action.href);
    if (action.kind === "download") window.open(action.href, "_blank", "noopener,noreferrer");
    if (action.kind === "chart") {
      setLocation("/data");
      window.setTimeout(() => window.dispatchEvent(new CustomEvent("resnova:guide-action", { detail: { galaxy: action.galaxy, showModel: true, showUncertainty: true } })), 140);
    }
    if (action.kind === "theory") {
      setLocation("/theory");
      window.setTimeout(() => window.dispatchEvent(new CustomEvent("resnova:theory-action", { detail: { bridge: action.bridge, focus: action.focus } })), 140);
    }
  };

  const submitText = (text: string) => {
    const trimmed = text.trim();
    if (!trimmed) return;
    const visitor: GuideMessage = { id: nextId, role: "visitor", text: trimmed };
    setMessages((current) => [...current, visitor]);
    setInput("");
    setIsTyping(true);
    setPendingRetrieval({ id: nextId + 1, text: trimmed });
    setRetrievalQuery(trimmed);
  };
  const submit = (event?: FormEvent) => {
    event?.preventDefault();
    submitText(input);
  };

  return <>
    {!open && <button className="guide-launcher" type="button" onClick={() => setOpen(true)} aria-label="Open the Res Nova research guide"><span className="guide-launcher-orbit"><Bot size={20} /></span><span><strong>Ask the atlas</strong><small>research guide</small></span><Sparkles size={15} /></button>}
    {open && <aside className="research-guide" aria-label="Res Nova research guide"><header className="guide-header"><div className="guide-identity"><span className="guide-avatar"><Bot size={19} /></span><div><strong>Research Guide</strong><small>evidence-aware atlas companion</small></div></div><button className="guide-close" type="button" onClick={() => setOpen(false)} aria-label="Close research guide"><X size={18} /></button></header><div className="guide-trust"><span className="guide-live-dot" /> Database-backed guide · answers are bounded by the published atlas</div><div className="guide-messages">{messages.map((message) => <div className={`guide-message ${message.role}`} key={message.id}><div className="guide-message-bubble">{message.text}</div>{message.action && <button className="guide-action" type="button" onClick={() => runAction(message.action)}>{message.action.kind === "download" ? <Download size={13} /> : <ArrowUpRight size={13} />}{message.action.label}</button>}{message.citation && <a className="guide-citation" href={message.citation.href} target={message.citation.href.startsWith("/") ? undefined : "_blank"} rel="noreferrer"><ExternalLink size={12} />{message.citation.label}</a>}</div>)}{isTyping && <div className="guide-message guide"><div className="guide-message-bubble guide-typing" aria-label="Research Guide is typing"><i /><i /><i /></div></div>}<div ref={messagesEndRef} /></div><div className="guide-suggestions"><span>Suggested prompts</span><div className="guide-prompt-chips">{suggestedQuestions.map((question) => <button key={question.prompt} type="button" onClick={() => submitText(question.prompt)} disabled={isTyping}>{question.label}<ChevronRight size={12} /></button>)}</div></div><form className="guide-composer" onSubmit={submit}><label className="sr-only" htmlFor="guide-input">Ask the research guide</label><input id="guide-input" disabled={isTyping} value={input} onChange={(event) => setInput(event.target.value)} placeholder="Ask about the map, data, or theory…" /><button type="submit" disabled={isTyping} aria-label="Send question"><Send size={16} /></button></form><footer className="guide-footer"><span>Answers distinguish observation, derivation, and open interpretation.</span><a href={sparcSource.archiveUrl} target="_blank" rel="noreferrer" aria-label="Open SPARC source archive"><ExternalLink size={12} /></a></footer></aside>}
  </>;
}
