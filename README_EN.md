# Claude Code Insights

> Systematic intelligence on Claude Code version evolution and Anthropic's technical ecosystem.

English | **[中文](README.md)**

## Quick Preview

| Module | Preview | Description |
|--------|---------|-------------|
| Version Chronicle | **[Open →](version-chronicle/index.html)** | v0.2.21 → v2.1.150, 15 milestones |
| Articles Hub | **[Open →](articles-hub/site/index.html)** | 42 articles + 7-dim scoring dashboard |
| HTML Showcase | **[Open →](html-showcase/index.html)** | 20 zero-dependency interactive demos |

<!-- TODO: Add screenshots here
![Version Chronicle](docs/images/version-chronicle.png)
![Articles Dashboard](docs/images/articles-dashboard.png)
![HTML Showcase](docs/images/html-showcase.png)
-->

Three modules, **zero dependencies** (pure HTML/CSS/JS, no build tools). Clone and browse.

## Modules

### [Version Chronicle](version-chronicle/) — Claude Code Timeline

Tracking Claude Code's evolution from **v0.2.21 to v2.1.150**.

- **15 milestone versions** with detailed feature breakdown
- **4 eras** (Genesis → Growth → Maturation → Acceleration) with expandable timelines
- **Model evolution cards** (Opus / Sonnet / Haiku progression)
- **SVG charts**: donut chart, heatmap, area chart, milestone timeline
- **3-phase roadmap**: Released / In Progress / Long-term Vision
- **Interactive**: Category filtering, card/timeline view toggle, dependency graph

<!-- TODO: Replace with actual screenshot -->
<!-- ![Version Chronicle Screenshot](docs/images/version-chronicle.png) -->

### [Articles Hub](articles-hub/) — Anthropic Article Knowledge System

Systematically curated, scored, and categorized analysis of **42 Anthropic technical articles**.

**7-dimension weighted scoring system**:

| Dimension | Weight | Measures |
|-----------|--------|---------|
| Technical Depth | 1.1 | Detail and accuracy |
| Actionability | 1.3 | Directly applicable? |
| Innovation | 1.0 | Novel concepts or methods |
| Impact | 1.3 | Community adoption, derivative projects |
| Educational Value | 1.1 | Learning benefit |
| Timeliness | 1.0 | Long-term value retention |
| Reproducibility | 1.0 | Can you replicate the results? |

- **5-category taxonomy**: Agent Development, Engineering Practice, Model Research, Tool Platform, Security Policy
- **GitHub project mapping**: Links to 85+ Anthropic repos and community projects
- **Static site generator**: Python scripts produce a zero-dependency HTML dashboard
- **42 detail pages**: Each article with score breakdown, key takeaways, and related resources

<!-- TODO: Replace with actual screenshot -->
<!-- ![Articles Dashboard Screenshot](docs/images/articles-dashboard.png) -->

### [HTML Showcase](html-showcase/) — Interactive HTML Demonstrations

20 self-contained HTML examples demonstrating HTML as a powerful output format. *Based on [Anthropic's "The unreasonable effectiveness of HTML"](https://github.com/anthropics/html-effectiveness).*

| Category | Examples |
|----------|---------|
| Exploration | Code approaches, visual designs |
| Code | Review, understanding, design systems, component variants |
| Prototyping | Animation, interaction |
| Communication | Slide deck, status report, incident report, PR write-up |
| Diagrams & Research | Flowchart, feature/concept explainers |
| Custom Editing UIs | Triage board, feature flags, prompt tuner |

## Directory Structure

```
claude-code-insights/
├── version-chronicle/          # Single HTML page, ~126K
│   └── index.html              # Open directly in browser
├── articles-hub/               # Python-powered static site
│   ├── data/                   # YAML article data + JSON indexes
│   │   └── articles/           # Per-article YAML files
│   ├── docs/                   # Scoring criteria & methodology
│   ├── scripts/                # Generation scripts (Python)
│   └── site/                   # Generated HTML (42 articles + dashboards)
├── html-showcase/              # 20 standalone HTML demos
│   ├── index.html
│   └── 01-20 *.html
└── README.md
```

## Browsing

| Module | Open File |
|--------|-----------|
| Version Chronicle | `version-chronicle/index.html` |
| Articles Hub | `articles-hub/site/index.html` |
| HTML Showcase | `html-showcase/index.html` |

Zero install, zero build. Open any `.html` file in a browser.

## Data Sources

| Source | Coverage |
|--------|---------|
| [ClaudeLog](https://claudelog.com/claude-code-changelog/) | Full version history (11,376 lines) |
| [GitHub Releases](https://github.com/anthropics/claude-code/releases) | Latest versions |
| [Anthropic Blog](https://www.anthropic.com/blog) | Engineering + Research articles |
| Code with Claude 2026 Keynote | Roadmap information |

## Attribution

- **HTML Showcase**: Based on [Anthropic's html-effectiveness](https://github.com/anthropics/html-effectiveness) (Apache License 2.0)
- **Article content**: All article content is copyright Anthropic. This project is for personal study only.

## License

MIT (original code). HTML Showcase retains Apache License 2.0 from Anthropic.
