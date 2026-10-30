import json, re
from search import retrieve

def mod(n):
    m = re.search(r"Mod\d", str(n)); return m.group() if m else ""

items = json.load(open("eval_questions.json", encoding="utf-8"))
for it in items:
    raw = retrieve(it["q"], k=50)
    rank = None
    for i, r in enumerate(raw, 1):
        c = r[1]
        if (mod(c["source"]) == mod(it["source"]) and c["page"] == it["page"]
                and it["keyword"].lower() in c["text"].lower()):
            rank = i
            break
    print(rank, "|", it["q"][:60])