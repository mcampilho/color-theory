"""Colour (and contrast) illusions: an illustrated document in PDF and Markdown.

    python3 -m colortheory.illusions                  # -> colour_illusions_en.pdf, .md, illusion_images/
    python3 -m colortheory.illusions --lang pt
    python3 -m colortheory.illusions -o out.pdf --md docs/illusions.md

Every figure is drawn from scratch (illusion_figures.py); the descriptions are short summaries
in our own words, each with a link to the Wikipedia article.
"""
import argparse
import os
import urllib.parse

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from colortheory import i18n
from colortheory import illusion_figures as F
from colortheory.i18n import BOLD, ITAL, REG
from colortheory.illusion_links import LINKS
from colortheory.locales.illusions import STRINGS as _MORE

# (category, key, English Wikipedia article, figure, second figure that proves or extends it)
ILLUSIONS = [
    ("colour", "contrast", "Contrast effect", F.simultaneous_contrast, None),
    ("colour", "bezold", "Bezold effect", F.bezold, None),
    ("colour", "constancy", "Color constancy", F.color_constancy, None),
    ("colour", "afterimage", "Afterimage", F.afterimage, None),
    ("colour", "lilac", "Lilac chaser", F.lilac_chaser, None),
    ("colour", "mccollough", "McCollough effect", F.mccollough, None),
    ("colour", "chromostereopsis", "Chromostereopsis", F.chromostereopsis, None),
    ("brightness", "checker", "Checker shadow illusion", F.checker_shadow, lambda: F.checker_shadow(proof=True)),
    ("brightness", "white", "White's illusion", F.white_illusion, F.munker),
    ("brightness", "mach", "Mach bands", F.mach_bands, None),
    ("brightness", "cornsweet", "Cornsweet illusion", F.cornsweet, None),
    ("brightness", "grid", "Grid illusion", F.hermann_grid, F.scintillating_grid),
    ("brightness", "ehrenstein", "Ehrenstein illusion", F.ehrenstein, None),
    ("brightness", "irradiation", "Irradiation illusion", F.irradiation, None),
    ("size", "ebbinghaus", "Ebbinghaus illusion", F.ebbinghaus, None),
    ("size", "muller_lyer", "Müller-Lyer illusion", F.muller_lyer, None),
    ("size", "ponzo", "Ponzo illusion", F.ponzo, None),
    ("lines", "cafe", "Café wall illusion", F.cafe_wall, None),
    ("lines", "fraser", "Fraser spiral illusion", F.fraser_spiral, None),
    ("lines", "hering", "Hering illusion", F.hering, None),
    ("lines", "wundt", "Wundt illusion", F.wundt, None),
    ("lines", "orbison", "Orbison illusion", F.orbison, None),
    ("lines", "zollner", "Zöllner illusion", F.zollner, None),
    ("lines", "poggendorff", "Poggendorff illusion", F.poggendorff, lambda: F.poggendorff(proof=True)),
    ("lines", "tilt", "Visual tilt effects", F.tilt, None),
    ("motion", "motion", "Illusory motion", F.illusory_motion, None),
    ("motion", "drift", "Peripheral drift illusion", F.peripheral_drift, None),
    ("form", "rubin", "Rubin vase", F.rubin_vase, None),
    ("form", "penrose", "Penrose triangle", F.penrose_triangle, None),
]
CATEGORIES = ["colour", "brightness", "size", "lines", "motion", "form"]

# --------------------------------------------------------------------------
# TEXTS: "illusions" is key -> (name, what you see, why it happens, try this)
# --------------------------------------------------------------------------
STRINGS = {
    "en": {
        "title": "Colour Illusions",
        "subtitle": "What the eye sees is not what is on the page",
        "intro": "Colour, brightness, size and shape are not read off the image point by point: the visual "
                 "system compares each area with its surroundings and guesses what is out there. These "
                 "illusions show that guessing at work. Not all of them are about hue; several need only "
                 "the contrast between black and white.",
        "tips": "Look at the figures on a screen or on a good colour print, at a comfortable distance. The "
                "strength of each illusion varies from person to person. A few use movement or flicker: "
                "stop if they bother you.",
        "contents": "Contents",
        "see": "What you see",
        "why": "Why it happens",
        "try": "Try this",
        "wiki": "Wikipedia article",
        "in_english": "in English",
        "credits": "All figures were drawn for this document. The texts are short summaries based on the "
                   "linked Wikipedia articles (available under the CC BY-SA licence).",
        "animated": "The figure is animated in the Markdown version.",
        "page": "Page",
        "cat_colour": "Colour",
        "cat_brightness": "Brightness and contrast",
        "cat_size": "Size and length",
        "cat_lines": "Bent and tilted lines",
        "cat_motion": "Motion in still pictures",
        "cat_form": "Figure, ground and impossible objects",
        "illusions": {
            "contrast": (
                "Simultaneous contrast",
                "The four small squares are the same grey. On the dark ground it looks lighter than on the "
                "light one; on blue it leans toward yellow, and on yellow toward blue.",
                "Colour is judged by difference. A surround pushes the area inside it away from itself, in "
                "lightness and in hue.",
                "Cut two holes in a sheet of paper so that only two of the small squares show: the "
                "difference disappears."),
            "bezold": (
                "Bezold effect",
                "The red behind the black stripes looks deeper and darker than the red behind the white "
                "stripes, which looks paler and pinker. It is one and the same red.",
                "When small areas of colour alternate, the eye partly blends them (assimilation): the red "
                "takes on some of its neighbour. Wilhelm von Bezold noticed it while redesigning rugs by "
                "changing a single colour.",
                "Step back from the page: the further away you are, the stronger the blend."),
            "constancy": (
                "Colour constancy",
                "Two copies of a mosaic are lit by a warm and by a cool light (the discs above). The second "
                "tile of the second row looks bluish on the left and yellowish on the right, yet it is the "
                "same neutral grey.",
                "To keep objects recognisable, the brain estimates the colour of the light and discounts "
                "it. A grey seen in a scene that is all orange is read as a bluish surface.",
                "Cover everything except the two grey tiles."),
            "afterimage": (
                "Negative afterimage",
                "After staring at the dot in the coloured rings, the plain dot on the right seems to be "
                "surrounded by rings of other colours: red, green and yellow.",
                "The cells that respond to a colour tire (adapt). On a white surface the other cells "
                "answer more strongly and you see the complementary colour.",
                "Stare at the left dot for 30 seconds without moving your eyes, then look at the right "
                "dot and blink."),
            "lilac": (
                "Lilac chaser",
                "Staring at the cross, a gap runs round the ring of lilac discs; then the gap turns into a "
                "green disc, and after a while the lilac discs may fade away altogether.",
                "The moving gap is apparent motion (the phi phenomenon). Where a disc vanishes, an "
                "afterimage of the opposite colour, green, appears. The blurred discs that stay still in "
                "the periphery fade from awareness (Troxler's effect).",
                "Fix your eyes on the cross for at least 30 seconds. Jeremy Hinton created this "
                "animation before 2005."),
            "mccollough": (
                "McCollough effect",
                "After looking in turn at red horizontal and green vertical stripes, the black and white "
                "patches below look tinted: greenish where the stripes are horizontal and pink where they "
                "are vertical.",
                "The visual system adapts to a colour tied to an orientation. Celeste McCollough described "
                "it in 1965; it can last for hours and even months.",
                "Alternate between the two coloured gratings, a few seconds each, for several minutes, "
                "then look at the small patches. Note that the effect can persist for a long time."),
            "chromostereopsis": (
                "Chromostereopsis",
                "Red and blue on black do not seem to lie in the same plane: for most people the red floats "
                "in front of the blue, for some it sinks behind.",
                "The lens bends short and long wavelengths by different amounts (chromatic aberration), so "
                "the two colours land in slightly different places in each eye, and the brain reads the "
                "offset as depth.",
                "View it in a dim room, with both eyes; try with and without glasses."),
            "checker": (
                "Checker shadow illusion",
                "Square A looks much darker than square B. They are exactly the same grey, as the bar in "
                "the second figure shows.",
                "The brain reads a chequered floor with a shadow on it and corrects for the shadow: B must "
                "be a light square, so it is seen as light. Edward Adelson published the illusion in 1995.",
                "Hide the rest of the board with two pieces of paper, leaving only A and B."),
            "white": (
                "White's illusion and Munker",
                "The grey bars set into the black stripes look lighter than those set into the white "
                "stripes. In the coloured version (Munker), the same red looks orange on one side and "
                "purplish on the other.",
                "Surprisingly, each bar looks more like the stripe it replaces lies next to, against what "
                "simple contrast would predict: the eye seems to group each bar with the stripe it belongs "
                "to.",
                "Compare the two groups through a small hole cut in paper."),
            "mach": (
                "Mach bands",
                "Each flat grey strip looks darker near its lighter neighbour and lighter near its darker "
                "one, as if the strips were fluted.",
                "Neighbouring cells in the retina inhibit one another (lateral inhibition), which "
                "exaggerates edges. Ernst Mach described the effect in 1865.",
                "Cover all strips but one: it is perfectly even."),
            "cornsweet": (
                "Cornsweet illusion",
                "The left half looks lighter than the right half. Away from the middle, both are the same "
                "grey.",
                "Only the edge differs, rising on one side and falling on the other. The visual system "
                "takes the step at the edge as the difference between the whole areas.",
                "Lay a pencil along the middle line and watch the two halves become equal."),
            "grid": (
                "Grid illusions: Hermann and scintillating",
                "In the white grid, grey smudges appear at the crossings, except where you look. With discs "
                "on a grey grid, black dots seem to flash on and off.",
                "Hermann's grid (1870) was long explained by lateral inhibition alone; later experiments "
                "(bending the lines removes it) show that it also depends on how the cortex handles "
                "straight lines. The scintillating version was reported in the 1990s.",
                "Let your eyes wander over the grid, then fix a single crossing."),
            "ehrenstein": (
                "Ehrenstein illusion",
                "Where the lines stop short of each other, bright discs seem to appear, whiter than the "
                "paper.",
                "The line ends suggest a shape lying on top and hiding the crossings. The brain draws its "
                "outline (an illusory contour) and fills it with brightness.",
                "Close the gaps in your mind, or with a pencil: the discs vanish."),
            "irradiation": (
                "Irradiation illusion",
                "The white square on black looks larger than the black square on white, although they are "
                "the same size.",
                "Light scatters inside the eye and a bright area spreads on the retina. Galileo mentioned "
                "it in 1632; Helmholtz gave it its name.",
                "Measure the two squares."),
            "ebbinghaus": (
                "Ebbinghaus illusion (Titchener circles)",
                "The orange circle surrounded by large circles looks smaller than the one surrounded by "
                "small circles.",
                "Size is judged relative to the context; the distance and spacing of the surrounding "
                "circles also matter.",
                "Cover the blue circles with your fingers."),
            "muller_lyer": (
                "Müller-Lyer illusion",
                "The line with outward fins looks longer than the one with inward fins. Both are equal, "
                "like the red line below.",
                "The fins shift where the ends of the line seem to be; one account links them to the "
                "corners of rooms and buildings seen in depth. Franz Müller-Lyer described it in 1889.",
                "Compare both shafts with the dashed guides."),
            "ponzo": (
                "Ponzo illusion",
                "The upper yellow bar looks longer than the lower one.",
                "Converging lines suggest distance, like railway tracks: a bar of the same size on the "
                "page, but farther away, would have to be larger.",
                "Measure the two bars, or turn the page upside down."),
            "cafe": (
                "Café wall illusion",
                "The grey mortar lines seem to slope alternately, although they are parallel and level.",
                "The offset black and white tiles, with a mortar of intermediate grey, create small tilted "
                "elements along each line. Richard Gregory named it in 1973 after a café wall in Bristol.",
                "Look along a mortar line with the page almost edge-on."),
            "fraser": (
                "Fraser spiral illusion",
                "A spiral seems to wind into the centre. There is no spiral: the black and white strands "
                "form concentric circles.",
                "Each short strand is tilted, and the twisted background adds to the tilt, so the eye joins "
                "them into a spiral. James Fraser described it in 1908.",
                "Put a finger on one strand and follow it: you come back to where you started."),
            "hering": (
                "Hering illusion",
                "The two red lines seem to bow apart near the middle. They are straight and parallel.",
                "The angles with the radiating lines are overestimated, and the pattern also suggests "
                "motion into depth. Ewald Hering discovered it in 1861.",
                "Hold a ruler along a red line."),
            "wundt": (
                "Wundt illusion",
                "The two red lines seem to bow inward, toward each other, in the middle. They are straight "
                "and parallel.",
                "It is the counterpart of Hering's figure: the radiating lines now spread from points on "
                "either side, so the angles bias the red lines the other way. Wilhelm Wundt described it in "
                "1898.",
                "Compare it with the Hering illusion."),
            "orbison": (
                "Orbison illusion",
                "The red square looks distorted, its sides bent and its corners pulled.",
                "As in Hering's figure, the crossings with the background rings bias the perceived "
                "direction of each side. William Orbison described it in 1939.",
                "Check the sides with a ruler."),
            "zollner": (
                "Zöllner illusion",
                "The long diagonal lines seem to converge and diverge. They are parallel.",
                "The short strokes cross them at an angle and the visual system exaggerates acute angles, "
                "turning each line a little. Johann Zöllner reported it in 1860.",
                "Look along the long lines from one corner of the page."),
            "poggendorff": (
                "Poggendorff illusion",
                "The black line entering the grey block on the left seems to come out as the blue line. It "
                "comes out as the upper black one, as the second figure shows.",
                "Acute angles between the line and the block are seen as wider than they are, shifting the "
                "apparent path. It was noticed in Zöllner's own drawings.",
                "Extend the left line with a ruler."),
            "tilt": (
                "Tilt illusion and tilt aftereffect",
                "The stripes in the two inner discs are both vertical, but seem to lean away from the "
                "stripes around them.",
                "Cells tuned to nearby orientations inhibit one another, repelling the perceived angle. "
                "Looking long at tilted stripes has a similar effect on what you see next.",
                "Cover the outer rings and compare the inner discs."),
            "motion": (
                "Illusory motion",
                "The rings seem to turn slowly, especially those you are not looking at directly.",
                "Blocks of different contrast are processed with slightly different delays, and each small "
                "eye movement restarts the sequence; motion detectors read it as movement.",
                "Move your gaze from one wheel to another, or blink."),
            "drift": (
                "Peripheral drift illusion",
                "The rings made of grey ramps appear to rotate when seen out of the corner of the eye.",
                "A repeating ramp from dark to light (a sawtooth) stimulates motion detectors in the "
                "periphery; the motion is seen from dark to light.",
                "Look to the side of the figure and blink quickly."),
            "rubin": (
                "Rubin vase",
                "A pale vase, or two dark faces looking at each other: one or the other, hardly both at "
                "once.",
                "The shared outline can belong to only one side at a time: what is taken as the figure gets "
                "the shape and the rest becomes background. Edgar Rubin studied it around 1915.",
                "Try to switch at will, and count how often it flips by itself."),
            "penrose": (
                "Penrose triangle",
                "A solid triangle of three square beams, each joined to the next at a right angle.",
                "Every corner is consistent on its own, but the three cannot be true together: no such "
                "object exists. Oscar Reutersvärd drew it in 1934; Lionel and Roger Penrose made it "
                "popular, and it inspired M. C. Escher's Waterfall.",
                "Cover one corner at a time: the rest becomes possible."),
        },
    },
    "pt": {
        "title": "Ilusões de Cor",
        "subtitle": "O que o olho vê não é o que está na página",
        "intro": "A cor, a luminosidade, o tamanho e a forma não são lidos ponto a ponto na imagem: o sistema "
                 "visual compara cada zona com o que a rodeia e faz uma estimativa do que lá está. Estas "
                 "ilusões mostram essa estimativa em ação. Nem todas dizem respeito ao matiz; várias só "
                 "precisam do contraste entre preto e branco.",
        "tips": "Veja as figuras num ecrã ou numa boa impressão a cores, a uma distância confortável. A "
                "intensidade de cada ilusão varia de pessoa para pessoa. Algumas usam movimento ou "
                "cintilação: pare se incomodarem.",
        "contents": "Índice",
        "see": "O que se vê",
        "why": "Porque acontece",
        "try": "Experimente",
        "wiki": "Artigo na Wikipédia",
        "in_english": "em inglês",
        "credits": "Todas as figuras foram desenhadas para este documento. Os textos são resumos curtos "
                   "baseados nos artigos da Wikipédia indicados (disponíveis sob a licença CC BY-SA).",
        "animated": "A figura está animada na versão Markdown.",
        "page": "Página",
        "cat_colour": "Cor",
        "cat_brightness": "Luminosidade e contraste",
        "cat_size": "Tamanho e comprimento",
        "cat_lines": "Linhas curvadas e inclinadas",
        "cat_motion": "Movimento em imagens paradas",
        "cat_form": "Figura, fundo e objetos impossíveis",
        "illusions": {
            "contrast": (
                "Contraste simultâneo",
                "Os quatro quadrados pequenos são do mesmo cinzento. No fundo escuro parece mais claro do "
                "que no claro; sobre azul puxa para o amarelo e sobre amarelo puxa para o azul.",
                "A cor é avaliada por diferença. O fundo afasta de si a zona que envolve, na luminosidade "
                "e no matiz.",
                "Faça dois furos numa folha de modo a ver só dois dos quadrados pequenos: a diferença "
                "desaparece."),
            "bezold": (
                "Efeito Bezold",
                "O vermelho entre riscas pretas parece mais profundo e escuro do que o vermelho entre riscas "
                "brancas, que parece mais pálido e rosado. É um único vermelho.",
                "Quando pequenas áreas de cor se alternam, o olho mistura-as em parte (assimilação): o "
                "vermelho fica com um pouco do vizinho. Wilhelm von Bezold reparou nisto ao redesenhar "
                "tapetes mudando uma só cor.",
                "Afaste-se da página: quanto mais longe, mais forte a mistura."),
            "constancy": (
                "Constância da cor",
                "Duas cópias de um mosaico são iluminadas por uma luz quente e por uma luz fria (os discos "
                "de cima). A segunda peça da segunda linha parece azulada à esquerda e amarelada à direita, "
                "mas é o mesmo cinzento neutro.",
                "Para reconhecer os objetos, o cérebro estima a cor da luz e desconta-a. Um cinzento numa "
                "cena toda alaranjada é lido como uma superfície azulada.",
                "Tape tudo menos as duas peças cinzentas."),
            "afterimage": (
                "Pós-imagem negativa",
                "Depois de fixar o ponto nos anéis coloridos, o ponto simples à direita parece rodeado de "
                "anéis de outras cores: vermelho, verde e amarelo.",
                "As células que respondem a uma cor cansam-se (adaptam-se). Sobre branco, as outras "
                "respondem com mais força e vê-se a cor complementar.",
                "Fixe o ponto da esquerda durante 30 segundos sem mover os olhos, depois olhe para o ponto "
                "da direita e pestaneje."),
            "lilac": (
                "Perseguidor lilás",
                "Com os olhos na cruz, uma falha corre à volta do anel de discos lilás; depois a falha "
                "transforma-se num disco verde e, passado algum tempo, os discos lilás podem desaparecer.",
                "A falha que anda é movimento aparente (fenómeno phi). Onde um disco desaparece surge uma "
                "pós-imagem da cor oposta, verde. Os discos desfocados e parados na periferia somem-se da "
                "perceção (efeito de Troxler).",
                "Fixe a cruz pelo menos 30 segundos. Jeremy Hinton criou esta animação antes de 2005."),
            "mccollough": (
                "Efeito McCollough",
                "Depois de olhar à vez para riscas horizontais vermelhas e verticais verdes, as manchas a "
                "preto e branco em baixo parecem tingidas: esverdeadas onde as riscas são horizontais e "
                "rosadas onde são verticais.",
                "O sistema visual adapta-se a uma cor ligada a uma orientação. Celeste McCollough "
                "descreveu-o em 1965; pode durar horas e até meses.",
                "Alterne entre as duas grelhas coloridas, alguns segundos em cada, durante vários minutos, "
                "e depois olhe para as manchas pequenas. Atenção: o efeito pode persistir muito tempo."),
            "chromostereopsis": (
                "Cromostereopsia",
                "Vermelho e azul sobre preto não parecem estar no mesmo plano: para a maioria o vermelho "
                "flutua à frente do azul, para algumas pessoas fica atrás.",
                "O cristalino desvia de forma diferente os comprimentos de onda curtos e longos (aberração "
                "cromática), as duas cores caem em sítios ligeiramente diferentes em cada olho e o cérebro "
                "lê o desvio como profundidade.",
                "Veja numa sala pouco iluminada, com os dois olhos; experimente com e sem óculos."),
            "checker": (
                "Ilusão da sombra no xadrez",
                "O quadrado A parece muito mais escuro do que o B. São exatamente do mesmo cinzento, como "
                "mostra a barra da segunda figura.",
                "O cérebro vê um chão aos quadrados com uma sombra e corrige a sombra: o B tem de ser um "
                "quadrado claro, por isso é visto como claro. Edward Adelson publicou a ilusão em 1995.",
                "Tape o resto do tabuleiro com dois papéis, deixando só o A e o B."),
            "white": (
                "Ilusão de White e de Munker",
                "As barras cinzentas metidas nas riscas pretas parecem mais claras do que as metidas nas "
                "riscas brancas. Na versão a cores (Munker), o mesmo vermelho parece alaranjado de um lado "
                "e arroxeado do outro.",
                "Surpreendentemente, o resultado contraria o que o contraste simples preveria: o olho parece "
                "agrupar cada barra com a risca a que pertence.",
                "Compare os dois grupos através de um pequeno furo num papel."),
            "mach": (
                "Bandas de Mach",
                "Cada faixa cinzenta lisa parece mais escura junto à vizinha mais clara e mais clara junto à "
                "mais escura, como se as faixas fossem caneladas.",
                "Células vizinhas da retina inibem-se umas às outras (inibição lateral), o que exagera as "
                "arestas. Ernst Mach descreveu o efeito em 1865.",
                "Tape todas as faixas menos uma: é perfeitamente uniforme."),
            "cornsweet": (
                "Ilusão de Cornsweet",
                "A metade esquerda parece mais clara do que a direita. Longe do meio, são do mesmo "
                "cinzento.",
                "Só a fronteira difere, a subir de um lado e a descer do outro. O sistema visual toma o "
                "degrau da fronteira como a diferença entre as áreas inteiras.",
                "Ponha um lápis sobre a linha do meio e veja as duas metades igualarem-se."),
            "grid": (
                "Ilusões de grelha: Hermann e cintilante",
                "Na grelha branca aparecem manchas cinzentas nos cruzamentos, exceto onde se olha. Com "
                "discos numa grelha cinzenta, pontos pretos parecem acender e apagar.",
                "A grelha de Hermann (1870) foi durante muito tempo explicada só pela inibição lateral; "
                "experiências posteriores (curvar as linhas elimina-a) mostram que depende também do modo "
                "como o córtex trata linhas retas. A versão cintilante foi descrita nos anos 1990.",
                "Passeie o olhar pela grelha e depois fixe um só cruzamento."),
            "ehrenstein": (
                "Ilusão de Ehrenstein",
                "Onde as linhas param antes de se cruzarem parecem surgir discos luminosos, mais brancos "
                "do que o papel.",
                "As pontas das linhas sugerem uma forma por cima a tapar os cruzamentos. O cérebro desenha o "
                "seu contorno (contorno ilusório) e enche-o de brilho.",
                "Feche as falhas com a imaginação, ou com um lápis: os discos desaparecem."),
            "irradiation": (
                "Ilusão de irradiação",
                "O quadrado branco sobre preto parece maior do que o quadrado preto sobre branco, mas têm o "
                "mesmo tamanho.",
                "A luz espalha-se dentro do olho e uma zona clara alarga-se na retina. Galileu refere-a em "
                "1632; Helmholtz deu-lhe o nome.",
                "Meça os dois quadrados."),
            "ebbinghaus": (
                "Ilusão de Ebbinghaus (círculos de Titchener)",
                "O círculo laranja rodeado de círculos grandes parece menor do que o rodeado de círculos "
                "pequenos.",
                "O tamanho é avaliado em relação ao contexto; a distância e o espaçamento dos círculos à "
                "volta também contam.",
                "Tape os círculos azuis com os dedos."),
            "muller_lyer": (
                "Ilusão de Müller-Lyer",
                "A linha com as aletas para fora parece mais comprida do que a das aletas para dentro. São "
                "iguais, como a linha vermelha em baixo.",
                "As aletas deslocam o sítio onde parecem estar as pontas da linha; uma explicação liga-as "
                "aos cantos de salas e edifícios vistos em profundidade. Franz Müller-Lyer descreveu-a em "
                "1889.",
                "Compare os dois segmentos com as guias tracejadas."),
            "ponzo": (
                "Ilusão de Ponzo",
                "A barra amarela de cima parece mais comprida do que a de baixo.",
                "As linhas convergentes sugerem distância, como carris: uma barra com o mesmo tamanho na "
                "página, mas mais afastada, teria de ser maior.",
                "Meça as duas barras ou vire a página ao contrário."),
            "cafe": (
                "Ilusão da parede do café",
                "As linhas cinzentas de argamassa parecem inclinar-se alternadamente, mas são paralelas e "
                "horizontais.",
                "Os ladrilhos pretos e brancos desencontrados, com argamassa de um cinzento intermédio, "
                "criam pequenos elementos inclinados ao longo de cada linha. Richard Gregory deu-lhe o nome "
                "em 1973, a partir da parede de um café em Bristol.",
                "Olhe ao longo de uma linha de argamassa com a página quase de perfil."),
            "fraser": (
                "Espiral de Fraser",
                "Parece haver uma espiral a enrolar-se para o centro. Não há espiral: os cordões pretos e "
                "brancos formam círculos concêntricos.",
                "Cada pequeno troço está inclinado e o fundo torcido reforça a inclinação, pelo que o olho "
                "os une numa espiral. James Fraser descreveu-a em 1908.",
                "Ponha um dedo num cordão e siga-o: volta ao ponto de partida."),
            "hering": (
                "Ilusão de Hering",
                "As duas linhas vermelhas parecem curvar-se para fora ao meio. São retas e paralelas.",
                "Os ângulos com as linhas radiais são sobrestimados e o padrão sugere também movimento em "
                "profundidade. Ewald Hering descobriu-a em 1861.",
                "Encoste uma régua a uma linha vermelha."),
            "wundt": (
                "Ilusão de Wundt",
                "As duas linhas vermelhas parecem curvar-se para dentro, uma para a outra, ao meio. São "
                "retas e paralelas.",
                "É o reverso da figura de Hering: as linhas radiais partem agora de pontos de um lado e do "
                "outro, e os ângulos enviesam as linhas vermelhas no sentido contrário. Wilhelm Wundt "
                "descreveu-a em 1898.",
                "Compare-a com a ilusão de Hering."),
            "orbison": (
                "Ilusão de Orbison",
                "O quadrado vermelho parece deformado, com os lados vergados e os cantos puxados.",
                "Como na figura de Hering, os cruzamentos com os anéis do fundo enviesam a direção "
                "percebida de cada lado. William Orbison descreveu-a em 1939.",
                "Verifique os lados com uma régua."),
            "zollner": (
                "Ilusão de Zöllner",
                "As linhas diagonais compridas parecem convergir e divergir. São paralelas.",
                "Os traços curtos cruzam-nas em ângulo e o sistema visual exagera os ângulos agudos, "
                "rodando um pouco cada linha. Johann Zöllner comunicou-a em 1860.",
                "Olhe ao longo das linhas compridas a partir de um canto da página."),
            "poggendorff": (
                "Ilusão de Poggendorff",
                "A linha preta que entra no bloco cinzento pela esquerda parece sair como linha azul. Sai "
                "como a preta de cima, como mostra a segunda figura.",
                "Os ângulos agudos entre a linha e o bloco parecem mais abertos do que são, deslocando o "
                "trajeto aparente. Foi notada nos próprios desenhos de Zöllner.",
                "Prolongue a linha da esquerda com uma régua."),
            "tilt": (
                "Ilusão e pós-efeito de inclinação",
                "As riscas dos dois discos interiores são verticais, mas parecem inclinar-se para o lado "
                "oposto ao das riscas em redor.",
                "Células afinadas para orientações próximas inibem-se, afastando o ângulo percebido. Olhar "
                "muito tempo para riscas inclinadas tem um efeito semelhante no que se vê a seguir.",
                "Tape os anéis exteriores e compare os discos interiores."),
            "motion": (
                "Movimento ilusório",
                "As rodas parecem girar devagar, sobretudo aquelas para onde não se está a olhar.",
                "Blocos com contrastes diferentes são processados com atrasos ligeiramente diferentes e cada "
                "pequeno movimento dos olhos reinicia a sequência; os detetores de movimento leem-na como "
                "deslocação.",
                "Salte o olhar de uma roda para outra, ou pestaneje."),
            "drift": (
                "Deriva periférica",
                "Os anéis feitos de rampas de cinzento parecem rodar quando vistos pelo canto do olho.",
                "Uma rampa repetida do escuro para o claro (dente de serra) estimula os detetores de "
                "movimento na periferia; o movimento é visto do escuro para o claro.",
                "Olhe para o lado da figura e pestaneje depressa."),
            "rubin": (
                "Vaso de Rubin",
                "Um vaso claro, ou duas caras escuras a olhar uma para a outra: um ou outro, dificilmente os "
                "dois ao mesmo tempo.",
                "O contorno comum só pode pertencer a um dos lados de cada vez: o que é tomado como figura "
                "fica com a forma e o resto passa a fundo. Edgar Rubin estudou-o por volta de 1915.",
                "Tente alternar à vontade e conte quantas vezes muda sozinho."),
            "penrose": (
                "Triângulo de Penrose",
                "Um triângulo maciço de três vigas quadradas, cada uma unida à seguinte em ângulo reto.",
                "Cada canto é coerente por si, mas os três não podem ser verdadeiros em conjunto: o objeto "
                "não existe. Oscar Reutersvärd desenhou-o em 1934; Lionel e Roger Penrose popularizaram-no, "
                "e inspirou a Queda de Água de M. C. Escher.",
                "Tape um canto de cada vez: o resto passa a ser possível."),
        },
    },
    "es": {
        "title": "Ilusiones de Color",
        "subtitle": "Lo que ve el ojo no es lo que hay en la página",
        "intro": "El color, la luminosidad, el tamaño y la forma no se leen punto por punto en la imagen: el "
                 "sistema visual compara cada zona con su entorno y estima lo que hay. Estas ilusiones "
                 "muestran esa estimación en marcha. No todas tienen que ver con el tono; varias solo "
                 "necesitan el contraste entre blanco y negro.",
        "tips": "Mire las figuras en una pantalla o en una buena impresión en color, a una distancia cómoda. "
                "La intensidad de cada ilusión varía de una persona a otra. Algunas usan movimiento o "
                "parpadeo: deténgase si le molestan.",
        "contents": "Índice",
        "see": "Lo que se ve",
        "why": "Por qué ocurre",
        "try": "Pruebe",
        "wiki": "Artículo en Wikipedia",
        "in_english": "en inglés",
        "credits": "Todas las figuras se han dibujado para este documento. Los textos son resúmenes breves "
                   "basados en los artículos de Wikipedia indicados (disponibles con licencia CC BY-SA).",
        "animated": "La figura está animada en la versión Markdown.",
        "page": "Página",
        "cat_colour": "Color",
        "cat_brightness": "Luminosidad y contraste",
        "cat_size": "Tamaño y longitud",
        "cat_lines": "Líneas curvadas e inclinadas",
        "cat_motion": "Movimiento en imágenes fijas",
        "cat_form": "Figura, fondo y objetos imposibles",
        "illusions": {
            "contrast": (
                "Contraste simultáneo",
                "Los cuatro cuadrados pequeños son del mismo gris. Sobre el fondo oscuro parece más claro "
                "que sobre el claro; sobre azul tira a amarillo y sobre amarillo tira a azul.",
                "El color se juzga por diferencia. El fondo aleja de sí la zona que rodea, en luminosidad y "
                "en tono.",
                "Haga dos agujeros en un papel para ver solo dos de los cuadrados pequeños: la diferencia "
                "desaparece."),
            "bezold": (
                "Efecto Bezold",
                "El rojo entre rayas negras parece más profundo y oscuro que el rojo entre rayas blancas, "
                "que parece más pálido y rosado. Es un único rojo.",
                "Cuando se alternan pequeñas áreas de color, el ojo las mezcla en parte (asimilación): el "
                "rojo toma algo de su vecino. Wilhelm von Bezold lo observó al rediseñar alfombras "
                "cambiando un solo color.",
                "Aléjese de la página: cuanto más lejos, más fuerte la mezcla."),
            "constancy": (
                "Constancia del color",
                "Dos copias de un mosaico están iluminadas por una luz cálida y otra fría (los discos de "
                "arriba). La segunda pieza de la segunda fila parece azulada a la izquierda y amarillenta a "
                "la derecha, pero es el mismo gris neutro.",
                "Para reconocer los objetos, el cerebro estima el color de la luz y lo descuenta. Un gris en "
                "una escena toda anaranjada se lee como una superficie azulada.",
                "Tape todo menos las dos piezas grises."),
            "afterimage": (
                "Imagen remanente negativa",
                "Tras fijar la vista en el punto de los anillos de colores, el punto solo de la derecha "
                "parece rodeado de anillos de otros colores: rojo, verde y amarillo.",
                "Las células que responden a un color se cansan (se adaptan). Sobre blanco, las demás "
                "responden con más fuerza y se ve el color complementario.",
                "Mire el punto izquierdo 30 segundos sin mover los ojos, luego mire el punto derecho y "
                "parpadee."),
            "lilac": (
                "Perseguidor lila",
                "Con la vista en la cruz, un hueco recorre el anillo de discos lilas; después el hueco se "
                "convierte en un disco verde y, al cabo de un rato, los discos lilas pueden desaparecer.",
                "El hueco que avanza es movimiento aparente (fenómeno phi). Donde desaparece un disco surge "
                "una imagen remanente del color opuesto, verde. Los discos borrosos y quietos en la "
                "periferia se desvanecen (efecto Troxler).",
                "Fije la cruz al menos 30 segundos. Jeremy Hinton creó esta animación antes de 2005."),
            "mccollough": (
                "Efecto McCollough",
                "Tras mirar por turnos rayas horizontales rojas y verticales verdes, las manchas en blanco "
                "y negro de abajo parecen teñidas: verdosas donde las rayas son horizontales y rosadas "
                "donde son verticales.",
                "El sistema visual se adapta a un color ligado a una orientación. Celeste McCollough lo "
                "describió en 1965; puede durar horas e incluso meses.",
                "Alterne entre las dos rejillas de color, unos segundos en cada una, durante varios "
                "minutos, y mire después las manchas pequeñas. Atención: el efecto puede persistir mucho."),
            "chromostereopsis": (
                "Cromoestereopsis",
                "El rojo y el azul sobre negro no parecen estar en el mismo plano: para la mayoría el rojo "
                "flota delante del azul; para algunas personas queda detrás.",
                "El cristalino desvía de forma distinta las longitudes de onda cortas y largas (aberración "
                "cromática), los dos colores caen en sitios algo distintos en cada ojo y el cerebro lee el "
                "desfase como profundidad.",
                "Mírelo en una sala con poca luz, con ambos ojos; pruebe con gafas y sin ellas."),
            "checker": (
                "Ilusión de la sombra en el tablero",
                "El cuadrado A parece mucho más oscuro que el B. Son exactamente del mismo gris, como "
                "muestra la barra de la segunda figura.",
                "El cerebro ve un suelo a cuadros con una sombra y la corrige: B tiene que ser un cuadrado "
                "claro, así que se ve claro. Edward Adelson publicó la ilusión en 1995.",
                "Tape el resto del tablero con dos papeles, dejando solo A y B."),
            "white": (
                "Ilusión de White y de Munker",
                "Las barras grises metidas en las rayas negras parecen más claras que las metidas en las "
                "rayas blancas. En la versión en color (Munker), el mismo rojo parece anaranjado a un lado "
                "y violáceo al otro.",
                "Sorprendentemente, el resultado contradice lo que predeciría el contraste simple: el ojo "
                "parece agrupar cada barra con la raya a la que pertenece.",
                "Compare los dos grupos a través de un agujero pequeño en un papel."),
            "mach": (
                "Bandas de Mach",
                "Cada franja gris lisa parece más oscura junto a su vecina clara y más clara junto a la "
                "oscura, como si las franjas fueran acanaladas.",
                "Las células vecinas de la retina se inhiben entre sí (inhibición lateral), lo que exagera "
                "los bordes. Ernst Mach describió el efecto en 1865.",
                "Tape todas las franjas menos una: es perfectamente uniforme."),
            "cornsweet": (
                "Ilusión de Cornsweet",
                "La mitad izquierda parece más clara que la derecha. Lejos del centro, son del mismo gris.",
                "Solo el borde difiere, subiendo a un lado y bajando al otro. El sistema visual toma el "
                "escalón del borde como la diferencia entre las áreas enteras.",
                "Ponga un lápiz sobre la línea central y verá igualarse las dos mitades."),
            "grid": (
                "Ilusiones de rejilla: Hermann y centelleante",
                "En la rejilla blanca aparecen manchas grises en los cruces, salvo donde se mira. Con discos "
                "sobre una rejilla gris, puntos negros parecen encenderse y apagarse.",
                "La rejilla de Hermann (1870) se explicó mucho tiempo solo por inhibición lateral; "
                "experimentos posteriores (curvar las líneas la elimina) muestran que depende también de "
                "cómo trata la corteza las líneas rectas. La versión centelleante se describió en los 90.",
                "Pasee la mirada por la rejilla y después fije un solo cruce."),
            "ehrenstein": (
                "Ilusión de Ehrenstein",
                "Donde las líneas se detienen antes de cruzarse parecen surgir discos luminosos, más "
                "blancos que el papel.",
                "Los extremos de las líneas sugieren una forma encima que tapa los cruces. El cerebro "
                "dibuja su contorno (contorno ilusorio) y lo llena de brillo.",
                "Cierre los huecos con la imaginación, o con un lápiz: los discos desaparecen."),
            "irradiation": (
                "Ilusión de irradiación",
                "El cuadrado blanco sobre negro parece mayor que el negro sobre blanco, pero miden lo mismo.",
                "La luz se dispersa dentro del ojo y una zona clara se ensancha en la retina. Galileo la "
                "menciona en 1632; Helmholtz le dio nombre.",
                "Mida los dos cuadrados."),
            "ebbinghaus": (
                "Ilusión de Ebbinghaus (círculos de Titchener)",
                "El círculo naranja rodeado de círculos grandes parece menor que el rodeado de círculos "
                "pequeños.",
                "El tamaño se juzga según el contexto; la distancia y la separación de los círculos de "
                "alrededor también influyen.",
                "Tape los círculos azules con los dedos."),
            "muller_lyer": (
                "Ilusión de Müller-Lyer",
                "La línea con las aletas hacia fuera parece más larga que la de las aletas hacia dentro. Son "
                "iguales, como la línea roja de abajo.",
                "Las aletas desplazan el lugar donde parecen estar los extremos; una explicación las "
                "relaciona con las esquinas de salas y edificios vistos en profundidad. Franz Müller-Lyer "
                "la describió en 1889.",
                "Compare los dos segmentos con las guías discontinuas."),
            "ponzo": (
                "Ilusión de Ponzo",
                "La barra amarilla de arriba parece más larga que la de abajo.",
                "Las líneas convergentes sugieren distancia, como unas vías: una barra del mismo tamaño en "
                "la página, pero más lejana, tendría que ser mayor.",
                "Mida las dos barras o ponga la página del revés."),
            "cafe": (
                "Ilusión de la pared del café",
                "Las líneas grises de mortero parecen inclinarse alternadamente, pero son paralelas y "
                "horizontales.",
                "Las baldosas blancas y negras desplazadas, con un mortero de gris intermedio, crean "
                "pequeños elementos inclinados a lo largo de cada línea. Richard Gregory le dio nombre en "
                "1973 por la pared de un café de Bristol.",
                "Mire a lo largo de una línea de mortero con la página casi de canto."),
            "fraser": (
                "Espiral de Fraser",
                "Parece haber una espiral que se enrolla hacia el centro. No la hay: los cordones blancos y "
                "negros forman círculos concéntricos.",
                "Cada tramo corto está inclinado y el fondo retorcido refuerza la inclinación, así que el "
                "ojo los une en una espiral. James Fraser la describió en 1908.",
                "Ponga un dedo en un cordón y sígalo: volverá al punto de partida."),
            "hering": (
                "Ilusión de Hering",
                "Las dos líneas rojas parecen curvarse hacia fuera en el centro. Son rectas y paralelas.",
                "Los ángulos con las líneas radiales se sobrestiman y el patrón sugiere además un movimiento "
                "en profundidad. Ewald Hering la descubrió en 1861.",
                "Apoye una regla en una línea roja."),
            "wundt": (
                "Ilusión de Wundt",
                "Las dos líneas rojas parecen curvarse hacia dentro, una hacia la otra, en el centro. Son "
                "rectas y paralelas.",
                "Es el reverso de la figura de Hering: las líneas radiales parten ahora de puntos a un lado "
                "y a otro, y los ángulos sesgan las líneas rojas en sentido contrario. Wilhelm Wundt la "
                "describió en 1898.",
                "Compárela con la ilusión de Hering."),
            "orbison": (
                "Ilusión de Orbison",
                "El cuadrado rojo parece deformado, con los lados vencidos y las esquinas estiradas.",
                "Como en la figura de Hering, los cruces con los anillos del fondo sesgan la dirección "
                "percibida de cada lado. William Orbison la describió en 1939.",
                "Compruebe los lados con una regla."),
            "zollner": (
                "Ilusión de Zöllner",
                "Las líneas diagonales largas parecen converger y divergir. Son paralelas.",
                "Los trazos cortos las cruzan en ángulo y el sistema visual exagera los ángulos agudos, "
                "girando un poco cada línea. Johann Zöllner la comunicó en 1860.",
                "Mire a lo largo de las líneas largas desde una esquina de la página."),
            "poggendorff": (
                "Ilusión de Poggendorff",
                "La línea negra que entra por la izquierda en el bloque gris parece salir como línea azul. "
                "Sale como la negra de arriba, como muestra la segunda figura.",
                "Los ángulos agudos entre la línea y el bloque parecen más abiertos de lo que son y "
                "desplazan el trayecto aparente. Se advirtió en los propios dibujos de Zöllner.",
                "Prolongue la línea izquierda con una regla."),
            "tilt": (
                "Ilusión y efecto posterior de inclinación",
                "Las rayas de los dos discos interiores son verticales, pero parecen inclinarse en sentido "
                "contrario a las de alrededor.",
                "Las células sintonizadas a orientaciones próximas se inhiben y alejan el ángulo percibido. "
                "Mirar mucho rato rayas inclinadas tiene un efecto parecido sobre lo que se ve después.",
                "Tape los anillos exteriores y compare los discos interiores."),
            "motion": (
                "Movimiento ilusorio",
                "Las ruedas parecen girar despacio, sobre todo las que no se miran directamente.",
                "Los bloques de distinto contraste se procesan con retrasos algo distintos y cada pequeño "
                "movimiento de los ojos reinicia la secuencia; los detectores de movimiento la leen como "
                "desplazamiento.",
                "Salte la mirada de una rueda a otra, o parpadee."),
            "drift": (
                "Deriva periférica",
                "Los anillos de rampas grises parecen girar cuando se ven con el rabillo del ojo.",
                "Una rampa repetida de oscuro a claro (diente de sierra) estimula los detectores de "
                "movimiento de la periferia; el movimiento se ve de lo oscuro a lo claro.",
                "Mire al lado de la figura y parpadee deprisa."),
            "rubin": (
                "Copa de Rubin",
                "Una copa clara, o dos caras oscuras frente a frente: lo uno o lo otro, difícilmente a la "
                "vez.",
                "El contorno común solo puede pertenecer a un lado cada vez: lo que se toma como figura "
                "recibe la forma y el resto pasa a ser fondo. Edgar Rubin la estudió hacia 1915.",
                "Intente alternar a voluntad y cuente cuántas veces cambia sola."),
            "penrose": (
                "Triángulo de Penrose",
                "Un triángulo macizo de tres vigas cuadradas, cada una unida a la siguiente en ángulo recto.",
                "Cada esquina es coherente por sí sola, pero las tres no pueden ser ciertas a la vez: el "
                "objeto no existe. Oscar Reutersvärd lo dibujó en 1934; Lionel y Roger Penrose lo "
                "popularizaron, e inspiró la Cascada de M. C. Escher.",
                "Tape una esquina cada vez: lo demás se vuelve posible."),
        },
    },
}
STRINGS.update(_MORE)
LANGS = [code for code, _ in i18n.LANGS if code in STRINGS]


def T(key):
    """Translated string for the active language (falls back to English)."""
    return STRINGS.get(i18n.current(), STRINGS["en"]).get(key, STRINGS["en"].get(key, key))


def wiki(article, lang):
    """(URL, True if it is in the requested language) of the Wikipedia article."""
    code = lang.split("-")[0]
    title = LINKS.get(article, {}).get(code)
    if code == "en" or not title:
        code, title, own = "en", article, code == "en"
    else:
        own = True
    return "https://%s.wikipedia.org/wiki/%s" % (code, urllib.parse.quote(title.replace(" ", "_"))), own


def _link_label(article, lang):
    url, own = wiki(article, lang)
    return url, T("wiki") + ("" if own else " (%s)" % T("in_english"))


# ==========================================================================
# PDF
# ==========================================================================
PAGE_W, PAGE_H = A4
LEFT, TEXT_W = 56, PAGE_W - 112
INK, SOFT, ACCENT = (0.13, 0.13, 0.15), (0.42, 0.42, 0.46), (0.11, 0.33, 0.68)


def _lines(c, text, x, y, width, font=REG, size=10.5, leading=14.5, colour=INK):
    c.setFillColorRGB(*colour)
    c.setFont(font, size)
    for line in i18n.wrap(text, font, size, width):
        i18n.draw_line(c, x, y, line, width)
        y -= leading
    return y


def _footer(c, number):
    c.setFillColorRGB(*SOFT)
    c.setFont(REG, 8.5)
    page = T("page")
    c.drawCentredString(PAGE_W / 2, 30, page % number if "%d" in page else "%s %d" % (page, number))


def _start(c, text, y, font, size, colour, indent=0):
    """One line at the side where reading starts; returns its (left, right) edges."""
    c.setFillColorRGB(*colour)
    c.setFont(font, size)
    width = stringWidth(i18n.visual(text), font, size)
    if i18n.rtl():
        c.drawRightString(LEFT + TEXT_W - indent, y, text)
        return LEFT + TEXT_W - indent - width, LEFT + TEXT_W - indent
    c.drawString(LEFT + indent, y, text)
    return LEFT + indent, LEFT + indent + width


def _cover(c):
    _start(c, T("title"), PAGE_H - 110, BOLD, 34, INK)
    _lines(c, T("subtitle"), LEFT, PAGE_H - 138, TEXT_W, ITAL, 14, 18, SOFT)
    half = (TEXT_W - 16) / 2
    height = half * F.HEIGHT / F.WIDTH
    for k, fig in enumerate((F.cafe_wall, F.munker, F.fraser_spiral, F.rubin_vase)):
        row, col = divmod(k, 2)
        fig().draw(c, LEFT + col * (half + 16), PAGE_H - 170 - row * (height + 16), half)
    y = PAGE_H - 170 - 2 * height - 54
    y = _lines(c, T("intro"), LEFT, y, TEXT_W)
    y = _lines(c, T("tips"), LEFT, y - 8, TEXT_W)
    _lines(c, T("credits"), LEFT, y - 8, TEXT_W, ITAL, 8.5, 11.5, SOFT)
    c.showPage()


def _contents(c, first_page):
    _start(c, T("contents"), PAGE_H - 80, BOLD, 22, INK)
    texts = T("illusions")
    y, page = PAGE_H - 116, first_page
    for category in CATEGORIES:
        _start(c, T("cat_" + category), y, BOLD, 11.5, ACCENT)
        y -= 18
        for cat, key, *_ in ILLUSIONS:
            if cat != category:
                continue
            _start(c, texts[key][0], y, REG, 10.5, INK, indent=14)
            if i18n.rtl():
                c.drawString(LEFT, y, str(page))
            else:
                c.drawRightString(LEFT + TEXT_W, y, str(page))
            c.linkRect("", key, (LEFT, y - 3, LEFT + TEXT_W, y + 11), relative=0, thickness=0)
            y -= 15.5
            page += 1
        y -= 10
    _footer(c, 2)
    c.showPage()


def _text_height(key, texts):
    """Height of everything written below the figures."""
    height = 14
    for text in texts:
        height += 14 + 14.5 * len(i18n.wrap(text, REG, 10.5, TEXT_W)) + 7
    if key == "lilac":
        height += 13 * len(i18n.wrap(T("animated"), ITAL, 9.5, TEXT_W)) + 7
    return height


def _illusion_page(c, entry, number):
    category, key, article, figure, second = entry
    name, see, why, try_ = T("illusions")[key]
    c.bookmarkPage(key)
    c.addOutlineEntry(name, key, level=0)
    heading = T("cat_" + category)
    if i18n.current() == "tr":
        heading = heading.replace("i", "İ")                         # Turkish dotted capital
    _start(c, heading.upper(), PAGE_H - 52, BOLD, 9.5, ACCENT)
    _start(c, name, PAGE_H - 76, BOLD, 21, INK)
    figures = [fig for fig in (figure, second) if fig is not None]
    width = TEXT_W if second is None else 360
    # long texts: smaller figures, so that the link stays above the page number
    room = PAGE_H - 92 - 52 - _text_height(key, (see, why, try_)) - 12 * len(figures)
    width = min(width, room / len(figures) * F.WIDTH / F.HEIGHT)
    height = width * F.HEIGHT / F.WIDTH
    x = (PAGE_W - width) / 2
    y = PAGE_H - 92
    for fig in figures:
        fig().draw(c, x, y, width)
        c.setStrokeColorRGB(0.82, 0.82, 0.84)
        c.setLineWidth(0.6)
        c.rect(x, y - height, width, height, stroke=1, fill=0)
        y -= height + 12
    y -= 14
    for label, text in (("see", see), ("why", why), ("try", try_)):
        _start(c, T(label), y, BOLD, 10.5, ACCENT)
        y = _lines(c, text, LEFT, y - 14, TEXT_W) - 7
    if key == "lilac":
        y = _lines(c, T("animated"), LEFT, y, TEXT_W, ITAL, 9.5, 13, SOFT) - 7
    url, label = _link_label(article, i18n.current())
    left, right = _start(c, label, y, REG, 10, ACCENT)
    c.linkURL(url, (left, y - 3, right, y + 10), thickness=0)
    _footer(c, number)
    c.showPage()


def write_pdf(path):
    c = canvas.Canvas(path, pagesize=A4, invariant=1)
    c.setTitle(T("title"))
    c.setAuthor("colortheory.illusions")
    _cover(c)
    _contents(c, 3)
    for number, entry in enumerate(ILLUSIONS, 3):
        _illusion_page(c, entry, number)
    c.save()


# ==========================================================================
# MARKDOWN
# ==========================================================================
def write_images(folder):
    """One SVG per figure; they have no words, so every language uses the same files."""
    os.makedirs(folder, exist_ok=True)
    for _, key, _, figure, second in ILLUSIONS:
        for suffix, fig in (("", figure), ("_2", second)):
            if fig is not None:
                with open(os.path.join(folder, key + suffix + ".svg"), "w", encoding="utf-8", newline="\n") as out:
                    out.write(fig().svg())


def markdown(images):
    """The document as Markdown; images is the folder of the SVG files, relative to the .md file."""
    texts = T("illusions")
    lines = ["# " + T("title"), "", "*%s*" % T("subtitle"), "", T("intro"), "", T("tips"), "",
             "> " + T("credits"), "", "## " + T("contents"), ""]
    # Chinese and Japanese take their own full-width colon instead of a full stop
    labelled = "**%s**：%s" if i18n.current() in ("zh", "ja") else "**%s.** %s"
    for category in CATEGORIES:
        lines.append("- **%s**" % T("cat_" + category))
        lines += ["  - [%s](#%s)" % (texts[key][0], key) for cat, key, *_ in ILLUSIONS if cat == category]
    for category in CATEGORIES:
        lines += ["", "## " + T("cat_" + category)]
        for cat, key, article, _, second in ILLUSIONS:
            if cat != category:
                continue
            name, see, why, try_ = texts[key]
            lines += ["", '<a id="%s"></a>' % key, "", "### " + name, "",
                      "![%s](%s/%s.svg)" % (name, images, key)]
            if second is not None:
                lines += ["", "![%s](%s/%s_2.svg)" % (name, images, key)]
            for label, text in (("see", see), ("why", why), ("try", try_)):
                lines += ["", labelled % (T(label), text)]
            url, label = _link_label(article, i18n.current())
            lines += ["", "[%s](%s)" % (label, url)]
    if i18n.rtl():
        lines = ['<div dir="rtl">', ""] + lines + ["", "</div>"]
    return "\n".join(lines) + "\n"


def write_markdown(path, image_folder=None):
    base = os.path.dirname(os.path.abspath(path))
    folder = os.path.abspath(image_folder) if image_folder else os.path.join(base, "illusion_images")
    write_images(folder)
    relative = os.path.relpath(folder, base).replace(os.sep, "/")
    with open(path, "w", encoding="utf-8", newline="\n") as out:
        out.write(markdown(urllib.parse.quote(relative)))


def main():
    ap = argparse.ArgumentParser(description="Colour illusions: an illustrated PDF and Markdown document")
    ap.add_argument("--lang", default="en", choices=LANGS, help="text language")
    ap.add_argument("-o", "--out", default=None, help="output PDF path")
    ap.add_argument("--md", default=None, help="output Markdown path (default: next to the PDF)")
    ap.add_argument("--images", default=None, metavar="DIR",
                    help="folder of the SVG figures (default: illusion_images next to the Markdown file)")
    a = ap.parse_args()
    i18n.use_lang(a.lang)
    out = a.out or "colour_illusions_%s.pdf" % a.lang
    md = a.md or os.path.splitext(out)[0] + ".md"
    write_pdf(out)
    write_markdown(md, a.images)
    print("Saved", out)
    print("Saved", md)


if __name__ == "__main__":
    main()
