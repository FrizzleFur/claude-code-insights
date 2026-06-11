#!/usr/bin/env python3
"""Add slug fields and clickable links to rankings.html JS data."""
import re

path = 'site/rankings.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# Short title -> slug mapping (from rankings.html display titles)
slug_map = {
    "Effective Context Engineering": "effective-context-engineering",
    "Introducing Advanced Tool Use": "advanced-tool-use",
    "Introducing Contextual Retrieval": "contextual-retrieval",
    "Building Effective AI Agents": "building-effective-agents",
    "Writing Effective Tools for Agents": "writing-effective-tools",
    "Claude Code: Best Practices": "claude-code-best-practices",
    'The "Think" Tool': "think-tool",
    "Multi-Agent Research System": "multi-agent-research-system",
    "Desktop Extensions: MCP": "desktop-extensions-mcp",
    "Beyond Permission Prompts": "beyond-permission-prompts",
    "Code Execution with MCP": "code-execution-mcp",
    "Scaling Managed Agents": "scaling-managed-agents",
    "Agent Skills": "agent-skills",
    "Harness Design Long-Running": "harness-design-long-running",
    "C Compiler Parallel Claudes": "c-compiler-parallel-claudes",
    "Effective Harnesses Agents": "effective-harnesses-agents",
    "Demystifying Evals": "demystifying-evals-agents",
    "Teaching Claude Why": "teaching-claude-why",
    "Automated Alignment Researchers": "automated-alignment-researchers",
    "NL Autoencoders": "natural-language-autoencoders",
    "Claude Code Auto Mode": "claude-code-auto-mode",
    "Infrastructure Noise Evals": "infrastructure-noise-evals",
    "What 81K People Want from AI": "what-81000-people-want",
    "SWE-bench Verified": "swe-bench-verified",
    "AI-Resistant Evaluations": "ai-resistant-evaluations",
    "BioMysteryBench": "biomysterybench",
    "Donating Alignment Tool": "donating-alignment-tool",
    "Eval Awareness BrowseComp": "eval-awareness-browsecomp",
    "Project Deal": "project-deal",
    "What 81K: Economics of AI": "what-81000-people-economics",
    "Personal Guidance": "personal-guidance",
    "Project Vend Phase Two": "project-vend-phase-two",
    "Economic Index Survey": "economic-index-survey",
    "2028 Scenarios": "2028-scenarios",
    "Claude Code Quality Update": "claude-code-quality-update",
    "Postmortem Three Issues": "postmortem-three-issues",
    "Institute Focus Areas": "anthropic-institute-focus",
}

def add_slug(match):
    entry = match.group(0)
    # Extract title
    title_match = re.match(r'\{t:"([^"]+)"', entry)
    if not title_match:
        title_match = re.match(r"\{t:'([^']+)'", entry)
    if not title_match:
        return entry
    title = title_match.group(1)
    slug = slug_map.get(title)
    if slug:
        return entry.replace('{t:', '{slug:"' + slug + '",t:', 1)
    return entry

# Add slug to each data entry
html = re.sub(r'\{t:"[^"]*"[^}]+\}', add_slug, html)
html = re.sub(r"\{t:'[^']*'[^}]+\}", add_slug, html)

# Make title clickable in render function
old_render = 'strong.textContent=a.t;title.appendChild(strong)'
new_render = '''const a2=document.createElement("a");a2.href="articles/"+a.slug+".html";a2.textContent=a.t;a2.style.color="var(--clay)";a2.style.textDecoration="none";strong.appendChild(a2);title.appendChild(strong)'''
html = html.replace(old_render, new_render)

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

linked = html.count('slug:"')
print(f'rankings.html: {linked} entries with slug fields added')
