#!/usr/bin/env python3
"""Copy Slate's reference docs into the site.

    python3 scripts/sync_reference.py [--slate ../slate] [--ref main]

The reference pages (features, keymaps, commands, configuration, ...) are
maintained next to the code in the slate repository, where tests read some of
them. This copies them into `docs/reference/`, keeping links between the
copied pages. The slate repository is private, so the files those pages point
at (the config template, example scripts) are copied into `examples/` and
linked on the slate-docs repository instead; links to anything else become
plain text. Run it before publishing a version so the site matches that release.
"""
import argparse
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = "https://github.com/dborovcanin/slate-docs"
SITE = "https://dborovcanin.github.io/slate-docs/latest"
# Files from the slate repository that readers may open, and where they live here.
COPIES = {
    "config.example.toml": "examples/config.example.toml",
    "scripts/examples": "examples/scripts",
    "scripts/fake_agent.py": "examples/fake_agent.py",
}
PAGES = [
    "features",
    "keymaps",
    "command-reference",
    "configuration",
    "variables",
    "export",
    "scripting",
    "mcp",
    "agent",
]
FENCE = re.compile(r"(````.*?````|```.*?```)", re.S)
# A link (its text may hold inline code), or an inline code span to leave alone.
LINK = re.compile(r"\[((?:[^\]`\n]|`[^`\n]*`)*)\]\(([^)\s]+)\)|`[^`\n]*`")
# Lines that only point at the private repository.
DROP = re.compile(r"^Planned features: .*\n\n?", re.M)


def resolve(base: str, path: str) -> str:
    """Return `path`, relative to slate's `base` directory, from the repo root."""
    parts = []
    for part in pathlib.PurePosixPath(base, path).parts:
        if part == "..":
            if parts:
                parts.pop()
        elif part != ".":
            parts.append(part)
    return "/".join(parts)


def copied(path: str):
    """Return where a slate file is copied in this repository, if it is."""
    for source, dest in COPIES.items():
        if path == source or path.startswith(source + "/"):
            return dest + path[len(source):]
    return None


def rewrite(text: str, target: str, base: str, local: bool) -> str:
    """Rewrite one markdown link found in a file from slate's `base` directory.

    `local` pages are served by the site, so links between reference pages stay
    relative; copied example files link to the site instead.
    """
    if re.match(r"[a-z]+:", target) or target.startswith("#"):
        return f"[{text}]({target})"
    path, hashed, anchor = target.partition("#")
    full = resolve(base, path)
    name = pathlib.PurePosixPath(full)
    if full == f"docs/{name.name}" and name.stem in PAGES:
        url = f"{name.stem}.md" if local else f"{SITE}/reference/{name.stem}/"
        return f"[{text}]({url}{hashed}{anchor})"
    dest = copied(full)
    if dest is None:
        return text
    kind = "blob" if pathlib.PurePosixPath(dest).suffix else "tree"
    return f"[{text}]({REPO}/{kind}/main/{dest}{hashed}{anchor})"


def convert(text: str, base: str, local: bool) -> str:
    """Rewrite the links in markdown text, leaving code alone."""
    def link(m):
        return m.group(0) if m.group(2) is None else rewrite(m.group(1), m.group(2), base, local)

    pieces = FENCE.split(text)
    for i in range(0, len(pieces), 2):
        pieces[i] = LINK.sub(link, pieces[i])
    return "".join(pieces)


def copy_examples(slate: pathlib.Path):
    for source, dest in COPIES.items():
        src, out = slate / source, ROOT / dest
        if out.is_dir():
            shutil.rmtree(out)
        files = sorted(src.rglob("*")) if src.is_dir() else [src]
        for path in files:
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            rel = path.relative_to(slate).as_posix()
            target = ROOT / copied(rel)
            target.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix == ".md":
                base = str(pathlib.PurePosixPath(rel).parent)
                target.write_text(convert(path.read_text(), base, local=False))
            else:
                shutil.copy2(path, target)
            print(target.relative_to(ROOT))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--slate", type=pathlib.Path, default=ROOT.parent / "slate")
    args = parser.parse_args()
    out = ROOT / "docs/reference"
    out.mkdir(parents=True, exist_ok=True)
    for page in PAGES:
        text = DROP.sub("", (args.slate / "docs" / f"{page}.md").read_text())
        (out / f"{page}.md").write_text(convert(text, "docs", local=True))
        print(f"docs/reference/{page}.md")
    copy_examples(args.slate)


if __name__ == "__main__":
    main()
