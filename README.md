# Slate docs

The user guide and reference for [Slate](https://github.com/dborovcanin/slate),
published at **https://dborovcanin.github.io/slate-docs/**.

Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
(search, light and dark themes) and versioned with
[mike](https://github.com/jimporter/mike).

## Layout

| Path | What |
| --- | --- |
| `docs/*.md` | The guide, one page per topic |
| `docs/reference/` | Reference pages, copied from the slate repo (do not edit here) |
| `docs/media/` | Recordings and screenshots |
| `mkdocs.yml` | Site config and navigation |
| `VERSION` | The docs version that pushes to `main` publish |
| `scripts/capture.py`, `scripts/scenarios.py` | Re-record the GIFs from the real apps |
| `scripts/sync_reference.py` | Copy the reference pages from a slate checkout |

## Preview

```sh
make serve        # live preview at http://127.0.0.1:8000
make build        # strict build; fails on broken links or anchors
```

## Publish

Every push to `main` runs `.github/workflows/publish.yml`: it checks the site
builds, publishes the version in `VERSION` to the `gh-pages` branch under
its own folder, points the `latest` alias at it, and makes it the default
the site root redirects to. Older versions stay published and appear in the
version selector.

To start a new version, bump `VERSION` (for example to `v1.1.0`) and push.
To fix an old version, check out the commit it was published from, edit,
and run `make publish` with that `VERSION`.

Without CI, `make publish` does the same from your machine.

### One-time GitHub setup

1. Push `main` once, so the workflow creates the `gh-pages` branch.
2. In the repository's **Settings › Pages**, set **Source** to *Deploy from
   a branch*, branch `gh-pages`, folder `/ (root)`.
3. In **Settings › Actions › General › Workflow permissions**, allow *Read
   and write permissions* (the workflow pushes to `gh-pages`).

## Reference pages

The reference (features, keymaps, commands, configuration, …) is written
next to the code in the slate repo, where tests read parts of it. Before
publishing a version, refresh the copies:

```sh
make reference                                  # from ../slate at main
python3 scripts/sync_reference.py --ref v1.0.0  # links into slate at a tag
```

## Recordings

The GIFs are recorded from release builds of both apps on a virtual display,
over a large demo notebook:

```sh
make capture DATA=~/tst                          # every scenario
python3 scripts/capture.py --data ~/tst graph    # just one
```

Needs Xvfb, xdotool, xclip, ffmpeg, Alacritty, Mesa's lavapipe Vulkan driver,
`pdftoppm` and Pillow. Scenarios create and edit notes in the data
directory, so point `--data` at a test dataset, never at your own notes. The
`ask` scenario makes a real Claude Code request.
