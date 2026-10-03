import { FormEvent, useEffect, useMemo, useState } from "react";
import { CheckCircle2, Eye, EyeOff, FileText, History, LockKeyhole, Save, ShieldCheck, Users } from "lucide-react";
import { useAuth } from "@/_core/hooks/useAuth";
import { startLogin } from "@/const";
import DashboardLayout from "../components/DashboardLayout";
import ResearchFileLibrary from "../components/ResearchFileLibrary";
import { releaseState } from "../data/research";
import { trpc } from "../lib/trpc";

const emptyClaim = { id: "", status: "", tone: "", domain: "", title: "", summary: "", source: "", limitation: "" };
const defaultRelease = { version: releaseState.version, researchRelease: releaseState.researchRelease, commit: releaseState.commit, note: releaseState.note, links: releaseState.links };
type ClaimForm = typeof emptyClaim;

function AccessState({ kind }: { kind: "login" | "denied" }) {
  return <div className="admin-access-state"><div className="admin-access-icon"><LockKeyhole size={25} /></div><span className="eyebrow">Admin workspace</span><h1>{kind === "login" ? "Sign in to manage the atlas." : "This account is not an atlas administrator."}</h1><p>{kind === "login" ? "Claims, releases, roles, audit history, and research-file metadata are protected by the server-side admin role." : "Ask the project owner to grant the admin role before attempting to edit publication-facing records."}</p>{kind === "login" && <button className="button button-primary" onClick={() => startLogin()}>Sign in with Manus</button>}</div>;
}

function AdminWorkspace() {
  const { user, loading } = useAuth();
  const isAdmin = user?.role === "admin";
  const claims = trpc.admin.claims.list.useQuery(undefined, { enabled: isAdmin, retry: false });
  const currentRelease = trpc.admin.release.current.useQuery(undefined, { enabled: isAdmin, retry: false });
  const files = trpc.admin.files.list.useQuery(undefined, { enabled: isAdmin, retry: false });
  const users = trpc.admin.users.list.useQuery(undefined, { enabled: isAdmin, retry: false });
  const audit = trpc.admin.audit.list.useQuery(undefined, { enabled: isAdmin, retry: false });
  const utils = trpc.useUtils();
  const updateClaim = trpc.admin.claims.update.useMutation({ onSuccess: () => { void claims.refetch(); void utils.atlas.snapshot.invalidate(); void audit.refetch(); } });
  const createRelease = trpc.admin.release.create.useMutation({ onSuccess: () => { void currentRelease.refetch(); void utils.atlas.snapshot.invalidate(); void audit.refetch(); } });
  const setRole = trpc.admin.users.setRole.useMutation({ onSuccess: () => { void users.refetch(); void audit.refetch(); } });
  const [selectedId, setSelectedId] = useState("");
  const [claimForm, setClaimForm] = useState<ClaimForm>(emptyClaim);
  const [releaseForm, setReleaseForm] = useState(defaultRelease);
  const [notice, setNotice] = useState("");
  const [previewOpen, setPreviewOpen] = useState(false);

  const selectedClaim = useMemo(() => claims.data?.find((claim) => claim.id === selectedId), [claims.data, selectedId]);
  useEffect(() => {
    if (!selectedClaim) return;
    setClaimForm({ id: selectedClaim.id, status: selectedClaim.status, tone: selectedClaim.tone, domain: selectedClaim.domain, title: selectedClaim.title, summary: selectedClaim.summary, source: selectedClaim.source, limitation: selectedClaim.limitation });
  }, [selectedClaim]);
  useEffect(() => {
    if (!currentRelease.data) return;
    const links = JSON.parse(currentRelease.data.linksJson) as typeof releaseState.links;
    setReleaseForm({ version: currentRelease.data.version, researchRelease: currentRelease.data.researchRelease, commit: currentRelease.data.commit, note: currentRelease.data.note, links });
  }, [currentRelease.data]);

  if (loading) return <div className="admin-loading">Loading administrator session…</div>;
  if (!user) return <AccessState kind="login" />;
  if (!isAdmin) return <AccessState kind="denied" />;

  const updateClaimField = (field: keyof ClaimForm, value: string) => setClaimForm((current) => ({ ...current, [field]: value }));
  const submitClaim = (event: FormEvent) => {
    event.preventDefault();
    setNotice("");
    updateClaim.mutate(claimForm, { onSuccess: () => setNotice(`Saved ${claimForm.id}.`), onError: (error) => setNotice(error.message) });
  };
  const submitRelease = (event: FormEvent) => {
    event.preventDefault();
    setNotice("");
    createRelease.mutate(releaseForm, { onSuccess: () => { setPreviewOpen(false); setNotice(`Published release snapshot ${releaseForm.commit}.`); }, onError: (error) => setNotice(error.message) });
  };
  const setLink = (key: keyof typeof releaseForm.links, value: string) => setReleaseForm((current) => ({ ...current, links: { ...current.links, [key]: value } }));

  return <div className="admin-workspace"><header className="admin-workspace-header"><div><span className="eyebrow">Res Nova / protected control room</span><h1>Curate the public research state.</h1><p>Edit only what the evidence ledger can support. Every change is persisted in the database and immediately visible to the public atlas after cache refresh.</p></div><div className="admin-role-badge"><ShieldCheck size={17} /> {user.name || user.email || "administrator"}</div></header>{notice && <div className="admin-notice"><CheckCircle2 size={16} /> {notice}</div>}<div className="admin-grid"><section className="admin-card"><div className="admin-card-heading"><div><span className="eyebrow">Claim registry</span><h2>Edit a curated claim</h2></div><FileText size={20} /></div><label className="admin-field"><span>Select claim</span><select value={selectedId} onChange={(event) => setSelectedId(event.target.value)}><option value="">Choose a claim…</option>{claims.data?.map((claim) => <option key={claim.id} value={claim.id}>{claim.id} · {claim.title}</option>)}</select></label>{selectedId && <form className="admin-form" onSubmit={submitClaim}><div className="admin-form-split"><label className="admin-field"><span>Status</span><select value={claimForm.status} onChange={(event) => updateClaimField("status", event.target.value)}><option>derived</option><option>computed</option><option>conditional</option><option>open</option><option>superseded</option><option>refuted</option></select></label><label className="admin-field"><span>Tone</span><select value={claimForm.tone} onChange={(event) => updateClaimField("tone", event.target.value)}><option>blue</option><option>amber</option><option>red</option><option>slate</option></select></label></div><label className="admin-field"><span>Domain</span><input value={claimForm.domain} onChange={(event) => updateClaimField("domain", event.target.value)} /></label><label className="admin-field"><span>Title</span><input value={claimForm.title} onChange={(event) => updateClaimField("title", event.target.value)} /></label><label className="admin-field"><span>Summary</span><textarea rows={4} value={claimForm.summary} onChange={(event) => updateClaimField("summary", event.target.value)} /></label><label className="admin-field"><span>Source artifact</span><input value={claimForm.source} onChange={(event) => updateClaimField("source", event.target.value)} /></label><label className="admin-field"><span>Boundary / limitation</span><textarea rows={3} value={claimForm.limitation} onChange={(event) => updateClaimField("limitation", event.target.value)} /></label><button className="button button-primary" type="submit" disabled={updateClaim.isPending}><Save size={15} /> {updateClaim.isPending ? "Saving…" : "Save claim"}</button></form>}</section><section className="admin-card"><div className="admin-card-heading"><div><span className="eyebrow">Release state</span><h2>Preview before publishing</h2></div><ShieldCheck size={20} /></div><form className="admin-form" onSubmit={submitRelease}><div className="admin-form-split"><label className="admin-field"><span>Version</span><input value={releaseForm.version} onChange={(event) => setReleaseForm({ ...releaseForm, version: event.target.value })} /></label><label className="admin-field"><span>Commit</span><input value={releaseForm.commit} onChange={(event) => setReleaseForm({ ...releaseForm, commit: event.target.value })} /></label></div><label className="admin-field"><span>Research release</span><input value={releaseForm.researchRelease} onChange={(event) => setReleaseForm({ ...releaseForm, researchRelease: event.target.value })} /></label><label className="admin-field"><span>Release note</span><textarea rows={4} value={releaseForm.note} onChange={(event) => setReleaseForm({ ...releaseForm, note: event.target.value })} /></label><details className="admin-links"><summary>Publication links</summary>{(Object.keys(releaseForm.links) as Array<keyof typeof releaseForm.links>).map((key) => <label className="admin-field" key={key}><span>{key}</span><input value={releaseForm.links[key]} onChange={(event) => setLink(key, event.target.value)} /></label>)}</details><div className="admin-release-actions"><button className="button button-quiet" type="button" onClick={() => setPreviewOpen((open) => !open)}>{previewOpen ? <EyeOff size={15} /> : <Eye size={15} />} {previewOpen ? "Hide preview" : "Preview snapshot"}</button><button className="button button-dark" type="submit" disabled={createRelease.isPending}><Save size={15} /> {createRelease.isPending ? "Publishing…" : "Publish snapshot"}</button></div>{previewOpen && <div className="admin-release-preview"><span className="eyebrow">Unpublished preview</span><strong>{releaseForm.version}</strong><small>{releaseForm.researchRelease} · {releaseForm.commit}</small><p>{releaseForm.note}</p><span className="admin-preview-boundary">Publishing will make this the current public release and record an audit event.</span></div>}</form></section></div><section className="admin-card admin-users-card"><div className="admin-card-heading"><div><span className="eyebrow">Access control</span><h2>Role management</h2></div><Users size={20} /></div><div className="admin-user-list">{users.data?.map((member) => <div className="admin-user-row" key={member.id}><span><strong>{member.name || member.email || `User ${member.id}`}</strong><small>{member.email || "No email provided"}</small></span><select value={member.role} onChange={(event) => setRole.mutate({ id: member.id, role: event.target.value as "user" | "admin" })} disabled={setRole.isPending}><option value="admin">admin</option><option value="user">user</option></select></div>)}</div></section><section className="admin-card admin-audit-card"><div className="admin-card-heading"><div><span className="eyebrow">Immutable change history</span><h2>Administrative audit trail</h2></div><History size={20} /></div><div className="admin-audit-list">{audit.data?.length ? audit.data.map((entry) => <div className="admin-audit-row" key={entry.id}><span className="admin-audit-action">{entry.action}</span><span><strong>{entry.summary}</strong><small>{entry.entityType} · {entry.entityId} · {new Date(entry.createdAt).toLocaleString()}</small></span></div>) : <div className="admin-empty">No administrative changes recorded yet.</div>}</div></section><section className="admin-card admin-files-card"><div className="admin-card-heading"><div><span className="eyebrow">Storage inventory</span><h2>Uploaded research artifacts</h2></div><span className="admin-count">{files.data?.length ?? 0} records</span></div><div className="admin-file-list">{files.data?.map((file) => <a className="admin-file-row" key={file.id} href={file.publicUrl} target="_blank" rel="noreferrer"><span><strong>{file.title}</strong><small>{file.category} · {file.fileName} · {file.sizeBytes.toLocaleString()} bytes</small></span><span className="admin-file-status">{file.visibility}</span></a>)}</div></section><ResearchFileLibrary /></div>;
}

export default function AdminDashboard() {
  return <DashboardLayout><AdminWorkspace /></DashboardLayout>;
}
