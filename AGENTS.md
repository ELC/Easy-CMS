# AGENTS.md

## Terminology is non-negotiable

[`CONTEXT.md`](./CONTEXT.md) is the single source of truth for project vocabulary. Every message you produce — chat replies, plans, commit messages, PR descriptions, code comments, identifiers, docs — MUST conform to it.

## The rule

Before sending any message, validate it against `CONTEXT.md`:

1. **Re-read `CONTEXT.md`** at the start of every task. Do not rely on memory from prior turns.
2. **Use the defined term verbatim** (preserving capitalization) whenever you refer to a concept that has an entry.
3. **Never use a word from any `_Avoid_` list** to refer to the concept it shadows. This applies even in casual phrasing, examples, analogies, and code identifiers.
4. **If a concept you need has no entry, or an existing entry is wrong**, stop and follow the [`domain-modeling`](./.cursor/skills/domain-modeling/SKILL.md) skill before continuing. Do not invent vocabulary on the fly.
5. **Self-check before sending.** Scan your draft for any term in an `_Avoid_` list. If you find one, rewrite the sentence using the defined term.

## When `CONTEXT.md` is wrong or incomplete

Do not silently invent new terms. When you hit a gap, a fuzzy term, or a conflict with what `CONTEXT.md` says, follow the [`domain-modeling`](./.cursor/skills/domain-modeling/SKILL.md) skill — that is the canonical workflow for resolving terminology, updating `CONTEXT.md` inline, and deciding whether an ADR is warranted. In short:

- Read [`domain-modeling/SKILL.md`](./.cursor/skills/domain-modeling/SKILL.md) and apply it before changing the model.
- **On any ambiguity, ask the user. Never guess, never pick a term yourself, never "figure it out" from context.** This includes: which of two existing terms applies, whether a new term is needed, what to name a new term, and which `_Avoid_` words to list. Use `AskQuestion` to present the alternatives.
- Only after the user has resolved the ambiguity, edit `CONTEXT.md` in the same change, following [`CONTEXT-FORMAT.md`](./.cursor/skills/domain-modeling/CONTEXT-FORMAT.md), and call out the addition in your message.

## Scope

This rule applies to all natural-language output and to code-level naming (types, functions, variables, files, routes, database tables, event names). Vocabulary drift in code is as harmful as drift in prose.

## Contributor conventions

Follow [`CONTRIBUTING.md`](./CONTRIBUTING.md) for harness, workspace layout, Python HTTP surface, browser surface, testing, generated artifact, and Playwright BDD conventions. If future feedback changes a convention, update `CONTRIBUTING.md` in the same change. If the convention is ambiguous, ask the user before choosing.

## Harness

Use `mise run check` before declaring implementation complete. While iterating, prefer targeted commands such as `mise run test sync-server-service`, `mise run typecheck studio-service`, or `mise run lint studio-web`; finish with the full gate.

Keep executable orchestration in `mise.toml` and `.pre-commit-config.yaml`. Use `prek` for Git hooks, and keep `AGENTS.md` focused on guidance rather than long command lists.

## Mermaid diagrams

Every Mermaid diagram authored or edited in this repository (anywhere — `docs/`, ADRs, READMEs, the development plan, inline in chat-produced files) MUST be validated with [`maid`](https://github.com/probelabs/maid) before you consider the change done.

Run it via `npx`, no install required:

```bash
# validate a single Markdown or .mmd file
npx -y @probelabs/maid path/to/file.md

# validate every diagram under docs/ recursively
npx -y @probelabs/maid docs/
```

Rules:

1. **Exit code 0 with zero warnings is the bar.** A diagram that "renders fine in mermaid live" is not enough — `maid` is stricter (it catches `+` / `-` / reserved words like `and`, `activate`, `create`, `details` inside sequence-diagram messages, and flowchart edge labels that need pipe form `<-->|text|`). These are real latent bugs.
2. **Do not rely on `mermaid`-the-library + `jsdom`, on `mmdc`, or on visual rendering** as a substitute. They are looser parsers and let real bugs through.
3. If `maid` reports an error or warning, fix the diagram source until the output is `Valid`. Do not suppress, ignore, or work around diagnostics.
4. Prefer rephrasing message text over tricks: replace `+` with a comma, avoid `and` / `or` / `create` / `activate` / `deactivate` as bare words inside messages, and quote multi-word labels in flowcharts.
