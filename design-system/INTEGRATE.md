# Use the Retro systems in your apps

The 53 original styles are untouched in `styles/`, `tokens/` and `manifest.json`. This guide covers the drop-in kit in `design-system/dist/`, built from those same colours. Nothing here changes the originals.

## Fastest way: one CSS file, one attribute

Copy `design-system/dist/retro.css` into your app, then:

```html
<link rel="stylesheet" href="retro.css">
<body data-retro="win95">
  <div class="retro-panel">
    <button class="retro-btn">Cancel</button>
    <button class="retro-btn retro-btn--primary">OK</button>
  </div>
</body>
```

`data-retro` works on any element, so one page can mix eras (a CRT panel inside a Windows 95 window). Open `design-system/dist/example.html` to see all 53 switch live.

In your own CSS, style with the nine roles and your components re-skin for free:

```css
.card   { background: var(--ui-surface); color: var(--ui-ink); border: 2px solid var(--ui-border); }
.card h2 { color: var(--ui-accent2); }
.cta    { background: var(--ui-accent); color: var(--ui-onaccent); }   /* onaccent is always readable on accent */
```

| Role | Use |
|---|---|
| `--ui-bg` | page / desktop ground |
| `--ui-surface` | windows, cards, inputs |
| `--ui-ink` | main text |
| `--ui-muted` | secondary text (check contrast for the systems flagged in the brand book) |
| `--ui-border` | rules, window frames |
| `--ui-accent` | primary action, title bars |
| `--ui-accent2` | links, secondary highlight |
| `--ui-highlight` | selection, focus ring |
| `--ui-onaccent` | text on `accent` |
| `--ui-font`, `--ui-size` | the system's own font stack and body size |

## Switch from JavaScript

```html
<script src="retro.js"></script>
<script>
  Retro.set("crt");                                 // theme <body>
  Retro.set("vaporwave", document.querySelector("#panel"));   // or any element
  Retro.restore("win95");                           // last remembered choice, else win95
  Retro.picker(document.querySelector("#settings"));          // a ready <select> of all 53
</script>
```

## React, Vue, Svelte, Electron, Tauri

Import `retro.css` once at the entry point and set the attribute from state:

```jsx
import "./retro.css";
export default function App({ system = "win95" }) {
  return <div data-retro={system}>...</div>;
}
```

## Python, C#, native GUIs

`retro.json` has every system's nine colours, font stack and body size, so toolkits that are not CSS (Tkinter, Qt, WPF) can read it directly:

```python
import json
ds = json.load(open("retro.json", encoding="utf-8"))
win95 = next(s for s in ds["systems"] if s["id"] == "win95")
bg, ink, accent = win95["roles"]["bg"], win95["roles"]["ink"], win95["roles"]["accent"]
```

## Fonts

Each system lists its era font first (Chicago, MS Sans Serif, Topaz and so on) then fallbacks. The era fonts are not bundled, so most machines show the fallback. Bundle fonts you have the right to ship and keep the same `--ui-font` stack.

## Accessibility

`ink` on `surface` passes WCAG AA in all 53. `muted` and `onaccent` are the originals' own colours and a few fall short of AA for small text; the table is in `contrast-report.md`. Check it before using those roles for body text.

## Ids

| # | id | System | Era | Year |
|---|---|---|---|---|
| 01 | `macsys7` | Mac System 7 | Desktop OS | 1991 |
| 02 | `win95` | Windows 95 | Desktop OS | 1995 |
| 03 | `xpluna` | Windows XP Luna | Desktop OS | 2001 |
| 04 | `aqua` | Mac OS X Aqua | Desktop OS | 2001 |
| 05 | `amiga` | Amiga Workbench | Desktop OS | 1985 |
| 06 | `nextstep` | NeXTSTEP | Desktop OS | 1989 |
| 07 | `beos` | BeOS | Desktop OS | 1996 |
| 08 | `teletext` | Teletext | Broadcast | 1974 |
| 09 | `crt` | CRT Phosphor Terminal | Terminal | 1980 |
| 10 | `doscga` | DOS CGA | Terminal | 1981 |
| 11 | `arcade` | 8-Bit Arcade | Gaming | 1983 |
| 12 | `aero` | Frutiger Aero | Web/UI | 2007 |
| 13 | `winamp` | Winamp Skin | App | 1997 |
| 14 | `geocities` | GeoCities Web 1.0 | Web | 1996 |
| 15 | `cassette` | Cassette Futurism | Sci-Fi | 1979 |
| 16 | `vaporwave` | Vaporwave | Aesthetic | 2011 |
| 17 | `memphis` | Memphis | Design | 1981 |
| 18 | `ps1` | PS1 Tech | Gaming | 1994 |
| 19 | `os2warp` | OS/2 Warp | Desktop OS | 1994 |
| 20 | `macos9` | Mac OS 9 Platinum | Desktop OS | 1999 |
| 21 | `web20` | Web 2.0 Glossy | Web/UI | 2005 |
| 22 | `gameboy` | Game Boy DMG | Gaming | 1989 |
| 23 | `braun` | Braun / Dieter Rams | Design | 1960 |
| 24 | `tron` | Tron Vector | Sci-Fi | 1982 |
| 25 | `vhs` | VHS Tracking | Analog | 1980 |
| 26 | `riso` | Risograph | Print | 1986 |
| 27 | `ibm3270` | IBM 3270 Mainframe | Terminal | 1971 |
| 28 | `nethack` | NetHack ASCII | Terminal | 1987 |
| 29 | `templeos` | TempleOS | Desktop OS | 2013 |
| 30 | `bbsansi` | BBS ANSI Art | Terminal | 1989 |
| 31 | `mc` | Midnight Commander | Terminal | 1994 |
| 32 | `matrix` | Matrix Rain | Sci-Fi | 1999 |
| 33 | `btop` | btop Meters | Terminal | 2021 |
| 34 | `c64` | Commodore 64 BASIC | Terminal | 1982 |
| 35 | `flat2013` | Flat Design 2013 | Web/UI | 2013 |
| 36 | `glass` | Glassmorphism | Web/UI | 2020 |
| 37 | `neumorph` | Neumorphism | Web/UI | 2020 |
| 38 | `blueprint` | Blueprint / CAD | Technical | 1980 |
| 39 | `clay` | Claymorphism | Web/UI | 2021 |
| 40 | `brutalist` | Brutalist Web | Web/UI | 2016 |
| 41 | `swiss` | Swiss Style | Design | 1950 |
| 42 | `bauhaus` | Bauhaus | Design | 1919 |
| 43 | `popart` | Pop Art | Art | 1960 |
| 44 | `opart` | Op Art | Art | 1964 |
| 45 | `hypnagogic` | Hypnagogic | Aesthetic | 2015 |
| 46 | `zen` | Monochrome Zen | Design | 2010 |
| 47 | `browser` | Default Browser | Web | 1994 |
| 48 | `wireframe` | Wireframe Sketch | Technical | 2010 |
| 49 | `glitch` | Glitch Databend | Aesthetic | 2010 |
| 50 | `y2k` | Y2K Chrome | Aesthetic | 2000 |
| 51 | `duotone` | Duotone Poster | Print | 2015 |
| 52 | `gridpaper` | Grid Paper | Technical | 1980 |
| 53 | `maximalist` | Maximalist 90s Banner | Web | 1997 |

## Rebuild

```bash
python design-system/build/build.py        # roles, tokens, brand book (writes systems.json)
python design-system/build/dist.py         # this kit
```
