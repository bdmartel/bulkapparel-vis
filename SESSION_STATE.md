# Session State
**Updated:** 2026-11-21 10:00
**Chat:** bulkapparel-deals-check

## Currently Working On
Waiting for Black Friday and Cyber Monday. One-time jobs on the Mac open a session here on Fri Nov 27 and Mon Nov 30, 2026 at 9:07 am; each reruns the BulkApparel deal check and texts Ben the result.

## Done This Session
- Nov 18 check: the 10% bulk discount ($1,000 and up) and free shipping ($79 and up, counted before discounts) apply together; code AUTUMN7 gives 7% but cannot be combined with the bulk discount. Findings in DEALS-2026-11.md, texted to Ben.
- Set the Black Friday and Cyber Monday reruns: instructions in BLACK-FRIDAY-CHECK.md, each started by a one-time scheduled job that removes itself after it runs.

## Next Steps
### For Ben
- Nothing.
### Waiting on someone else
- Nothing.
### For Claude
- **Run the Black Friday check on Fri Nov 27, 2026.** It starts by itself at 9:07 am (or when the Mac next wakes). Follow BLACK-FRIDAY-CHECK.md: recheck BulkApparel, write DEALS-2026-11-27.md, commit, text Ben.
- **Run the Cyber Monday check on Mon Nov 30, 2026.** Same routine, starts by itself at 9:07 am; compare against Nov 18 and Black Friday, write DEALS-2026-11-30.md, commit, text Ben.

## Key Decisions / Context
- The scheduled jobs are `com.benmartel.bulkapparel-blackfriday` and `-cybermonday` in LaunchAgents; each runs `scrape/bf_job.py`, which opens a Remote Control session here with the task, and texts Ben if the session cannot start. Needs the Mac on, cmux and Chrome running.
- BulkApparel is not signed in in Chrome; checks run as a guest. Never order, sign up or enter payment.
- `scrape/site.py` drives Chrome through Apple Events (the Chrome extension tools were missing on Nov 18).
- Pushed to GitHub on Nov 21, 2026 at Ben's tidy-up request. Pushing to main deploys the public site at bulkapparel.benmartel.com and the repo is public, so keep private details out of commits.
