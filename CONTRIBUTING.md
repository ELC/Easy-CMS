# Contributing

This file is the shared convention guide for humans and agents working on Easy CMS. If future feedback changes a convention, update this file in the same change. If the feedback is ambiguous, ask the user before choosing.

## Language

- Re-read `CONTEXT.md` at the start of each task and use its terms exactly.
- When a new project term is needed, update `CONTEXT.md` through the domain-modeling workflow before using the term in code or prose.
- Use `Web View` for deterministic visible states in browser surfaces and Playwright Page Object Model boundaries.

## Harness

- Use `mise run check` before declaring implementation complete.
- Use targeted commands while iterating, such as `mise run test sync-server-service` or `mise run lint studio-web`, then finish with the full gate.
- Keep executable orchestration in `mise.toml` and `.pre-commit-config.yaml`.
- Use `prek` for Git hooks.
- Keep one root `uv.lock` and one root `pnpm-lock.yaml`.

## Workspace Layout

- Workspace members live under `src/apps` and `src/packages`.
- Python members keep package-local `src/` folders, for example `src/apps/sync-server/service/src/easy_cms_sync_server`.
- Keep the root `.gitignore` minimal. Package-local `.gitignore` files own package-local artifacts.

## Python HTTP Surfaces

- Python packages use `uv_build`.
- Python HTTP surfaces use FastAPI, Pydantic v2, `dependency_injector`, and vertical slices.
- Use relative imports inside a package. Do not import from grandchild packages; re-export public symbols through each package or slice `__init__.py`.
- Keep package-level container creation and wiring in `__main__.py`; wire at the whole package level.
- Endpoint dependencies use string identifiers such as `Provide["health_service"]`.
- Application services and returned domain objects are Pydantic `BaseModel`s.
- Service methods return domain objects, not HTTP response models.
- HTTP response models live in the corresponding Python HTTP surface.
- Shared Python code owns only shared value objects and enums used by multiple Python HTTP surfaces.
- Exceptions are dataclasses.
- Swagger examples live in each slice `api/examples.py`. Define them as valid Pydantic models and export `model_dump()` constants for FastAPI route decorators.
- Avoid trivial re-export files such as `api/schemas.py`.
- Use strict mypy only; do not add Pyright unless the user explicitly changes this convention.

## Python Tests

- Test trees mirror the package tree they cover.
- Route tests use `httpx.AsyncClient` with ASGI transport and AnyIO.
- Every route test validates response text with `model_validate_json(...)` before comparing output.
- Expected response models live in fixtures.
- Use `syrupy` snapshots against validated `model_dump()` output.
- Do not test raw shared `BaseModel` construction directly; cover shared contracts through Python HTTP surface tests.
- Keep tests no-mock. Use local resources first and in-memory fakes only when no suitable local resource exists.

## Browser Surfaces

- Use React 19.
- Use strict TypeScript and `ts-pattern`.
- Model UI state with string const values and map states to components with `match`.
- Use semantic HTML.
- Put styling in SCSS files with BEM class names; do not use inline styling.
- Orval output is limited to types, connectors, and hooks. Do not generate mock or MSW artifacts.

## Playwright BDD

- Use `@vitalets/playwright-bdd`.
- Browser-surface tests are Playwright-only.
- Define Gherkin scenarios for user-visible behavior.
- Page Object Models represent one Web View, not an entire browser surface.
- A Page Object Model method returns `self` or another Web View object.
- Avoid `page.goto(...)` outside Page Object Model initialization.
- Keep HAR fixtures checked in and update them through the harness command.

## Generated Artifacts

- Regenerate OpenAPI and Orval artifacts locally through `mise`.
- Check generated artifacts into the repository.
- Linux CI/CD consumes checked-in generated artifacts but does not regenerate them.
