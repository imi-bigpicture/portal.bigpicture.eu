# PROTOTYPE — a friendlier front page for non-technical visitors

Throwaway. Issue [imi-bigpicture/portal.bigpicture.eu#15](https://github.com/imi-bigpicture/portal.bigpicture.eu/issues/15).
Not for merge to `main`.

> Designs for visitors who aren't technical (clinicians, site managers,
> curious researchers), switchable via `?variant=` and a floating bottom bar,
> on three real pages: the front page, the submission overview and the
> download guide.

## Running it

```
quarto preview        # or: quarto render, then open docs/index.html
```

Open `/` and press `←` / `→`, or click the arrows in the black pill at the
bottom. The choice follows you across pages and survives reload, so you can
click from the front page into the other two and see one variant end to end.

| Page | What the variants change |
| --- | --- |
| `/` | the whole page |
| `/datasets/submission/` | an orientation block above the unchanged overview |
| `/datasets/download/downloading-data.html` | an orientation block above the unchanged guide |

On the two content pages the reference text stays exactly as it is. The
variants only add a friendlier way in, so `off` there is today's page.

If `quarto preview` starts failing with `BadResource: Bad resource ID` from
`SassCache`, or keeps showing an old page, stop it, delete
`.quarto/quarto-session-temp*` and start it again. Quarto 1.9's Sass cache
handle goes stale after a few full re-renders (each `_quarto.yml` edit causes
one). Edits to `switcher.html` are not watched (it's an `include-after-body`):
touch the three `.qmd` files to make the preview pick them up.

| Key | Name | URL |
| --- | --- | --- |
| `off` | Current front page (baseline) | `?variant=off` |
| `a` | Picture tiles | `?variant=a` |
| `b` | What brings you here? | `?variant=b` |
| `d` | Tile chooser (A's tiles, B's steps) | `?variant=d` |
| `e` | Tiles all the way | `?variant=e` |
| `f` | Everything visible | `?variant=f` |

The bar only appears on `localhost`, `127.0.0.1` or `file://`. Anywhere else
the page always shows `off`, so a stray merge changes nothing on the live site.

**Visual identity.** The site's real theme since #21 (identity C from #14,
indigo headings) lives in `custom.scss` on `main`. This branch merges `main`,
so every variant is seen in it. The CSS here uses only Bootstrap variables
and needs nothing of its own for the identity.

**Site-wide layout changes** (round 2 feedback), each marked
`# PROTOTYPE (#15): was …` in `_quarto.yml`: no right-hand "On this page"
TOC, sidebars `docked` flush left instead of `floating`, and a wider content
column (`grid: body-width: 1200px, margin-width: 0px`; the margin column only
held empty space once the TOC was gone).

## The variants

Round 1 had A, B and C. C (journey map) was dropped. Feedback on the rest:
*A's blocks of text look nicer, B's navigation is better: it starts from
"why am I here?".* D, E and F combine the two and disagree about one thing:
**how much of the answer is a tile, and whether you click to see it.**

| | Choosing | The steps | Tests |
| --- | --- | --- | --- |
| **A — Picture tiles** | none; tiles per destination | n/a | (round 1 baseline) |
| **B — What brings you here?** | big text buttons per audience | numbered list | (round 1 baseline) |
| **D — Tile chooser** | A-style tiles per audience (icon, title, one sentence); one equal row when there's room, compact stacked rows when not (container query); choosing scrolls the steps into view if they're off-screen | B's numbered list | does A's look on the *choice* alone fix it? |
| **E — Tiles all the way** | same tiles | numbered step tiles in a row, buttons at the bottom | are blocks also better for the *steps*? |
| **F — Everything visible** | no choosing: a jump bar of audience pills, then one section per audience | step tiles per section | is hiding the other audiences behind a click worth it? |

The audiences and step copy are B's, unchanged in meaning, on all three pages:

| | Front page | Submission overview | Download guide |
| --- | --- | --- | --- |
| audiences | use data / share data / curious / build algorithms (upcoming) | coordinate for my site / run the submission / have a question | requesting the data / doing the download / something went wrong |

In E and F, "something went wrong" items aren't sequential, so they get a
grey `!` instead of a number (`.fu-steptiles.fu-unnumbered`).

Copy is prototype-grade. Check the claims (e.g. "a data access committee
reviews your request") before shipping any of it.

## What Quarto supports cleanly, and what fights it

**Clean, native:**

- **B, D and E all use Quarto's own `panel-tabset`.** Tabs are plain markdown
  headings. D/E put the icon and the one-line description in the heading
  itself (`## <i class="bi bi-search"></i> I want to use data <span class="fu-tab-d">…</span>`),
  so the tile chooser is still editable as markdown.
- **Bootstrap Icons ship with Quarto websites** (`bi bi-*`), so icons cost nothing.
- **Page-scoped CSS and scripts** via front matter (`css:`, `include-after-body:`).

**Works, but against the grain:**

- **Quarto forces `.nav` to flex with `!important`** (a media-query rule,
  `.nav:not(.nav-hidden)`). Turning the tab list into a tile grid needs
  `display: grid !important`.
- **Step lists and step tiles are raw HTML** (`{=html}` blocks). Quarto has no
  card or step component for websites. A shortcode could hide that, at the
  cost of a small extension to maintain.
- **Tab headings would leak into a page TOC.** Content-page tabs carry
  `{.unlisted}`. Moot while the TOC is off, but keep it if it comes back.
- **An orientation block can't be one fenced div** when it wraps a tabset:
  it opens its `<div>` in one raw-HTML block and closes it in another.
- **Tabs are probably not linkable** (no selected tab in the URL). F has no
  such problem: its sections have anchors (`#fu-f-use`, …).

**Known gaps:**

- **Phone layout is unverified.** All tile grids use `auto-fill`/`auto-fit`
  and should stack, but check in browser devtools' device mode.
