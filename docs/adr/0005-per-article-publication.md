# Per-Article publication, no global "main"

Each Article is the unit of publication: the Sync Server tracks a `published_revision` and a `latest_draft_revision` per Article, and an Editor's Publish action advances exactly one Article's pointer. There is no global `main` branch on the Sync Server and no batch-publication concept. The change log is per-Article, scoped by `article_id`, with cross-Article ordering only mattering inside a single sync request from one Studio.

## Consequences

- Multiple Articles can be in flight (In progress or Ready for review) at the same time without blocking each other.
- The conflict UX in the Studio operates per Article; there is no concept of merging across Articles.
- `PublishSvc` triggers on every per-Article Publish, exporting the entire Site's current published state to the GitHub publishing repo. This implies one GitHub Action build per Publish, which is acceptable on a public repo where Actions usage is unmetered.

## Considered Options

- Batched publication with a global `main` (echoing Git). Rejected because the Sync Server has no Git internals and inventing a global lineage on top of a per-Article change log added complexity for no user-visible benefit.
- Per-change publication where every approved Change immediately goes live. Rejected because it forces every saved Revision through the Editor and conflicts with the Ready-for-review flow.
