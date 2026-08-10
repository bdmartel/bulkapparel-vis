"""Build data/colors.json + images/thumb/* from the downloaded image set.

- 480px-wide JPEG thumbs for the grid (full-size files stay for the lightbox).
- Samples the real garment colour from the flat-front shot, so hue sorting and
  family bucketing use the photographed dye, not the site's swatch hex (which is
  flat-out wrong for several of the neon and pastel colours).
- QA: cross-checks the on-model photo against the garment photo and reports any
  colour whose two shots don't agree — that is what a bad name->image mapping
  looks like.
"""
import json, os, re, colorsys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG = os.path.join(ROOT, "images")
THUMB = os.path.join(IMG, "thumb")
DATA = os.path.join(ROOT, "data")
os.makedirs(THUMB, exist_ok=True)
os.makedirs(DATA, exist_ok=True)

colors = json.load(open(os.path.join(HERE, "gallery.json")))
views = json.load(open(os.path.join(HERE, "views.json")))

LABEL = {"model_front": "On model - front", "model_side": "On model - side",
         "model_back": "On model - back", "flat_front": "Garment - front",
         "flat_angle": "Garment - angle", "flat_back": "Garment - back",
         "flat_detail": "Garment - detail"}
ORDER = list(LABEL)

# Torso crops: the flat shots are a garment filling the frame, the model shots
# are a person centred on white, so the chest sits higher and narrower.
CROP = {"flat": (.28, .36, .72, .70), "model": (.38, .40, .62, .58)}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def thumb(name):
    src, dst = os.path.join(IMG, name), os.path.join(THUMB, name)
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        return
    im = Image.open(src).convert("RGB")
    w, h = im.size
    im.resize((480, round(h * 480 / w)), Image.LANCZOS).save(
        dst, "JPEG", quality=82, optimize=True, progressive=True)


def dominant(name, kind="flat", k=8):
    """Biggest colour cluster in a torso crop, ignoring the seamless backdrop.
    Beats a plain median, which gets dragged toward blown highlights on the
    neon and pastel dyes."""
    im = Image.open(os.path.join(IMG, name)).convert("RGB")
    w, h = im.size
    x0, y0, x1, y1 = CROP[kind]
    c = im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1))).resize((120, 120), Image.LANCZOS)
    q = c.quantize(colors=k, method=Image.MEDIANCUT)
    pal = q.getpalette()[:k * 3]
    for _, idx in sorted(q.getcolors(), reverse=True):
        r, g, b = pal[idx * 3:idx * 3 + 3]
        _, ll, ss = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        if ll > .96 and ss < .12:
            continue
        return r, g, b
    return 128, 128, 128


# Hue bucketing gets a handful of garment dyes wrong wherever the cut points sit
# (muted plums read grey, rust reads orange). Curate those by hand.
OVERRIDE = {
    "Espresso": "Brown", "Yam": "Brown",
    "Wine": "Purple", "Dusk": "Purple", "Berry": "Purple", "Orchid": "Purple",
    "Peachy": "Orange", "Terracotta": "Orange", "Neon Cantaloupe": "Orange",
    "Neon Red Orange": "Orange",
    "Blossom": "Pink", "Neon Lemon": "Yellow",
    "Island Green": "Green", "Chalky Mint": "Green",
    "Royal Caribe": "Blue", "Chambray": "Blue", "Sapphire": "Blue",
}


def family(r, g, b):
    hh, ll, ss = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    H, L, S = hh * 360, ll, ss
    if L >= .88 and S <= .45:
        return "White"
    if L <= .18:
        return "Black"
    if S <= .11:                       # near-neutral: let hue pick the flavour
        if 55 <= H <= 165:
            return "Green"             # sage, moss, bay
        if 16 <= H < 55:
            return "Neutral"           # khaki, sandstone
        if 165 < H <= 205:
            return "Teal"
        return "Grey"
    if H < 14 or H >= 344:
        return "Pink" if (L >= .70 and S >= .40) else "Red"
    if H < 36:
        return "Brown" if L < .35 else "Orange"
    if H < 70:
        return "Yellow"
    if H < 168:
        return "Green"
    if H < 202:
        return "Teal"
    if H < 248:
        return "Blue"
    if H < 292:
        return "Purple"
    return "Pink"


def dist(a, b):
    """Rough perceptual distance, weighted the way the eye weights RGB."""
    rm = (a[0] + b[0]) / 2
    dr, dg, db = a[0] - b[0], a[1] - b[1], a[2] - b[2]
    return ((2 + rm / 256) * dr * dr + 4 * dg * dg + (2 + (255 - rm) / 256) * db * db) ** .5


out, warn = [], []
for c in colors:
    s = slug(c["name"])
    vs = []
    for k in ORDER:
        fn = f"{s}__{k}.jpg"
        if os.path.exists(os.path.join(IMG, fn)):
            thumb(fn)
            vs.append({"k": k, "f": fn, "label": LABEL[k]})
    if not vs:
        warn.append(f"{c['name']}: no images at all")
        continue

    flat = f"{s}__flat_front.jpg"
    rgb = dominant(flat, "flat") if os.path.exists(os.path.join(IMG, flat)) else dominant(vs[0]["f"], "model")
    mf = f"{s}__model_front.jpg"
    if os.path.exists(os.path.join(IMG, mf)) and os.path.exists(os.path.join(IMG, flat)):
        d = dist(rgb, dominant(mf, "model"))
        if d > 120:
            warn.append(f"{c['name']}: model vs garment colour differ by {d:.0f} "
                        f"(garment #{'%02x%02x%02x' % rgb}, model #{'%02x%02x%02x' % dominant(mf, 'model')})")

    r, g, b = rgb
    hh, ll, ss = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    out.append({
        "name": c["name"], "slug": s, "hex": c["hex"], "code": c["code"], "pid": c["pid"],
        "alpha": views.get(c["name"], {}).get("alpha"), "order": c["order"],
        "featured": c["featured"], "avg": "#%02x%02x%02x" % (r, g, b),
        "h": round(hh * 360, 1), "l": round(ll, 4), "s": round(ss, 4),
        "family": OVERRIDE.get(c["name"], family(r, g, b)),
        "model": any(v["k"].startswith("model") for v in vs),
        "views": vs,
    })

meta = {
    "style": "1717", "brand": "Comfort Colors",
    "title": "Comfort Colors 1717 Garment Dyed Heavyweight Ringspun Short Sleeve Shirt",
    "source": ("https://www.bulkapparel.com/tshirts/"
               "comfort-colors-1717-garment-dyed-heavyweight-ringspun-short-sleeve-shirt"),
    "price": "6.78", "colors": len(out),
    "with_model": sum(1 for c in out if c["model"]),
    "images": sum(len(c["views"]) for c in out),
}
json.dump({"meta": meta, "colors": out}, open(os.path.join(DATA, "colors.json"), "w"), indent=1)

print(json.dumps(meta, indent=1))
from collections import Counter
print("families:", Counter(c["family"] for c in out).most_common())
print("thumbs:", len(os.listdir(THUMB)))
print("QA warnings:", len(warn))
for w in warn:
    print("  !", w)
