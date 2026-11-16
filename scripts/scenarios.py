"""The user guide's recordings, one function per GIF (see capture.py).

Each scenario drives a real app with the keyboard (the mouse only where a
gesture needs it) over the demo dataset, and records one GIF or still.
"""

GUI = {
    "vim": False,
    "theme": "everforest_dark",
    "sidebar": False,
    "wrap": True,
    "proportional_prose": True,
    "font_size": 17.0,
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
    s.key("Down", "Down", "Down", pause=0.5)
    s.key("Return", pause=2.5)
    s.stop("search")


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
    """The link graph around a hub note, then a step out."""
    s.gui(GUI)
    open_note(s, "woodworking hub", settle=2.0)
    # The first opening indexes every note's links once; do it off camera.
    command(s, "graph", pause=50)
    s.key("Escape", pause=1.5)
    s.record("graph")
    s.wait(0.8)
    command(s, "graph", pause=4.0)
    for key in ("Right", "Right", "Down", "Down", "Left"):
        s.key(key, pause=0.7)
    s.scroll(640, 420, up=True, clicks=4, pause=1.2)
    s.scroll(640, 420, up=False, clicks=4, pause=1.0)
    s.key("slash", pause=0.5)
    s.type("dovetail", delay=90, pause=1.5)
    s.key("Return", pause=1.5)
    s.stop("graph", width=880, fps=8, colors=96)


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
    s.key("Escape", pause=1.0)
    s.stop("history")


def diagram(s):
    """Draw a diagram on the canvas; it stays Markdown text in the note."""
    s.gui(GUI)
    s.record("diagram")
    s.wait(0.8)
    new_note(s, "Service sketch")
    command(s, "diagram", pause=1.5)
    s.move(420, 300)
    s.key("r", pause=0.5)
    s.key("Return", pause=0.3)
    s.type("API", delay=80)
    s.key("Return", pause=0.5)
    s.move(800, 300)
    s.key("c", pause=0.5)
    s.key("Return", pause=0.3)
    s.type("Postgres", delay=80)
    s.key("Return", pause=0.5)
    s.move(420, 560)
    s.key("d", pause=0.5)
    s.key("Return", pause=0.3)
    s.type("Cached?", delay=80)
    s.key("Return", pause=0.5)
    # Connect: drag from a side port (shown on hover) to another shape.
    s.move(430, 300, pause=0.6)
    s.drag(544, 296, 804, 300, pause=0.8)
    s.move(430, 300, pause=0.6)
    s.drag(424, 356, 424, 556, pause=0.8)
    # Colour the shapes from the Style presets.
    s.click(380, 280, pause=0.5)
    s.click(1184, 109, pause=0.8)
    s.click(760, 310, pause=0.5)
    s.click(1243, 109, pause=0.8)
    s.click(424, 556, pause=0.5)
    s.click(1128, 143, pause=0.8)
    s.click(1070, 23, pause=2.0)
    s.key("Escape", pause=0.6)
    s.key("Escape", pause=1.2)
    s.key("Escape", pause=0.6)
    s.key("ctrl+Home", pause=0.2)
    s.key("Up", "Up", "Up", "Up", pause=0.1)
    s.wait(2.0)
    s.stop("diagram")


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
    command(s, "collection create Private", pause=0.8)
    command(s, "collection choose Private", pause=0.8)
    new_note(s, "Travel documents")
    s.type("Passport 0123456, expires 2031", delay=40, pause=0.6)
    command(s, "browse", pause=1.8)
    s.key("Escape", pause=0.4)
    s.key("Tab", pause=0.6)
    # Down the collections to Private (sorted by name, after the 14 topics).
    for _ in range(16):
        s.key("Down", pause=0.1)
    s.key("e", pause=1.0)
    s.type("battery staple", delay=90, pause=0.3)
    s.key("Return", pause=0.8)
    s.type("battery staple", delay=90, pause=0.3)
    s.key("Return", pause=2.5)
    s.key("Escape", pause=0.4)
    s.key("Escape", pause=0.8)
    command(s, "collection choose none", pause=1.5)
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
    # Copy latest puts the answer on the clipboard (Insert latest writes it into the note).
    s.click(411, 707, pause=1.5)
    s.key("Escape", pause=1.5)
    s.stop("ask")


def help_and_palette(s):
    """F1 help, and the command palette."""
    s.gui(GUI)
    s.record("help")
    s.wait(0.8)
    s.key("F1", pause=1.5)
    s.type("table", delay=90, pause=1.8)
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
    s.stop("help")


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
        open_note(s, "weekend in lisbon", settle=1.5)
        s.key("ctrl+Home", pause=0.8)
        frames.append(s.grab())
        s.restart()
    out = s.media("themes.gif")
    small = [f.resize((1024, 640), Image.LANCZOS) for f in frames]
    small[0].save(out, save_all=True, append_images=small[1:], duration=1600, loop=0)
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
        ["pdftoppm", "-png", "-r", "80", "-f", "1", "-l", "1", "-singlefile", str(pdf), str(out)],
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


SCENARIOS = {
    "tour": tour,
    "writing": writing,
    "calc": calc,
    "currency": currency,
    "variables": variables,
    "cross-note": cross_note,
    "tables": tables,
    "search": search,
    "browser": browser,
    "graph": graph,
    "history": history,
    "diagram": diagram,
    "encryption": encryption,
    "ask": ask,
    "help": help_and_palette,
    "themes": themes,
    "export": export_pdf,
    "tui-vim": tui_vim,
    "tui-tour": tui_tour,
    "capture": capture_shell,
}
