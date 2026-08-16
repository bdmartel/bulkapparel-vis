# Session State
**Updated:** 2026-08-16 14:50
**Chat:** bulkapparel-color-browser

## Currently Working On
Done. Built and now deployed: https://bulkapparel.benmartel.com

## Done This Session
- Scraped all 68 Comfort Colors 1717 colors from BulkApparel (375 photos); fixed the two-numbering-systems trap by clicking every swatch in a real browser
- Built the single-file app: named grid, family filters, sorting, size slider, star shortlist, lightbox with zoom/slideshow, print contact sheet
- Deployed to bulkapparel.benmartel.com: GitHub repo (public, bdmartel/bulkapparel-vis), nginx vhost + certbot SSL on droplet 178.128.155.186, GitHub Actions auto-deploy on push (dedicated keypair)
- Verified live in a headless browser: 68 cards, all images load, lightbox works, zero errors
- Added row to claude.benmartel.com directory, verified behind gate, committed

## Next Steps
- Nothing pending. Push to main auto-deploys.

## Key Decisions / Context
- `index.html` is generated from `app.template.html` via `scrape/build_app.py` -- never hand-edit
- Repo made public to match the invoice deploy pattern (droplet pulls without auth)
- DNS was zero-work: wildcard `*.benmartel.com` already points at the droplet
- Site data quirks documented in CLAUDE.md: swatch codes ≠ photo codes, site hex wrong for several dyes
