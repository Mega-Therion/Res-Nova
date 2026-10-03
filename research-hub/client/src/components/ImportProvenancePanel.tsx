import { useState } from "react";
import { Check, Clipboard, FileArchive, ShieldCheck } from "lucide-react";
import { importProvenance } from "@/data/import-provenance";

export default function ImportProvenancePanel() {
  const [copied, setCopied] = useState(false);
  const copyChecksum = async () => {
    try {
      await navigator.clipboard.writeText(importProvenance.archiveSha256);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setCopied(false);
    }
  };

  return (
    <section className="provenance-panel" aria-labelledby="import-provenance-title">
      <div className="provenance-heading">
        <div className="provenance-icon" aria-hidden="true"><FileArchive size={19} /></div>
        <div>
          <span className="eyebrow">Import provenance</span>
          <h2 id="import-provenance-title">The package has a durable fingerprint.</h2>
          <p>This public layer was imported from the named archive. The checksum and manifest snapshot let readers verify what was used without treating the package as a substitute for the pinned research release.</p>
        </div>
      </div>
      <div className="provenance-grid">
        <div className="provenance-fingerprint">
          <span className="provenance-label"><ShieldCheck size={13} /> SHA-256 archive checksum</span>
          <code>{importProvenance.archiveSha256}</code>
          <button type="button" className="provenance-copy" onClick={copyChecksum}>
            {copied ? <Check size={12} /> : <Clipboard size={12} />} {copied ? "Copied" : "Copy checksum"}
          </button>
        </div>
        <div className="provenance-meta">
          <span><b>Archive</b>{importProvenance.archiveFile}</span>
          <span><b>Source</b>{importProvenance.sourceWorkspace}</span>
          <span><b>Imported</b>{importProvenance.importedAt}</span>
        </div>
      </div>
      <details className="provenance-manifest">
        <summary>View package manifest snapshot</summary>
        <pre>{JSON.stringify(importProvenance.manifest, null, 2)}</pre>
      </details>
    </section>
  );
}
