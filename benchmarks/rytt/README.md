# RYTT benchmark fixtures from the Res-Nova manuscript (issue #48)

`manuscript_passages.json` holds six passages of `res_nova_manuscript.tex` (abstract, introduction, epistemic policy, Lean scope, limitations, conclusion). Each passage carries its exact source lines and commit, and its metrics from the canonical RYTT encoder: `rytt-core-benchmark`, built from RYTT-Sovereign-Semiotics at `bdbc971`.

Per passage: source characters, PUA stream length (RYTT tokens), token savings, and whether decoding recovers the exact text. All six recover exactly.

RYTT stays the encoder and Res-Nova stays the scientific corpus. Nothing here merges the two. The passages are benchmark text, not claims; for the physics status of anything they say, read `CURRENT_STATE_READ_THIS_FIRST.md`.

To regenerate, feed the `corpus`/`source` pairs as a JSON array to `rytt-core-benchmark` on stdin.
