# Easy CMS

Easy CMS is a portable, offline-first content management system that lets non-technical authors collaborate on a static website hosted on GitHub Pages. The Sync Server is the central authority for identity and content; the CMS Studio is the per-user authoring app; the Generated Site is what readers see.

## Language

### Components

**Sync Server**:
The hosted multi-tenant authority. Owns identity, the change log, and triggers publication.
_Avoid_: backend, server, API

**CMS Studio**:
The per-user portable authoring app, run locally by Writers, Editors, and Site Admins.
_Avoid_: client, frontend, app

**Generated Site**:
The public read-only static site produced from one Site's content, hosted on GitHub Pages.
_Avoid_: published site, frontend, public app

**Web View**:
A deterministic visible state inside a browser surface. Playwright Page Object Models are scoped to one Web View and transition to another Web View only through explicit user behavior.
_Avoid_: screen, page, POM page, route component

### Tenancy

**Site**:
A tenant on the Sync Server. Owns its own Articles, Users, and Generated Site URL.
_Avoid_: tenant, blog, project

### Content

**Article**:
A single Markdown document with front-matter metadata. The unit of authorship and the unit of publication. Has a stable identity that persists across rename and Slug changes.
_Avoid_: post, page, document

**Slug**:
The URL-safe identifier of an Article, unique within a Site. Determines the public URL on the Generated Site. Lives in the Article's front matter and is therefore part of its content (changing it produces a new Revision).
_Avoid_: path, permalink, url

**Former slug**:
A Slug an Article previously held. The Generated Site emits an HTML redirect from each Former slug to the current Slug so that old bookmarks and inbound links keep working.
_Avoid_: alias, redirect, old url

**Asset**:
A binary file (image, document, attachment) uploaded into a Site's Asset library. Independent of any single Article and referenced by URL from Article content. Deleting an Article never deletes Assets.
_Avoid_: media, upload, attachment, file

**Unpublish**:
The Editor action that clears an Article's Published revision. The Article remains in the CMS with all its history; its public URL 404s on the next Generated Site build. Republishing makes the Article live again.
_Avoid_: retract, depublish, hide

**Delete (soft)**:
The Writer or Editor action that hides an Article from the CMS and removes it from the Generated Site. The Slug stays reserved. A Site Admin can restore the Article or perform a Hard delete.
_Avoid_: archive, trash

**Hard delete**:
The Site-Admin-only action that permanently removes a soft-Deleted Article and frees its Slug. No history is preserved.
_Avoid_: purge, wipe

**Initial sync**:
The first download a Studio performs after a Site User signs in for a Site, pulling every Article and Asset in reverse-chronological order. Runs in the background, is interruption-resumable, never blocks the user from creating new Articles, and exposes an optional progress bar with ETA plus a 'sync ready' icon when complete.
_Avoid_: bootstrap, hydration, full sync, first sync

**Revision**:
A complete saved state of an Article at a point in time. Revisions are immutable.
_Avoid_: version, snapshot

**Published revision**:
The Revision of an Article currently rendered on the Generated Site. Each Article has at most one.
_Avoid_: live revision, current revision

**Latest draft revision**:
The most recent Revision of an Article on the Sync Server. May equal the Published revision (in which case the Article has no pending work) or be ahead of it.
_Avoid_: head, tip, latest

**Publish**:
The Editor action that advances an Article's Published revision to its Latest draft revision. Triggers a re-export of the entire Generated Site.
_Avoid_: promote, accept, approve, merge

**In progress**:
The state of an Article whose Latest draft revision is ahead of its Published revision and that a Writer has not yet flagged for review. Editors do not see In progress Articles in their review queue.
_Avoid_: draft, WIP

**Ready for review**:
The state of an Article whose Latest draft revision is ahead of its Published revision and that a Writer has flagged for Editor review. Such Articles appear in the Editor's review queue.
_Avoid_: pending, submitted

**Send back**:
The Editor action that returns a Ready for review Article to In progress, optionally with a comment shown to the Writer. The Latest draft revision is preserved; only the review state changes.
_Avoid_: reject, decline, return

**Superseded change**:
A queued change the Sync Server records but does not apply because the relevant Article or Site state has already advanced past it.
_Avoid_: skipped change, not applied change

### Roles

**Platform Admin**:
Operates the Sync Server. Creates Sites and assigns the initial Site Admin per Site.
_Avoid_: super admin, root, owner

**Site Admin**:
Top-level role within one Site. Manages Site Users and Site settings. Has Editor and Writer privileges by default.
_Avoid_: owner, manager

**Editor**:
Site User who can Publish and Send back Articles. Has Writer privileges by default; a single user wearing both hats is the expected model on small Sites. An Editor cannot edit a Ready for review draft directly without Sending it back first.
_Avoid_: reviewer, approver

**Writer**:
Site User who can create and edit Articles but cannot Publish them.
_Avoid_: author, contributor

**Site Visitor**:
Anonymous reader of the Generated Site. Not a Sync Server User.
_Avoid_: reader, audience

**Subscriber**:
An email address registered to a Site via the Generated Site's Subscribe form. Receives an email on every Publish for that Site. Distinct from a Site User and never logs in.
_Avoid_: follower, member, mailing list entry
