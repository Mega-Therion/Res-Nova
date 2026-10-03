import { int, mysqlEnum, mysqlTable, text, timestamp, varchar } from "drizzle-orm/mysql-core";

export const users = mysqlTable("users", {
  id: int("id").autoincrement().primaryKey(),
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export const atlasClaims = mysqlTable("atlas_claims", {
  id: varchar("id", { length: 80 }).primaryKey(),
  status: varchar("status", { length: 24 }).notNull(),
  tone: varchar("tone", { length: 24 }).notNull(),
  domain: varchar("domain", { length: 120 }).notNull(),
  title: text("title").notNull(),
  summary: text("summary").notNull(),
  source: text("source").notNull(),
  limitation: text("limitation").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export const atlasWorkstreams = mysqlTable("atlas_workstreams", {
  id: varchar("id", { length: 80 }).primaryKey(),
  label: varchar("label", { length: 160 }).notNull(),
  short: text("short").notNull(),
  status: varchar("status", { length: 24 }).notNull(),
  progress: int("progress").notNull(),
  color: varchar("color", { length: 16 }).notNull(),
});

export const atlasPublications = mysqlTable("atlas_publications", {
  id: int("id").autoincrement().primaryKey(),
  type: varchar("type", { length: 80 }).notNull(),
  year: varchar("year", { length: 12 }).notNull(),
  title: text("title").notNull(),
  summary: text("summary").notNull(),
  href: text("href").notNull(),
  tag: varchar("tag", { length: 80 }).notNull(),
});

export const atlasDatasets = mysqlTable("atlas_datasets", {
  id: int("id").autoincrement().primaryKey(),
  name: varchar("name", { length: 160 }).notNull(),
  scope: text("scope").notNull(),
  artifact: text("artifact").notNull(),
  provenance: text("provenance").notNull(),
  color: varchar("color", { length: 16 }).notNull(),
});

export const atlasTimeline = mysqlTable("atlas_timeline", {
  id: int("id").autoincrement().primaryKey(),
  date: varchar("date", { length: 40 }).notNull(),
  title: text("title").notNull(),
  body: text("body").notNull(),
});

export const theoryNodes = mysqlTable("theory_nodes", {
  id: varchar("id", { length: 80 }).primaryKey(),
  number: varchar("number", { length: 8 }).notNull(),
  title: varchar("title", { length: 120 }).notNull(),
  detail: text("detail").notNull(),
  status: varchar("status", { length: 24 }).notNull(),
});

export const theoryBridges = mysqlTable("theory_bridges", {
  id: varchar("id", { length: 80 }).primaryKey(),
  label: varchar("label", { length: 160 }).notNull(),
  description: text("description").notNull(),
  fromNode: varchar("fromNode", { length: 80 }).notNull(),
  toNode: varchar("toNode", { length: 80 }).notNull(),
});

export const atlasReleaseState = mysqlTable("atlas_release_state", {
  id: int("id").autoincrement().primaryKey(),
  version: varchar("version", { length: 80 }).notNull(),
  researchRelease: varchar("researchRelease", { length: 160 }).notNull(),
  commit: varchar("commit", { length: 80 }).notNull(),
  note: text("note").notNull(),
  linksJson: text("linksJson").notNull(),
  isCurrent: int("isCurrent").notNull().default(1),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export const researchFiles = mysqlTable("research_files", {
  id: int("id").autoincrement().primaryKey(),
  title: varchar("title", { length: 240 }).notNull(),
  category: varchar("category", { length: 80 }).notNull(),
  description: text("description"),
  fileName: varchar("fileName", { length: 240 }).notNull(),
  mimeType: varchar("mimeType", { length: 160 }).notNull(),
  sizeBytes: int("sizeBytes").notNull(),
  storageKey: text("storageKey").notNull().unique(),
  publicUrl: text("publicUrl").notNull(),
  checksum: varchar("checksum", { length: 128 }),
  visibility: mysqlEnum("visibility", ["public", "private"]).default("public").notNull(),
  uploadedBy: int("uploadedBy"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export const adminAuditLog = mysqlTable("admin_audit_log", {
  id: int("id").autoincrement().primaryKey(),
  actorId: int("actorId"),
  action: varchar("action", { length: 80 }).notNull(),
  entityType: varchar("entityType", { length: 80 }).notNull(),
  entityId: varchar("entityId", { length: 160 }).notNull(),
  summary: text("summary").notNull(),
  beforeJson: text("beforeJson"),
  afterJson: text("afterJson"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;
export type AtlasClaim = typeof atlasClaims.$inferSelect;
export type ResearchFile = typeof researchFiles.$inferSelect;
export type AdminAuditLog = typeof adminAuditLog.$inferSelect;
