"""Texts of tilings.py in the added languages (see locales/__init__.py).
For now the names of the colour schemes, which wallpapers.py uses too; the rest
of the catalogue falls back to English."""

_KEYS = ["s_mono", "s_analogous", "s_complementary", "s_split", "s_triad", "s_tetrad",
         "s_square", "s_rainbow", "s_zellij", "s_azulejo", "s_girih", "s_earth", "s_grey",
         "s_ramp", "s_sweep"]

_NAMES = {
    "pt-BR": ["monocromático", "análogo", "complementar", "complementar dividido", "tríade",
              "tétrade (retângulo)", "quadrado", "arco-íris", "paleta zellij", "paleta azulejo",
              "paleta girih", "tons de terra", "cinzas", "degradê, do escuro ao claro",
              "passagem de matizes"],
    "fr": ["monochrome", "analogue", "complémentaire", "complémentaires adjacentes", "triade",
           "tétrade (rectangle)", "carré", "arc-en-ciel", "palette zellige", "palette azulejo",
           "palette girih", "tons de terre", "gris", "dégradé, du sombre au clair",
           "balayage de teintes"],
    "it": ["monocromatico", "analogo", "complementare", "complementari divisi", "triade",
           "tetrade (rettangolo)", "quadrato", "arcobaleno", "tavolozza zellige",
           "tavolozza azulejo", "tavolozza girih", "toni della terra", "grigi",
           "sfumatura, dallo scuro al chiaro", "passaggio di tinte"],
    "de": ["monochrom", "analog", "komplementär", "geteilt komplementär", "Triade",
           "Tetrade (Rechteck)", "Quadrat", "Regenbogen", "Zellige-Palette", "Azulejo-Palette",
           "Girih-Palette", "Erdtöne", "Grautöne", "Verlauf, von dunkel nach hell",
           "Farbtonfolge"],
    "nl": ["monochroom", "analoog", "complementair", "gesplitst complementair", "triade",
           "tetrade (rechthoek)", "vierkant", "regenboog", "zellige-palet", "azulejo-palet",
           "girih-palet", "aardetinten", "grijstinten", "verloop, van donker naar licht",
           "reeks kleurtonen"],
    "pl": ["monochromatyczny", "analogiczny", "dopełniający", "dopełniające rozszczepione",
           "triada", "tetrada (prostokąt)", "kwadrat", "tęcza", "paleta zellige",
           "paleta azulejo", "paleta girih", "barwy ziemi", "szarości",
           "gradient, od ciemnego do jasnego", "przejście barw"],
    "tr": ["tek renkli", "benzeşik", "tamamlayıcı", "bölünmüş tamamlayıcı", "üçlü",
           "dörtlü (dikdörtgen)", "kare", "gökkuşağı", "zellij paleti", "azulejo paleti",
           "girih paleti", "toprak tonları", "griler", "geçiş, koyudan açığa",
           "renk tonu dizisi"],
    "ru": ["монохромная", "аналоговая", "дополнительная", "расщеплённая дополнительная",
           "триада", "тетрада (прямоугольник)", "квадрат", "радуга", "палитра зеллидж",
           "палитра азулежу", "палитра гирих", "земляные тона", "оттенки серого",
           "градиент от тёмного к светлому", "переход тонов"],
    "zh": ["单色", "类似色", "互补色", "分裂互补色", "三角配色", "四色配色（矩形）", "正方形",
           "彩虹", "泽利吉配色", "葡式瓷砖配色", "吉里赫配色", "大地色", "灰色系",
           "渐变（由暗到明）", "色相过渡"],
    "ja": ["モノクロマティック", "類似色", "補色", "分裂補色", "トライアド", "テトラード（長方形）",
           "正方形", "虹色", "ゼリージュの配色", "アズレージョの配色", "ギリーの配色", "アースカラー",
           "グレー", "グラデーション（暗→明）", "色相の移り変わり"],
    "ko": ["단색", "유사색", "보색", "분보색", "3색 배색", "4색 배색(직사각형)", "정사각형", "무지개",
           "젤리주 팔레트", "아줄레주 팔레트", "기리 팔레트", "흙색 계열", "회색 계열",
           "그라데이션(어두움→밝음)", "색상 변화"],
}

STRINGS = {lang: dict(zip(_KEYS, names)) for lang, names in _NAMES.items()}
