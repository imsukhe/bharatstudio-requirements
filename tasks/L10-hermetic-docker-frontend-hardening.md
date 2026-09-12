# L10 — Hermetic Docker frontend hardening

**Status:** `Locally implemented and verified`  
**Level:** L3  
**Parent authority:** `L10-release-readiness-and-rollout.md`; `L01-contracts-and-database-baseline.md`  
**Test record:** [`../tests/TC-L10-hermetic-docker-frontend-hardening.md`](../tests/TC-L10-hermetic-docker-frontend-hardening.md)  
**Review:** [`../reviews/2026-09-09-L10-hermetic-docker-frontend-hardening-decision.md`](../reviews/2026-09-09-L10-hermetic-docker-frontend-hardening-decision.md)

## Scope

The three declared service Dockerfiles specify `# syntax=docker/dockerfile:1`
but use no syntax-only feature. BuildKit therefore attempts an avoidable public
registry fetch before evaluating source, blocking deterministic local evidence
when that frontend is unavailable. Remove only this redundant directive so the
engine's bundled Dockerfile frontend is used. Keep all pinned base-image
digests, stages, commands, users, ports, and image targets unchanged.

## Boundaries and rollback

No application source, dependency version, service interface, runtime config,
deployment manifest, registry destination, provider, migration, or production
release is changed. Rollback is restoration of the comments, which would
restore the unnecessary dependency. Local image builds are required; registry
publication, deployed runtime, signing, provenance, vulnerability scanning,
staging and production are separate external gates.

## Acceptance

- API, payment-webhook and alert-worker declared builds complete without a
  Dockerfile-frontend registry fetch.
- The normal complete local verifier passes with its three image builds.
- Base image digest pinning and runtime entrypoints remain unchanged.

## Local evidence — 2026-09-09

- Removed only the redundant `# syntax=docker/dockerfile:1` directive from
  the API, payment-webhook and alert-worker Dockerfiles. The initial failed
  build had stopped at that remote frontend; after the change it progressed
  directly to each already-pinned base image. A slow base-image metadata
  lookup recovered, and all three declared images completed successfully.
- `pnpm verify:local` subsequently passed end-to-end: contracts (34 fixtures,
  60 paths, 67 operations), deployment positives/negatives, 45 SQL files,
  19 role-separated proofs, L09 load/fault 5/5 each, API/web 293/293,
  production builds, all Go race/vet suites, and API/payment/worker images.
- This is local build evidence only. Registry publication, image signing/SBOM,
  scanning, deployed runtime, staging and production remain external gates.
