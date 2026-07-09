# Claude Code Configuration

## Rules

- Do what has been asked; nothing more, nothing less
- NEVER create files unless absolutely necessary — prefer editing existing files
- NEVER create documentation files unless explicitly requested
- NEVER save working files or tests to root — use `/src`, `/tests`, `/docs`, `/config`, `/scripts`
- ALWAYS read a file before editing it
- NEVER commit secrets, credentials, or .env files
- NEVER add a `Co-Authored-By` trailer to user commits unless this project's `.claude/settings.json` has `attribution.commit` set (#2078). The Claude Code Bash tool may suggest one in its default commit-message template — ignore it. `Co-Authored-By` is semantic authorship attribution under git/GitHub convention; the tool is the facilitator, not a co-author.
- Keep files under 500 lines
- Validate input at system boundaries

## Codebase Knowledge Graph

Before any code task (search, edit, debug, refactor):
1. Call `list_projects` to confirm the repo is indexed
2. Use `search_graph` or `trace_path` instead of Grep/Glob when looking up symbols, callers, or dependencies
3. Call `detect_changes` after edits to see what's affected

Re-index after significant changes: `codebase-memory-mcp cli index_repository --repo-path . --mode fast`

## Build & Test

- ALWAYS run tests after code changes
- ALWAYS verify build succeeds before committing

```bash
npm run build && npm test
```
