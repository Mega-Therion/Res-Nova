import { z } from "zod";
import { COOKIE_NAME } from "@shared/const";
import { TRPCError } from "@trpc/server";
import { getSessionCookieOptions } from "./_core/cookies";
import { adminProcedure, publicProcedure, router } from "./_core/trpc";
import { createAdminAuditLog, createReleaseSnapshot, createResearchFile, getAtlasSnapshot, getCurrentAtlasRelease, getResearchFileById, listAdminAuditLog, listAdminUsers, listAllResearchFiles, listAtlasClaims, listAtlasDatasets, listPublicResearchFiles, updateAtlasClaim, updateUserRole } from "./db";
import { storagePut } from "./storage";
import { systemRouter } from "./_core/systemRouter";

export const appRouter = router({
  system: systemRouter,
  auth: router({
    me: publicProcedure.query(opts => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return { success: true } as const;
    }),
  }),
  atlas: router({
    snapshot: publicProcedure.query(async () => {
      const snapshot = await getAtlasSnapshot();
      if (!snapshot) throw new TRPCError({ code: "INTERNAL_SERVER_ERROR", message: "Atlas database is not available" });
      return snapshot;
    }),
    claims: publicProcedure.input(z.object({ status: z.string().max(24).optional(), search: z.string().max(160).optional(), limit: z.number().int().min(1).max(100).default(100) }).optional()).query(({ input }) => listAtlasClaims(input)),
    datasets: publicProcedure.input(z.object({ search: z.string().max(160).optional(), limit: z.number().int().min(1).max(50).default(50) }).optional()).query(({ input }) => listAtlasDatasets(input)),
    release: publicProcedure.query(() => getCurrentAtlasRelease()),
    search: publicProcedure.input(z.object({ query: z.string().min(1).max(160), limit: z.number().int().min(1).max(20).default(10) })).query(async ({ input }) => {
      const [matchedClaims, matchedDatasets, files] = await Promise.all([
        listAtlasClaims({ search: input.query, limit: input.limit }),
        listAtlasDatasets({ search: input.query, limit: input.limit }),
        listPublicResearchFiles(),
      ]);
      const normalized = input.query.toLowerCase();
      return {
        claims: matchedClaims,
        datasets: matchedDatasets,
        files: files.filter((file) => `${file.title} ${file.category} ${file.fileName} ${file.description ?? ""}`.toLowerCase().includes(normalized)).slice(0, input.limit),
      };
    }),
  }),
  researchFiles: router({
    listPublic: publicProcedure.query(() => listPublicResearchFiles()),
    getPublic: publicProcedure.input(z.object({ id: z.number().int().positive() })).query(({ input }) => getResearchFileById(input.id)),
    upload: adminProcedure
      .input(z.object({
        title: z.string().min(1).max(240),
        category: z.string().min(1).max(80),
        description: z.string().max(5000).optional(),
        fileName: z.string().min(1).max(240),
        mimeType: z.string().min(1).max(160),
        base64: z.string().min(1).max(20_000_000),
        checksum: z.string().max(128).optional(),
        visibility: z.enum(["public", "private"]).default("public"),
      }))
      .mutation(async ({ ctx, input }) => {
        const safeName = input.fileName.replace(/[^a-zA-Z0-9._-]/g, "-");
        const raw = Buffer.from(input.base64, "base64");
        if (raw.byteLength === 0) throw new TRPCError({ code: "BAD_REQUEST", message: "The uploaded file is empty" });
        if (raw.byteLength > 15 * 1024 * 1024) throw new TRPCError({ code: "PAYLOAD_TOO_LARGE", message: "Research files must be 15 MB or smaller" });
        const { key, url } = await storagePut(`research-files/${crypto.randomUUID()}-${safeName}`, raw, input.mimeType);
        return createResearchFile({
          title: input.title,
          category: input.category,
          description: input.description,
          fileName: input.fileName,
          mimeType: input.mimeType,
          sizeBytes: raw.byteLength,
          storageKey: key,
          publicUrl: url,
          checksum: input.checksum,
          visibility: input.visibility,
          uploadedBy: ctx.user.id,
        });
      }),
  }),
  admin: router({
    claims: router({
      list: adminProcedure.query(() => listAtlasClaims({ limit: 100 })),
      update: adminProcedure.input(z.object({
        id: z.string().min(1).max(80),
        status: z.string().min(1).max(24).optional(),
        tone: z.string().min(1).max(24).optional(),
        domain: z.string().min(1).max(120).optional(),
        title: z.string().min(1).max(500).optional(),
        summary: z.string().min(1).max(5000).optional(),
        source: z.string().min(1).max(2000).optional(),
        limitation: z.string().min(1).max(2000).optional(),
      }).refine((input) => Object.keys(input).some((key) => key !== "id"), "At least one claim field must be updated")).mutation(async ({ ctx, input }) => {
        const { id, ...patch } = input;
        const before = (await listAtlasClaims({ search: id, limit: 1 }))[0];
        const updated = await updateAtlasClaim(id, patch);
        await createAdminAuditLog({ actorId: ctx.user.id, action: "update", entityType: "claim", entityId: id, summary: `Updated curated claim ${id}`, beforeJson: JSON.stringify(before ?? null), afterJson: JSON.stringify(updated ?? null) });
        return updated;
      }),
    }),
    release: router({
      current: adminProcedure.query(() => getCurrentAtlasRelease()),
      create: adminProcedure.input(z.object({
        version: z.string().min(1).max(80),
        researchRelease: z.string().min(1).max(160),
        commit: z.string().min(1).max(80),
        note: z.string().min(1).max(5000),
        links: z.object({ github: z.string().url(), zenodo: z.string().url(), orcid: z.string().url(), claimRegistry: z.string().url(), releaseManifest: z.string().url() }),
      })).mutation(async ({ ctx, input }) => {
        const before = await getCurrentAtlasRelease();
        const created = await createReleaseSnapshot({ version: input.version, researchRelease: input.researchRelease, commit: input.commit, note: input.note, linksJson: JSON.stringify(input.links), isCurrent: 1 });
        await createAdminAuditLog({ actorId: ctx.user.id, action: "publish", entityType: "release", entityId: input.commit, summary: `Published release snapshot ${input.version} at ${input.commit}`, beforeJson: JSON.stringify(before ?? null), afterJson: JSON.stringify(created ?? null) });
        return created;
      }),
    }),
    files: router({
      list: adminProcedure.query(() => listAllResearchFiles()),
    }),
    users: router({
      list: adminProcedure.query(() => listAdminUsers()),
      setRole: adminProcedure.input(z.object({ id: z.number().int().positive(), role: z.enum(["user", "admin"]) })).mutation(async ({ ctx, input }) => {
        if (input.id === ctx.user.id && input.role === "user") throw new TRPCError({ code: "BAD_REQUEST", message: "You cannot remove your own administrator role." });
        const before = (await listAdminUsers()).find((user) => user.id === input.id);
        const updated = await updateUserRole(input.id, input.role);
        await createAdminAuditLog({ actorId: ctx.user.id, action: "role_change", entityType: "user", entityId: String(input.id), summary: `Changed role for user ${input.id} to ${input.role}`, beforeJson: JSON.stringify(before ?? null), afterJson: JSON.stringify(updated ?? null) });
        return updated;
      }),
    }),
    audit: router({
      list: adminProcedure.query(() => listAdminAuditLog()),
    }),
  }),
});

export type AppRouter = typeof appRouter;
