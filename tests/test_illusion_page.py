"""The interactive page: languages, every illusion present, a text for each help, and the layers."""
import json
import re
import xml.dom.minidom

import pytest

from colortheory import illusion_figures as F
from colortheory import illusion_page, illusions
from test_generate import run

KEYS = [entry[1] for entry in illusions.ILLUSIONS]


def page_data(text):
    return json.loads(re.search(r'<script type="application/json" id="data">(.*?)</script>', text, re.S).group(1))


def helped_keys():
    """Illusions whose figures have something to hide or show, plus the one with an animation."""
    return {illusion_page.ANIMATED} | {
        key for key, variants in illusion_page.figures() if any('class="t-' in svg for _, svg in variants)}


@pytest.mark.parametrize("lang", illusions.LANGS)
def test_interface_texts(lang):
    table = illusion_page.UI[lang]
    assert set(table) == set(illusion_page.UI["en"])
    assert set(table["aids"]) == helped_keys()
    assert all(p[0] in table for p in illusion_page.PALETTES)


def test_the_requested_illusions_have_help():
    assert {"checker", "ebbinghaus", "hering", "muller_lyer", "orbison", "poggendorff", "white",
            "wundt"} <= helped_keys()


def test_help_layers_stay_out_of_the_documents():
    plain, page = F.ebbinghaus().svg(), F.ebbinghaus().svg(page=True)
    assert "class=" not in plain
    assert page.count('class="t-aid"') == 2
    assert plain.count("<path") == page.count("<path") - 2


def test_figures_are_well_formed():
    for _, variants in illusion_page.figures():
        for _, svg in variants:
            xml.dom.minidom.parseString(svg)


def test_page_is_written(tmp_path):
    out = tmp_path / "page.html"
    run("illusion_page", "-o", str(out))
    text = out.read_text(encoding="utf-8")
    data = page_data(text)
    assert sorted(item["key"] for item in data["illusions"]) == sorted(KEYS)
    assert list(data["languages"]) == illusions.LANGS
    assert "__DATA__" not in text
    # self-contained: nothing is loaded from elsewhere
    assert not re.search(r'<(script|link|img)[^>]+(src|href)=', text)
