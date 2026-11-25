# External sources captured during Res-Nova audit

This file records outside evidence used in the 2026-11-25 audit. It is a source ledger, not a theory instruction file.

## AeST reference theory

The primary Skordis–Złośnik paper proposes a relativistic MOND theory, reports agreement with the observed CMB and matter power spectra on linear cosmological scales, and states that its action expanded to second order is free of ghost instabilities. Those claims establish the scope of the published reference construction. They do not establish Res Nova's selected branch, its nonspherical external-field response, a covariant screening operator, or the repository's unresolved 5D closure. [1]

## SPARC data scope

The primary SPARC paper introduces a public sample of 175 nearby galaxies with Spitzer 3.6 μm photometry and high-quality rotation curves. It describes the sample as a test bed for galaxy-formation models and reports mass-model properties. This supports the repository's use of SPARC as an empirical galaxy-dynamics dataset, but it does not independently validate Res Nova's interpolation law or its covariant completion. [2]

## Vercel operations

Vercel's official limits documentation states that Hobby accounts are limited to 100 deployments per hour and 100 deployments per day, and that rate-limit responses require waiting for capacity to reset or refill. It also distinguishes deployments/builds from static-file hosting. This supports treating issue #185 as an account/project operations blocker rather than a source-code or physics failure. The audit did not perform an external production deployment or alter the user's Vercel account. [3]

## GitHub checks

GitHub's official documentation distinguishes detailed Checks from simpler commit statuses and explains that a completed check receives a conclusion such as success, failure, skipped, or timed out. A successful check therefore proves only the scope of that check; it is not evidence of empirical theory validation. This is the rule used throughout the audit when interpreting CI and deployment receipts. [4]

## Sources

[1]: https://arxiv.org/abs/2007.00082 "A new relativistic theory for Modified Newtonian Dynamics"
[2]: https://arxiv.org/abs/1606.09251 "SPARC: Mass Models for 175 Disk Galaxies with Spitzer Photometry and Accurate Rotation Curves"
[3]: https://vercel.com/docs/limits "Vercel limits"
[4]: https://docs.github.com/en/pull-requests/reference/status-checks "GitHub status checks"
