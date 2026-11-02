# Color Theory — guia e pósteres de teoria da cor

Pasta de documentos sobre teoria da cor, publicada em https://github.com/mcampilho/color-theory
(público, licença MIT, ramo `master`), com GitHub Pages a servir o ramo: a página das rodas
fica em https://mcampilho.github.io/color-theory/web/ (`?lang=pt` escolhe o idioma), por isso
`web/discs/` tem de ser regenerado e enviado quando os discos mudam. O `README.md` está em inglês e o `README.pt.md` em
português europeu: mudar os dois em conjunto. As imagens dos READMEs estão em `images/`; os
PDFs atuais (`colour_theory_*.pdf`, `colour_wheels_*.pdf`) e `web/discs/` vão para o
repositório, para se poderem usar sem Python. Contém:

- `Claude - The Complete Guide to Color Theory.md` — guia de referência completo (da física da luz
  aos espaços de cor e sistemas de correspondência), em inglês. As versões `.docx` e `.pdf`
  com o mesmo nome são exportações deste texto; se o `.md` mudar, ficam desatualizadas.
- `color_theory_document.py` — póster de 10 páginas em PDF vetorial (ReportLab + Pillow):
  1. roda RYB, esquemas e significados;
  2. modelos de cor, disco de matiz/saturação e harmonias;
  3. matiz e luminosidade: cruz matiz × tinta/sombra, rodas de tintas, tons e sombras,
     hexágono do cubo RGB visto do vértice branco;
  4. mistura e códigos: RYB/RGB/CMYK lado a lado, estrela CMYK com percentagens, paleta web-safe;
  5. nomes das cores: roda de círculos sobrepostos com nomes, roda de cores CSS com códigos hex;
  6. cor e emoção: roda de Plutchik, rosácea em espiral, flor de pétalas translúcidas;
  7. "The Color Wheel": 6 círculos RYB que passam pelo centro, com nomes nas sobreposições e
     no anel exterior, e esfera em espiral em fundo negro (36 círculos pelo centro);
  8. espaço das cores visíveis: diagrama de cromaticidade CIE 1931 (lugar espectral, lugar de
     Planck, triângulo sRGB), espetro visível e funções de correspondência de cor;
  9. tintas e sombras: 10 cores de base no meio de uma escala de 90 % branco a 90 % preto;
  10. círculos de matiz: círculo de Munsell (20 matizes, a cor sRGB mais saturada de cada ângulo
      CIELAB em `MUNSELL_HUES`, que são aproximados) e estrelas de 12 cores RYB e RGB.
  Todo o texto está na tabela `STRINGS` (en, pt, es); para um idioma novo copia-se o bloco `en`.
  As páginas 3–10 foram inspiradas em imagens de referência, mas todas as cores são calculadas
  (cubo RYB, HSB, cubo RGB, modelo de tintas CMY em `cmy_to_rgb`, valores das palavras-chave CSS,
  funções CIE em `cmf`). O contorno do diagrama CIE usa a tabela oficial `SPECTRAL_LOCUS`, porque o
  ajuste gaussiano de `cmf` se desvia abaixo de ~440 nm e acima de ~650 nm.
  O Inkscape ignora recortes encaixados (`clipPath` dentro de `clipPath`): usar um só recorte.
- `color_wheel.py` — rodas de cores para construir em casa: PDF A4 de 6 páginas (instruções de
  montagem, como usar e glossário; depois os 4 discos para recortar, cada um numa página com
  barra de escala de 100 mm). Disco 1 (misturas): o disco da frente tem 5 patilhas e 5 janelas a
  raios diferentes (`D1_BANDS`, `D1_TAB_ANGLES`); no disco de trás a mistura do matiz i com a
  patilha k está no ângulo do matiz i e na banda k, por isso só aparece na janela k quando o
  matiz está junto à patilha. Disco 2 (relações): janelas fixas na frente (`D2_FANS`, sentido
  horário a partir do topo) e tinta/tom/sombra no disco de trás. Importa cores e funções de
  desenho do `color_theory_document.py` (incluindo os nomes `hue_names` da tabela `STRINGS`);
  os textos próprios estão na sua `STRINGS` (en, pt, es).
  Versões no ecrã, com as 4 partes a rodar (rato, roda do rato, setas): `--app` abre uma janela
  Tkinter e `--web` escreve `web/discs/<lang>/*.svg` e `web/discs/data.js` para a página
  `web/index.html` (`app.js` e `style.css` escritos à mão, sem build). Ambas desenham as
  mesmas funções `build_disc*` com `_VIRTUAL = True` (sem moldura de página; as janelas são
  furos feitos por `disc_base`) num `ShapeRecorder`, que imita o canvas do ReportLab e guarda
  as formas; `items_to_svg` e `items_to_image` (Pillow) escrevem-nas. O recorder só tem os
  métodos que os discos usam (sem recortes): se um disco passar a usar outro método do canvas,
  é preciso acrescentá-lo lá. As janelas vêm de `d1_windows`/`d2_windows`, usadas no desenho e
  para saber que parte está debaixo do rato (`hit_part`; no JS, `hit`).
  `--webview` abre a página web numa janela própria com o pywebview (`pip install pywebview`;
  é a única dependência opcional): `run_webview` escreve `web/discs` se faltar e chama
  `window.setLang` do `app.js` depois de a página carregar.
  Modo escuro (só no ecrã; os PDFs ficam sempre claros): as cores de papel, texto, linhas e
  diagrama dos discos vêm de `THEMES` via `set_theme`, e `record_part(build, lang, theme)`
  desenha o tema escuro. Nos discos usar `PAPER`/`INK`/`LINE`/`RULE`/`DIAGRAM`, não `WHITE` ou
  `BLACK`, quando a cor é do papel e não uma cor real (a tinta, a patilha + branco, a escala de
  cinzentos). O `--web` escreve `<part>-dark.svg`; a página escolhe o tema no `<head>`
  (`?theme=`, `localStorage`, sistema) e o `app.js` troca os SVG. Na janela Tkinter, as cores
  estão em `UI_COLOURS` (iguais às do `style.css`); `--theme auto` usa `system_theme()`.
- `tilings.py` — pavimentações e mosaicos dos artigos da Wikipedia listados em `tiles.md`, com
  várias colorações e as cores dos esquemas RYB (importa `ryb_to_rgb`, `hue_ryb`, `mix` e os
  `hue_names` do `color_theory_document.py`). Sem argumentos escreve o catálogo A4
  `tilings_<lang>.pdf` (`CATALOGUE`: uma família por artigo, 6 painéis por página); com o
  nome de uma pavimentação escreve uma imagem `.png`/`.svg`/`.pdf`. Estrutura:
  - `Periodic`: motivo de polígonos numa rede (a1, a2).
  - `with_gaps`: acrescenta os buracos entre peças, encontrados por `faces`, as faces do grafo
    plano (corta segmentos que se cruzam ou tocam). Não separa duas peças em falta que
    partilhem uma aresta (por isso a `snub_square` corta os losangos à mão).
  - `dual`: centros das peças à volta de cada vértice completo.
  - `hankin`: linhas a `theta` graus a partir do meio das arestas, emparelhadas pela soma mais
    curta, e as faces entre elas.
  - Não periódicas: `penrose` (deflação de triângulos de Robinson; P2 junta as metades pela
    aresta AB, P3 pela BC; as regras do P2 foram confirmadas por uma procura em que todas as
    metades interiores ficam emparelhadas); `hat` (metapeças de Kaplan, reescritas do hatviz); `robinson`;
    `wang` (procura com retrocesso das 11 peças de Jeandel–Rao, lidas do SVG da Wikipedia).
  - `TILINGS` regista cada pavimentação com as suas colorações próprias (`TRI_COLOURINGS`,
    `HEX_COLOURINGS`, por célula da rede) e parâmetros. As colorações universais (`UNIVERSAL`)
    usam `shape_info` (forma, quiralidade, orientação) ou a adjacência por arestas.
  - Folhas: vários argumentos `chave:opção=valor:...` (`parse_item`; as opções fora de
    `ITEM_KEYS` são parâmetros) ou `--vary scheme|hue|colouring` (`variations`) →
    `write_sheet` (PNG via `render_sheet`, SVG com `svg_panel` e um `clipPath` por painel,
    porque o Inkscape não recorta `<svg>` encaixados; PDF com `draw_ops_pdf`). O
    `build_scene` ignora parâmetros que a pavimentação não tem, para que `-p` sirva a todos os painéis.
  - `--show` abre `PreviewApp` (Tkinter): caixas para pavimentação, coloração, esquema,
    matiz, largura e parâmetros; redesenha ao mudar, e *Guardar…* chama `write_file` /
    `write_sheet`. Os textos da janela são as chaves `app_*`.
  - Os textos estão na `STRINGS` no fim do ficheiro (en, pt, es).
  - Não usar ⁴ ⁶ nos textos (a Helvetica do PDF não os tem): escrever 3.3.3.3.6.
  - Ficou de fora, por falta de geometria fiável: a P1 de Penrose e os arcos de
    correspondência, o pentágono do tipo 15, as estrelas 3-9 e o Cairo equilátero/colinear.
- `patterns.py` — mosaicos decorados sobre o motor do `tilings.py`: regista as suas
  pavimentações em `tl.TILINGS`, junta a sua `STRINGS` à do `tilings.py`, troca o
  `tl.PROGRAM` (catálogo, chaves mostradas na lista e na janela, nome do PDF) e chama
  `tl.main()`. Por isso tudo o que o `tilings.py` faz (folhas, `--vary`, `--show`) funciona aqui.
  - `decorate`: facetas e faixas sobre qualquer pavimentação (`base`).
  - `voxel_patch`: renderizador isométrico de voxels. Desenha por ordem de x+y+z e salta as
    faces tapadas. As arestas são tiras finas desenhadas logo a seguir à sua face, só onde o
    objeto dobra ou acaba, e o objeto de um voxel é dado por (i, j).
  - Outros padrões: `tripods` (cantos na rede (2,-1,-1), (-1,2,-1), a única que encontrei a
    encaixar), `framework`, `quilt` (tabelas `QUILT_LAYOUTS`), `jigsaw`, `weave`, `beadwork`.
  - Labirintos e espirais: uma grelha periódica de paredes (`wall_patch`), com corredores nas
    linhas/colunas ímpares (alargados por `wide`) e paredes nas pares, desenhada plana ou com
    voxels. `maze` é um labirinto perfeito num toro (DFS com semente); `spiral` usa a espiral
    quadrada (`link` = grega, `pinwheel` = quatro à volta de um canto). Os passos do chão vêm de
    uma BFS no toro do período (`_distances`), que dá também o caminho mais longo.
  - `whirl`: polígonos em remoinho sobre qualquer `base`; as colorações `arm`/`twist` seguem os
    dois sentidos dos braços de espiral.
  - Peças sem contorno levam no PDF e no SVG um traço fino da própria cor, para tapar as costuras.
  - Para isto o `tilings.py` ganhou:
    - `Tile.shade` (luz aplicada depois da cor), `Tile.colour` (cor fixa, para juntas) e `Tile.stroke`;
    - linhas com papel `line:<largura>[:<hex>]`, e `background` e `lw` por pavimentação;
    - os esquemas `ramp` e `sweep` e a coloração `gradient`.
- `wallpapers.py` — wallpapers abstratos (numpy, scipy, Pillow; usa só `tl.palette` e os
  nomes de esquemas e matizes do `tilings.py`). Cada estilo é `f(spec, W, H, rng, noise, cols, p)`
  e devolve um array RGB em 0..1 de qualquer tamanho com o aspeto W x H; o `render()`
  redimensiona, junta vinheta e grão. Coordenadas em alturas da imagem; formas que dependem
  do tamanho usam `min(A, 1)`, para servirem também em vertical. `Noise` é ruído fractal
  periódico (grelhas aleatórias + `map_coordinates` cúbico). Estilos suaves desenham numa
  grelha reduzida (`grid(W, H, max_px)`); `ribbons` e `trails` desenham linhas com Pillow
  a 2x. Tamanhos em `SIZES`/`SIZE_GROUPS`; `--show` abre uma janela Tk com comboboxes.
- `color_theory_poster.py` — versão anterior, só a página 1, sem traduções (ReportLab).
- PDFs gerados: `colour_theory_en.pdf`, `colour_theory_pt.pdf`, `colour_theory_es.pdf`
  (do `color_theory_document.py`), `colour_wheels_en.pdf`, `colour_wheels_pt.pdf`,
  `colour_wheels_es.pdf` (do `color_wheel.py`), `colour_theory.pdf` (do poster). `Color_Theory_Guide.pdf` e
  `claude_colour_theory.pdf` são versões antigas.

## Comandos

```bash
pip install reportlab pillow
python3 color_theory_document.py                      # -> colour_theory_en.pdf (10 páginas)
python3 color_theory_document.py --lang pt            # -> colour_theory_pt.pdf
python3 color_theory_document.py --lang es -o es.pdf
python3 color_theory_document.py --pages 3 4          # só as páginas 3 e 4
python3 color_theory_poster.py [saida.pdf]            # -> colour_theory.pdf
python3 color_wheel.py [--lang pt]                    # -> colour_wheels_<lang>.pdf (A4, 6 páginas)
python3 color_wheel.py --app [--lang pt]              # rodas numa janela (Tkinter)
python3 color_wheel.py --web                          # -> web/discs/ para web/index.html
python3 color_wheel.py --webview [--lang pt]          # a página web numa janela (pywebview)
python3 color_wheel.py --app --theme dark             # --theme auto|light|dark (--app, --webview)
python3 tilings.py [--lang pt]                        # -> tilings_<lang>.pdf (catálogo, 22 páginas)
python3 tilings.py --list                             # pavimentações, colorações, esquemas
python3 tilings.py hexagonal -c 7 --scheme rainbow -o hex.svg
python3 tilings.py cairo --show                       # janela de pré-visualização
python3 tilings.py cairo --vary scheme --cols 4 -o folha.png   # folha de variações
python3 patterns.py [--lang pt]                       # -> patterns_<lang>.pdf (mosaicos decorados)
python3 patterns.py tripods --show                    # qualquer opção do tilings.py serve
python3 wallpapers.py ribbons --size 4k -o r.png      # wallpapers (pip install numpy scipy)
python3 wallpapers.py --show [--lang pt]              # janela de pré-visualização
python3 wallpapers.py --gallery --size iphone         # todos os estilos numa folha
```

Para ver uma página como imagem:
`inkscape --pages=3 --export-type=png --export-dpi=130 --export-filename=p3.png colour_theory_en.pdf`.

## Regras

- Desenho 100% vetorial em ReportLab (página carta em paisagem, 792×612 pt). A página 1 usa a
  grelha 750×570 (`X()`/`Y()`); as páginas 2–6 usam pontos com origem em baixo à esquerda.
- Texto novo vai para `STRINGS` nos três idiomas, nunca diretamente no código de desenho.
  Os nomes das cores CSS (`CSS_COLOURS`) são palavras-chave e não se traduzem.
- Cada página nova é uma função `build_page_N(c)` registada em `PAGES`.
- O script principal é `color_theory_document.py`; o `color_theory_poster.py` fica como referência.
- Depois de mudar o desenho, verificar as páginas visualmente nos três idiomas
  (os textos em pt/es são mais compridos).
