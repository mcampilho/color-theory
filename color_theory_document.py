#!/usr/bin/env python3
"""
color_theory_document.py
------------------------
Ten-page Colour Theory poster as a vector PDF (ReportLab + Pillow).

  Page 1 - RYB colour wheel, primary/secondary/tertiary, tint/tone/shade,
           colour meanings, complementary and colour schemes.
  Page 2 - Colour models (CMYK, RGB, HSB, grayscale), a full-spectrum
           hue/saturation disc, colour meanings, colour properties
           (warm, cool, saturated ...) and colour harmonies.
  Page 3 - Hue & lightness: a cross of hue x tint/shade swatches, tint,
           tone and shade wheels, and the RGB cube seen from its white
           corner as a hexagon of hexagons.
  Page 4 - Colour mixing & codes: RYB / RGB / CMYK side by side, a CMYK
           hexagram with ink percentages and the 216-colour web-safe palette.
  Page 5 - Named colours: an overlapping-circles RYB wheel with colour
           names and a wheel of CSS named colours with hex codes.
  Page 6 - Colour & emotion: Plutchik's wheel of emotions, a spiral
           rosette of tints and shades and translucent petals.
  Page 7 - "The Color Wheel": six RYB circles through the centre with
           named overlaps and ring, and a spiral sphere on black.
  Page 8 - The space of visible colours: the CIE 1931 chromaticity
           diagram, the visible spectrum and the colour-matching functions.
  Page 9 - Tints and shades: ten base colours from 90 % white to 90 % black.
  Page 10 - Hue circles: Munsell's 20 hues, and RYB / RGB twelve-colour stars.

Every colour is computed (RYB cube, HSB, RGB cube, CMY ink model, CSS
keyword values, CIE colour-matching functions, CIELAB); no image is copied.

All text lives in the STRINGS table below. English is the default;
Portuguese (pt) and Spanish (es) are included. To add a language, copy the
"en" block, translate the values and register it under a new key.

    pip install reportlab pillow
    python color_theory_document.py                     # English
    python color_theory_document.py --lang pt           # Portuguese
    python color_theory_document.py --lang es -o es.pdf # Spanish
    python color_theory_document.py --pages 2           # only page 2
    python color_theory_document.py --pages 3 4 5 6     # only the new pages
"""
import argparse
import colorsys
import math

from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

import i18n
from i18n import BOLD, ITAL, REG

# ==========================================================================
# 1. TRANSLATIONS
# ==========================================================================
STRINGS = {
    # ------------------------------------------------------------------ EN
    "en": {
        # ---- page 1
        "title1": "COLOUR THEORY",
        "primary_t": "Primary Colours",
        "primary_d": "3 pigment colours that can not be mixed or formed by any combination "
                     "of other colours. All other colours are derived from these 3 hues.",
        "secondary_t": "Secondary Colours",
        "secondary_d": "These are the colours formed by mixing two primary colours.",
        "tertiary_t": "Tertiary Colours",
        "tertiary_d": "These are the colours formed by mixing a primary and a secondary colour. "
                      "That's why the hue is a two word name, such as blue-green, red-violet, "
                      "and yellow-orange.",
        "analogous_t": "Analogous",
        "analogous_d": "Analogous colours sit next to one another on the colour wheel. "
                       "These colours are in harmony with one another.",
        "neutral_d": "White, black and gray are considered to be neutral.",
        "tint_t": "Tint", "tint_d": "A tint describes a colour that is mixed with white.",
        "tone_t": "Tone", "tone_d": "A tone describes a colour that is mixed with grey.",
        "shade_t": "Shade", "shade_d": "A shade describes a colour that is mixed with black.",
        "mono_t": "Monochromatic",
        "mono_d": "The term monochrome refers to the use of one colour or various shades "
                  "and tints of one colour in a single form.",
        "meaning_t": "Meaning of Colour", "meaning_sub": "(Western Culture)",
        "cold_t": "Cold Colours",
        "cold_d": "They give an impression of calm, and create a soothing impression. "
                  "They remind us of cold water.",
        "warm_t": "Warm Colours",
        "warm_d": "They are vivid and energetic, they are visually and emotionally exciting. "
                  "They remind us of fire and heat.",
        "cold": "COLD", "warm": "WARM",
        "tertiary_lbl": "TERTIARY", "primary_lbl": "PRIMARY", "secondary_lbl": "SECONDARY",
        "hue_names": ["YELLOW", "YELLOW-ORANGE", "ORANGE", "RED-ORANGE", "RED", "RED-VIOLET",
                      "VIOLET", "BLUE-VIOLET", "BLUE", "BLUE-GREEN", "GREEN", "YELLOW-GREEN"],
        "comp_t1": "Complementary", "comp_t2": "Colours",
        "comp_d": "Colours that are opposite each other on the colour wheel are considered "
                  "to be complementary colours (example: red and green).",
        "comp_d2": "When put together, they appear more vivid than when apart.",
        "sch_triadic": ["Triadic", "colour scheme"],
        "sch_rect": ["Rectangle (tetradic)", "colour scheme"],
        "sch_split": ["Split-Complementary", "colour scheme"],
        "sch_square": ["Square", "colour scheme"],
        "meanings1": [
            ("RED:", "Passion, Love, Fire, Anger, Blood"),
            ("ORANGE:", "Energy, Happiness, Vitality, Stimulation"),
            ("YELLOW:", "Sunshine, Happiness, Hope, Deceit"),
            ("GREEN:", "New Beginnings, Abundance, Nature"),
            ("BLUE:", "Sky, Calm, Responsible, Sadness, Sea"),
            ("VIOLET:", "Creativity, Royalty, Wealth, Ambition"),
            ("BLACK:", "Mystery, Elegance, Evil, Death, Power"),
            ("GRAY:", "Moody, Conservative, Formality"),
            ("WHITE:", "Purity, Cleanliness, Virtue, Innocence"),
            ("BROWN:", "Nature, Wholesomeness, Dependability"),
            ("TAN OR BEIGE:", "Conservative, Piety, Dull"),
            ("CREAM OR IVORY:", "Calm, Elegant, Purity"),
        ],
        # ---- page 2
        "title2": "COLOR THEORY",
        "models_h": "COLOR MODELS", "meanings_h": "COLOR MEANINGS",
        "properties_h": "COLOR PROPERTIES", "harmonies_h": "COLOR HARMONIES",
        "m_cmyk": ("CMYK", "Printing standard.", "Mix of cyan, magenta, yellow and black inks."),
        "m_rgb": ("RGB", "Digital standard.", "Mix of red, green and blue channels of light."),
        "m_hsb": ("HSB", "Variation of RGB.", "Mix of hue, saturation and brightness."),
        "m_gray": ("GRAYSCALE", "Intensity of black.", "Uses only black intensity to create shade."),
        "meanings2": [
            "PASSION, LOVE, BLOOD, DANGER, STRENGTH",
            "ROMANTIC, FEMININE, LOVE, SENSITIVITY, EXCITING",
            "OPTIMISM, SUNSHINE, CONFIDENCE, ATTENTION, SUCCESS",
            "HEALTH, GROWTH, PEACE, VITALITY, WEALTH",
            "ENERGY, HAPPINESS, SUCCESS, WARMTH, CREATIVITY",
            "TRUST, SERENITY, PEACE, COMMUNICATION, SADNESS",
            "ROYALTY, MAJESTY, MYSTERY, SPIRITUALITY, LUXURY",
            "ORGANIC, HONEST, NATURAL, SIMPLE, WHOLESOME",
            "COMPROMISE, NEUTRAL, BALANCE, CONSERVATIVE, FRUSTRATION",
            "ELEGANCE, POWER, LUXURY, MYSTERY, SORROW",
            "PURE, SIMPLE, INNOCENCE, VIRGINITY, MINIMALISM",
        ],
        "properties": ["WARM", "COOL", "SATURATED", "DESATURATED", "BRIGHT", "DARK", "MONOCHROME"],
        "harmonies": ["ANALOGOUS", "COMPLEMENTARY", "TRIAD", "SPLIT COMPLEMENTARY",
                      "TETRAD", "MONOCHROMATIC", "SQUARE"],
        # ---- shared by pages 3-5
        "rgb_names": ["RED", "YELLOW", "GREEN", "CYAN", "BLUE", "MAGENTA"],
        # ---- page 3
        "title3": "HUE & LIGHTNESS",
        "cross_t": "HUE × LIGHTNESS",
        "cross_d": "Each row is a hue; each column adds white (left) or black (right). "
                   "The long stem runs through every hue, the arm through the whole range "
                   "from tint to shade.",
        "plus_white": "+ WHITE", "plus_black": "+ BLACK",
        "tints_t": "TINTS",
        "tints_d": "24 hues of the RYB wheel, mixed with more and more white toward the centre.",
        "tones_t": "TONES",
        "tones_d": "The same hues mixed with grey: softer, duller colours toward the centre.",
        "shades_t": "SHADES",
        "shades_d": "12 hues of light, darkened ring by ring by adding black.",
        "shade_names": ["RED", "ORANGE", "YELLOW", "LIME", "GREEN", "TURQUOISE", "CYAN",
                        "SKY BLUE", "BLUE", "VIOLET", "MAGENTA", "ROSE"],
        "hex_t": "THE RGB CUBE SEEN FROM ITS WHITE CORNER",
        "hex_d": "Looking down the grey diagonal of the RGB cube, its three bright faces form "
                 "a hexagon: white in the centre, the six pure hues at the corners, and every "
                 "mixture of two channels in between. The hidden faces hold the darker colours.",
        # ---- page 4
        "title4": "COLOUR MIXING & CODES",
        "mix_ryb": ("TRADITIONAL COLOUR", "Mixing pigments: painting and fine art.",
                    "Subtractive: the three primaries make a dark brown.",
                    "Complementary: red – green"),
        "mix_rgb": ("LIGHT", "Mixing light: screens, cameras and photos.",
                    "Additive: the three primaries make white.",
                    "Complementary: red – cyan"),
        "mix_cmyk": ("PRINTING", "Mixing inks: commercial printing.",
                     "Subtractive: the three inks make a near-black, so black (K) ink is added. "
                     "White is the paper.",
                     "Complementary: cyan – red"),
        "star_t": "CMYK INK PERCENTAGES",
        "star_d": "Each triangle gives the percentages of cyan (C), magenta (M) and yellow (Y) "
                  "ink that print it. Two inks at full strength make red, green or blue.",
        "web_t": "WEB-SAFE PALETTE",
        "web_d": "216 colours whose red, green and blue channels each take one of six values: "
                 "00, 33, 66, 99, CC or FF. The three-digit code #F93 is short for #FF9933. "
                 "Each block has one red value; rows change green and columns change blue.",
        # ---- page 5
        "title5": "NAMED COLOURS",
        "wheel5_t": "THE COLOUR WHEEL",
        "wheel5_d": "Six overlapping circles of the RYB wheel: where two meet, their mixture "
                    "appears. The outer ring shows each hue darkened with black.",
        "lens_names": ["AMBER", "VERMILION", "MAGENTA", "INDIGO", "TEAL", "CHARTREUSE"],
        "dark_names": ["OLIVE", "OCHRE", "RUST", "BRICK", "MAROON", "PLUM", "AUBERGINE",
                       "MIDNIGHT", "NAVY", "PETROL", "FOREST", "MOSS"],
        "css_t": "CSS NAMED COLOURS",
        "css_d": "Colour names of the web (CSS keywords) with their hex codes, grouped by "
                 "colour family and ordered by hue.",
        "css_families": ["RED", "ORANGE", "BROWN", "YELLOW", "GREEN", "CYAN", "BLUE",
                         "PURPLE", "PINK", "GREY"],
        # ---- page 6
        "title6": "COLOUR & EMOTION",
        "plutchik_t": "PLUTCHIK'S WHEEL OF EMOTIONS",
        "plutchik_d": "Eight basic emotions: stronger toward the centre, milder toward the tips. "
                      "Between the petals, the feelings that combine two neighbours.",
        # clockwise from the top: (intense, basic, mild)
        "emotions": [("ECSTASY", "JOY", "SERENITY"), ("ADMIRATION", "TRUST", "ACCEPTANCE"),
                     ("TERROR", "FEAR", "APPREHENSION"), ("AMAZEMENT", "SURPRISE", "DISTRACTION"),
                     ("GRIEF", "SADNESS", "PENSIVENESS"), ("LOATHING", "DISGUST", "BOREDOM"),
                     ("RAGE", "ANGER", "ANNOYANCE"), ("VIGILANCE", "ANTICIPATION", "INTEREST")],
        "dyads": ["LOVE", "SUBMISSION", "AWE", "DISAPPROVAL", "REMORSE", "CONTEMPT",
                  "AGGRESSIVENESS", "OPTIMISM"],
        "rosette_t": "SPIRAL OF TINTS AND SHADES",
        "rosette_d": "Each ring is turned a little further than the one inside it, so hue and "
                     "lightness sweep round in a spiral, from a white core to dark edges.",
        "petals_t": "TRANSLUCENT PETALS",
        "petals_d": "Two crowns of 24 half-transparent petals: where petals overlap, their "
                    "colours combine into deeper ones.",
        # ---- page 7
        "cw_title": "THE COLOR WHEEL",
        # clockwise from the top: circles, lenses (red/violet first), ring cells
        "cw_circles": ["RED", "VIOLET", "CYAN BLUE", "GREEN", "YELLOW", "ORANGE"],
        "cw_lenses": ["BURGUNDY", "STEEL BLUE", "TURQUOISE", "GREEN APPLE", "GOLD",
                      "VERMILLION"],
        "cw_ring": ["CRIMSON", "PURPLE", "INDIGO", "SKY BLUE", "PEACOCK", "TEAL", "LEAF GREEN",
                    "CHARTREUSE", "SAFFRON", "AMBER", "TANGERINE", "SCARLET"],
        "sphere_t": "SPIRAL SPHERE",
        "sphere_d": "36 circles meet at the centre and cross again further out, cutting curved "
                    "cells that wind outward in spirals. Each spiral arm keeps one hue; a light "
                    "from the upper right shades the disc like a sphere, from a white highlight "
                    "to a dark rim.",
        # ---- page 8
        "title8": "THE SPACE OF VISIBLE COLOURS",
        "cie_t": "CIE 1931 CHROMATICITY DIAGRAM",
        "cie_d": "Every colour the eye can see, at equal brightness, placed by its chromaticity "
                 "coordinates x and y. Pure colours of a single wavelength lie on the curved "
                 "edge; the straight base joins red and violet and holds the purples, which no "
                 "single wavelength can produce. Inside are mixtures, paler toward white. A "
                 "screen shows only the colours inside its triangle, so the fill here is an "
                 "approximation.",
        "cie_legend": ["Spectral locus: one wavelength (nm)", "Line of purples: red + violet",
                       "Planckian locus: colour of a glowing body (K)",
                       "sRGB: the colours a screen can show", "E: equal-energy white"],
        "cie_regions": ["Green", "Yellowish green", "Yellow green", "Greenish yellow", "Yellow",
                        "Orange yellow", "Orange", "Reddish orange", "Red", "Pink",
                        "Purplish red", "Reddish purple", "Purple", "Violet", "Purplish blue",
                        "Blue", "Greenish blue", "Bluish green"],
        "spectrum_t": "THE VISIBLE SPECTRUM",
        "spectrum_d": "Bottom: wavelengths from 380 to 700 nm as screen colours. Top: the three "
                      "colour-matching functions x, y, z, which turn any light into the X, Y, Z "
                      "values behind the diagram.",
        # ---- page 9
        "title9": "TINTS AND SHADES",
        "ts_sub": "A tint adds white to a base colour; a shade adds black.",
        "add_white": "ADD WHITE", "add_black": "ADD BLACK", "base_colour": "BASE COLOUR",
        "ts_rows": ["RED", "ORANGE", "YELLOW", "GREEN", "TEAL", "BLUE", "PURPLE", "PINK",
                    "BROWN", "GREY"],
        "ts_note": "Tints are lighter and softer versions of a colour, shades are darker ones. "
                   "Together they add depth, contrast and richness to any design.",
        # ---- page 10
        "title10": "HUE CIRCLES",
        "munsell_t": "MUNSELL HUE CIRCLE",
        "munsell_d": "Five principal hues (R, Y, G, B, P) and five in between (YR, GY, BG, PB, "
                     "RP), each split into steps 1 to 10; shown here at 5 and 10. Each swatch "
                     "is the most saturated screen colour of that hue.",
        "ryb_star_d": "The painter's wheel: primaries red, yellow and blue on one triangle, "
                      "secondaries on the other, tertiaries in the notches between them.",
        "rgb_star_d": "The wheel of light: primaries red, green and blue; their mixtures "
                      "yellow, cyan and magenta; and six more colours in between.",
        "rgb12_names": ["RED", "ORANGE", "YELLOW", "CHARTREUSE", "GREEN", "SPRING GREEN",
                        "CYAN", "AZURE", "BLUE", "VIOLET", "MAGENTA", "ROSE"],
    },
    # ------------------------------------------------------------------ PT
    "pt": {
        "title1": "TEORIA DA COR",
        "primary_t": "Cores Primárias",
        "primary_d": "3 cores-pigmento que não podem ser misturadas nem formadas por qualquer "
                     "combinação de outras cores. Todas as outras cores derivam destes 3 matizes.",
        "secondary_t": "Cores Secundárias",
        "secondary_d": "São as cores formadas pela mistura de duas cores primárias.",
        "tertiary_t": "Cores Terciárias",
        "tertiary_d": "São as cores formadas pela mistura de uma cor primária com uma secundária. "
                      "Por isso o matiz tem nome composto, como azul-verde, vermelho-violeta "
                      "e amarelo-laranja.",
        "analogous_t": "Análogas",
        "analogous_d": "As cores análogas ficam lado a lado no círculo cromático. "
                       "Estas cores estão em harmonia entre si.",
        "neutral_d": "Branco, preto e cinza são considerados neutros.",
        "tint_t": "Tinta (tint)", "tint_d": "Uma tinta (tint) é uma cor misturada com branco.",
        "tone_t": "Tom (tone)", "tone_d": "Um tom (tone) é uma cor misturada com cinza.",
        "shade_t": "Sombra (shade)", "shade_d": "Uma sombra (shade) é uma cor misturada com preto.",
        "mono_t": "Monocromático",
        "mono_d": "O termo monocromático refere-se ao uso de uma só cor, ou de vários tons "
                  "claros e escuros dessa cor, numa única composição.",
        "meaning_t": "Significado das Cores", "meaning_sub": "(Cultura Ocidental)",
        "cold_t": "Cores Frias",
        "cold_d": "Transmitem uma impressão de calma e criam um efeito tranquilizante. "
                  "Lembram-nos a água fria.",
        "warm_t": "Cores Quentes",
        "warm_d": "São vivas e enérgicas, visual e emocionalmente estimulantes. "
                  "Lembram-nos o fogo e o calor.",
        "cold": "FRIO", "warm": "QUENTE",
        "tertiary_lbl": "TERCIÁRIA", "primary_lbl": "PRIMÁRIA", "secondary_lbl": "SECUNDÁRIA",
        "hue_names": ["AMARELO", "AMARELO-LARANJA", "LARANJA", "VERMELHO-LARANJA", "VERMELHO",
                      "VERMELHO-VIOLETA", "VIOLETA", "AZUL-VIOLETA", "AZUL", "AZUL-VERDE",
                      "VERDE", "AMARELO-VERDE"],
        "comp_t1": "Cores", "comp_t2": "Complementares",
        "comp_d": "Cores opostas entre si no círculo cromático são consideradas "
                  "complementares (exemplo: vermelho e verde).",
        "comp_d2": "Quando colocadas juntas, parecem mais vivas do que separadas.",
        "sch_triadic": ["Esquema", "triádico"],
        "sch_rect": ["Esquema retangular", "(tetrádico)"],
        "sch_split": ["Esquema complementar", "dividido"],
        "sch_square": ["Esquema", "quadrado"],
        "meanings1": [
            ("VERMELHO:", "Paixão, Amor, Fogo, Raiva, Sangue"),
            ("LARANJA:", "Energia, Felicidade, Vitalidade, Estímulo"),
            ("AMARELO:", "Sol, Felicidade, Esperança, Engano"),
            ("VERDE:", "Recomeços, Abundância, Natureza"),
            ("AZUL:", "Céu, Calma, Responsabilidade, Tristeza, Mar"),
            ("VIOLETA:", "Criatividade, Realeza, Riqueza, Ambição"),
            ("PRETO:", "Mistério, Elegância, Maldade, Morte, Poder"),
            ("CINZA:", "Melancolia, Conservadorismo, Formalidade"),
            ("BRANCO:", "Pureza, Limpeza, Virtude, Inocência"),
            ("MARROM:", "Natureza, Saúde, Confiabilidade"),
            ("BEGE:", "Conservador, Piedade, Monótono"),
            ("CREME OU MARFIM:", "Calma, Elegância, Pureza"),
        ],
        "title2": "TEORIA DA COR",
        "models_h": "MODELOS DE COR", "meanings_h": "SIGNIFICADO DAS CORES",
        "properties_h": "PROPRIEDADES DA COR", "harmonies_h": "HARMONIAS DE COR",
        "m_cmyk": ("CMYK", "Padrão de impressão.", "Mistura de tintas ciano, magenta, amarela e preta."),
        "m_rgb": ("RGB", "Padrão digital.", "Mistura dos canais de luz vermelho, verde e azul."),
        "m_hsb": ("HSB", "Variação do RGB.", "Mistura de matiz, saturação e brilho."),
        "m_gray": ("ESCALA DE CINZA", "Intensidade do preto.",
                   "Usa apenas a intensidade do preto para criar sombra."),
        "meanings2": [
            "PAIXÃO, AMOR, SANGUE, PERIGO, FORÇA",
            "ROMÂNTICO, FEMININO, AMOR, SENSIBILIDADE, EXCITAÇÃO",
            "OTIMISMO, SOL, CONFIANÇA, ATENÇÃO, SUCESSO",
            "SAÚDE, CRESCIMENTO, PAZ, VITALIDADE, RIQUEZA",
            "ENERGIA, FELICIDADE, SUCESSO, CALOR, CRIATIVIDADE",
            "CONFIANÇA, SERENIDADE, PAZ, COMUNICAÇÃO, TRISTEZA",
            "REALEZA, MAJESTADE, MISTÉRIO, ESPIRITUALIDADE, LUXO",
            "ORGÂNICO, HONESTO, NATURAL, SIMPLES, SAUDÁVEL",
            "COMPROMISSO, NEUTRO, EQUILÍBRIO, CONSERVADOR, FRUSTRAÇÃO",
            "ELEGÂNCIA, PODER, LUXO, MISTÉRIO, LUTO",
            "PURO, SIMPLES, INOCÊNCIA, VIRGINDADE, MINIMALISMO",
        ],
        "properties": ["QUENTE", "FRIA", "SATURADA", "DESSATURADA", "BRILHANTE", "ESCURA",
                       "MONOCROMÁTICA"],
        "harmonies": ["ANÁLOGAS", "COMPLEMENTARES", "TRÍADE", "COMPLEMENTAR DIVIDIDA",
                      "TÉTRADE", "MONOCROMÁTICA", "QUADRADO"],
        "rgb_names": ["VERMELHO", "AMARELO", "VERDE", "CIANO", "AZUL", "MAGENTA"],
        "title3": "MATIZ E LUMINOSIDADE",
        "cross_t": "MATIZ × LUMINOSIDADE",
        "cross_d": "Cada linha é um matiz; cada coluna junta branco (à esquerda) ou preto "
                   "(à direita). A haste longa percorre todos os matizes e o braço toda a "
                   "gama, da tinta à sombra.",
        "plus_white": "+ BRANCO", "plus_black": "+ PRETO",
        "tints_t": "TINTAS (TINTS)",
        "tints_d": "24 matizes do círculo RYB, misturados com cada vez mais branco para o centro.",
        "tones_t": "TONS (TONES)",
        "tones_d": "Os mesmos matizes misturados com cinza: cores mais suaves e baças para o centro.",
        "shades_t": "SOMBRAS (SHADES)",
        "shades_d": "12 matizes da luz, escurecidos anel a anel com a adição de preto.",
        "shade_names": ["VERMELHO", "LARANJA", "AMARELO", "LIMA", "VERDE", "TURQUESA", "CIANO",
                        "CELESTE", "AZUL", "VIOLETA", "MAGENTA", "ROSA"],
        "hex_t": "O CUBO RGB VISTO DO VÉRTICE BRANCO",
        "hex_d": "Olhando ao longo da diagonal cinzenta do cubo RGB, as suas três faces claras "
                 "formam um hexágono: branco no centro, os seis matizes puros nos vértices e "
                 "todas as misturas de dois canais pelo meio. As faces escondidas guardam as "
                 "cores escuras.",
        "title4": "MISTURA E CÓDIGOS DE COR",
        "mix_ryb": ("COR TRADICIONAL", "Mistura de pigmentos: pintura e belas-artes.",
                    "Subtrativa: as três primárias dão um castanho escuro.",
                    "Complementares: vermelho – verde"),
        "mix_rgb": ("LUZ", "Mistura de luz: ecrãs, câmaras e fotografia.",
                    "Aditiva: as três primárias dão branco.",
                    "Complementares: vermelho – ciano"),
        "mix_cmyk": ("IMPRESSÃO", "Mistura de tintas: impressão comercial.",
                     "Subtrativa: as três tintas dão um quase-preto, por isso junta-se tinta "
                     "preta (K). O branco é o papel.",
                     "Complementares: ciano – vermelho"),
        "star_t": "PERCENTAGENS DE TINTA CMYK",
        "star_d": "Cada triângulo indica as percentagens de tinta ciano (C), magenta (M) e "
                  "amarela (Y) que o imprimem. Duas tintas no máximo dão vermelho, verde ou azul.",
        "web_t": "PALETA WEB-SAFE",
        "web_d": "216 cores cujos canais vermelho, verde e azul tomam um de seis valores: "
                 "00, 33, 66, 99, CC ou FF. O código de três dígitos #F93 abrevia #FF9933. "
                 "Cada bloco tem um valor de vermelho; as linhas mudam o verde e as colunas o azul.",
        "title5": "NOMES DAS CORES",
        "wheel5_t": "O CÍRCULO CROMÁTICO",
        "wheel5_d": "Seis círculos sobrepostos do círculo RYB: onde dois se cruzam, surge a sua "
                    "mistura. O anel exterior mostra cada matiz escurecido com preto.",
        "lens_names": ["ÂMBAR", "VERMELHÃO", "MAGENTA", "ÍNDIGO", "VERDE-AZULADO", "VERDE-LIMA"],
        "dark_names": ["OLIVA", "OCRE", "FERRUGEM", "TIJOLO", "GRENÁ", "AMEIXA", "BERINGELA",
                       "MEIA-NOITE", "AZUL-MARINHO", "PETRÓLEO", "VERDE-FLORESTA", "MUSGO"],
        "css_t": "CORES COM NOME EM CSS",
        "css_d": "Nomes de cores da web (palavras-chave CSS) com os códigos hexadecimais, "
                 "agrupados por família de cor e ordenados por matiz.",
        "css_families": ["VERMELHO", "LARANJA", "CASTANHO", "AMARELO", "VERDE", "CIANO", "AZUL",
                         "ROXO", "ROSA", "CINZA"],
        "title6": "COR E EMOÇÃO",
        "plutchik_t": "RODA DAS EMOÇÕES DE PLUTCHIK",
        "plutchik_d": "Oito emoções básicas: mais intensas para o centro, mais suaves para as "
                      "pontas. Entre as pétalas, os sentimentos que juntam duas vizinhas.",
        "emotions": [("ÊXTASE", "ALEGRIA", "SERENIDADE"), ("ADMIRAÇÃO", "CONFIANÇA", "ACEITAÇÃO"),
                     ("TERROR", "MEDO", "APREENSÃO"), ("ESPANTO", "SURPRESA", "DISTRAÇÃO"),
                     ("DESGOSTO", "TRISTEZA", "MELANCOLIA"), ("AVERSÃO", "NOJO", "TÉDIO"),
                     ("FÚRIA", "RAIVA", "IRRITAÇÃO"), ("VIGILÂNCIA", "ANTECIPAÇÃO", "INTERESSE")],
        "dyads": ["AMOR", "SUBMISSÃO", "REVERÊNCIA", "DESAPROVAÇÃO", "REMORSO", "DESPREZO",
                  "AGRESSIVIDADE", "OTIMISMO"],
        "rosette_t": "ESPIRAL DE TINTAS E SOMBRAS",
        "rosette_d": "Cada anel roda um pouco mais do que o anterior, e o matiz e a luminosidade "
                     "giram em espiral, de um núcleo branco até às margens escuras.",
        "petals_t": "PÉTALAS TRANSLÚCIDAS",
        "petals_d": "Duas coroas de 24 pétalas semitransparentes: onde as pétalas se sobrepõem, "
                    "as cores juntam-se em tons mais profundos.",
        # ---- page 7
        "cw_title": "A RODA DAS CORES",
        "cw_circles": ["VERMELHO", "VIOLETA", "AZUL-CIANO", "VERDE", "AMARELO", "LARANJA"],
        "cw_lenses": ["BORDÔ", "AZUL-AÇO", "TURQUESA", "VERDE-MAÇÃ", "DOURADO", "VERMELHÃO"],
        "cw_ring": ["CARMESIM", "PÚRPURA", "ÍNDIGO", "AZUL-CÉU", "AZUL-PAVÃO", "VERDE-AZULADO",
                    "VERDE-FOLHA", "VERDE-LIMA", "AÇAFRÃO", "ÂMBAR", "TANGERINA", "ESCARLATE"],
        "sphere_t": "ESFERA EM ESPIRAL",
        "sphere_d": "36 círculos encontram-se no centro e voltam a cruzar-se mais longe, "
                    "recortando células curvas que se enrolam em espirais para fora. Cada braço "
                    "da espiral mantém um matiz; uma luz vinda de cima, à direita, sombreia o "
                    "disco como uma esfera, do brilho branco à orla escura.",
        # ---- page 8
        "title8": "O ESPAÇO DAS CORES VISÍVEIS",
        "cie_t": "DIAGRAMA DE CROMATICIDADE CIE 1931",
        "cie_d": "Todas as cores que o olho vê, com o mesmo brilho, colocadas pelas coordenadas "
                 "de cromaticidade x e y. As cores puras de um só comprimento de onda ficam na "
                 "orla curva; a base reta une o vermelho ao violeta e contém os púrpuras, que "
                 "nenhum comprimento de onda produz sozinho. No interior ficam as misturas, mais "
                 "pálidas perto do branco. Um ecrã só mostra as cores dentro do seu triângulo, "
                 "por isso o preenchimento aqui é aproximado.",
        "cie_legend": ["Lugar espectral: um comprimento de onda (nm)",
                       "Linha dos púrpuras: vermelho + violeta",
                       "Lugar de Planck: cor de um corpo incandescente (K)",
                       "sRGB: as cores que um ecrã consegue mostrar", "E: branco de energia igual"],
        "cie_regions": ["Verde", "Verde amarelado", "Verde-amarelo", "Amarelo esverdeado",
                        "Amarelo", "Amarelo alaranjado", "Laranja", "Laranja avermelhado",
                        "Vermelho", "Rosa", "Vermelho arroxeado", "Púrpura avermelhado", "Púrpura",
                        "Violeta", "Azul arroxeado", "Azul", "Azul esverdeado", "Verde azulado"],
        "spectrum_t": "O ESPETRO VISÍVEL",
        "spectrum_d": "Em baixo: os comprimentos de onda de 380 a 700 nm como cores de ecrã. Em "
                      "cima: as três funções de correspondência de cor x, y, z, que transformam "
                      "qualquer luz nos valores X, Y, Z por trás do diagrama.",
        # ---- page 9
        "title9": "TINTAS E SOMBRAS",
        "ts_sub": "Uma tinta junta branco a uma cor de base; uma sombra junta preto.",
        "add_white": "JUNTAR BRANCO", "add_black": "JUNTAR PRETO", "base_colour": "COR DE BASE",
        "ts_rows": ["VERMELHO", "LARANJA", "AMARELO", "VERDE", "VERDE-AZULADO", "AZUL",
                    "ROXO", "ROSA", "CASTANHO", "CINZENTO"],
        "ts_note": "As tintas são versões mais claras e suaves de uma cor; as sombras, versões "
                   "mais escuras. Juntas dão profundidade, contraste e riqueza a qualquer design.",
        # ---- page 10
        "title10": "CÍRCULOS DE MATIZ",
        "munsell_t": "CÍRCULO DE MATIZES DE MUNSELL",
        "munsell_d": "Cinco matizes principais (R, Y, G, B, P) e cinco intermédios (YR, GY, BG, "
                     "PB, RP), cada um dividido em passos de 1 a 10; aqui aparecem o 5 e o 10. "
                     "Cada amostra é a cor de ecrã mais saturada desse matiz.",
        "ryb_star_d": "O círculo do pintor: primárias vermelho, amarelo e azul num triângulo, "
                      "secundárias no outro, terciárias nos recortes entre eles.",
        "rgb_star_d": "O círculo da luz: primárias vermelho, verde e azul; as suas misturas "
                      "amarelo, ciano e magenta; e mais seis cores entre elas.",
        "rgb12_names": ["VERMELHO", "LARANJA", "AMARELO", "CHARTREUSE", "VERDE",
                        "VERDE-PRIMAVERA", "CIANO", "AZUL-CELESTE", "AZUL", "VIOLETA", "MAGENTA",
                        "ROSA"],
    },
    # ------------------------------------------------------------------ ES
    "es": {
        "title1": "TEORÍA DEL COLOR",
        "primary_t": "Colores Primarios",
        "primary_d": "3 colores pigmento que no pueden obtenerse mezclando ni combinando otros "
                     "colores. Todos los demás colores derivan de estos 3 tonos.",
        "secondary_t": "Colores Secundarios",
        "secondary_d": "Son los colores que se forman al mezclar dos colores primarios.",
        "tertiary_t": "Colores Terciarios",
        "tertiary_d": "Son los colores que resultan de mezclar un color primario con uno "
                      "secundario. Por eso el tono tiene un nombre compuesto, como azul-verde, "
                      "rojo-violeta y amarillo-naranja.",
        "analogous_t": "Análogos",
        "analogous_d": "Los colores análogos están uno al lado del otro en el círculo "
                       "cromático. Estos colores armonizan entre sí.",
        "neutral_d": "El blanco, el negro y el gris se consideran neutros.",
        "tint_t": "Tinte (tint)", "tint_d": "Un tinte (tint) es un color mezclado con blanco.",
        "tone_t": "Tono (tone)", "tone_d": "Un tono (tone) es un color mezclado con gris.",
        "shade_t": "Sombra (shade)", "shade_d": "Una sombra (shade) es un color mezclado con negro.",
        "mono_t": "Monocromático",
        "mono_d": "El término monocromo se refiere al uso de un solo color o de varias "
                  "sombras y tintes de un mismo color en una sola forma.",
        "meaning_t": "Significado de los Colores", "meaning_sub": "(Cultura occidental)",
        "cold_t": "Colores Fríos",
        "cold_d": "Dan una impresión de calma y crean un efecto relajante. "
                  "Nos recuerdan al agua fría.",
        "warm_t": "Colores Cálidos",
        "warm_d": "Son vivos y enérgicos, visual y emocionalmente estimulantes. "
                  "Nos recuerdan al fuego y al calor.",
        "cold": "FRÍO", "warm": "CÁLIDO",
        "tertiary_lbl": "TERCIARIO", "primary_lbl": "PRIMARIO", "secondary_lbl": "SECUNDARIO",
        "hue_names": ["AMARILLO", "AMARILLO-NARANJA", "NARANJA", "ROJO-NARANJA", "ROJO",
                      "ROJO-VIOLETA", "VIOLETA", "AZUL-VIOLETA", "AZUL", "AZUL-VERDE",
                      "VERDE", "AMARILLO-VERDE"],
        "comp_t1": "Colores", "comp_t2": "Complementarios",
        "comp_d": "Los colores opuestos entre sí en el círculo cromático se consideran "
                  "complementarios (ejemplo: rojo y verde).",
        "comp_d2": "Colocados juntos, parecen más vivos que por separado.",
        "sch_triadic": ["Esquema", "triádico"],
        "sch_rect": ["Esquema rectangular", "(tetrádico)"],
        "sch_split": ["Esquema complementario", "dividido"],
        "sch_square": ["Esquema", "cuadrado"],
        "meanings1": [
            ("ROJO:", "Pasión, Amor, Fuego, Ira, Sangre"),
            ("NARANJA:", "Energía, Felicidad, Vitalidad, Estímulo"),
            ("AMARILLO:", "Sol, Felicidad, Esperanza, Engaño"),
            ("VERDE:", "Nuevos comienzos, Abundancia, Naturaleza"),
            ("AZUL:", "Cielo, Calma, Responsabilidad, Tristeza, Mar"),
            ("VIOLETA:", "Creatividad, Realeza, Riqueza, Ambición"),
            ("NEGRO:", "Misterio, Elegancia, Maldad, Muerte, Poder"),
            ("GRIS:", "Melancolía, Conservadurismo, Formalidad"),
            ("BLANCO:", "Pureza, Limpieza, Virtud, Inocencia"),
            ("MARRÓN:", "Naturaleza, Salubridad, Fiabilidad"),
            ("BEIGE:", "Conservador, Piedad, Apagado"),
            ("CREMA O MARFIL:", "Calma, Elegante, Pureza"),
        ],
        "title2": "TEORÍA DEL COLOR",
        "models_h": "MODELOS DE COLOR", "meanings_h": "SIGNIFICADO DE LOS COLORES",
        "properties_h": "PROPIEDADES DEL COLOR", "harmonies_h": "ARMONÍAS DE COLOR",
        "m_cmyk": ("CMYK", "Estándar de impresión.", "Mezcla de tintas cian, magenta, amarilla y negra."),
        "m_rgb": ("RGB", "Estándar digital.", "Mezcla de los canales de luz rojo, verde y azul."),
        "m_hsb": ("HSB", "Variación del RGB.", "Mezcla de tono, saturación y brillo."),
        "m_gray": ("ESCALA DE GRISES", "Intensidad del negro.",
                   "Usa solo la intensidad del negro para crear sombra."),
        "meanings2": [
            "PASIÓN, AMOR, SANGRE, PELIGRO, FUERZA",
            "ROMÁNTICO, FEMENINO, AMOR, SENSIBILIDAD, EMOCIÓN",
            "OPTIMISMO, SOL, CONFIANZA, ATENCIÓN, ÉXITO",
            "SALUD, CRECIMIENTO, PAZ, VITALIDAD, RIQUEZA",
            "ENERGÍA, FELICIDAD, ÉXITO, CALIDEZ, CREATIVIDAD",
            "CONFIANZA, SERENIDAD, PAZ, COMUNICACIÓN, TRISTEZA",
            "REALEZA, MAJESTAD, MISTERIO, ESPIRITUALIDAD, LUJO",
            "ORGÁNICO, HONESTO, NATURAL, SIMPLE, SALUDABLE",
            "COMPROMISO, NEUTRO, EQUILIBRIO, CONSERVADOR, FRUSTRACIÓN",
            "ELEGANCIA, PODER, LUJO, MISTERIO, LUTO",
            "PURO, SIMPLE, INOCENCIA, VIRGINIDAD, MINIMALISMO",
        ],
        "properties": ["CÁLIDO", "FRÍO", "SATURADO", "DESATURADO", "BRILLANTE", "OSCURO",
                       "MONOCROMO"],
        "harmonies": ["ANÁLOGOS", "COMPLEMENTARIOS", "TRÍADA", "COMPLEMENTARIO DIVIDIDO",
                      "TÉTRADA", "MONOCROMÁTICO", "CUADRADO"],
        "rgb_names": ["ROJO", "AMARILLO", "VERDE", "CIAN", "AZUL", "MAGENTA"],
        "title3": "MATIZ Y LUMINOSIDAD",
        "cross_t": "MATIZ × LUMINOSIDAD",
        "cross_d": "Cada fila es un matiz; cada columna añade blanco (a la izquierda) o negro "
                   "(a la derecha). El tallo largo recorre todos los matices y el brazo toda la "
                   "gama, del tinte a la sombra.",
        "plus_white": "+ BLANCO", "plus_black": "+ NEGRO",
        "tints_t": "TINTES (TINTS)",
        "tints_d": "24 matices del círculo RYB, mezclados con cada vez más blanco hacia el centro.",
        "tones_t": "TONOS (TONES)",
        "tones_d": "Los mismos matices mezclados con gris: colores más suaves y apagados hacia el centro.",
        "shades_t": "SOMBRAS (SHADES)",
        "shades_d": "12 matices de la luz, oscurecidos anillo a anillo al añadir negro.",
        "shade_names": ["ROJO", "NARANJA", "AMARILLO", "LIMA", "VERDE", "TURQUESA", "CIAN",
                        "CELESTE", "AZUL", "VIOLETA", "MAGENTA", "ROSA"],
        "hex_t": "EL CUBO RGB VISTO DESDE SU VÉRTICE BLANCO",
        "hex_d": "Mirando a lo largo de la diagonal gris del cubo RGB, sus tres caras claras "
                 "forman un hexágono: blanco en el centro, los seis matices puros en los vértices "
                 "y todas las mezclas de dos canales entre ellos. Las caras ocultas guardan los "
                 "colores oscuros.",
        "title4": "MEZCLA Y CÓDIGOS DE COLOR",
        "mix_ryb": ("COLOR TRADICIONAL", "Mezcla de pigmentos: pintura y bellas artes.",
                    "Sustractiva: los tres primarios dan un marrón oscuro.",
                    "Complementarios: rojo – verde"),
        "mix_rgb": ("LUZ", "Mezcla de luz: pantallas, cámaras y fotografía.",
                    "Aditiva: los tres primarios dan blanco.",
                    "Complementarios: rojo – cian"),
        "mix_cmyk": ("IMPRESIÓN", "Mezcla de tintas: impresión comercial.",
                     "Sustractiva: las tres tintas dan un casi negro, por eso se añade tinta "
                     "negra (K). El blanco es el papel.",
                     "Complementarios: cian – rojo"),
        "star_t": "PORCENTAJES DE TINTA CMYK",
        "star_d": "Cada triángulo indica los porcentajes de tinta cian (C), magenta (M) y "
                  "amarilla (Y) que lo imprimen. Dos tintas al máximo dan rojo, verde o azul.",
        "web_t": "PALETA WEB-SAFE",
        "web_d": "216 colores cuyos canales rojo, verde y azul toman uno de seis valores: "
                 "00, 33, 66, 99, CC o FF. El código de tres dígitos #F93 abrevia #FF9933. "
                 "Cada bloque tiene un valor de rojo; las filas cambian el verde y las columnas el azul.",
        "title5": "NOMBRES DE LOS COLORES",
        "wheel5_t": "EL CÍRCULO CROMÁTICO",
        "wheel5_d": "Seis círculos superpuestos del círculo RYB: donde dos se cruzan aparece su "
                    "mezcla. El anillo exterior muestra cada matiz oscurecido con negro.",
        "lens_names": ["ÁMBAR", "BERMELLÓN", "MAGENTA", "ÍNDIGO", "VERDE AZULADO", "VERDE LIMA"],
        "dark_names": ["OLIVA", "OCRE", "ÓXIDO", "LADRILLO", "GRANATE", "CIRUELA", "BERENJENA",
                       "MEDIANOCHE", "AZUL MARINO", "PETRÓLEO", "VERDE BOSQUE", "MUSGO"],
        "css_t": "COLORES CON NOMBRE EN CSS",
        "css_d": "Nombres de colores de la web (palabras clave CSS) con sus códigos "
                 "hexadecimales, agrupados por familia de color y ordenados por matiz.",
        "css_families": ["ROJO", "NARANJA", "MARRÓN", "AMARILLO", "VERDE", "CIAN", "AZUL",
                         "PÚRPURA", "ROSA", "GRIS"],
        "title6": "COLOR Y EMOCIÓN",
        "plutchik_t": "RUEDA DE LAS EMOCIONES DE PLUTCHIK",
        "plutchik_d": "Ocho emociones básicas: más intensas hacia el centro, más suaves hacia las "
                      "puntas. Entre los pétalos, los sentimientos que combinan dos vecinas.",
        "emotions": [("ÉXTASIS", "ALEGRÍA", "SERENIDAD"), ("ADMIRACIÓN", "CONFIANZA", "ACEPTACIÓN"),
                     ("TERROR", "MIEDO", "TEMOR"), ("ASOMBRO", "SORPRESA", "DISTRACCIÓN"),
                     ("PENA", "TRISTEZA", "MELANCOLÍA"), ("AVERSIÓN", "ASCO", "ABURRIMIENTO"),
                     ("FURIA", "IRA", "ENFADO"), ("VIGILANCIA", "ANTICIPACIÓN", "INTERÉS")],
        "dyads": ["AMOR", "SUMISIÓN", "SOBRECOGIMIENTO", "DESAPROBACIÓN", "REMORDIMIENTO",
                  "DESPRECIO", "AGRESIVIDAD", "OPTIMISMO"],
        "rosette_t": "ESPIRAL DE TINTES Y SOMBRAS",
        "rosette_d": "Cada anillo gira un poco más que el anterior, y el matiz y la luminosidad "
                     "dan vueltas en espiral, de un núcleo blanco a los bordes oscuros.",
        "petals_t": "PÉTALOS TRANSLÚCIDOS",
        "petals_d": "Dos coronas de 24 pétalos semitransparentes: donde los pétalos se "
                    "superponen, sus colores se combinan en tonos más profundos.",
        # ---- page 7
        "cw_title": "LA RUEDA DE COLORES",
        "cw_circles": ["ROJO", "VIOLETA", "AZUL CIAN", "VERDE", "AMARILLO", "NARANJA"],
        "cw_lenses": ["BURDEOS", "AZUL ACERO", "TURQUESA", "VERDE MANZANA", "DORADO",
                      "BERMELLÓN"],
        "cw_ring": ["CARMESÍ", "PÚRPURA", "ÍNDIGO", "AZUL CIELO", "AZUL PAVO REAL",
                    "VERDE AZULADO", "VERDE HOJA", "VERDE LIMA", "AZAFRÁN", "ÁMBAR", "MANDARINA",
                    "ESCARLATA"],
        "sphere_t": "ESFERA EN ESPIRAL",
        "sphere_d": "36 círculos se encuentran en el centro y vuelven a cruzarse más lejos, "
                    "recortando celdas curvas que se enrollan hacia fuera en espirales. Cada "
                    "brazo de la espiral mantiene un tono; una luz desde arriba a la derecha "
                    "sombrea el disco como una esfera, del brillo blanco al borde oscuro.",
        # ---- page 8
        "title8": "EL ESPACIO DE LOS COLORES VISIBLES",
        "cie_t": "DIAGRAMA DE CROMATICIDAD CIE 1931",
        "cie_d": "Todos los colores que ve el ojo, con el mismo brillo, situados por sus "
                 "coordenadas de cromaticidad x e y. Los colores puros de una sola longitud de "
                 "onda están en el borde curvo; la base recta une el rojo y el violeta y contiene "
                 "los púrpuras, que ninguna longitud de onda produce sola. Dentro están las "
                 "mezclas, más pálidas hacia el blanco. Una pantalla solo muestra los colores "
                 "dentro de su triángulo, así que el relleno aquí es aproximado.",
        "cie_legend": ["Lugar espectral: una longitud de onda (nm)",
                       "Línea de los púrpuras: rojo + violeta",
                       "Lugar de Planck: color de un cuerpo incandescente (K)",
                       "sRGB: los colores que puede mostrar una pantalla",
                       "E: blanco de igual energía"],
        "cie_regions": ["Verde", "Verde amarillento", "Verde amarillo", "Amarillo verdoso",
                        "Amarillo", "Amarillo anaranjado", "Naranja", "Naranja rojizo", "Rojo",
                        "Rosa", "Rojo purpúreo", "Púrpura rojizo", "Púrpura", "Violeta",
                        "Azul purpúreo", "Azul", "Azul verdoso", "Verde azulado"],
        "spectrum_t": "EL ESPECTRO VISIBLE",
        "spectrum_d": "Abajo: las longitudes de onda de 380 a 700 nm como colores de pantalla. "
                      "Arriba: las tres funciones de igualación de color x, y, z, que convierten "
                      "cualquier luz en los valores X, Y, Z detrás del diagrama.",
        # ---- page 9
        "title9": "TINTES Y SOMBRAS",
        "ts_sub": "Un tinte añade blanco a un color base; una sombra añade negro.",
        "add_white": "AÑADIR BLANCO", "add_black": "AÑADIR NEGRO", "base_colour": "COLOR BASE",
        "ts_rows": ["ROJO", "NARANJA", "AMARILLO", "VERDE", "VERDE AZULADO", "AZUL", "MORADO",
                    "ROSA", "MARRÓN", "GRIS"],
        "ts_note": "Los tintes son versiones más claras y suaves de un color; las sombras, "
                   "versiones más oscuras. Juntos dan profundidad, contraste y riqueza a "
                   "cualquier diseño.",
        # ---- page 10
        "title10": "CÍRCULOS DE TONO",
        "munsell_t": "CÍRCULO DE TONOS DE MUNSELL",
        "munsell_d": "Cinco tonos principales (R, Y, G, B, P) y cinco intermedios (YR, GY, BG, "
                     "PB, RP), cada uno dividido en pasos de 1 a 10; aquí aparecen el 5 y el 10. "
                     "Cada muestra es el color de pantalla más saturado de ese tono.",
        "ryb_star_d": "La rueda del pintor: primarios rojo, amarillo y azul en un triángulo, "
                      "secundarios en el otro, terciarios en los huecos entre ellos.",
        "rgb_star_d": "La rueda de la luz: primarios rojo, verde y azul; sus mezclas amarillo, "
                      "cian y magenta; y seis colores más entre ellos.",
        "rgb12_names": ["ROJO", "NARANJA", "AMARILLO", "CHARTREUSE", "VERDE", "VERDE PRIMAVERA",
                        "CIAN", "AZUR", "AZUL", "VIOLETA", "MAGENTA", "ROSA"],
    },
}

# the added languages (locales/); until a language has the whole poster translated, only
# its hue names are there and it is not offered on the command line
from locales.color_theory_document import STRINGS as _MORE   # noqa: E402

for _lang, _table in _MORE.items():
    STRINGS.setdefault(_lang, {}).update(_table)
POSTER_LANGS = [k for k, _ in i18n.LANGS if k in STRINGS and len(STRINGS[k]) >= len(STRINGS["en"])]

_LANG = "en"


def set_lang(code):
    global _LANG
    if code not in STRINGS:
        raise SystemExit("Unknown language '%s'. Available: %s" % (code, ", ".join(STRINGS)))
    _LANG = code
    i18n.use_lang(code)


def T(key):
    """Translated string for the active language (falls back to English)."""
    return STRINGS.get(_LANG, STRINGS["en"]).get(key, STRINGS["en"][key])


# ==========================================================================
# 2. PAGE GEOMETRY + GENERIC HELPERS
# ==========================================================================
W, H = landscape(letter)                  # 792 x 612 pt
SX, SY = W / 750.0, H / 570.0             # page-1 layout grid (750 x 570)


def X(x):
    return x * SX


def Y(y):
    return H - y * SY


def pol(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def luma(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def text_on(c):
    return (1, 1, 1) if luma(c) < 0.62 else (0.1, 0.1, 0.1)


def mix(c1, c2, t):
    return tuple(a + (b - a) * t for a, b in zip(c1, c2))


def fit_size(text, font, size, max_w, tracking=0.0):
    """Largest font size <= size for which the text fits max_w points."""
    while size > 4 and stringWidth(text, font, size) + tracking * (len(text) - 1) > max_w:
        size -= 0.25
    return size


def tracked(c, text, x, y, font, size, color, tracking=0.0, align="left", max_w=None):
    """Draw letter-spaced text (x = left, centre or right per `align`)."""
    if max_w:
        size = fit_size(text, font, size, max_w, tracking)
    w = stringWidth(text, font, size) + tracking * (len(text) - 1)
    x0 = {"left": x, "center": x - w / 2.0, "right": x - w}[align]
    c.saveState()
    t = c.beginText()
    t.setFont(font, size)
    t.setCharSpace(tracking)
    t.setTextOrigin(x0, y)
    t.setFillColorRGB(*color)
    t.textOut(text)
    c.drawText(t)
    c.restoreState()


def fill_poly(c, pts, fill, stroke=(1, 1, 1), lw=1.4):
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    c.setFillColorRGB(*fill)
    c.setStrokeColorRGB(*stroke)
    c.setLineWidth(lw)
    c.drawPath(p, fill=1, stroke=1)


def ring_wedge(cx, cy, r_in, r_out, a0, a1, steps=24):
    outer = [pol(cx, cy, r_out, a0 + (a1 - a0) * k / steps) for k in range(steps + 1)]
    inner = [pol(cx, cy, r_in, a1 + (a0 - a1) * k / steps) for k in range(steps + 1)]
    return outer + inner


def arc_text(c, text, cx, cy, base_r, mid_deg, font, size, color, inward=False, tracking=0.0):
    """Text along a circular arc centred on mid_deg (inward=True keeps the
    lower half of a wheel upright)."""
    widths = [stringWidth(ch, font, size) + tracking for ch in text]
    total, pos = sum(widths), 0.0
    for ch, w in zip(text, widths):
        ang = (pos + w / 2.0) / base_r
        if not inward:
            theta = math.radians(mid_deg) + total / (2 * base_r) - ang
            rot = math.degrees(theta) - 90
        else:
            theta = math.radians(mid_deg) - total / (2 * base_r) + ang
            rot = math.degrees(theta) + 90
        c.saveState()
        c.translate(cx + base_r * math.cos(theta), cy + base_r * math.sin(theta))
        c.rotate(rot)
        c.setFillColorRGB(*color)
        c.setFont(font, size)
        c.drawCentredString(0, 0, ch)
        c.restoreState()
        pos += w


def arc_arrow(c, cx, cy, r, a_from, a_to, color=(0.35, 0.35, 0.35)):
    sgn = 1 if a_to > a_from else -1
    end = a_to - sgn * 4.5
    pts = [pol(cx, cy, r, a_from + (end - a_from) * k / 20) for k in range(21)]
    c.setStrokeColorRGB(*color)
    c.setLineWidth(0.9)
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    c.drawPath(p, fill=0, stroke=1)
    q = c.beginPath()
    q.moveTo(*pol(cx, cy, r, a_to))
    q.lineTo(*pol(cx, cy, r + 3.2, end))
    q.lineTo(*pol(cx, cy, r - 3.2, end))
    q.close()
    c.setFillColorRGB(*color)
    c.drawPath(q, fill=1, stroke=0)


def swatch_row(c, cx_px, top_px, colors, w=29, h=15, gap=7, radius=3.5):
    total = len(colors) * w + (len(colors) - 1) * gap
    x0, y0 = X(cx_px) - total / 2.0, Y(top_px) - h
    for i, col in enumerate(colors):
        c.setFillColorRGB(*col)
        c.setStrokeColorRGB(0.55, 0.55, 0.55) if luma(col) > 0.93 else c.setStrokeColorRGB(*col)
        c.setLineWidth(0.6)
        c.roundRect(x0 + i * (w + gap), y0, w, h, radius, fill=1, stroke=1)


def para(c, text, cx_px, top_px, width_px, size=6.8, leading=8.4, font=REG,
         color=(0.12, 0.12, 0.12), align="center"):
    """Wrapped paragraph in page-1 layout px. Returns the last baseline (pt)."""
    lines = simpleSplit(text, font, size, width_px * SX)
    y = Y(top_px) - size
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    for ln in lines:
        (c.drawCentredString if align == "center" else c.drawString)(X(cx_px), y, ln)
        y -= leading
    return y + leading


def heading(c, text, cx_px, y_px, size=8.4, align="center", max_w_pt=None):
    if max_w_pt:
        size = fit_size(text, BOLD, size, max_w_pt)
    c.setFont(BOLD, size)
    c.setFillColorRGB(0, 0, 0)
    (c.drawCentredString if align == "center" else c.drawString)(X(cx_px), Y(y_px), text)


# ==========================================================================
# 3. RYB COLOUR MODEL  (page 1)
# ==========================================================================
# sRGB colours of the 8 corners of the RYB cube; inside the cube colours are
# trilinearly interpolated with smoothstep easing (Gossett & Chen, 2004).
# Primaries and secondaries are the RYB wheel of w3schools and Canva; the
# tertiaries, halfway along the edges, come out as the averages of their two
# neighbours, which are exactly the tertiaries of that wheel too.
def _hex(h):
    return tuple(int(h[k:k + 2], 16) / 255.0 for k in (0, 2, 4))


RYB_CORNERS = {
    (0, 0, 0): (1.00, 1.00, 1.00),   # white
    (1, 0, 0): _hex("FE2712"),       # red
    (0, 1, 0): _hex("FEFE33"),       # yellow
    (0, 0, 1): _hex("0247FE"),       # blue
    (1, 1, 0): _hex("FB9902"),       # orange  = red + yellow
    (0, 1, 1): _hex("66B032"),       # green   = yellow + blue
    (1, 0, 1): _hex("8601AF"),       # violet  = red + blue
    (1, 1, 1): (0.20, 0.10, 0.08),   # all pigments -> near black
}


def ryb_to_rgb(r, y, b):
    r, y, b = (t * t * (3 - 2 * t) for t in (r, y, b))
    out = [0.0, 0.0, 0.0]
    for (cr, cy, cb), col in RYB_CORNERS.items():
        w = (r if cr else 1 - r) * (y if cy else 1 - y) * (b if cb else 1 - b)
        for k in range(3):
            out[k] += w * col[k]
    return tuple(out)


# 12 hues clockwise from the top (points on the edges of the RYB cube)
HUE_RYB = [(0, 1, 0), (.5, 1, 0), (1, 1, 0), (1, .5, 0), (1, 0, 0), (1, 0, .5),
           (1, 0, 1), (.5, 0, 1), (0, 0, 1), (0, .5, 1), (0, 1, 1), (0, 1, .5)]


def hue_ryb(t):
    t %= 12
    i = int(math.floor(t))
    f = t - i
    a, b = HUE_RYB[i], HUE_RYB[(i + 1) % 12]
    return tuple(a[k] + (b[k] - a[k]) * f for k in range(3))


def hue_rgb(i):
    return ryb_to_rgb(*HUE_RYB[i % 12])


def draw_ryb_wheel(c, cx, cy, R, segments=12):
    """RYB ring + Itten hexagon. segments=24/36/60 gives a finer ring."""
    r_in, step = 0.72 * R, 360.0 / segments
    for i in range(segments):
        rgb = ryb_to_rgb(*hue_ryb(i * 12.0 / segments))
        mid = 90 - step * i
        fill_poly(c, ring_wedge(cx, cy, r_in, R, mid - step / 2, mid + step / 2), rgb,
                  lw=1.6 if segments <= 12 else 0.4)

    if segments == 12:                                   # tertiary labels
        names, mid_r, size = T("hue_names"), (r_in + R) / 2.0, 5.4
        cap = size * 0.72
        for i in (1, 3, 5, 7, 9, 11):
            mid = 90 - 30 * i
            col = text_on(hue_rgb(i))
            l1, l2 = T("tertiary_lbl"), names[i]
            if math.sin(math.radians(mid)) >= -1e-9:
                arc_text(c, l1, cx, cy, mid_r + cap * .35, mid, BOLD, size, col, False, .5)
                arc_text(c, l2, cx, cy, mid_r - cap * 1.45, mid, BOLD, size, col, False, .5)
            else:
                arc_text(c, l1, cx, cy, mid_r - cap * .35, mid, BOLD, size, col, True, .5)
                arc_text(c, l2, cx, cy, mid_r + cap * 1.45, mid, BOLD, size, col, True, .5)

    rh = r_in - 0.5                                       # centre hexagon
    Yv, Ov, Rv = pol(cx, cy, rh, 90), pol(cx, cy, rh, 30), pol(cx, cy, rh, -30)
    Vv, Bv, Gv = pol(cx, cy, rh, -90), pol(cx, cy, rh, -150), pol(cx, cy, rh, 150)
    C = (cx, cy)

    def mid_pt(p, q):
        return ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)

    mYB, mYR, mRB = mid_pt(Yv, Bv), mid_pt(Yv, Rv), mid_pt(Rv, Bv)
    cy_, cr_, cb_ = hue_rgb(0), hue_rgb(4), hue_rgb(8)
    co_, cv_, cg_ = hue_rgb(2), hue_rgb(6), hue_rgb(10)
    fill_poly(c, [Gv, Yv, Bv], cg_)
    fill_poly(c, [Ov, Yv, Rv], co_)
    fill_poly(c, [Vv, Rv, Bv], cv_)
    fill_poly(c, [Yv, mYB, C, mYR], cy_)
    fill_poly(c, [Rv, mYR, C, mRB], cr_)
    fill_poly(c, [Bv, mYB, C, mRB], cb_)

    def label(pts, l1, l2, col, rot=0, size=7.4):
        gx, gy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
        c.saveState()
        c.translate(gx, gy)
        c.rotate(rot)
        c.setFillColorRGB(*text_on(col))
        c.setFont(BOLD, size)
        c.drawCentredString(0, 1.2, l1)
        c.drawCentredString(0, -size - 0.4, l2)
        c.restoreState()

    names, P, S = T("hue_names"), T("primary_lbl"), T("secondary_lbl")
    label([Yv, mYB, C, mYR], P, names[0], cy_)
    label([Rv, mYR, C, mRB], P, names[4], cr_)
    label([Bv, mYB, C, mRB], P, names[8], cb_)
    label([Gv, Yv, Bv], S, names[10], cg_, rot=60)
    label([Ov, Yv, Rv], S, names[2], co_, rot=-60)
    label([Vv, Rv, Bv], S, names[6], cv_, rot=0)

    rr, grey = R + 13, (0.2, 0.2, 0.2)                    # cold / warm marks
    for ang in (90, 270):
        a, b = pol(cx, cy, R + 6, ang), pol(cx, cy, R + 21, ang)
        c.setStrokeColorRGB(0.35, 0.35, 0.35)
        c.setLineWidth(0.9)
        c.line(a[0], a[1], b[0], b[1])
    arc_text(c, T("cold"), cx, cy, rr, 90 + 14, REG, 6.4, grey, False, 0.9)
    arc_text(c, T("warm"), cx, cy, rr, 90 - 14, REG, 6.4, grey, False, 0.9)
    arc_arrow(c, cx, cy, rr + 2.5, 90 + 24, 90 + 42)
    arc_arrow(c, cx, cy, rr + 2.5, 90 - 24, 90 - 42)
    arc_text(c, T("cold"), cx, cy, rr + 5, 270 - 14, REG, 6.4, grey, True, 0.9)
    arc_text(c, T("warm"), cx, cy, rr + 5, 270 + 14, REG, 6.4, grey, True, 0.9)
    arc_arrow(c, cx, cy, rr + 2.5, 270 - 24, 270 - 42)
    arc_arrow(c, cx, cy, rr + 2.5, 270 + 24, 270 + 42)


def draw_mini_ryb(c, cx, cy, r, picks=None):
    r_in = r * 0.42
    for i in range(12):
        mid = 90 - 30 * i
        fill_poly(c, ring_wedge(cx, cy, r_in, r, mid - 15, mid + 15, steps=8),
                  hue_rgb(i), lw=0.5)
    if picks:
        mr = (r + r_in) / 2.0
        pts = [pol(cx, cy, mr, 90 - 30 * i) for i in picks]
        c.setStrokeColorRGB(.1, .1, .1)
        c.setLineWidth(.9)
        p = c.beginPath()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        if len(pts) > 2:
            p.close()
        c.drawPath(p, fill=0, stroke=1)
        for (px, py) in pts:
            c.setFillColorRGB(1, 1, 1)
            c.setStrokeColorRGB(.1, .1, .1)
            c.setLineWidth(.7)
            c.circle(px, py, r * 0.085, fill=1, stroke=1)


def scheme_item(c, cx_px, cy_px, r_pt, picks, caption):
    cx, cy = X(cx_px), Y(cy_px)
    draw_mini_ryb(c, cx, cy, r_pt, picks)
    c.setFont(BOLD, 6.8)
    c.setFillColorRGB(0, 0, 0)
    x, y = cx + r_pt + 6, cy + 3 * (len(caption) - 1)
    for ln in caption:
        c.drawString(x, y, ln)
        y -= 8


# ==========================================================================
# 4. PAGE 1
# ==========================================================================
def build_page_1(c):
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    tracked(c, T("title1"), X(375), Y(50), ITAL, 43, (.05, .05, .05),
            tracking=1.2, align="center", max_w=430)

    # ---- left column
    LX, LW = 76, 140
    Yel, Red, Blu = hue_rgb(0), hue_rgb(4), hue_rgb(8)
    Ora, Gre, Vio = hue_rgb(2), hue_rgb(10), hue_rgb(6)
    mw = 150                                           # max heading width (pt)

    swatch_row(c, LX, 16, [Yel, Red, Blu], w=34, gap=10)
    heading(c, T("primary_t"), LX, 52, max_w_pt=mw)
    para(c, T("primary_d"), LX, 58, LW)

    swatch_row(c, LX, 136, [Ora, Gre, Vio], w=34, gap=10)
    heading(c, T("secondary_t"), LX, 173, max_w_pt=mw)
    para(c, T("secondary_d"), LX, 180, LW)

    swatch_row(c, LX, 226, [hue_rgb(1), hue_rgb(3), hue_rgb(5)], w=34, gap=10)
    swatch_row(c, LX, 249, [hue_rgb(7), hue_rgb(9), hue_rgb(11)], w=34, gap=10)
    heading(c, T("tertiary_t"), LX, 283, max_w_pt=mw)
    para(c, T("tertiary_d"), LX, 289, LW)

    swatch_row(c, LX, 388, [hue_rgb(11), hue_rgb(10), hue_rgb(9)], w=34, gap=10)
    heading(c, T("analogous_t"), LX, 425, max_w_pt=mw)
    para(c, T("analogous_d"), LX, 431, LW)

    swatch_row(c, LX, 495, [(1, 1, 1), (.72, .72, .72), (.05, .05, .05)], w=34, gap=10)
    para(c, T("neutral_d"), LX, 520, LW)

    # ---- right column
    RX, RW = 669, 138
    base, white, grey, black = hue_rgb(4), (1, 1, 1), (.5, .5, .5), (0, 0, 0)
    tints = [mix(base, white, k) for k in (0, .3, .6, .8)]
    tones = [mix(base, grey, k) for k in (0, .3, .55, .8)]
    shades = [mix(base, black, k) for k in (0, .3, .55, .8)]
    mono = [mix(base, white, .55), mix(base, white, .25), base, mix(base, black, .4)]

    for top, ttl, dsc, cols in ((16, "tint", "tint_d", tints), (82, "tone", "tone_d", tones),
                                (146, "shade", "shade_d", shades)):
        swatch_row(c, RX, top, cols, w=27, gap=5)
        heading(c, T(ttl + "_t"), RX, top + 34, max_w_pt=140)
        para(c, T(dsc), RX, top + 40, RW)
    swatch_row(c, RX, 212, mono, w=27, gap=5)
    heading(c, T("mono_t"), RX, 244, max_w_pt=140)
    para(c, T("mono_d"), RX, 250, RW)

    heading(c, T("meaning_t"), RX, 306, size=8.2, max_w_pt=140)
    c.setFont(REG, 5.6)
    c.setFillColorRGB(.2, .2, .2)
    c.drawCentredString(X(RX), Y(315), T("meaning_sub"))
    label_cols = [hue_rgb(4), hue_rgb(2), (.90, .72, 0), hue_rgb(10), hue_rgb(8), hue_rgb(6),
                  (0, 0, 0), (.4, .4, .4), (.72, .72, .72), (.50, .32, .16),
                  (.82, .62, .25), (.88, .80, .50)]
    y = 331
    for (lab, txt), col in zip(T("meanings1"), label_cols):
        c.setFont(BOLD, 6.2)
        c.setFillColorRGB(*col)
        c.drawCentredString(X(RX), Y(y), lab)
        c.setFont(REG, 5.6)
        c.setFillColorRGB(.1, .1, .1)
        c.drawCentredString(X(RX), Y(y + 9), txt)
        y += 19.2

    # ---- cold / warm texts
    heading(c, T("cold_t"), 166, 99, size=7.6, align="left", max_w_pt=100)
    para(c, T("cold_d"), 166, 104, 88, size=6.2, leading=7.6, align="left")
    heading(c, T("warm_t"), 484, 82, size=7.6, align="left", max_w_pt=115)
    para(c, T("warm_d"), 484, 87, 112, size=6.2, leading=7.6, align="left")

    # ---- wheel
    draw_ryb_wheel(c, X(347), Y(265), 172, segments=12)

    # ---- complementary block + schemes
    draw_mini_ryb(c, X(200), Y(418), 25, picks=[4, 10])
    heading(c, T("comp_t1"), 212, 458, size=8, max_w_pt=100)
    heading(c, T("comp_t2"), 212, 468, size=8, max_w_pt=100)
    last = para(c, T("comp_d"), 160, 473, 106, size=6.2, leading=7.6, align="left")
    nxt_top = (H - last) / SY + 6                       # px just below paragraph 1
    para(c, T("comp_d2"), 160, nxt_top, 106, size=6.2, leading=7.6, align="left")

    gcol, rcol = hue_rgb(10), hue_rgb(4)
    for k, (outer, inner) in enumerate([(gcol, rcol), (rcol, gcol)]):
        bx, by = X(272), Y(478 + k * 27) - 21
        c.setFillColorRGB(*outer)
        c.roundRect(bx, by, 36, 21, 3, fill=1, stroke=0)
        c.setFillColorRGB(*inner)
        c.roundRect(bx + 10, by + 5, 16, 11, 2, fill=1, stroke=0)

    scheme_item(c, 345, 497, 24, [0, 4, 8], T("sch_triadic"))
    scheme_item(c, 468, 493, 24, [1, 3, 7, 9], T("sch_rect"))
    scheme_item(c, 366, 546, 24, [0, 5, 7], T("sch_split"))
    scheme_item(c, 512, 546, 24, [0, 3, 6, 9], T("sch_square"))


# ==========================================================================
# 5. PAGE 2  (HSB / RGB colour disc, models, properties, harmonies)
# ==========================================================================
INK = (0.18, 0.18, 0.18)


def hsb(h, s, v):
    """Hue in degrees, s and v in 0..1 -> RGB tuple."""
    return colorsys.hsv_to_rgb((h % 360) / 360.0, max(0, min(1, s)), max(0, min(1, v)))


def make_disc_image(size=1000, ss=4):
    """
    Hue/saturation disc (value = 1) as an anti-aliased RGBA bitmap.
    Hue = polar angle (red at 3 o'clock, counter-clockwise: yellow, green,
    cyan, blue, magenta); saturation grows from white at the centre to the
    pure hue at the rim.
    """
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (size, size), (255, 255, 255))
    px = img.load()
    cen, R = (size - 1) / 2.0, size / 2.0
    for j in range(size):
        dy = cen - j
        for i in range(size):
            dx = i - cen
            s = min(math.hypot(dx, dy) / R, 1.0)
            h6 = (math.degrees(math.atan2(dy, dx)) % 360.0) / 60.0
            k = int(h6)
            f = h6 - k
            p, q, t = 1 - s, 1 - s * f, 1 - s * (1 - f)
            r, g, b = ((1, t, p), (q, 1, p), (p, 1, t), (p, q, 1), (t, p, 1), (1, p, q))[k % 6]
            px[i, j] = (int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5))
    mask = Image.new("L", (size * ss, size * ss), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size * ss - 1, size * ss - 1), fill=255)
    img.putalpha(mask.resize((size, size), Image.LANCZOS))
    return img


def circle_clip(c, x, y, r):
    p = c.beginPath()
    p.circle(x, y, r)
    c.clipPath(p, stroke=0, fill=0)


def venn(c, cx, cy, r, cols, mode):
    """Three overlapping circles; overlaps are computed per colour model:
    mode='multiply' (subtractive/ink), 'add' (light) or 'ryb' (cols are RYB
    pigment amounts, mixed on the RYB cube)."""
    def comb(*cs):
        if mode == "ryb":
            return ryb_to_rgb(*(min(1.0, sum(col[k] for col in cs)) for k in range(3)))
        if mode == "add":
            return tuple(min(1.0, sum(col[k] for col in cs)) for k in range(3))
        out = [1.0, 1.0, 1.0]
        for col in cs:
            out = [out[k] * col[k] for k in range(3)]
        return tuple(out)

    d = r * 0.95
    ctr = [(cx, cy + d * 0.62), (cx - d * 0.72, cy - d * 0.42), (cx + d * 0.72, cy - d * 0.42)]
    for (x, y), col in zip(ctr, cols):
        c.setFillColorRGB(*comb(col))
        c.circle(x, y, r, stroke=0, fill=1)
    for i, j in ((0, 1), (0, 2), (1, 2)):
        c.saveState()
        circle_clip(c, ctr[i][0], ctr[i][1], r)
        c.setFillColorRGB(*comb(cols[i], cols[j]))
        c.circle(ctr[j][0], ctr[j][1], r, stroke=0, fill=1)
        c.restoreState()
    c.saveState()
    circle_clip(c, ctr[0][0], ctr[0][1], r)
    circle_clip(c, ctr[1][0], ctr[1][1], r)
    c.setFillColorRGB(*comb(*cols))
    c.circle(ctr[2][0], ctr[2][1], r, stroke=0, fill=1)
    c.restoreState()
    c.setStrokeColorRGB(.78, .78, .78)
    c.setLineWidth(.35)
    for (x, y) in ctr:
        c.circle(x, y, r, stroke=1, fill=0)


def prop_style(mode):
    """-> (hue_fn(theta), outer (s,v), inner (s,v), spoke colour) for a wheel."""
    def dist_top(theta):                       # 0 at the top, 1 at the bottom
        return abs(((theta - 90 + 180) % 360) - 180) / 180.0
    if mode == "warm":
        return (lambda th, i: 60 - 85 * dist_top(th)), (1, 1), (.42, 1), (1, 1, 1)
    if mode == "cool":
        return (lambda th, i: 150 + 135 * dist_top(th)), (1, 1), (.42, 1), (1, 1, 1)
    if mode == "saturated":
        return (lambda th, i: th), (1, 1), (.42, 1), (1, 1, 1)
    if mode == "desaturated":
        return (lambda th, i: th), (.36, .97), (.16, 1), (1, 1, 1)
    if mode == "bright":
        return (lambda th, i: th), (.62, 1), (.26, 1), (1, 1, 1)
    if mode == "dark":
        return (lambda th, i: th), (1, .46), (1, .26), (.06, .06, .06)
    if mode == "mono":
        return (lambda th, i: 335), None, None, (1, 1, 1)
    raise ValueError(mode)


def draw_prop_wheel(c, cx, cy, r, mode):
    hue_fn, outer, inner, spoke = prop_style(mode)
    r0, r1 = 0.20 * r, 0.56 * r
    for i in range(12):
        th = 30 * i
        if mode == "mono":                      # pinks of varying strength
            s_o = (.30, .55, .80, .45, .70, .38)[i % 6]
            col_o = hsb(335, s_o, 1)
            col_i = hsb(335, s_o * .55, 1)
        else:
            col_o = hsb(hue_fn(th, i), *outer)
            col_i = hsb(hue_fn(th, i), *inner)
        fill_poly(c, ring_wedge(cx, cy, r1, r, th - 15, th + 15, 6), col_o, spoke, .5)
        fill_poly(c, ring_wedge(cx, cy, r0, r1, th - 15, th + 15, 6), col_i, spoke, .5)
    c.setFillColorRGB(*((.18, .18, .18) if mode == "dark" else (.97, .97, .97)))
    c.setStrokeColorRGB(*spoke)
    c.setLineWidth(.5)
    c.circle(cx, cy, r0, stroke=1, fill=1)


def harmony_spec(i):
    """-> (marker (angle, radius-factor) list, line style)."""
    return [
        ([(60, .8), (90, .8), (120, .8)], "poly_open"),                    # analogous
        ([(90, .8), (270, .8)], "poly_open"),                              # complementary
        ([(90, .8), (210, .8), (330, .8)], "spokes"),                      # triad
        ([(90, .8), (240, .8), (300, .8)], "spokes"),                      # split compl.
        ([(90, .8), (120, .8), (270, .8), (300, .8)], "poly_closed"),      # tetrad
        ([(90, .88), (90, .66), (90, .44)], "none"),                       # monochromatic
        ([(90, .8), (0, .8), (270, .8), (180, .8)], "cross"),              # square
    ][i]


def draw_harmony_wheel(c, cx, cy, r, i):
    draw_prop_wheel(c, cx, cy, r, "saturated")
    marks, style = harmony_spec(i)
    pts = [pol(cx, cy, r * f, a) for a, f in marks]
    c.setStrokeColorRGB(.12, .12, .12)
    c.setLineWidth(.7)
    if style in ("poly_open", "poly_closed"):
        p = c.beginPath()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        if style == "poly_closed":
            p.close()
        c.drawPath(p, fill=0, stroke=1)
    elif style == "spokes":
        for q in pts:
            c.line(cx, cy, q[0], q[1])
    elif style == "cross":
        c.line(pts[0][0], pts[0][1], pts[2][0], pts[2][1])
        c.line(pts[1][0], pts[1][1], pts[3][0], pts[3][1])
    elif style == "none":
        c.line(cx, cy, pts[0][0], pts[0][1])
    for (px, py) in pts:
        c.setFillColorRGB(1, 1, 1)
        c.setStrokeColorRGB(.12, .12, .12)
        c.setLineWidth(.7)
        c.circle(px, py, r * 0.085, stroke=1, fill=1)


def build_page_2(c):
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    tracked(c, T("title2"), W / 2, 566, BOLD, 26, INK, tracking=3.2,
            align="center", max_w=470)

    # ---------------------------------------------------------------- models
    LXL = 26
    tracked(c, T("models_h"), LXL, 528, BOLD, 10.5, INK, 1.6, max_w=170)
    models = [
        ("m_cmyk", [(.0, .63, .89), (.90, .0, .50), (1, .93, 0)][::1], "multiply"),
        ("m_rgb", [(1, 0, 0), (0, 1, 0), (0, 0, 1)], "add"),
        ("m_hsb", [(.95, .0, .45), (.98, .78, .84), (.20, .20, .22)], "multiply"),
        ("m_gray", [(.08, .08, .08), (.90, .90, .90), (.45, .45, .45)], "multiply"),
    ]
    # circle order in venn(): top, left, right
    venn_cols = {
        "m_cmyk": [(.90, .0, .50), (1, .93, 0), (0, .63, .89)],     # M top, Y left, C right
        "m_rgb": [(1, 0, 0), (0, .85, 0), (0, .2, 1)],
        "m_hsb": [(.95, .0, .45), (.98, .78, .84), (.20, .20, .22)],
        "m_gray": [(.08, .08, .08), (.90, .90, .90), (.45, .45, .45)],
    }
    top = 514
    for key, _cols, mode in models:
        name, d1, d2 = T(key)
        c.setFont(BOLD, 6.4)
        c.setFillColorRGB(*INK)
        c.drawString(LXL, top - 6, name)
        c.setFont(REG, 5.3)
        c.setFillColorRGB(.3, .3, .3)
        y = top - 14.5
        c.drawString(LXL, y, d1)
        for ln in simpleSplit(d2, REG, 5.3, 165):
            y -= 6.6
            c.drawString(LXL, y, ln)
        venn(c, LXL + 21, top - 45, 9.5, venn_cols[key], mode)
        top -= 65

    # ------------------------------------------------------------------ disc
    if not hasattr(build_page_2, "_disc"):
        build_page_2._disc = ImageReader(make_disc_image())
    R = 125
    c.drawImage(build_page_2._disc, W / 2 - R, 412 - R, 2 * R, 2 * R, mask="auto")

    # -------------------------------------------------------------- meanings
    RXL = 592
    tracked(c, T("meanings_h"), RXL, 528, BOLD, 10.5, INK, 1.6, max_w=182)
    sw = [(1, .10, .05), (1, 0, .50), (1, .87, 0), (.40, .95, .10), (1, .60, 0),
          (.27, .40, 1), (.45, .10, 1), (.40, .20, 0), (.70, .70, .70),
          (.10, .10, .10), (.94, .94, .94)]
    top = 514
    for col, txt in zip(sw, T("meanings2")):
        c.setFillColorRGB(*col)
        c.rect(RXL, top - 12, 12, 12, stroke=0, fill=1)
        c.setFont(BOLD, 5.0)
        c.setFillColorRGB(.25, .25, .25)
        y = top - 4.8
        for ln in simpleSplit(txt, BOLD, 5.0, 160)[:2]:
            c.drawString(RXL + 18, y, ln)
            y -= 6.2
        top -= 21.5

    # ------------------------------------------------------------ properties
    xs = [66 + 110 * k for k in range(7)]
    tracked(c, T("properties_h"), W / 2, 258, BOLD, 10.5, INK, 1.6,
            align="center", max_w=300)
    modes = ["warm", "cool", "saturated", "desaturated", "bright", "dark", "mono"]
    for x, m, lab in zip(xs, modes, T("properties")):
        draw_prop_wheel(c, x, 212, 31, m)
        tracked(c, lab, x, 169, BOLD, 5.6, INK, .5, align="center", max_w=100)

    # ------------------------------------------------------------- harmonies
    tracked(c, T("harmonies_h"), W / 2, 136, BOLD, 10.5, INK, 1.6,
            align="center", max_w=300)
    for k, (x, lab) in enumerate(zip(xs, T("harmonies"))):
        draw_harmony_wheel(c, x, 92, 31, k)
        tracked(c, lab, x, 49, BOLD, 5.6, INK, .5, align="center", max_w=104)


# ==========================================================================
# 6. HELPERS FOR PAGES 3-6
# ==========================================================================
WHITE, BLACK, GREY = (1, 1, 1), (0, 0, 0), (.5, .5, .5)


def page_start(c, title_key):
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    tracked(c, T(title_key), W / 2, 566, BOLD, 26, INK, tracking=3.2,
            align="center", max_w=600)


def caption(c, x, y, head, desc, width, align="center", size=5.8, cols=(INK, (.3, .3, .3))):
    """Section heading at baseline y with a wrapped description below it."""
    tracked(c, head, x, y, BOLD, 8.4, cols[0], 1.2, align=align, max_w=width)
    c.setFont(REG, size)
    c.setFillColorRGB(*cols[1])
    yy = y - 11
    for ln in simpleSplit(desc, REG, size, width):
        (c.drawCentredString if align == "center" else c.drawString)(x, yy, ln)
        yy -= size * 1.3


def ring_text(c, text, cx, cy, r, mid, size, color, max_w, font=BOLD):
    """Text along an arc, visually centred on radius r, upright on both halves."""
    size = fit_size(text, font, size, max_w, 0.3)
    inward = math.sin(math.radians(mid)) < -1e-9
    rb = r + size * 0.36 if inward else r - size * 0.36
    arc_text(c, text, cx, cy, rb, mid, font, size, color, inward, 0.3)


def radial_text(c, text, cx, cy, r0, mid, size, color, font=BOLD):
    """Text along the radius at angle mid, starting at r0 and reading outward
    (kept upright by flipping it on the left half)."""
    c.saveState()
    c.translate(cx, cy)
    c.setFillColorRGB(*color)
    c.setFont(font, size)
    if math.cos(math.radians(mid)) >= -1e-9:
        c.rotate(mid)
        c.drawString(r0, -size * 0.36, text)
    else:
        c.rotate(mid + 180)
        c.drawRightString(-r0, -size * 0.36, text)
    c.restoreState()


def ring_wheel(c, cx, cy, radii, n, colour_fn, lw=0.5, stroke=WHITE):
    """Concentric rings of n cells, radii from outside in; colour_fn(i, k)
    gives hue i (clockwise from the top) in ring k (0 = outermost)."""
    step = 360.0 / n
    for k in range(len(radii) - 1):
        for i in range(n):
            mid = 90 - step * i
            fill_poly(c, ring_wedge(cx, cy, radii[k + 1], radii[k], mid - step / 2,
                                    mid + step / 2, 6), colour_fn(i, k), stroke, lw)


def hex_rgb(code):
    return tuple(int(code[k:k + 2], 16) / 255.0 for k in (0, 2, 4))


# ==========================================================================
# 7. PAGE 3  (hue x lightness: cross, tints / tones / shades, RGB hexagon)
# ==========================================================================
def draw_hue_cross(c, x0, top, cell, cols=19, rows=38, arm=(8, 15), stem=(6, 13)):
    """Cross of swatches. Rows step through the hues (from magenta, via red and
    yellow, round to violet); columns go from tint (+ white, left) through the
    pure hue (centre) to shade (+ black, right). Only cells in the long stem
    or the arm are drawn."""
    mid = (cols - 1) / 2.0
    for j in range(rows):
        base = hsb(300 + j * 360.0 / rows, 1, 1)
        for i in range(cols):
            if not (arm[0] <= j < arm[1] or stem[0] <= i < stem[1]):
                continue
            t = (i - mid) / mid * 0.92
            col = mix(base, WHITE, -t) if t < 0 else mix(base, BLACK, t)
            c.setFillColorRGB(*col)
            c.setStrokeColorRGB(1, 1, 1)
            c.setLineWidth(0.8)
            c.rect(x0 + i * cell, top - (j + 1) * cell, cell, cell, fill=1, stroke=1)
    ya = top - arm[0] * cell + 4
    tracked(c, T("plus_white"), x0, ya, BOLD, 5.6, INK, .4)
    tracked(c, T("plus_black"), x0 + cols * cell, ya, BOLD, 5.6, INK, .4,
            align="right")


def draw_tint_wheel(c, cx, cy, R, towards, fracs, n=24):
    """RYB hue wheel whose rings are mixed with `towards` (white = tints,
    grey = tones) by the fractions in fracs, from the rim inward."""
    radii = [R * (1 - 0.78 * k / len(fracs)) for k in range(len(fracs) + 1)]
    ring_wheel(c, cx, cy, radii, n,
               lambda i, k: mix(ryb_to_rgb(*hue_ryb(i * 12.0 / n)), towards, fracs[k]))
    c.setFillColorRGB(*mix(towards, WHITE, .0 if towards == WHITE else .15))
    c.setStrokeColorRGB(1, 1, 1)
    c.setLineWidth(.5)
    c.circle(cx, cy, radii[-1], stroke=1, fill=1)


def draw_shade_wheel(c, cx, cy, R):
    """12 RGB hues (red at the top) darkened with black ring by ring; the
    outer ring carries the hue names."""
    radii = [R, .70 * R, .52 * R, .36 * R, .21 * R]
    fracs = [0, .3, .55, .78]
    ring_wheel(c, cx, cy, radii, 12, lambda i, k: mix(hsb(30 * i, 1, 1), BLACK, fracs[k]),
               lw=.7)
    c.setFillColorRGB(.06, .06, .06)
    c.circle(cx, cy, radii[-1], stroke=0, fill=1)
    rm = (radii[0] + radii[1]) / 2
    for i, name in enumerate(T("shade_names")):
        mid = 90 - 30 * i
        ring_text(c, name, cx, cy, rm, mid, 5.4, text_on(hsb(30 * i, 1, 1)),
                  max_w=2 * math.pi * rm / 12 - 5)


def draw_rgb_hexagon(c, cx, cy, N, d):
    """Hexagon of hexagons: the three faces of the RGB cube that meet at the
    white corner, seen along the grey diagonal. A cell's offset from the
    centre is split along two of three axes 120 deg apart (remove blue ->
    up, remove green -> lower right, remove red -> lower left)."""
    axes = {2: (0.0, 1.0), 1: (math.cos(math.radians(-30)), math.sin(math.radians(-30))),
            0: (math.cos(math.radians(210)), math.sin(math.radians(210)))}
    pairs = ((2, 1), (1, 0), (0, 2))

    def colour(px, py):
        for i, j in pairs:
            (ax, ay), (bx, by) = axes[i], axes[j]
            det = ax * by - ay * bx
            a = (px * by - py * bx) / det
            b = (ax * py - ay * px) / det
            if a >= -1e-9 and b >= -1e-9:
                out = [1.0, 1.0, 1.0]
                out[i] -= a
                out[j] -= b
                return tuple(max(0.0, min(1.0, v)) for v in out)
        return WHITE

    e1 = (d * math.cos(math.radians(30)), d * math.sin(math.radians(30)))
    rc = d / math.sqrt(3)
    for q in range(-N, N + 1):
        for r in range(-N, N + 1):
            if abs(q + r) > N:
                continue
            x, y = q * e1[0], q * e1[1] + r * d
            pts = [pol(cx + x, cy + y, rc, 60 * k) for k in range(6)]
            fill_poly(c, pts, colour(x / (N * d), y / (N * d)), (.35, .35, .35), .25)
    names = T("rgb_names")                 # red, yellow, green, cyan, blue, magenta
    for name, ang in zip(names, (30, 90, 150, 210, 270, 330)):
        x, y = pol(cx, cy, N * d + rc + 9, ang)
        align = "left" if math.cos(math.radians(ang)) > .1 else (
            "right" if math.cos(math.radians(ang)) < -.1 else "center")
        tracked(c, name, x, y - 2.2, BOLD, 6.2, INK, .6, align=align)


def build_page_3(c):
    page_start(c, "title3")

    cell = 11
    draw_hue_cross(c, 30, 540, cell)
    caption(c, 30 + 19 * cell / 2, 106, T("cross_t"), T("cross_d"), 205)

    wheels = [(338, "tints", lambda x: draw_tint_wheel(c, x, 452, 76, WHITE,
                                                       [0, .18, .36, .54, .70, .84])),
              (510, "tones", lambda x: draw_tint_wheel(c, x, 452, 76, (.55, .55, .55),
                                                       [0, .22, .44, .62, .78])),
              (682, "shades", lambda x: draw_shade_wheel(c, x, 452, 76))]
    for x, key, draw in wheels:
        draw(x)
        caption(c, x, 362, T(key + "_t"), T(key + "_d"), 158)

    draw_rgb_hexagon(c, 418, 172, 8, 16.5)
    caption(c, 600, 236, T("hex_t"), T("hex_d"), 170, align="left")


# ==========================================================================
# 8. PAGE 4  (RYB / RGB / CMYK, CMYK star, web-safe palette)
# ==========================================================================
CMY_INKS = ((0.0, .62, .90), (.90, 0.0, .52), (1.0, .93, 0.0))


def cmy_to_rgb(cmy):
    """Cyan, magenta and yellow ink coverage (0..1) -> sRGB, by multiplying
    the filtering of each ink."""
    out = [1.0, 1.0, 1.0]
    for v, ink in zip(cmy, CMY_INKS):
        out = [o * (1 - v * (1 - ink[k])) for k, o in enumerate(out)]
    return tuple(out)


def draw_mix_system(c, x, cy, key, cols, mode, letters, comp, dark=False):
    head, l1, l2, comp_lbl = T(key)
    r = 29
    if dark:
        c.setFillColorRGB(.08, .08, .08)
        c.roundRect(x - 2.45 * r, cy - 1.85 * r, 4.9 * r, 3.75 * r, 6, stroke=0, fill=1)
    venn(c, x, cy, r, cols, mode)
    # big coloured letters
    size = 30
    widths = [stringWidth(ch, REG, size) for ch, _ in letters]
    lx = x - sum(widths) / 2
    for (ch, col), w in zip(letters, widths):
        c.setFillColorRGB(*col)
        c.setFont(REG, size)
        c.drawString(lx, cy - 92, ch)
        lx += w
    tracked(c, head, x, cy - 106, BOLD, 7.6, INK, 1.0, align="center", max_w=160)
    c.setFont(REG, 5.8)
    c.setFillColorRGB(.3, .3, .3)
    y = cy - 117
    for ln in simpleSplit(l1, REG, 5.8, 160) + simpleSplit(l2, REG, 5.8, 160):
        c.drawCentredString(x, y, ln)
        y -= 7.4
    tw = stringWidth(comp_lbl, BOLD, 5.8)
    sx = x - (tw + 26) / 2
    for k, col in enumerate(comp):
        c.setFillColorRGB(*col)
        c.rect(sx + k * 11, y - 3.5, 10, 10, stroke=0, fill=1)
    c.setFont(BOLD, 5.8)
    c.setFillColorRGB(*INK)
    c.drawString(sx + 26, y - 1, comp_lbl)


def draw_cmy_star(c, cx, cy, s):
    """Hexagram on a triangular lattice. Each small triangle gets C, M, Y ink
    values from its position: each ink grows toward its own point (cyan at the
    bottom, magenta upper left, yellow upper right) and every ink is 30 % in
    the centre; the values are rounded to steps of 10 %."""
    e1, e2 = (s, 0.0), (s / 2.0, s * math.sqrt(3) / 2)

    def P(i, j):
        return (i * e1[0] + j * e2[0], i * e1[1] + j * e2[1])

    o = P(3, 3)                                       # star centre

    def at(i, j):
        p = P(i, j)
        return (cx + p[0] - o[0], cy + p[1] - o[1])

    tri_a = [at(0, 0), at(9, 0), at(0, 9)]            # red point up
    tri_b = [at(6, 6), at(-3, 6), at(6, -3)]          # cyan point down

    def inside(p, tri):
        def side(a, b):
            return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        d = [side(tri[k], tri[(k + 1) % 3]) for k in range(3)]
        return all(v > 0 for v in d) or all(v < 0 for v in d)

    r_tip = math.hypot(tri_a[2][0] - cx, tri_a[2][1] - cy)
    r_cell = r_tip - s / math.sqrt(3)                 # centroid of a tip triangle
    gain = 0.7 / (0.5 * r_cell / r_tip)               # tip cells reach 100 %
    dirs = [pol(0, 0, 1, a) for a in (270, 150, 30)]  # C, M, Y

    for i in range(-4, 10):
        for j in range(-4, 10):
            for tri in ((at(i, j), at(i + 1, j), at(i, j + 1)),
                        (at(i + 1, j), at(i + 1, j + 1), at(i, j + 1))):
                g = (sum(p[0] for p in tri) / 3, sum(p[1] for p in tri) / 3)
                if not (inside(g, tri_a) or inside(g, tri_b)):
                    continue
                rel = ((g[0] - cx) / r_tip, (g[1] - cy) / r_tip)
                vals = [max(0, min(10, int(round(10 * (gain * (rel[0] * dx + rel[1] * dy) + .3)))))
                        for dx, dy in dirs]
                col = cmy_to_rgb([v / 10.0 for v in vals])
                fill_poly(c, list(tri), col, WHITE, .8)
                lines = ["%s%d" % (n, 10 * v) for n, v in zip("CMY", vals) if v]
                c.setFont(REG, 3.5)
                c.setFillColorRGB(*text_on(col))
                y = g[1] + (len(lines) - 1) * 2.0 - 1.2
                for ln in lines:
                    c.drawCentredString(g[0], y, ln)
                    y -= 4.0
    names = T("rgb_names")                            # red, yellow, green, cyan, blue, magenta
    for name, ang in zip(names, (90, 30, -30, -90, -150, 150)):
        x, y = pol(cx, cy, r_tip, ang)                # labels above / below each point
        y += 7 if ang > 0 else -13
        tracked(c, name, x, y, BOLD, 6.6, INK, .6, align="center")


def draw_web_safe(c, x0, top, cell):
    """216 web-safe colours: six 6x6 blocks (one per red level, 2 rows of 3);
    in a block rows change green and columns change blue."""
    digits = "0369CF"
    for rr in range(6):
        bx, by = x0 + (rr % 3) * 6 * cell, top - (rr // 3) * 6 * cell
        for g in range(6):
            for b in range(6):
                col = (rr / 5.0, g / 5.0, b / 5.0)
                x, y = bx + b * cell, by - (g + 1) * cell
                c.setFillColorRGB(*col)
                c.rect(x, y, cell, cell, stroke=0, fill=1)
                c.setFont(BOLD, 5.0)
                c.setFillColorRGB(*text_on(col))
                c.drawCentredString(x + cell / 2, y + cell / 2 - 1.8, digits[rr] + digits[g] + digits[b])
    c.setStrokeColorRGB(1, 1, 1)
    c.setLineWidth(1.6)
    for k in range(1, 3):
        c.line(x0 + 6 * k * cell, top, x0 + 6 * k * cell, top - 12 * cell)
    c.line(x0, top - 6 * cell, x0 + 18 * cell, top - 6 * cell)


def build_page_4(c):
    page_start(c, "title4")

    red, yel, blu = hue_rgb(4), hue_rgb(0), hue_rgb(8)
    draw_mix_system(c, 100, 478, "mix_ryb", [(1, 0, 0), (0, 1, 0), (0, 0, 1)], "ryb",
                    [("R", red), ("Y", (.95, .80, 0)), ("B", blu)], (red, hue_rgb(10)))
    draw_mix_system(c, 272, 478, "mix_rgb", [(1, 0, 0), (0, .85, 0), (0, .2, 1)], "add",
                    [("R", (1, .1, .1)), ("G", (0, .75, 0)), ("B", (0, .2, 1))],
                    ((1, 0, 0), (0, 1, 1)), dark=True)
    draw_mix_system(c, 444, 478, "mix_cmyk", [CMY_INKS[1], CMY_INKS[2], CMY_INKS[0]],
                    "multiply", [("C", (0, .70, .95)), ("M", CMY_INKS[1]), ("Y", (.95, .80, 0)),
                                 ("K", BLACK)], (CMY_INKS[0], cmy_to_rgb((0, 1, 1))))

    draw_web_safe(c, 30, 312, 19.5)
    caption(c, 395, 300, T("web_t"), T("web_d"), 125, align="left")

    draw_cmy_star(c, 662, 396, 23)
    caption(c, 662, 240, T("star_t"), T("star_d"), 200)


# ==========================================================================
# 9. PAGE 5  (overlapping-circles colour wheel, CSS named colours)
# ==========================================================================
# CSS colour keywords grouped by family (family order = css_families).
CSS_COLOURS = [
    [("crimson", "DC143C"), ("red", "FF0000"), ("firebrick", "B22222"), ("darkred", "8B0000"),
     ("indianred", "CD5C5C"), ("lightcoral", "F08080"), ("salmon", "FA8072"),
     ("tomato", "FF6347")],
    [("orangered", "FF4500"), ("coral", "FF7F50"), ("darkorange", "FF8C00"),
     ("orange", "FFA500")],
    [("sienna", "A0522D"), ("saddlebrown", "8B4513"), ("chocolate", "D2691E"),
     ("sandybrown", "F4A460"), ("peru", "CD853F"), ("burlywood", "DEB887"), ("tan", "D2B48C")],
    [("darkgoldenrod", "B8860B"), ("goldenrod", "DAA520"), ("gold", "FFD700"),
     ("khaki", "F0E68C"), ("olive", "808000"), ("yellow", "FFFF00")],
    [("yellowgreen", "9ACD32"), ("olivedrab", "6B8E23"), ("chartreuse", "7FFF00"),
     ("limegreen", "32CD32"), ("forestgreen", "228B22"), ("green", "008000"),
     ("darkgreen", "006400"), ("lime", "00FF00"), ("palegreen", "98FB98"),
     ("seagreen", "2E8B57"), ("mediumseagreen", "3CB371"), ("springgreen", "00FF7F")],
    [("aquamarine", "7FFFD4"), ("turquoise", "40E0D0"), ("lightseagreen", "20B2AA"),
     ("teal", "008080"), ("darkcyan", "008B8B"), ("cyan", "00FFFF"),
     ("darkturquoise", "00CED1"), ("cadetblue", "5F9EA0")],
    [("deepskyblue", "00BFFF"), ("skyblue", "87CEEB"), ("steelblue", "4682B4"),
     ("dodgerblue", "1E90FF"), ("cornflowerblue", "6495ED"), ("royalblue", "4169E1"),
     ("blue", "0000FF"), ("navy", "000080"), ("midnightblue", "191970"),
     ("slateblue", "6A5ACD")],
    [("mediumpurple", "9370DB"), ("blueviolet", "8A2BE2"), ("indigo", "4B0082"),
     ("darkviolet", "9400D3"), ("darkorchid", "9932CC"), ("purple", "800080"),
     ("plum", "DDA0DD"), ("violet", "EE82EE"), ("orchid", "DA70D6"), ("magenta", "FF00FF")],
    [("mediumvioletred", "C71585"), ("deeppink", "FF1493"), ("hotpink", "FF69B4"),
     ("palevioletred", "DB7093"), ("pink", "FFC0CB")],
    [("white", "FFFFFF"), ("silver", "C0C0C0"), ("gray", "808080"), ("black", "000000")],
]
CSS_FAMILY_COLOURS = ["FF0000", "FF8C00", "A0522D", "FFD700", "228B22", "00CED1", "1E90FF",
                      "8A2BE2", "FF69B4", "808080"]


def css_hue_key(hx):
    h, s, v = colorsys.rgb_to_hsv(*hex_rgb(hx))
    return ((h * 360 + 20) % 360, -v)


def draw_overlap_wheel(c, cx, cy, d):
    """Six RYB circles (yellow at the top) whose overlaps show the mixture of
    each pair of neighbours, inside a ring of the 12 hues darkened."""
    rc = 0.72 * d
    r0, r1 = d + rc + 5, d + rc + 48
    darks = [mix(hue_rgb(i), BLACK, .45) for i in range(12)]
    for i, name in enumerate(T("dark_names")):
        mid = 90 - 30 * i
        fill_poly(c, ring_wedge(cx, cy, r0, r1, mid - 15, mid + 15, 10), darks[i], WHITE, 1.4)
        ring_text(c, name, cx, cy, (r0 + r1) / 2, mid, 6.6, WHITE,
                  max_w=2 * math.pi * (r0 + r1) / 2 / 12 - 8)
    ctr = [pol(cx, cy, d, 90 - 60 * k) for k in range(6)]
    for k in range(6):
        c.setFillColorRGB(*hue_rgb(2 * k))
        c.circle(ctr[k][0], ctr[k][1], rc, stroke=0, fill=1)
    for k in range(6):
        nxt = ctr[(k + 1) % 6]
        c.saveState()
        circle_clip(c, ctr[k][0], ctr[k][1], rc)
        c.setFillColorRGB(*hue_rgb(2 * k + 1))
        c.circle(nxt[0], nxt[1], rc, stroke=0, fill=1)
        c.restoreState()
    c.setStrokeColorRGB(1, 1, 1)
    c.setLineWidth(1.2)
    for (x, y) in ctr:
        c.circle(x, y, rc, stroke=1, fill=0)
    names = T("hue_names")
    for k in range(6):
        ang = 90 - 60 * k
        x, y = pol(cx, cy, d + rc * .38, ang)
        tracked(c, names[2 * k], x, y - 2.5, BOLD, 7, text_on(hue_rgb(2 * k)), .5,
                align="center", max_w=rc * 1.25)
        x, y = pol(cx, cy, d * math.cos(math.radians(30)), ang - 30)
        lens = T("lens_names")[k]
        tracked(c, lens, x, y - 2.2, BOLD, 6.2, text_on(hue_rgb(2 * k + 1)), .3,
                align="center", max_w=2 * rc - d - 4)


def draw_css_wheel(c, cx, cy, r_out):
    fams = [sorted(f, key=lambda e: css_hue_key(e[1])) if k < 9 else f
            for k, f in enumerate(CSS_COLOURS)]
    flat = [e for f in fams for e in f]
    n = len(flat)
    step = 360.0 / n
    r_in, f_in, f_out = 0.53 * r_out, 0.30 * r_out, 0.50 * r_out
    for i, (name, hx) in enumerate(flat):
        mid = 90 - step * i
        col = hex_rgb(hx)
        fill_poly(c, ring_wedge(cx, cy, r_in, r_out, mid - step / 2, mid + step / 2, 4), col,
                  WHITE if luma(col) < .9 else (.8, .8, .8), .4)
        text = "%s  #%s" % (name, hx)
        size = fit_size(text, BOLD, 4.9, r_out - r_in - 6)
        radial_text(c, text, cx, cy, r_in + 3, mid, size, text_on(col))
    i = 0
    for fam, name, hx in zip(fams, T("css_families"), CSS_FAMILY_COLOURS):
        a0 = 90 - step * (i - .5)
        a1 = a0 - step * len(fam)
        col = hex_rgb(hx)
        fill_poly(c, ring_wedge(cx, cy, f_in, f_out, a1, a0, 16), col, WHITE, 1.2)
        rm = (f_in + f_out) / 2
        ring_text(c, name, cx, cy, rm, (a0 + a1) / 2, 6.0, text_on(col),
                  max_w=math.radians(a0 - a1) * rm - 4)
        i += len(fam)


def build_page_5(c):
    page_start(c, "title5")
    caption(c, 205, 528, T("wheel5_t"), T("wheel5_d"), 300)
    draw_overlap_wheel(c, 205, 282, 80)
    caption(c, 592, 528, T("css_t"), T("css_d"), 300)
    draw_css_wheel(c, 592, 282, 192)


# ==========================================================================
# 10. PAGE 6  (Plutchik's wheel, spiral rosette, translucent petals)
# ==========================================================================
EMOTION_HUES = [52, 90, 140, 190, 220, 285, 355, 28]   # joy ... anticipation (hsb)


def draw_plutchik(c, cx, cy, R):
    """Eight petals, clockwise from joy at the top. Each petal is a full
    45-degree sector up to r_full and then tapers to a tip at R; it is cut in
    three bands (intense, basic, mild)."""
    r_c, r_full = .12 * R, .60 * R
    bands = (.12 * R, .37 * R, .63 * R, R)

    def half_angle(r):
        if r <= r_full:
            return 22.5
        hw = r_full * math.sin(math.radians(22.5)) * \
            math.cos(math.pi / 2 * (r - r_full) / (R - r_full)) ** .8
        return math.degrees(math.asin(min(1.0, hw / r)))

    def band_poly(a, lo, hi, steps=14):
        rs = [lo + (hi - lo) * k / steps for k in range(steps + 1)]
        right = [pol(cx, cy, r, a - half_angle(r)) for r in rs]
        left = [pol(cx, cy, r, a + half_angle(r)) for r in reversed(rs)]
        w_hi, w_lo = half_angle(hi), half_angle(lo)
        top = [pol(cx, cy, hi, a - w_hi + 2 * w_hi * k / 8) for k in range(1, 8)]
        bot = [pol(cx, cy, lo, a + w_lo - 2 * w_lo * k / 8) for k in range(1, 8)]
        return right + top + left + bot

    for k, (words, h) in enumerate(zip(T("emotions"), EMOTION_HUES)):
        a = 90 - 45 * k
        base = hsb(h, .9, 1)
        cols = (mix(hsb(h, 1, 1), BLACK, .22), base, mix(base, WHITE, .55))
        for b in range(3):
            fill_poly(c, band_poly(a, bands[b], bands[b + 1]), cols[b], WHITE, 1.2)
            rm = (bands[b] + bands[b + 1]) / 2 if b < 2 else bands[2] + .33 * (R - bands[2])
            # horizontal text: its width spreads across the petal (tangential)
            # and along it (radial) according to the petal's angle
            across = 2 * rm * math.sin(math.radians(half_angle(rm))) - 9
            along = 2 * (rm - bands[b]) - 6
            ca, sa = abs(math.cos(math.radians(a))), abs(math.sin(math.radians(a)))
            width = min(along / ca if ca > 1e-6 else 1e9, across / sa if sa > 1e-6 else 1e9)
            x, y = pol(cx, cy, rm, a)
            tracked(c, words[b], x, y - 2.3, BOLD, 6.6 if b == 1 else 5.8,
                    text_on(cols[b]), .3, align="center", max_w=width)
    c.setFillColorRGB(1, 1, 1)
    c.circle(cx, cy, r_c, stroke=0, fill=1)
    for k, word in enumerate(T("dyads")):
        a = 90 - 45 * k - 22.5
        x, y = pol(cx, cy, .86 * R, a)
        col = mix(mix(hsb(EMOTION_HUES[k], 1, 1), hsb(EMOTION_HUES[(k + 1) % 8], 1, 1), .5),
                  BLACK, .35)
        tracked(c, word, x, y - 2, BOLD, 5.8, col, .3, align="center", max_w=62)


def draw_rosette(c, cx, cy, R, rings=15, n=24, twist=8.0):
    """Rings of n cells, each ring turned `twist` degrees further than the
    one inside. A cell keeps the hue of its column i, so each hue winds
    outward in a spiral arm; saturation grows and value falls toward the rim."""
    step = 360.0 / n
    radii = [R * ((k + 1) / float(rings)) ** .85 for k in range(rings)]
    for k in range(1, rings):
        t = (k + 1) / float(rings)
        for i in range(n):
            a0 = i * step + k * twist
            pts = ring_wedge(cx, cy, radii[k - 1], radii[k], a0, a0 + step, 4)
            col = hsb(i * step, .12 + .88 * t, 1 - .62 * t ** 2.2)
            fill_poly(c, pts, col, (.05, .05, .05), .35)
    c.setFillColorRGB(1, 1, 1)
    c.circle(cx, cy, radii[0], stroke=0, fill=1)


def draw_petals(c, cx, cy, L, n=24):
    """Two crowns of translucent pointed petals; overlaps blend by alpha."""
    def petal(ang, length, width, col):
        a = math.radians(ang)
        ux, uy = math.cos(a), math.sin(a)
        vx, vy = -uy, ux
        tip = (cx + ux * length, cy + uy * length)
        p = c.beginPath()
        p.moveTo(cx, cy)
        p.curveTo(cx + ux * length * .3 + vx * width, cy + uy * length * .3 + vy * width,
                  cx + ux * length * .75 + vx * width * .8, cy + uy * length * .75 + vy * width * .8,
                  *tip)
        p.curveTo(cx + ux * length * .75 - vx * width * .8, cy + uy * length * .75 - vy * width * .8,
                  cx + ux * length * .3 - vx * width, cy + uy * length * .3 - vy * width,
                  cx, cy)
        p.close()
        c.setFillColorRGB(*col)
        c.drawPath(p, fill=1, stroke=0)

    c.saveState()
    c.setFillAlpha(.45)
    for i in range(n):
        ang = 90 - 360.0 * i / n
        petal(ang, L, L * .19, hsb(360.0 * i / n, .75, 1))
    for i in range(n):
        ang = 90 - 360.0 * (i + .5) / n
        petal(ang, L * .62, L * .13, hsb(360.0 * (i + .5) / n, 1, .8))
    c.restoreState()


def build_page_6(c):
    page_start(c, "title6")
    caption(c, 210, 528, T("plutchik_t"), T("plutchik_d"), 330)
    draw_plutchik(c, 210, 290, 200)

    x0, y0, side = 432, 316, 196
    c.setFillColorRGB(.03, .03, .03)
    c.rect(x0, y0, side, side, stroke=0, fill=1)
    draw_rosette(c, x0 + side / 2, y0 + side / 2, side * .46)
    caption(c, 645, 470, T("rosette_t"), T("rosette_d"), 125, align="left")

    draw_petals(c, x0 + side / 2, 170, 100)
    caption(c, 645, 200, T("petals_t"), T("petals_d"), 125, align="left")


# ==========================================================================
# 11. PAGE 7  (The Color Wheel with names, spiral sphere)
# ==========================================================================
# How far each colour is pushed toward white (+) or black (-): lenses
# clockwise from red/violet, ring cells clockwise from the top.
CW_LENS_TWEAK = [-.45, -.3, .3, .12, 0, .08]
CW_RING_TWEAK = [-.22, 0, -.38, .45, -.45, -.3, -.42, .25, 0, .1, .15, 0]


def tweak(col, t):
    return mix(col, WHITE, t) if t >= 0 else mix(col, BLACK, -t)


def draw_named_wheel(c, cx, cy, d):
    """Six RYB circles of radius d (red at the top), all passing through the
    centre. Two neighbours overlap in a lens of their mixture; near the
    centre three circles meet and the middle hue is darkened. A ring of the
    12 hues in between shows in the gaps between the circles."""
    r0, r1 = 1.5 * d, 2.24 * d
    ring_cols = [tweak(ryb_to_rgb(*hue_ryb(4.5 + j)), t) for j, t in enumerate(CW_RING_TWEAK)]
    for j, col in enumerate(ring_cols):
        mid = 75 - 30 * j
        fill_poly(c, ring_wedge(cx, cy, r0, r1, mid - 15, mid + 15, 10), col, WHITE, 1.6)
    ctr = [pol(cx, cy, d, 90 - 60 * k) for k in range(6)]
    hues = [hue_rgb(4 + 2 * k) for k in range(6)]
    lenses = [tweak(hue_rgb(5 + 2 * k), t) for k, t in enumerate(CW_LENS_TWEAK)]

    def fill_inside(clips, k, col):
        """Fill circle k, clipped to the circles in `clips`."""
        c.saveState()
        for q in clips:
            circle_clip(c, ctr[q % 6][0], ctr[q % 6][1], d)
        c.setFillColorRGB(*col)
        c.circle(ctr[k % 6][0], ctr[k % 6][1], d, stroke=0, fill=1)
        c.restoreState()

    for k in range(6):
        fill_inside([], k, hues[k])
    for k in range(6):
        fill_inside([k], k + 1, lenses[k])
    # circles k-1 and k+1 meet in a lens from the centre to the centre of
    # circle k, which lies wholly inside circle k (one clip is enough)
    for k in range(6):
        fill_inside([k - 1], k + 1, tweak(hues[k], -.35))
    c.setStrokeColorRGB(1, 1, 1)
    c.setLineWidth(1.6)
    for (x, y) in ctr:
        c.circle(x, y, d, stroke=1, fill=0)

    rm = 2.09 * d
    for j, name in enumerate(T("cw_ring")):
        ring_text(c, name, cx, cy, rm, 75 - 30 * j, 8, text_on(ring_cols[j]),
                  max_w=math.radians(22) * rm)
    for k, name in enumerate(T("cw_circles")):
        x, y = pol(cx, cy, 1.5 * d, 90 - 60 * k)
        tracked(c, name, x, y - 3, BOLD, 8.5, text_on(hues[k]), .4,
                align="center", max_w=.8 * d)
    for k, name in enumerate(T("cw_lenses")):
        x, y = pol(cx, cy, 1.07 * d, 60 - 60 * k)
        tracked(c, name, x, y - 2.6, BOLD, 7.4, text_on(lenses[k]), .3,
                align="center", max_w=.72 * d)


def draw_spiral_sphere(c, cx, cy, R, n=36):
    """n circles of radius R/2 through the centre. Circles j and k cross a
    second time at R/2 * (u_j + u_k), so the crossings form a lattice of
    curved four-sided cells that wind outward in spirals. A cell takes the
    hue of circle j, and is shaded like a sphere lit from the upper right
    (diffuse light plus a white highlight)."""
    r = R / 2.0
    lx, ly, lz = .24, .3, .92
    ln = math.sqrt(lx * lx + ly * ly + lz * lz)
    lx, ly, lz = lx / ln, ly / ln, lz / ln

    def arc(k, a, b, steps=4):
        """Points on circle k from angle index a toward b (end excluded)."""
        ak = 2 * math.pi * k / n
        ox, oy = cx + r * math.cos(ak), cy + r * math.sin(ak)
        return [(ox + r * math.cos(2 * math.pi * (a + (b - a) * s / steps) / n),
                 oy + r * math.sin(2 * math.pi * (a + (b - a) * s / steps) / n))
                for s in range(steps)]

    for m in range(1, n // 2):
        for j in range(n):
            k = j + m
            pts = arc(k, j, j + 1) + arc(j + 1, k, k + 1) + arc(k + 1, j + 1, j) + \
                arc(j, k + 1, k)
            px = (sum(p[0] for p in pts) / len(pts) - cx) / R
            py = (sum(p[1] for p in pts) / len(pts) - cy) / R
            pz = math.sqrt(max(0.0, 1 - px * px - py * py))
            lit = max(0.0, px * lx + py * ly + pz * lz)
            col = tweak(hsb(125 - 360.0 * j / n, 1, .1 + .9 * lit ** 1.6), lit ** 9)
            fill_poly(c, pts, col, mix(col, BLACK, .3), .4)


def build_page_7(c):
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(1.2)
    c.rect(20, 20, 420, 572, stroke=1, fill=0)
    tracked(c, T("cw_title"), 230, 532, REG, 30, INK, 2.5, align="center", max_w=390)
    draw_named_wheel(c, 230, 262, 88)

    c.setFillColorRGB(.02, .02, .02)
    c.rect(452, 20, 320, 572, stroke=0, fill=1)
    draw_spiral_sphere(c, 612, 372, 145)
    caption(c, 612, 180, T("sphere_t"), T("sphere_d"), 250, size=6.6,
            cols=(WHITE, (.75, .75, .75)))


# ==========================================================================
# 12. PAGE 8  (CIE 1931 chromaticity diagram, visible spectrum)
# ==========================================================================
# CIE 1931 chromaticity (x, y) of the pure spectral colours, 380-700 nm
# every 5 nm (the official table; the Gaussian fit below drifts at the ends).
SPECTRAL_LOCUS = [
    (.1741, .0050), (.1740, .0050), (.1738, .0049), (.1736, .0049), (.1733, .0048),
    (.1730, .0048), (.1726, .0048), (.1721, .0048), (.1714, .0051), (.1703, .0058),
    (.1689, .0069), (.1669, .0086), (.1644, .0109), (.1611, .0138), (.1566, .0177),
    (.1510, .0227), (.1440, .0297), (.1355, .0399), (.1241, .0578), (.1096, .0868),
    (.0913, .1327), (.0687, .2007), (.0454, .2950), (.0235, .4127), (.0082, .5384),
    (.0039, .6548), (.0139, .7502), (.0389, .8120), (.0743, .8338), (.1142, .8262),
    (.1547, .8059), (.1929, .7816), (.2296, .7543), (.2658, .7243), (.3016, .6923),
    (.3373, .6589), (.3731, .6245), (.4087, .5896), (.4441, .5547), (.4788, .5202),
    (.5125, .4866), (.5448, .4544), (.5752, .4242), (.6029, .3965), (.6270, .3725),
    (.6482, .3514), (.6658, .3340), (.6801, .3197), (.6915, .3083), (.7006, .2993),
    (.7079, .2920), (.7140, .2859), (.7190, .2809), (.7230, .2770), (.7260, .2740),
    (.7283, .2717), (.7300, .2700), (.7311, .2689), (.7320, .2680), (.7327, .2673),
    (.7334, .2666), (.7340, .2660), (.7344, .2656), (.7346, .2654), (.7347, .2653),
]


def locus_xy(lam):
    """Chromaticity of wavelength lam (nm), interpolated in SPECTRAL_LOCUS
    with a Catmull-Rom spline."""
    n = len(SPECTRAL_LOCUS)
    t = min(max((lam - 380) / 5.0, 0), n - 1)
    i = min(int(t), n - 2)
    f = t - i
    p0, p1, p2, p3 = (SPECTRAL_LOCUS[min(max(k, 0), n - 1)] for k in (i - 1, i, i + 1, i + 2))
    return tuple(.5 * (2 * b + (c - a) * f + (2 * a - 5 * b + 4 * c - d) * f * f
                       + (3 * b - a - 3 * c + d) * f ** 3) for a, b, c, d in zip(p0, p1, p2, p3))


def cmf(lam):
    """CIE 1931 2-degree colour-matching functions x, y, z at wavelength lam
    (nm), from the multi-lobe Gaussian fit of Wyman, Sloan & Shirley (2013)."""
    def g(mu, s1, s2):
        return math.exp(-.5 * ((lam - mu) / (s1 if lam < mu else s2)) ** 2)
    return (1.056 * g(599.8, 37.9, 31.0) + .362 * g(442.0, 16.0, 26.7)
            - .065 * g(501.1, 20.4, 26.2),
            .821 * g(568.8, 46.9, 40.5) + .286 * g(530.9, 16.3, 31.1),
            1.217 * g(437.0, 11.8, 36.0) + .681 * g(459.0, 26.0, 13.8))


def xy_of(xyz):
    s = sum(xyz)
    return xyz[0] / s, xyz[1] / s


def xyz_to_linear_srgb(X, Y, Z):
    return (3.2406 * X - 1.5372 * Y - .4986 * Z,
            -.9689 * X + 1.8758 * Y + .0415 * Z,
            .0557 * X - .2040 * Y + 1.0570 * Z)


def srgb_gamma(v):
    v = max(0.0, min(1.0, v))
    return 12.92 * v if v <= .0031308 else 1.055 * v ** (1 / 2.4) - .055


def displayable(rgb):
    """Pull a linear RGB colour outside sRGB toward white (by adding grey)
    until no channel is negative."""
    lo = min(rgb)
    return tuple(v - lo for v in rgb) if lo < 0 else tuple(rgb)


def xy_colour(x, y):
    """Brightest displayable colour of chromaticity (x, y)."""
    rgb = displayable(xyz_to_linear_srgb(x / y, 1.0, max(0.0, 1 - x - y) / y))
    hi = max(rgb)
    return tuple(srgb_gamma(v / hi) for v in rgb)


def planck_xy(T):
    """Chromaticity of a black body at temperature T (kelvin)."""
    acc = [0.0, 0.0, 0.0]
    for lam in range(380, 785, 5):
        l = lam * 1e-9
        e = 1.0 / (l ** 5 * (math.exp(1.4388e-2 / (l * T)) - 1))
        for k, v in enumerate(cmf(lam)):
            acc[k] += e * v
    return xy_of(acc)


def make_cie_image(x1, y1, px):
    """Bitmap of xy_colour over [0, x1] x [0, y1], px pixels per unit."""
    from PIL import Image
    nx, ny = int(x1 * px), int(y1 * px)
    img = Image.new("RGB", (nx, ny))
    pix = img.load()
    for j in range(ny):
        y = (ny - j - .5) / px
        for i in range(nx):
            r, g, b = xy_colour((i + .5) / px, y)
            pix[i, j] = (int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5))
    return img


# Where each region name of cie_regions sits (x, y), and the marked
# colour temperatures on the Planckian locus.
CIE_REGION_XY = [(.13, .55), (.27, .64), (.39, .575), (.435, .535), (.475, .49), (.515, .448),
                 (.555, .36), (.605, .33), (.645, .295), (.44, .315), (.49, .22), (.40, .15),
                 (.31, .10), (.24, .065), (.20, .035), (.12, .11), (.11, .21), (.11, .34)]
CIE_KELVIN = [2000, 3000, 4000, 6500, 10000]
SRGB_XY = [(.64, .33), (.30, .60), (.15, .06)]


def draw_cie(c, ox, oy, s):
    def P(x, y):
        return ox + x * s, oy + y * s

    def polyline(pts, close=False):
        p = c.beginPath()
        p.moveTo(*P(*pts[0]))
        for q in pts[1:]:
            p.lineTo(*P(*q))
        if close:
            p.close()
        return p

    edge = [locus_xy(lam) for lam in range(380, 701)]

    c.setStrokeColorRGB(.65, .65, .65)
    c.setLineWidth(.4)
    c.setDash(1, 2)
    for k in range(1, 8):
        c.line(*P(k / 10.0, 0), *P(k / 10.0, .9))
    for k in range(1, 9):
        c.line(*P(0, k / 10.0), *P(.8, k / 10.0))
    c.setDash()
    c.setFillColorRGB(*INK)
    c.setFont(REG, 7)
    for k in range(9):
        c.drawCentredString(P(k / 10.0, 0)[0], oy - 11, "0" if k == 0 else ".%d" % k)
    for k in range(10):
        c.drawRightString(ox - 4, P(0, k / 10.0)[1] - 2.5, "0" if k == 0 else ".%d" % k)
    c.setFont(ITAL, 10)
    c.drawCentredString(ox + .4 * s, oy - 25, "x")
    c.drawCentredString(ox - 24, oy + .45 * s, "y")

    c.saveState()
    c.clipPath(polyline(edge, True), stroke=0, fill=0)
    c.drawImage(ImageReader(make_cie_image(.75, .85, 700)), ox, oy, .75 * s, .85 * s)
    c.restoreState()
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(.7)
    c.drawPath(polyline(edge, True), stroke=1, fill=0)
    c.rect(ox, oy, .8 * s, .9 * s, stroke=1, fill=0)

    # wavelength ticks, pointing away from white
    c.setFont(REG, 5.6)
    for lam in list(range(450, 631, 5)) + [700]:
        (x0, y0), (x1, y1), (x, y) = locus_xy(lam - 5), locus_xy(lam + 5), locus_xy(lam)
        nx, ny = y1 - y0, x0 - x1
        nl = math.hypot(nx, ny)
        nx, ny = nx / nl, ny / nl
        if nx * (x - 1 / 3.0) + ny * (y - 1 / 3.0) < 0:
            nx, ny = -nx, -ny
        bx, by = P(x, y)
        tick = 5 if lam % 10 == 0 else 3
        c.line(bx, by, bx + nx * tick, by + ny * tick)
        if lam % 10 == 0 and (460 <= lam <= 600 or lam in (620, 700)):
            c.drawCentredString(bx + nx * (tick + 8), by + ny * (tick + 8) - 2, str(lam))

    # Planckian locus with marked temperatures
    temps = [1000 * 25 ** (k / 60.0) for k in range(61)]
    c.setLineWidth(.8)
    c.drawPath(polyline([planck_xy(t) for t in temps]), stroke=1, fill=0)
    c.setFont(REG, 5)
    for t in CIE_KELVIN:
        bx, by = P(*planck_xy(t))
        c.circle(bx, by, 1.5, stroke=0, fill=1)
        c.drawCentredString(bx, by - 8, "%d K" % t)

    # sRGB triangle and the equal-energy white point
    c.setDash(3, 2)
    c.setLineWidth(.7)
    c.drawPath(polyline(SRGB_XY, True), stroke=1, fill=0)
    c.setDash()
    c.setFont(BOLD, 6.5)
    gx, gy = P(*SRGB_XY[1])
    c.drawString(gx + 5, gy + 1, "sRGB")
    ex, ey = P(1 / 3.0, 1 / 3.0)
    c.circle(ex, ey, 1.6, stroke=0, fill=1)
    c.drawString(ex + 4, ey + 1, "E")

    for name, (x, y) in zip(T("cie_regions"), CIE_REGION_XY):
        bx, by = P(x, y)
        tracked(c, name, bx, by - 2, REG, 5.4, text_on(xy_colour(x, y)), align="center")


def draw_legend_glyph(c, k, x, y):
    c.setStrokeColorRGB(*INK)
    c.setFillColorRGB(*INK)
    c.setLineWidth(.7)
    if k == 0:
        p = c.beginPath()
        p.moveTo(x, y - 3)
        p.curveTo(x + 6, y + 4, x + 14, y + 4, x + 20, y - 3)
        c.drawPath(p, stroke=1, fill=0)
        for t in (.25, .5, .75):
            c.line(x + 20 * t, y + 2.2, x + 20 * t, y + 5)
    elif k == 1:
        c.line(x, y, x + 20, y)
    elif k == 2:
        c.line(x, y, x + 20, y)
        for t in (.2, .8):
            c.circle(x + 20 * t, y, 1.5, stroke=0, fill=1)
    elif k == 3:
        c.setDash(3, 2)
        c.line(x, y, x + 20, y)
        c.setDash()
    else:
        c.circle(x + 10, y, 1.6, stroke=0, fill=1)


def draw_spectrum(c, x0, y0, w, h_curves, h_strip):
    """Colour-matching functions above, the spectrum as screen colours below,
    on a shared wavelength axis (380-700 nm)."""
    lams = range(380, 701)
    sx = w / 320.0
    lin = {}
    for lam in lams:     # chromaticity from the table, brightness from y(lam)
        x, y = locus_xy(lam)
        Y = cmf(lam)[1]
        lin[lam] = displayable(xyz_to_linear_srgb(x / y * Y, Y, (1 - x - y) / y * Y))
    top = max(max(v) for v in lin.values())
    for lam in lams:
        c.setFillColorRGB(*(srgb_gamma(v / top) for v in lin[lam]))
        c.rect(x0 + (lam - 380) * sx, y0, sx + .3, h_strip, stroke=0, fill=1)

    base = y0 + h_strip + 8
    peak = 1.8
    curves = [(0, (.85, .15, .15), "x"), (1, (.15, .6, .2), "y"), (2, (.15, .3, .85), "z")]
    c.setLineWidth(1.1)
    for k, col, label in curves:
        pts = [(x0 + (lam - 380) * sx, base + cmf(lam)[k] / peak * h_curves) for lam in lams]
        p = c.beginPath()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        c.setStrokeColorRGB(*col)
        c.drawPath(p, stroke=1, fill=0)
        lx, ly = max(pts, key=lambda q: q[1])
        c.setFillColorRGB(*col)
        c.setFont(ITAL, 8)
        c.drawCentredString(lx, ly + 4, label)
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(.5)
    c.line(x0, base, x0 + w, base)
    c.setFillColorRGB(*INK)
    c.setFont(REG, 6)
    for lam in range(400, 701, 50):
        x = x0 + (lam - 380) * sx
        c.line(x, y0 - 2, x, y0)
        c.drawCentredString(x, y0 - 9, "%d nm" % lam if lam == 700 else str(lam))


def build_page_8(c):
    page_start(c, "title8")
    draw_cie(c, 72, 62, 520)

    x0 = 525
    caption(c, x0, 520, T("cie_t"), T("cie_d"), 240, align="left", size=6.4)
    y = 410
    for k, text in enumerate(T("cie_legend")):
        draw_legend_glyph(c, k, x0, y + 2)
        tracked(c, text, x0 + 28, y, REG, 6.6, INK, max_w=212)
        y -= 17
    caption(c, x0, 300, T("spectrum_t"), T("spectrum_d"), 240, align="left", size=6.4)
    draw_spectrum(c, x0, 90, 240, 130, 16)


# ==========================================================================
# 13. PAGE 9  (table of tints and shades)
# ==========================================================================
# Base colour of each row of ts_rows (hsb), grey last.
TS_BASES = [hsb(4, .78, .97), hsb(28, .92, .98), hsb(48, .92, 1), hsb(125, .72, .68),
            hsb(176, .88, .66), hsb(208, .88, .76), hsb(280, .5, .66), hsb(336, .66, .96),
            hsb(24, .52, .62), (.5, .5, .5)]


def arrow(c, x0, x1, y, col=INK):
    c.setStrokeColorRGB(*col)
    c.setFillColorRGB(*col)
    c.setLineWidth(.8)
    c.line(x0, y, x1, y)
    d = 4 if x1 > x0 else -4
    fill_poly(c, [(x1 + d, y), (x1 - d, y + 2.6), (x1 - d, y - 2.6)], col, col, .1)


def build_page_9(c):
    """Rows of base colours: 90 % ... 10 % white on the left (tints), the
    base colour in the middle, 10 % ... 90 % black on the right (shades)."""
    page_start(c, "title9")
    tracked(c, T("ts_sub"), W / 2, 538, REG, 10, INK, align="center", max_w=600)
    steps = [-.9, -.8, -.7, -.6, -.5, -.4, -.3, -.2, -.1, 0, .1, .2, .3, .4, .5, .6, .7, .8, .9]
    x0, cell, step, top, row = 112, 29, 34.5, 452, 38.5   # top = bottom of the first row
    xb = x0 + 9 * step                             # base column

    c.setStrokeColorRGB(.7, .7, .7)
    c.setLineWidth(.8)
    c.roundRect(xb - 3.5, top - 9 * row - 4, cell + 7, 9 * row + cell + 33, 5,
                stroke=1, fill=0)
    tracked(c, T("add_white"), x0 + 4.5 * step + cell / 2, 508, BOLD, 7, INK, 1,
            align="center", max_w=200)
    arrow(c, xb - 8, x0, 501)
    tracked(c, T("add_black"), x0 + 13.5 * step + cell / 2, 508, BOLD, 7, INK, 1,
            align="center", max_w=200)
    arrow(c, xb + cell + 8, x0 + 18 * step + cell, 501)
    for i, t in enumerate(steps):
        x = x0 + i * step + cell / 2
        if t == 0:
            tracked(c, T("base_colour"), x, 499, BOLD, 6, INK, align="center",
                    max_w=46)
        else:
            tracked(c, "%d%%" % round(abs(t) * 100), x, top + cell + 6, BOLD, 6.6,
                    INK, align="center")

    for r, (name, base) in enumerate(zip(T("ts_rows"), TS_BASES)):
        y = top - r * row
        c.setFillColorRGB(*base)
        c.circle(32, y + cell / 2, 7, stroke=0, fill=1)
        tracked(c, name, 44, y + cell / 2 - 2.3, BOLD, 6.4, INK, max_w=62)
        for i, t in enumerate(steps):
            c.setFillColorRGB(*tweak(base, -t))
            c.roundRect(x0 + i * step, y, cell, cell, 3, stroke=0, fill=1)

    c.setFont(REG, 8)
    c.setFillColorRGB(*INK)
    yy = 62
    for ln in simpleSplit(T("ts_note"), REG, 8, 520):
        c.drawCentredString(W / 2, yy, ln)
        yy -= 10.5


# ==========================================================================
# 14. PAGE 10  (Munsell hue circle, RYB and RGB stars)
# ==========================================================================
# Munsell hues clockwise from 5R at the top, with the approximate CIELAB hue
# angle of each (degrees).
MUNSELL_HUES = [("5R", 10), ("10R", 45), ("5YR", 60), ("10YR", 72), ("5Y", 85), ("10Y", 100),
                ("5GY", 115), ("10GY", 135), ("5G", 155), ("10G", 168), ("5BG", 180),
                ("10BG", 195), ("5B", 212), ("10B", 232), ("5PB", 260), ("10PB", 312),
                ("5P", 320), ("10P", 328), ("5RP", 340), ("10RP", 355)]


def lab_to_linear_srgb(L, a, b):
    """CIELAB (D65 white) -> linear sRGB (may fall outside 0..1)."""
    def inv(t):
        return t ** 3 if t > 6 / 29.0 else 3 * (6 / 29.0) ** 2 * (t - 4 / 29.0)
    fy = (L + 16) / 116.0
    return xyz_to_linear_srgb(.95047 * inv(fy + a / 500.0), inv(fy), 1.08883 * inv(fy - b / 200.0))


def cusp_colour(h):
    """Most saturated sRGB colour of CIELAB hue angle h: for each lightness,
    the largest chroma still inside sRGB (bisection), then the best of all."""
    ca, sa = math.cos(math.radians(h)), math.sin(math.radians(h))
    best_c, best = 0.0, (0.5, 0.5, 0.5)
    for L in range(20, 99):
        lo, hi = 0.0, 150.0
        for _ in range(16):
            mid = (lo + hi) / 2
            rgb = lab_to_linear_srgb(L, mid * ca, mid * sa)
            if min(rgb) >= 0 and max(rgb) <= 1:
                lo = mid
            else:
                hi = mid
        if lo > best_c:
            best_c, best = lo, lab_to_linear_srgb(L, lo * ca, lo * sa)
    return tuple(srgb_gamma(v) for v in best)


def draw_munsell(c, cx, cy, R, side):
    n = len(MUNSELL_HUES)
    c.setStrokeColorRGB(*INK)
    for i, (code, h) in enumerate(MUNSELL_HUES):
        a = 90 - 360.0 * i / n
        x, y = pol(cx, cy, R, a)
        c.saveState()
        c.translate(x, y)
        c.rotate(a - 90)
        c.setFillColorRGB(*cusp_colour(h))
        c.setLineWidth(.7)
        c.rect(-side / 2, -side / 2, side, side, stroke=1, fill=1)
        c.restoreState()
        c.setLineWidth(.6)
        c.line(*pol(cx, cy, .4 * R, a), *pol(cx, cy, .68 * R, a))
        ring_text(c, code, cx, cy, .79 * R, a, 8.5, INK, max_w=40)


def coloured_word(c, x, y, letters, size):
    """Letters each in its own colour, with a thin dark outline."""
    w = sum(stringWidth(ch, BOLD, size) for ch, _ in letters) + 1.5 * (len(letters) - 1)
    c.saveState()
    t = c.beginText()
    t.setFont(BOLD, size)
    t.setTextRenderMode(2)
    t.setTextOrigin(x - w / 2, y)
    t.setCharSpace(1.5)
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(.6)
    for ch, col in letters:
        t.setFillColorRGB(*col)
        t.textOut(ch)
    c.drawText(t)
    c.restoreState()


def draw_hue_star(c, cx, cy, R, cols, names):
    """Two six-pointed stars: the six main colours on the points of the front
    star, the six in between on a copy turned 30 degrees behind it, which
    shows in the notches. cols and names hold 12 entries clockwise from the
    top."""
    ri = R / math.sqrt(3)
    for j in list(range(1, 12, 2)) + list(range(0, 12, 2)):
        a = 90 - 30 * j
        fill_poly(c, [pol(cx, cy, R, a), pol(cx, cy, ri, a - 30), pol(cx, cy, ri, a + 30)],
                  cols[j], WHITE, .1)
    v = [pol(cx, cy, ri, 30 + 60 * m) for m in range(6)]
    c.setStrokeColorRGB(.65, .65, .65)
    c.setLineWidth(.4)
    for m in range(6):
        c.line(*v[m], *v[(m + 2) % 6])
        c.line(cx, cy, *v[m])
    for j, name in enumerate(names):
        a = 90 - 30 * j
        main = j % 2 == 0
        x, y = pol(cx, cy, R + 9 if main else R + 6, a)
        ca = math.cos(math.radians(a))
        align = "left" if ca > .3 else "right" if ca < -.3 else "center"
        sa = math.sin(math.radians(a))
        dy = 2 if sa > .9 else -8 if sa < -.9 else -2.5
        tracked(c, name, x, y + dy, BOLD if main else REG,
                8.2 if main else 6.4, INK, .3, align=align, max_w=95)


def build_page_10(c):
    page_start(c, "title10")
    caption(c, 205, 528, T("munsell_t"), T("munsell_d"), 330)
    draw_munsell(c, 205, 272, 150, 30)

    ryb = [hue_rgb(4 - j) for j in range(12)]
    names = T("hue_names")
    draw_hue_star(c, 500, 392, 72, ryb, [names[(4 - j) % 12] for j in range(12)])
    coloured_word(c, 712, 425, list(zip("RYB", (ryb[0], ryb[4], ryb[8]))), 24)
    caption(c, 712, 400, "", T("ryb_star_d"), 112, size=6.6)

    rgb = [hsb(30 * j, 1, 1) for j in range(12)]
    draw_hue_star(c, 500, 152, 72, rgb, T("rgb12_names"))
    coloured_word(c, 712, 185, list(zip("RGB", (rgb[0], rgb[4], rgb[8]))), 24)
    caption(c, 712, 160, "", T("rgb_star_d"), 112, size=6.6)


# ==========================================================================
# 15. MAIN
# ==========================================================================
PAGES = {1: build_page_1, 2: build_page_2, 3: build_page_3, 4: build_page_4,
         5: build_page_5, 6: build_page_6, 7: build_page_7, 8: build_page_8,
         9: build_page_9, 10: build_page_10}


def main():
    ap = argparse.ArgumentParser(description="Colour theory poster (PDF)")
    ap.add_argument("--lang", default="en", choices=POSTER_LANGS, help="text language")
    ap.add_argument("-o", "--out", default=None, help="output PDF path")
    ap.add_argument("--pages", type=int, nargs="+", default=sorted(PAGES), choices=sorted(PAGES),
                    help="which pages to render (default: all)")
    a = ap.parse_args()
    set_lang(a.lang)
    out = a.out or "colour_theory_%s.pdf" % a.lang
    c = canvas.Canvas(out, pagesize=(W, H))
    c.setTitle(T("title1").title())
    for n in a.pages:
        PAGES[n](c)
        c.showPage()
    c.save()
    print("Saved", out)


if __name__ == "__main__":
    main()
