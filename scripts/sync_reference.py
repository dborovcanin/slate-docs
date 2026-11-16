#!/usr/bin/env python3
"""Copy Slate's reference docs into the site.

    python3 scripts/sync_reference.py [--slate ../slate] [--ref main]

The reference pages (features, keymaps, commands, configuration, ...) are
maintained next to the code in the slate repository, where tests read some of
them. This copies them into `docs/reference/`, keeping links between the
copied pages and pointing every other relative link (architecture notes,
example scripts, the config template) at the slate repository on GitHub at
`--ref`. Run it before publishing a version so the site matches that release.
"""
import argparse
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = "https://github.com/dborovcanin/slate"
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
CODE = re.compile(r"(````.*?````|```.*?```|`[^`\n]*`)", re.S)
LINK = re.compile(r"\]\(([^)\s]+)\)")


def rewrite(target: str, ref: str) -> str:
    if re.match(r"[a-z]+:", target) or target.startswith("#"):
        return target
    path, hashed, anchor = target.partition("#")
    name = pathlib.PurePosixPath(path)
    if len(name.parts) <= 2 and name.parts[0] in (".", name.name) and name.stem in PAGES:
        return f"{name.stem}.md{hashed}{anchor}"
    # Anything else lives in the slate repository, relative to docs/.
    resolved = pathlib.PurePosixPath("docs", path)
    parts = []
    for part in resolved.parts:
        if part == "..":
            parts.pop()
        elif part != ".":
            parts.append(part)
    kind = "tree" if not pathlib.PurePosixPath(*parts).suffix else "blob"
    return f"{REPO}/{kind}/{ref}/{'/'.join(parts)}{hashed}{anchor}"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--slate", type=pathlib.Path, default=ROOT.parent / "slate")
    parser.add_argument("--ref", default="main", help="slate git ref for outside links")
    args = parser.parse_args()
    out = ROOT / "docs/reference"
    out.mkdir(parents=True, exist_ok=True)
    for page in PAGES:
        text = (args.slate / "docs" / f"{page}.md").read_text()
        pieces = CODE.split(text)
        for i in range(0, len(pieces), 2):
            pieces[i] = LINK.sub(lambda m: f"]({rewrite(m.group(1), args.ref)})", pieces[i])
        (out / f"{page}.md").write_text("".join(pieces))
        print(f"docs/reference/{page}.md")


if __name__ == "__main__":
    main()
