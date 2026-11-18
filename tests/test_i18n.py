"""Languages, line breaking and right-to-left text (i18n.py)."""
import pytest

import i18n


def test_fifteen_languages():
    codes = [code for code, _ in i18n.LANGS]
    assert len(codes) == len(set(codes)) == 15
    assert set(codes) >= {"en", "pt", "es", "pt-BR", "ar", "zh", "ja", "ko"}
    assert all(name for _, name in i18n.LANGS)
    assert sorted(i18n.RTL) == ["ar"]


def test_fallback_uses_english_for_missing_texts():
    table = {"en": {"a": "one", "b": "two"}, "pt": {"a": "um"}}
    assert i18n.fallback(table, "pt") == {"a": "um", "b": "two"}
    assert i18n.fallback(table, "es") == {"a": "one", "b": "two"}


def test_words_break_between_chinese_characters():
    assert [u for _, u in i18n.words("日本語")] == ["日", "本", "語"]


def test_closing_punctuation_stays_with_the_previous_character():
    assert [u for _, u in i18n.words("テキスト。")] == ["テ", "キ", "ス", "ト。"]


def test_opening_punctuation_stays_with_the_next_character():
    assert [u for _, u in i18n.words("（注）")] == ["（注）"]


def test_latin_runs_are_kept_whole_inside_cjk_text():
    assert [u for _, u in i18n.words("使用 RGB 模式")] == ["使", "用", "RGB", "模", "式"]


def test_wrap_breaks_on_spaces_and_respects_the_width():
    from reportlab.pdfbase.pdfmetrics import stringWidth
    font = "Helvetica"
    width = stringWidth("aaa bbb", font, 10) + 1
    assert i18n.wrap("aaa bbb ccc", font, 10, width) == ["aaa bbb", "ccc"]
    assert i18n.wrap("aaa bbb ccc", font, 10, 1000) == ["aaa bbb ccc"]
    assert i18n.wrap("one\ntwo", font, 10, 1000) == ["one", "two"]


def test_visual_joins_and_reorders_arabic(monkeypatch):
    pytest.importorskip("arabic_reshaper")
    pytest.importorskip("bidi")
    monkeypatch.setattr(i18n, "_LANG", "ar")
    assert i18n.rtl()
    text = "عجلة الألوان"
    shaped = i18n.visual(text)
    assert shaped != text
    # joined letters are the presentation forms of the Arabic blocks
    assert any("ﭐ" <= ch <= "ﻼ" for ch in shaped)
    assert i18n.visual("abc") == "abc"          # no Arabic letters: untouched
    assert i18n.visual("") == ""


def test_visual_does_nothing_for_left_to_right_languages(monkeypatch):
    monkeypatch.setattr(i18n, "_LANG", "en")
    assert not i18n.rtl()
    assert i18n.visual("عجلة") == "عجلة"
