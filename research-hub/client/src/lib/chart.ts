export function niceTicks(min: number, max: number, count = 5): number[] {
  if (!Number.isFinite(min) || !Number.isFinite(max) || min === max) {
    return [min || 0];
  }
  const span = max - min;
  const raw = span / Math.max(1, count - 1);
  const mag = 10 ** Math.floor(Math.log10(raw));
  const residual = raw / mag;
  const step = residual >= 7.5 ? 10 * mag : residual >= 3.5 ? 5 * mag : residual >= 1.5 ? 2 * mag : mag;
  const start = Math.ceil(min / step) * step;
  const ticks: number[] = [];
  for (let value = start; value <= max + step * 0.001; value += step) {
    ticks.push(Number(value.toPrecision(12)));
  }
  if (ticks[0] !== min) ticks.unshift(Number(min.toPrecision(12)));
  if (ticks[ticks.length - 1] !== max) ticks.push(Number(max.toPrecision(12)));
  return ticks;
}

export function linePath(
  points: Array<{ x: number; y: number }>,
  xScale: (v: number) => number,
  yScale: (v: number) => number,
) {
  return points
    .map((point, index) => `${index === 0 ? "M" : "L"} ${xScale(point.x).toFixed(2)} ${yScale(point.y).toFixed(2)}`)
    .join(" ");
}

export function logTicks(minExp: number, maxExp: number): number[] {
  const ticks: number[] = [];
  for (let exp = Math.ceil(minExp); exp <= Math.floor(maxExp); exp += 1) ticks.push(exp);
  return ticks;
}

const SUPER: Record<string, string> = {
  "-": "⁻",
  "0": "⁰",
  "1": "¹",
  "2": "²",
  "3": "³",
  "4": "⁴",
  "5": "⁵",
  "6": "⁶",
  "7": "⁷",
  "8": "⁸",
  "9": "⁹",
};

export function decadeLabel(exp: number) {
  return `10${String(exp).replace(/./g, (char) => SUPER[char] ?? char)}`;
}

function saveBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  window.setTimeout(() => URL.revokeObjectURL(url), 800);
}

export function exportSvgElement(svg: SVGSVGElement, filename: string) {
  const clone = svg.cloneNode(true) as SVGSVGElement;
  clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
  const serialized = new XMLSerializer().serializeToString(clone);
  saveBlob(new Blob([serialized], { type: "image/svg+xml" }), filename);
}

export function exportSvgAsPng(svg: SVGSVGElement, filename: string, background: string) {
  const clone = svg.cloneNode(true) as SVGSVGElement;
  clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
  const serialized = new XMLSerializer().serializeToString(clone);
  const blob = new Blob([serialized], { type: "image/svg+xml;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const image = new Image();
  image.onload = () => {
    const box = svg.viewBox.baseVal;
    const width = Math.round((box?.width || svg.clientWidth || 1200) * 2);
    const height = Math.round((box?.height || svg.clientHeight || 720) * 2);
    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.fillStyle = background;
    ctx.fillRect(0, 0, width, height);
    ctx.drawImage(image, 0, 0, width, height);
    canvas.toBlob((png) => png && saveBlob(png, filename), "image/png");
    URL.revokeObjectURL(url);
  };
  image.src = url;
}

export function printSvgAsPdf(svg: SVGSVGElement, title: string, caption: string, source?: string) {
  const clone = svg.cloneNode(true) as SVGSVGElement;
  clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
  const serialized = new XMLSerializer().serializeToString(clone);
  const popup = window.open("", "_blank", "noopener,noreferrer,width=980,height=760");
  if (!popup) return;
  popup.document.write(`<!doctype html><html><head><title>${title}</title><style>
    @page { size: A4 landscape; margin: 14mm; }
    body { margin: 0; color: #10262d; font-family: Arial, sans-serif; }
    h1 { font-size: 18px; margin: 0 0 12px; }
    img { display: block; width: 100%; max-height: 155mm; object-fit: contain; }
    p { font-size: 11px; line-height: 1.45; margin: 10px 0 0; }
    small { display: block; margin-top: 6px; color: #64777b; font-family: monospace; }
  </style></head><body><h1>${title}</h1><img alt="${title}" src="data:image/svg+xml;charset=utf-8,${encodeURIComponent(serialized)}"/><p>${caption}</p>${source ? `<small>${source}</small>` : ""}</body></html>`);
  popup.document.close();
  popup.focus();
  window.setTimeout(() => popup.print(), 250);
}
