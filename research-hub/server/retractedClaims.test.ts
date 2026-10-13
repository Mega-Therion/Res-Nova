import { describe, expect, it } from "vitest";
import fs from "fs";
import path from "path";
import { retractedClaims } from "@/data/research";

// The hub's retracted-claim list must match the registry's `retracted` states exactly.
describe("retracted claims", () => {
  it("matches assurance/claims.json", () => {
    const registryPath = path.resolve(import.meta.dirname, "..", "..", "assurance", "claims.json");
    const raw = JSON.parse(fs.readFileSync(registryPath, "utf8"));
    const items: Array<{ id: string; state: string }> = Array.isArray(raw)
      ? raw
      : Array.isArray(raw.claims)
        ? raw.claims
        : Object.values(raw.claims ?? raw);
    const registry = items.filter(c => c.state === "retracted").map(c => c.id).sort();
    const hub = retractedClaims.map(c => c.id).sort();
    expect(hub).toEqual(registry);
  });
});
