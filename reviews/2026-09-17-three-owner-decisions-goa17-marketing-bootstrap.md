# Three owner decisions — GOA-17, marketing_section, admin bootstrap

**Date:** 2026-09-17
**Owner:** Sukhdev Singh
**Status:** `Approved`
**Authority:** `FULL-PRODUCT-DEFINITION.md` §6 module #11, §20.2, §20.5, §31 rows `GOA-17`,
`CTL-10`/`11`/`12`, `ADM-07` · `reviews/2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md`

---

## 1. `GOA-17` — reveal only, and the exposure log is dropped

**Decision.** The sponsor trigger action keeps its **reveal-card** half. The
**"log exposure with timestamp for proof-of-delivery"** half is **dropped**.

**Why this was a contradiction and not a preference.** The same-day owner decision on §6
module #11 dropped the sponsor exposure log entirely, and migration `0145` enforces it: its SQL
test scans `information_schema.columns` and every shipped function body for `count`,
`impression`, `exposure`, `views`, `shown_at`, `displayed_at` and `duration`. An
exposure-logging action would **fail that guard by design** — the two could not both ship.

**What this costs, stated rather than buried.** A sponsor asking *"show me it ran"* gets nothing
from us. That is the cost the §6 #11 decision already accepted, for the reason recorded there:
any number we render eventually becomes a number a sponsor relies on to pay, and a label saying
it is not auditable protects nobody at that moment.

**What it does NOT authorise.** No impression metric, no duration accounting, no "last revealed
at". Reinstating any of them reopens the legal question, not just the code.

---

## 2. `marketing_section` — a separate field, not a seventh `kind`

**Decision.** Marketing sections get **their own field**, not a value in §20.2's `kind` enum.
`CTL-12`'s wording (*"marketing sections behind flags (`kind = marketing_section`)"*) is
**corrected** to match.

**Why.** §20.2's `kind` is a taxonomy of **capabilities** — widget, module, feature, hub_lane,
lobby_mode, ai_feature. A marketing section is a page region, not a capability a creator is
entitled to. Widening the enum would have been the smaller diff and the worse model: the
registry would then mean two different things, and `capacity_class` already exists precisely
because conflating taxonomies there is dangerous (`CTL-14`).

**What unblocks.** `CTL-10` (`GET /v1/public/capability-matrix`), `CTL-11` (marketing build
reads the snapshot, webhook revalidation) and `CTL-12` were all blocked on this and are now
buildable.

**The cost, honestly.** §20.5's *"full site behind flags"* now routes through two places rather
than one, and `CTL-11`'s *"marketing reads the same source"* becomes slightly less literal —
the marketing build reads one published snapshot that carries both.

---

## 3. Admin bootstrap — a one-time seeded migration

**Decision.** The first platform admin is created by a **one-time, audited seed** that is inert
afterwards.

**The problem it solves, which is now proven rather than suspected.**
`app_private.staff_set_platform_admin` requires the caller to already be an admin, and no
empty-registry branch exists. Zeroing the registry makes **both** self-targeting and
third-party grants fail `42501`. So a fresh deployment has **no admin and no reachable way to
create one** except direct database access. This predates migration `0156`; `0156` did not
introduce it and did not fix it.

**Where the first identity comes from — and why this is not the allowlist again.** The seed
takes its identity from a **deployment-provided value, configured but unset**. Unset means
**no admin is seeded and the system says so** — never a guessed default, never a hardcoded
address. This differs from the `PLATFORM_ADMIN_EMAILS` allowlist that `ADM-07` just deleted in
the way that matters: the allowlist was a **standing authorisation decision** consulted on
every request, whereas this is **one write, audited, after which the database is the only
authority**. A break-glass credential that stays valid while the registry is empty was
considered and declined for exactly that reason — it would have reintroduced a standing
credential in configuration.

**Requirements on the seed.**
- It writes an audit row like any other grant — `0156` reuses `0155`'s append-only
  `reject_table_mutation` trigger, and the seed must not be exempt from it.
- It is **idempotent and inert once an admin exists**: running it again with an admin present
  must change nothing.
- It must not become a second standing authorisation path. After it runs,
  `app_private.is_platform_admin()` is the only authority, exactly as `ADM-07` established.

**Still not decided, and not decided here.** MFA. `ADM-07` built none because no provider,
enrolment flow or recovery-code policy exists. Seeding the first admin makes the *authority*
reachable; it does not make the *authentication* stronger, and §20.6's *"behind platform-admin
auth with MFA"* remains unmet.
