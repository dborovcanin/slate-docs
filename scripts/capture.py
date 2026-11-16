#!/usr/bin/env python3
"""Record the user guide's GIFs from the real apps on a virtual display.

    python3 scripts/capture.py --data ~/tst [--slate ../slate] [scenario ...]

`--slate` is a slate checkout with release builds of both apps (`make build`
and `make ui-build`). `--data` is the data directory of a demo database (`<data>/slate/notes.db`,
used as `XDG_DATA_HOME`); scenarios create and edit notes in it, so point it
at a test dataset, never your own notes. Its `gui-settings.json` is put back
afterwards. The config is `scripts/config.toml`, in a temporary directory. Each scenario starts the release build of the desktop app (or the
terminal app in Alacritty) on its own Xvfb display, drives it with xdotool,
records it with ffmpeg and writes `docs/media/<name>.gif`.
Needs Xvfb, xdotool, xclip, ffmpeg and Mesa's lavapipe Vulkan driver.
"""
import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
MEDIA = ROOT / "docs/media"
WIDTH, HEIGHT = 1600, 1000


class Session:
    """One app on one virtual display, with input helpers and a recorder."""

    def __init__(self, slate: pathlib.Path, data: pathlib.Path, config: pathlib.Path, display: int):
        self.slate = slate
        self.data = data
        self.log = config / "capture.log"
        self.display = f":{display}"
        self.env = os.environ.copy()
        self.env.pop("WAYLAND_DISPLAY", None)
        runtime = pathlib.Path(tempfile.mkdtemp(prefix="slate-docs-"))
        runtime.chmod(0o700)
        self.env.update(
            DISPLAY=self.display,
            XDG_DATA_HOME=str(data),
            XDG_CONFIG_HOME=str(config),
            XDG_RUNTIME_DIR=str(runtime),
            GPUI_FORCE_X11="1",
            VK_ICD_FILENAMES=next(
                iter(sorted(pathlib.Path("/usr/share/vulkan/icd.d").glob("lvp*.json"))), ""
            ).__str__(),
        )
        self.xvfb = subprocess.Popen(
            ["Xvfb", self.display, "-screen", "0", f"{WIDTH}x{HEIGHT}x24", "-nolisten", "tcp"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # Ready once it answers a query (a stale socket file does not).
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            ready = subprocess.run(
                ["xdotool", "getdisplaygeometry"], env=self.env, capture_output=True
            )
            if ready.returncode == 0 and self.xvfb.poll() is None:
                break
            time.sleep(0.1)
        time.sleep(0.5)
        self.app = None
        self.window = None
        self.recorder = None

    # -- apps -------------------------------------------------------------

    def gui(self, settings: dict, args=()):
        path = self.data / "slate/gui-settings.json"
        path.write_text(json.dumps(settings, indent=2))
        self._launch([str(self.slate / "crates/gui/target/release/slate-gui"), *args])

    def tui(self, args=()):
        command = [
            "alacritty",
            "--config-file",
            str(ROOT / "scripts/alacritty.toml"),
            "-e",
            str(self.slate / "target/release/slate"),
            *args,
        ]
        self._launch(command)

    def terminal(self, *argv, path=()):
        """Alacritty running `argv` (a shell, for example)."""
        self.env["PATH"] = os.pathsep.join([*map(str, path), self.env["PATH"]])
        self._launch(
            ["alacritty", "--config-file", str(ROOT / "scripts/alacritty.toml"), "-e", *argv]
        )

    def _launch(self, command):
        log = open(self.log, "a")
        self.app = subprocess.Popen(command, env=self.env, stdout=log, stderr=log)
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            found = subprocess.run(
                ["xdotool", "search", "--onlyvisible", "--pid", str(self.app.pid)],
                env=self.env,
                capture_output=True,
                text=True,
            ).stdout.split()
            if found:
                self.window = found[0]
                break
            if self.app.poll() is not None:
                sys.exit(f"app exited; see {self.log}")
            time.sleep(0.25)
        else:
            sys.exit("no window appeared")
        self.x("windowmove", self.window, "0", "0")
        self.x("windowsize", self.window, str(WIDTH), str(HEIGHT))
        self.x("windowfocus", "--sync", self.window)
        time.sleep(2.0)

    # -- input ------------------------------------------------------------

    def x(self, *args):
        subprocess.run(["xdotool", *args], env=self.env, check=True)

    def key(self, *keys, pause=0.35):
        for key in keys:
            self.x("key", "--clearmodifiers", key)
            time.sleep(pause)

    def type(self, text, delay=55, pause=0.4):
        for i, line in enumerate(text.split("\n")):
            if i:
                self.x("key", "Return")
            if line:
                self.x("type", "--delay", str(delay), "--", line)
        time.sleep(pause)

    def paste(self, text, pause=0.6):
        subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode(), env=self.env)
        self.key("ctrl+v", pause=pause)

    def paste_image(self, path, pause=1.5):
        subprocess.run(
            ["xclip", "-selection", "clipboard", "-t", "image/png", "-i", str(path)],
            env=self.env, check=True,
        )
        self.key("ctrl+v", pause=pause)

    def click(self, x, y, button="1", pause=0.5):
        self.x("mousemove", str(x), str(y))
        self.x("click", button)
        time.sleep(pause)

    def drag(self, x1, y1, x2, y2, steps=20, pause=0.5):
        """Press at (x1, y1), move to (x2, y2) in steps, release."""
        self.x("mousemove", str(x1), str(y1))
        time.sleep(0.25)
        self.x("mousedown", "1")
        for i in range(1, steps + 1):
            self.x("mousemove", str(x1 + (x2 - x1) * i // steps), str(y1 + (y2 - y1) * i // steps))
            time.sleep(0.03)
        time.sleep(0.15)
        self.x("mouseup", "1")
        time.sleep(pause)

    def scroll(self, x, y, up=True, clicks=3, pause=0.4):
        self.x("mousemove", str(x), str(y))
        for _ in range(clicks):
            self.x("click", "4" if up else "5")
            time.sleep(0.08)
        time.sleep(pause)

    def move(self, x, y, pause=0.3):
        self.x("mousemove", str(x), str(y))
        time.sleep(pause)

    def wait(self, seconds):
        time.sleep(seconds)

    # -- recording --------------------------------------------------------

    def record(self, name):
        self.clip = self.log.parent / f"{name}.mkv"
        self.recorder = subprocess.Popen(
            [
                "ffmpeg", "-y", "-loglevel", "error",
                "-f", "x11grab", "-framerate", "25",
                "-video_size", f"{WIDTH}x{HEIGHT}", "-i", f"{self.display}+0,0",
                "-c:v", "libx264rgb", "-preset", "ultrafast", "-crf", "0",
                str(self.clip),
            ],
            stdin=subprocess.PIPE,
            env=self.env,
        )
        time.sleep(0.8)

    def stop(self, name, width=WIDTH, fps=15, colors=256, still=True):
        self.key("ctrl+s", pause=1.5)
        self.recorder.communicate(b"q")
        self.recorder = None
        if still:
            self.still(name)
        MEDIA.mkdir(parents=True, exist_ok=True)
        gif = MEDIA / f"{name}.gif"
        graph = (
            f"fps={fps},scale={width}:-1:flags=lanczos,split[a][b];"
            f"[a]palettegen=max_colors={colors}:stats_mode=diff[p];"
            "[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle"
        )
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(self.clip),
             "-vf", graph, "-loop", "0", str(gif)],
            check=True,
        )
        # Retain the lossless source outside the published site for recuts and
        # sharp screenshots, without checking large intermediates into Git.
        sources = ROOT / ".cache/capture"
        sources.mkdir(parents=True, exist_ok=True)
        shutil.move(str(self.clip), sources / f"{name}.mkv")
        print(f"{gif.relative_to(ROOT)}: {gif.stat().st_size / 1e6:.1f} MB", flush=True)

    def still(self, name, box=None):
        """A PNG of the screen, optionally cropped to (x, y, w, h)."""
        MEDIA.mkdir(parents=True, exist_ok=True)
        out = MEDIA / f"{name}.png"
        crop = [] if box is None else ["-vf", "crop={2}:{3}:{0}:{1}".format(*box)]
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "x11grab",
             "-video_size", f"{WIDTH}x{HEIGHT}", "-i", f"{self.display}+0,0",
             "-frames:v", "1", *crop, str(out)],
            env=self.env,
            check=True,
        )
        print(out)

    def grab(self):
        """The screen as a PIL image."""
        from PIL import Image

        shot = self.log.parent / "grab.png"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "x11grab",
             "-video_size", f"{WIDTH}x{HEIGHT}", "-i", f"{self.display}+0,0",
             "-frames:v", "1", str(shot)],
            env=self.env,
            check=True,
        )
        return Image.open(shot).convert("RGB")

    def media(self, name):
        MEDIA.mkdir(parents=True, exist_ok=True)
        return MEDIA / name

    def restart(self):
        """Quit the app, keeping the display, so another can start."""
        if self.app and self.app.poll() is None:
            self.app.terminate()
            try:
                self.app.wait(5)
            except subprocess.TimeoutExpired:
                self.app.kill()
        self.app = None

    def close(self):
        if self.recorder and self.recorder.poll() is None:
            self.recorder.kill()
        if self.app and self.app.poll() is None:
            self.app.terminate()
            try:
                self.app.wait(5)
            except subprocess.TimeoutExpired:
                self.app.kill()
        self.xvfb.terminate()
        self.xvfb.wait(10)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data", type=pathlib.Path, required=True)
    parser.add_argument("--slate", type=pathlib.Path, default=ROOT.parent / "slate")
    parser.add_argument("--display", type=int, default=91)
    parser.add_argument("names", nargs="*")
    args = parser.parse_args()
    data = args.data.expanduser().resolve()
    if not (data / "slate/notes.db").exists():
        sys.exit(f"no notes database at {data / 'slate/notes.db'}")
    config = pathlib.Path(tempfile.mkdtemp(prefix="slate-docs-config-"))
    (config / "slate").mkdir()
    # Currency rates come from the dataset's own cache, without a fetch.
    cache = data / "slate/exchange_rates.json"
    rates = [
        sys.executable, "-c",
        "import json,sys; d=json.load(open(sys.argv[1])); d.pop('fetched_at',None); print(json.dumps(d))",
        str(cache),
    ]
    template = (ROOT / "scripts/config.toml").read_text()
    (config / "slate/config.toml").write_text(template.replace("@RATES@", json.dumps(rates)))
    import scenarios

    settings = data / "slate/gui-settings.json"
    saved = settings.read_bytes() if settings.exists() else None
    names = args.names or list(scenarios.SCENARIOS)
    unknown = set(names) - scenarios.SCENARIOS.keys()
    if unknown:
        parser.error(f"unknown scenarios: {', '.join(sorted(unknown))}")
    try:
        for name in names:
            session = Session(args.slate.resolve(), data, config, args.display)
            try:
                scenarios.SCENARIOS[name](session)
            finally:
                session.close()
    finally:
        if saved is None:
            settings.unlink(missing_ok=True)
        else:
            settings.write_bytes(saved)
    print(f"log: {config / 'capture.log'}")


if __name__ == "__main__":
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    main()
