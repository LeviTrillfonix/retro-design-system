/** The nine roles every system defines; `ui-<role>` is the active one. */
export type RetroRole = 'bg' | 'surface' | 'ink' | 'muted' | 'border' | 'accent' | 'accent2' | 'highlight' | 'onaccent';
export interface RetroSystem { num: number; id: string; name: string; era: string; year: number | null; tags: string[]; font: string; featured: boolean }
/** Plain DOM, no React: each component takes a host element and returns what it built. */
export interface RetroWindowProps { /** system id, e.g. "win95"; omit to follow the page's theme */ system?: string; title?: string; text?: string; caption?: string }
export declare function RetroWindow(el: HTMLElement, props?: RetroWindowProps): HTMLElement;
export interface SystemSwitcherProps { /** system id shown first */ initial?: string; onChange?: (system: RetroSystem) => void }
export declare function SystemSwitcher(el: HTMLElement, props?: SystemSwitcherProps): { set(id: string): void; get(): RetroSystem };
export interface PaletteGridProps { onSelect?: (system: RetroSystem) => void }
export declare function PaletteGrid(el: HTMLElement, props?: PaletteGridProps): HTMLTableElement;
/** Point the ui-* roles (and font-family) of `el` at any of the 53 systems. */
export declare function apply(el: HTMLElement, id: string): RetroSystem;
export declare function reset(el: HTMLElement): void;
export declare function contrast(id: string, fg: RetroRole, ground: RetroRole): number;
declare global { interface Window { Retro: { systems: RetroSystem[]; roles: RetroRole[]; featured: string[]; apply: typeof apply; reset: typeof reset; contrast: typeof contrast; byId(id: string): RetroSystem | null; RetroWindow: typeof RetroWindow; SystemSwitcher: typeof SystemSwitcher; PaletteGrid: typeof PaletteGrid } } }
