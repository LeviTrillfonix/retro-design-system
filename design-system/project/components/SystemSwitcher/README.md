# SystemSwitcher

Live-switches a preview window between all 53 systems, past the artifact's 8-native-theme limit.

- It calls `Retro.apply(el, id)`, which points the nine `ui-*` custom properties of one element at `--<id>-<role>` and sets that system's `font-family`. Everything inside re-skins; the page around it keeps its own theme.
- The side panel shows the nine resolved colours and live WCAG ratios for ink and muted text on the surface, measured the same way as the README table.
- A star marks the eight systems that are also native themes (theme switcher above).
- Use the same call in your own pages: `Retro.apply(document.body, 'vaporwave')`.
