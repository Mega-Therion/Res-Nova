#!/usr/bin/env python3
"""
Sync Res-Nova benchmark data, verification certificates, and manuscript artifacts
to Hugging Face dataset repository: ChyRho/res-nova.
"""

import os
import sys
from pathlib import Path

REPO_ID = "ChyRho/res-nova"
REPO_ROOT = Path(__file__).resolve().parent.parent

def get_token():
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if not token:
        env_file = Path.home() / ".chyren" / "one-true.env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("HF_TOKEN=") or line.startswith("HUGGINGFACE_TOKEN="):
                    token = line.split("=", 1)[1].strip()
                    break
    if not token:
        raise RuntimeError("HF_TOKEN not found in environment or ~/.chyren/one-true.env")
    return token

# Directories mirrored to the dataset. The card's "Structure" section is generated
# from this list so it can never advertise a directory that is not uploaded (the
# card previously listed a `Lean/` directory that has never existed).
DIRS_TO_UPLOAD = {
    "02_galaxy_dynamics": "SPARC-derived measurement outputs, fits and a0 extractions (raw SPARC tables are not vendored; see the directory README).",
    "05_lean_formalization": "Lean 4 sources and the proof gate (`verify_all_proofs.sh`). Machine-checked means the mathematics compiles; see each module's docstring for what it does and does not establish physically.",
    "mvpc_manifests": "Claim manifests for the MVPC-X claim judge.",
    "reproducibility": "Scripts reproducing published figures and tables.",
}

ROOT_FILES = ["VERSION", "CHANGELOG.md", ".zenodo.json", "references.bib"]

# Build artifacts that must never be mirrored (a local run would otherwise push
# the multi-GB Mathlib cache under 05_lean_formalization/.lake).
IGNORE_PATTERNS = [".lake/**", "**/.lake/**", "**/__pycache__/**", "*.olean", "*.ilean"]


def generate_hf_readme():
    structure = "\n".join(f"- `{d}/`: {desc}" for d, desc in DIRS_TO_UPLOAD.items())
    return """---
license: cc-by-4.0
pretty_name: "Res Nova: Geometrically Ordered Dynamics & SPARC Benchmark"
tags:
  - modified-gravity
  - formal-verification
  - lean4
  - sparc
  - cosmology
  - astrophysics
---

# Res Nova: Empirical Benchmark, Verification Package & Theory Atlas

Reproducibility and verification package for **Res Nova**, mirrored from the GitHub
repository (the source of truth). Epistemic status is tracked claim-by-claim in
`assurance/claims.json` and `CURRENT_STATE_READ_THIS_FIRST.md` on GitHub; read those
before relying on any result here.

- **SPARC benchmark**: rotation-curve fits and the a0 extraction under the live
  interpolating function mu_std(x) = x/sqrt(1+x^2). The anchor a0 = cH0/(2*pi) is a
  declared normalisation, not a derivation: horizon-temperature (KMS) matching gives
  a = cH, with the 2*pi cancelling.
- **Solar system (status, not a pass)**: the isolated-Sun monopole deviation of mu_std is
  ~1e-12 at Saturn, but with the Milky Way external field the Cassini quadrupole Q2
  **excludes bare mu_std at ~4.6 sigma** at the derived a0. A screening mechanism is
  required; the working one is phenomenological and has no covariant realization yet.
- **Formal verification**: Lean 4 modules checked by `05_lean_formalization/verify_all_proofs.sh`
  with no `sorry` and only the standard axioms. That certifies the mathematics, not the
  physical identification each theorem is given.
- **Claim manifests**: MVPC-X manifests for the O-series claims.

---

### 🔗 Canonical Links & Provenance

- **GitHub Source of Truth**: [https://github.com/Mega-Therion/Res-Nova](https://github.com/Mega-Therion/Res-Nova)
- **Interactive Research Atlas**: [https://resnova-hub-f4ucvy3e.manus.space](https://resnova-hub-f4ucvy3e.manus.space)
- **Zenodo Release Archive**: [https://doi.org/10.5281/zenodo.21969121](https://doi.org/10.5281/zenodo.21969121)
- **Author**: R.W. Yett ([ORCID: 0009-0001-1303-7190](https://orcid.org/0009-0001-1303-7190))
- **LinkedIn**: [R.W. Yett](https://www.linkedin.com/in/r-w-yett/)
- **X (Twitter)**: [@_ChyRho_](https://x.com/_chyrho_)

---

### 📂 Structure

""" + structure + """
- `VERSION`, `CHANGELOG.md`, `.zenodo.json`, `references.bib`: release metadata.
"""

def main():
    from huggingface_hub import HfApi  # deferred: the card test imports this module without it

    token = get_token()
    api = HfApi(token=token)
    print(f"Ensuring repository {REPO_ID} exists...")
    api.create_repo(repo_id=REPO_ID, repo_type="dataset", exist_ok=True)

    # 1. Upload dataset card README.md
    print("Uploading Hugging Face dataset card README.md...")
    api.upload_file(
        path_or_fileobj=generate_hf_readme().encode("utf-8"),
        path_in_repo="README.md",
        repo_id=REPO_ID,
        repo_type="dataset",
        commit_message="docs: update dataset card from scripts/sync_huggingface.py"
    )

    # 2. Upload directories
    for d in DIRS_TO_UPLOAD:
        folder_path = REPO_ROOT / d
        if folder_path.exists():
            print(f"Uploading directory {d}...")
            api.upload_folder(
                folder_path=str(folder_path),
                path_in_repo=d,
                repo_id=REPO_ID,
                repo_type="dataset",
                ignore_patterns=IGNORE_PATTERNS,
                commit_message=f"sync: upload {d} to Hugging Face dataset"
            )

    # 3. Upload key root metadata files
    for rf in ROOT_FILES:
        fp = REPO_ROOT / rf
        if fp.exists():
            print(f"Uploading {rf}...")
            api.upload_file(
                path_or_fileobj=str(fp),
                path_in_repo=rf,
                repo_id=REPO_ID,
                repo_type="dataset",
                commit_message=f"sync: upload {rf}"
            )

    print(f"Successfully synced Res-Nova to https://huggingface.co/datasets/{REPO_ID}")

if __name__ == "__main__":
    main()
