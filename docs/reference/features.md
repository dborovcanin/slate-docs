# Feature Guide

Every Slate feature in one place, grouped by area, with the keys and commands that drive it.

Conventions:

- **Insert** is the text-editing mode (also the only mode when you never press `Esc`). **Normal** is vim normal mode.
- Commands are typed in the bottom bar: `:` in Normal/Visual, `Ctrl+E` in Insert or Normal. F1 provides command and keyboard discovery.
- **TUI:** commands stay in the bottom bar, with bracketed word completions such as `:export  [md  pdf  txt]`. Tab/Shift+Tab select completions; Enter or Ctrl+Left fills the selected word, then a later Enter executes. Otherwise Ctrl+Left/Right move by word. Up/Down recall history, and Esc closes the bar immediately. F1 opens the command catalogue.
- **GUI:** a compact popup shows up to six recent or contextual suggestions. The bar shows only typed text and a faint completion suffix. Nothing is highlighted automatically. Down or Tab selects; Enter or Ctrl+Left fills the selection, then a later Enter executes. Up recalls history when no suggestion is selected. Esc hides suggestions first, then closes the bar. `[editor] command_popup = false` keeps the quiet bar with Tab word completion.
- Full alias lists: [Command Reference](command-reference.md). Key tables by mode: [Keymaps](keymaps.md).

## Contents

- [Feature Guide](#feature-guide)
  - [Contents](#contents)
  - [Notes and switching](#notes-and-switching)
  - [Saving](#saving)
    - [Note history](#note-history)
  - [Command line entry points](#command-line-entry-points)
  - [Daily notes, capture and pipe append](#daily-notes-capture-and-pipe-append)
  - [Editing and markdown helpers](#editing-and-markdown-helpers)
  - [Inline formatting and list commands](#inline-formatting-and-list-commands)
  - [Vim mode](#vim-mode)
  - [Macros](#macros)
  - [Search](#search)
  - [Wiki links](#wiki-links)
  - [Images and image preview](#images-and-image-preview)
  - [Diagrams](#diagrams)
  - [Inline calculations](#inline-calculations)
  - [Variables and cross-note variables](#variables-and-cross-note-variables)
  - [Tables](#tables)
  - [Folding](#folding)
  - [Dates and reminders](#dates-and-reminders)
  - [Lookup](#lookup)
  - [Ask the agent](#ask-the-agent)
  - [Clipboard and clip-watch](#clipboard-and-clip-watch)
  - [Collections](#collections)
    - [Collection browser](#collection-browser)
  - [Per-note modules](#per-note-modules)
  - [Note security](#note-security)
  - [Export and backup](#export-and-backup)
  - [IMAP email sync](#imap-email-sync)
  - [MCP server](#mcp-server)
  - [Themes, wrap and other settings](#themes-wrap-and-other-settings)
  - [Diagnostics](#diagnostics)

## Notes and switching

- Notes live in SQLite (`~/.local/share/slate/notes.db`, WAL mode). The last-open note is restored on start.
- A note's title is its first non-empty line (heading markers dropped) until you rename it in the browser (`r`); a renamed title stays put like a file name, and an empty name makes it follow the first line again. Encrypting a note keeps its title visible.
- Markdown files open directly: `slate path/to/file.md` or `slate-gui path/to/file.md` (`.md`, `.markdown`, `.mdown`, `.mkd`); edits are saved back to the file.
- Terminal colors follow `TERM`/`COLORTERM`: true color when advertised or when `TERM` names a truecolor terminal family (kitty, alacritty, foot, wezterm, ghostty, …) whose `COLORTERM` was dropped by ssh or sudo, otherwise 256 or basic 16 colors. A nonempty `NO_COLOR` (or `TERM=dumb`) uses terminal-default colors with monochrome emphasis for highlighted backgrounds. Capability detection happens once at startup.
- The terminal app names the open note in the terminal's window title (`Note - Slate`) and puts the terminal's own title back on exit. Encrypted notes show only `Slate` there, since the title stays visible in tab bars and window lists.

The note switcher and collection picker are popups styled like the [collection browser](#collection-browser): a search bar over a list with icons, ages or match lines, and key hints at the bottom. One `Ctrl+P` query searches titles, tags, collections and note text; use `contains:` for body text. A collection name appears in the title when the search is scoped to one.

| Key / command                              | Action                                                                                    |
| ------------------------------------------ | ----------------------------------------------------------------------------------------- |
| `Ctrl+N` (Insert, switcher)                | New note (in the working collection, if one is set)                                       |
| `Ctrl+P`                                   | Search notes with one structured query                                                    |
| `Tab` in the switcher                      | Accept a field or value completion, if available; otherwise move to the results           |
| `Enter` in the switcher                    | In the query, move to the results with the best match picked; in the results, open the picked note at the matching line |
| `Up` / `Down` in the switcher query        | Recall earlier searches; `Down` past the newest moves to the results                      |
| `Ctrl+L` in the switcher                   | Toggle between the working collection and all notes                                       |
| `Ctrl+R` in the switcher                   | [History](#note-history) of the selected note                                             |
| `Delete` in the switcher                   | Delete the selected note (confirm with `y`/`Enter`; protected notes ask for the password) |
| `Ctrl+W`, `Ctrl+Backspace` in the switcher | Delete the last word of the query                                                         |
| `Esc` / `Ctrl+P` in the switcher           | Close it                                                                                  |
| `Ctrl+Q`                                   | Quit (from any mode)                                                                      |
| `F1`, `:help` (`:h`), `?` (Normal)         | Help: keyboard shortcuts with how each works, then every command; type to filter, `Enter` puts a command in the command bar |

In either collection browser, press `P` (Shift+P), or choose **Pin note** / **Pin collection** from the actions menu, to toggle a persistent list pin. Matching pinned items appear first in the browsers and pickers; the normal sort or search ranking applies within each group. Use `:note pin` or `:note unpin` in the editor to pin or unpin the current stored note without changing its text. Pins never override search, tag or collection filters. Desktop rows show a pin icon; terminal rows show `*` beside the age or count. “All notes” and “Unsorted” remain navigation entries above collections.

The note switcher, collection picker and collection browser fetch lists in pages of 100 as you navigate. Title filters search the entire scope in the background, including notes and collections outside the loaded pages. Changing the scope, filter or sort starts a fresh list. Browser End and Select All can load all matching pages.

Encrypted notes ask for their password (or their collection's) before opening. Content search only indexes unprotected notes.

## Background activity

Both apps show background work that lasts longer than a second, such as saving,
backups or exchange-rate updates, in the status bar with a small spinner.

Slate opens databases with its current schema, and upgrades ones from an
older release after keeping a copy (`notes.db.before-upgrade-v<N>`). A
database or backup from a pre-release version (schemas 2 to 6, Slate 0.8.0
and older) is refused with an error and left untouched. To keep its notes,
open it with Slate 0.8.0, run `:backup export md <directory>`, then
`:backup load <directory>` in this version.

## Saving

| Key / command                                  | Action                                                                                        |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------- |
| autosave (`[editor] autosave = true`, default) | Saves after a short idle pause on a background thread, and before switching notes or quitting |
| `Ctrl+S`                                       | Save now (in Insert only while autosave is on; otherwise use `:w`)                            |
| `:w` / `:w!`                                   | Write / force write (overwrites a newer revision on disk)                                     |
| `:wq` / `:wq!`                                 | Write and quit                                                                                |
| `:q` / `:q!`                                   | Quit / quit without saving                                                                    |

`[editor] format_on_save = true` runs `:format` before every save. If the note changed elsewhere since it was loaded, a save stops with `note changed since last load; use :w! to force save`.

While idle (unless `[editor] reload_outside_changes = false`), Slate checks about once a second whether the open note changed elsewhere (`slate mcp`, `slate append`, `slate capture`, IMAP sync, another Slate, an edited markdown file). Without unsaved changes the new text is loaded in place as one undoable edit, with the cursor and reminders kept on their lines (`note changed outside Slate; reloaded (u undoes)`). With unsaved changes your text is kept and the status line says so: `:e!` loads the stored note, `:w!` keeps your version.

### Note info

Press `F4` in the editor, or run `:info`, to inspect the current note in either front end. The desktop app also has **File → Note info**. The dialog shows its title, ID, source, tags, collections, creation and last saved update times, encryption, lock state, and unsaved edits. The terminal dialog also lists the notes this note links to (from its current text) and the notes linking to it (from their saved text, up to 500 listed), each with a count; in a large library the linking notes appear a moment after the dialog opens. The desktop app shows these in the note inspector. It fits short content and scrolls long metadata lists; long names wrap in both front ends. Opening it does not save or change the note. File-backed notes use filesystem timestamps; unavailable creation dates show “Unknown”.

Use arrows or Page Up/Down to scroll long lists; Home/End jump to the beginning/end. Escape, Enter, or F4 closes the dialog and preserves the editing mode, cursor and selection. Ctrl+I keeps its existing behavior.

### Note history

Slate keeps older versions of every stored note. Saves less than five minutes apart form one editing session, and each session keeps the text from before it as a version (a session longer than half an hour is split). Versions are stored as the line changes between them, with an occasional full copy, so a small edit to a large note costs a few bytes; the history of an encrypted note is encrypted with it. File-backed notes (`slate file.md`) keep no history.

Old versions are thinned out when a new one is added: every version of the last day stays, then the newest of each day for a month, then the newest of each week, up to 500 versions per note.

`:history` (or `:versions`), `H` on a note in the browser, or `Ctrl+R` in the note switcher opens the history in the browser: the current text first, then each version with its time and the lines its session added and removed. The preview shows what restoring would change (`-` current lines, `+` lines of the version), or the version's text.

| Key                                                | Action                                                                      |
| -------------------------------------------------- | --------------------------------------------------------------------------- |
| `j` / `k`, arrows, `gg` / `G`, `Ctrl+D` / `Ctrl+U` | Move between the current text and older versions                            |
| `Tab`, `t`                                         | Preview what restoring would change, or the version's full text             |
| `Enter`, `l`                                       | Restore the version (`y` confirms); the text before it is kept as a version |
| `h`, `-`, `Esc`                                    | Back to the notes                                                           |
| `q`, `Ctrl+B`                                      | Close the browser                                                           |

## Command line entry points

```text
slate                        open the last note
slate --new | -n             create and open a new note
slate --id <note-id>         open a specific note
slate --list | -l            list notes and exit (works without a TTY)
slate <file.md>              open a markdown file as a note
slate today                  open today's daily note
slate capture [text...]      add a timestamped entry to today's daily note and exit
cmd | slate capture          capture piped stdin
cmd | slate append [--id <note-id>]   append stdin to a note and exit
slate imap-sync              pull new mail once and exit
slate mcp                    serve notes to MCP clients over stdio (needs [mcp] enabled = true)
slate --help | -h
```

## Daily notes, capture and pipe append

- **Daily notes**: `slate today` or `:today` (alias `:daily`) opens today's note, creating it from the `[daily]` template (`note_prefix`, default `daily`; `template`, default `"# {date}\n\n"`). The cursor lands at the end, ready to type.
- **Quick capture**: `slate capture buy milk` appends a `- HH:MM buy milk` line to today's daily note without opening the editor. With no text it reads piped stdin, so any command output can be captured:

  ```sh
  slate capture call the bank at 3
  git log -1 --oneline | slate capture
  ```

- **Pipe append**: `cmd | slate append` appends stdin verbatim to the most recently edited note (email inbox notes are skipped); `--id <note-id>` picks the target note.

  ```sh
  curl -s wttr.in/?format=3 | slate append
  make test 2>&1 | slate append --id 01HX4VHR...
  ```

## Editing and markdown helpers

Markdown stays raw text; styling is drawn in place (no preview pane).

- live styling for headings, quotes, lists, checklists, inline code, code fences, bold/italic/strike, markdown links and wiki links
- a `---`, `***` or `___` line is drawn as a full-width divider; the Markdown shows again while the cursor is on it
- list continuation on `Enter` (bullets, numbers, checklists)
- checklists `- [ ]` / `- [x]`; a trailing ` /x` toggles an item; with `[editor] checklist_auto_reorder = true` checked items move below unchecked ones
- markdown table autoformat and alignment while typing (see [Tables](#tables))
- soft wrap for prose (`[editor] wrap = true`); tables and code keep horizontal scrolling
- undo/redo with cursor restore

| Key                                   | Action (Insert)                                                                                                                 |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `Enter`                               | New line / continue list / accept popup selection                                                                               |
| `Tab` / `Shift+Tab`                   | Accept completion, else apply calc result, else next/previous table cell, else indent/outdent list item, else insert two spaces |
| `Ctrl+W`, `Ctrl+Backspace`            | Delete word before the cursor (table-aware)                                                                                     |
| `Ctrl+Delete`                         | Delete forward (table-aware)                                                                                                    |
| `Ctrl+ArrowLeft` / `Ctrl+ArrowRight`  | Previous / next word (previous / next cell in tables)                                                                           |
| `Home` / `End`, `PageUp` / `PageDown` | Line start / end, page up / down                                                                                                |
| `ArrowUp` / `ArrowDown`               | Move by screen row on wrapped lines; move popup selection when a popup is open                                                  |
| `Esc`                                 | Close popup, else switch to Normal mode                                                                                         |

## Inline formatting and list commands

Select text first (`v` / `V`, then `:`); the command applies to the selection.

| Command                 | Aliases                                                                                            | Action                             |
| ----------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `format bold`           | `bold`                                                                                             | Toggle `**bold**`                  |
| `format italic`         | `italic`                                                                                           | Toggle `*italic*`                  |
| `format strike`         | `strike`, `strikethrough`                                                                          | Toggle `~~strike~~`                |
| `format code`           | `icode`, `inline-code`                                                                             | Toggle `` `code` ``                |
| `format clear`          | `clear-format`, `unformat`, `plain`                                                                | Strip inline formatting            |
| `format heading-1`      | `title`, `h1`, `heading 1`, `format title`, `format h1`, `format heading`                          | Turn lines into a heading          |
| `format heading-2`      | `h2`, `heading 2`, `format h2`                                                                     | Turn lines into a level 2 heading  |
| `format heading-3`      | `h3`, `heading 3`, `format h3`                                                                     | Turn lines into a level 3 heading  |
| `format text`           | `normal text`, `format normal`                                                                     | Back to plain text                 |
| `checklist toggle`      | `toggle`, `check`, `tick`                                                                          | Tick or untick checkboxes          |
| `format checklist`      | `clist`, `checklist`, `checkbox`, `checkboxes`, `todo`, `format clist`                             | Turn lines into a checklist        |
| `format unordered-list` | `ulist`, `unordered-list`, `unordered`, `format bulleted-list`, `format unordered`, `format ulist` | Turn lines into a bullet list      |
| `format ordered-list`   | `olist`, `ordered-list`, `ordered`, `format ordered`, `format olist`                               | Turn lines into a numbered list    |
| `format`                | `fmt`                                                                                              | Format the whole markdown document |

## Vim mode

Slate is modal: `Esc` leaves Insert for Normal mode. `[editor] vim_mode = true` starts in Normal mode instead of Insert.

| Keys                                                                      | Action                                                                                       |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `h` `j` `k` `l`, arrows                                                   | Move (with counts)                                                                           |
| `w` / `b`, `e`                                                            | Next / previous word, end of word                                                            |
| `0` / `$` (`Home` / `End`), `^`                                           | Line start / end, first non-blank character                                                  |
| `f{c}` `F{c}` `t{c}` `T{c}`, `;` `,`                                      | Find a character on the line (onto / till, forward / back); repeat the find                  |
| `%`                                                                       | Jump to the bracket matching the next one on the line                                        |
| `gg` / `G`, `{n}G` / `{n}gg`                                              | First / last line, line `n`                                                                  |
| `gj` / `gk`                                                               | Down / up one screen row on wrapped lines                                                    |
| `i` `a` `I` `A` `o` `O`                                                   | Enter Insert (before, after, line start, line end, new line below/above)                     |
| `x`, `s`, `S`                                                             | Delete character; substitute character / line text and enter Insert                          |
| `D`, `J`                                                                  | Delete to line end; join lines                                                               |
| `.`                                                                       | Repeat the last change, including the text typed with it                                     |
| `dd` `yy` `cc`                                                            | Delete / yank / change line (`3dd`, `2yy`)                                                   |
| `d` `y` `c` + `w` `b` `e` `0` `$` `^` `%`                                 | Operator + motion (`d2w`, `y$`, `d%`); `cw` changes to the end of the word, as in Vim        |
| `d` `y` `c` + `f` `F` `t` `T` `{c}`                                       | Operator + find (`df,`, `ct)`, `yT(`)                                                        |
| `diw` `daw` `yiw` `yaw` `ciw` `caw`                                       | Word text objects                                                                            |
| `di\|` `da\|` `yi\|` `ya\|` `ci\|`                                        | Table cell text objects                                                                      |
| `di(` `di[` `di{` `di"` ``di` `` `di*` `di~` `di_` (and `da`, `ci`, `ca`) | Delimiter text objects                                                                       |
| ``di` `` ``ci` `` ``da` `` ``ca` `` in a fenced block (no code span on the line) | Clear the block's body (`c` keeps an empty line) or the whole block, like Vim's `i{` over lines |
| `C`                                                                       | Change to line end                                                                           |
| `p` / `P`                                                                 | Paste after / before                                                                         |
| `u` / `Ctrl+R`                                                            | Undo / redo                                                                                  |
| `v` / `V`                                                                 | Visual / visual-line mode; then `y` yank, `d`/`x` delete, `c` change, `:` command        |
| `/`, `Ctrl+F`                                                             | Search in note (see [Search](#search))                                                       |
| `:` / `Ctrl+E`                                                            | Command bar                                                                                  |
| `za`                                                                      | Toggle fold                                                                                  |
| `gd`, `Ctrl+]`                                                            | Follow wiki link; `gd` on a variable goes to its definition                                  |
| `K`                                                                       | Preview linked note                                                                          |
| `gx`                                                                      | Preview image at cursor                                                                      |
| `gX`                                                                      | Open image at cursor in the default viewer                                                   |
| `?`                                                                       | Keyboard shortcuts (help)                                                                    |

Yanks are copied to the system clipboard as well as the register.

## Macros

Macros record Normal-mode actions and Insert-mode typing, and replay them.

| Keys      | Action                                                                 |
| --------- | ---------------------------------------------------------------------- |
| `q{r}`    | Start recording into register `r` (`a`-`z`, `0`-`9`; case-insensitive) |
| `q`       | Stop recording (status shows `recorded @r (N steps)`)                  |
| `@{r}`    | Replay register `r`                                                    |
| `{n}@{r}` | Replay `n` times (`3@a`)                                               |
| `Esc`     | Cancel a pending `q` / `@` before the register key                     |

Replays are capped at 10,000 steps; a longer replay stops with `replay aborted: step budget exceeded`.

## Search

In-note search (`/` or `Ctrl+F`) is case-insensitive and highlights every match.

In large notes, previews update after a brief typing pause and matching runs in
the background. Enter starts the search immediately; `n`/`N` pressed while it
is running are applied when the results arrive. Escape cancels the preview and
restores the original cursor and scroll position.

| Key                                | Action                                             |
| ---------------------------------- | -------------------------------------------------- |
| type                               | Jump to the nearest match below the start position |
| `Tab` / `ArrowDown` / `Ctrl+N`     | Next match                                         |
| `Shift+Tab` / `ArrowUp` / `Ctrl+P` | Previous match                                     |
| `Enter`                            | Keep the position (status shows `/query (i/n)`)    |
| `Esc`                              | Cancel and restore the original cursor and scroll  |
| `n` / `N` (Normal)                 | Next / previous match after `Enter`                |

Across notes: `Ctrl+P` with `contains:` shows matching snippets; see [Notes and switching](#notes-and-switching).

### Queries across notes

The note switcher (`Ctrl+P`), browser note filter (`Ctrl+B`) and graph search (`/` in the graph) accept the same query syntax. Enter title, text, tag, and collection terms in the same search bar. The graph searches when you press Enter in the terminal and as you type on the desktop. Plain words in the title switcher and browser keep ordered fuzzy title matching: `cat dog` looks for those letters in order. `cat AND dog` checks each word independently.

At the end of a note-search input, `Ctrl+Right` completes a field name or a matching tag or collection name. Typing `tag:`, `#`, `coll:` or `collection:` opens label suggestions immediately, with no minimum prefix length. Up/Down select a suggestion; Tab or Enter accepts it and quotes spaces automatically. Escape dismisses suggestions before closing the search. The TUI also supports Page Up/Down; the GUI supports scrolling the suggestions. Labels are fetched in pages of 100, with eight visible rows, and typing fetches matches for the new prefix. An exact label leaves Enter available to open a note.

| Syntax | Example | Matches |
| --- | --- | --- |
| `title:` or `h:` | `title:"daily log"` | Title contains the phrase, ignoring case |
| `tag:` or `#` | `#work` | Exact tag name, ignoring case |
| `coll:` or `collection:` | `coll:"Work notes"` | Exact collection name, ignoring case |
| `contains:`, `text:` or `t:` | `contains:"release date"` | Literal phrase in indexed note text |
| `AND`, `OR`, `NOT`, `-`, parentheses | `(tag:work OR #home) AND -title:draft` | Boolean combinations; AND binds tighter than OR |

By default, the desktop shows field glyphs, keeping a quoted value's quotes, and the terminal dims typed field prefixes (`tag:`, `title:`, `contains:`, `coll:`). Set `[search] beautiful = false` in `config.toml` to show the literal query without these decorations in both apps. The query language and results stay the same.

Operator words are case-insensitive, so `and`, `or` and `not` work like their uppercase forms. Spaces between terms mean AND, and redundant whitespace is ignored while evaluating the query. Double quotes keep spaces inside a value; `\"` and `\\` escape a quote and backslash, inside quotes or not, so `contains:say\"hi\"` ranks notes holding `say"hi"` first. The index keeps only words, so punctuation alone, such as `contains:\"`, matches nothing. In search fields of both apps, typing `"` after a field prefix such as `contains:` inserts a closed pair with the cursor inside, typing `"` at a closing quote steps over it, and Backspace inside an empty pair removes both; other text fields type quotes as they are. Multiple tags selected with the browser's `T` control become `tag:` terms joined with AND in the effective query. Collection scope still applies alongside the query.

In note lists, bare title matches rank by fuzzy score, `contains:` matches by full-text relevance, and field-only queries show newer notes first. The index ignores punctuation, so `` contains:```diagram `` also matches a bare `diagram`; notes holding the literal text rank first among the 512 most relevant matches. A better match outranks a pin: notes with the literal text or whole word come first, pinned ones leading, then the other pinned matches, then the rest, each by relevance; when no match is better, pins simply lead. These levels come before relevance, so while a word is unfinished a note that mentions it once as a whole word ranks above a note full of longer words that begin with it; finishing the word with a space drops those prefix-only matches. Graph match cycling follows link degree. `contains:` reads only unprotected notes; a protected note can still match by its title, tags or collections. Consequently, `-contains:secret` includes protected notes because their bodies are absent from the index. Parse errors show a position and leave the previous result list visible. Bare words match titles in every search view, including the terminal's `Ctrl+P` picker, the browser's `Ctrl+F` view, sidebar search, and MCP `search_notes`. An unfinished `contains:rel` matches indexed words beginning with `rel`, and among the 512 most relevant, notes holding the whole word `rel` rank first; a space or a following query term finishes the word and requires an exact match. In `Ctrl+P` in both apps, Enter (or Tab without a suggestion) moves from the query to the results with the best match picked, and a second Enter opens it, even while a word is unfinished; Up from the first result, Tab or Esc return to the query, and typing edits it again. In the terminal browser's `Ctrl+F` view, Enter finishes the word. Quotes (`contains:"rel"`) also require an exact token. Quoted bare text such as `"cat dog"` matches that literal title phrase, while `cat dog` keeps ordered fuzzy matching. Snippet and matching-line views include only unprotected notes.

## Wiki links

Syntax: `[[ID]]`, `[[ID#Heading]]`, `[[ID|Title]]`, `[[ID#Heading|Title]]`. `ID` is the exact full target note ID (ULID or `daily-YYYY-MM-DD`), inserted by autocomplete. IDs are case-sensitive; short prefixes do not resolve. Heading and title do not change target identity.

- Links render collapsed (title only) until the cursor enters them; broken links render distinctly and resolve when the note appears.
- Without a custom label, a missing target shows `ID (no such note)` in both apps, retaining any `#Heading` before the diagnostic. While note titles are still loading after startup, links show their target without it.
- Typing `[[` auto-closes to `[[]]` and opens a note picker; typing `#` inside a link suggests the target note's headings.

| Key                                             | Action                                                                 |
| ----------------------------------------------- | ---------------------------------------------------------------------- |
| `[[`                                            | Insert link and open note autocomplete                                 |
| `ArrowUp` / `ArrowDown`, `Enter` / `Tab`, `Esc` | Pick, accept, cancel a suggestion                                      |
| `Ctrl+]` (any editing mode), `gd` (Normal)      | Open the linked note                                                   |
| `K` (Normal)                                    | Toggle a preview popup of the linked note; moving the cursor closes it |

Markdown links `[text](url)` are styled in place.

## Images and image preview

Syntax: `![alt](./assets/image.png)`. In the editor an image shows as a compact `[image: alt]` placeholder; the raw markdown appears while the cursor is inside it.

- Pasting an image file path imports the image into the note's assets and inserts a relative image link.
- An image itself on the clipboard (a screenshot tool's copy) never reaches the terminal as a paste: `p` / `P` with an empty register import it, as does `:paste-image`. Reading it needs `wl-paste` (Wayland) or `xclip` (X11).
- The preview opens in a bounded dialog using sixel, kitty or iTerm2 graphics (half-blocks as fallback); decoding happens off the input thread and is cached. Inside tmux, passthrough is used when `allow-passthrough` is on.
- Remote (`http://...`) images are never fetched.

| Key                                            | Action                              |
| ---------------------------------------------- | ----------------------------------- |
| `gx` (Normal), `Ctrl+O` (Insert, vim mode off) | Preview the image at the cursor     |
| `gX` (Normal)                                  | Open it in the default image viewer |
| `o` in the preview                             | Open the image in the system viewer |
| `Esc` in the preview                           | Close it                            |

Config (`[terminal]`): `images = "auto" | "sixel" | "kitty" | "iterm2" | "halfblocks" | "off"` (`off` opens the external viewer directly) and `image_max_rows` (1-100, default 15).

## Diagrams

A fenced `diagram` block describes boxes and connectors, one element per line.
It stays plain Markdown text: undo, history, search, sync and export treat it
like any other code block.

````markdown
```diagram
node api rect 0 0 140 60 "API server" fill=#dae8fc stroke=#6c8ebf
node db cylinder 260 0 110 80 "Postgres"
node q rhombus 40 140 120 80 "Cached?"
edge e1 api db "SQL"
edge e2 api q route=orthogonal points=100,120
```
````

- `node <id> <shape> <x> <y> <w> <h> ["label"] [key=value | flag]...`
- Lines indented by two spaces under a `node` line are its body: the label,
  one paragraph per line, so longer text stays readable and editable in the
  note. Blank lines stay in the body when more body lines follow; anything
  not indented ends it. A quoted label and a body join, and a label with a
  line break or over 1 KiB is always written as a body. Inside a body, write
  code fences with the other fence character than the diagram's own (`~~~`
  inside a ```` ``` ```` diagram), since a matching fence closes the diagram.
  When Slate writes a label back and one of its lines would close the
  diagram, it keeps the label quoted on the node line instead.
- `edge <id> <from> <to> ["label"] [key=value | flag]...`; each end is a
  node identifier or a free point `@x,y` (`edge e1 api @300,40`)
- Shapes: `rect`, `rounded`, `ellipse`, `rhombus`, `text`, `cylinder`, `callout`,
  `hexagon`, `clipped`, `triangle`, `actor`, `document`, `cloud`, `gear`, `arrow`. Other
  names draw as `rect` and keep their name.
- Keys: `fill`, `stroke` and `text` take `#rgb`, `#rrggbb`, `#rrggbbaa`
  (with opacity) or `none` (no fill, no outline or no label); `dashed` and
  `dotted` select the outline pattern; `stroke_width=` sets connector and
  outline thickness from 0.5 to 12 (default 1.5).
  `route=straight|orthogonal|curved`; `arrow=none|end|both`; `points=x,y;x,y`
  (waypoints). Unknown keys are kept and ignored.
- Coordinates are whole numbers within ±1,000,000; sizes are positive.
  Labels escape `\"`, `\\` and `\n`; `size=` (6 to 96, default 13),
  `align=left|center|right` and `valign=top|middle|bottom` set size and placement.
  `bold`, `italic` and `underline` format node and connector labels.
  `text` nodes are text blocks: small notes whose label is markdown, best
  written as body lines. Each line is a heading (`#` to `######`, larger and
  bold), a bullet, numbered or checklist item (`- [ ]`, `- [x]`; indent two
  spaces to nest), a quote (`>`), a rule (`---`), a code block line or plain
  text; blank lines add space. Inside them, inline markdown works as in a
  note: `**bold**`, `*italic*`, `~~strike~~`, `` `code` ``,
  `[text](https://…)` and `[[note-id|text]]`. Without `|text` the desktop app
  shows the linked note's title, as in the note text; exports show the id.
  Code is set in the monospace font on a tint. Markers are hidden in the
  picture, canvas and exports; image syntax stays as written. Web links are
  clickable in SVG and PDF exports, and `Ctrl+click` follows a link in the
  picture or on the canvas; on a checkbox it ticks or unticks it, as one undo
  step that rewrites only that line. A text block follows the node's `align` and
  `valign` and is cut with … when it does not fit. Labels of other shapes and of
  connectors are plain text.
  `text_bg=#RRGGBB[AA]` gives labels a background; `text_bg=none` removes it,
  including the default on-screen connector label background.
  A node's label
  wraps to its width and is cut with … when it does not fit its height.
- Identifiers (`[A-Za-z_][A-Za-z0-9_-]*`) are unique per block and shared by
  nodes and edges.

Unreadable lines are kept exactly as written and are not drawn; the picture
shows how many there are. An edge to a missing node is not drawn; a free end is drawn where it is, and moves with a group move or paste when its edge is selected. A repeated
identifier keeps its first definition and makes the block read-only on the
canvas until the source is fixed. Blocks over 256 KiB or 2,000 elements show
their source with a "too large to draw" note; lines over 4 KiB, quoted labels over
1 KiB and bodies over 16 KiB are unreadable.

In the desktop app a block away from the cursor is drawn as one picture.
With the cursor or a selection in it, the block shows its source with the
picture under it, so edits show as they are typed. A folded block shows its
opening line. The terminal shows the source.

On desktop, `:diagram` opens the diagram at the cursor; outside a diagram, it
inserts an empty block and opens its canvas. Clicking a picture also opens the
canvas. In the terminal, `:diagram` inserts an empty diagram block; inside an
existing block it reports that the canvas is desktop-only and changes nothing:

| Input | Action |
| --- | --- |
| Drag a node / several selected nodes | Move: snaps to a 10-unit grid and lines up with other shapes' edges and centres, with guides shown; Shift moves freely |
| Arrow keys (Shift: one unit) | Nudge the selection by a grid step |
| `Ctrl+Z`, `Ctrl+Shift+Z` / `Ctrl+Y` | Undo and redo, one gesture at a time, through the note's history |
| Drag empty space | Select with a box (Shift adds to the selection) |
| Shift+click | Add or remove an element |
| Ctrl+drag, middle-drag / scroll | Pan / zoom (eased unless `[gui] animations = false`) |
| Drag a port (dots on a hovered node) to another node, or to empty space | Connect, or draw a line with a free end |
| Drag an end of the selected edge | Attach it to the node it is dropped on, or leave it free |
| Drag a corner of the selected node | Resize; a live width × height badge shows diagram units |
| Select an edge, drag its handles | Bend through waypoints; double-click a waypoint removes it |
| Shapes panel (left; its header collapses it): click, or drag onto the canvas; `r` `o` `e` `d` `t` `c`; double-click empty space | Add rect, rounded, ellipse, rhombus, text, cylinder |
| Lines panel: click, or drag onto the canvas | Add a free line (plain, arrow, double arrow, orthogonal, curved, dashed); new connections use the last one picked |
| `g` or Grid | Show or hide the alignment grid |
| Fullscreen icon or `F11` | Toggle fullscreen; Esc exits fullscreen before closing the canvas |
| `Enter`, `F2` or double-click an element | Edit its label in place (Shift+Enter breaks the line; `Ctrl+B` / `Ctrl+I` mark the selection bold or italic; Enter or a click elsewhere keeps, Esc cancels) |
| `Ctrl+click` a link in a text block | Open a web link in the browser, or close the canvas and open the linked note |
| `Ctrl+click` a checkbox in a text block | Tick or untick it (also in the note's picture) |
| Properties panel (right) | **Style**: preset fill/line pairs, fill and line colour (the colour picker used by graph groups, with an opacity track; None removes the colour, Theme default resets it), keyboard-editable line width (0.5–12, with half-point steps) beside solid, dashed and dotted previews, and for lines route (straight, elbow, curved) and arrows (none, end, both). **Text**: keyboard-editable size (6–96 pt; Enter applies, Esc cancels), bold/italic/underline, horizontal and vertical alignment, text and background colour. Choose Background → None to remove connector label boxes. **Arrange**: X, Y, width and height of one selected shape. Each change, pick or drag is one undo step |
| `Ctrl+C` / `Ctrl+X` / `Ctrl+V` / `Ctrl+D` | Copy, cut, paste at the pointer, duplicate |
| `Ctrl+S` | Save the note |
| `Delete`, `Backspace`, `x` | Delete (a node's edges go with it) |
| `f`, `+`, `-` | Fit, zoom in, zoom out |
| `Esc` | Cancel the drag in progress, or close |

Fixed connections use `from_port=top|right|bottom|left` and
`to_port=top|right|bottom|left`. Dragging from or onto a side port fixes the
attachment; dropping on a node body uses automatic attachment. Free endpoints
ignore port attributes. The Connector properties expose each attached end's
Auto or fixed side. Fixed ports follow node movement and resizing.

Arrange provides alignment to selection edges/centres, equal-gap distribution
of three or more nodes, and matching width/height to the first selected node.
Edges are excluded from arrangement calculations. Click X/Y/Width/Height values
to enter whole numbers directly; Enter keeps a valid value, Escape cancels.
Invalid values stay open on Enter and are discarded when another gesture starts.
Each arrangement is atomic, including range and serialized-size checks.

Create next (Arrange) adds a same-sized, same-styled neighbour with a 40-unit
gap in the chosen direction, connects fixed facing ports, and opens its blank
label. Creation and connection form one undo step; label editing is separate.
Copy style/Paste style apply supported styling to elements of the same kind,
without copying geometry, labels, endpoints, waypoints, or unknown attributes.
The style clipboard lasts until the canvas closes.

The canvas toolbar's sidebar icons at the left and right independently hide
or show their panels, with arrows and hover labels indicating the action.
The fullscreen icon beside the right sidebar toggle (or `F11`) fills the
screen; closing the canvas restores the window. **Grid** and **Fit** control the view.

Open **Export…** for background and output actions. **Export SVG**
and **Export PNG** save standalone images through the native save dialog.
**Copy PNG** places an image on the clipboard, with progress and completion
shown at the bottom of the canvas. Choose transparent or white background.
PNGs are drawn at twice the diagram's size, sharp on HiDPI screens and in
documents. Export uses the
current diagram snapshot, preserving fixed ports, curves, styles and clipped
labels; unreadable lines or missing endpoints must be fixed before exporting.
The note itself is unchanged. A PNG is at most 16384 pixels per side and 16
megapixels: a larger diagram is drawn smaller, and the status line names the
scale used. SVG has no size limit.

An exported SVG also carries a draw.io copy of the diagram, so draw.io opens
it for editing (File > Open, or name it `*.drawio.svg`). The copy is one-way
and lossy: positions, labels, colours, line styles, ports and waypoints carry
over, and text blocks with markdown become draw.io HTML labels; `clipped`, `document`, `actor` and `callout` use their nearest draw.io
shapes, `gear` becomes an ellipse, and draw.io redraws curves its own way.
Edits made in draw.io do not come back to the note.

PDF export renders diagram blocks as images on white backgrounds. If a block
cannot be rendered or exceeds the image budget, the PDF includes its source and
an explanation. Markdown export keeps the editable fenced source.

Each finished gesture changes only the lines it touches and is one undo step
in the note. A gesture whose block changed meanwhile (moved, edited, or no
longer a diagram) is refused and the canvas reloads.

## Inline calculations

Lines that evaluate show a ghost result on the right; non-math lines stay quiet.

```text
200 * 1.19              → 238
50 kg to lbs            → 110.231 lb
sqrt(144) + 3^2         → 21
```

- Arithmetic, percentages, unit conversions and everything [fend](https://github.com/printfn/fend) evaluates.
- Works on plain lines, list/checklist bodies, and table formula cells.
- Date-like lines (`2026-09-29`, `29.09.2026`, `09/29/2026`) are ignored.
- Clock times and ranges, see below.
- Large notes compute only the visible region and fill values in off the input thread.

| Key / command                 | Action                                                                   |
| ----------------------------- | ------------------------------------------------------------------------ |
| `Tab` (Insert)                | Replace the expression with its result (after any open completion popup) |
| `:sum` / `:avg`               | Sum / average the selection, or the whole note without one               |

`:sum` and `:avg` count each variable, formula and formula cell as its computed value, other table cells as their own expression (units kept), and other text as the numbers in it, skipping list markers. The result is inserted after the selection (at the cursor without one) and copied.

The terminal status bar shows sum, average and count only while text or table
cells are selected. These live statistics extract numeric literals, skip list
markers and digits belonging to names such as `usteda_13`, and do not replace
the expression-aware `:sum` / `:avg` commands. An unindented decimal such as
`3434.5 kg` is a number, not nested list numbering; nested numbering such as
`2.1` is recognized on indented lines.

### Clock times

```text
09:10-11:45                → 2h 35min
09:10-11:45 + 13:00-17:30  → 7h 5min
11:45 - 09:10              → 2h 35min
09:10 + 2h 30min           → 11:40
9am-5pm - 30min            → 7h 30min
22:00-02:00                → 4h
(17:00 - 09:00) / 3        → 2h 40min
10:30-11:00 standup        → 30min
```

- Clock times: `09:10`, `9:10:30`, `9:10pm` / `9:10 pm`, `9am` (a bare hour needs `am`/`pm` attached, so `5 pm` stays picometres), `24:00`.
- A range is two clock times joined by `-` with no spaces; it runs forward, past midnight if it ends before it starts (`00:00-24:00` is a whole day). With spaces, `-` subtracts.
- Clock time - clock time is a duration and clock time ± duration a clock time; adding, multiplying or dividing clock times gives no result.
- Results read as `2h 35min` and `11:10`, so `Tab` and variables keep them: `start := 09:10`, `lunch := 12:00-12:45`, then `17:30 - start - lunch`.
- A clock time on its own (`meeting at 10:30`) shows no result. Words after a calculation are a label (`11:45 - 09:10 work` → `2h 35min`), but a line with more times or arithmetic after its words shows nothing (`9:00-17:00 office, 12:00-12:30 lunch`): put each range on its own line. `to` / `in` converts a duration as usual: `(17:00 - 09:00) to min`; a clock time does not convert.
- A variable holding a clock time or duration is not offered to other notes yet. Durations written directly (`lunch := 45min`) keep only their number, like other units in variables.
- `:sum` / `:avg` do not add up ranges yet.

## Variables and cross-note variables

- Assign with `name := expression`; reference by name anywhere in the note. Names are case-insensitive and may contain spaces.
- Dependents update as definitions change; conversions store numeric values (`len := 3 m to km`).
- `gd` (Normal) on a variable jumps to its definition (the last assignment, the one in effect). On `[[id]].name` it opens the other note at that definition.
- Variable names are highlighted; an autocomplete popup appears after `[editor] variable_autocomplete_min_chars` (default 3) characters.
- Another note's variable: `[[ID]].name` (needs the `cross_note` module); typing `[[ID]].` suggests that note's variables.

| Key                     | Action                     |
| ----------------------- | -------------------------- |
| `ArrowUp` / `ArrowDown` | Move in the variable popup |
| `Tab` / `Enter`         | Accept the suggestion      |
| `Esc`                   | Close the popup            |

Full rules: [Variables Specification](variables.md).

## Tables

Markdown tables align as you type, and the cursor moves by cell.

- Formula cells start with `:=`: `:=sum_col()`, `:=avg_row() * 2`, `:=tax_rate * subtotal`, `:=(1,2) + (2,2)` (1-based data-row references). `.` means the formula's own row or column, with an optional offset: `:=(.,2) * (.,3)` multiplies two cells of the same row, `:=(.-1,.) + (.,4)` keeps a running total. Such a formula reads the same in every row. To copy a formula, select cells with `Shift+Arrows` from it and press `Ctrl+D` (down) or `Ctrl+R` (right); in the desktop app you can also drag the dot on the focused cell's corner, as in a spreadsheet. Numbered references move with each copy: `:=(4,2)-(3,2)` filled one row down becomes `:=(5,2)-(4,2)`; `.` references are kept as written, and `$` pins a number so fills keep it: `:=(.,2) * ($1,$4)` always reads cell (1,4). A filled date continues as a series, a day per row or column, kept in its own format: `03. November 2026.`, `2026-11-03`, `3.11.2026.`, `3 Nov 2026` and `November 3, 2026` are recognised.
- Helpers: `sum_row()`, `sum_col()`, `avg_row()`, `avg_col()`. Typing a helper name in a formula cell (`sum`, `avg_`) offers them in the autocomplete popup, with matching variables after.
- Reference errors render as `!ERROR#out_of_bounds`, `!ERROR#non_numeric`, `!ERROR#self_reference`, `!ERROR#cycle`.
- Multiline cells use continuation rows starting with `|>`.
- Pasting CSV or TSV (cells copied from a spreadsheet) makes a table, the first row its header: on a blank line in its place, otherwise below the cursor's line; `p` / `P` from the system clipboard paste it as whole lines. TSV needs the same number of tabs on every row; CSV (`,` or `;`, `"`-quoted fields) also needs no space after a delimiter, so prose like `Hello, world` stays text. Inside a code block or a table, or with the table module off, the paste stays text.

| Key (Insert)                                | Action                                                          |
| ------------------------------------------- | --------------------------------------------------------------- |
| `\|`                                        | Start a row / add a column where applicable                     |
| `Tab` / `Shift+Tab`                         | Next / previous cell                                            |
| `Ctrl+ArrowLeft` / `Ctrl+ArrowRight`        | Previous / next cell                                            |
| `ArrowLeft` / `ArrowRight`                  | Move within the cell, then cross into the next                  |
| `ArrowUp` / `ArrowDown`                     | Same column, previous / next row                                |
| `Shift+Enter`                               | Split the cell into a `\|>` continuation row                    |
| `Backspace` / `Delete`                      | Cell-aware delete at cell boundaries                            |
| `Ctrl+Backspace` / `Ctrl+Delete` / `Ctrl+W` | Structural edit: merge cells or delete a column from the header |

Vim: `di|`, `ci|`, `yi|`, `da|` work on cells. Select rows and `:sum` / `:avg` to aggregate them.

## Folding

Fold and unfold the block at the cursor.

| Key / command                  | Action                |
| ------------------------------ | --------------------- |
| `za` (Normal)                  | Toggle fold at cursor |
| `:fold` (`:zc`, `:closefold`)  | Fold                  |
| `:unfold` (`:zo`, `:openfold`) | Unfold                |
| `:fold-toggle` (`:za`)         | Toggle                |

## Dates and reminders

| Command              | Action                                                                           |
| -------------------- | -------------------------------------------------------------------------------- |
| `:date`              | Pick a date and insert it (`[editor] date_format`; `date_time_format` with time) |
| `:remind` (`:alarm`) | Set a reminder on the current line (date + time)                                 |
| `:remind toggle`     | Remove the line's reminder, or set one if there is none                          |
| `:today` (`:daily`)  | Open today's daily note                                                          |

Date picker: type `tomorrow`, `next friday 10 pm`, or `in 3 weeks` in its input. Left/right arrows move the input caret. `Tab` switches focus between the input and calendar. With calendar focus, arrows move by day/week, `PageUp`/`PageDown` (or `Ctrl+ArrowLeft`/`Ctrl+ArrowRight`) by month, `Alt+ArrowLeft`/`Alt+ArrowRight` by hour, and `Alt+ArrowUp`/`Alt+ArrowDown` by one minute. `Ctrl+T` toggles time, `Enter` confirms, and `Esc` cancels. Typed dates and the calendar share the configured formats.

Reminders show as a ghost on their line and fire a desktop notification (`notify-send`) when due; setting and removing them is undoable.

## Lookup

| Key / command                                           | Action                                                |
| ------------------------------------------------------- | ----------------------------------------------------- |
| `:lookup [query]`                                       | Open the lookup overlay (runs the query if given)     |
| type, `Enter`                                           | Run the search                                        |
| `ArrowUp` / `ArrowDown`                                 | Select a result                                       |
| `Enter` on a result                                     | Open it in the browser (HTTP(S) only)                 |
| `Shift+Enter` on a result                               | Insert it as a markdown link at the cursor            |
| `Esc`                                                   | Close                                                 |

Config `[web_search]`: `provider = "auto" | "brave" | "google" | "duckduckgo"`, `api_key`, `search_engine_id`, `max_results` (1-10). Keyed providers fall back to DuckDuckGo on failure.

## Ask the agent

Off by default; see [Ask the Agent](agent.md) for setup, what is sent and what the agent can reach.

| Key / command           | Action                                                           |
| ----------------------- | ---------------------------------------------------------------- |
| `:ask [prompt]`         | Ask the local agent (Claude Code, Codex or a custom command)     |
| `Esc`                   | Cancel a running request, or close                               |
| `Enter`                 | Insert the answer at the cursor                                  |
| `ArrowUp` / `ArrowDown` | Scroll the answer                                                |
| `/`                     | Ask again                                                        |

The note is saved first. Edits the agent makes to the open note arrive as one undo step.

## Clipboard and clip-watch

- Vim yanks and `:export markdown` / `:export text` without a path go to the system clipboard (status shows the backend used): through `wl-copy`, `xclip`, `xsel`, `pbcopy`, `clip.exe` or tmux, otherwise OSC 52. With `[terminal] clipboard = "osc52"` copies go only through OSC 52, so the terminal holds them: they outlive slate and work over SSH, but a terminal without OSC 52 support drops them silently.
- Clipboard text is read natively (Wayland data-control or X11), with the same tools as a fallback.
- Pasted text is inserted as-is (no autoformat pass).

| Command                    | Action                                                    |
| -------------------------- | --------------------------------------------------------- |
| `:clip-watch on` (`start`) | Watch the clipboard and paste each new text at the cursor |
| `:clip-watch off` (`stop`) | Stop watching                                             |
| `:paste-image`             | Paste the image on the clipboard at the cursor            |

## Collections

Collections group notes; the working collection is session-scoped and applies to new notes and the `Ctrl+P` switcher.

| Key / command                                         | Action                                                                                         |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `Ctrl+G`                                              | Collection picker (type to filter, `Enter` set working collection, `Ctrl+E` edit, `Esc` close) |
| `:collection create <name>`                           | Create                                                                                         |
| `:collection choose [name]` / `choose none` / `clear` | Set / clear the working collection; omit the name to open the picker                             |
| `:collection join [name]` / `leave [name]`            | Add / remove the current note; without a name, open its Organize dialog on collections           |
| `:collection update <name>`                           | Edit name, description and default tags (`Tab` between fields, `Enter` save)                   |
| `:collection delete <name>`                           | Delete the collection only                                                                     |
| `:collection purge <name>`                            | Delete the collection and its notes                                                            |

### Collection browser

The browser footer shows only the main actions. Press `a` for **Actions** or `?` for contextual shortcuts: choose with Up/Down (or j/k), run with Enter, and close with Esc. Existing direct shortcuts still work. The popup follows the focused note or collection, exposes batch actions when notes are selected, and keeps deletion behind its existing confirmation.

`Ctrl+B`, `-` in Normal mode, or `:browse` (`:explore`, `:files`) opens a full-screen browser in three columns, like the yazi file manager: collections on the left, the notes of the open collection in the middle and a preview of the hovered note (title, age, collections, tags and the start of the body) on the right. `All notes` and `Unsorted` (notes in no collection) sit above the collections. It opens on the working collection with the current note hovered and title search focused. Type to filter immediately, or press `Esc` to navigate.

`Ctrl+F` (or `Ctrl+/`) searches note text inside the open collection. Hits show the line they matched on, the preview scrolls to that line with the search terms highlighted, and `Enter` opens the note there. Title filtering, text search, and tag filtering use the same bordered input style above the results.

Tags classify notes across collections (for example `meeting` or `idea`); collections provide the workspace and defaults for new notes. On the terminal notes list, `t` edits the hovered note's comma-separated tags: `Enter` replaces its tags, an empty input removes them all, and `Esc` cancels. Marked notes are unaffected. Tags are saved immediately as metadata, independently of note text and its undo history. The terminal preview wraps tags across at most three lines, with an additional overflow indicator when needed, while reserving space for the note text.

From the editor, `:tag add work` and `:tag remove work` add or remove one tag on the open note (names match in any case; spaces are part of the name, commas are refused). Without a name, both open the note's Organize dialog, as do `:tag` and `:organize`, *Organize…* in the GUI note header, or clicking a tag or the collections label there. The dialog lists the note's tags (or, after Tab, its collections) first and marked, then every other one; typing searches and offers to create a new tag, Enter adds or removes the highlighted row, and Esc returns to the note. File-backed notes have no tags.

`T` accepts comma-separated exact tags (for example `work, urgent`), requiring every tag to match (AND). Matching ignores letter case, including Unicode and surrounding spaces; spaces within a tag are preserved. The tag filter combines with the open collection, `/` title filtering, and `Ctrl+F` text search. The header shows `tags: work AND urgent`; an unknown tag gives an empty list. Set an empty tag filter or press `Esc` after clearing any selection and title filter or leaving text search to clear it. The filter survives changing collections, and resets when the browser closes. Collection counts still show total membership. New notes receive collection default tags, not the active browser filter.

A note can belong to several collections, so notes are copied into collections rather than moved like files: `y` then `p` adds a note to another collection, `x` then `p` moves it out of the collection it was cut from, and `d` removes it from the open collection without deleting it. `u` undoes the last of these.

| Key                                                | Action                                                                                                                                                               |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `j` / `k`, arrows, `gg` / `G`, `Ctrl+D` / `Ctrl+U` | Move                                                                                                                                                                 |
| `o`, `l`, `Enter`                                  | Open the collection or note (asks for the password of a locked note or encrypted collection)                                                                         |
| `h`, `-`, `Backspace`                              | Back to the collections list                                                                                                                                         |
| `/`                                                | Filter the list (fuzzy); `Esc` clears it                                                                                                                             |
| `t` / `T`                                          | Edit the hovered note's tags / set a single tag filter (empty input clears)                                                                                          |
| `Ctrl+F`, `Ctrl+/`                                 | Search note text in the open collection (or the hovered one): type to search, `↑` `↓` / `Ctrl+N` `Ctrl+P` move, `Enter` opens the note at the match, `Esc` goes back |
| `Space` / `Ctrl+A`                                 | Mark the note and move down / mark all                                                                                                                               |
| `y` / `x`                                          | Yank / cut the marked (or hovered) notes                                                                                                                             |
| `p`                                                | Paste into the open or hovered collection: copy adds the notes to it, cut moves them                                                                                 |
| `d`                                                | Leave: take the notes out of the open collection (the notes stay)                                                                                                    |
| `u`                                                | Undo the last paste or remove                                                                                                                                        |
| `D`                                                | Delete the notes, or the hovered collection (its notes stay); `y` confirms, and a protected note asks for its password instead                                       |
| `n` / `r`                                          | New note (in the open collection) or collection / rename the hovered one (a note keeps the name; empty follows its first line)                                       |
| `e`                                                | Encrypt the hovered collection, or decrypt an encrypted one                                                                                                          |
| `s`                                                | Sort notes by modification time or title                                                                                                                             |
| `w`                                                | Make the collection the working collection (`All notes` clears it)                                                                                                   |
| `R`                                                | Reload                                                                                                                                                               |
| `q`, `Esc`, `Ctrl+B`                               | Close                                                                                                                                                                |

Icons use Nerd Font glyphs by default; set `[theme] icons = "unicode"` or `"ascii"` for other fonts.

## Per-note modules

Each note stores its own module switches; `[editor.modules]` sets defaults for new notes.

| Module       | Controls                                       |
| ------------ | ---------------------------------------------- |
| `math`       | Master calc switch                             |
| `table`      | Table formulas                                 |
| `variables`  | Variable assignments, references, autocomplete |
| `style`      | Markdown styling helpers                       |
| `cross_note` | `[[ID]].name` references                  |

Commands: `:module status` (`:modules`), `:module <name> on|off|toggle` (also `:module on <name>`).

## Note security

| Command         | Action                                                                                     |
| --------------- | ------------------------------------------------------------------------------------------ |
| `:note encrypt` | Encrypt the note with its own password; on an unlocked encrypted note, change its password |
| `:note decrypt` | Store it unencrypted again                                                                 |

Both ask for the password in a masked dialog, and encrypting asks for it twice.

An encrypted note's text and history are sealed with its own random key, and the password only unlocks that key, so changing a password does not rewrite the note. Its title stays visible (encrypting pins it; rename it to something vaguer, or clear it to show "Encrypted note"). Renaming an encrypted note asks for its password first. Opening one asks for the password and keeps it unlocked for 15 minutes of inactivity.

**Encrypted collections.** `e` on a collection in the browser encrypts it with a password (asked twice): its notes are encrypted with the collection's key, with their titles pinned, and notes created in it, pasted into it or added with `:collection join` are encrypted too. Entering the collection or opening any of its notes asks for its password once and unlocks all of them. While a note belongs to the collection it cannot be decrypted on its own or given its own password (`:note decrypt` and `:note encrypt` are refused); remove it from the collection or decrypt the collection instead. A note that leaves the collection stays encrypted with the collection's password until the collection is decrypted (`e` again), and can then also be decrypted or given its own password; a collection that still protects notes cannot be deleted. Notes that were locked, or belong to another encrypted collection, keep their own protection.

Reminder text and images attached to encrypted notes are still stored unencrypted.

`[editor.security] encrypt_notes = true` encrypts new notes by default using the password in `password_env`. Not available for file-backed notes.

## Export and backup

| Command                     | Action                                                                 |
| --------------------------- | ---------------------------------------------------------------------- |
| `:export pdf <path>`        | Markdown-aware PDF (headings, lists, code, tables, images, checklists) |
| `:export markdown [path]`         | Markdown to a file, or the clipboard without a path                    |
| `:export text [path]`        | Plain text to a file, or the clipboard                                 |
| `:backup export <path.zip>` | Back up the whole notes database (runs in the background)              |
| `:backup export md <directory>` | Export Markdown files in collection folders; write each note once |
| `:backup load <path>`   | Detect a Slate ZIP backup or a Markdown directory/ZIP; restore or add notes accordingly |

Details: [Export Reference](export.md).

## IMAP email sync

- `slate imap-sync` pulls new messages once; `[imap] auto_sync_on_startup = true` polls in the background while Slate runs.
- Messages are appended to daily inbox notes (`inbox-email-YYYY-MM-DD` by default), newest first, with UID checkpoints so nothing is imported twice.
- First sync only takes recent mail (`initial_sync_past_days`, default 1). New mail triggers a desktop notification.
- Any IMAP-over-TLS provider works; the password comes from `password_env`. Build without IMAP: `cargo build -p slate --no-default-features`.

## MCP server

`slate mcp` lets AI assistants and bots (Claude Code, Codex, opencode, any MCP client) list, search, read, create and edit notes over stdio. It is off until `[mcp] enabled = true`. Clients can also rename notes, manage collection membership and archive notes. Writes are checked against the revision the client read, encrypted and file-backed notes stay closed, and deleting is off unless `[mcp] allow_delete = true`. Setup for each client and the tool list: [MCP Server](mcp.md).

## Themes, wrap and other settings

- `[theme] color_scheme` (14 schemes, default `gruvbox-light`) and `accent`; config changes reload live.
- `[theme.colors]` replaces single colours with exact hex, or `none` for the terminal's own (e.g. a transparent background); see [configuration](configuration.md#themecolors).
- `[editor] wrap`, `markdown_autoformat`, `checklist_auto_reorder`, `autosave`, `format_on_save`, `vim_mode`, `date_format`, `date_time_format`, `variable_autocomplete_min_chars`.

All keys: [Configuration](configuration.md).

## Diagnostics

| Command                       | Action                                    |
| ----------------------------- | ----------------------------------------- |
| `:perf status`                | Show perf tracing state                   |
| `:perf toggle` / `on` / `off` | Toggle tracing                            |
| `:perf dump [top]`            | Write the slowest buckets to the perf log |
| `:perf where`                 | Show the log path                         |
| `:perf cap <n>`               | Samples kept per bucket                   |

Planned features: [`roadmap/features.md`](https://github.com/dborovcanin/slate/blob/main/roadmap/features.md).

## Table of contents

`:toc` (or `:outline`) opens a heading picker for the current note in the terminal and desktop apps. Headings appear in document order, indented by level, with their line numbers. Duplicate titles remain separate; headings inside fenced code blocks are excluded.

Type to filter headings with case-insensitive fuzzy matching. Use Up/Down or `Ctrl+N`/`Ctrl+P` to choose, Page Up/Down to move ten headings, and Enter to jump. Left/Right, Home/End, Backspace, and Delete edit the query. Escape closes without moving. The picker starts on the section containing the cursor and reveals enclosing folds when jumping. In the desktop app, click a heading to jump. Opening the picker again reads the current text; it never inserts or changes note content.

### Generated TOC sections

`:toc insert` inserts a generated section above the cursor's line, keeping the cursor on the original text. Move outside code blocks, lists, and tables before inserting:

````markdown
```toc
**Table of contents**

- [Introduction](#introduction)
  - [Setup](#setup)
- [Usage](#usage)
```
````

The contents render as Markdown in both apps. Headings inside code fences are excluded; duplicate headings receive distinct link anchors. Use `gd` in Vim mode or `Ctrl+]` on an entry to jump to its heading, revealing enclosing folds.

`:toc refresh` regenerates every existing `toc` section in the current note, replacing only the text between its fences. Each insert or refresh is one undoable change. Heading edits do not update a TOC automatically; refresh when needed. An unchanged refresh does not add an undo entry. To remove a TOC, delete its fenced section.

You can also write a closed, empty `toc` fence yourself and run `:toc refresh`. Unfinished TOC fences must be closed first. Ordinary code examples containing a `toc` fence are left alone. The generated text and fences are saved with the note. Exports unwrap closed TOC fences: PDF shows a formatted heading list, and Markdown/text exports contain the stored TOC body without its fences. Export does not regenerate stale entries; run `:toc refresh` first when needed.

## Note graph

`:graph` shows how notes link to each other through `[[id]]` wiki links, in the terminal and desktop apps. It fills the view in both apps, hiding the note and editor controls until you close it. It opens on the current note and the notes within two link hops of it, following links in both directions. Links inside code blocks and inline code do not count, and notes that are encrypted contribute no links.

Nodes are laid out by a force simulation: linked notes pull together, unrelated ones push apart. The layout is the same every time for the same links. `◆` marks the centre note, `◉` the selection, and `○` a link to a note that no longer exists. The arrow keys or `h`/`j`/`k`/`l` move the selection to the nearest node in that direction, and Tab/Shift+Tab step through all nodes. Enter opens the selected note. `c` (or Space) recentres the graph on it, `+`/`-` change the number of hops (1 to 4), and `w` toggles between the local graph and every note. Neither view limits the number of nodes. Escape closes the view.

The desktop advances graphs of up to 2,000 nodes one layout step per frame on the UI thread; larger graphs animate snapshots from a worker. While dragging a node in a graph with more than 2,000 nodes, only that node moves; settling resumes after release. Smaller graphs keep settling around the pinned node during the drag. The terminal settles graphs of up to 1,000 nodes immediately; larger graphs use a worker and show a loading panel until settled. Closing or rebuilding a view cancels its old layout work. Views with more than 2,000 on-screen nodes omit ordinary labels, keeping the selection's label (and the hovered node's on desktop); zooming into a sparse cluster restores ordinary labels. Only visible background edges count toward drawing budgets, and every visible link touching the focused node is kept. These drawing reductions do not change which notes and links are in the graph or available to navigation and search.

In the terminal, `/` finds notes in the graph by title: Enter selects the best match, and `n`/`N` step through the others. `]` and `[` zoom in and out, Shift+`H`/`J`/`K`/`L` pan, and `0` shows the whole graph again; when zoomed in, the view follows the selection.

The link index refreshes in the background each time the graph opens, rescanning only notes edited or renamed since the last time. The first open reads every note once and shows its progress ("Indexing links…") until it finishes; later opens show the graph at once and update it if anything changed.

Note text containing embedded NUL characters is rejected on save because SQLite text operations cannot reliably preserve its search locations. Existing note data is not rewritten.

Search accepts unquoted URLs, times such as `10:30`, and ordinary titles such as `Re: meeting` as bare title terms. Known fields still take precedence (`title:10:30`); close field-name typos such as `titel:daily` report an error.

A positive `contains:` query shows matching body excerpts in paged note lists as well as the matching-snippet view. The browser preview highlights and focuses the body hit. Opening a result with a body hit places the cursor on that source line, in either app. Title-only and metadata-only results keep normal opening behavior.

### Diagram captions

Add plain text after the opening fence language, for example
````diagram System overview`. It appears as a centered caption below the
inline diagram and in PDF exports, including source fallback. Captions wrap
within the preview width and add no source line or separate line number.
Markdown keeps the opening fence; standalone SVG and PNG images omit captions.
