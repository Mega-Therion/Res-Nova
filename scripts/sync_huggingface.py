#!/usr/bin/env python3
"""
Sync Res-Nova benchmark data, verification certificates, and manuscript artifacts
to Hugging Face dataset repository: ChyRho/res-nova.
"""

import os
import sys
from pathlib import Path
from huggingface_hub import HfApi

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

def generate_hf_readme():
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

This dataset contains the complete reproducibility, empirical verification package, and formal mathematical certificates for **Res Nova v1.9.0**:

- **SPARC 175-Galaxy Benchmark**: 3,391 empirical rotation curve data points with distance-corrected $a_0 = cH_0 / (2\\pi)$ validation.
- **Variational Action Closure**: Exact $\\mu_{\\text{std}}(x) = x/\\sqrt{1+x^2}$ action closure clearing Cassini $Q_2$ quadrupole bounds and planetary precession.
- **Formal Verification Package**: 100% verified Lean 4 mathematical modules (0 `sorry` / bypasses).
- **Audit Manifests & Ledgers**: Machine-checkable SHA-256 manifests across all empirical and theoretical claims.

---

### 🔗 Canonical Links & Provenance

- **GitHub Source of Truth**: [https://github.com/Mega-Therion/Res-Nova](https://github.com/Mega-Therion/Res-Nova)
- **Interactive Research Atlas**: [https://resnova-hub-f4ucvy3e.manus.space](https://resnova-hub-f4ucvy3e.manus.space)
- **Zenodo Release Archive**: [https://doi.org/10.5281/zenodo.21969121](https://doi.org/10.5281/zenodo.21969121)
- **Author**: Ryan W. Yett ([ORCID: 0009-0001-1303-7190](https://orcid.org/0009-0001-1303-7190))
- **LinkedIn**: [R.W. Yett](https://www.linkedin.com/in/r-w-yett-152085293/)
- **X (Twitter)**: [@_ChyRho_](https://x.com/_chyrho_)

---

### 📂 Structure

- `02_galaxy_dynamics/`: Raw and processed SPARC catalog data, rotational velocities, and $a_0$ measurement outputs.
- `mvpc_manifests/`: Multi-variable proof-carrying manifests verifying claims $O_1$ through $O_5$.
- `Lean/`: Machine-checked Lean 4 modules proving core geometric and algebraic lemmas.
- `reproducibility/`: Python, R, and bash automated pipelines reproducing every published figure and table.
- `CHANGELOG.md` & `VERSION`: Semantic versioning and changelog trail.
"""

def main():
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
        commit_message="docs: update dataset card with cross-platform links and Res Nova v1.9.0 metadata"
    )

    # 2. Upload directories
    dirs_to_upload = [
        "02_galaxy_dynamics",
        "mvpc_manifests",
        "Lean",
        "reproducibility",
    ]

    for d in dirs_to_upload:
        folder_path = REPO_ROOT / d
        if folder_path.exists():
            print(f"Uploading directory {d}...")
            api.upload_folder(
                folder_path=str(folder_path),
                path_in_repo=d,
                repo_id=REPO_ID,
                repo_type="dataset",
                commit_message=f"sync: upload {d} to Hugging Face dataset"
            )

    # 3. Upload key root metadata files
    root_files = [
        "VERSION",
        "CHANGELOG.md",
        ".zenodo.json",
        "references.bib",
    ]
    for rf in root_files:
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
