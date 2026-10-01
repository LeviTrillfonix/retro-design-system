#!/usr/bin/env python3
"""Write project/README.md (the brand book). All counts are computed from systems.json."""
import json, os, re

# Paths: this file lives in design-system/build/ of the repo.
DS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # design-system/
REPO = os.path.dirname(DS)                                          # repo root
HERE = DS
S = json.load(open(os.path.join(HERE, 'systems.json'), encoding='utf-8'))
G = json.load(open(os.path.join(HERE, 'gen-meta.json'), encoding='utf-8'))
BY = {s['id']: s for s in S}
FEAT = G['featured']
LICENSE = open(os.path.join(REPO, 'LICENSE'), encoding='utf-8').read().strip()

def g(r): return 'AA' if r >= 4.5 else ('large' if r >= 3 else 'fail')
def cnt(key):
    d = {'AA': 0, 'large': 0, 'fail': 0}
    for s in S: d[g(s['contrast'][key])] += 1
    return d
def names(key, grade):
    return ', '.join(f"{s['name']} ({s['contrast'][key]}:1)" for s in S if g(s['contrast'][key]) == grade)
def first_face(stack):
    return re.match(r'\s*"?([^",]+)', stack).group(1)

ink, mut, oa = cnt('ink_surface'), cnt('muted_surface'), cnt('onaccent_accent')
GF = ('https://fonts.googleapis.com/css2?family=VT323&family=Press+Start+2P&family=Orbitron:wght@400;700'
      '&family=Share+Tech+Mono&family=Space+Mono&family=Space+Grotesk:wght@400;700&family=Inter:wght@400;600'
      '&family=IBM+Plex+Mono&family=Kalam&family=Bungee&family=Nunito:wght@400;700&family=Patrick+Hand'
      '&family=Shadows+Into+Light&family=Rajdhani:wght@400;700&family=JetBrains+Mono&display=swap')
feat_names = ', '.join(BY[t]['name'].replace(' Terminal', '') for t in FEAT)
eras = []
for s in S:
    if s['era'] not in eras: eras.append(s['era'])

rows = []
for s in S:
    c = s['contrast']
    star = ' ★' if s['id'] in FEAT else ''
    rows.append(f"| {s['num']} | {s['name']}{star} | {s['era']} · {s['year']} | `{s['id']}` | {c['ink_surface']} {g(c['ink_surface'])} | {c['muted_surface']} {g(c['muted_surface'])} | {first_face(s['font'])} |")
notes = '\n'.join(f"- **{s['name']}** (`{s['id']}`): {s['note']}" for s in S if s['note'])

md = f'''# Retro Design System

Fifty-three interface eras, from Mac System 7 to 90s banner ads, kept as one token set. Every era keeps its own palette and type; a nine-role layer makes any one of them the live skin for a window, an overlay, a flyer or a whole page. Built for TrillFx: VJ overlays, tool GUIs like VJToolbox, stream graphics and show flyers.

The source is NovusGFX's MIT-licensed *Retro Design System* collection, mirrored at `github.com/LeviTrillfonix/retro-design-system` (commit `911d9b1`). Every colour here is one of that repo's own values; nothing was invented. Credits and the license are at the end.

## How it is built

Three layers, from raw to live:

1. **System palettes.** Each of the 53 systems has nine colour tokens named `<id>-<role>`: `win95-accent`, `crt-ink`, `vaporwave-surface`. They are listed per system in Colors, in era order. Where a system has no distinct tone for a role, the token is an alias of another role (`swiss-accent2` is `{{swiss-ink}}`) rather than a repeated hex.
2. **The role layer.** Nine `ui-*` tokens (`ui-bg` to `ui-onaccent`) always hold the active system. Components, the cover and anything you build should use only these.
3. **Switching.** This artifact allows eight native themes, so eight featured systems are themes, marked ★ below: {feat_names}. The theme switcher on this page flips everything between them. The other 45 are one line away:

```js
Retro.apply(document.querySelector('.stage'), 'geocities'); // any of the 53 ids
```

```css
/* the same thing in plain CSS: repoint the roles on a container */
.stage {{ --ui-bg: var(--c64-bg); --ui-surface: var(--c64-surface); --ui-ink: var(--c64-ink); --ui-muted: var(--c64-muted);
  --ui-border: var(--c64-border); --ui-accent: var(--c64-accent); --ui-accent2: var(--c64-accent2);
  --ui-highlight: var(--c64-highlight); --ui-onaccent: var(--c64-onaccent); }}
```

The SystemSwitcher component does exactly this, live, for all 53.

## The nine roles

| Role | What it is | Rule |
|---|---|---|
| `bg` | Page or desktop background. | Text goes on `surface`; check the table before setting text straight on `bg`. |
| `surface` | Windows, panels, the tube face of a CRT, the LCD of a Game Boy. | The default ground for text. |
| `ink` | Primary text. | {ink['AA']} of 53 pass AA (4.5:1) on `surface`. |
| `muted` | Secondary text: captions, metadata, timestamps. | {mut['AA']} pass AA, {mut['large']} only for large text, {mut['fail']} fail. Check the table before using it under 18px. |
| `border` | Edges, rules, bevel and frame lines. | Decorative. Not tested for 3:1, so never the only boundary of a control. |
| `accent` | Title bars, primary buttons, links, the era's signature colour. | A fill. Text on it is `onaccent`. |
| `accent2` | A second signal colour. | A fill or large type; never text on `accent`. |
| `highlight` | Selection, glow, emphasis. | A fill, or the colour of a glow. |
| `onaccent` | Text and icons on an `accent` fill. | Picked per system from its own colours, never a new one. {oa['AA']} of 53 reach AA; the rest pass for large text. |

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
<link rel="stylesheet" href="{GF}">
```

Chicago, MS Sans Serif, Geneva, Lucida Grande, Helvetica Neue, Akzidenz-Grotesk, Futura, Frutiger, Eurostile, Söhne, Topaz, Perfect DOS VGA 437, Px437, C64 Pro, IBM 3270 and Matrix Code NFI are not bundled. They render where installed and fall back down their stacks otherwise. To lock a look for the stage or a stream, add the font files under `fonts/` if you hold the rights to them.

## Voice

The TrillFx rule holds everywhere: direct, physical, short verbs, no hype. "Loop locked. 140 BPM." Each era adds a register on top. Keep one era per surface.

| Era | Write it like | Not like |
|---|---|---|
| Terminal, DOS, C64 | `READY.` `C:\\>RENDER /ALL` `> LOOP 04 ARMED` | "Your loop is ready to go!" |
| Desktop OS | Title-case dialog labels: `OK`, `Cancel`, `Apply`. "Rendering 12 of 40 clips." | "Hang tight while we render" |
| Gaming, arcade | Capitals, scores, one word: `INSERT COIN`, `1UP`, `STAGE CLEAR` | Long sentences in Press Start 2P |
| Sci-fi | Clipped status: `SECTOR 7 ONLINE`, `END OF LINE` | Emoji, exclamation marks |
| Print & design | Sentence case, flush left: "Less, but better." | Centred capitals on everything |
| Web 1.0 | Earnest and loud, the one place `!!!` is allowed: "Welcome to my homepage!!!" | Corporate polish |

## Iconography

No icon set ships with the collection: the source systems draw controls in CSS and use Unicode glyphs. Use box-drawing characters (`─ │ ┌ ┐ └ ┘`) and block elements (`█ ▓ ▒ ░`) for terminal eras, simple geometric glyphs (`▶ ◀ ■ ▲ ●`) for the rest, in `ink`. Screenshots of nine systems and the repo poster are under Assets › Showcase: use them to check a build against the original.

## Accessibility

Primary text is safe everywhere: `ink` on `surface` passes AA in all {ink['AA']} systems. Secondary text is where the eras show their age, and those values are kept as the originals had them and flagged in each token's note:

- `muted` fails outright in {mut['fail']}: {names('muted_surface', 'fail')}. Use it for disabled or decorative text only.
- `muted` passes only at large sizes (18px, or 14px bold) in {mut['large']}: {names('muted_surface', 'large')}.
- `onaccent` passes only at large sizes in {oa['large']}: {names('onaccent_accent', 'large')}. Title bars at 14px bold are fine; small button labels are not.

Many eras signal state by hue alone (red and green lamps, CGA magenta). Always pair colour with a label or a glyph. Motion from the VHS, glitch and Matrix systems stays at three flashes a second or fewer.

## The 53 systems

★ = native theme. Contrast columns are WCAG ratios on the system's own `surface`.

| # | System | Era · year | id | ink | muted | First font |
|---|---|---|---|---|---|---|
''' + '\n'.join(rows) + f'''

### Notes by system

{notes}

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
{LICENSE}
```
'''
open(os.path.join(HERE, 'project', 'README.md'), 'w', encoding='utf-8', newline='\n').write(md)
print('README bytes:', len(md.encode()), '| ink', ink, '| muted', mut, '| onaccent', oa)
