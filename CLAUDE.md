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
