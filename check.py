import json, re

def mod(n):
    m = re.search(r"Mod\d", str(n))
    return m.group() if m else ""

chunks = json.load(open("chunks.json", encoding="utf-8"))
items = json.load(open("eval_questions.json", encoding="utf-8"))

for it in items:
    kw = it["keyword"].lower()
    m = mod(it["source"])
    on_page = [c for c in chunks if mod(c["source"]) == m and c["page"] == it["page"]]
    pages = sorted({c["page"] for c in chunks
                    if mod(c["source"]) == m and kw in c["text"].lower()})
    print(f'{m} p{it["page"]} "{it["keyword"]}": '
            f'chunks on page={len(on_page)}, keyword found on pages {pages}')