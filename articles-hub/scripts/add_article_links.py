#!/usr/bin/env python3
"""Add clickable article links to existing HTML pages (fuzzy matching)."""
import re, os, yaml

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'articles')
SITE_DIR = os.path.join(os.path.dirname(__file__), '..', 'site')

title_to_slug = {}
slug_to_title = {}
for section in ['engineering', 'research']:
    section_dir = os.path.join(DATA_DIR, section)
    if not os.path.isdir(section_dir):
        continue
    for fname in sorted(os.listdir(section_dir)):
        if not fname.endswith('.yaml'):
            continue
        with open(os.path.join(section_dir, fname), 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        title_to_slug[data['title']] = data['slug']
        slug_to_title[data['slug']] = data['title']

def find_slug(h4_text):
    """Try multiple strategies to find the slug for an h4 title."""
    text = h4_text.strip()
    # Exact match
    if text in title_to_slug:
        return title_to_slug[text]
    # Try matching if h4 text is a prefix of a YAML title
    for title, slug in title_to_slug.items():
        if title.startswith(text):
            return slug
    # Try if YAML title starts with h4 text
    for title, slug in title_to_slug.items():
        if text.startswith(title):
            return slug
    # Fuzzy: normalize both and check containment
    norm_text = text.lower().replace(':', '').replace('"', '').replace('"', '')
    for title, slug in title_to_slug.items():
        norm_title = title.lower().replace(':', '').replace('"', '').replace('"', '')
        if norm_text in norm_title or norm_title in norm_text:
            return slug
    # Check key words (first 4+ words)
    words = text.split()[:4]
    if len(words) >= 2:
        phrase = ' '.join(words).lower()
        for title, slug in title_to_slug.items():
            if phrase in title.lower():
                return slug
    return None

def linkify_h4(match):
    # Skip if already linked
    inner = match.group(1)
    if '<a ' in inner:
        return match.group(0)
    title = re.sub(r'<[^>]+>', '', inner).strip()
    slug = find_slug(title)
    if slug:
        return f'<h4><a href="articles/{slug}.html">{title}</a></h4>'
    return match.group(0)

for page in ['index.html', 'categories.html']:
    path = os.path.join(SITE_DIR, page)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    html = re.sub(r'<h4>([^<]+)</h4>', linkify_h4, html)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    linked = html.count('<h4><a href="articles/')
    remaining = len(re.findall(r'<h4>(?!<a)', html))
    print(f'  {page}: {linked} linked, {remaining} non-article h4 remaining')

# rankings.html uses JS to render - need to update the JS data
path = os.path.join(SITE_DIR, 'rankings.html')
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# Find the articles data array in JS and add slug field
def add_slug_to_data(match):
    entry = match.group(0)
    # Extract title from the entry
    title_match = re.search(r'title:\s*"([^"]+)"', entry)
    if not title_match:
        return entry
    title = title_match.group(1)
    slug = find_slug(title)
    if slug and 'slug:' not in entry:
        return entry.rstrip() + f',\n      slug: "{slug}"'
    return entry

# Update the render function to make titles clickable
html = re.sub(r'const td = document\.createElement\("td"\);\s*td\.textContent = article\.title;',
              'const td = document.createElement("td");\n      const a = document.createElement("a");\n      a.href = "articles/" + article.slug + ".html";\n      a.textContent = article.title;\n      a.style.color = "var(--clay)";\n      td.appendChild(a);',
              html)

# Add slug to each article data entry
# Pattern: {title: "...", section: "...", ...}
def inject_slug(match):
    block = match.group(0)
    title_m = re.search(r'title:\s*"([^"]+)"', block)
    if not title_m:
        return block
    slug = find_slug(title_m.group(1))
    if slug and 'slug:' not in block:
        return block.replace('title:', f'slug: "{slug}",\n      title:')
    return block

html = re.sub(r'\{[^}]+title:[^}]+\}', inject_slug, html)

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'  rankings.html: updated with slug links')

print('\nDone!')
