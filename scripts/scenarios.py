"""The user guide's recordings, one function per GIF (see capture.py).

Each scenario drives a real app with the keyboard (the mouse only where a
gesture needs it) over the demo dataset, and records one GIF or still.
"""
import json
from pathlib import Path

GUI = {
    "vim": False,
    "theme": "everforest_dark",
    "sidebar": False,
    "inspector": False,
    "open_tabs": [],
    "wrap": True,
    "proportional_prose": True,
    "font_size": 20.0,
    "ui_scale": 1.0,
}
VIM_GUI = {**GUI, "vim": True}


# -- helpers --------------------------------------------------------------


def open_note(s, query, settle=1.5):
    """Open a note through the Ctrl+P switcher."""
    s.key("ctrl+p", pause=0.8)
    s.type(query, delay=45, pause=1.4)
    # Pick the best match explicitly, then open it.
    s.key("Down", pause=0.3)
    s.key("Return", pause=settle)


def command(s, text, pause=1.0):
    """Run a command from the command bar (Ctrl+E)."""
    s.key("ctrl+e", pause=0.6)
    s.type(text, delay=55, pause=0.5)
    s.key("Return", pause=pause)


def new_note(s, title):
    s.key("ctrl+n", pause=1.0)
    s.type(title + "\n\n", delay=45, pause=0.4)
    s.key("ctrl+s", pause=0.8)


# -- desktop app ----------------------------------------------------------


def tour(s):
    """25,000 notes: find one by title, open a 6 MB note, search inside it."""
    s.gui(GUI)
    s.record("tour")
    s.wait(1)
    open_note(s, "photometry 11681", settle=3.0)
    for _ in range(6):
        s.key("Page_Down", pause=0.3)
    s.key("ctrl+f", pause=0.6)
    s.type("redshift", delay=80, pause=1.5)
    for _ in range(4):
        s.key("Tab", pause=0.6)
    s.key("Return", pause=0.8)
    s.key("Escape", pause=1.0)
    s.stop("tour")


def writing(s):
    """Markdown styled in place: headings, emphasis, lists, checklists."""
    s.gui(GUI)
    s.record("writing")
    s.wait(0.8)
    s.key("ctrl+n", pause=1.0)
    s.type("Weekend in Lisbon\n\n", delay=50)
    s.type("Flying out on **Friday** with *Ana* and Marko. Tram 28 at `08:15`.\n\n", delay=40)
    s.type("## Packing\n\n", delay=50)
    s.type("- [ ] Passport\nCharger\nSunscreen", delay=50, pause=0.6)
    # A trailing " /x" ticks an item.
    s.key("Up", "Up", pause=0.3)
    s.key("End", pause=0.3)
    s.type(" /x", delay=150, pause=1.0)
    s.key("Down", "Down", pause=0.2)
    s.key("End", pause=0.2)
    s.type("\n\n## Ideas\n\n", delay=50)
    s.type("1. Pastéis in Belém\nSunset at the Miradouro\n\n", delay=45)
    s.type("> Bring cash for the tram.", delay=45, pause=2.0)
    s.stop("writing")


def calc(s):
    """Every line is a calculator: arithmetic, percentages, units, times."""
    s.gui(GUI)
    s.record("calc")
    s.wait(0.8)
    new_note(s, "Quick sums")
    for line in (
        "200 * 1.19",
        "15% of 240",
        "sqrt(144) + 3^2",
        "50 kg to lbs",
        "5 km in miles",
        "3 cups to ml",
        "09:10-17:30 - 45min",
        "9am-5pm + 13:00-14:30",
    ):
        s.type(line + "\n", delay=55, pause=0.5)
    s.type("1250 * 12", delay=60, pause=1.0)
    # Tab replaces the expression with its result.
    s.key("Tab", pause=1.8)
    s.stop("calc")


def currency(s):
    """Currency conversion with cached exchange rates."""
    s.gui(GUI)
    s.record("currency")
    s.wait(0.8)
    new_note(s, "Exchange")
    for line in (
        "100 USD to EUR",
        "$10 + 5 EUR",
        "2000 RSD to EUR",
        "45 GBP in JPY",
        "1200 CHF / 12 to USD",
    ):
        s.type(line + "\n", delay=55, pause=0.6)
    s.wait(1.5)
    s.stop("currency")


def variables(s):
    """Variables: change one value and everything that depends on it updates."""
    s.gui(GUI)
    s.record("variables")
    s.wait(0.8)
    new_note(s, "Lisbon budget")
    for line in (
        "nights := 3",
        "hotel := nights * 74",
        "flights := 2 * 189.90",
        "food := nights * 2 * 35",
        "total := hotel + flights + food",
        "total",
        "total / 2",
        "in dollars := total EUR to USD",
    ):
        s.type(line + "\n", delay=45, pause=0.4)
    s.wait(1.0)
    # Back to the first line: three nights become five.
    for _ in range(8):
        s.key("Up", pause=0.12)
    s.key("End", pause=0.3)
    s.key("BackSpace", pause=0.4)
    s.type("5", pause=2.0)
    s.stop("variables")


def cross_note(s):
    """Use another note's variable and follow the link to it."""
    s.gui(GUI)
    s.record("cross-note")
    s.wait(0.8)
    new_note(s, "Year plan")
    s.type("trips := ", delay=60)
    s.type("[[", delay=150, pause=0.8)
    s.type("lisbon budget", delay=70, pause=1.2)
    s.key("Tab", pause=0.8)
    # No heading: leave the link and ask for one of its variables.
    s.key("Escape", pause=0.4)
    s.key("End", pause=0.4)
    s.type(".", pause=1.0)
    s.type("tot", delay=120, pause=0.8)
    s.key("Tab", pause=0.5)
    s.type(" * 3\n", delay=80, pause=0.6)
    s.type("monthly := trips / 12\n", delay=60, pause=0.4)
    s.key("Escape", pause=1.5)
    # Follow the link to the budget note and come back.
    s.key("Up", "Up", pause=0.3)
    s.key("Home", pause=0.2)
    for _ in range(11):
        s.key("Right", pause=0.05)
    s.key("ctrl+bracketright", pause=2.2)
    s.key("alt+Left", pause=2.0)
    s.stop("cross-note")


def links(s):
    """Insert a wiki link from completion, follow it, and return."""
    s.gui(GUI)
    new_note(s, "Reading trails")
    s.record("links")
    s.type("Start with ", delay=70)
    s.type("[[", delay=160, pause=0.8)
    s.type("research desk", delay=90, pause=1.2)
    s.key("Tab", pause=0.7)
    s.key("Escape", pause=0.5)
    s.key("End", pause=0.4)
    s.type(" and follow the connections.\n\n", delay=45, pause=0.8)
    s.key("ctrl+s", pause=1)
    s.still("links")
    s.key("Up", "Up", "Home", pause=0.2)
    for _ in range(14):
        s.key("Right", pause=0.04)
    s.key("ctrl+bracketright", pause=2)
    s.key("alt+Left", pause=1.5)
    s.stop("links", still=False)


def images(s):
    """Paste a local screenshot into a note as an inline image."""
    s.gui(GUI)
    new_note(s, "Visual notes")
    s.type("Keep the picture beside the idea.\n\n", delay=50)
    s.record("images")
    s.paste_image(s.media("diagram-detail.png"), pause=2)
    s.key("ctrl+s", pause=1)
    s.key("ctrl+Home", "Down", pause=0.6)
    s.wait(2)
    s.stop("images")


def desktop(s):
    """A real desktop overview with the new sidebar, tabs, and inspector."""
    demo = json.loads((Path(__file__).resolve().parents[1] / ".cache/capture/demo-notes.json").read_text())
    s.gui({**GUI, "sidebar": True, "inspector": True,
           "open_tabs": [demo[key]["id"] for key in ("home", "writing", "numbers")]},
          ["--id", demo["home"]["id"]])
    s.key("ctrl+Home", "Down", pause=1)
    s.move(90, 950)
    s.still("desktop")


def tables(s):
    """A table with formula cells and a column total."""
    s.gui(GUI)
    s.record("tables")
    s.wait(0.8)
    new_note(s, "Lisbon expenses")
    s.paste(
        "| Item | Qty | Price | Total |\n"
        "| --- | ---: | ---: | ---: |\n"
        "| Tram pass | 2 | 6.60 |  |\n"
        "| Museum | 2 | 12 |  |\n"
        "| Dinner | 3 | 28.50 |  |",
        pause=1.5,
    )
    # The cursor is in the last Total cell: start at the first row.
    s.key("Up", "Up", pause=0.4)
    for row in (1, 2, 3):
        s.type(f":=({row},2)*({row},3)", delay=60, pause=0.6)
        if row < 3:
            s.key("Down", pause=0.5)
    # Tab in the last cell adds a row: a total for the column.
    s.key("Tab", pause=0.4)
    s.key("Tab", pause=0.6)
    s.type("Sum", delay=80)
    s.key("Tab", "Tab", "Tab", pause=0.3)
    s.type(":=sum_col()", delay=80, pause=0.6)
    s.key("Up", pause=2.0)
    s.stop("tables")


def search(s):
    """One query language: tags, collections, titles and full text."""
    s.gui(GUI)
    s.record("search")
    s.wait(0.8)
    s.key("ctrl+p", pause=0.8)
    s.type("#topic/sa", delay=90, pause=1.2)
    s.key("Tab", pause=0.6)
    s.type("contains:mooring", delay=80, pause=2.0)
    s.type(" -#status/draft ", delay=80, pause=2.0)
    s.still("search")
    s.key("Down", "Down", "Down", pause=0.5)
    s.key("Return", pause=2.5)
    s.stop("search", still=False)


def browser(s):
    """The collection browser: collections, notes and a live preview."""
    s.gui(GUI)
    s.record("browser")
    s.wait(0.8)
    s.key("ctrl+shift+b", pause=1.5)
    s.key("Escape", pause=0.5)
    s.key("Tab", pause=0.4)
    # Down to the sailing collection.
    for _ in range(17):
        s.key("Down", pause=0.12)
    s.key("Tab", pause=0.6)
    for _ in range(4):
        s.key("Down", pause=0.4)
    s.key("ctrl+f", pause=0.6)
    s.type("regatta", delay=90, pause=2.0)
    s.key("Down", "Down", pause=0.6)
    s.wait(1.5)
    s.stop("browser")


def graph(s):
    """Readable topic clusters, then keyboard navigation and graph search."""
    demo = json.loads((Path(__file__).resolve().parents[1] / ".cache/capture/demo-notes.json").read_text())
    settings = {**GUI, "graph": {
        "filter": 'collection:"Slate demo"',
        "groups": [{"query": f'collection:"{topic.title()}"', "color": {"Theme": color}}
                   for topic, color in [("writing", 7), ("research", 0), ("numbers", 1), ("design", 2), ("projects", 6)]],
        "node_size": 1.15, "link_width": 0.8, "text_fade": 0.0,
    }}
    s.gui(settings, ["--id", demo["home"]["id"]])
    command(s, "graph", pause=35)
    s.key("0", pause=2)
    s.scroll(800, 500, up=False, clicks=1, pause=0.8)
    s.move(80, 950)
    s.still("graph-overview")
    s.key("Escape", pause=0.8)
    s.record("graph")
    s.wait(0.8)
    command(s, "graph", pause=4.0)
    for key in ("Right", "Down", "Tab", "Tab"):
        s.key(key, pause=0.7)
    s.key("0", pause=1)
    s.scroll(800, 500, up=False, clicks=1, pause=0.8)
    s.still("graph-connections")
    s.key("slash", pause=0.5)
    s.type("writing", delay=100, pause=1.5)
    s.key("Return", pause=1)
    s.still("graph-search")
    s.key("n", pause=1)
    s.key("f", pause=1.2)
    s.still("graph-groups")
    s.stop("graph")


def history(s):
    """Every note keeps its older versions; compare and restore."""
    s.gui(GUI)
    open_note(s, "replication experiment 11864", settle=2.0)
    s.record("history")
    s.wait(0.8)
    command(s, "history", pause=2.0)
    s.key("Down", pause=1.8)
    s.key("Down", pause=1.8)
    s.key("Tab", pause=1.8)
    s.key("Tab", pause=1.5)
    s.still("history")
    s.key("Escape", pause=1.0)
    s.stop("history", still=False)


def diagram(s):
    """Build a colourful garden-day plan, briskly, using the actual canvas."""
    s.gui(GUI)
    new_note(s, "A day in the community garden")
    command(s, "diagram", pause=0.6)
    s.key("F11", pause=0.4)
    s.click(30, 24, pause=0.2)  # Hide the shape palette; keep the style presets.
    s.key("F6", pause=0.1)  # Return keyboard focus from the toolbar to the canvas.
    s.key("minus", "minus", "minus", pause=0.12)  # Fixed 1.024x view while building.

    # name, shape shortcut, label, screen centre, preset colour. The canvas
    # remains fixed until the final Fit so the build is easy to follow.
    nodes = [
        ("day", "o", "Garden day", 650, 130, "green"),
        ("before", "o", "Before the day", 270, 270, "blue"),
        ("welcome", "o", "Welcome, neighbours!", 650, 270, "green"),
        ("weather", "d", "Dry forecast?", 1100, 270, "yellow"),
        ("tools", "r", "Seeds & tools", 100, 430, "blue"),
        ("invite", "r", "Invite neighbours", 270, 430, "blue"),
        ("food", "r", "Plan the picnic", 440, 430, "blue"),
        ("choose", "o", "Pick an activity", 650, 430, "purple"),
        ("outside", "e", "Picnic outdoors", 990, 430, "green"),
        ("inside", "o", "In the greenhouse", 1220, 430, "yellow"),
        ("herbs", "r", "Plant herbs", 470, 620, "purple"),
        ("feeders", "r", "Make bird feeders", 650, 620, "purple"),
        ("pots", "r", "Paint plant pots", 830, 620, "purple"),
        ("picnic", "o", "A shared picnic", 650, 810, "rose"),
        ("stories", "e", "Swap seeds & stories", 1070, 810, "yellow"),
        ("thanks", "o", "Photos & thank-yous", 270, 810, "green"),
    ]
    presets = {
        "blue": ((1505, 110), (218, 232, 252)),
        "green": ((1562, 110), (213, 232, 212)),
        "yellow": ((1448, 144), (255, 242, 204)),
        "purple": ((1562, 144), (225, 213, 231)),
        "rose": ((1505, 144), (248, 206, 204)),
    }
    s.record("diagram")
    for name, shape, label, x, y, colour in nodes:
        s.click(x, y, pause=0.04)
        s.key(shape, "Return", pause=0.06)
        s.type(label, delay=8, pause=0.04)
        s.key("Return", pause=0.06)
        s.click(*presets[colour][0], pause=0.10)
        s.key("F6", pause=0.06)

    # Read actual painted bounds after grid snapping. This avoids missing a
    # connector port by a few pixels at fractional zoom and UI scale.
    frame = s.grab()
    bounds = {}
    for name, _, _, x, y, colour in nodes:
        rgb = presets[colour][1]
        pixels = [(px, py) for py in range(y - 65, y + 65)
                  for px in range(x - 78, x + 78)
                  if all(abs(a - b) <= 2 for a, b in zip(frame.getpixel((px, py)), rgb))]
        if not pixels:
            raise RuntimeError(f"diagram: {name} did not appear with the expected colour")
        xs, ys = zip(*pixels)
        bounds[name] = (min(xs), min(ys), max(xs), max(ys))

    connections = [
        ("day", "before", "bottom", False), ("day", "welcome", "bottom", False),
        ("day", "weather", "bottom", False),
        ("before", "tools", "bottom", False), ("before", "invite", "bottom", False),
        ("before", "food", "bottom", False), ("welcome", "choose", "bottom", False),
        ("weather", "outside", "bottom", False), ("weather", "inside", "bottom", False),
        ("choose", "herbs", "bottom", False), ("choose", "feeders", "bottom", False),
        ("choose", "pots", "bottom", False),
        ("herbs", "picnic", "bottom", False), ("feeders", "picnic", "bottom", False),
        ("pots", "picnic", "bottom", False),
        ("outside", "picnic", "bottom", True), ("inside", "picnic", "bottom", True),
        ("picnic", "stories", "right", False), ("picnic", "thanks", "left", False),
    ]
    for source, target, port, elbow in connections:
        # Clear the previous edge's endpoint handles before reusing a port.
        s.click(1275, 900, pause=0.04)
        left, top, right, bottom = bounds[source]
        cx, cy = (left + right) // 2, (top + bottom) // 2
        start = {"bottom": (cx, bottom + 1), "right": (right + 1, cy), "left": (left - 1, cy)}[port]
        left, top, right, bottom = bounds[target]
        end = ((left + right) // 2, (top + bottom) // 2)
        s.move(cx, cy, pause=0.05)
        s.drag(*start, *end, steps=5, pause=0.05)
        if source == "weather":
            s.key("Return", pause=0.08)
            s.type("Yes" if target == "outside" else "No", delay=15, pause=0.05)
            s.key("Return", pause=0.08)
        if elbow:
            s.click(1470, 437, pause=0.08)

    s.click(1275, 900, pause=0.15)
    s.click(1293, 24, pause=0.5)  # Fit the finished plan.
    s.move(40, 940, pause=0.1)
    s.still("diagram-canvas")
    s.still("diagram-detail", box=(925, 190, 400, 300))
    # Speed up construction, then hold the finished diagram long enough to read.
    s.stop("diagram", speed=2.2, hold=3)


def encryption(s):
    """Encrypt one note, then a whole collection."""
    s.gui(GUI)
    s.record("encryption")
    s.wait(0.8)
    new_note(s, "Bank details")
    s.type("IBAN RS35 1234 5678 9012 3456 78\nPIN reminder: the year we met", delay=40, pause=0.6)
    command(s, "note encrypt", pause=1.2)
    s.type("correct horse", delay=90, pause=0.3)
    s.key("Return", pause=0.8)
    s.type("correct horse", delay=90, pause=0.3)
    s.key("Return", pause=1.5)
    # A collection with its own password protects every note in it.
    command(s, "collection create A demo safe", pause=0.8)
    command(s, "collection choose A demo safe", pause=0.8)
    new_note(s, "Travel documents")
    s.type("Passport 0123456, expires 2031", delay=40, pause=0.6)
    command(s, "browse", pause=1.8)
    s.key("Escape", pause=0.4)
    # The demo collection sorts first after All notes and Unsorted. Clicking
    # it avoids depending on the count of collections in a live fixture.
    s.click(100, 226, pause=0.8)
    s.key("e", pause=1.0)
    s.type("battery staple", delay=90, pause=0.3)
    s.key("Return", pause=0.8)
    s.type("battery staple", delay=90, pause=0.3)
    s.key("Return", pause=2.5)
    s.stop("encryption")


def ask(s):
    """Ask the agent (Claude Code) about the open note."""
    s.gui(GUI)
    open_note(s, "welcome to slate", settle=1.5)
    s.record("ask")
    s.wait(0.8)
    command(s, "ask", pause=1.0)
    s.type("What is left of the salary after rent and tax? One sentence.", delay=45, pause=0.4)
    s.key("Return", pause=1.0)
    s.wait(16)
    s.still("ask")
    # Copy latest puts the answer on the clipboard (Insert latest writes it into the note).
    s.click(411, 707, pause=1.5)
    s.key("Escape", pause=1.5)
    s.stop("ask", still=False)


def help_and_palette(s):
    """F1 help, and the command palette."""
    s.gui(GUI)
    s.record("help")
    s.wait(0.8)
    s.key("F1", pause=1.5)
    s.type("table", delay=90, pause=1.8)
    s.still("help")
    s.key("Escape", pause=0.4)
    s.key("Escape", pause=0.8)
    s.key("ctrl+shift+p", pause=1.0)
    s.type("export", delay=90, pause=1.2)
    s.key("Down", "Down", pause=0.6)
    s.key("Escape", pause=0.8)
    s.key("ctrl+e", pause=0.8)
    s.type("coll", delay=120, pause=1.5)
    s.key("Escape", pause=0.4)
    s.key("Escape", pause=0.8)
    s.stop("help", still=False)


THEMES = [
    ("everforest-dark", "everforest_dark"),
    ("catppuccin-mocha", {"scheme": "catppuccin-mocha"}),
    ("tokyo-night", {"scheme": "tokyo-night"}),
    ("gruvbox-light", {"scheme": "gruvbox-light"}),
    ("nord", {"scheme": "nord"}),
    ("everforest-light", "everforest_light"),
    ("dracula", {"scheme": "dracula"}),
    ("solarized-light", {"scheme": "solarized-light"}),
]


def themes(s):
    """The same note in several themes (stills joined into one GIF)."""
    from PIL import Image

    frames = []
    for name, theme in THEMES:
        s.gui({**GUI, "theme": theme})
        open_note(s, 'title:"Weekend in Lisbon" -collection:"Slate demo"', settle=1.5)
        s.key("ctrl+Home", "Down", pause=0.8)
        frames.append(s.grab())
        s.restart()
    out = s.media("themes.gif")
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=1600, loop=0)
    print(out)


def export_pdf(s):
    """Export a note to PDF and keep a picture of its first page."""
    import subprocess

    s.gui(GUI)
    open_note(s, "welcome to slate", settle=1.5)
    pdf = s.log.parent / "welcome.pdf"
    command(s, f"export pdf {pdf}", pause=4.0)
    out = s.media("export-pdf")
    subprocess.run(
            ["pdftoppm", "-png", "-r", "160", "-f", "1", "-l", "1", "-singlefile", str(pdf), str(out)],
        check=True,
    )
    print(f"{out}.png")


# -- terminal app ---------------------------------------------------------


def tui_vim(s):
    """Vim mode in the terminal app: motions, operators, a macro, search."""
    s.tui(["--new"])
    s.record("tui-vim")
    s.wait(0.8)
    s.type("Groceries\n\napples\nsourdough bread\nold cheese\ndates\n", delay=55, pause=0.5)
    s.key("Escape", pause=0.6)
    # A macro: make one line a checklist item, then replay it.
    s.key("g", "g", "j", "j", pause=0.3)
    s.key("q", "a", pause=0.4)
    s.key("I", pause=0.2)
    s.type("- [ ] ", delay=90)
    s.key("Escape", "j", pause=0.3)
    s.key("q", pause=0.6)
    s.key("3", "at", "a", pause=1.0)
    # Search, change a word, delete a line, undo.
    s.key("slash", pause=0.3)
    s.type("old", delay=90)
    s.key("Return", pause=0.5)
    s.key("c", "i", "w", pause=0.3)
    s.type("aged", delay=90)
    s.key("Escape", pause=0.6)
    s.key("j", "d", "d", pause=0.8)
    s.key("u", pause=0.8)
    s.key("question", pause=2.5)
    s.key("Escape", pause=1.0)
    s.stop("tui-vim")


def tui_tour(s):
    """The terminal app: switcher, browser and graph over 25,000 notes."""
    s.tui()
    s.wait(1.0)
    # The link index is built once per run; build it before recording.
    s.key("ctrl+e", pause=0.4)
    s.type("graph", delay=20)
    s.key("Return", pause=50)
    s.key("Escape", pause=1.0)
    s.record("tui-tour")
    s.wait(1.0)
    s.key("ctrl+p", pause=0.8)
    s.type("sailing hub", delay=70, pause=1.5)
    s.key("Down", pause=0.3)
    s.key("Return", pause=1.5)
    s.key("ctrl+b", pause=1.5)
    s.key("Escape", pause=0.5)
    s.key("h", pause=0.5)
    for _ in range(6):
        s.key("j", pause=0.3)
    s.key("l", pause=0.8)
    for _ in range(5):
        s.key("j", pause=0.4)
    s.key("q", pause=0.8)
    s.key("ctrl+e", pause=0.4)
    s.type("graph", delay=80)
    s.key("Return", pause=4.0)
    for key in ("l", "l", "j", "j", "Tab", "Tab", "bracketright", "bracketright"):
        s.key(key, pause=0.7)
    s.key("Escape", pause=1.0)
    s.stop("tui-tour")


def capture_shell(s):
    """Capture from the shell into today's note, then open it."""
    s.env["PS1"] = "$ "
    s.terminal("bash", "--norc", "--noprofile", path=[s.slate / "target/release"])
    s.record("capture")
    s.wait(1.0)
    s.type('slate capture "call the bank about the card"', delay=45)
    s.key("Return", pause=0.8)
    s.type('echo "deploy 4.2 finished" | slate capture', delay=45)
    s.key("Return", pause=0.8)
    s.type("slate today", delay=60)
    s.key("Return", pause=3.0)
    s.key("ctrl+q", pause=1.5)
    s.stop("capture")


def fill_handle(s):
    """Centre of the fill handle: the filled accent dot on the focused cell's
    corner. Formula values share the accent colour, so only a round, mostly
    filled blob counts."""
    from PIL import ImageChops

    image = s.grab()
    accent = (0xA7, 0xC0, 0x80)  # everforest_dark
    bands = [
        band.point(lambda v, t=target: 255 if abs(v - t) < 24 else 0)
        for band, target in zip(image.split(), accent)
    ]
    mask = ImageChops.multiply(ImageChops.multiply(bands[0], bands[1]), bands[2])
    width = image.width
    on = {(i % width, i // width) for i, v in enumerate(mask.getdata()) if v}
    best = None
    while on:
        blob, stack = [], [on.pop()]
        while stack:
            x, y = stack.pop()
            blob.append((x, y))
            for near in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if near in on:
                    on.remove(near)
                    stack.append(near)
        xs, ys = [p[0] for p in blob], [p[1] for p in blob]
        w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
        if 5 <= w <= 18 and abs(w - h) <= 2 and len(blob) >= 0.6 * w * h:
            if best is None or len(blob) > best[0]:
                best = (len(blob), (min(xs) + max(xs)) // 2, (min(ys) + max(ys)) // 2)
    if best is None:
        raise SystemExit("fill handle not found on screen")
    return best[1], best[2]


def table_fill(s):
    """A diff formula and a date, each written once and dragged down."""
    s.gui(GUI)
    s.wait(0.8)
    new_note(s, "Daily balance")
    s.paste(
        "| Date | Amount | Diff |\n"
        "| --- | ---: | ---: |\n"
        "| 03. November 2026. | 455801 | N/A |\n"
        "|  | 460250 |  |\n"
        "|  | 462470 |  |\n"
        "|  | 466966 |  |\n"
        "|  | 471492 |  |\n"
        "|  | 476034 |  |",
        pause=1.5,
    )
    # The cursor is in the last Diff cell; the handle's step between two
    # rows gives the row height.
    _, last = fill_handle(s)
    s.key("Up", pause=0.4)
    _, above = fill_handle(s)
    row = last - above
    s.key("Up", "Up", "Up", pause=0.4)
    s.record("table-fill")
    s.wait(1.0)
    # Row 2's change from row 1, then drag it down to the last row.
    s.type(":=(2,2)-(1,2)", delay=70, pause=1.0)
    x, y = fill_handle(s)
    s.drag(x, y, x, y + int(3.5 * row), steps=30, pause=1.8)
    # The first date, dragged down: the next days fill in.
    s.key("Up", "Up", "Up", "Up", "Up", pause=0.3)
    s.key("shift+Tab", "shift+Tab", pause=0.8)
    x, y = fill_handle(s)
    s.drag(x, y, x, y + int(4.5 * row), steps=30, pause=2.5)
    s.stop("table-fill")


SCENARIOS = {
    "tour": tour,
    "writing": writing,
    "calc": calc,
    "currency": currency,
    "variables": variables,
    "cross-note": cross_note,
    "tables": tables,
    "table-fill": table_fill,
    "search": search,
    "browser": browser,
    "graph": graph,
    "history": history,
    "diagram": diagram,
    "links": links,
    "images": images,
    "desktop": desktop,
    "encryption": encryption,
    "ask": ask,
    "help": help_and_palette,
    "themes": themes,
    "export": export_pdf,
    "tui-vim": tui_vim,
    "tui-tour": tui_tour,
    "capture": capture_shell,
}
