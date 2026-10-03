import { existsSync, readFileSync, statSync } from "node:fs";

const required = [
  "client/src/data/sparc.ts",
  "client/src/data/research.ts",
  "client/public/downloads/sparc-rotation-curves-slice.csv",
  "client/public/downloads/sparc-rotation-curves-slice.svg",
];
for (const file of required) {
  if (!existsSync(file) || statSync(file).size === 0) throw new Error(`Missing or empty release artifact: ${file}`);
}
const source = readFileSync("client/src/data/sparc.ts", "utf8");
const csv = readFileSync("client/public/downloads/sparc-rotation-curves-slice.csv", "utf8");
const research = readFileSync("client/src/data/research.ts", "utf8");
const galaxyCount = (source.match(/\"name\":/g) ?? []).length;
const pointCount = csv.trim().split("\n").filter((line) => !line.startsWith("#")).length - 1;
if (galaxyCount !== 175) throw new Error(`Expected 175 galaxies, found ${galaxyCount}`);
if (pointCount < 3000) throw new Error(`Expected at least 3000 exported points, found ${pointCount}`);
for (const name of ["NGC2403", "NGC3198", "DDO154"]) {
  if (!source.includes(`\"name\": \"${name}\"`)) throw new Error(`Missing featured galaxy ${name}`);
}
for (const token of ["10.5281/zenodo.16284118", "CC BY 4.0", "claimRegistry", "releaseManifest"]) {
  if (!source.includes(token) && !research.includes(token)) throw new Error(`Missing provenance/release token ${token}`);
}
console.log(`release assets valid: ${galaxyCount} galaxies, ${pointCount} points, claim registry linked`);
