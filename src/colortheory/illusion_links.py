"""Titles of the Wikipedia articles of the illusions in each language (from the language links of the
English articles). A missing language falls back to the English article."""
LINKS = {
    "Afterimage": {
        "ar": "صورة تلوية (طب العيون)", "de": "Nachbild", "es": "Imagen remanente",
        "fr": "Image rémanente", "ja": "残像効果", "ko": "잔상", "nl": "Nabeeld", "pl": "Kontrast następczy",
        "ru": "Послеобраз", "zh": "後像",
    },
    "Bezold effect": {
        "de": "Bezold-Effekt", "es": "Efecto Bezold", "fr": "Effet Bezold", "ja": "ベツォルト効果",
        "nl": "Bezoldeffect", "ru": "Эффект Бецольда",
    },
    "Café wall illusion": {
        "de": "Café Wall Illusion", "es": "Ilusión de la pared de la cafetería",
        "fr": "Illusion du mur du café", "ja": "カフェウォール錯視", "nl": "Cafémuur-illusie",
        "pt": "Ilusão de Münsterberg", "ru": "Иллюзия стены кафе", "tr": "Kafe duvarı illüzyonu",
    },
    "Checker shadow illusion": {
        "ar": "خدعة رقعة الشطرنج", "de": "Adelsons Schachbrett-Illusion",
        "es": "Tablero de ajedrez de Adelson", "fr": "Échiquier d'Adelson", "ja": "チェッカーシャドー錯視",
        "ko": "체커 그림자 착시", "nl": "Dambord van Adelson", "pl": "Szachownica Adelsona",
        "ru": "Иллюзия с тенью на шахматной доске", "zh": "棋盤陰影錯覺",
    },
    "Chromostereopsis": {
        "fr": "Chromostereopsis",
    },
    "Color constancy": {
        "ar": "ثبات لوني", "de": "Farbwahrnehmung#Farbkonstanz", "fr": "Constance de couleur",
        "ja": "色の恒常性", "ko": "색채항등성", "nl": "Kleurconstantie", "ru": "Цветопостоянство",
    },
    "Contrast effect": {
        "de": "Kontrasteffekt", "es": "Efecto contraste",
        "fr": "Loi du contraste simultané des couleurs", "ja": "対比効果", "pl": "Efekt kontrastu",
        "ru": "Эффект контраста",
    },
    "Cornsweet illusion": {
        "de": "Cornsweet-Illusion", "es": "Ilusión de Cornsweet", "fr": "Illusion de Cornsweet",
        "ja": "クレイク・オブライエン・コーンスウィート錯視", "zh": "康士維錯覺",
    },
    "Ebbinghaus illusion": {
        "ar": "خداع إيبنغهاوس البصري", "de": "Ebbinghaus-Täuschung", "es": "Ilusión de Ebbinghaus",
        "fr": "Illusion d'Ebbinghaus", "ja": "エビングハウス錯視", "ko": "에빙하우스 착시", "nl": "Ebbinghaus-illusie",
        "pl": "Złudzenie Ebbinghausa", "pt": "Ilusão de Ebbinghaus", "ru": "Иллюзия Эббингауза",
        "tr": "Ebbinghaus illüzyonu", "zh": "艾賓浩斯錯覺",
    },
    "Ehrenstein illusion": {
        "de": "Ehrenstein-Täuschung", "es": "Ilusión de Ehrenstein", "ja": "エーレンシュタイン錯視",
    },
    "Fraser spiral illusion": {
        "de": "Fraser-Spirale", "es": "Ilusión de la espiral de Fraser", "fr": "Spirale de Fraser",
        "ja": "フレイザー錯視", "nl": "Fraser-spiraal", "ru": "Спираль Фрэзера",
        "tr": "Fraser spiral illüzyonu", "zh": "弗雷澤螺旋錯覺",
    },
    "Grid illusion": {
        "pt": "Ilusão da grelha",
    },
    "Hering illusion": {
        "ar": "خداع هيرينغ", "de": "Hering-Täuschung", "es": "Ilusión de Hering",
        "fr": "Illusion de Hering", "ja": "ヘリング錯視", "ko": "헤링 착시", "nl": "Hering-illusie",
        "ru": "Иллюзия Геринга", "zh": "黑林错觉",
    },
    "Illusory motion": {
        "ja": "運動錯覚",
    },
    "Irradiation illusion": {
        "de": "Irradiation", "es": "Irradiación (óptica)", "nl": "Irradiatie",
        "pl": "Irradiacja (fizyka)", "ru": "Иррадиация (оптика)", "zh": "辐照错觉",
    },
    "Lilac chaser": {
        "ar": "خدعة اللولب الأرجواني", "es": "Perseguidor del lila", "zh": "丁香追逐者",
    },
    "Mach bands": {
        "de": "Machsche Streifen", "es": "Bandas de Mach", "fr": "Bandes de Mach", "it": "Effetto Mach",
        "ja": "マッハバンド", "ko": "마흐 밴드", "pl": "Pasmo Macha", "pt": "Bandas de Mach", "ru": "Полосы Маха",
        "zh": "马赫带",
    },
    "McCollough effect": {
        "es": "Efecto McCollough", "fr": "Effet McCollough", "pl": "Efekt McCollough",
        "ru": "Эффект Маккалоу", "zh": "麥科洛效應",
    },
    "Müller-Lyer illusion": {
        "ar": "خداع مولر-لاير", "de": "Müller-Lyer-Illusion", "es": "Ilusión de Müller-Lyer",
        "fr": "Illusion de Müller-Lyer", "it": "Illusione di Müller-Lyer", "ja": "ミュラー・リヤー錯視",
        "ko": "뮐러-라이어 착시", "nl": "Müller-Lyer-illusie", "pt": "Ilusão de Müller-Lyer",
        "ru": "Иллюзия Мюллера-Лайера", "zh": "米勒-莱尔错觉",
    },
    "Orbison illusion": {
        "ar": "خداع أربيسن", "de": "Orbison-Täuschung", "es": "Ilusión de Orbison",
        "fr": "Illusion de Orbison", "ja": "オービソン錯視", "ko": "오비슨 착시", "nl": "Orbison-illusie",
        "ru": "Иллюзия Орбисона",
    },
    "Penrose triangle": {
        "ar": "مثلث بنروز", "de": "Penrose-Dreieck", "es": "Triángulo de Penrose",
        "fr": "Triangle de Penrose", "it": "Triangolo di Penrose", "ja": "ペンローズの三角形", "ko": "펜로즈 삼각형",
        "nl": "Penrose-driehoek", "pl": "Trójkąt Penrose’a", "pt": "Triângulo de Penrose",
        "ru": "Треугольник Пенроуза", "zh": "潘洛斯三角",
    },
    "Peripheral drift illusion": {
        "nl": "Perifere drift-illusie (gezichtsbedrog)",
    },
    "Poggendorff illusion": {
        "ar": "خداع بوغندورف", "de": "Poggendorff-Täuschung", "es": "Ilusión de Poggendorff",
        "fr": "Illusion de Poggendorff", "ja": "ポゲンドルフ錯視", "ko": "포겐도르프 착시",
        "pt": "Ilusão de Poggendorff", "ru": "Иллюзия Поггендорфа", "zh": "波根多夫错觉",
    },
    "Ponzo illusion": {
        "ar": "خداع بونزو", "de": "Ponzo-Täuschung", "es": "Ilusión de Ponzo",
        "it": "Illusione di Ponzo", "ja": "ポンゾ錯視", "ko": "폰조 착시", "nl": "Ponzo-illusie",
        "ru": "Иллюзия Понцо", "tr": "Ponzo yanılsaması",
    },
    "Rubin vase": {
        "es": "Copa de Rubin", "ja": "ルビンの壺", "ko": "루빈의 꽃병", "nl": "Vaas van Rubin",
        "pt": "Vaso de Rubin", "ru": "Ваза Рубина", "zh": "魯賓之盃",
    },
    "Visual tilt effects": {
    },
    "White's illusion": {
        "ja": "ホワイト効果", "tr": "Munker illüzyonu",
    },
    "Zöllner illusion": {
        "ar": "خداع زولنر", "de": "Zöllner-Täuschung", "es": "Ilusión de Zöllner",
        "fr": "Illusion de Zollner", "ja": "ツェルナー錯視", "ko": "쵤너 착시", "nl": "Zöllner-illusie",
        "pt": "Ilusão de Zöllner", "ru": "Иллюзия Цёлльнера", "zh": "策尔纳错觉",
    },
    "Wundt illusion": {
        "ar": "خداع فونت", "de": "Wundt-Täuschung", "es": "Ilusión de Wundt", "fr": "Illusion de Wundt",
        "ja": "ヴント錯視", "ko": "분트 착시", "nl": "Wundt-illusie", "ru": "Иллюзия Вундта",
    },
}
