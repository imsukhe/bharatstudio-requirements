# L10 review — API image and production configuration contract

**Date:** 2026-09-09  
**Scope:** Local deployment manifest and image wiring in `bharatstudio-alerts`  
**Disposition:** Local defect remediated; release remains blocked

## Finding

The Cloud Run API service declared an `alerts-api` image, but the repository had
no corresponding API Dockerfile. It also omitted several values which API
startup makes mandatory in staging/production: Google client ID, payment origin
and OIDC audience, internal-service audience allowlist, notification token
encryption key, and Turnstile secret. A manifest-only pass could therefore give
a false indication that the service was deployable.

## Remediation reviewed

- Added `apps/api/Dockerfile`: pinned Node base, root workspace build, compiled
  `dist/src/index.js` command, production dependency closure and non-root
  runtime user.
- Added the missing Cloud Run bindings, using secret references for secret
  material and placeholders only for deployment-specific URLs.
- Extended `deployment/validate-manifests.sh` to reject missing bindings, a
  missing API Dockerfile, or a Dockerfile that does not launch the compiled API.
- Added an isolated `pnpm deployment:test` harness. It proves the canonical
  fixture passes and rejects missing Google-client and direct-database bindings,
  an altered compiled entrypoint, and a fixture with every release substitution
  removed.
- Documented root API and service-specific image build inputs.

## Reproduction

On 2026-09-09 the API, alert-worker, and payment-webhook images each built with
their checked-in Dockerfiles. `pnpm deployment:test && pnpm deployment:validate`
returned `BSA_DEPLOYMENT_MANIFEST_TESTS=PASS (1 positive, 4 negative)` and
`BSA_DEPLOYMENT_MANIFESTS=PASS`. The API container, bound to `HOST=0.0.0.0`,
returned `{"status":"ok","service":"bharatstudio-alerts-api"}` from
`/healthz`. Image inspection showed the API runs as `node`; the Go images run
as `nonroot:nonroot`.

## Residual gates

This is local evidence only. It does not prove Cloud Run substitution or IAM,
secret existence/rotation, real database readiness, migration compatibility,
provider connectivity, deployment/rollback, capacity, or any public-release
criterion. L10 remains blocked pending its existing staging, provider, store,
legal and independent-review gates.
