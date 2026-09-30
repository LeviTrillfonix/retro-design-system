# Retro Design System

Fifty-three interface eras, from Mac System 7 to 90s banner ads, kept as one token set. Every era keeps its own palette and type; a nine-role layer makes any one of them the live skin for a window, an overlay, a flyer or a whole page. Built for TrillFx: VJ overlays, tool GUIs like VJToolbox, stream graphics and show flyers.

The source is NovusGFX's MIT-licensed *Retro Design System* collection, mirrored at `github.com/LeviTrillfonix/retro-design-system` (commit `911d9b1`). Every colour here is one of that repo's own values; nothing was invented. Credits and the license are at the end.

## How it is built

Three layers, from raw to live:

1. **System palettes.** Each of the 53 systems has nine colour tokens named `<id>-<role>`: `win95-accent`, `crt-ink`, `vaporwave-surface`. They are listed per system in Colors, in era order. Where a system has no distinct tone for a role, the token is an alias of another role (`swiss-accent2` is `{swiss-ink}`) rather than a repeated hex.
2. **The role layer.** Nine `ui-*` tokens (`ui-bg` to `ui-onaccent`) always hold the active system. Components, the cover and anything you build should use only these.
3. **Switching.** This artifact allows eight native themes, so eight featured systems are themes, marked ★ below: CRT Phosphor, Vaporwave, Windows 95, 8-Bit Arcade, Tron Vector, Game Boy DMG, Risograph, Swiss Style. The theme switcher on this page flips everything between them. The other 45 are one line away:

```js
Retro.apply(document.querySelector('.stage'), 'geocities'); // any of the 53 ids
```

```css
/* the same thing in plain CSS: repoint the roles on a container */
.stage { --ui-bg: var(--c64-bg); --ui-surface: var(--c64-surface); --ui-ink: var(--c64-ink); --ui-muted: var(--c64-muted);
  --ui-border: var(--c64-border); --ui-accent: var(--c64-accent); --ui-accent2: var(--c64-accent2);
  --ui-highlight: var(--c64-highlight); --ui-onaccent: var(--c64-onaccent); }
```

The SystemSwitcher component does exactly this, live, for all 53.

## The nine roles

| Role | What it is | Rule |
|---|---|---|
| `bg` | Page or desktop background. | Text goes on `surface`; check the table before setting text straight on `bg`. |
| `surface` | Windows, panels, the tube face of a CRT, the LCD of a Game Boy. | The default ground for text. |
| `ink` | Primary text. | 53 of 53 pass AA (4.5:1) on `surface`. |
| `muted` | Secondary text: captions, metadata, timestamps. | 38 pass AA, 10 only for large text, 5 fail. Check the table before using it under 18px. |
| `border` | Edges, rules, bevel and frame lines. | Decorative. Not tested for 3:1, so never the only boundary of a control. |
| `accent` | Title bars, primary buttons, links, the era's signature colour. | A fill. Text on it is `onaccent`. |
| `accent2` | A second signal colour. | A fill or large type; never text on `accent`. |
| `highlight` | Selection, glow, emphasis. | A fill, or the colour of a glow. |
| `onaccent` | Text and icons on an `accent` fill. | Picked per system from its own colours, never a new one. 49 of 53 reach AA; the rest pass for large text. |

## Visual foundations

**Colour.** Each palette is closed. Do not mix roles across systems: a `win95-accent` title bar on a `crt-surface` window is two eras at once and reads as a mistake. Want a hybrid? Make it a new system.

**Shape.** Square by default: `radius-0`. Radii exist for the glossy eras only (XP, Aqua, Web 2.0, Y2K, clay, glass), stepped at the values the source files use most: 2, 4, 8, 20 and 999px.

**Depth is drawn, not blurred.** Desktop-OS controls use `bevel-raised` and `bevel-sunken` (the Windows 95 greys); Memphis, Pop Art and System 7 use `hard-drop`, a 4px black offset. Phosphor and neon systems glow with a text-shadow in their own ink, as the CRT source does: `text-shadow: 0 0 4px var(--ui-ink), 0 0 10px var(--ui-ink)`.

**Texture** (scanlines, dithering, VHS tracking, pixel scaling with `image-rendering: pixelated`) belongs to the image and motion layer, not to tokens. The source demo pages draw it in CSS; copy from `styles/<slug>/index.html`.

**Spacing** is the TrillFx 4px spine (`space-1` 4px to `space-24` 96px), shared with Iron, Sludge and Night Terminal. The source eras space by eye, so nothing per-era was extracted.

## Type

Each system keeps its own `font-family` stack (first face in the table below; the full stack is in each system's data and `Retro.apply` sets it). The twelve `--font-*` families are verbatim stacks from representative systems: `pixel` (8-Bit Arcade), `terminal` (CRT), `dos` (Midnight Commander), `chicago` (System 7), `win` (Windows 95), `display` (Tron), `grotesk` (Swiss), `geometric` (Bauhaus), `serif`, `hand` (Wireframe), `mono` (Glitch) and `modern` (Glassmorphism). The type styles record the body size each era actually used: 11px for Windows 95, 20px for a CRT, 18px for DOS.

Free faces, all in one request:

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=VT323&family=Press+Start+2P&family=Orbitron:wght@400;700&family=Share+Tech+Mono&family=Space+Mono&family=Space+Grotesk:wght@400;700&family=Inter:wght@400;600&family=IBM+Plex+Mono&family=Kalam&family=Bungee&family=Nunito:wght@400;700&family=Patrick+Hand&family=Shadows+Into+Light&family=Rajdhani:wght@400;700&family=JetBrains+Mono&display=swap">
```

Chicago, MS Sans Serif, Geneva, Lucida Grande, Helvetica Neue, Akzidenz-Grotesk, Futura, Frutiger, Eurostile, Söhne, Topaz, Perfect DOS VGA 437, Px437, C64 Pro, IBM 3270 and Matrix Code NFI are not bundled. They render where installed and fall back down their stacks otherwise. To lock a look for the stage or a stream, add the font files under `fonts/` if you hold the rights to them.

## Voice

The TrillFx rule holds everywhere: direct, physical, short verbs, no hype. "Loop locked. 140 BPM." Each era adds a register on top. Keep one era per surface.

| Era | Write it like | Not like |
|---|---|---|
| Terminal, DOS, C64 | `READY.` `C:\>RENDER /ALL` `> LOOP 04 ARMED` | "Your loop is ready to go!" |
| Desktop OS | Title-case dialog labels: `OK`, `Cancel`, `Apply`. "Rendering 12 of 40 clips." | "Hang tight while we render" |
| Gaming, arcade | Capitals, scores, one word: `INSERT COIN`, `1UP`, `STAGE CLEAR` | Long sentences in Press Start 2P |
| Sci-fi | Clipped status: `SECTOR 7 ONLINE`, `END OF LINE` | Emoji, exclamation marks |
| Print & design | Sentence case, flush left: "Less, but better." | Centred capitals on everything |
| Web 1.0 | Earnest and loud, the one place `!!!` is allowed: "Welcome to my homepage!!!" | Corporate polish |

## Iconography

No icon set ships with the collection: the source systems draw controls in CSS and use Unicode glyphs. Use box-drawing characters (`─ │ ┌ ┐ └ ┘`) and block elements (`█ ▓ ▒ ░`) for terminal eras, simple geometric glyphs (`▶ ◀ ■ ▲ ●`) for the rest, in `ink`. Screenshots of nine systems and the repo poster are under Assets › Showcase: use them to check a build against the original.

## Accessibility

Primary text is safe everywhere: `ink` on `surface` passes AA in all 53 systems. Secondary text is where the eras show their age, and those values are kept as the originals had them and flagged in each token's note:

- `muted` fails outright in 5: Windows 95 (2.17:1), Amiga Workbench (2.79:1), Flat Design 2013 (2.56:1), Neumorphism (2.42:1), Hypnagogic (2.98:1). Use it for disabled or decorative text only.
- `muted` passes only at large sizes (18px, or 14px bold) in 10: Mac System 7 (3.54:1), Windows XP Luna (4.35:1), CRT Phosphor Terminal (4.09:1), Winamp Skin (3.2:1), Web 2.0 Glossy (4.41:1), Game Boy DMG (3.29:1), Tron Vector (3.4:1), Risograph (3.63:1), Commodore 64 BASIC (3.34:1), Wireframe Sketch (3.3:1).
- `onaccent` passes only at large sizes in 4: Web 2.0 Glossy (4.44:1), Flat Design 2013 (3.86:1), Neumorphism (3.07:1), Bauhaus (4.41:1). Title bars at 14px bold are fine; small button labels are not.

Many eras signal state by hue alone (red and green lamps, CGA magenta). Always pair colour with a label or a glyph. Motion from the VHS, glitch and Matrix systems stays at three flashes a second or fewer.

## The 53 systems

★ = native theme. Contrast columns are WCAG ratios on the system's own `surface`.

| # | System | Era · year | id | ink | muted | First font |
|---|---|---|---|---|---|---|
| 1 | Mac System 7 | Desktop OS · 1991 | `macsys7` | 21.0 AA | 3.54 large | Chicago |
| 2 | Windows 95 ★ | Desktop OS · 1995 | `win95` | 11.54 AA | 2.17 fail | MS Sans Serif |
| 3 | Windows XP Luna | Desktop OS · 2001 | `xpluna` | 17.21 AA | 4.35 large | Trebuchet MS |
| 4 | Mac OS X Aqua | Desktop OS · 2001 | `aqua` | 14.2 AA | 5.35 AA | Lucida Grande |
| 5 | Amiga Workbench | Desktop OS · 1985 | `amiga` | 8.03 AA | 2.79 fail | Topaz |
| 6 | NeXTSTEP | Desktop OS · 1989 | `nextstep` | 8.89 AA | 5.89 AA | Helvetica Neue |
| 7 | BeOS | Desktop OS · 1996 | `beos` | 13.48 AA | 6.66 AA | Swiss 721 |
| 8 | Teletext | Broadcast · 1974 | `teletext` | 21.0 AA | 16.75 AA | VT323 |
| 9 | CRT Phosphor Terminal ★ | Terminal · 1980 | `crt` | 13.5 AA | 4.09 large | VT323 |
| 10 | DOS CGA | Terminal · 1981 | `doscga` | 9.04 AA | 7.33 AA | Perfect DOS VGA 437 |
| 11 | 8-Bit Arcade ★ | Gaming · 1983 | `arcade` | 14.42 AA | 11.21 AA | Press Start 2P |
| 12 | Frutiger Aero | Web/UI · 2007 | `aero` | 10.52 AA | 10.52 AA | Frutiger |
| 13 | Winamp Skin | App · 1997 | `winamp` | 9.51 AA | 3.2 large | Helvetica Neue |
| 14 | GeoCities Web 1.0 | Web · 1996 | `geocities` | 19.56 AA | 16.75 AA | Comic Sans MS |
| 15 | Cassette Futurism | Sci-Fi · 1979 | `cassette` | 9.89 AA | 8.38 AA | Orbitron |
| 16 | Vaporwave ★ | Aesthetic · 2011 | `vaporwave` | 13.98 AA | 4.54 AA | Times New Roman |
| 17 | Memphis | Design · 1981 | `memphis` | 21.0 AA | 21.0 AA | Helvetica Neue |
| 18 | PS1 Tech | Gaming · 1994 | `ps1` | 11.68 AA | 7.82 AA | Eurostile |
| 19 | OS/2 Warp | Desktop OS · 1994 | `os2warp` | 11.54 AA | 5.7 AA | Helvetica |
| 20 | Mac OS 9 Platinum | Desktop OS · 1999 | `macos9` | 15.46 AA | 5.49 AA | Charcoal |
| 21 | Web 2.0 Glossy | Web/UI · 2005 | `web20` | 14.35 AA | 4.41 large | Lucida Grande |
| 22 | Game Boy DMG ★ | Gaming · 1989 | `gameboy` | 6.02 AA | 3.29 large | Press Start 2P |
| 23 | Braun / Dieter Rams | Design · 1960 | `braun` | 17.4 AA | 5.5 AA | Akzidenz-Grotesk |
| 24 | Tron Vector ★ | Sci-Fi · 1982 | `tron` | 11.08 AA | 3.4 large | Orbitron |
| 25 | VHS Tracking | Analog · 1980 | `vhs` | 17.14 AA | 12.22 AA | VT323 |
| 26 | Risograph ★ | Print · 1986 | `riso` | 13.08 AA | 3.63 large | Helvetica Neue |
| 27 | IBM 3270 Mainframe | Terminal · 1971 | `ibm3270` | 10.42 AA | 11.37 AA | IBM 3270 |
| 28 | NetHack ASCII | Terminal · 1987 | `nethack` | 16.52 AA | 8.03 AA | Px437 IBM VGA |
| 29 | TempleOS | Desktop OS · 2013 | `templeos` | 13.29 AA | 10.6 AA | Px437 IBM VGA 8x16 |
| 30 | BBS ANSI Art | Terminal · 1989 | `bbsansi` | 21.0 AA | 9.04 AA | Px437 IBM VGA 8x16 |
| 31 | Midnight Commander | Terminal · 1994 | `mc` | 5.72 AA | 5.72 AA | Px437 IBM VGA 8x16 |
| 32 | Matrix Rain | Sci-Fi · 1999 | `matrix` | 6.64 AA | 6.64 AA | Matrix Code NFI |
| 33 | btop Meters | Terminal · 2021 | `btop` | 14.27 AA | 4.51 AA | Hack |
| 34 | Commodore 64 BASIC | Terminal · 1982 | `c64` | 4.55 AA | 3.34 large | C64 Pro |
| 35 | Flat Design 2013 | Web/UI · 2013 | `flat2013` | 9.29 AA | 2.56 fail | Helvetica Neue Light |
| 36 | Glassmorphism | Web/UI · 2020 | `glass` | 8.02 AA | 4.91 AA | Inter |
| 37 | Neumorphism | Web/UI · 2020 | `neumorph` | 5.94 AA | 2.42 fail | Inter |
| 38 | Blueprint / CAD | Technical · 1980 | `blueprint` | 12.95 AA | 4.53 AA | Helvetica Neue |
| 39 | Claymorphism | Web/UI · 2021 | `clay` | 12.17 AA | 4.64 AA | Nunito |
| 40 | Brutalist Web | Web/UI · 2016 | `brutalist` | 15.91 AA | 15.91 AA | Times New Roman |
| 41 | Swiss Style ★ | Design · 1950 | `swiss` | 17.82 AA | 4.87 AA | Helvetica Neue |
| 42 | Bauhaus | Design · 1919 | `bauhaus` | 16.65 AA | 16.65 AA | Futura |
| 43 | Pop Art | Art · 1960 | `popart` | 14.8 AA | 14.8 AA | Bungee |
| 44 | Op Art | Art · 1964 | `opart` | 18.16 AA | 18.16 AA | Helvetica Neue |
| 45 | Hypnagogic | Aesthetic · 2015 | `hypnagogic` | 10.91 AA | 2.98 fail | Times New Roman |
| 46 | Monochrome Zen | Design · 2010 | `zen` | 18.93 AA | 18.93 AA | Söhne |
| 47 | Default Browser | Web · 1994 | `browser` | 21.0 AA | 21.0 AA | Times New Roman |
| 48 | Wireframe Sketch | Technical · 2010 | `wireframe` | 13.73 AA | 3.3 large | Kalam |
| 49 | Glitch Databend | Aesthetic · 2010 | `glitch` | 17.37 AA | 17.37 AA | Space Mono |
| 50 | Y2K Chrome | Aesthetic · 2000 | `y2k` | 16.02 AA | 5.95 AA | Neue Haas Grotesk |
| 51 | Duotone Poster | Print · 2015 | `duotone` | 14.01 AA | 14.01 AA | Futura |
| 52 | Grid Paper | Technical · 1980 | `gridpaper` | 13.9 AA | 6.71 AA | Shadows Into Light |
| 53 | Maximalist 90s Banner | Web · 1997 | `maximalist` | 19.56 AA | 19.56 AA | Comic Sans MS |

### Notes by system

- **Mac System 7** (`macsys7`): Monochrome by design: System 7 draws UI in black, white and greys, and shows selection by inversion, so the accent is black.
- **Windows 95** (`win95`): `muted` is Windows disabled-text grey (#808080); it fails as body text on the silver chrome. Use it for disabled states only.
- **Windows XP Luna** (`xpluna`): Blue page background is the middle stop of the Bliss-sky body gradient; Start-button green is `accent2`.
- **Mac OS X Aqua** (`aqua`): Gel buttons are radial gradients in the source; the traffic-light body colours (red/yellow) are used flat.
- **Amiga Workbench** (`amiga`): Workbench 1.x four-colour palette has no secondary-text tone; `muted` reuses the desktop blue and fails on the grey window.
- **NeXTSTEP** (`nextstep`): Greyscale by design; no hue anywhere in the NeXT palette.
- **Teletext** (`teletext`): Teletext has no grey; secondary text is cyan, as on Ceefax. Page background is the #1a1a1a around the black "TV".
- **CRT Phosphor Terminal** (`crt`): Two-colour phosphor: green text plus an amber alert. Page is #000; the tube face is #001a00.
- **DOS CGA** (`doscga`): Body is grey-on-blue DOS; the black surface is the terminal window.
- **8-Bit Arcade** (`arcade`): `surface` is the purple glow at the top of the page (#1a1440), from the body gradient.
- **Frutiger Aero** (`aero`): Surface is 35% white glass. Contrast is measured with the glass composited over the sky. No secondary-text tone in source; `muted` = `ink`.
- **Winamp Skin** (`winamp`): LCD green is the accent; page is the dark #0e0e12 behind the skin.
- **GeoCities Web 1.0** (`geocities`): Black starfield with yellow text. Default link blue (#0000ee) is kept out of the text roles: it measures 2.2:1 on black.
- **Cassette Futurism** (`cassette`): Amber instrument panel with red WARN and green OK lamps.
- **Vaporwave** (`vaporwave`): `surface` is the deep purple second stop of the sunset body gradient.
- **Memphis** (`memphis`): Primaries on white with black outlines; no grey tone by design.
- **Game Boy DMG** (`gameboy`): The four DMG greens (#0f380f to #9bbc0f) are the UI; the grey shell is used as the page so the device reads as one piece. The source page itself is near-black (#1a1a22).
- **Risograph** (`riso`): Two-ink print: text in black, secondary text in riso blue.
- **TempleOS** (`templeos`): 16-colour VGA; no grey, so secondary text is cyan.
- **Midnight Commander** (`mc`): Grey-on-blue panels; the palette has no dimmer text tone, so `muted` = `ink`.
- **Matrix Rain** (`matrix`): The dim green (#003b00) is trail colour only (1.7:1); `muted` = `ink`.
- **Commodore 64 BASIC** (`c64`): Page is the light-blue C64 border; the dark-blue screen is the surface.
- **Flat Design 2013** (`flat2013`): Flat grey caption text (#95a5a6) fails on both grounds, as it did in 2013. Keep it for large labels only.
- **Neumorphism** (`neumorph`): The known neumorphism problem: soft grey text measures under 3:1. Surfaces equal the background and differ only by shadow.
- **Brutalist Web** (`brutalist`): Raw HTML: values are the few literal colours in the source file. `a:hover` red (#ff0000) is not mapped.
- **Swiss Style** (`swiss`): Black, paper and one red by design.
- **Bauhaus** (`bauhaus`): Three primaries and black on paper; no grey by design.
- **Op Art** (`opart`): Black, white and one red by design.
- **Monochrome Zen** (`zen`): Monochrome by design; the only non-ink value is the 15% hairline.
- **Default Browser** (`browser`): The source uses no stylesheet at all, so every value is the browser default it relies on (documented per token).
- **Wireframe Sketch** (`wireframe`): Greyscale by design; the accent is the pale highlighter fill.
- **Duotone Poster** (`duotone`): Paper plus two spot inks by design.
- **Grid Paper** (`gridpaper`): Grid lines and highlighter are translucent in the source and kept that way.
- **Maximalist 90s Banner** (`maximalist`): Magenta/cyan/yellow stripes with black text; no grey by design.

## Method

Values come from two places in the source repo and nowhere else: each system's generated `tokens/<slug>.css`, and the `body` rule of its demo page `styles/<slug>/index.html`. Every role is one of four things:

1. A source custom property, named in the token note (`--chrome`).
2. One colour stop of a source gradient, named with its stop number (XP's sky, Aqua's chrome and gel buttons, the Start-button green, the arcade glow, the vaporwave sunset, the glass background).
3. A literal colour copied from the demo page (a `body` background, a white card). The build fails if the literal is not in that file.
4. An alias of another role of the same system, when the era has no distinct tone.

Two deliberate exceptions: Default Browser has no stylesheet at all, so its values are the browser defaults its page relies on; Game Boy DMG uses its grey shell as the page so the device reads as one piece (the demo page itself is near-black). `onaccent` is computed: of the system's own ink, surface, bg and highlight, whichever reads best on its accent.

Not extracted: spacing (the TrillFx spine is used), per-era radii and shadows (the shared scales are stepped from what the sources use most), motion and texture.

## Credits and license

Original collection: *Retro Design System* by NovusGFX, released under the MIT License. Tokens, notes, components and this book are a derivative work and keep that notice:

```text
MIT License

Copyright (c) 2026 NovusGFX
Copyright (c) 2026 Levi Trillfonix / TrillFx (design-system/ and the TrillFx additions)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
