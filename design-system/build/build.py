#!/usr/bin/env python3
"""Rebuild the TrillFx Retro Design System from the repo's own styles/ and tokens/.

    python design-system/build/build.py            # extract -> tokens, components, README
    python design-system/build/build.py --verify   # also render every preview headless (needs: pip install playwright; playwright install chromium)

Outputs land in design-system/project/ (the files the Design System artifact holds),
plus design-system/systems.json and design-system/contrast-report.md.
"""
import os, runpy, sys
HERE = os.path.dirname(os.path.abspath(__file__))
steps = ['extract.py', 'gen.py', 'readme.py'] + (['verify.py'] if '--verify' in sys.argv else [])
for step in steps:
    print(f'== {step}')
    runpy.run_path(os.path.join(HERE, step), run_name='__main__')
print('done')
