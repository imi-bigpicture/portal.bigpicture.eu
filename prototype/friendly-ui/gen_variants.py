"""Generate B/D/E orientation blocks for more friendly-ui prototype pages.

Each page's content is defined once; B (text buttons + numbered list), D (tile
chooser + numbered list) and E (tile chooser + step tiles) are rendered from it
and inserted after the page's front matter, together with the css /
include-after-body front-matter keys. Re-running replaces the generated block.
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


def fu_iconlinks(aud):
    """A choice that is just a line of text and a grid of linked icons (same in B/D/E)."""
    out = [f'<p class="fu-iconlinks-lead">{aud["intro"]}</p>', '<div class="fu-iconlinks">']
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
            body = fu_iconlinks(a)
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
             "g": "G — Icons for every choice", "h": "H — Tools below the choices"}
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
    keys = (f"# PROTOTYPE (issue #15) — delete these two keys and the generated block\n"
            f"# below to revert. See prototype/friendly-ui/README.md.\n"
            f"css: {rel}prototype/friendly-ui/friendly-ui.css\n"
            f"include-after-body: {rel}prototype/friendly-ui/switcher.html")
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
                S("Explore and learn about data exploration tooling", "",
                  ("Data exploration tools", "tools/data-exploration.html")),
            ]},
            {"emoji": "🧰", "icon": "bi-tools", "label": "Explore tools",
             "intro": "Explore and learn more about BigPicture tooling.",
             "icons": [
                 ("Data exploration tools", "tools/data-exploration.html", "bi-binoculars"),
                 ("Data access tools", "tools/data-access.html", "bi-key"),
                 ("Data contributing tools", "tools/data-contributing.html", "bi-upload"),
                 ("Tool contributing tools", "tools/tool-contributing.html", "bi-cpu"),
             ]},
            {"emoji": "🔑", "icon": "bi-key", "label": "Access data", "steps": [
                S("Find a dataset", "Look through the collections and pick one that fits your research.",
                  ("Browse datasets", "https://datasets.bp.nbis.se/")),
                S("Ask for access", "Apply for the dataset in REMS. A data access committee reviews your request.",
                  ("Apply in REMS", "https://bp-rems.sd.csc.fi/")),
                S("Download it", "A detailed overview on how to download.",
                  ("Download guide", "datasets/download/downloading-data.html")),
                S("Explore and learn about data access tooling", "",
                  ("Data access tools", "tools/data-access.html")),
            ]},
            {"emoji": "📤", "icon": "bi-upload", "label": "Contribute data", "numbered": False, "steps": [
                S("Plan a contribution", "For the person arranging it at their site: agreements, access and planning.",
                  ("Plan a contribution", "datasets/submission/plan-a-contribution.html")),
                S("Run a submission", "For the technical person doing the upload: the step-by-step manual.",
                  ("Submission manual", "datasets/submission/index.html")),
                S("Explore and learn about data contributing tooling", "",
                  ("Data contributing tools", "tools/data-contributing.html")),
            ]},
            {"emoji": "🧪", "icon": "bi-cpu", "label": "Contribute tools", "numbered": False, "steps": [
                S("Coming later", "Contributing models, benchmarks and algorithms to BigPicture. Nothing to contribute to yet.",
                  ("What's planned", "algorithms/index.html")),
            ]},
        ],
    },
    {
        "file": "datasets/submission/support.qmd",
        "title": "What kind of problem is it?",
        "lead": "Different problems reach different teams. Pick the one closest to yours.",
        "aud": [
            {"emoji": "🛠️", "icon": "bi-tools", "label": "Something in the pipeline is broken",
             "desc": "A bug, a confusing step, or unexpected behaviour.",
             "steps": [
                 S("Check the FAQ", "Recurring errors are answered there, sorted by manual step.", ("FAQ", "faq.html")),
                 S("Open an issue", "On the pipeline's GitHub page. The answer stays visible for the next person.",
                   ("Open an issue", "https://github.com/imi-bigpicture/bp-submission-pipeline/issues")),
                 S("No GitHub account?", "Email the servicedesk instead. It gets picked up from there.",
                   ("Contact details", "#get-help")),
             ]},
            {"emoji": "📦", "icon": "bi-server", "label": "The upload or the archive has a problem",
             "desc": "The inbox, the upload addresses, or where your data lands.",
             "steps": [
                 S("Write down what happened", "The step you were on, the exact command, and what you saw.",
                   ("What to include", "#when-you-ask-include")),
                 S("Email bp-ops", "The team that runs the BigPicture servers.", ("Contact details", "#get-help")),
             ]},
            {"emoji": "🔑", "icon": "bi-key", "label": "I need access, or have a general question",
             "desc": "Access requests and anything else.",
             "steps": [
                 S("Check the FAQ", "It may already be answered.", ("FAQ", "faq.html")),
                 S("Email the servicedesk", "For general and technical support, and access requests.",
                   ("Contact details", "#get-help")),
             ]},
            {"emoji": "📝", "icon": "bi-journal-text", "label": "This manual is wrong or unclear",
             "desc": "Missing steps, unclear instructions, broken links.",
             "steps": [
                 S("Note the page", "Which page, and what you expected instead.",
                   ("What to include", "#when-you-ask-include")),
                 S("Open an issue", "On the portal's GitHub page.",
                   ("Open an issue", "https://github.com/imi-bigpicture/portal.bigpicture.eu/issues")),
             ]},
        ],
    },
    {
        "file": "datasets/submission/faq.qmd",
        "title": "Where are you stuck?",
        "lead": "The answers follow the manual's steps. Pick the part you're in.",
        "after": "All questions follow below, by step.",
        "aud": [
            {"emoji": "⚙️", "icon": "bi-gear", "label": "Setting up", "desc": "Access, installing, configuring (steps B–D).",
             "numbered": False, "steps": [
                 S("B. GitHub access", "Questions about getting at the private code and images.", ("Go to B", "#b.-github-access")),
                 S("C. Install package", "Questions and errors while installing.", ("Go to C", "#c.-install-package")),
                 S("D. Configure", "Questions about the configuration.", ("Go to D", "#d.-configure")),
             ]},
            {"emoji": "🧾", "icon": "bi-table", "label": "Preparing the data", "desc": "The model and mapper files (step E).",
             "numbered": False, "steps": [
                 S("E1. model.json", "Questions about the model file.", ("Go to E1", "#e1.-model.json")),
                 S("E2. mappers.xlsx", "Questions about the mapper workbook.", ("Go to E2", "#e2.-mappers.xlsx")),
             ]},
            {"emoji": "▶️", "icon": "bi-play-circle", "label": "Running and checking",
             "desc": "Certificates, starting up, the test run, validating (F–I).",
             "numbered": False, "steps": [
                 S("F. TLS + credentials", "Certificates and logins.", ("Go to F", "#f.-tls-credentials")),
                 S("G. Preflight + boot", "Starting the stack.", ("Go to G", "#g.-preflight-boot")),
                 S("H. Run a submission test", "The test run.", ("Go to H", "#h.-run-a-submission-test")),
                 S("I. Validate the bundle", "Checking the result.", ("Go to I", "#i.-validate-the-bundle")),
             ]},
            {"emoji": "☁️", "icon": "bi-cloud-arrow-up", "label": "Uploading and after",
             "desc": "The upload, and what happens next.",
             "numbered": False, "steps": [
                 S("J. Upload to BigPicture", "The upload itself.", ("Go to J", "#j.-upload-to-bigpicture")),
                 S("After submission", "What happens once it's uploaded.", ("Go there", "#after-submission")),
             ]},
        ],
    },
    {
        "file": "datasets/submission/key-concepts.qmd",
        "title": "Which words do you need?",
        "lead": "You don't need all of them. Pick your role and start with these.",
        "after": "The full glossary follows below, alphabetically. Click a word to open it.",
        "aud": [
            {"emoji": "💻", "icon": "bi-terminal", "label": "I run the submission",
             "desc": "The words for the run and its tools.", "numbered": False, "steps": [
                 S("The run", "What a submission run works with and produces.",
                   ("Batch", "#batch"), ("Bundle", "#bundle"), ("Slidetap outbox", "#slidetap-outbox")),
                 S("The tools", "The software you work with.",
                   ("Curation UI", "#curation-ui"), ("Encryption & upload tools", "#encryption-upload-tools"),
                   ("Dicomize", "#dicomize")),
             ]},
            {"emoji": "🧾", "icon": "bi-table", "label": "I prepare the metadata",
             "desc": "The words for describing slides.", "numbered": False, "steps": [
                 S("Describing slides", "The spreadsheets you fill in, and what they describe.",
                   ("Metadata workbook", "#metadata-workbook"), ("Mapper workbook", "#mapper-workbook"),
                   ("Mapper group", "#mapper-group"), ("WSI", "#wsi")),
                 S("Standards and codes", "The formats and vocabularies used.",
                   ("MetaFleX", "#metaflex"), ("MSMdad", "#msmdad"), ("SNOMED CT", "#snomed-ct"),
                   ("Coded attribute", "#coded-attribute")),
                 S("Reference files and checks", "Words you'll meet when the data is checked.",
                   ("model.json", "#model-json"), ("Reference data", "#reference-data"),
                   ("Invalid item", "#invalid-item")),
             ]},
        ],
    },
    {
        "file": "datasets/submission/bp-submission-pipeline/prerequisites.qmd",
        "title": "Before you install anything",
        "lead": "Setting up needs six tools on one computer. Pick who you are.",
        "aud": [
            {"emoji": "💻", "icon": "bi-terminal", "label": "I'm setting up the computer",
             "desc": "Install and check six tools.", "steps": [
                 S("Make sure you have access", "To the private BigPicture code and images. Later steps fail without it.",
                   ("Requesting access", "github-access.html")),
                 S("Install the six tools", "Docker, Git, GitHub CLI, make, OpenSSL and Python. Each has a tab per operating system.",
                   ("Start with Docker", "#docker-compose-v2")),
                 S("Check each one", "Every tool has a Verify box. Move on when all six report a version.",
                   ("Python, the last one", "#python")),
                 S("Continue", "The next step is GitHub access.", ("B. GitHub access", "github-access.html")),
             ]},
            {"emoji": "🆘", "icon": "bi-life-preserver", "label": "A tool won't install",
             "desc": "Where to look, and who to ask.", "steps": [
                 S("Check the FAQ", "Common errors, by manual step.", ("FAQ", "../faq.html")),
                 S("Ask a person", "Which team to contact for which problem.", ("Support", "../support.html")),
             ]},
        ],
    },
    {
        "file": "datasets/submission/add-landing-page.qmd",
        "title": "Adding a landing page later",
        "lead": "No need to resubmit. Which steps you follow depends on how you uploaded.",
        "aud": [
            {"emoji": "🔁", "icon": "bi-arrow-repeat", "label": "I uploaded with the pipeline",
             "desc": "And still have its upload.db file.", "steps": [
                 S("Prepare the landing page", "Write landing_page.xml by hand, or generate it.",
                   ("Prepare", "#prepare-the-landing-page")),
                 S("Upload with the pipeline", "Into the same dataset folder, not as a new submission.",
                   ("Upload via the pipeline", "#upload-via-bp-submission-pipeline")),
                 S("Tell bp-ops", "So they know a landing page was added.", ("After uploading", "#after-uploading")),
             ]},
            {"emoji": "✋", "icon": "bi-hand-index", "label": "I uploaded another way",
             "desc": "Or the upload.db file is lost.", "steps": [
                 S("Prepare the landing page", "Write landing_page.xml by hand, or generate it.",
                   ("Prepare", "#prepare-the-landing-page")),
                 S("Upload by hand", "Into the same dataset folder, not as a new submission.",
                   ("Upload manually", "#upload-manually-no-upload.db")),
                 S("Tell bp-ops", "So they know a landing page was added.", ("After uploading", "#after-uploading")),
             ]},
            {"emoji": "🆘", "icon": "bi-life-preserver", "label": "Something went wrong",
             "desc": "It isn't showing, or you're unsure it arrived.", "numbered": False, "steps": [
                 S("Not sure it arrived", "Contact support with the dataset identifier before uploading again.",
                   ("If something goes wrong", "#if-something-goes-wrong")),
                 S("Still not showing", "Contact support rather than uploading again.", ("Support", "support.html")),
             ]},
        ],
    },
]

for p in PAGES:
    apply(p)
