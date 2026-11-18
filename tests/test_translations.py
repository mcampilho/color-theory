"""Every language has every text of every program, shaped like the English one.

The English table is the reference. For each other language the tests check the same
keys, the same kind of value (text, list, tuple), the same number of items in lists, and
the same % placeholders (%d, %s) in every text, because the programs fill those in.
"""
import re

import pytest

import color_theory_document as doc
import color_wheel as wheel
import i18n
import patterns
import tilings
import wallpapers

# %d, %s, %.1f, %(name)s and %%; no flags, so "100 % drucken" is not read as "% d"
PLACEHOLDER = re.compile(r"%(?:\([^)]*\))?\d*(?:\.\d+)?[sdif]|%%")

# program name -> its table {lang: {key: text}}
PROGRAMS = {
    "color_theory_document": doc.STRINGS,
    "color_wheel": wheel.STRINGS,
    "tilings": tilings.STRINGS,
    "patterns": patterns.STRINGS,
    "wallpapers": wallpapers.STRINGS,
}
LANG_CODES = [code for code, _ in i18n.LANGS]


def flatten(value, path=()):
    """Every text of a value with the path that leads to it, and the shape of lists."""
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, (list, tuple)):
        yield path + ("#len",), len(value)
        yield path + ("#type",), type(value).__name__
        for i, item in enumerate(value):
            yield from flatten(item, path + (i,))
    else:
        raise AssertionError("unexpected %s at %s" % (type(value).__name__, path))


def shape(table):
    return {k: dict(flatten(v)) for k, v in table.items()}


@pytest.mark.parametrize("program", PROGRAMS)
def test_every_language_is_present(program):
    missing = [code for code in LANG_CODES if code not in PROGRAMS[program]]
    assert not missing, "%s has no texts for %s" % (program, missing)


@pytest.mark.parametrize("lang", LANG_CODES)
@pytest.mark.parametrize("program", PROGRAMS)
def test_same_keys_and_shape_as_english(program, lang):
    table = PROGRAMS[program]
    if lang == "en" or lang not in table:
        pytest.skip("reference or missing (reported by test_every_language_is_present)")
    en, other = shape(table["en"]), shape(table[lang])
    assert not set(en) - set(other), "missing keys in %s/%s: %s" % (program, lang, sorted(set(en) - set(other))[:8])
    assert not set(other) - set(en), "extra keys in %s/%s: %s" % (program, lang, sorted(set(other) - set(en))[:8])
    for key, parts in en.items():
        got = other[key]
        assert set(parts) == set(got), "%s/%s/%s: lists differ in length or nesting" % (program, lang, key)
        for path, ref in parts.items():
            if path and path[-1] == "#len":
                assert got[path] == ref, "%s/%s/%s: %s items instead of %s" % (program, lang, key, got[path], ref)
            elif path and path[-1] == "#type":
                assert got[path] == ref, "%s/%s/%s: %s instead of %s" % (program, lang, key, got[path], ref)


@pytest.mark.parametrize("lang", LANG_CODES)
@pytest.mark.parametrize("program", PROGRAMS)
def test_same_placeholders_as_english(program, lang):
    table = PROGRAMS[program]
    if lang == "en" or lang not in table:
        pytest.skip("reference or missing")
    en = shape(table["en"])
    other = shape(table[lang])
    for key, parts in en.items():
        for path, ref in parts.items():
            if isinstance(ref, str) and ref not in ("list", "tuple"):
                want = sorted(PLACEHOLDER.findall(ref))
                have = sorted(PLACEHOLDER.findall(other[key][path]))
                if key == "page" and want == [] and have == ["%d"]:
                    continue    # catalogue page label where the number goes inside: "第 %d 页"
                assert have == want, "%s/%s/%s%s: placeholders %s instead of %s" % (
                    program, lang, key, list(path), have, want)


@pytest.mark.parametrize("program", PROGRAMS)
def test_no_empty_texts(program):
    for lang, table in PROGRAMS[program].items():
        for key, value in shape(table).items():
            for path, text in value.items():
                if isinstance(text, str) and path[-1:] not in (("#type",),):
                    assert text.strip() or path == (), "%s/%s/%s is empty" % (program, lang, key)


def test_programs_offer_every_language():
    assert doc.POSTER_LANGS == LANG_CODES
    assert wheel.languages() == LANG_CODES
    assert tilings.catalogue_langs() == LANG_CODES
