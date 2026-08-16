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
