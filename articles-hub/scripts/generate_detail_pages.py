#!/usr/bin/env python3
"""Generate article detail pages from YAML data."""
import yaml, json, os, sys, re

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'articles')
SITE_DIR = os.path.join(os.path.dirname(__file__), '..', 'site', 'articles')

os.makedirs(SITE_DIR, exist_ok=True)

TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Anthropic Articles</title>
<style>
:root{{:root}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:var(--sans);background:var(--ivory);color:var(--slate);line-height:1.6}}
a{{color:var(--clay);text-decoration:none}}a:hover{{text-decoration:underline}}
header{{background:var(--slate);color:var(--ivory);padding:2rem}}
header h1{{font-family:var(--serif);font-size:1.8rem;margin-bottom:.25rem}}
header .meta{{color:var(--g300);font-size:.9rem}}
nav{{background:var(--paper);border-bottom:1px solid var(--g300);padding:0 2rem;display:flex;gap:1.5rem}}
nav a{{color:var(--slate);padding:.75rem 0;font-size:.9rem;border-bottom:2px solid transparent}}
nav a:hover{{border-bottom-color:var(--clay);text-decoration:none}}
nav a.active{{border-bottom-color:var(--clay);font-weight:600}}
main{{max-width:900px;margin:0 auto;padding:2rem}}
h2{{font-family:var(--serif);font-size:1.3rem;margin:1.5rem 0 .75rem;color:var(--clay);border-bottom:1px solid var(--oat);padding-bottom:.5rem}}
.score-grid{{display:grid;grid-template-columns:200px 1fr;gap:2rem;align-items:start;margin-bottom:1rem}}
.radar-box{{background:var(--paper);border:1px solid var(--g300);border-radius:8px;padding:1rem}}
.scores-list{{background:var(--paper);border:1px solid var(--g300);border-radius:8px;padding:1.25rem}}
.score-row{{display:flex;align-items:center;margin-bottom:.5rem;gap:.75rem}}
.score-row .label{{width:80px;font-size:.85rem;color:var(--g500)}}
.score-row .bar-wrap{{flex:1;height:8px;background:var(--g100);border-radius:4px;overflow:hidden}}
.score-row .bar{{height:100%;background:var(--clay);border-radius:4px;transition:width .3s}}
.score-row .val{{width:30px;font-family:var(--mono);font-size:.9rem;font-weight:700;text-align:right}}
.overall{{text-align:center;margin-bottom:1rem}}
.overall .big{{font-size:3rem;font-weight:700;font-family:var(--serif);color:var(--clay)}}
.grade{{font-size:.85rem;padding:3px 12px;border-radius:4px;font-weight:600;display:inline-block;margin-left:.5rem}}
.g-S{{background:#FDE68A;color:#92400E}}.g-A{{background:#BBF7D0;color:#166534}}.g-B{{background:#BFDBFE;color:#1E40AF}}
.g-C{{background:var(--g100);color:var(--g700)}}.g-D{{background:var(--g300);color:var(--g500)}}
.tags{{display:flex;gap:.5rem;flex-wrap:wrap;margin:.5rem 0}}
.tag{{font-size:.75rem;padding:2px 8px;border-radius:4px;background:var(--g100);color:var(--g500)}}
.tag.cat{{background:var(--oat);color:var(--slate)}}
.tag.diff{{background:var(--clay);color:white}}
.takeaway{{background:var(--paper);border:1px solid var(--g300);border-radius:8px;padding:1rem 1.25rem;margin-bottom:.5rem;font-size:.9rem;position:relative;padding-left:2.5rem}}
.takeaway::before{{content:"\\2605";position:absolute;left:.75rem;top:.75rem;color:var(--clay);font-size:1.2rem}}
.practice{{background:var(--paper);border:1px solid var(--g300);border-radius:8px;padding:1rem 1.25rem;margin-bottom:.75rem}}
.practice h4{{font-family:var(--serif);font-size:.95rem;margin-bottom:.25rem}}
.practice .meta{{font-size:.8rem;color:var(--g500);margin-bottom:.5rem}}
.practice p{{font-size:.9rem;color:var(--g700)}}
.github-link{{display:block;background:var(--paper);border:1px solid var(--g300);border-radius:8px;padding:.75rem 1rem;margin-bottom:.5rem}}
.github-link strong{{display:block;margin-bottom:.25rem}}
.github-link .desc{{font-size:.85rem;color:var(--g500)}}
.github-link .stars{{font-family:var(--mono);font-size:.85rem;color:var(--clay)}}
.mindmap-box{{background:var(--paper);border:1px solid var(--g300);border-radius:8px;padding:1.5rem;overflow-x:auto}}
.outline{{background:var(--paper);border:1px solid var(--g300);border-radius:8px;padding:1rem 1.25rem;margin-bottom:.5rem}}
.outline h4{{font-family:var(--serif);font-size:.95rem;margin-bottom:.15rem;color:var(--clay)}}
.outline .odesc{{font-size:.85rem;color:var(--g500);margin-bottom:.5rem;padding-left:1rem;border-left:2px solid var(--oat)}}
.excerpt-block{{background:var(--paper);border:1px solid var(--g300);border-radius:10px;margin-bottom:1.5rem;overflow:hidden}}
.excerpt-block .eheader{{display:flex;align-items:center;gap:.5rem;padding:.6rem 1.25rem;background:linear-gradient(135deg,var(--oat),#f0e8d8);border-bottom:1px solid var(--g300)}}
.excerpt-block .ebadge{{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:var(--clay);color:white;font-size:.75rem;font-weight:700;font-family:var(--mono)}}
.excerpt-block .econtext{{font-size:.82rem;color:var(--g500);font-weight:500}}
.excerpt-block .eoriginal{{padding:1rem 1.5rem;margin:0;border-left:4px solid var(--olive);background:#f8faf3;font-size:.92rem;line-height:1.75;font-family:var(--serif);color:var(--g700);font-style:italic;position:relative}}
.excerpt-block .eoriginal::before{{content:"原文";position:absolute;top:.75rem;left:-28px;background:var(--olive);color:white;font-size:.6rem;padding:1px 6px;border-radius:3px;font-style:normal;font-family:var(--sans);letter-spacing:.5px}}
.excerpt-block .eimage{{width:100%;border-radius:6px;margin:.75rem 1.25rem;max-height:360px;object-fit:cover}}
.excerpt-block .ecaption{{font-size:.78rem;color:var(--g500);padding:0 1.25rem .5rem;text-align:center;font-style:italic}}
.excerpt-block .ecommentary{{padding:1rem 1.5rem;font-size:.88rem;color:var(--slate);line-height:1.8;border-top:2px solid var(--oat);position:relative}}
.excerpt-block .ecommentary::before{{content:"解读";display:inline-block;background:var(--clay);color:white;font-size:.65rem;padding:2px 8px;border-radius:3px;margin-bottom:.75rem;font-weight:600;letter-spacing:.5px;font-family:var(--sans)}}
.excerpt-block .ecommentary p{{margin-bottom:.75rem}}
.excerpt-block .ecommentary p:first-of-type{{margin-top:.25rem}}
.excerpt-block .ecommentary p:last-child{{margin-bottom:0}}
.excerpt-block .ecommentary strong{{color:var(--clay);font-weight:700}}
.excerpt-block .ecommentary ul,.excerpt-block .ecommentary ol{{margin:.5rem 0 .75rem 1.25rem}}
.excerpt-block .ecommentary li{{margin-bottom:.35rem}}
.excerpt-block .ecommentary li::marker{{color:var(--clay)}}
.excerpt-block .ecommentary code{{font-family:var(--mono);font-size:.82rem;background:var(--g100);padding:1px 5px;border-radius:3px;color:var(--g700)}}
.excerpt-block .ecommentary pre{{background:#1e1e1e;color:#d4d4d4;padding:.75rem 1rem;border-radius:6px;overflow-x:auto;margin:.5rem 0 .75rem;font-size:.82rem;line-height:1.5}}
.excerpt-block .ecommentary pre code{{background:none;padding:0;color:inherit}}
.relation-links{{display:flex;gap:1rem;flex-wrap:wrap;margin-top:.5rem}}
.relation-links a{{font-size:.9rem;padding:4px 10px;border-radius:4px;background:var(--g100)}}
.relation-links a:hover{{background:var(--oat)}}
footer{{text-align:center;padding:2rem;color:var(--g500);font-size:.85rem;border-top:1px solid var(--g300);margin-top:2rem}}
</style>
</head>
<body>
<header>
  <h1>{title}</h1>
  <div class="meta">{date} | {section} | {authors}</div>
</header>
<nav>
  <a href="../index.html">总览</a>
  <a href="../rankings.html">排行榜</a>
  <a href="../categories.html">分类浏览</a>
  <a href="../relations.html">文章关系图</a>
  <a href="../github-map.html">GitHub 映射</a>
</nav>
<main>
  <div class="tags">
    <span class="tag cat">{category} {category_name}</span>
    <span class="tag diff">{difficulty}</span>
    {tags_html}
  </div>

  <h2>综合评分</h2>
  <div class="score-grid">
    <div class="radar-box">
      <div class="overall">
        <div class="big">{overall_score:.1f}</div>
        <span class="grade g-{grade}">{grade} 级</span>
      </div>
      <canvas id="radar" width="180" height="180"></canvas>
    </div>
    <div class="scores-list">
      {score_rows}
    </div>
  </div>

  <h2>核心要点</h2>
  {takeaways_html}

  {outline_html}

  {deep_analysis_html}

  {github_html}

  {practice_html}

  <h2>思维流程导图</h2>
  <div class="mindmap-box">
    <pre class="mermaid">
{mind_map}
    </pre>
  </div>

  {relation_html}

  <p style="margin-top:1rem"><a href="{url}">阅读原文 &rarr;</a></p>
</main>
<footer>Anthropic Articles Knowledge Management System</footer>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad:true,theme:"base",themeVariables:{{primaryColor:"#E3DACC",primaryTextColor:"#141413",lineColor:"#D97757"}}}})</script>
<script>
const dims=["技术深度","可操作性","创新性","影响力","教育价值","时效性","可复现性"];
const vals=[{scores_array}];
const c=document.getElementById("radar").getContext("2d");
const cx=90,cy=90,r=70,n=dims.length;
c.strokeStyle="#D6D3D1";c.lineWidth=1;
for(let i=0;i<n;i++){{c.beginPath();c.moveTo(cx,cy);c.lineTo(cx+r*Math.cos(2*Math.PI*i/n-Math.PI/2),cy+r*Math.sin(2*Math.PI*i/n-Math.PI/2));c.stroke()}}
for(let ring=1;ring<=4;ring++){{c.beginPath();for(let i=0;i<=n;i++){{const a=2*Math.PI*((i%n)/n)-Math.PI/2,rr=r*ring/4;c.lineTo(cx+rr*Math.cos(a),cy+rr*Math.sin(a))}}c.strokeStyle="#F5F5F4";c.stroke()}}
c.beginPath();c.fillStyle="rgba(217,119,87,0.2)";c.strokeStyle="#D97757";c.lineWidth=2;
for(let i=0;i<=n;i++){{const a=2*Math.PI*((i%n)/n)-Math.PI/2,rr=r*vals[i%n]/10;c.lineTo(cx+rr*Math.cos(a),cy+rr*Math.sin(a))}}c.fill();c.stroke();
c.fillStyle="#141413";c.font="11px system-ui";c.textAlign="center";
for(let i=0;i<n;i++){{const a=2*Math.PI*i/n-Math.PI/2,lx=cx+(r+15)*Math.cos(a),ly=cy+(r+15)*Math.sin(a);c.fillText(dims[i],lx,ly+4)}}
</script>
</body>
</html>'''

DEEP_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — 苏格拉底式深度解读</title>
<style>
:root{{:root}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:var(--sans);background:var(--ivory);color:var(--slate);line-height:1.7}}
a{{color:var(--clay);text-decoration:none}}a:hover{{text-decoration:underline}}
.progress-bar{{position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,var(--clay),var(--olive));z-index:100;transition:width .15s}}
.wrap{{max-width:820px;margin:0 auto;padding:2rem 1.5rem}}
.back{{display:inline-flex;align-items:center;gap:.4rem;color:var(--g500);font-size:.88rem;padding:.5rem 0}}
.back:hover{{color:var(--clay);text-decoration:none}}
.deep-header{{padding:1.5rem 0;border-bottom:2px solid var(--oat);margin-bottom:1.5rem}}
.deep-header h1{{font-family:var(--serif);font-size:1.8rem;color:var(--slate);margin-bottom:.2rem}}
.deep-header .sub{{color:var(--clay);font-size:.95rem;font-weight:600}}
.toc{{background:var(--paper);border:1px solid var(--g300);border-radius:8px;padding:1rem 1.25rem;margin-bottom:2rem}}
.toc h3{{font-family:var(--serif);font-size:.95rem;margin-bottom:.6rem;color:var(--slate)}}
.toc a{{display:block;padding:.3rem 0;color:var(--g500);font-size:.88rem;border-bottom:1px solid var(--g100)}}
.toc a:last-child{{border-bottom:none}}
.toc a:hover{{color:var(--clay)}}
.sec{{margin-bottom:3rem}}
.sec-title{{display:flex;align-items:center;gap:.75rem;font-family:var(--serif);font-size:1.25rem;color:var(--slate);margin-bottom:1.25rem;padding-bottom:.5rem;border-bottom:2px solid var(--oat)}}
.sec-num{{display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;border-radius:50%;background:var(--clay);color:white;font-size:.9rem;font-weight:700;font-family:var(--mono);flex-shrink:0}}
.excerpt-card{{background:var(--paper);border:1px solid var(--g300);border-left:4px solid var(--olive);border-radius:0 8px 8px 0;padding:1.25rem 1.5rem;margin-bottom:1.5rem;position:relative}}
.excerpt-card .elabel{{font-size:.72rem;color:var(--olive);font-weight:700;letter-spacing:1px;margin-bottom:.4rem}}
.excerpt-card blockquote{{font-family:var(--serif);font-size:.92rem;line-height:1.75;color:var(--g700);font-style:italic;padding-left:1rem;border-left:3px solid var(--oat);margin:0}}
.excerpt-card blockquote::before{{content:"\\201C";position:absolute;left:1rem;top:1.8rem;font-size:2.5rem;color:var(--oat);font-family:Georgia,serif;line-height:1;opacity:.5}}
.excerpt-card img{{width:100%;border-radius:6px;margin-top:.75rem;max-height:380px;object-fit:cover}}
.excerpt-card .ecap{{font-size:.78rem;color:var(--g500);text-align:center;margin-top:.4rem;font-style:italic}}
.analogy-card{{background:linear-gradient(135deg,#FFFAF3,#FFF5E8);border:1px solid #E8D5BF;border-radius:10px;padding:1.25rem 1.5rem;margin-bottom:1.5rem}}
.analogy-card .alabel{{font-size:.78rem;color:var(--clay);font-weight:700;letter-spacing:.5px;margin-bottom:.5rem}}
.analogy-card p{{font-size:.92rem;line-height:1.75;color:var(--slate)}}
.qa-chain{{margin-bottom:1.5rem}}
.qa-pair{{margin-bottom:.75rem;padding:.75rem 1rem .75rem 1.25rem;border-radius:6px;position:relative}}
.qa-pair.depth-0{{background:var(--paper);border-left:3px solid var(--clay)}}
.qa-pair.depth-1{{margin-left:1.5rem;background:#FAFAF5;border-left:3px solid var(--olive)}}
.qa-pair.depth-2{{margin-left:3rem;background:#F5F5F0;border-left:3px solid #A8A29E}}
.qa-pair .q{{font-weight:700;color:var(--slate);font-size:.92rem;margin-bottom:.3rem;display:flex;align-items:start;gap:.5rem}}
.qa-pair .q::before{{content:"Q";display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;border-radius:50%;background:var(--clay);color:white;font-size:.6rem;font-weight:700;flex-shrink:0;margin-top:2px}}
.qa-pair.depth-1 .q::before{{background:var(--olive)}}
.qa-pair.depth-2 .q::before{{background:#A8A29E}}
.qa-pair .a{{font-size:.88rem;color:var(--g700);line-height:1.75;padding-left:1.7rem}}
.diagram-card{{background:var(--paper);border:1px solid var(--g300);border-radius:8px;padding:1.25rem;margin-bottom:1.5rem}}
.diagram-card .dlabel{{font-size:.78rem;color:var(--clay);font-weight:700;letter-spacing:.5px;margin-bottom:.6rem}}
.diagram-card .dcap{{font-size:.78rem;color:var(--g500);text-align:center;margin-top:.5rem}}
.gh-ref{{display:flex;align-items:start;gap:.75rem;background:var(--paper);border:1px solid var(--g300);border-radius:8px;padding:.85rem 1rem;margin-bottom:.5rem;text-decoration:none}}
.gh-ref:hover{{border-color:var(--clay);text-decoration:none}}
.gh-icon{{width:30px;height:30px;border-radius:6px;background:var(--slate);color:white;display:flex;align-items:center;justify-content:center;font-size:.7rem;font-weight:700;flex-shrink:0}}
.gh-ref .gh-name{{font-weight:600;color:var(--slate);font-size:.88rem}}
.gh-ref .gh-path{{font-family:var(--mono);font-size:.78rem;color:var(--clay);margin-top:.15rem}}
.gh-ref .gh-note{{font-size:.82rem;color:var(--g500);margin-top:.15rem}}
.nav-links{{display:flex;justify-content:space-between;margin-top:2rem;padding-top:1rem;border-top:1px solid var(--g300)}}
.nav-links a{{font-size:.88rem}}
footer{{text-align:center;padding:2rem;color:var(--g500);font-size:.82rem;border-top:1px solid var(--g300);margin-top:1.5rem}}
</style>
</head>
<body>
<div class="progress-bar" id="pbar"></div>
<div class="wrap">
<a href="{slug}.html" class="back">&larr; 返回文章详情</a>
<div class="deep-header">
<h1>{title}</h1>
<div class="sub">苏格拉底式深度解读</div>
</div>
{toc_html}
{sections_html}
<div class="nav-links">
<a href="{slug}.html">&larr; 返回文章详情</a>
<a href="{url}" target="_blank">阅读原文 &rarr;</a>
</div>
</div>
<footer>Anthropic Articles Knowledge Management System</footer>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad:true,theme:"base",themeVariables:{{primaryColor:"#E3DACC",primaryTextColor:"#141413",lineColor:"#D97757"}}}})</script>
<script>
window.addEventListener('scroll',function(){{var s=document.documentElement.scrollTop,h=document.documentElement.scrollHeight-document.documentElement.clientHeight;document.getElementById('pbar').style.width=(s/h*100)+'%'}});
</script>
</body>
</html>'''

DIM_NAMES = ['technical_depth', 'actionability', 'novelty', 'impact', 'educational_value', 'timeliness', 'reproducibility']
DIM_LABELS = ['技术深度', '可操作性', '创新性', '影响力', '教育价值', '时效性', '可复现性']
DIM_WEIGHTS = [1.1, 1.3, 1.0, 1.3, 1.1, 1.0, 1.0]
CAT_NAMES = {'C1': 'Agent 开发', 'C2': '工程实践', 'C3': '模型研究', 'C4': '工具与平台', 'C5': '安全与政策'}

CSS_VARS = '--ivory:#FAF9F5;--paper:#FFF;--slate:#141413;--clay:#D97757;--oat:#E3DACC;--olive:#788C5D;--g100:#F5F5F4;--g300:#D6D3D1;--g500:#78716C;--g700:#44403C;--serif:Georgia,serif;--sans:system-ui,sans-serif;--mono:"SF Mono",Menlo,monospace'

def grade(score):
    if score >= 9: return 'S'
    if score >= 8: return 'A'
    if score >= 7: return 'B'
    if score >= 6: return 'C'
    return 'D'

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def inline_md(text):
    """Convert inline markdown: bold, code, links."""
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text

def md_to_html(text):
    """Convert a subset of markdown to structured HTML."""
    lines = text.split('\n')
    out = []
    in_code = False
    in_list = False
    list_tag = None

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Code block toggle
        if stripped.startswith('```'):
            if not in_code:
                if in_list:
                    out.append(f'</{list_tag}>')
                    in_list = False
                lang = stripped[3:].strip()
                cls = f' class="lang-{lang}"' if lang else ''
                out.append(f'<pre><code{cls}>')
                in_code = True
            else:
                out.append('</code></pre>')
                in_code = False
            i += 1
            continue

        if in_code:
            out.append(escape_html(line))
            i += 1
            continue

        # Blank line
        if not stripped:
            if in_list:
                out.append(f'</{list_tag}>')
                in_list = False
            i += 1
            continue

        # Ordered list
        ol_m = re.match(r'^(\d+)\.\s+(.*)', stripped)
        if ol_m:
            if not in_list or list_tag != 'ol':
                if in_list:
                    out.append(f'</{list_tag}>')
                out.append('<ol>')
                in_list = True
                list_tag = 'ol'
            out.append(f'<li>{inline_md(ol_m.group(2))}</li>')
            i += 1
            continue

        # Unordered list
        if stripped.startswith('- '):
            if not in_list or list_tag != 'ul':
                if in_list:
                    out.append(f'</{list_tag}>')
                out.append('<ul>')
                in_list = True
                list_tag = 'ul'
            out.append(f'<li>{inline_md(stripped[2:])}</li>')
            i += 1
            continue

        # Regular paragraph
        if in_list:
            out.append(f'</{list_tag}>')
            in_list = False
        out.append(f'<p>{inline_md(stripped)}</p>')
        i += 1

    if in_list:
        out.append(f'</{list_tag}>')

    return '\n'.join(out)

def gen_detail(data):
    scores = data['scores']
    vals = [scores[d] for d in DIM_NAMES]
    ov = data['overall_score']
    g = grade(ov)

    score_rows = ''
    for i, (label, val) in enumerate(zip(DIM_LABELS, vals)):
        w = DIM_WEIGHTS[i]
        weight_str = f' (x{w})' if w != 1.0 else ''
        score_rows += f'<div class="score-row"><span class="label">{label}{weight_str}</span><div class="bar-wrap"><div class="bar" style="width:{val*10}%"></div></div><span class="val">{val}</span></div>\n'

    takeaways_html = ''
    for t in data.get('key_takeaways', []):
        takeaways_html += f'<div class="takeaway">{t}</div>\n'

    tags_html = ''
    for t in data.get('tags', [])[:5]:
        tags_html += f'<span class="tag">{t}</span>\n'

    github_html = ''
    gh_projects = data.get('related_github_projects', [])
    if gh_projects:
        github_html = '<h2>关联 GitHub 项目</h2>\n'
        for p in gh_projects:
            stars = f'<span class="stars">{p.get("stars","N/A")} stars</span>' if p.get('stars') else ''
            github_html += f'<a href="{p["url"]}" class="github-link"><strong>{p["name"]}</strong>{stars}<div class="desc">{p["description"]}</div></a>\n'

    outline_html = ''
    outline = data.get('outline', [])
    if outline:
        outline_html = '<h2>文章结构大纲</h2>\n'
        for i, item in enumerate(outline, 1):
            outline_html += f'<div class="outline"><h4>{i}. {item["title"]}</h4><div class="odesc">{item["description"]}</div></div>\n'

    deep_analysis_html = ''
    deep_analysis = data.get('deep_analysis', [])
    if deep_analysis:
        has_deep = any(item.get('qa_chain') for item in deep_analysis)
        deep_link = f' <a href="deep-{data["slug"]}.html" style="font-size:.78rem;color:var(--clay);font-weight:400;vertical-align:middle">苏格拉底式深度解读 &rarr;</a>' if has_deep else ''
        deep_analysis_html = f'<h2>深度解读{deep_link}</h2>\n'
        for idx, item in enumerate(deep_analysis, 1):
            commentary_html = md_to_html(item['commentary'])
            image_html = ''
            if item.get('image'):
                caption = f'<div class="ecaption">{item["image_caption"]}</div>' if item.get('image_caption') else ''
                image_html = f'<img class="eimage" src="{item["image"]}" alt="{item.get("image_caption", "")}" loading="lazy">\n{caption}\n'
            deep_analysis_html += f'''<div class="excerpt-block">
<div class="eheader"><span class="ebadge">{idx}</span><span class="econtext">{item["context"]}</span></div>
<div class="eoriginal">{item["excerpt"]}</div>
{image_html}<div class="ecommentary">{commentary_html}</div>
</div>\n'''

    practice_html = ''
    practices = data.get('practice_ideas', [])
    if practices:
        practice_html = '<h2>代码实践建议</h2>\n'
        for p in practices:
            practice_html += f'<div class="practice"><h4>{p["title"]}</h4><div class="meta">{p["difficulty"]} | {p["tech_stack"]}</div><p>{p["description"]}</p></div>\n'

    relation_html = ''
    prereqs = data.get('prerequisites', [])
    follows = data.get('follows_up', [])
    if prereqs or follows:
        relation_html = '<h2>文章关系</h2><div class="relation-links">\n'
        for p in prereqs:
            relation_html += f'<a href="{p}.html">前置: {p}</a>\n'
        for f in follows:
            relation_html += f'<a href="{f}.html">后续: {f}</a>\n'
        relation_html += '</div>\n'

    mind_map = data.get('mind_map', 'flowchart TD\n    A["No mind map"]')

    authors = ', '.join(data.get('authors', []))
    section = data['section'].capitalize()

    html = TEMPLATE.format(
        title=data['title'],
        date=data['date'],
        section=section,
        authors=authors,
        category=data['category'],
        category_name=CAT_NAMES.get(data['category'], ''),
        difficulty=data['difficulty'],
        tags_html=tags_html,
        overall_score=ov,
        grade=g,
        score_rows=score_rows,
        takeaways_html=takeaways_html,
        outline_html=outline_html,
        deep_analysis_html=deep_analysis_html,
        github_html=github_html,
        practice_html=practice_html,
        mind_map=mind_map,
        relation_html=relation_html,
        url=data['url'],
        scores_array=','.join(str(v) for v in vals),
        root=CSS_VARS
    )
    return html

def gen_deep_dive(data):
    """Generate a standalone deep-dive Socratic analysis page."""
    slug = data['slug']
    deep_analysis = data.get('deep_analysis', [])
    if not any(item.get('qa_chain') for item in deep_analysis):
        return None

    # TOC
    toc_html = '<div class="toc"><h3>解读目录</h3>\n'
    for i, item in enumerate(deep_analysis, 1):
        toc_html += f'<a href="#s{i}">{i}. {item["context"]}</a>\n'
    toc_html += '</div>\n'

    # Sections
    sections_html = ''
    for i, item in enumerate(deep_analysis, 1):
        ctx = item.get('context', f'要点 {i}')
        sections_html += f'<div class="sec" id="s{i}">\n'
        sections_html += f'<div class="sec-title"><span class="sec-num">{i}</span>{ctx}</div>\n'

        # Excerpt card
        img_html = ''
        if item.get('image'):
            cap = f'<div class="ecap">{item["image_caption"]}</div>' if item.get('image_caption') else ''
            img_html = f'<img src="{item["image"]}" alt="{item.get("image_caption","")}" loading="lazy">\n{cap}'
        sections_html += f'<div class="excerpt-card"><div class="elabel">原文摘录</div><blockquote>{item["excerpt"]}</blockquote>{img_html}</div>\n'

        # Analogy
        if item.get('analogy'):
            sections_html += f'<div class="analogy-card"><div class="alabel">&#128161; 类比理解</div><p>{inline_md(item["analogy"])}</p></div>\n'

        # Q&A chain
        for qa in item.get('qa_chain', []):
            d = qa.get('depth', 0)
            sections_html += f'<div class="qa-pair depth-{d}"><div class="q">{qa["q"]}</div><div class="a">{inline_md(qa["a"])}</div></div>\n'

        # Diagram
        if item.get('diagram'):
            dcap = f'<div class="dcap">{item["diagram_caption"]}</div>' if item.get('diagram_caption') else ''
            sections_html += f'<div class="diagram-card"><div class="dlabel">&#128202; 原理图解</div><pre class="mermaid">\n{item["diagram"]}\n</pre>{dcap}</div>\n'

        # GitHub refs
        for ref in item.get('github_refs', []):
            path_html = f'<div class="gh-path">{ref["path"]}</div>' if ref.get('path') else ''
            sections_html += f'<a href="{ref["url"]}" class="gh-ref" target="_blank"><div class="gh-icon">GH</div><div><div class="gh-name">{ref["name"]}</div>{path_html}<div class="gh-note">{ref.get("note","")}</div></div></a>\n'

        sections_html += '</div>\n'

    html = DEEP_TEMPLATE.format(
        title=data['title'], slug=slug, url=data['url'],
        toc_html=toc_html, sections_html=sections_html, root=CSS_VARS
    )
    return html

def main():
    count = 0
    deep_count = 0
    for section in ['engineering', 'research']:
        section_dir = os.path.join(DATA_DIR, section)
        if not os.path.isdir(section_dir):
            continue
        for fname in sorted(os.listdir(section_dir)):
            if not fname.endswith('.yaml'):
                continue
            fpath = os.path.join(section_dir, fname)
            data = load_yaml(fpath)
            slug = data['slug']
            html = gen_detail(data)
            out_path = os.path.join(SITE_DIR, f'{slug}.html')
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html)
            count += 1

            deep_html = gen_deep_dive(data)
            if deep_html:
                deep_path = os.path.join(SITE_DIR, f'deep-{slug}.html')
                with open(deep_path, 'w', encoding='utf-8') as f:
                    f.write(deep_html)
                deep_count += 1
                print(f'  Generated: {slug}.html + deep-{slug}.html ({data["overall_score"]})')
            else:
                print(f'  Generated: {slug}.html ({data["overall_score"]})')
    print(f'\nTotal: {count} pages, {deep_count} deep-dive pages.')

if __name__ == '__main__':
    main()
