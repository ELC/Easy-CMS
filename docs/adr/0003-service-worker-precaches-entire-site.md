# Service worker precaches the entire Generated Site

The Generated Site's service worker precaches every Article, every Asset, and the offline fallback screen on first visit, rather than using the conventional stale-while-revalidate or cache-first-on-demand strategies. The use case explicitly assumes Site Visitors with intermittent connectivity (a connection window may be once a week or less); they must be able to read every Article on the Site without further connectivity, and updates can happen in the background whenever connectivity returns. The build emits a `precache-manifest.json` listing every address produced for the Site; the service worker downloads the full set on install and re-precaches atomically when `version.json` reports a new build hash.

## Consequences

- First-visit bandwidth is high (entire Site downloaded). Acceptable for article-shaped content; a soft cap of ~200 MB per Site is documented for Site authors.
- Storage in the browser grows with the Site; eviction is the browser's responsibility and could surprise a visitor on a small device.
- A Sync Server outage or GitHub Pages outage is invisible to visitors mid-session because the cache-first runtime strategy serves cached content on any network failure.
