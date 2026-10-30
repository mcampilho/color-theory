# Teoria da Cor

*English: [README.md](README.md)*

Um guia de teoria da cor, um póster vetorial de dez páginas e duas rodas de cores para
construir em casa, tudo gerado em Python. As rodas podem ser impressas e recortadas, ou
rodadas no ecrã (aplicação de computador ou página web). Todos os textos existem em inglês,
português e espanhol.

**Experimente as rodas online: https://mcampilho.github.io/color-theory/web/?lang=pt**

![As duas rodas de cores no ecrã](images/on_screen.jpg)

## Póster

O `color_theory_document.py` desenha com o ReportLab um póster de dez páginas em formato
carta, na horizontal. Todas as cores são calculadas: o cubo RYB, o HSB, o cubo RGB, um
modelo simples de tintas CMY, os valores das palavras-chave de cor do CSS, as funções de
correspondência de cor CIE 1931 e o CIELAB. Nenhuma imagem é copiada. PDFs prontos:
[English](colour_theory_en.pdf), [Português](colour_theory_pt.pdf),
[Español](colour_theory_es.pdf).

| Página | Conteúdo |
|--------|----------|
| 1 | Roda RYB, cores primárias, secundárias e terciárias, tinta/tom/sombra, significados das cores, esquemas de cores |
| 2 | Modelos de cor (CMYK, RGB, HSB, escala de cinzentos), disco de matiz/saturação, propriedades e harmonias |
| 3 | Matiz e luminosidade: cruz de amostras matiz × tinta/sombra, rodas de tintas, tons e sombras, e o cubo RGB visto do vértice branco (hexágono de hexágonos) |
| 4 | Mistura e códigos: RYB, RGB e CMYK lado a lado, um hexagrama CMYK com percentagens de tinta e a paleta web-safe de 216 cores |
| 5 | Nomes das cores: roda RYB de círculos sobrepostos com nomes, e roda das cores com nome do CSS com os códigos hex |
| 6 | Cor e emoção: roda das emoções de Plutchik, rosácea em espiral de tintas e sombras, e pétalas translúcidas |
| 7 | "The Color Wheel": seis círculos RYB que passam pelo centro, com nomes nas sobreposições e no anel exterior, e uma esfera em espiral em fundo negro |
| 8 | O espaço das cores visíveis: diagrama de cromaticidade CIE 1931 (lugar espectral, lugar de Planck, triângulo sRGB), o espetro visível e as funções de correspondência de cor |
| 9 | Tintas e sombras: dez cores de base no meio de uma escala de 90 % branco (esquerda) a 90 % preto (direita) |
| 10 | Círculos de matiz: o círculo de 20 matizes de Munsell (a cor sRGB mais saturada de cada matiz, via CIELAB) e estrelas de doze cores RYB e RGB |

| | |
|---|---|
| ![Página 1](images/poster_p1.png) | ![Página 3](images/poster_p3.png) |
| ![Página 7](images/poster_p7.png) | ![Página 8](images/poster_p8.png) |
| ![Página 9](images/poster_p9.png) | ![Página 10](images/poster_p10.png) |

Todo o texto está na tabela `STRINGS`.

```bash
pip install reportlab pillow
python3 color_theory_document.py                 # todas as páginas -> colour_theory_en.pdf
python3 color_theory_document.py --lang pt       # português -> colour_theory_pt.pdf
python3 color_theory_document.py --lang es -o es.pdf
python3 color_theory_document.py --pages 3 4     # só algumas páginas
```

Opções:

- `--lang {en,pt,es}`: idioma do texto (por omissão `en`).
- `-o, --out CAMINHO`: PDF de saída (por omissão `colour_theory_<lang>.pdf`).
- `--pages N [N ...]`: páginas a desenhar (por omissão, as dez).

Para acrescentar um idioma, copia-se o bloco `en` da tabela `STRINGS`, traduzem-se os
valores e regista-se com uma chave nova.

## Rodas de cores para construir em casa

O `color_wheel.py` cria um PDF A4 de seis páginas, pronto a imprimir, com duas rodas de
cores em papel para recortar e montar em casa. Cada roda tem um disco de trás, que roda, e
um disco da frente com janelas, unidos no centro por um atache. PDFs prontos:
[English](colour_wheels_en.pdf), [Português](colour_wheels_pt.pdf),
[Español](colour_wheels_es.pdf).

![Os quatro discos para recortar](images/wheels_pages.png)

| Página | Conteúdo |
|--------|----------|
| 1 | Material necessário, impressão, recorte e montagem (com uma vista explodida) |
| 2 | Como usar as duas rodas e um glossário das palavras da cor |
| 3 | Disco 1, trás: as 12 cores RYB e cinco anéis de misturas (+ vermelho, + amarelo, + azul, + branco, + preto) |
| 4 | Disco 1, frente: cinco patilhas coloridas com as suas janelas, uma escala de cinzentos (valor 1 a 10) e definições das cores |
| 5 | Disco 2, trás: as 12 cores com os nomes, e a tinta, o tom e a sombra de cada uma |
| 6 | Disco 2, frente: 12 janelas para os nomes, 8 janelas grandes e o diagrama das harmonias (complementar, complementares divididas, tríade, tétrades) |

No disco 1, cada janela fica a uma distância diferente do centro. Por isso, a mistura de
uma cor com o que a patilha acrescenta pode ser impressa no ângulo dessa cor no disco de
trás: aparece na janela quando a cor está mesmo junto à patilha.

```bash
python3 color_wheel.py                 # -> colour_wheels_en.pdf
python3 color_wheel.py --lang pt       # português
python3 color_wheel.py --lang es -o es.pdf
```

As páginas 3 a 6 devem ser impressas em tamanho real (100 %); cada página tem uma barra de
100 mm para confirmar a escala. O programa vai buscar as cores e algumas funções de desenho
ao `color_theory_document.py`, por isso os dois ficheiros têm de estar na mesma pasta.

### No ecrã

As mesmas duas rodas podem ser rodadas no computador, com todas as partes (trás e frente
de cada disco) móveis:

- arrasta-se um disco com o rato (um disco de trás pela borda colorida ou através de uma janela);
- a roda do rato roda o disco debaixo do ponteiro, uma cor de cada vez;
- ← e → rodam o disco selecionado uma cor; ↑ e ↓ (ou Tab) escolhem outro disco.

**Computador** (Tkinter e Pillow, nada mais para instalar):

```bash
python3 color_wheel.py --app            # inglês
python3 color_wheel.py --app --lang pt  # começa em português; o idioma pode ser mudado na janela
```

**Web**: abre-se o `web/index.html` num browser. A caixa de idioma no topo alterna entre
inglês, português e espanhol. A página carrega os discos de `web/discs/` (SVG) e os textos e
a geometria dos discos de `web/discs/data.js`, ambos escritos por:

```bash
python3 color_wheel.py --web            # -> web/discs/  (ou: --web OUTRA_PASTA)
```

É preciso voltar a executá-lo depois de mudar os discos ou os textos. A página em si
(`index.html`, `style.css`, `app.js`) é HTML, CSS e JavaScript simples, sem passo de build.

**A página web numa janela própria** (pywebview): a mesma página, numa janela do
computador sem browser. Se a pasta `web/discs/` faltar, é escrita primeiro.

```bash
pip install pywebview
python3 color_wheel.py --webview            # inglês
python3 color_wheel.py --webview --lang pt  # começa em português
```

No Windows usa o Edge WebView2, que já vem com o Windows 10 e 11.

## Outros ficheiros

- `Claude - The Complete Guide to Color Theory.md`: o guia de referência completo, da física
  da luz aos espaços de cor, em inglês (também em `.docx` e `.pdf`).
- `color_theory_poster.py`: o póster anterior, de uma página, só em inglês.
- `images/`: as imagens deste README.

## Licença

[MIT](LICENSE)
