# TrillFx Retro Design System

> 53 retro UI eras as one switchable design system, built for TrillFx audio-visual work: VJ overlays, tool GUIs, stream graphics and show flyers. Based on NovusGFX's *Retro Design System* (MIT).

![Retro Design Systems social poster](./assets/social-poster.png)

[![GitHub stars](https://img.shields.io/github/stars/LeviTrillfonix/retro-design-system?style=for-the-badge)](https://github.com/LeviTrillfonix/retro-design-system/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/LeviTrillfonix/retro-design-system?style=for-the-badge)](https://github.com/LeviTrillfonix/retro-design-system/commits/main)
[![Systems](https://img.shields.io/badge/systems-53-ff2d95?style=for-the-badge)](./design-system/project/README.md)
[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](./LICENSE)

Use it in your apps: [design-system/INTEGRATE.md](./design-system/INTEGRATE.md). The original README is [README.md](./README.md).

## What TrillFx adds

The original 53 standalone styles are unchanged in `styles/`, `tokens/` and `manifest.json`. On top of them, `design-system/` turns the collection into one token set:

- **Nine shared roles** (`bg`, `surface`, `ink`, `muted`, `border`, `accent`, `accent2`, `highlight`, `onaccent`), mapped for every system from its own source values: 486 colour tokens, none invented.
- **Any element, any era.** `Retro.apply(el, 'win95')` re-skins an element and everything in it; in plain CSS, repoint the nine `--ui-*` custom properties.
- **Components** in plain JavaScript, no framework: RetroWindow, SystemSwitcher (all 53, live) and PaletteGrid.
- **A brand book** with roles, type, voice by era, iconography and a WCAG contrast audit of all 53: [`design-system/project/README.md`](./design-system/project/README.md).
- **A reproducible build.** Every colour is traced to a source file, and the build stops if a hand-picked colour is not in its source.

### Build

```bash
python design-system/build/build.py            # tokens, components, brand book
python design-system/build/build.py --verify   # + render every preview headless
                                               #   (pip install playwright; playwright install chromium)
```

| Path | What |
|---|---|
| `design-system/project/` | The design system itself: `tokens.json`, the brand book, `components/` (bundle, styles, types, previews, cover). The same files the TrillFx Design System artifact holds. |
| `design-system/build/` | `extract.py` (source values to roles, contrast), `gen.py` (tokens and components), `readme.py` (brand book), `verify.py` (headless render check), `build.py` (runs them in order). |
| `design-system/systems.json` | All 53 systems resolved: roles, sources, fonts, contrast. |
| `design-system/contrast-report.md` | The contrast table on its own. |

### Staying in sync with the original

This repo is a fork of [NovusGFX/retro-design-system](https://github.com/NovusGFX/retro-design-system). To pull in new styles:

```bash
git remote add upstream https://github.com/NovusGFX/retro-design-system.git   # once
git fetch upstream && git merge upstream/main
python design-system/build/build.py --verify
```

A new style needs an id and a role mapping in `design-system/build/extract.py`; the build stops and names any system that has none. The original README.md is kept exactly as upstream wrote it, so upstream merges stay clean.

## Credits

The original collection, its 53 styles, screenshots and tooling are by **NovusGFX**, MIT. The `design-system/` layer and this header are by **Levi Trillfonix / TrillFx**, MIT. The original MIT notice is in [LICENSE](./LICENSE); the TrillFx notice is in [design-system/LICENSE](./design-system/LICENSE).
