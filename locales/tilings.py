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

# ---------------------------------------------------------------------- PT-BR
STRINGS["pt-BR"].update({
    "title": "PAVIMENTAÇÕES E MOSAICOS",
    "subtitle": "Pavimentações regulares, semirregulares, aperiódicas e islâmicas, coloridas com teoria da cor",
    "intro": "Uma pavimentação cobre o plano com formas, sem buracos nem sobreposições. A mesma "
             "pavimentação muda de caráter com a coloração: pelo tipo de peça, pela orientação, pela "
             "imagem espelhada, ou de modo que peças vizinhas sejam sempre diferentes. Cada página "
             "desenha as pavimentações de um artigo da Wikipédia com várias colorações; as cores vêm "
             "dos esquemas da roda RYB ou de paletas tradicionais de azulejos. Tudo é calculado: "
             "redes de polígonos, duais, a deflação de Penrose, as metapeças do chapéu, uma busca "
             "de pavimentações de Wang e o método de Hankin para os padrões de estrelas.",
    "schemes_t": "Esquemas de cores",
    "schemes_d": "Os esquemas RYB pegam matizes a passos fixos da roda de 12 matizes a partir de um "
                 "matiz base (aqui o vermelho); quando uma pavimentação precisa de mais cores do que "
                 "o esquema tem, são acrescentados tons claros e escuros dos mesmos matizes. As paletas "
                 "com nome copiam azulejos tradicionais.",
    "contents": "Sumário", "colouring": "Coloração", "cont": "continuação", "page": "página",
    "c_single": "uma cor", "c_kind": "por tipo de peça", "c_shape": "por forma",
    "c_chirality": "por imagem espelhada", "c_orientation": "por orientação",
    "c_proper": "vizinhas diferentes", "c_random": "aleatória", "c_rings": "anéis a partir do centro",
    "c_classic": "as quatro cores das bordas", "c_scheme": "cores das bordas de um esquema",
    "c_checker": "xadrez", "c_gradient": "degradê na diagonal",
    "f_triangular": "Pavimentação triangular",
    "f_triangular_d": "Seis triângulos equiláteros se encontram em cada vértice. As colorações uniformes "
                      "levam o nome das cores em volta de um vértice: 121212 alterna duas cores, 121314 "
                      "precisa de quatro. Cortando mais os triângulos obtêm-se as pavimentações "
                      "kisrhombille e kisdeltile.",
    "f_truncated_square": "Pavimentação quadrada truncada",
    "f_truncated_square_d": "Um quadrado e dois octógonos regulares em cada vértice (4.8.8), o piso de "
                            "muitas cozinhas. Os quadrados podem ter dois tamanhos e, no limite, metade "
                            "deles desaparece (pavimentação chanfrada). A dual é a pavimentação "
                            "tetrakis quadrada.",
    "f_hexagonal": "Pavimentação hexagonal",
    "f_hexagonal_d": "Três hexágonos em cada vértice, como num favo de mel. Os hexágonos podem ser "
                     "coloridos com 2, 3, 4 ou 7 cores de forma regular; com 7, cada hexágono toca todas "
                     "as outras cores. Cortando alguns hexágonos em triângulos obtêm-se pavimentações "
                     "2-uniformes.",
    "f_trihexagonal": "Pavimentação tri-hexagonal",
    "f_trihexagonal_d": "Triângulos e hexágonos alternam em volta de cada vértice (3.6.3.6); as arestas "
                        "formam três famílias de retas, o padrão kagome dos cestos japoneses. Girar ou "
                        "redimensionar os triângulos mantém a mesma estrutura.",
    "f_rhombille": "Pavimentação de losangos",
    "f_rhombille_d": "Losangos iguais de 60°, três em volta de um canto e seis em volta do outro: a "
                     "dual da tri-hexagonal. Com três valores de um matiz parece uma pilha de cubos, "
                     "padrão de pisos antigos como o da Catedral de Siena.",
    "f_pythagorean": "Pavimentação pitagórica",
    "f_pythagorean_d": "Quadrados de dois tamanhos, cada um tocando quatro quadrados do outro tamanho. É "
                       "a figura de uma demonstração clássica do teorema de Pitágoras e um padrão comum "
                       "de piso (cata-vento ou amarelinha).",
    "f_regular": "Polígonos regulares",
    "f_regular_d": "As onze pavimentações uniformes (arquimedianas) por polígonos regulares: todos os "
                   "vértices têm os mesmos polígonos em volta, escritos pelos números de lados (3.4.6.4 "
                   "é triângulo, quadrado, hexágono, quadrado). Misturar tipos de vértice dá "
                   "pavimentações k-uniformes.",
    "f_penrose": "Pavimentações de Penrose",
    "f_penrose_d": "Duas peças que cobrem o plano só sem se repetir: losangos largos e estreitos (P3), "
                   "ou pipas e dardos (P2). São desenhadas cortando repetidamente triângulos de ouro "
                   "(deflação) e mostram simetria de ordem cinco em toda parte.",
    "f_aperiodic": "Pavimentações aperiódicas",
    "f_aperiodic_d": "Pavimentações que nunca se repetem. O chapéu (2023) é uma única forma, usada com "
                     "sua imagem espelhada, que só pavimenta de forma aperiódica; as seis peças "
                     "quadradas de Robinson forçam quadrados encaixados cada vez maiores.",
    "f_herringbone": "Espinha de peixe",
    "f_herringbone_d": "Retângulos dispostos em escada, cada um em ângulo reto com os vizinhos: o padrão "
                       "clássico de tijolos e tacos. Tijolos mais longos, um giro de 45° ou "
                       "paralelogramos mudam o aspecto; o trançado de cesto agrupa os tijolos em pares.",
    "f_pentagonal": "Pavimentações pentagonais",
    "f_pentagonal_d": "Pentágonos regulares não pavimentam o plano, mas 15 famílias de pentágonos "
                      "convexos sim. Dividir hexágonos ao meio dá o tipo 1; as duais de três "
                      "pavimentações uniformes dão as pentagonais do Cairo, prismática e floral.",
    "f_cairo": "Pavimentação pentagonal do Cairo",
    "f_cairo_d": "Pentágonos com quatro lados longos e um curto, a dual da pavimentação quadrada "
                 "achatada, com o nome das ruas do Cairo. Quatro pentágonos se encontram em alguns "
                 "vértices, três em outros, e pares de pentágonos formam hexágonos.",
    "f_girih": "Peças girih",
    "f_girih_d": "Cinco peças de lados iguais (decágono, pentágono, hexágono, gravata-borboleta, losango) "
                 "usadas na arquitetura persa. As linhas desenhadas nelas cruzam cada aresta no ponto "
                 "médio a 54°, e assim se unem de peça para peça no padrão de estrelas visível.",
    "f_wang": "Peças de Wang",
    "f_wang_d": "Quadrados com bordas coloridas, colocados de modo que bordas em contato tenham a mesma "
                "cor, sem nunca girar. As 11 peças de Jeandel e Rao (2015) só pavimentam o plano de "
                "forma aperiódica; este trecho foi encontrado por uma busca com retrocesso.",
    "f_zellij": "Zellige",
    "f_zellij_d": "Mosaico marroquino e andaluz de peças vidradas cortadas à mão, em branco, verde, "
                  "preto, ocre e azuis. São típicas as estrelas de oito pontas com cruzes e os sistemas "
                  "de estrelas de 6, 8, 10 e 12 pontas.",
    "f_islamic": "Padrões geométricos islâmicos",
    "f_islamic_d": "Padrões de estrelas feitos com o método de Hankin dos polígonos em contato: do meio "
                   "de cada aresta de uma pavimentação saem duas linhas num ângulo fixo até se "
                   "encontrarem. A pavimentação de base e o ângulo decidem as estrelas; as tiras são "
                   "desenhadas como fitas.",
    "v_uniform": "Coloração uniforme %s",
    "v_tri_regular": "Pavimentação triangular regular {3,6}",
    "v_kisrhombille": "Kisrhombille: triângulos 30-60-90 (dual de 4.6.12)",
    "v_triakis": "Kisdeltile: triângulos 30-30-120 (dual de 3.12.12)",
    "v_ts_plain": "Pavimentação quadrada truncada 4.8.8",
    "v_circlepack": "Empacotamento de círculos: um círculo em cada vértice",
    "v_ts_alt": "Quadrados de tamanhos alternados",
    "v_ts_chamfer": "Pavimentação quadrada chanfrada (os quadrados pequenos desaparecem)",
    "v_tetrakis": "Pavimentação tetrakis quadrada (dual de 4.8.8)",
    "v_dual_overlay": "Com a dual desenhada por cima",
    "v_hex_regular": "Pavimentação hexagonal regular {6,3}",
    "v_hex_2": "Duas cores, em fileiras",
    "v_hex_21": "Duas cores, um hexágono em cada três",
    "v_hex_3": "Três cores: vizinhos sempre diferentes",
    "v_hex_4": "Quatro cores",
    "v_hex_7": "Sete cores: cada hexágono toca todos os outros",
    "v_kissing": "Empacotamento mais denso de círculos",
    "v_dissect1": "2-uniforme: um terço dos hexágonos cortados em triângulos",
    "v_dissect2": "2-uniforme: dois terços dos hexágonos cortados em triângulos",
    "v_kagome": "Kagome: arestas coloridas pela direção",
    "v_unequal": "Triângulos de dois tamanhos",
    "v_twisted": "Triângulos girados: os hexágonos viram estrelas",
    "v_twisted2": "Girados ainda mais",
    "v_hexstar": "Hexágonos e estrelas de seis pontas",
    "v_rhombille": "Pavimentação de losangos de 60°",
    "v_siena": "Três tons pela orientação, como na Catedral de Siena",
    "v_cubes": "Cubos empilhados: um matiz em três valores",
    "v_rh_dual": "Sobre a dual, a pavimentação tri-hexagonal",
    "v_skew": "Inclinada e girada: paralelogramos",
    "v_pyth_half": "Quadrados de lados 1 e 1/2",
    "v_pyth_golden": "Lados na razão áurea",
    "v_pyth_random": "Lados 1 e 0,3, tons de terra aleatórios",
    "n_triangular": "3.3.3.3.3.3 triangular",
    "n_square": "4.4.4.4 quadrada",
    "n_hexagonal": "6.6.6 hexagonal",
    "n_trihexagonal": "3.6.3.6 tri-hexagonal",
    "n_truncated_hexagonal": "3.12.12 hexagonal truncada",
    "n_truncated_square": "4.8.8 quadrada truncada",
    "n_truncated_trihexagonal": "4.6.12 tri-hexagonal truncada",
    "n_rhombitrihexagonal": "3.4.6.4 rombitri-hexagonal",
    "n_snub_hexagonal": "3.3.3.3.6 hexagonal achatada",
    "n_elongated_triangular": "3.3.3.4.4 triangular alongada",
    "n_snub_square": "3.3.4.3.4 quadrada achatada",
    "v_p3": "P3: losangos largos e estreitos",
    "v_p3_ori": "P3 pelas dez orientações dos losangos",
    "v_p3_proper": "P3, losangos vizinhos diferentes",
    "v_p3_rings": "P3 em anéis em volta do centro",
    "v_p2": "P2: pipas e dardos",
    "v_p2_rings": "P2 em anéis em volta do centro",
    "v_p2_proper": "P2, peças vizinhas diferentes",
    "v_hat": "O chapéu: uma forma e sua imagem espelhada",
    "v_hat_ori": "Chapéus pela orientação",
    "v_robinson": "Peças de Robinson: as marcas desenham quadrados encaixados",
    "v_hb_2": "Tijolos 2:1",
    "v_hb_45": "Girado 45°",
    "v_hb_3": "Tijolos 3:1",
    "v_hb_long": "Tábuas longas, cerca de 6,6:1",
    "v_hb_par": "Paralelogramos",
    "v_basket": "Trançado de cesto",
    "v_halves": "Tipo 1: hexágonos cortados ao meio",
    "v_halves_alt": "Tipo 1, cortado em três direções",
    "v_cairo_p": "Pavimentação do Cairo (tipos 2 e 4)",
    "v_prismatic": "Pentagonal prismática (dual de 3.3.3.4.4)",
    "v_floret": "Pentagonal floral (dual de 3.3.3.3.6)",
    "v_floret_proper": "Pentagonal floral, vizinhas diferentes",
    "v_cairo": "Pavimentação do Cairo: dual da quadrada achatada",
    "v_cairo_ori": "Quatro orientações",
    "v_cairo_proper": "Pentágonos vizinhos diferentes",
    "v_cairo_dual": "Sobre a dual, a pavimentação quadrada achatada",
    "v_girih_tiles": "Decágonos e gravatas-borboleta",
    "v_girih_lines": "Linhas girih, cruzando cada aresta a 54°",
    "v_girih_star": "O padrão girih, colorido",
    "v_girih_star2": "O mesmo padrão, paleta zellige",
    "v_wang": "Jeandel–Rao: 11 peças, 4 cores, aperiódica",
    "v_wang_scheme": "As mesmas peças, cores de um esquema",
    "v_stars_crosses": "Estrelas de oito pontas e cruzes",
    "v_sc_azulejo": "Estrelas e cruzes em azuis de azulejo",
    "v_z8": "Estrelas de oito pontas a partir de octógonos em contato",
    "v_z12": "Estrelas de doze, seis e quatro pontas",
    "v_z10": "Estrelas de dez pontas (base girih)",
    "v_i6": "Estrelas de seis pontas a partir de hexágonos em contato",
    "v_i_sq": "Octógonos e estrelas de quatro pontas a partir de quadrados",
    "v_i_31212": "Estrelas de doze pontas a partir de 3.12.12",
    "v_i_4612": "Rosetas a partir de 4.6.12",
    "v_i_3464": "Estrelas a partir de 3.4.6.4",
    "v_i_snub": "Estrelas a partir da pavimentação quadrada achatada",
    "app_title": "Pavimentações e mosaicos", "app_tiling": "Pavimentação", "app_scheme": "Esquema",
    "app_hue": "Matiz base", "app_size": "Largura", "app_save": "Salvar…", "app_saved": "Salvo: %s",
    "app_drawing": "Desenhando…", "app_error": "Não é possível desenhar esta combinação: %s",
    "app_panels": "painéis",
    "app_params": "Parâmetros", "app_params_hint": "nome=valor, separados por espaços; Enter aplica",
})

# ---------------------------------------------------------------------- FR
STRINGS["fr"].update({
    "title": "PAVAGES ET MOSAÏQUES",
    "subtitle": "Pavages réguliers, semi-réguliers, apériodiques et islamiques, colorés par la théorie des couleurs",
    "intro": "Un pavage recouvre le plan de formes, sans trous ni chevauchements. Le même pavage change "
             "de caractère selon sa coloration : par type de pièce, par orientation, par image miroir, "
             "ou de sorte que les pièces voisines diffèrent toujours. Chaque page dessine les pavages "
             "d'un article de Wikipédia avec plusieurs colorations ; les couleurs viennent des "
             "harmonies du cercle RYB ou de palettes traditionnelles de carreaux. Tout est calculé : "
             "réseaux de polygones, duaux, déflation de Penrose, métatuiles du chapeau, recherche de "
             "pavages de Wang et méthode de Hankin pour les motifs d'étoiles.",
    "schemes_t": "Harmonies de couleurs",
    "schemes_d": "Les harmonies RYB prennent des teintes à pas fixes sur le cercle de 12 teintes à "
                 "partir d'une teinte de base (ici le rouge) ; quand un pavage demande plus de couleurs, "
                 "on ajoute des versions claires et sombres des mêmes teintes. Les palettes nommées "
                 "reprennent des carreaux émaillés traditionnels.",
    "contents": "Sommaire", "colouring": "Coloration", "cont": "suite", "page": "page",
    "c_single": "une couleur", "c_kind": "par type de pièce", "c_shape": "par forme",
    "c_chirality": "par image miroir", "c_orientation": "par orientation",
    "c_proper": "voisines différentes", "c_random": "aléatoire", "c_rings": "anneaux depuis le centre",
    "c_classic": "les quatre couleurs de bord", "c_scheme": "couleurs de bord d'une harmonie",
    "c_checker": "damier", "c_gradient": "dégradé en diagonale",
    "f_triangular": "Pavage triangulaire",
    "f_triangular_d": "Six triangles équilatéraux se rencontrent à chaque sommet. Ses colorations "
                      "uniformes sont nommées d'après les couleurs autour d'un sommet : 121212 alterne "
                      "deux couleurs, 121314 en demande quatre. En recoupant les triangles on obtient les "
                      "pavages kisrhombille et kisdeltile.",
    "f_truncated_square": "Pavage carré tronqué",
    "f_truncated_square_d": "Un carré et deux octogones réguliers à chaque sommet (4.8.8), le sol de "
                            "nombreuses cuisines. Les carrés peuvent avoir deux tailles, et à la limite "
                            "la moitié disparaît (pavage chanfreiné). Son dual est le pavage tétrakis "
                            "carré.",
    "f_hexagonal": "Pavage hexagonal",
    "f_hexagonal_d": "Trois hexagones à chaque sommet, comme dans une ruche. On peut colorer les "
                     "hexagones régulièrement avec 2, 3, 4 ou 7 couleurs ; avec 7, chaque hexagone touche "
                     "toutes les autres couleurs. Couper certains hexagones en triangles donne des "
                     "pavages 2-uniformes.",
    "f_trihexagonal": "Pavage trihexagonal",
    "f_trihexagonal_d": "Triangles et hexagones alternent autour de chaque sommet (3.6.3.6) ; ses "
                        "arêtes forment trois familles de droites, le motif kagome des paniers japonais. "
                        "Tourner ou redimensionner les triangles garde la même structure.",
    "f_rhombille": "Pavage rhombique",
    "f_rhombille_d": "Losanges identiques de 60°, trois autour d'un coin et six autour de l'autre : le "
                     "dual du pavage trihexagonal. Avec trois valeurs d'une teinte, il se lit comme un "
                     "empilement de cubes, motif de sols anciens comme celui de la cathédrale de Sienne.",
    "f_pythagorean": "Pavage pythagoricien",
    "f_pythagorean_d": "Carrés de deux tailles, chacun touchant quatre carrés de l'autre taille. C'est "
                       "la figure d'une démonstration classique du théorème de Pythagore, et un motif "
                       "de sol courant (moulinet ou marelle).",
    "f_regular": "Polygones réguliers",
    "f_regular_d": "Les onze pavages uniformes (archimédiens) par polygones réguliers : chaque sommet a "
                   "les mêmes polygones autour de lui, notés par leur nombre de côtés (3.4.6.4 : "
                   "triangle, carré, hexagone, carré). Mélanger les types de sommets donne des pavages "
                   "k-uniformes.",
    "f_penrose": "Pavages de Penrose",
    "f_penrose_d": "Deux pièces qui ne recouvrent le plan que sans se répéter : losanges épais et "
                   "minces (P3), ou cerfs-volants et fléchettes (P2). On les dessine en découpant "
                   "plusieurs fois des triangles d'or (déflation) ; ils montrent partout une symétrie "
                   "d'ordre cinq.",
    "f_aperiodic": "Pavages apériodiques",
    "f_aperiodic_d": "Des pavages qui ne se répètent jamais. Le chapeau (2023) est une seule forme, "
                     "employée avec son image miroir, qui ne pave que de façon apériodique ; les six "
                     "carreaux de Robinson imposent des carrés emboîtés toujours plus grands.",
    "f_herringbone": "Point de Hongrie (chevrons)",
    "f_herringbone_d": "Rectangles posés en escalier, chacun à angle droit de ses voisins : le motif "
                       "classique des briques et du parquet. Des briques plus longues, une rotation de "
                       "45° ou des parallélogrammes en changent l'aspect ; le tressage associe les "
                       "briques par paires.",
    "f_pentagonal": "Pavages pentagonaux",
    "f_pentagonal_d": "Les pentagones réguliers ne pavent pas le plan, mais 15 familles de pentagones "
                      "convexes le font. Couper des hexagones en deux donne le type 1 ; les duaux de "
                      "trois pavages uniformes donnent les pavages pentagonaux du Caire, prismatique et "
                      "en fleurettes.",
    "f_cairo": "Pavage pentagonal du Caire",
    "f_cairo_d": "Pentagones à quatre longs côtés et un court, dual du pavage carré adouci, nommé "
                 "d'après les rues du Caire. Quatre pentagones se rencontrent à certains sommets, trois "
                 "à d'autres, et des paires de pentagones forment des hexagones.",
    "f_girih": "Carreaux girih",
    "f_girih_d": "Cinq carreaux à côtés égaux (décagone, pentagone, hexagone, nœud papillon, losange) "
                 "de l'architecture persane. Les lignes tracées dessus coupent chaque arête en son milieu "
                 "à 54°, et se raccordent d'un carreau à l'autre en un motif d'étoiles.",
    "f_wang": "Tuiles de Wang",
    "f_wang_d": "Carrés à bords colorés, posés de sorte que les bords en contact s'accordent, sans "
                "jamais les tourner. Les 11 tuiles de Jeandel et Rao (2015) ne pavent le plan que de "
                "façon apériodique ; ce morceau a été trouvé par une recherche avec retour arrière.",
    "f_zellij": "Zellige",
    "f_zellij_d": "Mosaïque marocaine et andalouse de pièces émaillées taillées à la main, en blanc, "
                  "vert, noir, ocre et bleus. Les étoiles à huit branches avec croix et les systèmes "
                  "d'étoiles à 6, 8, 10 et 12 branches sont typiques.",
    "f_islamic": "Motifs géométriques islamiques",
    "f_islamic_d": "Motifs d'étoiles obtenus par la méthode de Hankin des polygones en contact : du "
                   "milieu de chaque arête d'un pavage partent deux lignes à angle fixe jusqu'à leur "
                   "rencontre. Le pavage de base et l'angle décident des étoiles ; les entrelacs sont "
                   "dessinés comme des rubans.",
    "v_uniform": "Coloration uniforme %s",
    "v_tri_regular": "Pavage triangulaire régulier {3,6}",
    "v_kisrhombille": "Kisrhombille : triangles 30-60-90 (dual de 4.6.12)",
    "v_triakis": "Kisdeltile : triangles 30-30-120 (dual de 3.12.12)",
    "v_ts_plain": "Pavage carré tronqué 4.8.8",
    "v_circlepack": "Empilement de cercles : un cercle à chaque sommet",
    "v_ts_alt": "Carrés de tailles alternées",
    "v_ts_chamfer": "Pavage carré chanfreiné (les petits carrés disparaissent)",
    "v_tetrakis": "Pavage tétrakis carré (dual de 4.8.8)",
    "v_dual_overlay": "Avec son dual dessiné par-dessus",
    "v_hex_regular": "Pavage hexagonal régulier {6,3}",
    "v_hex_2": "Deux couleurs, en rangées",
    "v_hex_21": "Deux couleurs, un hexagone sur trois",
    "v_hex_3": "Trois couleurs : les voisins diffèrent toujours",
    "v_hex_4": "Quatre couleurs",
    "v_hex_7": "Sept couleurs : chaque hexagone touche tous les autres",
    "v_kissing": "Empilement de cercles le plus dense",
    "v_dissect1": "2-uniforme : un tiers des hexagones coupés en triangles",
    "v_dissect2": "2-uniforme : deux tiers des hexagones coupés en triangles",
    "v_kagome": "Kagome : arêtes colorées par direction",
    "v_unequal": "Triangles de deux tailles",
    "v_twisted": "Triangles tournés : les hexagones deviennent des étoiles",
    "v_twisted2": "Tournés davantage",
    "v_hexstar": "Hexagones et étoiles à six branches",
    "v_rhombille": "Pavage rhombique : losanges de 60°",
    "v_siena": "Trois nuances par orientation, comme à la cathédrale de Sienne",
    "v_cubes": "Cubes empilés : une teinte en trois valeurs",
    "v_rh_dual": "Sur son dual, le pavage trihexagonal",
    "v_skew": "Incliné et tourné : parallélogrammes",
    "v_pyth_half": "Carrés de côtés 1 et 1/2",
    "v_pyth_golden": "Côtés dans le nombre d'or",
    "v_pyth_random": "Côtés 1 et 0,3, tons de terre aléatoires",
    "n_triangular": "3.3.3.3.3.3 triangulaire",
    "n_square": "4.4.4.4 carré",
    "n_hexagonal": "6.6.6 hexagonal",
    "n_trihexagonal": "3.6.3.6 trihexagonal",
    "n_truncated_hexagonal": "3.12.12 hexagonal tronqué",
    "n_truncated_square": "4.8.8 carré tronqué",
    "n_truncated_trihexagonal": "4.6.12 trihexagonal tronqué",
    "n_rhombitrihexagonal": "3.4.6.4 rhombitrihexagonal",
    "n_snub_hexagonal": "3.3.3.3.6 hexagonal adouci",
    "n_elongated_triangular": "3.3.3.4.4 triangulaire allongé",
    "n_snub_square": "3.3.4.3.4 carré adouci",
    "v_p3": "P3 : losanges épais et minces",
    "v_p3_ori": "P3 selon les dix orientations des losanges",
    "v_p3_proper": "P3, losanges voisins différents",
    "v_p3_rings": "P3 en anneaux autour du centre",
    "v_p2": "P2 : cerfs-volants et fléchettes",
    "v_p2_rings": "P2 en anneaux autour du centre",
    "v_p2_proper": "P2, pièces voisines différentes",
    "v_hat": "Le chapeau : une forme et son image miroir",
    "v_hat_ori": "Chapeaux par orientation",
    "v_robinson": "Tuiles de Robinson : leurs marques dessinent des carrés emboîtés",
    "v_hb_2": "Briques 2:1",
    "v_hb_45": "Tourné de 45°",
    "v_hb_3": "Briques 3:1",
    "v_hb_long": "Lames longues, environ 6,6:1",
    "v_hb_par": "Parallélogrammes",
    "v_basket": "Tressage",
    "v_halves": "Type 1 : hexagones coupés en deux",
    "v_halves_alt": "Type 1, coupé dans trois directions",
    "v_cairo_p": "Pavage du Caire (types 2 et 4)",
    "v_prismatic": "Pentagonal prismatique (dual de 3.3.3.4.4)",
    "v_floret": "Pentagonal en fleurettes (dual de 3.3.3.3.6)",
    "v_floret_proper": "En fleurettes, voisins différents",
    "v_cairo": "Pavage du Caire : dual du pavage carré adouci",
    "v_cairo_ori": "Quatre orientations",
    "v_cairo_proper": "Pentagones voisins différents",
    "v_cairo_dual": "Sur son dual, le pavage carré adouci",
    "v_girih_tiles": "Décagones et nœuds papillon",
    "v_girih_lines": "Lignes girih, coupant chaque arête à 54°",
    "v_girih_star": "Le motif girih, coloré",
    "v_girih_star2": "Le même motif, palette zellige",
    "v_wang": "Jeandel–Rao : 11 tuiles, 4 couleurs, apériodique",
    "v_wang_scheme": "Les mêmes tuiles, couleurs d'une harmonie",
    "v_stars_crosses": "Étoiles à huit branches et croix",
    "v_sc_azulejo": "Étoiles et croix en bleus d'azulejo",
    "v_z8": "Étoiles à huit branches à partir d'octogones en contact",
    "v_z12": "Étoiles à douze, six et quatre branches",
    "v_z10": "Étoiles à dix branches (base girih)",
    "v_i6": "Étoiles à six branches à partir d'hexagones en contact",
    "v_i_sq": "Octogones et étoiles à quatre branches à partir de carrés",
    "v_i_31212": "Étoiles à douze branches à partir de 3.12.12",
    "v_i_4612": "Rosaces à partir de 4.6.12",
    "v_i_3464": "Étoiles à partir de 3.4.6.4",
    "v_i_snub": "Étoiles à partir du pavage carré adouci",
    "app_title": "Pavages et mosaïques", "app_tiling": "Pavage", "app_scheme": "Harmonie",
    "app_hue": "Teinte de base", "app_size": "Largeur", "app_save": "Enregistrer…",
    "app_saved": "Enregistré : %s", "app_drawing": "Dessin…",
    "app_error": "Impossible de dessiner cette combinaison : %s", "app_panels": "panneaux",
    "app_params": "Paramètres", "app_params_hint": "nom=valeur, séparés par des espaces ; Entrée applique",
})

# ---------------------------------------------------------------------- IT
STRINGS["it"].update({
    "title": "TASSELLATURE E MOSAICI",
    "subtitle": "Tassellature regolari, semiregolari, aperiodiche e islamiche, colorate con la teoria del colore",
    "intro": "Una tassellatura copre il piano con delle forme, senza buchi né sovrapposizioni. La "
             "stessa tassellatura cambia carattere con la colorazione: per tipo di tessera, per "
             "orientamento, per immagine speculare, o in modo che le tessere vicine siano sempre "
             "diverse. Ogni pagina disegna le tassellature di una voce di Wikipedia con diverse "
             "colorazioni; i colori vengono dagli schemi del cerchio RYB o da tavolozze tradizionali "
             "di piastrelle. Tutto è calcolato: reticoli di poligoni, duali, la deflazione di Penrose, "
             "le metatessere del cappello, una ricerca di tassellature di Wang e il metodo di Hankin "
             "per i motivi a stella.",
    "schemes_t": "Schemi di colore",
    "schemes_d": "Gli schemi RYB prendono tinte a passi fissi sul cerchio di 12 tinte a partire da una "
                 "tinta di base (qui il rosso); quando una tassellatura chiede più colori, si aggiungono "
                 "versioni chiare e scure delle stesse tinte. Le tavolozze con nome riprendono "
                 "piastrelle smaltate tradizionali.",
    "contents": "Indice", "colouring": "Colorazione", "cont": "segue", "page": "pagina",
    "c_single": "un colore", "c_kind": "per tipo di tessera", "c_shape": "per forma",
    "c_chirality": "per immagine speculare", "c_orientation": "per orientamento",
    "c_proper": "vicine diverse", "c_random": "casuale", "c_rings": "anelli dal centro",
    "c_classic": "i quattro colori dei bordi", "c_scheme": "colori dei bordi da uno schema",
    "c_checker": "scacchiera", "c_gradient": "sfumatura in diagonale",
    "f_triangular": "Tassellatura triangolare",
    "f_triangular_d": "Sei triangoli equilateri si incontrano in ogni vertice. Le colorazioni uniformi "
                      "prendono il nome dai colori attorno a un vertice: 121212 alterna due colori, "
                      "121314 ne richiede quattro. Tagliando ancora i triangoli si ottengono le "
                      "tassellature kisrhombille e kisdeltile.",
    "f_truncated_square": "Tassellatura quadrata troncata",
    "f_truncated_square_d": "Un quadrato e due ottagoni regolari in ogni vertice (4.8.8), il pavimento "
                            "di molte cucine. I quadrati possono avere due dimensioni e al limite metà "
                            "di essi scompare (tassellatura smussata). La sua duale è la tassellatura "
                            "tetrakis quadrata.",
    "f_hexagonal": "Tassellatura esagonale",
    "f_hexagonal_d": "Tre esagoni in ogni vertice, come in un alveare. Gli esagoni si possono colorare "
                     "in modo regolare con 2, 3, 4 o 7 colori; con 7 ogni esagono tocca tutti gli altri "
                     "colori. Tagliando alcuni esagoni in triangoli si ottengono tassellature "
                     "2-uniformi.",
    "f_trihexagonal": "Tassellatura triesagonale",
    "f_trihexagonal_d": "Triangoli ed esagoni si alternano attorno a ogni vertice (3.6.3.6); i lati "
                        "formano tre famiglie di rette, il motivo kagome dei cesti giapponesi. Ruotare "
                        "o ridimensionare i triangoli mantiene la stessa struttura.",
    "f_rhombille": "Tassellatura a rombi",
    "f_rhombille_d": "Rombi uguali di 60°, tre attorno a un angolo e sei attorno all'altro: la duale "
                     "della triesagonale. Con tre valori di una tinta sembra una pila di cubi, motivo di "
                     "pavimenti antichi come quello del Duomo di Siena.",
    "f_pythagorean": "Tassellatura pitagorica",
    "f_pythagorean_d": "Quadrati di due dimensioni, ognuno a contatto con quattro quadrati dell'altra "
                       "dimensione. È la figura di una classica dimostrazione del teorema di Pitagora "
                       "e un motivo comune di pavimento (girandola o campana).",
    "f_regular": "Poligoni regolari",
    "f_regular_d": "Le undici tassellature uniformi (archimedee) con poligoni regolari: ogni vertice ha "
                   "attorno gli stessi poligoni, indicati con il numero dei lati (3.4.6.4 è triangolo, "
                   "quadrato, esagono, quadrato). Mescolare tipi di vertice dà tassellature k-uniformi.",
    "f_penrose": "Tassellature di Penrose",
    "f_penrose_d": "Due tessere che coprono il piano solo senza ripetersi: rombi larghi e stretti (P3), "
                   "o aquiloni e dardi (P2). Si disegnano tagliando più volte triangoli aurei "
                   "(deflazione) e mostrano ovunque una simmetria di ordine cinque.",
    "f_aperiodic": "Tassellature aperiodiche",
    "f_aperiodic_d": "Tassellature che non si ripetono mai. Il cappello (2023) è un'unica forma, usata "
                     "con la sua immagine speculare, che tassella solo in modo aperiodico; le sei "
                     "tessere quadrate di Robinson impongono quadrati annidati sempre più grandi.",
    "f_herringbone": "Spina di pesce",
    "f_herringbone_d": "Rettangoli posati a scala, ognuno ad angolo retto con i vicini: il classico "
                       "motivo di mattoni e parquet. Mattoni più lunghi, una rotazione di 45° o "
                       "parallelogrammi ne cambiano l'aspetto; l'intreccio a cesto accoppia i mattoni.",
    "f_pentagonal": "Tassellature pentagonali",
    "f_pentagonal_d": "I pentagoni regolari non tassellano il piano, ma 15 famiglie di pentagoni "
                      "convessi sì. Dimezzare gli esagoni dà il tipo 1; le duali di tre tassellature "
                      "uniformi danno le pentagonali del Cairo, prismatica e a fiore.",
    "f_cairo": "Tassellatura pentagonale del Cairo",
    "f_cairo_d": "Pentagoni con quattro lati lunghi e uno corto, duale della tassellatura quadrata "
                 "camusa, dal nome delle strade del Cairo. In alcuni vertici si incontrano quattro "
                 "pentagoni, in altri tre, e coppie di pentagoni formano esagoni.",
    "f_girih": "Tessere girih",
    "f_girih_d": "Cinque tessere a lati uguali (decagono, pentagono, esagono, farfallino, rombo) "
                 "dell'architettura persiana. Le linee tracciate su di esse tagliano ogni lato nel punto "
                 "medio a 54°, e si uniscono da tessera a tessera nel motivo a stelle.",
    "f_wang": "Tessere di Wang",
    "f_wang_d": "Quadrati con i bordi colorati, posati in modo che i bordi a contatto coincidano, "
                "senza mai ruotarli. Le 11 tessere di Jeandel e Rao (2015) tassellano il piano solo "
                "in modo aperiodico; questo tratto è stato trovato con una ricerca a ritroso.",
    "f_zellij": "Zellige",
    "f_zellij_d": "Mosaico marocchino e andaluso di tessere smaltate tagliate a mano, in bianco, verde, "
                  "nero, ocra e azzurri. Tipiche le stelle a otto punte con croci e i sistemi di "
                  "stelle a 6, 8, 10 e 12 punte.",
    "f_islamic": "Motivi geometrici islamici",
    "f_islamic_d": "Motivi a stella ottenuti con il metodo di Hankin dei poligoni a contatto: dal "
                   "punto medio di ogni lato di una tassellatura partono due linee con un angolo fisso "
                   "finché si incontrano. La tassellatura di base e l'angolo decidono le stelle; gli "
                   "intrecci sono disegnati come nastri.",
    "v_uniform": "Colorazione uniforme %s",
    "v_tri_regular": "Tassellatura triangolare regolare {3,6}",
    "v_kisrhombille": "Kisrhombille: triangoli 30-60-90 (duale di 4.6.12)",
    "v_triakis": "Kisdeltile: triangoli 30-30-120 (duale di 3.12.12)",
    "v_ts_plain": "Tassellatura quadrata troncata 4.8.8",
    "v_circlepack": "Impacchettamento di cerchi: un cerchio in ogni vertice",
    "v_ts_alt": "Quadrati di dimensioni alternate",
    "v_ts_chamfer": "Tassellatura quadrata smussata (i quadrati piccoli scompaiono)",
    "v_tetrakis": "Tassellatura tetrakis quadrata (duale di 4.8.8)",
    "v_dual_overlay": "Con la duale disegnata sopra",
    "v_hex_regular": "Tassellatura esagonale regolare {6,3}",
    "v_hex_2": "Due colori, a file",
    "v_hex_21": "Due colori, un esagono su tre",
    "v_hex_3": "Tre colori: i vicini sono sempre diversi",
    "v_hex_4": "Quattro colori",
    "v_hex_7": "Sette colori: ogni esagono tocca tutti gli altri",
    "v_kissing": "Impacchettamento di cerchi più denso",
    "v_dissect1": "2-uniforme: un terzo degli esagoni tagliati in triangoli",
    "v_dissect2": "2-uniforme: due terzi degli esagoni tagliati in triangoli",
    "v_kagome": "Kagome: lati colorati per direzione",
    "v_unequal": "Triangoli di due dimensioni",
    "v_twisted": "Triangoli ruotati: gli esagoni diventano stelle",
    "v_twisted2": "Ruotati ancora",
    "v_hexstar": "Esagoni e stelle a sei punte",
    "v_rhombille": "Tassellatura a rombi di 60°",
    "v_siena": "Tre toni per orientamento, come nel Duomo di Siena",
    "v_cubes": "Cubi impilati: una tinta in tre valori",
    "v_rh_dual": "Sulla sua duale, la tassellatura triesagonale",
    "v_skew": "Inclinata e ruotata: parallelogrammi",
    "v_pyth_half": "Quadrati di lato 1 e 1/2",
    "v_pyth_golden": "Lati nella sezione aurea",
    "v_pyth_random": "Lati 1 e 0,3, toni della terra casuali",
    "n_triangular": "3.3.3.3.3.3 triangolare",
    "n_square": "4.4.4.4 quadrata",
    "n_hexagonal": "6.6.6 esagonale",
    "n_trihexagonal": "3.6.3.6 triesagonale",
    "n_truncated_hexagonal": "3.12.12 esagonale troncata",
    "n_truncated_square": "4.8.8 quadrata troncata",
    "n_truncated_trihexagonal": "4.6.12 triesagonale troncata",
    "n_rhombitrihexagonal": "3.4.6.4 rombitriesagonale",
    "n_snub_hexagonal": "3.3.3.3.6 esagonale camusa",
    "n_elongated_triangular": "3.3.3.4.4 triangolare allungata",
    "n_snub_square": "3.3.4.3.4 quadrata camusa",
    "v_p3": "P3: rombi larghi e stretti",
    "v_p3_ori": "P3 secondo i dieci orientamenti dei rombi",
    "v_p3_proper": "P3, rombi vicini diversi",
    "v_p3_rings": "P3 ad anelli attorno al centro",
    "v_p2": "P2: aquiloni e dardi",
    "v_p2_rings": "P2 ad anelli attorno al centro",
    "v_p2_proper": "P2, tessere vicine diverse",
    "v_hat": "Il cappello: una forma e la sua immagine speculare",
    "v_hat_ori": "Cappelli per orientamento",
    "v_robinson": "Tessere di Robinson: i segni disegnano quadrati annidati",
    "v_hb_2": "Mattoni 2:1",
    "v_hb_45": "Ruotato di 45°",
    "v_hb_3": "Mattoni 3:1",
    "v_hb_long": "Listoni lunghi, circa 6,6:1",
    "v_hb_par": "Parallelogrammi",
    "v_basket": "Intreccio a cesto",
    "v_halves": "Tipo 1: esagoni tagliati a metà",
    "v_halves_alt": "Tipo 1, tagliato in tre direzioni",
    "v_cairo_p": "Tassellatura del Cairo (tipi 2 e 4)",
    "v_prismatic": "Pentagonale prismatica (duale di 3.3.3.4.4)",
    "v_floret": "Pentagonale a fiore (duale di 3.3.3.3.6)",
    "v_floret_proper": "A fiore, vicine diverse",
    "v_cairo": "Tassellatura del Cairo: duale della quadrata camusa",
    "v_cairo_ori": "Quattro orientamenti",
    "v_cairo_proper": "Pentagoni vicini diversi",
    "v_cairo_dual": "Sulla sua duale, la tassellatura quadrata camusa",
    "v_girih_tiles": "Decagoni e farfallini",
    "v_girih_lines": "Linee girih, che tagliano ogni lato a 54°",
    "v_girih_star": "Il motivo girih, colorato",
    "v_girih_star2": "Lo stesso motivo, tavolozza zellige",
    "v_wang": "Jeandel–Rao: 11 tessere, 4 colori, aperiodica",
    "v_wang_scheme": "Le stesse tessere, colori da uno schema",
    "v_stars_crosses": "Stelle a otto punte e croci",
    "v_sc_azulejo": "Stelle e croci negli azzurri degli azulejos",
    "v_z8": "Stelle a otto punte da ottagoni a contatto",
    "v_z12": "Stelle a dodici, sei e quattro punte",
    "v_z10": "Stelle a dieci punte (base girih)",
    "v_i6": "Stelle a sei punte da esagoni a contatto",
    "v_i_sq": "Ottagoni e stelle a quattro punte da quadrati",
    "v_i_31212": "Stelle a dodici punte da 3.12.12",
    "v_i_4612": "Rosoni da 4.6.12",
    "v_i_3464": "Stelle da 3.4.6.4",
    "v_i_snub": "Stelle dalla tassellatura quadrata camusa",
    "app_title": "Tassellature e mosaici", "app_tiling": "Tassellatura", "app_scheme": "Schema",
    "app_hue": "Tinta di base", "app_size": "Larghezza", "app_save": "Salva…",
    "app_saved": "Salvato: %s", "app_drawing": "Disegno…",
    "app_error": "Impossibile disegnare questa combinazione: %s", "app_panels": "riquadri",
    "app_params": "Parametri", "app_params_hint": "nome=valore, separati da spazi; Invio applica",
})

# ---------------------------------------------------------------------- DE
STRINGS["de"].update({
    "title": "PARKETTIERUNGEN UND MOSAIKE",
    "subtitle": "Reguläre, halbreguläre, aperiodische und islamische Parkettierungen, gefärbt nach der Farbenlehre",
    "intro": "Eine Parkettierung bedeckt die Ebene mit Formen, ohne Lücken und Überlappungen. Dieselbe "
             "Parkettierung verändert ihren Charakter mit der Färbung: nach Art der Fliese, nach "
             "Ausrichtung, nach Spiegelbild oder so, dass benachbarte Fliesen immer verschieden sind. "
             "Jede Seite zeichnet die Parkettierungen eines Wikipedia-Artikels in mehreren Färbungen; "
             "die Farben stammen aus den Farbschemata des RYB-Kreises oder aus traditionellen "
             "Fliesenpaletten. Alles ist berechnet: Polygongitter, duale Parkettierungen, die "
             "Penrose-Deflation, die Metakacheln des Hutes, eine Suche nach Wang-Parkettierungen und "
             "Hankins Methode für Sternmuster.",
    "schemes_t": "Farbschemata",
    "schemes_d": "RYB-Schemata nehmen Farbtöne in festen Schritten des 12-teiligen Kreises ab einem "
                 "Grundfarbton (hier Rot); braucht eine Parkettierung mehr Farben, als ein Schema hat, "
                 "kommen hellere und dunklere Stufen derselben Farbtöne hinzu. Die benannten Paletten "
                 "folgen traditionellen glasierten Fliesen.",
    "contents": "Inhalt", "colouring": "Färbung", "cont": "Fortsetzung", "page": "Seite",
    "c_single": "eine Farbe", "c_kind": "nach Fliesenart", "c_shape": "nach Form",
    "c_chirality": "nach Spiegelbild", "c_orientation": "nach Ausrichtung",
    "c_proper": "Nachbarn verschieden", "c_random": "zufällig", "c_rings": "Ringe um die Mitte",
    "c_classic": "die vier Kantenfarben", "c_scheme": "Kantenfarben aus einem Schema",
    "c_checker": "Schachbrett", "c_gradient": "Verlauf diagonal",
    "f_triangular": "Dreiecksparkett",
    "f_triangular_d": "An jeder Ecke treffen sich sechs gleichseitige Dreiecke. Die gleichmäßigen "
                      "Färbungen heißen nach den Farben um eine Ecke: 121212 wechselt zwei Farben ab, "
                      "121314 braucht vier. Weiteres Teilen der Dreiecke ergibt die Kisrhombille- und "
                      "Kisdeltile-Parkettierungen.",
    "f_truncated_square": "Abgestumpftes Quadratparkett",
    "f_truncated_square_d": "Ein Quadrat und zwei reguläre Achtecke an jeder Ecke (4.8.8), der Boden "
                            "vieler Küchen. Die Quadrate können zwei Größen haben; im Grenzfall "
                            "verschwindet die Hälfte (abgeschrägtes Parkett). Sein Dual ist das "
                            "Tetrakis-Quadratparkett.",
    "f_hexagonal": "Sechseckparkett",
    "f_hexagonal_d": "Drei Sechsecke an jeder Ecke, wie in einer Bienenwabe. Die Sechsecke lassen sich "
                     "regelmäßig mit 2, 3, 4 oder 7 Farben färben; bei 7 berührt jedes Sechseck alle "
                     "anderen Farben. Teilt man einige Sechsecke in Dreiecke, entstehen 2-uniforme "
                     "Parkettierungen.",
    "f_trihexagonal": "Trihexagonales Parkett",
    "f_trihexagonal_d": "Dreiecke und Sechsecke wechseln sich um jede Ecke ab (3.6.3.6); die Kanten "
                        "bilden drei Scharen von Geraden, das Kagome-Muster japanischer Körbe. Drehen "
                        "oder Skalieren der Dreiecke erhält die Struktur.",
    "f_rhombille": "Rautenparkett",
    "f_rhombille_d": "Gleiche 60°-Rauten, drei um die eine Ecke und sechs um die andere: das Dual des "
                     "trihexagonalen Parketts. Mit drei Helligkeiten eines Farbtons wirkt es wie ein "
                     "Stapel Würfel, ein Muster alter Böden wie im Dom von Siena.",
    "f_pythagorean": "Pythagoreisches Parkett",
    "f_pythagorean_d": "Quadrate zweier Größen, jedes berührt vier Quadrate der anderen Größe. Es ist "
                       "das Bild eines klassischen Beweises des Satzes des Pythagoras und ein häufiges "
                       "Bodenmuster.",
    "f_regular": "Reguläre Vielecke",
    "f_regular_d": "Die elf gleichmäßigen (archimedischen) Parkettierungen aus regulären Vielecken: an "
                   "jeder Ecke liegen dieselben Vielecke, angegeben durch ihre Eckenzahl (3.4.6.4 ist "
                   "Dreieck, Quadrat, Sechseck, Quadrat). Gemischte Eckentypen ergeben k-uniforme "
                   "Parkettierungen.",
    "f_penrose": "Penrose-Parkettierungen",
    "f_penrose_d": "Zwei Fliesen, die die Ebene nur ohne Wiederholung bedecken: dicke und dünne Rauten "
                   "(P3) oder Drachen und Pfeile (P2). Sie entstehen durch wiederholtes Teilen goldener "
                   "Dreiecke (Deflation) und zeigen überall fünfzählige Symmetrie.",
    "f_aperiodic": "Aperiodische Parkettierungen",
    "f_aperiodic_d": "Parkettierungen, die sich nie wiederholen. Der Hut (2023) ist eine einzige Form, "
                     "zusammen mit ihrem Spiegelbild, die nur aperiodisch parkettiert; Robinsons sechs "
                     "Quadratfliesen erzwingen verschachtelte, immer größere Quadrate.",
    "f_herringbone": "Fischgrätmuster",
    "f_herringbone_d": "Rechtecke treppenartig verlegt, jedes rechtwinklig zu seinen Nachbarn: das "
                       "klassische Ziegel- und Parkettmuster. Längere Steine, eine Drehung um 45° oder "
                       "Parallelogramme verändern es; der Flechtverband legt die Steine paarweise.",
    "f_pentagonal": "Fünfeckparkettierungen",
    "f_pentagonal_d": "Reguläre Fünfecke parkettieren die Ebene nicht, wohl aber 15 Familien konvexer "
                      "Fünfecke. Halbierte Sechsecke ergeben Typ 1; die Duale dreier gleichmäßiger "
                      "Parkettierungen ergeben das Kairo-, das prismatische und das Blüten-Fünfeckparkett.",
    "f_cairo": "Kairo-Fünfeckparkett",
    "f_cairo_d": "Fünfecke mit vier langen und einer kurzen Seite, das Dual des abgeschrägten "
                 "Quadratparketts, benannt nach den Straßen von Kairo. An manchen Ecken treffen sich vier "
                 "Fünfecke, an anderen drei, und Paare von Fünfecken bilden Sechsecke.",
    "f_girih": "Girih-Fliesen",
    "f_girih_d": "Fünf gleichseitige Fliesen (Zehneck, Fünfeck, Sechseck, Fliege, Raute) der "
                 "persischen Architektur. Die Linien auf ihnen kreuzen jede Kante in der Mitte unter 54° "
                 "und verbinden sich über die Fliesen hinweg zum sichtbaren Sternmuster.",
    "f_wang": "Wang-Kacheln",
    "f_wang_d": "Quadrate mit farbigen Kanten, so gelegt, dass sich berührende Kanten übereinstimmen, "
                "ohne sie je zu drehen. Die 11 Kacheln von Jeandel und Rao (2015) parkettieren die "
                "Ebene nur aperiodisch; dieser Ausschnitt wurde mit einer Rückverfolgungssuche gefunden.",
    "f_zellij": "Zellige",
    "f_zellij_d": "Marokkanisches und andalusisches Mosaik aus handgeschnittenen glasierten Stücken in "
                  "Weiß, Grün, Schwarz, Ocker und Blautönen. Typisch sind achtzackige Sterne mit "
                  "Kreuzen und Sternsysteme mit 6, 8, 10 und 12 Zacken.",
    "f_islamic": "Islamische geometrische Muster",
    "f_islamic_d": "Sternmuster nach Hankins Methode der sich berührenden Vielecke: von der Mitte jeder "
                   "Kante einer Parkettierung gehen zwei Linien unter festem Winkel aus, bis sie sich "
                   "treffen. Grundparkett und Winkel bestimmen die Sterne; die Bänder werden als "
                   "Flechtbänder gezeichnet.",
    "v_uniform": "Gleichmäßige Färbung %s",
    "v_tri_regular": "Reguläres Dreiecksparkett {3,6}",
    "v_kisrhombille": "Kisrhombille: 30-60-90-Dreiecke (Dual von 4.6.12)",
    "v_triakis": "Kisdeltile: 30-30-120-Dreiecke (Dual von 3.12.12)",
    "v_ts_plain": "Abgestumpftes Quadratparkett 4.8.8",
    "v_circlepack": "Kreispackung: ein Kreis an jeder Ecke",
    "v_ts_alt": "Quadrate abwechselnder Größe",
    "v_ts_chamfer": "Abgeschrägtes Quadratparkett (kleine Quadrate verschwinden)",
    "v_tetrakis": "Tetrakis-Quadratparkett (Dual von 4.8.8)",
    "v_dual_overlay": "Mit seinem Dual darüber",
    "v_hex_regular": "Reguläres Sechseckparkett {6,3}",
    "v_hex_2": "Zwei Farben, in Reihen",
    "v_hex_21": "Zwei Farben, jedes dritte Sechseck",
    "v_hex_3": "Drei Farben: Nachbarn immer verschieden",
    "v_hex_4": "Vier Farben",
    "v_hex_7": "Sieben Farben: jedes Sechseck berührt alle anderen",
    "v_kissing": "Dichteste Kreispackung",
    "v_dissect1": "2-uniform: ein Drittel der Sechsecke in Dreiecke geteilt",
    "v_dissect2": "2-uniform: zwei Drittel der Sechsecke in Dreiecke geteilt",
    "v_kagome": "Kagome: Kanten nach Richtung gefärbt",
    "v_unequal": "Dreiecke zweier Größen",
    "v_twisted": "Gedrehte Dreiecke: aus Sechsecken werden Sterne",
    "v_twisted2": "Weiter gedreht",
    "v_hexstar": "Sechsecke und sechszackige Sterne",
    "v_rhombille": "Rautenparkett: 60°-Rauten",
    "v_siena": "Drei Stufen nach Ausrichtung, wie im Dom von Siena",
    "v_cubes": "Gestapelte Würfel: ein Farbton in drei Helligkeiten",
    "v_rh_dual": "Über seinem Dual, dem trihexagonalen Parkett",
    "v_skew": "Geschert und gedreht: Parallelogramme",
    "v_pyth_half": "Quadrate mit den Seiten 1 und 1/2",
    "v_pyth_golden": "Seiten im Goldenen Schnitt",
    "v_pyth_random": "Seiten 1 und 0,3, zufällige Erdtöne",
    "n_triangular": "3.3.3.3.3.3 Dreiecke",
    "n_square": "4.4.4.4 Quadrate",
    "n_hexagonal": "6.6.6 Sechsecke",
    "n_trihexagonal": "3.6.3.6 trihexagonal",
    "n_truncated_hexagonal": "3.12.12 abgestumpft hexagonal",
    "n_truncated_square": "4.8.8 abgestumpft quadratisch",
    "n_truncated_trihexagonal": "4.6.12 abgestumpft trihexagonal",
    "n_rhombitrihexagonal": "3.4.6.4 rhombitrihexagonal",
    "n_snub_hexagonal": "3.3.3.3.6 abgeschrägt hexagonal",
    "n_elongated_triangular": "3.3.3.4.4 gestreckt dreieckig",
    "n_snub_square": "3.3.4.3.4 abgeschrägt quadratisch",
    "v_p3": "P3: dicke und dünne Rauten",
    "v_p3_ori": "P3 nach den zehn Ausrichtungen der Rauten",
    "v_p3_proper": "P3, benachbarte Rauten verschieden",
    "v_p3_rings": "P3 in Ringen um die Mitte",
    "v_p2": "P2: Drachen und Pfeile",
    "v_p2_rings": "P2 in Ringen um die Mitte",
    "v_p2_proper": "P2, benachbarte Fliesen verschieden",
    "v_hat": "Der Hut: eine Form und ihr Spiegelbild",
    "v_hat_ori": "Hüte nach Ausrichtung",
    "v_robinson": "Robinson-Fliesen: ihre Markierungen zeichnen verschachtelte Quadrate",
    "v_hb_2": "Ziegel 2:1",
    "v_hb_45": "Um 45° gedreht",
    "v_hb_3": "Ziegel 3:1",
    "v_hb_long": "Lange Dielen, etwa 6,6:1",
    "v_hb_par": "Parallelogramme",
    "v_basket": "Flechtverband",
    "v_halves": "Typ 1: halbierte Sechsecke",
    "v_halves_alt": "Typ 1, in drei Richtungen geteilt",
    "v_cairo_p": "Kairo-Parkett (Typen 2 und 4)",
    "v_prismatic": "Prismatisches Fünfeckparkett (Dual von 3.3.3.4.4)",
    "v_floret": "Blüten-Fünfeckparkett (Dual von 3.3.3.3.6)",
    "v_floret_proper": "Blüten-Fünfeckparkett, Nachbarn verschieden",
    "v_cairo": "Kairo-Parkett: Dual des abgeschrägten Quadratparketts",
    "v_cairo_ori": "Vier Ausrichtungen",
    "v_cairo_proper": "Benachbarte Fünfecke verschieden",
    "v_cairo_dual": "Über seinem Dual, dem abgeschrägten Quadratparkett",
    "v_girih_tiles": "Zehnecke und Fliegen",
    "v_girih_lines": "Girih-Linien, die jede Kante unter 54° kreuzen",
    "v_girih_star": "Das Girih-Muster, gefärbt",
    "v_girih_star2": "Dasselbe Muster, Zellige-Palette",
    "v_wang": "Jeandel–Rao: 11 Kacheln, 4 Farben, aperiodisch",
    "v_wang_scheme": "Dieselben Kacheln, Farben aus einem Schema",
    "v_stars_crosses": "Achtzackige Sterne und Kreuze",
    "v_sc_azulejo": "Sterne und Kreuze in Azulejo-Blau",
    "v_z8": "Achtzackige Sterne aus sich berührenden Achtecken",
    "v_z12": "Zwölf-, sechs- und vierzackige Sterne",
    "v_z10": "Zehnzackige Sterne (Girih-Grundlage)",
    "v_i6": "Sechszackige Sterne aus sich berührenden Sechsecken",
    "v_i_sq": "Achtecke und vierzackige Sterne aus Quadraten",
    "v_i_31212": "Zwölfzackige Sterne aus 3.12.12",
    "v_i_4612": "Rosetten aus 4.6.12",
    "v_i_3464": "Sterne aus 3.4.6.4",
    "v_i_snub": "Sterne aus dem abgeschrägten Quadratparkett",
    "app_title": "Parkettierungen und Mosaike", "app_tiling": "Parkett", "app_scheme": "Schema",
    "app_hue": "Grundfarbton", "app_size": "Breite", "app_save": "Speichern…",
    "app_saved": "Gespeichert: %s", "app_drawing": "Wird gezeichnet…",
    "app_error": "Diese Kombination lässt sich nicht zeichnen: %s", "app_panels": "Felder",
    "app_params": "Parameter", "app_params_hint": "name=wert, durch Leerzeichen getrennt; Eingabe übernimmt",
})

# ---------------------------------------------------------------------- NL
STRINGS["nl"].update({
    "title": "BETEGELINGEN EN MOZAÏEKEN",
    "subtitle": "Regelmatige, halfregelmatige, aperiodieke en islamitische betegelingen, gekleurd met kleurenleer",
    "intro": "Een betegeling bedekt het vlak met vormen, zonder gaten of overlappingen. Dezelfde "
             "betegeling krijgt een ander karakter door de kleuring: per soort tegel, per richting, per "
             "spiegelbeeld, of zo dat buurtegels altijd verschillen. Elke pagina tekent de betegelingen "
             "van één Wikipedia-artikel met meerdere kleuringen; de kleuren komen uit de kleurenschema's "
             "van de RYB-cirkel of uit traditionele tegelpaletten. Alles is berekend: roosters van "
             "veelhoeken, dualen, Penrose-deflatie, de metategels van de hoed, een zoektocht naar "
             "Wang-betegelingen en de methode van Hankin voor stermotieven.",
    "schemes_t": "Kleurenschema's",
    "schemes_d": "RYB-schema's nemen kleurtonen met vaste stappen op de cirkel van 12 tonen vanaf een "
                 "basistoon (hier rood); heeft een betegeling meer kleuren nodig dan een schema heeft, "
                 "dan komen lichtere en donkerdere varianten van dezelfde tonen erbij. De benoemde "
                 "paletten volgen traditionele geglazuurde tegels.",
    "contents": "Inhoud", "colouring": "Kleuring", "cont": "vervolg", "page": "pagina",
    "c_single": "één kleur", "c_kind": "per soort tegel", "c_shape": "per vorm",
    "c_chirality": "per spiegelbeeld", "c_orientation": "per richting",
    "c_proper": "buren verschillend", "c_random": "willekeurig", "c_rings": "ringen vanuit het midden",
    "c_classic": "de vier randkleuren", "c_scheme": "randkleuren uit een schema",
    "c_checker": "dambord", "c_gradient": "diagonaal verloop",
    "f_triangular": "Driehoeksbetegeling",
    "f_triangular_d": "In elk hoekpunt komen zes gelijkzijdige driehoeken samen. De uniforme kleuringen "
                      "zijn genoemd naar de kleuren rond een hoekpunt: 121212 wisselt twee kleuren af, "
                      "121314 heeft er vier nodig. Verder delen van de driehoeken geeft de kisrhombille- "
                      "en kisdeltile-betegelingen.",
    "f_truncated_square": "Afgeknotte vierkantsbetegeling",
    "f_truncated_square_d": "Een vierkant en twee regelmatige achthoeken in elk hoekpunt (4.8.8), de "
                            "vloer van veel keukens. De vierkanten kunnen twee maten hebben; in het "
                            "uiterste geval verdwijnt de helft (afgeschuinde betegeling). De duale is "
                            "de tetrakis-vierkantsbetegeling.",
    "f_hexagonal": "Zeshoeksbetegeling",
    "f_hexagonal_d": "Drie zeshoeken in elk hoekpunt, zoals in een honingraat. Zeshoeken kunnen "
                     "regelmatig met 2, 3, 4 of 7 kleuren gekleurd worden; met 7 raakt elke zeshoek alle "
                     "andere kleuren. Sommige zeshoeken in driehoeken delen geeft 2-uniforme "
                     "betegelingen.",
    "f_trihexagonal": "Trihexagonale betegeling",
    "f_trihexagonal_d": "Driehoeken en zeshoeken wisselen elkaar af rond elk hoekpunt (3.6.3.6); de "
                        "randen vormen drie families rechte lijnen, het kagome-patroon van Japanse "
                        "manden. Draaien of schalen van de driehoeken behoudt de structuur.",
    "f_rhombille": "Ruitenbetegeling",
    "f_rhombille_d": "Gelijke ruiten van 60°, drie rond de ene hoek en zes rond de andere: de duale van "
                     "de trihexagonale betegeling. Met drie waarden van één kleurtoon lijkt het een "
                     "stapel kubussen, een patroon op oude vloeren zoals in de kathedraal van Siena.",
    "f_pythagorean": "Pythagoreïsche betegeling",
    "f_pythagorean_d": "Vierkanten van twee maten, elk rakend aan vier vierkanten van de andere maat. Het "
                       "is de figuur bij een klassiek bewijs van de stelling van Pythagoras en een "
                       "gangbaar vloerpatroon.",
    "f_regular": "Regelmatige veelhoeken",
    "f_regular_d": "De elf uniforme (archimedische) betegelingen met regelmatige veelhoeken: elk "
                   "hoekpunt heeft dezelfde veelhoeken eromheen, genoteerd als hun aantal zijden "
                   "(3.4.6.4 is driehoek, vierkant, zeshoek, vierkant). Gemengde hoekpunttypen geven "
                   "k-uniforme betegelingen.",
    "f_penrose": "Penrose-betegelingen",
    "f_penrose_d": "Twee tegels die het vlak alleen zonder herhaling bedekken: dikke en dunne ruiten (P3), "
                   "of vliegers en pijlen (P2). Ze worden getekend door gulden driehoeken steeds "
                   "opnieuw te delen (deflatie) en tonen overal vijftallige symmetrie.",
    "f_aperiodic": "Aperiodieke betegelingen",
    "f_aperiodic_d": "Betegelingen die zich nooit herhalen. De hoed (2023) is één vorm, samen met zijn "
                     "spiegelbeeld gebruikt, die alleen aperiodiek betegelt; de zes vierkante tegels "
                     "van Robinson dwingen geneste, steeds grotere vierkanten af.",
    "f_herringbone": "Visgraatpatroon",
    "f_herringbone_d": "Rechthoeken in een trap gelegd, elk haaks op de buren: het klassieke baksteen- "
                       "en parketpatroon. Langere stenen, een draai van 45° of parallellogrammen "
                       "veranderen het uiterlijk; het mandverband legt de stenen in paren.",
    "f_pentagonal": "Vijfhoeksbetegelingen",
    "f_pentagonal_d": "Regelmatige vijfhoeken betegelen het vlak niet, maar 15 families convexe "
                      "vijfhoeken wel. Gehalveerde zeshoeken geven type 1; de dualen van drie uniforme "
                      "betegelingen geven de Caïro-, de prismatische en de bloemvijfhoeksbetegeling.",
    "f_cairo": "Caïro-vijfhoeksbetegeling",
    "f_cairo_d": "Vijfhoeken met vier lange zijden en één korte, de duale van de afgeschuinde "
                 "vierkantsbetegeling, genoemd naar de straten van Caïro. In sommige hoekpunten komen vier "
                 "vijfhoeken samen, in andere drie, en paren vijfhoeken vormen zeshoeken.",
    "f_girih": "Girih-tegels",
    "f_girih_d": "Vijf tegels met gelijke zijden (tienhoek, vijfhoek, zeshoek, strikje, ruit) uit de "
                 "Perzische architectuur. De lijnen erop snijden elke rand in het midden onder 54° en "
                 "lopen zo van tegel tot tegel door in het zichtbare stermotief.",
    "f_wang": "Wang-tegels",
    "f_wang_d": "Vierkanten met gekleurde randen, zo gelegd dat aanliggende randen overeenkomen, zonder "
                "ze ooit te draaien. De 11 tegels van Jeandel en Rao (2015) betegelen het vlak alleen "
                "aperiodiek; dit stuk is gevonden met een zoektocht met terugkrabbelen.",
    "f_zellij": "Zellige",
    "f_zellij_d": "Marokkaans en Andalusisch mozaïek van met de hand gehakte geglazuurde stukjes, in wit, "
                  "groen, zwart, oker en blauwtinten. Typisch zijn achtpuntige sterren met kruisen en "
                  "stersystemen met 6, 8, 10 en 12 punten.",
    "f_islamic": "Islamitische geometrische patronen",
    "f_islamic_d": "Stermotieven volgens de methode van Hankin van rakende veelhoeken: vanuit het midden "
                   "van elke rand van een betegeling vertrekken twee lijnen onder een vaste hoek tot ze "
                   "elkaar ontmoeten. De basisbetegeling en de hoek bepalen de sterren; de banden worden "
                   "als linten getekend.",
    "v_uniform": "Uniforme kleuring %s",
    "v_tri_regular": "Regelmatige driehoeksbetegeling {3,6}",
    "v_kisrhombille": "Kisrhombille: driehoeken 30-60-90 (duaal van 4.6.12)",
    "v_triakis": "Kisdeltile: driehoeken 30-30-120 (duaal van 3.12.12)",
    "v_ts_plain": "Afgeknotte vierkantsbetegeling 4.8.8",
    "v_circlepack": "Cirkelstapeling: een cirkel in elk hoekpunt",
    "v_ts_alt": "Vierkanten van afwisselende grootte",
    "v_ts_chamfer": "Afgeschuinde vierkantsbetegeling (kleine vierkanten verdwijnen)",
    "v_tetrakis": "Tetrakis-vierkantsbetegeling (duaal van 4.8.8)",
    "v_dual_overlay": "Met de duale eroverheen",
    "v_hex_regular": "Regelmatige zeshoeksbetegeling {6,3}",
    "v_hex_2": "Twee kleuren, in rijen",
    "v_hex_21": "Twee kleuren, één op de drie zeshoeken",
    "v_hex_3": "Drie kleuren: buren altijd verschillend",
    "v_hex_4": "Vier kleuren",
    "v_hex_7": "Zeven kleuren: elke zeshoek raakt alle andere",
    "v_kissing": "Dichtste cirkelstapeling",
    "v_dissect1": "2-uniform: een derde van de zeshoeken in driehoeken gedeeld",
    "v_dissect2": "2-uniform: twee derde van de zeshoeken in driehoeken gedeeld",
    "v_kagome": "Kagome: randen gekleurd per richting",
    "v_unequal": "Driehoeken van twee maten",
    "v_twisted": "Gedraaide driehoeken: de zeshoeken worden sterren",
    "v_twisted2": "Verder gedraaid",
    "v_hexstar": "Zeshoeken en zespuntige sterren",
    "v_rhombille": "Ruitenbetegeling: ruiten van 60°",
    "v_siena": "Drie tinten per richting, zoals in de kathedraal van Siena",
    "v_cubes": "Gestapelde kubussen: één kleurtoon in drie waarden",
    "v_rh_dual": "Boven de duale, de trihexagonale betegeling",
    "v_skew": "Scheef en gedraaid: parallellogrammen",
    "v_pyth_half": "Vierkanten met zijden 1 en 1/2",
    "v_pyth_golden": "Zijden in de gulden snede",
    "v_pyth_random": "Zijden 1 en 0,3, willekeurige aardetinten",
    "n_triangular": "3.3.3.3.3.3 driehoeken",
    "n_square": "4.4.4.4 vierkanten",
    "n_hexagonal": "6.6.6 zeshoeken",
    "n_trihexagonal": "3.6.3.6 trihexagonaal",
    "n_truncated_hexagonal": "3.12.12 afgeknot zeshoekig",
    "n_truncated_square": "4.8.8 afgeknot vierkant",
    "n_truncated_trihexagonal": "4.6.12 afgeknot trihexagonaal",
    "n_rhombitrihexagonal": "3.4.6.4 rombitrihexagonaal",
    "n_snub_hexagonal": "3.3.3.3.6 afgeschuind zeshoekig",
    "n_elongated_triangular": "3.3.3.4.4 verlengd driehoekig",
    "n_snub_square": "3.3.4.3.4 afgeschuind vierkant",
    "v_p3": "P3: dikke en dunne ruiten",
    "v_p3_ori": "P3 per de tien richtingen van de ruiten",
    "v_p3_proper": "P3, buurruiten verschillend",
    "v_p3_rings": "P3 in ringen rond het midden",
    "v_p2": "P2: vliegers en pijlen",
    "v_p2_rings": "P2 in ringen rond het midden",
    "v_p2_proper": "P2, buurtegels verschillend",
    "v_hat": "De hoed: één vorm en zijn spiegelbeeld",
    "v_hat_ori": "Hoeden per richting",
    "v_robinson": "Robinson-tegels: hun tekens tekenen geneste vierkanten",
    "v_hb_2": "Stenen 2:1",
    "v_hb_45": "45° gedraaid",
    "v_hb_3": "Stenen 3:1",
    "v_hb_long": "Lange planken, ongeveer 6,6:1",
    "v_hb_par": "Parallellogrammen",
    "v_basket": "Mandverband",
    "v_halves": "Type 1: gehalveerde zeshoeken",
    "v_halves_alt": "Type 1, in drie richtingen gedeeld",
    "v_cairo_p": "Caïro-betegeling (types 2 en 4)",
    "v_prismatic": "Prismatische vijfhoeksbetegeling (duaal van 3.3.3.4.4)",
    "v_floret": "Bloemvijfhoeksbetegeling (duaal van 3.3.3.3.6)",
    "v_floret_proper": "Bloemvijfhoeken, buren verschillend",
    "v_cairo": "Caïro-betegeling: duaal van de afgeschuinde vierkantsbetegeling",
    "v_cairo_ori": "Vier richtingen",
    "v_cairo_proper": "Buurvijfhoeken verschillend",
    "v_cairo_dual": "Boven de duale, de afgeschuinde vierkantsbetegeling",
    "v_girih_tiles": "Tienhoeken en strikjes",
    "v_girih_lines": "Girih-lijnen, die elke rand onder 54° snijden",
    "v_girih_star": "Het girih-motief, gekleurd",
    "v_girih_star2": "Hetzelfde motief, zellige-palet",
    "v_wang": "Jeandel–Rao: 11 tegels, 4 kleuren, aperiodiek",
    "v_wang_scheme": "Dezelfde tegels, kleuren uit een schema",
    "v_stars_crosses": "Achtpuntige sterren en kruisen",
    "v_sc_azulejo": "Sterren en kruisen in azulejoblauw",
    "v_z8": "Achtpuntige sterren uit rakende achthoeken",
    "v_z12": "Twaalf-, zes- en vierpuntige sterren",
    "v_z10": "Tienpuntige sterren (girih-basis)",
    "v_i6": "Zespuntige sterren uit rakende zeshoeken",
    "v_i_sq": "Achthoeken en vierpuntige sterren uit vierkanten",
    "v_i_31212": "Twaalfpuntige sterren uit 3.12.12",
    "v_i_4612": "Rozetten uit 4.6.12",
    "v_i_3464": "Sterren uit 3.4.6.4",
    "v_i_snub": "Sterren uit de afgeschuinde vierkantsbetegeling",
    "app_title": "Betegelingen en mozaïeken", "app_tiling": "Betegeling", "app_scheme": "Schema",
    "app_hue": "Basistoon", "app_size": "Breedte", "app_save": "Opslaan…",
    "app_saved": "Opgeslagen: %s", "app_drawing": "Tekenen…",
    "app_error": "Deze combinatie kan niet getekend worden: %s", "app_panels": "panelen",
    "app_params": "Parameters", "app_params_hint": "naam=waarde, gescheiden door spaties; Enter past toe",
})

# ---------------------------------------------------------------------- PL
STRINGS["pl"].update({
    "title": "PARKIETAŻE I MOZAIKI",
    "subtitle": "Parkietaże foremne, półforemne, aperiodyczne i islamskie, pokolorowane według teorii koloru",
    "intro": "Parkietaż pokrywa płaszczyznę kształtami, bez luk i nakładania się. Ten sam parkietaż "
             "zmienia charakter wraz z kolorowaniem: według rodzaju płytki, orientacji, odbicia "
             "lustrzanego lub tak, by sąsiednie płytki zawsze się różniły. Każda strona rysuje "
             "parkietaże z jednego artykułu Wikipedii w kilku kolorowaniach; kolory pochodzą ze "
             "schematów koła RYB lub z tradycyjnych palet płytek. Wszystko jest obliczane: siatki "
             "wielokątów, parkietaże dualne, deflacja Penrose'a, metapłytki kapelusza, wyszukiwanie "
             "parkietaży Wanga i metoda Hankina dla wzorów gwiaździstych.",
    "schemes_t": "Schematy kolorów",
    "schemes_d": "Schematy RYB biorą barwy w stałych krokach 12-barwnego koła, zaczynając od barwy "
                 "bazowej (tu czerwieni); gdy parkietaż potrzebuje więcej kolorów, niż ma schemat, "
                 "dodaje się jaśniejsze i ciemniejsze odmiany tych samych barw. Nazwane palety "
                 "naśladują tradycyjne płytki szkliwione.",
    "contents": "Spis treści", "colouring": "Kolorowanie", "cont": "ciąg dalszy", "page": "strona",
    "c_single": "jeden kolor", "c_kind": "według rodzaju płytki", "c_shape": "według kształtu",
    "c_chirality": "według odbicia lustrzanego", "c_orientation": "według orientacji",
    "c_proper": "sąsiedzi różni", "c_random": "losowo", "c_rings": "pierścienie od środka",
    "c_classic": "cztery kolory krawędzi", "c_scheme": "kolory krawędzi ze schematu",
    "c_checker": "szachownica", "c_gradient": "gradient po przekątnej",
    "f_triangular": "Parkietaż trójkątny",
    "f_triangular_d": "W każdym wierzchołku spotyka się sześć trójkątów równobocznych. Jego jednorodne "
                      "kolorowania nazywa się według kolorów wokół wierzchołka: 121212 przeplata dwa "
                      "kolory, 121314 wymaga czterech. Dalszy podział trójkątów daje parkietaże "
                      "kisrhombille i kisdeltile.",
    "f_truncated_square": "Ścięty parkietaż kwadratowy",
    "f_truncated_square_d": "Kwadrat i dwa ośmiokąty foremne w każdym wierzchołku (4.8.8), podłoga "
                            "wielu kuchni. Kwadraty mogą mieć dwa rozmiary, a w granicy połowa z nich "
                            "znika (parkietaż sfazowany). Jego dualem jest parkietaż tetrakis "
                            "kwadratowy.",
    "f_hexagonal": "Parkietaż sześciokątny",
    "f_hexagonal_d": "Trzy sześciokąty w każdym wierzchołku, jak w plastrze miodu. Sześciokąty można "
                     "regularnie pokolorować 2, 3, 4 lub 7 kolorami; przy 7 każdy sześciokąt dotyka "
                     "wszystkich innych kolorów. Podział części sześciokątów na trójkąty daje "
                     "parkietaże 2-jednorodne.",
    "f_trihexagonal": "Parkietaż trójsześciokątny",
    "f_trihexagonal_d": "Trójkąty i sześciokąty przeplatają się wokół każdego wierzchołka (3.6.3.6); "
                        "krawędzie tworzą trzy rodziny prostych, wzór kagome japońskich koszy. Obrót "
                        "lub zmiana wielkości trójkątów zachowuje strukturę.",
    "f_rhombille": "Parkietaż rombowy",
    "f_rhombille_d": "Jednakowe romby 60°, trzy wokół jednego narożnika i sześć wokół drugiego: dual "
                     "parkietażu trójsześciokątnego. Z trzema jasnościami jednej barwy wygląda jak stos "
                     "sześcianów, wzór dawnych posadzek, np. w katedrze w Sienie.",
    "f_pythagorean": "Parkietaż pitagorejski",
    "f_pythagorean_d": "Kwadraty dwóch rozmiarów, każdy styka się z czterema kwadratami drugiego "
                       "rozmiaru. To rysunek do klasycznego dowodu twierdzenia Pitagorasa i częsty "
                       "wzór posadzek.",
    "f_regular": "Wielokąty foremne",
    "f_regular_d": "Jedenaście parkietaży jednorodnych (archimedesowych) z wielokątów foremnych: każdy "
                   "wierzchołek ma wokół te same wielokąty, zapisane liczbą boków (3.4.6.4 to trójkąt, "
                   "kwadrat, sześciokąt, kwadrat). Mieszanie typów wierzchołków daje parkietaże "
                   "k-jednorodne.",
    "f_penrose": "Parkietaże Penrose'a",
    "f_penrose_d": "Dwie płytki, które pokrywają płaszczyznę tylko bez powtórzeń: grube i cienkie romby "
                   "(P3) lub latawce i strzałki (P2). Rysuje się je, wielokrotnie dzieląc złote trójkąty "
                   "(deflacja); wszędzie widać symetrię piątego rzędu.",
    "f_aperiodic": "Parkietaże aperiodyczne",
    "f_aperiodic_d": "Parkietaże, które nigdy się nie powtarzają. Kapelusz (2023) to jeden kształt, "
                     "używany z lustrzanym odbiciem, który parkietuje tylko aperiodycznie; sześć "
                     "kwadratowych płytek Robinsona wymusza zagnieżdżone, coraz większe kwadraty.",
    "f_herringbone": "Jodełka",
    "f_herringbone_d": "Prostokąty układane schodkowo, każdy prostopadle do sąsiadów: klasyczny wzór "
                       "cegieł i parkietu. Dłuższe cegły, obrót o 45° lub równoległoboki zmieniają jego "
                       "wygląd; wątek koszykowy łączy cegły w pary.",
    "f_pentagonal": "Parkietaże pięciokątne",
    "f_pentagonal_d": "Pięciokąty foremne nie parkietują płaszczyzny, ale 15 rodzin pięciokątów "
                      "wypukłych tak. Połówki sześciokątów dają typ 1; duale trzech parkietaży "
                      "jednorodnych dają parkietaże pięciokątne kairski, pryzmatyczny i kwiatowy.",
    "f_cairo": "Kairski parkietaż pięciokątny",
    "f_cairo_d": "Pięciokąty o czterech długich bokach i jednym krótkim, dual parkietażu kwadratowego "
                 "przyciętego, nazwany od ulic Kairu. W niektórych wierzchołkach spotykają się cztery "
                 "pięciokąty, w innych trzy, a pary pięciokątów tworzą sześciokąty.",
    "f_girih": "Płytki girih",
    "f_girih_d": "Pięć płytek o równych bokach (dziesięciokąt, pięciokąt, sześciokąt, muszka, romb) z "
                 "architektury perskiej. Linie na nich przecinają każdą krawędź w połowie pod kątem 54°, "
                 "więc łączą się między płytkami w widoczny wzór gwiazd.",
    "f_wang": "Płytki Wanga",
    "f_wang_d": "Kwadraty o kolorowych krawędziach, układane tak, by stykające się krawędzie pasowały, "
                "bez obracania. 11 płytek Jeandela i Rao (2015) parkietuje płaszczyznę tylko "
                "aperiodycznie; ten fragment znaleziono przeszukiwaniem z nawrotami.",
    "f_zellij": "Zellige",
    "f_zellij_d": "Marokańska i andaluzyjska mozaika z ręcznie ciętych szkliwionych kawałków w bieli, "
                  "zieleni, czerni, ochrze i błękitach. Typowe są ośmioramienne gwiazdy z krzyżami oraz "
                  "układy gwiazd 6-, 8-, 10- i 12-ramiennych.",
    "f_islamic": "Islamskie wzory geometryczne",
    "f_islamic_d": "Wzory gwiaździste tworzone metodą Hankina stykających się wielokątów: ze środka "
                   "każdej krawędzi parkietażu wychodzą dwie linie pod stałym kątem, aż się spotkają. "
                   "Parkietaż bazowy i kąt decydują o gwiazdach; plecionki rysuje się jak wstęgi.",
    "v_uniform": "Kolorowanie jednorodne %s",
    "v_tri_regular": "Foremny parkietaż trójkątny {3,6}",
    "v_kisrhombille": "Kisrhombille: trójkąty 30-60-90 (dual 4.6.12)",
    "v_triakis": "Kisdeltile: trójkąty 30-30-120 (dual 3.12.12)",
    "v_ts_plain": "Ścięty parkietaż kwadratowy 4.8.8",
    "v_circlepack": "Upakowanie kół: koło w każdym wierzchołku",
    "v_ts_alt": "Kwadraty na przemian dwóch rozmiarów",
    "v_ts_chamfer": "Sfazowany parkietaż kwadratowy (małe kwadraty znikają)",
    "v_tetrakis": "Parkietaż tetrakis kwadratowy (dual 4.8.8)",
    "v_dual_overlay": "Z dualem narysowanym na wierzchu",
    "v_hex_regular": "Foremny parkietaż sześciokątny {6,3}",
    "v_hex_2": "Dwa kolory, rzędami",
    "v_hex_21": "Dwa kolory, co trzeci sześciokąt",
    "v_hex_3": "Trzy kolory: sąsiedzi zawsze różni",
    "v_hex_4": "Cztery kolory",
    "v_hex_7": "Siedem kolorów: każdy sześciokąt dotyka wszystkich innych",
    "v_kissing": "Najgęstsze upakowanie kół",
    "v_dissect1": "2-jednorodny: jedna trzecia sześciokątów podzielona na trójkąty",
    "v_dissect2": "2-jednorodny: dwie trzecie sześciokątów podzielone na trójkąty",
    "v_kagome": "Kagome: krawędzie według kierunku",
    "v_unequal": "Trójkąty dwóch rozmiarów",
    "v_twisted": "Obrócone trójkąty: sześciokąty stają się gwiazdami",
    "v_twisted2": "Obrócone dalej",
    "v_hexstar": "Sześciokąty i sześcioramienne gwiazdy",
    "v_rhombille": "Parkietaż rombowy: romby 60°",
    "v_siena": "Trzy odcienie według orientacji, jak w katedrze w Sienie",
    "v_cubes": "Ułożone sześciany: jedna barwa w trzech jasnościach",
    "v_rh_dual": "Na swoim dualu, parkietażu trójsześciokątnym",
    "v_skew": "Pochylony i obrócony: równoległoboki",
    "v_pyth_half": "Kwadraty o bokach 1 i 1/2",
    "v_pyth_golden": "Boki w złotej proporcji",
    "v_pyth_random": "Boki 1 i 0,3, losowe barwy ziemi",
    "n_triangular": "3.3.3.3.3.3 trójkątny",
    "n_square": "4.4.4.4 kwadratowy",
    "n_hexagonal": "6.6.6 sześciokątny",
    "n_trihexagonal": "3.6.3.6 trójsześciokątny",
    "n_truncated_hexagonal": "3.12.12 ścięty sześciokątny",
    "n_truncated_square": "4.8.8 ścięty kwadratowy",
    "n_truncated_trihexagonal": "4.6.12 ścięty trójsześciokątny",
    "n_rhombitrihexagonal": "3.4.6.4 rombotrójsześciokątny",
    "n_snub_hexagonal": "3.3.3.3.6 przycięty sześciokątny",
    "n_elongated_triangular": "3.3.3.4.4 wydłużony trójkątny",
    "n_snub_square": "3.3.4.3.4 przycięty kwadratowy",
    "v_p3": "P3: grube i cienkie romby",
    "v_p3_ori": "P3 według dziesięciu orientacji rombów",
    "v_p3_proper": "P3, sąsiednie romby różne",
    "v_p3_rings": "P3 w pierścieniach wokół środka",
    "v_p2": "P2: latawce i strzałki",
    "v_p2_rings": "P2 w pierścieniach wokół środka",
    "v_p2_proper": "P2, sąsiednie płytki różne",
    "v_hat": "Kapelusz: jeden kształt i jego lustrzane odbicie",
    "v_hat_ori": "Kapelusze według orientacji",
    "v_robinson": "Płytki Robinsona: ich znaki rysują zagnieżdżone kwadraty",
    "v_hb_2": "Cegły 2:1",
    "v_hb_45": "Obrócone o 45°",
    "v_hb_3": "Cegły 3:1",
    "v_hb_long": "Długie deski, ok. 6,6:1",
    "v_hb_par": "Równoległoboki",
    "v_basket": "Wątek koszykowy",
    "v_halves": "Typ 1: sześciokąty przecięte na pół",
    "v_halves_alt": "Typ 1, cięty w trzech kierunkach",
    "v_cairo_p": "Parkietaż kairski (typy 2 i 4)",
    "v_prismatic": "Pięciokątny pryzmatyczny (dual 3.3.3.4.4)",
    "v_floret": "Pięciokątny kwiatowy (dual 3.3.3.3.6)",
    "v_floret_proper": "Kwiatowy, sąsiedzi różni",
    "v_cairo": "Parkietaż kairski: dual parkietażu kwadratowego przyciętego",
    "v_cairo_ori": "Cztery orientacje",
    "v_cairo_proper": "Sąsiednie pięciokąty różne",
    "v_cairo_dual": "Na swoim dualu, parkietażu kwadratowym przyciętym",
    "v_girih_tiles": "Dziesięciokąty i muszki",
    "v_girih_lines": "Linie girih przecinające każdą krawędź pod kątem 54°",
    "v_girih_star": "Wzór girih, pokolorowany",
    "v_girih_star2": "Ten sam wzór, paleta zellige",
    "v_wang": "Jeandel–Rao: 11 płytek, 4 kolory, aperiodyczny",
    "v_wang_scheme": "Te same płytki, kolory ze schematu",
    "v_stars_crosses": "Ośmioramienne gwiazdy i krzyże",
    "v_sc_azulejo": "Gwiazdy i krzyże w błękitach azulejo",
    "v_z8": "Ośmioramienne gwiazdy ze stykających się ośmiokątów",
    "v_z12": "Gwiazdy dwunasto-, sześcio- i czteroramienne",
    "v_z10": "Dziesięcioramienne gwiazdy (podstawa girih)",
    "v_i6": "Sześcioramienne gwiazdy ze stykających się sześciokątów",
    "v_i_sq": "Ośmiokąty i czteroramienne gwiazdy z kwadratów",
    "v_i_31212": "Dwunastoramienne gwiazdy z 3.12.12",
    "v_i_4612": "Rozety z 4.6.12",
    "v_i_3464": "Gwiazdy z 3.4.6.4",
    "v_i_snub": "Gwiazdy z parkietażu kwadratowego przyciętego",
    "app_title": "Parkietaże i mozaiki", "app_tiling": "Parkietaż", "app_scheme": "Schemat",
    "app_hue": "Barwa bazowa", "app_size": "Szerokość", "app_save": "Zapisz…",
    "app_saved": "Zapisano: %s", "app_drawing": "Rysowanie…",
    "app_error": "Nie można narysować tej kombinacji: %s", "app_panels": "panele",
    "app_params": "Parametry", "app_params_hint": "nazwa=wartość, oddzielone spacjami; Enter stosuje",
})

# ---------------------------------------------------------------------- TR
STRINGS["tr"].update({
    "title": "DÖŞEMELER VE MOZAİKLER",
    "subtitle": "Düzgün, yarı düzgün, periyodik olmayan ve İslami döşemeler, renk kuramıyla renklendirilmiş",
    "intro": "Bir döşeme düzlemi boşluk ve örtüşme olmadan şekillerle kaplar. Aynı döşeme "
             "renklendirmeyle karakter değiştirir: parça türüne, yöne, ayna görüntüsüne göre ya da komşu "
             "parçalar hep farklı olacak şekilde. Her sayfa bir Vikipedi maddesinin döşemelerini birkaç "
             "renklendirmeyle çizer; renkler RYB çemberinin renk şemalarından ya da geleneksel çini "
             "paletlerinden gelir. Hepsi hesaplanır: çokgen ızgaraları, dualler, Penrose deflasyonu, "
             "şapkanın üst parçaları, Wang döşemeleri için bir arama ve yıldız desenleri için Hankin "
             "yöntemi.",
    "schemes_t": "Renk şemaları",
    "schemes_d": "RYB şemaları, 12 renkli çemberde bir temel renkten (burada kırmızı) sabit adımlarla "
                 "renk tonları alır; bir döşeme şemadakinden fazla renk isterse aynı tonların açık ve "
                 "koyu hâlleri eklenir. Adlı paletler geleneksel sırlı çinileri izler.",
    "contents": "İçindekiler", "colouring": "Renklendirme", "cont": "devam", "page": "sayfa",
    "c_single": "tek renk", "c_kind": "parça türüne göre", "c_shape": "şekle göre",
    "c_chirality": "ayna görüntüsüne göre", "c_orientation": "yöne göre",
    "c_proper": "komşular farklı", "c_random": "rastgele", "c_rings": "merkezden halkalar",
    "c_classic": "dört kenar rengi", "c_scheme": "şemadan kenar renkleri",
    "c_checker": "dama", "c_gradient": "çapraz geçiş",
    "f_triangular": "Üçgen döşeme",
    "f_triangular_d": "Her köşede altı eşkenar üçgen buluşur. Düzgün renklendirmeleri bir köşe "
                      "etrafındaki renklere göre adlandırılır: 121212 iki rengi dönüşümlü kullanır, "
                      "121314 dört renk ister. Üçgenleri daha da bölmek kisrhombille ve kisdeltile "
                      "döşemelerini verir.",
    "f_truncated_square": "Kesik kare döşeme",
    "f_truncated_square_d": "Her köşede bir kare ve iki düzgün sekizgen (4.8.8), pek çok mutfağın "
                            "zemini. Kareler iki boyutta olabilir; uç durumda yarısı kaybolur (pahlı "
                            "döşeme). Duali tetrakis kare döşemedir.",
    "f_hexagonal": "Altıgen döşeme",
    "f_hexagonal_d": "Her köşede üç altıgen, bir bal peteğindeki gibi. Altıgenler 2, 3, 4 ya da 7 "
                     "renkle düzenli biçimde renklendirilebilir; 7 renkte her altıgen diğer tüm renklere "
                     "dokunur. Bazı altıgenleri üçgenlere bölmek 2-düzgün döşemeler verir.",
    "f_trihexagonal": "Üçlü altıgen döşeme",
    "f_trihexagonal_d": "Her köşede üçgenler ve altıgenler sırayla gelir (3.6.3.6); kenarlar üç doğru "
                        "ailesi oluşturur, Japon sepetlerinin kagome deseni. Üçgenleri döndürmek ya da "
                        "boyutlandırmak yapıyı korur.",
    "f_rhombille": "Eşkenar dörtgen döşeme",
    "f_rhombille_d": "Eş 60° eşkenar dörtgenler, bir köşede üç, diğerinde altı tane: üçlü altıgen "
                     "döşemenin duali. Bir rengin üç değeriyle üst üste küpler gibi görünür; Siena "
                     "Katedrali gibi eski zeminlerde bulunan bir desen.",
    "f_pythagorean": "Pisagor döşemesi",
    "f_pythagorean_d": "İki boyutta kareler, her biri diğer boyuttaki dört kareye dokunur. Pisagor "
                       "teoreminin klasik bir kanıtının resmi ve yaygın bir zemin desenidir.",
    "f_regular": "Düzgün çokgenler",
    "f_regular_d": "Düzgün çokgenlerle yapılan on bir düzgün (Arşimet) döşeme: her köşenin etrafında "
                   "aynı çokgenler vardır, kenar sayılarıyla yazılır (3.4.6.4: üçgen, kare, altıgen, "
                   "kare). Köşe türlerini karıştırmak k-düzgün döşemeler verir.",
    "f_penrose": "Penrose döşemeleri",
    "f_penrose_d": "Düzlemi yalnızca tekrar etmeden kaplayan iki parça: kalın ve ince eşkenar "
                   "dörtgenler (P3) ya da uçurtmalar ve oklar (P2). Altın üçgenler tekrar tekrar "
                   "bölünerek (deflasyon) çizilirler ve her yerde beşli simetri gösterirler.",
    "f_aperiodic": "Periyodik olmayan döşemeler",
    "f_aperiodic_d": "Hiç tekrar etmeyen döşemeler. Şapka (2023), ayna görüntüsüyle birlikte "
                     "kullanılan ve yalnızca periyodik olmayan biçimde döşeyen tek bir şekildir; "
                     "Robinson'un altı kare parçası giderek büyüyen iç içe kareleri zorunlu kılar.",
    "f_herringbone": "Balıksırtı deseni",
    "f_herringbone_d": "Merdiven gibi dizilmiş dikdörtgenler, her biri komşularına dik açıda: klasik "
                       "tuğla ve parke deseni. Daha uzun tuğlalar, 45° döndürme ya da paralelkenarlar "
                       "görünümü değiştirir; sepet örgüsü tuğlaları çiftler hâlinde dizer.",
    "f_pentagonal": "Beşgen döşemeler",
    "f_pentagonal_d": "Düzgün beşgenler düzlemi döşeyemez, ama 15 dışbükey beşgen ailesi döşer. "
                      "Altıgenleri ikiye bölmek tip 1'i verir; üç düzgün döşemenin dualleri Kahire, "
                      "prizmatik ve çiçek beşgen döşemelerini verir.",
    "f_cairo": "Kahire beşgen döşemesi",
    "f_cairo_d": "Dört uzun ve bir kısa kenarlı beşgenler, kırpık kare döşemenin duali, adını Kahire "
                 "sokaklarından alır. Bazı köşelerde dört beşgen, bazılarında üç beşgen buluşur ve "
                 "beşgen çiftleri altıgenler oluşturur.",
    "f_girih": "Girih parçaları",
    "f_girih_d": "Fars mimarisinde kullanılan, kenarları eşit beş parça (ongen, beşgen, altıgen, papyon, "
                 "eşkenar dörtgen). Üzerlerindeki çizgiler her kenarı ortasından 54° ile keser ve "
                 "böylece parçalar boyunca birleşerek görünen yıldız desenini oluşturur.",
    "f_wang": "Wang karoları",
    "f_wang_d": "Kenarları renkli kareler, değen kenarlar eşleşecek biçimde ve hiç döndürülmeden "
                "dizilir. Jeandel ve Rao'nun (2015) 11 karosu düzlemi yalnızca periyodik olmayan "
                "biçimde döşer; bu parça geri izlemeli bir aramayla bulundu.",
    "f_zellij": "Zellige",
    "f_zellij_d": "Elle kesilmiş sırlı parçalardan beyaz, yeşil, siyah, okr ve mavilerle yapılan Fas ve "
                  "Endülüs mozaiği. Haçlı sekiz köşeli yıldızlar ve 6, 8, 10 ve 12 köşeli yıldız "
                  "sistemleri tipiktir.",
    "f_islamic": "İslami geometrik desenler",
    "f_islamic_d": "Hankin'in temas eden çokgenler yöntemiyle yapılan yıldız desenleri: bir döşemenin "
                   "her kenarının ortasından sabit açıyla iki çizgi çıkar ve buluşana kadar ilerler. "
                   "Temel döşeme ve açı yıldızları belirler; şeritler kurdele gibi çizilir.",
    "v_uniform": "Düzgün renklendirme %s",
    "v_tri_regular": "Düzgün üçgen döşeme {3,6}",
    "v_kisrhombille": "Kisrhombille: 30-60-90 üçgenleri (4.6.12'nin duali)",
    "v_triakis": "Kisdeltile: 30-30-120 üçgenleri (3.12.12'nin duali)",
    "v_ts_plain": "Kesik kare döşeme 4.8.8",
    "v_circlepack": "Daire dizilimi: her köşede bir daire",
    "v_ts_alt": "Dönüşümlü boyutlarda kareler",
    "v_ts_chamfer": "Pahlı kare döşeme (küçük kareler kaybolur)",
    "v_tetrakis": "Tetrakis kare döşeme (4.8.8'in duali)",
    "v_dual_overlay": "Üzerine duali çizilmiş",
    "v_hex_regular": "Düzgün altıgen döşeme {6,3}",
    "v_hex_2": "İki renk, sıralar hâlinde",
    "v_hex_21": "İki renk, üç altıgenden biri",
    "v_hex_3": "Üç renk: komşular hep farklı",
    "v_hex_4": "Dört renk",
    "v_hex_7": "Yedi renk: her altıgen diğer hepsine dokunur",
    "v_kissing": "En sık daire dizilimi",
    "v_dissect1": "2-düzgün: altıgenlerin üçte biri üçgenlere bölünmüş",
    "v_dissect2": "2-düzgün: altıgenlerin üçte ikisi üçgenlere bölünmüş",
    "v_kagome": "Kagome: kenarlar yöne göre renkli",
    "v_unequal": "İki boyutta üçgenler",
    "v_twisted": "Döndürülmüş üçgenler: altıgenler yıldız olur",
    "v_twisted2": "Daha çok döndürülmüş",
    "v_hexstar": "Altıgenler ve altı köşeli yıldızlar",
    "v_rhombille": "Eşkenar dörtgen döşeme: 60° eşkenar dörtgenler",
    "v_siena": "Yöne göre üç ton, Siena Katedrali'ndeki gibi",
    "v_cubes": "Üst üste küpler: bir rengin üç değeri",
    "v_rh_dual": "Duali olan üçlü altıgen döşemenin üzerinde",
    "v_skew": "Eğilmiş ve döndürülmüş: paralelkenarlar",
    "v_pyth_half": "Kenarları 1 ve 1/2 olan kareler",
    "v_pyth_golden": "Kenarlar altın oranda",
    "v_pyth_random": "Kenarlar 1 ve 0,3, rastgele toprak tonları",
    "n_triangular": "3.3.3.3.3.3 üçgen",
    "n_square": "4.4.4.4 kare",
    "n_hexagonal": "6.6.6 altıgen",
    "n_trihexagonal": "3.6.3.6 üçlü altıgen",
    "n_truncated_hexagonal": "3.12.12 kesik altıgen",
    "n_truncated_square": "4.8.8 kesik kare",
    "n_truncated_trihexagonal": "4.6.12 kesik üçlü altıgen",
    "n_rhombitrihexagonal": "3.4.6.4 eşkenar üçlü altıgen",
    "n_snub_hexagonal": "3.3.3.3.6 kırpık altıgen",
    "n_elongated_triangular": "3.3.3.4.4 uzatılmış üçgen",
    "n_snub_square": "3.3.4.3.4 kırpık kare",
    "v_p3": "P3: kalın ve ince eşkenar dörtgenler",
    "v_p3_ori": "Eşkenar dörtgenlerin on yönüne göre P3",
    "v_p3_proper": "P3, komşu eşkenar dörtgenler farklı",
    "v_p3_rings": "Merkez çevresinde halkalar hâlinde P3",
    "v_p2": "P2: uçurtmalar ve oklar",
    "v_p2_rings": "Merkez çevresinde halkalar hâlinde P2",
    "v_p2_proper": "P2, komşu parçalar farklı",
    "v_hat": "Şapka: bir şekil ve ayna görüntüsü",
    "v_hat_ori": "Yöne göre şapkalar",
    "v_robinson": "Robinson karoları: işaretleri iç içe kareler çizer",
    "v_hb_2": "Tuğlalar 2:1",
    "v_hb_45": "45° döndürülmüş",
    "v_hb_3": "Tuğlalar 3:1",
    "v_hb_long": "Uzun tahtalar, yaklaşık 6,6:1",
    "v_hb_par": "Paralelkenarlar",
    "v_basket": "Sepet örgüsü",
    "v_halves": "Tip 1: ikiye bölünmüş altıgenler",
    "v_halves_alt": "Tip 1, üç yönde bölünmüş",
    "v_cairo_p": "Kahire döşemesi (tip 2 ve 4)",
    "v_prismatic": "Prizmatik beşgen (3.3.3.4.4'ün duali)",
    "v_floret": "Çiçek beşgen (3.3.3.3.6'nın duali)",
    "v_floret_proper": "Çiçek beşgen, komşular farklı",
    "v_cairo": "Kahire döşemesi: kırpık kare döşemenin duali",
    "v_cairo_ori": "Dört yön",
    "v_cairo_proper": "Komşu beşgenler farklı",
    "v_cairo_dual": "Duali olan kırpık kare döşemenin üzerinde",
    "v_girih_tiles": "Ongenler ve papyonlar",
    "v_girih_lines": "Her kenarı 54° ile kesen girih çizgileri",
    "v_girih_star": "Girih deseni, renkli",
    "v_girih_star2": "Aynı desen, zellige paleti",
    "v_wang": "Jeandel–Rao: 11 karo, 4 renk, periyodik değil",
    "v_wang_scheme": "Aynı karolar, şemadan renkler",
    "v_stars_crosses": "Sekiz köşeli yıldızlar ve haçlar",
    "v_sc_azulejo": "Azulejo mavilerinde yıldızlar ve haçlar",
    "v_z8": "Temas eden sekizgenlerden sekiz köşeli yıldızlar",
    "v_z12": "On iki, altı ve dört köşeli yıldızlar",
    "v_z10": "On köşeli yıldızlar (girih tabanı)",
    "v_i6": "Temas eden altıgenlerden altı köşeli yıldızlar",
    "v_i_sq": "Karelerden sekizgenler ve dört köşeli yıldızlar",
    "v_i_31212": "3.12.12'den on iki köşeli yıldızlar",
    "v_i_4612": "4.6.12'den rozetler",
    "v_i_3464": "3.4.6.4'ten yıldızlar",
    "v_i_snub": "Kırpık kare döşemeden yıldızlar",
    "app_title": "Döşemeler ve mozaikler", "app_tiling": "Döşeme", "app_scheme": "Şema",
    "app_hue": "Temel renk", "app_size": "Genişlik", "app_save": "Kaydet…",
    "app_saved": "Kaydedildi: %s", "app_drawing": "Çiziliyor…",
    "app_error": "Bu birleşim çizilemiyor: %s", "app_panels": "pano",
    "app_params": "Parametreler", "app_params_hint": "ad=değer, boşlukla ayrılmış; Enter uygular",
})

# ---------------------------------------------------------------------- RU
STRINGS["ru"].update({
    "title": "ПАРКЕТЫ И МОЗАИКИ",
    "subtitle": "Правильные, полуправильные, апериодические и исламские паркеты, раскрашенные по теории цвета",
    "intro": "Паркет покрывает плоскость фигурами без пробелов и наложений. Один и тот же паркет "
             "меняет характер с раскраской: по виду плитки, по ориентации, по зеркальному отражению "
             "или так, чтобы соседние плитки всегда различались. Каждая страница рисует паркеты одной "
             "статьи Википедии в нескольких раскрасках; цвета берутся из цветовых схем круга RYB или из "
             "традиционных палитр плитки. Всё вычисляется: решётки многоугольников, двойственные "
             "паркеты, дефляция Пенроуза, метаплитки «шляпы», поиск паркетов Вана и метод Хэнкина для "
             "звёздных узоров.",
    "schemes_t": "Цветовые схемы",
    "schemes_d": "Схемы RYB берут тона с постоянным шагом на круге из 12 тонов, начиная с базового "
                 "(здесь красного); если паркету нужно больше цветов, чем в схеме, добавляются "
                 "светлые и тёмные варианты тех же тонов. Именованные палитры повторяют традиционную "
                 "глазурованную плитку.",
    "contents": "Содержание", "colouring": "Раскраска", "cont": "продолжение", "page": "страница",
    "c_single": "один цвет", "c_kind": "по виду плитки", "c_shape": "по форме",
    "c_chirality": "по зеркальному отражению", "c_orientation": "по ориентации",
    "c_proper": "соседи различны", "c_random": "случайно", "c_rings": "кольца от центра",
    "c_classic": "четыре цвета рёбер", "c_scheme": "цвета рёбер из схемы",
    "c_checker": "шахматный порядок", "c_gradient": "градиент по диагонали",
    "f_triangular": "Треугольный паркет",
    "f_triangular_d": "В каждой вершине сходятся шесть правильных треугольников. Однородные раскраски "
                      "называют по цветам вокруг вершины: 121212 чередует два цвета, 121314 требует "
                      "четырёх. Дальнейшее деление треугольников даёт паркеты кисромбилль и кисдельтиль.",
    "f_truncated_square": "Усечённый квадратный паркет",
    "f_truncated_square_d": "Квадрат и два правильных восьмиугольника в каждой вершине (4.8.8), пол "
                            "многих кухонь. Квадраты могут быть двух размеров, а в пределе половина "
                            "из них исчезает (скошенный паркет). Двойственный к нему — тетракис-"
                            "квадратный паркет.",
    "f_hexagonal": "Шестиугольный паркет",
    "f_hexagonal_d": "Три шестиугольника в каждой вершине, как в пчелиных сотах. Шестиугольники можно "
                     "правильно раскрасить в 2, 3, 4 или 7 цветов; при 7 каждый шестиугольник касается "
                     "всех остальных цветов. Деление части шестиугольников на треугольники даёт "
                     "2-однородные паркеты.",
    "f_trihexagonal": "Тришестиугольный паркет",
    "f_trihexagonal_d": "Треугольники и шестиугольники чередуются вокруг каждой вершины (3.6.3.6); рёбра "
                        "образуют три семейства прямых — узор кагомэ японских корзин. Поворот или "
                        "изменение размера треугольников сохраняет структуру.",
    "f_rhombille": "Ромбический паркет",
    "f_rhombille_d": "Одинаковые ромбы с углом 60°, три вокруг одного угла и шесть вокруг другого: "
                     "двойственный к тришестиугольному. В трёх светлотах одного тона он выглядит как "
                     "стопка кубов — узор старых полов, например в Сиенском соборе.",
    "f_pythagorean": "Пифагоров паркет",
    "f_pythagorean_d": "Квадраты двух размеров, каждый касается четырёх квадратов другого размера. Это "
                       "чертёж к классическому доказательству теоремы Пифагора и распространённый "
                       "рисунок пола.",
    "f_regular": "Правильные многоугольники",
    "f_regular_d": "Одиннадцать однородных (архимедовых) паркетов из правильных многоугольников: у каждой "
                   "вершины одни и те же многоугольники, записанные числом сторон (3.4.6.4 — "
                   "треугольник, квадрат, шестиугольник, квадрат). Смешение типов вершин даёт "
                   "k-однородные паркеты.",
    "f_penrose": "Паркеты Пенроуза",
    "f_penrose_d": "Две плитки, покрывающие плоскость только без повторений: толстые и тонкие ромбы (P3) "
                   "или «воздушные змеи» и «дротики» (P2). Их рисуют, многократно разрезая золотые "
                   "треугольники (дефляция); всюду видна симметрия пятого порядка.",
    "f_aperiodic": "Апериодические паркеты",
    "f_aperiodic_d": "Паркеты, которые никогда не повторяются. «Шляпа» (2023) — одна фигура, "
                     "используемая вместе с зеркальным отражением, которая укладывается только "
                     "апериодически; шесть квадратных плиток Робинсона создают вложенные квадраты всё "
                     "большего размера.",
    "f_herringbone": "Ёлочка",
    "f_herringbone_d": "Прямоугольники, уложенные лесенкой, каждый под прямым углом к соседям: "
                       "классический рисунок кирпичной кладки и паркета. Более длинные кирпичи, поворот "
                       "на 45° или параллелограммы меняют вид; плетёнка укладывает кирпичи парами.",
    "f_pentagonal": "Пятиугольные паркеты",
    "f_pentagonal_d": "Правильные пятиугольники не покрывают плоскость, а 15 семейств выпуклых "
                      "пятиугольников — покрывают. Половинки шестиугольников дают тип 1; двойственные к "
                      "трём однородным паркетам — каирский, призматический и цветочный пятиугольные "
                      "паркеты.",
    "f_cairo": "Каирский пятиугольный паркет",
    "f_cairo_d": "Пятиугольники с четырьмя длинными сторонами и одной короткой, двойственный к "
                 "плосконосому квадратному паркету, названный по улицам Каира. В одних вершинах сходятся "
                 "четыре пятиугольника, в других три, а пары пятиугольников образуют шестиугольники.",
    "f_girih": "Плитки гирих",
    "f_girih_d": "Пять равносторонних плиток (десятиугольник, пятиугольник, шестиугольник, «бабочка», "
                 "ромб) персидской архитектуры. Линии на них пересекают каждое ребро в середине под "
                 "углом 54° и соединяются от плитки к плитке в видимый звёздный узор.",
    "f_wang": "Плитки Вана",
    "f_wang_d": "Квадраты с цветными рёбрами, уложенные так, чтобы соприкасающиеся рёбра совпадали, и "
                "никогда не поворачиваемые. 11 плиток Жанделя и Рао (2015) покрывают плоскость только "
                "апериодически; этот фрагмент найден поиском с возвратом.",
    "f_zellij": "Зеллидж",
    "f_zellij_d": "Марокканская и андалусская мозаика из вырезанных вручную глазурованных кусочков: "
                  "белых, зелёных, чёрных, охристых и синих. Типичны восьмиконечные звёзды с крестами и "
                  "системы звёзд с 6, 8, 10 и 12 лучами.",
    "f_islamic": "Исламские геометрические узоры",
    "f_islamic_d": "Звёздные узоры по методу Хэнкина соприкасающихся многоугольников: из середины "
                   "каждого ребра паркета выходят две линии под постоянным углом, пока не встретятся. "
                   "Базовый паркет и угол определяют звёзды; плетение рисуется лентами.",
    "v_uniform": "Однородная раскраска %s",
    "v_tri_regular": "Правильный треугольный паркет {3,6}",
    "v_kisrhombille": "Кисромбилль: треугольники 30-60-90 (двойственный к 4.6.12)",
    "v_triakis": "Кисдельтиль: треугольники 30-30-120 (двойственный к 3.12.12)",
    "v_ts_plain": "Усечённый квадратный паркет 4.8.8",
    "v_circlepack": "Упаковка кругов: круг в каждой вершине",
    "v_ts_alt": "Квадраты чередующихся размеров",
    "v_ts_chamfer": "Скошенный квадратный паркет (малые квадраты исчезают)",
    "v_tetrakis": "Тетракис-квадратный паркет (двойственный к 4.8.8)",
    "v_dual_overlay": "С двойственным поверх",
    "v_hex_regular": "Правильный шестиугольный паркет {6,3}",
    "v_hex_2": "Два цвета, рядами",
    "v_hex_21": "Два цвета, каждый третий шестиугольник",
    "v_hex_3": "Три цвета: соседи всегда различны",
    "v_hex_4": "Четыре цвета",
    "v_hex_7": "Семь цветов: каждый шестиугольник касается всех остальных",
    "v_kissing": "Плотнейшая упаковка кругов",
    "v_dissect1": "2-однородный: треть шестиугольников разрезана на треугольники",
    "v_dissect2": "2-однородный: две трети шестиугольников разрезаны на треугольники",
    "v_kagome": "Кагомэ: рёбра окрашены по направлению",
    "v_unequal": "Треугольники двух размеров",
    "v_twisted": "Повёрнутые треугольники: шестиугольники становятся звёздами",
    "v_twisted2": "Повёрнуты сильнее",
    "v_hexstar": "Шестиугольники и шестиконечные звёзды",
    "v_rhombille": "Ромбический паркет: ромбы 60°",
    "v_siena": "Три тона по ориентации, как в Сиенском соборе",
    "v_cubes": "Стопка кубов: один тон в трёх светлотах",
    "v_rh_dual": "Поверх двойственного, тришестиугольного паркета",
    "v_skew": "Скошен и повёрнут: параллелограммы",
    "v_pyth_half": "Квадраты со сторонами 1 и 1/2",
    "v_pyth_golden": "Стороны в золотом сечении",
    "v_pyth_random": "Стороны 1 и 0,3, случайные земляные тона",
    "n_triangular": "3.3.3.3.3.3 треугольный",
    "n_square": "4.4.4.4 квадратный",
    "n_hexagonal": "6.6.6 шестиугольный",
    "n_trihexagonal": "3.6.3.6 тришестиугольный",
    "n_truncated_hexagonal": "3.12.12 усечённый шестиугольный",
    "n_truncated_square": "4.8.8 усечённый квадратный",
    "n_truncated_trihexagonal": "4.6.12 усечённый тришестиугольный",
    "n_rhombitrihexagonal": "3.4.6.4 ромботришестиугольный",
    "n_snub_hexagonal": "3.3.3.3.6 плосконосый шестиугольный",
    "n_elongated_triangular": "3.3.3.4.4 удлинённый треугольный",
    "n_snub_square": "3.3.4.3.4 плосконосый квадратный",
    "v_p3": "P3: толстые и тонкие ромбы",
    "v_p3_ori": "P3 по десяти ориентациям ромбов",
    "v_p3_proper": "P3, соседние ромбы различны",
    "v_p3_rings": "P3 кольцами вокруг центра",
    "v_p2": "P2: «змеи» и «дротики»",
    "v_p2_rings": "P2 кольцами вокруг центра",
    "v_p2_proper": "P2, соседние плитки различны",
    "v_hat": "«Шляпа»: одна фигура и её зеркальное отражение",
    "v_hat_ori": "«Шляпы» по ориентации",
    "v_robinson": "Плитки Робинсона: их метки рисуют вложенные квадраты",
    "v_hb_2": "Кирпичи 2:1",
    "v_hb_45": "Повёрнуто на 45°",
    "v_hb_3": "Кирпичи 3:1",
    "v_hb_long": "Длинные доски, около 6,6:1",
    "v_hb_par": "Параллелограммы",
    "v_basket": "Плетёнка",
    "v_halves": "Тип 1: шестиугольники, разрезанные пополам",
    "v_halves_alt": "Тип 1, разрезанный в трёх направлениях",
    "v_cairo_p": "Каирский паркет (типы 2 и 4)",
    "v_prismatic": "Призматический пятиугольный (двойственный к 3.3.3.4.4)",
    "v_floret": "Цветочный пятиугольный (двойственный к 3.3.3.3.6)",
    "v_floret_proper": "Цветочный, соседи различны",
    "v_cairo": "Каирский паркет: двойственный к плосконосому квадратному",
    "v_cairo_ori": "Четыре ориентации",
    "v_cairo_proper": "Соседние пятиугольники различны",
    "v_cairo_dual": "Поверх двойственного, плосконосого квадратного паркета",
    "v_girih_tiles": "Десятиугольники и «бабочки»",
    "v_girih_lines": "Линии гирих, пересекающие каждое ребро под углом 54°",
    "v_girih_star": "Узор гирих в цвете",
    "v_girih_star2": "Тот же узор, палитра зеллидж",
    "v_wang": "Жандель–Рао: 11 плиток, 4 цвета, апериодический",
    "v_wang_scheme": "Те же плитки, цвета из схемы",
    "v_stars_crosses": "Восьмиконечные звёзды и кресты",
    "v_sc_azulejo": "Звёзды и кресты в синих тонах азулежу",
    "v_z8": "Восьмиконечные звёзды из соприкасающихся восьмиугольников",
    "v_z12": "Двенадцати-, шести- и четырёхконечные звёзды",
    "v_z10": "Десятиконечные звёзды (основа гирих)",
    "v_i6": "Шестиконечные звёзды из соприкасающихся шестиугольников",
    "v_i_sq": "Восьмиугольники и четырёхконечные звёзды из квадратов",
    "v_i_31212": "Двенадцатиконечные звёзды из 3.12.12",
    "v_i_4612": "Розетки из 4.6.12",
    "v_i_3464": "Звёзды из 3.4.6.4",
    "v_i_snub": "Звёзды из плосконосого квадратного паркета",
    "app_title": "Паркеты и мозаики", "app_tiling": "Паркет", "app_scheme": "Схема",
    "app_hue": "Базовый тон", "app_size": "Ширина", "app_save": "Сохранить…",
    "app_saved": "Сохранено: %s", "app_drawing": "Рисуем…",
    "app_error": "Не удаётся нарисовать это сочетание: %s", "app_panels": "панелей",
    "app_params": "Параметры", "app_params_hint": "имя=значение через пробел; Enter применяет",
})

# ---------------------------------------------------------------------- ZH
STRINGS["zh"].update({
    "title": "镶嵌与马赛克",
    "subtitle": "正则、半正则、非周期与伊斯兰镶嵌图案，按色彩理论着色",
    "intro": "镶嵌用图形铺满平面，既无空隙也不重叠。同一种镶嵌会随着色方式改变面貌：按图块种类、按方向、按镜像，或让相邻图块总是不同。每页绘制一篇维基百科条目中的镶嵌，并给出几种着色；颜色来自 RYB 色轮的配色方案或传统瓷砖调色板。一切都由计算得出：多边形晶格、对偶镶嵌、彭罗斯的收缩剖分、“帽子”的元图块、王氏镶嵌的搜索，以及汉金的星形图案方法。",
    "schemes_t": "配色方案",
    "schemes_d": "RYB 配色方案从一个基础色相（这里是红色）出发，在 12 色相环上按固定间隔取色；当镶嵌需要的颜色多于方案所含，就加入同一色相的明色和暗色。带名称的调色板仿照传统釉面瓷砖。",
    "contents": "目录", "colouring": "着色", "cont": "续", "page": "第 %d 页",
    "c_single": "单色", "c_kind": "按图块种类", "c_shape": "按形状",
    "c_chirality": "按镜像", "c_orientation": "按方向",
    "c_proper": "相邻不同", "c_random": "随机", "c_rings": "由中心向外成环",
    "c_classic": "四种边色", "c_scheme": "取自方案的边色",
    "c_checker": "棋盘格", "c_gradient": "斜向渐变",
    "f_triangular": "三角形镶嵌",
    "f_triangular_d": "每个顶点处有六个正三角形相交。其均匀着色按顶点周围的颜色命名：121212 交替两色，121314 需要四色。继续分割三角形可得到 kisrhombille 和 kisdeltile 镶嵌。",
    "f_truncated_square": "截角正方形镶嵌",
    "f_truncated_square_d": "每个顶点处有一个正方形和两个正八边形（4.8.8），是许多厨房的地砖。正方形可以有两种大小，极限情况下其中一半消失（倒角镶嵌）。它的对偶是四角化正方形镶嵌。",
    "f_hexagonal": "六边形镶嵌",
    "f_hexagonal_d": "每个顶点处有三个六边形，如同蜂巢。六边形可用 2、3、4 或 7 种颜色规则着色；用 7 色时每个六边形都与其他所有颜色相邻。把部分六边形切成三角形可得到 2-均匀镶嵌。",
    "f_trihexagonal": "三六边形镶嵌",
    "f_trihexagonal_d": "三角形和六边形在每个顶点周围交替出现（3.6.3.6）；其边构成三组直线，即日本竹篮的笼目图案。旋转或缩放三角形，结构保持不变。",
    "f_rhombille": "菱形镶嵌",
    "f_rhombille_d": "相同的 60° 菱形，一端围绕三个，另一端围绕六个：三六边形镶嵌的对偶。用同一色相的三种明度，看起来像一堆立方体，这是锡耶纳大教堂等古老地面上的图案。",
    "f_pythagorean": "毕达哥拉斯镶嵌",
    "f_pythagorean_d": "两种大小的正方形，每个都与四个另一种大小的正方形相接。它是勾股定理一个经典证明的图示，也是常见的地砖图案。",
    "f_regular": "正多边形",
    "f_regular_d": "由正多边形构成的十一种均匀（阿基米德）镶嵌：每个顶点周围的多边形都相同，用边数表示（3.4.6.4 即三角形、正方形、六边形、正方形）。混合不同顶点类型可得到 k-均匀镶嵌。",
    "f_penrose": "彭罗斯镶嵌",
    "f_penrose_d": "两种图块只能以不重复的方式铺满平面：宽菱形和窄菱形（P3），或风筝和飞镖（P2）。它们通过反复切分黄金三角形（收缩剖分）绘制，处处呈现五重对称。",
    "f_aperiodic": "非周期镶嵌",
    "f_aperiodic_d": "永不重复的镶嵌。“帽子”（2023）是单一形状，与其镜像一起使用，只能非周期地铺满平面；罗宾逊的六种方形图块迫使出现越来越大的嵌套正方形。",
    "f_herringbone": "人字形图案",
    "f_herringbone_d": "长方形呈阶梯状铺设，每块都与相邻者成直角：经典的砖块和木地板图案。更长的砖、旋转 45° 或改用平行四边形会改变外观；编篮式铺法则把砖两两成对。",
    "f_pentagonal": "五边形镶嵌",
    "f_pentagonal_d": "正五边形无法铺满平面，但有 15 类凸五边形可以。把六边形对半切开得到第 1 类；三种均匀镶嵌的对偶给出开罗、棱柱和花形五边形镶嵌。",
    "f_cairo": "开罗五边形镶嵌",
    "f_cairo_d": "四条长边、一条短边的五边形，是扭棱正方形镶嵌的对偶，因开罗街道而得名。有些顶点处四个五边形相交，有些处三个，成对的五边形组成六边形。",
    "f_girih": "吉里赫图块",
    "f_girih_d": "波斯建筑中使用的五种等边图块（十边形、五边形、六边形、蝴蝶结、菱形）。图块上的线以 54° 在每条边的中点穿过，因此在图块之间相连，形成可见的星形图案。",
    "f_wang": "王氏砖",
    "f_wang_d": "边缘着色的正方形，摆放时相邻边颜色必须一致，且从不旋转。Jeandel 和 Rao（2015）的 11 块砖只能非周期地铺满平面；这一片段由回溯搜索找到。",
    "f_zellij": "泽利吉",
    "f_zellij_d": "摩洛哥和安达卢西亚的马赛克，由手工切割的釉面碎片组成，颜色有白、绿、黑、赭和各种蓝。典型图案是带十字的八角星，以及 6、8、10、12 角星系统。",
    "f_islamic": "伊斯兰几何图案",
    "f_islamic_d": "用汉金“多边形相接”方法绘制的星形图案：从镶嵌每条边的中点以固定角度引出两条线，直到相遇。基础镶嵌和角度决定星形；编织带画成丝带状。",
    "v_uniform": "均匀着色 %s",
    "v_tri_regular": "正三角形镶嵌 {3,6}",
    "v_kisrhombille": "Kisrhombille：30-60-90 三角形（4.6.12 的对偶）",
    "v_triakis": "Kisdeltile：30-30-120 三角形（3.12.12 的对偶）",
    "v_ts_plain": "截角正方形镶嵌 4.8.8",
    "v_circlepack": "圆堆积：每个顶点一个圆",
    "v_ts_alt": "大小交替的正方形",
    "v_ts_chamfer": "倒角正方形镶嵌（小正方形消失）",
    "v_tetrakis": "四角化正方形镶嵌（4.8.8 的对偶）",
    "v_dual_overlay": "叠加其对偶",
    "v_hex_regular": "正六边形镶嵌 {6,3}",
    "v_hex_2": "两色，成行",
    "v_hex_21": "两色，三个六边形中一个",
    "v_hex_3": "三色：相邻总是不同",
    "v_hex_4": "四色",
    "v_hex_7": "七色：每个六边形与所有其他颜色相邻",
    "v_kissing": "最密圆堆积",
    "v_dissect1": "2-均匀：三分之一的六边形切成三角形",
    "v_dissect2": "2-均匀：三分之二的六边形切成三角形",
    "v_kagome": "笼目：边按方向着色",
    "v_unequal": "两种大小的三角形",
    "v_twisted": "旋转的三角形：六边形变成星形",
    "v_twisted2": "旋转得更多",
    "v_hexstar": "六边形与六角星",
    "v_rhombille": "菱形镶嵌：60° 菱形",
    "v_siena": "按方向三种明度，如锡耶纳大教堂",
    "v_cubes": "堆叠的立方体：一个色相的三种明度",
    "v_rh_dual": "叠在其对偶三六边形镶嵌上",
    "v_skew": "倾斜并旋转：平行四边形",
    "v_pyth_half": "边长 1 和 1/2 的正方形",
    "v_pyth_golden": "边长成黄金比",
    "v_pyth_random": "边长 1 和 0.3，随机大地色",
    "n_triangular": "3.3.3.3.3.3 三角形",
    "n_square": "4.4.4.4 正方形",
    "n_hexagonal": "6.6.6 六边形",
    "n_trihexagonal": "3.6.3.6 三六边形",
    "n_truncated_hexagonal": "3.12.12 截角六边形",
    "n_truncated_square": "4.8.8 截角正方形",
    "n_truncated_trihexagonal": "4.6.12 截角三六边形",
    "n_rhombitrihexagonal": "3.4.6.4 小斜方截半三六边形",
    "n_snub_hexagonal": "3.3.3.3.6 扭棱六边形",
    "n_elongated_triangular": "3.3.3.4.4 延长三角形",
    "n_snub_square": "3.3.4.3.4 扭棱正方形",
    "v_p3": "P3：宽菱形与窄菱形",
    "v_p3_ori": "P3 按菱形的十个方向",
    "v_p3_proper": "P3，相邻菱形不同",
    "v_p3_rings": "P3 绕中心成环",
    "v_p2": "P2：风筝与飞镖",
    "v_p2_rings": "P2 绕中心成环",
    "v_p2_proper": "P2，相邻图块不同",
    "v_hat": "“帽子”：一种形状及其镜像",
    "v_hat_ori": "按方向着色的“帽子”",
    "v_robinson": "罗宾逊砖：标记画出嵌套的正方形",
    "v_hb_2": "砖 2:1",
    "v_hb_45": "旋转 45°",
    "v_hb_3": "砖 3:1",
    "v_hb_long": "长木板，约 6.6:1",
    "v_hb_par": "平行四边形",
    "v_basket": "编篮式",
    "v_halves": "第 1 类：对半切开的六边形",
    "v_halves_alt": "第 1 类，沿三个方向切开",
    "v_cairo_p": "开罗镶嵌（第 2 类和第 4 类）",
    "v_prismatic": "棱柱五边形（3.3.3.4.4 的对偶）",
    "v_floret": "花形五边形（3.3.3.3.6 的对偶）",
    "v_floret_proper": "花形五边形，相邻不同",
    "v_cairo": "开罗镶嵌：扭棱正方形镶嵌的对偶",
    "v_cairo_ori": "四个方向",
    "v_cairo_proper": "相邻五边形不同",
    "v_cairo_dual": "叠在其对偶扭棱正方形镶嵌上",
    "v_girih_tiles": "十边形与蝴蝶结",
    "v_girih_lines": "吉里赫线，以 54° 穿过每条边",
    "v_girih_star": "吉里赫图案，着色",
    "v_girih_star2": "同一图案，泽利吉配色",
    "v_wang": "Jeandel–Rao：11 块砖，4 种颜色，非周期",
    "v_wang_scheme": "同样的砖，颜色取自方案",
    "v_stars_crosses": "八角星与十字",
    "v_sc_azulejo": "葡式瓷砖蓝的星与十字",
    "v_z8": "由相接八边形得到的八角星",
    "v_z12": "十二角、六角和四角星",
    "v_z10": "十角星（吉里赫基础）",
    "v_i6": "由相接六边形得到的六角星",
    "v_i_sq": "由正方形得到的八边形和四角星",
    "v_i_31212": "由 3.12.12 得到的十二角星",
    "v_i_4612": "由 4.6.12 得到的玫瑰花饰",
    "v_i_3464": "由 3.4.6.4 得到的星形",
    "v_i_snub": "由扭棱正方形镶嵌得到的星形",
    "app_title": "镶嵌与马赛克", "app_tiling": "镶嵌", "app_scheme": "配色",
    "app_hue": "基础色相", "app_size": "宽度", "app_save": "保存…", "app_saved": "已保存：%s",
    "app_drawing": "正在绘制…", "app_error": "无法绘制此组合：%s", "app_panels": "格",
    "app_params": "参数", "app_params_hint": "名称=值，用空格分隔；按 Enter 应用",
})

# ---------------------------------------------------------------------- JA
STRINGS["ja"].update({
    "title": "タイリングとモザイク",
    "subtitle": "正則・半正則・非周期・イスラームのタイリングを色彩理論で彩色",
    "intro": "タイリングは、すき間も重なりもなく図形で平面を覆うものです。同じタイリングでも彩色によって印象が変わります：タイルの種類、向き、鏡像によって、あるいは隣り合うタイルが必ず異なるように。各ページはウィキペディアの 1 つの記事のタイリングをいくつかの彩色で描き、色は RYB 色相環の配色か伝統的なタイルのパレットから取っています。すべて計算で作られています：多角形の格子、双対、ペンローズの収縮分割、「ハット」のメタタイル、ワンタイルの探索、星形模様のためのハンキンの方法。",
    "schemes_t": "配色",
    "schemes_d": "RYB 配色は、基準の色相（ここでは赤）から 12 色相環の上で一定の間隔で色相を取ります。タイリングに配色より多くの色が必要なときは、同じ色相の明るい色と暗い色を加えます。名前の付いたパレットは伝統的な釉薬タイルにならっています。",
    "contents": "目次", "colouring": "彩色", "cont": "続き", "page": "%d ページ",
    "c_single": "単色", "c_kind": "タイルの種類別", "c_shape": "形別",
    "c_chirality": "鏡像別", "c_orientation": "向き別",
    "c_proper": "隣は別の色", "c_random": "ランダム", "c_rings": "中心からの輪",
    "c_classic": "4 つの辺の色", "c_scheme": "配色による辺の色",
    "c_checker": "市松模様", "c_gradient": "斜めのグラデーション",
    "f_triangular": "三角形タイリング",
    "f_triangular_d": "各頂点に 6 つの正三角形が集まります。一様な彩色は頂点のまわりの色で名付けられ、121212 は 2 色を交互に、121314 は 4 色を使います。三角形をさらに分割すると kisrhombille や kisdeltile のタイリングになります。",
    "f_truncated_square": "切頂正方形タイリング",
    "f_truncated_square_d": "各頂点に正方形 1 つと正八角形 2 つ（4.8.8）。多くの台所の床に見られます。正方形は 2 つの大きさにでき、極限では半分が消えます（面取りタイリング）。双対は四方正方形タイリングです。",
    "f_hexagonal": "六角形タイリング",
    "f_hexagonal_d": "蜂の巣のように各頂点に 3 つの六角形。六角形は 2、3、4、7 色で規則的に彩色でき、7 色では各六角形がほかのすべての色に接します。一部の六角形を三角形に分けると 2-一様タイリングになります。",
    "f_trihexagonal": "三六角形タイリング",
    "f_trihexagonal_d": "各頂点のまわりで三角形と六角形が交互に並びます（3.6.3.6）。辺は 3 方向の直線群をなし、日本のかごの籠目模様になります。三角形を回したり大きさを変えても構造は変わりません。",
    "f_rhombille": "菱形タイリング",
    "f_rhombille_d": "同じ 60° の菱形が、一方の角に 3 つ、もう一方に 6 つ集まります。三六角形タイリングの双対です。1 つの色相の 3 段階の明度で塗ると積み重ねた立方体に見え、シエナ大聖堂などの古い床に見られる模様です。",
    "f_pythagorean": "ピタゴラスのタイリング",
    "f_pythagorean_d": "2 つの大きさの正方形で、それぞれがもう一方の大きさの正方形 4 つに接します。ピタゴラスの定理の古典的な証明の図であり、よくある床の模様です。",
    "f_regular": "正多角形",
    "f_regular_d": "正多角形による 11 の一様（アルキメデス）タイリング：どの頂点のまわりにも同じ多角形が並び、辺の数で表します（3.4.6.4 は三角形、正方形、六角形、正方形）。頂点の種類を混ぜると k-一様タイリングになります。",
    "f_penrose": "ペンローズ・タイリング",
    "f_penrose_d": "繰り返さないかぎり平面を覆えない 2 種類のタイル：太い菱形と細い菱形（P3）、または凧と矢（P2）。黄金三角形を繰り返し分割（収縮分割）して描かれ、いたるところに 5 回対称が現れます。",
    "f_aperiodic": "非周期タイリング",
    "f_aperiodic_d": "決して繰り返さないタイリング。「ハット」（2023）は鏡像とともに使う 1 つの形で、非周期的にしか平面を覆えません。ロビンソンの 6 枚の正方形タイルは、しだいに大きくなる入れ子の正方形を生じます。",
    "f_herringbone": "ヘリンボーン",
    "f_herringbone_d": "長方形を階段状に並べ、それぞれが隣と直角になる、れんがや寄木の古典的な模様。長いれんが、45° の回転、平行四辺形で見た目が変わり、バスケット織りではれんがを 2 枚ずつ組みます。",
    "f_pentagonal": "五角形タイリング",
    "f_pentagonal_d": "正五角形では平面を覆えませんが、15 種類の凸五角形は覆えます。六角形を半分にすると第 1 種、3 つの一様タイリングの双対からカイロ、柱状、花形の五角形タイリングが得られます。",
    "f_cairo": "カイロ五角形タイリング",
    "f_cairo_d": "長い辺 4 本と短い辺 1 本の五角形で、変形正方形タイリングの双対。カイロの街路にちなんで名付けられました。4 つの五角形が集まる頂点と 3 つが集まる頂点があり、五角形の対が六角形をつくります。",
    "f_girih": "ギリー・タイル",
    "f_girih_d": "ペルシャ建築で使われる辺の長さの等しい 5 種類のタイル（十角形、五角形、六角形、蝶ネクタイ、菱形）。表面の線は各辺の中点を 54° で横切るので、タイルどうしでつながって星形模様が現れます。",
    "f_wang": "ワンタイル",
    "f_wang_d": "辺に色の付いた正方形を、接する辺の色が一致するように、回転させずに並べます。Jeandel と Rao（2015）の 11 枚のタイルは非周期的にしか平面を覆えません。この部分はバックトラック探索で見つけました。",
    "f_zellij": "ゼリージュ",
    "f_zellij_d": "白、緑、黒、黄土色、青の釉薬片を手で切って組んだモロッコとアンダルシアのモザイク。十字を伴う八芒星や、6、8、10、12 芒の星の系が典型的です。",
    "f_islamic": "イスラームの幾何学模様",
    "f_islamic_d": "ハンキンの「接する多角形」の方法による星形模様：タイリングの各辺の中点から一定の角度で 2 本の線を出し、出会うまで延ばします。基のタイリングと角度が星を決め、組紐はリボンとして描きます。",
    "v_uniform": "一様彩色 %s",
    "v_tri_regular": "正三角形タイリング {3,6}",
    "v_kisrhombille": "Kisrhombille：30-60-90 の三角形（4.6.12 の双対）",
    "v_triakis": "Kisdeltile：30-30-120 の三角形（3.12.12 の双対）",
    "v_ts_plain": "切頂正方形タイリング 4.8.8",
    "v_circlepack": "円の充塡：各頂点に円",
    "v_ts_alt": "大きさが交互の正方形",
    "v_ts_chamfer": "面取り正方形タイリング（小さな正方形が消える）",
    "v_tetrakis": "四方正方形タイリング（4.8.8 の双対）",
    "v_dual_overlay": "双対を重ねて",
    "v_hex_regular": "正六角形タイリング {6,3}",
    "v_hex_2": "2 色、列ごと",
    "v_hex_21": "2 色、3 つに 1 つの六角形",
    "v_hex_3": "3 色：隣は必ず別の色",
    "v_hex_4": "4 色",
    "v_hex_7": "7 色：各六角形がほかのすべてに接する",
    "v_kissing": "円の最密充塡",
    "v_dissect1": "2-一様：六角形の 3 分の 1 を三角形に分割",
    "v_dissect2": "2-一様：六角形の 3 分の 2 を三角形に分割",
    "v_kagome": "籠目：辺を方向別に彩色",
    "v_unequal": "2 つの大きさの三角形",
    "v_twisted": "回した三角形：六角形が星になる",
    "v_twisted2": "さらに回転",
    "v_hexstar": "六角形と六芒星",
    "v_rhombille": "菱形タイリング：60° の菱形",
    "v_siena": "向き別に 3 段階、シエナ大聖堂のように",
    "v_cubes": "積み重ねた立方体：1 色相の 3 段階の明度",
    "v_rh_dual": "双対の三六角形タイリングに重ねて",
    "v_skew": "傾けて回転：平行四辺形",
    "v_pyth_half": "辺が 1 と 1/2 の正方形",
    "v_pyth_golden": "辺が黄金比",
    "v_pyth_random": "辺 1 と 0.3、ランダムなアースカラー",
    "n_triangular": "3.3.3.3.3.3 三角形",
    "n_square": "4.4.4.4 正方形",
    "n_hexagonal": "6.6.6 六角形",
    "n_trihexagonal": "3.6.3.6 三六角形",
    "n_truncated_hexagonal": "3.12.12 切頂六角形",
    "n_truncated_square": "4.8.8 切頂正方形",
    "n_truncated_trihexagonal": "4.6.12 切頂三六角形",
    "n_rhombitrihexagonal": "3.4.6.4 斜方三六角形",
    "n_snub_hexagonal": "3.3.3.3.6 変形六角形",
    "n_elongated_triangular": "3.3.3.4.4 伸長三角形",
    "n_snub_square": "3.3.4.3.4 変形正方形",
    "v_p3": "P3：太い菱形と細い菱形",
    "v_p3_ori": "菱形の 10 の向き別の P3",
    "v_p3_proper": "P3、隣の菱形は別の色",
    "v_p3_rings": "中心のまわりの輪の P3",
    "v_p2": "P2：凧と矢",
    "v_p2_rings": "中心のまわりの輪の P2",
    "v_p2_proper": "P2、隣のタイルは別の色",
    "v_hat": "ハット：1 つの形とその鏡像",
    "v_hat_ori": "向き別のハット",
    "v_robinson": "ロビンソン・タイル：印が入れ子の正方形を描く",
    "v_hb_2": "れんが 2:1",
    "v_hb_45": "45° 回転",
    "v_hb_3": "れんが 3:1",
    "v_hb_long": "長い板、約 6.6:1",
    "v_hb_par": "平行四辺形",
    "v_basket": "バスケット織り",
    "v_halves": "第 1 種：半分に切った六角形",
    "v_halves_alt": "第 1 種、3 方向に切断",
    "v_cairo_p": "カイロ・タイリング（第 2 種と第 4 種）",
    "v_prismatic": "柱状五角形（3.3.3.4.4 の双対）",
    "v_floret": "花形五角形（3.3.3.3.6 の双対）",
    "v_floret_proper": "花形五角形、隣は別の色",
    "v_cairo": "カイロ・タイリング：変形正方形タイリングの双対",
    "v_cairo_ori": "4 つの向き",
    "v_cairo_proper": "隣の五角形は別の色",
    "v_cairo_dual": "双対の変形正方形タイリングに重ねて",
    "v_girih_tiles": "十角形と蝶ネクタイ",
    "v_girih_lines": "各辺を 54° で横切るギリーの線",
    "v_girih_star": "ギリー模様、彩色",
    "v_girih_star2": "同じ模様、ゼリージュの配色",
    "v_wang": "Jeandel–Rao：11 枚、4 色、非周期",
    "v_wang_scheme": "同じタイル、配色による色",
    "v_stars_crosses": "八芒星と十字",
    "v_sc_azulejo": "アズレージョの青の星と十字",
    "v_z8": "接する八角形からの八芒星",
    "v_z12": "十二芒、六芒、四芒の星",
    "v_z10": "十芒星（ギリーの基）",
    "v_i6": "接する六角形からの六芒星",
    "v_i_sq": "正方形からの八角形と四芒星",
    "v_i_31212": "3.12.12 からの十二芒星",
    "v_i_4612": "4.6.12 からのロゼット",
    "v_i_3464": "3.4.6.4 からの星",
    "v_i_snub": "変形正方形タイリングからの星",
    "app_title": "タイリングとモザイク", "app_tiling": "タイリング", "app_scheme": "配色",
    "app_hue": "基準の色相", "app_size": "幅", "app_save": "保存…", "app_saved": "保存しました：%s",
    "app_drawing": "描画中…", "app_error": "この組み合わせは描けません：%s", "app_panels": "枚",
    "app_params": "パラメーター", "app_params_hint": "名前=値をスペース区切りで；Enter で適用",
})

# ---------------------------------------------------------------------- KO
STRINGS["ko"].update({
    "title": "타일링과 모자이크",
    "subtitle": "정규·준정규·비주기·이슬람 타일링을 색채 이론으로 채색",
    "intro": "타일링은 빈틈이나 겹침 없이 도형으로 평면을 덮는 것입니다. 같은 타일링도 채색에 따라 느낌이 달라집니다. 타일의 종류, 방향, 거울상에 따라, 또는 이웃한 타일이 늘 다르도록 칠할 수 있습니다. 각 쪽은 위키백과 문서 하나의 타일링을 여러 채색으로 그리며, 색은 RYB 색상환의 배색이나 전통 타일 팔레트에서 가져옵니다. 모든 것은 계산으로 만들어집니다. 다각형 격자, 쌍대, 펜로즈 수축 분할, '모자'의 메타타일, 왕 타일 탐색, 별무늬를 위한 행킨의 방법.",
    "schemes_t": "배색",
    "schemes_d": "RYB 배색은 기준 색상(여기서는 빨강)에서 시작해 12색상환 위에서 일정한 간격으로 색상을 고릅니다. 타일링에 배색보다 많은 색이 필요하면 같은 색상의 밝은 색과 어두운 색을 더합니다. 이름 있는 팔레트는 전통 유약 타일을 따릅니다.",
    "contents": "차례", "colouring": "채색", "cont": "계속", "page": "%d쪽",
    "c_single": "한 가지 색", "c_kind": "타일 종류별", "c_shape": "모양별",
    "c_chirality": "거울상별", "c_orientation": "방향별",
    "c_proper": "이웃은 다른 색", "c_random": "무작위", "c_rings": "중심에서 고리 모양",
    "c_classic": "네 가지 변 색", "c_scheme": "배색에서 고른 변 색",
    "c_checker": "체커보드", "c_gradient": "대각선 그라데이션",
    "f_triangular": "삼각형 타일링",
    "f_triangular_d": "각 꼭짓점에 정삼각형 여섯 개가 모입니다. 균일 채색은 꼭짓점 주위의 색으로 이름을 붙이며, 121212는 두 색을 번갈아, 121314는 네 색을 씁니다. 삼각형을 더 나누면 kisrhombille과 kisdeltile 타일링이 됩니다.",
    "f_truncated_square": "깎은 정사각형 타일링",
    "f_truncated_square_d": "각 꼭짓점에 정사각형 하나와 정팔각형 둘(4.8.8)로, 많은 부엌 바닥에 쓰입니다. 정사각형은 두 크기로 할 수 있고, 극한에서는 절반이 사라집니다(모따기 타일링). 쌍대는 사방 정사각형 타일링입니다.",
    "f_hexagonal": "육각형 타일링",
    "f_hexagonal_d": "벌집처럼 각 꼭짓점에 육각형 세 개. 육각형은 2, 3, 4, 7가지 색으로 규칙적으로 칠할 수 있고, 7색이면 각 육각형이 다른 모든 색과 닿습니다. 일부 육각형을 삼각형으로 나누면 2-균일 타일링이 됩니다.",
    "f_trihexagonal": "삼육각형 타일링",
    "f_trihexagonal_d": "각 꼭짓점 주위에 삼각형과 육각형이 번갈아 놓입니다(3.6.3.6). 변은 세 방향의 직선 무리를 이루어 일본 바구니의 가고메 무늬가 됩니다. 삼각형을 돌리거나 크기를 바꿔도 구조는 같습니다.",
    "f_rhombille": "마름모 타일링",
    "f_rhombille_d": "같은 60° 마름모가 한쪽 꼭짓점에 셋, 다른 쪽에 여섯 모입니다. 삼육각형 타일링의 쌍대입니다. 한 색상의 세 가지 명도로 칠하면 쌓인 정육면체처럼 보이며, 시에나 대성당 같은 옛 바닥에서 볼 수 있습니다.",
    "f_pythagorean": "피타고라스 타일링",
    "f_pythagorean_d": "두 크기의 정사각형으로, 각각 다른 크기의 정사각형 네 개와 닿습니다. 피타고라스 정리의 고전적인 증명 그림이자 흔한 바닥 무늬입니다.",
    "f_regular": "정다각형",
    "f_regular_d": "정다각형으로 만든 11가지 균일(아르키메데스) 타일링: 모든 꼭짓점 주위에 같은 다각형이 놓이며, 변의 수로 나타냅니다(3.4.6.4는 삼각형, 정사각형, 육각형, 정사각형). 꼭짓점 종류를 섞으면 k-균일 타일링이 됩니다.",
    "f_penrose": "펜로즈 타일링",
    "f_penrose_d": "반복하지 않을 때만 평면을 덮는 두 가지 타일: 두꺼운 마름모와 얇은 마름모(P3), 또는 연과 화살(P2). 황금 삼각형을 거듭 나누어(수축 분할) 그리며, 어디서나 5회 대칭이 나타납니다.",
    "f_aperiodic": "비주기 타일링",
    "f_aperiodic_d": "결코 반복하지 않는 타일링. '모자'(2023)는 거울상과 함께 쓰는 하나의 모양으로, 비주기적으로만 평면을 덮습니다. 로빈슨의 정사각형 타일 여섯 개는 점점 커지는 겹친 정사각형을 만들어 냅니다.",
    "f_herringbone": "헤링본 무늬",
    "f_herringbone_d": "직사각형을 계단식으로 놓아 각각이 이웃과 직각을 이루는 벽돌과 쪽매 바닥의 고전 무늬. 더 긴 벽돌, 45° 회전, 평행사변형으로 모양이 바뀌며, 바구니 짜기는 벽돌을 두 개씩 묶습니다.",
    "f_pentagonal": "오각형 타일링",
    "f_pentagonal_d": "정오각형으로는 평면을 덮을 수 없지만 볼록 오각형 15가지 부류는 덮을 수 있습니다. 육각형을 반으로 나누면 1형, 세 균일 타일링의 쌍대에서 카이로, 프리즘, 꽃 모양 오각형 타일링이 나옵니다.",
    "f_cairo": "카이로 오각형 타일링",
    "f_cairo_d": "긴 변 넷과 짧은 변 하나의 오각형으로, 다듬은 정사각형 타일링의 쌍대이며 카이로 거리에서 이름을 땄습니다. 어떤 꼭짓점에는 오각형 넷, 어떤 곳에는 셋이 모이고, 오각형 두 개가 육각형을 이룹니다.",
    "f_girih": "기리 타일",
    "f_girih_d": "페르시아 건축에 쓰인, 변의 길이가 같은 다섯 가지 타일(십각형, 오각형, 육각형, 나비넥타이, 마름모). 그 위의 선은 각 변의 중점을 54°로 지나므로 타일끼리 이어져 별무늬가 드러납니다.",
    "f_wang": "왕 타일",
    "f_wang_d": "변에 색이 있는 정사각형을 맞닿은 변의 색이 같도록, 돌리지 않고 놓습니다. Jeandel과 Rao(2015)의 타일 11개는 비주기적으로만 평면을 덮습니다. 이 부분은 백트래킹 탐색으로 찾았습니다.",
    "f_zellij": "젤리주",
    "f_zellij_d": "흰색, 초록, 검정, 황토, 파랑 계열의 유약 조각을 손으로 잘라 만든 모로코와 안달루시아의 모자이크. 십자와 함께 있는 팔각별과 6, 8, 10, 12각 별 체계가 특징입니다.",
    "f_islamic": "이슬람 기하학 무늬",
    "f_islamic_d": "행킨의 '맞닿은 다각형' 방법으로 만든 별무늬: 타일링의 각 변 중점에서 일정한 각도로 두 선을 내어 만날 때까지 그립니다. 바탕 타일링과 각도가 별을 정하고, 끈 무늬는 리본으로 그립니다.",
    "v_uniform": "균일 채색 %s",
    "v_tri_regular": "정삼각형 타일링 {3,6}",
    "v_kisrhombille": "Kisrhombille: 30-60-90 삼각형(4.6.12의 쌍대)",
    "v_triakis": "Kisdeltile: 30-30-120 삼각형(3.12.12의 쌍대)",
    "v_ts_plain": "깎은 정사각형 타일링 4.8.8",
    "v_circlepack": "원 채우기: 꼭짓점마다 원 하나",
    "v_ts_alt": "크기가 번갈아 바뀌는 정사각형",
    "v_ts_chamfer": "모따기 정사각형 타일링(작은 정사각형이 사라짐)",
    "v_tetrakis": "사방 정사각형 타일링(4.8.8의 쌍대)",
    "v_dual_overlay": "쌍대를 겹쳐 그림",
    "v_hex_regular": "정육각형 타일링 {6,3}",
    "v_hex_2": "두 색, 줄마다",
    "v_hex_21": "두 색, 세 개 중 하나",
    "v_hex_3": "세 색: 이웃은 늘 다름",
    "v_hex_4": "네 색",
    "v_hex_7": "일곱 색: 각 육각형이 다른 모든 색과 닿음",
    "v_kissing": "가장 빽빽한 원 채우기",
    "v_dissect1": "2-균일: 육각형의 3분의 1을 삼각형으로 나눔",
    "v_dissect2": "2-균일: 육각형의 3분의 2를 삼각형으로 나눔",
    "v_kagome": "가고메: 변을 방향별로 채색",
    "v_unequal": "두 크기의 삼각형",
    "v_twisted": "돌린 삼각형: 육각형이 별이 됨",
    "v_twisted2": "더 돌림",
    "v_hexstar": "육각형과 육각별",
    "v_rhombille": "마름모 타일링: 60° 마름모",
    "v_siena": "방향별 세 가지 명도, 시에나 대성당처럼",
    "v_cubes": "쌓인 정육면체: 한 색상의 세 명도",
    "v_rh_dual": "쌍대인 삼육각형 타일링 위에",
    "v_skew": "기울이고 돌림: 평행사변형",
    "v_pyth_half": "변이 1과 1/2인 정사각형",
    "v_pyth_golden": "변이 황금비",
    "v_pyth_random": "변 1과 0.3, 무작위 흙색",
    "n_triangular": "3.3.3.3.3.3 삼각형",
    "n_square": "4.4.4.4 정사각형",
    "n_hexagonal": "6.6.6 육각형",
    "n_trihexagonal": "3.6.3.6 삼육각형",
    "n_truncated_hexagonal": "3.12.12 깎은 육각형",
    "n_truncated_square": "4.8.8 깎은 정사각형",
    "n_truncated_trihexagonal": "4.6.12 깎은 삼육각형",
    "n_rhombitrihexagonal": "3.4.6.4 마름모삼육각형",
    "n_snub_hexagonal": "3.3.3.3.6 다듬은 육각형",
    "n_elongated_triangular": "3.3.3.4.4 늘인 삼각형",
    "n_snub_square": "3.3.4.3.4 다듬은 정사각형",
    "v_p3": "P3: 두꺼운 마름모와 얇은 마름모",
    "v_p3_ori": "마름모의 열 가지 방향별 P3",
    "v_p3_proper": "P3, 이웃 마름모는 다른 색",
    "v_p3_rings": "중심 둘레 고리 모양의 P3",
    "v_p2": "P2: 연과 화살",
    "v_p2_rings": "중심 둘레 고리 모양의 P2",
    "v_p2_proper": "P2, 이웃 타일은 다른 색",
    "v_hat": "모자: 한 모양과 그 거울상",
    "v_hat_ori": "방향별 모자",
    "v_robinson": "로빈슨 타일: 표시가 겹친 정사각형을 그림",
    "v_hb_2": "벽돌 2:1",
    "v_hb_45": "45° 회전",
    "v_hb_3": "벽돌 3:1",
    "v_hb_long": "긴 널판, 약 6.6:1",
    "v_hb_par": "평행사변형",
    "v_basket": "바구니 짜기",
    "v_halves": "1형: 반으로 자른 육각형",
    "v_halves_alt": "1형, 세 방향으로 자름",
    "v_cairo_p": "카이로 타일링(2형과 4형)",
    "v_prismatic": "프리즘 오각형(3.3.3.4.4의 쌍대)",
    "v_floret": "꽃 모양 오각형(3.3.3.3.6의 쌍대)",
    "v_floret_proper": "꽃 모양 오각형, 이웃은 다른 색",
    "v_cairo": "카이로 타일링: 다듬은 정사각형 타일링의 쌍대",
    "v_cairo_ori": "네 방향",
    "v_cairo_proper": "이웃 오각형은 다른 색",
    "v_cairo_dual": "쌍대인 다듬은 정사각형 타일링 위에",
    "v_girih_tiles": "십각형과 나비넥타이",
    "v_girih_lines": "각 변을 54°로 지나는 기리 선",
    "v_girih_star": "기리 무늬, 채색",
    "v_girih_star2": "같은 무늬, 젤리주 팔레트",
    "v_wang": "Jeandel–Rao: 타일 11개, 4색, 비주기",
    "v_wang_scheme": "같은 타일, 배색에서 고른 색",
    "v_stars_crosses": "팔각별과 십자",
    "v_sc_azulejo": "아줄레주 파랑의 별과 십자",
    "v_z8": "맞닿은 팔각형에서 만든 팔각별",
    "v_z12": "십이각, 육각, 사각 별",
    "v_z10": "십각별(기리 바탕)",
    "v_i6": "맞닿은 육각형에서 만든 육각별",
    "v_i_sq": "정사각형에서 만든 팔각형과 사각별",
    "v_i_31212": "3.12.12에서 만든 십이각별",
    "v_i_4612": "4.6.12에서 만든 장미 무늬",
    "v_i_3464": "3.4.6.4에서 만든 별",
    "v_i_snub": "다듬은 정사각형 타일링에서 만든 별",
    "app_title": "타일링과 모자이크", "app_tiling": "타일링", "app_scheme": "배색",
    "app_hue": "기준 색상", "app_size": "너비", "app_save": "저장…", "app_saved": "저장함: %s",
    "app_drawing": "그리는 중…", "app_error": "이 조합은 그릴 수 없습니다: %s", "app_panels": "칸",
    "app_params": "매개변수", "app_params_hint": "이름=값, 공백으로 구분; Enter로 적용",
})

# ------------------------------------------------------------------------- AR
# Arabic, written right to left: the programs draw it through i18n.visual().
STRINGS["ar"] = {
    "s_mono": "أحادي اللون", "s_analogous": "متجاور", "s_complementary": "متكامل",
    "s_split": "متكامل منقسم", "s_triad": "ثلاثي", "s_tetrad": "رباعي (مستطيل)",
    "s_square": "مربع", "s_rainbow": "قوس قزح", "s_zellij": "ألوان الزليج",
    "s_azulejo": "ألوان الأزوليجو", "s_girih": "ألوان الكره", "s_earth": "ألوان ترابية",
    "s_grey": "رماديات", "s_ramp": "تدرّج، من الداكن إلى الفاتح", "s_sweep": "تعاقب التدرّجات",
    "title": "التبليطات والفسيفساء",
    "subtitle": "تبليطات منتظمة وشبه منتظمة ولادورية وإسلامية، ملوّنة وفق نظرية الألوان",
    "intro": "يغطي التبليط المستوى بأشكال، دون فراغات أو تداخل. ويتغير طابع التبليط نفسه "
             "بتلوينه: حسب نوع القطعة، أو اتجاهها، أو صورتها في المرآة، أو بحيث تختلف "
             "القطع المتجاورة دائمًا. ترسم كل صفحة أدناه تبليطات مقالة واحدة من ويكيبيديا "
             "بعدة تلوينات؛ وتأتي الألوان من مخططات ألوان عجلة RYB أو من ألوان البلاط "
             "التقليدية. وكل ذلك محسوب: شبكات من المضلعات، والتبليطات الثنائية، وتصغير "
             "بنروز، وقطع \"القبعة\" الكبرى، والبحث عن تبليطات وانغ، وطريقة هانكين لأنماط "
             "النجوم.",
    "schemes_t": "مخططات الألوان",
    "schemes_d": "تأخذ مخططات RYB تدرّجات على خطوات ثابتة من عجلة التدرّجات الاثني عشر بدءًا "
                 "من تدرّج أساسي (هنا الأحمر)؛ وحين يحتاج التبليط إلى ألوان أكثر مما في "
                 "المخطط، تُضاف درجات فاتحة وداكنة من التدرّجات نفسها. أما اللوحات المسماة "
                 "فتحاكي البلاط المزجج التقليدي.",
    "contents": "المحتويات",
    "colouring": "التلوين",
    "cont": "تتمة",
    "page": "صفحة",
    "c_single": "لون واحد",
    "c_kind": "حسب نوع القطعة",
    "c_shape": "حسب الشكل",
    "c_chirality": "حسب الصورة في المرآة",
    "c_orientation": "حسب الاتجاه",
    "c_proper": "المتجاورات مختلفة",
    "c_random": "عشوائي",
    "c_rings": "حلقات من المركز",
    "c_classic": "ألوان الحواف الأربعة",
    "c_scheme": "ألوان الحواف من مخطط",
    "c_checker": "رقعة شطرنج",
    "c_gradient": "تدرّج عبر الصورة",
    "f_triangular": "التبليط المثلثي",
    "f_triangular_d": "تلتقي ستة مثلثات متساوية الأضلاع عند كل رأس. وتُسمّى تلويناته المنتظمة "
                      "بالألوان حول الرأس: 121212 يناوب بين لونين، و121314 يحتاج إلى أربعة. "
                      "وتقطيع المثلثات أكثر يعطي تبليطَي kisrhombille وkisdeltile.",
    "f_truncated_square": "التبليط المربع المقطوع",
    "f_truncated_square_d": "مربع ومثمنان منتظمان عند كل رأس (4.8.8)، وهو أرضية كثير من "
                            "المطابخ. يمكن أن تكون المربعات بحجمين، وفي الحد يختفي نصفها "
                            "(التبليط المشطوف). وثنائيه هو التبليط المربع الرباعي.",
    "f_hexagonal": "التبليط السداسي",
    "f_hexagonal_d": "ثلاثة مسدسات عند كل رأس، كما في خلية النحل. ويمكن تلوين المسدسات "
                     "بانتظام بلونين أو 3 أو 4 أو 7 ألوان؛ ومع 7 يلامس كل مسدس جميع الألوان "
                     "الأخرى. وتقطيع بعض المسدسات إلى مثلثات يعطي تبليطات ثنائية الانتظام.",
    "f_trihexagonal": "التبليط الثلاثي السداسي",
    "f_trihexagonal_d": "تتناوب المثلثات والمسدسات حول كل رأس (3.6.3.6)؛ وحوافه ثلاث عائلات "
                        "من الخطوط المستقيمة، وهو نمط كاغومي في السلال اليابانية. وتدوير "
                        "المثلثات أو تغيير حجمها يحافظ على البنية نفسها.",
    "f_rhombille": "تبليط المعينات",
    "f_rhombille_d": "معينات متطابقة بزاوية 60°، ثلاثة حول إحدى الزاويتين وستة حول الأخرى: "
                     "ثنائي التبليط الثلاثي السداسي. وبثلاث قيم من تدرّج واحد يبدو ككومة من "
                     "المكعبات، وهو نمط موجود في أرضيات قديمة مثل كاتدرائية سيينا.",
    "f_pythagorean": "التبليط الفيثاغوري",
    "f_pythagorean_d": "مربعات بحجمين، يلامس كل منها أربعة مربعات من الحجم الآخر. وهو الشكل "
                       "الذي يقوم عليه برهان كلاسيكي لمبرهنة فيثاغورس، ونمط شائع للأرضيات.",
    "f_regular": "المضلعات المنتظمة",
    "f_regular_d": "التبليطات المنتظمة الأحد عشر (الأرخميدية) بمضلعات منتظمة: حول كل رأس "
                   "المضلعات نفسها، وتُكتب بأعداد أضلاعها (3.4.6.4 مثلث ومربع ومسدس ومربع). "
                   "ومزج أنواع الرؤوس يعطي تبليطات k-منتظمة.",
    "f_penrose": "تبليطات بنروز",
    "f_penrose_d": "قطعتان لا تغطيان المستوى إلا دون تكرار: معينات سميكة ورفيعة (P3)، أو "
                   "طائرات ورقية وسهام (P2). تُرسم بتقطيع المثلثات الذهبية مرة بعد مرة "
                   "(التصغير)، وتُظهر تماثلًا خماسيًا في كل مكان.",
    "f_aperiodic": "التبليطات اللادورية",
    "f_aperiodic_d": "تبليطات لا تتكرر أبدًا. \"القبعة\" (2023) شكل واحد، يُستعمل مع صورته في "
                     "المرآة، ولا يبلّط إلا لادوريًا؛ وقطع روبنسون المربعة الست تفرض مربعات "
                     "متداخلة تكبر بلا نهاية.",
    "f_herringbone": "نمط عظم السمكة",
    "f_herringbone_d": "مستطيلات مرصوفة كالدرج، كل منها عمودي على جيرانه: النمط الكلاسيكي "
                       "للطوب والباركيه. والطوب الأطول أو التدوير بزاوية 45° أو متوازيات "
                       "الأضلاع تغيّر مظهره؛ أما نسج السلة فيجمع الطوب أزواجًا.",
    "f_pentagonal": "التبليطات الخماسية",
    "f_pentagonal_d": "لا تستطيع المخمسات المنتظمة تبليط المستوى، لكن 15 عائلة من المخمسات "
                      "المحدبة تستطيع. وتنصيف المسدسات يعطي النوع 1؛ وثنائيات ثلاثة تبليطات "
                      "منتظمة تعطي التبليطات الخماسية القاهرية والمنشورية والزهرية.",
    "f_cairo": "التبليط الخماسي القاهري",
    "f_cairo_d": "مخمسات بأربعة أضلاع طويلة وضلع قصير، ثنائي التبليط المربع الأفطس، سُمّي "
                 "على اسم شوارع القاهرة. تلتقي أربعة مخمسات عند بعض الرؤوس وثلاثة عند "
                 "غيرها، وكل مخمسين يشكلان مسدسًا.",
    "f_girih": "قطع الكره (گره)",
    "f_girih_d": "خمس قطع متساوية الأضلاع (معشّر، مخمس، مسدس، ربطة عنق، معين) استُعملت في "
                 "العمارة الفارسية. والخطوط المرسومة عليها تقطع كل ضلع في منتصفه بزاوية 54°، "
                 "فتتصل عبر القطع لتكوّن نمط النجوم الظاهر.",
    "f_wang": "قطع وانغ",
    "f_wang_d": "مربعات بحواف ملوّنة، توضع بحيث تتطابق الحواف المتلامسة ولا تُدار أبدًا. "
                "قطع جاندل وراو الإحدى عشرة (2015) لا تبلّط المستوى إلا لادوريًا؛ وقد وُجدت "
                "هذه الرقعة ببحث تراجعي.",
    "f_zellij": "الزليج",
    "f_zellij_d": "فسيفساء مغربية وأندلسية من قطع مزججة مقطوعة باليد، بالأبيض والأخضر "
                  "والأسود والمغرة والأزرق. ومن سماتها النجوم الثمانية مع الصلبان، وأنظمة "
                  "النجوم ذات 6 و8 و10 و12 رأسًا.",
    "f_islamic": "الأنماط الهندسية الإسلامية",
    "f_islamic_d": "أنماط نجمية مصنوعة بطريقة هانكين للمضلعات المتلامسة: من منتصف كل ضلع في "
                   "التبليط يخرج خطان بزاوية ثابتة حتى يلتقيا. ويحدد التبليط الأساسي والزاوية "
                   "شكل النجوم؛ وتُرسم الأشرطة كأشرطة متشابكة.",
    "v_uniform": "تلوين منتظم %s",
    "v_tri_regular": "التبليط المثلثي المنتظم {3,6}",
    "v_kisrhombille": "Kisrhombille: مثلثات 30-60-90 (ثنائي 4.6.12)",
    "v_triakis": "Kisdeltile: مثلثات 30-30-120 (ثنائي 3.12.12)",
    "v_ts_plain": "التبليط المربع المقطوع 4.8.8",
    "v_circlepack": "رصّ الدوائر: دائرة عند كل رأس",
    "v_ts_alt": "مربعات بأحجام متناوبة",
    "v_ts_chamfer": "التبليط المربع المشطوف (تختفي المربعات الصغيرة)",
    "v_tetrakis": "التبليط المربع الرباعي (ثنائي 4.8.8)",
    "v_dual_overlay": "مع ثنائيه مرسومًا فوقه",
    "v_hex_regular": "التبليط السداسي المنتظم {6,3}",
    "v_hex_2": "لونان، في صفوف",
    "v_hex_21": "لونان، مسدس من كل ثلاثة",
    "v_hex_3": "ثلاثة ألوان: المتجاورات مختلفة دائمًا",
    "v_hex_4": "أربعة ألوان",
    "v_hex_7": "سبعة ألوان: كل مسدس يلامس جميع الألوان الأخرى",
    "v_kissing": "أكثف رصّ للدوائر",
    "v_dissect1": "ثنائي الانتظام: ثلث المسدسات مقطوع إلى مثلثات",
    "v_dissect2": "ثنائي الانتظام: ثلثا المسدسات مقطوعان إلى مثلثات",
    "v_kagome": "كاغومي: الحواف ملوّنة حسب الاتجاه",
    "v_unequal": "مثلثات بحجمين",
    "v_twisted": "مثلثات مُدارة: تصبح المسدسات نجومًا",
    "v_twisted2": "مُدارة أكثر",
    "v_hexstar": "مسدسات ونجوم سداسية",
    "v_rhombille": "تبليط المعينات: معينات 60°",
    "v_siena": "ثلاث درجات حسب الاتجاه، كما في كاتدرائية سيينا",
    "v_cubes": "مكعبات مكدّسة: تدرّج واحد بثلاث قيم",
    "v_rh_dual": "فوق ثنائيه، التبليط الثلاثي السداسي",
    "v_skew": "مائل ومُدار: متوازيات أضلاع",
    "v_pyth_half": "مربعات بأضلاع 1 و1/2",
    "v_pyth_golden": "أضلاع بالنسبة الذهبية",
    "v_pyth_random": "أضلاع 1 و0.3، ألوان ترابية عشوائية",
    "n_triangular": "3.3.3.3.3.3 مثلثي",
    "n_square": "4.4.4.4 مربع",
    "n_hexagonal": "6.6.6 سداسي",
    "n_trihexagonal": "3.6.3.6 ثلاثي سداسي",
    "n_truncated_hexagonal": "3.12.12 سداسي مقطوع",
    "n_truncated_square": "4.8.8 مربع مقطوع",
    "n_truncated_trihexagonal": "4.6.12 ثلاثي سداسي مقطوع",
    "n_rhombitrihexagonal": "3.4.6.4 معيني ثلاثي سداسي",
    "n_snub_hexagonal": "3.3.3.3.6 سداسي أفطس",
    "n_elongated_triangular": "3.3.3.4.4 مثلثي مستطال",
    "n_snub_square": "3.3.4.3.4 مربع أفطس",
    "v_p3": "P3: معينات سميكة ورفيعة",
    "v_p3_ori": "P3 حسب الاتجاهات العشرة للمعينات",
    "v_p3_proper": "P3، المعينات المتجاورة مختلفة",
    "v_p3_rings": "P3 في حلقات حول المركز",
    "v_p2": "P2: طائرات ورقية وسهام",
    "v_p2_rings": "P2 في حلقات حول المركز",
    "v_p2_proper": "P2، القطع المتجاورة مختلفة",
    "v_hat": "القبعة: شكل واحد وصورته في المرآة",
    "v_hat_ori": "القبعات حسب الاتجاه",
    "v_robinson": "قطع روبنسون: علاماتها ترسم مربعات متداخلة",
    "v_hb_2": "طوب 2:1",
    "v_hb_45": "مُدار 45°",
    "v_hb_3": "طوب 3:1",
    "v_hb_long": "ألواح طويلة، نحو 6.6:1",
    "v_hb_par": "متوازيات أضلاع",
    "v_basket": "نسج السلة",
    "v_halves": "النوع 1: مسدسات مقطوعة نصفين",
    "v_halves_alt": "النوع 1، مقطوع في ثلاثة اتجاهات",
    "v_cairo_p": "التبليط القاهري (النوعان 2 و4)",
    "v_prismatic": "خماسي منشوري (ثنائي 3.3.3.4.4)",
    "v_floret": "خماسي زهري (ثنائي 3.3.3.3.6)",
    "v_floret_proper": "خماسي زهري، المتجاورات مختلفة",
    "v_cairo": "التبليط القاهري: ثنائي التبليط المربع الأفطس",
    "v_cairo_ori": "أربعة اتجاهات",
    "v_cairo_proper": "المخمسات المتجاورة مختلفة",
    "v_cairo_dual": "فوق ثنائيه، التبليط المربع الأفطس",
    "v_girih_tiles": "معشّرات وربطات عنق",
    "v_girih_lines": "خطوط الكره، تقطع كل ضلع بزاوية 54°",
    "v_girih_star": "نمط الكره، ملوّنًا",
    "v_girih_star2": "النمط نفسه، بألوان الزليج",
    "v_wang": "جاندل–راو: 11 قطعة، 4 ألوان، لادوري",
    "v_wang_scheme": "القطع نفسها، بألوان من مخطط",
    "v_stars_crosses": "نجوم ثمانية وصلبان",
    "v_sc_azulejo": "نجوم وصلبان بزرقة الأزوليجو",
    "v_z8": "نجوم ثمانية من مثمنات متلامسة",
    "v_z12": "نجوم باثني عشر وستة وأربعة رؤوس",
    "v_z10": "نجوم عشارية (أساس الكره)",
    "v_i6": "نجوم سداسية من مسدسات متلامسة",
    "v_i_sq": "مثمنات ونجوم رباعية من مربعات",
    "v_i_31212": "نجوم اثنا عشرية من 3.12.12",
    "v_i_4612": "وريدات من 4.6.12",
    "v_i_3464": "نجوم من 3.4.6.4",
    "v_i_snub": "نجوم من التبليط المربع الأفطس",
    "app_title": "التبليطات والفسيفساء",
    "app_tiling": "التبليط",
    "app_scheme": "المخطط",
    "app_hue": "التدرّج الأساسي",
    "app_size": "العرض",
    "app_save": "حفظ…",
    "app_saved": "حُفظ: %s",
    "app_drawing": "جارٍ الرسم…",
    "app_error": "تعذّر رسم هذا التركيب: %s",
    "app_panels": "لوحات",
    "app_params": "المعاملات",
    "app_params_hint": "اسم=قيمة، مفصولة بمسافات؛ Enter للتطبيق",
}
