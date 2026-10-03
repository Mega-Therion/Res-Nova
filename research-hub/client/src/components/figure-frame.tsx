import { useRef, useState, type ReactNode } from "react";
import { Clipboard, Download, FileText, Quote } from "lucide-react";
import { releaseState } from "@/data/research";
import { cn } from "@/lib/cn";
import { exportSvgAsPng, printSvgAsPdf } from "@/lib/chart";

function slugify(value: string) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}

export function FigureFrame({
  number,
  title,
  caption,
  source,
  children,
  dark = false,
  className,
}: {
  number: string;
  title: string;
  caption: string;
  source?: string;
  children: ReactNode;
  dark?: boolean;
  className?: string;
}) {
  const figureRef = useRef<HTMLElement>(null);
  const [citationState, setCitationState] = useState<"idle" | "copied">("idle");
  const baseName = `res-nova-figure-${number}-${slugify(title)}`;
  const citation = `Res Nova Research Atlas. Fig. ${number}: ${title}. ${releaseState.researchRelease}; release ${releaseState.commit}.${source ? ` Source: ${source}.` : ""}`;
  const bibtex = `@misc{resnova_${slugify(title).replaceAll("-", "_")},\n  title = {${title}},\n  author = {Res Nova Research Atlas},\n  year = {2026},\n  howpublished = {${releaseState.links.github}},\n  note = {${releaseState.researchRelease}; release ${releaseState.commit}${source ? `; source: ${source}` : ""}}\n}`;

  const getSvg = () => figureRef.current?.querySelector("svg") ?? null;
  const copyCitation = async () => {
    try {
      await navigator.clipboard.writeText(citation);
      setCitationState("copied");
      window.setTimeout(() => setCitationState("idle"), 1800);
    } catch {
      setCitationState("idle");
    }
  };
  const downloadBibtex = () => {
    const blob = new Blob([bibtex], { type: "application/x-bibtex;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `${baseName}.bib`;
    anchor.click();
    window.setTimeout(() => URL.revokeObjectURL(url), 800);
  };

  return (
    <figure ref={figureRef} className={cn("figure-frame rounded-xl", dark && "bg-ink text-paper", className)}>
      {children}
      <div className={cn("figure-actions", dark && "border-white/10")} aria-label={`Export and citation controls for figure ${number}`}>
        <button type="button" onClick={() => { const svg = getSvg(); if (svg) exportSvgAsPng(svg, `${baseName}.png`, dark ? "#10262d" : "#fbfcfa"); }}>
          <Download size={12} /> PNG
        </button>
        <button type="button" onClick={() => { const svg = getSvg(); if (svg) printSvgAsPdf(svg, `Fig. ${number} · ${title}`, caption, source); }}>
          <FileText size={12} /> PDF / print
        </button>
        <button type="button" onClick={copyCitation}>
          {citationState === "copied" ? <Clipboard size={12} /> : <Quote size={12} />} {citationState === "copied" ? "Copied" : "Cite"}
        </button>
        <button type="button" onClick={downloadBibtex}>
          <Download size={12} /> BibTeX
        </button>
      </div>
      <figcaption className={cn("figure-caption", dark && "border-white/10 text-mist")}>
        <strong className={dark ? "text-accent-2" : undefined}>
          Fig. {number} · {title}
        </strong>
        {caption}
        {source ? <span className="mt-2 block font-mono text-[10px] tracking-wide opacity-80">{source}</span> : null}
      </figcaption>
    </figure>
  );
}

export function SectionIntro({
  eyebrow,
  title,
  body,
  invert = false,
}: {
  eyebrow: string;
  title: string;
  body: string;
  invert?: boolean;
}) {
  return (
    <div className="max-w-xl">
      <span className={cn("eyebrow", invert && "text-accent-2")}>{eyebrow}</span>
      <h2 className={cn("mt-3 mb-3 font-display text-[clamp(1.9rem,4vw,3.1rem)] font-medium tracking-[-0.035em] leading-[1.05]", invert ? "text-paper" : "text-ink")}>
        {title}
      </h2>
      <p className={cn("m-0 text-[1.05rem] leading-relaxed", invert ? "text-[#a9bec0]" : "text-muted")}>{body}</p>
    </div>
  );
}
