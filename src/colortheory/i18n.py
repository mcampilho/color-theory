"""
i18n.py
-------
Languages and fonts shared by every program of the project.

Texts live in a STRINGS table per program ({lang: {key: text}}); a key missing
in a language falls back to English. The programs draw with three font names
that never change, REG, BOLD and ITAL; use_lang(lang) points them at a font
that has the letters of that language:

  - Western European languages: Helvetica (built into every PDF reader);
  - Polish, Turkish, Russian: Arial (or DejaVu / Liberation Sans);
  - Arabic: Arial, upright also for italic (or Tahoma / Noto Sans Arabic);
  - Chinese: Microsoft YaHei; Japanese: Yu Gothic; Korean: Malgun Gothic
    (or the other CJK fonts listed in FONT_FILES).

The same font files serve the pictures drawn with Pillow (font_file), and
css_family gives the fonts a web page should ask for.
"""
import os
import sys

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# code, name in its own language; the order of the language boxes
LANGS = [
    ("en", "English"),
    ("pt", "Português (Portugal)"),
    ("pt-BR", "Português (Brasil)"),
    ("es", "Español"),
    ("fr", "Français"),
    ("it", "Italiano"),
    ("de", "Deutsch"),
    ("nl", "Nederlands"),
    ("pl", "Polski"),
    ("tr", "Türkçe"),
    ("ru", "Русский"),
    ("ar", "العربية"),
    ("zh", "简体中文"),
    ("ja", "日本語"),
    ("ko", "한국어"),
]
LANG_NAMES = dict(LANGS)
RTL = {"ar"}

REG, BOLD, ITAL = "Sans", "Sans-Bold", "Sans-Oblique"

# the script of each language decides its font
SCRIPT = {"pl": "ext", "tr": "ext", "ru": "ext", "ar": "arab", "zh": "zh", "ja": "ja", "ko": "ko"}

# candidate files for (regular, bold, italic); the first one found is used
FONT_FILES = {
    "ext": (["arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf", "Arial.ttf"],
            ["arialbd.ttf", "DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "Arial Bold.ttf"],
            ["ariali.ttf", "DejaVuSans-Oblique.ttf", "LiberationSans-Italic.ttf", "Arial Italic.ttf"]),
    # Arabic has no italic: the italic name gets the upright letters
    "arab": (["arial.ttf", "tahoma.ttf", "DejaVuSans.ttf", "NotoSansArabic-Regular.ttf"],
             ["arialbd.ttf", "tahomabd.ttf", "DejaVuSans-Bold.ttf", "NotoSansArabic-Bold.ttf"],
             ["arial.ttf", "tahoma.ttf", "DejaVuSans.ttf", "NotoSansArabic-Regular.ttf"]),
    "zh": (["msyh.ttc", "simhei.ttf", "wqy-microhei.ttc", "Arial Unicode.ttf"],
           ["msyhbd.ttc", "simhei.ttf", "wqy-microhei.ttc", "Arial Unicode.ttf"],
           ["msyh.ttc", "simhei.ttf", "wqy-microhei.ttc", "Arial Unicode.ttf"]),
    "ja": (["YuGothM.ttc", "meiryo.ttc", "msgothic.ttc", "Arial Unicode.ttf"],
           ["YuGothB.ttc", "meiryob.ttc", "msgothic.ttc", "Arial Unicode.ttf"],
           ["YuGothM.ttc", "meiryo.ttc", "msgothic.ttc", "Arial Unicode.ttf"]),
    "ko": (["malgun.ttf", "gulim.ttc", "NanumGothic.ttf", "Arial Unicode.ttf"],
           ["malgunbd.ttf", "gulim.ttc", "NanumGothicBold.ttf", "Arial Unicode.ttf"],
           ["malgun.ttf", "gulim.ttc", "NanumGothic.ttf", "Arial Unicode.ttf"]),
    # Helvetica itself is not a file: these are close to it, for the pictures
    "latin": (["arial.ttf", "LiberationSans-Regular.ttf", "Arial.ttf", "DejaVuSans.ttf"],
              ["arialbd.ttf", "LiberationSans-Bold.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf"],
              ["ariali.ttf", "LiberationSans-Italic.ttf", "Arial Italic.ttf", "DejaVuSans-Oblique.ttf"]),
}
CSS = {
    "latin": "Helvetica, Arial, 'Liberation Sans', sans-serif",
    "ext": "Arial, 'DejaVu Sans', 'Liberation Sans', sans-serif",
    "arab": "Arial, Tahoma, 'Noto Sans Arabic', 'DejaVu Sans', sans-serif",
    "zh": "'Microsoft YaHei', 'PingFang SC', 'Noto Sans SC', 'Source Han Sans SC', sans-serif",
    "ja": "'Yu Gothic', 'Hiragino Sans', Meiryo, 'Noto Sans JP', sans-serif",
    "ko": "'Malgun Gothic', 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif",
}
FONT_DIRS = [os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
             os.path.expanduser(r"~\AppData\Local\Microsoft\Windows\Fonts"),
             "/usr/share/fonts", "/usr/local/share/fonts", os.path.expanduser("~/.fonts"),
             "/Library/Fonts", "/System/Library/Fonts", os.path.expanduser("~/Library/Fonts")]

_LANG = None
_found = {}


def script(lang):
    return SCRIPT.get(lang, "latin")


def _find(name):
    if name not in _found:
        _found[name] = None
        for d in FONT_DIRS:
            if not os.path.isdir(d):
                continue
            p = os.path.join(d, name)
            if os.path.isfile(p):
                _found[name] = p
                break
            for root, _, files in os.walk(d):           # Linux keeps fonts in subfolders
                if name in files:
                    _found[name] = os.path.join(root, name)
                    break
            if _found[name]:
                break
    return _found[name]


def font_file(lang, style=0):
    """Path of the font file for lang (style 0 regular, 1 bold, 2 italic), or None."""
    for name in FONT_FILES[script(lang)][style]:
        p = _find(name)
        if p:
            return p
    return None


def css_family(lang):
    return CSS[script(lang)]


def use_lang(lang):
    """Point REG, BOLD and ITAL at fonts that have the letters of lang."""
    global _LANG
    if lang == _LANG:
        return
    s = script(lang)
    for name in (REG, BOLD, ITAL):          # registerFont keeps a TrueType name already taken
        pdfmetrics._fonts.pop(name, None)
    if s == "latin":
        for name, face in ((REG, "Helvetica"), (BOLD, "Helvetica-Bold"), (ITAL, "Helvetica-Oblique")):
            pdfmetrics.registerFont(pdfmetrics.Font(name, face, "WinAnsiEncoding"))
    else:
        for style, name in enumerate((REG, BOLD, ITAL)):
            path = font_file(lang, style)
            if not path:
                sys.exit("No font with the letters of %r was found; install one of: %s"
                         % (lang, ", ".join(FONT_FILES[s][style])))
            pdfmetrics.registerFont(TTFont(name, path, subfontIndex=0))
    _LANG = lang


def current():
    return _LANG


# --------------------------------------------------------------------------
# Line breaking. Chinese and Japanese are written without spaces: a line may
# break between any two characters, except before closing punctuation and
# after opening punctuation; runs of Latin letters and digits stay whole.
# --------------------------------------------------------------------------
_CLOSE = set("、。，．：；！？）」』】〉》〕”’・ー々…%％")
_OPEN = set("（「『【〈《〔“‘")


def _wide(ch):
    o = ord(ch)
    return (0x2E80 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF or 0xFF00 <= o <= 0xFFEF
            or 0x3000 <= o <= 0x303F)


def words(text):
    """The units of text a line may break between, as (separator, unit): the
    separator (" " or "") goes before the unit when both are on one line."""
    out = []
    for part in text.split(" "):
        if not part:
            continue
        raw, run = [], ""
        for ch in part:                         # wide characters one by one, other runs whole
            if _wide(ch):
                if run:
                    raw.append(run)
                    run = ""
                raw.append(ch)
            else:
                run += ch
        if run:
            raw.append(run)
        units = []
        for u in raw:
            if units and (u[0] in _CLOSE or units[-1][-1] in _OPEN):
                units[-1] += u                  # no break before closing or after opening marks
            else:
                units.append(u)
        for k, u in enumerate(units):
            out.append((" " if out and k == 0 else "", u))
    return out


def wrap(text, font, size, width):
    """Lines of text no wider than width (pt) in font at size; long units overflow."""
    lines = []
    for para in text.split("\n"):
        line = ""
        for sep, unit in words(para):
            trial = line + sep + unit if line else unit
            if line and pdfmetrics.stringWidth(visual(trial), font, size) > width:
                lines.append(line)
                line = unit
            else:
                line = trial
        lines.append(line)
    return lines


# --------------------------------------------------------------------------
# Right-to-left text. Arabic letters change shape with their neighbours and
# lines run from right to left, but a PDF (and Pillow without raqm) draws the
# characters as given, left to right. visual() joins the letters into their
# contextual forms (arabic-reshaper) and puts them in display order
# (python-bidi); the canvas methods below call it, so the programs keep
# drawing logical text. Text must go through visual() exactly once: code that
# draws letter by letter (text on an arc) iterates over visual(text) and draws
# the single letters, which visual() leaves alone.
# --------------------------------------------------------------------------
def _has_rtl(text):
    return any("֐" <= ch <= "ࣿ" or "יִ" <= ch <= "ﻼ" for ch in text)


def rtl(lang=None):
    """True when lang (by default the current language) is written right to left."""
    return (lang or _LANG) in RTL


def visual(text):
    """text in display order with joined letters, for a right-to-left language."""
    if not rtl() or not text or not _has_rtl(text):
        return text
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
    except ImportError:
        sys.exit("Arabic text needs: pip install arabic-reshaper python-bidi")
    return "\n".join(get_display(arabic_reshaper.reshape(ln), base_dir="R")
                     for ln in text.split("\n"))


def line_x(x, width):
    """Where a line of a paragraph starts that spans x..x+width: its left edge in
    left-to-right languages; draw it with draw_line, which aligns it right in
    right-to-left ones."""
    return x + width if rtl() else x


def draw_line(c, x, y, text, width):
    """One line of a paragraph in the box x..x+width (aligned to the start side)."""
    if rtl():
        c.drawRightString(x + width, y, text)
    else:
        c.drawString(x, y, text)


def _patch_canvas():
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.pdfgen.textobject import PDFTextObject
    for cls, names in ((Canvas, ("drawString", "drawCentredString", "drawRightString")),
                       (PDFTextObject, ("textOut", "textLine"))):
        for name in names:
            orig = getattr(cls, name)
            if getattr(orig, "_rtl", False):
                continue
            if cls is Canvas:                   # these draw through a text object: shape once
                def wrapped(self, x, y, text, *a, _orig=orig, **k):
                    self._rtl_busy = True
                    try:
                        return _orig(self, x, y, visual(text), *a, **k)
                    finally:
                        self._rtl_busy = False
            else:
                def wrapped(self, text="", *a, _orig=orig, **k):
                    if not getattr(self._canvas, "_rtl_busy", False):
                        text = visual(text)
                    return _orig(self, text, *a, **k)
            wrapped._rtl = True
            setattr(cls, name, wrapped)


_patch_canvas()


def pil_font(path, size, lang=None):
    """A Pillow font for text that already went through visual() (no second reordering)."""
    from PIL import ImageFont
    if rtl(lang):
        return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.BASIC)
    return ImageFont.truetype(path, size)


def svg_bidi(lang=None):
    """Attributes for an SVG <text> holding visual() text, so the browser keeps its order."""
    return ' direction="ltr" unicode-bidi="bidi-override"' if rtl(lang) else ""


def fallback(table, lang):
    """The texts of lang, with English for any key it lacks."""
    out = dict(table["en"])
    out.update(table.get(lang, {}))
    return out


use_lang("en")
