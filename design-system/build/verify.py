#!/usr/bin/env python3
"""Local check before publishing: validate tokens.json against the type's grammar, compile a
tokens.css the way the page documents it, and render every preview headless in each theme."""
import json, os, re, sys, asyncio, pathlib
# Paths: this file lives in design-system/build/ of the repo.
DS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # design-system/
REPO = os.path.dirname(DS)                                          # repo root
HERE = DS
P = os.path.join(HERE, 'project')
WORK = os.path.join(HERE, '.verify'); os.makedirs(WORK, exist_ok=True)
OUT = os.path.join(WORK, 'shots'); os.makedirs(OUT, exist_ok=True)
tj = json.load(open(f'{P}/tokens.json', encoding='utf-8'))
errs = []

NAME = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$')
COL = re.compile(r'^(#[0-9a-f]{3,4}|#[0-9a-f]{6}|#[0-9a-f]{8}|rgba?\([\d\s.,%]+\))$')
themes = [t['id'] for t in tj['color']['themes']]
if len(themes) > 8: errs.append('more than 8 themes')
colors = {t['name']: t for t in tj['color']['tokens']}
if len(colors) > 600: errs.append('more than 600 colors')
allnames = list(colors) + [t['name'] for f in ('spacing', 'radius', 'shadow') for t in tj[f]['tokens']]
if len(allnames) != len(set(allnames)): errs.append('duplicate token names')
for n in allnames:
    if not NAME.match(n): errs.append(f'bad name {n}')

def val_for(tok, theme):
    v = tok['value']
    return v if isinstance(v, str) else v.get(theme, v[themes[0]])

def resolve(name, theme, depth=0):
    if depth > 16: raise ValueError('alias chain too deep: ' + name)
    v = val_for(colors[name], theme)
    m = re.fullmatch(r'\{([^}]+)\}', v)
    if m:
        if m.group(1) not in colors: raise ValueError(f'{name} -> missing {m.group(1)}')
        if m.group(1) == name: raise ValueError('self alias ' + name)
        return resolve(m.group(1), theme, depth + 1)
    if not COL.match(v): raise ValueError(f'{name}: invalid colour {v}')
    return v
for n in colors:
    for t in themes:
        try: resolve(n, t)
        except ValueError as e: errs.append(str(e))
for t in tj['color']['tokens']:
    if len(t.get('usage', '')) > 1000: errs.append('usage too long ' + t['name'])
    if not t.get('usage'): errs.append('no usage ' + t['name'])
for k, v in tj['type']['families'].items():
    if len(v) > 200 or re.search(r'[;{}<>\\()]', v): errs.append('bad family ' + k)
styles = [s for g in tj['type']['groups'] for s in g['styles']]
if len(styles) > 80: errs.append('too many styles')

def cssval(v):
    m = re.fullmatch(r'\{([^}]+)\}', v)
    return f'var(--{m.group(1)})' if m else v

first = themes[0]
lines = [f':root, [data-theme="{first}"] {{']
for t in tj['color']['tokens']:
    lines.append(f"  --{t['name']}: {cssval(val_for(t, first))};")
for t in tj['shadow']['tokens']:
    lines.append(f"  --{t['name']}: {t['value']};")
lines.append('}')
for th in themes[1:]:
    lines.append(f'[data-theme="{th}"] {{')
    for t in tj['color']['tokens']:
        if isinstance(t['value'], dict) and th in t['value']:
            lines.append(f"  --{t['name']}: {cssval(t['value'][th])};")
    lines.append('}')
lines.append(':root {')
for f in ('spacing', 'radius'):
    for t in tj[f]['tokens']: lines.append(f"  --{t['name']}: {t['value']};")
for k, v in tj['type']['families'].items(): lines.append(f'  --font-{k}: {v};')
lines.append('}')
tokens_css = '\n'.join(lines)
open(os.path.join(WORK, 'tokens.test.css'), 'w', encoding='utf-8', newline='\n').write(tokens_css)

print('grammar:', 'OK' if not errs else 'ERRORS')
for e in errs[:30]: print('  ', e)
if errs: sys.exit(1)

bundle_css = open(f'{P}/components/bundle.css', encoding='utf-8').read()
bundle_js = open(f'{P}/components/bundle.js', encoding='utf-8').read()

def frame(preview_html, theme):
    body = preview_html.split('\n', 1)[1]  # drop the marker line
    inject = f'<style>{tokens_css}</style><style>{bundle_css}</style><script>{bundle_js}</script>'
    body = body.replace('<head>', '<head>' + inject, 1)
    return body.replace('<html lang="en">', f'<html lang="en" data-theme="{theme}">', 1)

async def main():
    from playwright.async_api import async_playwright
    comps = ['Cover', 'RetroWindow', 'SystemSwitcher', 'PaletteGrid']
    problems = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for comp in comps:
            html = open(f'{P}/components/{comp}/preview.html', encoding='utf-8').read()
            m = re.search(r'height=(\d+)', html.split('\n')[0]); h = int(m.group(1)) if m else 400
            for th in (themes if comp in ('Cover', 'RetroWindow') else [themes[0], 'win95']):
                pg = await b.new_page(viewport={'width': 960, 'height': h})
                msgs = []
                pg.on('console', lambda m, msgs=msgs: msgs.append(m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
                pg.on('pageerror', lambda e, msgs=msgs: msgs.append('pageerror: ' + str(e)))
                path = os.path.join(WORK, f'_t_{comp}_{th}.html')
                open(path, 'w', encoding='utf-8', newline='\n').write(frame(html, th))
                await pg.goto(pathlib.Path(path).as_uri())
                await pg.wait_for_timeout(700)
                msgs = [m for m in msgs if 'fonts.googleapis' not in m and 'net::' not in m]
                if msgs: problems.append((comp, th, msgs))
                await pg.screenshot(path=os.path.join(OUT, f'{comp}_{th}.png'), full_page=(comp == 'PaletteGrid'))
                if comp == 'SystemSwitcher' and th == themes[0]:
                    # exercise: step through all 53 with the Next button, collect any errors
                    for _ in range(53):
                        await pg.click('button[aria-label="Next system"]')
                    cur = await pg.eval_on_selector('select', 'e => e.value')
                    info = await pg.inner_text('.rt-info')
                    print('switcher after 53 steps ->', cur, '|', info.splitlines()[0])
                    await pg.select_option('select', 'c64')
                    await pg.screenshot(path=os.path.join(OUT, 'SystemSwitcher_c64.png'))
                    await pg.select_option('select', 'geocities')
                    await pg.screenshot(path=os.path.join(OUT, 'SystemSwitcher_geocities.png'))
                    await pg.select_option('select', 'glass')
                    await pg.screenshot(path=os.path.join(OUT, 'SystemSwitcher_glass.png'))
                    # compare the page's live contrast with the build's Python numbers
                    js = await pg.evaluate("() => Retro.systems.map(s => [s.id, Retro.contrast(s.id,'ink','surface'), Retro.contrast(s.id,'muted','surface')])")
                    S = {s['id']: s for s in json.load(open(os.path.join(HERE, 'systems.json'), encoding='utf-8'))}
                    bad = [(i, a, m, S[i]['contrast']['ink_surface'], S[i]['contrast']['muted_surface']) for i, a, m in js
                           if abs(a - S[i]['contrast']['ink_surface']) > 0.02 or abs(m - S[i]['contrast']['muted_surface']) > 0.02]
                    print('JS vs Python contrast mismatches:', bad or 'none')
                    if msgs: problems.append((comp, 'stepping', msgs))
                await pg.close()
        await b.close()
    print('render problems:', problems or 'none')

asyncio.run(main())
