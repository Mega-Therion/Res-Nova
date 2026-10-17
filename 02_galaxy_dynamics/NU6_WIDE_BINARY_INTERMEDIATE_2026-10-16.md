# ν₆ on the intermediate wide-binary cut

**Pre-registration:** `PREREG_NU6_WIDE_BINARY_INTERMEDIATE_2026-10-16.md`, commit `dbf28bc`. Runner `f800e17`. No model χ² was computed.

**Tier:** the verdict string is `[D]`, from `nu6_wide_binary_intermediate.py` into `NU6_WIDE_BINARY_INTERMEDIATE.json`.

**Verdict, from that JSON.** The cut is not intermediate, and ν₆ is not excluded. Counts are clean 14542, intermediate 18053, loose 20156, so the count sits strictly between the two published samples. `nested` is false. The pre-registration says that a failed nest means no exclusion and ν₆ stays standing.

The nest fails because `wide_binary_fish.prepare` rebuilds the main-sequence locus inside each cut, so the color cut is not a fixed mask. A count of the same prepared rows, after the JSON was written, finds 35 of 14542 clean pairs absent from the intermediate sample and 26 of 18053 intermediate pairs absent from the loose sample. That count is not a χ². a₀ was not retuned.
