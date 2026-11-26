"""The colour illusions document: texts, links, the colours the figures claim to share, and output."""
import re
import xml.dom.minidom

import pytest

from colortheory import illusion_figures as F
from colortheory import i18n, illusions
from colortheory.illusion_links import LINKS
from test_generate import need_font, pdf_pages, run

KEYS = [entry[1] for entry in illusions.ILLUSIONS]


def test_languages():
    assert [code for code, _ in i18n.LANGS] == illusions.LANGS


@pytest.mark.parametrize("lang", illusions.LANGS)
def test_texts_are_complete(lang):
    table = illusions.STRINGS[lang]
    assert set(table) == set(illusions.STRINGS["en"])
    assert set(table["illusions"]) == set(KEYS)
    for texts in table["illusions"].values():
        assert len(texts) == 4 and all(t.strip() for t in texts)
    assert all("cat_" + c in table for c in illusions.CATEGORIES)


def test_every_illusion_has_a_category_and_an_article():
    assert len(KEYS) == len(set(KEYS))
    for category, _, article, *_ in illusions.ILLUSIONS:
        assert category in illusions.CATEGORIES
        assert article in LINKS


def test_wikipedia_links_fall_back_to_english():
    assert illusions.wiki("Penrose triangle", "pt") == (
        "https://pt.wikipedia.org/wiki/Tri%C3%A2ngulo_de_Penrose", True)
    assert illusions.wiki("Chromostereopsis", "pt") == ("https://en.wikipedia.org/wiki/Chromostereopsis", False)
    assert illusions.wiki("Penrose triangle", "pt-BR")[0].startswith("https://pt.")
    assert illusions.wiki("Mach bands", "en") == ("https://en.wikipedia.org/wiki/Mach_bands", True)


def test_checker_squares_a_and_b_are_the_same_grey():
    (ac, ar), (bc, br) = F.CHECKER_A, F.CHECKER_B
    assert (ac + ar) % 2 == 0 and (bc + br) % 2 == 1          # A is a dark square, B a light one
    assert F.checker_square(ac, ar) == pytest.approx(F.checker_square(bc, br), abs=1e-9)


def fills(figure):
    return [s[2] for s in figure.shapes]


def test_compared_patches_share_one_colour():
    assert fills(F.simultaneous_contrast()).count(F.SIMULTANEOUS_PATCH) == 4
    assert fills(F.color_constancy()).count(F.CONSTANCY_TARGET) == 2
    assert fills(F.white_illusion()).count(F.WHITE_GREY) == 8


@pytest.mark.parametrize("lang", ["en", "pt", "es", "ru", "ar", "zh"])
def test_document_is_written(tmp_path, lang):
    need_font(lang)                                           # e.g. no CJK font on the Linux runners
    out, md = tmp_path / "doc.pdf", tmp_path / "doc.md"
    run("illusions", "--lang", lang, "-o", str(out))
    assert pdf_pages(out) == 2 + len(KEYS)
    text = md.read_text(encoding="utf-8")
    images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    assert len(images) >= len(KEYS)
    for image in images:
        xml.dom.minidom.parse(str(tmp_path / image))          # exists and is well formed
    for anchor in re.findall(r"\]\(#(\w+)\)", text):
        assert '<a id="%s"></a>' % anchor in text
