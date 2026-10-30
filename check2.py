import json, re

def mod(n):
    m = re.search(r"Mod\d", str(n))
    return m.group() if m else ""

chunks = json.load(open("chunks.json", encoding="utf-8"))
items = json.load(open("eval_questions.json", encoding="utf-8"))

nosrc = [c for c in chunks if "source" not in c]
print("total chunks:", len(chunks), "| without source:", len(nosrc))
if nosrc:
    print("example keys:", list(nosrc[0].keys()))

for it in items:
    kw = it["keyword"].lower()
    m = mod(it["source"])
    on_page = [c for c in chunks
                if mod(c.get("source")) == m and c.get("page") == it["page"]]
    pages = sorted({c.get("page") for c in chunks
                    if mod(c.get("source")) == m
                    and kw in c.get("text", "").lower()})
    print(f'{m} p{it["page"]} "{it["keyword"]}": '
        f'chunks on page={len(on_page)}, keyword found on pages {pages}')