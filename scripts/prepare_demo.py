#!/usr/bin/env python3
"""Add a small, readable graph to an isolated recording dataset via Slate MCP."""
import argparse
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

# Titles, topic tags and links are kept small enough to read in a screenshot.
NOTES = {
    "home": ("A little space to think", "home", "A notebook for ideas that become useful things.", ["writing", "research", "numbers", "design", "projects"]),
    "writing": ("Writing room", "writing", "Keep the first draft close to the idea.", ["home", "drafts", "journal", "markdown", "voice"]),
    "drafts": ("First drafts", "writing", "Start rough. Find the shape while you write.", ["voice", "markdown", "ideas"]),
    "journal": ("Daily pages", "writing", "A few lines each morning, and a little room to reflect.", ["writing", "questions", "weekend"]),
    "markdown": ("Plain Markdown", "writing", "Headings, lists, links and images, saved as text.", ["drafts", "reading", "keyboard"]),
    "voice": ("Finding a voice", "writing", "Simple words. Clear sentences. Something worth saying.", ["drafts", "reading"]),
    "research": ("Research desk", "research", "Collect sources, ask better questions, and connect the answers.", ["home", "reading", "sources", "questions", "connections"]),
    "reading": ("Reading list", "research", "A place for books, articles and the notes they leave behind.", ["sources", "voice", "ideas"]),
    "sources": ("Good sources", "research", "Keep the original alongside the thought it inspired.", ["reading", "questions"]),
    "questions": ("Open questions", "research", "The useful questions are rarely answered in one sitting.", ["sources", "journal", "experiments"]),
    "connections": ("Unexpected connections", "research", "Follow a link. See where the next idea leads.", ["reading", "colors", "formulas"]),
    "numbers": ("Working with numbers", "numbers", "Let the notebook do the arithmetic while you think.", ["home", "budget", "formulas", "units", "expenses"]),
    "budget": ("Lisbon budget", "numbers", "nights := 3\nhotel := nights * 74\nflights := 379.80\nfood := nights * 70\ntotal := hotel + flights + food", ["expenses", "weekend", "formulas"]),
    "formulas": ("Useful formulas", "numbers", "200 * 1.19\n15% of 240\n50 kg to lbs", ["budget", "units", "experiments"]),
    "units": ("Units and measures", "numbers", "5 km in miles\n3 cups to ml\n90 min in hours", ["formulas", "expenses"]),
    "expenses": ("Small expenses", "numbers", "| Item | Cost |\n| --- | ---: |\n| Tram | 6.60 |\n| Museum | 12 |\n| Lunch | 18.50 |", ["budget", "weekend"]),
    "design": ("Design notebook", "design", "Make the important things easy to see and easy to reach.", ["home", "flows", "colors", "keyboard", "sketches"]),
    "flows": ("Service sketch", "design", "A small system: a client, an API, a cache and a database.", ["sketches", "experiments", "launch"]),
    "colors": ("A quieter palette", "design", "Sage, warm paper and a little contrast where it matters.", ["design", "sketches", "voice"]),
    "keyboard": ("Keyboard first", "design", "A few familiar keys, and your hands stay with the thought.", ["markdown", "flows"]),
    "sketches": ("Quick sketches", "design", "Draw the relationship before writing the implementation.", ["flows", "colors"]),
    "projects": ("Projects in motion", "projects", "Turn a collection of notes into a little forward motion.", ["home", "launch", "ideas", "weekend", "experiments"]),
    "launch": ("Launch checklist", "projects", "- [x] Make a small prototype\n- [ ] Check the details\n- [ ] Share what works", ["flows", "drafts", "experiments"]),
    "ideas": ("Ideas to come back to", "projects", "Leave a trail for your future self.", ["drafts", "connections", "launch"]),
    "weekend": ("Weekend in Lisbon", "projects", "Walk by the river. Take the tram. Leave room for a detour.", ["budget", "journal", "reading"]),
    "experiments": ("Small experiments", "projects", "Change one thing, observe, and keep a note of what happened.", ["questions", "formulas", "launch"]),
}
title, topic, body, _ = NOTES["home"]
body += "\n\n## Today\n\n- [x] Capture an idea\n- [ ] Follow a useful connection\n- [ ] Make a little progress\n\n## A quick calculation\n\ncoffee := 3.50\nnotebooks := 2 * 12\ncoffee + notebooks\n\n> Keep a little room for the next thought."
NOTES["home"] = (title, topic, body, [key for key in NOTES if key != "home"])


def prepare(data, slate):
    data = data.expanduser().resolve()
    if not (data / "slate/notes.db").is_file():
        raise SystemExit(f"no notes database at {data / 'slate/notes.db'}")
    cache = ROOT / ".cache/capture"
    config = cache / "mcp-config/slate"
    config.mkdir(parents=True, exist_ok=True)
    (config / "config.toml").write_text("[mcp]\nenabled = true\n")
    env = {**os.environ, "XDG_DATA_HOME": str(data.resolve()), "XDG_CONFIG_HOME": str(config.parent)}
    app = subprocess.Popen([str(slate.resolve()), "mcp"], env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    serial = 0

    def call(name, arguments):
        nonlocal serial
        serial += 1
        request = {"jsonrpc": "2.0", "id": serial, "method": "tools/call", "params": {"name": name, "arguments": arguments}}
        app.stdin.write(json.dumps(request) + "\n")
        app.stdin.flush()
        response = json.loads(app.stdout.readline())
        result = response.get("result", {})
        if response.get("error") or result.get("isError"):
            raise RuntimeError(response)
        return json.loads(result["content"][0]["text"])

    try:
        topics = {value[1] for value in NOTES.values()}
        for name in ["Slate demo", *[topic.title() for topic in sorted(topics)]]:
            try:
                call("create_collection", {"name": name})
            except RuntimeError as error:
                if "already exists" not in str(error).lower():
                    raise
        out = cache / "demo-notes.json"
        source = cache / "demo-data.txt"
        same_data = source.exists() and source.read_text() == str(data.resolve())
        notes = json.loads(out.read_text()) if same_data and out.exists() else {}
        for key, (title, topic, body, links) in NOTES.items():
            if key in notes:
                try:
                    notes[key] = call("read_note", {"id": notes[key]["id"]})
                except RuntimeError as error:
                    if not any(term in str(error).lower() for term in ("not found", "no such note")):
                        raise
                    del notes[key]
            if key not in notes:
                notes[key] = call("create_note", {"text": f"# {title}\n\n{body}", "collection": "Slate demo"})
            call("add_to_collection", {"id": notes[key]["id"], "collection": topic.title()})
        for key, (title, topic, body, links) in NOTES.items():
            text = f"# {title}\n\n{body}\n\n## Connections\n\n" + " · ".join(f"[[{notes[link]['id']}]]" for link in links)
            call("update_note", {"id": notes[key]["id"], "revision": notes[key]["revision"], "text": text})
        out.write_text(json.dumps(notes, indent=2))
        source.write_text(str(data.resolve()))
        print(f"Prepared {len(notes)} connected notes: {out}", flush=True)
    finally:
        app.stdin.close()
        app.wait(timeout=15)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--slate", type=Path, default=ROOT.parent / "slate/target/release/slate")
    args = parser.parse_args()
    prepare(args.data, args.slate)
