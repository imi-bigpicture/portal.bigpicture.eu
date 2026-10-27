# PROTOTYPE — a friendlier front page for non-technical visitors

Throwaway. Issue [imi-bigpicture/portal.bigpicture.eu#15](https://github.com/imi-bigpicture/portal.bigpicture.eu/issues/15).
Not for merge to `main`.

> Three structurally different front pages for visitors who aren't technical
> (clinicians, site managers, curious researchers), switchable via `?variant=`
> and a floating bottom bar, on the real front page (`/`).

## Running it

```
quarto preview        # or: quarto render, then open docs/index.html
```

Open `/` and press `←` / `→`, or click the arrows in the black pill at the
bottom. The choice survives reload and coming back to the front page.

| Key | Name | URL |
| --- | --- | --- |
| `off` | Current front page (baseline) | `?variant=off` |
| `a` | Picture tiles | `?variant=a` |
| `b` | What brings you here? | `?variant=b` |
| `c` | Journey map | `?variant=c` |

The bar only appears on `localhost`, `127.0.0.1` or `file://`. Anywhere else
the page always shows `off`, so a stray merge changes nothing on the live site.

Only `index.qmd` changes (two front-matter keys plus the variant blocks).
`_quarto.yml` and `custom.scss` are untouched, and the CSS uses only the
theme's Bootstrap variables. So this branch composes with whichever restyle
#14 picks (`prototype/bp-visual-identity`): merge both locally to see them
together.

## The variants

Each one disagrees with the others about the **primary affordance**:

| | Organised by | Primary affordance | Best for |
| --- | --- | --- | --- |
| **A — Picture tiles** | destination ("what is there") | a grid of large clickable cards with an icon and one plain sentence each; upcoming services greyed out | visitors who know roughly what they want |
| **B — What brings you here?** | audience ("who are you") | four big "I want to…" buttons; each reveals 3 numbered steps with buttons | first-time visitors who don't know the vocabulary |
| **C — Journey map** | process ("how it works") | a clickable two-lane diagram, from hospitals (prepare → submit → archive) to researchers (find → request → download) | explaining what BigPicture *is*, and where you fit |

All three rewrite the copy in plain language: no "landing pages website root",
"federated discovery" or "indirect access". Copy is prototype-grade. Check the
claims (e.g. "a data access committee reviews your request") before shipping
any of it.

## What Quarto supports cleanly, and what fights it

**Clean, native:**

- **B's buttons are Quarto's own `panel-tabset`**, restyled with ~20 lines of
  CSS. Tabs are plain markdown headings, so editors who don't know HTML can
  change the content. It's the most maintainable of the three.
- **Bootstrap Icons ship with Quarto websites** (`bi bi-*` classes, already
  loaded). A's icons cost nothing.
- **Page-scoped CSS and scripts** via the page's front matter (`css:`,
  `include-after-body:`), so a front-page redesign needn't touch the site theme.
- **Bootstrap's stretched-link pattern** makes a whole tile clickable with
  correct keyboard focus.

**Works, but against the grain:**

- **A's tiles and B's step lists are raw HTML** (`{=html}` blocks). Quarto has
  no card or step component for websites (cards exist only in Quarto
  *dashboards*). Editing them means editing HTML. A shortcode or a Lua filter
  could hide that, at the cost of a small extension to maintain.
- **C's diagram is hand-written SVG.** Every box is positioned by coordinates.
  Adding a step means re-laying out the drawing. Quarto's native Mermaid can
  make clickable diagrams from text, but gives much less control over layout
  and styling.
- **The theme's link underline reaches into SVG text** and has to be undone
  (`.fu-map a { text-decoration: none }`).
- **A div that starts with a heading becomes a `<section>`.** Quarto rewrites
  `::: {.x}` + `## Heading` into `<section class="level2 x">`. That's harmless,
  but selectors must not assume `div`.
- **Tabs are probably not linkable.** As far as I know, Quarto's tabset doesn't
  put the selected tab in the URL, so B couldn't be deep-linked to "I want to
  share data". Not verified; a few lines of JS would add it if needed.

**Known gaps (not addressed):**

- **C on a phone:** the SVG scales down as a whole, so at phone width its text
  becomes too small to read. Shipping C needs a stacked, vertical layout below
  ~700px, i.e. a second drawing or an HTML/CSS rebuild of the map.
- **Phone layout generally is unverified.** Headless screenshots at 390px
  overflowed on every page, including untouched ones, which points at the
  headless viewport rather than the variants. Check in browser devtools'
  device mode.

## Recommendation (author's, to react to)

**B for the front page, with C's map as a section lower down or on an
"About" page.** B is the only variant that works without knowing any
BigPicture words, and it's built on a native Quarto feature, so it stays
editable. A reads well but is mostly the current page's links in boxes, which
helps people who already know what they want. C explains the system best but
is the costliest to maintain and to make work on phones.
