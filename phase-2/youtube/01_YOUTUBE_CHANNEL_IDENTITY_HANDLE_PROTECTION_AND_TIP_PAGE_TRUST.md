# YT-IDENTITY-01 — YouTube Channel Identity, Handle Protection, and Tip-Page Trust

**Status:** `Proposed / Phase 2 — not in v1`  
**Product:** BharatStudio Alerts  
**Priority:** P0 for the YouTube integration  
**Owner:** Product + Identity/Integrations engineering  
**Dependencies:** Google sign-in, YouTube OAuth, channel model, public tip page, audit logging, background jobs  
**Legacy evidence:** `requirements/16_YOUTUBE_UNIFIED_EVENTS_AND_SUPPORTER_IDENTITY.md` and `tasks/youtube/P16-youtube-unified-events-and-supporter-identity.md` from the frozen legacy snapshot; evidence only  

## Objective

Allow a creator to prove that a BharatStudio channel belongs to a specific YouTube channel, permanently protect the creator's current and historical YouTube handles inside BharatStudio, and give donors a trustworthy identity signal on the public tip page.

The immutable YouTube channel ID is the ownership key. A YouTube handle is a changeable public alias and must never be treated as the permanent identity.

This slice does not reopen YouTube for v1. It becomes implementation-eligible only after the YouTube reopening plan, provider scopes, quota model, privacy review, and launch authority are approved.

## Product decisions

### Identity separation

| Identity | Purpose |
|---|---|
| Google account subject (`sub`) | BharatStudio authentication |
| YouTube channel ID | Verified YouTube ownership |
| Current YouTube handle | Current public alias |
| BharatStudio channel ID | Permanent internal channel identity |
| BharatStudio handle | BharatStudio URL and public identity |

Google sign-in alone must never grant YouTube ownership or a YouTube verification badge.

### URL and handle namespaces

```text
/u/<slug>                 ordinary BharatStudio user/channel slug
/@<youtube-handle>        verified YouTube creator alias
/channel/<stable-id>      permanent BharatStudio channel URL
```

Rules:

1. Only a verified YouTube channel can claim the `/@<youtube-handle>` namespace.
2. Users without YouTube verification may use `/u/<slug>` but cannot block a verified creator alias.
3. Once a YouTube handle is verified in BharatStudio, its current and historical aliases are permanently reserved for that YouTube channel ID.
4. Historical aliases are not automatically released because of handle change, disconnect, inactivity, channel deletion, or OAuth expiry.
5. Known high-risk/public creator names may be pre-protected through an audited protected-name registry.
6. Matching must be case-insensitive and protect against Unicode confusables, punctuation variants, and reserved system/platform names.

## Creator connection flow

1. Creator signs in to BharatStudio with Google.
2. Creator selects **Connect YouTube channel**.
3. BharatStudio starts an OAuth authorization-code flow with state and PKCE protection.
4. The backend validates the authorization and calls YouTube with `mine=true`.
5. If the Google account manages multiple channels, the creator explicitly selects one.
6. The backend stores the immutable channel ID and imports the current name, handle, avatar, and canonical channel URL.
7. In one transaction, BharatStudio creates or updates the verified alias and permanent ownership record.
8. The creator confirms an identity preview before the public tip page displays the verified block.
9. Disconnecting YouTube stops future synchronization but does not release protected aliases.

Primary references:

- [YouTube channel implementation and `mine=true`](https://developers.google.com/youtube/v3/guides/implementation/channels)
- [YouTube OAuth authentication](https://developers.google.com/youtube/v3/guides/authentication)
- [YouTube handle rules](https://support.google.com/youtube/answer/11585688?hl=en)

## Public tip-page trust experience

For a verified creator, show server-derived identity data:

```text
✓ Verified YouTube channel

<YouTube channel name>
@<current YouTube handle>

This tip page is connected to the verified YouTube channel.
[Open verified YouTube channel]
```

Requirements:

- The badge is rendered only from server-side verification state.
- Name, handle, avatar, and canonical link come from the verified YouTube record.
- The canonical link uses the YouTube channel ID, not only a mutable handle URL.
- Users cannot upload or type a replacement verification badge.
- The tip page remains usable without YouTube, but the active badge is removed when verification becomes invalid or stale.
- Do not expose Google email, OAuth tokens, private YouTube data, or unnecessary statistics.
- Clearly distinguish identity verification from payment/refund guarantees.

## Handle-change flow

When YouTube changes `@alpha` to `@alphalive`:

```text
/@alphalive       -> current creator profile
/@alpha           -> same profile, marked "previously used"
/channel/<id>     -> permanent canonical profile
```

The update is atomic. The old alias remains permanently protected and cannot be claimed by another BharatStudio user, even if YouTube later makes it available to another channel.

If a later YouTube channel attempts to verify the same historical alias, do not transfer it automatically. Freeze the conflict for manual review.

## Synchronization and state model

### Sync triggers

- Initial YouTube connection
- Every sign-in for a linked creator
- Manual **Refresh YouTube identity**
- Tip-page/dashboard refresh when identity data is stale
- Scheduled background synchronization for creators who opt into YouTube integration

### States

```text
verified_current
    -> handle_changed
    -> verified_current

verified_current
    -> sync_pending
    -> stale
    -> connection_attention_required

any state
    -> frozen_for_review
```

Rules:

- Temporary API, quota, or network failures must not be treated as handle changes.
- Keep the last verified identity while retrying.
- OAuth revocation stops synchronization but does not release aliases.
- Channel deletion, ownership ambiguity, or suspicious conflict freezes the identity record.
- A handle/name change must not create a new BharatStudio channel automatically.

Recommended initial freshness policy, subject to quota approval:

- Sync on connection, sign-in, manual refresh, and at least daily while enabled.
- Keep the active badge when the last verification is within 24 hours.
- After 24 hours, show a refresh-pending state if synchronization has not succeeded.
- After the approved stale limit, hide the active badge but preserve the profile and historical aliases.

## Data and audit requirements

### YouTube channel link

Store a minimized record containing:

- BharatStudio channel ID
- YouTube channel ID
- Current and normalized handle
- Channel name and avatar snapshot
- Canonical channel URL
- Verification status
- First verified timestamp
- Last successful synchronization timestamp
- OAuth consent/token status
- Last error category without credentials or raw payloads

### Handle history and protected aliases

Store:

- Alias text and normalized alias
- Owning YouTube channel ID
- Owning BharatStudio channel ID
- Current or historical status
- First observed and retired timestamps
- Permanent reservation flag
- Conflict/review state

Enforce uniqueness for:

- One active BharatStudio link per YouTube channel ID
- One active verified alias per current namespace
- Every current and historical protected alias across the verified namespace

Audit connect, disconnect, channel selection, verification, handle/name changes, reservations, stale/revoked/frozen transitions, and manual conflict decisions.

## Security, privacy, and support requirements

- OAuth authorization-code flow with PKCE and state validation.
- Server-side token storage only; encrypt refresh tokens if background sync is enabled.
- Strict redirect URI allowlist and Google identity validation.
- Never accept a typed URL, screenshot, name, or handle as ownership proof.
- Client cannot decide badge or alias validity.
- Rate-limit connect, refresh, and conflict attempts.
- Redact tokens, email addresses, raw provider payloads, and private data from logs.
- Provide disconnect/revoke controls and explain what stops versus what is retained.
- Apply approved privacy retention and access rules to snapshots, token metadata, and alias history.
- Resolve handle disputes using channel ID/OAuth evidence, not screenshots or email claims.
- Never automatically transfer a protected alias to another channel.

## Edge cases

- **Multiple channels:** one explicit BharatStudio channel profile per selected YouTube channel; never infer the selection from Google email.
- **Brand Account/manager changes:** continue using the YouTube channel ID; a new manager must not create a duplicate channel record.
- **OAuth revoked:** stop polling, mark attention required after the approved grace period, remove the active badge when stale, and keep aliases protected.
- **Channel deleted/unavailable:** freeze the record, preserve audit history, and do not reassign aliases automatically.
- **Unverified impersonation:** allow a `/u/` slug only; do not allow the matching verified `/@` alias.
- **Later YouTube owner of an old handle:** keep the first BharatStudio reservation and require manual review for any conflict.

## Acceptance criteria

- [ ] Google sign-in without YouTube OAuth never produces a YouTube verification badge.
- [ ] `channels.list` with `mine=true` verifies the authorized channel and rejects typed-name ownership claims.
- [ ] Multiple channels can be selected without cross-linking data.
- [ ] Verified current handles are unique in the BharatStudio verified namespace.
- [ ] A changed YouTube handle creates a new current alias and permanently protects the previous alias.
- [ ] An unverified user cannot block a verified creator alias.
- [ ] The stable channel-ID URL remains unchanged across handle changes.
- [ ] Temporary API/quota failure does not incorrectly change or remove identity.
- [ ] OAuth revocation stops synchronization without releasing aliases.
- [ ] Conflicting claimants are rejected or frozen and cannot silently take an alias.
- [ ] Tip pages show the correct server-derived name, handle, avatar, badge, and canonical channel link.
- [ ] Disconnected/stale pages remain usable without an active verification badge.
- [ ] No Google email, token, private data, or raw provider payload appears publicly or in logs.
- [ ] All identity, alias, sync, and conflict actions are audited.
- [ ] Browser, mobile, accessibility, localization, long-name, stale-state, quota, retry, and cross-replica tests pass.
- [ ] Independent identity/privacy review and deployed staging verification are complete.

## Explicit non-goals

- This task does not make YouTube a v1 launch dependency.
- It does not automatically reserve every YouTube handle that has never been linked to BharatStudio.
- It does not transfer aliases automatically between YouTube channels.
- Full offline YouTube growth summaries require a separate polling, event, and retention task.

## Work sequence

| ID | Work | Required evidence |
|---|---|---|
| YT-ID-01 | Approve scope, consent, quota, privacy, and alias policy | authority/provider/legal/security decision |
| YT-ID-02 | Define channel-link, alias-history, conflict, and audit contracts | schema/API contract review |
| YT-ID-03 | Implement OAuth/channel selection and server verification | identity/access/redaction tests |
| YT-ID-04 | Implement protected current/historical alias transactions | concurrency/conflict/rollback tests |
| YT-ID-05 | Implement tip-page verification card and canonical links | browser/accessibility/localization tests |
| YT-ID-06 | Implement sign-in/manual/background synchronization | stale/revocation/quota/retry tests |
| YT-ID-07 | Run deployed staging and independent identity/privacy review | staging evidence and review record |

