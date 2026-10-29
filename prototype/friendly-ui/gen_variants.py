"""Generate B/D/E orientation blocks for more friendly-ui prototype pages.

Each page's content is defined once; B (text buttons + numbered list), D (tile
chooser + numbered list) and E (tile chooser + step tiles) are rendered from it
and inserted after the page's front matter, together with the css /
css front-matter key. Re-running replaces the generated block. (The switcher
script is included site-wide from _quarto.yml.)
"""
import html, re, sys
from pathlib import Path

ROOT = Path(sys.argv[1])
BEGIN = "<!-- PROTOTYPE (#15) generated variants: begin -->"
END = "<!-- PROTOTYPE (#15) generated variants: end -->"


def step_links(links):
    return " ".join(f'<a class="fu-btn" href="{h}">{html.escape(l)}</a>' for l, h in links)


def fu_steps(aud):
    cls = "fu-steps" + ("" if aud.get("numbered", True) else " fu-unnumbered")
    out = [f'<ol class="{cls}">']
    for s in aud["steps"]:
        text = f'\n    {s["x"]}<br>' if s["x"] else ""
        out.append(f'  <li><strong>{s["t"]}</strong>{text}\n    {step_links(s["l"])}</li>')
    out.append("</ol>")
    return "\n".join(out)


def fu_steptiles(aud):
    cls = "fu-steptiles" + ("" if aud.get("numbered", True) else " fu-unnumbered")
    out = [f'<ol class="{cls}">']
    for s in aud["steps"]:
        text = f'\n    <p>{s["x"]}</p>' if s["x"] else ""
        out.append(f'  <li><strong>{s["t"]}</strong>{text}\n'
                   f'    <div class="fu-actions">{step_links(s["l"])}</div></li>')
    out.append("</ol>")
    return "\n".join(out)


# G shows every destination under a choice as an icon; icons by button label.
LINK_ICONS = {
    "Browse datasets": "bi-images", "Metrics": "bi-bar-chart-line", "Archive status": "bi-speedometer2",
    "Data exploration services": "bi-binoculars", "Data access services": "bi-key",
    "Data contributing services": "bi-upload", "Apply in REMS": "bi-shield-check",
    "Download guide": "bi-cloud-arrow-down", "Plan a contribution": "bi-clipboard-check",
    "Submission manual": "bi-journal-text", "Contribute models": "bi-cpu",
    "Access models": "bi-box-arrow-in-down", "Model access services": "bi-box-arrow-in-down",
}


def step_icons(aud):
    """G: the destinations of a choice's steps as (label, href, icon), in order."""
    return [(l, h, LINK_ICONS.get(l, "bi-box-arrow-up-right")) for s in aud["steps"] for l, h in s["l"]]


def fu_iconlinks(aud):
    """A line of text (optional) and a grid of linked icons."""
    out = [f'<p class="fu-iconlinks-lead">{aud["intro"]}</p>'] if aud.get("intro") else []
    out.append('<div class="fu-iconlinks">')
    for label, href, icon in aud["icons"]:
        out.append(f'  <a href="{href}"><i class="bi {icon}"></i><span>{html.escape(label)}</span></a>')
    out.append("</div>")
    return "\n".join(out)


def block(page, key):
    home = page.get("home")
    if home:  # front page: no heading, straight into the choices
        head = '::: {.panel-tabset}\n'
    else:
        head = (f'```{{=html}}\n<div class="fu-orient">\n  <p class="fu-title">{page["title"]}</p>\n'
                f'  <p class="fu-lead">{page["lead"]}</p>\n```\n\n::: {{.panel-tabset}}\n')
    tabs, below = [], []
    for a in page["aud"]:
        if key == "h" and "icons" in a:  # H: tools go below the choices, not in them
            below.append(a)
            continue
        desc = f' <span class="fu-tab-d">{a["desc"]}</span>' if a.get("desc") else ""
        h = f'## <i class="bi {a["icon"]}"></i> {a["label"]}{desc} {{.unlisted}}'
        if "icons" in a:
            body = fu_iconlinks({"icons": a["icons"]} if key == "g" else a)  # G: no intro line
        elif key == "g":
            body = fu_iconlinks({"icons": step_icons(a)})
        else:
            body = fu_steptiles(a) if key == "e" else fu_steps(a)
        tabs.append(f'{h}\n\n```{{=html}}\n{body}\n```\n')
    if home:
        tail = ":::\n"
        for a in below:
            tail += f'\n```{{=html}}\n<div class="fu-tools-below">\n{fu_iconlinks(a)}\n</div>\n```\n'
    else:
        tail = (f':::\n\n```{{=html}}\n  <p class="fu-after">{page.get("after", "The full page follows below.")}</p>\n'
                f'</div>\n```\n')
    names = {"d": "D — Tile chooser", "e": "E — Tiles all the way",
             "g": "G — Icons for the steps", "h": "H — Services below the choices"}
    # G and H only redesign the home page; elsewhere they show D's block
    also = ' data-also="g h"' if key == "d" and not home else ""
    return (f'<!-- ===================== {names[key]} ===================== -->\n'
            f'::: {{.proto-variant data-key="{key}"{also}}}\n{head}\n' + "\n".join(tabs) + f'\n{tail}:::\n')


def apply(page):
    path = ROOT / page["file"]
    src = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", src, re.S)
    fm, rest = m.group(1), src[m.end():]
    rel = "../" * page["file"].count("/")
    keys = (f"# PROTOTYPE (issue #15) — delete this key and the generated block\n"
            f"# below to revert. See prototype/friendly-ui/README.md.\n"
            f"css: {rel}prototype/friendly-ui/friendly-ui.css")
    if "friendly-ui.css" not in fm:
        fm = fm + "\n" + keys
    keys = ("d", "e", "g", "h") if page.get("home") else ("d", "e")
    gen = BEGIN + "\n\n" + "\n".join(block(page, k) for k in keys) + "\n" + END + "\n\n"
    marked = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n*", re.S)
    if marked.search(rest):  # replace in place, wherever the markers are
        rest = marked.sub(lambda _: gen, rest, count=1)
        path.write_text(f"---\n{fm}\n---\n{rest}", encoding="utf-8")
    else:                    # first run: right after the front matter
        path.write_text(f"---\n{fm}\n---\n\n{gen}{rest.lstrip(chr(10))}", encoding="utf-8")
    print("wrote", page["file"])


def S(t, x, *links):
    return {"t": t, "x": x, "l": list(links)}


PAGES = [
    {
        "file": "index.qmd",
        "home": True,
        "title": "What brings you here?",
        "lead": "BigPicture is a European archive of digital pathology slides for AI research.",
        "aud": [
            {"emoji": "🔭", "icon": "bi-binoculars", "label": "Explore data", "numbered": False, "steps": [
                S("Browse datasets", "Every dataset has a public page describing it. No account needed.",
                  ("Browse datasets", "https://datasets.bp.nbis.se/")),
                S("See the numbers", "Slides, datasets and partners in the archive today.",
                  ("Metrics", "metrics/index.html"),
                  ("Archive status", "https://grafana.bp.nbis.se/public-dashboards/c465fe145d7844b59d7eea87be8e199d")),
                S("Explore and learn about data exploration services", "",
                  ("Data exploration services", "services/data-exploration.html")),
            ]},
            {"emoji": "🧰", "icon": "bi-diagram-3", "label": "Explore services",
             "intro": "Explore and learn more about BigPicture services.",
             "icons": [
                 ("Data exploration services", "services/data-exploration.html", "bi-binoculars"),
                 ("Data access services", "services/data-access.html", "bi-key"),
                 ("Data contributing services", "services/data-contributing.html", "bi-upload"),
                 ("Model access services", "services/model-access.html", "bi-box-arrow-in-down"),
                 ("Model contributing services", "services/model-contributing.html", "bi-cpu"),
             ]},
            {"emoji": "🔑", "icon": "bi-key", "label": "Access data", "steps": [
                S("Find a dataset", "Look through the collections and pick one that fits your research.",
                  ("Browse datasets", "https://datasets.bp.nbis.se/")),
                S("Ask for access", "Apply for the dataset in REMS. A data access committee reviews your request.",
                  ("Apply in REMS", "https://bp-rems.sd.csc.fi/")),
                S("Download it", "A detailed overview on how to download.",
                  ("Download guide", "datasets/download/downloading-data.html")),
                S("Explore and learn about data access services", "",
                  ("Data access services", "services/data-access.html")),
            ]},
            {"emoji": "📥", "icon": "bi-box-arrow-in-down", "label": "Access models", "numbered": False, "steps": [
                S("Access models", "Information will follow.",
                  ("Access models", "models/access.html")),
            ]},
            {"emoji": "📤", "icon": "bi-upload", "label": "Contribute data", "numbered": False, "steps": [
                S("Plan a contribution", "Access, a test in staging, and production.",
                  ("Plan a contribution", "datasets/submission/plan-a-contribution.html")),
                S("Submission manual", "Step-by-step instructions for the three submission paths.",
                  ("Submission manual", "datasets/submission/index.html")),
                S("Explore and learn about data contributing services", "",
                  ("Data contributing services", "services/data-contributing.html")),
            ]},
            {"emoji": "🧪", "icon": "bi-cpu", "label": "Contribute models", "numbered": False, "steps": [
                S("Contribute models", "Information will follow.",
                  ("Contribute models", "models/contribute.html")),
            ]},
        ],
    },
]

for p in PAGES:
    apply(p)
