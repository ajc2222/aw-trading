# Herdr

Herdr is a terminal-workspace manager for coding agents, installed globally on this
machine (not part of this repo). It organizes terminals into **workspaces → tabs →
panes**, recognizes coding agents (Claude, Codex, etc.) running inside those panes,
and exposes everything through the `herdr` CLI so one agent can inspect or delegate
work to another.

- CLI: `/home/aj/.local/bin/herdr` (`herdr --version` → 0.8.2 at time of writing)
- Config: `/home/aj/.config/herdr/config.toml`
- Logs: `/home/aj/.config/herdr/herdr.log`, `herdr-client.log`, `herdr-server.log`
- Socket: `/home/aj/.config/herdr/herdr.sock`
- Home: https://herdr.dev

## Am I running inside Herdr?

```bash
test "${HERDR_ENV:-}" = 1
```

If that fails, this session isn't inside a Herdr-managed pane and none of the control
commands below apply. When it's set, Herdr also injects:

```bash
echo "$HERDR_WORKSPACE_ID" "$HERDR_TAB_ID" "$HERDR_PANE_ID"
```

These identify the calling pane's own workspace/tab/pane IDs (e.g. `wA`, `wA:t1`,
`wA:p1`). IDs are opaque, stable, and never reused once closed.

## Two primitives — pick the right one

- **Pane commands** control raw terminals: shells, tests, servers, arbitrary input/output.
  A pane exists whether or not an agent is in it.
- **Agent commands** control the recognized coding agent occupying a pane, and understand
  its lifecycle (`idle`, `working`, `blocked`, `done`, `unknown`).

`agent start` requires an *already-existing, available* shell pane at its prompt — it
never creates or splits layout itself. Split first, then start an agent in the new pane.

## Discovering current state

```bash
herdr workspace list
herdr tab list --workspace "$HERDR_WORKSPACE_ID"
herdr pane current --current
herdr pane list --workspace "$HERDR_WORKSPACE_ID"
herdr pane layout --pane "$HERDR_PANE_ID"
herdr agent list
```

Everything returns JSON — read IDs from `.result.*`, never guess them from sidebar
order or from examples in this doc.

## Splitting a pane

```bash
herdr pane split --current --direction right --cwd "$PWD" --no-focus
```

- Use `right` for a narrow/tall caller pane, `down` for a wide one (check with
  `herdr pane layout` first).
- `--cwd "$PWD"` preserves the working directory in the new pane.
- `--no-focus` keeps the user's view on the calling pane.
- New pane ID comes back at `.result.pane.pane_id`.

## Starting and delegating to an agent

```bash
herdr agent start <name> --kind <kind> --pane <pane-id>
```

- `<name>` must match `[a-z][a-z0-9_-]{0,31}` and be unique among live agents.
- Supported kinds (`herdr agent` lists them): `pi claude codex gemini cursor devin agy
  cline omp mastracode opencode copilot kimi kiro droid amp grok hermes kilo qodercli
  qwen maki`.
- Native agent CLI args go after `--`.
- The target pane must be a plain shell at its prompt — no foreground command/editor/agent.

Delegate a task and wait for it to settle:

```bash
herdr agent prompt <name> "<task>" --wait --timeout 120000
```

`--wait` waits for the first settled `idle`/`done`/`blocked`. Only add `--until <state>`
for a state-specific wait, e.g. waiting for an already-running agent to ask a question:

```bash
herdr agent wait <name> --until blocked --timeout 120000
```

Check in on it:

```bash
herdr agent get <name>
herdr agent read <name> --source recent-unwrapped --lines 120
```

`recent-unwrapped` is the right read source for logs/transcripts. If more `--lines`
doesn't reveal more, the agent is probably on the terminal's alternate screen
(unrecoverable via scrollback) — fall back to asking it to write its answer to a file
and reading that file instead.

Other agent commands: `send-keys` (logical keys like `esc`, `ctrl+c`), `rename`,
`focus`, `attach [--takeover]`, `explain`.

## Running a plain command in another pane (no agent)

```bash
herdr pane split --current --direction right --cwd "$PWD" --no-focus
herdr pane run <pane-id> "npm test"
herdr pane wait-output <pane-id> --match "test result" --timeout 120000
herdr pane read <pane-id> --source recent-unwrapped --lines 120
```

`pane wait-output` supports `--match <literal>` or `--regex <rust-regex>`, and searches
the existing snapshot immediately, so already-present output can match right away.

Read sources: `visible` (rendered viewport), `recent` (recent output incl. soft wraps),
`recent-unwrapped` (soft wraps joined — best for logs), `detection` (plain-text snapshot
used for agent recognition).

## Guardrails

- Only touch panes/tabs/workspaces this session created; don't close ones it didn't.
- Always target with `--current`, an explicit pane ID, or a unique agent name — never
  rely on another client's UI-focused pane.
- Don't create a new workspace/tab/worktree unless the user explicitly asks for that
  topology.
- Parse IDs from JSON responses, never from examples or assumed order.
- Never run `herdr server stop` unless explicitly asked to stop the server (it kills
  every managed pane's process too).
- Never kill the main Herdr process; use a named test session for isolated experiments.

## Getting the authoritative docs

The installed binary is the source of truth and can drift from this file:

```bash
herdr --help          # top-level command list
herdr agent            # subcommand help for a group, e.g. agent/pane/workspace/tab
herdr --skill          # full agent-facing skill doc (re-run if this file feels stale)
```
