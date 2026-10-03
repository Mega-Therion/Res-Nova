import { and, desc, eq, like, or } from "drizzle-orm";
import { drizzle } from "drizzle-orm/mysql2";
import {
  atlasClaims,
  atlasDatasets,
  atlasPublications,
  atlasReleaseState,
  atlasTimeline,
  atlasWorkstreams,
  adminAuditLog,
  InsertUser,
  researchFiles,
  theoryBridges,
  theoryNodes,
  users,
} from "../drizzle/schema";
import { ENV } from "./_core/env";

let _db: ReturnType<typeof drizzle> | null = null;

export async function getDb() {
  if (!_db && process.env.DATABASE_URL) {
    try {
      _db = drizzle(process.env.DATABASE_URL);
    } catch (error) {
      console.warn("[Database] Failed to connect:", error);
      _db = null;
    }
  }
  return _db;
}

export async function upsertUser(user: InsertUser): Promise<void> {
  if (!user.openId) throw new Error("User openId is required for upsert");
  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot upsert user: database not available");
    return;
  }

  const values: InsertUser = { openId: user.openId };
  const updateSet: Record<string, unknown> = {};
  const textFields = ["name", "email", "loginMethod"] as const;
  for (const field of textFields) {
    if (user[field] !== undefined) {
      values[field] = user[field] ?? null;
      updateSet[field] = user[field] ?? null;
    }
  }
  if (user.lastSignedIn !== undefined) {
    values.lastSignedIn = user.lastSignedIn;
    updateSet.lastSignedIn = user.lastSignedIn;
  }
  if (user.role !== undefined) {
    values.role = user.role;
    updateSet.role = user.role;
  } else if (user.openId === ENV.ownerOpenId) {
    values.role = "admin";
    updateSet.role = "admin";
  }
  values.lastSignedIn ??= new Date();
  if (Object.keys(updateSet).length === 0) updateSet.lastSignedIn = new Date();
  await db.insert(users).values(values).onDuplicateKeyUpdate({ set: updateSet });
}

export async function getUserByOpenId(openId: string) {
  const db = await getDb();
  if (!db) return undefined;
  const result = await db.select().from(users).where(eq(users.openId, openId)).limit(1);
  return result[0];
}

export async function getAtlasSnapshot() {
  const db = await getDb();
  if (!db) return null;
  const [claims, workstreams, publications, datasets, timeline, nodes, bridges, releases] = await Promise.all([
    db.select().from(atlasClaims),
    db.select().from(atlasWorkstreams),
    db.select().from(atlasPublications),
    db.select().from(atlasDatasets),
    db.select().from(atlasTimeline),
    db.select().from(theoryNodes),
    db.select().from(theoryBridges),
    db.select().from(atlasReleaseState).where(eq(atlasReleaseState.isCurrent, 1)).orderBy(desc(atlasReleaseState.createdAt)).limit(1),
  ]);
  return { claims, workstreams, publications, datasets, timeline, nodes, bridges, release: releases[0] ?? null };
}

export async function listAtlasClaims(input?: { status?: string; search?: string; limit?: number }) {
  const db = await getDb();
  if (!db) return [];
  const predicates = [];
  if (input?.status) predicates.push(eq(atlasClaims.status, input.status));
  if (input?.search) {
    const term = `%${input.search}%`;
    predicates.push(or(like(atlasClaims.id, term), like(atlasClaims.domain, term), like(atlasClaims.title, term), like(atlasClaims.summary, term)));
  }
  const query = db.select().from(atlasClaims);
  if (predicates.length > 0) query.where(and(...predicates));
  return query.orderBy(atlasClaims.id).limit(Math.min(input?.limit ?? 100, 100));
}

export async function listAtlasDatasets(input?: { search?: string; limit?: number }) {
  const db = await getDb();
  if (!db) return [];
  const query = db.select().from(atlasDatasets);
  if (input?.search) query.where(or(like(atlasDatasets.name, `%${input.search}%`), like(atlasDatasets.scope, `%${input.search}%`)));
  return query.orderBy(atlasDatasets.id).limit(Math.min(input?.limit ?? 50, 50));
}

export async function getCurrentAtlasRelease() {
  const db = await getDb();
  if (!db) return undefined;
  const result = await db.select().from(atlasReleaseState).where(eq(atlasReleaseState.isCurrent, 1)).orderBy(desc(atlasReleaseState.createdAt)).limit(1);
  return result[0];
}

export async function listPublicResearchFiles() {
  const db = await getDb();
  if (!db) return [];
  return db.select().from(researchFiles).where(eq(researchFiles.visibility, "public")).orderBy(desc(researchFiles.createdAt));
}

export async function getResearchFileById(id: number, includePrivate = false) {
  const db = await getDb();
  if (!db) return undefined;
  const conditions = includePrivate
    ? eq(researchFiles.id, id)
    : and(eq(researchFiles.id, id), eq(researchFiles.visibility, "public"));
  const result = await db.select().from(researchFiles).where(conditions).limit(1);
  return result[0];
}

export async function createResearchFile(input: typeof researchFiles.$inferInsert) {
  const db = await getDb();
  if (!db) throw new Error("Database is not available");
  const result = await db.insert(researchFiles).values(input);
  const id = Number(result[0].insertId);
  return getResearchFileById(id, true);
}

export async function updateAtlasClaim(id: string, patch: Partial<Pick<typeof atlasClaims.$inferInsert, "status" | "tone" | "domain" | "title" | "summary" | "source" | "limitation">>) {
  const db = await getDb();
  if (!db) throw new Error("Database is not available");
  await db.update(atlasClaims).set(patch).where(eq(atlasClaims.id, id));
  const result = await db.select().from(atlasClaims).where(eq(atlasClaims.id, id)).limit(1);
  return result[0];
}

export async function createReleaseSnapshot(input: typeof atlasReleaseState.$inferInsert) {
  const db = await getDb();
  if (!db) throw new Error("Database is not available");
  await db.update(atlasReleaseState).set({ isCurrent: 0 }).where(eq(atlasReleaseState.isCurrent, 1));
  await db.insert(atlasReleaseState).values({ ...input, isCurrent: 1 });
  return getCurrentAtlasRelease();
}

export async function listAllResearchFiles() {
  const db = await getDb();
  if (!db) return [];
  return db.select().from(researchFiles).orderBy(desc(researchFiles.createdAt));
}

export async function listAdminUsers() {
  const db = await getDb();
  if (!db) return [];
  return db.select({ id: users.id, name: users.name, email: users.email, role: users.role, lastSignedIn: users.lastSignedIn }).from(users).orderBy(desc(users.lastSignedIn)).limit(100);
}

export async function updateUserRole(id: number, role: "user" | "admin") {
  const db = await getDb();
  if (!db) throw new Error("Database is not available");
  await db.update(users).set({ role }).where(eq(users.id, id));
  const result = await db.select({ id: users.id, name: users.name, email: users.email, role: users.role, lastSignedIn: users.lastSignedIn }).from(users).where(eq(users.id, id)).limit(1);
  return result[0];
}

export async function createAdminAuditLog(input: typeof adminAuditLog.$inferInsert) {
  const db = await getDb();
  if (!db) throw new Error("Database is not available");
  await db.insert(adminAuditLog).values(input);
}

export async function listAdminAuditLog() {
  const db = await getDb();
  if (!db) return [];
  return db.select().from(adminAuditLog).orderBy(desc(adminAuditLog.createdAt)).limit(100);
}
