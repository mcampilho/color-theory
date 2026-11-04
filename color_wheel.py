#!/usr/bin/env python3
"""
color_wheel.py
--------------
Build-your-own colour wheels: a printable A4 PDF with two paper colour
wheels to cut out and assemble at home, plus the instructions.

Each wheel has two discs joined at the centre by a split pin: a back disc
that turns, with all the colours, and a front disc with windows.

  Disc 1 - Mixing colours. The front disc has five coloured tabs (+ red,
           + yellow, + blue, + white, + black) and five windows in its top
           half, each at a different distance from the centre. The colour
           of the back disc's outer ring just beyond a tab, mixed with the
           tab's colour, shows in that tab's window. The lower half has a
           grey scale from value 1 (black) to value 10 (white), and the
           centre holds colour definitions and how to use it.
  Disc 2 - Colour relationships. The front disc has 12 windows at the rim
           (the colour names) and 8 large windows that show tint, tone and
           shade of the colours that go with the one at the top:
           complementary, split complementary, triad and tetrads, as the
           central diagram shows.

    pip install reportlab pillow
    python3 color_wheel.py                  # English -> colour_wheels_en.pdf
    python3 color_wheel.py --lang pt        # Portuguese
    python3 color_wheel.py --lang es -o es.pdf
    python3 color_wheel.py --app [--lang pt]  # the wheels in a window (Tkinter)
    python3 color_wheel.py --web              # SVG discs + data for web/index.html
    python3 color_wheel.py --webview          # that web page in its own window (pywebview)
    --theme auto|light|dark                   # colours of --app and --webview

On screen every part of both wheels turns: drag it with the mouse, use the
mouse wheel, or the arrow keys (up/down choose the part).

The colours and several helpers come from color_theory_document.py, which
must sit in the same folder.
"""
import argparse
import json
import math
import os
from xml.sax.saxutils import escape as xml_escape

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import FILL_EVEN_ODD

import i18n
from i18n import BOLD, ITAL, LANG_NAMES, REG

from color_theory_document import (HUE_RYB, STRINGS as DOC_STRINGS, arc_text, fill_poly, fit_size,
                                   luma, mix, pol, radial_text, ring_text, ring_wedge, ryb_to_rgb,
                                   srgb_gamma, text_on, tracked)

# ==========================================================================
# 1. TRANSLATIONS
# ==========================================================================
STRINGS = {
    # ------------------------------------------------------------------ EN
    "en": {
        "doc_title": "Build your own colour wheels",
        "title": "BUILD YOUR OWN COLOUR WHEELS",
        "subtitle": "Two paper colour wheels to cut out and assemble: one to mix colours, "
                    "one to find colours that go together.",
        "need_t": "YOU NEED",
        "need": ["A printer and 4 sheets of A4 paper, ideally thick (160-250 g/m²), or "
                 "ordinary paper glued onto thin card.",
                 "Scissors, a craft knife and a cutting mat.",
                 "Two paper fasteners (split pins), about 10 mm long.",
                 "Optional: a glue stick, and lamination to make the discs last longer."],
        "print_t": "1. PRINT",
        "print": ["Print pages 3 to 6 at actual size (100 %, no \"fit to page\").",
                  "Each page has a 100 mm bar: measure it to check the scale.",
                  "On thin paper, glue each page onto card before cutting."],
        "cut_t": "2. CUT",
        "cut": ["Cut each disc along its solid outer line.",
                "Cut out every hatched window with the craft knife, on the mat. Cut from the "
                "corners inward and keep the blade upright.",
                "Pierce the centre of each disc at the small cross, with the tip of the knife "
                "or a needle."],
        "build_t": "3. ASSEMBLE",
        "build": ["Lay the back disc (the one with all the colours) face up.",
                  "Put the front disc (the one with the windows) face up on top of it, centres "
                  "aligned.",
                  "Push a split pin through both centres and open its legs behind. Do not "
                  "press too tight: the back disc must turn freely."],
        "pieces_t": "THE PIECES",
        "pieces": ["Page 3 - Disc 1, back: the 12 colours and their mixtures.",
                   "Page 4 - Disc 1, front: 5 mixing windows, grey scale and definitions.",
                   "Page 5 - Disc 2, back: the 12 colours with tint, tone and shade.",
                   "Page 6 - Disc 2, front: 20 windows and the harmony diagram."],
        "fig_front": "front disc (windows)", "fig_back": "back disc (turns)",
        "fig_pin": "split pin",
        "use_t": "HOW TO USE THEM",
        "use1_t": "DISC 1 - MIXING COLOURS",
        "use1": ["Turn the back disc. Each coloured tab on the edge of the front disc names a "
                 "colour to add: red, yellow, blue, white or black.",
                 "The colour on the outer ring, just beyond a tab, is the base colour. The "
                 "tab's window shows what you get by mixing the two in equal parts.",
                 "Example: turn orange to the \"+ blue\" tab; the window shows the dark, dull "
                 "colour of orange and blue mixed (they are complementary).",
                 "The grey scale on the lower half goes from value 1 (black) to value 10 "
                 "(white). Hold a colour next to it to judge how light or dark it is."],
        "use2_t": "DISC 2 - COLOUR RELATIONSHIPS",
        "use2": ["Turn the back disc until the colour you want shows in the top window, marked "
                 "\"pure colour\", where the arrow points.",
                 "Complementary: the window opposite, at the bottom.",
                 "Split complementary: the two windows on either side of the complement.",
                 "Triad: the windows at the corners of the triangle with equal sides.",
                 "Tetrad: the windows at the corners of either rectangle.",
                 "Diad: the windows two steps away from the top one, on either side.",
                 "Each large window also shows its colour as a tint (with white), a tone (with "
                 "grey) and a shade (with black)."],
        "gloss_t": "COLOUR WORDS",
        "gloss": [("Primary colours", "red, yellow and blue: they cannot be mixed from other "
                   "colours."),
                  ("Secondary colours", "orange, green and violet: two primaries mixed."),
                  ("Tertiary colours", "a primary mixed with a neighbouring secondary, such as "
                   "red-orange."),
                  ("Warm colours", "reds, oranges and yellows: they seem to come forward."),
                  ("Cool colours", "greens, blues and violets: they seem to move back."),
                  ("Hue", "another name for a colour, such as red or blue-green."),
                  ("Tint", "a colour plus white."),
                  ("Tone", "a colour plus grey."),
                  ("Shade", "a colour plus black."),
                  ("Value", "how light or dark a colour is."),
                  ("Chroma", "how bright or dull a colour is (also intensity or saturation)."),
                  ("Neutral grey", "black and white mixed, with no hue."),
                  ("Key colour", "the main colour of a colour scheme.")],
        "note": "The printed colours are a guide: real paints mix a little differently, "
                "depending on their pigments.",
        "page": "Page %d of %d",
        # ---- disc pages
        "head_d1b": "DISC 1 - BACK (TURNS)",
        "head_d1f": "DISC 1 - FRONT (WINDOWS)",
        "head_d2b": "DISC 2 - BACK (TURNS)",
        "head_d2f": "DISC 2 - FRONT (WINDOWS)",
        "scale": "Print at 100 %: this bar must measure 100 mm.",
        "legend": ["Cut along the solid lines", "Hatched: cut out", "Cross: pierce here"],
        "d1_title": "A GUIDE TO MIXING COLOURS",
        "tabs": ["+ RED", "+ YELLOW", "+ BLUE", "+ WHITE", "+ BLACK"],
        "value": "VALUE",
        "full_black": "100% BLACK",
        "full_white": "100% WHITE",
        "grey_title": "GREY SCALE",
        "d1_how": "HOW TO USE: turn the back disc. The colour beyond a tab, mixed with the "
                  "tab's colour, shows in its window.",
        "d1_left": [("Primary", "red, yellow, blue: not mixed from others."),
                    ("Secondary", "two primaries mixed: orange, green, violet."),
                    ("Tertiary", "a primary and a secondary mixed."),
                    ("Warm", "reds, oranges, yellows: they advance."),
                    ("Cool", "greens, blues, violets: they recede.")],
        "d1_right": [("Hue", "another name for colour."),
                     ("Tint", "colour + white."),
                     ("Tone", "colour + grey."),
                     ("Shade", "colour + black."),
                     ("Value", "lightness or darkness."),
                     ("Chroma", "brightness or dullness."),
                     ("Neutral grey", "black + white.")],
        "d2_title": "COLOUR RELATIONSHIPS",
        "d2_how": [("How to use", "turn the back disc until a colour shows in the top window. "
                    "The diagram points to the colours that go with it.")],
        "d2_defs_a": [("Complementary", "opposite colours: the strongest contrast."),
                      ("Split complementary", "the two colours beside the complement.")],
        "d2_defs_b": [("Triad", "three colours evenly spaced."),
                      ("Tetrad", "two pairs of complements: a rectangle."),
                      ("Diad", "two colours with one between them.")],
        "pure": "PURE COLOUR", "comp": "COMPLEMENTARY", "split": "SPLIT COMPLEMENTARY",
        "triad": "TRIAD", "tetrad": "TETRAD",
        "bands": ["TINT", "TONE", "SHADE"],
        # on-screen wheels (desktop app and web page)
        "app_title": "Colour wheels",
        "app_lang": "Language",
        "app_reset": "Reset",
        "app_dark": "Dark mode",
        "app_light": "Light mode",
        "app_wait": "Drawing the discs...",
        "app_selected": "Selected",
        "parts": ["Disc 1, back", "Disc 1, front", "Disc 2, back", "Disc 2, front"],
        "app_help": ["Drag any disc with the mouse to turn it; the mouse wheel turns it one "
                     "colour at a time.",
                     "Keyboard: ← and → turn the selected disc one colour; ↑ and ↓ (or Tab) "
                     "choose another disc.",
                     "Grab a back disc by its coloured rim or through a window."],
    },
    # ------------------------------------------------------------------ PT
    "pt": {
        "doc_title": "Construa as suas rodas de cores",
        "title": "CONSTRUA AS SUAS RODAS DE CORES",
        "subtitle": "Duas rodas de cores em papel para recortar e montar: uma para misturar "
                    "cores, outra para encontrar as cores que combinam.",
        "need_t": "PRECISA DE",
        "need": ["Uma impressora e 4 folhas A4, de preferência grossas (160-250 g/m²), ou "
                 "papel comum colado em cartolina fina.",
                 "Tesoura, x-ato e uma base de corte.",
                 "Dois ataches de papelaria (bailarinas), com cerca de 10 mm.",
                 "Opcional: cola em stick e plastificação, para os discos durarem mais."],
        "print_t": "1. IMPRIMIR",
        "print": ["Imprima as páginas 3 a 6 em tamanho real (100 %, sem \"ajustar à "
                  "página\").",
                  "Cada página tem uma barra de 100 mm: meça-a para confirmar a escala.",
                  "Em papel fino, cole cada página em cartolina antes de recortar."],
        "cut_t": "2. RECORTAR",
        "cut": ["Recorte cada disco pela linha exterior contínua.",
                "Recorte todas as janelas tracejadas com o x-ato, sobre a base de corte. Corte "
                "dos cantos para dentro e mantenha a lâmina na vertical.",
                "Fure o centro de cada disco na pequena cruz, com a ponta do x-ato ou uma "
                "agulha."],
        "build_t": "3. MONTAR",
        "build": ["Ponha o disco de trás (o que tem todas as cores) virado para cima.",
                  "Coloque por cima o disco da frente (o das janelas), também virado para "
                  "cima, com os centros alinhados.",
                  "Passe um atache pelos dois centros e abra as pernas por trás. Não aperte "
                  "demasiado: o disco de trás tem de rodar à vontade."],
        "pieces_t": "AS PEÇAS",
        "pieces": ["Página 3 - Disco 1, trás: as 12 cores e as suas misturas.",
                   "Página 4 - Disco 1, frente: 5 janelas de mistura, escala de cinzentos e "
                   "definições.",
                   "Página 5 - Disco 2, trás: as 12 cores com tinta, tom e sombra.",
                   "Página 6 - Disco 2, frente: 20 janelas e o diagrama de harmonias."],
        "fig_front": "disco da frente (janelas)", "fig_back": "disco de trás (roda)",
        "fig_pin": "atache",
        "use_t": "COMO USAR",
        "use1_t": "DISCO 1 - MISTURAR CORES",
        "use1": ["Rode o disco de trás. Cada patilha colorida na borda do disco da frente "
                 "indica uma cor a juntar: vermelho, amarelo, azul, branco ou preto.",
                 "A cor do anel exterior, logo a seguir a uma patilha, é a cor de base. A "
                 "janela dessa patilha mostra o resultado de misturar as duas em partes "
                 "iguais.",
                 "Exemplo: rode o laranja até à patilha \"+ azul\"; a janela mostra a cor "
                 "escura e baça do laranja com o azul (são complementares).",
                 "A escala de cinzentos na metade de baixo vai do valor 1 (preto) ao valor 10 "
                 "(branco). Encoste-lhe uma cor para avaliar se é clara ou escura."],
        "use2_t": "DISCO 2 - RELAÇÕES ENTRE CORES",
        "use2": ["Rode o disco de trás até a cor que quer aparecer na janela de cima, marcada "
                 "\"cor pura\", para onde aponta a seta.",
                 "Complementar: a janela oposta, em baixo.",
                 "Complementares divididas: as duas janelas de cada lado da complementar.",
                 "Tríade: as janelas nos cantos do triângulo de lados iguais.",
                 "Tétrade: as janelas nos cantos de qualquer um dos retângulos.",
                 "Díade: as janelas a dois passos da de cima, de cada lado.",
                 "Cada janela grande mostra também a sua cor como tinta (com branco), tom (com "
                 "cinzento) e sombra (com preto)."],
        "gloss_t": "PALAVRAS DA COR",
        "gloss": [("Cores primárias", "vermelho, amarelo e azul: não se obtêm misturando "
                   "outras cores."),
                  ("Cores secundárias", "laranja, verde e violeta: duas primárias "
                   "misturadas."),
                  ("Cores terciárias", "uma primária misturada com uma secundária vizinha, "
                   "como o vermelho-laranja."),
                  ("Cores quentes", "vermelhos, laranjas e amarelos: parecem avançar."),
                  ("Cores frias", "verdes, azuis e violetas: parecem recuar."),
                  ("Matiz", "outro nome para uma cor, como vermelho ou azul-verde."),
                  ("Tinta", "uma cor mais branco."),
                  ("Tom", "uma cor mais cinzento."),
                  ("Sombra", "uma cor mais preto."),
                  ("Valor", "quão clara ou escura é uma cor."),
                  ("Croma", "quão viva ou baça é uma cor (também intensidade ou saturação)."),
                  ("Cinzento neutro", "preto e branco misturados, sem matiz."),
                  ("Cor-chave", "a cor principal de um esquema de cores.")],
        "note": "As cores impressas são uma orientação: as tintas reais misturam-se de forma "
                "um pouco diferente, conforme os pigmentos.",
        "page": "Página %d de %d",
        "head_d1b": "DISCO 1 - TRÁS (RODA)",
        "head_d1f": "DISCO 1 - FRENTE (JANELAS)",
        "head_d2b": "DISCO 2 - TRÁS (RODA)",
        "head_d2f": "DISCO 2 - FRENTE (JANELAS)",
        "scale": "Imprimir a 100 %: esta barra tem de medir 100 mm.",
        "legend": ["Recortar pelas linhas contínuas", "Tracejado: recortar e retirar",
                   "Cruz: furar aqui"],
        "d1_title": "GUIA PARA MISTURAR CORES",
        "tabs": ["+ VERMELHO", "+ AMARELO", "+ AZUL", "+ BRANCO", "+ PRETO"],
        "value": "VALOR",
        "full_black": "100% PRETO",
        "full_white": "100% BRANCO",
        "grey_title": "ESCALA DE CINZENTOS",
        "d1_how": "COMO USAR: rode o disco de trás. A cor junto a uma patilha, misturada com a "
                  "cor da patilha, aparece na janela.",
        "d1_left": [("Primárias", "vermelho, amarelo, azul: não se obtêm de outras."),
                    ("Secundárias", "duas primárias: laranja, verde, violeta."),
                    ("Terciárias", "uma primária e uma secundária."),
                    ("Quentes", "vermelhos, laranjas, amarelos: avançam."),
                    ("Frias", "verdes, azuis, violetas: recuam.")],
        "d1_right": [("Matiz", "outro nome para cor."),
                     ("Tinta", "cor + branco."),
                     ("Tom", "cor + cinzento."),
                     ("Sombra", "cor + preto."),
                     ("Valor", "claro ou escuro."),
                     ("Croma", "viva ou baça."),
                     ("Cinzento neutro", "preto + branco.")],
        "d2_title": "RELAÇÕES ENTRE CORES",
        "d2_how": [("Como usar", "rode o disco de trás até uma cor aparecer na janela de cima. "
                    "O diagrama aponta para as cores que combinam com ela.")],
        "d2_defs_a": [("Complementares", "cores opostas: o maior contraste."),
                      ("Complementares divididas", "as duas cores ao lado da "
                       "complementar.")],
        "d2_defs_b": [("Tríade", "três cores à mesma distância."),
                      ("Tétrade", "dois pares de complementares: um retângulo."),
                      ("Díade", "duas cores com uma entre elas.")],
        "pure": "COR PURA", "comp": "COMPLEMENTAR", "split": "COMPLEMENTARES DIVIDIDAS",
        "triad": "TRÍADE", "tetrad": "TÉTRADE",
        "bands": ["TINTA", "TOM", "SOMBRA"],
        "app_title": "Rodas de cores",
        "app_lang": "Idioma",
        "app_reset": "Repor",
        "app_dark": "Modo escuro",
        "app_light": "Modo claro",
        "app_wait": "A desenhar os discos...",
        "app_selected": "Selecionado",
        "parts": ["Disco 1, trás", "Disco 1, frente", "Disco 2, trás", "Disco 2, frente"],
        "app_help": ["Arraste qualquer disco com o rato para o rodar; a roda do rato roda-o "
                     "uma cor de cada vez.",
                     "Teclado: ← e → rodam o disco selecionado uma cor; ↑ e ↓ (ou Tab) "
                     "escolhem outro disco.",
                     "Agarre um disco de trás pela borda colorida ou através de uma janela."],
    },
    # ------------------------------------------------------------------ ES
    "es": {
        "doc_title": "Construye tus ruedas de colores",
        "title": "CONSTRUYE TUS RUEDAS DE COLORES",
        "subtitle": "Dos ruedas de colores de papel para recortar y montar: una para mezclar "
                    "colores, otra para encontrar los colores que combinan.",
        "need_t": "NECESITAS",
        "need": ["Una impresora y 4 hojas A4, mejor gruesas (160-250 g/m²), o papel normal "
                 "pegado sobre cartulina fina.",
                 "Tijeras, un cúter y una base de corte.",
                 "Dos encuadernadores de papelería (patas abiertas), de unos 10 mm.",
                 "Opcional: pegamento en barra y plastificado, para que los discos duren "
                 "más."],
        "print_t": "1. IMPRIMIR",
        "print": ["Imprime las páginas 3 a 6 a tamaño real (100 %, sin \"ajustar a la "
                  "página\").",
                  "Cada página tiene una barra de 100 mm: mídela para comprobar la escala.",
                  "Con papel fino, pega cada página sobre cartulina antes de recortar."],
        "cut_t": "2. RECORTAR",
        "cut": ["Recorta cada disco por su línea exterior continua.",
                "Recorta todas las ventanas rayadas con el cúter, sobre la base. Corta desde "
                "las esquinas hacia dentro y mantén la cuchilla vertical.",
                "Perfora el centro de cada disco en la pequeña cruz, con la punta del cúter o "
                "una aguja."],
        "build_t": "3. MONTAR",
        "build": ["Pon el disco trasero (el que tiene todos los colores) boca arriba.",
                  "Coloca encima el disco delantero (el de las ventanas), también boca arriba, "
                  "con los centros alineados.",
                  "Pasa un encuadernador por los dos centros y abre las patas por detrás. No "
                  "aprietes demasiado: el disco trasero tiene que girar con soltura."],
        "pieces_t": "LAS PIEZAS",
        "pieces": ["Página 3 - Disco 1, trasero: los 12 colores y sus mezclas.",
                   "Página 4 - Disco 1, delantero: 5 ventanas de mezcla, escala de grises y "
                   "definiciones.",
                   "Página 5 - Disco 2, trasero: los 12 colores con tinte, tono y sombra.",
                   "Página 6 - Disco 2, delantero: 20 ventanas y el diagrama de armonías."],
        "fig_front": "disco delantero (ventanas)", "fig_back": "disco trasero (gira)",
        "fig_pin": "encuadernador",
        "use_t": "CÓMO USARLAS",
        "use1_t": "DISCO 1 - MEZCLAR COLORES",
        "use1": ["Gira el disco trasero. Cada pestaña de color en el borde del disco delantero "
                 "indica un color para añadir: rojo, amarillo, azul, blanco o negro.",
                 "El color del anillo exterior, justo al lado de una pestaña, es el color base. "
                 "La ventana de esa pestaña muestra el resultado de mezclar los dos a partes "
                 "iguales.",
                 "Ejemplo: gira el naranja hasta la pestaña \"+ azul\"; la ventana muestra el "
                 "color oscuro y apagado del naranja con el azul (son complementarios).",
                 "La escala de grises de la mitad inferior va del valor 1 (negro) al valor 10 "
                 "(blanco). Acerca un color para juzgar si es claro u oscuro."],
        "use2_t": "DISCO 2 - RELACIONES ENTRE COLORES",
        "use2": ["Gira el disco trasero hasta que el color que quieres aparezca en la ventana "
                 "de arriba, marcada \"color puro\", donde apunta la flecha.",
                 "Complementario: la ventana opuesta, abajo.",
                 "Complementarios divididos: las dos ventanas a cada lado del complementario.",
                 "Tríada: las ventanas en las esquinas del triángulo de lados iguales.",
                 "Tétrada: las ventanas en las esquinas de cualquiera de los rectángulos.",
                 "Díada: las ventanas a dos pasos de la de arriba, a cada lado.",
                 "Cada ventana grande muestra también su color como tinte (con blanco), tono "
                 "(con gris) y sombra (con negro)."],
        "gloss_t": "PALABRAS DEL COLOR",
        "gloss": [("Colores primarios", "rojo, amarillo y azul: no se obtienen mezclando "
                   "otros colores."),
                  ("Colores secundarios", "naranja, verde y violeta: dos primarios "
                   "mezclados."),
                  ("Colores terciarios", "un primario mezclado con un secundario vecino, como "
                   "el rojo-naranja."),
                  ("Colores cálidos", "rojos, naranjas y amarillos: parecen avanzar."),
                  ("Colores fríos", "verdes, azules y violetas: parecen retroceder."),
                  ("Matiz", "otro nombre para un color, como rojo o azul-verde."),
                  ("Tinte", "un color más blanco."),
                  ("Tono", "un color más gris."),
                  ("Sombra", "un color más negro."),
                  ("Valor", "lo claro u oscuro que es un color."),
                  ("Croma", "lo vivo o apagado que es un color (también intensidad o "
                   "saturación)."),
                  ("Gris neutro", "negro y blanco mezclados, sin tono."),
                  ("Color clave", "el color principal de un esquema de colores.")],
        "note": "Los colores impresos son una guía: las pinturas reales se mezclan de forma "
                "algo distinta, según sus pigmentos.",
        "page": "Página %d de %d",
        "head_d1b": "DISCO 1 - TRASERO (GIRA)",
        "head_d1f": "DISCO 1 - DELANTERO (VENTANAS)",
        "head_d2b": "DISCO 2 - TRASERO (GIRA)",
        "head_d2f": "DISCO 2 - DELANTERO (VENTANAS)",
        "scale": "Imprimir al 100 %: esta barra debe medir 100 mm.",
        "legend": ["Recortar por las líneas continuas", "Rayado: recortar y quitar",
                   "Cruz: perforar aquí"],
        "d1_title": "GUÍA PARA MEZCLAR COLORES",
        "tabs": ["+ ROJO", "+ AMARILLO", "+ AZUL", "+ BLANCO", "+ NEGRO"],
        "value": "VALOR",
        "full_black": "100% NEGRO",
        "full_white": "100% BLANCO",
        "grey_title": "ESCALA DE GRISES",
        "d1_how": "CÓMO USAR: gira el disco trasero. El color junto a una pestaña, mezclado con "
                  "el color de la pestaña, aparece en su ventana.",
        "d1_left": [("Primarios", "rojo, amarillo, azul: no salen de otros."),
                    ("Secundarios", "dos primarios: naranja, verde, violeta."),
                    ("Terciarios", "un primario y un secundario."),
                    ("Cálidos", "rojos, naranjas, amarillos: avanzan."),
                    ("Fríos", "verdes, azules, violetas: retroceden.")],
        "d1_right": [("Matiz", "otro nombre para el color."),
                     ("Tinte", "color + blanco."),
                     ("Tono", "color + gris."),
                     ("Sombra", "color + negro."),
                     ("Valor", "claro u oscuro."),
                     ("Croma", "vivo o apagado."),
                     ("Gris neutro", "negro + blanco.")],
        "d2_title": "RELACIONES ENTRE COLORES",
        "d2_how": [("Cómo usar", "gira el disco trasero hasta que un color aparezca en la "
                    "ventana de arriba. El diagrama señala los colores que combinan con él.")],
        "d2_defs_a": [("Complementarios", "colores opuestos: el mayor contraste."),
                      ("Complementarios divididos", "los dos colores junto al "
                       "complementario.")],
        "d2_defs_b": [("Tríada", "tres colores a la misma distancia."),
                      ("Tétrada", "dos pares de complementarios: un rectángulo."),
                      ("Díada", "dos colores con uno entre ellos.")],
        "pure": "COLOR PURO", "comp": "COMPLEMENTARIO", "split": "COMPLEMENTARIOS DIVIDIDOS",
        "triad": "TRÍADA", "tetrad": "TÉTRADA",
        "bands": ["TINTE", "TONO", "SOMBRA"],
        "app_title": "Ruedas de colores",
        "app_lang": "Idioma",
        "app_reset": "Restablecer",
        "app_dark": "Modo oscuro",
        "app_light": "Modo claro",
        "app_wait": "Dibujando los discos...",
        "app_selected": "Seleccionado",
        "parts": ["Disco 1, trasero", "Disco 1, delantero", "Disco 2, trasero",
                  "Disco 2, delantero"],
        "app_help": ["Arrastre cualquier disco con el ratón para girarlo; la rueda del ratón "
                     "lo gira un color cada vez.",
                     "Teclado: ← y → giran el disco seleccionado un color; ↑ y ↓ (o Tab) "
                     "eligen otro disco.",
                     "Agarre un disco trasero por su borde de color o a través de una ventana."],
    },
}
# the other languages are in locales/color_wheel.py
from locales.color_wheel import STRINGS as _MORE   # noqa: E402

STRINGS.update(_MORE)

_LANG = "en"
# True while drawing the discs for the screen (desktop app and web page):
# no page frame, windows become see-through holes.
_VIRTUAL = False


def T(key):
    return STRINGS.get(_LANG, STRINGS["en"]).get(key, STRINGS["en"][key])


def hue_names():
    """The 12 RYB hue names, clockwise from yellow (from the poster's table)."""
    return DOC_STRINGS.get(_LANG, {}).get("hue_names", DOC_STRINGS["en"]["hue_names"])


def languages():
    """The languages with texts for the wheels, in the order of i18n.LANGS."""
    return [k for k, _ in i18n.LANGS if k in STRINGS]


# ==========================================================================
# 2. GEOMETRY, COLOURS, DRAWING HELPERS
# ==========================================================================
W, H = A4                                   # 595 x 842 pt, portrait
MM = 72 / 25.4
WHITE, BLACK = (1, 1, 1), (0, 0, 0)

# Theme colours of the discs: the paper, its text, outlines, thin rules and
# the shapes of the harmony diagram (tetrad, tetrad, triad, split
# complementary). The printed pages always use the light theme; the
# on-screen wheels can also use the dark one (set_theme).
THEMES = {
    "light": {"PAPER": WHITE, "INK": (0.18, 0.18, 0.18), "LINE": BLACK, "RULE": (.6, .6, .6),
              "DIAGRAM": [(.64, .64, .64), (.52, .52, .52), (.84, .84, .84), WHITE]},
    "dark": {"PAPER": (.14, .14, .15), "INK": (.88, .88, .88), "LINE": (.82, .82, .82),
             "RULE": (.40, .40, .40),
             "DIAGRAM": [(.40, .40, .40), (.33, .33, .33), (.24, .24, .25), (.14, .14, .15)]},
}
PAPER, INK, LINE, RULE, DIAGRAM = (THEMES["light"][k] for k in
                                   ("PAPER", "INK", "LINE", "RULE", "DIAGRAM"))


def set_theme(name):
    """Switch the theme colours above ("light" or "dark")."""
    global PAPER, INK, LINE, RULE, DIAGRAM
    t = THEMES[name]
    PAPER, INK, LINE, RULE, DIAGRAM = t["PAPER"], t["INK"], t["LINE"], t["RULE"], t["DIAGRAM"]
NPAGES = 6
CX, CY = W / 2, 392                         # centre of the disc on its page

# Disc sizes (mm). The back disc of disc 1 sticks out beyond its front disc
# to show the ring of 12 hues; disc 2 shows its hues through windows.
D1_BACK, D1_FRONT = 95, 78
D2_BACK, D2_FRONT = 95, 88
# Disc 1: the five mixing bands (inner, outer radius, mm), one per tab,
# and the angle of each tab and window on the front disc (degrees,
# counter-clockwise from 3 o'clock).
D1_BANDS = [(58, 67), (47, 56), (36, 45), (25, 34), (14, 23)]
D1_TAB_ANGLES = [150, 120, 90, 60, 30]
# Disc 2: windows of the front disc, clockwise from the top in degrees.
D2_FANS = [0, 60, 120, 150, 180, 210, 240, 300]
D2_FAN_R = (45, 73)
D2_BANDS = [(64, 74), (54, 64), (44, 54)]   # tint, tone, shade on the back disc
D2_NAME_R = (76, 95)                        # hue ring of the back disc


def hue_angle(i):
    """Angle of hue i (0 = yellow, clockwise) on the back discs."""
    return 90 - 30 * i


def hue_colour(i):
    return ryb_to_rgb(*HUE_RYB[i % 12])


# What each tab adds, as a point of the RYB cube (white is handled apart).
ADDED_RYB = [(1, 0, 0), (0, 1, 0), (0, 0, 1), None, (1, 1, 1)]
TAB_COLOURS = [ryb_to_rgb(1, 0, 0), ryb_to_rgb(0, 1, 0), ryb_to_rgb(0, 0, 1), WHITE,
               (.1, .1, .1)]


def mixture(i, k):
    """Hue i mixed in equal parts with what tab k adds. Paints are averaged
    in the RYB cube and scaled so the strongest pigment is full; white
    lightens the colour instead.

    Where the three pigments come out nearly balanced (a colour and its
    complement), the cube alone would give the same near-black for every
    pair. Real paints give a dark, dull colour that keeps a bias towards the
    two paints mixed (red + green a brown, violet + yellow a greyish tan,
    orange + blue a slate grey), so the result moves towards the average of
    the two paints, darkened, as the mixture becomes neutral."""
    if ADDED_RYB[k] is None:
        return mix(hue_colour(i), WHITE, .5)
    s = [(a + b) / 2.0 for a, b in zip(HUE_RYB[i], ADDED_RYB[k])]
    top = max(s)
    cube = ryb_to_rgb(*(v / top for v in s))
    if k > 2:                              # black paint: a shade, not a mixture of hues
        return cube
    neutral = (min(s) / top) ** 2          # 0 for two neighbouring hues, 1 for complements
    paints = mix(hue_colour(i), ryb_to_rgb(*ADDED_RYB[k]), .5)
    return mix(cube, mix(paints, BLACK, .22), .85 * neutral)


def grey_value(v):
    """Grey of value v (1 = black ... 10 = white), even steps of CIE lightness."""
    L = 100.0 * (v - 1) / 9
    Y = ((L + 16) / 116.0) ** 3 if L > 8 else L / 903.3
    g = srgb_gamma(Y)
    return (g, g, g)


def path_of(c, pts):
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return p


def window(c, r0, r1, a0, a1):
    """Annular window (radii in mm, angles in degrees) to be cut out:
    hatched inside, solid outline. On screen only the outline is drawn: the
    hole itself comes from disc_base."""
    pts = ring_wedge(CX, CY, r0 * MM, r1 * MM, a0, a1, 16)
    if _VIRTUAL:
        c.setStrokeColorRGB(*LINE)
        c.setLineWidth(.6)
        c.drawPath(path_of(c, pts), stroke=1, fill=0)
        return
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    c.saveState()
    c.clipPath(path_of(c, pts), stroke=0, fill=0)
    c.setFillColorRGB(1, 1, 1)
    c.rect(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys), stroke=0, fill=1)
    c.setStrokeColorRGB(.7, .7, .7)
    c.setLineWidth(.5)
    h = max(ys) - min(ys)
    x = min(xs) - h
    while x < max(xs):
        c.line(x, min(ys), x + h, max(ys))
        x += 3.2
    c.restoreState()
    c.setStrokeColorRGB(*BLACK)
    c.setLineWidth(.6)
    c.drawPath(path_of(c, pts), stroke=1, fill=0)


def pierce_mark(c):
    if _VIRTUAL:
        return
    c.setStrokeColorRGB(*BLACK)
    c.setLineWidth(.5)
    c.line(CX - 2.5 * MM, CY, CX + 2.5 * MM, CY)
    c.line(CX, CY - 2.5 * MM, CX, CY + 2.5 * MM)
    c.circle(CX, CY, 1.2 * MM, stroke=1, fill=0)


def rim_text(c, text, r, mid, size, color, max_w):
    """Text along an arc of a turning disc, centred on radius r (pt), with
    its top always toward the rim, so every name reads the same way as the
    disc turns."""
    size = fit_size(text, BOLD, size, max_w, 0.3)
    arc_text(c, text, CX, CY, r - size * 0.36, mid, BOLD, size, color, False, 0.3)


def d1_windows():
    """Windows of the front of disc 1: (inner, outer radius in mm, start,
    end angle in degrees counter-clockwise from 3 o'clock)."""
    return [(r0 + 1, r1 - 1, a - 10, a + 10) for (r0, r1), a in zip(D1_BANDS, D1_TAB_ANGLES)]


def d2_windows():
    """Windows of the front of disc 2: the 12 at the rim, then the 8 large ones."""
    rim = [(D2_NAME_R[0] + 1, D2_FRONT - 3, hue_angle(i) - 12, hue_angle(i) + 12)
           for i in range(12)]
    fans = [(D2_FAN_R[0], D2_FAN_R[1], 90 - a - 11, 90 - a + 11) for a in D2_FANS]
    return rim + fans


def disc_base(c, r, holes=()):
    """On screen, the paper of a disc: a circle of the paper colour with the windows cut
    out (even-odd fill), so what lies below shows through. Printed pages
    need none."""
    if not _VIRTUAL:
        return
    p = c.beginPath()
    p.circle(CX, CY, r * MM)
    for r0, r1, a0, a1 in holes:
        pts = ring_wedge(CX, CY, r0 * MM, r1 * MM, a0, a1, 16)
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        p.close()
    c.setFillColorRGB(*PAPER)
    c.drawPath(p, stroke=0, fill=1, fillMode=FILL_EVEN_ODD)


def disc_outline(c, r):
    c.setStrokeColorRGB(*LINE)
    c.setLineWidth(.8)
    c.circle(CX, CY, r * MM, stroke=1, fill=0)


def wrap_lines(text, font, size, width_at):
    """Greedy word wrap where width_at(n) gives the width of line n."""
    words, lines = i18n.words(text), []
    while words:
        line = words.pop(0)[1]
        while words and stringWidth(line + "".join(words[0]), font, size) <= width_at(len(lines)):
            line += "".join(words.pop(0))
        lines.append(line)
    return lines


def flow(c, items, y, bounds, size, x_shift=0.0):
    """Write (heading, text) items line by line from height y down. Each
    line may have its own extent: bounds(y) -> (x0, x1) in the current
    frame. The heading is bold and runs into the text. Returns the next y."""
    lead = size * 1.24
    rtl = i18n.rtl()                        # Arabic: words go from the right edge leftwards
    c.setFillColorRGB(*INK)
    for head, body in items:
        colon = "：" if i18n.script(_LANG) in ("zh", "ja") else ":"
        words = ([(s, w, BOLD) for s, w in i18n.words(head + colon)]
                 + [(" " if k == 0 else s, w, REG) for k, (s, w) in enumerate(i18n.words(body))])
        while words:
            x0, x1 = bounds(y)
            x, first = x0 + x_shift, True
            while words:
                sep, w, font = words[0]
                gap = 0 if first else stringWidth(sep, REG, size)
                ww = stringWidth(i18n.visual(w), font, size) + gap   # joined letters are narrower
                if not first and x + ww > x1:
                    break
                c.setFont(font, size)
                if rtl:
                    c.drawRightString(x1 - (x - x0 - x_shift) - gap, y, w)
                else:
                    c.drawString(x + gap, y, w)
                x += ww
                first = False
                words.pop(0)
            y -= lead
        y -= lead * .35
    return y


def page_frame(c, head, page):
    """Header with the piece name and the scale bar, legend and page number."""
    if _VIRTUAL:
        return
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    tracked(c, T(head), W / 2, H - 52, BOLD, 15, INK, 1.6, align="center", max_w=W - 80)
    x0, y0 = W / 2 - 50 * MM, H - 82
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(1)
    c.line(x0, y0, x0 + 100 * MM, y0)
    for k in range(11):
        t = 4 if k % 5 == 0 else 2.2
        c.line(x0 + k * 10 * MM, y0, x0 + k * 10 * MM, y0 + t)
    c.setFont(REG, 6)
    c.setFillColorRGB(*INK)
    c.drawString(x0, y0 - 9, "0")
    c.drawRightString(x0 + 100 * MM, y0 - 9, "100 mm")
    c.drawCentredString(W / 2, y0 - 9, T("scale"))

    # legend: cut line, hatched window, pierce mark
    y = 42
    xs = [60, 240, 410]
    labels = T("legend")
    c.setLineWidth(.8)
    c.setStrokeColorRGB(*BLACK)
    c.line(xs[0], y + 2.5, xs[0] + 22, y + 2.5)
    c.saveState()
    c.rect(xs[1], y - 2, 22, 9, stroke=1, fill=0)
    c.setStrokeColorRGB(.7, .7, .7)
    c.setLineWidth(.5)
    p = c.beginPath()
    p.rect(xs[1], y - 2, 22, 9)
    c.clipPath(p, stroke=0, fill=0)
    for k in range(-10, 30, 3):
        c.line(xs[1] + k, y - 2, xs[1] + k + 9, y + 7)
    c.restoreState()
    c.setLineWidth(.5)
    c.line(xs[2] + 4, y + 2.5, xs[2] + 18, y + 2.5)
    c.line(xs[2] + 11, y - 4.5, xs[2] + 11, y + 9.5)
    c.circle(xs[2] + 11, y + 2.5, 3.4, stroke=1, fill=0)
    for x, text in zip(xs, labels):
        tracked(c, text, x + 28, y, REG, 7, INK, max_w=140)
    c.setFont(REG, 6.5)
    c.drawRightString(W - 40, 22, T("page") % (page, NPAGES))


# ==========================================================================
# 3. INSTRUCTION PAGES
# ==========================================================================
def text_column(c, x, y, width, blocks, size=9.2):
    """blocks: (heading, [paragraphs]); paragraphs are bulleted. Returns y."""
    lead = size * 1.32
    for head, paras in blocks:
        tracked(c, head, x, y, BOLD, size + 1.6, INK, 1.0, max_w=width)
        y -= lead * 1.6
        for para in paras:
            lines = i18n.wrap(para, REG, size, width - 10)
            c.setFillColorRGB(*INK)
            c.circle(x + width - 2.5 if i18n.rtl() else x + 2.5, y + size * .32, 1.3, stroke=0, fill=1)
            c.setFont(REG, size)
            for ln in lines:
                i18n.draw_line(c, x + (0 if i18n.rtl() else 10), y, ln, width - 10)
                y -= lead
            y -= lead * .3
        y -= lead * .8
    return y


def draw_assembly(c, x, y, w):
    """Exploded view: back disc, front disc above it, split pin through both."""
    rx, ry = w / 2, w / 2 * .32
    # back disc: ring of hues seen at a slant
    c.saveState()
    c.translate(x, y)
    c.scale(1, .32)
    for i in range(12):
        a = hue_angle(i)
        fill_poly(c, ring_wedge(0, 0, rx * .72, rx, a - 15, a + 15, 6), hue_colour(i), WHITE, .6)
    c.setFillColorRGB(.93, .93, .93)
    c.circle(0, 0, rx * .72, stroke=0, fill=1)
    c.restoreState()
    # front disc, lifted
    dy = 70
    c.saveState()
    c.translate(x, y + dy)
    c.scale(1, .32)
    c.setFillColorRGB(1, 1, 1)
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(1.2)
    c.circle(0, 0, rx * .84, stroke=1, fill=1)
    for k, a in enumerate(D1_TAB_ANGLES):
        r0, r1 = (v * rx * .84 / D1_FRONT for v in D1_BANDS[k])
        fill_poly(c, ring_wedge(0, 0, r0, r1, a - 10, a + 10, 5), (.85, .85, .85), INK, .8)
    c.restoreState()
    # split pin
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(1.4)
    c.setDash(3, 2)
    c.line(x, y - 22, x, y + dy + 30)
    c.setDash()
    c.setFillColorRGB(.75, .62, .25)
    c.circle(x, y + dy + 32, 4.5, stroke=1, fill=1)
    c.setFont(REG, 7.5)
    c.setFillColorRGB(*INK)
    c.drawString(x + 9, y + dy + 30, T("fig_pin"))
    c.drawString(x + rx * .84 + 6, y + dy - 2, T("fig_front"))
    c.drawString(x + rx + 6, y - 2, T("fig_back"))


def build_page_1(c):
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    tracked(c, T("title"), W / 2, H - 70, BOLD, 21, INK, 2.2, align="center", max_w=W - 70)
    c.setFont(REG, 9.5)
    c.setFillColorRGB(.3, .3, .3)
    y = H - 92
    for ln in i18n.wrap(T("subtitle"), REG, 9.5, 440):
        c.drawCentredString(W / 2, y, ln)
        y -= 12
    left = [(T("need_t"), T("need")), (T("print_t"), T("print")), (T("cut_t"), T("cut"))]
    text_column(c, 48, H - 150, 240, left)
    y = text_column(c, 312, H - 150, 240, [(T("build_t"), T("build"))])
    draw_assembly(c, 410, y - 110, 150)
    text_column(c, 312, y - 175, 240, [(T("pieces_t"), T("pieces"))])
    c.setFont(REG, 6.5)
    c.setFillColorRGB(*INK)
    c.drawRightString(W - 40, 22, T("page") % (1, NPAGES))


def build_page_2(c):
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    tracked(c, T("use_t"), W / 2, H - 70, BOLD, 21, INK, 2.2, align="center", max_w=W - 70)
    left, right = (312, 48) if i18n.rtl() else (48, 312)    # Arabic reads the right column first
    text_column(c, left, H - 120, 240, [(T("use1_t"), T("use1")), (T("use2_t"), T("use2"))])
    x, y, width, size = right, H - 120, 240, 8.6
    tracked(c, T("gloss_t"), x, y, BOLD, size + 1.6, INK, 1.0, max_w=width)
    y -= size * 2.1
    for term, text in T("gloss"):
        y = flow(c, [(term, text)], y, lambda yy: (x, x + width), size) + size * .2
    c.setFont(ITAL, 8)
    c.setFillColorRGB(.35, .35, .35)
    y -= 8
    for ln in i18n.wrap(T("note"), ITAL, 8, width):
        i18n.draw_line(c, x, y, ln, width)
        y -= 10
    c.setFont(REG, 6.5)
    c.setFillColorRGB(*INK)
    c.drawRightString(W - 40, 22, T("page") % (2, NPAGES))


# ==========================================================================
# 4. DISC 1  (mixing colours)
# ==========================================================================
def build_disc1_back(c):
    """Outer ring of the 12 hues with names; inside it, five bands of 12
    cells. The cell of hue i in band k sits at hue i's angle and holds hue i
    mixed with what tab k adds, so it shows in window k exactly when hue i
    stands beyond tab k."""
    page_frame(c, "head_d1b", 3)
    disc_base(c, D1_BACK)
    names = hue_names()
    for i in range(12):
        a = hue_angle(i)
        col = hue_colour(i)
        fill_poly(c, ring_wedge(CX, CY, (D1_FRONT - 3) * MM, D1_BACK * MM, a - 15, a + 15, 10),
                  col, PAPER, .8)
        rim_text(c, names[i], (D1_FRONT + D1_BACK) / 2 * MM, a, 7.4, text_on(col),
                 max_w=math.radians(28) * (D1_FRONT + D1_BACK) / 2 * MM)
        for k, (r0, r1) in enumerate(D1_BANDS):
            fill_poly(c, ring_wedge(CX, CY, r0 * MM, r1 * MM, a - 15, a + 15, 6),
                      mixture(i, k), PAPER, .5)
    disc_outline(c, D1_BACK)
    pierce_mark(c)


def build_disc1_front(c):
    page_frame(c, "head_d1f", 4)
    R = D1_FRONT
    disc_base(c, R, d1_windows())
    # tabs with what they add, pointer lines and the five windows
    for k, a in enumerate(D1_TAB_ANGLES):
        col = TAB_COLOURS[k]
        # the white or black tab, when close to the paper colour, gets a grey edge
        edge = (.6, .6, .6) if k >= 3 and abs(luma(col) - luma(PAPER)) < .3 else PAPER
        fill_poly(c, ring_wedge(CX, CY, (R - 6) * MM, R * MM, a - 14, a + 14, 10), col, edge, .6)
        ring_text(c, T("tabs")[k], CX, CY, (R - 3) * MM, a, 6.8, text_on(col),
                  max_w=math.radians(26) * (R - 3) * MM)
        r0, r1 = D1_BANDS[k]
        window(c, *d1_windows()[k])
        c.setStrokeColorRGB(*INK)
        c.setLineWidth(.6)
        x0, y0 = pol(CX, CY, (R - 7) * MM, a)
        x1, y1 = pol(CX, CY, (r1 + .5) * MM, a)
        c.line(x0, y0, x1, y1)
        ux, uy = math.cos(math.radians(a)), math.sin(math.radians(a))
        fill_poly(c, [(x1, y1), (x1 + 5 * ux - 2.2 * uy, y1 + 5 * uy + 2.2 * ux),
                      (x1 + 5 * ux + 2.2 * uy, y1 + 5 * uy - 2.2 * ux)], INK, INK, .1)
    c.setStrokeColorRGB(*RULE)
    c.setLineWidth(.4)
    for b in (165, 135, 105, 75, 45, 15):
        c.line(*pol(CX, CY, 9 * MM, b), *pol(CX, CY, (R - 6) * MM, b))

    # grey scale, value 1 (black, left) round the bottom to value 10 (white);
    # white figures on the dark half (1-5), black on the light half (6-10)
    g0, g1 = 61, 75
    for v in range(1, 11):
        a0 = 180 + 18 * (v - 1)
        col = grey_value(v)
        ink = WHITE if v <= 5 else BLACK
        fill_poly(c, ring_wedge(CX, CY, g0 * MM, g1 * MM, a0, a0 + 18, 6), col, (.55, .55, .55),
                  .5)
        # the two ends also say what they are, on the line above the value
        extra = {1: ("full_black", -1), 10: ("full_white", 1)}.get(v)
        if extra:
            key, up = extra
            size = fit_size(T(key), BOLD, 5.2, (g1 - g0 - 3) * MM, 0)
            radial_text(c, T(key), CX, CY, (g0 + 1.6) * MM, a0 + 9 + 3.6 * up, size, ink,
                        font=BOLD)
            radial_text(c, "%s %d" % (T("value"), v), CX, CY, (g0 + 1.6) * MM,
                        a0 + 9 - 2.8 * up, 5.6, ink, font=BOLD)
        else:
            radial_text(c, "%s %d" % (T("value"), v), CX, CY, (g0 + 1.6) * MM, a0 + 9, 5.6,
                        ink, font=BOLD)
    ring_text(c, T("grey_title"), CX, CY, (g0 - 2.6) * MM, 270, 6.4, INK, max_w=120)

    # centre: title, how to use, definitions in two columns
    tracked(c, T("d1_title"), CX, CY - 8 * MM, BOLD, 9, INK, .8, align="center",
            max_w=70 * MM)
    c.setFont(REG, 6.8)
    c.setFillColorRGB(*INK)
    y = CY - 12.5 * MM
    for ln in i18n.wrap(T("d1_how"), REG, 6.8, 80 * MM):
        c.drawCentredString(CX, y, ln)
        y -= 8.4
    y -= 6
    r_lim, gap, col_w = 56 * MM, 3 * MM, 45 * MM

    def half_chord(yy):
        d = CY - yy + 2.5
        return min(col_w, math.sqrt(max(0.0, r_lim ** 2 - d * d)))

    flow(c, T("d1_left"), y, lambda yy: (CX - half_chord(yy), CX - gap), 6.6)
    flow(c, T("d1_right"), y, lambda yy: (CX + gap, CX + half_chord(yy)), 6.6)

    disc_outline(c, R)
    pierce_mark(c)


# ==========================================================================
# 5. DISC 2  (colour relationships)
# ==========================================================================
def build_disc2_back(c):
    """Ring of the 12 hues with names (seen through the rim windows and as a
    grip beyond the front disc); inside it, tint, tone and shade of each
    hue (seen through the large windows)."""
    page_frame(c, "head_d2b", 5)
    disc_base(c, D2_BACK)
    names = hue_names()
    r_name = (D2_NAME_R[0] + D2_FRONT - 3) / 2.0          # middle of the rim windows
    for i in range(12):
        a = hue_angle(i)
        col = hue_colour(i)
        fill_poly(c, ring_wedge(CX, CY, D2_NAME_R[0] * MM, D2_NAME_R[1] * MM, a - 15, a + 15,
                                10), col, PAPER, .8)
        rim_text(c, names[i], r_name * MM, a, 6.6, text_on(col),
                 max_w=math.radians(21) * r_name * MM)
        variants = (mix(col, WHITE, .55), mix(col, (.55, .55, .55), .5), mix(col, BLACK, .5))
        for (r0, r1), v in zip(D2_BANDS, variants):
            fill_poly(c, ring_wedge(CX, CY, r0 * MM, r1 * MM, a - 15, a + 15, 6), v, PAPER, .5)
    disc_outline(c, D2_BACK)
    pierce_mark(c)


def sector_flow(c, items, mid, half, r1, size):
    """Flow text into the gap between windows centred on angle mid (degrees,
    screen), half-width `half` degrees, inside radius r1 (pt). The text runs
    across the gap, tangentially, from the outer edge inward."""
    c.saveState()
    c.translate(CX, CY)
    c.rotate(mid - 90)
    t = math.tan(math.radians(half))

    def bounds(yy):
        w = min(yy * t, math.sqrt(max(0.0, r1 ** 2 - (yy + size) ** 2))) - 2.5
        return -w, w

    flow(c, items, r1 - size * 1.6, bounds, size)
    c.restoreState()


def side_flow(c, items, side, half, r0, r1, size):
    """Flow horizontal text into the gap on the right (side=1) or left
    (side=-1) of the disc: between radii r0 and r1, within `half` degrees
    of the horizontal."""
    t = math.tan(math.radians(half))
    lead = size * 1.24
    n = sum(len(i18n.wrap(h + ": " + b, REG, size, r1 - r0 - 6)) for h, b in items)
    y_top = CY + (n * lead + lead * .35 * len(items)) / 2 - size

    def bounds(yy):
        dy = abs(yy - CY) + size
        x0 = max(r0, dy / t) + 2
        x1 = math.sqrt(max(0.0, r1 ** 2 - dy * dy)) - 2
        return (CX + x0, CX + x1) if side > 0 else (CX - x1, CX - x0)

    flow(c, items, y_top, bounds, size)


def draw_harmony_diagram(c, r):
    """Shapes on the front disc joining the windows (clockwise angles from
    the top): two tetrad rectangles, the triad, the split complementary and
    the complementary arrow."""
    def P(a, rr=r):
        return pol(CX, CY, rr, 90 - a)

    # opaque greys, drawn from back to front: the two tetrads darker (and
    # unequal), the triad light, the split complementary the paper colour
    # (on dark paper the order of the greys is reversed); then every
    # outline on top so no edge is hidden
    shapes = list(zip([(0, 60, 180, 240), (0, 120, 180, 300), (0, 120, 240), (0, 150, 210)],
                      DIAGRAM))
    for angles, col in shapes:
        c.setFillColorRGB(*col)
        c.drawPath(path_of(c, [P(a) for a in angles]), stroke=0, fill=1)
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(.5)
    for angles, _ in shapes:
        c.drawPath(path_of(c, [P(a) for a in angles]), stroke=1, fill=0)
    # complementary line, top to bottom
    c.setStrokeColorRGB(*LINE)
    c.setLineWidth(1.2)
    c.line(*P(0), *P(180))
    # an arrow from each corner to its window
    tip = (D2_FAN_R[0] - .6) * MM
    for a in D2_FANS:
        ux, uy = math.sin(math.radians(a)), math.cos(math.radians(a))
        x0, y0 = P(a)
        x1, y1 = P(a, tip)
        c.setLineWidth(.9)
        c.line(x0, y0, x1 - 4 * ux, y1 - 4 * uy)
        fill_poly(c, [(x1, y1), (x1 - 5 * ux - 2.4 * uy, y1 - 5 * uy + 2.4 * ux),
                      (x1 - 5 * ux + 2.4 * uy, y1 - 5 * uy - 2.4 * ux)], LINE, LINE, .1)
    c.saveState()
    c.translate(CX - 2.5, CY + r * .3)
    c.rotate(90)
    tracked(c, T("comp"), 0, 0, BOLD, 5.6, INK, .4, align="center", max_w=r * .62)
    c.restoreState()
    # labels on a ground of their shape's grey, so no line runs through them
    for key, a, rr, ground in (("tetrad", 40, .76, shapes[0][1]),
                               ("tetrad", -40, .76, shapes[1][1]),
                               ("triad", 242.5, .65, shapes[2][1]),
                               ("split", 180, .76, shapes[3][1])):
        x, y = P(a, r * rr)
        size = fit_size(T(key), BOLD, 5.2, r * .62, .3)
        w = stringWidth(T(key), BOLD, size) + .3 * len(T(key)) + 4
        c.setFillColorRGB(*ground)
        c.rect(x - w / 2, y - 3.6, w, 7.4, stroke=0, fill=1)
        tracked(c, T(key), x, y - 2, BOLD, size, INK, .3, align="center", max_w=r * .62)


def build_disc2_front(c):
    page_frame(c, "head_d2f", 6)
    R = D2_FRONT
    disc_base(c, R, d2_windows())
    for w in d2_windows():
        window(c, *w)
    # what each window means, along the rim
    for key, a in (("pure", 0), ("comp", 180), ("split", 150), ("split", 210)):
        ring_text(c, T(key), CX, CY, (R - 1.5) * MM, 90 - a, 5.2, INK,
                  max_w=math.radians(40) * R * MM)
    # tint / tone / shade beside the top window
    for side in (-1, 1):
        for (r0, r1), word in zip(D2_BANDS, T("bands")):
            r = (r0 + r1) / 2.0 + (1 if r0 == D2_BANDS[0][0] else 0)
            ring_text(c, word, CX, CY, r * MM, 90 + side * 16.5, 4.8, INK,
                      max_w=math.radians(8) * r * MM)
    draw_harmony_diagram(c, 41 * MM)

    # text in the gaps between the large windows
    r0, r1 = (D2_FAN_R[0] + 1) * MM, (D2_NAME_R[0] - .5) * MM
    c.saveState()
    c.translate(CX, CY)
    c.rotate(57 - 90)
    y = r1 - 14
    for ln in i18n.wrap(T("d2_title"), BOLD, 7.6, 22 * MM):
        tracked(c, ln, 0, y, BOLD, 7.6, INK, .6, align="center")
        y -= 9.5
    c.restoreState()
    sector_flow(c, T("d2_how"), 121, 12, r1, 5.6)
    side_flow(c, T("d2_defs_a"), 1, 18, r0, r1, 5.6)
    side_flow(c, T("d2_defs_b"), -1, 18, r0, r1, 5.6)

    disc_outline(c, R)
    pierce_mark(c)


# ==========================================================================
# 6. DISCS ON SCREEN
#    The disc pages are drawn once more into a canvas that only records
#    shapes, and the record is written out as SVG (web page) or as a
#    bitmap with Pillow (desktop app).
# ==========================================================================
PARTS = [("d1b", build_disc1_back), ("d1f", build_disc1_front),
         ("d2b", build_disc2_back), ("d2f", build_disc2_front)]
VIEW_MM = 96                                # half the side of the square round a disc
STEP = 30                                   # one hue, in degrees


class _RecPath:
    """Just enough of a ReportLab path: closed subpaths of straight lines."""

    def __init__(self):
        self.subpaths = []

    def moveTo(self, x, y):
        self.subpaths.append([(x, y)])

    def lineTo(self, x, y):
        self.subpaths[-1].append((x, y))

    def close(self):
        pass

    def circle(self, x, y, r):
        n = max(64, int(r / 2))
        self.subpaths.append([(x + r * math.cos(2 * math.pi * k / n),
                               y + r * math.sin(2 * math.pi * k / n)) for k in range(n)])

    def rect(self, x, y, w, h):
        self.subpaths.append([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])


class _RecText:
    """Just enough of a ReportLab text object for tracked()."""

    def __init__(self):
        self.font, self.size, self.space = REG, 10, 0.0
        self.x = self.y = 0.0
        self.colour, self.runs = None, []

    def setFont(self, font, size):
        self.font, self.size = font, size

    def setCharSpace(self, space):
        self.space = space

    def setTextOrigin(self, x, y):
        self.x, self.y = x, y

    def setFillColorRGB(self, r, g, b):
        self.colour = (r, g, b)

    def textOut(self, text):
        text = i18n.visual(text)
        self.runs.append((text, self.x, self.y, self.font, self.size, self.space, self.colour))
        self.x += stringWidth(text, self.font, self.size) + self.space * len(text)


class ShapeRecorder:
    """Stands in for a ReportLab canvas while a disc is drawn, and keeps every
    shape in page coordinates:
      ("path", subpaths, fill, stroke, width, even_odd, closed)
      ("text", text, x, y, angle, font, size, colour)
    Only what the disc pages use is there; clipping is not."""

    def __init__(self):
        self.items = []
        self._m = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
        self._fill, self._stroke, self._lw, self._font = BLACK, BLACK, 1.0, (REG, 10)
        self._stack = []

    # state and transformations
    def saveState(self):
        self._stack.append((self._m, self._fill, self._stroke, self._lw, self._font))

    def restoreState(self):
        self._m, self._fill, self._stroke, self._lw, self._font = self._stack.pop()

    def _concat(self, a, b, c, d, e, f):
        m = self._m
        self._m = (m[0] * a + m[2] * b, m[1] * a + m[3] * b, m[0] * c + m[2] * d,
                   m[1] * c + m[3] * d, m[0] * e + m[2] * f + m[4], m[1] * e + m[3] * f + m[5])

    def translate(self, dx, dy):
        self._concat(1, 0, 0, 1, dx, dy)

    def rotate(self, deg):
        co, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        self._concat(co, si, -si, co, 0, 0)

    def _pt(self, x, y):
        m = self._m
        return m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]

    def _scale(self):
        return math.hypot(self._m[0], self._m[1])

    def setFillColorRGB(self, r, g, b):
        self._fill = (r, g, b)

    def setStrokeColorRGB(self, r, g, b):
        self._stroke = (r, g, b)

    def setLineWidth(self, w):
        self._lw = w

    def setFont(self, font, size):
        self._font = (font, size)

    # shapes
    def beginPath(self):
        return _RecPath()

    def drawPath(self, p, stroke=1, fill=0, fillMode=None):
        subs = [[self._pt(*q) for q in s] for s in p.subpaths]
        self.items.append(("path", subs, self._fill if fill else None,
                           self._stroke if stroke else None, self._lw * self._scale(),
                           fillMode == FILL_EVEN_ODD, True))

    def clipPath(self, *args, **kwargs):
        raise NotImplementedError("clipping is not drawn on screen")

    def line(self, x1, y1, x2, y2):
        self.items.append(("path", [[self._pt(x1, y1), self._pt(x2, y2)]], None, self._stroke,
                           self._lw * self._scale(), False, False))

    def rect(self, x, y, w, h, stroke=1, fill=0):
        p = _RecPath()
        p.rect(x, y, w, h)
        self.drawPath(p, stroke, fill)

    def circle(self, x, y, r, stroke=1, fill=0):
        p = _RecPath()
        p.circle(x, y, r)
        self.drawPath(p, stroke, fill)

    # text
    def _text(self, text, x, y, font, size, colour, space=0.0):
        ang = math.degrees(math.atan2(self._m[1], self._m[0]))
        if space:              # letter-spaced: one item per letter
            for ch in text:
                self._text(ch, x, y, font, size, colour)
                x += stringWidth(ch, font, size) + space
            return
        X, Y = self._pt(x, y)
        self.items.append(("text", text, X, Y, ang, font, size * self._scale(), colour))

    def drawString(self, x, y, text):
        text = i18n.visual(text)
        self._text(text, x, y, self._font[0], self._font[1], self._fill)

    def drawCentredString(self, x, y, text):
        text = i18n.visual(text)
        w = stringWidth(text, *self._font)
        self._text(text, x - w / 2.0, y, self._font[0], self._font[1], self._fill)

    def drawRightString(self, x, y, text):
        text = i18n.visual(text)
        w = stringWidth(text, *self._font)
        self._text(text, x - w, y, self._font[0], self._font[1], self._fill)

    def beginText(self):
        return _RecText()

    def drawText(self, t):
        for text, x, y, font, size, space, colour in t.runs:
            self._text(text, x, y, font, size, colour or self._fill, space)


def record_part(build, lang, theme="light"):
    """The shapes of one disc (a build_disc* function) in language lang and
    theme "light" or "dark"."""
    global _LANG, _VIRTUAL
    old = _LANG, _VIRTUAL, i18n.current()
    _LANG, _VIRTUAL = lang, True
    i18n.use_lang(lang)
    set_theme(theme)
    try:
        rec = ShapeRecorder()
        build(rec)
    finally:
        _LANG, _VIRTUAL = old[:2]
        i18n.use_lang(old[2])
        set_theme("light")
    return rec.items


def _hex(col):
    return "#%02x%02x%02x" % tuple(int(round(255 * v)) for v in col)


def items_to_svg(items, lang="en"):
    """SVG of one disc: a square of 2 * VIEW_MM millimetres centred on it."""
    half = VIEW_MM * MM
    x0, top = CX - half, CY + half

    def P(x, y):
        return "%.2f,%.2f" % (x - x0, top - y)

    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.2f %.2f" font-family="%s">'
           % (2 * half, 2 * half, i18n.css_family(lang).replace('"', "'"))]
    for it in items:
        if it[0] == "path":
            _, subs, fill, stroke, lw, even_odd, closed = it
            d = " ".join("M" + " L".join(P(*q) for q in s) + (" Z" if closed else "")
                         for s in subs)
            attrs = 'fill="%s"' % (_hex(fill) if fill else "none")
            if even_odd:
                attrs += ' fill-rule="evenodd"'
            if stroke:
                attrs += ' stroke="%s" stroke-width="%.2f" stroke-linejoin="round"' % (
                    _hex(stroke), lw)
            out.append('<path d="%s" %s/>' % (d, attrs))
        elif it[1].strip():
            _, text, x, y, ang, font, size, col = it
            X, Y = x - x0, top - y
            extra = (' font-weight="bold"' if font == BOLD else "") + i18n.svg_bidi(lang)
            if abs(ang) > .01:
                extra += ' transform="rotate(%.2f %.2f %.2f)"' % (-ang, X, Y)
            out.append('<text x="%.2f" y="%.2f" font-size="%.2f" fill="%s"%s>%s</text>'
                       % (X, Y, size, _hex(col), extra, xml_escape(text)))
    out.append("</svg>\n")
    return "\n".join(out)


# The bitmaps use the font files of i18n (close to Helvetica for Western languages).
_fonts = {}


def _font(name, px, lang="en"):
    from PIL import ImageFont
    key = (i18n.script(lang), i18n.rtl(lang), name, round(px * 4) / 4.0)
    if key not in _fonts:
        path = i18n.font_file(lang, {REG: 0, BOLD: 1, ITAL: 2}.get(name, 0))
        try:
            _fonts[key] = i18n.pil_font(path, key[3], lang)
        except (OSError, TypeError, AttributeError):
            _fonts[key] = ImageFont.load_default(key[3])
    return _fonts[key]


def items_to_image(items, size, ss=3, lang="en"):
    """Bitmap (Pillow RGBA, size x size pixels) of one disc, drawn ss times
    larger and scaled down for smooth edges. In an even-odd path the first
    subpath is filled and the others are cut out of it."""
    from PIL import Image, ImageDraw
    S = size * ss
    k = S / (2 * VIEW_MM * MM)
    x0, top = CX - VIEW_MM * MM, CY + VIEW_MM * MM

    def P(x, y):
        return (x - x0) * k, (top - y) * k

    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for it in items:
        if it[0] == "path":
            _, subs, fill, stroke, lw, even_odd, closed = it
            pts = [[P(*q) for q in s] for s in subs]
            if fill:
                for n, s in enumerate(pts):
                    hole = even_odd and n > 0
                    draw.polygon(s, fill=(0, 0, 0, 0) if hole else _hex(fill))
            if stroke:
                w = max(1, int(round(lw * k)))
                for s in pts:
                    draw.line(s + (s[:1] if closed else []), fill=_hex(stroke), width=w,
                              joint="curve")
        elif it[1].strip():
            _, text, x, y, ang, font, fs, col = it
            f = _font(font, fs * k, lang)
            X, Y = P(x, y)
            if abs(ang) < .01:
                draw.text((X, Y), text, font=f, fill=_hex(col), anchor="ls")
                continue
            pad = int(f.getlength(text) + 2 * fs * k) + 2
            tile = Image.new("RGBA", (2 * pad, 2 * pad), (0, 0, 0, 0))
            ImageDraw.Draw(tile).text((pad, pad), text, font=f, fill=_hex(col), anchor="ls")
            tile = tile.rotate(ang, resample=Image.BICUBIC, center=(pad, pad))
            img.paste(tile, (int(round(X)) - pad, int(round(Y)) - pad), tile)
    return img.resize((size, size), Image.LANCZOS)


def disc_geometry():
    """Radii and windows (mm, degrees) of both discs, for finding which part
    lies under the pointer."""
    return [{"back_r": D1_BACK, "front_r": D1_FRONT, "windows": d1_windows()},
            {"back_r": D2_BACK, "front_r": D2_FRONT, "windows": d2_windows()}]


def hit_part(disc, r, ang, front_turn):
    """Index in PARTS of the part of disc 0 or 1 under a point at r mm from
    the centre and at angle ang (degrees, counter-clockwise from 3 o'clock),
    with the front disc turned front_turn degrees clockwise; None if off it."""
    g = disc_geometry()[disc]
    if r > g["back_r"]:
        return None
    if r > g["front_r"]:
        return 2 * disc
    a = ang + front_turn
    for r0, r1, a0, a1 in g["windows"]:
        if r0 <= r <= r1 and (a - a0) % 360 <= a1 - a0:
            return 2 * disc
    return 2 * disc + 1


# ==========================================================================
# 7. DESKTOP APP  (Tkinter)
# ==========================================================================
# Window colours of each theme (the same as web/style.css).
UI_COLOURS = {
    "light": {"bg": "#f4f4f2", "fg": "#2e2e2e", "muted": "#5c5c5c", "field": "#ffffff",
              "border": "#b9b9b4", "accent": "#1a73e8"},
    "dark": {"bg": "#1e1e20", "fg": "#e6e6e6", "muted": "#a8a8a8", "field": "#2c2c2f",
             "border": "#4a4a4e", "accent": "#8ab4f8"},
}


def system_theme():
    """"dark" when the operating system uses dark mode (Windows, macOS), else "light"."""
    try:
        if os.name == "nt":
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows"
                                 r"\CurrentVersion\Themes\Personalize")
            return "light" if winreg.QueryValueEx(key, "AppsUseLightTheme")[0] else "dark"
        if os.uname().sysname == "Darwin":
            import subprocess
            out = subprocess.run(["defaults", "read", "-g", "AppleInterfaceStyle"],
                                 capture_output=True, text=True).stdout
            return "dark" if "Dark" in out else "light"
    except (OSError, AttributeError):
        pass
    return "light"


class WheelApp:
    """Both wheels side by side. Each part (back and front of each disc)
    turns by dragging it, with the mouse wheel, or with the arrow keys."""

    def __init__(self, root, lang, theme="light"):
        import tkinter as tk
        from tkinter import ttk
        self.tk, self.root, self.theme = tk, root, theme
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        self.size = int(max(300, min((sw - 100) / 2, sh - 300, 640)))
        self.gap = 30
        self.turn = [0.0] * 4               # clockwise turn of each part, degrees
        self.sel, self.drag, self.images, self.photos = 1, None, {}, [None, None]
        self.moving = None                  # part being dragged or eased
        self.turned = [None] * 4            # last rotated image of each part
        self.pending, self.after_id = set(), None
        self.style = ttk.Style(root)
        self.style.theme_use("clam")        # the built-in theme that takes custom colours

        bar = ttk.Frame(root, padding=(14, 10))
        bar.pack(fill="x")
        self.title = ttk.Label(bar, font=("Helvetica", 15, "bold"))
        self.title.pack(side="left")
        self.reset_btn = ttk.Button(bar, command=self.reset)
        self.reset_btn.pack(side="right")
        self.theme_btn = ttk.Button(bar, command=self.toggle_theme)
        self.theme_btn.pack(side="right", padx=(0, 8))
        self.lang_box = ttk.Combobox(bar, state="readonly", width=20,
                                     values=[LANG_NAMES[k] for k in languages()])
        self.lang_box.pack(side="right", padx=(6, 14))
        self.lang_box.bind("<<ComboboxSelected>>", self.on_lang)
        self.lang_label = ttk.Label(bar)
        self.lang_label.pack(side="right")

        w = 2 * self.size + self.gap
        self.canvas = tk.Canvas(root, width=w + 28, height=self.size + 20,
                                highlightthickness=0)
        self.canvas.pack(padx=0, pady=0)
        self.status = ttk.Label(root, padding=(14, 4))
        self.status.pack(anchor="w")
        self.help = ttk.Label(root, padding=(14, 0, 14, 12), justify="left",
                              wraplength=w)
        self.help.pack(anchor="w")

        cv = self.canvas
        cv.bind("<ButtonPress-1>", self.on_press)
        cv.bind("<B1-Motion>", self.on_move)
        cv.bind("<ButtonRelease-1>", self.on_release)
        cv.bind("<MouseWheel>", lambda e: self.on_wheel(e, -1 if e.delta > 0 else 1))
        cv.bind("<Button-4>", lambda e: self.on_wheel(e, -1))
        cv.bind("<Button-5>", lambda e: self.on_wheel(e, 1))
        cv.bind("<Left>", lambda e: self.turn_by(self.sel, -STEP))
        cv.bind("<Right>", lambda e: self.turn_by(self.sel, STEP))
        cv.bind("<Up>", lambda e: self.select(self.sel - 1))
        cv.bind("<Down>", lambda e: self.select(self.sel + 1))
        cv.bind("<Tab>", lambda e: self.select(self.sel + 1) or "break")
        cv.bind("<Shift-Tab>", lambda e: self.select(self.sel - 1) or "break")
        self.apply_theme()
        self.set_lang(lang)
        cv.focus_set()

    # theme
    def apply_theme(self):
        """Window colours, the canvas ground and the title bar of the theme."""
        from PIL import Image
        c, st = UI_COLOURS[self.theme], self.style
        self.root.configure(bg=c["bg"])
        self.canvas.configure(bg=c["bg"])
        self.ground = Image.new("RGBA", (self.size, self.size), c["bg"])
        st.configure(".", background=c["bg"], foreground=c["fg"], bordercolor=c["border"],
                     lightcolor=c["field"], darkcolor=c["field"], troughcolor=c["bg"])
        st.configure("TLabel", background=c["bg"], foreground=c["fg"])
        st.configure("TButton", background=c["field"], foreground=c["fg"], padding=(10, 3))
        st.map("TButton", background=[("active", c["border"])], bordercolor=[("focus",
                                                                              c["accent"])])
        st.configure("TCombobox", fieldbackground=c["field"], background=c["field"],
                     foreground=c["fg"], arrowcolor=c["fg"])
        st.map("TCombobox", fieldbackground=[("readonly", c["field"])],
               foreground=[("readonly", c["fg"])], selectbackground=[("readonly", c["field"])],
               selectforeground=[("readonly", c["fg"])])
        # the list that drops down from the language box
        for opt, val in (("background", c["field"]), ("foreground", c["fg"]),
                         ("selectBackground", c["accent"]), ("selectForeground", c["bg"])):
            self.root.option_add("*TCombobox*Listbox." + opt, val)
        try:
            pop = self.root.tk.call("ttk::combobox::PopdownWindow", self.lang_box)
            self.root.tk.call(pop + ".f.l", "configure", "-background", c["field"],
                              "-foreground", c["fg"])
        except self.tk.TclError:
            pass
        self.help.configure(foreground=c["muted"])
        if os.name == "nt":             # dark or light title bar (Windows 10 2004 and later)
            try:
                import ctypes
                self.root.update_idletasks()
                hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
                on = ctypes.c_int(1 if self.theme == "dark" else 0)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(on), 4)
            except (AttributeError, OSError):
                pass

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.apply_theme()
        self.set_lang(_LANG)
        self.canvas.focus_set()

    # geometry of the canvas
    def centre(self, disc):
        return 14 + self.size / 2 + disc * (self.size + self.gap), 10 + self.size / 2

    def px_per_mm(self):
        return self.size / (2.0 * VIEW_MM)

    def locate(self, x, y):
        """(disc, r mm, angle) of a canvas point, or None between the discs."""
        disc = 0 if x < 14 + self.size + self.gap / 2 else 1
        cx, cy = self.centre(disc)
        dx, dy = (x - cx) / self.px_per_mm(), (cy - y) / self.px_per_mm()
        return disc, math.hypot(dx, dy), math.degrees(math.atan2(dy, dx))

    def part_at(self, x, y):
        disc, r, a = self.locate(x, y)
        return hit_part(disc, r, a, self.turn[2 * disc + 1]), a

    # language
    def on_lang(self, _event):
        name = self.lang_box.get()
        self.set_lang(next(k for k, v in LANG_NAMES.items() if v == name))
        self.canvas.focus_set()

    def set_lang(self, lang):
        global _LANG
        _LANG = lang
        self.lang_box.set(LANG_NAMES[lang])
        self.root.title(T("app_title"))
        self.title.config(text=T("app_title"))
        self.lang_label.config(text=T("app_lang") + ":")
        self.reset_btn.config(text=T("app_reset"))
        self.help.config(text="\n".join("• " + t for t in T("app_help")))
        self.theme_btn.config(text="☀  " + T("app_light") if self.theme == "dark"
                              else "☾  " + T("app_dark"))
        key = (lang, self.theme)
        if key not in self.images:
            self.canvas.delete("all")
            self.canvas.create_text(*self.centre(0), text=T("app_wait"), anchor="w",
                                    font=("Helvetica", 13), fill=UI_COLOURS[self.theme]["fg"])
            self.root.config(cursor="watch")
            self.root.update()
            self.images[key] = [items_to_image(record_part(build, lang, self.theme), self.size,
                                               lang=lang) for _, build in PARTS]
            self.root.config(cursor="")
        self.canvas.delete("all")
        self.photos = [None, None]
        self.redraw()

    # drawing
    def rotated(self, part):
        """Image of a part at its present turn, kept until the turn changes.
        The part that is moving turns with the quick bilinear filter; at
        rest it is redone with the smoother bicubic one."""
        from PIL import Image
        fast = part == self.moving
        key = (_LANG, self.theme)
        was_key, turn, was_fast, img = self.turned[part] or (None, None, None, None)
        if (was_key, turn) == (key, self.turn[part]) and (fast or not was_fast):
            return img
        img = self.images[key][part].rotate(
            -self.turn[part], resample=Image.BILINEAR if fast else Image.BICUBIC)
        self.turned[part] = (key, self.turn[part], fast, img)
        return img

    def redraw(self, discs=(0, 1)):
        from PIL import ImageTk
        cv = self.canvas
        for d in discs:
            # an opaque image on the canvas colour: Tk takes it far quicker
            # than one with transparency
            img = self.ground.copy()
            img.alpha_composite(self.rotated(2 * d))
            img.alpha_composite(self.rotated(2 * d + 1))
            img = img.convert("RGB")
            cx, cy = self.centre(d)
            if self.photos[d] is None:
                self.photos[d] = ImageTk.PhotoImage(img)
                cv.create_image(cx, cy, image=self.photos[d], tags="disc%d" % d)
            else:
                self.photos[d].paste(img)
            cv.delete("deco%d" % d)
            if self.sel // 2 == d:          # ring round the selected part
                g = disc_geometry()[d]
                r = (g["front_r"] if self.sel % 2 else g["back_r"]) * self.px_per_mm() + 2
                cv.create_oval(cx - r, cy - r, cx + r, cy + r,
                               outline=UI_COLOURS[self.theme]["accent"], width=3,
                               dash=(8, 5), tags="deco%d" % d)
            p = 2.6 * self.px_per_mm()      # the split pin
            cv.create_oval(cx - p, cy - p, cx + p, cy + p, fill="#b8b2a4", outline="#6d675c",
                           tags="deco%d" % d)
        self.status.config(text="%s: %s" % (T("app_selected"), T("parts")[self.sel]))

    def redraw_soon(self, disc):
        """Redraw once the pending mouse events are handled, so a fast drag
        draws only its latest position instead of falling behind."""
        self.pending.add(disc)
        if not self.after_id:
            self.after_id = self.root.after_idle(self.flush)

    def flush(self):
        discs, self.pending, self.after_id = self.pending, set(), None
        self.redraw(discs)

    # actions
    def select(self, part):
        old = self.sel // 2
        self.sel = part % 4
        self.redraw({old, self.sel // 2})

    def turn_by(self, part, deg):
        self.turn[part] += deg
        self.redraw((part // 2,))

    def reset(self):
        self.turn = [0.0] * 4
        self.redraw()
        self.canvas.focus_set()

    def on_press(self, e):
        self.canvas.focus_set()
        part, a = self.part_at(e.x, e.y)
        if part is None:
            return
        self.drag, self.moving = (part, a), part
        self.select(part)

    def on_move(self, e):
        if not self.drag:
            return
        part, a0 = self.drag
        cx, cy = self.centre(part // 2)             # angle round the dragged disc
        a = math.degrees(math.atan2(cy - e.y, e.x - cx))
        self.turn[part] -= (a - a0 + 180) % 360 - 180
        self.drag = (part, a)
        self.redraw_soon(part // 2)

    def on_release(self, _e):
        if not self.drag:
            return
        part = self.drag[0]
        self.drag = None
        self.snap(part)

    def snap(self, part, frames=6):
        """Ease the part to the nearest whole hue."""
        target = round(self.turn[part] / STEP) * STEP
        if frames <= 1 or abs(target - self.turn[part]) < .5:
            self.turn[part], self.moving = target, None
            self.redraw_soon(part // 2)
            return
        self.turn[part] += (target - self.turn[part]) / 2.0
        self.redraw_soon(part // 2)
        self.root.after(16, self.snap, part, frames - 1)

    def on_wheel(self, e, sign):
        part, _ = self.part_at(e.x, e.y)
        if part is None:
            return
        self.sel = part
        self.turn[part] = round(self.turn[part] / STEP) * STEP + sign * STEP
        self.redraw()


def run_app(lang, theme="auto"):
    import tkinter as tk
    root = tk.Tk()
    root.resizable(False, False)
    WheelApp(root, lang, system_theme() if theme == "auto" else theme)
    root.mainloop()


# ==========================================================================
# 8. WEB PAGE  (the SVG discs and the data for web/app.js)
# ==========================================================================
def export_web(folder):
    """Write folder/discs/<lang>/<part>.svg and <part>-dark.svg for every
    language and folder/discs/data.js with the texts and the disc geometry."""
    base = os.path.join(folder, "discs")
    for lang in languages():
        os.makedirs(os.path.join(base, lang), exist_ok=True)
        for name, build in PARTS:
            for theme, suffix in (("light", ""), ("dark", "-dark")):
                path = os.path.join(base, lang, name + suffix + ".svg")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(items_to_svg(record_part(build, lang, theme), lang))
    keys = ["app_title", "app_lang", "app_reset", "app_selected", "parts", "app_help",
            "app_dark", "app_light"]
    data = {"view_r": VIEW_MM, "step": STEP, "parts": [n for n, _ in PARTS],
            "lang_names": {k: LANG_NAMES[k] for k in languages()}, "discs": disc_geometry(),
            "rtl": sorted(i18n.RTL & set(languages())),
            "langs": {lang: {k: STRINGS[lang].get(k, STRINGS["en"][k]) for k in keys}
                      for lang in languages()}}
    with open(os.path.join(base, "data.js"), "w", encoding="utf-8") as f:
        f.write("// Written by color_wheel.py --web: do not edit by hand.\n")
        f.write("window.WHEEL_DATA = %s;\n" % json.dumps(data, ensure_ascii=False, indent=1))
    print("Saved", base)


def run_webview(lang, theme="auto"):
    """The web page in a window of its own (pip install pywebview): the same
    wheels as in the browser, without one. Writes web/discs first if they
    are missing."""
    import webview
    web = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
    if not os.path.exists(os.path.join(web, "discs", "en", "d2f-dark.svg")):
        export_web(web)
    theme = system_theme() if theme == "auto" else theme
    window = webview.create_window(STRINGS[lang]["app_title"], os.path.join(web, "index.html"),
                                   width=1360, height=860, min_size=(420, 500),
                                   background_color=UI_COLOURS[theme]["bg"])
    # the page reads ?lang= from its address; here it is told once loaded
    window.events.loaded += lambda: window.evaluate_js(
        "setLang(%s); setTheme(%s, false)" % (json.dumps(lang), json.dumps(theme)))
    webview.start()


# ==========================================================================
# 9. MAIN
# ==========================================================================
PAGES = [build_page_1, build_page_2, build_disc1_back, build_disc1_front, build_disc2_back,
         build_disc2_front]


def main():
    global _LANG
    ap = argparse.ArgumentParser(description="Build-your-own colour wheels (A4 PDF), and the "
                                             "same wheels on screen")
    ap.add_argument("--lang", default="en", choices=languages(), help="text language")
    ap.add_argument("-o", "--out", default=None, help="output PDF path")
    ap.add_argument("--app", action="store_true", help="open the wheels in a window to turn")
    ap.add_argument("--web", nargs="?", const="web", metavar="DIR",
                    help="write the discs and data for the web page (default folder: web)")
    ap.add_argument("--webview", action="store_true",
                    help="open the web page in a window of its own (needs pywebview)")
    ap.add_argument("--theme", default="auto", choices=["auto", "light", "dark"],
                    help="colours of --app and --webview (auto: as the operating system)")
    a = ap.parse_args()
    if a.app:
        run_app(a.lang, a.theme)
        return
    if a.webview:
        run_webview(a.lang, a.theme)
        return
    if a.web:
        export_web(a.web)
        return
    _LANG = a.lang
    i18n.use_lang(a.lang)
    out = a.out or "colour_wheels_%s.pdf" % a.lang
    c = canvas.Canvas(out, pagesize=A4)
    c.setTitle(T("doc_title"))
    for build in PAGES:
        build(c)
        c.showPage()
    c.save()
    print("Saved", out)


if __name__ == "__main__":
    main()
