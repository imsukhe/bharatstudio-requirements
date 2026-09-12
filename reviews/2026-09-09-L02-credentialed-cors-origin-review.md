# L02 review — credentialed CORS origin configuration

**Date:** 2026-09-09  
**Decision state:** `Implemented and locally verified; independent/deployed review open`  
**Authority:** `tasks/L02-security-rls-and-archive-proof.md`

## Finding

`APP_ORIGIN` was only required to be non-empty even though the API uses it as
the exact credentialed CORS allowlist. A malformed value, a path-bearing URL,
or production HTTP could start successfully and either create an unusable
allowlist or weaken transport expectations.

## Remediation

The API now parses and canonicalises `APP_ORIGIN` at startup. Only absolute
HTTP(S) origins with no credentials, path, query or fragment are accepted, and
staging/production require HTTPS. This remains a single exact origin; it does
not introduce origin reflection or a wildcard.

## Evidence

The configuration regression tests cover malformed, credential-bearing,
path-bearing and production HTTP values plus trailing-slash normalisation.
`npx tsc --noEmit && npm test && npm run build` passed 402/402 on 2026-09-09;
the OpenAPI and hostile deployment-manifest checks also passed.

## Residual gates

The local test does not prove real domain ownership, certificate deployment,
Cloud Run environment substitution, WAF behavior, browser/device behavior, or
independent security review. L02 remains conditional and L10 remains blocked.
