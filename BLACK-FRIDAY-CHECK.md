# Black Friday and Cyber Monday checks (run Fri Nov 27 and Mon Nov 30, 2026, by themselves)

Ben asked on Nov 18, 2026 for the BulkApparel deal check to be run again on Black Friday and again on Cyber Monday, each reported the same way: a text to himself. He should not have to do anything until that text arrives. Do not ask him anything first.

## What to do

1. Read `DEALS-2026-11.md` first, and on Cyber Monday also `DEALS-2026-11-27.md` (the Black Friday result). The first is the Nov 18 baseline (free shipping at $79, bulk tiers 5/7/10/12/14% at $250/$500/$1,000/$2,500/$5,000, code AUTUMN7 for 7%, 1717 white M at $6.74, colors $7.43).
2. Check [bulkapparel.com](https://www.bulkapparel.com) in Ben's Chrome, in your own tab, closed after. The Chrome extension tools may be missing; `python3 scrape/site.py` does the same job through Apple Events (`open URL` prints a tab id, then `text TAB`, `js TAB 'code'`, `go TAB URL`, `close TAB`). Look at:
   - the home page banner and any popup, for a Black Friday or Cyber Monday sale or code
   - `/build-black-friday-wishlist`, `/sales`, `/kickoff20`, `/shipping`, `/help` (the "Exclusions & Offer Limitations" part)
   - the Comfort Colors 1717 page: are today's prices lower than the baseline?
3. Cart test, same as Nov 18: add 160 white M 1717 shirts, read the order summary, then try any Black Friday code and AUTUMN7 at about $80, $256 and $1,078. Find out whether a Black Friday offer stacks with the bulk discount and with free shipping, and whether the $79 line or the tiers changed. Go to the checkout page but stop before any address or payment.
4. Never place an order, make an account, sign up for anything in his name or enter payment details. Empty the cart and close the tab when done.
5. Write `DEALS-2026-11-27.md` (Black Friday) or `DEALS-2026-11-30.md` (Cyber Monday) here in the same shape as the baseline, with a short "What changed" list at the top (since Nov 18, and on Monday since Friday too) and a source for each answer. Commit it. Do not push (pushing deploys the public site).
6. Text Ben the answer in two or three lines with `remind --text` set two minutes out (a text to himself, no approval step, no em dashes). Lead with the verdict: is today a better day to order than Nov 18 (and on Monday, than Black Friday), and what to use (code or bulk discount) by order size.
7. Update `SESSION_STATE.md` and the chat log.

If the site blocks the browser or Chrome is closed, open Chrome and try once more; if it still fails, text him that the check could not run and why.
