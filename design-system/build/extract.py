#!/usr/bin/env python3
"""Step 1+2: map every retro system onto the shared role set, from source values only,
then measure WCAG contrast. Writes systems.json + contrast-report.md.

Spec grammar for a role:
  v:NAME        CSS custom property --NAME from tokens/<slug>.css (var() chains resolved)
  g:NAME:i      i-th colour stop of gradient property --NAME
  b:i           i-th colour in the page's <body> background (index.html)
  #hex / rgba() literal found in the source file (body rule, inline style) or a UA default
  =ROLE         alias of another role of the same system (no distinct tone in source)
"""
import json, re, os, sys

# Paths: this file lives in design-system/build/ of the repo.
DS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # design-system/
REPO = os.path.dirname(DS)                                          # repo root
OUT = DS

ROLES = ['bg', 'surface', 'ink', 'muted', 'border', 'accent', 'accent2', 'highlight', 'onaccent']

IDS = {
 '01-mac-system-7':'macsys7','02-windows-95':'win95','03-windows-xp-luna':'xpluna','04-aqua-osx':'aqua',
 '05-amiga-workbench':'amiga','06-nextstep':'nextstep','07-beos':'beos','08-teletext':'teletext',
 '09-crt-phosphor':'crt','10-dos-cga':'doscga','11-8bit-arcade':'arcade','12-frutiger-aero':'aero',
 '13-winamp-skin':'winamp','14-geocities-web10':'geocities','15-cassette-futurism':'cassette',
 '16-vaporwave':'vaporwave','17-memphis':'memphis','18-ps1-tech':'ps1','19-os2-warp':'os2warp',
 '20-macos9-platinum':'macos9','21-web20-glossy':'web20','22-gameboy-dmg':'gameboy','23-braun-rams':'braun',
 '24-tron-vector':'tron','25-vhs-tracking':'vhs','26-risograph':'riso','27-ibm-3270':'ibm3270',
 '28-nethack-ascii':'nethack','29-templeos':'templeos','30-bbs-ansi':'bbsansi','31-midnight-commander':'mc',
 '32-matrix-rain':'matrix','33-btop-meters':'btop','34-c64-basic':'c64','35-flat-2013':'flat2013',
 '36-glassmorphism':'glass','37-neumorphism':'neumorph','38-blueprint-cad':'blueprint','39-claymorphism':'clay',
 '40-brutalist-web':'brutalist','41-swiss-intl':'swiss','42-bauhaus':'bauhaus','43-pop-art-lichtenstein':'popart',
 '44-op-art':'opart','45-hypnagogic':'hypnagogic','46-monochrome-zen':'zen','47-default-browser':'browser',
 '48-wireframe-sketch':'wireframe','49-glitch-databend':'glitch','50-y2k-chrome':'y2k','51-duotone-poster':'duotone',
 '52-grid-paper':'gridpaper','53-maximalist-banners':'maximalist',
}

# role order: bg, surface, ink, muted, border, accent, accent2, highlight
M = {
 '01-mac-system-7':    ['v:desktop','v:paper','v:ink','=bg','v:shadow','=ink','v:chrome','v:bg'],
 '02-windows-95':      ['v:bg','v:chrome','v:ink','v:chrome-dark','v:chrome-darker','v:title','=bg','v:chrome-lighter'],
 '03-windows-xp-luna': ['b:1','v:chrome','#000000','g:title-gradient:1','v:luna-blue-3','v:luna-blue','g:start-green:1','v:bg-bot'],
 '04-aqua-osx':        ['v:bg','g:chrome:0','v:ink','v:aqua-blue-deep','g:chrome:1','v:aqua-blue','g:jelly-red:1','g:jelly-yellow:1'],
 '05-amiga-workbench': ['v:wb-blue','v:wb-gray','v:ink','=bg','v:wb-black','v:wb-orange','v:wb-white','=accent2'],
 '06-nextstep':        ['v:bg','v:chrome','v:ink','v:chrome-darker','v:chrome-dark','v:accent','v:chrome-light','v:chrome-lighter'],
 '07-beos':            ['v:bg','v:chrome','v:ink','v:chrome-darker','v:chrome-dark','v:yellow','v:red-dot','v:chrome-lighter'],
 '08-teletext':        ['#1a1a1a','v:tt-black','v:tt-white','v:tt-cyan','v:tt-blue','v:tt-yellow','v:tt-red','v:tt-green'],
 '09-crt-phosphor':    ['#000000','v:bg','v:ink','v:ink-dim','=muted','v:ink-bright','v:amber','=ink'],
 '10-dos-cga':         ['v:c-blue','v:c-black','v:c-gray','v:c-cyan','v:c-white','v:c-cyan-bright','v:c-magenta','v:c-yellow'],
 '11-8bit-arcade':     ['v:bg','b:0','v:ink','v:cyan','v:purple','v:pink','v:yellow','v:green'],
 '12-frutiger-aero':   ['v:sky-top','v:glass','v:ink','=ink','=accent','v:aero-blue','v:aero-green','v:sky-bot'],
 '13-winamp-skin':     ['#0e0e12','v:chrome','#eeeeee','v:chrome-lighter','v:chrome-light','v:lcd','v:accent','v:accent-red'],
 '14-geocities-web10': ['#000000','=bg','v:yellow','v:cyan','=muted','v:hotpink','v:lime','v:red'],
 '15-cassette-futurism':['v:bg','v:panel','v:amber','v:ink','v:bezel','v:amber-bright','v:red-warn','v:green-ok'],
 '16-vaporwave':       ['v:bg','b:1','v:ink','v:purple','v:grid','v:pink','v:cyan','v:green'],
 '17-memphis':         ['v:white','=bg','v:black','=ink','=ink','v:pink','v:teal','v:yellow'],
 '18-ps1-tech':        ['v:bg','v:chrome-darker','v:ink','v:chrome','v:chrome-dark','v:neon-cyan','v:neon-purple','v:neon-green'],
 '19-os2-warp':        ['v:desktop','v:chrome','v:ink','v:chrome-darker','v:chrome-dark','v:titlebar','v:warp-red','v:titlebar-2'],
 '20-macos9-platinum': ['v:desktop','v:platinum','v:ink','v:platinum-darker','v:platinum-dark','v:accent','v:stripe','v:platinum-light'],
 '21-web20-glossy':    ['v:bg','v:panel','v:ink','v:muted','v:sky-1','v:blue','v:orange','v:green'],
 '22-gameboy-dmg':     ['v:shell','v:lcd-3','v:lcd-0','v:lcd-1','v:screen-bezel','v:btn-purple','v:red-led','=muted'],
 '23-braun-rams':      ['v:paper','v:white','v:ink','v:gray-3','v:gray-2','v:orange','v:green','v:gray-1'],
 '24-tron-vector':     ['v:bg','v:grid','v:ink','v:cyan-dim','=muted','v:orange','v:red','v:cyan-bright'],
 '25-vhs-tracking':    ['v:bg','v:tape','v:osd-white','v:osd-cyan','=muted','v:rec-red','v:osd-yellow','v:smpte-magenta'],
 '26-risograph':       ['v:paper','v:paper-dark','v:ink','v:riso-blue','=ink','v:fluoro-pink','v:riso-green','v:riso-yellow'],
 '27-ibm-3270':        ['#0a0a0a','v:bg','v:green','v:turquoise','v:dim','v:yellow','v:pink','v:white'],
 '28-nethack-ascii':   ['v:bg','=bg','v:ink','v:wall','v:dim','v:player','v:monster-red','v:item-cyan'],
 '29-templeos':        ['v:bg','=bg','v:text','v:cyan','=muted','v:yellow','v:red','v:green'],
 '30-bbs-ansi':        ['v:bg','=bg','v:white-hi','v:white','=muted','v:cyan-hi','v:magenta-hi','v:yellow-hi'],
 '31-midnight-commander':['#000000','v:panel','v:text','=ink','v:panel-border','v:selected-bg','v:yellow','v:text-hi'],
 '32-matrix-rain':     ['v:bg','=bg','v:mx','=ink','v:mx-dim','v:mx-hi','v:warn','v:mx-white'],
 '33-btop-meters':     ['v:bg','v:panel-bg','v:ink','v:muted','v:panel-border','v:accent','v:mem','v:cpu-1'],
 '34-c64-basic':       ['v:border','v:bg','v:text-hi','v:text','v:bg-dark','v:cyan','v:yellow','v:white'],
 '35-flat-2013':       ['v:bg','#ffffff','v:dark','v:gray','v:silver','v:turq','v:blue','v:yellow'],
 '36-glassmorphism':   ['b:1','v:glass-bg','v:ink','v:muted','v:glass-border','v:accent','v:accent-2','=ink'],
 '37-neumorphism':     ['v:bg','=bg','v:ink','v:muted','v:shadow-dark','v:accent','=border','v:shadow-light'],
 '38-blueprint-cad':   ['v:bg','v:bg-dark','v:ink','v:line-dim','v:line','v:yellow','v:red','=border'],
 '39-claymorphism':    ['v:bg','#ffffff','v:ink','v:muted','v:purple','v:pink','v:blue','v:mint'],
 '40-brutalist-web':   ['#ffffff','#e0e0e0','#000000','=ink','=ink','#0000ee','#551a8b','#ffff00'],
 '41-swiss-intl':      ['v:paper','=bg','v:ink','v:muted','v:line','v:red','=ink','=accent'],
 '42-bauhaus':         ['v:paper','=bg','v:ink','=ink','=ink','v:red','v:blue','v:yellow'],
 '43-pop-art-lichtenstein':['v:paper','v:skin','v:ink','=ink','=ink','v:red','v:blue','v:yellow'],
 '44-op-art':          ['v:white','=bg','v:black','=ink','=ink','v:red','=ink','=accent'],
 '45-hypnagogic':      ['v:wall','v:ceiling','v:ink','v:faded','v:shadow','v:sign','v:exit','v:fluor'],
 '46-monochrome-zen':  ['v:paper','=bg','v:ink','=ink','v:rule','=ink','=border','=bg'],
 '47-default-browser': ['#ffffff','=bg','#000000','=ink','#808080','#0000ee','#800080','#ff0000'],
 '48-wireframe-sketch':['v:paper','=bg','v:ink','v:muted','v:light','v:hi','=border','=accent'],
 '49-glitch-databend': ['v:bg','=bg','v:ink','=ink','v:magenta','v:red','v:cyan','v:yellow'],
 '50-y2k-chrome':      ['v:bg-1','v:chrome-hi','v:ink','v:chrome-low','v:chrome-mid','v:pink','v:blue','v:purple'],
 '51-duotone-poster':  ['v:paper','=bg','v:spot-2','=ink','=ink','v:spot-1','=ink','=accent'],
 '52-grid-paper':      ['v:paper','=bg','v:ink','v:pencil','v:grid-major','v:red-ink','v:green-ink','v:highlighter'],
 '53-maximalist-banners':['v:bg','v:bg-3','v:ink','=ink','=ink','v:bg-2','=surface','=bg'],
}

# where a literal came from (for usage notes / README method section)
LIT_SRC = {
 ('03-windows-xp-luna','ink'): 'body `color: #000`',
 ('08-teletext','bg'): 'body background `#1a1a1a`',
 ('09-crt-phosphor','bg'): 'body background `#000`',
 ('13-winamp-skin','bg'): 'body background `#0e0e12`',
 ('13-winamp-skin','ink'): 'body `color: #eee`',
 ('14-geocities-web10','bg'): 'body background `#000` (starfield)',
 ('27-ibm-3270','bg'): 'body background `#0a0a0a`',
 ('31-midnight-commander','bg'): 'body background `#000`',
 ('35-flat-2013','surface'): 'white card `background: #fff`',
 ('39-claymorphism','surface'): 'white card `background: #fff`',
 ('40-brutalist-web','bg'): 'body background `#ffffff`',
 ('40-brutalist-web','surface'): '`th { background: #e0e0e0 }`',
 ('40-brutalist-web','ink'): 'body `color: #000000`',
 ('40-brutalist-web','accent'): 'link blue `#0000ee`',
 ('40-brutalist-web','accent2'): 'visited link `#551a8b`',
 ('40-brutalist-web','highlight'): '`.warn { background: #ffff00 }`',
 ('47-default-browser','bg'): 'browser default page white (source has no stylesheet)',
 ('47-default-browser','ink'): 'browser default text black',
 ('47-default-browser','border'): 'browser default `<hr>` grey',
 ('47-default-browser','accent'): 'browser default link `#0000ee`',
 ('47-default-browser','accent2'): 'inline `style="color:purple"` (visited example) = `#800080`',
 ('47-default-browser','highlight'): 'browser default active-link red',
}

NOTES = {
 '01-mac-system-7': 'Monochrome by design: System 7 draws UI in black, white and greys, and shows selection by inversion, so the accent is black.',
 '02-windows-95': '`muted` is Windows disabled-text grey (#808080); it fails as body text on the silver chrome. Use it for disabled states only.',
 '03-windows-xp-luna': 'Blue page background is the middle stop of the Bliss-sky body gradient; Start-button green is `accent2`.',
 '04-aqua-osx': 'Gel buttons are radial gradients in the source; the traffic-light body colours (red/yellow) are used flat.',
 '05-amiga-workbench': 'Workbench 1.x four-colour palette has no secondary-text tone; `muted` reuses the desktop blue and fails on the grey window.',
 '06-nextstep': 'Greyscale by design; no hue anywhere in the NeXT palette.',
 '08-teletext': 'Teletext has no grey; secondary text is cyan, as on Ceefax. Page background is the #1a1a1a around the black "TV".',
 '09-crt-phosphor': 'Two-colour phosphor: green text plus an amber alert. Page is #000; the tube face is #001a00.',
 '10-dos-cga': 'Body is grey-on-blue DOS; the black surface is the terminal window.',
 '11-8bit-arcade': '`surface` is the purple glow at the top of the page (#1a1440), from the body gradient.',
 '12-frutiger-aero': 'Surface is 35% white glass. Contrast is measured with the glass composited over the sky. No secondary-text tone in source; `muted` = `ink`.',
 '13-winamp-skin': 'LCD green is the accent; page is the dark #0e0e12 behind the skin.',
 '14-geocities-web10': 'Black starfield with yellow text. Default link blue (#0000ee) is kept out of the text roles: it measures 2.2:1 on black.',
 '15-cassette-futurism': 'Amber instrument panel with red WARN and green OK lamps.',
 '16-vaporwave': '`surface` is the deep purple second stop of the sunset body gradient.',
 '17-memphis': 'Primaries on white with black outlines; no grey tone by design.',
 '22-gameboy-dmg': 'The four DMG greens (#0f380f to #9bbc0f) are the UI; the grey shell is used as the page so the device reads as one piece. The source page itself is near-black (#1a1a22).',
 '26-risograph': 'Two-ink print: text in black, secondary text in riso blue.',
 '29-templeos': '16-colour VGA; no grey, so secondary text is cyan.',
 '31-midnight-commander': 'Grey-on-blue panels; the palette has no dimmer text tone, so `muted` = `ink`.',
 '32-matrix-rain': 'The dim green (#003b00) is trail colour only (1.7:1); `muted` = `ink`.',
 '34-c64-basic': 'Page is the light-blue C64 border; the dark-blue screen is the surface.',
 '35-flat-2013': 'Flat grey caption text (#95a5a6) fails on both grounds, as it did in 2013. Keep it for large labels only.',
 '37-neumorphism': 'The known neumorphism problem: soft grey text measures under 3:1. Surfaces equal the background and differ only by shadow.',
 '40-brutalist-web': 'Raw HTML: values are the few literal colours in the source file. `a:hover` red (#ff0000) is not mapped.',
 '41-swiss-intl': 'Black, paper and one red by design.',
 '42-bauhaus': 'Three primaries and black on paper; no grey by design.',
 '44-op-art': 'Black, white and one red by design.',
 '46-monochrome-zen': 'Monochrome by design; the only non-ink value is the 15% hairline.',
 '47-default-browser': 'The source uses no stylesheet at all, so every value is the browser default it relies on (documented per token).',
 '48-wireframe-sketch': 'Greyscale by design; the accent is the pale highlighter fill.',
 '51-duotone-poster': 'Paper plus two spot inks by design.',
 '52-grid-paper': 'Grid lines and highlighter are translucent in the source and kept that way.',
 '53-maximalist-banners': 'Magenta/cyan/yellow stripes with black text; no grey by design.',
}

COLOR_RE = re.compile(r'#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)')

def parse_vars(css):
    body = css[css.index('{')+1: css.rindex('}')]
    out = {}
    for m in re.finditer(r'--([\w-]+)\s*:\s*([^;]+);', body):
        out[m.group(1)] = m.group(2).strip()
    return out

def parse_body_bg(html):
    m = re.search(r'(?:^|\n)\s*(?:html,\s*)?body\s*\{([^}]*)\}', html)
    if not m: return None
    b = m.group(1)
    bg = re.search(r'background(?:-color)?\s*:\s*([^;]+)', b)
    return bg.group(1) if bg else None

def body_font_size(html):
    m = re.search(r'(?:^|\n)\s*(?:html,\s*)?body\s*\{([^}]*)\}', html)
    if not m: return None
    fs = re.search(r'font-size\s*:\s*([^;]+)', m.group(1))
    return fs.group(1).strip() if fs else None

def norm_hex(c):
    c = c.strip().lower()
    if c.startswith('#') and len(c) == 4:
        c = '#' + ''.join(ch*2 for ch in c[1:])
    return c

def resolve_var(vars_, name, seen=()):
    v = vars_[name]
    m = re.fullmatch(r'var\(--([\w-]+)\)', v.strip())
    if m:
        if m.group(1) in seen: raise ValueError('cycle')
        return resolve_var(vars_, m.group(1), seen + (name,))
    return v

def colours_in(value, vars_):
    """ordered colours inside a value, resolving var() refs"""
    out = []
    for m in re.finditer(r'var\(--([\w-]+)\)|#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)', value):
        if m.group(1):
            out.append(norm_hex(resolve_var(vars_, m.group(1))))
        else:
            out.append(norm_hex(m.group(0)))
    return out

def is_colour(v):
    v = v.strip()
    return bool(re.fullmatch(r'#[0-9a-fA-F]{3,8}|rgba?\([\d\s.,%]+\)', v))

# ---------- contrast ----------
def to_rgba(c):
    c = c.strip().lower()
    if c.startswith('#'):
        h = c[1:]
        if len(h) in (3, 4): h = ''.join(x*2 for x in h)
        r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
        a = int(h[6:8],16)/255 if len(h) == 8 else 1.0
        return (r, g, b, a)
    m = re.fullmatch(r'rgba?\(([^)]*)\)', c)
    p = [x.strip() for x in m.group(1).split(',')]
    return (float(p[0]), float(p[1]), float(p[2]), float(p[3]) if len(p) > 3 else 1.0)

def over(fg, bg):
    r, g, b, a = fg; R, G, B, _ = bg
    return (r*a + R*(1-a), g*a + G*(1-a), b*a + B*(1-a), 1.0)

def lum(c):
    def ch(v):
        v /= 255
        return v/12.92 if v <= 0.03928 else ((v+0.055)/1.055)**2.4
    r, g, b, _ = c
    return 0.2126*ch(r) + 0.7152*ch(g) + 0.0722*ch(b)

def ratio(fg, ground, base):
    """fg over ground (ground itself composited over base if translucent)"""
    gr = to_rgba(ground)
    if gr[3] < 1: gr = over(gr, to_rgba(base))
    f = to_rgba(fg)
    if f[3] < 1: f = over(f, gr)
    l1, l2 = sorted([lum(f), lum(gr)], reverse=True)
    return round((l1 + 0.05) / (l2 + 0.05), 2)

def grade(r):
    return 'AA' if r >= 4.5 else ('large' if r >= 3 else 'fail')

# ---------- main ----------
man = json.load(open(f'{REPO}/manifest.json', encoding='utf-8'))
systems = []
problems = []
for s in man['systems']:
    slug = s['slug']
    if slug not in IDS or slug not in M:
        problems.append(f'{slug}: new system in manifest.json - add an id to IDS and a role mapping to M in extract.py')
        continue
    sid = IDS[slug]
    css = open(f'{REPO}/tokens/{slug}.css', encoding='utf-8').read()
    html = open(f'{REPO}/styles/{slug}/index.html', encoding='utf-8').read()
    vars_ = parse_vars(css)
    body_bg = parse_body_bg(html)
    specs = M[slug]
    assert len(specs) == 8, slug
    roles = {}
    for role, spec in zip(ROLES[:8], specs):
        if spec.startswith('='):
            roles[role] = {'alias': spec[1:], 'src': f'same as `{spec[1:]}`'}
        elif spec.startswith('v:'):
            name = spec[2:]
            if name not in vars_: problems.append(f'{slug}: missing --{name}'); continue
            v = resolve_var(vars_, name)
            if not is_colour(v): problems.append(f'{slug}: --{name} not a flat colour: {v}'); continue
            roles[role] = {'value': norm_hex(v), 'src': f'`--{name}`'}
        elif spec.startswith('g:'):
            _, name, i = spec.split(':')
            cs = colours_in(vars_[name], vars_)
            roles[role] = {'value': cs[int(i)], 'src': f'`--{name}` gradient, stop {int(i)+1} of {len(cs)}'}
        elif spec.startswith('b:'):
            i = int(spec[2:])
            cs = colours_in(body_bg, vars_)
            roles[role] = {'value': cs[i], 'src': f'body background gradient, stop {i+1} of {len(cs)}'}
        else:
            # literal: must appear in the source file unless it is a documented UA default
            lit = norm_hex(spec)
            src = LIT_SRC.get((slug, role))
            if not src: problems.append(f'{slug}.{role}: literal without a source note')
            if slug != '47-default-browser':
                hay = html.lower().replace(' ', '')
                short = lit
                variants = {lit}
                if re.fullmatch(r'#([0-9a-f])\1([0-9a-f])\2([0-9a-f])\3', lit):
                    variants.add('#' + lit[1] + lit[3] + lit[5])
                if not any(v in hay for v in variants):
                    problems.append(f'{slug}.{role}: literal {lit} NOT found in source html')
            roles[role] = {'value': lit, 'src': src or 'literal'}

    def val(role, depth=0):
        r = roles[role]
        return val(r['alias'], depth+1) if 'alias' in r else r['value']

    # onaccent: whichever of the system's own ink/surface/bg/highlight reads best on the accent fill
    acc = val('accent')
    cands = []
    for c in ['ink', 'surface', 'bg', 'highlight']:
        cv = val(c)
        if to_rgba(cv)[3] < 1: continue
        cands.append((ratio(cv, acc, val('bg')), c))
    best = max(cands)
    roles['onaccent'] = {'alias': best[1], 'src': f'computed: the system colour with most contrast on `accent` ({best[1]}, {best[0]}:1)'}

    # fonts
    fonts = {k: v for k, v in vars_.items() if k.startswith('font')}
    if not fonts:  # 40, 47: no tokens
        fonts = {'font': '"Times New Roman", Times, serif'}
    primary_key = next((k for k in ['font', 'font-sys', 'font-pixel'] if k in fonts), sorted(fonts)[0])
    font = fonts[primary_key]
    alt = {k: v for k, v in fonts.items() if k != primary_key}

    res = {r: val(r) for r in ROLES}
    c = {
        'ink_surface': ratio(res['ink'], res['surface'], res['bg']),
        'ink_bg': ratio(res['ink'], res['bg'], res['bg']),
        'muted_surface': ratio(res['muted'], res['surface'], res['bg']),
        'onaccent_accent': ratio(res['onaccent'], res['accent'], res['bg']),
    }
    systems.append({
        'num': s['id'], 'slug': slug, 'id': sid, 'name': s['name'], 'era': s['era'], 'year': s['year'],
        'tags': s['tags'], 'path': s['path'], 'palette': s['palette'],
        'roles': roles, 'resolved': res, 'contrast': c,
        'font': font, 'fontAlt': alt, 'bodySize': body_font_size(html),
        'note': NOTES.get(slug, ''),
    })

if problems:
    print('PROBLEMS:'); print('\n'.join(problems)); sys.exit(1)

json.dump(systems, open(f'{OUT}/systems.json', 'w', encoding='utf-8', newline='\n'), indent=1)

# report
lines = ['| # | System | ink/surface | ink/bg | muted/surface | onaccent/accent |', '|---|---|---|---|---|---|']
tally = {'ink_surface': {'AA':0,'large':0,'fail':0}, 'muted_surface': {'AA':0,'large':0,'fail':0}}
for s in systems:
    c = s['contrast']
    for k in tally: tally[k][grade(c[k])] += 1
    lines.append(f"| {s['num']} | {s['name']} | {c['ink_surface']} {grade(c['ink_surface'])} | {c['ink_bg']} {grade(c['ink_bg'])} | {c['muted_surface']} {grade(c['muted_surface'])} | {c['onaccent_accent']} {grade(c['onaccent_accent'])} |")
open(f'{OUT}/contrast-report.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
print('systems:', len(systems))
print('ink on surface  :', tally['ink_surface'])
print('muted on surface:', tally['muted_surface'])
for s in systems:
    c = s['contrast']
    flags = [k for k in ('ink_surface', 'muted_surface', 'onaccent_accent') if grade(c[k]) != 'AA']
    if flags:
        print(f"  {s['num']:>2} {s['name']:<24} " + '  '.join(f"{k}={c[k]}({grade(c[k])})" for k in flags))
