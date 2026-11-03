// Colour wheels on the web: the same two wheels as color_wheel.py --app.
// Every part (back and front of each disc) turns by dragging it, with the
// mouse wheel, or with the arrow keys; the select box changes the language
// and a button switches between light and dark mode.
// Angles: turns are clockwise in degrees; window angles in data.js are
// counter-clockwise from 3 o'clock, as in color_wheel.py.
"use strict";

(function () {
  const D = window.WHEEL_DATA;
  const STEP = D.step;
  const turn = [0, 0, 0, 0];         // order of D.parts: d1b, d1f, d2b, d2f
  let sel = 1;
  let lang = "en";
  let drag = null;

  const $ = (id) => document.getElementById(id);
  const imgs = D.parts.map((p) => $("img-" + p));
  const discs = [$("disc-0"), $("disc-1")];
  const rings = [$("ring-0"), $("ring-1")];
  const wheels = $("wheels");
  const mod = (a, n) => ((a % n) + n) % n;

  function startLang() {
    const asked = new URLSearchParams(location.search).get("lang");
    if (asked && D.langs[asked]) return asked;
    // the browser's languages in order of preference: a full code (pt-BR) first, then
    // the language alone (fr-CA -> fr, zh-Hans-CN -> zh)
    for (const code of navigator.languages || [navigator.language || "en"]) {
      if (D.langs[code]) return code;
      const base = code.split("-")[0];
      if (base === "pt" && /-BR$/i.test(code) && D.langs["pt-BR"]) return "pt-BR";
      if (D.langs[base]) return base;
    }
    return "en";
  }

  function setLang(l) {
    lang = l;
    const S = D.langs[l];
    document.documentElement.lang = l;
    document.documentElement.dir = (D.rtl || []).includes(l) ? "rtl" : "ltr";
    document.title = S.app_title;
    $("title").textContent = S.app_title;
    $("lang-label").textContent = S.app_lang;
    $("reset").textContent = S.app_reset;
    $("lang").value = l;
    themeButton();
    const help = $("help");
    help.replaceChildren(...S.app_help.map((t) => {
      const li = document.createElement("li");
      li.textContent = t;
      return li;
    }));
    D.parts.forEach((p, i) => { imgs[i].alt = S.parts[i]; });
    discSources();
    render();
  }

  // light or dark: set on <html> by the script in index.html, changed by
  // the button (remembered) or by the system while nothing was chosen
  const theme = () => document.documentElement.dataset.theme;

  function discSources() {
    const suffix = theme() === "dark" ? "-dark" : "";
    D.parts.forEach((p, i) => { imgs[i].src = "discs/" + lang + "/" + p + suffix + ".svg"; });
  }

  function themeButton() {
    const S = D.langs[lang];
    $("theme").textContent = theme() === "dark" ? "☀ " + S.app_light : "☾ " + S.app_dark;
  }

  function setTheme(t, remember = true) {
    document.documentElement.dataset.theme = t;
    if (remember) {
      try { localStorage.setItem("wheels-theme", t); } catch (e) { /* private mode */ }
    }
    themeButton();
    discSources();
  }

  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (ev) => {
    let chosen = null;
    try { chosen = localStorage.getItem("wheels-theme"); } catch (e) { /* private mode */ }
    if (!chosen) setTheme(ev.matches ? "dark" : "light", false);
  });

  function render() {
    imgs.forEach((img, i) => { img.style.transform = "rotate(" + turn[i] + "deg)"; });
    rings.forEach((ring, d) => {
      const g = D.discs[d];
      ring.style.display = (sel >> 1) === d ? "" : "none";
      ring.setAttribute("r", (sel & 1 ? g.front_r : g.back_r) + 0.6);
    });
    const S = D.langs[lang];
    $("status").textContent = S.app_selected + ": " + S.parts[sel];
  }

  // pointer position on disc d: distance (mm) and angle (degrees, ccw)
  function locate(d, ev) {
    const box = discs[d].getBoundingClientRect();
    const k = (2 * D.view_r) / box.width;
    const x = (ev.clientX - box.left - box.width / 2) * k;
    const y = -(ev.clientY - box.top - box.height / 2) * k;
    return { r: Math.hypot(x, y), a: Math.atan2(y, x) * 180 / Math.PI };
  }

  // index of the part of disc d under p, or -1 off the disc
  function hit(d, p) {
    const g = D.discs[d];
    if (p.r > g.back_r) return -1;
    if (p.r > g.front_r) return 2 * d;
    const a = p.a + turn[2 * d + 1];
    for (const [r0, r1, a0, a1] of g.windows) {
      if (p.r >= r0 && p.r <= r1 && mod(a - a0, 360) <= a1 - a0) return 2 * d;
    }
    return 2 * d + 1;
  }

  const snap = (part) => { turn[part] = Math.round(turn[part] / STEP) * STEP; };

  discs.forEach((el, d) => {
    el.addEventListener("pointerdown", (ev) => {
      const p = locate(d, ev);
      const part = hit(d, p);
      if (part < 0) return;
      ev.preventDefault();
      wheels.focus({ preventScroll: true });
      sel = part;
      drag = { d, part, a: p.a, id: ev.pointerId };
      el.setPointerCapture(ev.pointerId);
      el.classList.add("dragging");
      render();
    });
    el.addEventListener("pointermove", (ev) => {
      if (!drag || drag.id !== ev.pointerId) return;
      const p = locate(d, ev);
      turn[drag.part] -= mod(p.a - drag.a + 180, 360) - 180;
      drag.a = p.a;
      render();
    });
    const end = (ev) => {
      if (!drag || drag.id !== ev.pointerId) return;
      el.classList.remove("dragging");
      snap(drag.part);
      drag = null;
      render();
    };
    el.addEventListener("pointerup", end);
    el.addEventListener("pointercancel", end);
    el.addEventListener("wheel", (ev) => {
      const part = hit(d, locate(d, ev));
      if (part < 0) return;
      ev.preventDefault();
      sel = part;
      snap(part);
      turn[part] += ev.deltaY > 0 ? STEP : -STEP;
      render();
    }, { passive: false });
  });

  document.addEventListener("keydown", (ev) => {
    const at = document.activeElement;
    if (at && (at.tagName === "SELECT" || at.tagName === "BUTTON")) return;
    if (ev.key === "Tab" && at !== wheels) return;   // keep normal Tab outside the wheels
    switch (ev.key) {
      case "ArrowLeft": snap(sel); turn[sel] -= STEP; break;
      case "ArrowRight": snap(sel); turn[sel] += STEP; break;
      case "ArrowUp": sel = mod(sel - 1, 4); break;
      case "ArrowDown": sel = mod(sel + 1, 4); break;
      case "Tab": sel = mod(sel + (ev.shiftKey ? -1 : 1), 4); break;
      default: return;
    }
    ev.preventDefault();
    render();
  });

  const select = $("lang");
  for (const [code, name] of Object.entries(D.lang_names)) {
    if (D.langs[code]) select.add(new Option(name, code));
  }
  select.addEventListener("change", () => setLang(select.value));
  $("reset").addEventListener("click", () => { turn.fill(0); render(); });
  $("theme").addEventListener("click", () => setTheme(theme() === "dark" ? "light" : "dark"));

  window.setLang = setLang;          // for color_wheel.py --webview
  window.setTheme = setTheme;
  setLang(startLang());
})();
