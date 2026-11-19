# Configuration

Slate reads config from:

- `$XDG_CONFIG_HOME/slate/config.toml`
- fallback: `~/.config/slate/config.toml`

The file is auto-generated on first run.

The complete template is [config.example.toml](https://github.com/dborovcanin/slate/blob/main/config.example.toml), which
also supplies the generated file. It lists supported settings and commented
script, keybinding and currency examples. Existing files are not automatically
rewritten when Slate adds settings.

`[editor] command_popup` defaults to `true` and controls contextual suggestions
in the GUI, leaving its bottom command bar visible. The TUI always uses the
bottom bar with inline word completion and ignores this setting. An explicit value overrides the desktop's remembered
preference. Without one, old `gui-settings.json` values `"command_bar": "bottom"`
and `"command_bar": "popup"` are preserved as popup off/on respectively.

## Example

```toml
[gui]
# Desktop effects; false skips all animations for immediate presentation.
animations = true
# Ctrl+P switcher lists pinned notes by edit time instead of first.
switcher_ignore_pins = false

[gui.dialog_animation]
style = "fade-slide" # "none", "fade", "slide", "fade-slide", or "bounce"
open_ms = 240
close_ms = 160
distance_px = 24

[gui.dialog_backdrop]
style = "dim" # or "none"
opacity = 65  # percent

[theme]
color_scheme = "gruvbox-light"
accent = "auto"
icons = "nerd"
# Desktop fonts; the TUI uses its terminal emulator's font settings.
font = "JetBrains Mono"
font_size = 16
fallback = ["Symbols Nerd Font Mono", "Noto Color Emoji", "Noto Sans CJK JP"]

[editor]
markdown_autoformat = true
checklist_auto_reorder = true
autosave = true
reload_outside_changes = true
format_on_save = false
vim_mode = false
# Keep the bottom command bar and show searchable suggestions above it.
command_popup = true
wrap = true
# Editor line numbers. Unset, they show in the TUI and stay off in the GUI.
# line_numbers = true
status_hints = true
date_format = "%Y-%m-%d"
date_time_format = "%Y-%m-%d %H:%M"
variable_autocomplete_min_chars = 3

[editor.modules]
math = true
table = true
variables = true
style = true
cross_note = true

[editor.security]
encrypt_notes = false
password_env = "SLATE_NOTES_PASSWORD"

[special_notes]
email_note_prefix = "inbox-email"
email_rotation = "daily-local"

[daily]
note_prefix = "daily"
template = "# {date}\n\n"

[imap]
host = "imap.example.com"
port = 993
username = ""
password_env = "SLATE_IMAP_PASSWORD"
folder = "INBOX"
poll_seconds = 60
auto_sync_on_startup = false
initial_sync_max_messages = 200
initial_sync_past_days = 1
max_message_bytes = 8388608
max_body_bytes = 524288

[perf]
enabled = false
log_path = ""

[web_search]
provider = "auto"
api_key = ""
search_engine_id = ""
max_results = 10

[terminal]
images = "auto"
image_max_rows = 15
clipboard = "auto"

[mcp]
enabled = false
allow_delete = false

[startup]
default_collection = ""
background_tasks_enabled = true

# Copy scripts/examples/rates.py to your config directory and set its absolute path.
# [currency]
# argv = ["python3", "/absolute/path/to/slate/scripts/examples/rates.py", "EUR"]
# timeout_seconds = 30
```

Explicit TUI note-list refreshes and wiki-completion loads always prepare their
catalogue on a worker, including when optional startup background tasks are
disabled. This setting does not switch catalogue hydration onto the input thread.

## Desktop switcher pins

`[gui] switcher_ignore_pins` defaults to `false`: the desktop note switcher
(`Ctrl+P`) lists pinned notes first, as the sidebar does. Set it to `true` so
the empty switcher lists notes strictly by when they were last edited, pinned
or not. Pinned notes still lead the sidebar, and a typed switcher search still
ranks pinned matches first. The TUI ignores this option.

## Desktop animations

`[gui] animations` defaults to `true`. Set it to `false` and restart the GUI
to disable all menu and dialog effects. `[gui.dialog_animation]` configures
only dialogs: `style` accepts `"none"`, `"fade"`, `"slide"`, `"fade-slide"`
(default), or `"bounce"`. Opaque `slide` and `bounce` exits disappear at the
end of their movement; use `fade-slide` for a fading exit. Fade changes opacity;
slide moves the dialog; fade-slide combines both; bounce adds a positional
overshoot without resizing its contents. `open_ms` defaults to 240,
`close_ms` to 160, and `distance_px` to 24 logical pixels. Distance applies
only to slide, fade-slide and bounce. Dialogs dim the window behind them;
the dim stays fixed and fades with transition progress in every style. Menus
and the docked command bar leave the window undimmed.
`[gui.dialog_backdrop]` sets the dim: `style` is `"dim"` (default) or `"none"`,
and `opacity` is its strength in percent of the theme background (default 65,
capped at 100).
Zero duration skips that direction; durations are capped at 1000 ms
and distance at 32 pixels. `style = "none"` leaves menu opening fades enabled.

Dialog actions run immediately while the old presentation closes. A new
dialog replaces any closing presentation. Typing and menu switching remain
immediate, and no animation frames are requested at rest. Full-page browser,
help and history views stay immediate. The TUI ignores these settings.

## Currency rates

The repository includes [rates.py](https://github.com/dborovcanin/slate/blob/main/scripts/examples/rates.py). Register its
absolute path under `[currency]` to enable currency calculations. The optional
last argument chooses the base currency (EUR in the example); `timeout_seconds`
defaults to 30 and accepts 1–3600.

Slate loads cached rates immediately, fetches once in the background at
startup when `background_tasks_enabled = true`, and refreshes on
`:currency refresh`. See [Currency rates](scripting.md#currency-rates) for the
script protocol and offline example. Paths do not expand `~`.

## Default collection

Set `[startup] default_collection = "Work"` to start with an existing collection
as the working collection. Note browsing and search are scoped to it, and new
notes (including `slate --new`) are created in it. Names use the same
case-insensitive matching as collection commands.

An empty or omitted value keeps all notes in scope. A missing collection shows a
status message and falls back to all notes; it is not created automatically.
The setting does not change which existing note opens at startup: an explicit
note or the most recent note still opens as usual. You can change the working
collection during the session with `:collection choose Work` or clear it with
`:collection choose none`. Encrypted collections still require unlocking before
new notes can be created in them.

## Theme settings

`[theme]` keys:

- `color_scheme`
- `accent`
- `icons`
- `[theme.colors]`, see below

### color_scheme values

- `slate-light`
- `slate-dark`
- `catppuccin-mocha`
- `catppuccin-latte`
- `gruvbox-dark`
- `gruvbox-light`
- `dracula`
- `dark`
- `white`
- `solarized-dark`
- `solarized-light`
- `nord`
- `tokyo-night`
- `one-dark`

### accent values

- `auto`
- `amber`
- `sage`
- `rose`
- `plum`
- `cobalt`
- `slate`
- custom hex like `#4f7bd9`

### icons values

- `nerd` (default): Nerd Font glyphs, as in yazi or lsd. Needs a [Nerd Font](https://www.nerdfonts.com/) in the terminal.
- `unicode`: symbols from standard Unicode blocks, for any font.
- `ascii`: plain ASCII markers.


### `[theme.colors]`

Colours that replace the color scheme's, much like foot's `[colors]`. Each value is hex (`2e3440` or `#2e3440`), shown exactly as written, or `none` for the terminal's own colour; `background = "none"` lets the terminal background (and its transparency) show through the editor. Unset keys, and values slate cannot read, keep the scheme's colour. `accent` here wins over `[theme] accent`.

```toml
[theme.colors]
foreground = "eceff4"
background = "none"
accent = "88c0d0"
code-block-background = "3b4252"
selection-background = "434c5e"
keyword = "81a1c1"
string = "a3be8c"
number = "b48ead"
comment = "616e88"
function = "88c0d0"
type = "8fbcbb"
variable = "ebcb8b"
search-match = "5e81ac"
search-current = "bf616a"
```

With `background = "none"`, slate treats the background as dark when picking text colours on it; on a light terminal, set `selection-background` too.

## Editor settings

`[editor]` keys:

- `markdown_autoformat`
- `checklist_auto_reorder`
- `autosave`
- `reload_outside_changes`
- `format_on_save`
- `vim_mode`
- `wrap`
- `date_format`: daily note titles and the dates of notes older than a week in the browser and switcher
- `date_time_format`: date-picker input, previews, inserted dates, reminders, and a note's modified and added times in the browser preview. Both GUI and TUI accept this format, with or without its clock suffix. Date-only insertion uses the date portion of this same pattern; natural input such as `in 3 weeks` still works.
- `variable_autocomplete_min_chars`

Behavior notes:

- `autosave = true` enables implicit save flows (idle flush + save on exit/switch).
- with `autosave = false`, explicit writes persist body changes. Switching notes or quitting with unsaved changes is refused once (vim's E37); repeating it, `:q!` or `:e!` discards them.
- a failed save (for example a note changed elsewhere) keeps the editor open with the changes; autosave waits for the next edit. `:w!` overwrites, `:e!` reloads.
- `reload_outside_changes = true` (default) checks the open note about once a second while idle (in the terminal app also as soon as the terminal regains focus) and loads changes made elsewhere (`slate mcp`, `slate append`, `slate capture`, IMAP sync, another Slate) as one undoable edit when there are no unsaved changes. Set it to `false` to skip the check; such changes then show up as a save conflict, as before.
- `format_on_save = true` runs format before save.
- `vim_mode = true` starts the editor in vim normal mode.
- `wrap = true` (default) soft-wraps long lines at word boundaries. Tables, code fences, code blocks, and code files keep horizontal scrolling so columns stay aligned. With `wrap = false` every line scrolls horizontally.
- `line_numbers` is unset by default: the TUI shows line numbers and the GUI hides them. Set it to `true` or `false` to choose for both; GUI fold controls remain available, and View › Line numbers in the GUI overrides it. Restart Slate after changing it.
- `status_hints = true` (default) shows key hints in the terminal status bar: `:` commands, `?` keys, `Ctrl+P` notes and `F1` help in vim mode (`Ctrl+E` for commands otherwise). Status messages replace them while they show. Set it to `false` to hide them.
- `variable_autocomplete_min_chars` is clamped to `1..8`.

## Per-note module defaults

`[editor.modules]` sets defaults for new notes:

- `math`
- `table`
- `variables`
- `style`
- `cross_note`

Module state is then persisted per note and can diverge note-by-note.

## Note security defaults

`[editor.security]` keys:

- `encrypt_notes`: whether newly created notes default to encrypted-at-rest storage
- `password_env`: environment variable name used for default encryption password

Behavior notes:

- if `encrypt_notes = true`, `password_env` must resolve to a non-empty environment variable at runtime
- a new note in an encrypted working collection is encrypted with the collection's key instead
- note encrypt/decrypt commands are not supported for file-backed markdown notes (`slate path/to/file.md`)

## Daily notes

`[daily]` keys:

- `note_prefix` (default `daily`): daily note ids are `<prefix>-YYYY-MM-DD`
- `template` (default `"# {date}\n\n"`): body of a new daily note; `{date}` uses `[editor] date_format`

Daily notes are opened with `:today` or `slate today`, and `slate capture <text>` (or piped stdin) appends a `- HH:MM text` entry without opening the editor.

## Special notes

`[special_notes]` keys:

- `email_note_prefix`
- `email_rotation` (currently `daily-local`)

## IMAP

`[imap]` keys:

- connection: `host`, `port`, `username`, `password_env`, `folder`
- polling: `poll_seconds`, `auto_sync_on_startup`
- bootstrap and limits:
  - `initial_sync_max_messages`
  - `initial_sync_past_days`
  - `max_message_bytes`
  - `max_body_bytes`

Runtime validation constraints:

- `poll_seconds`: `10..86400`
- `initial_sync_max_messages`: `1..100000`
- `initial_sync_past_days`: `0..3650`
- `max_body_bytes <= max_message_bytes`
- `host`, `username`, `password_env`, and `folder` must be non-empty

## MCP server

`[mcp]` keys:

- `enabled` (default `false`): lets `slate mcp` serve notes to MCP clients such as AI assistants. While it is `false`, `slate mcp` refuses to start.
- `allow_delete` (default `false`): also offers `delete_note`, which deletes a note and its history for good. Without it, clients can only move notes to the `Archive` collection.

Notes created over MCP use `[editor.modules]` and `[editor.security]` like notes created in the editor. See [MCP Server](mcp.md) for client setup.

## Agent

`[agent]` keys, for `:ask` (see [Ask the Agent](agent.md)):

- `enabled` (default `false`): lets `:ask` run the agent. The prompt, the context and whatever the agent reads go to that agent's model.
- `preset` (default `"claude"`): `"claude"`, `"codex"`, or `"custom"` with `argv`.
- `argv`: the command for `preset = "custom"`; not allowed with the other presets.
- `context` (default `"selection"`): what of the open note goes into the prompt: `"selection"`, `"note"` or `"none"`.
- `notes` (default `"write"`): what the agent may do with notes through Slate's MCP server: `"write"` (never delete), `"read"` or `"none"`. Needs `[mcp] enabled = true`; without it requests run as `"none"`.
- `timeout_seconds` (default `300`, 1–3600).

An unknown key or a bad combination is an error shown when `:ask` runs. Settings
reload for every request. Built-in presets resolve `claude`/`codex` from Slate's
inherited `PATH`; authenticate the CLI first. There is no Slate model/API-key or
extra-arguments setting. A custom preset may use an absolute executable path,
but must implement the prompt-on-stdin/answer-on-stdout contract and its own MCP
setup. See [the setup guide](agent.md#setup) for native config paths, executable
discovery, platform qualification, and troubleshooting.

Ask retains one conversation across notes until `/clear`, Clear context, or app
exit. Changing `context` or `notes` does not erase earlier exchanges.

## Date format tokens

Common supported tokens:

- `%Y`, `%y`
- `%m`, `%d`
- `%b`, `%B`

## Desktop fonts

`[theme] font` selects the desktop font family throughout the app, and
`font_size` sets its initial size in pixels (9–32). These settings override the
remembered desktop size at startup; zoom shortcuts still work during the
session. Family names are case insensitive; the old `jetbrains-mono` spelling
also resolves to `JetBrains Mono`.

`fallback` lists the installed families available for missing glyphs. All
variants of the selected families are retained. A missing configured family
is a startup error. With no list (or an empty one), Slate selects a small
installed set covering symbols, emoji, and CJK where available. With no primary
font, Slate retains separate automatic monospace/editor and sans/UI choices.

On Linux, Fontconfig's cached catalogue resolves the families before GPUI
starts. A private font directory restricts discovery to the selected files;
other installed families are not parsed. `fc-list` from the `fontconfig`
package is required. Other desktop platforms use their native font systems;
font discovery is not restricted there.

The TUI does not load, select, or restrict font files. Configure its terminal
emulator (Ghostty, Alacritty, etc.) for the same primary and fallback fonts.
