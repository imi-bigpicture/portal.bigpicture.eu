# PROTOTYPE — a friendlier front page for non-technical visitors

Throwaway. Issue [imi-bigpicture/portal.bigpicture.eu#15](https://github.com/imi-bigpicture/portal.bigpicture.eu/issues/15).
Not for merge to `main`.

> Designs for visitors who aren't technical (clinicians, site managers,
> curious researchers), switchable via `?variant=` and a floating bottom bar.

## Running it

```
quarto preview        # or: quarto render, then open docs/index.html
```

Open `/` and press `←` / `→`, or click the arrows in the black pill at the
bottom. The choice follows you across pages and survives reload.

| Key | Name | What it is |
| --- | --- | --- |
| `off` | Current site | today's pages (localhost only) |
| `d` | Tile chooser | choices as tiles (icon + name); steps as a numbered list |
| `e` | Tiles all the way | same tiles; steps as tiles too |
| `g` | Icons for the steps | home only: same five tiles; what opens underneath is a row of linked icons (one per destination), like Explore tools |
| `h` | Tools below the choices | home only: four tiles; Explore tools as an icon row below the steps |

G and H only redesign the home page. Elsewhere they show D's block
(`data-also="g h"` on D's blocks), so a reviewer can still click through.

The bar only appears on `localhost`, `127.0.0.1`, `file://` and the `/preview/`
copy. Anywhere else the page always shows `off`.

## What's prototyped

| Page | Change |
| --- | --- |
| Home | five choices, no heading: Explore data, Explore tools, Access data, Contribute data, Contribute tools |
| Plan a contribution (new) | the coordinator's entry point: agreement (to confirm with WP2), access, staging run, production, hand-over |
| Download guide | an orientation block above the unchanged text |
| Submission manual | untangled (option B, structure only): sidebar as Path 1 (pipeline in stages Set up A–G · Test run H–J · Go to production) · Path 2 · Path 3 · Help; no orientation blocks; overview shows the paths once (table, then the two questions); prev/next hidden where it would cross paths |
| Tools (new, `tools/`) | overview, four "by purpose" section pages, ten placeholder tool pages |

**Upload guide untangled (option B), structure only.** Content moves still to do on `main`: "do a staging run first" to the start of Test run; production storage out of D into Prepare for production (Best Practices purely about scale); a visible test step for direct upload; one place for the access requirement; tool names cross-linked. A–J letters unchanged.

**Contribute data is untangled (option B).** Coordinators get their own page,
*Plan a contribution*. The manual (overview, A. Prerequisites, Key concepts)
no longer has coordinator tabs; the overview points coordinators to the new
page. Still to do on `main` if this is adopted: collapse the eight places
that explain the access requirement into one, and cross-link the tools pages
with the manual's names for them (Slidetap = curation UI, and so on).

**Top menu mirrors the home page:** Home, Explore data, Explore tools, Access
data, Contribute data, Contribute tools, each holding the same destinations as
the home page. Today's Algorithms and Compute placeholders sit under Contribute
tools as "Coming later". Software (the Cytomine docs link) stays its own item
until it's decided where it goes. Fits on one line at 1366px.

**Site-wide layout**, each marked `# PROTOTYPE (#15)` in `_quarto.yml`: no
right-hand "On this page", docked sidebars, a 1200px content column, `noindex`.

## Generated content

- `gen_variants.py` writes the D/E (and on the home page G/H) blocks of the
  home page and the five generated content pages, between
  `generated variants: begin/end` markers. Each page's content is defined once.
  The overview and the download guide have hand-written D/E blocks.
- `gen_tools.py` writes everything under `tools/` from one mapping. To add a
  tool or move it between sections, edit the mapping, re-run it, and update
  the Tools sidebar in `_quarto.yml` (the script prints it).

Run both from the repo root: `python prototype/friendly-ui/gen_variants.py .`

## Reviewer preview at /preview/

The publish workflow on `main` (PR #24) builds this branch and publishes it at
`https://portal.bigpicture.eu/preview/` (unlisted, `noindex`). There the
switcher offers D, E, G and H as "Design n of 4", opens on D, and the home page
lists the prototyped pages. To update it, push this branch and run the publish
workflow by hand. Merge `main` in now and then so the reference text doesn't
drift.

## Troubleshooting the preview

If `quarto preview` fails with `BadResource: Bad resource ID` from `SassCache`,
or keeps serving an old page, stop it, delete `.quarto/quarto-session-temp*`
and start it again. Quarto 1.9's Sass cache goes stale after full re-renders
(each `_quarto.yml` edit causes one). `switcher.html` isn't watched: touch the
pages that include it.

## What Quarto supports cleanly, and what fights it

- **Choices are Quarto's own `panel-tabset`.** Tabs are markdown headings with
  an icon in them, so they stay editable as markdown.
- **Quarto forces `.nav` to flex with `!important`.** A tile or icon grid
  needs `display: grid !important`.
- **Step lists and tiles are raw HTML** (`{=html}`). Quarto has no card or
  step component for websites.
- **`<aside>` is margin content in Quarto** and gets moved to the margin
  column. Use a `<div>`.
- **Tabs aren't linkable** (no selected tab in the URL).
- **Phone layout is unverified.** Grids use `auto-fill`/`auto-fit` and should
  stack; check in devtools' device mode.

Copy is prototype-grade. Check the claims before shipping any of it.
