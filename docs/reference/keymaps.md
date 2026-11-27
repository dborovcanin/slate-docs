# Keymaps

Key tables by mode. The [Feature Guide](features.md) lists the same keys grouped by feature.

**Insert** is the text-editing mode; **Normal** is vim normal mode (`Esc` from Insert; `[editor] vim_mode = true` starts there).

## Everywhere

| Key      | Action                                       |
| -------- | -------------------------------------------- |
| `F4` / `:info` | Current note information (from the editor) |
| `F11` / `:read` | Read mode (from the editor) |
| `Ctrl+Q` | Quit                                         |
| `Ctrl+P` | Note switcher                                |
| `Ctrl+G` | Collection picker                            |
| `Ctrl+B` | Collection browser (also `-` in Normal mode) |
| `Ctrl+E` | Command bar (Insert, Normal, Visual)         |
| `Ctrl+]` | Follow wiki link at cursor (Insert, Normal)  |
| `Ctrl+S` | Save (in Insert only while autosave is on)   |

## Insert mode

| Key                                   | Action                                                                                                  |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `Ctrl+N`                              | New note                                                                                                |
| `Ctrl+F`                              | Search in note                                                                                          |
| `Ctrl+O`                              | Preview image at cursor (vim mode off)                                                                  |
| `Tab`                                 | Accept completion, else apply calc result, else next table cell, else indent list item, else two spaces |
| `Shift+Tab`                           | Previous table cell / outdent list item                                                                 |
| `Enter`                               | New line, continue list, or accept popup selection                                                      |
| `Shift+Enter`                         | Split table cell into a `\|>` continuation row                                                          |
| `Ctrl+W`, `Ctrl+Backspace`            | Delete word before cursor (table-aware)                                                                 |
| `Ctrl+Delete`                         | Delete forward (table-aware)                                                                            |
| `Ctrl+ArrowLeft` / `Ctrl+ArrowRight`  | Previous / next word (previous / next cell in tables)                                                   |
| `ArrowUp` / `ArrowDown`               | Screen-row motion on wrapped lines; same column in tables; popup selection                              |
| `Home` / `End`, `PageUp` / `PageDown` | Line start / end, page up / down                                                                        |
| `[[`                                  | Insert wiki link and open note autocomplete                                                             |
| `Esc`                                 | Close popup, else Normal mode                                                                           |

## Normal mode

| Key                                                      | Action                                                                  |
| -------------------------------------------------------- | ----------------------------------------------------------------------- |
| `h` `j` `k` `l`, arrows                                  | Move (counts supported)                                                 |
| `w` / `b`, `e`                                           | Next / previous word, end of word                                       |
| `0` / `$`, `Home` / `End`, `^`                           | Line start / end, first non-blank character                             |
| `f{c}` / `F{c}`, `t{c}` / `T{c}`                         | Onto / till the next or previous `c` on the line (counts supported)     |
| `;` / `,`                                                | Repeat the last find, same / other direction                            |
| `%`                                                      | Bracket matching the next one on the line                               |
| `gg` / `G`, `{n}G`                                       | First / last / `n`th line                                               |
| `gj` / `gk`                                              | Screen row down / up on wrapped lines                                   |
| `i` `a` `I` `A` `o` `O`                                  | Enter Insert                                                            |
| `x`, `p` / `P`                                           | Delete char, paste after / before                                       |
| `s` / `S`                                                | Substitute character / line text and enter Insert                       |
| `D`, `J`                                                 | Delete to line end, join lines (`3J` joins three)                       |
| `.`                                                      | Repeat the last change, including typed text (`3.` replaces its count)  |
| `r{c}`, `{n}r{c}`                                        | Replace char(s) under the cursor with `c`                               |
| `dd` `yy` `cc` `C`                                       | Delete / yank / change line, change to line end                         |
| `d` `y` `c` + `w` `b` `e` `0` `$` `^` `%`                | Operator + motion; `cw` changes to the word's end, as in Vim            |
| `d` `y` `c` + `f` `F` `t` `T` `{c}`                      | Operator + find (`df,`, `ct)`, `yT(`)                                   |
| `iw` `aw` `i\|` `a\|`                                    | Word and table-cell text objects (`diw`, `yi\|`, ...)                   |
| `i(` `i[` `i{` `i"` `` i` `` `i*` `i~` `i_` (and `a...`) | Delimiter text objects for `d` and `c`                                  |
| `` di` `` `` ci` `` `` da` `` `` ca` `` in a fenced block          | Without a code span on the line: clear the body (`c` keeps an empty line) or the whole block |
| `u` / `Ctrl+R`                                           | Undo / redo                                                             |
| `v` / `V`                                                | Visual / visual-line                                                    |
| `/`, `Ctrl+F`                                            | Search; `n` / `N` next / previous match                                 |
| `:`                                                      | Command bar                                                             |
| `q{r}` ... `q`, `@{r}`, `{n}@{r}`                        | Record, stop, replay macro                                              |
| `za`                                                     | Toggle fold                                                             |
| `gd`                                                     | Follow wiki link, or go to the definition of the variable at the cursor |
| `K`                                                      | Toggle linked-note preview; elsewhere, inspect the line's result        |
| `gx`                                                     | Preview image at cursor                                                 |
| `gX`                                                     | Open image at cursor in the default viewer                              |
| `?`                                                      | Keyboard shortcuts (the help list, with how each key works)             |

After a prefix (`g`, `d`, `y`, `c`, `ci`, `q`...) the status line lists the keys that may follow and what each does, as the desktop status bar does; `Esc` cancels.

## Visual and visual-line mode

| Key                                      | Action                                                     |
| ---------------------------------------- | ---------------------------------------------------------- |
| motions, counts, `gg` / `G`, `gj` / `gk` | Extend selection                                           |
| `y`                                      | Yank (also to system clipboard)                            |
| `d` / `x`                                | Delete                                                     |
| `c`                                      | Change: delete the selection and enter Insert              |
| `e` `^` `f` `F` `t` `T` `;` `,` `%`      | Extend selection with the same motions as Normal mode      |
| `:` / `Ctrl+E`                           | Command bar on the selection (format, list, calc commands) |
| `v` / `V` / `Esc` / `Ctrl+C`             | Leave visual mode                                          |

## Table editing (Insert)

| Key                                                       | Action                                                   |
| --------------------------------------------------------- | -------------------------------------------------------- |
| `ArrowLeft` / `ArrowRight`                                | Move within cell content; cross cells at boundaries      |
| `ArrowUp` / `ArrowDown`                                   | Same column, previous / next row                         |
| `Tab` / `Shift+Tab`, `Ctrl+ArrowLeft` / `Ctrl+ArrowRight` | Next / previous cell                                     |
| `Shift+Enter`                                             | Split cell into multiline continuation row (`\|>`)       |
| `Backspace` / `Delete`                                    | Cell-aware boundary edit                                 |
| `Ctrl+Backspace` / `Ctrl+Delete` / `Ctrl+W`               | Structural edit (merge cells, delete column from header) |

## Table cell selection (Normal and Insert)

| Key                         | Action                                                              |
| --------------------------- | ------------------------------------------------------------------- |
| `Shift+Arrows`              | Select a rectangle of whole cells; outside a table, move as arrows  |
| `Ctrl+D` / `Ctrl+R`         | Fill down / right from the cell the selection started at (one undo) |
| `Delete` / `Backspace`      | Clear the selected cells                                            |
| `y` (Normal) / `Ctrl+C`     | Copy the cells as tab-separated rows and drop the selection         |
| `Esc`                       | Drop the selection; any other key drops it and acts as usual        |

## Popups (variables, wiki links)

| Key                     | Action         |
| ----------------------- | -------------- |
| `ArrowUp` / `ArrowDown` | Move selection |
| `Tab` / `Enter`         | Accept         |
| `Esc`                   | Close          |

## In-note search (`/`)

| Key                                | Action                            |
| ---------------------------------- | --------------------------------- |
| `Tab` / `ArrowDown` / `Ctrl+N`     | Next match                        |
| `Shift+Tab` / `ArrowUp` / `Ctrl+P` | Previous match                    |
| `Enter`                            | Keep position                     |
| `Esc`                              | Cancel, restore cursor and scroll |

## Note switcher (`Ctrl+P`)

Popup with one query bar for titles, tags, collections and note text; the title shows a collection scope when active.

| Key                        | Action                                                           |
| -------------------------- | ---------------------------------------------------------------- |
| type                       | Search titles; use `contains:` for note text                    |
| `Enter`, `Tab` (query)     | Move to the results, best match picked (`Tab` first accepts a completion) |
| `ArrowUp` / `ArrowDown` (query) | Recall earlier searches; `Down` past the newest moves to the results |
| `ArrowUp` / `ArrowDown` (results) | Move selection; `Up` from the first row returns to the query |
| `Enter` (results)          | Open note at the matching line (asks for password if protected)  |
| `Tab`, `Esc`, typing (results) | Back to the query                                            |
| `Ctrl+L`                   | Toggle working collection / all notes                            |
| `Ctrl+N`                   | New note                                                         |
| `Ctrl+G`                   | Collection picker                                                |
| `Ctrl+R`                   | History of the selected note                                     |
| `Delete`                   | Delete selected note (`y` / `Enter` confirm, `n` / `Esc` cancel) |
| `Ctrl+W`, `Ctrl+Backspace` | Delete last query word                                           |
| `Esc` / `Ctrl+P`           | Close                                                            |

## Collection picker (`Ctrl+G`)

Popup listing collections with note counts; `All notes` clears the working collection.

| Key                           | Action                                                                           |
| ----------------------------- | -------------------------------------------------------------------------------- |
| type, `ArrowUp` / `ArrowDown` | Filter, move selection                                                           |
| `Enter`                       | Set working collection                                                           |
| `Ctrl+E`                      | Edit collection (`Tab` / `Shift+Tab` between fields, `Enter` save, `Esc` cancel) |
| `Esc` / `Ctrl+G` / `Ctrl+P`   | Close                                                                            |

## Collection browser (`Ctrl+B`, `-`, `:browse`)

Title filtering and text search use the same compact input row, marked
`[FILTER]` or `[SEARCH]`. While filtering, left/right edit the query, up/down
move through results, `Ctrl+F` switches to text search, `Enter` finishes
editing the filter, and `Esc` clears it.

| Key                                                | Action                                                                                                                                                               |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `j` / `k`, arrows, `gg` / `G`, `Ctrl+D` / `Ctrl+U` | Move                                                                                                                                                                 |
| `o`, `l`, `Enter`                                  | Open the collection or note (asks for the password of a locked note or encrypted collection)                                                                         |
| `h`, `-`, `Backspace`                              | Back to the collections list                                                                                                                                         |
| `/`                                                | Filter the list (fuzzy); `Esc` clears it                                                                                                                             |
| `Ctrl+F`, `Ctrl+/`                                 | Search note text in the open collection (or the hovered one): type to search, `↑` `↓` / `Ctrl+N` `Ctrl+P` move, `Enter` opens the note at the match, `Esc` goes back |
| `Space` / `Ctrl+A`                                 | Mark the note and move down / mark all                                                                                                                               |
| `y` / `x`                                          | Yank / cut the marked (or hovered) notes                                                                                                                             |
| `p`                                                | Paste into the open or hovered collection: copy adds the notes to it, cut moves them                                                                                 |
| `d`                                                | Leave: take the notes out of the open collection (the notes stay)                                                                                                    |
| `u`                                                | Undo the last paste or remove                                                                                                                                        |
| `D`                                                | Delete the notes, or the hovered collection (its notes stay); `y` confirms, and a protected note asks for its password instead                                       |
| `n` / `r`                                          | New note (in the open collection) or collection / rename the hovered one (a note keeps the name; empty follows its first line)                                       |
| `e`                                                | Encrypt the hovered collection (password asked twice), or decrypt an encrypted one                                                                                   |
| `s`                                                | Sort notes by modification time or title                                                                                                                             |
| `w`                                                | Make the collection the working collection (`All notes` clears it)                                                                                                   |
| `H`                                                | History of the hovered note                                                                                                                                          |
| `R`                                                | Reload                                                                                                                                                               |
| `q`, `Esc`, `Ctrl+B`                               | Close                                                                                                                                                                |

## Note history (`:history`, `H` in the browser, `Ctrl+R` in the switcher)

| Key                                                | Action                                                                      |
| -------------------------------------------------- | --------------------------------------------------------------------------- |
| `j` / `k`, arrows, `gg` / `G`, `Ctrl+D` / `Ctrl+U` | Move between the current text and older versions                            |
| `Tab`, `t`                                         | Preview what restoring would change, or the version's full text             |
| `Enter`, `l`                                       | Restore the version (`y` confirms); the text before it is kept as a version |
| `h`, `-`, `Esc`                                    | Back to the notes                                                           |
| `q`, `Ctrl+B`                                      | Close the browser                                                           |

## Image preview

| Key   | Action                |
| ----- | --------------------- |
| `o`   | Open in system viewer |
| `Esc` | Close                 |

## Lookup (`:lookup`)

| Key                     | Action                         |
| ----------------------- | ------------------------------ |
| type, `Enter`           | Run search                     |
| `ArrowUp` / `ArrowDown` | Select result                  |
| `Enter`                 | Open result in browser         |
| `Shift+Enter`           | Insert result as markdown link |
| `Esc`                   | Close                          |

## Ask the agent (`:ask`)

The desktop keeps a permanent input below the scrollable conversation.
Use **Insert latest** or **Copy latest** for the reply and **Stop** to cancel a run without closing the conversation.

| Key                     | Action                              |
| ----------------------- | ----------------------------------- |
| type, `Enter`           | Send the prompt                     |
| `Shift+Enter`           | Add a line break in the prompt      |
| `Esc`                   | Cancel a running request, or close  |
| `Enter`                 | Send desktop prompt; insert terminal answer |
| `ArrowUp` / `ArrowDown` | Scroll the answer                   |
| `/`                     | Continue the conversation           |
| `/clear` (in prompt)     | Clear conversation context          |

## Date picker (`:date`, `:remind`)

Type a date or time (`tomorrow`, `next friday 10 pm`, `in 3 weeks`) in
its input field. The preview uses the configured date/time formats. Invalid
input stays open when confirmed; calendar navigation replaces typed input.

| Key | Action |
| --- | --- |
| `ArrowLeft` / `ArrowRight` | Move the input caret while typing; day when the calendar is focused |
| `ArrowUp` / `ArrowDown` | Week when the calendar is focused |
| `PageUp` / `PageDown`, `Ctrl+ArrowLeft` / `Ctrl+ArrowRight` | Month |
| `Alt+ArrowLeft` / `Alt+ArrowRight` | Hour |
| `Alt+ArrowUp` / `Alt+ArrowDown` | Minute (1-minute steps) |
| `Tab` / `Shift+Tab` | Switch focus between input and calendar |
| `Ctrl+T` | Toggle time for date insertion |
| `Home` / `End`, `Ctrl+A` / `Ctrl+E` | Start / end of input |
| `Backspace` / `Delete`, `Ctrl+W` / `Ctrl+U` | Edit input |
| `Enter` / `Esc` | Confirm / cancel |

## Command bar and text inputs

| Key                                        | TUI                                                          | GUI                                                         |
| ------------------------------------------ | ------------------------------------------------------------ | ----------------------------------------------------------- |
| `ArrowLeft` / `ArrowRight`                 | Move input cursor                                            | Move input cursor                                           |
| `Home` / `End`, `Ctrl+A` / `Ctrl+E`        | Start / end of input                                         | Start / end of input                                        |
| `Ctrl+ArrowLeft` / `Ctrl+ArrowRight`       | Previous / next word; Ctrl+Left fills a highlighted word     | Previous / next word; Ctrl+Left fills a highlighted command |
| `Backspace` / `Delete`                     | Delete before / at cursor                                    | Delete before / at cursor                                   |
| `Ctrl+W`, `Ctrl+Backspace` / `Ctrl+Delete` | Delete word before / after cursor                            | Delete word before / after cursor                           |
| `Ctrl+U` / `Ctrl+K`                        | Delete to start / end                                        | Delete to start / end                                       |
| `Tab` / `Shift+Tab`                        | Select inline word completion             | Cycle suggestions; bar-only mode opens word completion      |
| `ArrowUp` / `ArrowDown`                    | Command history                                              | Navigate suggestions; Up recalls history when none selected |
| `Ctrl+P` / `Ctrl+N`                        | —                                                            | Select suggestions                                          |
| `Alt+ArrowUp` / `Alt+ArrowDown`            | Command history                                              | Command history                                             |
| `Enter`                                    | Fill selected word; otherwise execute literal input | Fill selection; otherwise execute literal input             |
| `Esc`                                      | Close the bar immediately                                    | Hide suggestions first; press again to close                |

The TUI uses only the bottom bar with bracketed inline word completion.
The GUI uses a compact contextual popup and faint completion suffix;
`[editor] command_popup = false` disables the GUI popup.
F1 remains available in both apps.

Command syntax and aliases: [Command Reference](command-reference.md).

### Current note information

`F4` or `:info` opens a read-only metadata dialog in both front ends. Scroll with Up/Down or Page Up/Down; Home/End jump to the beginning/end. Escape, Enter, or F4 closes it. Ctrl+I remains available for italic in standard desktop editing and for Vim behavior; it is not rebound to note info.

### Read mode

`F11` or `:read` (`:preview`) shows the note read-only, with every line rendered as it rests: the cursor line no longer reveals its markdown source, and the terminal hides line numbers and the caret and wraps long lines. `j`/`k` or Up/Down scroll by a line, Space/Page Down and Page Up by a page, `g`/Home and `G`/End jump to the start or end. Escape, `q` or F11 leaves, keeping the view; Ctrl+Q quits. The desktop app also goes fullscreen. Some terminals take F11 for their own fullscreen; use `:read` there.
