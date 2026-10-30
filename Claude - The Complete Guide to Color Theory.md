# The Complete Guide to Color Theory

*A reference guide from the physics of light to color spaces and color-matching systems*

## 1. Introduction

Color is not a property of objects alone. It is a perception created when light, a surface (or light source), and a visual system interact. Light with a particular mix of wavelengths reaches the eye, three types of cone cells respond to it in different amounts, and the brain turns those responses into the sensation we call color.

Color theory is the body of practical and scientific knowledge that explains how colors are produced, mixed, described, measured and combined. It has two broad sides:

- **Artistic and design theory**: the color wheel, harmony, contrast, temperature, schemes and palettes. This is how artists and designers choose colors that work together.
- **Scientific and technical theory**: spectra, color models, color spaces, color depth and color-matching systems. This is how colors are measured, stored, reproduced and communicated between people and devices.

This guide covers both, starting with the physics of light and ending with modern color spaces such as CIELAB, HSLuv, sRGB and Adobe RGB.

## 2. Light and the Visible Spectrum

### 2.1 Electromagnetic radiation

Visible light is a narrow band of the electromagnetic spectrum, which runs from radio waves (very long wavelengths) through microwaves, infrared, visible light, ultraviolet, X-rays and gamma rays (very short wavelengths). Wavelength is measured in nanometers (nm), where 1 nm is one billionth of a meter.

### 2.2 The visible spectrum: about 390–710 nm

The human eye responds to wavelengths from roughly **390 nm to 710 nm**. The exact limits are not sharp: different references quote 380–750 nm, 390–700 nm or 400–700 nm, because sensitivity fades gradually at both ends and varies between individuals and with brightness. The CIE (International Commission on Illumination) tabulates color-matching data from 360 nm to 830 nm to be safe.

Approximate wavelength ranges of the spectral colors:

| Color | Approximate wavelength (nm) |
| --- | --- |
| Violet | 390–450 |
| Blue | 450–495 |
| Green | 495–570 |
| Yellow | 570–590 |
| Orange | 590–620 |
| Red | 620–710 |

These boundaries are conventional. The spectrum is continuous, and where one color ends and the next begins is partly a matter of language and culture.

### 2.3 Spectral colors and non-spectral colors

A **spectral color** is produced by a single wavelength (monochromatic light), such as the pure red of a laser. Many colors we see have no single wavelength. **Magenta** and **purple** (the non-spectral purples) appear only when red and blue/violet light are mixed, so they are not on the rainbow. White, gray, black, brown and pink are also not spectral colors.

### 2.4 How we see color

The retina contains two kinds of photoreceptors:

- **Rods** work in dim light and see only brightness (no color).
- **Cones** work in bright light and give color vision. Humans normally have three types, called **S** (short, peak around 420 nm), **M** (medium, around 534 nm) and **L** (long, around 564 nm). They are often loosely called blue, green and red cones.

The brain compares the signals from the three cone types. This is called **trichromacy**, and it is the reason three numbers are enough to describe any color we can perceive, and why screens can imitate almost any color with only three primaries. It also explains **metamerism**: two lights with completely different spectra can look identical if they produce the same three cone responses.

A further stage of processing, described by **opponent-process theory**, organizes signals into three channels: light vs. dark, red vs. green, and blue vs. yellow. This is why we never perceive a "reddish green" or a "yellowish blue", and it underlies systems such as the Natural Color System and spaces such as CIELAB.

### 2.5 Why objects have color

A surface appears colored because it absorbs some wavelengths and reflects or transmits others. A ripe tomato absorbs most blue and green light and reflects red. The color you see also depends on the **light source**: the same surface looks different under daylight, candlelight and fluorescent light. This is why the **illuminant** (for example D65 or D50 daylight) is always specified in serious color work.

## 3. Additive vs. Subtractive Color

There are two fundamental ways to create color by mixing.

### 3.1 Additive color (mixing light)

In additive mixing, colored lights are combined and the result gets **brighter**. Starting from darkness (black), adding light produces color, and adding all of the primaries at full strength produces white.

- **Primaries**: Red, Green, Blue (RGB).
- Red + Green = **Yellow**
- Green + Blue = **Cyan**
- Blue + Red = **Magenta**
- Red + Green + Blue = **White**

Used in: screens (monitors, phones, TVs), projectors, stage lighting, cameras' sensors. Each pixel on a display is made of tiny red, green and blue sub-pixels.

### 3.2 Subtractive color (mixing pigments, inks and dyes)

In subtractive mixing, pigments absorb (subtract) wavelengths from the white light that falls on them, and the result gets **darker**. Starting from white paper, each added layer of ink removes more light.

- **Primaries (printing)**: Cyan, Magenta, Yellow (CMY), with Black (K) added in practice, giving **CMYK**.
- Cyan + Magenta = **Blue**
- Magenta + Yellow = **Red**
- Yellow + Cyan = **Green**
- Cyan + Magenta + Yellow = a dark, muddy brown-black in practice (ideal black in theory)

Used in: printing, painting, dyeing, photography prints, and any reflective medium.

In traditional art education, the subtractive primaries are taught as **red, yellow and blue (RYB)**. This is a historical simplification that works reasonably well with paints but cannot reproduce as wide a range of colors as the cyan–magenta–yellow set.

### 3.3 Summary comparison

|  | Additive | Subtractive |
| --- | --- | --- |
| Medium | Emitted light | Reflected/transmitted light through pigment |
| Primaries | R, G, B | C, M, Y (+K) |
| Starting point | Black (no light) | White (paper, canvas) |
| Mixing all primaries | White | Dark (near black) |
| Typical use | Screens, lighting | Print, painting |
| Mixing effect | Brighter | Darker |

## 4. The Color Wheel

The **color wheel** arranges hues around a circle so that relationships between colors can be seen at a glance. Isaac Newton created the first color circle in 1666 after splitting white light with a prism and bending the spectrum into a circle, closing the gap between red and violet with the non-spectral purples. Later versions came from Goethe, Munsell, Itten (the 12-part wheel taught in art schools) and others.

A standard artist's wheel has **12 hues**: three primary, three secondary and six tertiary colors. Different wheels (RYB, RGB, CMY) place the "pure" hues at different positions, so the exact look of a wheel depends on the model it represents.

### 4.1 Primary colors

Primary colors are the base colors from which others are mixed, and which cannot be made by mixing other colors in the same system.

- **RYB (traditional art)**: red, yellow, blue.
- **RGB (additive)**: red, green, blue.
- **CMY (subtractive print)**: cyan, magenta, yellow.

Note that "primary" is a property of a system, not a universal truth. Three primaries are chosen because the eye has three cone types, and each set can only reproduce the colors inside the triangle (the *gamut*) they span.

### 4.2 Secondary colors

Secondary colors are made by mixing two primaries in equal amounts.

- RYB: **orange** (red + yellow), **green** (yellow + blue), **violet** (blue + red).
- RGB: **yellow**, **cyan**, **magenta**.
- CMY: **red**, **green**, **blue**.

### 4.3 Tertiary colors

Tertiary (intermediate) colors are made by mixing a primary with its neighboring secondary. On the RYB wheel there are six: **red-orange, yellow-orange, yellow-green, blue-green, blue-violet and red-violet**. Their names always put the primary first and the secondary second (for example, "yellow-green" is more yellow than "green-yellow" would be).

### 4.4 Hue, and the wheel as a map of hue

The wheel is a map of **hue**, the attribute that distinguishes red from green or blue. Moving around the circle changes the hue; moving toward the center (mixing with gray or white) changes saturation or lightness. Digital color pickers usually express hue as an angle: 0° red, 60° yellow, 120° green, 180° cyan, 240° blue, 300° magenta.

## 5. Color Relationships and Harmony

**Color harmony** is the pleasing, balanced arrangement of colors. Harmony does not have a single scientific definition. It is a set of time-tested guidelines that describe which combinations tend to feel unified (low tension) or vibrant (high tension). The classic harmonies are defined by geometric positions on the color wheel.

### 5.1 Analogous colors

Colors that sit **next to each other** on the wheel, usually two to five neighbors (for example yellow, yellow-green and green).

- **Effect**: calm, cohesive, natural, easy on the eye. Found in nature (sunsets, foliage).
- **Risk**: low contrast, so the design can feel flat. Fix this by varying lightness and saturation, and by choosing one dominant color with the others in support.

### 5.2 Complementary colors

Colors **directly opposite** each other on the wheel (for example red and green, blue and orange, yellow and violet).

- **Effect**: maximum hue contrast, energetic, each color makes the other look more intense. Mixed together as pigments, complements neutralize each other toward gray or brown; mixed as lights they approach white.
- **Risk**: can be harsh when both are used at full saturation and equal area. Use one as the dominant color and the other as an accent.
- **Related**: **split-complementary** uses a hue plus the two colors adjacent to its complement. It keeps much of the contrast with less tension.

### 5.3 Triadic colors

Three hues **evenly spaced** around the wheel (120° apart), forming an equilateral triangle. Examples: red, yellow, blue; or orange, green, violet.

- **Effect**: vibrant and balanced while keeping variety, even when desaturated.
- **Tip**: let one color dominate and use the other two sparingly.

### 5.4 Tetradic colors (double complementary / rectangle)

Four hues forming a **rectangle** on the wheel: two pairs of complementary colors. For example, blue and orange together with red-violet and yellow-green.

- **Effect**: rich and varied, with many possibilities.
- **Risk**: hard to balance. Let one color dominate and manage warm and cool tones carefully.
- **Square scheme**: a related harmony using four hues spaced 90° apart.

### 5.5 Other harmonies

- **Monochromatic**: one hue in different tints, tones and shades.
- **Neutral + accent**: grays, blacks, whites and browns with one saturated accent.
- **Accented analogous**: an analogous group plus a complementary accent.

### 5.6 Principles that make harmony work

Wheel geometry is only a starting point. What usually determines success:

1. **Proportion**: the common 60-30-10 guideline gives 60% to a dominant color, 30% to a secondary and 10% to an accent.
2. **Saturation control**: a palette of highly saturated colors tires the eye. Mix saturated colors with muted ones.
3. **Value structure**: a clear pattern of lights and darks is often more important than the hues themselves.
4. **Context**: colors change appearance depending on neighbors (simultaneous contrast), lighting and surface texture.

## 6. Warm and Cool Colors

Colors are commonly divided by **temperature**.

- **Warm colors**: reds, oranges, yellows, and warm browns. They are associated with sun, fire and energy. They tend to **advance** (appear closer) and feel stimulating.
- **Cool colors**: blues, greens, violets and cool grays. They are associated with water, sky, ice and shade. They tend to **recede** (appear farther) and feel calming.

Temperature is relative. A yellow-green is cool next to orange but warm next to blue-green. Even neutrals have temperature: a warm gray leans toward brown or red, a cool gray toward blue.

Practical uses:

- Painters build depth by using warmer colors in the foreground and cooler colors in the distance (atmospheric perspective).
- Light and shadow often contrast in temperature: warm light creates cool shadows, and the reverse.
- Interfaces use warm colors for calls to action and alerts, cool colors for backgrounds and calm areas.
- Photographers and filmmakers speak about **color temperature** of light in kelvin (K). Note the reversal: low kelvin values (candle, around 1900 K) look orange and "warm", high values (overcast sky, 6500–10000 K) look blue and "cool".

## 7. Mixing Pigments: Tint, Tone and Shade

A pure hue can be modified in three classic ways by adding white, gray or black.

| Term | Added to pure hue | Result |
| --- | --- | --- |
| **Tint** | White | Lighter, paler, often softer (pastels) |
| **Tone** | Gray (white + black) | Less saturated, subtler, more sophisticated |
| **Shade** | Black | Darker, richer, heavier |

Example: starting with red, pink is a tint, a dusty rose or brick red is a tone, and maroon is a shade.

Notes for painters:

- Adding **black** to a color not only darkens it but often shifts its hue (yellow plus black turns greenish). Many painters darken colors with a darker hue (such as a deep blue or brown) instead.
- Adding the **complement** of a color is another way to tone it down (desaturate it) while keeping it lively.
- **Opacity and transparency** matter: glazing transparent pigments creates different results than mixing opaque ones.
- Real pigments are never pure. Each "primary" paint has a bias toward the next hue (for example, a warm red leans toward orange, a cool red toward violet), which is why painters often keep a warm and a cool version of each primary.

Tints, tones and shades together form the **tonal range** of a hue, and generating them systematically is the easiest way to build a harmonious monochromatic palette.

## 8. Color Contrast

Contrast is a difference between colors that makes them distinguishable and creates visual emphasis. Johannes Itten described **seven types of color contrast**, still widely taught:

1. **Contrast of hue**: the difference between pure hues (for example red, yellow and blue together).
2. **Light-dark contrast**: difference in lightness or value. This is the strongest type and the most important for legibility.
3. **Cold-warm contrast**: difference in color temperature.
4. **Complementary contrast**: opposite hues placed side by side.
5. **Simultaneous contrast**: a color induces its complement in neighboring areas, so a gray patch on red looks slightly greenish.
6. **Contrast of saturation**: pure, intense colors next to dull, muted ones.
7. **Contrast of extension**: the relative amounts (areas) of colors. A small amount of a strong color balances a large area of a weaker one.

### 8.1 Contrast in accessibility

For text and user interfaces, contrast is measured as a **contrast ratio** based on the relative luminance of foreground and background, from 1:1 (identical) to 21:1 (black on white). The Web Content Accessibility Guidelines (WCAG) recommend at least **4.5:1** for normal text and **3:1** for large text and essential interface elements (level AA), and **7:1** for normal text at the stricter AAA level.

Lightness contrast is what matters most here. Two colors with different hues but similar luminance (such as red text on a green background) can be unreadable, especially for people with color vision deficiency.

### 8.2 Color vision deficiency

About 8% of men and 0.5% of women have some form of color vision deficiency, most commonly red–green. Good design never relies on color alone: add labels, icons, patterns or differences in lightness. Blue–orange combinations are generally safe for most forms of color blindness.

## 9. Color Schemes

A **color scheme** is a selection of colors chosen using a rule so that they work together. The harmonies in section 5 are the basis of most schemes:

| Scheme | Rule | Character |
| --- | --- | --- |
| Monochromatic | One hue, varying tint/tone/shade | Unified, elegant, safe |
| Analogous | Neighboring hues | Harmonious, natural |
| Complementary | Opposite hues | High contrast, vibrant |
| Split-complementary | One hue plus two flanking its complement | Contrasting but gentler |
| Triadic | Three hues at 120° | Balanced and colorful |
| Tetradic (rectangle) | Two complementary pairs | Rich, complex |
| Square | Four hues at 90° | Rich, varied |
| Neutral with accent | Neutrals plus one color | Modern, focused |

A practical workflow for choosing a scheme:

1. Define the **purpose and mood** (calm, urgent, luxurious, playful).
2. Pick a **dominant hue** and decide on its temperature.
3. Choose the **harmony rule** and derive supporting hues.
4. Adjust **lightness and saturation** to build clear contrast and a hierarchy.
5. Add **neutrals** (grays, off-whites, near-blacks tinted toward the main hue).
6. **Test** in context, in grayscale, and for color-blind viewers.

## 10. Palettes

In art and design, a **palette** is the collection of colors used in a work. In computing, the word has a precise technical meaning: a table of the specific colors available to an image or display. Digital palettes are classified by how their colors are chosen.

### 10.1 Monochrome palettes

A monochrome palette contains **two colors** (1 bit per pixel): one for "off" and one for "on". Traditionally these were black and white, but also green or amber on black for old terminals and monitors. Related variants are **grayscale palettes** with 4, 16 or 256 steps of gray (2, 4 or 8 bits per pixel).

### 10.2 Dichrome palettes

A dichrome palette uses **two color channels** instead of three, so its colors lie along a plane through color space rather than a full cube. Some early computer systems and printing processes produced two-ink (duotone) images with a limited but pleasant color range, such as red and cyan. Dichrome palettes are also used on purpose for stylistic duotone effects and for data visualization.

### 10.3 Regular RGB palettes

A regular RGB palette divides each channel into **evenly spaced levels**, so every combination of red, green and blue levels is present and the palette forms a regular grid in the RGB cube. Examples:

- **3-3-2 palette (8-bit)**: 8 levels of red, 8 of green, 4 of blue = 256 colors.
- **Web-safe palette**: 6 levels per channel (0, 51, 102, 153, 204, 255, or hex 00, 33, 66, 99, CC, FF) = 6 × 6 × 6 = **216 colors**.
- **RGB555 / RGB565 (high color)**: 32 levels for each channel (15-bit) or 32/64/32 levels (16-bit).
- **RGB888 (true color)**: 256 levels per channel = 16,777,216 colors.

### 10.4 Non-regular RGB palettes

Non-regular palettes do not use evenly spaced grids. The number of levels per channel may differ in odd ways, or the colors may be hand-picked or computed to suit the image. Examples:

- **Adaptive (optimized) palettes**: generated from an image by algorithms such as median cut or octree quantization, so the 256 colors are the best fit for that picture.
- **Fixed hand-chosen palettes**: the 16-color EGA/VGA palette, the original Macintosh and Windows system palettes, and the Commodore 64 palette.
- **Uneven grids**: palettes such as 6-8-5 levels or 6-7-6 levels per channel (which together give 240 or 252 colors) that spend more levels on the channels the eye is most sensitive to (green) and fewer on blue.

Adaptive palettes usually look much better for photographs, while regular palettes are simpler and work well on any image because no analysis is needed. **Dithering** (mixing nearby pixels of palette colors) is used with either type to simulate colors that aren't in the palette.

## 11. Color Models

A **color model** is an abstract mathematical system that describes colors as tuples of numbers (usually three or four). A **color space** is a color model combined with a precise definition of what those numbers mean (primaries, white point, transfer function), so that the same numbers always give the same physical color. For example, RGB is a model, while sRGB and Adobe RGB are two different color spaces based on it.

| Model | Components | Type | Typical use |
| --- | --- | --- | --- |
| **RGB** | Red, Green, Blue | Additive | Screens, cameras, scanners, web |
| **CMY / CMYK** | Cyan, Magenta, Yellow (+ blacK) | Subtractive | Printing |
| **RYB** | Red, Yellow, Blue | Subtractive (traditional) | Painting education |
| **HSL / HSV (HSB)** | Hue, Saturation, Lightness / Value | Perceptual-style rearrangement of RGB | Color pickers, design tools |
| **YUV / YCbCr** | Luma + two color-difference channels | Luma–chroma | Video, JPEG, broadcast |
| **CIE XYZ / Lab / Luv** | Device-independent coordinates | Colorimetric | Color measurement, color management |
| **Munsell / NCS** | Hue, value/blackness, chroma | Appearance-based | Physical color atlases |

### 11.1 RGB

Each color is described by the amounts of red, green and blue light, either as a fraction (0–1), a percentage, or an integer (usually 0–255). RGB follows the way cameras and displays work, but it is **device-dependent**: the same RGB triplet looks different on different screens unless a color space and profile define it.

### 11.2 CMYK

CMYK adds **black (K, the “key” plate)** to cyan, magenta and yellow. Black is added because overprinting the three colored inks gives a muddy dark brown rather than a true black, it uses a lot of ink, and it makes text and fine detail blurry through slight misregistration. CMYK has a smaller gamut than RGB, particularly for saturated blues, greens and oranges, so vivid screen colors often look duller in print. Values are given as percentages of ink coverage (0–100% per channel). Real CMYK always depends on the **press, ink and paper**, which is why profiles such as FOGRA39, SWOP or GRACoL exist.

### 11.3 Luma–chroma models (YUV, YCbCr)

Video and image compression separate brightness (luma, Y′) from color (two color-difference channels, Cb and Cr). Because human vision resolves fine detail in brightness much better than in color, the color channels can be stored at lower resolution (**chroma subsampling**, written 4:4:4, 4:2:2, 4:2:0) with little visible loss. This is how JPEG, MPEG and most video formats save space.

## 12. Web Colors

### 12.1 Notation

Web colors are specified in sRGB. The common CSS notations are:

- **Hexadecimal**: `#RRGGBB`, for example `#FF8800` (red FF = 255, green 88 = 136, blue 00 = 0). Shorthand `#RGB` doubles each digit (`#F80` = `#FF8800`). An optional 4th pair gives **alpha** (opacity): `#RRGGBBAA`.
- **Functional**: `rgb(255 136 0)`, `rgb(255 136 0 / 50%)`, `hsl(32 100% 50%)`.
- **Named colors**: 140 names such as `red`, `rebeccapurple`, `cornflowerblue`, `papayawhip`.
- **Modern CSS Color Level 4**: `lab()`, `lch()`, `oklab()`, `oklch()`, and `color(display-p3 …)` for colors outside sRGB.

### 12.2 Web-safe colors

In the 1990s many displays could only show 256 colors at once. The **web-safe palette** of 216 colors (6 levels per channel: 00, 33, 66, 99, CC, FF, a regular RGB palette as seen in section 10) was meant to display without dithering on all systems. Because practically all screens now show millions of colors, it has no practical importance today, but it remains a useful historical reference and a quick way to pick evenly spaced colors.

## 13. Color Depth

**Color depth (bit depth)** is the number of bits used to represent the color of a pixel. More bits allow more distinct colors and smoother gradients.

| Bits per pixel | Name | Number of colors | Notes |
| --- | --- | --- | --- |
| 1 | Monochrome | 2 | Black and white |
| 4 |  | 16 | EGA/VGA text modes |
| 8 | Indexed color / grayscale | 256 | Uses a palette (CLUT) or 256 gray levels |
| 15/16 | High color | 32,768 / 65,536 | 5-5-5 or 5-6-5 bits per channel |
| 24 | True color | 16.7 million | 8 bits per channel (R, G, B) |
| 30 | Deep color | \~1.07 billion | 10 bits per channel, used for HDR and wide gamut |
| 36–48 |  | 68 billion – 281 trillion | 12–16 bits per channel, in RAW photos and professional work |

Points worth knowing:

- The human eye can distinguish roughly **a few million to about ten million** different colors, so 24-bit is enough for most uses, but **banding** (visible steps) can appear in smooth gradients such as skies. Higher bit depth, or dithering, reduces it.
- **32-bit** images are usually 24-bit color plus an 8-bit **alpha channel** (transparency).
- Editing at 16 bits per channel preserves headroom, so repeated adjustments do not destroy tonal detail.
- **Floating-point (HDR) formats** (such as OpenEXR) store values that go well above 1.0, to represent real-world brightness ranges.
- Bit depth is distinct from **gamut**: the same number of colors can be spread across a small gamut (sRGB) or a large one (Rec. 2020).

## 14. Color Matching and Color Order Systems

Numeric models are good for machines, but designers, printers, manufacturers and scientists also need ways to **name, order and physically reproduce** colors. These systems give each color a reference code, usually with a physical sample.

### 14.1 Pantone Matching System (PMS)

The **Pantone Matching System**, introduced in 1963 by Pantone, is the best-known proprietary color-matching system. It is built around **spot colors**: premixed inks made from a small set of base pigments (13 base pigments plus black) according to published formulas, so that a printer anywhere in the world can reproduce, say, PANTONE 485 C identically.

- **Why it exists**: CMYK printing builds colors from tiny dots, which cannot reproduce certain vivid colors, metallics, fluorescents or exact brand colors. A spot ink is a single, consistent ink.
- **Naming**: a number plus a suffix for the paper: **C** (coated), **U** (uncoated), **M** (matte). The same number looks different on different stocks, so the suffix matters.
- **Products**: swatch books (Formula Guides), chips, and extended systems for fashion, home and interiors (the TPX/TCX/TPG families), plus metallics and pastels and neons.
- **Pantone Color of the Year**: a yearly trend announcement made since 2000.
- **Limitations**: it is a licensed, proprietary system, swatches fade over time, and many Pantone colors lie outside the CMYK or sRGB gamut, so on-screen or CMYK equivalents are only approximations.

### 14.2 Pantone GoeSystem

**GoeSystem** was a Pantone product line launched in 2007 as a more modern and more systematically organized set of colors, with about **2,000 colors** (around 2,058). Its distinguishing features were:

- Colors arranged by **hue and lightness** in an orderly sequence, so it was easier to find a color and its neighbors than in the traditional PMS, which grew historically.
- A cleaner, more vivid palette with a stronger, more consistent coverage of the color range, and a numeric system of codes organized to reflect hue families.
- Higher-quality printed chips (the GoeGuide and GoeSticks) and digital tools.

Pantone later focused on its other product lines, and GoeSystem has since been largely phased out in favor of the main Pantone Matching System and newer systems and tools. Older projects may still refer to Goe numbers.

### 14.3 Munsell color system

Created by the American painter and teacher **Albert H. Munsell** (first published in *A Color Notation*, 1905), this is the first color system to describe color in three perceptually organized dimensions, and it remains a foundation of modern color science.

- **Hue**: arranged around a circle with five principal hues (**Red, Yellow, Green, Blue, Purple**) and five intermediates (YR, GY, BG, PB, RP), each subdivided into 10 steps (a total of 100 hue steps).
- **Value**: lightness from 0 (black) to 10 (white), with neutral grays in between.
- **Chroma**: the purity or strength of a color, from 0 (neutral gray) upward in steps of 2 with no fixed upper limit (some colors reach 14–20 or more).

A color is written **hue value/chroma**, for example `5R 4/14` is a strong, medium-dark red. Munsell aimed for **equal visual steps** in each dimension. Because the maximum chroma differs by hue and value, the resulting color solid is irregular and lopsided, often compared to a tree with branches of different length rather than a neat sphere. This was an important insight: perceptual color space is not symmetrical. The system was refined by the Optical Society of America in the **1943 Munsell Renotations**, and Munsell notation can be converted to CIE coordinates.

It is still widely used in **soil science** (Munsell soil color charts), geology, archaeology, forensics, dentistry, and food and paint industries.

### 14.4 Natural Color System (NCS)

The **Natural Color System** was developed in Sweden (based on Ewald Hering’s 19th-century opponent-colors theory) and adopted as a Swedish national standard in 1979. Rather than mixing ingredients, NCS describes **how a color appears to a human observer**, in terms of how similar it looks to six **elementary colors**: white, black, yellow, red, blue and green (these form three opponent pairs: white–black, red–green, yellow–blue).

A notation such as `S 2030-Y90R` reads as follows:

- `S` = standard sample (second edition).
- `20` = **blackness** (20% black).
- `30` = **chromaticness** (30% of the maximum color intensity).
- `Y90R` = **hue**: 90% of the way from yellow toward red, so it is a reddish orange.

Whiteness is whatever remains (100 − 20 − 30 = 50%). NCS is very popular in **architecture, interior design and paint**, especially in Scandinavia and Europe. Other widely used reference systems include **RAL** (industrial and construction colors), **Federal Standard 595** and **British Standard** colors.

## 15. Color Terminology: Precise Definitions

Color vocabulary is used loosely in everyday speech. The terms below have distinct technical meanings, and mixing them up is a common source of confusion between disciplines.

| Term | Meaning | Type |
| --- | --- | --- |
| **Hue** | The attribute that distinguishes red, green, blue, etc. Shown as the angle around the color wheel. | Perceptual |
| **Radiance** | The physical power of light emitted or reflected from a surface, per unit area and solid angle (W·sr⁻¹·m⁻²). Not weighted by human sensitivity. | Physical |
| **Luminance** | Radiance weighted by the eye’s sensitivity to each wavelength (the V(λ) function, peak at 555 nm). Measured in cd/m². In CIE XYZ it is the **Y** component. | Physical/photometric |
| **Luma** | The weighted sum of **gamma-encoded** R′G′B′ values used in video (Y′). An approximation of luminance, not identical to it. | Technical |
| **Brightness** | The perceived amount of light coming from a source or an area. Subjective; goes from dim to bright. | Perceptual |
| **Lightness** | The brightness of a surface judged relative to a similarly lit white surface (dark to light). CIE **L\*** measures it. | Perceptual |
| **Value** | In Munsell, lightness of a surface. In HSV/HSB, the largest of the R, G, B components (not a perceptual quantity). | Both |
| **Colorfulness** | The degree to which an area appears different from gray. Absolute: it increases as illumination increases (the Hunt effect). | Perceptual |
| **Chroma** | Colorfulness of an area judged **relative to the brightness of a similarly lit white**. Applies to surfaces; in CIELAB, **C\*** = √(a\*² + b\*²). | Perceptual |
| **Saturation** | Colorfulness of an area judged **relative to its own brightness**: vividness or purity. A gray has zero saturation. | Perceptual |

### 15.1 How they relate

- A dim red room and the same room in bright sunlight have different **colorfulness**, but similar **chroma** and **saturation**, because those are relative measures.
- A pale pink has **low saturation** and high lightness. A deep maroon can be **highly saturated** but low in lightness.
- **Luminance** is physical and **brightness** is the sensation it creates, and the relation between them is nonlinear (roughly a power law of about 1/3 for lightness).
- In sRGB the relative luminance of a color uses **linear-light** values: `Y = 0.2126 R + 0.7152 G + 0.0722 B`. The coefficients show why green looks brightest and blue darkest at equal RGB values.
- Video **luma** uses the same idea on gamma-encoded values: `Y′ = 0.299 R′ + 0.587 G′ + 0.114 B′` (Rec. 601, standard definition), `0.2126 / 0.7152 / 0.0722` (Rec. 709, HD) and `0.2627 / 0.6780 / 0.0593` (Rec. 2020, UHD).

## 16. Color Spaces

### 16.1 HSL and HSV (HSB)

**HSL** (Hue, Saturation, Lightness) and **HSV** (Hue, Saturation, Value; also called HSB, with B for Brightness) were developed in the 1970s (by Alvy Ray Smith and by Joblove and Greenberg, 1978) as **more intuitive ways to arrange RGB**. They rotate the RGB cube into a cylinder (HSL) or cone/hexcone (HSV) so users can choose a hue first, then adjust how vivid or light it is.

With R, G, B in \[0, 1\], `max` = largest and `min` = smallest:

- **Hue** (same in both): an angle from 0° to 360° depending on which channel is largest, e.g. if R is the max, `H = 60° × ((G − B) / (max − min))`. Red = 0°, green = 120°, blue = 240°.
- **HSV**: `V = max`, `S = (max − min) / max`.
- **HSL**: `L = (max + min) / 2`, `S = (max − min) / (1 − |2L − 1|)`.

Differences:

|  | HSL | HSV |
| --- | --- | --- |
| Full-color point | L = 50% | V = 100%, S = 100% |
| L / V = max | Always white | Pure hue (or lighter at lower S) |
| Lightness axis | Symmetric: black → pure color → white | Asymmetric: black → pure color only |
| Natural for | CSS, tints and shades | Color pickers, painting software |

**Weakness**: both are simple geometric re-arrangements of RGB, so they are **not perceptually uniform**. Pure yellow (`hsl(60 100% 50%)`) looks far lighter than pure blue (`hsl(240 100% 50%)`) even though both have L = 50%, and a given step in hue or saturation produces different visual changes in different regions. Because of this, they can mislead when you need predictable contrast.

### 16.2 TSL color space

**TSL (Tint, Saturation, Lightness)** is a color space derived from normalized RGB (chromaticity coordinates), designed mostly for **computer vision**, notably for detecting human **skin** because skin tones cluster tightly in it regardless of brightness. With normalized values `r = R/(R+G+B)`, `g = G/(R+G+B)`, and `r′ = r − 1/3`, `g′ = g − 1/3`:

- **T (tint)** = `arctan(r′ / g′) / 2π + 1/4` (with adjustments depending on the sign of g′).
- **S (saturation)** = `√( (9/5)(r′² + g′²) )`
- **L (lightness)** = `0.299 R + 0.587 G + 0.114 B`

Because it separates chromaticity (T, S) from intensity (L), it is robust to lighting changes, and it appears in face detection and image segmentation.

### 16.3 CIE 1931 XYZ color space

The **CIE 1931 XYZ** space is the foundation of modern colorimetry. In the late 1920s, W. David Wright and John Guild ran experiments in which observers matched spectral colors by adjusting three primary lights. Averaged and standardized by the CIE in 1931 (for a **2° field of view**; a 10° observer was added in 1964), the results gave the **color-matching functions**, the response of a “standard observer”.

- Physical RGB primaries cannot match all colors without “negative” amounts of light. The CIE therefore defined **imaginary primaries X, Y, Z** so that all visible colors have non-negative coordinates.
- **Y** is defined to equal **luminance**; Z is roughly the blue stimulation; X is a mix of the cone responses.
- Normalized chromaticity coordinates are `x = X/(X+Y+Z)`, `y = Y/(X+Y+Z)`. Plotting x against y gives the familiar **horseshoe-shaped chromaticity diagram**: the curved edge (the **spectral locus**) is pure spectral light from about 380 to 700 nm, and the straight bottom edge (the **line of purples**) joins red and violet.
- Any color made by mixing two lights lies on the straight line between them in this diagram, and the triangle between three primaries is that device’s **gamut**.
- The **white point** matters: D65 (daylight, x = 0.3127, y = 0.3290) for screens, D50 for printing.

XYZ is **device-independent**, so it works as the common reference (the “profile connection space”) of color management systems. Its main flaw is that it is **not perceptually uniform**: equal distances in XYZ or xy do not correspond to equal perceived differences (MacAdam ellipses, which show the range of colors indistinguishable from a center color, vary hugely in size and shape across the diagram).

### 16.4 CIELAB (L\*a\*b\*) color space

Published by the CIE in 1976, **CIELAB** is a nonlinear transformation of XYZ designed to be **approximately perceptually uniform**, inspired by opponent-process theory and Munsell.

- **L\***: lightness, 0 (black) to 100 (diffuse white).
- **a\***: green (−) to red (+).
- **b\***: blue (−) to yellow (+).

With `f(t) = t^(1/3)` for larger t (with a linear section near zero) and the reference white `(Xn, Yn, Zn)`: `L\* = 116 f(Y/Yn) − 16`, `a\* = 500 [f(X/Xn) − f(Y/Yn)]`, `b\* = 200 [f(Y/Yn) − f(Z/Zn)]`.

- **Polar form (CIELCh)**: chroma `C\* = √(a\*² + b\*²)` and hue angle `h° = atan2(b\*, a\*)`, which is easier for people to reason about.
- **Color difference ΔE**: the distance between two colors, originally `ΔE\*ab = √(ΔL\*² + Δa\*² + Δb\*²)`. A ΔE of about 1 is roughly the smallest difference an observer can notice. Later improvements, **ΔE94** and **ΔE2000**, correct for the remaining non-uniformities and are the standards in print, textile and paint quality control.
- Lab is **device-independent**, covers the whole visible gamut (and more) and is used in Photoshop, ICC profiles and color-difference measurements.

Known weaknesses: it is only approximately uniform (for instance, blues can shift toward purple when lightness changes), and it models a fixed viewing condition without full account of surround or adaptation.

### 16.5 CIELUV (L\*u\*v\*) color space

Also published in 1976, alongside CIELAB, **CIELUV** is another approximately uniform space, based on the **CIE 1976 UCS chromaticity diagram** (u′, v′): `u′ = 4X / (X + 15Y + 3Z)`, `v′ = 9Y / (X + 15Y + 3Z)`.

- `L\*` is the same lightness as in CIELAB; `u\* = 13 L\* (u′ − u′n)`, `v\* = 13 L\* (v′ − v′n)`.
- Its key advantage: **additive mixtures of lights stay on straight lines** in the u′v′ plane, so it is the preferred space for **displays, lighting, television and emissive color**. CIELAB is preferred for **surface colors** (print, paint, textiles).
- It has a polar version too (CIELCHuv, with C\*uv and h\*uv).

### 16.6 CIEUVW (CIE 1964 U\*V\*W\*)

**CIE 1964 U\*V\*W\*** is an earlier uniform color space based on the CIE 1960 UCS diagram (u, v). Its lightness is `W\* = 25 Y^(1/3) − 17` (valid for Y between 1 and 99), and `U\* = 13 W\* (u − u0)`, `V\* = 13 W\* (v − v0)`, where (u0, v0) is the white point. It was recommended for computing color differences and for color-rendering calculations (the original Color Rendering Index of light sources was computed in it). It has since been **superseded by CIELAB and CIELUV**, but it remains a part of the history of uniform color spaces and appears in older standards and lighting documents.

### 16.7 Uniform color spaces

A **uniform (perceptually uniform) color space** is one in which equal Euclidean distances correspond to equal perceived color differences. It is a very useful property for gradients, palette generation, color-difference metrics, image processing and data visualization. No fixed space achieves it perfectly, since color perception depends on context, but several come close:

- **CIELAB and CIELUV** (1976): the classic approximations.
- **CAM02-UCS and CAM16-UCS**: based on *color appearance models* (CIECAM02, CAM16) that also account for viewing conditions and chromatic adaptation. They are more accurate but more complex.
- **Jₐzₐbₐ** (2017): designed for HDR and wide-gamut content.
- **OKLab / OKLCH** (Björn Ottosson, 2020): a simple, computationally cheap space with good uniformity, hue linearity (blue stays blue as it is lightened) and smooth gradients. It is now supported in CSS and widely used in design systems.

In a non-uniform space like RGB or HSL, a gradient between blue and yellow can look gray and muddy or have uneven brightness in the middle. In a uniform space, the steps look even.

### 16.8 HSLuv color space

**HSLuv** (created by Alexei Boronine, previously called HUSL) is a human-friendly alternative to HSL, built on top of **CIELUV in its polar form (LCHuv)**.

- **H** is the hue angle from LCHuv.
- **L** is CIE lightness (L\*), so equal L really does look equally light, and its relation to contrast is predictable (a yellow and a blue at the same L have a similar luminance).
- **S** is chroma **rescaled to 0–100% of the maximum that fits within sRGB** for that hue and lightness. Unlike CIELCH, this means any (H, S, L) combination is a valid sRGB color, with no out-of-gamut values to clip.

A variant, **HPLuv**, restricts saturation to the largest chroma that is available at every hue (for a given lightness), producing only pastel-like colors that all share the same chroma. HSLuv is useful for generating **palettes with consistent perceived lightness**, theming and accessible UI colors. Its downside is that scaling saturation relative to the gamut boundary means saturation values do not correspond to constant chroma across hues, and it inherits the minor non-uniformities of CIELUV.

### 16.9 LMS color space

**LMS** describes color as the responses of the three types of cone cells: **L** (long), **M** (medium) and **S** (short wavelengths). It is derived from XYZ by a linear matrix. A widely used matrix, the Hunt–Pointer–Estevez (D65) transform, is:

`L = 0.4002 X + 0.7076 Y − 0.0808 Z` `M = −0.2263 X + 1.1653 Y + 0.0457 Z` `S = 0.9182 Z`

Uses of LMS:

- **Chromatic adaptation**: simulating how the eye adjusts to a different illuminant (the von Kries transform scales L, M and S independently; the Bradford transform is a refined variant used in ICC profiles).
- **Color vision deficiency simulation**: protanopia (missing L), deuteranopia (missing M) and tritanopia (missing S) can be simulated by removing or projecting out one cone channel.
- **Color appearance models** such as CIECAM02 and CAM16 and newer spaces such as OKLab, which begin with a cone-response stage.

### 16.10 sRGB

**sRGB** (“standard RGB”) was created in 1996 by HP and Microsoft and standardized as IEC 61966-2-1 (1999). It is the **default color space of the web, most consumer cameras, operating systems and non-color-managed content**.

- **Primaries**: those of ITU-R BT.709 (HDTV): red (0.640, 0.330), green (0.300, 0.600), blue (0.150, 0.060) in xy.
- **White point**: D65 (0.3127, 0.3290).
- **Transfer function (gamma)**: a piecewise curve close to a power function of about **2.2**, linear for very dark values (`12.92 × c` up to 0.0031308) and `1.055 × c^(1/2.4) − 0.055` above. It approximates the response of a CRT display and also allocates more code values to dark tones, where the eye is more sensitive.
- **Gamut**: relatively small, covering roughly a third of the chromaticities in the CIE 1931 diagram, but it is the common denominator of displays.

### 16.11 Adobe RGB (1998)

**Adobe RGB (1998)** was designed by Adobe to cover most of the colors reproducible by **CMYK printers**, while still being defined using RGB.

- **Primaries**: red (0.640, 0.330), green (**0.210, 0.710**), blue (0.150, 0.060). The red and blue are identical to sRGB; the difference is a far more saturated **green**.
- **White point**: D65. **Gamma**: about 2.2 (563/256 ≈ 2.199).
- **Gamut**: about **35% larger than sRGB**, mostly in **cyan–green** tones, which suits photography and print workflows (roughly half of the visible chromaticities).

If Adobe RGB images are shown without color management, they look dull and desaturated as if they were sRGB, so the profile must be embedded and honored. For web delivery, convert to sRGB.

### 16.12 Other important color spaces

- **Display P3**: DCI-P3 primaries, D65 white and the sRGB curve; about 25% larger than sRGB. Used by Apple devices and modern phones and monitors, and available in CSS.
- **Rec. 2020 (BT.2020)**: the very wide gamut for UHD television, using nearly monochromatic primaries.
- **ProPhoto RGB**: a very large gamut that includes colors outside the visible range, used for photo editing at high bit depth.
- **Rec. 2100 (PQ and HLG)**: HDR formats with transfer functions designed for very high luminance.

## 17. Gamut, Gamma and Color Management

- **Gamut**: the range of colors a device or space can represent. Colors a device cannot reproduce are **out of gamut**. Typical comparison: sRGB < Display P3 < Adobe RGB (roughly similar size, different shape) < Rec. 2020 < ProPhoto; the CMYK gamut is smaller than RGB in some regions and larger in others (cyans).
- **Gamma / transfer function**: the nonlinear curve that maps stored values to light intensity. Encoding is nonlinear so that bits are spent where the eye is sensitive. For physically correct operations (blending, blurring, lighting), values should first be converted to **linear light**.
- **ICC profiles**: files that describe how a device’s numbers map to a device-independent space (XYZ or Lab). A **color management system** converts between profiles.
- **Rendering intents** decide how out-of-gamut colors are handled: **perceptual** (compresses the whole range to keep relationships), **relative colorimetric** (keeps in-gamut colors exact and clips the rest, with white point adjustment), **saturation** (keeps vividness, for graphics) and **absolute colorimetric** (keeps exact appearance, including paper white, for proofing).
- **Calibration**: measuring and adjusting a monitor with a colorimeter so that its output is predictable.

## 18. Color Psychology and Culture

Color affects mood, attention and meaning, but the effects are **context-dependent and culturally variable**, and many popular claims are overstated. Reasonably well-supported tendencies:

- **Red**: high arousal; used for danger, urgency, passion, and in Western contexts for stop and error. Luck and celebration in China.
- **Orange and yellow**: energy, optimism, caution. Yellow is the most visible color against dark backgrounds.
- **Green**: nature, growth, health, safety (“go”), and money in some countries.
- **Blue**: calm, trust, stability; the most commonly cited favorite color across many cultures, and widely used by banks and technology firms.
- **Purple**: historically royalty and luxury (expensive dyes), now also creativity and mystery.
- **Black, white and gray**: formality, elegance, neutrality. White means purity and weddings in much of the West, but mourning in parts of East Asia.

Cultural meanings differ, so check the intended audience. Never rely on a color meaning alone; pair color with text, icons or shape.

## 19. Practical Guidelines

1. **Start with value, then add hue.** Check your design in grayscale. If it works there, color will make it better.
2. **Limit the palette**: one dominant color, one or two supporting colors, one accent and a set of neutrals. Use the 60-30-10 rule as a start.
3. **Tint your neutrals** slightly toward your main hue for a more cohesive look.
4. **Use temperature for depth and emphasis**: warm to advance, cool to recede.
5. **Design in a uniform space** (OKLCH, HSLuv, CIELCh) when you need consistent steps in lightness or predictable contrast.
6. **Check contrast** with WCAG ratios and test with color-blindness simulators.
7. **Know your medium**: screen colors (RGB, sRGB or P3) and printed colors (CMYK or spot colors) differ, so request proofs, and use Pantone for critical brand colors.
8. **Work in a color-managed workflow**: choose a working space, embed profiles, convert to sRGB for the web and to the printer’s profile for print.
9. **Mind the lighting**: judge physical colors under standardized light (D50 or D65 viewing booths) and beware metamerism.
10. **Test in context**: colors change next to other colors (simultaneous contrast), so always evaluate them in the real layout.

## 20. Quick-Reference Glossary

- **Additive mixing**: combining lights; more light gives a brighter result (RGB).
- **Analogous**: neighboring hues on the wheel.
- **Chroma**: colorfulness relative to a white reference (Munsell, CIELAB C\*).
- **CIE**: International Commission on Illumination, the standards body for colorimetry.
- **Complementary**: opposite hues on the wheel.
- **Gamut**: the set of colors a device or space can reproduce.
- **Hue**: the “color family” (red, green, blue …).
- **Illuminant**: the light source assumed when a color is defined (D50, D65 …).
- **Luminance**: photometric measure of light weighted by the eye’s sensitivity (Y).
- **Metamerism**: different spectra that look the same under a given light.
- **Saturation**: vividness relative to own brightness.
- **Shade, Tint, Tone**: hue plus black, white or gray.
- **Spot color**: a premixed ink (such as Pantone) printed as a single plate.
- **Subtractive mixing**: combining pigments or filters; more ink gives a darker result (CMY).
- **Value / Lightness**: how light or dark a color is.
- **White point**: the color treated as pure white in a color space (D65, D50).
