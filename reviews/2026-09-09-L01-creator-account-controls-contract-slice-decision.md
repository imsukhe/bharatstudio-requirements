# Decision — L01 creator account-controls contract slice

**State:** `Approved for local implementation by active QA goal`

Creator self-service account-control responses carry sensitive information and
must not rely on TypeScript declarations or database behavior alone for their
public shape. This decision authorizes strict v1 serialization, fixtures and
client validation only. It does not authorize a change in account lifecycle,
retention, legal policy, provider use, deployment, or production data access.
