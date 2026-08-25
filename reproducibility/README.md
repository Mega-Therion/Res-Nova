# Res-Nova reproducibility pipeline

Public, receipt-producing verification. This directory is the new canonical home for run envelopes, schemas, profiles, and incidents.

Historical `VERIFICATION_RUN_00x` directories remain immutable. They are indexed in `LEGACY_RUN_INDEX.json` and are not rewritten.

## What this is not

A passing static preflight is not a proved claim, not an empirical result, and not an independent reproduction.

## Entry points

```bash
python3 scripts/repro/preflight.py --help
python3 scripts/repro/preflight.py --legacy-index reproducibility/LEGACY_RUN_INDEX.json
```

Exit codes follow the integration contract: `0` pass, `10` preflight/schema, `20` integrity, `50` lock drift, `70` visibility.
