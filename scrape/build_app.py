"""Inline data/colors.json into app.template.html -> index.html (self-contained, file:// safe)."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tpl = open(os.path.join(ROOT, "app.template.html"), encoding="utf-8").read()
data = json.load(open(os.path.join(ROOT, "data", "colors.json"), encoding="utf-8"))
# item codes for the add to cart button (scrape/skus.json, read from the store page by clicking each color)
skp = os.path.join(ROOT, "scrape", "skus.json")
if os.path.exists(skp):
    sk = json.load(open(skp, encoding="utf-8"))
    data["meta"]["pid"] = sk["pid"]
    for c in data["colors"]:
        if c["name"] in sk["colors"]:
            c["sk"] = sk["colors"][c["name"]]   # size -> [item code, price]
blob = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
assert "/*__DATA__*/" in tpl, "template placeholder missing"
out = tpl.replace("/*__DATA__*/", blob)
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(out)
print("index.html", round(len(out) / 1024, 1), "KB |", data["meta"]["colors"], "colors,",
      data["meta"]["images"], "photos")
