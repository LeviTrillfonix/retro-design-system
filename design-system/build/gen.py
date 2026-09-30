#!/usr/bin/env python3
"""Step 3: write the Design System files under project/ from systems.json."""
import json, os, datetime

# Paths: this file lives in design-system/build/ of the repo.
DS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # design-system/
REPO = os.path.dirname(DS)                                          # repo root
HERE = DS
P = os.path.join(HERE, 'project')
S = json.load(open(os.path.join(HERE, 'systems.json'), encoding='utf-8'))
BY = {s['id']: s for s in S}
ROLES = ['bg', 'surface', 'ink', 'muted', 'border', 'accent', 'accent2', 'highlight', 'onaccent']
FEATURED = ['crt', 'vaporwave', 'win95', 'arcade', 'tron', 'gameboy', 'riso', 'swiss']
TITLE = 'Retro Design System'
NOW = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

ROLE_DOC = {
 'bg': 'Page / desktop background.',
 'surface': 'Window, panel or screen surface; body text sits here.',
 'ink': 'Primary text, on surface and bg.',
 'muted': 'Secondary text: captions, metadata.',
 'border': 'Borders, rules, bevel and frame edges.',
 'accent': 'Primary accent: title bars, primary buttons, links.',
 'accent2': 'Secondary accent: a second signal colour.',
 'highlight': 'Selection, glow and emphasis.',
 'onaccent': 'Text and icons on an accent fill.',
}

def grade(r):
    return 'AA' if r >= 4.5 else ('AA large text only' if r >= 3 else 'fails, decorative or disabled use only')

def w(path, text):
    full = os.path.join(P, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8', newline='\n').write(text)

# ------------------------------------------------------------------ tokens.json
tokens = []
for r in ROLES:
    tokens.append({
        'name': f'ui-{r}',
        'value': {t: '{' + f'{t}-{r}' + '}' for t in FEATURED},
        'usage': f'Active system: {ROLE_DOC[r]} Each theme points it at that system\'s `<id>-{r}`; Retro.apply() repoints it to any of the 53.',
    })
for s in S:
    c = s['contrast']
    for r in ROLES:
        spec = s['roles'][r]
        value = '{' + f"{s['id']}-{spec['alias']}" + '}' if 'alias' in spec else spec['value']
        u = f"{s['name']}: {ROLE_DOC[r]} Source: {spec['src']}."
        if r == 'bg':
            u = f"{s['name']} ({s['era']}, {s['year']}): {ROLE_DOC[r]} Source: {spec['src']}."
            if s['note']: u += ' ' + s['note']
        if r == 'ink':
            u += f" {c['ink_surface']}:1 on surface ({grade(c['ink_surface'])}), {c['ink_bg']}:1 on bg."
        if r == 'muted':
            u += f" {c['muted_surface']}:1 on surface ({grade(c['muted_surface'])})."
        if r == 'onaccent':
            u = f"{s['name']}: {ROLE_DOC[r]} {spec['src'][0].upper() + spec['src'][1:]}; {grade(c['onaccent_accent'])}."
        tokens.append({'name': f"{s['id']}-{r}", 'value': value, 'usage': u[:1000]})

assert len(tokens) <= 600, len(tokens)
names = [t['name'] for t in tokens]
assert len(names) == len(set(names))

def fam(sid, key='font'):
    return BY[sid]['font'] if key == 'font' else BY[sid]['fontAlt'][key]

families = {
    'pixel': fam('arcade'),
    'terminal': fam('crt'),
    'dos': fam('mc'),
    'chicago': fam('macsys7'),
    'win': fam('win95'),
    'display': fam('tron'),
    'grotesk': fam('swiss'),
    'geometric': fam('bauhaus'),
    'serif': fam('hypnagogic'),
    'hand': fam('wireframe'),
    'mono': fam('glitch'),
    'modern': fam('glass'),
}
for k, v in families.items():
    assert not any(ch in v for ch in ';{}<>\\()'), (k, v)

def st(name, family, size, lh, weight, sample, usage, **kw):
    d = {'name': name, 'family': family, 'fontSize': size, 'lineHeight': lh, 'fontWeight': weight, 'sample': sample, 'usage': usage}
    d.update(kw); return d

type_ = {
    'fonts': [],
    'families': families,
    'groups': [
        {'name': 'Screen & terminal', 'family': 'terminal',
         'note': 'Bitmap and CRT faces. VT323, Press Start 2P and IBM Plex Mono are free Google Fonts; the DOS and C64 faces fall back to VT323.',
         'styles': [
            st('pixel-display', 'pixel', '24px', '32px', 400, 'INSERT COIN', 'Arcade and Game Boy headlines. Press Start 2P runs about 1em per letter: short labels only.'),
            st('pixel-body', 'pixel', '14px', '22px', 400, 'PLAYER 1 READY', '8-Bit Arcade body size (14px in the source).'),
            st('terminal', 'terminal', '20px', '24px', 400, '> RUN VJTOOLBOX.EXE', 'CRT phosphor body size (20px in the source); VT323 reads small, so 20px is its body size.'),
            st('dos', 'dos', '18px', '18px', 400, 'C:\\>DIR /W', 'DOS, BBS, TempleOS and Midnight Commander body size (18px in the sources).'),
         ]},
        {'name': 'Desktop OS', 'family': 'win',
         'note': 'Chicago and MS Sans Serif are not web fonts; these stacks fall back to Geneva/Tahoma. Keep the small sizes: they are what makes the era.',
         'styles': [
            st('os-title', 'chicago', '12px', '16px', 700, 'About This Macintosh', 'Mac System 7 / OS 9 titles (12px in the source).'),
            st('os-body', 'win', '11px', '14px', 400, 'Start', 'Windows 95 / XP body size (11px in the sources).'),
         ]},
        {'name': 'Sci-fi display', 'family': 'display',
         'styles': [
            st('display', 'display', '28px', '32px', 700, 'END OF LINE', 'Tron, PS1 and cassette-futurism headings. Orbitron is a free Google Font.', letterSpacing='0.08em'),
            st('display-body', 'display', '14px', '20px', 400, 'Grid bike 2 online', 'Tron Vector body size (14px in the source).'),
         ]},
        {'name': 'Print & design', 'family': 'grotesk',
         'note': 'Akzidenz, Futura and Helvetica are licensed; the stacks fall back to Helvetica/Arial and Century Gothic.',
         'styles': [
            st('grotesk-display', 'grotesk', '48px', '48px', 700, 'Form follows function', 'Swiss and Braun headlines; flush left, tight.', letterSpacing='-0.02em'),
            st('grotesk-body', 'grotesk', '15px', '22px', 400, 'Less, but better.', 'Swiss, Braun and Risograph body size (15px in the sources).'),
            st('geometric-display', 'geometric', '40px', '44px', 700, 'BAUHAUS 1919', 'Bauhaus and duotone-poster headlines, set in capitals.'),
            st('serif-body', 'serif', '16px', '20px', 400, 'Welcome to my homepage!', 'Default Browser and Brutalist Web: the browser default of 16px Times.'),
         ]},
        {'name': 'Modern & code', 'family': 'modern',
         'styles': [
            st('modern-body', 'modern', '15px', '22px', 400, 'Frosted glass, soft light', 'Glassmorphism, neumorphism and claymorphism body size (15px).'),
            st('hand', 'hand', '16px', '24px', 400, '[ login button goes here ]', 'Wireframe sketch (16px in the source). Kalam is a free Google Font.'),
            st('mono', 'mono', '14px', '20px', 400, '0x00FF41 // databend', 'Glitch and btop readouts (14px in the sources).'),
         ]},
    ],
}

spacing = {'note': 'The TrillFx shared spine: a 4px scale. Not extracted per era; the source systems each space by eye.',
    'tokens': [
        {'name': 'space-1', 'value': '4px', 'usage': 'Icon-to-label gap; title-bar padding.'},
        {'name': 'space-2', 'value': '8px', 'usage': 'Inside controls; between buttons.'},
        {'name': 'space-3', 'value': '12px', 'usage': 'Between related rows.'},
        {'name': 'space-4', 'value': '16px', 'usage': 'Window body padding.'},
        {'name': 'space-6', 'value': '24px', 'usage': 'Between windows; page gutter.'},
        {'name': 'space-8', 'value': '32px', 'usage': 'Between sections.'},
        {'name': 'space-12', 'value': '48px', 'usage': 'Hero spacing.'},
        {'name': 'space-16', 'value': '64px', 'usage': 'Poster margins.'},
        {'name': 'space-24', 'value': '96px', 'usage': 'Full-bleed stage spacing.'},
    ]}
radius = {'note': 'Square is the default: most of the 53 use no radius at all. Steps are the values the source files use most.',
    'tokens': [
        {'name': 'radius-0', 'value': '0', 'usage': 'Default for every desktop-OS, terminal, print and pixel system.'},
        {'name': 'radius-sm', 'value': '2px', 'usage': 'XP and Aqua controls; the softest a retro control gets.'},
        {'name': 'radius-md', 'value': '4px', 'usage': 'Web 2.0 inputs and Frutiger panels (the most-used px radius in the sources).'},
        {'name': 'radius-lg', 'value': '8px', 'usage': 'Glossy cards.'},
        {'name': 'radius-xl', 'value': '20px', 'usage': 'Clay and glass panels, Y2K bubbles.'},
        {'name': 'radius-pill', 'value': '999px', 'usage': 'Aqua gel buttons, Web 2.0 pills (999px in the sources).'},
    ]}
shadow = {'note': 'Retro depth is drawn, not blurred: bevels and hard offsets.',
    'tokens': [
        {'name': 'bevel-raised', 'value': 'inset -1px -1px 0 #808080, inset 1px 1px 0 #ffffff', 'usage': 'Raised control: Windows 95, OS/2, Mac OS 9. Values are Windows 95 chrome-dark and chrome-lighter.'},
        {'name': 'bevel-sunken', 'value': 'inset 1px 1px 0 #808080, inset -1px -1px 0 #ffffff', 'usage': 'Pressed button, text field well.'},
        {'name': 'hard-drop', 'value': '4px 4px 0 #000000', 'usage': 'Memphis, Pop Art and Mac System 7 offset shadow (4px 4px 0 black in the sources).'},
    ]}

tj = {'name': TITLE, 'version': 1,
      'meta': {'source': 'github.com/LeviTrillfonix/retro-design-system @ 911d9b1 (NovusGFX, MIT)'},
      'color': {'themes': [{'id': t, 'name': BY[t]['name'].replace(' Terminal', '')} for t in FEATURED], 'tokens': tokens},
      'type': type_, 'spacing': spacing, 'radius': radius, 'shadow': shadow}
w('tokens.json', json.dumps(tj, indent=1, ensure_ascii=False) + '\n')

# ------------------------------------------------------------------ bundle
meta = [{'num': s['num'], 'id': s['id'], 'name': s['name'], 'era': s['era'], 'year': s['year'],
         'tags': s['tags'], 'font': s['font'], 'featured': s['id'] in FEATURED} for s in S]
bundle = r'''/* @ds-bundle: {"format":4,"namespace":"Retro","components":[{"name":"RetroWindow"},{"name":"SystemSwitcher"},{"name":"PaletteGrid"}]} */
(function () {
  "use strict";
  var SYSTEMS = __SYSTEMS__;
  var ROLES = ["bg", "surface", "ink", "muted", "border", "accent", "accent2", "highlight", "onaccent"];
  var FEATURED = __FEATURED__;

  function byId(id) {
    for (var i = 0; i < SYSTEMS.length; i++) if (SYSTEMS[i].id === id) return SYSTEMS[i];
    return null;
  }
  function apply(el, id) {
    var s = byId(id);
    if (!s) throw new Error("Retro: unknown system " + id);
    ROLES.forEach(function (r) { el.style.setProperty("--ui-" + r, "var(--" + id + "-" + r + ")"); });
    el.style.fontFamily = s.font;
    el.setAttribute("data-system", id);
    return s;
  }
  function reset(el) {
    ROLES.forEach(function (r) { el.style.removeProperty("--ui-" + r); });
    el.style.removeProperty("font-family");
    el.removeAttribute("data-system");
  }
  function h(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function computed(ctx, prop) {
    var p = h("span");
    p.style.color = "var(" + prop + ")";
    p.style.display = "none";
    ctx.appendChild(p);
    var c = getComputedStyle(p).color;
    ctx.removeChild(p);
    return c;
  }
  function rgb(c) {
    var m = (c.match(/[\d.]+/g) || [0, 0, 0]).map(Number);
    return { r: m[0], g: m[1], b: m[2], a: m.length > 3 ? m[3] : 1 };
  }
  function hex(c) {
    var o = rgb(c);
    var x = "#" + [o.r, o.g, o.b].map(function (v) { return ("0" + Math.round(v).toString(16)).slice(-2); }).join("");
    return o.a < 1 ? x + " " + Math.round(o.a * 100) + "%" : x;
  }
  function over(f, b) {
    return { r: f.r * f.a + b.r * (1 - f.a), g: f.g * f.a + b.g * (1 - f.a), b: f.b * f.a + b.b * (1 - f.a), a: 1 };
  }
  function lum(o) {
    function ch(v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
    return 0.2126 * ch(o.r) + 0.7152 * ch(o.g) + 0.0722 * ch(o.b);
  }
  /* WCAG ratio of role fg on role ground for system id; translucent grounds sit on bg */
  function contrast(id, fg, ground) {
    var ctx = document.body;
    var base = rgb(computed(ctx, "--" + id + "-bg"));
    var g = rgb(computed(ctx, "--" + id + "-" + ground));
    if (g.a < 1) g = over(g, base);
    var f = rgb(computed(ctx, "--" + id + "-" + fg));
    if (f.a < 1) f = over(f, g);
    var a = lum(f), b = lum(g);
    return Math.round(((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)) * 100) / 100;
  }
  function gradeOf(r) { return r >= 4.5 ? "AA" : r >= 3 ? "large only" : "fails"; }

  function RetroWindow(el, props) {
    props = props || {};
    var stage = h("div", "rt-stage");
    if (props.system) apply(stage, props.system);
    var win = h("div", "rt-win");
    var bar = h("div", "rt-bar");
    var title = h("span", "rt-bar-title", props.title || "Untitled");
    var btns = h("span", "rt-bar-btns");
    btns.setAttribute("aria-hidden", "true");
    btns.appendChild(h("i")); btns.appendChild(h("i")); btns.appendChild(h("i"));
    bar.appendChild(title); bar.appendChild(btns);
    var body = h("div", "rt-body");
    body.appendChild(h("p", "rt-text", props.text || "Loop locked. 140 BPM. Twelve clips rendered to the bin."));
    body.appendChild(h("p", "rt-muted", props.caption || "Last render 00:04:12 ago"));
    var row = h("div", "rt-row");
    row.appendChild(h("button", "rt-btn rt-primary", "Render"));
    row.appendChild(h("button", "rt-btn", "Cancel"));
    var input = h("input", "rt-input");
    input.value = "140";
    input.setAttribute("aria-label", "BPM");
    row.appendChild(input);
    body.appendChild(row);
    var keys = h("div", "rt-keys");
    [["accent", "Accent"], ["accent2", "Accent 2"], ["highlight", "Highlight"]].forEach(function (k) {
      var s = h("span", "rt-key");
      var d = h("i", "rt-dot");
      d.style.background = "var(--ui-" + k[0] + ")";
      s.appendChild(d); s.appendChild(document.createTextNode(k[1]));
      keys.appendChild(s);
    });
    body.appendChild(keys);
    win.appendChild(bar); win.appendChild(body);
    stage.appendChild(win);
    stage._title = title;
    el.appendChild(stage);
    return stage;
  }

  function SystemSwitcher(el, props) {
    props = props || {};
    var wrap = h("div", "rt-switch");
    var controls = h("div", "rt-controls");
    var label = h("label", "rt-label", "System");
    var sel = h("select");
    sel.id = "rt-sel-" + Math.random().toString(36).slice(2, 7);
    label.setAttribute("for", sel.id);
    var eras = [];
    SYSTEMS.forEach(function (s) { if (eras.indexOf(s.era) < 0) eras.push(s.era); });
    eras.forEach(function (era) {
      var g = h("optgroup"); g.label = era;
      SYSTEMS.forEach(function (s) {
        if (s.era !== era) return;
        var o = h("option", null, s.num + ". " + s.name + (s.featured ? "  \u2605" : ""));
        o.value = s.id; g.appendChild(o);
      });
      sel.appendChild(g);
    });
    var prev = h("button", "rt-step", "\u25C0"); prev.setAttribute("aria-label", "Previous system");
    var next = h("button", "rt-step", "\u25B6"); next.setAttribute("aria-label", "Next system");
    var count = h("span", "rt-count");
    controls.appendChild(label); controls.appendChild(sel); controls.appendChild(prev); controls.appendChild(next); controls.appendChild(count);
    var split = h("div", "rt-split");
    var left = h("div", "rt-left");
    var stage = RetroWindow(left, {});
    var info = h("div", "rt-info");
    var name = h("h3");
    var metaLine = h("p", "rt-meta");
    var fontLine = h("p", "rt-code");
    var strip = h("div", "rt-strip");
    var ratios = h("p", "rt-meta");
    info.appendChild(name); info.appendChild(metaLine); info.appendChild(strip); info.appendChild(ratios); info.appendChild(fontLine);
    split.appendChild(left); split.appendChild(info);
    wrap.appendChild(controls); wrap.appendChild(split);
    el.appendChild(wrap);

    var current = null;
    function set(id) {
      var s = apply(stage, id);
      current = s;
      stage._title.textContent = s.name + (s.year ? " \u2014 " + s.year : "");
      sel.value = id;
      count.textContent = s.num + " / " + SYSTEMS.length + (s.featured ? " \u00B7 native theme" : "");
      name.textContent = s.name;
      metaLine.textContent = s.era + (s.year ? " \u00B7 " + s.year : "") + " \u00B7 " + s.tags.join(", ");
      fontLine.textContent = "font-family: " + s.font;
      strip.textContent = "";
      ROLES.forEach(function (r) {
        var cell = h("div", "rt-sw");
        var chip = h("b"); chip.style.background = "var(--" + id + "-" + r + ")";
        var txt = h("span");
        txt.appendChild(h("span", "rt-role", r));
        txt.appendChild(h("span", "rt-hex", hex(computed(document.body, "--" + id + "-" + r))));
        cell.appendChild(chip); cell.appendChild(txt);
        strip.appendChild(cell);
      });
      var a = contrast(id, "ink", "surface"), m = contrast(id, "muted", "surface");
      ratios.textContent = "ink on surface " + a + ":1 " + gradeOf(a) + " \u00B7 muted on surface " + m + ":1 " + gradeOf(m);
      if (props.onChange) props.onChange(s);
    }
    function step(d) {
      var i = SYSTEMS.indexOf(current);
      set(SYSTEMS[(i + d + SYSTEMS.length) % SYSTEMS.length].id);
    }
    sel.addEventListener("change", function () { set(sel.value); });
    prev.addEventListener("click", function () { step(-1); });
    next.addEventListener("click", function () { step(1); });
    set(props.initial && byId(props.initial) ? props.initial : SYSTEMS[0].id);
    return { set: set, get: function () { return current; } };
  }

  function PaletteGrid(el, props) {
    props = props || {};
    var t = h("table", "rt-grid");
    var thead = h("thead"), hr = h("tr");
    ["#", "System", "Era", "Year"].concat(ROLES).concat(["ink / surface"]).forEach(function (c) { hr.appendChild(h("th", null, c)); });
    thead.appendChild(hr); t.appendChild(thead);
    var tb = h("tbody");
    SYSTEMS.forEach(function (s) {
      var tr = h("tr");
      tr.appendChild(h("td", "rt-num", String(s.num)));
      tr.appendChild(h("td", "rt-name", s.name + (s.featured ? " \u2605" : "")));
      tr.appendChild(h("td", null, s.era));
      tr.appendChild(h("td", null, s.year ? String(s.year) : ""));
      ROLES.forEach(function (r) {
        var td = h("td", "sw"), i = h("i");
        i.style.background = "var(--" + s.id + "-" + r + ")";
        i.title = s.id + "-" + r + "  " + hex(computed(document.body, "--" + s.id + "-" + r));
        td.appendChild(i); tr.appendChild(td);
      });
      var c = contrast(s.id, "ink", "surface");
      tr.appendChild(h("td", "rt-num", c + ":1"));
      if (props.onSelect) { tr.tabIndex = 0; tr.addEventListener("click", function () { props.onSelect(s); }); }
      tb.appendChild(tr);
    });
    t.appendChild(tb);
    el.appendChild(t);
    return t;
  }

  window.Retro = {
    systems: SYSTEMS, roles: ROLES, featured: FEATURED,
    apply: apply, reset: reset, byId: byId, contrast: contrast,
    RetroWindow: RetroWindow, SystemSwitcher: SystemSwitcher, PaletteGrid: PaletteGrid
  };
})();
'''
bundle = bundle.replace('__SYSTEMS__', json.dumps(meta, ensure_ascii=False)).replace('__FEATURED__', json.dumps(FEATURED))
assert '</script' not in bundle.lower() and '<!--' not in bundle
w('components/bundle.js', bundle)

w('components/bundle.css', '''body { margin: 0; background: var(--ui-bg); color: var(--ui-ink); font-family: var(--font-modern); }
.rt-stage { background: var(--ui-bg); color: var(--ui-ink); padding: var(--space-6); }
.rt-win { background: var(--ui-surface); color: var(--ui-ink); border: 2px solid var(--ui-border); max-width: 520px; }
.rt-bar { display: flex; align-items: center; justify-content: space-between; gap: var(--space-2); background: var(--ui-accent); color: var(--ui-onaccent); padding: var(--space-1) var(--space-2); font-weight: 700; font-size: 14px; }
.rt-bar-btns i { display: inline-block; width: 11px; height: 11px; margin-left: var(--space-1); border: 1px solid var(--ui-onaccent); vertical-align: middle; }
.rt-body { padding: var(--space-4); }
.rt-text { margin: 0 0 var(--space-2); font-size: 15px; line-height: 1.4; }
.rt-muted { margin: 0 0 var(--space-4); font-size: 13px; color: var(--ui-muted); }
.rt-row { display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-2); }
.rt-btn { font: inherit; font-size: 14px; min-height: 32px; padding: 0 var(--space-4); background: var(--ui-surface); color: var(--ui-ink); border: 2px solid var(--ui-border); border-radius: var(--radius-0); cursor: pointer; }
.rt-primary { background: var(--ui-accent); color: var(--ui-onaccent); border-color: var(--ui-ink); }
.rt-input { font: inherit; font-size: 14px; min-height: 32px; width: 72px; padding: 0 var(--space-2); background: var(--ui-surface); color: var(--ui-ink); border: 2px solid var(--ui-border); border-radius: var(--radius-0); }
.rt-btn:focus-visible, .rt-input:focus-visible, .rt-controls select:focus-visible, .rt-controls button:focus-visible { outline: 2px solid var(--ui-ink); outline-offset: 2px; }
.rt-keys { display: flex; flex-wrap: wrap; gap: var(--space-4); margin-top: var(--space-4); font-size: 13px; }
.rt-dot { display: inline-block; width: 12px; height: 12px; margin-right: 6px; vertical-align: -1px; border: 1px solid var(--ui-ink); }
.rt-switch { background: var(--ui-bg); color: var(--ui-ink); font-family: var(--font-modern); }
.rt-controls { display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-2); padding: var(--space-3) var(--space-4); border-bottom: 1px solid var(--ui-border); }
.rt-label { font-size: 13px; font-weight: 600; }
.rt-controls select, .rt-controls button { font: inherit; font-size: 14px; min-height: 32px; padding: 0 var(--space-2); background: var(--ui-surface); color: var(--ui-ink); border: 1px solid var(--ui-border); border-radius: var(--radius-0); }
.rt-controls button { cursor: pointer; min-width: 36px; }
.rt-count { margin-left: auto; font-size: 13px; }
.rt-split { display: flex; flex-wrap: wrap; }
.rt-left { flex: 1 1 380px; min-width: 0; display: flex; flex-direction: column; }
.rt-left .rt-stage { flex: 1 1 auto; box-sizing: border-box; }
.rt-info { flex: 1 1 300px; padding: var(--space-4); font-size: 13px; line-height: 1.5; }
.rt-info h3 { margin: 0 0 var(--space-1); font-size: 18px; }
.rt-meta { margin: 0 0 var(--space-3); }
.rt-code { margin: var(--space-3) 0 0; font-family: var(--font-mono); font-size: 12px; word-break: break-word; }
.rt-strip { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-2); margin-bottom: var(--space-3); }
.rt-sw { display: flex; align-items: center; gap: 6px; min-width: 0; }
.rt-sw b { flex: none; width: 24px; height: 24px; border: 1px solid var(--ui-ink); }
.rt-role { display: block; font-weight: 600; font-size: 12px; }
.rt-hex { display: block; font-family: var(--font-mono); font-size: 11px; }
.rt-grid { border-collapse: collapse; width: 100%; font-size: 12px; font-family: var(--font-modern); background: var(--ui-bg); color: var(--ui-ink); }
.rt-grid th, .rt-grid td { padding: 3px 6px; text-align: left; white-space: nowrap; border-bottom: 1px solid var(--ui-border); }
.rt-grid th { position: sticky; top: 0; background: var(--ui-surface); font-weight: 600; }
.rt-grid td.sw { padding: 2px 3px; }
.rt-grid td.sw i { display: block; width: 22px; height: 18px; box-shadow: inset 0 0 0 1px rgba(128, 128, 128, 0.45); }
.rt-num { font-family: var(--font-mono); }
.rt-name { font-weight: 600; }
/* native themes carry their system's own type into components (Retro.apply sets it inline for the other 45) */
''' + '\n'.join(f'[data-theme="{t}"] .rt-stage {{ font-family: {BY[t]["font"]}; }}' for t in FEATURED) + '\n')

w('components/index.d.ts', '''/** The nine roles every system defines; `ui-<role>` is the active one. */
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
''')

GF = ('https://fonts.googleapis.com/css2?family=VT323&family=Press+Start+2P&family=Orbitron:wght@400;700'
      '&family=Share+Tech+Mono&family=Space+Mono&family=Space+Grotesk:wght@400;700&family=Inter:wght@400;600'
      '&family=IBM+Plex+Mono&family=Kalam&family=Bungee&family=Nunito:wght@400;700&family=Patrick+Hand'
      '&family=Shadows+Into+Light&family=Rajdhani:wght@400;700&family=JetBrains+Mono&display=swap')

def preview(marker, title, script, root='<div id="root"></div>', fonts=True):
    link = f'<link rel="stylesheet" href="{GF}">\n' if fonts else ''
    return f'''{marker}
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>{title}</title>
{link}</head>
<body>
{root}
<script>
{script}
</script>
</body>
</html>
'''

w('components/RetroWindow/preview.html', preview('<!-- @dsCard group="Surfaces" height=300 subtitle="Follows the active theme" -->', 'RetroWindow — preview',
  "  Retro.RetroWindow(document.getElementById('root'), { title: 'VJToolbox.exe' });"))
w('components/SystemSwitcher/preview.html', preview('<!-- @dsCard group="Explore" height=400 subtitle="All 53 systems, live" -->', 'SystemSwitcher — preview',
  "  Retro.SystemSwitcher(document.getElementById('root'), { initial: 'win95' });"))
w('components/PaletteGrid/preview.html', preview(f'<!-- @dsCard group="Reference" height={53*25+60} subtitle="53 systems x 9 roles" -->', 'PaletteGrid — preview',
  "  Retro.PaletteGrid(document.getElementById('root'));", fonts=False))

w('components/RetroWindow/README.md', '''# RetroWindow

A classic window (title bar, body copy, buttons, a field) drawn entirely from the nine `ui-*` roles, so it re-skins to whichever system is active.

- With no `system` it follows the page's theme; pass `system: "c64"` (any of the 53 ids) to pin it.
- Title bar is `ui-accent` with `ui-onaccent` text; the primary button repeats that pair. Everything else is `ui-ink` on `ui-surface`.
- Consumer provides the host element and the copy. Keep copy era-true: short, literal, no exclamation marks except on GeoCities.
''')
w('components/SystemSwitcher/README.md', '''# SystemSwitcher

Live-switches a preview window between all 53 systems, past the artifact's 8-native-theme limit.

- It calls `Retro.apply(el, id)`, which points the nine `ui-*` custom properties of one element at `--<id>-<role>` and sets that system's `font-family`. Everything inside re-skins; the page around it keeps its own theme.
- The side panel shows the nine resolved colours and live WCAG ratios for ink and muted text on the surface, measured the same way as the README table.
- A star marks the eight systems that are also native themes (theme switcher above).
- Use the same call in your own pages: `Retro.apply(document.body, 'vaporwave')`.
''')
w('components/PaletteGrid/README.md', '''# PaletteGrid

Every system's nine roles side by side, read live from the tokens.

- Hover a swatch for its token name and hex. The last column is ink-on-surface contrast.
- Pass `onSelect` to make rows clickable, for example to drive a SystemSwitcher.
''')

# ------------------------------------------------------------------ cover
cover = '''<!-- @dsCard height=320 -->
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Retro Design System</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap">
<style>
  html, body { margin: 0; height: 100%; }
  body { background: var(--ui-surface); color: var(--ui-ink); font-family: var(--font-display); overflow: hidden; }
  .cover { position: relative; height: 320px; overflow: hidden; }
  .band { position: absolute; top: 0; left: 0; width: 960px; height: 120px; }
  .band svg { display: block; width: 960px; height: 120px; }
  .ink { fill: var(--ui-ink); }
  .acc { fill: var(--ui-accent); }
  .acc2 { fill: var(--ui-accent2); }
  .hi { fill: var(--ui-highlight); }
  .cut { fill: var(--ui-surface); }
  .blk { rx: var(--radius-0); }
  .words { position: absolute; left: var(--space-6); right: var(--space-6); bottom: var(--space-6); }
  .name { margin: 0; font-size: 64px; line-height: .95; font-weight: 700; letter-spacing: .01em; color: var(--ui-ink); }
  .tag { margin: var(--space-2) 0 0 2px; font-family: var(--font-modern); font-size: 14px; line-height: 20px; color: var(--ui-ink); }
</style>
</head>
<body>
<div class="cover">
<div class="band" aria-hidden="true">
<svg viewBox="0 0 960 120" width="960" height="120">
<!--
  blocks      ui-ink 24 wide (a phosphor edge) · ui-accent 400x128 slab, bled off the top · ui-accent2 232x96 · ui-highlight 152x128 · ui-accent 128x64 bled off the right; about 34% of 960x320
  arrangement top-band skeleton (the name at 64px is wider than 440): a strip of unequal bands, like SMPTE bars, space-2 gutters
  pattern     scanlines, from "CRT, VHS and synthwave all read as horizontal scan": six ground-cut stripes across the accent slab, 2 to 12px thick, thickening downward like a synthwave sun
  scales      widths in space-2 multiples; gutters space-2; stripe pitch space-3 then space-2; corners radius-0 (retro is square). Tagline in ui-ink: ui-muted fails on several systems' surfaces.
-->
<rect class="ink blk" x="0" y="-8" width="24" height="128" rx="0"/>
<rect class="acc blk" x="32" y="-8" width="400" height="128" rx="0"/>
<rect class="cut" x="32" y="52" width="400" height="2"/>
<rect class="cut" x="32" y="64" width="400" height="3"/>
<rect class="cut" x="32" y="76" width="400" height="5"/>
<rect class="cut" x="32" y="89" width="400" height="7"/>
<rect class="cut" x="32" y="102" width="400" height="9"/>
<rect class="cut" x="32" y="116" width="400" height="12"/>
<rect class="acc2 blk" x="440" y="-8" width="232" height="104" rx="0"/>
<rect class="hi blk" x="680" y="-8" width="152" height="128" rx="0"/>
<rect class="acc blk" x="840" y="-8" width="128" height="72" rx="0"/>
</svg>
</div>
<div class="words">
<h1 class="name">Retro Design<br>System</h1>
<p class="tag">53 interface eras, one switchable token set.</p>
</div>
</div>
</body>
</html>
'''
w('components/Cover/preview.html', cover)

# ------------------------------------------------------------------ assets group README
SHOTS = ['social-poster.png'] + sorted(f for f in os.listdir(os.path.join(REPO, 'assets')) if f.startswith('system-'))
w('assets/Showcase/README.md', '# Showcase\n\nScreenshots of nine of the 53 systems (every screenshot the source repo ships; NovusGFX, MIT) plus the repo\'s social poster. They show each style as its own demo page renders it: use them to check a build against the original.\n\n'
  + '\n'.join(f'- `{f}`' + (' - repo social poster, all 53 at a glance.' if f == 'social-poster.png' else f' - {BY[[s["id"] for s in S if s["slug"].startswith(f[7:9])][0]]["name"]}.') for f in SHOTS) + '\n')

json.dump({'shots': SHOTS, 'featured': FEATURED, 'tokens': len(tokens)}, open(os.path.join(HERE, 'gen-meta.json'), 'w', encoding='utf-8', newline='\n'))
print('tokens:', len(tokens), '| families:', len(families), '| styles:', sum(len(g['styles']) for g in type_['groups']))
