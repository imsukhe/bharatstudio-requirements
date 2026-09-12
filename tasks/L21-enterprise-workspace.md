# L21 — Enterprise workspace

**Status:** `TODO — not started (governance-blocked in v1)`
**Level:** L4
**Owner:** [OWNER — product/payments/legal, unassigned]
**Depends on:** L10's go/no-go gate; the corrected money-flow model in Part 9
**Blocks:** none — this task itself is blocked from proceeding until L10 is amended and Part 9's open question is answered
**Test record:** [`../tests/TC-L21-enterprise-workspace.md`](../tests/TC-L21-enterprise-workspace.md)

## Authority and evidence

Master plan Part 6, "L21 — Enterprise workspace" (lines ~1147–1154, "See Part 9 for the corrected money flow. Governance-blocked in v1 by L10."); Part 9 in full ("ENTERPRISE (PHASE 2)") — the corrected enterprise↔creator split model via Razorpay Route, the one open question about which party's Razorpay account hosts the Route parent, and the 2026-09-02 position that the **enterprise** holds the parent account and BharatStudio is never the parent; Part 9 §9.4 governance status: "**Blocked in v1.**" L10 states plainly "v1 contains no YouTube or Enterprise capability/claim," and the marketing site must carry no Enterprise tier, CTA, or contact-sales flow until L10 is amended.

## Objective

Define (not yet build) the Enterprise workspace: multi-channel allocations, SSO, RBAC beyond owner/moderator, shared brand kits and licensed design packs, campaigns, cross-channel analytics, API and outbound webhooks, finance/audit exports, SLA and named support. A workspace can allocate a different tier per channel.

## Tasks

1. Multi-channel allocation model: a workspace assigns a different tier per channel.
2. SSO integration.
3. RBAC beyond owner/moderator.
4. Shared brand kits and licensed design packs.
5. Campaign tooling.
6. Cross-channel analytics.
7. API and outbound webhooks (workspace-scoped).
8. Finance and audit exports.
9. SLA and named support tier.
10. Razorpay Route split configuration (percentage or flat amount, per-creator override) — **entirely contingent on the open question below being answered in writing.**

## Exact implementation boundary

Nothing in this task may be implemented, and no Enterprise tier, CTA, or "contact sales" flow may appear on the marketing site or in the product, until both of the following are true: (a) L10 is formally amended to permit Enterprise capability/claim in whatever release phase this task targets, and (b) Razorpay has confirmed in writing the five questions in Part 9 §9.2 (parent-account holder, third-party split-instruction write access under a scoped grant, direct settlement with no intermediate custody, per-linked-account split-rule flexibility, and in-flight-split behavior on a suspended linked account).

This task file is a definition placeholder for what Enterprise will contain once unblocked — it authorizes no implementation now.

## Non-negotiable implementation rules

- BharatStudio takes 0% of the enterprise↔creator split and holds nothing: no custody, no wallet, no settlement, no payout, ever, at any stage of this feature.
- The split is enterprise↔creator, never BharatStudio↔anyone.
- The **enterprise** holds the parent Razorpay Route account; creators are linked accounts beneath it; BharatStudio only reads webhooks and writes the split instructions the enterprise configured. BharatStudio is never the parent. If Razorpay's answer requires a BharatStudio-owned parent instead, that is a product decision to reopen — not something to accept quietly, because it would put BharatStudio structurally in the money flow and contradict the platform's zero-custody rule (§1.4).

## Definition gate

Per `governance/AGENTS.md`, this is L4 work (release/irreversible external change touching money flow and a public product tier) — the highest classification, requiring the most conservative gate. Implementation is not merely paused pending approval; it is **structurally blocked** by L10's governance status until L10 is amended.

**Open legal/payment question — not decided here.** Whether a third-party platform (BharatStudio) can write Razorpay Route split instructions against an enterprise-owned parent account under a scoped grant, without holding or routing funds, is exactly the kind of payment/provider-policy conclusion that, per `governance/AGENTS.md`, "requires dated primary evidence or written professional/provider advice" and must not be approved from memory. This task records the five confirmation items from Part 9 §9.2 as open and unresolved; it asserts no answer on Razorpay's behalf.

**Open decision — owner unassigned:** [OWNER].

## Acceptance criteria

- No Enterprise tier, CTA, or contact-sales flow exists on the marketing site or in the product while L10's block stands — this is a standing, checkable acceptance criterion for every deploy, not a one-time check.
- Before any implementation begins, this task's evidence trail carries Razorpay's dated written answers to all five items in Part 9 §9.2.
- Any subsequent implementation task derived from this definition must show, by test, that BharatStudio's system never holds settlement funds and never appears as the Route parent account.
- Split-rule configuration (percentage or flat, per-creator override) is provably driven by the enterprise's configuration, never a BharatStudio-set default disguised as an enterprise choice.

## Evidence required for closure

This definition task closes only as a definition record, not as a shipped feature. Its evidence is: the dated written Razorpay confirmation (or explicit record of its absence) for each of the five Part 9 §9.2 items, and the specific L10 amendment (dated, with reviewer) that lifts the Enterprise block. No artifact/screenshot directory; no implementation evidence is claimed here because none exists.

## Rollback

Not applicable at the definition stage — no code or schema exists yet. Once unblocked and implemented, any future task must specify migration/rollback separately, subject to this file's non-negotiable rules remaining unchanged.
