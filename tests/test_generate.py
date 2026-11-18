"""Smoke tests: each program runs and writes a real file, in a few languages.

Languages with their own script need a font (see FONT_FILES in i18n.py); where it is
not installed those cases are skipped instead of failing.
"""
import subprocess
import sys

import pytest

import i18n
from conftest import ROOT

LATIN = ["en", "pt", "es"]
OWN_SCRIPT = ["ja", "ar"]


def run(*args, timeout=300):
    done = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    assert done.returncode == 0, done.stdout[-500:] + done.stderr[-1500:]
    return done


def pdf_pages(path):
    data = path.read_bytes()
    assert data.startswith(b"%PDF")
    return data.count(b"/Type /Page\n") + data.count(b"/Type /Page ") + data.count(b"/Type /Page>>")


def need_font(lang):
    if i18n.script(lang) != "latin" and not i18n.font_file(lang):
        pytest.skip("no font for %s installed" % lang)
    if lang in i18n.RTL:
        pytest.importorskip("arabic_reshaper")
        pytest.importorskip("bidi")


@pytest.mark.fonts
@pytest.mark.parametrize("lang", LATIN + OWN_SCRIPT)
def test_poster_pages(tmp_path, lang):
    need_font(lang)
    out = tmp_path / "poster.pdf"
    run("color_theory_document.py", "--lang", lang, "--pages", "1", "4", "-o", str(out))
    assert out.stat().st_size > 20_000
    assert pdf_pages(out) == 2


@pytest.mark.fonts
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_colour_wheels_pdf(tmp_path, lang):
    need_font(lang)
    out = tmp_path / "wheels.pdf"
    run("color_wheel.py", "--lang", lang, "-o", str(out))
    assert pdf_pages(out) == 6


def test_single_tiling_as_svg_and_png(tmp_path):
    svg, png = tmp_path / "hex.svg", tmp_path / "hex.png"
    run("tilings.py", "hexagonal", "-c", "7", "--scheme", "rainbow", "-o", str(svg))
    run("tilings.py", "hexagonal", "-o", str(png))
    assert "<svg" in svg.read_text(encoding="utf-8")[:300]
    assert png.read_bytes().startswith(b"\x89PNG")


def test_pattern_image(tmp_path):
    out = tmp_path / "tripods.png"
    run("patterns.py", "tripods", "-o", str(out))
    assert out.read_bytes().startswith(b"\x89PNG")


def test_wallpaper(tmp_path):
    pytest.importorskip("numpy")
    pytest.importorskip("scipy")
    out = tmp_path / "mesh.png"
    run("wallpapers.py", "mesh", "--size", "320x200", "-o", str(out))
    from PIL import Image
    with Image.open(out) as img:
        assert img.size == (320, 200)


def test_unknown_language_is_refused():
    done = subprocess.run([sys.executable, "tilings.py", "--lang", "xx"], cwd=ROOT,
                          capture_output=True, text=True, timeout=60)
    assert done.returncode != 0
