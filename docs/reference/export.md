# Export Reference

Slate supports clipboard and file export from the command bar.
It also supports full database backup and restore commands for moving all notes together.

## Export formats

- markdown (`.md`)
- plain text (`.txt`)
- PDF (`.pdf`)

## Command syntax

- `export pdf <path>`
- `export markdown [path]`
- `export text [path]`
- `backup export <path.zip>`
- `backup export md <directory>`
- `backup load <backup.zip|notes.zip|notes-directory>`
- `backup <path.zip>` (legacy alias for `backup export`)
- `backup notes <path.zip>` (legacy alias for `backup export`)

Suggestions display only `markdown`, `pdf` and `text`. The aliases `md` and
`txt` remain accepted and match their full-name suggestions when typed.

If path is omitted:

- Markdown and text copy to the clipboard.
- The desktop app opens a path prompt for PDF; the terminal requires a path
  and reports usage when it is missing.

Markdown and text currently write the stored Markdown text, with generated TOC
fences removed by the shared export preparation. Text export does not strip
all Markdown formatting. PDF typesets that content.

Path behavior:

- `~` / `~/...` is expanded to `$HOME` in command-path exports
- relative paths are resolved from the current process working directory
- parent directory must already exist and be writable

## Export entry points

- command bar export via `export ...`
- clipboard fallback for `export markdown` / `export text` with no path

## PDF rendering details

PDF export is markdown-aware and currently includes:

- headings and paragraph flow
- ordered/unordered lists
- checklist rendering
- fenced/inline code styling
- generated `toc` sections as formatted heading lists, preserving nested indentation
- markdown tables
- markdown images (`![alt](src)`)
- `diagram` fences drawn as vector graphics with real text

Diagrams are drawn from the same shapes as SVG export, at one point per
diagram unit, shrunk to fit the page, with a subtle gray frame. They stay
sharp at any zoom and their labels are selectable text; opacity, dashes and
clipping carry over. Invalid, unfinished, or oversized diagrams retain their
source with a “Diagram unavailable” notice. Image budgets (decoded pixels and
encoded bytes) apply to note images. Markdown exports keep the editable
`diagram` fences unchanged.

Closed `toc` fences are omitted from all export formats, leaving their stored Markdown contents. Ordinary code fences, including examples containing a `toc` fence, retain code styling. Export uses the existing TOC text; run `:toc refresh` before exporting to update it.

PDF links are clickable: TOC and same-note heading links jump to their heading, and Markdown URL, email, and file links open their destinations. Relative file links are written as absolute `file:` links, resolved against the note's folder (the app data folder for notes stored in the database), so they keep working wherever the PDF is saved. Bare web URLs and email addresses are linked too. Wrapped labels keep a clickable area on each line, including links in tables and quotes. Links to missing headings stay inactive; refresh a stale TOC before export. Cross-note wiki links are not exported as navigation links.

Color behavior follows export palette rules used by host runtime.

### Fonts

Standard PDF fonts declare WinAnsi encoding. On supported installations, the
Unicode fallback embeds regular and available sibling bold/italic faces and
uses their glyph widths for layout. Only used faces are embedded. Set
`SLATE_PDF_UNICODE_FONT` to a TrueType font file to override the regular face;
styled siblings are discovered by family/style filename. A missing styled
face uses the regular face; characters absent from installed fonts may still
fall back. Font availability therefore affects coverage and styling.

## Image sources

Image resolution supports:

- db-backed image placeholders resolved through note source service
- file-backed markdown image paths
- data-url image payloads

## Error behavior

Typical export error classes:

- invalid/missing path for file export
- filesystem write failures
- unsupported/bad image payload during PDF decode
- clipboard write failure for clipboard exports

Host command status messages are returned to the status bar/toast layer.

## Database Backup

`backup export <path.zip>` writes a portable zip containing:

- `notes.db`: a consistent SQLite snapshot of the full Slate notes database
- `manifest.json`: backup metadata
- `README.txt`: manual restore notes

The zip uses stored (uncompressed) entries so the file can be opened by any standard zip tool.

## Database Restore

`backup load <path>` automatically recognizes a Slate database backup, a ZIP
of Markdown notes (stored or Deflate-compressed), or a Markdown directory.
Native backups follow the replacement workflow below. Markdown is added as
described in [Markdown directory backups](#markdown-directory-backups):
existing notes identified by `slate-id` retain their edits; files without an
id become new notes. Other compressed archive formats are not supported.

A typed directory must look like a note folder: it holds the `.slate-export`
marker written by `backup export md`, a `.obsidian` folder, or a Markdown file
at its top level. So a slip such as `backup load ~` is refused rather than
importing every Markdown file below it. A ZIP needs a Markdown file anywhere.
A ZIP's single enclosing folder is removed only when it holds the marker or
`.obsidian`; any other single folder may be the content, so it is kept and
becomes a collection for notes without `collections` front matter.

Markdown ZIPs are unpacked to a private folder beside the database (not a
RAM-backed `/tmp`), which is removed after import or failure. Unsafe paths,
symlinks and duplicate paths (`a.md` and `./a.md`) are rejected before
importing any notes; names differing only by case are distinct files, unless
the file system cannot hold both. Extraction is limited to 100,000 entries,
512 MiB per file and 4 GiB total. A ZIP containing root-level `notes.db` is
always treated as a native backup; a damaged backup does not fall back to
importing unrelated Markdown files.

For a Slate backup, `backup load <path.zip>` validates and restores while the
app remains open:

1. Extract and stage `notes.db` at `<data_dir>/notes.db.staged-restore`.
2. Validate SQLite integrity, the schema version, and required tables/columns.
   Backups at the current schema (1) are restored, older released ones are
   upgraded first, and pre-release (2 to 6) or newer ones are refused.
3. Drain in-flight database work and save pending edits before the swap.
4. Replace/reopen the database, retain the previous file as
   `notes.db.before-restore`, and reload note/catalogue state. A failed reopen
   restores the prior database.

A staged restore left by an interrupted session can also be applied during
startup. Normal successful restore does not require quitting/restarting.

Manual restore remains possible: close all Slate clients, unzip a compatible
backup and replace the active database. Keep a copy of the original database.

## Markdown directory backups

`backup export md <directory>` writes every readable note to a new or empty
directory, in the background with its count in the status bar. It refuses a
directory holding anything but `.obsidian`, so it cannot overwrite earlier
notes. Directories read like other paths: quotes, a leading `~` and `file://`
all work. The result also opens as an Obsidian vault.

- One folder per collection; empty collections get an empty folder. A note in
  several collections is written once, to the first collection by
  case-insensitive name, then exact name and id. Notes without a collection
  stay at the root. Sanitized folder names receive numeric suffixes on
  collision.
- Each note becomes `<title>.md`. Characters unsafe in a file name become
  spaces, and repeated titles get a number.
- `[[id]]` links become `[[folder/title]]`, keeping any `#heading` and `|text`.
  Links in code stay as written, and links to missing notes stay as ids.
- Front matter holds `slate-id`, `aliases` when the name differs from the
  title, `tags`, and every collection in `collections`. Tag spaces become `-`,
  and `slate-tags` keeps the exact names.
- Stored images go to `attachments/`, linked relatively from collection
  folders. Encrypted notes are skipped and counted.
- An empty `.slate-export` file marks the directory for `backup load`.

This is a Markdown export, not a full database snapshot. `backup load` adds
such a directory, or a ZIP of it, back. It reads `.md` files and skips hidden
folders such as `.obsidian` and `.trash`:

- A note whose `slate-id` already exists here is left as it is, so loading
  twice adds nothing and never overwrites an edit.
- The file name becomes a `# heading` when a file does not open with one.
- `[[name]]`, `[[folder/name]]`, aliases and relative `[text](file.md)` links
  become note links. Links nothing matches stay as text and are counted.
- `![[image.png]]` and relative `![alt](image.png)` import the image. Embedding a
  note, `![[note]]`, becomes a plain link.
- Front matter tags and inline `#tags` become tags; `collections`, or else the
  note's folder, becomes a collection (`Projects - Deep` for `Projects/Deep`).
  Other front matter stays visible in a `yaml` block under the title.

File dates are not kept: imported notes count as written at import.

`backup export <path.zip>` continues to produce the full database backup
described above, with the same archive layout and overwrite behavior.

### Diagram captions

Add plain text after the opening fence language, for example
````diagram System overview`. It appears as a centered caption below the
inline diagram and in PDF exports, including source fallback. Captions wrap
within the preview width and add no source line or separate line number.
Markdown keeps the opening fence; standalone SVG and PNG images omit captions.

PDF export runs in the background in both frontends. In the terminal, editing
can continue while the captured note is exported; the status reports completion
or failure. Only one PDF export or backup job runs at a time. PNG
diagram exports (desktop only) load system fallback fonts only when labels need
glyphs absent from the regular export font.

PNG export is the `slate-export` crate's `raster` feature, which only the
desktop app enables; the terminal app carries no rasteriser. Its tests run with
`cargo test -p slate-export --features raster`.
