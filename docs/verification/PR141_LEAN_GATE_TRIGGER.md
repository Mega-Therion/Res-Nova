# PR #141 Lean-gate verification branch

This branch exists only to obtain the repository's scheduled/push-triggered Lean gate for the proposed derivative theorem in PR #141.

Source PR head at branch creation: `5e89c532b222a24822a47c111c08b80855063cb5`.

The PR workflow intentionally skips `lean-gate` for all pull requests, so its green local Python gate cannot establish that `F_dual_hasDerivAt` compiles. The branch name matches the existing `diamond-standard/**` push trigger in `.github/workflows/verify.yml`.

No new physics claim is made by this file. Keep CLM-01 in `proposed` and the retired D1.2 claim in `[X]` until the Lean job's actual result is inspected.
