"""Interactive page of the colour illusions: one at a time, with other colours and with help.

    python3 -m colortheory.illusion_page                     # -> colour_illusions.html
    python3 -m colortheory.illusion_page -o docs/illusions/colour_illusions.html

One self-contained HTML file (no server, no external resources) with every language of the
illusions document. Figures and texts are the same as in the document; this module adds the
interface texts, the colour pairs and what each "help" does.
"""
import argparse
import json

from colortheory import i18n, illusions
from colortheory.locales.illusion_page import UI as _MORE

# keys whose second figure is another version of the illusion (the others are the proof, which
# the page shows through the help)
VARIANTS = {
    "white": ["White", "Munker–White"],
    "grid": ["Hermann", None],                                      # None: the "scintillating" label
}
ANIMATED = "lilac"                                                  # its help stops the animation
FIXED_COLOURS = ["lilac", "constancy"]                              # a colour pair would spoil them
LINE_ACCENT = ["hering", "wundt", "orbison"]                        # the red lines follow the pair

# id, replaces black, replaces white, colour of the help and of the highlighted lines
PALETTES = [
    ("original", "#000000", "#ffffff", "#d02028"),
    ("red_green", "#8e0f1e", "#8fe388", "#ffffff"),
    ("blue_orange", "#12328a", "#ffa53d", "#ffffff"),
    ("violet_yellow", "#471a86", "#ffe840", "#e0202a"),
    ("blue_yellow", "#10207a", "#fff27a", "#d02028"),
    ("equal_light", "#e0402f", "#009000", "#ffffff"),               # red and green of similar luminance
]

UI = {
    "en": {
        "language": "Language", "illusion": "Illusion", "previous": "Previous", "next": "Next",
        "version": "Version", "scintillating": "Scintillating", "colours": "Colour pair",
        "dark": "Instead of black", "light": "Instead of white", "colour": "Colour",
        "hue": "Rotate hue", "reset": "Original colours", "help": "Show help", "unhelp": "Hide help",
        "fixed": "This illusion depends on its own colours: use the hue slider.",
        "note": "Greys become mixtures of the two colours, so areas that were equal stay equal. Many "
                "illusions weaken when both colours are equally light.",
        "original": "Original", "red_green": "Red / green", "blue_orange": "Blue / orange",
        "violet_yellow": "Violet / yellow", "blue_yellow": "Blue / yellow",
        "equal_light": "Red / green, equal lightness", "custom": "Custom",
        # "what you see" where the document points to a figure the page does not show
        "see": {
            "checker": "Square A looks much darker than square B. They are exactly the same grey: turn on the help to see it.",
            "muller_lyer": "The line with outward fins looks longer than the one with inward fins. Both are equal.",
            "poggendorff": "The black line entering the grey block on the left seems to come out as the blue line. It comes out as the upper black one: turn on the help to see it.",
        },
        "aids": {
            "contrast": "The four surrounds are removed.",
            "bezold": "The stripes are removed.",
            "constancy": "Everything but the two compared tiles is removed.",
            "lilac": "The animation stops.",
            "checker": "A strip of one colour joins squares A and B.",
            "white": "The stripes are removed.",
            "mach": "Gaps separate the bands, and each one looks uniform.",
            "cornsweet": "The edge between the two halves is covered.",
            "ehrenstein": "The lines are completed, and the discs vanish.",
            "irradiation": "Guide lines compare the sides of the squares.",
            "ebbinghaus": "Two parallel lines touch both central circles.",
            "muller_lyer": "The fins are removed and the lengths compared.",
            "ponzo": "The railway is removed.",
            "cafe": "Straight lines are drawn along the mortar.",
            "fraser": "Perfect circles are drawn over the figure.",
            "hering": "The background lines are removed.",
            "wundt": "The background lines are removed.",
            "orbison": "The background rings are removed.",
            "zollner": "The short strokes are removed.",
            "poggendorff": "The hidden part of the line is shown.",
            "tilt": "The surrounding gratings are removed.",
        },
    },
    "pt": {
        "language": "Língua", "illusion": "Ilusão", "previous": "Anterior", "next": "Seguinte",
        "version": "Versão", "scintillating": "Cintilante", "colours": "Par de cores",
        "dark": "Em vez do preto", "light": "Em vez do branco", "colour": "Cor",
        "hue": "Rodar o matiz", "reset": "Cores originais", "help": "Mostrar ajuda", "unhelp": "Esconder ajuda",
        "fixed": "Esta ilusão depende das suas próprias cores: use o controlo do matiz.",
        "note": "Os cinzentos passam a misturas das duas cores, por isso áreas iguais continuam iguais. "
                "Muitas ilusões enfraquecem quando as duas cores são igualmente claras.",
        "original": "Original", "red_green": "Vermelho / verde", "blue_orange": "Azul / laranja",
        "violet_yellow": "Violeta / amarelo", "blue_yellow": "Azul / amarelo",
        "equal_light": "Vermelho / verde, igual luminosidade", "custom": "Personalizado",
        # "what you see" where the document points to a figure the page does not show
        "see": {
            "checker": "O quadrado A parece muito mais escuro do que o B. São exatamente do mesmo cinzento: ligue a ajuda para o ver.",
            "muller_lyer": "A linha com as aletas para fora parece mais comprida do que a das aletas para dentro. São iguais.",
            "poggendorff": "A linha preta que entra no bloco cinzento pela esquerda parece sair como linha azul. Sai como a preta de cima: ligue a ajuda para o ver.",
        },
        "aids": {
            "contrast": "Os quatro fundos são retirados.",
            "bezold": "As riscas são retiradas.",
            "constancy": "Retira-se tudo menos os dois mosaicos comparados.",
            "lilac": "A animação para.",
            "checker": "Uma faixa de uma só cor liga os quadrados A e B.",
            "white": "As riscas são retiradas.",
            "mach": "Intervalos separam as faixas, e cada uma parece uniforme.",
            "cornsweet": "Tapa-se a fronteira entre as duas metades.",
            "ehrenstein": "As linhas são completadas, e os discos desaparecem.",
            "irradiation": "Linhas-guia comparam os lados dos quadrados.",
            "ebbinghaus": "Duas linhas paralelas tocam nos dois círculos centrais.",
            "muller_lyer": "Retiram-se as setas e comparam-se os comprimentos.",
            "ponzo": "A linha de comboio é retirada.",
            "cafe": "Traçam-se retas sobre a argamassa.",
            "fraser": "Desenham-se círculos perfeitos sobre a figura.",
            "hering": "As linhas de fundo são retiradas.",
            "wundt": "As linhas de fundo são retiradas.",
            "orbison": "Os anéis de fundo são retirados.",
            "zollner": "Os traços curtos são retirados.",
            "poggendorff": "Mostra-se a parte escondida da linha.",
            "tilt": "As grelhas à volta são retiradas.",
        },
    },
    "es": {
        "language": "Idioma", "illusion": "Ilusión", "previous": "Anterior", "next": "Siguiente",
        "version": "Versión", "scintillating": "Centelleante", "colours": "Par de colores",
        "dark": "En lugar del negro", "light": "En lugar del blanco", "colour": "Color",
        "hue": "Girar el tono", "reset": "Colores originales", "help": "Mostrar ayuda", "unhelp": "Ocultar ayuda",
        "fixed": "Esta ilusión depende de sus propios colores: use el control del tono.",
        "note": "Los grises pasan a ser mezclas de los dos colores, así que las zonas iguales siguen iguales. "
                "Muchas ilusiones se debilitan cuando los dos colores son igual de claros.",
        "original": "Original", "red_green": "Rojo / verde", "blue_orange": "Azul / naranja",
        "violet_yellow": "Violeta / amarillo", "blue_yellow": "Azul / amarillo",
        "equal_light": "Rojo / verde, igual luminosidad", "custom": "Personalizado",
        # "what you see" where the document points to a figure the page does not show
        "see": {
            "checker": "El cuadrado A parece mucho más oscuro que el B. Son exactamente del mismo gris: active la ayuda para verlo.",
            "muller_lyer": "La línea con las aletas hacia fuera parece más larga que la de las aletas hacia dentro. Son iguales.",
            "poggendorff": "La línea negra que entra por la izquierda en el bloque gris parece salir como línea azul. Sale como la negra de arriba: active la ayuda para verlo.",
        },
        "aids": {
            "contrast": "Se quitan los cuatro fondos.",
            "bezold": "Se quitan las franjas.",
            "constancy": "Se quita todo menos las dos baldosas comparadas.",
            "lilac": "La animación se detiene.",
            "checker": "Una banda de un solo color une las casillas A y B.",
            "white": "Se quitan las franjas.",
            "mach": "Unos huecos separan las bandas, y cada una parece uniforme.",
            "cornsweet": "Se tapa el borde entre las dos mitades.",
            "ehrenstein": "Las líneas se completan, y los discos desaparecen.",
            "irradiation": "Unas líneas guía comparan los lados de los cuadrados.",
            "ebbinghaus": "Dos líneas paralelas tocan los dos círculos centrales.",
            "muller_lyer": "Se quitan las puntas y se comparan las longitudes.",
            "ponzo": "Se quita la vía del tren.",
            "cafe": "Se trazan rectas sobre el mortero.",
            "fraser": "Se dibujan círculos perfectos sobre la figura.",
            "hering": "Se quitan las líneas del fondo.",
            "wundt": "Se quitan las líneas del fondo.",
            "orbison": "Se quitan los anillos del fondo.",
            "zollner": "Se quitan los trazos cortos.",
            "poggendorff": "Se muestra la parte oculta de la línea.",
            "tilt": "Se quitan las rejillas de alrededor.",
        },
    },
}

UI.update(_MORE)


def figures():
    """(key, [(variant label, SVG with all layers)]) in the order of the document."""
    for category in illusions.CATEGORIES:
        for cat, key, _, figure, second in illusions.ILLUSIONS:
            if cat != category:
                continue
            if key in VARIANTS:
                first, other = VARIANTS[key]
                yield key, [(first, figure().svg(page=True)), (other, second().svg(page=True))]
            else:
                yield key, [(None, figure().svg(page=True))]


def data():
    """Everything the page needs, as JSON-ready values."""
    entries = {entry[1]: entry for entry in illusions.ILLUSIONS}
    out = {"categories": illusions.CATEGORIES, "palettes": PALETTES, "animated": ANIMATED,
           "fixed": FIXED_COLOURS, "lineAccent": LINE_ACCENT,
           "illusions": [{"key": key, "category": entries[key][0], "variants": variants}
                         for key, variants in figures()],
           "languages": {}}
    for lang in illusions.LANGS:
        table = illusions.STRINGS[lang]
        out["languages"][lang] = {
            "ui": UI[lang],
            "name": i18n.LANG_NAMES[lang],
            "rtl": i18n.rtl(lang),
            "font": i18n.css_family(lang),
            "title": table["title"],
            "subtitle": table["subtitle"],
            "headings": [table["see"], table["why"], table["try"]],
            "categories": {c: table["cat_" + c] for c in illusions.CATEGORIES},
            "texts": table["illusions"],
            "links": {key: illusions.wiki(entry[2], lang) for key, entry in entries.items()},
            "wiki": table["wiki"],
            "inEnglish": table["in_english"],
        }
    return out


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Colour Illusions</title>
<style>
  :root { --page: #e9e9ea; --card: #fafafa; --ink: #202024; --soft: #606068; --line: #c9c9ce; --link: #1c54ad; }
  @media (prefers-color-scheme: dark) {
    :root { --page: #232326; --card: #2e2e32; --ink: #ececee; --soft: #a8a8b0; --line: #4a4a50; --link: #8ab4f8; }
  }
  * { box-sizing: border-box; }
  body { margin: 0; padding: 16px; background: var(--page); color: var(--ink);
         font: 15px/1.45 system-ui, "Segoe UI", sans-serif; }
  main { max-width: 860px; margin: 0 auto; }
  h1 { margin: 0; font-size: 26px; }
  h2 { margin: 14px 0 8px; font-size: 20px; }
  h3 { margin: 12px 0 2px; font-size: 15px; color: var(--link); }
  p { margin: 0; }
  a { color: var(--link); }
  .soft { color: var(--soft); }
  .row { display: flex; flex-wrap: wrap; gap: 8px 14px; align-items: end; margin-top: 10px; }
  label { display: flex; flex-direction: column; gap: 2px; font-size: 12px; color: var(--soft); }
  select, button, input { font: inherit; color: var(--ink); background: var(--card);
                          border: 1px solid var(--line); border-radius: 6px; }
  select, button { height: 34px; padding: 0 10px; }
  button { cursor: pointer; }
  button[aria-pressed="true"] { background: var(--link); border-color: var(--link); color: var(--card); }
  button:disabled { opacity: .45; cursor: default; }
  input[type="color"] { width: 62px; height: 34px; padding: 2px 4px; }
  input[type="range"] { width: 180px; height: 34px; border: 0; background: none; }
  [hidden] { display: none !important; }
  #stage { direction: ltr; margin-top: 10px; background: var(--card); border: 1px solid var(--line); }
  #stage svg { display: block; width: 100%; height: auto; max-height: 72vh; }
  #stage .t-remove, #stage .t-aid, #stage .t-guide { transition: opacity .7s; }
  #stage .t-aid, #stage .t-guide { opacity: 0; }
  #stage.aided .t-aid, #stage.aided .t-guide { opacity: 1; }
  #stage.aided .t-remove { opacity: 0; }
</style>
</head>
<body>
<main>
  <h1 id="title"></h1>
  <p id="subtitle" class="soft"></p>
  <div class="row">
    <label><span data-ui="language"></span><select id="lang"></select></label>
    <label><span data-ui="illusion"></span><select id="illusion"></select></label>
    <button id="previous">&#9664;</button>
    <button id="next">&#9654;</button>
    <label id="variant-box"><span data-ui="version"></span><select id="variant"></select></label>
  </div>
  <div class="row">
    <label><span data-ui="colours"></span><select id="palette"></select></label>
    <label class="pair"><span data-ui="dark"></span><input type="color" id="dark"></label>
    <label class="pair"><span data-ui="light"></span><input type="color" id="light"></label>
    <span id="pickers" class="row"></span>
    <label><span data-ui="hue"></span><input type="range" id="hue" min="0" max="359" value="0"></label>
    <button id="reset" data-ui="reset"></button>
  </div>
  <h2 id="name"></h2>
  <div class="row">
    <button id="help" aria-pressed="false"></button>
    <p id="help-text" class="soft"></p>
  </div>
  <div id="stage"></div>
  <p id="note" class="soft"></p>
  <div id="texts"></div>
</main>
<script type="application/json" id="data">__DATA__</script>
<script>
"use strict";
const DATA = JSON.parse(document.getElementById("data").textContent);
const $ = id => document.getElementById(id);
const state = { lang: "en", index: 0, variant: 0, palette: "original", dark: "#000000", light: "#ffffff",
                accent: "#d02028", own: {}, hue: 0, aided: false };

// ---------------------------------------------------------------- colours
const rgb = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
const hex = c => "#" + c.map(v => Math.round(Math.max(0, Math.min(255, v))).toString(16).padStart(2, "0")).join("");
const isGrey = h => { const [r, g, b] = rgb(h); return r === g && g === b; };

function rotate(colour, degrees) {
  if (!degrees) return colour;
  const [r, g, b] = rgb(colour).map(v => v / 255);
  const max = Math.max(r, g, b), min = Math.min(r, g, b), d = max - min, l = (max + min) / 2;
  if (!d) return colour;
  const s = d / (1 - Math.abs(2 * l - 1));
  let h = max === r ? ((g - b) / d) % 6 : max === g ? (b - r) / d + 2 : (r - g) / d + 4;
  h = (h * 60 + degrees + 360) % 360;
  const f = n => {
    const k = (n + h / 30) % 12;
    return 255 * (l - s * Math.min(l, 1 - l) * Math.max(-1, Math.min(k - 3, 9 - k, 1)));
  };
  return hex([f(0), f(8), f(4)]);
}

const current = () => DATA.illusions[state.index];
const fixedColours = () => DATA.fixed.includes(current().key);
const followsAccent = el => el.matches(".t-aid, .t-guide") || DATA.lineAccent.includes(current().key);

// Colour of one element: greys are mixed from the pair, so equal greys stay equal.
function mapped(original, el) {
  const pair = !fixedColours();
  let colour = original;
  if (isGrey(original)) {
    if (pair) {
      const t = rgb(original)[0] / 255, a = rgb(state.dark), b = rgb(state.light);
      colour = hex(a.map((v, i) => v + (b[i] - v) * t));
    }
  } else if (state.own[original]) {
    colour = state.own[original];
  } else if (pair && state.palette !== "original" && followsAccent(el)) {
    colour = state.accent;
  }
  return rotate(colour, state.hue);
}

function paint() {
  for (const el of $("stage").querySelectorAll("[data-fill], [data-stroke]")) {
    for (const what of ["fill", "stroke"]) {
      if (el.dataset[what]) el.setAttribute(what, mapped(el.dataset[what], el));
    }
  }
}

// Colour pickers for the chromatic colours of the figure, when there are only a few.
function pickers() {
  const found = new Map();
  for (const el of $("stage").querySelectorAll("[data-fill], [data-stroke]")) {
    if (el.matches(".t-aid, .t-guide")) continue;
    for (const c of [el.dataset.fill, el.dataset.stroke]) {
      if (c && !isGrey(c) && !found.has(c)) found.set(c, el);
    }
  }
  const box = $("pickers");
  box.replaceChildren();
  if (found.size > 4) return;
  const ui = DATA.languages[state.lang].ui;
  let n = 0;
  for (const [original, el] of found) {
    const label = document.createElement("label"), input = document.createElement("input");
    label.textContent = ui.colour + " " + (++n);
    input.type = "color";
    const hue = state.hue;
    state.hue = 0;
    input.value = mapped(original, el);
    state.hue = hue;
    input.addEventListener("input", () => { state.own[original] = input.value; paint(); });
    label.append(input);
    box.append(label);
  }
}

// ---------------------------------------------------------------- page
function option(value, text) {
  const o = document.createElement("option");
  o.value = value;
  o.textContent = text;
  return o;
}

function figure() {
  const stage = $("stage");
  stage.innerHTML = current().variants[state.variant][1];
  const svg = stage.querySelector("svg");
  svg.removeAttribute("width");
  svg.removeAttribute("height");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", DATA.languages[state.lang].texts[current().key][0]);
  for (const el of svg.querySelectorAll("path, circle, text")) {
    for (const what of ["fill", "stroke"]) {
      const c = el.getAttribute(what);
      if (c && c !== "none") el.dataset[what] = c;
    }
  }
  paint();
  pickers();
  help();
}

function help() {
  const key = current().key, ui = DATA.languages[state.lang].ui, text = ui.aids[key];
  if (!text) state.aided = false;
  $("help").hidden = $("help-text").hidden = !text;
  $("help").textContent = state.aided ? ui.unhelp : ui.help;
  $("help").setAttribute("aria-pressed", state.aided);
  $("help-text").textContent = text || "";
  $("stage").classList.toggle("aided", state.aided);
  const svg = $("stage").querySelector("svg");
  if (key === DATA.animated) state.aided ? svg.pauseAnimations() : svg.unpauseAnimations();
}

function controls() {
  const fixed = fixedColours(), ui = DATA.languages[state.lang].ui;
  $("palette").value = state.palette;
  $("palette").disabled = $("dark").disabled = $("light").disabled = fixed;
  $("dark").value = state.dark;
  $("light").value = state.light;
  $("hue").value = state.hue;
  $("note").textContent = fixed ? ui.fixed : state.palette === "original" ? "" : ui.note;
}

function show() {
  const L = DATA.languages[state.lang], ui = L.ui, item = current(), texts = L.texts[item.key];
  document.documentElement.lang = state.lang;
  document.documentElement.dir = L.rtl ? "rtl" : "ltr";
  document.body.style.fontFamily = L.font;
  $("previous").textContent = L.rtl ? "\u25B6" : "\u25C0";
  $("next").textContent = L.rtl ? "\u25C0" : "\u25B6";
  document.title = L.title + " – " + texts[0];
  $("title").textContent = L.title;
  $("subtitle").textContent = L.subtitle;
  for (const el of document.querySelectorAll("[data-ui]")) el.textContent = ui[el.dataset.ui];
  $("previous").title = ui.previous;
  $("next").title = ui.next;
  $("previous").setAttribute("aria-label", ui.previous);
  $("next").setAttribute("aria-label", ui.next);

  $("illusion").replaceChildren(...DATA.categories.map(category => {
    const group = document.createElement("optgroup");
    group.label = L.categories[category];
    DATA.illusions.forEach((it, i) => {
      if (it.category === category) group.append(option(i, L.texts[it.key][0]));
    });
    return group;
  }));
  $("illusion").value = state.index;

  $("variant-box").hidden = item.variants.length < 2;
  $("variant").replaceChildren(...item.variants.map((v, i) => option(i, v[0] || ui.scintillating)));
  $("variant").value = state.variant;

  $("palette").replaceChildren(...DATA.palettes.map(p => option(p[0], ui[p[0]])), option("custom", ui.custom));

  $("name").textContent = texts[0];
  const blocks = [];
  L.headings.forEach((heading, i) => {
    const h = document.createElement("h3"), p = document.createElement("p");
    h.textContent = heading;
    p.textContent = (i === 0 && ui.see[item.key]) || texts[i + 1];
    blocks.push(h, p);
  });
  const [url, own] = L.links[item.key], more = document.createElement("p"), a = document.createElement("a");
  a.href = url;
  a.target = "_blank";
  a.rel = "noopener";
  a.textContent = L.wiki + (own ? "" : " (" + L.inEnglish + ")");
  more.append(a);
  more.style.marginTop = "12px";
  blocks.push(more);
  $("texts").replaceChildren(...blocks);

  controls();
  figure();
}

function go(index) {
  const n = DATA.illusions.length;
  Object.assign(state, { index: (index + n) % n, variant: 0, own: {}, hue: 0, aided: false });
  history.replaceState(null, "", "#" + current().key);  // keeps ?lang=
  show();
}

function choosePalette(id) {
  const p = DATA.palettes.find(q => q[0] === id);
  state.palette = id;
  if (p) [, state.dark, state.light, state.accent] = p;
  state.own = {};
  controls();
  paint();
  pickers();
}

$("lang").addEventListener("change", e => {
  state.lang = e.target.value;
  history.replaceState(null, "", "?lang=" + state.lang + "#" + current().key);
  show();
});
$("illusion").addEventListener("change", e => go(Number(e.target.value)));
$("previous").addEventListener("click", () => go(state.index - 1));
$("next").addEventListener("click", () => go(state.index + 1));
$("variant").addEventListener("change", e => {
  state.variant = Number(e.target.value);
  state.own = {};
  figure();
});
$("palette").addEventListener("change", e => choosePalette(e.target.value));
for (const id of ["dark", "light"]) {
  $(id).addEventListener("input", e => {
    state[id] = e.target.value;
    state.palette = "custom";
    controls();
    paint();
  });
}
$("hue").addEventListener("input", e => { state.hue = Number(e.target.value); paint(); });
$("reset").addEventListener("click", () => { state.hue = 0; choosePalette("original"); });
$("help").addEventListener("click", () => { state.aided = !state.aided; help(); });

$("lang").append(...Object.keys(DATA.languages).map(code => option(code, DATA.languages[code].name)));
// ?lang=xx in the address, else the browser's language (pt-BR before pt)
const asked = new URLSearchParams(location.search).get("lang") || navigator.language || "en";
state.lang = [asked, asked.slice(0, 2)].find(code => DATA.languages[code]) || "en";
$("lang").value = state.lang;
const wanted = DATA.illusions.findIndex(it => "#" + it.key === location.hash);
state.index = Math.max(0, wanted);
show();
</script>
</body>
</html>
"""


def html():
    # "</" must not appear inside the <script> that holds the data
    payload = json.dumps(data(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return TEMPLATE.replace("__DATA__", payload)


def write_html(path):
    with open(path, "w", encoding="utf-8", newline="\n") as out:
        out.write(html())


def main():
    ap = argparse.ArgumentParser(description="Colour illusions: an interactive HTML page")
    ap.add_argument("-o", "--out", default="colour_illusions.html", help="output HTML path")
    a = ap.parse_args()
    write_html(a.out)
    print("Saved", a.out)


if __name__ == "__main__":
    main()
