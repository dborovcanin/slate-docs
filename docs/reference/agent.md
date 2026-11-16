# Ask the Agent (`:ask`)

`:ask <prompt>` sends a question to the agent CLI you already have (Claude Code, Codex, or your own command) and shows its answer. The desktop app keeps a follow-up input below the scrollable conversation; `Enter` sends the prompt, and **Insert latest** inserts the latest answer at the cursor. In the terminal app, `Enter` inserts the answer from the result view. Ask keeps one conversation across notes until you clear it. With note access on, the agent can also read your other notes and edit notes through Slate's [MCP server](mcp.md). It is **off by default** in both desktop and terminal apps.

- [Setup](#setup)
- [Using it](#using-it)
- [What is sent, and what the agent can reach](#what-is-sent-and-what-the-agent-can-reach)
- [Edits the agent makes](#edits-the-agent-makes)
- [Custom agents](#custom-agents)
- [Limits](#limits)

## Setup

### 1. Install and sign in to an agent CLI

Install [Claude Code](https://code.claude.com/docs/en/setup) or
[Codex CLI](https://github.com/openai/codex) using the vendor's instructions for
your OS. Installing a desktop agent app alone does not necessarily install its CLI.
In a terminal, verify the executable you intend Slate to use:

```sh
claude --version
# or
codex --version
```

Run `claude` and complete sign-in (use `/login` inside Claude Code if needed),
or run `codex login` for [Codex authentication](https://developers.openai.com/codex/auth/).
Finish authentication before invoking Ask: Slate's background worker cannot
answer an interactive login prompt. Slate does not have its own API-key or model
configuration. Built-in presets use the CLI's default model and authentication;
they deliberately suppress user settings/configuration as described below.

### 2. Locate Slate's config

Edit the existing `config.toml`; merge the examples into its `[agent]` and `[mcp]`
sections rather than adding duplicate sections.

| OS | Config path |
| --- | --- |
| Linux | `$XDG_CONFIG_HOME/slate/config.toml`, default `~/.config/slate/config.toml` |
| macOS | `~/Library/Application Support/io.github.slate/config.toml` |
| Windows | `%APPDATA%\github\slate\config\config.toml` |

These are native Slate paths. Slate running inside WSL uses the Linux path.
The complete defaults are in [config.example.toml](https://github.com/dborovcanin/slate/blob/main/config.example.toml).

### 3. Choose the agent and note access

```toml
[agent]
enabled = true
preset = "claude"       # "claude", "codex", or "custom"
context = "selection"   # "selection", "note", or "none"
notes = "read"          # "write", "read", or "none"
timeout_seconds = 300  # 1..3600

[mcp]
enabled = true         # Required for Slate note tools
allow_delete = false   # Ask never gets delete_note, even when this is true
```

To switch to Codex, change only `preset = "codex"`. Do not add `argv` to a
built-in preset; it is accepted only for `preset = "custom"` (see below).
Unknown settings, invalid enum values, and invalid combinations are errors.
There is no separate Slate model selector or extra-arguments setting for presets.

`context` selects what is attached from the current note on each turn.
`notes` controls the agent's MCP access to the note database. They are independent:
`context = "note", notes = "none"` sends the current note without starting a note
server; `context = "none", notes = "read"` lets the agent retrieve notes through tools.
Neither setting removes earlier conversation history; use `/clear` to start fresh.

Without `[mcp] enabled = true`, requests run with no note tools. To use those tools,
install the `slate` terminal executable alongside the desktop app or put it on
`PATH`. Slate checks beside its running executable first, then falls back to
`slate` on `PATH`. The MCP server reads the same native Slate config and database.
No MCP configuration needs to be added to the agent CLI: Slate generates it for
each request. Custom commands must explicitly consume that generated config.

### 4. Check executable discovery and send a request

On Linux/macOS, `command -v claude`, `command -v codex`, and `command -v slate`
show the executable paths. On Windows, use `where.exe claude`, `where.exe codex`,
and `where.exe slate` (subject to the native Windows limitations below).

Slate inherits the environment of the process that launched it. Shell aliases
and functions are not executable commands. If Ask reports `cannot start`, launch
`slate-gui` from the terminal where the CLI works, or put the actual executable's
directory on the desktop session's `PATH`. Finder and other desktop launchers
can have a different `PATH` from your shell. A custom preset can use an absolute
executable path; switching to custom also makes you responsible for CLI flags and
MCP integration. `argv` does not expand `~`, environment variables, pipes or shell code.

Open an ordinary, unencrypted note and run `:ask Say hello`. For a note-access
check, use `notes = "read"` and ask it to read the current note with the Slate tool.
Check the returned answer, not just whether the agent process started.
The config reloads on every request, so changing the preset needs no restart.

### Platform status

| Platform | Slate Ask status |
| --- | --- |
| Linux | Tested with isolated custom-agent/MCP and GUI/terminal checks. Built-in preset qualifications are listed under tool access below. |
| macOS | Uses the same Unix process-group runner as Linux, but native builds and agent interaction are not qualified. Check desktop `PATH`, authentication, and the installed MCP executable on the target Mac. |
| Native Windows | Not fully qualified. Sibling MCP lookup currently checks `slate`, not `slate.exe`, so PATH fallback may be needed. Cancellation kills the immediate child rather than the entire agent/MCP process tree. Do not treat descendant cleanup as guaranteed. |

A vendor CLI supporting an OS does not establish that Slate's integration has
been tested on that OS. These limits describe the current implementation; this
setup does not change platform support.

## Using it

| Key / command | Action |
| --- | --- |
| `:ask <prompt>` | Ask; the view opens while the agent works |
| `:ask` | Open the existing conversation and follow-up prompt |
| `/clear` (in the prompt), or `:ask /clear` | Clear the conversation locally |
| Clear context (desktop button) | Clear the conversation locally |
| `Shift+Enter` | Add a line break while typing the prompt |
| `Esc` | Cancel a running request, or close the view |
| `Enter` | Send the desktop prompt; insert the answer from the terminal result view |
| Insert latest / Copy latest (desktop buttons) | Insert or copy the latest answer |
| Stop (desktop button) | Cancel the run and keep the conversation open |
| `ArrowUp` / `ArrowDown` (terminal), wheel / scrollbar (desktop) | Scroll the conversation |
| `/` (terminal result view) | Open a follow-up prompt |

In the desktop app the input remains available while a reply is running, so you can draft the next prompt. Send it after the current request finishes.

Long prompts wrap in both apps; pasted line breaks are preserved. In the desktop app, click the close button or press `Esc` to cancel or close Ask; clicking outside the dialog keeps it open.

Agents usually take 10–60 seconds. The terminal shows elapsed time; the desktop shows the running request. The note cannot be edited through the Ask dialog while the agent runs. One request runs at a time: a new one is refused until the previous one has stopped.

The open note is saved before the agent starts. If that save fails (for example because the note changed elsewhere), nothing is sent. `:ask` is refused for a locked note and for an encrypted one, even when it is unlocked.

## Conversation context

Closing Ask, inserting a reply, or switching notes keeps the conversation.
Each successful exchange retains the prompt, supplied note context, note identity,
and answer. Follow-ups send those exchanges together with the current prompt and
fresh context chosen by `[agent] context`. Earlier note contexts are snapshots; a
context unchanged since the previous exchange is kept once, not repeated per turn.
Failed or cancelled requests are not added; completed note writes still remain.

Type `/clear` in the prompt or click **Clear context** in the desktop header to
start over. This does not edit notes or contact the agent. History is held in
memory for the current app window and is lost on exit. It retains prompts and
answers rather than the CLI's internal tool trace. An oversized conversation
asks you to clear it instead of silently forgetting older exchanges.

## What is sent, and what the agent can reach

Everything in the prompt goes to the agent's model provider. The prompt holds:

- your prompt text and retained conversation history;
- the context `[agent] context` selects: the selection when there is one (`"selection"`), the whole open note (`"note"`), or nothing (`"none"`);
- the open note's id and title.

Whatever the agent reads through the note tools is sent to the model as well.

Note access is set by `[agent] notes` and **enforced by Slate's own server**, which Slate starts for the request in that mode:

| `notes` | The agent can |
| --- | --- |
| `"write"` | Read, search, create, edit, rename and archive notes and manage collections. Never delete, whatever `[mcp] allow_delete` says |
| `"read"` | List, search and read notes |
| `"none"` | Nothing: no Slate server is started |

Encrypted notes stay unreachable in every mode, as for any MCP client.

The built-in presets also narrow the agent itself:

- **`claude`** runs with no built-in tools (no file access, shell or web), none of your other MCP servers, and none of your Claude Code settings or hooks. Only the Slate note tools for the chosen mode are allowed. Checked against Claude Code 2.1.322.
- **`codex`** runs without your Codex configuration and MCP servers, in its read-only sandbox, with its shell tools switched off. These flags are accepted by Codex 0.167.1, but their effect has not been confirmed by a real run yet: until it is, assume the Codex preset may read any file you can. Codex 0.167.1 also still reads `~/.codex/hooks.json` with these flags.

Slate does not sandbox the agent process: it runs as you, in an empty temporary directory so it picks up no project instructions (`AGENTS.md`, `CLAUDE.md`). What keeps a preset away from your files is that agent's own options above.

## Edits the agent makes

Agent writes go through the same revision-checked saves as any MCP client and are recorded in note history.

While the agent runs, Slate does not reload the open note. When the agent's processes have stopped, whether it finished, failed or was cancelled, its writes to the open note come into the editor as **one undo step**, and the view says `the agent changed this note (u undoes)`. Inserting the answer afterwards is a separate undo step.

Writes the agent completed before a cancel or a failure stay. If you switched to another note meanwhile, nothing is applied to that note; the writes are stored and `:history` can bring the earlier version back, as for edits to other notes.

Quitting Slate cancels a running agent first and waits up to five seconds for it. Unix kills the process group; native Windows descendant cleanup remains incomplete (see platform status).

## Custom agents

`preset = "custom"` runs a command that implements the stdin/stdout contract:

```toml
[agent]
enabled = true
preset = "custom"
argv = ["/absolute/path/to/my-agent", "run"]
```

The command runs as given, without a shell, with:

- the prompt on standard input, and its answer expected on standard output;
- an empty temporary working directory;
- `SLATE_AGENT_MCP_CONFIG`: the path of a JSON file (`{"mcpServers": {...}}`) naming Slate's server in the mode `notes` asks for, or no server for `"none"`.

Slate gives no guarantee about a custom command's own tools: it is a trusted executable with your permissions. Note access still goes through Slate's server only if the command uses that file. [`scripts/fake_agent.py`](https://github.com/dborovcanin/slate/blob/main/scripts/fake_agent.py) is a small working example that reads the file and talks to the server.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Agent is off | Set `[agent] enabled = true` in the config path shown in the error. |
| Cannot start `claude`, `codex`, or custom executable | Check the actual executable, permissions, and the environment/PATH of Slate's launcher; use absolute paths for custom commands. |
| Agent exits with a login/authentication error | Sign in from a terminal as the same OS user, then retry. |
| Unknown flag | Compare the installed CLI version with the preset flags in `crates/app-core/src/agent.rs`. CLI releases can change compatibility; do not remove isolation flags blindly. |
| No note tools / MCP server failed | Enable `[mcp]`, verify the terminal `slate` executable is discoverable, and check its version and config path. |
| Agent has no selection context | Select text before opening Ask, or choose `context = "note"`. The default `"selection"` sends nothing when no selection exists. |
| Old note details still appear after changing context | Conversation history is separate; clear it with `/clear` or Clear context. |
| Conversation is full | Use `/clear`; Slate refuses an oversized context instead of silently dropping older exchanges. |
| Timed out / no answer | Check CLI authentication and stdout behavior; a successful custom command must print nonempty answer text. Increase `timeout_seconds` only within 1..3600. |

## Limits

- No streaming: the answer appears when the agent is done.
- Output over 4 MiB, or a run longer than `timeout_seconds` (1–3600), is stopped with an error.
- File-backed notes (`slate <file>`) can be the context, but the note tools cannot reach them.
