import json
import re
from search import retrieve

K = 5

def unpack(r):
    if isinstance(r, (tuple, list)):
        for x in r:
            if isinstance(x, dict):
                return x
    return r

def mod(name):
    m = re.search(r"Mod\d", str(name))
    return m.group() if m else ""

def is_hit(results, item):
    for r in results:
        c = unpack(r)
        if (mod(c.get("source")) == mod(item["source"])
                and c.get("page") == item["page"]
                and item["keyword"].lower() in c.get("text", "").lower()):
            return True
    return False

with open("eval_questions.json", encoding="utf-8") as f:
    items = json.load(f)

hits = 0
for it in items:
    raw = retrieve(it["q"], k=10)
    seen, results = set(), []
    for r in raw:
        c = unpack(r)
        key = (mod(c.get("source")), c.get("page"))
        if key in seen:
            continue
        seen.add(key)
        results.append(r)
    results = results[:K]

    ok = is_hit(results, it)
    hits += ok
    print(("HIT  " if ok else "MISS ") + it["q"])
    if not ok:
        print("   wanted:", mod(it["source"]), "p", it["page"], "|", it["keyword"])
        for r in results:
            c = unpack(r)
            print("   got:   ", mod(c.get("source")), "p", c.get("page"))

print(f"\nHit@{K}: {hits}/{len(items)} = {hits/len(items):.0%}")