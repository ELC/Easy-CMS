# JSON change-log protocol between CMS Studio and Sync Server

The Sync Server is deployed as Vercel serverless functions, whose filesystem is ephemeral and per-invocation, so it cannot host bare Git repositories. Instead of self-hosting Git on a separate persistent VPS or pushing directly from each CMS Studio to a private GitHub repo per Site, the CMS Studio talks to the Sync Server through an HTTPS JSON change-log protocol persisted in Supabase Postgres. CMS Studio history in v1 is reconstructed from immutable Article Revisions in SQLite and the Sync Server; there is no local Git working tree on the sync or history path.

## Considered Options

- Self-host Git smart-HTTP on a small VPS alongside Vercel + Supabase. Rejected: splits the deployment model and undermines the serverless choice.
- Have each CMS Studio push directly to a private GitHub repo per Site, brokered by the Sync Server. Rejected: leaks GitHub coupling into every CMS Studio install and complicates revocation and rate-limit handling.
- The chosen JSON change-log protocol. Keeps deployment fully serverless and gives CMS Studio precise control over conflict UX.
