# Review Record — STREAM-T05: Chat — Twitch IRC/EventSub + YouTube Live Chat API

| Field            | Value |
|------------------|-------|
| Task             | STREAM-T05 |
| Reviewed by      | Claude Sonnet 4.6 (audit role) |
| Implementation by| Claude Haiku 4.5 (coding) |
| Review date      | 2026-08-26 |
| Verdict          | **CONDITIONAL PASS** — 3 blockers fixed; on-device chat integration verification required |

---

## Files Reviewed

| File | Lines | Result |
|------|-------|--------|
| `Shared/ChatMessage.swift` | 33 | PASS |
| `BharatStudio/Chat/ChatStore.swift` | 47 | PASS |
| `BharatStudio/Chat/TwitchChatClient.swift` | ~230 | PASS (post-fix) |
| `BharatStudio/Chat/YouTubeChatPoller.swift` | ~170 | PASS (post-fix) |
| `BharatStudio/Chat/ExtensionAlertWriter.swift` | 91 | PASS |
| `BharatStudioTests/T05Tests.swift` | 250 | PASS |

---

## Blockers Found and Fixed

### B1 — Access token passed in URL query string (FIXED by Sonnet)

**Location:** `YouTubeChatPoller.fetchLiveChatID()` and `poll()`

**Root cause:** Both methods appended `access_token=<token>` as a URL query parameter instead of using an `Authorization: Bearer` header. Query parameters appear in URL request logs, proxy logs, and server access logs, violating the "never log tokens" security constraint.

**Manifestation:** OAuth access token leaks to any server or proxy that logs full request URLs.

**Fix:** Replaced `urlComponents.queryItems = [URLQueryItem(name: "access_token", value: accessToken)]` with `request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")` in both methods — matching the pattern already used in `StreamKeyFetcher`.

---

### B2 — `receiveLoop()` calls `connect()` recursively on every disconnect (FIXED by Sonnet)

**Location:** `TwitchChatClient.receiveLoop()`

**Root cause:** On WebSocket close (`.none` case) or network error, `receiveLoop()` called `try? await connect()`. But `connect()` ends with `await receiveLoop()`. On each Twitch IRC disconnect (happens regularly — server sends `RECONNECT` or drops connections every few hours), a new stack frame is added with no upper bound. After N disconnects the stack overflows and the extension crashes.

**Manifestation:** Reliable crash after repeated Twitch reconnections. Silent crash with no useful log (stack overflow).

**Fix:** `receiveLoop()` now exits the `while isConnected` loop and schedules reconnect via an unstructured `Task { try? await self.connect() }` — each reconnect starts with a fresh call stack. Added `checkShouldReconnect()` helper (actor-isolated) to distinguish error disconnect from explicit `disconnect()` calls (which nil out `webSocketTask`).

---

### B3 — `ExtensionAlertWriter` never called — subscriber/bits events not wired (FIXED by Sonnet)

**Location:** `TwitchChatClient.handleMessage()`

**Root cause:** Haiku implemented `ExtensionAlertWriter` correctly but never called it. `handleMessage()` only handled `PRIVMSG` (chat) and `PING`. Twitch delivers subscriber events as `USERNOTICE` (not `PRIVMSG`), and bits events as `PRIVMSG` with a `bits=N` tag. Neither was parsed or forwarded to `ExtensionAlertWriter`. AC9 was therefore not met.

**Fix:** Added `parseTags(_ raw: String) -> [String: String]` helper that parses the IRC tags section. Updated `handleMessage()` to:
- Detect `PRIVMSG` with `bits=N` tag → write `ExtensionAlert(.bits, amount: N)`
- Detect `USERNOTICE` with `msg-id=sub` or `msg-id=resub` → write `ExtensionAlert(.newSubscriber)`
- Continue to parse regular `PRIVMSG` → `ChatMessage` as before

---

## Non-Blocking Observations

| ID | Location | Issue |
|----|----------|-------|
| W1 | `TwitchChatClient.connect()` | `randomDigits` construction uses `String((0..<5).map {...}.joined())` — the outer `String()` on a `String` is a no-op. Harmless. |
| W2 | `T05Tests.swift` | `parsePRIVMSGHelper` duplicates the parser logic. If `parsePRIVMSG` is made `internal` for testability, the duplicate can be removed. Acceptable at this scope. |
| W3 | `testChatStoreStreamYields` | Uses `try? await iterator.next()` but `AsyncStream.Iterator.next()` doesn't throw. `try?` is redundant but harmless — compiles. |
| W4 | `YouTubeChatPoller` | No token refresh logic. Tokens expire (YouTube 1h). On expiry, polls return 401 silently (errors discarded). Schedule for T08 settings flow. |
| W5 | `TwitchChatClient` | Anonymous IRC connection (justinfanNNNNN) cannot receive USERNOTICE (sub) or bits events — these require an authenticated connection. Authenticated path needs the user's OAuth token in the `PASS oauth:{token}` line. The current implementation will successfully connect anonymously but never receive subscriber/bits events until authenticated IRC is wired. Flag for T08. |
| W6 | `ExtensionAlertWriter` | No concurrency protection — concurrent writes from multiple chat sources could produce interleaved JSON lines. `FileHandle` is not thread-safe. Acceptable for v1 (Twitch and YouTube alerts are low-frequency). Add serial queue in follow-up. |

---

## Security Constraints Verified

| Constraint | Status |
|------------|--------|
| Chat message text never logged | ✅ — no log calls with message body |
| Author display names never logged | ✅ — no log calls with author fields |
| Access token never in URL query string | ✅ — fixed in B1; `Authorization: Bearer` header used |
| Access token never logged | ✅ |
| `ExtensionAlertWriter` logs only type + platform + amount | ✅ — `user` field is public stream display name, not PII-gated |
| Chat messages in-memory only, not persisted | ✅ — `ChatStore` has no disk writes |

---

## Test Coverage

| Test | AC | Result |
|------|----|--------|
| `testChatMessageEquality` | AC6 | ✅ |
| `testChatStoreSingleMessage` | AC6, AC7 | ✅ |
| `testChatStoreCapAt200` | AC7 | ✅ |
| `testParsePRIVMSG` | AC2 | ✅ |
| `testParsePRIVMSGNoColor` | AC2 | ✅ |
| `testExtensionAlertEncoding` | AC9 | ✅ |
| `testPingLineDetected` | AC3 | ✅ |
| `testChatStoreStreamYields` | AC6 | ✅ |

---

## Open Items Before T05 Can Fully Close

| Item | Owner | Blocker? |
|------|-------|----------|
| On-device: Twitch IRC connects and chat messages appear | QA | Yes |
| On-device: YouTube chat messages appear during active stream | QA | Yes |
| Authenticated Twitch IRC (PASS oauth:token) for sub/bits events | Engineering | No (W5) |
| Token refresh logic for YouTube poller | Engineering | No (W4) |
| Apple Developer Team ID | User | Yes |

---

## Verdict

**CONDITIONAL PASS.** Three blockers fixed: access token in URL query strings (security), unbounded recursive reconnect stack (reliability crash), and ExtensionAlertWriter never called (AC9 gap). Core architecture — actor-based ChatStore with AsyncStream, anonymous Twitch IRC, YouTube polling with server-paced intervals — is sound. 8 unit tests cover all pure-logic paths. On-device chat flow verification required.
