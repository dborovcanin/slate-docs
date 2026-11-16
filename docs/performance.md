# Performance

Slate is built to open instantly and stay quick no matter how big your notes
or your notebook get. Every recording in this guide runs on a demo notebook
that is far larger than most people's:

- **25,000 notes** in a **4 GB** database,
- the largest single note **6.3 MB**, almost **800,000 words** (70,000 lines),
- **130,000 links** between notes.

With all of that, Slate opens on the last note, finds any note by title as
you type, searches the text of every note, opens the 6 MB note and scrolls
it, searches inside it, and draws the graph of all 25,000 notes. See the
[tour](index.md), [search](search.md) and [graph](links-and-graph.md)
recordings.

## How it stays fast

- **Nothing heavy blocks your typing.** Saving, searching, exchange-rate
  updates, backups, reading linked notes and laying out the graph all run in
  the background. A small spinner in the status bar shows work that lasts
  longer than a second.
- **Only what you see is worked on.** In large notes, calculations are
  computed for the visible part first and the rest fills in off to the side.
  Styling is computed once per change, not on every frame.
- **Small changes stay small.** An edit updates only the lines it touches;
  history stores only changed lines; the link index rereads only notes that
  changed since last time.
- **Lists load in pages.** The switcher, browser and pickers fetch 100
  notes at a time as you scroll, so they open at once with any number of
  notes, while title filters still search everything in the background.
- **Search uses an index.** Text search goes through SQLite's full-text
  index instead of reading every note.
- **The graph scales.** Big graphs are split into communities and laid out
  on a background thread; when tens of thousands of notes are on screen, the
  desktop draws the most connected ones and adds detail as you zoom in.
- **Native, not a web page.** The desktop app draws with the GPU
  (no browser engine inside), and the terminal app is a single small
  binary, so both use little memory.

## If something feels slow

`:perf on` starts recording timings, `:perf dump` writes the slowest
operations to a log, and `:perf where` shows where the log is. Attach that
log to a bug report and it tells exactly what was slow.

For the measurements and the benchmarks behind these claims, see the
[performance reference](https://github.com/dborovcanin/slate/blob/main/docs/performance.md).
