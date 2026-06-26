# Generated Site Subscribe exception

The Generated Site is static and read-only for Site Visitors, but v1 allows one explicit exception: the Subscribe form may submit an email address to a narrowly scoped Sync Server endpoint for that Site. This keeps Subscriber signup in the Site Visitor flow while preserving the rule that Article rendering, offline reading, and all personalized behavior stay outside the Generated Site.

## Consequences

- The Subscribe endpoint must be unauthenticated, rate limited, and protected against automated abuse.
- The Generated Site still does not fetch Article data, Site User data, or personalized state from the Sync Server.
- If private hosting is added later, Subscriber signup remains a separate boundary decision rather than a general permission for the Generated Site to call the Sync Server.
