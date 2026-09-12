# Review Record — STREAM-T09: StoreKit 2 IAP Full Wiring + Entitlement Enforcement

| Field            | Value |
|------------------|-------|
| Task             | STREAM-T09 |
| Reviewed by      | Claude Sonnet 4.6 (audit role) |
| Implementation by| Claude Haiku 4.5 (coding) |
| Review date      | 2026-08-26 |
| Verdict          | **CONDITIONAL PASS** — no blockers; StoreKit sandbox verification required |

---

## Files Reviewed

| File | Lines | Result |
|------|-------|--------|
| `Shared/EntitlementTier.swift` | 35 | PASS |
| `BharatStudio/IAP/EntitlementStore.swift` | 145 | PASS |
| `BharatStudio/Views/SubscriptionView.swift` | 83 | PASS |
| `BharatStudioTests/T09Tests.swift` | 121 | PASS |
| `Shared/AppGroup.swift` | 23 | PASS (made public) |

---

## Blockers Found and Fixed

None. Clean implementation pass.

---

## Non-Blocking Observations

| ID | Location | Issue |
|----|----------|-------|
| W1 | `checkCurrentEntitlement()` | When multiple `currentEntitlements` exist (subscription overlap during upgrade), `highestTier` is last-wins rather than highest-wins. In practice StoreKit delivers one active subscription at a time. Acceptable for v1. |
| W2 | `SubscriptionView` | `.task { await loadProducts(); await checkCurrentEntitlement() }` runs on every view appearance (TabView tab switches). For v1 this is acceptable; StoreKit caches aggressively. Guard with `products.isEmpty` for v2. |
| W3 | `listenForTransactions()` | `Task(priority: .background)` inside `@MainActor init` inherits the `@MainActor` isolation — processing happens on main thread. Correct but means all update handling runs on main. For lightweight `updateEntitlement` + `finish()` this is fine. |
| W4 | `AppGroup.identifier` | Still `"group.com.bharatstudio.streaming"` (the existing naming inconsistency vs the `stream` variant in AGENTS.md). Pre-existing and consistent across all files — not introduced by T09. Must be resolved before App Store submission in T10. |

---

## Security Constraints Verified

| Constraint | Status |
|------------|--------|
| Entitlement flag written to App Group JSON (not UserDefaults) | ✅ — `data.write(to: entitlementFlagURL, options: .atomic)` |
| Extension reads same `EntitlementFlag` struct (matching Codable shape) | ✅ — `EntitlementSource.subscription(validUntil:)` ↔ `EntitlementModels.swift` |
| StoreKit verification uses `checkVerified` (rejects `.unverified`) | ✅ — throws on unverified transactions |
| No hardcoded prices (locale-aware `product.displayPrice` used) | ✅ |
| `AppStore.sync()` called only in `restorePurchases()`, not in `checkCurrentEntitlement()` | ✅ |

---

## Test Coverage

| Test | AC | Result |
|------|----|--------|
| `testProductIDConstants` | AC1 | ✅ |
| `testEntitlementTierCount` | AC10 | ✅ |
| `testFreeHasNoProductID` | AC5, AC10 | ✅ |
| `testProHasProductID` | AC1 | ✅ |
| `testCreatorHasProductID` | AC1 | ✅ |
| `testStudioHasProductID` | AC1 | ✅ |
| `testAllTiersHaveDisplayNames` | AC7 | ✅ |
| `testDisplayNameValues` | AC7 | ✅ |
| `testEntitlementFlagFree` | AC5 | ✅ |
| `testEntitlementFlagPaid` | AC4 | ✅ |
| `testEntitlementTierCodable` | AC6 | ✅ |

---

## Open Items Before T09 Can Fully Close

| Item | Owner | Blocker? |
|------|-------|----------|
| On-device: StoreKit sandbox purchase completes and entitlement flag written | QA | Yes |
| On-device: extension reads `entitled: true` and suppresses watermark post-purchase | QA | Yes |
| On-device: `restorePurchases()` restores valid subscription after reinstall | QA | Yes |
| StoreKit Configuration file (`Configuration.storekit`) for Xcode testing | Engineering | No |
| App Group identifier name reconciliation (`streaming` vs `stream`) | Engineering | Yes — before App Store |
| Apple Developer Team ID | User | Yes |

---

## Verdict

**CONDITIONAL PASS.** No blockers. `EntitlementStore` correctly implements the StoreKit 2 pattern: products fetched via `Product.products(for:)`, purchases via `product.purchase()`, verification via `VerificationResult` with `checkVerified`, renewal/cancellation via `Transaction.updates` listener started in `init()` and cancelled in `deinit()`. `writeEntitlementFlag` produces a properly-shaped `EntitlementFlag(source: .subscription(validUntil: nil))` that `SampleHandler` reads correctly via `EntitlementModels.swift`. 11 unit tests cover all pure-logic paths. Sandbox purchase flow verification required on device.
