#!/usr/bin/env python3
"""Create a brand project folder, or fill in what is missing, without overwriting anything.

The projects directory is --root, else $MIXREEL_PROJECTS_DIR, else
mixreel-projects/ under the current working directory. No network.
"""
import argparse
import json
import os
from pathlib import Path
import re
import sys

SKILL = Path(__file__).resolve().parents[1]
ENV = 'MIXREEL_PROJECTS_DIR'
DEFAULT = 'mixreel-projects'

BRAND_FILES = {
    'brand-context.md': (
        '# Brand context\n\n'
        '## Product\n\nWhat it is and what it does.\n\n'
        '## What is actually different\n\nEach difference, with the screenshot or photo that shows it.\n\n'
        '## Audience\n\nWho it is for, market, language, and the channels the ads run on.\n\n'
        '## Key messages\n\nThe one or two things they most want people to know.\n\n'
        '## Claims\n\n| Claim | Source | Conditions |\n| --- | --- | --- |\n\n'
        '## Must not claim\n\n\n'
        '## Assets\n\nEach file in `assets/`, what it may be used for, and where the real UI comes from. '
        'Missing files stay listed as missing.\n'),
    'requirements.md': (
        '# Requirements\n\n'
        "The client's standing rules for deliverables: lengths, ratios, channels, logo placement, "
        'end card, captions, words to avoid. Every stage follows them.\n'),
    'audience-taste.md': (
        '# Audience taste\n\n'
        'Longings broken down, familiar material, approved scripts with what the user said, '
        'rejected approaches with the reason.\n'),
    'competitors.md': (
        '# Competitors\n\n'
        'How competitors advertise and what their audience reacts to.\n'),
    'films.md': (
        '# Films\n\n'
        'One row per film idea with a written script. Add the row when a script is written. '
        'Update it when it goes into production, at each rework, when the film is delivered '
        'and when results come in. State is drafted, in production, delivered, running, '
        'turned down or cancelled. Why the user turned an idea down goes in audience-taste.md.\n\n'
        '| Film folder | Idea | Product | Key message | Theme | Moment it borrows | State | Script | '
        'Final file | What the user said | Rework count | Rework log | Ad sets and results |\n'
        '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n'),
}
BRAND_DIRS = ('assets', 'taste-library')


def slug(name):
    value = re.sub(r'[^\w-]+', '-', name.strip().lower()).strip('-')
    if not value or value in ('.', '..'):
        raise ValueError('Brand or film name must contain letters or digits')
    return value


def projects_root(root=None, environ=None, cwd=None):
    environ = os.environ if environ is None else environ
    if root:
        return Path(root).expanduser().absolute()
    if environ.get(ENV):
        return Path(environ[ENV]).expanduser().absolute()
    return Path(cwd or Path.cwd()).absolute() / DEFAULT


def write_new(path, text, results, key):
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ValueError('Not a regular file: ' + key)
    try:
        with path.open('x') as stream:
            stream.write(text)
    except FileExistsError:
        results[key] = 'preserved'
        return
    results[key] = 'created'


def initialize(brand, film=None, root=None, environ=None, cwd=None):
    project = projects_root(root, environ, cwd) / slug(brand)
    if project.resolve().is_relative_to(SKILL.resolve()):
        raise ValueError('Projects must be outside the installed skill')
    results = {}
    brand_dir = project / 'brand'
    for name in BRAND_DIRS:
        target = brand_dir / name
        existed = target.is_dir()
        target.mkdir(parents=True, exist_ok=True)
        results['brand/' + name + '/'] = 'preserved' if existed else 'created'
    for name, text in BRAND_FILES.items():
        write_new(brand_dir / name, text, results, 'brand/' + name)
    film_dir = None
    if film:
        film_dir = project / slug(film)
        film_dir.mkdir(parents=True, exist_ok=True)
        brief = (SKILL / 'assets' / 'BRIEF.template.md').read_text()
        write_new(film_dir / 'BRIEF.md', brief, results, slug(film) + '/BRIEF.md')
    return {'project': str(project), 'film': str(film_dir) if film_dir else None,
            'files': results, 'network_requests': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--brand', required=True, help='brand or client name')
    parser.add_argument('--film', help='optional film folder to create inside the project')
    parser.add_argument('--root', help='projects directory (default: $%s, else ./%s)' % (ENV, DEFAULT))
    args = parser.parse_args()
    try:
        result = initialize(args.brand, args.film, args.root)
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Project initialization failed: {exc}\n')
    # Show non-ASCII paths as written. A terminal that cannot encode them gets an escape, not a crash.
    sys.stdout.reconfigure(errors='backslashreplace')
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
