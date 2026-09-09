#!/usr/bin/env python3
"""
Static site generator — Jackson Pipe

Renders the home page project directory and each work/<slug>/index.html from
projects.json, so adding a project means one JSON entry plus one prose fragment.

  projects.json          ordered newest-first; every field the chrome needs
  work/<slug>/body.html  the case study itself, hand-written HTML

Usage:
  python build_site.py            rewrite the generated files
  python build_site.py --check    exit 1 if anything is out of date
"""

import io
import json
import os
import sys
from collections import OrderedDict

SITE_URL = 'https://jacksonpipe.dev'
EMAIL = 'jackbpipe@gmail.com'
BYLINE = 'Jackson Pipe'

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, 'projects.json')
HOME = os.path.join(ROOT, 'index.html')

# The home page is hand-written apart from the region between these markers.
OPEN_MARK = '        <!-- build:projects -->\n'
CLOSE_MARK = '        <!-- /build:projects -->'


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════
def esc(text):
    """Escape text for element content."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def attr(text):
    """Escape text for a double-quoted attribute value."""
    return esc(text).replace('"', '&quot;')


def read(path):
    return io.open(path, encoding='utf-8').read()


def write(path, text):
    """Write only when the content actually changed."""
    if os.path.exists(path) and read(path) == text:
        return False
    io.open(path, 'w', encoding='utf-8', newline='\n').write(text)
    return True


def load_projects():
    projects = json.loads(read(DATA), object_pairs_hook=OrderedDict)
    slugs = [p['slug'] for p in projects]
    if len(set(slugs)) != len(slugs):
        sys.exit('duplicate slug in projects.json')
    return projects


# ══════════════════════════════════════════════════════════════════════════════
# Home page — the project directory, newest first
# ══════════════════════════════════════════════════════════════════════════════
def render_year(year):
    """A single year, or a range written the way the timeline writes one."""
    if isinstance(year, list):
        return ' — '.join('<time datetime="%s">%s</time>' % (y, y) for y in year)
    return '<time datetime="%s">%s</time>' % (year, year)


def render_row(project):
    heading_id = '%s-title' % project['slug']
    return (
        '          <article class="project"><a class="project-row" href="work/%s/" aria-labelledby="%s">'
        '<div class="project-summary"><h3 id="%s">%s</h3><p>%s</p></div>'
        '<span class="project-tech">%s</span>'
        '<span class="project-year">%s</span>'
        '<span class="project-arrow" aria-hidden="true">↗</span></a></article>'
        % (project['slug'], heading_id, heading_id, esc(project['title']),
           esc(project['summary']), esc(project['tech']), render_year(project['year']))
    )


def render_home(projects):
    home = read(HOME)
    if OPEN_MARK not in home or CLOSE_MARK not in home:
        sys.exit('index.html is missing the build:projects markers')
    start = home.index(OPEN_MARK) + len(OPEN_MARK)
    end = home.index(CLOSE_MARK)
    directory = '\n'.join(
        ['        <div class="project-directory">']
        + [render_row(p) for p in projects]
        + ['        </div>', '']
    )
    return home[:start] + directory + home[end:]


# ══════════════════════════════════════════════════════════════════════════════
# Project pages — chrome rendered around the hand-written body fragment
# ══════════════════════════════════════════════════════════════════════════════
PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <meta name="description" content="{description}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{og_description}">
  <meta property="og:url" content="{url}">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="../../favicon.svg" type="image/svg+xml">
  <meta name="theme-color" content="#f5f3ee" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#1d201e" media="(prefers-color-scheme: dark)">
  <link rel="preload" href="../../assets/fonts/manrope.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="../../styles.css">
  <title>{page_title}</title>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="site">
    <header class="masthead">
      <a class="wordmark" href="../../" aria-label="{byline}, home"><span class="brand-mark" aria-hidden="true">jp<span>.</span></span><span>{byline}</span></a>
      <nav aria-label="Main navigation"><a href="../../#about">Background</a><a href="../../#work">Projects</a><a href="../../#contact">Contact</a><a class="nav-resume" href="../../Resume_Jackson-Pipe.pdf">Résumé <span aria-hidden="true">↗</span></a></nav>
    </header>
    <main id="main" tabindex="-1">
      <a class="back-link" href="../../#work"><span aria-hidden="true">←</span> All projects</a>
      <article>
        <header class="article-header">
          <p class="eyebrow">{eyebrow}</p>
          <h1>{title}</h1>
          <p class="article-lead">{lead}</p>
          <div class="article-meta">{meta}</div>
        </header>
{body}
      </article>
      <div class="article-end"><a href="../{next_slug}/"><span>{next_label}</span><span class="next-title">{next_title} →</span></a><a href="mailto:{email}">Email me about this project <span aria-hidden="true">↗</span></a></div>
    </main>
    <footer class="footer"><a href="../../">{byline}</a><span>Hamilton, Ontario</span></footer>
  </div>
</body>
</html>
"""


def render_meta(project):
    """Work / stack / optional note, then an optional link to the live thing."""
    items = ['<span><strong>Work</strong> %s</span>' % esc(project['work']),
             '<span>%s</span>' % esc(project['stack'])]
    if 'note' in project:
        items.append('<span>%s</span>' % esc(project['note']))
    if 'link' in project:
        items.append('<a href="%s">%s <span aria-hidden="true">↗</span></a>'
                     % (attr(project['link']['href']), esc(project['link']['label'])))
    return ''.join(items)


def render_page(project, projects):
    """Each page points at the next one; the last wraps back to the first."""
    index = projects.index(project)
    following = projects[(index + 1) % len(projects)]
    wrapped = index == len(projects) - 1

    body_path = os.path.join(ROOT, 'work', project['slug'], 'body.html')
    if not os.path.exists(body_path):
        sys.exit('missing prose fragment: %s' % os.path.relpath(body_path, ROOT))

    return PAGE.format(
        description=attr(project['description']),
        og_description=attr(project['ogDescription']),
        page_title=attr('%s — %s' % (project['title'], BYLINE)),
        url='%s/work/%s/' % (SITE_URL, project['slug']),
        byline=esc(BYLINE),
        eyebrow=esc(project['eyebrow']),
        title=esc(project['title']),
        lead=esc(project['lead']),
        meta=render_meta(project),
        body=read(body_path).rstrip('\n'),
        next_slug=following['slug'],
        next_label='Another project' if wrapped else 'Next project',
        next_title=esc(following['title']),
        email=attr(EMAIL),
    )


# ══════════════════════════════════════════════════════════════════════════════
# Build
# ══════════════════════════════════════════════════════════════════════════════
def build(check=False):
    projects = load_projects()

    outputs = [(HOME, render_home(projects))]
    for project in projects:
        outputs.append((os.path.join(ROOT, 'work', project['slug'], 'index.html'),
                        render_page(project, projects)))

    stale = []
    for path, content in outputs:
        name = os.path.relpath(path, ROOT).replace(os.sep, '/')
        if check:
            if not os.path.exists(path) or read(path) != content:
                stale.append(name)
        elif write(path, content):
            print('updated %s' % name)

    if check:
        if stale:
            print('out of date: %s' % ', '.join(stale))
            return 1
        print('%d files up to date' % len(outputs))
    return 0


if __name__ == '__main__':
    sys.exit(build(check='--check' in sys.argv[1:]))
