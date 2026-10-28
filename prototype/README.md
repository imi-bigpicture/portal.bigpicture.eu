# PROTOTYPE — bigpicture.eu-aligned visual identity

Throwaway. Issue [JeroenUMC/Nexus#110](https://github.com/JeroenUMC/Nexus/issues/110).
Not for merge to `main`.

> Three variants of the site's styling, switchable via `?variant=` and a floating
> bottom bar, applied to the real front page and the real submission manual.

## Decision

**Variant C**, with one change: all headings are indigo, h3 included,
instead of bigpicture.eu's pink h3. Pink is kept for accents only.
`brand-variants.scss` already carries the change (`?variant=c`). Recorded in
[portal.bigpicture.eu#14](https://github.com/imi-bigpicture/portal.bigpicture.eu/issues/14#issuecomment-6467026738),
which tracks shipping it. This branch stays as a record and is never merged;
shipping happens in `custom.scss` / `_quarto.yml` on `main`.

## Running it

```
quarto render      # or: quarto preview
```

One render produces all variants. Open the front page and press `←` / `→`, or
click the arrows in the black pill at the bottom of the screen. The variant
follows you as you click through the site and survives reload.

| Key | Name | URL |
| --- | --- | --- |
| `off` | Current site (baseline) | `?variant=off` |
| `a` | Palette only | `?variant=a` |
| `b` | Palette + type + chrome | `?variant=b` |
| `c` | Full BigPicture furniture | `?variant=c` |

Pages worth comparing: `/` (front page) and
`/datasets/submission/` (a content page with sidebar, TOC, callouts and code).

The bar is hidden unless the site is served from `localhost`, `127.0.0.1` or
`file://`, so a stray merge cannot show it on `bp.nbis.se`.

## The identity being matched

Read off the live bigpicture.eu theme stylesheet and the front/About pages:

| | |
| --- | --- |
| Primary | `#1c007b` deep indigo — h1/h2, nav, links, body copy accents |
| Accent | `#ff447c` hot pink — h3, buttons, active nav, bullets, "read more" |
| Ink | `#1d1d1b` |
| Washes | `#f2f0f7` lavender, `#fbf3f8` pink-lavender |
| Secondary | `#3fa0a2` teal, `#fedf6d` yellow, `#ef4123` orange-red |
| Body + headings | **Lato** 400/700/900 |
| Accent face | **Yrsa** serif — quotes, subtitles, article meta only. *Not* body copy. |
| Buttons | pink fill, white bold, `10px` radius, left-aligned text, chevron, min-width 9rem |
| Nav | uppercase, letterspaced, weight 500, indigo, pink on hover/active |
| Bullets | pink filled circles, generous line-height |
| Furniture | pill/stadium image masks, segmented indigo→pink rule, thin-bordered square cards |

Note the h3-is-pink rule is real, not a mistake — bigpicture.eu genuinely sets
`h3 { color: #ff447c }` while h1/h2 stay indigo.

## How far each variant goes

|  | Colour | Typography | Nav chrome | Page furniture | Layout / density |
| --- | --- | --- | --- | --- | --- |
| **A** | full swap | Quarto default | Quarto default | Quarto default | Quarto default |
| **B** | full swap | Lato + Yrsa accent, indigo/pink heading scale | white, taller, uppercase letterspaced, pink active | Quarto default | Quarto default |
| **C** | full swap | as B | as B | segmented rule, lavender hero panel, restyled callouts / sidebar / TOC / page-nav, indigo footer, 10px radii | looser rhythm, 1.0625rem/1.75 body |

**A — Palette only.** Swaps FEGA blue `#155177` for BigPicture indigo, hover to
pink. Nothing else moves. This is the "sibling identity that merely shares a
palette" end of the issue's open question.

**B — Family resemblance.** A, plus the two things that actually carry a brand
at a glance: the typeface and the navigation bar. Content pages keep Quarto's
density, so the manual still reads like documentation rather than a campaign
site.

**C — Full furniture.** B, plus everything Quarto will let CSS reach. This is
the "match bigpicture.eu closely" end. It is deliberately pushed past what I'd
recommend shipping, so the cost of the last 20% is visible.

## What fights the Quarto theme

Three separate categories — worth keeping apart, because only the third is a
real argument against going further.

### 1. Genuinely blocked inside the Quarto theme

- **Callout icons.** Quarto bakes its callout icons as background-image SVGs at
  fixed colours. They cannot be recoloured from CSS or SCSS; matching the pink
  icon language means shipping replacement SVG assets. Variant C fudges this
  with opacity and it still reads as "Quarto blue icon on a pink title".
- **Pill/stadium image masks.** The signature bigpicture.eu hero shape needs a
  known aspect ratio and an image that tolerates being clipped. Quarto content
  images are arbitrary screenshots and diagrams; a blanket `border-radius`
  mangles them. C approximates the shape with a rounded lavender *panel*
  instead, which is the honest limit without per-image markup.
- **The segmented colour rule** works, but only because C hangs it off
  `header#title-block-header::after`. Any page without a title block (the front
  page) doesn't get one. Real furniture needs a shortcode or an include.
- **Card chrome.** bigpicture.eu's thin-bordered image cards have no Quarto
  equivalent in this site's content — there's no listing page to hang them on.
  Out of reach until the content grows one.

### 2. Achievable, but only with `!important`

- **Navbar background.** `website.navbar.background: light` emits a utility
  class; overriding it from a variant needs `!important`. Shipping would set
  `background: white` in `_quarto.yml` instead and the `!important` disappears.
- **Footer background**, same story via `page-footer.background`.
- **Nav link colour**, same story.

None of these are theme resistance — they're artefacts of the variant being
*scoped*. See below.

### 3. Artefacts of prototyping, not of Quarto

This is the important caveat. Quarto compiles SCSS once per render, so
`scss:defaults` variables (`$primary`, `$link-color`, `$font-family-base`,
`$headings-color`, `$border-radius`) are **global and compile-time** — they
cannot be scoped to `body[data-proto="b"]`. To get three switchable variants out
of one render, this file overrides *rendered properties* instead of *setting
Bootstrap variables*.

That makes the prototype look harder and uglier than the real change would be.
Shipping any variant means deleting most of this file and writing perhaps 15
lines in `custom.scss`'s existing `scss:defaults` block. **Do not read the size
of this file as the cost of the restyle.** The friction list that matters is
category 1 only.

## Reverting

Delete `prototype/`, and from `_quarto.yml` remove the
`prototype/brand-variants.scss` theme entry and the `include-after-body` line.
Nothing else was touched.
