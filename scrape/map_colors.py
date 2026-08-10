"""Ground-truth scrape of the BulkApparel product page.

The swatch markup carries a vendor colour code that does NOT match the code used
by the on-model photo library, so the only reliable mapping is to drive the page:
click each swatch and read the gallery it swaps in. Writes scrape/gallery.json.
"""
import json, os, time, pathlib
from playwright.sync_api import sync_playwright

URL = ("https://www.bulkapparel.com/tshirts/"
       "comfort-colors-1717-garment-dyed-heavyweight-ringspun-short-sleeve-shirt")
HERE = pathlib.Path(__file__).parent
STATE = HERE / "cfstate.json"
OUT = HERE / "gallery.json"

SWATCHES = """() => {
  const seen = new Map();
  document.querySelectorAll('a.col[data-clrname]').forEach(a => {
    const n = a.dataset.clrname;
    if (seen.has(n)) return;
    const m = (a.dataset.mainImg || '').match(/\\/(\\d+)_f_fm\\.jpg/);
    seen.set(n, {name:n, hex:(a.dataset.clrcode||'').toLowerCase(),
                 code:a.dataset.valcode||'', pid:m?m[1]:null,
                 featured:+(a.dataset.featured||0), order:+(a.dataset.valc||0)});
  });
  return [...seen.values()];
}"""

GALLERY = """() => {
  const out = [];
  document.querySelectorAll('#mainimg picture img, .detail-thumb--image img').forEach(i => {
    out.push({src: i.getAttribute('src')||'', hr: i.dataset.highResoSrc||'',
              prev: i.dataset.previewDesktopSrc||'', alt: i.alt||''});
  });
  return out;
}"""

MAIN_ALT = "() => { const i = document.querySelector('#mainimg picture img'); return i ? i.alt : ''; }"
MAIN_SRC = "() => { const i = document.querySelector('#mainimg picture img'); return i ? (i.getAttribute('src')||'') : ''; }"

with sync_playwright() as p:
    b = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
    ctx = b.new_context(storage_state=str(STATE) if STATE.exists() else None,
                        viewport={"width": 1500, "height": 1000},
                        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                                   "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});")
    pg = ctx.new_page()
    pg.goto(URL, wait_until="domcontentloaded", timeout=90000)
    for _ in range(45):
        if "Just a moment" not in pg.title():
            break
        time.sleep(2)
    pg.wait_for_timeout(4000)
    ctx.storage_state(path=str(STATE))

    swatches = pg.evaluate(SWATCHES)
    print("colors in picker:", len(swatches))

    recs, failed = [], []
    for i, sw in enumerate(swatches):
        name = sw["name"]
        before = pg.evaluate(MAIN_SRC)
        ok = False
        n_anchor = pg.evaluate("n => document.querySelectorAll(`a.col[data-clrname=\"${n}\"]`).length", name)
        for k in range(n_anchor):
            pg.evaluate("([n,k]) => document.querySelectorAll(`a.col[data-clrname=\"${n}\"]`)[k].click()", [name, k])
            for _ in range(20):
                pg.wait_for_timeout(120)
                if pg.evaluate(MAIN_ALT) == name and pg.evaluate(MAIN_SRC) != before:
                    ok = True
                    break
            if ok:
                break
        pg.wait_for_timeout(250)
        g = pg.evaluate(GALLERY)
        if not ok and pg.evaluate(MAIN_ALT) != name:
            failed.append(name)
        recs.append({**sw, "gallery": g, "confirmed": ok or pg.evaluate(MAIN_ALT) == name})
        if i % 10 == 0:
            print(f"  {i+1}/{len(swatches)} {name}")

    OUT.write_text(json.dumps(recs, indent=1))
    print("saved", len(recs), "| unconfirmed:", failed)
    b.close()
