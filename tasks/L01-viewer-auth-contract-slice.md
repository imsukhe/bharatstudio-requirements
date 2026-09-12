# L01 — Viewer authentication contract slice

**Status:** `Implemented locally — executable evidence recorded`
**Level:** L3
**Authority:** L01 versioned API contracts

## Scope

Publish exact v1 OpenAPI contracts and redacted verified fixtures for the four
unauthenticated viewer-identity operations already implemented by Alerts:
signup, login, password-reset request, and password reset. The routes form a
separate opaque viewer-session namespace; they are not creator authentication
and must not be represented as a shared account/session surface.

## Security and privacy constraints

- Signup failure stays generic and does not confirm whether an email exists.
- Login failure remains a generic credential error.
- Password-reset request returns the same accepted response for registered,
  unregistered, and store-failure cases.
- Password-reset failure does not distinguish invalid, expired, or used tokens.
- Fixtures use an explicitly synthetic token only and reject account identity,
  email, password, or reset-token fields in response projections.

## Migration, deployment, and rollback

This is documentation/fixture hardening only: no migration, runtime endpoint,
database access, deployment configuration, or external provider behavior
changes. Rollback is removal of the new published operation contracts and
fixtures in a controlled contract revision; it does not change stored sessions
or credentials.

## Acceptance

1. Each route has bounded request and typed success/error response contracts.
2. The viewer bearer scheme is explicit and distinct from creator bearer auth.
3. Positive fixtures validate and hostile additions exposing identity/secret
   fields are rejected.
4. Contract, API, web, and deterministic local regression suites remain green.

## Local evidence — 2026-09-09

`pnpm contracts:validate` passed 24 fixtures, 49 OpenAPI paths, 56 operations,
all local references, and three hostile OpenAPI mutations. The route inventory
then reported 56 published runtime operations and zero stale contracts. API
tests passed **402/402** and web tests passed **289/289**. The fixtures reject
an account identifier in a session response, an email in the enumeration-safe
request response, and an access token in the reset-completion response.

No runtime authentication behavior, migration, deployed identity provider, or
production viewer data was changed or accessed.
