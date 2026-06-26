---
name: harness feedback
overview: Refine the Easy CMS harness implementation based on the feedback, codify the conventions in `CONTRIBUTING.md`, and make `AGENTS.md` reference that shared guidance so humans and agents follow the same rules.
todos:
  - id: document-conventions
    content: Create `CONTRIBUTING.md`, add `Web View` to `CONTEXT.md`, and update `AGENTS.md` to reference the shared guidance.
    status: completed
  - id: move-workspace-layout
    content: Move workspace members under `src/apps` and `src/packages`, then update all workspace references.
    status: completed
  - id: inline-mise-tasks
    content: Inline `mise` task bodies in `mise.toml`, remove `mise-tasks/harness.sh`, and pin tool versions.
    status: completed
  - id: harden-hooks-ci
    content: Update `prek` hooks, add YAML/TOML formatters, and pin CI actions to commit SHAs with version comments.
    status: completed
  - id: refactor-python-surfaces
    content: "Apply Python HTTP surface feedback: imports, DI wiring, examples, services, exceptions, tests, and strict mypy."
    status: completed
  - id: refactor-browser-surfaces
    content: Apply React 19, SCSS/BEM, semantic HTML, `ts-pattern`, and generated hook usage changes.
    status: completed
  - id: add-playwright-bdd
    content: Convert browser tests to Playwright BDD with Web View POMs and HAR fixtures.
    status: completed
  - id: validate-feedback
    content: Regenerate artifacts and run targeted and full harness validation commands.
    status: in_progress
isProject: false
---

# Easy CMS Harness Feedback Enhancement Plan

## Scope
Apply the feedback to the harness implementation without editing `.cursor/plans/harness_migration_f0d8d030.plan.md`. The work will revise structure, tooling, Python HTTP surface conventions, browser-surface conventions, tests, and contributor guidance.

## Documentation And Guidance
- Create `CONTRIBUTING.md` as the shared rulebook for humans and agents.
- Include the new rule that future feedback affecting conventions must update `CONTRIBUTING.md`; when a convention is ambiguous, ask the user before choosing.
- Update `AGENTS.md` to reference `CONTRIBUTING.md` for harness, layout, testing, Python, TypeScript, Playwright BDD, SCSS, BEM, and contribution rules, while keeping `CONTEXT.md` and Mermaid validation rules in place.
- Add `Web View` to `CONTEXT.md` as the term for a deterministic visible browser-surface state and Playwright Page Object Model boundary.
- For `Web View`, avoid `screen`, `page`, `POM page`, and `route component`.

## Workspace And Harness
- Move workspace members under the chosen layout:
  - `src/apps/studio/service`
  - `src/apps/studio/web`
  - `src/apps/sync-server/service`
  - `src/apps/sync-server/admin`
  - `src/apps/site-template`
  - `src/packages/python-shared`
  - `src/packages/design-system`
  - `src/packages/shared-types`
- Keep package-local `src/` folders inside Python members, for example `src/apps/sync-server/service/src/easy_cms_sync_server`.
- Update `pyproject.toml`, `pnpm-workspace.yaml`, Orval inputs, Playwright references, `mise` commands, package-local `.gitignore` files, and CI references for the new layout.
- Remove `mise-tasks/harness.sh` and inline the task bodies in `mise.toml` using multiline task syntax.
- Pin `mise.toml` tools to explicit versions from the current resolved harness pass where known, including Python `3.13.14` and pnpm `10.25.0`.
- Update `.github/workflows/ci.yml` to pin GitHub Actions to full commit SHA values with comments showing the readable action tag.
- Extend `.pre-commit-config.yaml` with YAML formatting via `yamlfmt` and TOML formatting via `tombi-toml`, while keeping `prek` and the full `mise run check` hook.

## Python HTTP Surfaces
- Return to `uv_build` for Python packages and make package metadata work with the existing import package names.
- Remove Pyright from Python member tooling; use strict mypy aligned with the `probabilidad` configuration, including the strictness options shown in `D:/repositories/probabilidad/pyproject.toml`.
- Keep examples out of shared `BaseModel` declarations. Define examples in each slice `api/examples.py` as valid `BaseModel` instances plus `model_dump()` constants used by FastAPI route decorators.
- Replace generic string fields in shared contracts with enums where the values are closed, such as service identity and health status.
- Remove trivial `api/schemas.py` re-export files; import response models directly from their owning slice or service boundary.
- Move responses out of `src/packages/python-shared`; response models should live in the corresponding Python HTTP surface. Shared Python code should only hold shared value objects and enums used by multiple Python HTTP surfaces, such as health status and service identity.
- Make application services and returned domain objects Pydantic `BaseModel`s.
- Keep service methods returning domain objects, not HTTP response models.
- Make exceptions dataclasses.
- Use relative imports inside each package. Do not import from grandchild modules; each package or slice `__init__.py` must re-export its public symbols.
- Keep `Provide["health_service"]` style string identifiers in endpoint dependencies to avoid circular imports.
- Move package-level container creation and wiring into `__main__.py`; wire at the whole package level, not individual endpoint modules.
- Remove unnecessary `from __future__ import annotations`; if retained for a circular import, document why with a short comment.
- Move route `responses={...}` dictionaries into `api/examples.py` constants.
- Add clear type aliases for verbose slice list types.

## Browser Surfaces
- Use React 19 across browser-surface packages and shared browser packages.
- Add `ts-pattern` and model every UI state as a string-const enum or equivalent const map. Components should `match` state to view components, so the UI flow is deterministic.
- Replace inline styling with SCSS files using BEM class names.
- Prefer semantic HTML elements over generic containers.
- Keep Orval output limited to types, connectors, and hooks; no mock/MSW output.
- Update generated hook consumption after Orval regeneration so version badge components read the generated response shape correctly.

## Playwright BDD Tests
- Add Playwright BDD using `@vitalets/playwright-bdd`.
- Define Gherkin scenarios for version badges and HAR replay.
- Replace direct `page.goto(...)` usage in tests with Page Object Models. Each POM represents one Web View, and its methods return `self` or the next POM.
- Keep browser-surface tests Playwright-only, with committed HAR fixtures.

## Test Structure And Assertions
- Move Python tests so the test tree mirrors the source tree one-to-one, for example service tests for `slices/health` live under matching test folders.
- Remove raw shared `BaseModel` instantiation tests from `src/packages/python-shared`; validate shared contracts through Python HTTP surface tests instead.
- Add `syrupy` snapshot testing for HTTP responses.
- For every FastAPI route test, use a pytest fixture to build the expected Pydantic model, parse response text through the expected model type with `model_validate_json(...)`, then compare the validated `model_dump()` to a `syrupy` snapshot.
- Store expected response models in fixtures instead of inline expected-output dictionaries.

## Validation
- Regenerate OpenAPI and Orval artifacts locally after structural changes.
- Run targeted gates first: `mise run check sync-server-service`, `mise run check studio-service`, `mise run check sync-server-admin`, and `mise run check studio-web`.
- Run the full gates before completion: `mise run check`, `mise run check:ci`, `mise run build`, and `prek run --all-files`.
- Re-run `npx -y @probelabs/maid docs/` if any Markdown with Mermaid diagrams changes.