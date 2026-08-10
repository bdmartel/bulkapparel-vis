"""Download every gallery photo the product page declares, per colour.

The plan is built from scrape/gallery.json (what the page actually swaps in when
each swatch is clicked) rather than guessed URL patterns. Stale entries left in
the DOM from the default colour are filtered out by matching the colour's own
alpha code / product id.

Rate limited: the CDN starts throwing 429s above roughly 5 req/s.
"""
import json, os, re, sys, threading, time, http.client
import concurrent.futures as cf

HOST = "www.bulkapparel.com"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG = os.path.join(ROOT, "images")
os.makedirs(IMG, exist_ok=True)

VIEWS = [("model_front", "On model - front"), ("model_side", "On model - side"),
         ("model_back", "On model - back"), ("flat_front", "Garment - front"),
         ("flat_angle", "Garment - angle"), ("flat_back", "Garment - back"),
         ("flat_detail", "Garment - detail")]
LABEL = dict(VIEWS)
RANK = {k: i for i, (k, _) in enumerate(VIEWS)}

ALPHA = re.compile(r"/image/alpha-colors/(?P<size>[a-z-]+)/c1717_(?P<v>sd_|bk_)?(?P<code>[0-9a-z]+)\.jpg")
FLAT = re.compile(r"/image/(?P<size>[a-z-]+)/(?P<pid>\d+)_(?P<v>[a-z]_)?fm\.jpg")
FLATV = {"f_": "flat_front", "": "flat_angle", "b_": "flat_back", "d_": "flat_detail"}
ALPHAV = {None: "model_front", "sd_": "model_side", "bk_": "model_back"}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def plan_for(c):
    """{view_key: [url, fallback_url]} using only entries that belong to this colour."""
    main = c["gallery"][0]["src"] if c["gallery"] else ""
    m = ALPHA.search(main)
    code = m.group("code") if (m and not m.group("v")) else None
    out = {}
    for e in c["gallery"]:
        for url in (e["hr"], e["prev"], e["src"]):
            if not url:
                continue
            a = ALPHA.search(url)
            if a:
                if code is None or a.group("code") != code:
                    continue
                key = ALPHAV[a.group("v")]
            else:
                f = FLAT.search(url)
                if not f or f.group("pid") != c["pid"]:
                    continue
                key = FLATV.get(f.group("v") or "")
                if not key:
                    continue
            hi = url.replace("/thumbnail/", "/high-reso/").replace("/thumbnail-m/", "/high-reso/") \
                    .replace("/fashion-wear/", "/high-reso/").replace("/fashion-wear-m/", "/high-reso/")
            lo = hi.replace("/high-reso/", "/fashion-wear/")
            out.setdefault(key, [hi, lo])
    return code, out


# ---- throttled fetching -------------------------------------------------
class Limiter:
    def __init__(self, rate):
        self.rate, self.next, self.lock = rate, time.monotonic(), threading.Lock()

    def wait(self):
        with self.lock:
            now = time.monotonic()
            self.next = max(self.next, now)
            t, self.next = self.next, self.next + 1.0 / self.rate
        d = t - time.monotonic()
        if d > 0:
            time.sleep(d)

    def slow(self):
        with self.lock:
            self.rate = max(0.7, self.rate * 0.6)
            self.next = time.monotonic() + 3.0
        return self.rate


lim = Limiter(4.0)
local = threading.local()


def get(path, tries=6):
    for a in range(tries):
        lim.wait()
        try:
            c = getattr(local, "c", None)
            if c is None:
                c = local.c = http.client.HTTPSConnection(HOST, timeout=30)
            c.request("GET", path, headers={"User-Agent": UA, "Referer": f"https://{HOST}/",
                                            "Accept": "image/*,*/*;q=0.8", "Connection": "keep-alive"})
            r = c.getresponse()
            body = r.read()
            if r.status == 200:
                return body
            if r.status == 404:
                return None
            print(f"  ! {r.status} {path} -> {lim.slow():.2f}/s", flush=True)
            time.sleep(2 * (a + 1))
        except Exception:
            try:
                local.c.close()
            except Exception:
                pass
            local.c = None
            time.sleep(1.5 * (a + 1))
    return None


colors = json.load(open(os.path.join(HERE, "gallery.json")))
manifest_path = os.path.join(HERE, "manifest.json")
manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else {}

jobs, meta = [], {}
for c in colors:
    code, p = plan_for(c)
    meta[c["name"]] = {"alpha": code, "views": sorted(p, key=lambda k: RANK[k])}
    s = slug(c["name"])
    for key, urls in p.items():
        jobs.append((f"{s}__{key}.jpg", urls))

print(f"{len(colors)} colors, {len(jobs)} images planned, "
      f"{sum(1 for v in meta.values() if v['alpha'])} with on-model photos")

lock = threading.Lock()
got, miss, skip = [], [], []


def run(job):
    fn, urls = job
    dest = os.path.join(IMG, fn)
    if manifest.get(fn) == urls[0] and os.path.exists(dest) and os.path.getsize(dest) > 2000:
        with lock:
            skip.append(fn)
        return
    for u in urls:
        body = get(u.split(HOST, 1)[-1] if HOST in u else u)
        if body and len(body) > 2000:
            with open(dest, "wb") as f:
                f.write(body)
            with lock:
                got.append(fn)
                manifest[fn] = urls[0]
                if len(got) % 40 == 0:
                    print(f"  fetched {len(got)}", flush=True)
            return
    with lock:
        miss.append(fn)


with cf.ThreadPoolExecutor(max_workers=3) as ex:
    list(ex.map(run, jobs))

# drop images that are no longer part of the plan
want = {fn for fn, _ in jobs}
for f in os.listdir(IMG):
    if f.endswith(".jpg") and f not in want:
        os.remove(os.path.join(IMG, f))
        t = os.path.join(IMG, "thumb", f)
        if os.path.exists(t):
            os.remove(t)
        manifest.pop(f, None)

json.dump(manifest, open(manifest_path, "w"), indent=1, sort_keys=True)
json.dump(meta, open(os.path.join(HERE, "views.json"), "w"), indent=1, sort_keys=True)
print(f"downloaded {len(got)} | cached {len(skip)} | missing {len(miss)}")
if miss:
    print("missing:", miss[:20])
