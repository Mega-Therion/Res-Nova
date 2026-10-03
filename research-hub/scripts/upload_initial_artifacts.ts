import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { basename, extname } from "node:path";
import { createResearchFile, listAllResearchFiles } from "../server/db";
import { storagePut } from "../server/storage";

const artifacts = [
  {
    path: "/home/ubuntu/res-nova-audit/RES_NOVA_CANONICAL_EDITION.pdf",
    title: "Res Nova canonical edition",
    category: "publication PDF",
    description: "Canonical-edition PDF from the audited Res Nova research corpus.",
  },
  {
    path: "/home/ubuntu/res-nova-audit/res_nova_manuscript.pdf",
    title: "Res Nova manuscript",
    category: "publication PDF",
    description: "Manuscript PDF associated with the current publication-readiness corpus.",
  },
  {
    path: "/home/ubuntu/res-nova-audit/VERIFICATION_RUN_002/02_sparc/SPARC_175_CANONICAL_382_RESIDUALS.csv",
    title: "SPARC canonical residuals",
    category: "dataset supplement",
    description: "Point-level residual table from the canonical SPARC verification run 002.",
  },
  {
    path: "/home/ubuntu/res-nova-audit/VERIFICATION_RUN_002/02_sparc/SPARC_175_CANONICAL_382_MANIFEST.json",
    title: "SPARC canonical manifest",
    category: "dataset supplement",
    description: "Machine-readable manifest for the canonical 175-galaxy SPARC verification run.",
  },
  {
    path: "/home/ubuntu/res-nova-audit/VERIFICATION_RUN_003/02_sparc/SPARC_DERIVED_CV_REPORT.json",
    title: "SPARC derived cross-validation report",
    category: "dataset supplement",
    description: "Derived cross-validation report from the third SPARC verification run.",
  },
];

function mimeFor(path: string) {
  const extension = extname(path).toLowerCase();
  if (extension === ".pdf") return "application/pdf";
  if (extension === ".csv") return "text/csv";
  if (extension === ".json") return "application/json";
  return "application/octet-stream";
}

async function main() {
  const existing = await listAllResearchFiles();
  let uploaded = 0;
  let skipped = 0;
  for (const artifact of artifacts) {
    const fileName = basename(artifact.path);
    if (existing.some((file) => file.fileName === fileName)) {
      console.log(`Skipping existing artifact: ${fileName}`);
      skipped += 1;
      continue;
    }
    const bytes = await readFile(artifact.path);
    const checksum = createHash("sha256").update(bytes).digest("hex");
    const { key, url } = await storagePut(`initial-release/${fileName}`, bytes, mimeFor(fileName));
    await createResearchFile({
      title: artifact.title,
      category: artifact.category,
      description: artifact.description,
      fileName,
      mimeType: mimeFor(fileName),
      sizeBytes: bytes.byteLength,
      storageKey: key,
      publicUrl: url,
      checksum,
      visibility: "public",
    });
    console.log(`Uploaded ${fileName} -> ${url}`);
    uploaded += 1;
  }
  console.log(`Initial artifact import complete: ${uploaded} uploaded, ${skipped} skipped`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
