# RetroWindow

A classic window (title bar, body copy, buttons, a field) drawn entirely from the nine `ui-*` roles, so it re-skins to whichever system is active.

- With no `system` it follows the page's theme; pass `system: "c64"` (any of the 53 ids) to pin it.
- Title bar is `ui-accent` with `ui-onaccent` text; the primary button repeats that pair. Everything else is `ui-ink` on `ui-surface`.
- Consumer provides the host element and the copy. Keep copy era-true: short, literal, no exclamation marks except on GeoCities.
