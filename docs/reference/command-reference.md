# Command Reference

Every command-bar command with its aliases. For what each feature does and its keys, see the [Feature Guide](features.md).

## Command modes

- Command bar: `:` in Normal/Visual mode, `Ctrl+E` in Insert or Normal mode.
- The leading `:` is optional; matching is case-insensitive.
- `Tab` / `Shift+Tab` complete command words; `ArrowUp` / `ArrowDown` walk command history.
- Commands run from Visual mode apply to the selection.
- `w`, `wq`, `q` (and their `!` forms) are available only when the bar was opened from Normal/Visual mode.

## Help

| Command | Aliases | Purpose |
| --- | --- | --- |
| `help` | `h` | Keyboard shortcuts and commands, filtered as you type (also `F1`, and `?` in Normal mode); `Enter` puts a command in the command bar |

## Calculation

| Command | Purpose |
| --- | --- |
| `sum` | Sum the numbers in the selection, or the whole note without one |
| `avg` | Average the numbers in the selection, or the whole note without one |

## Dates, reminders and daily notes

| Command | Aliases | Purpose |
| --- | --- | --- |
| `today` | `daily` | Open today's daily note, creating it from the `[daily]` template |
| `browse` | `explore`, `files` | Open the collection browser (`t` edits tags, `T` filters by tag) |
| `info` | `note info` | Show the current note’s tags, collections, saved dates and encryption; also F4 |
| `inspect` | | Show what the result on the cursor line was computed from; also `K` in Normal mode off a link |
| `read` | `preview` | Read mode: every line rendered, read-only; also F11 |
| `history` | `versions` | Browse and restore older versions of the open note |
| `date` | | Insert a picked date |
| `remind` | `alarm` | Set a reminder for the current line |
| `remind toggle` | | Remove the line's reminder, or set one if there is none |

## Formatting and lists

| Command | Aliases | Purpose |
| --- | --- | --- |
| `format` | `fmt` | Format markdown document |
| `format bold` | `bold` | Toggle `**` around selection |
| `format italic` | `italic` | Toggle `*` around selection |
| `format strike` | `strike`, `strikethrough` | Toggle `~~` around selection |
| `format code` | `icode`, `inline-code` | Toggle `` ` `` around selection |
| `format clear` | `clear-format`, `unformat`, `plain` | Strip inline formatting from selection |
| `format heading-1` | `title`, `h1`, `heading 1`, `format title`, `format h1`, `format heading` | Convert selected lines to a heading |
| `format heading-2` | `h2`, `heading 2`, `format h2` | Convert selected lines to a level 2 heading |
| `format heading-3` | `h3`, `heading 3`, `format h3` | Convert selected lines to a level 3 heading |
| `format text` | `normal text`, `format normal` | Remove heading and list markers from selected lines |
| `checklist toggle` | `toggle`, `check`, `tick` | Tick or untick the checkboxes on selected lines |
| `format checklist` | `clist`, `checklist`, `checkbox`, `checkboxes`, `todo`, `format clist` | Convert selected lines to a checklist |
| `format unordered-list` | `ulist`, `unordered-list`, `unordered`, `format bulleted-list`, `format unordered`, `format ulist` | Convert selected lines to an unordered list |
| `format ordered-list` | `olist`, `ordered-list`, `ordered`, `format ordered`, `format olist` | Convert selected lines to an ordered list |

Suggestions show only the canonical `format` names. Abbreviated aliases such as
`h2`, `clist`, and `olist` still work. The `paragraph` command family has been
removed; use `format` in commands and saved keybindings.

In Vim Visual (`v`) or Visual Line (`V`) mode, press `:` and type `format`
to select formatting with Tab completion. Inline styles apply to the selected
text; `format ordered-list`, `format unordered-list` (also `format bulleted-list`),
and `format checklist` convert the selected lines. This works in the terminal
and desktop apps. With Markdown autoformat enabled, Enter within list item
content splits it into two list items, preserving indentation and updating
ordered numbering. Enter on an empty item exits the list.


## Modules

| Command | Purpose |
| --- | --- |
| `module status` | Show the note's module state (aliases: `module`, `modules`, `modules status`) |
| `module math on/off/toggle` | Change math module |
| `module table on/off/toggle` | Change table module |
| `module variables on/off/toggle` | Change variables module |
| `module style on/off/toggle` | Change style module |
| `module cross_note on/off/toggle` | Change cross-note variables module |

`modules` works in place of `module`, and the action may come first: `module on math`, `modules off variables`.

## Outline and graph

| Command | Purpose |
| --- | --- |
| `toc` | Open the heading picker |
| `toc insert` | Insert a generated table-of-contents section |
| `toc refresh` | Regenerate existing closed TOC sections |
| `graph` | Open the note-link graph |

See [Generated TOC sections](features.md#generated-toc-sections) and
[Note graph](features.md#note-graph) for navigation and controls.

## Diagrams

| Command | Purpose |
| --- | --- |
| `diagram` | Desktop: open the diagram at the cursor, or insert an empty block and open its canvas. Terminal: insert an empty diagram block; inside one, say the canvas is desktop-only |

See [Diagrams](features.md#diagrams) for the block format and canvas controls.

## Folding

| Command | Aliases | Purpose |
| --- | --- | --- |
| `fold` | `closefold`, `zc` | Fold block at cursor |
| `unfold` | `openfold`, `zo` | Unfold block at cursor |
| `fold-toggle` | `fold_toggle`, `za` | Toggle fold at cursor |

## Clipboard watch

| Command | Aliases | Purpose |
| --- | --- | --- |
| `clip-watch on` | `clip-watch start` | Paste each new clipboard text at the cursor |
| `clip-watch off` | `clip-watch stop` | Stop clipboard watch |
| `paste-image` | | Paste the image on the clipboard at the cursor |

## Lookup

| Command | Aliases | Purpose |
| --- | --- | --- |
| `lookup [query]` | | Open the lookup overlay, running `query` if given |

## Ask the agent

| Command | Aliases | Purpose |
| --- | --- | --- |
| `ask [prompt]` | | Ask the local agent, or open the prompt; needs `[agent] enabled = true`. See [Ask the Agent](agent.md) |

## Note organization

| Command | Purpose |
| --- | --- |
| `organize` / `tag` | Open the current note's tag/collection organizer |
| `tag add [name]` | Add one tag, or open the organizer without a name |
| `tag remove [name]` | Remove one tag, or open the organizer without a name |
| `note pin` / `note unpin` | Set the current stored note's list pin without changing text |

Pins respect search and scope filters. File-backed notes do not have stored
note tags or list pins. Collection commands below change membership or the
working collection; these are separate contexts.

## Note security

| Command | Aliases | Purpose |
| --- | --- | --- |
| `note encrypt` | `note-encrypt`, `encrypt-note` | Encrypt the note with its own password; on an unlocked encrypted note, change its password |
| `note decrypt` | `note-decrypt`, `decrypt-note` | Store the note unencrypted (a note that left an encrypted collection takes the collection's password) |

Both ask for the password in a masked dialog (encrypting asks twice); a password typed on the command line is ignored. Collections are encrypted from the browser (`e`).

A note in an encrypted collection stays encrypted with the collection's password while it belongs to it: `note decrypt` is refused, and so is `note encrypt` for a note the collection's password protects. Remove the note from the collection (`:collection leave`) or decrypt the whole collection (`e` in the browser) first.

## Export and backup

| Command | Aliases | Purpose |
| --- | --- | --- |
| `export pdf <path>` | | Export note to PDF |
| `export markdown [path]` | `export md` | Markdown to file, or clipboard without a path |
| `export text [path]` | `export txt` | Plain text to file, or clipboard without a path |
| `backup export <path.zip>` | | Back up the full notes database |
| `backup export md <directory>` | | Export Markdown files under collection folders, writing each note once |
| `backup load <path>` | | Detect and restore a Slate ZIP backup, or add notes from a Markdown directory/ZIP |

## Collections

| Command | Purpose |
| --- | --- |
| `collection create <name>` | Create a collection |
| `collection delete <name>` | Delete a collection only |
| `collection purge <name>` | Delete a collection and all its notes |
| `collection choose <name>` | Set the working collection for this session |
| `collection choose none` / `collection clear` | Clear the working collection |
| `collection join [name]` | Add current note to a collection |
| `collection leave [name]` | Remove current note from a collection |
| `collection update <name>` | Edit name, description and default tags |

Without a name, `collection join` and `collection leave` open the current
note's collection organizer. `collection choose` without a name opens the
working-collection picker. Export suggestions show `markdown`, `pdf` and `text`
once each; typing `md` or `txt` still matches the full-name suggestion.

## Write and quit (Normal/Visual command bar)

| Command | Aliases | Purpose |
| --- | --- | --- |
| `w` | `write` | Write/save |
| `w!` | | Force write over a newer revision |
| `wq` | `writequit` | Write and quit |
| `wq!` | | Force write and quit |
| `q` | | Quit |
| `q!` | | Quit without saving |

## Diagnostics

| Command | Purpose |
| --- | --- |
| `perf status` | Show perf tracing state (also `perf`, `profile`, `profiler`) |
| `perf on` / `perf off` / `perf toggle` | Enable / disable / toggle tracing |
| `perf dump [top]` | Write the slowest buckets to the perf log |
| `perf where` | Show the perf log path |
| `perf clear` | Drop collected samples |
| `perf cap <n>` | Samples kept per bucket |
