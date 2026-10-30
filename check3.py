import json
from collections import Counter

chunks = json.load(open("chunks.json", encoding="utf-8"))

a = Counter(c["source"] for c in chunks if "source" in c)
b = Counter(c["file"] for c in chunks if "file" in c)

print("WITH source:")
for k, v in a.items():
    print("  ", v, k)
print("WITH file:")
for k, v in b.items():
    print("  ", v, k)