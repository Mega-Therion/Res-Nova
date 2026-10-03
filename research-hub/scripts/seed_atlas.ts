import { eq } from "drizzle-orm";
import {
  atlasClaims,
  atlasDatasets,
  atlasPublications,
  atlasReleaseState,
  atlasTimeline,
  atlasWorkstreams,
  theoryBridges,
  theoryNodes,
} from "../drizzle/schema";
import { claims, publications, datasets, timeline, workstreams, releaseState } from "../client/src/data/research";
import { getDb } from "../server/db";

const theoryNodeRows = [
  { id: "question", number: "01", title: "Question", detail: "Where scale-bridges break", status: "open" },
  { id: "action", number: "02", title: "Action", detail: "A variational object", status: "conditional" },
  { id: "weak-field", number: "03", title: "Weak field", detail: "AQUAL / μstd", status: "computed" },
  { id: "aest", number: "04", title: "AeST", detail: "Covariant completion", status: "conditional" },
  { id: "observable", number: "05", title: "Observable", detail: "Galaxy dynamics", status: "computed" },
  { id: "falsifier", number: "06", title: "Falsifier", detail: "What could stop it", status: "open" },
] as const;

const theoryBridgeRows = [
  { id: "question-action", label: "Gap → action", description: "A conceptual gap becomes a variational object.", fromNode: "question", toNode: "action" },
  { id: "action-weak-field", label: "Action → weak field", description: "The action is reduced to the galaxy-scale interpolation branch.", fromNode: "action", toNode: "weak-field" },
  { id: "weak-field-aest", label: "Weak field → AeST", description: "Phenomenology meets the conditional covariant completion.", fromNode: "weak-field", toNode: "aest" },
  { id: "aest-observable", label: "AeST → observable", description: "A relativistic construction is connected to a measurable system.", fromNode: "aest", toNode: "observable" },
  { id: "observable-falsifier", label: "Observable → falsifier", description: "A fit becomes meaningful only when failure modes are named.", fromNode: "observable", toNode: "falsifier" },
];

async function seed() {
  const db = await getDb();
  if (!db) throw new Error("DATABASE_URL is not configured");

  if ((await db.select({ id: atlasClaims.id }).from(atlasClaims).limit(1)).length === 0) {
    await db.insert(atlasClaims).values(claims.map((claim) => ({
      id: claim.id,
      status: claim.status,
      tone: claim.tone,
      domain: claim.domain,
      title: claim.title,
      summary: claim.summary,
      source: claim.source,
      limitation: claim.limitation,
    })));
  }
  if ((await db.select({ id: atlasWorkstreams.id }).from(atlasWorkstreams).limit(1)).length === 0) {
    await db.insert(atlasWorkstreams).values(workstreams.map((item) => ({ id: item.id, label: item.label, short: item.short, status: item.status, progress: item.progress, color: item.color })));
  }
  if ((await db.select({ id: atlasPublications.id }).from(atlasPublications).limit(1)).length === 0) {
    await db.insert(atlasPublications).values(publications.map((item) => ({ type: item.type, year: item.year, title: item.title, summary: item.summary, href: item.href, tag: item.tag })));
  }
  if ((await db.select({ id: atlasDatasets.id }).from(atlasDatasets).limit(1)).length === 0) {
    await db.insert(atlasDatasets).values(datasets.map((item) => ({ name: item.name, scope: item.scope, artifact: item.artifact, provenance: item.provenance, color: item.color })));
  }
  if ((await db.select({ id: atlasTimeline.id }).from(atlasTimeline).limit(1)).length === 0) {
    await db.insert(atlasTimeline).values(timeline.map((item) => ({ date: item.date, title: item.title, body: item.body })));
  }
  if ((await db.select({ id: theoryNodes.id }).from(theoryNodes).limit(1)).length === 0) await db.insert(theoryNodes).values(theoryNodeRows);
  if ((await db.select({ id: theoryBridges.id }).from(theoryBridges).limit(1)).length === 0) await db.insert(theoryBridges).values(theoryBridgeRows);
  if ((await db.select({ id: atlasReleaseState.id }).from(atlasReleaseState).where(eq(atlasReleaseState.commit, releaseState.commit)).limit(1)).length === 0) {
    await db.insert(atlasReleaseState).values({
      version: releaseState.version,
      researchRelease: releaseState.researchRelease,
      commit: releaseState.commit,
      note: releaseState.note,
      linksJson: JSON.stringify(releaseState.links),
      isCurrent: 1,
    });
  }
  console.log("Seeded Res Nova atlas content");
}

seed().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
