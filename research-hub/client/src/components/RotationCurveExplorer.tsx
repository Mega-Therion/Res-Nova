import { useEffect, useMemo, useState } from "react";
import { ChevronLeft, ChevronRight, Clipboard, Download, Info, MousePointer2, Quote, RotateCcw } from "lucide-react";
import { canonicalSparcCurves, sparcSource } from "../data/sparc";

export type RotationCurvePoint = {
  radius: number;
  observed: number;
  model: number;
  uncertainty: number;
};

type RotationCurveGalaxy = {
  id: string;
  name: string;
  morphology: string;
  distance: string;
  points: RotationCurvePoint[];
  note: string;
};

const curves: RotationCurveGalaxy[] = canonicalSparcCurves.map((curve) => ({
  ...curve,
  points: curve.points.map((point) => ({
    radius: point.radius,
    observed: point.observed,
    model: point.baryonicBaseline,
    uncertainty: point.uncertainty,
  })),
}));

const width = 760;
const height = 370;
const plot = { left: 64, right: 24, top: 22, bottom: 52 };
const xMax = 30;
const yMax = 240;
const xScale = (value: number) => plot.left + (value / xMax) * (width - plot.left - plot.right);
const yScale = (value: number) => height - plot.bottom - (value / yMax) * (height - plot.top - plot.bottom);
const linePath = (points: RotationCurvePoint[], key: "observed" | "model") => points.map((point, index) => `${index === 0 ? "M" : "L"} ${xScale(point.radius).toFixed(1)} ${yScale(point[key]).toFixed(1)}`).join(" ");
const PAGE_SIZE = 18;

function formatVelocity(value: number) {
  return `${value.toFixed(0)} km/s`;
}

function saveBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function createPdfFromJpeg(jpegDataUrl: string, width: number, height: number) {
  const encoder = new TextEncoder();
  const jpegBytes = Uint8Array.from(atob(jpegDataUrl.split(",")[1]), (character) => character.charCodeAt(0));
  const chunks: BlobPart[] = [];
  const offsets = [0];
  let offset = 0;
  const push = (chunk: Uint8Array) => { chunks.push(chunk as unknown as BlobPart); offset += chunk.length; };
  const object = (number: number, body: string, binary?: Uint8Array) => {
    offsets[number] = offset;
    push(encoder.encode(`${number} 0 obj\n${body}`));
    if (binary) push(binary);
    push(encoder.encode("\nendobj\n"));
  };
  push(encoder.encode("%PDF-1.4\n%\xFF\xFF\xFF\xFF\n"));
  object(1, "<< /Type /Catalog /Pages 2 0 R >>\n");
  object(2, "<< /Type /Pages /Kids [3 0 R] /Count 1 >>\n");
  object(3, `<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${width} ${height}] /Resources << /XObject << /Im0 4 0 R >> >> /Contents 5 0 R >>\n`);
  object(4, `<< /Type /XObject /Subtype /Image /Width ${width} /Height ${height} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ${jpegBytes.length} >>\nstream\n`, jpegBytes);
  const content = `q\n${width} 0 0 ${height} 0 0 cm\n/Im0 Do\nQ\n`;
  object(5, `<< /Length ${content.length} >>\nstream\n${content}endstream\n`);
  const xrefOffset = offset;
  const xref = `xref\n0 6\n0000000000 65535 f \n${[1, 2, 3, 4, 5].map((number) => `${String(offsets[number]).padStart(10, "0")} 00000 n `).join("\n")}\ntrailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n${xrefOffset}\n%%EOF`;
  push(encoder.encode(xref));
  return new Blob(chunks, { type: "application/pdf" });
}

function exportChart(format: "svg" | "png" | "pdf", galaxyName: string) {
  const svg = document.querySelector(".rotation-chart svg");
  if (!svg) return;
  const serialized = new XMLSerializer().serializeToString(svg);
  if (format === "svg") {
    saveBlob(new Blob([serialized], { type: "image/svg+xml" }), `${galaxyName.toLowerCase()}-rotation-curve.svg`);
    return;
  }
  const svgBlob = new Blob([serialized], { type: "image/svg+xml;charset=utf-8" });
  const url = URL.createObjectURL(svgBlob);
  const image = new Image();
  image.onload = () => {
    const width = 1520;
    const height = 740;
    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;
    const context = canvas.getContext("2d");
    if (!context) return;
    context.fillStyle = "#fbfcfa";
    context.fillRect(0, 0, width, height);
    context.drawImage(image, 0, 0, width, height);
    if (format === "png") canvas.toBlob((blob) => blob && saveBlob(blob, `${galaxyName.toLowerCase()}-rotation-curve.png`), "image/png");
    if (format === "pdf") saveBlob(createPdfFromJpeg(canvas.toDataURL("image/jpeg", 0.95), width, height), `${galaxyName.toLowerCase()}-rotation-curve.pdf`);
    URL.revokeObjectURL(url);
  };
  image.src = url;
}

export default function RotationCurveExplorer() {
  const [galaxyId, setGalaxyId] = useState(curves[0].id);
  const [showModel, setShowModel] = useState(true);
  const [showUncertainty, setShowUncertainty] = useState(true);
  const [activeIndex, setActiveIndex] = useState(0);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(0);
  const [citationCopied, setCitationCopied] = useState(false);
  const galaxy = curves.find((item) => item.id === galaxyId) ?? curves[0];
  const filteredCurves = useMemo(() => curves.filter((item) => item.name.toLowerCase().includes(search.toLowerCase())), [search]);
  const pageCount = Math.max(1, Math.ceil(filteredCurves.length / PAGE_SIZE));
  const pageCurves = filteredCurves.slice(page * PAGE_SIZE, page * PAGE_SIZE + PAGE_SIZE);
  const selectOptions = [galaxy, ...pageCurves.filter((item) => item.id !== galaxy.id)];
  const activePoint = galaxy.points[activeIndex] ?? galaxy.points[0];
  const residual = activePoint.observed - activePoint.model;
  const uncertaintyPath = useMemo(() => {
    if (!showUncertainty) return "";
    const upper = galaxy.points.map((point, index) => `${index === 0 ? "M" : "L"} ${xScale(point.radius).toFixed(1)} ${yScale(point.observed + point.uncertainty).toFixed(1)}`).join(" ");
    const lower = [...galaxy.points].reverse().map((point) => `L ${xScale(point.radius).toFixed(1)} ${yScale(Math.max(0, point.observed - point.uncertainty)).toFixed(1)}`).join(" ");
    return `${upper} ${lower} Z`;
  }, [galaxy, showUncertainty]);

  const selectGalaxy = (id: string) => {
    setGalaxyId(id);
    setActiveIndex(0);
  };

  const updateSearch = (value: string) => {
    setSearch(value);
    setPage(0);
  };

  const copyCitation = async () => {
    try {
      await navigator.clipboard.writeText(`Res Nova Research Atlas. ${galaxy.name} canonical SPARC rotation curve. ${sparcSource.authors}; ${sparcSource.archiveFile}; ${sparcSource.doi}.`);
      setCitationCopied(true);
      window.setTimeout(() => setCitationCopied(false), 1800);
    } catch {
      setCitationCopied(false);
    }
  };

  useEffect(() => {
    const handleGuideAction = (event: Event) => {
      const detail = (event as CustomEvent<{ galaxy?: string; showModel?: boolean; showUncertainty?: boolean }>).detail;
      if (detail.galaxy) {
        const requested = curves.find((item) => item.name.toLowerCase() === detail.galaxy?.toLowerCase());
        if (requested) selectGalaxy(requested.id);
      }
      if (typeof detail.showModel === "boolean") setShowModel(detail.showModel);
      if (typeof detail.showUncertainty === "boolean") setShowUncertainty(detail.showUncertainty);
    };
    window.addEventListener("resnova:guide-action", handleGuideAction);
    return () => window.removeEventListener("resnova:guide-action", handleGuideAction);
  }, []);

  return (
    <section className="rotation-explorer" aria-labelledby="rotation-explorer-title">
      <div className="rotation-explorer-head">
        <div>
          <span className="eyebrow">Canonical evidence · {sparcSource.galaxyCount} galaxies · {sparcSource.authors}</span>
          <h2 id="rotation-explorer-title">Read the curve point by point.</h2>
          <p>Hover or focus a marker to inspect an official SPARC radius, measured velocity, uncertainty, and the published baryonic component baseline.</p>
        </div>
        <div className="rotation-controls" aria-label="Rotation curve controls">
          <label className="rotation-select-label" htmlFor="galaxy-search">Find</label>
          <input className="rotation-search" id="galaxy-search" value={search} onChange={(event) => updateSearch(event.target.value)} placeholder="NGC…" />
          <label className="rotation-select-label" htmlFor="galaxy-select">Galaxy</label>
          <select id="galaxy-select" value={galaxyId} onChange={(event) => selectGalaxy(event.target.value)}>
            {selectOptions.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}
          </select>
          <button className={`rotation-toggle ${showModel ? "is-on" : ""}`} type="button" aria-pressed={showModel} onClick={() => setShowModel(!showModel)}><span className="toggle-swatch swatch-model" /> Baseline</button>
          <button className={`rotation-toggle ${showUncertainty ? "is-on" : ""}`} type="button" aria-pressed={showUncertainty} onClick={() => setShowUncertainty(!showUncertainty)}><span className="toggle-swatch swatch-band" /> Uncertainty</button>
          <div className="rotation-pagination"><button type="button" disabled={page === 0} onClick={() => setPage((current) => Math.max(0, current - 1))} aria-label="Previous galaxy page"><ChevronLeft size={13} /></button><span>{filteredCurves.length ? page * PAGE_SIZE + 1 : 0}–{Math.min((page + 1) * PAGE_SIZE, filteredCurves.length)} / {filteredCurves.length} galaxies</span><button type="button" disabled={page >= pageCount - 1} onClick={() => setPage((current) => Math.min(pageCount - 1, current + 1))} aria-label="Next galaxy page"><ChevronRight size={13} /></button></div>
        </div>
      </div>
      <div className="rotation-layout">
        <div className="rotation-chart-wrap">
          <div className="rotation-chart" role="img" aria-label={`Canonical SPARC rotation curve for ${galaxy.name}. Horizontal axis is radius in kiloparsecs; vertical axis is circular velocity in kilometers per second.`}>
            <svg viewBox={`0 0 ${width} ${height}`} preserveAspectRatio="none">
              <title>{galaxy.name} canonical SPARC rotation curve</title>
              <desc>Official observed velocity markers with published uncertainty and an optional baryonic component baseline.</desc>
              {[0, 60, 120, 180, 240].map((tick) => <g key={tick}><line className="rotation-gridline" x1={plot.left} x2={width - plot.right} y1={yScale(tick)} y2={yScale(tick)} /><text className="rotation-tick" x={plot.left - 12} y={yScale(tick) + 4} textAnchor="end">{tick}</text></g>)}
              {[0, 10, 20, 30].map((tick) => <g key={tick}><line className="rotation-gridline rotation-gridline-vertical" x1={xScale(tick)} x2={xScale(tick)} y1={plot.top} y2={height - plot.bottom} /><text className="rotation-tick" x={xScale(tick)} y={height - plot.bottom + 23} textAnchor="middle">{tick}</text></g>)}
              <line className="rotation-axis" x1={plot.left} x2={width - plot.right} y1={height - plot.bottom} y2={height - plot.bottom} />
              <line className="rotation-axis" x1={plot.left} x2={plot.left} y1={plot.top} y2={height - plot.bottom} />
              {showUncertainty && <path className="rotation-band" d={uncertaintyPath} />}
              {showModel && <path className="rotation-model" d={linePath(galaxy.points, "model")} />}
              {galaxy.points.map((point, index) => <g key={`${galaxy.id}-${point.radius}`} className="rotation-point-group" onMouseEnter={() => setActiveIndex(index)} onFocus={() => setActiveIndex(index)}><line className="rotation-error" x1={xScale(point.radius)} x2={xScale(point.radius)} y1={yScale(point.observed - point.uncertainty)} y2={yScale(point.observed + point.uncertainty)} /><line className="rotation-error-cap" x1={xScale(point.radius) - 4} x2={xScale(point.radius) + 4} y1={yScale(point.observed - point.uncertainty)} y2={yScale(point.observed - point.uncertainty)} /><line className="rotation-error-cap" x1={xScale(point.radius) - 4} x2={xScale(point.radius) + 4} y1={yScale(point.observed + point.uncertainty)} y2={yScale(point.observed + point.uncertainty)} /><circle className={`rotation-point ${activeIndex === index ? "is-active" : ""}`} tabIndex={0} role="button" aria-label={`${galaxy.name}, radius ${point.radius} kiloparsecs, observed ${formatVelocity(point.observed)}`} cx={xScale(point.radius)} cy={yScale(point.observed)} r={activeIndex === index ? 6 : 4} /></g>)}
              <text className="rotation-axis-label" x={(plot.left + width - plot.right) / 2} y={height - 8} textAnchor="middle">radius (kpc)</text>
              <text className="rotation-axis-label" transform={`translate(15 ${(plot.top + height - plot.bottom) / 2}) rotate(-90)`} textAnchor="middle">circular velocity (km/s)</text>
            </svg>
            <div className="rotation-tooltip" aria-live="polite"><span className="tooltip-kicker">{galaxy.name} · point {activeIndex + 1}/{galaxy.points.length}</span><strong>r = {activePoint.radius.toFixed(2)} kpc</strong><div><span>observed <b>{formatVelocity(activePoint.observed)}</b></span><span>error <b>±{formatVelocity(activePoint.uncertainty)}</b></span><span>baseline <b>{formatVelocity(activePoint.model)}</b></span><span>residual <b className={residual >= 0 ? "residual-positive" : "residual-negative"}>{residual > 0 ? "+" : ""}{residual.toFixed(0)} km/s</b></span></div></div>
          </div>
          <div className="rotation-legend"><span><i className="legend-point" /> observed</span><span><i className="legend-line" /> baryonic baseline</span><span><i className="legend-band" /> ± published error</span></div>
        </div>
        <aside className="rotation-reading"><div className="rotation-reading-icon"><MousePointer2 size={17} /></div><span className="eyebrow">Selected point</span><strong>{formatVelocity(activePoint.observed)}</strong><p>At <b>{activePoint.radius.toFixed(2)} kpc</b>, the observed curve sits <b>{Math.abs(residual).toFixed(0)} km/s {residual >= 0 ? "above" : "below"}</b> the published baryonic baseline.</p><div className="rotation-metadata"><span>morphology <b>{galaxy.morphology}</b></span><span>distance <b>{galaxy.distance}</b></span><span>points <b>{galaxy.points.length}</b></span></div><p className="rotation-caveat"><Info size={14} /> {galaxy.note}</p><div className="rotation-exports"><span>Publication exports</span><div><button type="button" onClick={() => exportChart("png", galaxy.name)}><Download size={12} /> PNG</button><button type="button" onClick={() => exportChart("pdf", galaxy.name)}><Download size={12} /> PDF</button><button type="button" onClick={() => exportChart("svg", galaxy.name)}><Download size={12} /> SVG</button><button type="button" onClick={copyCitation}>{citationCopied ? <Clipboard size={12} /> : <Quote size={12} />} {citationCopied ? "Copied" : "Cite"}</button></div></div><a className="rotation-source-link" href={sparcSource.archiveUrl} target="_blank" rel="noreferrer">Source archive · Zenodo DOI</a><button className="rotation-reset" type="button" onClick={() => { setGalaxyId(curves[0].id); setActiveIndex(0); setPage(0); setSearch(""); setShowModel(true); setShowUncertainty(true); }}><RotateCcw size={13} /> Reset explorer</button></aside>
      </div>
    </section>
  );
}
