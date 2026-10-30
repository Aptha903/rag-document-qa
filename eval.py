import json
from search import retrieve 
r = retrieve("What is a mask in NumPy?", k=1)
print(r)

K = 3

def is_hit(chunks, item):
    for c in chunks:
        same_src = item["source"] in str(c["source"])
        same_page = c["page"] == item["page"]
        has_kw = item["keyword"].lower() in c["text"].lower()
        if same_src and same_page and has_kw:
            return True
    return False

with open("eval_questions.json") as f:
    items = json.load(f)

hits = 0
for it in items:
    chunks = retrieve(it["q"], k=K)
    ok = is_hit(chunks, it)
    hits += ok
    print(("HIT  " if ok else "MISS ") + it["q"])

print(f"\nHit@{K}: {hits}/{len(items)} = {hits/len(items):.0%}")import json
from search import retrieve

K = 3

def unpack(r):
    # r may be a tuple like (score, dict) or (dict, score)
    if isinstance(r, (tuple, list)):
        for x in r:
            if isinstance(x, dict):
                return x
    return r

def get(d, names, default=""):
    for n in names:
        if n in d:
            return d[n]
    return default

def is_hit(results, item):
    for r in results:
        c = unpack(r)
        text = str(get(c, ["text", "chunk", "content"]))
        src = str(get(c, ["source", "file", "filename", "doc"]))
        page = get(c, ["page", "page_number", "page_no"], None)
        if (item["source"] in src
                and page == item["page"]
                and item["keyword"].lower() in text.lower()):
            return True
    return False

with open("eval_questions.json", encoding="utf-8") as f:
    items = json.load(f)

# Debug: show the keys of the first result
first = unpack(retrieve(items[0]["q"], k=1)[0])
print("KEYS:", list(first.keys()) if isinstance(first, dict) else type(first))

hits = 0
for it in items:
    results = retrieve(it["q"], k=K)
    ok = is_hit(results, it)
    hits += ok
    print(("HIT  " if ok else "MISS ") + it["q"])

print(f"\nHit@{K}: {hits}/{len(items)} = {hits/len(items):.0%}")