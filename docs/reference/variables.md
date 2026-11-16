# Variables Specification

This document defines variable and table-formula behavior in Slate.

## Syntax

- assignment form: `name := expression`
- no-space form also works: `name:=expression`
- table formula form: cell-local `:=expression`
- table cell reference in table formulas: `(row,col)` (1-based)

Variable names:

- case-insensitive
- may include ASCII letters, digits, underscore, and spaces
- internal spaces are normalized (multiple spaces collapse)

## Scope and precedence

- scope is note-local
- definitions are global inside the note
- if assigned multiple times, the last assignment wins
- vim `gd` on a reference jumps to that last assignment; on `[[id]].name` it opens that note at the assignment of `name`

## Module gating

Calc runtime is gated by per-note modules:

- `math`: master calc gate
- `variables`: variable definition/reference/autocomplete gate
- `table`: table formula parsing/eval gate
- `cross_note`: loading/resolution of values referenced through `[[ID]].name`

Matrix summary:

- `math=off`: no calc evaluation
- `math=on`, `variables=off`, `table=off`: plain/list arithmetic only
- `math=on`, `variables=on`, `table=off`: variable features enabled, table formulas ignored
- `math=on`, `variables=off`, `table=on`: table formulas work, variable refs remain unresolved
- `math=on`, `variables=on`, `table=on`: full behavior

## Evaluation behavior

- assignment lines do not show calc ghost output
- non-assignment lines are evaluated in context:
  - plain line: full line
  - list/checklist line: list body expression
  - table line: each `:=...` formula cell left to right

Table rule:

- `:=expr` inside a cell is always a formula marker
- it is never treated as a variable definition

## Table references and errors

Table references are table-local and use data rows only.

Inline table errors:

- `!ERROR#out_of_bounds`
- `!ERROR#non_numeric`
- `!ERROR#self_reference`
- `!ERROR#cycle`

## Conversion assignments

Conversion assignments are normalized to numeric values when stored.

Example:

```text
len := 3 m to km
len + 2
```

`len` is stored as numeric `0.003` and reused numerically.

## Error handling

- unresolved variable refs produce no ghost output
- cyclic dependencies produce no ghost output
- diagnostics exist for tests/debugging paths

## Cross-note variables

Values exported by one note can be referenced in another using its note ID, as in wiki-links:

```
[[ID]].var_name
```

`ID` is the note's full ID: its ULID, or `daily-YYYY-MM-DD` for a daily note. IDs are case-sensitive; the autocomplete inserts them. Variable name rules are identical to note-local variables (case-insensitive, spaces normalized).

Example:

```
# Budget note  (ID: 01KP0YD099X9TQENYJQ1SE9X8V)
monthly_income := 5000

# Goals note
[[01KP0YD099X9TQENYJQ1SE9X8V]].monthly_income * 12
```

### Evaluation

- Referenced stored notes can be loaded and evaluated on demand; opening the
  source first is not required. Large-note preparation can do this in a worker.
- Missing sources, missing definitions or disabled modules leave references
  unresolved, without a ghost result.
- A referenced note is evaluated for its exports only (assigned variables),
  never its lines or table cells, after every note it reads, however deep.
  Notes that read each other are evaluated again until their exports settle;
  variables that truly depend on each other across notes stay unresolved.
- The in-memory index tracks source revisions, dependencies and in-flight
  loads; changed exports invalidate dependent values for subsequent evaluation.
- With background tasks on, a note opens without waiting for the notes it
  reads: a worker loads them and its values appear when they finish. Edits
  meanwhile wait at most briefly for those notes instead of loading them.
  Without background tasks, references load before evaluation as before.

### Scoping rules

- only variables assigned with `:=` are exported; expression results are not
- conversion assignments export their resolved numeric value
- the consuming note needs `math`, `variables` and `cross_note`; the source must export the variable under its own module configuration

### Autocomplete

Typing `[[ID]].` (with or without a partial name) triggers cross-note variable suggestions drawn from the shared index. Names can be scanned from the stored source on first use without evaluating values or opening that note first.

The cross-note completion source is always active regardless of the local `variables_autocomplete_min_chars` threshold — it activates the moment the `[[ID]].` pattern is detected.

## Autocomplete

- source: backend/shared evaluation variable index
- default trigger threshold: 3 characters (`variable_autocomplete_min_chars`)

Popup interactions:

- `Up/Down`: move selection
- `Tab` or `Enter`: accept selection
- `Esc`: close popup

`Tab` fallback when popup is closed:

- accept active variable completion if available
- otherwise apply calc ghost result
