# Decision — L10 hermetic Docker frontend hardening

**State:** `Locally accepted after deterministic image verification`

The remote syntax directive is redundant in each current Dockerfile and blocks
local verification before source evaluation. Removing it is approved only if
the Dockerfiles require no syntax-specific features and all base image/runtime
semantics remain byte-for-byte otherwise. This is not deployment or production
readiness evidence.

## Post-change review — 2026-09-09

All three Dockerfiles were confirmed to use only standard instructions. The
remote frontend directive was the sole source change; pinned base digests and
runtime behavior remain intact. The complete verifier, including image builds,
now passes. This removes the local registry-front-end blocker but does not
prove registry publication, signing, scanning, staging or production release.
