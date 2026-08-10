# Comfort Colors 1717 — every color, one page

BulkApparel only shows one color at a time. This is all 68 of them at once, with the
color name next to each photo, plus a grid / zoom / slideshow so you can actually
compare and choose.

**Open `index.html`** in a browser (double-click works — no server needed).

## What's in it

| | |
|---|---|
| Colors | 68 |
| On-model photos | 58 colors (front, side, back) |
| Garment photos | all 68 (front, angle, back, some detail) |
| Total photos | 375, downloaded locally at 1000–1200px |

10 colors have no on-model photo anywhere on BulkApparel (Bright Orange, Dusk,
Espresso, Hydrangea, Navy, Neon Cantaloupe, Neon Lemon, Neon Violet, Peachy,
Rose Quartz). Those fall back to the garment shot and are tagged **NO MODEL PHOTO**
in the grid.

## Using it

**Grid**
- **On model / Garment** — flips every card between the person and the flat garment
- **Sort** — by color (grouped into families, then hue), light→dark, A–Z, or the site's own order
- **Family chips** — White, Neutral, Grey, Black, Brown, Red, Orange, Yellow, Green, Teal, Blue, Purple, Pink
- **Size slider** — from 12-across contact sheet to 3-across detail
- **★** on any card builds a shortlist; **★ only** filters to it; **Copy ★ list** puts the names on the clipboard
- **Cmd-P** prints a clean 5-across contact sheet

**Slideshow** (click any card)
- `←` `→` next / previous color
- `↑` `↓` next / previous angle (front, side, back, garment…)
- `Z` or double-click to zoom, scroll to zoom, drag to pan, pinch on touch
- `Space` autoplay · `F` save · `Esc` back to grid
- The color strip at the bottom jumps straight to any color
- **Buy ↗** opens that exact color on BulkApparel

Shortlist, sort, size and family filters persist in the browser between visits.

## How the data was built

`scrape/` holds the whole pipeline. Re-run it in this order if the product changes:

```
python3 scrape/map_colors.py     # drive the real page, record color -> gallery mapping
python3 scrape/fetch_images.py   # download every photo the gallery declares
python3 scrape/build_data.py     # thumbnails + data/colors.json + QA report
python3 scrape/build_app.py      # inline the data into index.html
```

### Two things that make this non-obvious

**The site is behind a Cloudflare managed challenge**, so plain `curl` gets a 403.
`map_colors.py` drives a real Chromium via Playwright and reuses the cleared cookie
in `scrape/cfstate.json`. Images themselves are not challenged — they download over
plain HTTPS, but the CDN starts returning 429 above roughly 5 requests/second, so
`fetch_images.py` runs a token-bucket limiter with adaptive backoff.

**The swatch color code is not the photo code.** Each swatch carries
`data-valcode` (e.g. Black = `50`), but the on-model photo library uses a different,
sometimes alphanumeric code (Black = `51`, Island Green = `c4`). Guessing the URL
from `data-valcode` produces a gallery where every name is attached to the wrong
shirt. The only reliable mapping is to click each swatch and read what the page
actually swaps in — which is exactly what `map_colors.py` does, and it verifies the
swap by checking the main image's `alt` matches the color it clicked.

### Color swatches

The hex the site publishes per color is wrong for several dyes (it lists Peachy as a
burnt orange and Island Green as a pale sage; the photos show a dusty peach and a
jade). So the chip colors, the hue sort and the family buckets all come from the
photograph — the dominant color cluster in a torso crop of the flat garment shot,
ignoring the seamless backdrop. `build_data.py` also cross-checks the model shot
against the garment shot for every color and prints any that disagree; the remaining
warnings are lighting differences within the same hue, not mismatches.

## Layout

```
index.html            the app — open this (self-contained, data inlined)
app.template.html     source template; edit this, then run build_app.py
images/               full-size photos (1000–1200px)
images/thumb/         480px grid thumbnails
data/colors.json      color metadata + view manifest
scrape/               scraper pipeline + captured raw data
```

If `images/` ever goes missing, the app falls back to loading each photo from
bulkapparel.com, so the HTML still works on its own with a connection.
