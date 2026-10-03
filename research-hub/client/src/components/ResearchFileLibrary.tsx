import { FormEvent, useState } from "react";
import { ArrowDownRight, FileUp, FolderOpen, Loader2, LockKeyhole } from "lucide-react";
import { useAuth } from "@/_core/hooks/useAuth";
import { trpc } from "../lib/trpc";

function formatBytes(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function ResearchFileLibrary() {
  const { user } = useAuth();
  const files = trpc.researchFiles.listPublic.useQuery();
  const upload = trpc.researchFiles.upload.useMutation({ onSuccess: () => files.refetch() });
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState("publication supplement");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    if (!selectedFile || !title.trim()) return;
    setMessage("");
    const base64 = await new Promise<string>((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(String(reader.result).split(",")[1] ?? "");
      reader.onerror = () => reject(reader.error);
      reader.readAsDataURL(selectedFile);
    });
    upload.mutate({ title: title.trim(), category, fileName: selectedFile.name, mimeType: selectedFile.type || "application/octet-stream", base64 }, {
      onSuccess: () => { setTitle(""); setSelectedFile(null); setMessage("File stored and added to the public catalog."); },
      onError: (error) => setMessage(error.message),
    });
  };

  return <section className="research-files-panel"><div className="research-files-heading"><div><span className="eyebrow">Persistent research files</span><h2>Artifacts with a durable home.</h2><p>Publication supplements, verified datasets, chart exports, and release documents are stored outside the application bundle and catalogued with provenance metadata.</p></div><FolderOpen size={26} /></div><div className="research-file-grid">{files.isLoading && <div className="research-file-empty"><Loader2 className="spin" size={18} /> Loading stored artifacts…</div>}{!files.isLoading && files.data?.length === 0 && <div className="research-file-empty">No public files have been uploaded yet. The catalog is ready for release artifacts.</div>}{files.data?.map((file) => <article className="research-file-card" key={file.id}><div className="research-file-icon"><FolderOpen size={17} /></div><div><span className="eyebrow">{file.category}</span><h3>{file.title}</h3><p>{file.description || file.fileName}</p><small>{file.mimeType} · {formatBytes(file.sizeBytes)}</small></div><a className="research-file-download" href={file.publicUrl} target="_blank" rel="noreferrer" aria-label={`Open ${file.title}`}><ArrowDownRight size={15} /></a></article>)}</div>{user?.role === "admin" && <form className="research-file-upload" onSubmit={submit}><div><span className="eyebrow">Admin upload</span><strong>Add a release artifact</strong><p>Files are uploaded to S3-compatible storage; only metadata is persisted in the database.</p></div><label><span className="sr-only">Artifact title</span><input value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Artifact title" required /></label><label><span className="sr-only">Artifact category</span><select value={category} onChange={(event) => setCategory(event.target.value)}><option>publication supplement</option><option>dataset</option><option>chart export</option><option>release document</option></select></label><label className="file-input-label"><FileUp size={15} /><span>{selectedFile?.name || "Choose file"}</span><input type="file" onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)} required /></label><button className="button button-dark" type="submit" disabled={upload.isPending || !selectedFile}>{upload.isPending ? "Storing…" : "Store artifact"}</button>{message && <span className="research-file-message">{message}</span>}</form>}{!user && <div className="research-file-access"><LockKeyhole size={14} /> Admin sign-in is required to upload new artifacts.</div>}</section>;
}
