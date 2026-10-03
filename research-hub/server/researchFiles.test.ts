import { describe, expect, it } from "vitest";
import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";

function context(role: "user" | "admin"): TrpcContext {
  return {
    user: {
      id: 7,
      openId: `research-${role}`,
      email: `${role}@example.com`,
      name: role,
      loginMethod: "test",
      role,
      createdAt: new Date(),
      updatedAt: new Date(),
      lastSignedIn: new Date(),
    },
    req: { protocol: "https", headers: {} } as TrpcContext["req"],
    res: {} as TrpcContext["res"],
  };
}

describe("researchFiles", () => {
  it("does not allow a regular user to upload a research artifact", async () => {
    const caller = appRouter.createCaller(context("user"));
    await expect(caller.researchFiles.upload({
      title: "Attempted upload",
      category: "dataset",
      fileName: "data.csv",
      mimeType: "text/csv",
      base64: "ZGF0YQ==",
      visibility: "public",
    })).rejects.toMatchObject({ code: "FORBIDDEN" });
  });

  it("does not allow a regular user to manage curated claims", async () => {
    const caller = appRouter.createCaller(context("user"));
    await expect(caller.admin.claims.list()).rejects.toMatchObject({ code: "FORBIDDEN" });
  });

  it("does not allow a regular user to manage roles or read audit history", async () => {
    const caller = appRouter.createCaller(context("user"));
    await expect(caller.admin.users.list()).rejects.toMatchObject({ code: "FORBIDDEN" });
    await expect(caller.admin.audit.list()).rejects.toMatchObject({ code: "FORBIDDEN" });
  });

  it("exposes a public catalog procedure without requiring authentication", async () => {
    const caller = appRouter.createCaller({
      ...context("user"),
      user: undefined,
    });
    const files = await caller.researchFiles.listPublic();
    expect(Array.isArray(files)).toBe(true);
  });

  it("exposes bounded atlas queries for claims, datasets, release, and guide search", async () => {
    const caller = appRouter.createCaller({ ...context("user"), user: undefined });
    const [claims, datasets, release, search] = await Promise.all([
      caller.atlas.claims({ search: "SPARC", limit: 5 }),
      caller.atlas.datasets({ search: "SPARC", limit: 5 }),
      caller.atlas.release(),
      caller.atlas.search({ query: "SPARC", limit: 5 }),
    ]);
    expect(claims.length).toBeLessThanOrEqual(5);
    expect(datasets.length).toBeLessThanOrEqual(5);
    expect(release === undefined || typeof release.commit === "string").toBe(true);
    expect(search.claims.length).toBeLessThanOrEqual(5);
    expect(search.datasets.length).toBeLessThanOrEqual(5);
    expect(Array.isArray(search.files)).toBe(true);
  });
});
