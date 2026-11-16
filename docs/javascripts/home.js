/* A small illustrative notebook. Feature previews use Material's native tabs. */
(() => {
  let dispose = () => {};
  const initialize = () => {
    dispose();
    const root = document.querySelector("[data-slate-network]");
    if (!root) return;
    const svg = root.querySelector("svg");
    const title = root.querySelector("[data-network-title]");
    const detail = root.querySelector("[data-network-detail]");
    const reset = root.querySelector(".slate-network__reset");
    const events = new AbortController();
    const signal = events.signal;
    const motion = matchMedia("(prefers-reduced-motion: reduce)");
    const entries = [
      ["My notebook", 0.52, 0.47, 1, "getting-started/"],
      ["Ideas", 0.26, 0.30, 0.72, "links-and-graph/"],
      ["Writing", 0.74, 0.26, 0.73, "writing/"],
      ["Projects", 0.79, 0.65, 0.79, "organizing/"],
      ["Reading", 0.28, 0.73, 0.69, "links-and-graph/"],
      ["Systems", 0.50, 0.16, 0.57, "organizing/"],
      ["Creativity", 0.14, 0.51, 0.59, "writing/"],
      ["Design", 0.91, 0.40, 0.52, "diagrams/"],
      ["Daily notes", 0.52, 0.82, 0.62, "organizing/"],
      ["Research", 0.68, 0.91, 0.43, "search/"],
      ["Diagrams", 0.91, 0.82, 0.46, "diagrams/"],
      ["Thoughts", 0.40, 0.58, 0.44, "writing/"],
      ["Goals", 0.08, 0.20, 0.35, "organizing/"],
      ["Connections", 0.66, 0.53, 0.42, "links-and-graph/"],
      ["Books", 0.17, 0.88, 0.35, "links-and-graph/"],
      ["Numbers", 0.82, 0.11, 0.36, "calculations/"],
      ["Archive", 0.39, 0.93, 0.34, "organizing/"],
      ["Patterns", 0.42, 0.34, 0.32, "links-and-graph/"],
    ];
    const pairs = [[0,1],[0,2],[0,3],[0,4],[0,5],[0,8],[0,11],[0,13],
      [1,6],[1,11],[1,12],[1,17],[2,5],[2,7],[2,15],[3,7],[3,9],[3,10],
      [3,13],[4,6],[4,14],[4,16],[5,13],[5,17],[6,12],[7,10],[8,9],
      [8,16],[9,10],[11,17],[13,17]];
    const create = (tag, attributes, parent = svg) => {
      const element = document.createElementNS("http://www.w3.org/2000/svg", tag);
      for (const [name, value] of Object.entries(attributes)) element.setAttribute(name, value);
      parent.append(element);
      return element;
    };
    svg.replaceChildren();
    const defs = create("defs", {});
    const glow = create("radialGradient", {id: "slate-network-glow"}, defs);
    create("stop", {offset: "0", "stop-color": "var(--network-green)", "stop-opacity": "0.24"}, glow);
    create("stop", {offset: "1", "stop-color": "var(--network-green)", "stop-opacity": "0"}, glow);
    const edges = pairs.map(([from, to], index) => ({from, to,
      element: create("line", {class: "slate-network__edge"}),
      particle: create("circle", {class: "slate-network__particle", r: "1.5"})}));
    const nodes = entries.map(([label, nx, ny, weight, href], index) => {
      const x = nx * 560, y = ny * 560;
      const color = index && index % 5 === 0 ? "purple" : "green";
      const radius = index ? 3.5 + weight * 4 : 10;
      const element = create("a", {href, tabindex: "0", class: `slate-network__node${index ? "" : " slate-network__node--main"}`,
        "aria-label": `${label}: open the guide`, style: `--node-color: var(--network-${color})`});
      create("circle", {class: "slate-network__glow", r: index ? "38" : "55"}, element);
      create("circle", {class: "slate-network__hit", r: "24"}, element);
      create("circle", {class: "slate-network__focus-ring", r: radius + 5}, element);
      if (!index) create("circle", {class: "slate-network__halo", r: "19"}, element);
      create("circle", {class: "slate-network__dot", r: radius}, element);
      create("text", {y: radius + 19}, element).textContent = label;
      return {label, x, y, initial: [x, y], vx: 0, vy: 0, seed: index * 1.4, element};
    });
    let elapsed = 0;
    const draw = () => {
      nodes.forEach(node => node.element.setAttribute("transform", `translate(${node.x} ${node.y})`));
      edges.forEach((edge, index) => {
        const from = nodes[edge.from], to = nodes[edge.to];
        for (const [name, value] of Object.entries({x1: from.x, y1: from.y, x2: to.x, y2: to.y})) edge.element.setAttribute(name, value);
        const progress = (elapsed * 0.0924 + index * 0.12) % 1;
        edge.particle.setAttribute("cx", from.x + (to.x - from.x) * progress);
        edge.particle.setAttribute("cy", from.y + (to.y - from.y) * progress);
      });
    };
    const select = index => {
      const related = new Set([index]);
      edges.forEach(edge => {
        const active = edge.from === index || edge.to === index;
        edge.element.classList.toggle("is-related", active);
        edge.particle.classList.toggle("is-related", active);
        if (active) { related.add(edge.from); related.add(edge.to); }
      });
      nodes.forEach((node, i) => {
        node.element.classList.toggle("is-related", related.has(i));
        node.element.classList.toggle("is-active", i === index);
      });
      root.classList.toggle("has-selection", index >= 0);
      title.textContent = index < 0 ? "Ideas & connections" : nodes[index].label;
      detail.textContent = index < 0 ? "Hover a node to explore" : `${related.size - 1} connected notes`;
    };
    let drag = null;
    let suppressClick = false;
    nodes.forEach((node, index) => {
      node.element.addEventListener("pointerenter", () => { if (!drag) select(index); }, {signal});
      node.element.addEventListener("focus", () => select(index), {signal});
      node.element.addEventListener("pointerdown", event => {
        if (event.button !== 0 || drag) return;
        suppressClick = false;
        drag = {node, pointer: event.pointerId, x: event.clientX, y: event.clientY};
        node.element.setPointerCapture(event.pointerId);
        select(index);
      }, {signal});
      node.element.addEventListener("click", event => {
        if (suppressClick) { event.preventDefault(); suppressClick = false; }
      }, {signal});
    });
    svg.addEventListener("pointermove", event => {
      if (!drag || drag.pointer !== event.pointerId) return;
      if (Math.hypot(event.clientX - drag.x, event.clientY - drag.y) < 5 && !suppressClick) return;
      suppressClick = true;
      const point = new DOMPoint(event.clientX, event.clientY).matrixTransform(svg.getScreenCTM().inverse());
      drag.node.x = Math.max(30, Math.min(530, point.x));
      drag.node.y = Math.max(30, Math.min(530, point.y));
      drag.node.vx = drag.node.vy = 0;
      draw();
    }, {signal});
    const release = () => { drag = null; };
    svg.addEventListener("pointerup", release, {signal});
    svg.addEventListener("pointercancel", release, {signal});
    svg.addEventListener("lostpointercapture", release, {signal});
    root.addEventListener("pointerleave", () => { if (!drag && !root.contains(document.activeElement)) select(-1); }, {signal});
    root.addEventListener("focusout", event => { if (!root.contains(event.relatedTarget)) select(-1); }, {signal});
    reset.addEventListener("click", () => {
      nodes.forEach(node => { [node.x, node.y] = node.initial; node.vx = node.vy = 0; });
      draw();
      select(-1);
    }, {signal});
    let visible = false;
    let running = false;
    let frame = 0;
    let previous = 0;
    const tick = now => {
      if (!running) return;
      const delta = previous ? Math.min(now - previous, 32) : 16.67;
      previous = now;
      elapsed += delta / 1000;
      const step = delta / 16.67;
      nodes.forEach(node => {
        if (node === drag?.node) return;
        const tx = node.initial[0] + Math.sin(elapsed * 0.3828 + node.seed) * 9;
        const ty = node.initial[1] + Math.cos(elapsed * 0.2904 + node.seed) * 10;
        node.vx = (node.vx + (tx - node.x) * 0.006 * step) * 0.92 ** step;
        node.vy = (node.vy + (ty - node.y) * 0.006 * step) * 0.92 ** step;
        node.x += node.vx * step;
        node.y += node.vy * step;
      });
      draw();
      frame = requestAnimationFrame(tick);
    };
    const animate = () => {
      const next = visible && !document.hidden && !motion.matches;
      root.classList.toggle("is-live", next);
      if (next === running) return;
      running = next;
      if (running) { previous = 0; frame = requestAnimationFrame(tick); }
      else { cancelAnimationFrame(frame); draw(); }
    };
    const observer = new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; animate(); });
    observer.observe(root);
    motion.addEventListener("change", animate, {signal});
    document.addEventListener("visibilitychange", animate, {signal});
    draw();
    root.classList.add("is-enhanced");
    svg.removeAttribute("hidden");
    reset.hidden = false;
    dispose = () => {
      running = false;
      cancelAnimationFrame(frame);
      events.abort();
      observer.disconnect();
      root.classList.remove("is-live");
    };
  };
  if (typeof document$ !== "undefined") document$.subscribe(initialize);
  else initialize();
})();
