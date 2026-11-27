# Session State
**Updated:** 2026-11-27 15:10
**Chat:** bulkapparel-deals-check

## Currently Working On
Black Friday check is done and texted to Ben. Waiting for Cyber Monday: a one-time job on the Mac opens a session here on Mon Nov 30, 2026 at 9:07 am to rerun the BulkApparel deal check and text Ben the result.

## Done This Session
- Add to cart button on the color page (Nov 27): one in each color's tag row with a size picker, one in the Select bar. In Safari (his phone) it fills the BulkApparel cart and lands on the cart page; in Chrome on a computer the store drops such adds, so there it opens the store page on that color and size. A color tagged qty 2 adds two. Details in CLAUDE.md.
- Claude's own condition tags from Ben's floor photo (Nov 27): replace, worn but keeping, good, and check name on the close calls, each starting with "claude:" and drawn in blue so they stand apart from his. Ben's own tags were left alone. Which colors got which is on the page only (signed in), not in this public repo.
- Naming real shirts from photos (Nov 27): the neck labels carry no color name, so a shirt is named by narrowing to the colors tagged bought and comparing against the model photos. Edit tags (rename a tag everywhere) is live on the color page. Lesson in CLAUDE.md.
- Tags on the color page (Nov 27, from the ops session): the 17 colors Ben has bought are tagged bought, with order dates; Select for bulk tagging, a tag row on each color, Tags filter with only/not. Synced for him when signed in. Details in CLAUDE.md.
- Black Friday check (Nov 27): the Thanksgiving code GRATEFUL10 still works and takes 10% off any order under $1,000, with free shipping kept. At $1,000 and up nothing changed (bulk discount, codes refused). No separate Black Friday sale, 1717 prices unchanged. Findings in DEALS-2026-11-27.md, texted to Ben.
- Earlier: Nov 18 baseline in DEALS-2026-11.md; Black Friday and Cyber Monday reruns set up.

## Next Steps
### For Ben
- **Check four shirt names on the color page at bulkapparel.benmartel.com.** Claude named your shirts from the floor photo and tagged each one replace, worn but keeping, or good. Four were close calls between two similar shades, and those four carry the blue tag "claude: check name". Tap that tag in the Tags row to see them; if one is the wrong shade, tell Claude which and it will move the tags.
### Waiting on someone else
- Nothing.
### For Claude
- **Run the Cyber Monday check on Mon Nov 30, 2026.** It starts by itself at 9:07 am (or when the Mac next wakes). Follow BLACK-FRIDAY-CHECK.md: recheck BulkApparel, compare against Nov 18 and Black Friday (DEALS-2026-11-27.md), write DEALS-2026-11-30.md, commit, text Ben.

## Key Decisions / Context
- Safari on the Mac has a guest BulkApparel cart holding two Yam M from the button test (Nov 27); Safari cannot be scripted to empty it. Harmless, nothing ordered.
- The Cyber Monday job is `com.benmartel.bulkapparel-cybermonday` in LaunchAgents; it runs `scrape/bf_job.py`, which opens a Remote Control session here with the task, and texts Ben if the session cannot start. Needs the Mac on, cmux and Chrome running.
- BulkApparel is not signed in in Chrome; checks run as a guest. Never order, sign up or enter payment.
- `scrape/site.py` drives Chrome through Apple Events. Cart page notes for Monday: the code box is `#formCouponDesktopInput` with button `#couponid`, the quantity box is `input.input-quantity.qty`, and the summary is `.new-cart-sidebar__container`. After applying a code over $250 the summary shows the old bulk line until the cart page is reloaded.
- GRATEFUL10 is billed as a Thanksgiving "today only" code; on Monday check first whether it still works.
- Pushing to main deploys the public site at bulkapparel.benmartel.com and the repo is public, so keep private details out of commits.
