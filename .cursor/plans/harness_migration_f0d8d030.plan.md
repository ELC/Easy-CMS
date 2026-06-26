---
name: harness migration
overview: Apply the quality harness patterns from `probabilidad` to Easy CMS while adapting them to a multi-package `uv` workspace, `mise` orchestration, `prek` hooks, and `pnpm` browser surfaces.
todos:
  - id: root-harness
    content: Add root workspace harness files for uv, mise, prek, pnpm, and Python 3.13.
    status: pending
  - id: python-members
    content: Create typed FastAPI Python workspace members with version and health endpoints plus no-mock tests.
    status: pending
  - id: browser-members
    content: Create pnpm browser-surface skeletons with version badges and strict TypeScript checks.
    status: pending
  - id: version-contract
    content: Add version alignment checks for semantic-version pairs and Generated Site CalVer.
    status: pending
  - id: agent-guidance
    content: Update AGENTS.md with concise harness instructions pointing to mise and prek.
    status: pending
  - id: validate-harness
    content: Run and document the full harness validation commands.
    status: pending
isProject: false
---

# Easy CMS Harness Migration Plan

## Scope
Add the repository harness only. Do not copy Jupyter Book, scientific, Binder, or notebook-specific pieces from `probabilidad`. The target is a multi-package Easy CMS workspace with strict Python and TypeScript checks, no-mock tests, 100% Python coverage, typed FastAPI health/version endpoints, OpenAPI-driven browser-surface connectors, and visible version badges.

Primary references:
- [D:/repositories/probabilidad/.pre-commit-config.yaml](D:/repositories/probabilidad/.pre-commit-config.yaml)
- [D:/repositories/probabilidad/.python-version](D:/repositories/probabilidad/.python-version)
- [D:/repositories/probabilidad/pyproject.toml](D:/repositories/probabilidad/pyproject.toml)
- [D:/repositories/probabilidad/AGENTS.md](D:/repositories/probabilidad/AGENTS.md)
- [D:/repositories/upskilling/backend/src/upskills/__main__.py](D:/repositories/upskilling/backend/src/upskills/__main__.py)
- [D:/repositories/upskilling/backend/src/upskills/api/app.py](D:/repositories/upskilling/backend/src/upskills/api/app.py)
- [D:/repositories/upskilling/backend/src/upskills/api/server.py](D:/repositories/upskilling/backend/src/upskills/api/server.py)
- [D:/repositories/upskilling/backend/src/upskills/injections/containers.py](D:/repositories/upskilling/backend/src/upskills/injections/containers.py)
- [Orval OpenAPI generator](https://orval.dev/)
- [D:/repositories/Easy-CMS/AGENTS.md](D:/repositories/Easy-CMS/AGENTS.md)
- [D:/repositories/Easy-CMS/docs/development-plan.md](D:/repositories/Easy-CMS/docs/development-plan.md)

## Decisions To Encode
- Use `uv` workspaces: each Python member gets its own `pyproject.toml`, while the root workspace owns a shared `uv.lock`.
- Use separate `uv` dependency groups so CI/CD jobs can run `uv sync --group <group>` without installing every development dependency.
- Use `mise` as the repository-wide command surface. `mise` tasks call the member-native tools: `uv` for Python packages and `pnpm` for TypeScript/React/Astro surfaces.
- Implement parameterized `mise` tasks as standalone task scripts. Use a `mise`-managed POSIX shell where possible.
- Use `prek` for Git hooks. `.pre-commit-config.yaml` runs the full repository check.
- Use `pnpm` workspaces for browser surfaces.
- Use Python `3.13`, matching `probabilidad`.
- Use `semantic-version` for Python semantic-version parsing and validation.
- Python package versions are the source of truth for CMS Studio and Platform Admin panel paired browser-surface versions.
- Python HTTP surfaces read their runtime version with `importlib.metadata.version(...)` from installed package metadata.
- Generated Site uses hardcoded CalVer in `YYYY.0M.MINOR` format, for example `2026.06.0`.
- Keep the root `.gitignore` minimal. Each package owns its own `.gitignore` so the repository can be split into smaller repositories later with less cleanup.
- Follow the `upskilling` Python HTTP surface structure as a base: keep `__main__.py`, `app_factory`, `server_factory`, `dependency_injector`, and direct service injection, but organize Easy CMS routes by vertical slice.
- Generate browser-surface connectors, types, and hooks with Orval from FastAPI-generated `openapi.json`.
- Use nested workspace members for mixed surfaces: `apps/studio/service`, `apps/studio/web`, `apps/sync-server/service`, and `apps/sync-server/admin`.
- Use role-specific package names for parameterized tasks: `studio-service`, `studio-web`, `sync-server-service`, `sync-server-admin`, `site-template`, and `python-shared`.
- Forbid Orval mock/MSW generation. Browser-surface tests use Playwright with committed HAR recordings.
- OpenAPI and Orval artifacts are checked in and regenerated locally through `mise`; Linux CI/CD must not generate or touch them.
- Use `mise run check` for the full Windows local harness and `mise run check:ci` for the Linux CI/CD subset.
- Every handled domain error response is RFC 9457 problem details JSON produced by slice-owned exception handlers. FastAPI request validation errors can keep FastAPI's default JSON shape for now.
- Each slice owns checked-in Markdown problem documentation served by its Python HTTP surface at `/problems/{problem_slug}`.
- Each problem page includes at least a title, the problem type URI, and a short detail paragraph.
- Check in one root `uv.lock` and one root `pnpm-lock.yaml` for the monorepo. Future repository splits will create package-local lockfiles.

## Repository Harness Files
Add root-level harness configuration:
- `.python-version` with `3.13`.
- `mise.toml` with pinned tools and repository tasks.
- `.pre-commit-config.yaml` using `prek`-compatible hooks with a full gate calling `mise run check`.
- Root `pyproject.toml` as the `uv` workspace root.
- Root `uv.lock` checked in for the current `uv` workspace.
- Root dependency groups for repository-wide tools only, split by purpose: `lint`, `typecheck`, `test`, `coverage`, `hooks`, `docs`, and `version`.
- The `hooks` group includes `prek` and `poethepoet`, and hook installation/use is documented through `prek`.
- `pnpm-workspace.yaml`, root `package.json`, and root `pnpm-lock.yaml` for TypeScript/Astro surfaces.
- Keep root `.gitignore` minimal, limited to repository-wide artifacts. Add package-local `.gitignore` files for package-local artifacts such as `node_modules/`, `.venv/`, `.ruff_cache/`, `.mypy_cache/`, coverage output, and build output. Do not ignore checked-in OpenAPI, Orval, or HAR artifacts.
- Update `AGENTS.md` to tell agents to use `mise run check` as the harness entrypoint while preserving the existing vocabulary and Mermaid rules.

## Python Workspace Members
Create minimal typed FastAPI package skeletons:
- `apps/sync-server/service/pyproject.toml` and `src/easy_cms_sync_server/`.
- `apps/studio/service/pyproject.toml` and `src/easy_cms_studio/` for the CMS Studio sidecar.
- `packages/python-shared/pyproject.toml` and `src/easy_cms_shared/`.

Each Python HTTP surface gets:
- `GET /health` returning a Pydantic v2 `BaseModel`.
- `GET /version` returning a Pydantic v2 `BaseModel` with the semantic version from that member's `pyproject.toml`.
- Swagger examples for every request payload and response model, including health and version responses.
- Every endpoint is async.
- Error responses are Pydantic v2 models serialized as RFC 9457 problem details JSON.
- Tests using real FastAPI test clients, no mocks.

Python HTTP surface structure:
- Keep `__main__.py` per package, delegating to `server_factory()`.
- Keep `api/app.py` with one global FastAPI `app_factory()` per package.
- Keep `api/server.py` with the Uvicorn server factory.
- Keep `injections/containers.py` using `dependency_injector`.
- Inject services directly into endpoint functions through dependency injection.
- Register routers, exception handlers, and middleware from all vertical slices in the global FastAPI app.
- Each slice `__init__.py` exports lists of its routers, exception handlers, and middleware. `api/app.py` imports those lists from each slice and registers them in loops.
- Organize code by vertical slice, for example `slices/health`, `slices/version`, and later `slices/articles`, where each slice owns its router, Pydantic v2 schemas, service, domain exceptions, exception handlers, problem documentation, and tests.
- Each slice uses subfolders:
  - `api/` for endpoints, schemas, and `examples.py`.
  - `domain/` for domain types and exceptions.
  - `application/` for services.
  - `problems/` for Markdown problem documentation.
  - `tests/` for tests mirroring the slice.
- Swagger examples live in `api/examples.py` next to `api/endpoints.py` and are imported into FastAPI route decorators.
- Each slice serves support-facing problem documentation from checked-in Markdown at `/problems/{problem_slug}` through its Python HTTP surface.
- Keep shared cross-slice code in explicit shared modules only when two slices already need it.

Python tooling per member:
- Runtime dependencies only where needed: FastAPI, Pydantic v2, `dependency-injector`, Uvicorn, `semantic-version`.
- Dependency groups are split by purpose instead of one large `dev` group:
  - `lint`: Ruff and Pylint.
  - `typecheck`: mypy and pyright.
  - `test`: pytest plus FastAPI/HTTP test support such as `httpx`.
  - `coverage`: pytest-cov and coverage-only support.
  - `version`: semantic-version validation helpers when not needed at runtime.
- `recording`: pytest-recording and VCR-related HTTP recording support when a package talks to external HTTP resources.
- `hooks`: poethepoet for package-local Poe task execution.
- Avoid broad catch-all development groups unless they are only convenience aliases; CI/CD should use the narrow groups.
- Every Python package exposes consistent Poe tasks in its `pyproject.toml`: `lint`, `typecheck`, `test`, `coverage`, `openapi`, `generated-check`, and `build` where applicable.
- Strict mypy, pyright, ruff, pylint, pytest, and coverage configuration in each member `pyproject.toml`.
- Coverage includes both source and tests, with line and branch coverage at 100%.
- Async tests use AnyIO instead of `pytest-asyncio`.
- FastAPI route tests use `httpx.AsyncClient` with ASGI transport under AnyIO.
- HTTP code uses `httpx`; tests that cross external HTTP boundaries use `pytest-recording`/VCR with committed cassettes in the default pytest-recording location.
- Tests use a separate test container installed by an autouse side-effect fixture. The test container overrides only services/providers that require external resources; the rest continue using the production container.
- External-resource replacements prefer real local resources such as SQLite or fakeredis. In-memory fake implementations are allowed only when no suitable local resource exists.

## Browser Surface Skeletons
Create minimal `pnpm` workspace members:
- CMS Studio React SPA under `apps/studio/web`.
- Platform Admin panel under `apps/sync-server/admin`.
- Generated Site under `apps/site-template`.
- Browser surfaces use strict TypeScript, ESLint with typed rules, and Prettier formatting.

OpenAPI and Orval:
- FastAPI emits a checked-in `openapi.json` for each Python HTTP surface through a `mise run openapi [package]` task.
- Orval consumes the checked-in OpenAPI files and creates checked-in TypeScript types, connectors, and hooks for the paired browser surfaces.
- Orval generates TanStack Query hooks using axios.
- Generated OpenAPI and Orval output are repository artifacts, not temporary CI/CD files. They are never hand-edited.
- `mise run openapi [package]` regenerates OpenAPI files; `mise run orval [package]` regenerates Orval output.
- `mise run check [package]` must fail locally if checked-in OpenAPI or Orval output is stale.
- `mise run check:ci [package]` must not generate, validate freshness, or touch OpenAPI/Orval artifacts; it only consumes checked-in files through typecheck/build.
- Orval configuration must disable mock/MSW generation.
- Browser-surface tests use the checked-in generated types.

Version badges:
- CMS Studio badge fetches the CMS Studio sidecar version and must match `apps/studio/service/pyproject.toml`.
- Platform Admin panel badge fetches the Sync Server version and must match `apps/sync-server/service/pyproject.toml`.
- CMS Studio and Platform Admin panel `package.json` versions must match their paired Python `pyproject.toml` versions.
- Generated Site badge renders the CalVer from `apps/site-template/package.json` in `YYYY.0M.MINOR` format.

Testing approach:
- TypeScript strict mode, linting, formatting, and Playwright tests are part of the `mise` harness.
- Version badge tests use Playwright visible assertions against real local processes or HAR replay.
- A repository-level version check verifies Python package versions and paired browser-surface versions stay aligned.
- Browser-surface connector tests should use Orval-generated types and real generated OpenAPI fixtures, not hand-written type duplicates.
- Browser-surface behavior is tested with Playwright only; do not add Vitest or another TypeScript unit test runner in this harness pass.
- Browser-surface tests use Playwright with committed HAR recordings. A first run records HAR files; later runs reuse them.
- HAR files live inside each browser surface test tree, for example `apps/studio/web/tests/fixtures/har/` and `apps/sync-server/admin/tests/fixtures/har/`.
- Every browser surface exposes consistent package scripts: `lint`, `typecheck`, `test`, `test:record`, `build`, and `orval`.

## `mise` Task Shape
Define repository commands that agents and humans use consistently:
- `mise run setup`: install the full local workspace for development.
- `mise run setup:lint`: `uv sync --group lint` plus the pnpm install needed for JavaScript linting.
- `mise run setup:typecheck`: `uv sync --group typecheck` plus the pnpm install needed for TypeScript type checks.
- `mise run setup:test`: `uv sync --group test --group coverage` plus the pnpm install needed for tests.
- `mise` task scripts are standalone scripts and use a `mise`-managed POSIX shell where possible.
- `mise run lint [package]`: sync only lint groups, then run Ruff, Pylint, ESLint, and formatting checks for the requested package or every package when omitted.
- `mise run typecheck [package]`: sync only typecheck groups, then run mypy, pyright, and TypeScript type checks for the requested package or every package when omitted.
- `mise run test [package]`: sync only test groups, then run Python and TypeScript tests for the requested package or every package when omitted.
- `mise run coverage [package]`: sync only test and coverage groups, then run Python tests with 100% line and branch coverage for the requested Python package or every Python package when omitted.
- `mise run openapi [package]`: regenerate checked-in FastAPI `openapi.json` for the requested Python HTTP surface or every Python HTTP surface when omitted.
- `mise run orval [package]`: regenerate checked-in Orval types, connectors, and hooks for the requested browser surface or every browser surface when omitted.
- `mise run generated-check [package]`: verify OpenAPI and Orval generated artifacts are up to date without leaving a diff.
- `mise run har:record [package]`: run Playwright against the real local Python HTTP surface and record committed HAR fixtures for the requested browser surface.
- `mise run har:test [package]`: run Playwright reusing committed HAR fixtures.
- `mise run docs`: sync only docs tooling, then run Mermaid validation with `npx -y @probelabs/maid docs/`.
- `mise run version-check [package]`: sync only version tooling, then verify semantic-version alignment and Generated Site CalVer shape for the requested package or every package when omitted.
- `mise run check [package]`: run the full gate for the requested package or the full repository when omitted.
- `mise run check:ci [package]`: run the Linux CI/CD subset for the requested package or the full repository when omitted. It runs check/build but never regenerates or freshness-checks OpenAPI, Orval, or HAR artifacts.
- `mise run build [package]`: build the requested package or every buildable surface when omitted.

Parameterized package names should match workspace member names, for example:
- `sync-server-service`
- `sync-server-admin`
- `studio-service`
- `studio-web`
- `python-shared`
- `site-template`
- `design-system`
- `shared-types`

Member-native commands stay inside each surface:
- Python commands use `uv run --package <member> poe <command>` after syncing only the dependency groups required by that task.
- Browser commands use `pnpm --filter <member> <script>`.
- The root task dispatch should fail fast with a clear list of valid packages when an unknown package name is supplied.

## `prek` Shape
Adapt the `probabilidad` pre-commit model to Easy CMS with `.pre-commit-config.yaml`:
- Use `prek` as the hook runner.
- `pre-commit` runs `mise run check`.
- The hook is intentionally full-strength because that was chosen in grilling.
- The hook verifies generated artifacts but does not regenerate or stage them. Developers run `mise run openapi`, `mise run orval`, and `mise run har:record` explicitly when contracts change.
- Include standard safety hooks: trailing whitespace, end-of-file fixing, YAML/TOML checks, large-file checks, merge-conflict checks, and private-key detection.
- Include a local hook for `mise run check` so hook behavior and manual agent behavior share one command surface.

## CI/CD Shape
Add Linux CI/CD workflows now, but keep them narrower than the Windows local harness:
- CI/CD runs `mise run check:ci` and `mise run build`.
- CI/CD uses narrow `uv sync --group ...` installs per job.
- CI/CD builds all buildable surfaces: Python packages, browser surfaces, and Generated Site template.
- CI/CD does not run OpenAPI generation, Orval generation, generated freshness checks, HAR recording, or HAR freshness checks.
- CI/CD consumes checked-in generated artifacts only through normal typecheck, test, and build commands.

## AGENTS Guidance
Update [D:/repositories/Easy-CMS/AGENTS.md](D:/repositories/Easy-CMS/AGENTS.md) with a short harness section:
- Use `mise run check` before declaring implementation complete.
- Use parameterized commands while iterating, for example `mise run test sync-server-service`, but finish with the full gate.
- Preserve the existing `CONTEXT.md` and Mermaid validation rules.
- Do not put long command lists into `AGENTS.md`; keep executable orchestration in `mise.toml` and `.pre-commit-config.yaml`.

## Validation
After implementation:
- Run `mise run check`.
- Run `mise run check sync-server-service` and `mise run check studio-service` to prove package-targeted checks work.
- Run `mise run check:ci` and `mise run build` to prove the Linux CI/CD subset commands exist.
- Confirm `prek run --all-files` runs the same gate.
- Confirm `uv lock` creates one shared workspace lockfile.
- Confirm `pnpm install` creates one root `pnpm-lock.yaml`.
- Confirm targeted installs work, for example `uv sync --group lint`, `uv sync --group typecheck`, and `uv sync --group test --group coverage`.
- Confirm `pnpm` workspace install succeeds.
- Confirm root `.gitignore` stays minimal and package-local `.gitignore` files own package-local artifacts.
- Confirm `__main__.py`, `app_factory`, `server_factory`, `dependency_injector`, direct service injection, and vertical-slice router registration are present in both Python HTTP surfaces.
- Confirm Python coverage fails below 100% and passes at 100%.
- Confirm no mock libraries or mock imports exist in tests.
- Confirm tests use the test container pattern for external resources and prefer local resources before in-memory fakes.
- Confirm HTTP tests use `httpx` and `pytest-recording`/VCR where external HTTP is involved, with committed cassettes.
- Confirm async tests use AnyIO instead of `pytest-asyncio`, and route tests use `httpx.AsyncClient` with ASGI transport.
- Confirm every FastAPI endpoint returns a Pydantic v2 `BaseModel` response and has Swagger examples.
- Confirm every FastAPI endpoint is async and examples live in each slice's `api/examples.py`.
- Confirm every handled domain error response uses RFC 9457 problem details JSON and every problem type has a served Markdown-backed support page.
- Confirm generated OpenAPI files are checked in and consumed by Orval to produce checked-in TypeScript types, connectors, and hooks.
- Confirm `mise run generated-check` fails if checked-in OpenAPI or Orval artifacts are stale.
- Confirm Orval mock/MSW output is disabled.
- Confirm Orval generates TanStack Query hooks using axios.
- Confirm Playwright tests can record HAR fixtures with `mise run har:record <package>` and reuse them with `mise run har:test <package>`.
- Confirm Playwright is the only browser-surface test runner.
- Confirm version badges and version endpoints agree for CMS Studio and Platform Admin panel.
- Confirm Generated Site badge matches `YYYY.0M.MINOR`.
- Confirm `npx -y @probelabs/maid docs/` remains valid.