# Public-by-default hosting on GitHub Pages

Generated Sites are hosted on GitHub Pages under `https://elc.github.io/easy-cms/<site-slug>/` and are public by default. Private hosting is explicitly out of scope for v1; supporting it would force a different publishing target (object storage with signed URLs or similar) and a visitor-side authentication story. The architecture leaves a `PublishSvc` seam where a future paid private-hosting tier can plug in an alternative sink without touching the rest of the system.

## Consequences

- Sites cannot host content a Writer or Editor would not show to the world.
- A Site's `<site-slug>` is part of its public URL; renaming a Site after creation breaks every external link to it. The Site slug is therefore treated as immutable.
- The Sync Server uses a single fine-scoped GitHub PAT to push to one shared publishing repo; no per-Site GitHub credentials are needed.
