# bulkapparel-vis

A single-page color browser for the Comfort Colors 1717 tee on BulkApparel. Built
because the store only shows one color at a time, so comparing 68 colors means 68
clicks. See `README.md` for the feature list and the scraper pipeline.

**Live at https://bulkapparel.benmartel.com** — served by nginx from the
DigitalOcean droplet `178.128.155.186` (same box as benmartel.com + invoice),
auto-deployed via GitHub Actions.

## Deploy — push to `main` → live

`.github/workflows/deploy.yml` SSHes as `deploy@178.128.155.186` and runs
`git pull origin main` in `/var/www/bulkapparel`. Mirrors the invoice pipeline.
Repo: `github.com/bdmartel/bulkapparel-vis` (public — required for the droplet's
unauthenticated `git pull`). DNS is the wildcard `*.benmartel.com` A record; SSL
via certbot (auto-renews). The GHA keypair is dedicated to this repo
(`gha-bulkapparel-deploy` in `/home/deploy/.ssh/authorized_keys`).

## Working rules

- `index.html` is **generated**. Edit `app.template.html`, then run
  `python3 scrape/build_app.py`. Never hand-edit `index.html`.
- The app must keep working from `file://` — no fetch of local JSON, no CDN, no
  build step at runtime. Data is inlined at build time.
- Vanilla JS only. Dark chrome, white photo tiles (a colored surround would bias
  color judgment, which is the whole point of the page).

## Traps worth remembering

- **Cloudflare**: the product page is behind a managed challenge. Only Playwright
  with a real browser profile gets through; the cleared cookie lives in
  `scrape/cfstate.json`. Images are not challenged but the CDN 429s above ~5 req/s.
- **`data-valcode` is a decoy.** The swatch color code does not match the on-model
  photo code (Black is `50` on the swatch, `51` in the photo library; some codes are
  alphanumeric, e.g. `c4`). Any mapping built from `data-valcode` silently attaches
  the wrong shirt to every name. Always derive the mapping by clicking swatches in
  `scrape/map_colors.py`.
- **The site's swatch hex is wrong for several dyes.** Sort, filter and chip colors
  come from the photographs, not from `data-clrcode`.
- **The flat colors (`hex` / `avg` in `data/colors.json`) mislead for telling near shades apart** (Nov 27, 2026).
  They make Moss look grayer than it is. To name a real shirt from a photo, compare against the model
  photos in `images/`: Moss is greener and more saturated, Sage is a low-saturation yellow-gray green,
  Hemp is darker and more yellow-olive. The neck labels carry no color name; narrow first to the colors
  tagged bought (the list lives on the droplet, see Tags), then compare model photos.

## Tags (Nov 27, 2026)

Ben asked: tag the colors he has bought, and let him tag any color one at a time or in bulk and filter by tag.
- **Select** (next to Filters) turns on picking: tap cards (shift-click for a range), All shown / None, type a
  tag, + Add tag or − Remove tag. One color: open it and use the tag row under its name (+ add tag, × removes).
- The Tags chips in the filters: one tap shows only colors with that tag, a second tap shows only colors
  without it ("not bought"), a third turns it off. Several chips: any of the shown tags.
- **Edit tags** (last chip in the Tags row, added Nov 27): tap it, then tap a tag to rename it. The new name goes on every
  color that has it; renaming to a name that already exists merges the two. The bought tag keeps its name (order dates hang on it).
- Tags are stored on the droplet in `/var/www/bulkapparel-data/tags.json` through `tags.php`, which only
  answers someone signed in with the shared benmartel.com sign-in (nginx sends just that one file to PHP).
  Anyone else, and `file://`, keeps tags in that browser only. The data is outside the repo on purpose:
  the repo and site are public, and what Ben bought is his business.
- `bought.json` next to it holds each bought color's order dates and counts (shown in the tag row). It was
  read from his BulkApparel order history on Nov 27, 2026 (three orders, Aug 1 to Oct 10, 17 colors of 1717).
  After a new order: read the order pages in his signed-in Chrome (bulkapparel.com/dashboard?page=orders),
  add the lines to bought.json and the "bought" tag to tags.json for each new color.

## Re-scraping

```
python3 scrape/map_colors.py && python3 scrape/fetch_images.py \
  && python3 scrape/build_data.py && python3 scrape/build_app.py
```

`fetch_images.py` is idempotent (manifest-backed) and prunes photos no longer in the
plan. `build_data.py` prints a QA report — investigate any color whose model shot and
garment shot disagree by more than lighting.

## Extending to another style

Everything is keyed to style `1717` in `scrape/map_colors.py` (the URL) and the
`c1717_` prefix in `scrape/fetch_images.py`. Those two constants plus the meta block
in `build_data.py` are the only style-specific pieces.
