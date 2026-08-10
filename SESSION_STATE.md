# Session State
**Updated:** 2026-08-09 21:20
**Chat:** bulkapparel-color-browser

## Currently Working On
Done. The color browser is built, tested and committed. `index.html` is open in Chrome.

## Done This Session
- Scraped all 68 Comfort Colors 1717 colors from BulkApparel (Cloudflare challenge cleared with Playwright)
- Downloaded 375 photos: 58 colors have on-model front/side/back, all 68 have flat garment front/angle/back
- Found and fixed a mapping trap: the swatch `data-valcode` is NOT the on-model photo code, so the first pass attached the wrong shirt to every name. Now derived by clicking each swatch and reading what the page swaps in.
- Built the single-file app: grid with names, color-family filters, hue/lightness/A-Z sorting, size slider, star shortlist, lightbox with zoom/pan/slideshow/keyboard nav, print contact sheet
- Verified every color name against its photo via labeled contact sheets; all 68 correct
- git init + first commit; added to PROJECTS.md

## Next Steps
- Nothing required. Possible additions if asked: publish a phone-friendly hosted copy, or extend the pipeline to another style number.

## Key Decisions / Context
- `index.html` is generated from `app.template.html` via `scrape/build_app.py` -- never hand-edit it
- Swatch chips, hue sort and family buckets come from the photographs, not the site's published hex (which is wrong for Peachy, Island Green, Neon Cantaloupe, Neon Violet, Neon Lemon)
- 10 colors have no on-model photo anywhere on BulkApparel; they show the garment shot tagged "NO MODEL PHOTO"
- Image CDN 429s above ~5 req/s, so the fetcher runs a token-bucket limiter with backoff
