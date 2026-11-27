# Session State
**Updated:** 2026-11-27 09:35
**Chat:** bulkapparel-deals-check

## Currently Working On
Black Friday check is done and texted to Ben. Waiting for Cyber Monday: a one-time job on the Mac opens a session here on Mon Nov 30, 2026 at 9:07 am to rerun the BulkApparel deal check and text Ben the result.

## Done This Session
- Black Friday check (Nov 27): the Thanksgiving code GRATEFUL10 still works and takes 10% off any order under $1,000, with free shipping kept. At $1,000 and up nothing changed (bulk discount, codes refused). No separate Black Friday sale, 1717 prices unchanged. Findings in DEALS-2026-11-27.md, texted to Ben.
- Earlier: Nov 18 baseline in DEALS-2026-11.md; Black Friday and Cyber Monday reruns set up.

## Next Steps
### For Ben
- Nothing.
### Waiting on someone else
- Nothing.
### For Claude
- **Run the Cyber Monday check on Mon Nov 30, 2026.** It starts by itself at 9:07 am (or when the Mac next wakes). Follow BLACK-FRIDAY-CHECK.md: recheck BulkApparel, compare against Nov 18 and Black Friday (DEALS-2026-11-27.md), write DEALS-2026-11-30.md, commit, text Ben.

## Key Decisions / Context
- The Cyber Monday job is `com.benmartel.bulkapparel-cybermonday` in LaunchAgents; it runs `scrape/bf_job.py`, which opens a Remote Control session here with the task, and texts Ben if the session cannot start. Needs the Mac on, cmux and Chrome running.
- BulkApparel is not signed in in Chrome; checks run as a guest. Never order, sign up or enter payment.
- `scrape/site.py` drives Chrome through Apple Events. Cart page notes for Monday: the code box is `#formCouponDesktopInput` with button `#couponid`, the quantity box is `input.input-quantity.qty`, and the summary is `.new-cart-sidebar__container`. After applying a code over $250 the summary shows the old bulk line until the cart page is reloaded.
- GRATEFUL10 is billed as a Thanksgiving "today only" code; on Monday check first whether it still works.
- Pushing to main deploys the public site at bulkapparel.benmartel.com and the repo is public, so keep private details out of commits.
