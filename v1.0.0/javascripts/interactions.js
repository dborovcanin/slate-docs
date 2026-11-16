/* Expand screenshots and recordings, including after instant navigation. */
(() => {
  const viewer = document.createElement("dialog");
  viewer.className = "slate-viewer";
  viewer.setAttribute("aria-label", "Media viewer");
  viewer.innerHTML = `
    <div class="slate-viewer__toolbar">
      <p class="slate-viewer__title"></p>
      <button type="button" class="slate-viewer__zoom" aria-pressed="false">Zoom in</button>
      <button type="button" class="slate-viewer__close" autofocus aria-label="Close viewer">Close <span aria-hidden="true">×</span></button>
    </div>
    <div class="slate-viewer__stage"><img alt=""></div>`;
  document.body.append(viewer);
  const image = viewer.querySelector("img");
  const title = viewer.querySelector(".slate-viewer__title");
  const zoom = viewer.querySelector(".slate-viewer__zoom");
  const stage = viewer.querySelector(".slate-viewer__stage");
  let opener;

  const setZoom = expanded => {
    viewer.classList.toggle("slate-viewer--zoomed", expanded);
    zoom.setAttribute("aria-pressed", String(expanded));
    zoom.textContent = expanded ? "Fit to screen" : "Zoom in";
    stage.scrollTo(0, 0);
  };
  zoom.addEventListener("click", () => setZoom(zoom.getAttribute("aria-pressed") !== "true"));
  image.addEventListener("click", () => zoom.click());
  viewer.querySelector(".slate-viewer__close").addEventListener("click", () => viewer.close());
  viewer.addEventListener("click", event => {
    if (event.target === stage) viewer.close();
  });
  viewer.addEventListener("close", () => {
    document.documentElement.classList.remove("slate-viewer-open");
    image.removeAttribute("src");
    if (opener?.isConnected) opener.focus({preventScroll: true});
  });

  document.addEventListener("click", event => {
    const link = event.target.closest(".slate-recording");
    if (!link || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
    event.preventDefault();
    opener = link;
    const recording = link.querySelector("img");
    image.src = recording.currentSrc || recording.src;
    image.alt = recording.alt;
    title.textContent = recording.alt || "Slate recording";
    setZoom(false);
    document.documentElement.classList.add("slate-viewer-open");
    viewer.showModal();
  });

  // Material's palette uses labels; give them keyboard activation as well.
  document.addEventListener("keydown", event => {
    if ((event.key === "Enter" || event.key === " ") && event.target.matches('[data-md-component="palette"] label')) {
      event.preventDefault();
      event.target.click();
      requestAnimationFrame(() => document.querySelector('[data-md-component="palette"] label:not([hidden])')?.focus());
    }
  });

  const enhance = () => {
    if (viewer.open) viewer.close();
    document.querySelectorAll('.md-content img').forEach(recording => {
      const source = new URL(recording.src);
      if (!source.pathname.includes("/media/") || !/\.(gif|png|jpe?g|webp)$/i.test(source.pathname)) return;
      let link = recording.closest("a");
      // Keep images that link to another page behaving as normal links.
      if (link && new URL(link.href).href !== source.href) return;
      if (!link) {
        link = document.createElement("a");
        link.href = recording.src;
        recording.replaceWith(link);
        link.append(recording);
      }
      link.classList.add("slate-recording");
      link.setAttribute("aria-haspopup", "dialog");
      link.setAttribute("aria-label", `Expand image: ${recording.alt || "Slate"}`);
    });
    document.querySelectorAll('[data-md-component="palette"] label').forEach(label => {
      label.tabIndex = 0;
      label.setAttribute("role", "button");
      label.setAttribute("aria-label", label.title);
    });
  };
  if (typeof document$ !== "undefined") document$.subscribe(enhance);
  else enhance();
})();
