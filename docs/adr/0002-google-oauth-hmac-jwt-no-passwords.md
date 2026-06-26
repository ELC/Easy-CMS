# Google OAuth + HMAC JWT, no password storage

User identity is delegated to Google OAuth; the Sync Server never stores passwords or implements password reset. After Google verifies an email, the Sync Server issues a long-lived (30-day) HMAC-SHA256-signed JWT, which CMS Studio caches in SQLite and uses as bearer authentication for every Sync Server request. The same JWT works offline as long as it is unexpired, so a Writer who connects once a week can keep writing all week without re-authenticating with Google.

## Consequences

- Users without a Google account cannot use the system in v1.
- There is no password reset flow to build, maintain, or attack; account recovery is implicitly delegated to Google.
- Per-token revocation is achieved by bumping a `token_version` column on the user row; outstanding JWTs that do not match are rejected on next use.
